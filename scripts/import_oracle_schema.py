#!/usr/bin/env python3
"""
import_oracle_schema.py — Importe le schéma Oracle dans le KB en DEUX couches.

Une seule passe d'extraction (le TSV), DEUX fichiers de sortie, MÊME timestamp
source — sinon inventaire et détail divergent à la première évolution de schéma.

  Couche 1 « inventaire » (résidente)  → section ``schema:`` du domaine KB
      (une entrée par table : rôle métier court, PK, nb colonnes). Chargée en
      permanence dans le prompt → garantit l'exhaustivité au niveau table.
  Couche 2 « détail » (à la demande)    → sidecar ``oracle_schema/detail.yaml``
      hors du répertoire KB → jamais mergé → jamais résident. Colonnes avec
      type / nullable / PK / FK, interrogé par nom de table.

Formats TSV acceptés (auto-détectés au nombre de colonnes, sans en-tête) :

  • DÉGRADÉ (8 col, ALL_TAB_COLUMNS seul — export actuel) :
      TABLE, COLUMN, DATA_TYPE, DATA_LENGTH, DATA_PRECISION, DATA_SCALE,
      NULLABLE, COLUMN_ID
    → PK/FK inconnus → marqueur ``non_extrait`` (JAMAIS omis : « pas de PK »
      confirmé ≠ « pas encore extrait »).

  • ENRICHI (12 col, jointure ALL_CONSTRAINTS + ALL_*_COMMENTS) :
      TABLE, TABLE_COMMENT, COLUMN, COLUMN_COMMENT, DATA_TYPE, DATA_LENGTH,
      DATA_PRECISION, DATA_SCALE, NULLABLE, COLUMN_ID, IS_PK(Y/vide),
      FK_REF_TABLE(vide/table)
    → rôle métier = TABLE_COMMENT, PK/FK réels. Le taux de remplissage des
      commentaires est reporté en fin d'import.

La ré-extraction enrichie n'est PAS sur le chemin critique : ce script tourne
tel quel sur le TSV dégradé et se met à niveau seul dès que l'enrichi arrive.

Régénération par écrasement : le fichier domaine ``schema_oracle.yaml`` est
supprimé puis reconstruit (pas de tables fantômes), et le sidecar détail est
réécrit en entier.

Usage :
    python3 scripts/import_oracle_schema.py \
        --tsv "~/rosetta-data/schema bd.txt" \
        --kb-path ~/rosetta-data/kb
    python3 scripts/import_oracle_schema.py --tsv <fichier> --dry-run
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import OrderedDict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from services.kb_service import KBService  # noqa: E402

DEGRADED_COLS = 8
ENRICHED_COLS = 12
DEFAULT_DOMAIN = "schema_oracle"
ROLE_MAX = 60  # rôle métier borné : 255 libellés × longueur → budget résident maîtrisé


def _truncate_role(comment: str) -> str:
    """Borne le rôle métier à ROLE_MAX caractères (inventaire résident compact)."""
    c = " ".join(comment.split())
    return c if len(c) <= ROLE_MAX else c[: ROLE_MAX - 1].rstrip() + "…"


def _fmt_oracle_type(dtype: str, length: str, precision: str, scale: str) -> str:
    """Reconstruit le type Oracle lisible : NUMBER(22,4), VARCHAR2(4000), DATE…"""
    dtype = (dtype or "").strip()
    precision, scale, length = precision.strip(), scale.strip(), length.strip()
    if precision:
        return f"{dtype}({precision},{scale})" if scale and scale != "0" else f"{dtype}({precision})"
    if length and dtype in ("VARCHAR2", "CHAR", "NVARCHAR2", "NCHAR", "RAW", "VARCHAR"):
        return f"{dtype}({length})"
    return dtype


def _nullable(flag: str) -> bool:
    return (flag or "").strip().upper() != "N"


def parse_tsv(path: Path) -> tuple[OrderedDict, bool, int]:
    """Parse le TSV → (tables ordonnées, enrichi?, nb_tables_avec_role).

    ``tables`` = {TABLE: {"role": str|None, "pk": list, "fk": {col:ref},
                          "colonnes": OrderedDict{COL: {type, nullable}}}}
    ``pk``/``fk`` valent None en mode dégradé (→ traduit en ``non_extrait``).
    """
    tables: "OrderedDict[str, dict]" = OrderedDict()
    enriched = False
    roles_filled = 0

    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            row = [c.strip() for c in row]
            if not row or not row[0]:
                continue
            if len(row) >= ENRICHED_COLS:
                enriched = True
                (tbl, tcomment, col, ccomment, dtype, length, prec, scale,
                 nullable, col_id, is_pk, fk_ref) = row[:ENRICHED_COLS]
            elif len(row) >= DEGRADED_COLS:
                (tbl, col, dtype, length, prec, scale, nullable, col_id) = row[:DEGRADED_COLS]
                tcomment = ccomment = is_pk = fk_ref = ""
            else:
                continue  # ligne mal formée : ignorée silencieusement

            t = tables.get(tbl)
            if t is None:
                t = {
                    "role": None,
                    "pk": [] if enriched else None,
                    "fk": {} if enriched else None,
                    "colonnes": OrderedDict(),
                }
                tables[tbl] = t

            if enriched:
                if tcomment and t["role"] is None:
                    t["role"] = _truncate_role(tcomment)
                    roles_filled += 1
                if is_pk.strip().upper() == "Y":
                    t["pk"].append(col)
                if fk_ref.strip():
                    t["fk"][col] = fk_ref.strip()

            cdef: dict = {
                "type": _fmt_oracle_type(dtype, length, prec, scale),
                "nullable": _nullable(nullable),
            }
            if enriched and ccomment.strip():
                cdef["commentaire"] = ccomment.strip()
            t["colonnes"][col] = cdef

    return tables, enriched, roles_filled


def build_detail(tables: OrderedDict, enriched: bool) -> dict:
    """Couche 2 : {TABLE: {pk, fk, colonnes}}. Marqueurs explicites si dégradé."""
    detail: dict = {}
    for tbl, t in tables.items():
        detail[tbl] = {
            "pk": t["pk"] if enriched else KBService.PK_UNKNOWN,
            "fk": t["fk"] if enriched else KBService.PK_UNKNOWN,
            "colonnes": dict(t["colonnes"]),
        }
    return detail


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tsv", required=True, help="Export TSV Oracle (dégradé 8 col ou enrichi 12 col)")
    ap.add_argument("--kb-path", default="~/rosetta-data/kb", help="Répertoire KB (défaut ~/rosetta-data/kb)")
    ap.add_argument("--domain", default=DEFAULT_DOMAIN, help="Domaine KB cible (défaut schema_oracle)")
    ap.add_argument("--source-date", default=str(date.today()),
                    help="Date d'export du schéma (YYYY-MM-DD) — MÊME pour les 2 couches")
    ap.add_argument("--dry-run", action="store_true", help="N'écrit rien, affiche le résumé")
    args = ap.parse_args()

    tsv_path = Path(args.tsv).expanduser()
    kb_path = Path(args.kb_path).expanduser()
    if not tsv_path.exists():
        print(f"[ERREUR] TSV introuvable : {tsv_path}", file=sys.stderr)
        return 1

    tables, enriched, roles_filled = parse_tsv(tsv_path)
    if not tables:
        print(f"[ERREUR] Aucune table lue depuis {tsv_path}", file=sys.stderr)
        return 1

    n_tables = len(tables)
    n_cols = sum(len(t["colonnes"]) for t in tables.values())
    mode = "ENRICHI (contraintes + commentaires)" if enriched else "DÉGRADÉ (colonnes seules, PK/FK = non_extrait)"
    source = (
        f"Oracle ALL_TAB_COLUMNS{'+CONSTRAINTS+COMMENTS' if enriched else ''} "
        f"— export {args.source_date}"
    )

    print(f"── Import schéma Oracle — mode {mode}")
    print(f"   {n_tables} tables, {n_cols} colonnes")
    print(f"   source (identique couches 1 & 2) : {source}")
    if enriched:
        pct = 100 * roles_filled // n_tables if n_tables else 0
        print(f"   rôle métier rempli (TABLE_COMMENT) : {roles_filled}/{n_tables} ({pct}%)")
        if pct < 20:
            print("   ⚠️  < 20 % : commentaires trop rares — envisager de laisser "
                  "l'inventaire à nom+PK et enrichir le rôle à la main au portage.")

    if args.dry_run:
        sample = list(tables)[:5]
        print(f"   [dry-run] aucune écriture. Échantillon tables : {', '.join(sample)}")
        return 0

    # Régénération par écrasement : on repart d'un fichier domaine propre.
    domain_file = kb_path / f"{args.domain}.yaml"
    if domain_file.exists():
        domain_file.unlink()

    svc = KBService(kb_path)

    # ── Couche 1 : inventaire résident (une entrée par table) ────────────────
    created = 0
    for tbl, t in tables.items():
        pk_val = t["pk"] if enriched else KBService.PK_UNKNOWN
        res = svc.capture_schema(
            table=tbl, role=t["role"], pk=pk_val,
            nb_colonnes=len(t["colonnes"]), domain=args.domain,
            source=source, confiance="high", force=True,
        )
        if res.success:
            created += 1

    # ── Couche 2 : détail sidecar (réécrit en entier) ────────────────────────
    detail = build_detail(tables, enriched)
    n_detail = svc.write_schema_detail(detail, source=source)

    print(f"── Écrit :")
    print(f"   couche 1 (inventaire, résident) : {created} tables → {domain_file}")
    print(f"   couche 2 (détail, à la demande) : {n_detail} tables → {svc._schema_detail_path()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
