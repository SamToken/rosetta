"""
Enchainement Map Generator
==========================
Génère des diagrammes Mermaid (stateDiagram-v2) à partir des relations
extraites par RelationExtractor (pattern_c, pattern_d).

CLI:
    python -m generators.enchainement_map_generator --ir-dir ./output/ --domaine enchainement -o map.md
    python -m generators.enchainement_map_generator --ir-dir ./output/ --all -o ./output/maps/
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def _slugify(text: str) -> str:
    """Convert to a valid Mermaid node ID."""
    s = re.sub(r"[^a-zA-Z0-9_]", "_", text)
    if s and s[0].isdigit():
        s = "N_" + s
    return s or "NODE"


def _load_relations(ir_dir: Path) -> list[dict]:
    """Load all relations from *_business_logic.json files in ir_dir."""
    relations = []
    for f in sorted(ir_dir.rglob("*_business_logic.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        relations.extend(data.get("relations", []))
    return relations


def _source_style(pattern: str) -> str:
    if pattern in ("pattern_c", "pattern_d"):
        return "-->"    # solid: legacy hardcoded
    if pattern == "config_db":
        return "-..->"  # dotted: data-driven
    return "~~>"        # wave: inferred


def generate_map(relations: list[dict], domaine: str | None = None) -> str:
    """Build a stateDiagram-v2 Mermaid string from a list of relation dicts."""
    # Filter to useful kinds
    trans_rels = [
        r for r in relations
        if r.get("kind") == "transitions_to"
        and (domaine is None or r.get("domaine") == domaine)
    ]
    implies_rels = [
        r for r in relations
        if r.get("kind") in ("implies", "requires")
        and r.get("pattern") in ("pattern_c", "pattern_d")
        and (domaine is None or r.get("domaine") == domaine)
    ]

    lines = ["stateDiagram-v2", "    direction LR", ""]

    # State aliases for readability
    states_used: set[str] = set()
    for r in trans_rels:
        fv = (r.get("from_entity") or {}).get("value", "?")
        tv = (r.get("to_entity") or {}).get("value", "?")
        states_used.add(fv)
        states_used.add(tv)

    for s in sorted(states_used):
        slug = _slugify(s)
        if slug != s:
            lines.append(f'    state "{s}" as {slug}')
    if states_used:
        lines.append("")

    # Transitions
    if trans_rels:
        lines.append("    %% Transitions d'état (enchaînements)")
        for r in trans_rels:
            fv = (r.get("from_entity") or {}).get("value", "?")
            tv = (r.get("to_entity") or {}).get("value", "?")
            pattern = r.get("pattern", "")
            arrow = _source_style(pattern)
            label = r.get("conditions", [""])[0] if r.get("conditions") else ""
            f_slug = _slugify(fv)
            t_slug = _slugify(tv)
            if label:
                lines.append(f"    {f_slug} {arrow} {t_slug} : {label[:60]}")
            else:
                lines.append(f"    {f_slug} {arrow} {t_slug}")
        lines.append("")

    # Module→service dispatches (implies/requires from pattern_c/d)
    if implies_rels:
        lines.append("    %% Dispatch module → service")
        for r in implies_rels:
            fv = (r.get("from_entity") or {}).get("value", "?")
            tv = (r.get("to_entity") or {}).get("value", "?")
            pattern = r.get("pattern", "")
            arrow = _source_style(pattern)
            f_slug = _slugify(fv)
            t_slug = _slugify(tv)
            label = tv[:50] if tv != fv else ""
            if label:
                lines.append(f"    {f_slug} {arrow} {t_slug} : {label}")
            else:
                lines.append(f"    {f_slug} {arrow} {t_slug}")
        lines.append("")

    if not trans_rels and not implies_rels:
        lines.append("    %% Aucune relation d'enchaînement trouvée")
        lines.append("    [*] --> [*] : vide")

    return "\n".join(lines)


def generate_md(
    relations: list[dict],
    domaine: str | None = None,
    title: str = "Cartographie des enchaînements",
) -> str:
    diagram = generate_map(relations, domaine)
    header = f"# {title}\n\n"
    if domaine:
        header += f"Domaine : `{domaine}`\n\n"
    header += f"Relations source : {len(relations)} au total.\n\n"
    return header + "```mermaid\n" + diagram + "\n```\n"


def main() -> None:
    import argparse
    p = argparse.ArgumentParser(description="Génère des cartes Mermaid des enchaînements")
    p.add_argument("--ir-dir", required=True, metavar="DIR", help="Répertoire des *_business_logic.json")
    p.add_argument("--domaine", default=None, metavar="DOM", help="Filtrer par domaine")
    p.add_argument("--all", dest="all_domaines", action="store_true", help="Générer une carte par domaine")
    p.add_argument("-o", "--output", required=True, metavar="PATH", help="Fichier .md de sortie (ou répertoire si --all)")
    args = p.parse_args()

    ir_dir = Path(args.ir_dir).expanduser()
    if not ir_dir.exists():
        print(f"Erreur : {ir_dir} n'existe pas", file=sys.stderr)
        sys.exit(1)

    relations = _load_relations(ir_dir)
    print(f"  {len(relations)} relations chargées depuis {ir_dir}")

    if args.all_domaines:
        out_dir = Path(args.output).expanduser()
        out_dir.mkdir(parents=True, exist_ok=True)
        domaines: set[str] = {r.get("domaine", "inconnu") for r in relations if r.get("domaine")}
        domaines.add("")  # also generate global
        for dom in sorted(domaines):
            slug = dom or "global"
            md = generate_md(relations, dom or None, f"Enchaînements — {slug}")
            path = out_dir / f"map_{slug}.md"
            path.write_text(md, encoding="utf-8")
            print(f"  → {path}")
    else:
        md = generate_md(relations, args.domaine, f"Enchaînements — {args.domaine or 'global'}")
        out = Path(args.output).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        print(f"  → {out}")


if __name__ == "__main__":
    main()
