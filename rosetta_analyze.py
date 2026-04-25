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

Sorties (fichier unique) :
    <Nom>_business_logic.json   IR enrichi avec flags et insights LLM
    <Nom>_business_doc.md       Documentation lisible par un PO
    <Nom>_flags.md              Zones à valider par un humain

Sorties (mode batch) :
    details/<Nom>_business_doc.md  Un rapport par contrôleur
    details/<Nom>_flags.md
    details/<Nom>_business_logic.json
    global_audit.md                Synthèse globale lisible par un PO
"""

import argparse
import os
import sys
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


def _print_usage_summary(usage, model: str) -> None:
    if not usage:
        print("💰 Coût LLM : $0.00 (--no-llm)")
        return
    from analyzers.llm_enricher import PRICING
    total = usage.total_cost(model)
    _, _, cache_economy = usage.costs(model)
    print(f"💰 Coût LLM estimé : ${total:.4f}")
    if usage.cache_read_tokens:
        print(f"⚡ Tokens cache : {usage.cache_read_tokens:,} (économie : ~${cache_economy:.4f})")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rosetta Analyze — Audit fonctionnel de contrôleurs PHP legacy"
    )
    parser.add_argument(
        "input",
        help="Fichier PHP ou répertoire à analyser (récursif si répertoire)",
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

    args = parser.parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    if not input_path.exists():
        print(f"Erreur : chemin introuvable : {input_path}", file=sys.stderr)
        sys.exit(1)

    # ======================================================================
    # Mode fichier unique (comportement original)
    # ======================================================================
    if input_path.is_file():
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n📄 Analyse : {input_path.name}")
        ir, usage = _analyze_single(input_path, output_dir, args.no_llm, args.model)
        print()
        print("✅ Analyse terminée")
        print(f"📄 3 fichiers générés dans {output_dir}/")
        print(f"🤖 {len(ir.llm_insights)} flags enrichis / {usage.skipped_flags if usage else 0} skippés")
        _print_usage_summary(usage, args.model)
        return

    # ======================================================================
    # Mode batch (répertoire)
    # ======================================================================
    php_files = sorted(input_path.rglob("*.php"))
    if not php_files:
        print(f"Erreur : aucun fichier .php trouvé dans {input_path}", file=sys.stderr)
        sys.exit(1)

    details_dir = output_dir / "details"
    details_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n🔍 Mode batch — {len(php_files)} fichier(s) PHP détecté(s) dans {input_path}")
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
    gaps_out.write_text(global_gen.generate_gaps_detail(insights), encoding="utf-8")
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
    print(f"⚠️  {insights.gap_count} gap(s) de logique à arbitrer")

    if any(u for u in all_usages):
        # Résumé coût agrégé
        if insights.total_usage:
            _print_usage_summary(insights.total_usage, args.model)
    else:
        print("💰 Coût LLM : $0.00 (--no-llm)")


if __name__ == "__main__":
    main()
