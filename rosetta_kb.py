"""
rosetta_kb.py — CLI Knowledge Base Rosetta v3
==============================================
--kb-path accepte :
  • un fichier YAML   → ~/rosetta-data/knowledge_base.yaml  (mode legacy)
  • un répertoire     → ~/rosetta-data/kb/                  (mode multi-domaine)

Mode répertoire :
  _global.yaml     → meta + pending_validation
  {domaine}.yaml   → codes, regles, schema, sql_artifacts

Variable d'environnement : ROSETTA_KB=~/rosetta-data/kb (fichier ou dossier)
Dépendances : pyyaml uniquement.
"""

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

DEFAULT_KB_PATH = os.environ.get("ROSETTA_KB", "~/rosetta-data/knowledge_base.yaml")
CONFIDENCE_ORDER = {"high": 2, "medium": 1, "inferred": 0}
CONFIDENCE_LABELS = {"high": "[HIGH]", "medium": "[MED] ", "inferred": "[INF] "}


# ---------------------------------------------------------------------------
# Structures de base
# ---------------------------------------------------------------------------

def _empty_kb() -> dict:
    return {
        "meta": {
            "projet": "monprojet",
            "version": "2.1.0",
            "last_updated": str(date.today()),
            "maintainer": "Samah",
        },
        "codes": {},
        "regles": {},
        "schema": {},
        "sql_artifacts": {"colonnes": {}, "vues": {}, "requetes": {}},
        "pending_validation": {},
    }


def _empty_domain() -> dict:
    return {
        "codes": {},
        "regles": {},
        "schema": {},
        "sql_artifacts": {"colonnes": {}, "vues": {}, "requetes": {}},
    }


# ---------------------------------------------------------------------------
# Helpers fichiers bas niveau
# ---------------------------------------------------------------------------

