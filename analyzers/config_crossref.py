"""
Config Crossref — croisement code ↔ configuration Oracle
=========================================================
Croise les flags issus de l'analyse statique (magic values, codes situation)
avec les lignes de configuration extraites des CSV Oracle (manifeste).

Trois sorties :
1. annotate() — les flags dont la valeur est un fait de config reçoivent
   ``resolved_by_config`` et une question remplacée par la réponse factuelle ;
   le LLM enricher les skippe (compteur config_hits, zéro appel LLM).
2. build_report() — rapport _crossref.md : CONFIG ORPHELINE (config jamais
   vue dans le code analysé) et VALEUR NON PARAMÉTRÉE (tokens du code absents
   de la config), avec la colonne « exécutions observées » si un CSV
   role=execution_log est fourni.
3. to_relations() / detect_conflicts() — transitions config pour la carte
   Mermaid et détection des divergences code ↔ config.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Optional

from analyzers.constants import STOP_TOKENS
from extractors.oracle_config_extractor import OracleConfigRow
from ir.schema import IRSchema

# Types de flags croisables : magic values et codes situation
CROSSREF_FLAG_TYPES = frozenset({
    "magic_value", "hardcoded_situation_code", "situation_coverage",
})

# Littéral MAJ quoté — même forme que les codes situation du flag engine
_UPPER_LITERAL = re.compile(r"""['"]([A-Z][A-Z0-9_]{1,})['"]""")


class ConfigCrossref:
    """Résout les flags dont la valeur est définie dans la config Oracle."""

    def __init__(self, rows: list[OracleConfigRow]) -> None:
        self.config_rows = [r for r in rows if r.role == "config"]
        self._by_cle: dict[str, OracleConfigRow] = {}
        for r in self.config_rows:
            self._by_cle.setdefault(r.cle, r)  # première définition prime
        self.exec_counts: Counter = Counter(
            r.cle for r in rows if r.role == "execution_log"
        )

    @property
    def has_execution_log(self) -> bool:
        return bool(self.exec_counts)

    def annotate(self, ir: IRSchema) -> int:
        """Enrichit les flags résolus par la config. Retourne le nombre de hits."""
        hits = 0
        for flag in ir.flags:
            if str(flag.type) not in CROSSREF_FLAG_TYPES:
                continue
            if flag.resolved_by_config:
                continue
            row = None
            for token in _UPPER_LITERAL.findall(flag.fragment or ""):
                if token in self._by_cle:
                    row = self._by_cle[token]
                    break
            if row is None:
                continue
            flag.resolved_by_config = {
                "table": row.table,
                "cle": row.cle,
                "label": row.label or row.cle,
                "conditions": row.conditions,
            }
            conds = " ; ".join(f"{k} = {v}" for k, v in row.conditions.items())
            flag.question = (
                f"Résolu par la configuration ({row.table}) : "
                f"'{row.cle}' = {row.label or row.cle}."
                + (f" Conditions : {conds}." if conds else "")
            )
            hits += 1
        return hits


# ---------------------------------------------------------------------------
# Tokens du code analysé (pour l'orphelinage config ↔ code)
# ---------------------------------------------------------------------------

