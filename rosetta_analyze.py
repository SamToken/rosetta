#!/usr/bin/env python3
"""
Rosetta Analyze — Compréhension métier d'un contrôleur PHP legacy
==================================================================
Usage :
    python rosetta_analyze.py UserController.php
    python rosetta_analyze.py UserController.php --no-llm
    python rosetta_analyze.py UserController.php --output-dir ./output

Sorties :
    <Nom>_business_logic.json   IR enrichi avec flags et insights LLM
    <Nom>_business_doc.md       Documentation lisible par un PO
    <Nom>_flags.md              Zones à valider par un humain
"""

import argparse
import os
import sys
from pathlib import Path

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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rosetta Analyze — Extraire les règles métier d'un contrôleur PHP legacy"
    )
    parser.add_argument("php_file", help="Chemin vers le fichier contrôleur PHP")
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

    php_path = Path(args.php_file)
    if not php_path.exists():
        print(f"Erreur : fichier introuvable : {php_path}", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    stem = php_path.stem

    # ------------------------------------------------------------------
    # Étape 1 — Extraction PHP → IR (déterministe)
    # ------------------------------------------------------------------
    print(f"[1/4] Extraction PHP → IR : {php_path.name}")
    ir = extract_php(php_path)
    print(f"      ✓ {len(ir.entry_points)} actions, {len(ir.operations)} opérations")

    # ------------------------------------------------------------------
    # Étape 2 — Détection des flags (déterministe)
    # ------------------------------------------------------------------
    print("[2/4] Analyse des flags (déterministe)...")
    engine = FlagEngine()
    ir.flags = engine.analyze(ir)
    counts = {}
    for f in ir.flags:
        counts[f.type] = counts.get(f.type, 0) + 1
    detail = ", ".join(f"{n}×{t}" for t, n in sorted(counts.items()))
    print(f"      ✓ {len(ir.flags)} flags détectés ({detail})")

    # ------------------------------------------------------------------
    # Étape 3 — Enrichissement LLM (optionnel)
    # ------------------------------------------------------------------
    enricher = None
    if args.no_llm:
        print("[3/4] LLM désactivé (--no-llm)")
    elif not ir.flags:
        print("[3/4] Aucun flag à enrichir")
    else:
        print(f"[3/4] Enrichissement LLM ({args.model})...")
        try:
            from analyzers.llm_enricher import LLMEnricher
            enricher = LLMEnricher(model=args.model)
            ir = enricher.enrich(ir)
            print(f"      ✓ {len(ir.llm_insights)} insights générés")
        except ImportError as exc:
            print(f"      ⚠ LLM indisponible ({exc}) — mode déterministe uniquement")
        except Exception as exc:
            print(f"      ⚠ Erreur LLM : {exc} — mode déterministe uniquement")

    usage = enricher.usage if enricher else None

    # ------------------------------------------------------------------
    # Étape 4 — Génération des documents
    # ------------------------------------------------------------------
    print("[4/4] Génération des documents...")

    json_out = output_dir / f"{stem}_business_logic.json"
    json_out.write_text(ir.to_json(indent=2), encoding="utf-8")
    print(f"      → {json_out}")

    gen = BusinessDocGenerator()

    doc_out = output_dir / f"{stem}_business_doc.md"
    doc_out.write_text(gen.generate(ir, usage=usage, model=args.model), encoding="utf-8")
    print(f"      → {doc_out}")

    flags_out = output_dir / f"{stem}_flags.md"
    flags_out.write_text(gen.generate_flags_summary(ir), encoding="utf-8")
    print(f"      → {flags_out}")

    # ------------------------------------------------------------------
    # Résumé console
    # ------------------------------------------------------------------
    print()
    print("✅ Analyse terminée")
    print(f"📄 3 fichiers générés dans {output_dir}/")
    print(f"🤖 {len(ir.llm_insights)} flags enrichis / {usage.skipped_flags if usage else 0} skippés")
    if usage:
        from analyzers.llm_enricher import PRICING
        total = usage.total_cost(args.model)
        _, _, cache_economy = usage.costs(args.model)
        print(f"💰 Coût LLM estimé : ${total:.4f}")
        if usage.cache_read_tokens:
            print(f"⚡ Tokens cache : {usage.cache_read_tokens:,} (économie : ~${cache_economy:.4f})")
    else:
        print("💰 Coût LLM : $0.00 (--no-llm)")


if __name__ == "__main__":
    main()
