"""
rosetta_kb.py — CLI Knowledge Base Rosetta v3 (thin client)
=============================================================
Toute la logique métier est dans services/kb_service.py.
Ce fichier : parsing des arguments + affichage console.

--kb-path accepte :
  • un fichier YAML   → ~/rosetta-data/knowledge_base.yaml  (mode legacy)
  • un répertoire     → ~/rosetta-data/kb/                  (mode multi-domaine)

Variable d'environnement : ROSETTA_KB=~/rosetta-data/kb
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))

from services.kb_service import (
    CONFIDENCE_LABELS,
    KBService,
    format_kb_for_prompt,
    normalize_domain,
)

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

DEFAULT_KB_PATH = os.environ.get("ROSETTA_KB", "~/rosetta-data/kb")


# ---------------------------------------------------------------------------
# Helpers CLI
# ---------------------------------------------------------------------------

def _resolve_kb(kb_path_arg: str) -> Path:
    return Path(kb_path_arg).expanduser().resolve()


def _domain_of(args: argparse.Namespace) -> str:
    raw = getattr(args, "domaine", None)
    if not raw:
        return "commun"
    return normalize_domain(raw)


# ---------------------------------------------------------------------------
# Backward compat API (importée par audit_service.py / llm_enricher.py)
# ---------------------------------------------------------------------------

def lookup_for_enricher(token: str, kb_path: str | None = None) -> dict[str, Any]:
    """Wrapper backward compat — délègue à KBService."""
    path = Path(kb_path or DEFAULT_KB_PATH).expanduser().resolve()
    return KBService(path).lookup_for_enricher(token)


# ---------------------------------------------------------------------------
# Commandes (thin handlers : args → KBService → print)
# ---------------------------------------------------------------------------

def cmd_capture(args: argparse.Namespace, svc: KBService) -> int:
    result = svc.capture(
        code=args.code, label=args.label, source=args.source,
        confiance=args.confiance, domain=_domain_of(args),
        champ=getattr(args, "champ", None),
        table=getattr(args, "table", None),
        lie_a=getattr(args, "lie_a", None),
        notes=getattr(args, "notes", None),
        force=getattr(args, "force", False),
    )
    if result.action == "skipped_high":
        print(f"[!] '{result.code}' existe déjà avec confiance high. Utilisez --force pour écraser.")
        return 1
    suffix = f"→ {result.file_path}" if result.file_path else ""
    print(f"[+] Code '{result.code}' capturé (confiance: {result.confiance}) {suffix}".strip())
    return 0


def cmd_lookup(args: argparse.Namespace, svc: KBService) -> int:
    result = svc.lookup(args.code)

    if not result.found:
        if args.json:
            print(json.dumps({"found": False, "code": args.code}, ensure_ascii=False))
        else:
            print(f"[?] '{args.code}' introuvable dans le KB.")
        return 1

    if args.json:
        print(json.dumps(result.to_json_dict(), ensure_ascii=False, indent=2))
        return 0

    entry = result.entry
    conf = entry.get("confiance", "?")
    print(f"\n{'='*60}")
    print(f"  {args.code}  [{conf.upper()}]")
    print(f"  Section : {result.section}")
    print(f"{'='*60}")
    print(f"  Label    : {entry.get('label', '—')}")
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


def cmd_pending(args: argparse.Namespace, svc: KBService) -> int:
    items = svc.list_pending(priorite=getattr(args, "priorite", None))

    if not items:
        pf = getattr(args, "priorite", None)
        if pf:
            print(f"Aucune question avec priorité '{pf}'.")
        else:
            print("Aucune question en attente de validation PO.")
        return 0

    print(f"\n{'─'*60}")
    print(f"  FILE PO — {len(items)} question(s) en attente")
    print(f"{'─'*60}")
    for item in items:
        suffix = f"  [{item.domaine}]" if item.domaine else ""
        print(f"\n  {item.id}  [{item.priorite.upper()}]  {item.code}{suffix}")
        print(f"  Q: {item.question}")
        if item.fichiers:
            print(f"  Dans: {', '.join(item.fichiers)}")
    print()
    return 0


def cmd_validate(args: argparse.Namespace, svc: KBService) -> int:
    result = svc.validate_pending(
        pending_id=args.id,
        label=getattr(args, "label", None),
        source=getattr(args, "source", None),
        notes=getattr(args, "notes", None),
        domaine=getattr(args, "domaine", None),
    )
    if not result.success:
        print(f"[!] {result.error}")
        return 1
    print(f"[✓] {result.pending_id} validé — '{result.code}' {result.action} avec confiance high (domaine: {result.domain}).")
    return 0


def cmd_add_pending(args: argparse.Namespace, svc: KBService) -> int:
    result = svc.add_pending(
        code=args.code, question=args.question,
        priorite=args.priorite,
        fichiers=getattr(args, "fichiers", None),
        kb_type=getattr(args, "kb_type", None),
        domaine=getattr(args, "domaine", None),
    )
    print(f"[+] {result.pending_id} — '{result.code}' ajouté en pending (priorité: {result.priorite}) [{result.destination}]")
    return 0


def cmd_capture_colonne(args: argparse.Namespace, svc: KBService) -> int:
    result = svc.capture_colonne(
        nom=args.nom, label=args.label, domain=_domain_of(args),
        table=getattr(args, "table", None),
        type_oracle=getattr(args, "type_oracle", None),
        semantique=getattr(args, "semantique", None),
        valeurs=getattr(args, "valeurs", None),
        distinctions=getattr(args, "distinctions", None),
        trouve_dans=getattr(args, "trouve_dans", None),
        migration=getattr(args, "migration", None),
        source=getattr(args, "source", None),
        confiance=args.confiance,
        force=getattr(args, "force", False),
    )
    if result.action == "skipped_high":
        print(f"[!] '{result.code}' existe déjà avec confiance high. Utilisez --force pour écraser.")
        return 1
    print(f"[+] Colonne '{result.code}' capturée (confiance: {result.confiance})")
    return 0


def cmd_capture_vue(args: argparse.Namespace, svc: KBService) -> int:
    result = svc.capture_vue(
        nom=args.nom, label=args.label, domain=_domain_of(args),
        semantique=getattr(args, "semantique", None),
        tables=getattr(args, "tables", None),
        piege=getattr(args, "piege", None),
        migration=getattr(args, "migration", None),
        source=getattr(args, "source", None),
        confiance=args.confiance,
        force=getattr(args, "force", False),
    )
    if result.action == "skipped_high":
        print(f"[!] '{result.code}' existe déjà avec confiance high. Utilisez --force pour écraser.")
        return 1
    print(f"[+] Vue '{result.code}' capturée (confiance: {result.confiance})")
    return 0


def cmd_capture_requete(args: argparse.Namespace, svc: KBService) -> int:
    try:
        result = svc.capture_requete(
            nom=args.nom, label=getattr(args, "label", None), domain=_domain_of(args),
            fichier=getattr(args, "fichier", None),
            lignes=getattr(args, "lignes", None),
            semantique=getattr(args, "semantique", None),
            constantes=getattr(args, "constantes", None),
            concepts=getattr(args, "concepts", None),
            index=getattr(args, "index", None),
            risque=getattr(args, "risque", None),
            migration=getattr(args, "migration", None),
            notes=getattr(args, "notes", None),
            source=getattr(args, "source", None),
            confiance=args.confiance,
            force=getattr(args, "force", False),
        )
    except ValueError as exc:
        print(f"[!] {exc}")
        return 1
    if result.action == "skipped_high":
        print(f"[!] '{result.code}' existe déjà avec confiance high. Utilisez --force pour écraser.")
        return 1
    print(f"[+] Requête '{result.code}' capturée (confiance: {result.confiance})")
    return 0


def cmd_stats(args: argparse.Namespace, svc: KBService) -> int:
    s = svc.stats()
    mode = f" [{len(s.files)} fichiers]" if s.is_dir else ""
    print(f"\n{'='*55}")
    print(f"  ROSETTA KB — {s.projet}  v{s.version}{mode}")
    print(f"  Mis à jour : {s.last_updated}  |  {s.maintainer}")
    print(f"{'='*55}")
    print(f"  SECTIONS")
    print(f"  {'Codes métier':<28} {s.codes:>5}")
    print(f"  {'Règles':<28} {s.regles:>5}")
    print(f"  {'Schéma':<28} {s.schema:>5}")
    print(f"  {'Colonnes Oracle':<28} {s.colonnes:>5}")
    print(f"  {'Vues Oracle':<28} {s.vues:>5}")
    print(f"  {'Requêtes complexes':<28} {s.requetes:>5}")
    print(f"  {'─'*35}")
    print(f"  {'TOTAL entrées':<28} {s.total:>5}")
    print(f"\n  CONFIANCE")
    print(f"  [HIGH]   validé PO           {s.high:>5}")
    print(f"  [MEDIUM] inféré/Copilot      {s.medium:>5}")
    print(f"  [INF]    non validé           {s.inferred:>5}")
    if s.files:
        print(f"\n  FICHIERS")
        for fe in s.files:
            if fe.is_global:
                print(f"  _global.yaml   ({fe.count} pending)")
            else:
                print(f"  {fe.name:<28} {fe.count:>3} entrées")
    if s.pending_total:
        print(f"\n  FILE PO ({s.pending_total} questions — {s.pending_high} haute priorité)")
    else:
        print(f"\n  File PO : vide")
    print()
    return 0


def cmd_search(args: argparse.Namespace, svc: KBService) -> int:
    results = svc.search(args.texte)
    if not results:
        print(f"Aucun résultat pour '{args.texte}'.")
        return 0
    print(f"\n{len(results)} résultat(s) pour '{args.texte}' :\n")
    for r in results:
        conf = r.entry.get("confiance", "?")
        label = r.entry.get("label", "—")
        print(f"  {CONFIDENCE_LABELS.get(conf, '[?]  ')}  {r.nom:<30}  {label}")
        print(f"             └─ {r.section}")
    print()
    return 0


def cmd_export(args: argparse.Namespace, svc: KBService) -> int:
    output = svc.export_markdown()
    if args.output:
        out_path = Path(args.output).expanduser()
        out_path.write_text(output, encoding="utf-8")
        print(f"[✓] Export écrit dans {out_path}")
    else:
        print(output)
    return 0


def cmd_export_prompt(args: argparse.Namespace, svc: KBService) -> int:
    domaine = getattr(args, "domaine", None) or None
    confiance_min = getattr(args, "confiance", "medium") or "medium"
    max_chars = int(getattr(args, "max_chars", 4000) or 4000)
    block = svc.export_prompt(domaine=domaine, confiance_min=confiance_min, max_chars=max_chars)
    if not block:
        print("(KB vide ou aucune entrée ne correspond aux filtres)")
        return 0
    if args.output:
        out = Path(args.output).expanduser()
        out.write_text(block, encoding="utf-8")
        print(f"[✓] Prompt KB écrit dans {out} ({len(block)} caractères)")
    else:
        print(block)
    return 0


def cmd_export_brief(args: argparse.Namespace, svc: KBService) -> int:
    md = svc.export_brief(
        domaine=getattr(args, "domaine", None) or None,
        priorite=getattr(args, "priorite", None) or None,
    )
    if not md:
        print("(Aucune entrée pending correspondant aux filtres)")
        return 0
    if getattr(args, "output", None):
        out = Path(args.output).expanduser()
        out.write_text(md, encoding="utf-8")
        print(f"[✓] Brief PO écrit dans {out}")
    else:
        print(md)
    return 0


def cmd_export_human(args: argparse.Namespace, svc: KBService) -> int:
    domaines_raw = getattr(args, "domaine", None) or ""
    domaines = [d.strip() for d in domaines_raw.split(",") if d.strip()] if domaines_raw else []
    sources_raw = getattr(args, "sources", None) or ""
    sources = [s.strip() for s in sources_raw.split(",") if s.strip()] if sources_raw else []

    md = svc.export_human(domaines=domaines, sources=sources)
    if getattr(args, "output", None):
        out = Path(args.output).expanduser()
        out.write_text(md, encoding="utf-8")
        print(f"[✓] Dossier écrit dans {out}")
    else:
        print(md)
    return 0


def cmd_split(args: argparse.Namespace, svc: KBService) -> int:
    source = Path(args.source).expanduser().resolve()
    try:
        result = svc.split(source)
    except (FileNotFoundError, ValueError) as exc:
        print(f"[!] {exc}")
        return 1
    print(f"  → _global.yaml  (meta + {result.pending_count} pending)")
    for domain, n in result.domains:
        print(f"  → {domain}.yaml  ({n} entrées)")
    print(f"\n[✓] {len(result.domains)} fichier(s) domaine + _global.yaml créés dans {result.output_dir}/")
    print(f"    {result.total_entries} entrées migrées.")
    print(f"\n  Mettre à jour ROSETTA_KB='{result.output_dir}' dans votre shell.")
    return 0


def cmd_import(args: argparse.Namespace, svc: KBService) -> int:
    docs_dir = Path(args.docs_dir).expanduser().resolve()
    try:
        result = svc.import_docs(docs_dir, dry_run=getattr(args, "dry_run", False))
    except ImportError as exc:
        print(f"Erreur : {exc}")
        return 1
    except FileNotFoundError as exc:
        print(f"Erreur : {exc}")
        return 1

    prefix = "[dry-run] " if getattr(args, "dry_run", False) else ""
    print(f"{prefix}{result.added} ajoutée(s), {result.updated} mise(s) à jour, "
          f"{result.ignored} ignorée(s) (high existant), {result.errors} erreur(s)")
    for msg in result.messages:
        print(f"  {msg}")
    return 1 if result.errors else 0


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
    p.add_argument("--sources",
                   help="Fichiers PHP sources cités en haut du document, séparés par virgule")
    p.add_argument("--output", help="Fichier de sortie .md (défaut: stdout)")

    return parser


# ---------------------------------------------------------------------------
# Dispatch
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

    svc = KBService(kb_path)
    return handler(args, svc)


if __name__ == "__main__":
    sys.exit(main())
