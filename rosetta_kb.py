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

DEFAULT_KB_PATH = os.environ.get("ROSETTA_KB", "~/rosetta-data/kb")
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


def _normalize_domain(name: str) -> str:
    """Convertit un nom de fichier PHP ou domaine court en identifiant YAML.

    Exemples :
      'OrchestraService.php'                              → 'OrchestraService'
      'application/src/Service/OrchestraService.php'     → 'OrchestraService'
      'orchestra-service'                                 → 'orchestra-service'
    """
    p = Path(name)
    if p.suffix.lower() == ".php":
        return p.stem
    return name


def _domain_file(kb_dir: Path, domain: str) -> Path:
    domain_safe = re.sub(r"[^A-Za-z0-9_-]", "_", domain)
    return kb_dir / f"{domain_safe}.yaml"


def _domain_of(args: argparse.Namespace) -> str:
    raw = getattr(args, "domaine", None)
    if not raw:
        return "commun"
    return _normalize_domain(raw)


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


# Types de flags qui indiquent une décision d'architecture, pas un token KB
_PENDING_DECISION_FLAG_TYPES: frozenset[str] = frozenset({
    "missing_branch", "external_state_dependency", "dynamic_session_key",
})
_PENDING_DECISION_CODE_RE = re.compile(
    r"^(BRANCHES_MANQUANTES_|DI-missing_branch--|DI-external_state--|FALLBACK_)",
    re.IGNORECASE,
)


def _detect_pending_type(
    code: str,
    kb_data: dict,
    flag_type: str | None = None,
) -> tuple[int, str]:
    """Détermine pending_type (1/2/3) et destination d'un pending.

    1 → token existe en KB (medium/inferred)  → destination: kb_upgrade
    2 → token absent du KB                    → destination: kb_new_entry
    3 → décision comportement/architecture    → destination: migration_notes
    """
    if flag_type in _PENDING_DECISION_FLAG_TYPES:
        return 3, "migration_notes"
    if _PENDING_DECISION_CODE_RE.match(code):
        return 3, "migration_notes"
    if _lookup_all(kb_data, code):
        return 1, "kb_upgrade"
    return 2, "kb_new_entry"


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

    kb_data = _load_kb(kb_path)
    ptype, dest = _detect_pending_type(args.code, kb_data, flag_type=getattr(args, "kb_type", None))
    item["pending_type"] = ptype
    item["destination"] = dest

    pending[pid] = item
    _save_pending(kb_path, pending)
    print(f"[+] {pid} — '{args.code}' ajouté en pending (priorité: {args.priorite}) [{dest}]")
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
# Commande : export-prompt
# ---------------------------------------------------------------------------

_CONF_LEVEL = {"high": 2, "medium": 1, "inferred": 0}


def _first_sentence(text: str, max_len: int = 220) -> str:
    """Première phrase complète d'un texte, tronquée à max_len si nécessaire."""
    if not text:
        return ""
    for sep in ('.', '!', '?'):
        idx = text.find(sep)
        if 0 < idx < max_len:
            return text[:idx + 1].strip()
    return text[:max_len].strip()


