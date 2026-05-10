"""Rosetta — Service d'audit PHP.

Contient la logique métier du pipeline d'analyse extraite de rosetta_analyze.py.
Le CLI (rosetta_analyze.py) devient un thin client qui orchestre ce service.

Architecture SOLID :
  SRP — AuditPipeline orchestre, ne génère pas de documents.
  DIP — dépend des Protocols (ExtractorProtocol, EnricherProtocol), pas des concrétions.
  OCP — ajouter un langage cible = nouvelle implémentation d'ExtractorProtocol.
"""
import json
import shutil
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional, Protocol, runtime_checkable

# ---------------------------------------------------------------------------
# Protocols (contrats d'interface — Phase 3 API / tests unitaires)
# ---------------------------------------------------------------------------

@runtime_checkable
class ExtractorProtocol(Protocol):
    def extract(self, path: Path): ...  # → IRSchema


@runtime_checkable
class EnricherProtocol(Protocol):
    def enrich(self, ir: Any) -> Any: ...


# ---------------------------------------------------------------------------
# Options et résultats
# ---------------------------------------------------------------------------

@dataclass
class AuditOptions:
    """Paramètres d'exécution du pipeline. Aucune valeur hardcodée."""

    no_llm: bool = False
    model: str = "claude-sonnet-4-6"
    bug_check: bool = False
    call_graph_root: Optional[Path] = None
    rebuild_callgraph: bool = False
    kb_root: Optional[Path] = None
    kb_output_dir: Optional[Path] = None
    kb_domain: Optional[str] = None
    git_root: Optional[Path] = None

    def __post_init__(self) -> None:
        if not self.no_llm:
            from config import settings
            settings.validate_for_llm()  # lève EnvironmentError si ANTHROPIC_API_KEY absent


@dataclass
class SingleFileResult:
    """Résultat de l'analyse d'un fichier PHP."""

    php_path: Path
    ir: Any                              # IRSchema
    usage: Any                           # TokenUsage | None
    kb_coverage: Any                     # KBCoverageReport | None
    output_files: dict[str, Path]        # {"json", "doc", "flags", "brief"}
    processing_time_seconds: float
    file_size_lines: int
    llm_cost_usd: float

    @property
    def status(self) -> str:
        return "no_llm" if self.usage is None else "success"


@dataclass
class BatchResult:
    """Résultat de l'analyse d'un lot de fichiers PHP."""

    php_paths: list[Path]
    results: list[SingleFileResult]
    insights: Any                        # AggregatedInsights
    global_audit_path: Path
    gaps_path: Path
    processing_time_seconds: float

    @property
    def total_insights(self) -> int:
        return sum(len(r.ir.llm_insights) for r in self.results)

    @property
    def total_cost_usd(self) -> float:
        return sum(r.llm_cost_usd for r in self.results)


# ---------------------------------------------------------------------------
# Fonctions d'archivage (extraites de rosetta_analyze.py)
# ---------------------------------------------------------------------------

def generate_archive_name(controller_names: list[str]) -> str:
    date = datetime.now().strftime("%Y-%m-%d_%Hh%M")
    controllers = "-".join(controller_names[:3])
    if len(controller_names) > 3:
        controllers += f"-et{len(controller_names) - 3}autres"
    return f"{date}_{controllers}"


def _update_index(memory_base: Path, meta: dict) -> None:
    index_path = memory_base / "index.md"

    dt = datetime.fromisoformat(meta["date"])
    date_str = dt.strftime("%Y-%m-%d %Hh%M")
    controllers = meta["controleurs"]
    controllers_str = ", ".join(controllers[:3])
    if len(controllers) > 3:
        controllers_str += f"... (+{len(controllers) - 3})"
    stats = meta["stats"]
    score = stats["score_sante_moyen"]
    emoji = "🟢" if score >= 70 else ("🟡" if score >= 40 else "🔴")
    contexte = meta.get("contexte") or "—"

    new_row = (
        f"| {date_str} | {contexte} | {controllers_str} "
        f"| {stats['gaps_total']} | {emoji} {score} | {stats['cout_llm']} |"
    )
    header = (
        "# Rosetta Memory — Index des Audits\n\n"
        "| Date | Contexte | Contrôleurs | Gaps | Score | Coût |\n"
        "|------|----------|-------------|------|-------|------|\n"
    )
    if not index_path.exists():
        index_path.write_text(header + new_row + "\n", encoding="utf-8")
    else:
        existing = index_path.read_text(encoding="utf-8")
        index_path.write_text(existing.rstrip() + "\n" + new_row + "\n", encoding="utf-8")


