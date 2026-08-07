"""
Feature Map Generator — carte de feature cross-fichier (#3)
==========================================================
Assemble les arêtes d'appel résolues (types certains) en chaînes lisibles
depuis chaque point d'entrée analysé : controller→service→repo.

Passe de l'inventaire par fichier à une vue par feature métier, exploitable
pour cadrer une migration (« qu'est-ce que ce point d'entrée touche vraiment »).

Déterministe, zéro LLM. Nécessite un CallGraphIndex avec arêtes avant (v4).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


class FeatureMapGenerator:
    """Rend la carte de feature en Markdown depuis les IR + le call graph."""

    def generate(self, irs: list[Any], call_graph: Any, max_depth: int = 4) -> str:
        class_blocks: list[str] = []
        total_chains = 0

        for ir in irs:
            class_full = Path(ir.metadata.source_file).stem
            ep_lines: list[str] = []

            for ep in ir.entry_points:
                root = f"{class_full}::{ep.original_name}"
                chain = call_graph.walk_downstream(root, max_depth=max_depth)
                if not chain:
                    continue
                total_chains += 1
                label = ep.original_name or ep.name
                ep_lines.append(f"### {label}()")
                for depth, target in chain:
                    indent = "  " * (depth - 1)
                    ep_lines.append(f"{indent}- `{target}()`")
                ep_lines.append("")

            if ep_lines:
                class_blocks.append(f"## {class_full}\n")
                class_blocks.extend(ep_lines)

        lines = ["# Carte de feature — chaînes d'appels cross-fichier", ""]
        if not class_blocks:
            lines.append(
                "> Aucune chaîne d'appel cross-fichier résolue sur ce périmètre "
                "(types de collaborateurs non résolus, ou aucun appel typé)."
            )
            return "\n".join(lines)

        lines.append(
            f"> {total_chains} point(s) d'entrée avec chaîne d'appels résolue "
            f"(profondeur max {max_depth}). Arêtes fiables (types certains), "
            "cycles coupés. Lecture : controller→service→repo."
        )
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.extend(class_blocks)
        return "\n".join(lines)
