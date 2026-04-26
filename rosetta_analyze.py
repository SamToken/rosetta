#!/usr/bin/env python3
"""
Rosetta Analyze — Audit fonctionnel de contrôleurs PHP legacy
==============================================================
Usage :
    # Fichier unique
    python rosetta_analyze.py UserController.php
    python rosetta_analyze.py UserController.php --no-llm
    python rosetta_analyze.py UserController.php --output-dir ./output

    # Répertoire complet (mode batch)
    python rosetta_analyze.py ./controllers/
    python rosetta_analyze.py ./controllers/ --output-dir ./audit --model claude-sonnet-4-6

    # Avec archivage automatique
    python rosetta_analyze.py ./controllers/ --archive
    python rosetta_analyze.py ./controllers/ --archive --contexte "Avant MEP US-1234"

Sorties (fichier unique) :
    <Nom>_business_logic.json   IR enrichi avec flags et insights LLM
    <Nom>_business_doc.md       Documentation lisible par un PO
    <Nom>_flags.md              Zones à valider par un humain

Sorties (mode batch) :
    details/<Nom>_business_doc.md  Un rapport par contrôleur
    details/<Nom>_flags.md
    details/<Nom>_business_logic.json
    global_audit.md                Synthèse globale lisible par un PO

Archive (--archive) :
    ~/rosetta-memory/audits/<date>_<contrôleurs>/
    ~/rosetta-memory/index.md
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Assurer que le répertoire courant est dans le path
sys.path.insert(0, str(Path(__file__).parent))

# Charger .env si présent (sans dépendance externe)
_env_file = Path(__file__).parent / ".env"
if _env_file.exists():
    for _line in _env_file.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _key, _, _val = _line.partition("=")
            os.environ.setdefault(_key.strip(), _val.strip())

from extractors.php_extractor import extract_php
from analyzers.flag_engine import FlagEngine
from generators.business_doc_generator import BusinessDocGenerator
from ir.schema import IRSchema


# =============================================================================
# Archive — fonctions utilitaires
# =============================================================================

def generate_archive_name(controller_names: list[str]) -> str:
    date = datetime.now().strftime("%Y-%m-%d_%Hh%M")
    controllers = "-".join(controller_names[:3])
    if len(controller_names) > 3:
        controllers += f"-et{len(controller_names) - 3}autres"
    return f"{date}_{controllers}"


def _health_emoji(score: float) -> str:
    if score >= 70:
        return "🟢"
    if score >= 40:
        return "🟡"
    return "🔴"


def _format_cost(usage, model: str) -> str:
    if not usage:
        return "$0.00"
    try:
        return f"${usage.total_cost(model):.2f}"
    except Exception:
        return "$0.00"


def _update_index(memory_base: Path, meta: dict) -> None:
    """Ajoute une ligne dans ~/rosetta-memory/index.md."""
    index_path = memory_base / "index.md"

    dt = datetime.fromisoformat(meta["date"])
    date_str = dt.strftime("%Y-%m-%d %Hh%M")

    controllers = meta["controleurs"]
    controllers_str = ", ".join(controllers[:3])
    if len(controllers) > 3:
        controllers_str += f"... (+{len(controllers) - 3})"

    stats = meta["stats"]
    score = stats["score_sante_moyen"]
    emoji = _health_emoji(score)
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


def _do_archive(
    output_dir: Path,
    archive_name: str,
    meta: dict,
    memory_base: Optional[Path] = None,
) -> Path:
    """Copie output_dir dans ~/rosetta-memory/audits/<archive_name>/ et met à jour index.md."""
    if memory_base is None:
        memory_base = Path.home() / "rosetta-memory"

    archive_dir = memory_base / "audits" / archive_name
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Copier tous les fichiers générés
    for item in output_dir.iterdir():
        dest = archive_dir / item.name
        if item.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest, symlinks=True)
        else:
            shutil.copy2(item, dest)

    # Écrire meta.json
    (archive_dir / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Mettre à jour l'index
    _update_index(memory_base, meta)

    return archive_dir


# =============================================================================
# Analyse d'un fichier PHP
# =============================================================================

def _analyze_single(
    php_path: Path,
    output_dir: Path,
    no_llm: bool,
    model: str,
) -> tuple[IRSchema, Optional[object]]:
    """Analyse un fichier PHP et écrit les 3 fichiers de sortie dans output_dir."""
    stem = php_path.stem

    # ------------------------------------------------------------------
    # Étape 1 — Extraction PHP → IR (déterministe)
    # ------------------------------------------------------------------
    print(f"  [1/4] Extraction PHP → IR : {php_path.name}")
    ir = extract_php(php_path)
    print(f"        ✓ {len(ir.entry_points)} actions, {len(ir.operations)} opérations")

    # ------------------------------------------------------------------
    # Étape 2 — Détection des flags (déterministe)
    # ------------------------------------------------------------------
    print("  [2/4] Analyse des flags (déterministe)...")
    engine = FlagEngine()
    ir.flags = engine.analyze(ir)
    counts: dict[str, int] = {}
    for f in ir.flags:
        counts[f.type] = counts.get(f.type, 0) + 1
    detail = ", ".join(f"{n}×{t}" for t, n in sorted(counts.items()))
    print(f"        ✓ {len(ir.flags)} flags ({detail})")

    # ------------------------------------------------------------------
    # Étape 3 — Enrichissement LLM (optionnel)
    # ------------------------------------------------------------------
    enricher = None
    if no_llm:
        print("  [3/4] LLM désactivé (--no-llm)")
    elif not ir.flags:
        print("  [3/4] Aucun flag à enrichir")
    else:
        print(f"  [3/4] Enrichissement LLM ({model})...")
        try:
            from analyzers.llm_enricher import LLMEnricher
            enricher = LLMEnricher(model=model)
            ir = enricher.enrich(ir)
            print(f"        ✓ {len(ir.llm_insights)} insights générés")
        except ImportError as exc:
            print(f"        ⚠ LLM indisponible ({exc}) — mode déterministe uniquement")
        except Exception as exc:
            print(f"        ⚠ Erreur LLM : {exc} — mode déterministe uniquement")

    usage = enricher.usage if enricher else None

    # ------------------------------------------------------------------
    # Étape 4 — Génération des documents
    # ------------------------------------------------------------------
    print("  [4/4] Génération des documents...")
    output_dir.mkdir(parents=True, exist_ok=True)

    json_out = output_dir / f"{stem}_business_logic.json"
    json_out.write_text(ir.to_json(indent=2), encoding="utf-8")

    gen = BusinessDocGenerator()

    doc_out = output_dir / f"{stem}_business_doc.md"
    doc_out.write_text(gen.generate(ir, usage=usage, model=model), encoding="utf-8")

    flags_out = output_dir / f"{stem}_flags.md"
    flags_out.write_text(gen.generate_flags_summary(ir), encoding="utf-8")

    print(f"        → {doc_out.relative_to(output_dir.parent) if output_dir.parent != output_dir else doc_out}")

    return ir, usage


_ALL_RULE_TYPES = [
    "missing_branch", "magic_value", "security_risk", "unmapped_dep",
    "business_logic_unclear", "side_effect", "dynamic_session_key",
    "chained_api_call", "situation_coverage", "oceane_state_dependency",
    "module_execution_gap", "hardcoded_situation_code",
    "empty_catch", "strong_coupling", "chained_method_call",
]


def _print_debug_rules(irs: list) -> None:
    """Affiche le nombre de flags par règle pour chaque fichier analysé."""
    print("\n=== Debug règles ===")
    # Agréger sur tous les IR
    totals: dict[str, int] = {t: 0 for t in _ALL_RULE_TYPES}
    for ir in irs:
        for flag in ir.flags:
            key = str(flag.type)
            if key in totals:
                totals[key] += 1
            else:
                totals[key] = totals.get(key, 0) + 1
    for rule, count in totals.items():
        status = "✅" if count > 0 else "⬜"
        note = " — aucun pattern détecté" if count == 0 else ""
        print(f"  {status} {rule:<32}: {count} flag(s){note}")
    print()


def _print_usage_summary(usage, model: str) -> None:
    if not usage:
        print("💰 Coût LLM : $0.00 (--no-llm)")
        return
    total = usage.total_cost(model)
    _, _, cache_economy = usage.costs(model)
    print(f"💰 Coût LLM estimé : ${total:.4f}")
    if usage.cache_read_tokens:
        print(f"⚡ Tokens cache : {usage.cache_read_tokens:,} (économie : ~${cache_economy:.4f})")


# =============================================================================
# Point d'entrée
# =============================================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rosetta Analyze — Audit fonctionnel de contrôleurs PHP legacy"
    )
    parser.add_argument(
        "input",
        nargs="+",
        help="Fichier(s) PHP ou répertoire à analyser (récursif si répertoire)",
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Désactiver l'enrichissement LLM (mode déterministe uniquement)",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        metavar="DIR",
        help="Répertoire de sortie (défaut : répertoire courant)",
    )
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-6",
        help="Modèle LLM Anthropic à utiliser (défaut : claude-sonnet-4-6)",
    )
    parser.add_argument(
        "--archive",
        action="store_true",
        help="Archiver les résultats dans ~/rosetta-memory/",
    )
    parser.add_argument(
        "--contexte",
        default="",
        metavar="TEXT",
        help="Contexte de l'audit pour l'archivage (ex: 'Avant MEP US-1234')",
    )
    parser.add_argument(
        "--git-root",
        default=None,
        metavar="DIR",
        help="Racine Git pour générer des liens cliquables dans gaps_complets.md (ex: ./application/src)",
    )
    parser.add_argument(
        "--debug-rules",
        action="store_true",
        help="Afficher le détail de déclenchement de chaque règle de détection",
    )

    args = parser.parse_args()
    output_dir = Path(args.output_dir)

    # Résoudre les chemins d'entrée
    input_paths = [Path(p) for p in args.input]
    for p in input_paths:
        if not p.exists():
            print(f"Erreur : chemin introuvable : {p}", file=sys.stderr)
            sys.exit(1)

    # Un seul répertoire → mode batch par répertoire
    if len(input_paths) == 1 and input_paths[0].is_dir():
        input_path = input_paths[0]
    # Un seul fichier → mode fichier unique
    elif len(input_paths) == 1 and input_paths[0].is_file():
        input_path = input_paths[0]
    else:
        input_path = None  # plusieurs fichiers explicites

    # ======================================================================
    # Mode fichier unique (comportement original)
    # ======================================================================
    if input_path is not None and input_path.is_file():
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n📄 Analyse : {input_path.name}")
        ir, usage = _analyze_single(input_path, output_dir, args.no_llm, args.model)
        print()
        print("✅ Analyse terminée")
        print(f"📄 3 fichiers générés dans {output_dir}/")
        print(f"🤖 {len(ir.llm_insights)} flags enrichis / {usage.skipped_flags if usage else 0} skippés")
        _print_usage_summary(usage, args.model)
        if args.debug_rules:
            _print_debug_rules([ir])

        if args.archive:
            controller_names = [ir.metadata.controller_name]
            archive_name = generate_archive_name(controller_names)
            gap_count = len([f for f in ir.flags if f.type == "missing_branch"])
            dep_count = len([f for f in ir.flags if f.type == "unmapped_dep"])
            risk_count = len([f for f in ir.flags if f.type == "security_risk"])
            health = max(0.0, round(100.0 - risk_count * 3 - gap_count * 4 - dep_count * 2, 1))
            meta = {
                "date": datetime.now().isoformat(timespec="seconds"),
                "contexte": args.contexte,
                "controleurs": controller_names,
                "stats": {
                    "gaps_total": gap_count,
                    "services_tiers": dep_count,
                    "score_sante_moyen": health,
                    "cout_llm": _format_cost(usage, args.model),
                },
                "modele": "--no-llm" if args.no_llm else args.model,
                "mode": "--no-llm" if args.no_llm else "llm",
                "fichiers_analyses": [str(input_path)],
            }
            archive_dir = _do_archive(output_dir, archive_name, meta)
            print(f"📦 Archivé → {archive_dir}")

        return

    # ======================================================================
    # Mode batch (répertoire ou liste de fichiers explicites)
    # ======================================================================
    if input_path is not None:
        # répertoire → scan récursif
        php_files = sorted(input_path.rglob("*.php"))
        batch_label = str(input_path)
    else:
        # liste de fichiers explicites
        php_files = input_paths
        batch_label = ", ".join(p.name for p in input_paths)

    if not php_files:
        print(f"Erreur : aucun fichier .php trouvé dans {batch_label}", file=sys.stderr)
        sys.exit(1)

    details_dir = output_dir / "details"
    details_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n🔍 Mode batch — {len(php_files)} fichier(s) PHP : {batch_label}")
    print(f"📂 Rapports détaillés → {details_dir}/")
    print(f"📊 Audit global      → {output_dir}/global_audit.md")
    print()

    all_irs: list[IRSchema] = []
    all_usages: list[Optional[object]] = []
    total_insights = 0

    for i, php_path in enumerate(php_files, 1):
        print(f"[{i}/{len(php_files)}] {php_path.name}")
        ir, usage = _analyze_single(php_path, details_dir, args.no_llm, args.model)
        all_irs.append(ir)
        all_usages.append(usage)
        total_insights += len(ir.llm_insights)
        print()

    # ------------------------------------------------------------------
    # Agrégation & rapport global
    # ------------------------------------------------------------------
    print("📊 Agrégation des résultats...")
    from aggregators.business_aggregator import BusinessAggregator
    from generators.global_audit_generator import GlobalAuditGenerator

    aggregator = BusinessAggregator()
    insights = aggregator.aggregate(all_irs, all_usages)

    global_gen = GlobalAuditGenerator()
    global_audit = global_gen.generate(insights, model=args.model)

    global_out = output_dir / "global_audit.md"
    global_out.write_text(global_audit, encoding="utf-8")
    print(f"   ✓ {global_out}")

    gaps_out = details_dir / "gaps_complets.md"
    gaps_out.write_text(global_gen.generate_gaps_detail(insights, git_root=args.git_root), encoding="utf-8")
    print(f"   ✓ {gaps_out}")

    # ------------------------------------------------------------------
    # Résumé console
    # ------------------------------------------------------------------
    print()
    print("✅ Audit terminé")
    print(f"📁 {len(php_files)} contrôleur(s) analysé(s)")
    print(f"📂 Rapports détaillés : {details_dir}/")
    print(f"📊 Audit global       : {global_out}")
    print(f"🤖 {total_insights} insights LLM générés au total")
    print(f"🏥 Score de santé global : {insights.health_score}/100")
    print(f"🔴 CRITICAL_CORRUPTION : {insights.critical_count} flag(s) — corriger avant MEP")
    print(f"🟠 API_OVERLOAD        : {insights.overload_count} flag(s) — risque performance")
    print(f"🟡 LOGIC_GAP           : {insights.logic_gap_count} flag(s) — arbitrage PO")

    if any(u for u in all_usages):
        if insights.total_usage:
            _print_usage_summary(insights.total_usage, args.model)
    else:
        print("💰 Coût LLM : $0.00 (--no-llm)")
    if args.debug_rules:
        _print_debug_rules(all_irs)

    # ------------------------------------------------------------------
    # Archivage (--archive)
    # ------------------------------------------------------------------
    if args.archive:
        controller_names = [ir.metadata.controller_name for ir in all_irs]
        archive_name = generate_archive_name(controller_names)
        cost = _format_cost(insights.total_usage, args.model)
        meta = {
            "date": datetime.now().isoformat(timespec="seconds"),
            "contexte": args.contexte,
            "controleurs": controller_names,
            "stats": {
                "gaps_total": insights.gap_count,
                "services_tiers": insights.dep_count,
                "score_sante_moyen": insights.health_score,
                "cout_llm": cost,
            },
            "modele": "--no-llm" if args.no_llm else args.model,
            "mode": "--no-llm" if args.no_llm else "llm",
            "fichiers_analyses": [str(p) for p in php_files],

        }
        archive_dir = _do_archive(output_dir, archive_name, meta)
        print(f"📦 Archivé → {archive_dir}")


if __name__ == "__main__":
    main()
