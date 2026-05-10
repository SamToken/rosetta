#!/usr/bin/env python3
"""
Rosetta Analyze — CLI (thin client)
====================================
La logique métier est dans services/audit_service.py.
Ce fichier : parsing des arguments + affichage console + orchestration de haut niveau.

Usage :
    python rosetta_analyze.py MonService.php
    python rosetta_analyze.py MonService.php --no-llm
    python rosetta_analyze.py A.php B.php --bug-check --archive
    python rosetta_analyze.py ./controllers/ --output-dir ./audit
    python rosetta_analyze.py --from-json output/Foo_business_logic.json
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from services.audit_service import AuditOptions, AuditPipeline, do_archive, generate_archive_name


# =============================================================================
# Affichage console (SRP : uniquement le rendu)
# =============================================================================

_ALL_RULE_TYPES = [
    "missing_branch", "magic_value", "security_risk", "unmapped_dep",
    "business_logic_unclear", "side_effect", "dynamic_session_key",
    "chained_api_call", "situation_coverage", "external_state_dependency",
    "module_execution_gap", "hardcoded_situation_code",
    "empty_catch", "strong_coupling", "chained_method_call",
]


def _print_usage_summary(usage, model: str) -> None:
    if not usage:
        print("💰 Coût LLM : $0.00 (--no-llm)")
        return
    total = usage.total_cost(model)
    _, _, cache_economy = usage.costs(model)
    print(f"💰 Coût LLM estimé : ${total:.4f}")
    if usage.cache_read_tokens:
        print(f"⚡ Tokens cache : {usage.cache_read_tokens:,} (économie : ~${cache_economy:.4f})")


def _print_debug_rules(irs: list) -> None:
    print("\n=== Debug règles ===")
    totals: dict[str, int] = {t: 0 for t in _ALL_RULE_TYPES}
    for ir in irs:
        for flag in ir.flags:
            key = str(flag.type)
            totals[key] = totals.get(key, 0) + 1
    for rule, count in totals.items():
        status = "✅" if count > 0 else "⬜"
        note = " — aucun pattern détecté" if count == 0 else ""
        print(f"  {status} {rule:<32}: {count} flag(s){note}")
    print()


def _print_single_summary(result, model: str) -> None:
    from telemetry.performance_logger import PerformanceLogger
    ir = result.ir
    print(f"📄 4 fichiers générés")
    print(f"🤖 {len(ir.llm_insights)} flags enrichis / {result.usage.skipped_flags if result.usage else 0} skippés")
    if ir.bug_findings:
        crit = sum(1 for b in ir.bug_findings if b.severity.value == "critical")
        high = sum(1 for b in ir.bug_findings if b.severity.value == "high")
        print(f"🐛 {len(ir.bug_findings)} bug(s) techniques — 🔴{crit} critical / 🟠{high} high")
    _print_usage_summary(result.usage, model)
    from telemetry.performance_logger import AuditRun
    PerformanceLogger().print_roi_line(
        AuditRun(
            timestamp="",
            filename=result.php_path.name,
            file_size_lines=result.file_size_lines,
            processing_time_seconds=result.processing_time_seconds,
            model_used="--no-llm" if result.usage is None else model,
            status=result.status,
        )
    )


def _print_batch_summary(batch, model: str) -> None:
    ins = batch.insights
    print()
    print("✅ Audit terminé")
    print(f"📁 {len(batch.php_paths)} contrôleur(s) analysé(s)")
    print(f"📂 Rapports détaillés : {batch.gaps_path.parent}/")
    print(f"📊 Audit global       : {batch.global_audit_path}")
    print(f"🤖 {batch.total_insights} insights LLM générés au total")
    print(f"🏥 Score de santé global : {ins.health_score}/100")
    print(f"🔴 CRITICAL_CORRUPTION : {ins.critical_count} flag(s) — corriger avant MEP")
    print(f"🟠 API_OVERLOAD        : {ins.overload_count} flag(s) — risque performance")
    print(f"🟡 LOGIC_GAP           : {ins.logic_gap_count} flag(s) — arbitrage PO")

    if ins.total_usage:
        _print_usage_summary(ins.total_usage, model)
    else:
        print("💰 Coût LLM : $0.00 (--no-llm)")


def _build_single_meta(result, args) -> dict:
    ir = result.ir
    gap_count = len([f for f in ir.flags if f.type == "missing_branch"])
    dep_count = len([f for f in ir.flags if f.type == "unmapped_dep"])
    risk_count = len([f for f in ir.flags if f.type == "security_risk"])
    health = max(0.0, round(100.0 - risk_count * 3 - gap_count * 4 - dep_count * 2, 1))
    cost_str = f"${result.llm_cost_usd:.4f}" if result.llm_cost_usd else "$0.00"
    return {
        "date": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
        "contexte": args.contexte,
        "controleurs": [ir.metadata.controller_name],
        "stats": {
            "gaps_total": gap_count,
            "services_tiers": dep_count,
            "score_sante_moyen": health,
            "cout_llm": cost_str,
        },
        "modele": "--no-llm" if args.no_llm else args.model,
        "mode": "--no-llm" if args.no_llm else "llm",
        "fichiers_analyses": [str(result.php_path)],
    }


def _build_batch_meta(batch, args) -> dict:
    ins = batch.insights
    cost_str = f"${batch.total_cost_usd:.4f}" if batch.total_cost_usd else "$0.00"
    return {
        "date": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
        "contexte": args.contexte,
        "controleurs": [r.ir.metadata.controller_name for r in batch.results],
        "stats": {
            "gaps_total": ins.gap_count,
            "services_tiers": ins.dep_count,
            "score_sante_moyen": ins.health_score,
            "cout_llm": cost_str,
        },
        "modele": "--no-llm" if args.no_llm else args.model,
        "mode": "--no-llm" if args.no_llm else "llm",
        "fichiers_analyses": [str(p) for p in batch.php_paths],
    }


# =============================================================================
# Parsing des arguments
# =============================================================================

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Rosetta Analyze — Audit fonctionnel de contrôleurs PHP legacy"
    )
    p.add_argument("input", nargs="*", help="Fichier(s) PHP ou répertoire à analyser")
    p.add_argument("--no-llm", action="store_true", help="Mode déterministe uniquement ($0)")
    p.add_argument("--output-dir", default=".", metavar="DIR")
    p.add_argument("--model", default="claude-sonnet-4-6", help="Modèle LLM Anthropic")
    p.add_argument("--archive", action="store_true", help="Archiver dans ~/rosetta-memory/")
    p.add_argument("--contexte", default="", metavar="TEXT", help="Label pour l'archive")
    p.add_argument("--git-root", default=None, metavar="DIR")
    p.add_argument("--bug-check", action="store_true", help="Grille bugs techniques (13 catégories)")
    p.add_argument("--call-graph-root", default=None, metavar="DIR")
    p.add_argument("--rebuild-callgraph", action="store_true")
    p.add_argument(
        "--kb-root",
        default=str(Path("~/projects/rosetta/kb").expanduser()),
        metavar="DIR",
    )
    p.add_argument("--kb-output-dir", default=None, metavar="DIR")
    p.add_argument("--kb-domain", default=None, metavar="DOMAIN")
    p.add_argument("--from-json", default=None, metavar="JSON")
    p.add_argument("--retry-failed", action="store_true")
    p.add_argument("--debug-rules", action="store_true")
    p.add_argument(
        "--roi",
        action="store_true",
        help="Afficher le dashboard ROI (métriques cumulées)",
    )
    p.add_argument(
        "--api",
        default=None,
        metavar="URL",
        help="Mode Remote : déléguer l'analyse à l'API Rosetta (ex: http://localhost:8765)",
    )
    return p


# =============================================================================
# Mode Remote — helpers
# =============================================================================

def _collect_php_files(input_paths: list[Path]) -> list[Path]:
    """Résout une liste de chemins en fichiers .php (miroir de pipeline.resolve_inputs)."""
    if len(input_paths) == 1 and input_paths[0].is_dir():
        return sorted(input_paths[0].rglob("*.php"))
    return [p for p in input_paths if p.is_file() and p.suffix.lower() == ".php"]


def _print_remote_result(data: dict) -> None:
    """Affiche le résumé d'un job terminé en mode Remote."""
    if data.get("status") == "error":
        print(f"\n❌ Erreur lors de l'analyse : {data.get('error', '?')}", file=sys.stderr)
        return

    result: dict = data.get("result") or {}
    print()
    print("✅ Analyse terminée (mode Remote)")
    print(f"📁 {result.get('total_files', 0)} fichier(s) analysé(s)")
    print(f"🤖 {result.get('total_insights', 0)} insight(s) LLM générés")
    health = result.get("health_score")
    if health is not None:
        print(f"🏥 Score de santé : {health}/100")
    print(f"💰 Coût LLM estimé : ${result.get('total_cost_usd', 0.0):.4f}")
    print(f"⏱  Temps total    : {result.get('processing_time_seconds', 0.0):.1f}s")

    for f in result.get("files", []):
        icon = "✅" if f.get("status") in ("success", "no_llm") else "⚠️ "
        print(
            f"  {icon} {f.get('filename')} "
            f"— {f.get('insights_total', 0)} insights, "
            f"{f.get('flags_total', 0)} flags"
        )


