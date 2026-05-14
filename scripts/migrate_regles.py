#!/usr/bin/env python3
"""
Rosetta — Migration kb_type: regle → regles_metier / bugs_connus / observations

Usage :
    python3 scripts/migrate_regles.py [--kb-dir ~/rosetta-data/kb/] [--dry-run]

Ce script est IDEMPOTENT : si une entrée existe déjà dans la section cible,
elle n'est pas dupliquée.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Heuristique de classification
# ---------------------------------------------------------------------------

_BUG_LABEL_MARKERS = [
    "[bug]", "bug —", "bug actif", "bug critique", "bug moyen",
    "bug important", "bug mineur", "mort", "dead_code", "dead code",
    "incorrect", "malform", "doublon", "collision", "fuite", "leak",
    "crash", "exception", "null_deref", "null deref",
    "fallthrough", "fall-through",
    "array_unchecked", "uninit", "state_mutation",
    "strpos", "foreach_null",
]

_BUG_NOM_MARKERS = [
    "bug_", "_bug_",
    "null_deref", "null_comparison", "split_missing",
    "uninit_", "state_mutation", "strpos_",
    "foreach_null", "array_unchecked", "dead_code",
    "false_index", "format_", "inner_join_",
    "next_modules_foreach", "oceane_index",
    "payload_partial", "get_execution_report",
    "date_format", "donnees_temps_reel_cles",
    "fallthrough_", "foreach_data_null",
    "get_from_api_cache", "replace_value_non_init",
    "type_ressource_ecrase",
]

_RULE_LABEL_MARKERS = [
    "règle", "regle", "guard ", "guard_", "cas ", "scénario", "scenario",
    "doit ", "ne doit pas", "toujours", "jamais", "obligatoire",
    "enchaînement", "enchainem",
]

_RULE_NOM_MARKERS = [
    "guard_", "exec_dernier", "rattachement_", "analyse_historique",
    "codes_retour", "validation_entree", "traitement_", "mecanisme_verrou",
    "unicite_", "matrice_", "ordre_auto", "rebalancement_", "swap_",
    "matching_", "traitement_alarme", "traitement_rendre",
]


def _classify_entry(nom: str, entry: dict) -> str:
    label = (entry.get("label") or "").lower()
    nom_lower = nom.lower()

    # Bugs : label
    if any(m in label for m in _BUG_LABEL_MARKERS):
        return "bugs_connus"

    # Bugs : nom
    if any(m in nom_lower for m in _BUG_NOM_MARKERS):
        return "bugs_connus"

    # Règles métier : label
    if any(m in label for m in _RULE_LABEL_MARKERS):
        return "regles_metier"

    # Règles métier : nom
    if any(m in nom_lower for m in _RULE_NOM_MARKERS):
        return "regles_metier"

    return "observations"


# ---------------------------------------------------------------------------
# Migration d'un fichier YAML
# ---------------------------------------------------------------------------

def _migrate_file(
    yaml_path: Path,
    dry_run: bool,
) -> dict[str, list[str]]:
    """
    Migre les entrées `regles` → (regles_metier | bugs_connus | observations).
    Retourne un dict {section: [nom, ...]} pour le rapport.
    """
    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    old_regles = data.get("regles") or {}

    if not old_regles:
        return {}

    moved: dict[str, list[str]] = {
        "regles_metier": [],
        "bugs_connus":   [],
        "observations":  [],
    }

    for nom, entry in old_regles.items():
        if not isinstance(entry, dict):
            # entrée malformée → passer en regles_metier par défaut
            target = "regles_metier"
        else:
            target = _classify_entry(nom, entry)

        # Idempotence : ne pas dupliquer si déjà présent dans la section cible
        if nom in (data.get(target) or {}):
            continue

        moved[target].append(nom)

        if not dry_run:
            data.setdefault(target, {})[nom] = entry

    if not dry_run:
        # Vider la section regles (on la laisse comme clé vide pour ne pas casser les lectures)
        data["regles"] = {}
        yaml_path.write_text(
            yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False),
            encoding="utf-8",
        )

    return moved


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Migration kb_type: regle → regles_metier / bugs_connus / observations"
    )
    parser.add_argument(
        "--kb-dir",
        default="~/rosetta-data/kb/",
        help="Répertoire KB (défaut: ~/rosetta-data/kb/)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simuler sans écrire (rapport uniquement)",
    )
    args = parser.parse_args()

    kb_dir = Path(args.kb_dir).expanduser()
    if not kb_dir.exists():
        print(f"[ERREUR] Répertoire KB introuvable : {kb_dir}", file=sys.stderr)
        return 1

    # Backup
    if not args.dry_run:
        backup_dir = kb_dir.parent / "kb_backup_avant_split"
        if not backup_dir.exists():
            print(f"[BACKUP] {kb_dir} → {backup_dir}")
            shutil.copytree(kb_dir, backup_dir)
        else:
            print(f"[BACKUP] Déjà existant — ignoré : {backup_dir}")

    if args.dry_run:
        print("[DRY-RUN] Simulation uniquement — aucun fichier modifié\n")

    # Migration
    print("Migration des règles KB")
    print("=======================")

    totals: dict[str, int] = {"regles_metier": 0, "bugs_connus": 0, "observations": 0}
    total_moved = 0

    yaml_files = sorted(f for f in kb_dir.glob("*.yaml") if f.name != "_global.yaml")

    for yaml_path in yaml_files:
        moved = _migrate_file(yaml_path, dry_run=args.dry_run)
        if not any(moved.values()):
            continue

        domain_name = yaml_path.stem
        print(f"\nDomaine: {domain_name}")

        for nom in moved.get("regles_metier", []):
            print(f"  → regles_metier  : {nom}")
            totals["regles_metier"] += 1
            total_moved += 1
        for nom in moved.get("bugs_connus", []):
            print(f"  → bugs_connus    : {nom}")
            totals["bugs_connus"] += 1
            total_moved += 1
        for nom in moved.get("observations", []):
            print(f"  → observations   : {nom}")
            totals["observations"] += 1
            total_moved += 1

    print("\n" + "=" * 40)
    print("Résumé :")
    print(f"  Règles métier  : {totals['regles_metier']}")
    print(f"  Bugs connus    : {totals['bugs_connus']}")
    print(f"  Observations   : {totals['observations']}")
    print(f"  Total migré    : {total_moved}")

    if args.dry_run:
        print("\n[DRY-RUN] Aucun fichier modifié. Relancer sans --dry-run pour appliquer.")
    else:
        print(f"\n[OK] Migration terminée — {total_moved} entrée(s) déplacée(s).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
