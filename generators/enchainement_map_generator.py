"""
Enchainement Map Generator
==========================
Génère des diagrammes Mermaid (flowchart LR) à partir des relations
extraites par RelationExtractor (pattern_c, pattern_f, pattern_g).

Règles de rendu :
  - Nœuds situations (H1, I1…) : cluster "Situations"
  - Nœuds modules (this.method, svc.method) : cluster "Phase d'analyse"
  - Nœuds événements (returnLongLabel) : cluster "États finaux"
  - Nœuds non classés : section libre
  - Flèches : dédupliquées par (from, to) ; conditions non-triviales fusionnées
  - Dispatches (implies/requires/produces) : flèches pointillées
  - Produces triviaux (absent, array, null…) : filtrés

CLI:
    python -m generators.enchainement_map_generator --ir-dir ./output/ -o map.md
    python -m generators.enchainement_map_generator --ir-dir ./output/ --all -o ./output/maps/
    python -m generators.enchainement_map_generator --ir-dir ./output/ --all-services -o ./output/maps/
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers I/O
# ---------------------------------------------------------------------------

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


def _find_source_file(rel: dict) -> str:
    """Extract the fichier from the first trouvé_dans entry."""
    found_in = rel.get("trouvé_dans") or []
    if found_in and isinstance(found_in[0], dict):
        return found_in[0].get("fichier", "")
    return ""


def _service_from_file(fichier: str) -> str:
    """'…/AutomatisationCarteService.php' → 'AutomatisationCarte'."""
    if not fichier:
        return "unknown"
    stem = Path(fichier).stem
    return re.sub(r"Service$", "", stem) if stem.endswith("Service") else stem


# ---------------------------------------------------------------------------
# Label shortcuts — applied before Mermaid render
# ---------------------------------------------------------------------------

_LABEL_SHORTCUTS: dict[str, str] = {
    "CONFIRMATION + DEMANDE INTERVENTION":            "Confirmation + DI",
    "CONFIRMATION + RESET + CLOTURE":                 "Confirmation + Reset + Clôture",
    "CONFIRMATION + RESET + DEMANDE INTERVENTION":    "Confirmation + Reset + DI",
    "CONFIRMATION + RESET + ECHEC DONNEES CLOTURE":   "Confirmation + Reset + Échec",
    "Echec Consultation Etat Carte(cannot get token)": "Échec consultation carte",
    "Echec confirmation incident":                     "Échec confirmation",
    "Arret de lenchainement":                          "Arrêt enchaînement",
}

_LABEL_MAXLEN = 30


def _shorten_label(text: str) -> str:
    """Apply shortcuts first; otherwise truncate at _LABEL_MAXLEN chars."""
    if text in _LABEL_SHORTCUTS:
        return _LABEL_SHORTCUTS[text]
    if len(text) > _LABEL_MAXLEN:
        return text[:_LABEL_MAXLEN - 1] + "…"
    return text


def _safe_label(text: str, is_event: bool = False) -> str:
    """Apply shortcuts + optional truncation, then escape for Mermaid node labels.

    For event labels (returnLongLabel strings), apply shortcuts + 30-char truncation.
    For module/situation labels, only apply shortcuts, keep up to 60 chars.
    """
    shortened = _shorten_label(text) if is_event else text
    escaped = shortened.replace('"', "'").replace("::", "·")
    limit = _LABEL_MAXLEN if is_event else 60
    return escaped[:limit]


# ---------------------------------------------------------------------------
# Node ID generation
# ---------------------------------------------------------------------------

_STOP = frozenset({"de", "le", "la", "les", "du", "un", "une", "en", "et", "ou", "ne", "pas"})


def _make_short_id(text: str, taken: set[str]) -> str:
    """'CONFIRMATION + DEMANDE INTERVENTION' → 'CONF_DEMA_INTE' (unique)."""
    words = re.findall(r'[A-Za-z][A-Za-z0-9]*', text)
    meaningful = [w for w in words if len(w) >= 3 and w.lower() not in _STOP]
    parts = [w[:4].upper() for w in meaningful[:4]]
    base = "_".join(parts) if parts else "NODE"
    cand = base
    n = 2
    while cand in taken:
        cand = f"{base}_{n}"
        n += 1
    return cand


def _is_simple_id(value: str) -> bool:
    """True if value is already a valid, short Mermaid node ID (no label def needed)."""
    return bool(re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', value)) and len(value) <= 25


def _register_node(
    value: str,
    registry: dict[str, str],
    node_labels: dict[str, str],
    taken: set[str],
) -> str:
    """Return the Mermaid ID for *value*, creating an entry if needed."""
    if value in registry:
        return registry[value]

    # Slugify: keep only alnum, replace everything else with _
    slug = re.sub(r'[^A-Za-z0-9]', '_', value)
    slug = re.sub(r'_+', '_', slug).strip('_')
    if slug and slug[0].isdigit():
        slug = 'N_' + slug

    if _is_simple_id(slug) and slug == value:
        nid = value                  # already a clean ID, no label definition
    elif _is_simple_id(slug):
        nid = slug                   # short slug OK, but original value needs label
        node_labels[nid] = value
    else:
        nid = _make_short_id(value, taken)   # long value → generate short ID
        node_labels[nid] = value

    taken.add(nid)
    registry[value] = nid
    return nid


# ---------------------------------------------------------------------------
# Condition helpers
# ---------------------------------------------------------------------------

# (var_fragment, value, semantic_label) — var_fragment matched against lowercase var name
_VAR_VALUE_SEMANTICS: list[tuple[str, str, str]] = [
    ("etatapres", "Statut OK", "reset OK"),
    ("etatapres", "Statut KO", "reset KO"),
    ("returncode", "200", "succès"),
    ("returncode", "400", "échec"),
    ("returncode", "500", "erreur"),
    ("etat", "ok", "OK"),
    ("etat", "ko", "KO"),
]

# Fallback: bare value → semantic label
_VALUE_SEMANTICS: dict[str, str] = {
    "200": "succès",
    "400": "échec",
    "500": "erreur",
    "ok": "OK",
    "ko": "KO",
}


def _shorten_condition(cond: str, from_id: str) -> str | None:
    """Extract a short readable label from a condition string.

    Returns None when the extracted value equals from_id (trivial, no label needed).
    Applies semantic simplification when the variable/value pair has a known meaning.
    Falls back to a truncated version of the raw condition for non-pattern-f cases.
    """
    m = re.search(r"==\s*['\"]([^'\"]+)['\"]", cond)
    if m:
        val = m.group(1)
        if val == from_id:
            return None
        var_m = re.search(r"\$(\w+)", cond)
        if var_m:
            var_lower = var_m.group(1).lower().replace("_", "")
            for var_frag, val_key, semantic in _VAR_VALUE_SEMANTICS:
                if var_frag in var_lower and val == val_key:
                    return semantic
        return _VALUE_SEMANTICS.get(val, val[:25])
    # Non pattern-f condition (e.g., "switch sur $module") — truncate
    short = cond[:35].strip()
    return short if short else None


# ---------------------------------------------------------------------------
# Clustering
# ---------------------------------------------------------------------------

# produces outcomes that are validity-test artefacts, not business values
_TRIVIAL_PRODUCES: frozenset[str] = frozenset({
    "absent", "présent",
    "array", "non-array",
    "vide", "non vide",
    "null", "non null",
    "clé présente", "clé absente",
})

# Situation code: one uppercase letter + 0–2 digits (H0–H4, I1–I2…)
_PAT_SITUATION_VAL = re.compile(r'^[A-Z]\d{0,2}$')

_CLUSTER_TITLES: dict[str, str] = {
    "analyse":    "Phase d'analyse",
    "situations": "Situations",
    "sorties":    "États finaux",
}


def _node_cluster(val: str, etype: str) -> str | None:
    """Return cluster key for a node, or None if ungrouped."""
    if _PAT_SITUATION_VAL.match(val):
        return "situations"
    if etype == "module":
        return "analyse"
    if etype == "event":
        return "sorties"
    return None


# ---------------------------------------------------------------------------
# Core: generate_map
# ---------------------------------------------------------------------------

def generate_map(
    relations: list[dict],
    domaine: str | None = None,
    service: str | None = None,
) -> str:
    """Build a flowchart LR Mermaid string from a list of relation dicts.

    Rules:
    - One node per unique entity value (no duplicates).
    - Short readable IDs for long event labels; direct IDs for situation codes.
    - Nodes grouped into subgraphs by entity type.
    - Multiple (from, to) pairs with the *same* condition → single arrow.
    - Multiple (from, to) pairs with *different* conditions → merged label.
    - Trivial conditions (condition value == from_id) → no label on arrow.
    - transitions_to → solid arrow -->
    - implies/requires/produces → dotted arrow -.->
    - Trivial produces (absent, array, null…) filtered out.
    """
    def _keep(r: dict) -> bool:
        if domaine is not None and r.get("domaine") != domaine:
            return False
        if service is not None and _service_from_file(_find_source_file(r)) != service:
            return False
        return True

    useful = [
        r for r in relations
        if (
            (
                r.get("kind") in ("transitions_to", "implies", "requires")
                and r.get("pattern") in ("pattern_c", "pattern_d", "pattern_f", "config_db")
            ) or (
                r.get("kind") == "produces"
                and r.get("pattern") == "pattern_g"
                and (r.get("to_entity") or {}).get("value", "") not in _TRIVIAL_PRODUCES
            )
        )
        and _keep(r)
    ]

    # Pattern G — inject source modules even when all their produces are trivial.
    # We register the module node in the "analyse" cluster without adding an edge,
    # so the "Phase d'analyse" cluster shows callers detected by Pattern G.
    _g_module_nodes: list[tuple[str, str]] = []  # (value, etype)
    for r in relations:
        if r.get("pattern") != "pattern_g" or r.get("kind") != "requires":
            continue
        if not _keep(r):
            continue
        te = (r.get("to_entity") or {})
        val, etype = te.get("value", ""), te.get("type", "module")
        if val and etype == "module":
            _g_module_nodes.append((val, etype))

    if not useful:
        return (
            '%%{init: {"flowchart": {"rankSpacing": 80, "nodeSpacing": 40}}}%%\n'
            "flowchart LR\n\n"
            "    %% Aucune relation d'enchaînement trouvée\n"
        )

    # ── Node registry ────────────────────────────────────────────────────
    registry:    dict[str, str] = {}          # original value → node_id
    node_labels: dict[str, str] = {}          # node_id → original label (needs def)
    taken_ids:   set[str]       = set()
    node_info:   dict[str, tuple[str, str]] = {}  # node_id → (value, entity_type)

    def nid(value: str, etype: str = "") -> str:
        n = _register_node(value, registry, node_labels, taken_ids)
        if n not in node_info:
            node_info[n] = (value, etype)
        return n

    # ── Group arrows: (from_id, to_id) → (style, [unique conditions]) ───
    Arrow = tuple[str, str]
    arrows: dict[Arrow, tuple[str, list[str]]] = {}

    for r in useful:
        fv = (r.get("from_entity") or {}).get("value", "?")
        ft = (r.get("from_entity") or {}).get("type", "")
        tv = (r.get("to_entity") or {}).get("value", "?")
        tt = (r.get("to_entity") or {}).get("type", "")
        fid = nid(fv, ft)
        tid = nid(tv, tt)

        style = "-.->" if r.get("kind") in ("implies", "requires", "produces") else "-->"

        key: Arrow = (fid, tid)
        if key not in arrows:
            arrows[key] = (style, [])

        _, cond_list = arrows[key]
        # produces arrows are self-explanatory (call → outcome); no label needed
        if r.get("kind") != "produces":
            for c in (r.get("conditions") or []):
                sc = _shorten_condition(c, fid)
                if sc and sc not in cond_list:
                    cond_list.append(sc)

    # ── Inject Pattern G source modules (may have no non-trivial edges) ─
    for val, etype in _g_module_nodes:
        nid(val, etype)  # registers into node_info if not already there

    # ── Fix: modules that are ONLY targets (never sources) → États finaux ─
    # e.g., "this.abandon" is a delegate call target in Pattern F, never produces
    # anything → belongs in "États finaux", not "Phase d'analyse".
    # Guard: only reclassify nodes that actually appear in arrows (have at
    # least one incoming edge). Pure inject-only nodes stay in "analyse".
    source_ids: set[str] = {fid for fid, _ in arrows}
    target_ids: set[str] = {tid for _, tid in arrows}
    for n, (val, etype) in list(node_info.items()):
        if etype == "module" and n in target_ids and n not in source_ids:
            node_info[n] = (val, "event")  # reclassify to "event" → sorties cluster

    # ── Categorise nodes into clusters ───────────────────────────────────
    by_cluster: dict[str, list[str]] = {}
    for n, (val, etype) in node_info.items():
        cl = _node_cluster(val, etype) or "__none__"
        by_cluster.setdefault(cl, []).append(n)

    # ── Build Mermaid output ─────────────────────────────────────────────
    lines = [
        '%%{init: {"flowchart": {"rankSpacing": 80, "nodeSpacing": 40}}}%%',
        "flowchart LR",
        "",
    ]

    def _node_def(n: str, indent: str) -> str:
        if n in node_labels:
            _, etype = node_info.get(n, ("", ""))
            is_ev = etype == "event"
            return f'{indent}{n}["{_safe_label(node_labels[n], is_event=is_ev)}"]'
        return f"{indent}{n}"

    # Subgraphs (left → right: Analyse → Situations → Sorties)
    for ckey in ("analyse", "situations", "sorties"):
        nodes = sorted(by_cluster.get(ckey, []))
        if not nodes:
            continue
        lines.append(f'    subgraph {ckey}["{_CLUSTER_TITLES[ckey]}"]')
        for n in nodes:
            lines.append(_node_def(n, "        "))
        lines.append("    end")
        lines.append("")

    # Ungrouped nodes that need a label definition
    ungrouped_labeled = sorted(
        n for n in by_cluster.get("__none__", []) if n in node_labels
    )
    if ungrouped_labeled:
        lines.append("    %% Nœuds non classés")
        for n in ungrouped_labeled:
            lines.append(_node_def(n, "    "))
        lines.append("")

    # Arrows
    lines.append("    %% Transitions")
    for (fid, tid), (style, conds) in arrows.items():
        if conds:
            cond_str = " / ".join(conds[:3])
            if len(conds) > 3:
                cond_str += f" +{len(conds) - 3}"
            lines.append(f'    {fid} {style}|"{cond_str}"| {tid}')
        else:
            lines.append(f'    {fid} {style} {tid}')
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def generate_md(
    relations: list[dict],
    domaine: str | None = None,
    title: str = "Cartographie des enchaînements",
    service: str | None = None,
) -> str:
    diagram = generate_map(relations, domaine=domaine, service=service)
    header = f"# {title}\n\n"
    if domaine:
        header += f"Domaine : `{domaine}`\n\n"
    if service:
        header += f"Service : `{service}`\n\n"
    return header + "```mermaid\n" + diagram + "\n```\n"


def generate_service_maps(relations: list[dict], out_dir: Path) -> list[Path]:
    """Generate one Mermaid map per source service file, plus a global map."""
    out_dir.mkdir(parents=True, exist_ok=True)

    services: set[str] = set()
    for r in relations:
        if r.get("pattern") in ("pattern_c", "pattern_d", "pattern_f"):
            svc = _service_from_file(_find_source_file(r))
            if svc and svc != "unknown":
                services.add(svc)

    written: list[Path] = []

    for svc in sorted(services):
        md = generate_md(relations, title=f"Enchaînements — {svc}", service=svc)
        path = out_dir / f"map_{svc}.md"
        path.write_text(md, encoding="utf-8")
        written.append(path)
        print(f"  → {path} ({svc})")

    global_path = out_dir / "_all_enchainements.md"
    global_md = generate_md(relations, title="Enchaînements — tous services")
    global_path.write_text(global_md, encoding="utf-8")
    written.append(global_path)
    print(f"  → {global_path} (global)")

    return written


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    import argparse
    p = argparse.ArgumentParser(description="Génère des cartes Mermaid des enchaînements")
    p.add_argument("--ir-dir", required=True, metavar="DIR")
    p.add_argument("--domaine", default=None, metavar="DOM")
    p.add_argument("--all", dest="all_domaines", action="store_true")
    p.add_argument("--all-services", dest="all_services", action="store_true")
    p.add_argument("-o", "--output", required=True, metavar="PATH")
    args = p.parse_args()

    ir_dir = Path(args.ir_dir).expanduser()
    if not ir_dir.exists():
        print(f"Erreur : {ir_dir} n'existe pas", file=sys.stderr)
        sys.exit(1)

    relations = _load_relations(ir_dir)
    print(f"  {len(relations)} relations chargées depuis {ir_dir}")

    if args.all_services:
        generate_service_maps(relations, Path(args.output).expanduser())

    elif args.all_domaines:
        out_dir = Path(args.output).expanduser()
        out_dir.mkdir(parents=True, exist_ok=True)
        domaines: set[str] = {r.get("domaine", "") for r in relations if r.get("domaine")}
        domaines.add("")
        for dom in sorted(domaines):
            slug = dom or "global"
            md = generate_md(relations, domaine=dom or None, title=f"Enchaînements — {slug}")
            path = out_dir / f"map_{slug}.md"
            path.write_text(md, encoding="utf-8")
            print(f"  → {path}")

    else:
        md = generate_md(relations, domaine=args.domaine,
                         title=f"Enchaînements — {args.domaine or 'global'}")
        out = Path(args.output).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        print(f"  → {out}")


if __name__ == "__main__":
    main()
