"""
SQL Map Generator — carte SQL cross-fichier (#7)
================================================
Agrège les faits SQL (analyzers.sql_analyzer) des opérations d'un run en une
carte : tables lues/écrites par fichier et par méthode, jointures, alertes.

Déterministe, zéro LLM, zéro accès base. Best-effort (regex).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from analyzers.sql_analyzer import parse_sql, SqlFacts


def _method_for_line(source_line, entry_points) -> str:
    if source_line:
        for ep in entry_points:
            if ep.start_line and ep.end_line and ep.start_line <= source_line <= ep.end_line:
                return ep.original_name or ep.name
    return "?"


class SqlMapGenerator:
    def generate(self, irs: list[Any]) -> str:
        blocks: list[str] = []
        all_tables_read: set[str] = set()
        all_tables_written: set[str] = set()
        total_joins = 0

        for ir in irs:
            class_full = Path(ir.metadata.source_file).stem
            f_read: set[str] = set()
            f_write: set[str] = set()
            f_joins: set[str] = set()
            star = 0
            outer = 0
            # méthode → (lues, écrites)
            by_method: dict[str, tuple[set[str], set[str]]] = {}

            for op in ir.operations:
                facts = parse_sql(op.details or "")
                if facts.is_empty and not facts.select_star:
                    continue
                f_read.update(facts.tables_read)
                f_write.update(facts.tables_written)
                f_joins.update(facts.joins)
                star += 1 if facts.select_star else 0
                outer += 1 if facts.oracle_outer_join else 0
                meth = _method_for_line(op.source_line, ir.entry_points)
                r, w = by_method.setdefault(meth, (set(), set()))
                r.update(facts.tables_read)
                w.update(facts.tables_written)

            if not (f_read or f_write):
                continue

            all_tables_read.update(f_read)
            all_tables_written.update(f_write)
            total_joins += len(f_joins)

            lines = [f"## {class_full}", ""]
            if f_read:
                lines.append(f"**Tables lues** : {', '.join(f'`{t}`' for t in sorted(f_read))}")
            if f_write:
                lines.append(f"**Tables écrites** : {', '.join(f'`{t}`' for t in sorted(f_write))}")
            if f_joins:
                lines.append("**Jointures** :")
                for j in sorted(f_joins):
                    lines.append(f"- `{j}`")
            alerts = []
            if star:
                alerts.append(f"`SELECT *` ×{star}")
            if outer:
                alerts.append(f"jointure externe Oracle `(+)` ×{outer}")
            if alerts:
                lines.append(f"⚠️ {' · '.join(alerts)}")
            # méthodes → tables
            meth_lines = []
            for meth, (r, w) in sorted(by_method.items()):
                parts = []
                if r:
                    parts.append("lit " + ", ".join(f"`{t}`" for t in sorted(r)))
                if w:
                    parts.append("écrit " + ", ".join(f"`{t}`" for t in sorted(w)))
                if parts:
                    meth_lines.append(f"- `{meth}()` : {' ; '.join(parts)}")
            if meth_lines:
                lines.append("")
                lines.append("**Méthodes → tables** :")
                lines.extend(meth_lines)
            lines.append("")
            blocks.append("\n".join(lines))

        header = ["# Carte SQL — tables, colonnes, jointures", ""]
        if not blocks:
            header.append("> Aucune opération SQL structurée détectée sur ce périmètre.")
            return "\n".join(header)
        header.append(
            f"> {len(all_tables_read)} table(s) lue(s), "
            f"{len(all_tables_written)} écrite(s), {total_joins} jointure(s). "
            "Extraction statique best-effort (regex, sans accès base)."
        )
        header.append("")
        header.append("---")
        header.append("")
        return "\n".join(header) + "\n".join(blocks)
