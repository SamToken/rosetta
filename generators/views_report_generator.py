"""
Views Report Generator — rapport de migration des vues .phtml (#6)
==================================================================
Agrège les PhtmlReport en un document Markdown : surface XSS, effort Twig,
view helpers à réécrire. Déterministe, zéro LLM.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


class ViewsReportGenerator:
    def generate(self, reports: list[Any]) -> str:
        n = len(reports)
        total_out = sum(r.total_outputs for r in reports)
        total_unescaped = sum(r.unescaped_outputs for r in reports)
        total_logic = sum(r.logic_constructs for r in reports)
        total_partials = sum(r.partials for r in reports)
        helpers: set[str] = set()
        for r in reports:
            helpers.update(r.helpers)

        lines = ["# Rapport de migration des vues (.phtml)", ""]
        if n == 0:
            lines.append("> Aucune vue .phtml trouvée dans le périmètre.")
            return "\n".join(lines)

        lines.append(
            f"> {n} vue(s) analysée(s) | {total_out} sortie(s) | "
            f"**{total_unescaped} non échappée(s)** | {total_logic} construction(s) "
            f"logique(s) | {total_partials} partial/render."
        )
        lines.append("")

        # Surface XSS
        lines.append("## ⚠️ Surface XSS — sorties non échappées")
        lines.append("")
        if total_unescaped:
            lines.append(
                f"**{total_unescaped} sortie(s)** émettent une variable sans fonction "
                "d'échappement. En Zend, l'échappement est manuel (souvent oublié) ; "
                "**Twig échappe par défaut** — la migration ferme la faille mais chaque "
                "sortie volontairement brute (`|raw`) doit être tranchée."
            )
            lines.append("")
            lines.append("| Vue | Non échappées | Effort Twig |")
            lines.append("|-----|---------------|-------------|")
            worst = sorted(reports, key=lambda r: r.unescaped_outputs, reverse=True)
            for r in worst[:15]:
                if r.unescaped_outputs == 0:
                    continue
                lines.append(f"| {Path(r.path).name} | {r.unescaped_outputs} | {r.effort} |")
        else:
            lines.append("Aucune sortie non échappée détectée.")
        lines.append("")

        # Helpers à réécrire
        lines.append("## View helpers à réécrire en Twig")
        lines.append("")
        if helpers:
            lines.append(
                "Chaque helper de vue Zend devient une fonction/filtre Twig ou une "
                "extension. À couvrir :"
            )
            lines.append("")
            lines.append(", ".join(f"`{h}()`" for h in sorted(helpers)))
        else:
            lines.append("Aucun view helper custom détecté.")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(
            "> Rappel migration : `.phtml` → `.html.twig` n'est pas automatique. "
            "`<?= $x ?>` → `{{ x }}` (échappé), logique PHP → balises Twig, "
            "partials → `{% include %}`."
        )
        return "\n".join(lines)
