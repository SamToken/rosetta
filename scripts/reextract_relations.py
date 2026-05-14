"""
Ré-extraction des relations sémantiques sur les IRs JSON existants.

Usage :
    .venv/bin/python3 scripts/reextract_relations.py [--dry-run] [--dir <path>]

Options :
    --dry-run   Affiche les résultats sans modifier les fichiers
    --dir       Répertoire racine des jobs API (défaut : $ROSETTA_API_OUTPUT ou
                ~/rosetta-data/api_jobs)
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Ajoute la racine du projet au PYTHONPATH pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from ir.schema import IRSchema
from analyzers.relation_extractor import RelationExtractor
from services.kb_service import KBService
from rosetta_kb import DEFAULT_KB_PATH


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--dir",
        default=os.environ.get("ROSETTA_API_OUTPUT", "~/rosetta-data/api_jobs"),
    )
    args = parser.parse_args()

    base = Path(args.dir).expanduser().resolve()
    if not base.exists():
        print(f"[ERR] Répertoire introuvable : {base}")
        sys.exit(1)

    # ── Charger les tokens connus depuis le KB YAML ───────────────────────────
    kb_path = Path(DEFAULT_KB_PATH).expanduser().resolve()
    if not kb_path.exists():
        print(f"[ERR] KB introuvable : {kb_path}")
        sys.exit(1)

    known_tokens = KBService(kb_path).list_known_tokens()
    print(f"[KB]  {len(known_tokens)} token(s) indexés")

    extractor = RelationExtractor(kb_token_exists=known_tokens.__contains__)

    # ── Scanner les IRs ───────────────────────────────────────────────────────
    json_files = sorted(base.rglob("*_business_logic.json"))
    print(f"[SRC] {len(json_files)} IR(s) trouvé(s) dans {base}")

    total_found = 0
    total_updated = 0
    total_already = 0
    errors = 0

    for json_path in json_files:
        try:
            ir = IRSchema.from_json(json_path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"  [ERR] {json_path.name} — lecture : {exc}")
            errors += 1
            continue

        if ir.relations:
            total_already += len(ir.relations)
            continue  # déjà extrait

        try:
            relations = extractor.extract(ir)
        except Exception as exc:
            print(f"  [ERR] {json_path.name} — extraction : {exc}")
            errors += 1
            continue

        if relations:
            total_found += len(relations)
            total_updated += 1
            label = json_path.name.replace("_business_logic.json", "")
            print(f"  [+{len(relations):2d}] {label}")
            if not args.dry_run:
                ir.relations = relations
                json_path.write_text(ir.to_json(indent=2), encoding="utf-8")
        # Pas de relations = pas de print (bruit inutile)

    # ── Résumé ────────────────────────────────────────────────────────────────
    mode = " (dry-run)" if args.dry_run else ""
    print()
    print(f"{'─'*50}")
    print(f"IRs traités     : {len(json_files)}")
    print(f"Déjà extraits   : {total_already} relations existantes ignorées")
    print(f"Mis à jour{mode} : {total_updated} fichier(s)")
    print(f"Nouvelles rels  : {total_found}")
    print(f"Erreurs         : {errors}")
    print(f"{'─'*50}")
    if args.dry_run:
        print("→ Relancer sans --dry-run pour écrire les fichiers.")


if __name__ == "__main__":
    main()