def format_kb_for_prompt(
    data: dict,
    domaine: str | None = None,
    confiance_min: str = "medium",
    max_chars: int = 4_000,
) -> str:
    """
    Sérialise le KB en bloc texte compact injectable dans un prompt LLM.

    Peut être appelée depuis llm_enricher.py ou rosetta_analyze.py.
    """
    min_level = _CONF_LEVEL.get(confiance_min, 1)

    def _keep(entry: dict) -> bool:
        if not isinstance(entry, dict):
            return False
        lvl = _CONF_LEVEL.get(entry.get("confiance", "inferred"), 0)
        if lvl < min_level:
            return False
        if domaine and entry.get("domaine") and entry.get("domaine") != domaine:
            return False
        return True

    def _valeurs_inline(vals: dict | None) -> str:
        if not vals:
            return ""
        return ", ".join(f"{k}={v}" for k, v in list(vals.items())[:5])

    def _conditions_inline(conds: list | None) -> str:
        if not conds:
            return ""
        return " | ".join(str(c) for c in conds[:3])

    lines: list[str] = []
    skipped = 0

    def _add(line: str) -> bool:
        nonlocal skipped
        projected = sum(len(l) + 1 for l in lines) + len(line) + 1
        if projected > max_chars:
            skipped += 1
            return False
        lines.append(line)
        return True

    # ── Codes ──────────────────────────────────────────────────────────────
    codes = {k: v for k, v in (data.get("codes") or {}).items() if _keep(v)}
    if codes:
        _add("## Codes métier")
        for nom, e in codes.items():
            conf = e.get("confiance", "?")
            label = e.get("label", "")
            sem = _first_sentence(e.get("semantique") or e.get("notes") or "")
            parts = [f"{nom} [{conf}] — {label}"]
            if sem and sem != label:
                parts.append(sem)
            _add("  " + ". ".join(parts).rstrip(".") + ".")

    # ── Règles ─────────────────────────────────────────────────────────────
    regles = {k: v for k, v in (data.get("regles") or {}).items() if _keep(v)}
    if regles:
        _add("## Règles métier")
        for nom, e in regles.items():
            conf = e.get("confiance", "?")
            label = e.get("label", "")
            sem = _first_sentence(e.get("semantique") or "")
            conds = _conditions_inline(e.get("conditions"))
            parts = [f"{nom} [{conf}] — {label}"]
            if sem:
                parts.append(sem)
            if conds:
                parts.append(f"Conditions: {conds}")
            _add("  " + ". ".join(parts).rstrip(".") + ".")

    # ── Colonnes ───────────────────────────────────────────────────────────
    cols = {k: v for k, v in (data.get("sql_artifacts", {}).get("colonnes") or {}).items() if _keep(v)}
    if cols:
        _add("## Colonnes Oracle")
        for nom, e in cols.items():
            conf = e.get("confiance", "?")
            table = e.get("table", "")
            otype = e.get("type_oracle", "")
            label = e.get("label", "")
            sem = _first_sentence(e.get("semantique") or "")
            vals = _valeurs_inline(e.get("valeurs"))
            meta = ", ".join(x for x in [table, otype] if x)
            head = f"{nom} [{meta}, {conf}]" if meta else f"{nom} [{conf}]"
            parts = [f"{head} — {label}"]
            if sem:
                parts.append(sem)
            if vals:
                parts.append(f"Valeurs: {vals}")
            _add("  " + ". ".join(parts).rstrip(".") + ".")

    # ── Vues ───────────────────────────────────────────────────────────────
    vues = {k: v for k, v in (data.get("sql_artifacts", {}).get("vues") or {}).items() if _keep(v)}
    if vues:
        _add("## Vues Oracle")
        for nom, e in vues.items():
            conf = e.get("confiance", "?")
            label = e.get("label", "")
            sem = _first_sentence(e.get("semantique") or "")
            piege = e.get("piège_connu", "")
            parts = [f"{nom} [{conf}] — {label}"]
            if sem:
                parts.append(sem)
            if piege:
                parts.append(f"Piège: {_first_sentence(piege, 120)}")
            _add("  " + ". ".join(parts).rstrip(".") + ".")

    # ── Requêtes ───────────────────────────────────────────────────────────
    reqs = {k: v for k, v in (data.get("sql_artifacts", {}).get("requetes") or {}).items() if _keep(v)}
    if reqs:
        _add("## Requêtes nommées")
        for nom, e in reqs.items():
            conf = e.get("confiance", "?")
            label = e.get("label", "")
            sem = _first_sentence(e.get("semantique") or "")
            parts = [f"{nom} [{conf}] — {label}"]
            if sem:
                parts.append(sem)
            _add("  " + ". ".join(parts).rstrip(".") + ".")

    if not lines:
        return ""

    total = sum(len(d) for d in [codes, regles, cols, vues, reqs])
    dom_label = f"domaine: {domaine} | " if domaine else ""
    header = f"════ CONTEXTE KB ({dom_label}confiance ≥ {confiance_min} | {total} entrée(s)) ════"
    footer = "════ FIN CONTEXTE KB ════"
    if skipped:
        footer = f"[… {skipped} entrée(s) supplémentaire(s) non incluses — augmenter --max-chars]\n{footer}"

    return "\n".join([header, ""] + lines + ["", footer])


