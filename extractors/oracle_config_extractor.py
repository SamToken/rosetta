"""
Oracle Config Extractor — CSV de paramétrage piloté par manifeste
==================================================================
Lit un répertoire d'exports CSV Oracle et un manifeste ``oracle_manifest.yaml``
qui décrit chaque fichier (table, rôle, colonnes clé/label/conditions).

Principe : AUCUN nom de table ou de colonne réel en dur dans ce code —
tout vient du manifeste, qui reste local (non versionné, .gitignore).

Robustesse exports Oracle legacy : sniffing du délimiteur (; , tab),
fallback encodage ISO-8859-1, BOM géré, espaces trimés, lignes vides ignorées.
"""

from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field

MANIFEST_NAME = "oracle_manifest.yaml"


class ManifestEntry(BaseModel):
    """Description d'un fichier CSV dans le manifeste."""
    fichier: str
    table: str
    role: str = "config"                  # config | execution_log
    domaine: str = "commun"               # kb_domaine cible
    kb_type: str = "code"                 # code | regle
    colonne_cle: str = ""                 # colonne identifiant (obligatoire pour l'import)
    colonne_label: str = ""               # colonne libellé
    colonnes_conditions: list[str] = Field(default_factory=list)
    colonne_ordre: Optional[str] = None
    # Optionnel — décrit une transition pour la cartographie Mermaid
    colonne_source: Optional[str] = None
    colonne_cible: Optional[str] = None

    model_config = {"extra": "ignore"}    # champs inconnus tolérés (compat avant)


class OracleConfigRow(BaseModel):
    """Une ligne de configuration (ou d'exécution) extraite d'un CSV."""
    table: str
    role: str = "config"
    domaine: str = "commun"
    kb_type: str = "code"
    cle: str
    label: str = ""
    ordre: Optional[int] = None
    conditions: dict[str, str] = Field(default_factory=dict)
    raw: dict[str, str] = Field(default_factory=dict)
    transition: Optional[tuple[str, str]] = None  # (source, cible) si le manifeste le décrit


# ---------------------------------------------------------------------------
# Lecture bas niveau
# ---------------------------------------------------------------------------

def _read_text(path: Path) -> str:
    """UTF-8 (BOM inclus) puis fallback ISO-8859-1 (exports Oracle legacy)."""
    data = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("iso-8859-1")


def _sniff_delimiter(sample: str) -> str:
    try:
        return csv.Sniffer().sniff(sample, delimiters=";,\t").delimiter
    except csv.Error:
        lines = sample.splitlines()
        first = lines[0] if lines else ""
        counts = {d: first.count(d) for d in (";", ",", "\t")}
        best = max(counts, key=lambda d: counts[d])
        return best if counts[best] else ";"


def load_manifest(path: Path) -> list[ManifestEntry]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    entries = data.get("fichiers") if isinstance(data, dict) else data
    if not isinstance(entries, list):
        raise ValueError(
            f"Manifeste invalide : liste attendue sous la clé 'fichiers' ({path})"
        )
    return [ManifestEntry(**e) for e in entries]


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

class OracleConfigExtractor:
    """Extrait les OracleConfigRow d'un répertoire CSV selon le manifeste."""

    def __init__(self, manifest_path: Path) -> None:
        self.manifest_path = Path(manifest_path)
        self.manifest = load_manifest(self.manifest_path)

    def extract(self, csv_dir: Path) -> list[OracleConfigRow]:
        csv_dir = Path(csv_dir)
        rows: list[OracleConfigRow] = []
        for entry in self.manifest:
            csv_path = csv_dir / entry.fichier
            if not csv_path.exists():
                continue
            rows.extend(self._extract_file(csv_path, entry))
        return rows

    def _extract_file(self, csv_path: Path, entry: ManifestEntry) -> list[OracleConfigRow]:
        text = _read_text(csv_path)
        delimiter = _sniff_delimiter(text[:4096])
        reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
        out: list[OracleConfigRow] = []
        for raw_row in reader:
            row = {
                (k or "").strip(): (v or "").strip()
                for k, v in raw_row.items() if k is not None
            }
            if not any(row.values()):
                continue  # ligne vide
            cle = row.get(entry.colonne_cle, "")
            if not cle:
                continue  # sans clé, la ligne n'est pas exploitable

            ordre: Optional[int] = None
            if entry.colonne_ordre:
                try:
                    ordre = int(row.get(entry.colonne_ordre) or "")
                except ValueError:
                    ordre = None

            transition: Optional[tuple[str, str]] = None
            if entry.colonne_source and entry.colonne_cible:
                src = row.get(entry.colonne_source, "")
                dst = row.get(entry.colonne_cible, "")
                if src and dst:
                    transition = (src, dst)

            out.append(OracleConfigRow(
                table=entry.table,
                role=entry.role,
                domaine=entry.domaine or "commun",
                kb_type=entry.kb_type,
                cle=cle,
                label=row.get(entry.colonne_label, "") if entry.colonne_label else "",
                ordre=ordre,
                conditions={c: row[c] for c in entry.colonnes_conditions if row.get(c)},
                raw=row,
                transition=transition,
            ))
        return out


# ---------------------------------------------------------------------------
# Scaffold — squelette de manifeste à compléter
# ---------------------------------------------------------------------------

def scaffold_manifest(csv_dir: Path, output: Optional[Path] = None) -> Path:
    """Scanne les CSV du répertoire et génère un manifeste squelette.

    Les colonnes détectées sont listées en commentaire ; les mappings
    (colonne_cle, colonne_label, …) restent à remplir à la main.
    """
    csv_dir = Path(csv_dir)
    output = output or csv_dir / MANIFEST_NAME
    lines = [
        "# Manifeste Oracle — squelette généré automatiquement, mappings à compléter.",
        "# Ce fichier contient des noms de tables réels : il reste LOCAL (.gitignore).",
        "fichiers:",
    ]
    for csv_path in sorted(csv_dir.glob("*.csv")):
        text = _read_text(csv_path)
        delimiter = _sniff_delimiter(text[:4096])
        header = next(csv.reader(io.StringIO(text), delimiter=delimiter), [])
        cols = [c.strip() for c in header if c.strip()]
        lines += [
            f"  - fichier: {csv_path.name}",
            f"    table: {csv_path.stem}",
            "    role: config              # config | execution_log",
            "    domaine: ''               # kb_domaine cible",
            "    kb_type: code             # code | regle",
            "    colonne_cle: ''           # identifiant — à choisir ci-dessous",
            "    colonne_label: ''",
            "    colonnes_conditions: []",
            "    colonne_ordre: null",
            "    # colonne_source: ''      # optionnel — transition pour la carte",
            "    # colonne_cible: ''",
            f"    # colonnes détectées : {', '.join(cols) if cols else '(fichier vide ?)'}",
        ]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output
