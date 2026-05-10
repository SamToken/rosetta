#!/usr/bin/env python3
"""Rosetta — Migration historique JSONL → SQLite.

Relit roi_metrics.jsonl et injecte les entrées comme jobs "success" dans la DB SQLite.
Idempotent : si la DB existe déjà, les entrées existantes sont ignorées (ON CONFLICT IGNORE).

Usage :
    cd ~/projects/rosetta
    .venv/bin/python3 scripts/migrate_jsonl_to_sqlite.py
    .venv/bin/python3 scripts/migrate_jsonl_to_sqlite.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def main() -> None:
    parser = argparse.ArgumentParser(description="Migration roi_metrics.jsonl → SQLite")
    parser.add_argument("--dry-run", action="store_true", help="Afficher sans écrire")
    args = parser.parse_args()

    jsonl_path = Path(
        os.environ.get("ROSETTA_ROI_METRICS", "~/rosetta-data/roi_metrics.jsonl")
    ).expanduser()

    if not jsonl_path.exists():
        print(f"Aucun fichier JSONL trouvé : {jsonl_path}")
        sys.exit(0)

    lines = [ln for ln in jsonl_path.read_text().splitlines() if ln.strip()]
    print(f"📂 {len(lines)} entrée(s) dans {jsonl_path}")

    if args.dry_run:
        for line in lines[:5]:
            print("  ", line[:120])
        if len(lines) > 5:
            print(f"  ... ({len(lines) - 5} de plus)")
        print("Mode --dry-run : aucune écriture.")
        return

    # Import après le dry-run check pour éviter d'initialiser la DB inutilement
    from api.database import create_tables, get_session
    from api.models import Job

    create_tables()

    inserted = skipped = errors = 0

    for line in lines:
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            print(f"⚠  JSONDecodeError : {exc}")
            errors += 1
            continue

        ts = row.get("timestamp", "")
        filename = row.get("filename", "unknown")
        status = row.get("status", "success")
        cost = row.get("llm_cost_usd", 0.0)
        lines_count = row.get("file_size_lines", 0)
        proc_time = row.get("processing_time_seconds", 0.0)

        result_payload = json.dumps({
            "total_files": 1,
            "total_insights": row.get("insights_total", 0),
            "total_cost_usd": cost,
            "processing_time_seconds": proc_time,
            "health_score": None,
            "output_dir": "",
            "files": [
                {
                    "filename": filename,
                    "file_size_lines": lines_count,
                    "processing_time_seconds": proc_time,
                    "flags_total": row.get("flags_total", 0),
                    "insights_total": row.get("insights_total", 0),
                    "llm_cost_usd": cost,
                    "status": status,
                }
            ],
        })

        job_id = str(uuid.uuid4())

        with get_session() as session:
            job = Job(
                id=job_id,
                status=status if status in ("success", "error", "queued", "running") else "success",
                created_at=ts or "1970-01-01T00:00:00+00:00",
                started_at=ts or None,
                finished_at=ts or None,
                result_json=result_payload,
            )
            session.add(job)
            try:
                session.commit()
                inserted += 1
            except Exception as exc:
                session.rollback()
                print(f"⚠  Insertion ignorée ({filename}) : {exc}")
                skipped += 1

    print(f"✅ Migration terminée : {inserted} insérée(s), {skipped} ignorée(s), {errors} erreur(s)")


if __name__ == "__main__":
    main()