def cmd_export_prompt(args: argparse.Namespace, kb_path: Path) -> int:
    data = _load_kb(kb_path)
    domaine = getattr(args, "domaine", None) or None
    confiance_min = getattr(args, "confiance", "medium") or "medium"
    max_chars = int(getattr(args, "max_chars", 4000) or 4000)

    block = format_kb_for_prompt(data, domaine=domaine, confiance_min=confiance_min, max_chars=max_chars)
    if not block:
        print("(KB vide ou aucune entrée ne correspond aux filtres)")
        return 0

    if args.output:
        out = Path(args.output).expanduser()
        out.write_text(block, encoding="utf-8")
        total_chars = len(block)
        print(f"[✓] Prompt KB écrit dans {out} ({total_chars} caractères)")
    else:
        print(block)
    return 0


# ---------------------------------------------------------------------------
# Commande : export-brief  (brief PO)
# ---------------------------------------------------------------------------

_TYPE_LABELS = {
    "magic_value":               "Valeur non documentée",
    "hardcoded_situation_code":  "Code situation hardcodé",
    "missing_branch":            "Branche non documentée",
    "external_state_dependency": "Dépendance état externe",
    "dynamic_session_key":       "Clé session dynamique",
}

_PRIO_ICONS = {"high": "🔴", "medium": "🟡", "low": "🟢"}


def _humanize_concept(concept: str) -> str:
    """'magic_value::automatisation' → 'Valeur non documentée — "automatisation"'"""
    if "::" in concept:
        ftype, value = concept.split("::", 1)
        label = _TYPE_LABELS.get(ftype, ftype)
        return f'{label} — "{value}"'
    return concept