def _propose_open_reports(output_dir: str) -> None:
    """Propose d'ouvrir le répertoire de sortie dans le gestionnaire de fichiers."""
    print(f"\n📂 Rapports disponibles → {output_dir}")
    try:
        answer = input("   Ouvrir le répertoire ? [o/N] ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return
    if answer in ("o", "oui", "y", "yes"):
        import shutil
        import subprocess
        opener = shutil.which("xdg-open") or shutil.which("open")
        if opener:
            subprocess.Popen([opener, output_dir])  # noqa: S603
        else:
            print(f"   (Ouvrir manuellement : {output_dir})")


def _main_remote(args) -> None:
    """Exécution en mode Remote — délègue à RosettaClient, pas de pipeline local."""
    if not args.input:
        print("Erreur : input requis en mode --api (fichier PHP ou répertoire)", file=sys.stderr)
        sys.exit(1)

    input_paths = [Path(p) for p in args.input]
    for p in input_paths:
        if not p.exists():
            print(f"Erreur : chemin introuvable : {p}", file=sys.stderr)
            sys.exit(1)

    php_files = _collect_php_files(input_paths)
    if not php_files:
        print("Erreur : aucun fichier .php trouvé dans les chemins spécifiés", file=sys.stderr)
        sys.exit(1)

    # Import local — httpx requis uniquement ici, jamais en mode local
    from api_client import RosettaClient  # noqa: PLC0415

    client = RosettaClient(args.api)
    data = client.run(
        php_files,
        no_llm=args.no_llm,
        model=args.model,
        bug_check=args.bug_check,
        kb_root=Path(args.kb_root).expanduser() if args.kb_root else None,
        call_graph_root=(
            Path(args.call_graph_root).expanduser() if args.call_graph_root else None
        ),
        contexte=args.contexte,
    )

    _print_remote_result(data)

    if data.get("status") == "success":
        output_dir = (data.get("result") or {}).get("output_dir")
        if output_dir:
            _propose_open_reports(output_dir)


# =============================================================================
# Point d'entrée
# =============================================================================

def main() -> None:
    args = _build_parser().parse_args()

    # ── Dashboard ROI seul ───────────────────────────────────────────────────
    if args.roi:
        from telemetry.performance_logger import PerformanceLogger
        PerformanceLogger().print_summary()
        return

    # ── Mode Remote (--api) — aucune dépendance locale requise ─────────────────
    if args.api:
        _main_remote(args)
        return

    output_dir = Path(args.output_dir)

    try:
        options = AuditOptions(
            no_llm=args.no_llm,
            model=args.model,
            bug_check=args.bug_check,
            call_graph_root=Path(args.call_graph_root).expanduser() if args.call_graph_root else None,
            rebuild_callgraph=args.rebuild_callgraph,
            kb_root=Path(args.kb_root).expanduser() if args.kb_root else None,
            kb_output_dir=Path(args.kb_output_dir).expanduser() if args.kb_output_dir else None,
            kb_domain=args.kb_domain,
            git_root=Path(args.git_root) if args.git_root else None,
        )
    except EnvironmentError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)

    pipeline = AuditPipeline(options)
    pipeline.setup()

    # ── Mode --from-json ─────────────────────────────────────────────────────
    if args.from_json:
        pipeline.regen_from_json(
            Path(args.from_json), output_dir, retry_failed=args.retry_failed
        )
        return

    if not args.input:
        print("Erreur : input requis (sauf avec --from-json ou --roi)", file=sys.stderr)
        sys.exit(1)

    input_paths = [Path(p) for p in args.input]
    for p in input_paths:
        if not p.exists():
            print(f"Erreur : chemin introuvable : {p}", file=sys.stderr)
            sys.exit(1)

    php_files = pipeline.resolve_inputs(input_paths)
    if not php_files:
        print(f"Erreur : aucun fichier .php trouvé dans les chemins spécifiés", file=sys.stderr)
        sys.exit(1)

    # Auto-inférer kb_domain depuis le nom du fichier unique
    if not options.kb_domain and len(php_files) == 1:
        options.kb_domain = php_files[0].stem

    # ── Fichier unique ───────────────────────────────────────────────────────
    if len(php_files) == 1:
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n📄 Analyse : {php_files[0].name}")
        result = pipeline.run_single(php_files[0], output_dir)
        print()
        print("✅ Analyse terminée")
        _print_single_summary(result, args.model)

        if args.archive:
            meta = _build_single_meta(result, args)
            archive_name = generate_archive_name(meta["controleurs"])
            archive_dir = do_archive(output_dir, archive_name, meta)
            print(f"📦 Archivé → {archive_dir}")

        if args.debug_rules:
            _print_debug_rules([result.ir])
        return

    # ── Mode batch ───────────────────────────────────────────────────────────
    batch = pipeline.run_batch(php_files, output_dir)
    _print_batch_summary(batch, args.model)

    if args.archive:
        meta = _build_batch_meta(batch, args)
        archive_name = generate_archive_name(meta["controleurs"])
        archive_dir = do_archive(output_dir, archive_name, meta)
        print(f"📦 Archivé → {archive_dir}")

    if args.debug_rules:
        _print_debug_rules([r.ir for r in batch.results])


if __name__ == "__main__":
    main()
