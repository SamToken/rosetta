#!/usr/bin/env python3
"""
kb_migrate_by_service.py — Réorganise le KB par nom de service PHP

Renomme les YAML de ~/rosetta-data/kb/ selon leur service PHP source.
Fusionne orchestra.yaml + diagnostic.yaml → OrchestraService.yaml.

Usage :
    python3 scripts/kb_migrate_by_service.py ~/rosetta-data/kb/
    python3 scripts/kb_migrate_by_service.py ~/rosetta-data/kb/ --dry-run
"""

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import yaml


MIGRATIONS = {
    # ancienne clé → nouvelle clé (None = conserver tel quel)
    "orchestra":                      "OrchestraService",
    "variables":                      "VariableService",
    "airele":                         "AireleService",
    "automatisation-evt":             "AutomatisationEvtService",
    "automatisation-dslam-isole-service": "AutomatisationDslamIsoleService",
    "automatisation":                 "AutomatisationService",
    # Garder tels quels (pas de service PHP direct identifié) :
    # "automatisation-dslam"   → garder
    # "aircom"                 → garder
    # "commun"                 → garder
    # "_global"                → garder (meta + pending)
}

# Fusionner diagnostic.yaml INTO OrchestraService.yaml
MERGES = {
    "diagnostic": "OrchestraService",
}


def _read(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def _merge_into(target: dict, source: dict) -> tuple[int, int]:
    """Fusionne source dans target. Retourne (ajoutés, ignorés car conflit)."""
    added = ignored = 0
    for section in ("codes", "regles", "schema"):
        target.setdefault(section, {})
        for k, v in source.get(section, {}).items():
            if k not in target[section]:
                target[section][k] = v
                added += 1
            else:
                ignored += 1
    target.setdefault("sql_artifacts", {"colonnes": {}, "vues": {}, "requetes": {}})
    for sub in ("colonnes", "vues", "requetes"):
        target["sql_artifacts"].setdefault(sub, {})
        for k, v in source.get("sql_artifacts", {}).get(sub, {}).items():
            if k not in target["sql_artifacts"][sub]:
                target["sql_artifacts"][sub][k] = v
                added += 1
            else:
                ignored += 1
    return added, ignored


def migrate(kb_dir: Path, dry_run: bool) -> None:
    print(f"\n{'[DRY-RUN] ' if dry_run else ''}Migration KB → organisation par service PHP")
    print(f"Répertoire : {kb_dir}\n")

    # 1. Renommages simples
    for old_name, new_name in MIGRATIONS.items():
        old_path = kb_dir / f"{old_name}.yaml"
        new_path = kb_dir / f"{new_name}.yaml"
        if not old_path.exists():
            print(f"  [SKIP]  {old_name}.yaml — introuvable")
            continue
        if new_path.exists():
            print(f"  [SKIP]  {old_name}.yaml → {new_name}.yaml — destination existe déjà")
            continue
        print(f"  [RENAME] {old_name}.yaml → {new_name}.yaml")
        if not dry_run:
            shutil.move(str(old_path), str(new_path))

    # 2. Fusions (ex: diagnostic → OrchestraService)
    for src_name, dst_name in MERGES.items():
        src_path = kb_dir / f"{src_name}.yaml"
        dst_name_resolved = MIGRATIONS.get(dst_name, dst_name)
        dst_path = kb_dir / f"{dst_name_resolved}.yaml"

        if not src_path.exists():
            print(f"  [SKIP]  fusion {src_name}.yaml — introuvable")
            continue

        src_data = _read(src_path)
        dst_data = _read(dst_path) if dst_path.exists() else {}

        added, ignored = _merge_into(dst_data, src_data)
        print(f"  [MERGE] {src_name}.yaml → {dst_name_resolved}.yaml "
              f"(+{added} entrées, {ignored} ignorées — déjà présentes)")

        if not dry_run:
            _write(dst_path, dst_data)
            src_path.unlink()
            print(f"          {src_name}.yaml supprimé")

    print()
    print("YAML restants :")
    for f in sorted(kb_dir.glob("*.yaml")):
        n = len(_read(f).get("codes", {})) + len(_read(f).get("regles", {}))
        print(f"  {f.name:<50} {n} entrées")

    if dry_run:
        print("\n(dry-run — aucun fichier modifié)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kb_dir", help="Répertoire du KB (ex: ~/rosetta-data/kb/)")
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans écrire")
    args = parser.parse_args()

    kb_dir = Path(args.kb_dir).expanduser().resolve()
    if not kb_dir.is_dir():
        print(f"Erreur : {kb_dir} n'est pas un répertoire", file=sys.stderr)
        sys.exit(1)

    migrate(kb_dir, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