def _read_file(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _write_file(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def _global_file(kb_dir: Path) -> Path:
    return kb_dir / "_global.yaml"


def _domain_file(kb_dir: Path, domain: str) -> Path:
    domain_safe = re.sub(r"[^\w-]", "_", domain)
    return kb_dir / f"{domain_safe}.yaml"


def _domain_of(args: argparse.Namespace) -> str:
    return getattr(args, "domaine", None) or "commun"


# ---------------------------------------------------------------------------
# Chargement — mode automatique (lecture)
# ---------------------------------------------------------------------------

def _load_kb(kb_path: Path) -> dict:
    """Charge le KB — fichier unique ou répertoire (lecture fusionnée)."""
    if kb_path.is_dir():
        return _load_kb_dir(kb_path)
    # Mode fichier unique
    base = _empty_kb()
    if kb_path.exists():
        with kb_path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        base.update(data)
    base.setdefault("sql_artifacts", {})
    base["sql_artifacts"].setdefault("colonnes", {})
    base["sql_artifacts"].setdefault("vues", {})
    base["sql_artifacts"].setdefault("requetes", {})
    return base


def _load_kb_dir(kb_dir: Path) -> dict:
    """Fusionne tous les *.yaml du répertoire en une vue unifiée."""
    merged = _empty_kb()
    for yaml_file in sorted(kb_dir.glob("*.yaml")):
        d = _read_file(yaml_file)
        if yaml_file.name == "_global.yaml":
            merged["meta"].update(d.get("meta", {}))
            merged["pending_validation"].update(d.get("pending_validation", {}))
        else:
            for section in ("codes", "regles", "schema"):
                merged[section].update(d.get(section, {}))
            sa = d.get("sql_artifacts", {})
            for sub in ("colonnes", "vues", "requetes"):
                merged["sql_artifacts"][sub].update(sa.get(sub, {}))
    return merged


# ---------------------------------------------------------------------------
# Chargement / sauvegarde — mode écriture (domaine ciblé)
# ---------------------------------------------------------------------------

def _load_for_write(kb_path: Path, domain: str) -> dict:
    """Pour les commandes d'écriture : charge uniquement le fichier cible."""
    if kb_path.is_dir():
        d = _read_file(_domain_file(kb_path, domain))
        base = _empty_domain()
        for section in ("codes", "regles", "schema"):
            base[section].update(d.get(section, {}))
        sa = d.get("sql_artifacts", {})
        for sub in ("colonnes", "vues", "requetes"):
            base["sql_artifacts"][sub].update(sa.get(sub, {}))
        return base
    return _load_kb(kb_path)


def _save_for_write(kb_path: Path, data: dict, domain: str) -> None:
    """Pour les commandes d'écriture : sauvegarde le fichier cible."""
    if kb_path.is_dir():
        kb_path.mkdir(parents=True, exist_ok=True)
        domain_path = _domain_file(kb_path, domain)
        domain_data = {k: v for k, v in data.items()
                       if k not in ("meta", "pending_validation")}
        _write_file(domain_path, domain_data)
        # Met à jour la date dans _global.yaml
        g = _read_file(_global_file(kb_path))
        g.setdefault("meta", {})["last_updated"] = str(date.today())
        _write_file(_global_file(kb_path), g)
    else:
        data["meta"]["last_updated"] = str(date.today())
        kb_path.parent.mkdir(parents=True, exist_ok=True)
        with kb_path.open("w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def _load_pending(kb_path: Path) -> dict:
    if kb_path.is_dir():
        return _read_file(_global_file(kb_path)).get("pending_validation", {})
    return _load_kb(kb_path).get("pending_validation", {})


def _save_pending(kb_path: Path, pending: dict) -> None:
    if kb_path.is_dir():
        kb_path.mkdir(parents=True, exist_ok=True)
        g = _read_file(_global_file(kb_path))
        g["pending_validation"] = pending
        g.setdefault("meta", {})["last_updated"] = str(date.today())
        _write_file(_global_file(kb_path), g)
    else:
        data = _load_kb(kb_path)
        data["pending_validation"] = pending
        data["meta"]["last_updated"] = str(date.today())
        _write_file(kb_path, data)


def _resolve_kb(kb_path_arg: str) -> Path:
    return Path(kb_path_arg).expanduser().resolve()


# ---------------------------------------------------------------------------
# Lookup générique (toutes sections)
# ---------------------------------------------------------------------------

def _lookup_all(data: dict, code: str) -> dict[str, Any] | None:
    checks = [
        ("codes",                data.get("codes", {})),
        ("regles",               data.get("regles", {})),
        ("schema",               data.get("schema", {})),
        ("sql_artifacts.colonnes", data.get("sql_artifacts", {}).get("colonnes", {})),
        ("sql_artifacts.vues",     data.get("sql_artifacts", {}).get("vues", {})),
        ("sql_artifacts.requetes", data.get("sql_artifacts", {}).get("requetes", {})),
    ]
    for section, bucket in checks:
        if bucket and code in bucket:
            return {"section": section, "entry": bucket[code]}
    return None


def _next_pending_id(pending: dict) -> str:
    n = len(pending) + 1
    while f"PV-{n:03d}" in pending:
        n += 1
    return f"PV-{n:03d}"


# ---------------------------------------------------------------------------
# Commande : capture
# ---------------------------------------------------------------------------

def cmd_capture(args: argparse.Namespace, kb_path: Path) -> int:
    domain = _domain_of(args)
    data = _load_for_write(kb_path, domain)
    codes = data["codes"]

    if args.code in codes and CONFIDENCE_ORDER.get(codes[args.code].get("confiance", "inferred"), 0) >= CONFIDENCE_ORDER["high"]:
        if not getattr(args, "force", False):
            print(f"[!] '{args.code}' existe déjà avec confiance high. Utilisez --force pour écraser.")
            return 1

    entry: dict[str, Any] = {
        "label": args.label,
        "source": args.source,
        "confiance": args.confiance,
    }
    if args.champ or args.table:
        ctx: dict[str, str] = {}
        if args.champ:
            ctx["champ"] = args.champ
        if args.table:
            ctx["table"] = args.table
        entry["contextes"] = [ctx]
    if args.domaine:
        entry["domaine"] = args.domaine
    if args.lie_a:
        entry["lié_à"] = [x.strip() for x in args.lie_a.split(",")]
    if args.notes:
        entry["notes"] = args.notes

    codes[args.code] = entry
    _save_for_write(kb_path, data, domain)
    mode = f"→ {_domain_file(kb_path, domain).name}" if kb_path.is_dir() else ""
    print(f"[+] Code '{args.code}' capturé (confiance: {args.confiance}) {mode}")
    return 0


# ---------------------------------------------------------------------------
# Commande : lookup
# ---------------------------------------------------------------------------

def cmd_lookup(args: argparse.Namespace, kb_path: Path) -> int:
    data = _load_kb(kb_path)
    code = args.code
    hit = _lookup_all(data, code)

    if not hit:
        if args.json:
            print(json.dumps({"found": False, "code": code}, ensure_ascii=False))
        else:
            print(f"[?] '{code}' introuvable dans le KB.")
        return 1

    entry = hit["entry"]
    result = {"found": True, "code": code, "section": hit["section"], **entry}

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    conf = entry.get("confiance", "?")
    label = entry.get("label", "—")
    print(f"\n{'='*60}")
    print(f"  {code}  [{conf.upper()}]")
    print(f"  Section : {hit['section']}")
    print(f"{'='*60}")
    print(f"  Label    : {label}")
    if "semantique" in entry:
        print(f"  Sémant.  : {entry['semantique']}")
    if "table" in entry:
        print(f"  Table    : {entry['table']}")
    if "type_oracle" in entry:
        print(f"  Type     : {entry['type_oracle']}")
    if "valeurs" in entry:
        print("  Valeurs  :")
        for k, v in entry["valeurs"].items():
            print(f"             {k!r} → {v}")
    if "distinctions" in entry:
        print("  Distinct :")
        for k, v in entry["distinctions"].items():
            print(f"             {k} : {v}")
    if "domaine" in entry:
        print(f"  Domaine  : {entry['domaine']}")
    if "lié_à" in entry:
        print(f"  Lié à    : {', '.join(entry['lié_à'])}")
    if "migration_note" in entry:
        print(f"  Migration: {entry['migration_note']}")
    if "piège_connu" in entry:
        print(f"  Piège    : {entry['piège_connu']}")
    if "trouvé_dans" in entry:
        print(f"  Dans     : {', '.join(entry['trouvé_dans'])}")
    if "source" in entry:
        print(f"  Source   : {entry['source']}")
    if entry.get("notes"):
        print(f"  Notes    : {entry['notes']}")
    print()
    return 0


# ---------------------------------------------------------------------------
# Commande : pending
# ---------------------------------------------------------------------------

def cmd_pending(args: argparse.Namespace, kb_path: Path) -> int:
    pending = _load_pending(kb_path)

    if not pending:
        print("Aucune question en attente de validation PO.")
        return 0

    prio_filter = getattr(args, "priorite", None)
    items = [
        (pid, p) for pid, p in pending.items()
        if not prio_filter or p.get("priorite") == prio_filter
    ]
    if not items:
        print(f"Aucune question avec priorité '{prio_filter}'.")
        return 0

    priority_order = {"high": 0, "medium": 1, "low": 2}
    items.sort(key=lambda x: priority_order.get(x[1].get("priorite", "low"), 3))

    print(f"\n{'─'*60}")
    print(f"  FILE PO — {len(items)} question(s) en attente")
    print(f"{'─'*60}")
    for pid, p in items:
        prio = p.get("priorite", "?")
        code = p.get("code", "?")
        question = p.get("question", "—")
        domaine = p.get("domaine", "")
        suffix = f"  [{domaine}]" if domaine else ""
        print(f"\n  {pid}  [{prio.upper()}]  {code}{suffix}")
        print(f"  Q: {question}")
        if p.get("fichiers"):
            print(f"  Dans: {', '.join(p['fichiers']) if isinstance(p['fichiers'], list) else p['fichiers']}")
    print()
    return 0


# ---------------------------------------------------------------------------
# Commande : validate
# ---------------------------------------------------------------------------

def cmd_validate(args: argparse.Namespace, kb_path: Path) -> int:
    pending = _load_pending(kb_path)

    if args.id not in pending:
        print(f"[!] ID '{args.id}' introuvable dans pending_validation.")
        return 1

    item = pending[args.id]
    code = item.get("code", "")
    kb_type = item.get("kb_type", "code")
    domain = args.domaine or item.get("domaine") or "commun"
    source = args.source or f"PO validé — {date.today()}"

    update: dict[str, Any] = {"confiance": "high", "source": source}
    if args.label:
        update["label"] = args.label
    if args.notes:
        update["notes"] = args.notes

    # Mise à jour dans le domaine
    data = _load_for_write(kb_path, domain)

    if kb_type == "colonne":
        section = data["sql_artifacts"]["colonnes"]
    elif kb_type == "vue":
        section = data["sql_artifacts"]["vues"]
    elif kb_type == "requete":
        section = data["sql_artifacts"]["requetes"]
    elif kb_type == "regle":
        section = data["regles"]
    else:
        section = data["codes"]

    action = "mis à jour" if code in section else "créé"
    section.setdefault(code, {}).update(update)

    _save_for_write(kb_path, data, domain)

    # Suppression du pending
    del pending[args.id]
    _save_pending(kb_path, pending)

    print(f"[✓] {args.id} validé — '{code}' {action} avec confiance high (domaine: {domain}).")
    return 0


# ---------------------------------------------------------------------------
# Commande : add-pending
# ---------------------------------------------------------------------------

def cmd_add_pending(args: argparse.Namespace, kb_path: Path) -> int:
    pending = _load_pending(kb_path)
    pid = _next_pending_id(pending)

    item: dict[str, Any] = {
        "code": args.code,
        "question": args.question,
        "priorite": args.priorite,
    }
    if args.fichiers:
        item["fichiers"] = [f.strip() for f in args.fichiers.split(",")]
    if args.kb_type:
        item["kb_type"] = args.kb_type
    if args.domaine:
        item["domaine"] = args.domaine

    pending[pid] = item
    _save_pending(kb_path, pending)
    print(f"[+] {pid} — '{args.code}' ajouté en pending (priorité: {args.priorite})")
    return 0


# ---------------------------------------------------------------------------
# Commande : capture-colonne
# ---------------------------------------------------------------------------

def cmd_capture_colonne(args: argparse.Namespace, kb_path: Path) -> int:
    domain = _domain_of(args)
    data = _load_for_write(kb_path, domain)
    colonnes = data["sql_artifacts"]["colonnes"]

    existing = colonnes.get(args.nom, {})
    if existing and CONFIDENCE_ORDER.get(existing.get("confiance", "inferred"), 0) >= CONFIDENCE_ORDER["high"]:
        if not getattr(args, "force", False):
            print(f"[!] '{args.nom}' existe déjà avec confiance high. Utilisez --force pour écraser.")
            return 1

    entry: dict[str, Any] = {
        "label": args.label,
        "source": args.source or f"capture — {date.today()}",
        "confiance": args.confiance,
    }
    if args.table:
        entry["table"] = args.table
    if args.type_oracle:
        entry["type_oracle"] = args.type_oracle
    if args.semantique:
        entry["semantique"] = args.semantique
    if args.valeurs:
        entry["valeurs"] = dict(
            kv.strip().split("=", 1) for kv in args.valeurs.split(",") if "=" in kv
        )
    if args.distinctions:
        entry["distinctions"] = dict(
            kv.strip().split("=", 1) for kv in args.distinctions.split(",") if "=" in kv
        )
    if args.trouve_dans:
        entry["trouvé_dans"] = [f.strip() for f in args.trouve_dans.split(",")]
    if args.migration:
        entry["migration_note"] = args.migration

    colonnes[args.nom] = entry
    _save_for_write(kb_path, data, domain)
    print(f"[+] Colonne '{args.nom}' capturée (confiance: {args.confiance})")
    return 0


# ---------------------------------------------------------------------------
# Commande : capture-vue
# ---------------------------------------------------------------------------

def cmd_capture_vue(args: argparse.Namespace, kb_path: Path) -> int:
    domain = _domain_of(args)
    data = _load_for_write(kb_path, domain)
    vues = data["sql_artifacts"]["vues"]

    existing = vues.get(args.nom, {})
    if existing and CONFIDENCE_ORDER.get(existing.get("confiance", "inferred"), 0) >= CONFIDENCE_ORDER["high"]:
        if not getattr(args, "force", False):
            print(f"[!] '{args.nom}' existe déjà avec confiance high. Utilisez --force pour écraser.")
            return 1

    entry: dict[str, Any] = {
        "label": args.label,
        "source": args.source or f"capture — {date.today()}",
        "confiance": args.confiance,
    }
    if args.semantique:
        entry["semantique"] = args.semantique
    if args.tables:
        entry["tables_source"] = [t.strip() for t in args.tables.split(",")]
    if args.piege:
        entry["piège_connu"] = args.piege
    if args.migration:
        entry["migration_note"] = args.migration

    vues[args.nom] = entry
    _save_for_write(kb_path, data, domain)
    print(f"[+] Vue '{args.nom}' capturée (confiance: {args.confiance})")
    return 0


# ---------------------------------------------------------------------------
# Commande : capture-requete
# ---------------------------------------------------------------------------

def cmd_capture_requete(args: argparse.Namespace, kb_path: Path) -> int:
    domain = _domain_of(args)
    data = _load_for_write(kb_path, domain)
    requetes = data["sql_artifacts"]["requetes"]

    existing = requetes.get(args.nom, {})
    if existing and CONFIDENCE_ORDER.get(existing.get("confiance", "inferred"), 0) >= CONFIDENCE_ORDER["high"]:
        if not getattr(args, "force", False):
            print(f"[!] '{args.nom}' existe déjà avec confiance high. Utilisez --force pour écraser.")
            return 1

    if not args.label and not existing:
        print("[!] --label obligatoire pour une nouvelle entrée.")
        return 1

    entry: dict[str, Any] = dict(existing) if existing else {}
    if args.label:
        entry["label"] = args.label
    entry["source"] = args.source or f"capture — {date.today()}"
    entry["confiance"] = args.confiance
    if args.fichier:
        entry["fichier_source"] = args.fichier
    if args.lignes:
        entry["lignes"] = args.lignes
    if args.semantique:
        entry["semantique"] = args.semantique
    if args.constantes:
        entry["constantes_magiques"] = dict(
            kv.strip().split("=", 1) for kv in args.constantes.split(",") if "=" in kv
        )
    if args.concepts:
        entry["concepts_métier"] = [c.strip() for c in args.concepts.split(",")]
    if args.index:
        entry["performance"] = {"index_critiques": [args.index]}
    if args.risque:
        entry.setdefault("performance", {})["risque_migration"] = args.risque
    if args.migration:
        entry["migration_note"] = args.migration
    if args.notes:
        entry["notes"] = args.notes

    requetes[args.nom] = entry
    _save_for_write(kb_path, data, domain)
    print(f"[+] Requête '{args.nom}' capturée (confiance: {args.confiance})")
    return 0


# ---------------------------------------------------------------------------
# Commande : stats
# ---------------------------------------------------------------------------

def cmd_stats(args: argparse.Namespace, kb_path: Path) -> int:
    data = _load_kb(kb_path)
    meta = data.get("meta", {})

    codes    = data.get("codes", {}) or {}
    regles   = data.get("regles", {}) or {}
    schema   = data.get("schema", {}) or {}
    colonnes = data.get("sql_artifacts", {}).get("colonnes", {}) or {}
    vues     = data.get("sql_artifacts", {}).get("vues", {}) or {}
    requetes = data.get("sql_artifacts", {}).get("requetes", {}) or {}
    pending  = data.get("pending_validation", {}) or {}

    all_entries = (list(codes.values()) + list(regles.values()) + list(schema.values()) +
                   list(colonnes.values()) + list(vues.values()) + list(requetes.values()))

    counts: dict[str, int] = {"high": 0, "medium": 0, "inferred": 0}
    for e in all_entries:
        if isinstance(e, dict):
            c = e.get("confiance", "inferred")
            counts[c] = counts.get(c, 0) + 1

    total = len(all_entries)
    mode = f" [{len(list(kb_path.glob('*.yaml')))} fichiers]" if kb_path.is_dir() else ""

    print(f"\n{'='*55}")
    print(f"  ROSETTA KB — {meta.get('projet', 'KB')}  v{meta.get('version', '?')}{mode}")
    print(f"  Mis à jour : {meta.get('last_updated', '?')}  |  {meta.get('maintainer', '?')}")
    print(f"{'='*55}")
    print(f"  SECTIONS")
    print(f"  {'Codes métier':<28} {len(codes):>5}")
    print(f"  {'Règles':<28} {len(regles):>5}")
    print(f"  {'Schéma':<28} {len(schema):>5}")
    print(f"  {'Colonnes Oracle':<28} {len(colonnes):>5}")
    print(f"  {'Vues Oracle':<28} {len(vues):>5}")
    print(f"  {'Requêtes complexes':<28} {len(requetes):>5}")
    print(f"  {'─'*35}")
    print(f"  {'TOTAL entrées':<28} {total:>5}")
    print(f"\n  CONFIANCE")
    print(f"  [HIGH]   validé PO           {counts.get('high', 0):>5}")
    print(f"  [MEDIUM] inféré/Copilot      {counts.get('medium', 0):>5}")
    print(f"  [INF]    non validé           {counts.get('inferred', 0):>5}")

    if kb_path.is_dir():
        print(f"\n  FICHIERS")
        for f in sorted(kb_path.glob("*.yaml")):
            d = _read_file(f)
            n = sum(len(d.get(s, {})) for s in ("codes", "regles", "schema"))
            n += sum(len(d.get("sql_artifacts", {}).get(s, {})) for s in ("colonnes", "vues", "requetes"))
            if f.name == "_global.yaml":
                n = len(d.get("pending_validation", {}))
                print(f"  _global.yaml   ({n} pending)")
            else:
                print(f"  {f.name:<28} {n:>3} entrées")

    if pending:
        prio_h = sum(1 for p in pending.values() if p.get("priorite") == "high")
        print(f"\n  FILE PO ({len(pending)} questions — {prio_h} haute priorité)")
    else:
        print(f"\n  File PO : vide")
    print()
    return 0


# ---------------------------------------------------------------------------
# Commande : search
# ---------------------------------------------------------------------------

def cmd_search(args: argparse.Namespace, kb_path: Path) -> int:
    data = _load_kb(kb_path)
    texte = args.texte.lower()
    results: list[tuple[str, str, dict]] = []

    sections = [
        ("codes",                  data.get("codes", {})),
        ("regles",                 data.get("regles", {})),
        ("schema",                 data.get("schema", {})),
        ("sql_artifacts.colonnes", data.get("sql_artifacts", {}).get("colonnes", {})),
        ("sql_artifacts.vues",     data.get("sql_artifacts", {}).get("vues", {})),
        ("sql_artifacts.requetes", data.get("sql_artifacts", {}).get("requetes", {})),
    ]

    for section_name, bucket in sections:
        if not bucket:
            continue
        for nom, entry in bucket.items():
            if not isinstance(entry, dict):
                continue
            haystack = nom.lower() + " " + json.dumps(entry, ensure_ascii=False).lower()
            if texte in haystack:
                results.append((section_name, nom, entry))

    if not results:
        print(f"Aucun résultat pour '{args.texte}'.")
        return 0

    print(f"\n{len(results)} résultat(s) pour '{args.texte}' :\n")
    for section, nom, entry in results:
        conf = entry.get("confiance", "?")
        label = entry.get("label", "—")
        print(f"  {CONFIDENCE_LABELS.get(conf, '[?]  ')}  {nom:<30}  {label}")
        print(f"             └─ {section}")
    print()
    return 0


# ---------------------------------------------------------------------------
# Commande : export
# ---------------------------------------------------------------------------

def cmd_export(args: argparse.Namespace, kb_path: Path) -> int:
    data = _load_kb(kb_path)
    meta = data.get("meta", {})
    lines: list[str] = []

    lines.append(f"# KB Rosetta — {meta.get('projet', 'KB')}")
    lines.append(f"*Version {meta.get('version', '?')} — {meta.get('last_updated', '?')}*\n")

    def _section_md(title: str, bucket: dict | None) -> None:
        if not bucket:
            return
        lines.append(f"## {title}\n")
        for nom, entry in bucket.items():
            if not isinstance(entry, dict):
                continue
            conf = entry.get("confiance", "?")
            label = entry.get("label", "—")
            lines.append(f"### `{nom}` [{conf.upper()}]")
            lines.append(f"**{label}**\n")
            if "semantique" in entry:
                lines.append(f"{entry['semantique']}\n")
            if "table" in entry:
                lines.append(f"- Table : `{entry['table']}`")
            if "type_oracle" in entry:
                lines.append(f"- Type Oracle : `{entry['type_oracle']}`")
            if "valeurs" in entry:
                lines.append("\n| Valeur | Signification |")
                lines.append("|--------|---------------|")
                for k, v in entry["valeurs"].items():
                    lines.append(f"| `{k}` | {v} |")
            if "migration_note" in entry:
                lines.append(f"\n> Migration : {entry['migration_note']}")
            if "piège_connu" in entry:
                lines.append(f"\n> Piège : {entry['piège_connu']}")
            if "source" in entry:
                lines.append(f"\n*Source : {entry['source']}*")
            lines.append("")

    _section_md("Codes métier",      data.get("codes"))
    _section_md("Règles",            data.get("regles"))
    _section_md("Schéma",            data.get("schema"))
    _section_md("Colonnes Oracle",   data.get("sql_artifacts", {}).get("colonnes"))
    _section_md("Vues Oracle",       data.get("sql_artifacts", {}).get("vues"))
    _section_md("Requêtes complexes", data.get("sql_artifacts", {}).get("requetes"))

    output = "\n".join(lines)

    if args.output:
        out_path = Path(args.output).expanduser()
        out_path.write_text(output, encoding="utf-8")
        print(f"[✓] Export écrit dans {out_path}")
    else:
        print(output)
    return 0


# ---------------------------------------------------------------------------
# Commande : split
# ---------------------------------------------------------------------------

def cmd_split(args: argparse.Namespace, kb_path: Path) -> int:
    """Migre un fichier YAML unique vers des fichiers par domaine dans kb_path (dossier)."""
    source = Path(args.source).expanduser().resolve()

    if not source.exists():
        print(f"[!] Fichier source introuvable : {source}")
        return 1
    if not kb_path.is_dir() and kb_path.exists():
        print(f"[!] --kb-path doit pointer vers un répertoire (existant ou à créer), pas un fichier.")
        return 1

    kb_path.mkdir(parents=True, exist_ok=True)

    with source.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    # _global.yaml : meta + pending_validation
    global_data = {
        "meta": data.get("meta", {}),
        "pending_validation": data.get("pending_validation", {}),
    }
    _write_file(_global_file(kb_path), global_data)
    print(f"  → _global.yaml  (meta + {len(global_data['pending_validation'])} pending)")

    # Grouper les entrées par domaine
    domain_buckets: dict[str, dict] = {}

    def _bucket(domain: str) -> dict:
        return domain_buckets.setdefault(domain, _empty_domain())

    for section in ("codes", "regles", "schema"):
        for key, entry in (data.get(section) or {}).items():
            domain = entry.get("domaine", "commun") if isinstance(entry, dict) else "commun"
            _bucket(domain)[section][key] = entry

    sa = data.get("sql_artifacts", {})
    for sub in ("colonnes", "vues", "requetes"):
        for key, entry in (sa.get(sub) or {}).items():
            domain = entry.get("domaine", "commun") if isinstance(entry, dict) else "commun"
            _bucket(domain)["sql_artifacts"][sub][key] = entry

    total_entries = 0
    for domain, domain_data in sorted(domain_buckets.items()):
        n = sum(len(domain_data.get(s, {})) for s in ("codes", "regles", "schema"))
        n += sum(len(domain_data.get("sql_artifacts", {}).get(s, {}))
                 for s in ("colonnes", "vues", "requetes"))
        _write_file(_domain_file(kb_path, domain), domain_data)
        total_entries += n
        print(f"  → {domain}.yaml  ({n} entrées)")

    print(f"\n[✓] {len(domain_buckets)} fichier(s) domaine + _global.yaml créés dans {kb_path}/")
    print(f"    {total_entries} entrées migrées.")
    print(f"\n  Mettre à jour ROSETTA_KB='{kb_path}' dans votre shell.")
    return 0


# ---------------------------------------------------------------------------
# API pour llm_enricher.py
# ---------------------------------------------------------------------------

def lookup_for_enricher(token: str, kb_path: str | None = None) -> dict[str, Any]:
    """
    Lookup un token dans toutes les sections du KB.
    Compatible fichier unique et répertoire multi-domaine.
    """
    path = Path(kb_path or DEFAULT_KB_PATH).expanduser().resolve()
    data = _load_kb(path)
    hit = _lookup_all(data, token)

    if not hit:
        return {"found": False, "confiance": None, "label": None, "valeurs": None,
                "semantique": None, "section": None}

    entry = hit["entry"]
    return {
        "found": True,
        "confiance": entry.get("confiance", "inferred"),
        "label": entry.get("label"),
        "valeurs": entry.get("valeurs"),
        "semantique": entry.get("semantique"),
        "section": hit["section"],
        **{k: v for k, v in entry.items() if k not in ("confiance", "label", "valeurs", "semantique")},
    }


# ---------------------------------------------------------------------------
# CLI — construction du parser
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rosetta_kb.py",
        description="Rosetta Knowledge Base CLI v3 (fichier unique ou répertoire multi-domaine)",
    )
    parser.add_argument(
        "--kb-path",
        default=DEFAULT_KB_PATH,
        help=f"Chemin vers knowledge_base.yaml OU répertoire kb/ (défaut: $ROSETTA_KB ou {DEFAULT_KB_PATH})",
    )

    sub = parser.add_subparsers(dest="command", metavar="<commande>")

    # ── capture ──────────────────────────────────────────────────────────────
    p = sub.add_parser("capture", help="Capturer un code/constante métier")
    p.add_argument("--code", required=True)
    p.add_argument("--label", required=True)
    p.add_argument("--source", required=True)
    p.add_argument("--confiance", default="high", choices=["high", "medium", "inferred"])
    p.add_argument("--champ")
    p.add_argument("--table")
    p.add_argument("--domaine", help="Domaine métier (détermine le fichier cible en mode répertoire)")
    p.add_argument("--lie-a", dest="lie_a")
    p.add_argument("--notes")
    p.add_argument("--force", action="store_true")

    # ── lookup ────────────────────────────────────────────────────────────────
    p = sub.add_parser("lookup", help="Chercher dans toutes les sections du KB")
    p.add_argument("--code", required=True)
    p.add_argument("--json", action="store_true")

    # ── pending ───────────────────────────────────────────────────────────────
    p = sub.add_parser("pending", help="Afficher la file de validation PO")
    p.add_argument("--priorite", choices=["high", "medium", "low"])

    # ── validate ──────────────────────────────────────────────────────────────
    p = sub.add_parser("validate", help="Valider une question PO (monte en confiance high)")
    p.add_argument("--id", required=True)
    p.add_argument("--label")
    p.add_argument("--source")
    p.add_argument("--notes")
    p.add_argument("--domaine", help="Domaine cible (mode répertoire — sinon lu dans le pending)")

    # ── add-pending ───────────────────────────────────────────────────────────
    p = sub.add_parser("add-pending", help="Ajouter une question dans la file PO")
    p.add_argument("--code", required=True)
    p.add_argument("--question", required=True)
    p.add_argument("--priorite", default="medium", choices=["high", "medium", "low"])
    p.add_argument("--fichiers")
    p.add_argument("--kb-type", dest="kb_type", default="code",
                   choices=["code", "regle", "colonne", "vue", "requete"])
    p.add_argument("--domaine", help="Domaine métier (stocké dans le pending pour validate)")

    # ── capture-colonne ───────────────────────────────────────────────────────
    p = sub.add_parser("capture-colonne", help="Capturer une colonne Oracle obscure")
    p.add_argument("--nom", required=True)
    p.add_argument("--label", required=True)
    p.add_argument("--table")
    p.add_argument("--type", dest="type_oracle")
    p.add_argument("--semantique")
    p.add_argument("--valeurs")
    p.add_argument("--distinctions")
    p.add_argument("--trouve-dans", dest="trouve_dans")
    p.add_argument("--migration")
    p.add_argument("--source")
    p.add_argument("--confiance", default="high", choices=["high", "medium", "inferred"])
    p.add_argument("--domaine")
    p.add_argument("--force", action="store_true")

    # ── capture-vue ───────────────────────────────────────────────────────────
    p = sub.add_parser("capture-vue", help="Capturer une vue Oracle")
    p.add_argument("--nom", required=True)
    p.add_argument("--label", required=True)
    p.add_argument("--semantique")
    p.add_argument("--tables")
    p.add_argument("--piege")
    p.add_argument("--migration")
    p.add_argument("--source")
    p.add_argument("--confiance", default="high", choices=["high", "medium", "inferred"])
    p.add_argument("--domaine")
    p.add_argument("--force", action="store_true")

    # ── capture-requete ───────────────────────────────────────────────────────
    p = sub.add_parser("capture-requete", help="Capturer une requête complexe 100+ lignes")
    p.add_argument("--nom", required=True)
    p.add_argument("--label")
    p.add_argument("--fichier")
    p.add_argument("--lignes")
    p.add_argument("--semantique")
    p.add_argument("--constantes")
    p.add_argument("--concepts")
    p.add_argument("--index")
    p.add_argument("--risque")
    p.add_argument("--migration")
    p.add_argument("--notes")
    p.add_argument("--source")
    p.add_argument("--confiance", default="high", choices=["high", "medium", "inferred"])
    p.add_argument("--domaine")
    p.add_argument("--force", action="store_true")

    # ── stats ─────────────────────────────────────────────────────────────────
    sub.add_parser("stats", help="Tableau de bord du KB")

    # ── search ────────────────────────────────────────────────────────────────
    p = sub.add_parser("search", help="Recherche textuelle dans tout le KB")
    p.add_argument("--texte", required=True)

    # ── export ────────────────────────────────────────────────────────────────
    p = sub.add_parser("export", help="Exporter le KB en Markdown")
    p.add_argument("--output")

    # ── split ─────────────────────────────────────────────────────────────────
    p = sub.add_parser("split", help="Migrer un fichier YAML unique vers des fichiers par domaine")
    p.add_argument("--source", required=True,
                   help="Fichier YAML source (ex: ~/rosetta-data/knowledge_base.yaml)")

    return parser


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

COMMANDS = {
    "capture":         cmd_capture,
    "lookup":          cmd_lookup,
    "pending":         cmd_pending,
    "validate":        cmd_validate,
    "add-pending":     cmd_add_pending,
    "capture-colonne": cmd_capture_colonne,
    "capture-vue":     cmd_capture_vue,
    "capture-requete": cmd_capture_requete,
    "stats":           cmd_stats,
    "search":          cmd_search,
    "export":          cmd_export,
    "split":           cmd_split,
}


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    kb_path = _resolve_kb(args.kb_path)
    handler = COMMANDS.get(args.command)
    if not handler:
        print(f"Commande inconnue : {args.command}", file=sys.stderr)
        return 1

    return handler(args, kb_path)


if __name__ == "__main__":
    sys.exit(main())