def do_archive(output_dir: Path, archive_name: str, meta: dict, memory_base: Optional[Path] = None) -> Path:
    """Copie output_dir dans ~/rosetta-memory/audits/ et met à jour index.md."""
    from config import settings
    if memory_base is None:
        memory_base = settings.memory_base

    archive_dir = memory_base / "audits" / archive_name
    archive_dir.mkdir(parents=True, exist_ok=True)

    for item in output_dir.iterdir():
        dest = archive_dir / item.name
        if item.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest, symlinks=True)
        else:
            shutil.copy2(item, dest)

    (archive_dir / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    _update_index(memory_base, meta)
    return archive_dir


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------

class AuditPipeline:
    """Orchestre le pipeline d'audit PHP : extract → flags → LLM → generate.

    Args:
        options:  Paramètres d'exécution (aucune valeur hardcodée).
        progress: Callback de progression. ``print`` pour la CLI,
                  ``lambda _: None`` pour l'API ou les tests.
    """

    def __init__(
        self,
        options: AuditOptions,
        progress: Optional[Callable[[str], None]] = None,
    ) -> None:
        self.options = options
        self._p: Callable[[str], None] = progress if progress is not None else print

        # Ressources lourdes — initialisées par setup()
        self._call_graph: Any = None
        self._kb_provider: Any = None
        self._kb_lookup: Any = None

        from telemetry.performance_logger import PerformanceLogger
        self._telemetry = PerformanceLogger()

    # ── Initialisation ───────────────────────────────────────────────────────

    def setup(self) -> None:
        """Initialise les ressources optionnelles (call graph, KB). Idempotent."""
        opts = self.options

        if opts.call_graph_root and opts.call_graph_root.is_dir():
            cache_path = opts.call_graph_root / ".callgraph.json"
            self._p(f"\n🔗 Call Graph Index — scan de {opts.call_graph_root} …", )
            try:
                from analyzers.call_graph import CallGraphIndex
                self._call_graph = CallGraphIndex.build(
                    opts.call_graph_root,
                    cache_path=cache_path,
                    force_rebuild=opts.rebuild_callgraph,
                )
                self._p(f"{len(self._call_graph)} méthodes indexées ✓")
            except Exception as exc:
                self._p(f"⚠ Call graph ignoré : {exc}")

        if opts.kb_root and opts.kb_root.is_dir() and not opts.no_llm:
            self._p(f"\n📚 KB Context — chargement depuis {opts.kb_root} …", )
            try:
                from analyzers.kb_context import KBContextProvider
                self._kb_provider = KBContextProvider(opts.kb_root, verbose=False)
                self._p(f"{len(self._kb_provider)} fiche(s) KB ✓")
            except ImportError as exc:
                self._p(f"⚠ python-frontmatter manquant ({exc}) — KB ignorée")

        if not opts.no_llm:
            try:
                from rosetta_kb import lookup_for_enricher as _fn
                self._kb_lookup = _fn
                self._p("  [KB] YAML lookup activé — tokens connus résolus sans LLM")
            except Exception:
                pass

    # ── Résolution des entrées ────────────────────────────────────────────────

    def resolve_inputs(self, input_paths: list[Path]) -> list[Path]:
        """Résout une liste de chemins (fichiers ou répertoires) en liste de .php."""
        if len(input_paths) == 1 and input_paths[0].is_dir():
            return sorted(input_paths[0].rglob("*.php"))
        return [p for p in input_paths if p.is_file()]

    # ── Analyse fichier unique ────────────────────────────────────────────────

    def run_single(self, php_path: Path, output_dir: Path) -> SingleFileResult:
        """Analyse un fichier PHP et retourne un résultat structuré."""
        t0 = time.perf_counter()
        file_size_lines = php_path.read_text(encoding="utf-8", errors="replace").count("\n")

        ir, usage, kb_coverage, output_files = self._run_pipeline(php_path, output_dir)

        elapsed = round(time.perf_counter() - t0, 2)
        llm_cost = usage.total_cost(self.options.model) if usage else 0.0

        result = SingleFileResult(
            php_path=php_path,
            ir=ir,
            usage=usage,
            kb_coverage=kb_coverage,
            output_files=output_files,
            processing_time_seconds=elapsed,
            file_size_lines=file_size_lines,
            llm_cost_usd=llm_cost,
        )

        from telemetry.performance_logger import AuditRun
        self._telemetry.record(AuditRun(
            timestamp=datetime.utcnow().isoformat() + "Z",
            filename=php_path.name,
            file_size_lines=file_size_lines,
            processing_time_seconds=elapsed,
            model_used="--no-llm" if self.options.no_llm else self.options.model,
            status=result.status,
            flags_total=len(ir.flags),
            insights_total=len(ir.llm_insights),
            llm_cost_usd=llm_cost,
            kb_coverage_pct=kb_coverage.coverage_pct if kb_coverage else 0.0,
        ))

        return result

    # ── Analyse batch ─────────────────────────────────────────────────────────

    def run_batch(self, php_files: list[Path], output_dir: Path) -> BatchResult:
        """Analyse un lot de fichiers PHP et retourne les résultats agrégés."""
        details_dir = output_dir / "details"
        details_dir.mkdir(parents=True, exist_ok=True)

        self._p(f"\n🔍 Mode batch — {len(php_files)} fichier(s) PHP")
        self._p(f"📂 Rapports détaillés → {details_dir}/")
        self._p(f"📊 Audit global      → {output_dir}/global_audit.md\n")

        t0 = time.perf_counter()
        results: list[SingleFileResult] = []

        for i, php_path in enumerate(php_files, 1):
            self._p(f"[{i}/{len(php_files)}] {php_path.name}")
            result = self.run_single(php_path, details_dir)
            results.append(result)
            self._p("")

        # Agrégation
        self._p("📊 Agrégation des résultats...")
        from aggregators.business_aggregator import BusinessAggregator
        from generators.global_audit_generator import GlobalAuditGenerator

        all_irs = [r.ir for r in results]
        all_usages = [r.usage for r in results]

        aggregator = BusinessAggregator()
        insights = aggregator.aggregate(all_irs, all_usages)

        global_gen = GlobalAuditGenerator()
        global_out = output_dir / "global_audit.md"
        global_out.write_text(
            global_gen.generate(insights, model=self.options.model), encoding="utf-8"
        )
        self._p(f"   ✓ {global_out}")

        gaps_out = details_dir / "gaps_complets.md"
        gaps_out.write_text(
            global_gen.generate_gaps_detail(insights, git_root=self.options.git_root),
            encoding="utf-8",
        )
        self._p(f"   ✓ {gaps_out}")

        return BatchResult(
            php_paths=php_files,
            results=results,
            insights=insights,
            global_audit_path=global_out,
            gaps_path=gaps_out,
            processing_time_seconds=round(time.perf_counter() - t0, 2),
        )

    # ── Régénération depuis JSON ──────────────────────────────────────────────

    def regen_from_json(
        self,
        json_path: Path,
        output_dir: Path,
        retry_failed: bool = False,
    ) -> None:
        """Régénère les docs depuis un IR JSON existant (sans relancer l'extraction)."""
        from ir.schema import IRSchema
        from generators.business_doc_generator import BusinessDocGenerator

        if not json_path.exists():
            self._p(f"Erreur : JSON introuvable : {json_path}")
            sys.exit(1)

        self._p(f"\n📂 Chargement IR depuis {json_path.name} …")
        ir = IRSchema.from_json(json_path.read_text(encoding="utf-8"))

        failed_ids = {
            ins.flag_id for ins in ir.llm_insights
            if "[Erreur parsing LLM]" in (ins.business_rule or "")
        }
        self._p(f"   {len(ir.llm_insights)} insights chargés — {len(failed_ids)} en erreur de parsing")

        usage = None

        if retry_failed and failed_ids:
            self._p(f"\n🔁 Re-enrichissement LLM — {len(failed_ids)} flag(s) en erreur ({self.options.model})…")
            try:
                from analyzers.llm_enricher import LLMEnricher
                enricher = LLMEnricher(
                    model=self.options.model,
                    kb_provider=self._kb_provider,
                    kb_lookup=self._kb_lookup,
                )
                method_bodies: dict[str, str] = {}
                for ep in ir.entry_points:
                    if ep.raw_code:
                        body = ep.raw_code[:2500]
                        if ep.original_name:
                            method_bodies[ep.original_name] = body
                        if ep.name and ep.name != ep.original_name:
                            method_bodies[ep.name] = body

                kb_context = ""
                if self._kb_provider:
                    kb_context = self._kb_provider.context_for(ir.metadata.controller_name or "")

                insights_map = {ins.flag_id: ins for ins in ir.llm_insights}
                flags_map = {f.id: f for f in ir.flags}

                for flag_id in failed_ids:
                    flag = flags_map.get(flag_id)
                    if not flag:
                        continue
                    method_body = (
                        method_bodies.get(flag.method_original_name or "")
                        or method_bodies.get(flag.method_name or "")
                    )
                    try:
                        insights_map[flag_id] = enricher._ask_llm(flag, method_body, kb_context)
                    except Exception as e:
                        self._p(f"  ⚠ Échec re-enrichissement {flag_id} : {e}")

                ir.llm_insights = list(insights_map.values())
                still_failed = sum(
                    1 for ins in ir.llm_insights
                    if "[Erreur parsing LLM]" in (ins.business_rule or "")
                )
                self._p(f"   ✓ {len(failed_ids) - still_failed} insights récupérés")
                if still_failed:
                    self._p(f"   ⚠ {still_failed} toujours en erreur")
                usage = enricher.usage

            except ImportError as exc:
                self._p(f"   ⚠ LLM indisponible : {exc}")

        elif retry_failed and not failed_ids:
            self._p("   ✓ Aucun insight en erreur — rien à re-enrichir")

        self._p("\n📄 Génération des documents…")
        output_dir.mkdir(parents=True, exist_ok=True)
        stem = json_path.stem.replace("_business_logic", "")

        if retry_failed:
            updated_json = output_dir / f"{stem}_business_logic.json"
            updated_json.write_text(ir.to_json(indent=2), encoding="utf-8")

        gen = BusinessDocGenerator()
        doc_out = output_dir / f"{stem}_business_doc.md"
        doc_out.write_text(gen.generate(ir, usage=usage, model=self.options.model), encoding="utf-8")

        flags_out = output_dir / f"{stem}_flags.md"
        flags_out.write_text(gen.generate_flags_summary(ir), encoding="utf-8")

        brief_out = output_dir / f"{stem}_brief_po.md"
        brief_out.write_text(gen.generate_po_brief(ir), encoding="utf-8")

        self._p(f"   → {doc_out}")
        self._p(f"   → {flags_out}")
        self._p(f"   → {brief_out}")
        self._p("\n✅ Régénération terminée")

    # ── Pipeline interne ─────────────────────────────────────────────────────

    def _run_pipeline(
        self, php_path: Path, output_dir: Path
    ) -> tuple[Any, Any, Any, dict[str, Path]]:
        """Cœur du pipeline : extract → flags → LLM → generate → fichiers."""
        from extractors.php_extractor import extract_php
        from analyzers.flag_engine import FlagEngine
        from generators.business_doc_generator import BusinessDocGenerator

        opts = self.options
        stem = php_path.stem

        # Étape 1 — Extraction PHP → IR
        self._p(f"  [1/4] Extraction PHP → IR : {php_path.name}")
        ir = extract_php(php_path)
        self._p(f"        ✓ {len(ir.entry_points)} actions, {len(ir.operations)} opérations")

        # Étape 2 — Flags (déterministe)
        self._p("  [2/4] Analyse des flags (déterministe)...")
        engine = FlagEngine()
        ir.flags = engine.analyze(ir)
        counts: dict[str, int] = {}
        for f in ir.flags:
            counts[f.type] = counts.get(f.type, 0) + 1
        detail = ", ".join(f"{n}×{t}" for t, n in sorted(counts.items()))
        self._p(f"        ✓ {len(ir.flags)} flags ({detail})")

        # Étape 3 — Enrichissement LLM
        enricher = None
        if opts.no_llm:
            self._p("  [3/4] LLM désactivé (--no-llm)")
        elif not ir.flags:
            self._p("  [3/4] Aucun flag à enrichir")
        else:
            self._p(f"  [3/4] Enrichissement LLM ({opts.model})...")
            try:
                from analyzers.llm_enricher import LLMEnricher
                enricher = LLMEnricher(
                    model=opts.model,
                    kb_provider=self._kb_provider,
                    kb_lookup=self._kb_lookup,
                )
                ir = enricher.enrich(ir)
                self._p(f"        ✓ {len(ir.llm_insights)} insights générés")
                if enricher._kb_lookup:
                    cov = enricher.coverage
                    total_ev = cov.flags_kb_resolved + cov.flags_llm_needed
                    if total_ev:
                        self._p(
                            f"  📊 Couverture KB : {cov.coverage_pct}% "
                            f"({cov.flags_kb_resolved}/{total_ev} flags résolus sans LLM)"
                        )
                        if cov.top_candidates:
                            top3 = ", ".join(f"{t}({n}×)" for t, n in cov.top_candidates[:3])
                            self._p(f"     → À enrichir en KB : {top3}")
            except ImportError as exc:
                self._p(f"        ⚠ LLM indisponible ({exc}) — mode déterministe uniquement")
            except Exception as exc:
                self._p(f"        ⚠ Erreur LLM : {exc} — mode déterministe uniquement")

        usage = enricher.usage if enricher else None
        kb_coverage = enricher.coverage if enricher else None

        # Étape 3b — Grille de bugs (--bug-check)
        if opts.bug_check and not opts.no_llm:
            self._p(f"  [3b/4] Grille bugs techniques ({opts.model})...")
            try:
                from analyzers.bug_enricher import BugEnricher
                bug_enricher = BugEnricher(model=opts.model, kb_provider=self._kb_provider)
                php_source = php_path.read_text(encoding="utf-8", errors="replace")
                ir = bug_enricher.enrich(ir, php_source, call_graph=self._call_graph)
                bug_cost = bug_enricher.usage.total_cost(opts.model)
                crit = sum(1 for b in ir.bug_findings if b.severity.value == "critical")
                high = sum(1 for b in ir.bug_findings if b.severity.value == "high")
                self._p(
                    f"        ✓ {len(ir.bug_findings)} bug(s) "
                    f"— 🔴{crit} critical / 🟠{high} high | ~${bug_cost:.4f}"
                )
            except Exception as exc:
                self._p(f"        ⚠ Grille bugs échouée : {exc}")
        elif opts.bug_check and opts.no_llm:
            self._p("  [3b/4] Grille bugs désactivée (--no-llm)")

        # Étape 4 — Génération des documents
        self._p("  [4/4] Génération des documents...")
        output_dir.mkdir(parents=True, exist_ok=True)

        gen = BusinessDocGenerator()
        output_files: dict[str, Path] = {
            "json":  output_dir / f"{stem}_business_logic.json",
            "doc":   output_dir / f"{stem}_business_doc.md",
            "flags": output_dir / f"{stem}_flags.md",
            "brief": output_dir / f"{stem}_brief_po.md",
        }

        output_files["json"].write_text(ir.to_json(indent=2), encoding="utf-8")
        output_files["doc"].write_text(gen.generate(ir, usage=usage, model=opts.model), encoding="utf-8")
        output_files["flags"].write_text(gen.generate_flags_summary(ir), encoding="utf-8")
        output_files["brief"].write_text(gen.generate_po_brief(ir, kb_coverage=kb_coverage), encoding="utf-8")

        brief_rel = (
            output_files["brief"].relative_to(output_dir.parent)
            if output_dir.parent != output_dir
            else output_files["brief"]
        )
        self._p(f"        → {brief_rel}")

        # Étape 4b — Fiches KB (--kb-output-dir)
        if opts.kb_output_dir and ir.llm_insights:
            try:
                from generators.kb_fiche_generator import KBFicheGenerator
                kb_gen = KBFicheGenerator(opts.kb_output_dir, domain=opts.kb_domain)
                created, updated, skipped = kb_gen.generate(ir, php_source_path=php_path)
                self._p(
                    f"  [KB] {created} fiche(s) créée(s), "
                    f"{updated} mise(s) à jour, {skipped} ignorée(s) (high)"
                )
            except Exception as exc:
                self._p(f"  ⚠ Génération fiches KB échouée : {exc}")

        return ir, usage, kb_coverage, output_files
