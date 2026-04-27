"""
kb_import.py — Import docs Copilot (Markdown + frontmatter) → knowledge_base.yaml
==================================================================================
Usage :
    python kb_import.py ~/rosetta-data/docs-kb/
    python kb_import.py ~/rosetta-data/docs-kb/ --kb-path ~/rosetta-data/knowledge_base.yaml
    python kb_import.py ~/rosetta-data/docs-kb/ --dry-run

Règles métier :
- Confiance max à l'import : medium (seul le PO monte en high via rosetta_kb.py validate)
- Collision high : ne pas écraser, logger warning
- Collision medium/inferred : mettre à jour
- Champs frontmatter inconnus : ignorés silencieusement
- Sections ## non reconnues : ignorées silencieusement
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import frontmatter
import yaml

# ---------------------------------------------------------------------------
# Types KB supportés → section cible dans knowledge_base.yaml
# ---------------------------------------------------------------------------

KB_TYPE_ROUTES: dict[str, tuple[str, ...]] = {
    "code":    ("codes",),
    "regle":   ("regles",),
    "colonne": ("sql_artifacts", "colonnes"),
    "vue":     ("sql_artifacts", "vues"),
    "requete": ("sql_artifacts", "requetes"),
}

CONFIDENCE_ORDER = {"high": 2, "medium": 1, "inferred": 0}


# ---------------------------------------------------------------------------
# Résultat d'import
# ---------------------------------------------------------------------------

@dataclass
class ImportResult:
    added: int = 0
    updated: int = 0
    ignored: int = 0   # high existant non écrasé
    errors: int = 0
    messages: list[str] = field(default_factory=list)

    def summary(self) -> str:
        lines = [
            f"{self.added} ajoutée(s), {self.updated} mise(s) à jour, "
            f"{self.ignored} ignorée(s) (high existant), {self.errors} erreur(s)"
        ]
        for msg in self.messages:
            lines.append(f"  {msg}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Parseurs de sections Markdown
# ---------------------------------------------------------------------------

def _parse_markdown_table(lines: list[str]) -> dict[str, str]:
    """Parse un tableau Markdown `| Valeur | Signification |` → dict."""
    result: dict[str, str] = {}
    for line in lines:
        line = line.strip()
        if not line.startswith("|") or re.match(r"^\|[-| ]+\|$", line):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) >= 2 and parts[0].lower() not in ("valeur", "colonne", "value", "clé", "code"):
            result[parts[0]] = parts[1]
    return result


def _parse_list(lines: list[str]) -> list[str]:
    """Parse une liste Markdown `- item` → list."""
    result = []
    for line in lines:
        line = line.strip()
        if line.startswith(("- ", "* ", "+ ")):
            result.append(line[2:].strip())
        elif re.match(r"^\d+\.\s", line):
            result.append(re.sub(r"^\d+\.\s+", "", line).strip())
    return result


def _extract_sections(content: str) -> dict[str, list[str]]:
    """Découpe le contenu Markdown en sections par titre `##`."""
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in content.splitlines():
        m = re.match(r"^##\s+(.+)", line)
        if m:
            current = m.group(1).strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return sections


def _section_text(lines: list[str]) -> str:
    return " ".join(l.strip() for l in lines if l.strip())


# ---------------------------------------------------------------------------
# Constructeurs d'entrée KB par type
# ---------------------------------------------------------------------------

def _build_code_entry(meta: dict, sections: dict) -> dict:
    entry: dict[str, Any] = {}
    if "Label" in sections:
        entry["label"] = _section_text(sections["Label"])
    if "Semantique" in sections:
        entry["semantique"] = _section_text(sections["Semantique"])
    if meta.get("kb_domaine"):
        entry["domaine"] = meta["kb_domaine"]
    if "Trouvé dans" in sections:
        refs = _parse_list(sections["Trouvé dans"])
        if refs:
            entry["contextes"] = [{"champ": r} for r in refs]
    if meta.get("kb_migration"):
        entry["migration_note"] = meta["kb_migration"]
    if "Notes" in sections:
        note = _section_text(sections["Notes"])
        if note and note.lower() not in ("aucune.", "aucune", "none", "~"):
            entry["notes"] = note
    entry["source"] = meta.get("kb_source", "kb_import — généré")
    entry["confiance"] = "medium"
    return entry


def _build_regle_entry(meta: dict, sections: dict) -> dict:
    entry: dict[str, Any] = {}
    if "Label" in sections:
        entry["label"] = _section_text(sections["Label"])
    if "Semantique" in sections:
        entry["semantique"] = _section_text(sections["Semantique"])
    if "Conditions" in sections:
        conds = _parse_list(sections["Conditions"])
        if conds:
            entry["conditions"] = conds
    if meta.get("kb_domaine"):
        entry["domaine"] = meta["kb_domaine"]
    if meta.get("kb_migration"):
        entry["migration_note"] = meta["kb_migration"]
    if "Notes" in sections:
        note = _section_text(sections["Notes"])
        if note and note.lower() not in ("aucune.", "aucune", "none", "~"):
            entry["notes"] = note
    entry["source"] = meta.get("kb_source", "kb_import — généré")
    entry["confiance"] = "medium"
    return entry


def _build_colonne_entry(meta: dict, sections: dict) -> dict:
    entry: dict[str, Any] = {}
    if "Label" in sections:
        entry["label"] = _section_text(sections["Label"])
    if meta.get("kb_table"):
        entry["table"] = meta["kb_table"]
    if meta.get("kb_type_oracle"):
        entry["type_oracle"] = meta["kb_type_oracle"]
    if "Semantique" in sections:
        entry["semantique"] = _section_text(sections["Semantique"])
    if "Valeurs" in sections:
        vals = _parse_markdown_table(sections["Valeurs"])
        if vals:
            entry["valeurs"] = vals
    if "Distinctions" in sections:
        dists = _parse_markdown_table(sections["Distinctions"])
        if dists:
            entry["distinctions"] = dists
    if "Trouvé dans" in sections:
        refs = _parse_list(sections["Trouvé dans"])
        if refs:
            entry["trouvé_dans"] = refs
    if meta.get("kb_migration"):
        entry["migration_note"] = meta["kb_migration"]
    if "Notes" in sections:
        note = _section_text(sections["Notes"])
        if note and note.lower() not in ("aucune.", "aucune", "none", "~"):
            entry["notes"] = note
    entry["source"] = meta.get("kb_source", "kb_import — généré")
    entry["confiance"] = "medium"
    return entry


def _build_vue_entry(meta: dict, sections: dict) -> dict:
    entry: dict[str, Any] = {}
    if "Label" in sections:
        entry["label"] = _section_text(sections["Label"])
    if "Semantique" in sections:
        entry["semantique"] = _section_text(sections["Semantique"])
    if meta.get("kb_tables"):
        entry["tables_source"] = [t.strip() for t in str(meta["kb_tables"]).split(",")]
    if "Piège" in sections:
        entry["piège_connu"] = _section_text(sections["Piège"])
    if meta.get("kb_migration"):
        entry["migration_note"] = meta["kb_migration"]
    if "Notes" in sections:
        note = _section_text(sections["Notes"])
        if note and note.lower() not in ("aucune.", "aucune", "none", "~"):
            entry["notes"] = note
    entry["source"] = meta.get("kb_source", "kb_import — généré")
    entry["confiance"] = "medium"
    return entry


def _build_requete_entry(meta: dict, sections: dict) -> dict:
    entry: dict[str, Any] = {}
    if "Label" in sections:
        entry["label"] = _section_text(sections["Label"])
    if meta.get("kb_fichier"):
        entry["fichier_source"] = meta["kb_fichier"]
    if meta.get("kb_lignes"):
        entry["lignes"] = meta["kb_lignes"]
    if "Semantique" in sections:
        entry["semantique"] = _section_text(sections["Semantique"])
    if "Constantes" in sections:
        consts = _parse_markdown_table(sections["Constantes"])
        if consts:
            entry["constantes_magiques"] = consts
    if "Concepts" in sections:
        concepts = _parse_list(sections["Concepts"])
        if concepts:
            entry["concepts_métier"] = concepts
    if meta.get("kb_migration"):
        entry["migration_note"] = meta["kb_migration"]
    if "Notes" in sections:
        note = _section_text(sections["Notes"])
        if note and note.lower() not in ("aucune.", "aucune", "none", "~"):
            entry["notes"] = note
    entry["source"] = meta.get("kb_source", "kb_import — généré")
    entry["confiance"] = "medium"
    return entry


_BUILDERS = {
    "code":    _build_code_entry,
    "regle":   _build_regle_entry,
    "colonne": _build_colonne_entry,
    "vue":     _build_vue_entry,
    "requete": _build_requete_entry,
}


# ---------------------------------------------------------------------------
# Accès / mutation du KB YAML
# ---------------------------------------------------------------------------

def _load_kb(kb_path: Path) -> dict:
    if kb_path.exists():
        with kb_path.open(encoding="utf-8", errors="replace") as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}
    # Garantir la structure minimale
    data.setdefault("meta", {
        "projet": "ASO",
        "version": "2.0.0",
        "last_updated": str(date.today()),
        "maintainer": "Samah",
    })
    data.setdefault("codes", {})
    data.setdefault("regles", {})
    data.setdefault("sql_artifacts", {})
    data["sql_artifacts"].setdefault("colonnes", {})
    data["sql_artifacts"].setdefault("vues", {})
    data["sql_artifacts"].setdefault("requetes", {})
    data.setdefault("pending_validation", {})
    return data


def _save_kb(kb_path: Path, data: dict) -> None:
    data["meta"]["last_updated"] = str(date.today())
    kb_path.parent.mkdir(parents=True, exist_ok=True)
    with kb_path.open("w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def _get_section(data: dict, route: tuple[str, ...]) -> dict:
    node = data
    for key in route:
        node = node.setdefault(key, {})
    return node


def _upsert_entry(
    section: dict,
    nom: str,
    new_entry: dict,
    result: ImportResult,
    file_name: str,
) -> None:
    existing = section.get(nom)
    if existing is None:
        section[nom] = new_entry
        result.added += 1
        result.messages.append(f"[+] {nom} ({file_name})")
        return

    existing_conf = CONFIDENCE_ORDER.get(existing.get("confiance", "inferred"), 0)
    if existing_conf >= CONFIDENCE_ORDER["high"]:
        result.ignored += 1
        result.messages.append(f"[!] {nom} ignoré — confiance high existante ({file_name})")
        return

    section[nom] = new_entry
    result.updated += 1
    result.messages.append(f"[~] {nom} mis à jour ({file_name})")


# ---------------------------------------------------------------------------
# Import d'un fichier unique
# ---------------------------------------------------------------------------

def import_file(md_path: Path, data: dict, result: ImportResult) -> None:
    try:
        post = frontmatter.loads(md_path.read_text(encoding="utf-8"))
    except Exception as e:
        result.errors += 1
        result.messages.append(f"[E] {md_path.name} — erreur lecture frontmatter : {e}")
        return

    meta = dict(post.metadata)
    kb_type = meta.get("kb_type", "").strip().lower()
    kb_nom = meta.get("kb_nom", "").strip()

    if not kb_type:
        # Pas de frontmatter kb_type : ignorer silencieusement
        return

    if kb_type not in KB_TYPE_ROUTES:
        result.errors += 1
        result.messages.append(f"[E] {md_path.name} — kb_type inconnu : '{kb_type}'")
        return

    if not kb_nom:
        result.errors += 1
        result.messages.append(f"[E] {md_path.name} — kb_nom manquant")
        return

    sections = _extract_sections(post.content)
    builder = _BUILDERS[kb_type]

    try:
        entry = builder(meta, sections)
    except Exception as e:
        result.errors += 1
        result.messages.append(f"[E] {md_path.name} — erreur construction entrée : {e}")
        return

    route = KB_TYPE_ROUTES[kb_type]
    section = _get_section(data, route)
    _upsert_entry(section, kb_nom, entry, result, md_path.name)


# ---------------------------------------------------------------------------
# Point d'entrée principal
# ---------------------------------------------------------------------------

def import_directory(
    docs_dir: Path,
    kb_path: Path,
    dry_run: bool = False,
) -> ImportResult:
    result = ImportResult()

    md_files = sorted(docs_dir.rglob("*.md"))
    if not md_files:
        result.messages.append(f"Aucun fichier .md trouvé dans {docs_dir}")
        return result

    data = _load_kb(kb_path)

    for md_path in md_files:
        import_file(md_path, data, result)

    if not dry_run and (result.added + result.updated) > 0:
        _save_kb(kb_path, data)

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Importe des docs Copilot (.md) dans knowledge_base.yaml"
    )
    default_kb_dir = Path(__file__).parent / "kb"
    parser.add_argument(
        "docs_dir",
        nargs="?",
        default=str(default_kb_dir),
        help=f"Dossier contenant les .md (défaut: {default_kb_dir})",
    )
    parser.add_argument(
        "--kb-path",
        default=os.environ.get("ROSETTA_KB", "~/rosetta-data/knowledge_base.yaml"),
        help="Chemin vers knowledge_base.yaml (défaut: $ROSETTA_KB)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans écrire le KB")
    args = parser.parse_args()

    docs_dir = Path(args.docs_dir).expanduser().resolve()
    kb_path = Path(args.kb_path).expanduser().resolve()

    if not docs_dir.exists():
        print(f"Erreur : dossier introuvable : {docs_dir}", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print(f"[dry-run] Simulation — KB non modifié")

    result = import_directory(docs_dir, kb_path, dry_run=args.dry_run)
    print(result.summary())

    if result.errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
