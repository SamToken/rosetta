"""
Code Citations — Références cliquables vers le code source PHP
================================================================
Résout un Flag (ou une location string) vers une référence
`fichier.php:ligne` cliquable dans VSCode / Cursor / les terminaux modernes.

Aujourd'hui les générateurs écrivent `[op_15]` ou `executeAction` — un dev
doit ensuite grep pour retrouver la ligne. Avec ce module, les sorties
deviennent `EnchainementController.php:152` que l'IDE ouvre en ctrl+clic.

Intégration recommandée
-----------------------
Dans `generators/business_doc_generator.py` :

    from generators.code_citations import cite, cite_md

    # Au lieu de :
    lines.append(f"- ⚠️ [{flag.location}] {flag.fragment}")

    # Écrire :
    lines.append(f"- ⚠️ {cite_md(ir, flag)} `{flag.fragment}`")

Deux formes :
    cite(ir, flag)     → "EnchainementController.php:152" (texte brut)
    cite_md(ir, flag)  → "[EnchainementController.php:152](./astro/.../file.php#L152)"
                         (lien markdown, fonctionne en ctrl+clic sur VSCode/Cursor
                         si le doc est ouvert au bon endroit relatif au repo)

Le chemin du lien est construit à partir de `ir.metadata.source_file`.
Pour qu'il soit cliquable, ce chemin doit être relatif à l'endroit où le
markdown est ouvert (typiquement la racine du repo `rosetta` ou un endroit
voisin du repo `astro`). Paramétrer `link_root` si nécessaire.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

from ir.schema import (
    IRSchema,
    Flag,
    EntryPoint,
    Operation,
    ControlBlock,
)


# =============================================================================
# Résolution location → ligne
# =============================================================================

def resolve_line(ir: IRSchema, location: str) -> Optional[int]:
    """
    Résout une `flag.location` vers un numéro de ligne dans le fichier source.

    `location` peut être :
    - un nom d'entry_point ("executeAction") → ep.start_line
    - un id d'opération ("op_15") → op.source_line
    - un id de bloc ("block_3") → ligne du premier op du bloc (best-effort)
    - un nom de dépendance → None (pas de ligne associée)
    """
    if not location:
        return None

    # 1) Cherche dans les entry_points
    for ep in ir.entry_points:
        if ep.name == location or ep.original_name == location:
            return ep.start_line

    # 2) Cherche dans les opérations
    for op in ir.operations:
        if op.id == location:
            return op.source_line

    # 3) Cherche dans les control_blocks → première op du bloc
    for block in ir.control_flow:
        if block.id == location and block.operations:
            first_op_id = block.operations[0]
            for op in ir.operations:
                if op.id == first_op_id:
                    return op.source_line

    return None


def resolve_line_from_flag(ir: IRSchema, flag: Flag) -> Optional[int]:
    """Comme `resolve_line` mais prend directement un Flag."""
    return resolve_line(ir, flag.location)


# =============================================================================
# Format texte
# =============================================================================

def cite(ir: IRSchema, target: Union[Flag, str]) -> str:
    """
    Référence texte vers le code source. Format : `FichierPHP.php:ligne`.

    Args:
        ir: l'IR contenant les metadata du fichier source
        target: un Flag ou une location string

    Retourne le nom du fichier seul si aucune ligne ne peut être résolue.
    """
    filename = _filename(ir)

    if isinstance(target, Flag):
        line = resolve_line_from_flag(ir, target)
    else:
        line = resolve_line(ir, target)

    if line is None:
        return filename
    return f"{filename}:{line}"


def cite_md(
    ir: IRSchema,
    target: Union[Flag, str],
    link_root: str = "../astro",
) -> str:
    """
    Lien markdown cliquable vers le code source.

    Format : `[FichierPHP.php:ligne](link_root/path/to/FichierPHP.php#L152)`

    Args:
        ir: l'IR contenant les metadata du fichier source
        target: un Flag ou une location string
        link_root: préfixe utilisé pour construire le lien. Par défaut
                   `../astro` (suppose que les outputs sont à côté du repo astro).
                   Adapter selon où le markdown est consommé.

    Si aucune ligne ne peut être résolue, retourne un lien sans ancre.
    """
    filename = _filename(ir)
    source_file = ir.metadata.source_file or filename

    if isinstance(target, Flag):
        line = resolve_line_from_flag(ir, target)
    else:
        line = resolve_line(ir, target)

    link_path = _build_link_path(source_file, link_root)
    anchor = f"#L{line}" if line is not None else ""
    label_suffix = f":{line}" if line is not None else ""

    return f"[{filename}{label_suffix}]({link_path}{anchor})"


# =============================================================================
# Helpers internes
# =============================================================================

def _filename(ir: IRSchema) -> str:
    """Nom de fichier court depuis ir.metadata.source_file."""
    source = ir.metadata.source_file
    if not source:
        return ir.metadata.controller_name + ".php"
    return Path(source).name


def _build_link_path(source_file: str, link_root: str) -> str:
    """
    Construit le chemin pour le lien markdown.

    Si source_file est absolu, on tente de le rendre relatif à link_root.
    Sinon on préfixe par link_root.
    """
    src = Path(source_file)

    # Cas 1 : source_file est absolu — on extrait la portion après "astro/"
    # si elle existe, sinon on garde juste le nom
    if src.is_absolute():
        parts = src.parts
        # Cherche "astro" dans le chemin pour reconstruire un lien relatif propre
        for i, part in enumerate(parts):
            if part == "astro":
                relative = Path(*parts[i + 1:])
                return f"{link_root.rstrip('/')}/{relative.as_posix()}"
        # Fallback : juste le nom de fichier
        return f"{link_root.rstrip('/')}/{src.name}"

    # Cas 2 : source_file est déjà relatif
    return f"{link_root.rstrip('/')}/{src.as_posix()}"


# =============================================================================
# Exemple d'utilisation (pour tests rapides)
# =============================================================================

if __name__ == "__main__":
    from ir.schema import IRMetadata

    ir = IRSchema(
        metadata=IRMetadata(
            source_file="/home/nixos/projects/astro/application/controllers/EnchainementController.php",
            controller_name="Enchainement",
        ),
        entry_points=[
            EntryPoint(name="executeAction", original_name="execute", start_line=142),
        ],
        operations=[
            Operation(id="op_1", type="db_read", details="SELECT *", source_line=158),
        ],
    )

    print("cite (text):       ", cite(ir, "executeAction"))
    print("cite (text op):    ", cite(ir, "op_1"))
    print("cite_md (default): ", cite_md(ir, "executeAction"))
    print("cite_md (custom):  ", cite_md(ir, "op_1", link_root="../astro"))
