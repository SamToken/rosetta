"""Rosetta — Service d'audit PHP.

Contient la logique métier du pipeline d'analyse extraite de rosetta_analyze.py.
Le CLI (rosetta_analyze.py) devient un thin client qui orchestre ce service.

Architecture SOLID :
  SRP — AuditPipeline orchestre, ne génère pas de documents.
  DIP — dépend des Protocols (ExtractorProtocol, EnricherProtocol), pas des concrétions.
  OCP — ajouter un langage cible = nouvelle implémentation d'ExtractorProtocol.
"""
import concurrent.futures
import json
import shutil
import sys
import threading
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
    kb_trust_medium: bool = False  # medium court-circuite le LLM (sinon : contexte prompt)
    oracle_config_dir: Optional[Path] = None  # répertoire CSV + oracle_manifest.yaml
    git_root: Optional[Path] = None
    max_workers: int = 1  # >1 active le ThreadPoolExecutor en mode batch API

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
        self._config_crossref: Any = None  # ConfigCrossref si --oracle-config
        self._known_tokens: frozenset = frozenset()  # filtre O(1) pour RelationExtractor

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

        if opts.kb_root and opts.no_llm:
            self._p("⚠  kb_root ignoré — sans effet en mode --no-llm")

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

        try:
            from rosetta_kb import DEFAULT_KB_PATH
            from services.kb_service import KBService
            _kb_path = Path(DEFAULT_KB_PATH).expanduser().resolve()
            if _kb_path.exists():
                self._known_tokens = KBService(_kb_path).list_known_tokens()
                self._p(f"  [KB] {len(self._known_tokens)} token(s) indexés pour RelationExtractor")
        except Exception:
            pass

        if opts.oracle_config_dir:
            try:
                from analyzers.config_crossref import ConfigCrossref
                from extractors.oracle_config_extractor import (
                    MANIFEST_NAME, OracleConfigExtractor,
                )
                manifest = opts.oracle_config_dir / MANIFEST_NAME
                rows = OracleConfigExtractor(manifest).extract(opts.oracle_config_dir)
                self._config_crossref = ConfigCrossref(rows)
                self._p(
                    f"  [ORACLE] {len(self._config_crossref.config_rows)} ligne(s) "
                    f"config chargées depuis {opts.oracle_config_dir}"
                )
            except FileNotFoundError:
                self._p(
                    f"⚠  Manifeste Oracle introuvable dans {opts.oracle_config_dir} "
                    f"— lancer : rosetta_kb.py oracle-scaffold {opts.oracle_config_dir}"
                )
            except Exception as exc:
                self._p(f"⚠  Config Oracle ignorée : {exc}")

    def _print_kb_maturity(self) -> None:
        """Dashboard maturité KB — une ligne par domaine, objectif >60% high."""
        try:
            from rosetta_kb import DEFAULT_KB_PATH
            from services.kb_service import KBService
            kb_path = Path(DEFAULT_KB_PATH).expanduser().resolve()
            if not kb_path.exists():
                return
            rows = KBService(kb_path).maturity_by_domain()
        except Exception:
            return
        if not rows:
            return
        self._p("  📈 Maturité KB (objectif : >60% high) :")
        for domain, high, total in rows:
            pct = round(100.0 * high / total, 1) if total else 0.0
            mark = "✅" if pct > 60 else "⚠️ "
            self._p(f"     {mark} {domain:<30} {high}/{total} high ({pct}%)")

    # ── Résolution des entrées ────────────────────────────────────────────────

    def resolve_inputs(self, input_paths: list[Path]) -> list[Path]:
        """Résout une liste de chemins (fichiers ou répertoires) en liste de .php."""
        files: list[Path] = []
        for p in input_paths:
            if p.is_dir():
                files.extend(sorted(p.rglob("*.php")))
            elif p.is_file() and p.suffix.lower() == ".php":
                files.append(p)
        return files

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

    # ── Worker léger pour exécution parallèle ────────────────────────────────

    @classmethod
    def _from_parent(
        cls,
        parent: "AuditPipeline",
        progress: Callable[[str], None],
    ) -> "AuditPipeline":
        """Clone léger partageant les ressources lourdes (read-only) du parent."""
        worker: AuditPipeline = cls.__new__(cls)
        worker.options = parent.options
        worker._p = progress
        worker._call_graph = parent._call_graph      # read-only après setup()
        worker._kb_provider = parent._kb_provider  # read-only après setup()
        worker._kb_lookup = parent._kb_lookup      # read-only après setup()
        worker._known_tokens = parent._known_tokens  # frozenset immuable
        worker._telemetry = parent._telemetry      # partagé, protégé par Lock
        return worker

    # ── Analyse batch ─────────────────────────────────────────────────────────

    def run_batch(self, php_files: list[Path], output_dir: Path) -> BatchResult:
        """Analyse un lot de fichiers PHP, en parallèle si max_workers > 1."""
        details_dir = output_dir / "details"
        details_dir.mkdir(parents=True, exist_ok=True)

        n = len(php_files)
        workers = min(self.options.max_workers, n)
        self._p(f"\n🔍 Mode batch — {n} fichier(s) PHP")
        self._p(f"📂 Rapports détaillés → {details_dir}/")
        self._p(f"📊 Audit global      → {output_dir}/global_audit.md")
        if workers > 1:
            self._p(f"⚡ Parallélisme — {workers} workers")
        self._p("")

        t0 = time.perf_counter()
        results: list[SingleFileResult] = []

        if workers > 1:
            results = self._run_batch_parallel(php_files, details_dir, workers)
        else:
            for i, php_path in enumerate(php_files, 1):
                self._p(f"[{i}/{n}] {php_path.name}")
                results.append(self.run_single(php_path, details_dir))
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

    # ── Exécution parallèle ───────────────────────────────────────────────────

    def _run_batch_parallel(
        self,
        php_files: list[Path],
        details_dir: Path,
        workers: int,
    ) -> list[SingleFileResult]:
        """Lance run_single() en parallèle via ThreadPoolExecutor.

        Chaque fichier s'exécute dans un worker cloné du parent (ressources
        read-only partagées). Les logs sont bufférisés par fichier et émis
        en bloc à la complétion pour garder une sortie lisible.
        Les échecs individuels sont loggés sans interrompre les autres fichiers.
        """
        n = len(php_files)
        ordered: list[Optional[SingleFileResult]] = [None] * n
        completed = 0

        def _run_one(args: tuple[int, Path]) -> tuple[int, SingleFileResult, list[str]]:
            idx, php_path = args
            buf: list[str] = []

            # Signal immédiat visible dans l'UI avant le premier log buffé
            self._p(f"[{idx + 1}/{n}] {php_path.name} — analyse en cours…")

            # Heartbeat toutes les 30s pour que l'UI ne paraisse pas gelée
            t_start = time.perf_counter()
            _stop = threading.Event()

            def _beat() -> None:
                while not _stop.wait(30):
                    elapsed = int(time.perf_counter() - t_start)
                    self._p(f"   ⏳ [{idx + 1}/{n}] {php_path.name} — en cours ({elapsed}s)…")

            _hb = threading.Thread(target=_beat, daemon=True)
            _hb.start()
            try:
                worker = AuditPipeline._from_parent(self, buf.append)
                result = worker.run_single(php_path, details_dir)
            finally:
                _stop.set()
                _hb.join(timeout=1)

            return idx, result, buf

        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_meta = {
                executor.submit(_run_one, (i, p)): (i, p)
                for i, p in enumerate(php_files)
            }
            for fut in concurrent.futures.as_completed(future_to_meta):
                i, php_path = future_to_meta[fut]
                completed += 1
                try:
                    idx, result, buf = fut.result()
                    ordered[idx] = result
                    self._p(f"[{completed}/{n}] {php_path.name} ✓")
                    for line in buf:
                        self._p(f"  {line}")
                    self._p("")
                except Exception as exc:
                    self._p(f"[{completed}/{n}] ⚠ {php_path.name} — erreur : {exc}")

        return [r for r in ordered if r is not None]

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
                    kb_trust_medium=self.options.kb_trust_medium,
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

        kb_bugs = (
            self._kb_provider.bug_entries_for(ir.metadata.controller_name or "")
            if self._kb_provider else []
        )
        flags_out = output_dir / f"{stem}_flags.md"
        flags_out.write_text(gen.generate_flags_summary(ir, kb_bugs=kb_bugs), encoding="utf-8")

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

        # Étape 1b — Reachability : marquer le code mort suspecté (#4)
        # Nécessite un call graph global (--call-graph-root). Heuristique
        # conservatrice par nom ; les points d'entrée framework (routing *Action,
        # magic __*) sont exclus car appelés hors code.
        if self._call_graph:
            suspects = 0
            for ep in ir.entry_points:
                orig = ep.original_name or ep.name
                if orig.endswith("Action") or orig.startswith("__"):
                    continue
                ep.is_referenced = self._call_graph.is_referenced(orig)
                ep.dead_code_suspected = not ep.is_referenced
                suspects += ep.dead_code_suspected
            if suspects:
                self._p(f"        🧹 {suspects} méthode(s) suspectée(s) code mort (jamais appelée)")

        # Étape 2 — Flags (déterministe)
        self._p("  [2/4] Analyse des flags (déterministe)...")
        engine = FlagEngine()
        ir.flags = engine.analyze(ir)
        counts: dict[str, int] = {}
        for f in ir.flags:
            counts[f.type] = counts.get(f.type, 0) + 1
        detail = ", ".join(f"{n}×{t}" for t, n in sorted(counts.items()))
        self._p(f"        ✓ {len(ir.flags)} flags ({detail})")

        # Étape 2a — Croisement config Oracle (déterministe, avant LLM)
        if self._config_crossref:
            hits = self._config_crossref.annotate(ir)
            if hits:
                self._p(f"        🗄  {hits} flag(s) résolus par la config Oracle")

        # Étape 2b — Relations sémantiques (déterministe)
        if self._known_tokens:
            try:
                from analyzers.relation_extractor import RelationExtractor
                rel_extractor = RelationExtractor(kb_token_exists=self._known_tokens.__contains__)
                ir.relations = rel_extractor.extract(ir)
                if ir.relations:
                    self._p(f"        ✓ {len(ir.relations)} relation(s) extraite(s)")
            except Exception as exc:
                self._p(f"        ⚠ RelationExtractor : {exc}")

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
                    kb_trust_medium=opts.kb_trust_medium,
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
                        self._p(
                            f"     kb_hits : {enricher.kb_hits} · "
                            f"kb_medium_hits : {enricher.kb_medium_hits}"
                            + ("" if opts.kb_trust_medium
                               else " (injectés en contexte prompt, pas en remplacement)")
                        )
                        self._print_kb_maturity()
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

        kb_bugs = (
            self._kb_provider.bug_entries_for(ir.metadata.controller_name or "")
            if self._kb_provider else []
        )
        output_files["json"].write_text(ir.to_json(indent=2), encoding="utf-8")
        output_files["doc"].write_text(gen.generate(ir, usage=usage, model=opts.model), encoding="utf-8")
        output_files["flags"].write_text(gen.generate_flags_summary(ir, kb_bugs=kb_bugs), encoding="utf-8")
        output_files["brief"].write_text(gen.generate_po_brief(ir, kb_coverage=kb_coverage), encoding="utf-8")

        brief_rel = (
            output_files["brief"].relative_to(output_dir.parent)
            if output_dir.parent != output_dir
            else output_files["brief"]
        )
        self._p(f"        → {brief_rel}")

        # Étape 4b — Fiches KB (--kb-output-dir)
        if opts.kb_output_dir and (ir.llm_insights or ir.relations):
            try:
                from generators.kb_fiche_generator import KBFicheGenerator
                kb_gen = KBFicheGenerator(opts.kb_output_dir, domain=opts.kb_domain)
                created, updated, skipped = kb_gen.generate(ir, php_source_path=php_path)
                if ir.relations:
                    rc, ru, rs = kb_gen.generate_relations(ir, php_source_path=php_path)
                    created += rc
                    updated += ru
                    skipped += rs
                self._p(
                    f"  [KB] {created} fiche(s) créée(s), "
                    f"{updated} mise(s) à jour, {skipped} ignorée(s) (high)"
                )
            except Exception as exc:
                self._p(f"  ⚠ Génération fiches KB échouée : {exc}")

        return ir, usage, kb_coverage, output_files
