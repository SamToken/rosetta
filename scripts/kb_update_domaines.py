#!/usr/bin/env python3
"""
kb_update_domaines.py — Met à jour kb_domaine dans les frontmatter des fiches MD

Aligne les fiches rosetta/kb/<dossier>/*.md sur le nom PascalCase du service PHP.

Usage :
    python3 scripts/kb_update_domaines.py ~/projects/rosetta/kb/
    python3 scripts/kb_update_domaines.py ~/projects/rosetta/kb/ --dry-run
"""

import argparse
import re
import sys
from pathlib import Path

# Mapping dossier → nom PascalCase du service PHP
DOMAIN_MAP = {
    "config-scenario":      "ConfigScenarioService",
    "orchestra":            "OrchestraService",
    "variable-service":     "VariableService",
    "airele":               "AireleService",
    "enrichissement-alarmes": "AdminEnrichissementAlarmesController",
}


def update_frontmatter_domaine(text: str, new_domaine: str) -> tuple[str, bool]:
    """Remplace kb_domaine dans le frontmatter YAML. Retourne (texte, modifié)."""
    # Retirer le BOM si présent
    if text.startswith("﻿"):
        text = text[1:]

    # Localiser le bloc frontmatter (entre les deux ---)
    pattern = re.compile(r"^(---\n)(.*?)(---\n)", re.DOTALL)
    m = pattern.match(text)
    if not m:
        return text, False

    front = m.group(2)
    old_domaine_match = re.search(r'^kb_domaine:\s*(.+)$', front, re.MULTILINE)
    if not old_domaine_match:
        return text, False

    old_domaine = old_domaine_match.group(1).strip().strip('"')
    if old_domaine == new_domaine:
        return text, False

    new_front = re.sub(
        r'^(kb_domaine:\s*)(.+)$',
        f'\\g<1>{new_domaine}',
        front,
        flags=re.MULTILINE,
    )
    new_text = m.group(1) + new_front + m.group(3) + text[m.end():]
    return new_text, True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kb_dir", help="Répertoire racine des fiches KB (ex: ~/projects/rosetta/kb/)")
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans écrire")
    args = parser.parse_args()

    kb_dir = Path(args.kb_dir).expanduser().resolve()
    if not kb_dir.is_dir():
        print(f"Erreur : {kb_dir} n'est pas un répertoire", file=sys.stderr)
        sys.exit(1)

    updated = skipped = unchanged = 0

    for subdir, new_domaine in DOMAIN_MAP.items():
        subdir_path = kb_dir / subdir
        if not subdir_path.is_dir():
            print(f"  [SKIP] {subdir}/ — dossier introuvable")
            skipped += 1
            continue

        md_files = sorted(subdir_path.glob("*.md"))
        if not md_files:
            print(f"  [SKIP] {subdir}/ — aucun .md")
            continue

        for md_path in md_files:
            text = md_path.read_text(encoding="utf-8-sig")
            new_text, changed = update_frontmatter_domaine(text, new_domaine)
            if changed:
                print(f"  [UPDATE] {subdir}/{md_path.name}  kb_domaine → {new_domaine}")
                if not args.dry_run:
                    md_path.write_text(new_text, encoding="utf-8")
                updated += 1
            else:
                unchanged += 1

    print()
    print(f"Résultat : {updated} mise(s) à jour, {unchanged} déjà à jour, {skipped} dossier(s) ignoré(s)")
    if args.dry_run:
        print("(dry-run — aucun fichier modifié)")


if __name__ == "__main__":
    main()