def collect_code_tokens(
    irs: list[IRSchema],
    extra_json_dir: Optional[Path] = None,
) -> dict[str, set[str]]:
    """token MAJ quoté → ensemble des fichiers analysés où il apparaît.

    ``extra_json_dir`` : répertoire des ``*_business_logic.json`` déjà produits
    (index d'impact cross-fichiers) — étend la détection au-delà du run courant.
    """
    locations: dict[str, set[str]] = {}

    def _scan(source_name: str, text: str) -> None:
        for token in _UPPER_LITERAL.findall(text or ""):
            if token not in STOP_TOKENS:
                locations.setdefault(token, set()).add(source_name)

    for ir in irs:
        name = ir.metadata.controller_name or ir.metadata.source_file
        for ep in ir.entry_points:
            _scan(name, ep.raw_code or "")

    if extra_json_dir and Path(extra_json_dir).exists():
        import json
        for f in sorted(Path(extra_json_dir).glob("*_business_logic.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            name = (data.get("metadata") or {}).get("controller_name") or f.stem
            for ep in data.get("entry_points") or []:
                _scan(name, ep.get("raw_code") or "")

    return locations


# ---------------------------------------------------------------------------
# Rapport _crossref.md
# ---------------------------------------------------------------------------

def build_report(
    crossref: ConfigCrossref,
    token_locations: dict[str, set[str]],
    config_hits: int = 0,
    conflicts: Optional[list[dict]] = None,
) -> str:
    """Rapport Markdown : orphelins config↔code + conflits éventuels."""
    exec_col = crossref.has_execution_log
    lines = [
        "# Croisement code ↔ configuration Oracle",
        "",
        f"- Lignes de configuration : **{len(crossref.config_rows)}**",
        f"- Flags résolus par la config (0 appel LLM) : **{config_hits}**",
        f"- Journal d'exécution fourni : **{'oui' if exec_col else 'non'}**",
        "",
    ]

    # a) CONFIG ORPHELINE — config jamais rencontrée dans le code analysé
    orphans = [r for r in crossref.config_rows if r.cle not in token_locations]
    lines.append("## CONFIG ORPHELINE")
    lines.append("")
    if orphans:
        lines.append(
            "Lignes de configuration dont la clé n'apparaît dans aucun fichier "
            "analysé. Orpheline **et** jamais exécutée → quasi certainement morte."
        )
        lines.append("")
        header = "| Table | Clé | Label |"
        sep = "|---|---|---|"
        if exec_col:
            header += " Exécutions observées |"
            sep += "---|"
        lines += [header, sep]
        for r in sorted(orphans, key=lambda x: (x.table, x.cle)):
            row = f"| {r.table} | {r.cle} | {r.label or '—'} |"
            if exec_col:
                row += f" {crossref.exec_counts.get(r.cle, 0)} |"
            lines.append(row)
    else:
        lines.append("Aucune — toute la config est référencée dans le code analysé.")
    lines.append("")

    # b) VALEUR NON PARAMÉTRÉE — tokens du code absents de la config
    config_keys = {r.cle for r in crossref.config_rows}
    unparam = sorted(t for t in token_locations if t not in config_keys)
    lines.append("## VALEUR NON PARAMÉTRÉE")
    lines.append("")
    if unparam:
        lines.append(
            "Tokens majuscules du code absents de la configuration — "
            "candidats à paramétrer ou à documenter en KB."
        )
        lines.append("")
        header = "| Token | Fichiers |"
        sep = "|---|---|"
        if exec_col:
            header += " Exécutions observées |"
            sep += "---|"
        lines += [header, sep]
        for token in unparam:
            files = ", ".join(sorted(token_locations[token])[:4])
            row = f"| {token} | {files} |"
            if exec_col:
                row += f" {crossref.exec_counts.get(token, 0)} |"
            lines.append(row)
    else:
        lines.append("Aucune — tous les tokens du code sont paramétrés.")
    lines.append("")

    # c) CONFLITS code ↔ config
    if conflicts:
        lines.append("## ⚠️ CONFLITS code ↔ config")
        lines.append("")
        lines.append(
            "Transitions définies différemment dans le code et dans la "
            "configuration — à arbitrer en priorité (le code et la config divergent)."
        )
        lines.append("")
        lines += ["| Depuis | Cible (code) | Cible (config) | Table |",
                  "|---|---|---|---|"]
        for c in conflicts:
            lines.append(
                f"| {c['from']} | {', '.join(c['code_targets'])} "
                f"| {c['config_target']} | {c['table']} |"
            )
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Transitions config → relations pour la carte Mermaid
# ---------------------------------------------------------------------------

def to_relations(rows: list[OracleConfigRow]) -> list[dict]:
    """Convertit les lignes config avec transition en relations pour la carte.

    Nécessite colonne_source / colonne_cible dans le manifeste.
    """
    rels: list[dict] = []
    counter = 0
    for row in rows:
        if row.role != "config" or not row.transition:
            continue
        counter += 1
        src, dst = row.transition
        rels.append({
            "id": f"cfg_{counter}",
            "kind": "transitions_to",
            "from_entity": {"type": "situation", "value": src},
            "to_entity": {"type": "situation", "value": dst},
            "direction": "one_way",
            "domaine": row.domaine,
            "confiance": "high",
            "conditions": [f"[cfg:{row.table}]"],
            "trouvé_dans": [],
            "semantique": row.label or "",
            "pattern": "oracle_config",
            "oracle_table": row.table,
        })
    return rels


def detect_conflicts(code_rels: list[dict], config_rels: list[dict]) -> list[dict]:
    """Détecte les transitions où code et config divergent (même départ,
    cible différente). Marque les relations config en conflit (``conflict: True``)
    et retourne la liste des conflits pour le rapport.
    """
    code_targets: dict[str, set[str]] = {}
    for r in code_rels:
        if r.get("kind") != "transitions_to" or r.get("pattern") == "oracle_config":
            continue
        frm = (r.get("from_entity") or {}).get("value")
        to = (r.get("to_entity") or {}).get("value")
        if frm and to:
            code_targets.setdefault(frm, set()).add(to)

    conflicts: list[dict] = []
    for r in config_rels:
        if r.get("pattern") != "oracle_config":
            continue
        frm = (r.get("from_entity") or {}).get("value")
        to = (r.get("to_entity") or {}).get("value")
        targets = code_targets.get(frm or "")
        if targets and to not in targets:
            r["conflict"] = True
            conflicts.append({
                "from": frm,
                "code_targets": sorted(targets),
                "config_target": to,
                "table": r.get("oracle_table", "?"),
            })
    return conflicts