def _build_brief_markdown(entries: list[dict], domaine: str, titre: str = "") -> str:
    lines: list[str] = []

    lines.append(f"# Brief PO — {titre or domaine}")
    lines.append(f"{date.today().isoformat()} · {len(entries)} concept(s) à valider")
    lines.append("")

    # Synthèse par type
    from collections import Counter
    type_counts = Counter(e.get("flag_type", "?") for e in entries)
    prio_counts = Counter(e.get("priorite", "low") for e in entries)

    lines.append("| Type | Concepts | Priorité |")
    lines.append("|------|----------|---------|")
    TYPE_META = {
        "dynamic_session_key":      ("🔴", "Session dynamique"),
        "external_state_dependency":("🔴", "Dépendance externe"),
        "hardcoded_situation_code": ("🟡", "Code hardcodé"),
        "missing_branch":           ("🟡", "Branche manquante"),
        "magic_value":              ("🟡", "Valeur magique"),
    }
    for ftype, count in sorted(type_counts.items(),
                                key=lambda kv: TYPE_META.get(kv[0], ("🟢", kv[0]))[0]):
        icon, label = TYPE_META.get(ftype, ("⚪", ftype))
        lines.append(f"| {icon} {label} | {count} | — |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Sections par type
    SECTION_ORDER = [
        ("dynamic_session_key",      "🔴 SESSION DYNAMIQUE"),
        ("external_state_dependency","🔴 DÉPENDANCES EXTERNES"),
        ("hardcoded_situation_code", "🟡 CODES HARDCODÉS"),
        ("magic_value",              "🟡 VALEURS MAGIQUES"),
        ("missing_branch",           "🟡 BRANCHES MANQUANTES"),
    ]

    CLUSTER_A = {"magic_value", "hardcoded_situation_code"}

    for ftype, section_title in SECTION_ORDER:
        section_entries = [e for e in entries if e.get("flag_type") == ftype]
        if not section_entries:
            continue

        section_entries = sorted(section_entries, key=lambda e: -e.get("occurrences", 1))
        lines.append(f"## {section_title}")
        lines.append("")

        if ftype in CLUSTER_A:
            lines.append("| Valeur | Méthode(s) | ×N | Question | Réponse |")
            lines.append("|--------|-----------|-----|---------|---------|")
            for entry in section_entries:
                concept = entry.get("concept", "")
                value = concept.split("::", 1)[-1] if "::" in concept else concept
                fichiers = entry.get("fichiers", [])
                methods = ", ".join(f.split(":")[0] for f in fichiers[:2])
                q = entry.get("question", "").replace("|", "·")
                n = entry.get("occurrences", 1)
                lines.append(f"| `{value}` | {methods} | ×{n} | {q} |  |")
        else:
            lines.append("| Méthode | ×N | Question | Réponse |")
            lines.append("|---------|-----|---------|---------|")
            for entry in section_entries:
                concept = entry.get("concept", "")
                method = concept.split("::", 1)[-1] if "::" in concept else concept
                q = entry.get("question", "").replace("|", "·")
                n = entry.get("occurrences", 1)
                lines.append(f"| `{method}()` | ×{n} | {q} |  |")

        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("*Brief généré par **Rosetta***")
    return "\n".join(lines)


def cmd_export_brief(args: argparse.Namespace, kb_path: Path) -> int:
    pending = _load_pending(kb_path)

    domaine_filter = getattr(args, "domaine", None) or None
    prio_filter = getattr(args, "priorite", None) or None

    entries = list(pending.values())

    if domaine_filter:
        entries = [e for e in entries if e.get("domaine") == domaine_filter]
    if prio_filter:
        entries = [e for e in entries if e.get("priorite") == prio_filter]

    # Exclure les entrées déjà validées
    entries = [e for e in entries if not e.get("validated")]

    if not entries:
        print("(Aucune entrée pending correspondant aux filtres)")
        return 0

    domaine_label = domaine_filter or "tous domaines"
    md = _build_brief_markdown(entries, domaine=domaine_label)

    if getattr(args, "output", None):
        out = Path(args.output).expanduser()
        out.write_text(md, encoding="utf-8")
        print(f"[✓] Brief PO écrit dans {out} ({len(entries)} entrées)")
    else:
        print(md)
    return 0


# ---------------------------------------------------------------------------
# Commande : export-human
# ---------------------------------------------------------------------------

def _conf_badge(conf: str) -> str:
    return {"high": "✅ validé PO", "medium": "⚠️ inféré", "inferred": "🔍 non validé"}.get(conf, conf)


def _migration_badge(note: str) -> str:
    if not note:
        return ""
    note_l = note.lower()
    if note_l.startswith("non"):
        return "🟢 aucune"
    if note_l.startswith("partiel"):
        return "🟡 partielle"
    return "🔴 requise"


def _truncate(text: str, max_len: int = 120) -> str:
    text = (text or "").replace("\n", " ").strip()
    if len(text) <= max_len:
        return text
    cut = text.rfind(" ", 0, max_len)
    return (text[:cut] if cut > 0 else text[:max_len]) + "…"


def _first_sentence(text: str, max_len: int = 300) -> str:
    """Retourne la première phrase complète.

    Coupe sur [.!?] suivi d'un espace + majuscule (ou fin de texte) pour éviter
    de couper sur '1. ' dans les listes numérotées ou sur des abréviations.
    """
    text = (text or "").replace("\n", " ").strip()
    # Fin de phrase = ponctuation (non précédée d'un chiffre) suivie d'espace+majuscule ou fin de chaîne
    for m in re.finditer(r'(?<!\d)[.!?](?=\s+[A-ZÀ-Ÿ«"(]|\s*$)', text[:max_len + 60]):
        end = m.end()
        if end <= max_len:
            return text[:end].strip()
    if len(text) <= max_len:
        return text
    cut = text.rfind(" ", 0, max_len)
    return (text[:cut] if cut > 0 else text[:max_len]) + "…"


_BUG_SHORTCODES = {
    "critique": "🔴 Critique",
    "important": "🟠 Important",
    "moyen": "🟡 Moyen",
    "mineur": "🟡 Moyen",
}

_MIGRATION_BADGE_WORDS = {"non", "partiel", "requis"}


def _bug_severity(label: str, notes: str) -> str:
    combined = (label + " " + (notes or "")).lower()
    if "🔴" in combined or "critique" in combined:
        return "🔴 Critique"
    if "🟠" in combined or "important" in combined:
        return "🟠 Important"
    return "🟡 Moyen"


def cmd_export_human(args: argparse.Namespace, kb_path: Path) -> int:
    """Génère un document Markdown lisible humain pour une réunion (fusion, PO, etc.)."""
    kb_data = _load_kb(kb_path)
    pending  = _load_pending(kb_path)

    domaines_raw = getattr(args, "domaine", None) or ""
    domaines = [d.strip() for d in domaines_raw.split(",") if d.strip()] if domaines_raw else []

    def _in_scope(entry: dict) -> bool:
        if not domaines:
            return True
        return entry.get("domaine", "") in domaines

    # ── Collecte KB ──────────────────────────────────────────────────────────
    regles, bugs, codes = [], [], []
    for code, entry in (kb_data.get("regles") or {}).items():
        if not _in_scope(entry):
            continue
        label = entry.get("label", code)
        if label.startswith("[BUG]"):
            bugs.append((code, entry))
        else:
            regles.append((code, entry))

    for code, entry in (kb_data.get("codes") or {}).items():
        if _in_scope(entry):
            codes.append((code, entry))

    # ── Collecte pending ─────────────────────────────────────────────────────
    pending_items = [
        p for p in pending.values()
        if not p.get("validated") and _in_scope(p)
    ]
    PRIO = {"high": 0, "medium": 1, "low": 2}
    pending_items.sort(key=lambda p: PRIO.get(p.get("priorite", "low"), 9))

    # ── Séparation pending par type ───────────────────────────────────────────
    pending_decisions = [p for p in pending_items if p.get("pending_type") == 3]
    pending_new       = [p for p in pending_items if p.get("pending_type") == 2]
    pending_upgrade   = [p for p in pending_items if p.get("pending_type") == 1]

    titre_domaine = ", ".join(domaines) if domaines else "tous domaines"
    date_str = __import__("datetime").date.today().isoformat()

    lines = [
        f"# {titre_domaine} — Dossier de fusion",
        f"> Généré par **Rosetta** · {date_str} · "
        f"{len(regles)} règles · {len(codes)} codes · "
        f"{len(bugs)} bugs · {len(pending_items)} questions ouvertes",
        "",
        "---",
        "",
    ]

    # ── Section 1 : Règles métier ─────────────────────────────────────────────
    if regles:
        lines += [
            "## 1. Règles métier documentées",
            "",
            "| Règle | Comportement | Confiance | Migration |",
            "|-------|-------------|-----------|-----------|",
        ]
        for code, e in sorted(regles, key=lambda x: x[1].get("confiance", "z")):
            sem = _first_sentence(e.get("semantique", e.get("label", "")), 280)
            mig = _migration_badge(e.get("migration_note", ""))
            lines.append(f"| `{code}` | {sem} | {_conf_badge(e.get('confiance',''))} | {mig} |")
        lines += [""]

    # ── Section 2 : Codes et constantes ──────────────────────────────────────
    if codes:
        lines += [
            "## 2. Codes et constantes connus",
            "",
            "| Token | Label | Contexte | Confiance | Migration |",
            "|-------|-------|---------|-----------|-----------|",
        ]
        for code, e in sorted(codes, key=lambda x: x[1].get("confiance", "z")):
            label = e.get("label", "")
            ctx_list = e.get("contextes", [])
            ctx = ctx_list[0].get("semantique", ctx_list[0].get("champ", "")) if ctx_list else ""
            mig = _migration_badge(e.get("migration_note", ""))
            lines.append(f"| `{code}` | {_truncate(label, 70)} | {_truncate(ctx, 60)} | {_conf_badge(e.get('confiance',''))} | {mig} |")
        lines += [""]

    # ── Section 3 : Bugs ──────────────────────────────────────────────────────
    if bugs:
        lines += [
            "## 3. Bugs identifiés avant migration",
            "",
            "| Bug | Description | Sévérité |",
            "|-----|------------|---------|",
        ]
        for code, e in bugs:
            label = e.get("label", code).replace("[BUG] ", "")
            sev = _bug_severity(label, e.get("notes", ""))
            lines.append(f"| `{code}` | {_first_sentence(label, 120)} | {sev} |")
        lines += [""]

    # ── Section 4 : Questions ouvertes ────────────────────────────────────────
    if pending_items:
        lines += ["## 4. Questions ouvertes — Arbitrage requis", ""]

        def _prio_icon(p: str) -> str:
            return {"high": "🔴", "medium": "🟡", "low": "⚪"}.get(p, "")

        if pending_decisions:
            lines += [
                "### 4a. Décisions d'architecture / comportement",
                "",
                "| Priorité | Méthode | Question |",
                "|----------|---------|---------|",
            ]
            for p in pending_decisions:
                icon = _prio_icon(p.get("priorite", ""))
                method = (p.get("fichiers") or [""])[0].split(":")[0] if p.get("fichiers") else p.get("concept", "")
                q = (p.get("question", "") or "").replace("\n", " ").strip()
                lines.append(f"| {icon} {p.get('priorite','').upper()} | `{method}` | {q} |")
            lines += [""]

        if pending_new:
            lines += [
                "### 4b. Tokens non documentés — à capturer en KB",
                "",
                "| Priorité | Token / Concept | Question |",
                "|----------|----------------|---------|",
            ]
            for p in pending_new:
                icon = _prio_icon(p.get("priorite", ""))
                concept = p.get("concept", p.get("code", ""))
                q = (p.get("question", "") or "").replace("\n", " ").strip()
                lines.append(f"| {icon} {p.get('priorite','').upper()} | `{concept}` | {q} |")
            lines += [""]

        if pending_upgrade:
            lines += [
                "### 4c. Tokens en KB — à valider PO (confiance à monter)",
                "",
                "| Priorité | Token | Question |",
                "|----------|-------|---------|",
            ]
            for p in pending_upgrade:
                icon = _prio_icon(p.get("priorite", ""))
                q = (p.get("question", "") or "").replace("\n", " ").strip()
                lines.append(f"| {icon} {p.get('priorite','').upper()} | `{p.get('code','')}` | {q} |")
            lines += [""]

    # ── Section 5 : Notes migration ───────────────────────────────────────────
    migration_notes = [
        (code, e.get("migration_note", ""))
        for section in (regles, codes)
        for code, e in section
        if e.get("migration_note")
        and e["migration_note"].strip().lower() not in _MIGRATION_BADGE_WORDS
        and not e["migration_note"].lower().startswith("non")
    ]
    if migration_notes:
        lines += [
            "## 5. Notes de migration Symfony",
            "",
            "| Token | Migration | Note |",
            "|-------|-----------|------|",
        ]
        for code, note in migration_notes:
            lines.append(f"| `{code}` | {_migration_badge(note)} | {_first_sentence(note, 180)} |")
        lines += [""]

    lines += ["---", "", "*Document généré par **Rosetta** — outil d'audit statique PHP*"]

    md = "\n".join(lines)

    out_path = getattr(args, "output", None)
    if out_path:
        out = Path(out_path).expanduser()
        out.write_text(md, encoding="utf-8")
        print(f"[✓] Dossier écrit dans {out}")
        print(f"    {len(regles)} règles · {len(codes)} codes · {len(bugs)} bugs · {len(pending_items)} questions")
    else:
        print(md)
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
# Import docs Markdown → KB (cmd_import)
# ---------------------------------------------------------------------------

_IMPORT_TYPE_ROUTES: dict[str, tuple[str, ...]] = {
    "code":    ("codes",),
    "regle":   ("regles",),
    "bug":     ("regles",),
    "colonne": ("sql_artifacts", "colonnes"),
    "vue":     ("sql_artifacts", "vues"),
    "requete": ("sql_artifacts", "requetes"),
}
# _CONF_LEVEL défini dans la section export-prompt (plus haut)


def _import_extract_sections(content: str) -> dict[str, list[str]]:
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


def _import_text(lines: list[str]) -> str:
    return " ".join(l.strip() for l in lines if l.strip())


def _import_parse_table(lines: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in lines:
        line = line.strip()
        if not line.startswith("|") or re.match(r"^\|[-| ]+\|$", line):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) >= 2 and parts[0].lower() not in ("valeur", "colonne", "value", "clé", "code"):
            result[parts[0]] = parts[1]
    return result


def _import_parse_list(lines: list[str]) -> list[str]:
    result = []
    for line in lines:
        line = line.strip()
        if line.startswith(("- ", "* ", "+ ")):
            result.append(line[2:].strip())
        elif re.match(r"^\d+\.\s", line):
            result.append(re.sub(r"^\d+\.\s+", "", line).strip())
    return result


def _import_build_entry(kb_type: str, meta: dict, sections: dict) -> dict:
    """Construit une entrée KB depuis le frontmatter et les sections Markdown."""
    t = _import_text
    entry: dict[str, Any] = {}

    if "Label" in sections:
        entry["label"] = t(sections["Label"])
    sem_lines = sections.get("Semantique") or sections.get("Sémantique") or []
    if sem_lines:
        entry["semantique"] = t(sem_lines)

    if kb_type == "code":
        if meta.get("kb_domaine"):
            entry["domaine"] = meta["kb_domaine"]
        refs = _import_parse_list(sections.get("Trouvé dans", []))
        if refs:
            entry["contextes"] = [{"champ": r} for r in refs]

    elif kb_type in ("regle", "bug"):
        conds = _import_parse_list(sections.get("Conditions", []))
        if conds:
            entry["conditions"] = conds
        if meta.get("kb_domaine"):
            entry["domaine"] = meta["kb_domaine"]
        if kb_type == "bug":
            if "label" in entry and not entry["label"].startswith("[BUG]"):
                entry["label"] = "[BUG] " + entry["label"]
            sev_lines = sections.get("Sévérité", [])
            if sev_lines:
                entry.setdefault("notes", "")
                sev = _import_text(sev_lines)
                entry["notes"] = f"Sévérité: {sev}. " + entry.get("notes", "")
            refs = _import_parse_list(sections.get("Trouvé dans", []))
            if refs:
                entry["contextes"] = [{"champ": r} for r in refs]

    elif kb_type == "colonne":
        if meta.get("kb_table"):
            entry["table"] = meta["kb_table"]
        if meta.get("kb_type_oracle"):
            entry["type_oracle"] = meta["kb_type_oracle"]
        vals = _import_parse_table(sections.get("Valeurs", []))
        if vals:
            entry["valeurs"] = vals
        dists = _import_parse_table(sections.get("Distinctions", []))
        if dists:
            entry["distinctions"] = dists
        refs = _import_parse_list(sections.get("Trouvé dans", []))
        if refs:
            entry["trouvé_dans"] = refs

    elif kb_type == "vue":
        if meta.get("kb_tables"):
            entry["tables_source"] = [s.strip() for s in str(meta["kb_tables"]).split(",")]
        piege = sections.get("Piège", [])
        if piege:
            entry["piège_connu"] = t(piege)

    elif kb_type == "requete":
        if meta.get("kb_fichier"):
            entry["fichier_source"] = meta["kb_fichier"]
        if meta.get("kb_lignes"):
            entry["lignes"] = meta["kb_lignes"]
        consts = _import_parse_table(sections.get("Constantes", []))
        if consts:
            entry["constantes_magiques"] = consts
        concepts = _import_parse_list(sections.get("Concepts", []))
        if concepts:
            entry["concepts_métier"] = concepts

    if meta.get("kb_migration"):
        entry["migration_note"] = meta["kb_migration"]
    note_lines = sections.get("Notes", [])
    if note_lines:
        note = t(note_lines)
        if note and note.lower() not in ("aucune.", "aucune", "none", "~"):
            entry["notes"] = note

    entry["source"] = meta.get("kb_source", "kb_import — généré")
    entry["confiance"] = "medium"
    return entry


def cmd_import(args: argparse.Namespace, kb_path: Path) -> int:
    """Importe des fiches .md (frontmatter kb_type) dans le KB YAML."""
    try:
        import frontmatter as _fm
    except ImportError:
        print("Erreur : python-frontmatter requis — pip install python-frontmatter")
        return 1

    docs_dir = Path(args.docs_dir).expanduser().resolve()
    if not docs_dir.exists():
        print(f"Erreur : dossier introuvable : {docs_dir}")
        return 1

    dry_run: bool = getattr(args, "dry_run", False)
    added = updated = ignored = errors = 0
    messages: list[str] = []

    # Collecter et parser tous les .md, grouper par domaine
    by_domain: dict[str, list[tuple[tuple[str, ...], str, dict, str]]] = {}

    for md_path in sorted(docs_dir.rglob("*.md")):
        try:
            post = _fm.loads(md_path.read_text(encoding="utf-8-sig"))
        except Exception as e:
            errors += 1
            messages.append(f"[E] {md_path.name} — frontmatter : {e}")
            continue

        meta = dict(post.metadata)
        kb_type = meta.get("kb_type", "").strip().lower()
        kb_nom = meta.get("kb_nom", "").strip()

        if not kb_type:
            continue  # pas un fichier KB — ignorer
        if kb_type not in _IMPORT_TYPE_ROUTES:
            errors += 1
            messages.append(f"[E] {md_path.name} — kb_type inconnu : '{kb_type}'")
            continue
        if not kb_nom:
            errors += 1
            messages.append(f"[E] {md_path.name} — kb_nom manquant")
            continue

        domain = str(meta.get("kb_domaine") or "commun")
        sections = _import_extract_sections(post.content)
        try:
            entry = _import_build_entry(kb_type, meta, sections)
        except Exception as e:
            errors += 1
            messages.append(f"[E] {md_path.name} — construction entrée : {e}")
            continue

        route = _IMPORT_TYPE_ROUTES[kb_type]
        by_domain.setdefault(domain, []).append((route, kb_nom, entry, md_path.name))

    if not by_domain and not errors:
        print(f"Aucun fichier KB (.md avec kb_type) trouvé dans {docs_dir}")
        return 0

    # Écrire domaine par domaine
    for domain, entries in sorted(by_domain.items()):
        data = _load_for_write(kb_path, domain)
        domain_added = domain_updated = False
        for route, nom, entry, fname in entries:
            node = data
            for key in route:
                node = node.setdefault(key, {})
            existing = node.get(nom)
            if existing is None:
                node[nom] = entry
                added += 1
                domain_added = True
                messages.append(f"[+] {nom} ({fname})")
            elif _CONF_LEVEL.get(existing.get("confiance", "inferred"), 0) >= 2:
                ignored += 1
                messages.append(f"[!] {nom} ignoré — confiance high existante ({fname})")
            else:
                node[nom] = entry
                updated += 1
                domain_updated = True
                messages.append(f"[~] {nom} mis à jour ({fname})")
        if not dry_run and (domain_added or domain_updated):
            _save_for_write(kb_path, data, domain)

    prefix = "[dry-run] " if dry_run else ""
    print(f"{prefix}{added} ajoutée(s), {updated} mise(s) à jour, "
          f"{ignored} ignorée(s) (high existant), {errors} erreur(s)")
    for msg in messages:
        print(f"  {msg}")
    return 1 if errors else 0


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

    # ── import ────────────────────────────────────────────────────────────────
    p = sub.add_parser("import", help="Importer des fiches .md (frontmatter kb_type) dans le KB")
    p.add_argument(
        "docs_dir",
        help="Dossier contenant les fiches .md avec frontmatter kb_type",
    )
    p.add_argument(
        "--dry-run", action="store_true",
        help="Simuler l'import sans écrire le KB",
    )

    # ── export-prompt ─────────────────────────────────────────────────────────
    p = sub.add_parser("export-prompt", help="Exporter le KB au format compact pour injection LLM")
    p.add_argument("--domaine", help="Filtrer par domaine (ex: ticketing, sav)")
    p.add_argument(
        "--confiance", default="medium", choices=["high", "medium", "inferred"],
        help="Confiance minimale à inclure (défaut: medium)",
    )
    p.add_argument(
        "--max-chars", type=int, default=4000,
        help="Limite en caractères du bloc généré (défaut: 4000)",
    )
    p.add_argument("--output", help="Fichier de sortie (défaut: stdout)")

    # ── export-brief ──────────────────────────────────────────────────────────
    p = sub.add_parser("export-brief", help="Générer un brief PO à partir du pending_validation")
    p.add_argument("--domaine", help="Filtrer par domaine (ex: demande-intervention)")
    p.add_argument(
        "--priorite", choices=["high", "medium", "low"],
        help="Filtrer par priorité (défaut: toutes)",
    )
    p.add_argument("--output", help="Fichier de sortie .md (défaut: stdout)")

    # ── export-human ──────────────────────────────────────────────────────────
    p = sub.add_parser("export-human", help="Dossier lisible humain : règles + bugs + questions (réunion, fusion)")
    p.add_argument("--domaine", required=True,
                   help="Domaine(s) à exporter, séparés par virgule (ex: RetablirCloturerController)")
    p.add_argument("--output", help="Fichier de sortie .md (défaut: stdout)")

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
    "import":          cmd_import,
    "export-prompt":   cmd_export_prompt,
    "export-brief":    cmd_export_brief,
    "export-human":    cmd_export_human,
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
