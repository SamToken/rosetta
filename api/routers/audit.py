"""Rosetta API — Router /audit (jobs d'analyse PHP).

Pattern :
    POST /audit/start  → crée un job (HTTP 202), lance en BackgroundTask
    GET  /audit/       → liste tous les jobs
    GET  /audit/roi    → dashboard ROI (métriques cumulées)
    GET  /audit/{id}   → état d'un job

Les appels bloquants (AuditPipeline) sont délégués à asyncio.to_thread
pour ne pas bloquer l'event loop.
"""
from __future__ import annotations

import asyncio
import traceback
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query

from api.schemas import (
    AuditFileSummary,
    AuditJobResult,
    AuditStartRequest,
    JobCreatedResponse,
    JobStatusResponse,
    ROIDayResponse,
    ROISummaryResponse,
)
from services.audit_service import AuditOptions, AuditPipeline

router = APIRouter(prefix="/audit", tags=["Audit"])

# =============================================================================
# Job store en mémoire
# =============================================================================

_JOB_STORE: dict[str, dict[str, Any]] = {}


def _job_output_dir(job_id: str) -> Path:
    import os
    base = Path(os.environ.get("ROSETTA_API_OUTPUT", "~/rosetta-data/api_jobs")).expanduser()
    return base / job_id


# =============================================================================
# Tâche de fond (async → asyncio.to_thread pour le pipeline synchrone)
# =============================================================================

async def _execute_audit_job(
    job_id: str,
    php_files: list[Path],
    output_dir: Path,
    options: AuditOptions,
) -> None:
    """Lance AuditPipeline dans un thread pool et met à jour le job store."""
    logs: list[str] = _JOB_STORE[job_id]["logs"]

    _JOB_STORE[job_id]["status"] = "running"
    _JOB_STORE[job_id]["started_at"] = datetime.now(timezone.utc).isoformat()

    pipeline = AuditPipeline(options, progress=logs.append)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # setup() indexe le call graph et charge le KB context — bloquant
        await asyncio.to_thread(pipeline.setup)

        # run_batch() est le coeur du pipeline — bloquant (LLM, génération docs)
        batch = await asyncio.to_thread(pipeline.run_batch, php_files, output_dir)

        files_summary = [
            AuditFileSummary(
                filename=r.php_path.name,
                file_size_lines=r.file_size_lines,
                processing_time_seconds=r.processing_time_seconds,
                flags_total=len(r.ir.flags),
                insights_total=len(r.ir.llm_insights),
                llm_cost_usd=r.llm_cost_usd,
                status=r.status,
            )
            for r in batch.results
        ]

        _JOB_STORE[job_id]["result"] = AuditJobResult(
            total_files=len(batch.php_paths),
            total_insights=batch.total_insights,
            total_cost_usd=batch.total_cost_usd,
            processing_time_seconds=batch.processing_time_seconds,
            health_score=getattr(batch.insights, "health_score", None),
            output_dir=str(output_dir),
            files=files_summary,
        )
        _JOB_STORE[job_id]["status"] = "success"

    except Exception as exc:
        _JOB_STORE[job_id]["status"] = "error"
        _JOB_STORE[job_id]["error"] = str(exc)
        logs.append(f"[ERREUR] {exc}")
        logs.append(traceback.format_exc())

    finally:
        _JOB_STORE[job_id]["finished_at"] = datetime.now(timezone.utc).isoformat()


# =============================================================================
# Endpoints
# =============================================================================

@router.post(
    "/start",
    status_code=202,
    response_model=JobCreatedResponse,
    summary="Lancer un job d'audit PHP",
    description=(
        "Soumet un ou plusieurs fichiers PHP à analyser. "
        "Retourne un `job_id` immédiatement (HTTP 202). "
        "Le pipeline s'exécute en arrière-plan via BackgroundTasks. "
        "Interroger `GET /audit/{job_id}` pour suivre l'avancement."
    ),
)
async def start_audit(
    request: AuditStartRequest,
    background_tasks: BackgroundTasks,
) -> JobCreatedResponse:
    # ── Résolution des chemins ─────────────────────────────────────────────
    php_files: list[Path] = []
    for raw in request.php_paths:
        p = Path(raw).expanduser().resolve()
        if not p.exists():
            raise HTTPException(status_code=422, detail=f"Chemin introuvable : {raw}")
        if p.is_dir():
            php_files.extend(sorted(p.rglob("*.php")))
        elif p.suffix.lower() == ".php":
            php_files.append(p)
        else:
            raise HTTPException(
                status_code=422,
                detail=f"Doit être un fichier .php ou un répertoire : {raw}",
            )

    if not php_files:
        raise HTTPException(status_code=422, detail="Aucun fichier .php trouvé dans les chemins fournis.")

    # ── Construction des options (valide les secrets si LLM) ──────────────
    try:
        options = AuditOptions(
            no_llm=request.no_llm,
            model=request.model,
            bug_check=request.bug_check,
            kb_root=Path(request.kb_root).expanduser() if request.kb_root else None,
            call_graph_root=(
                Path(request.call_graph_root).expanduser() if request.call_graph_root else None
            ),
            # Cap au nombre réel de fichiers pour éviter des workers inutiles
            max_workers=min(request.max_workers, len(php_files)),
        )
    except EnvironmentError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    # ── Création du job ────────────────────────────────────────────────────
    job_id = str(uuid.uuid4())
    output_dir = _job_output_dir(job_id)

    _JOB_STORE[job_id] = {
        "status": "queued",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "started_at": None,
        "finished_at": None,
        "logs": [],
        "error": None,
        "result": None,
    }

    background_tasks.add_task(
        _execute_audit_job, job_id, php_files, output_dir, options
    )

    n = len(php_files)
    return JobCreatedResponse(
        job_id=job_id,
        message=f"{n} fichier(s) PHP en file — GET /audit/{job_id} pour suivre",
    )


@router.get(
    "/roi",
    response_model=ROISummaryResponse,
    summary="Dashboard ROI — métriques cumulées de tous les audits",
)
async def get_roi() -> ROISummaryResponse:
    from telemetry.performance_logger import PerformanceLogger

    summary = await asyncio.to_thread(PerformanceLogger().summary)
    if summary.get("total_runs", 0) == 0:
        return ROISummaryResponse(
            total_runs=0, total_lines_analyzed=0, total_human_hours_saved=0.0,
            financial_saving_eur=0.0, total_llm_cost_usd=0.0,
            total_machine_seconds=0.0, success_rate_pct=0.0,
            avg_processing_seconds=0.0, lines_per_hour_constant=1000,
            hourly_rate_eur=75.0,
        )
    return ROISummaryResponse(**summary)


@router.get(
    "/roi/history",
    response_model=list[ROIDayResponse],
    summary="Évolution quotidienne des audits (N derniers jours)",
)
async def get_roi_history(
    days: int = Query(7, ge=1, le=90, description="Nombre de jours à retourner"),
) -> list[ROIDayResponse]:
    import json
    import os
    from collections import defaultdict
    from datetime import date, timedelta

    jsonl_path = Path(
        os.environ.get("ROSETTA_ROI_METRICS", "~/rosetta-data/roi_metrics.jsonl")
    ).expanduser()

    buckets: dict[str, dict] = defaultdict(
        lambda: {"runs": 0, "lines_analyzed": 0, "hours_saved": 0.0, "cost_usd": 0.0}
    )

    if jsonl_path.exists():
        for line in jsonl_path.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
                day = row.get("timestamp", "")[:10]
                buckets[day]["runs"] += 1
                buckets[day]["lines_analyzed"] += row.get("file_size_lines", 0)
                buckets[day]["hours_saved"] += row.get("human_hours_saved", 0.0)
                buckets[day]["cost_usd"] += row.get("llm_cost_usd", 0.0)
            except (json.JSONDecodeError, KeyError):
                continue

    cutoff = date.today() - timedelta(days=days - 1)
    result: list[ROIDayResponse] = []
    for i in range(days):
        d = (cutoff + timedelta(days=i)).isoformat()
        b = buckets.get(d, {"runs": 0, "lines_analyzed": 0, "hours_saved": 0.0, "cost_usd": 0.0})
        result.append(
            ROIDayResponse(
                date=d,
                runs=b["runs"],
                lines_analyzed=b["lines_analyzed"],
                hours_saved=round(b["hours_saved"], 2),
                cost_usd=round(b["cost_usd"], 4),
            )
        )
    return result


@router.get(
    "/",
    response_model=list[JobStatusResponse],
    summary="Lister tous les jobs (sans les logs)",
)
async def list_jobs() -> list[JobStatusResponse]:
    return [
        JobStatusResponse(
            job_id=jid,
            status=job["status"],
            created_at=job["created_at"],
            started_at=job.get("started_at"),
            finished_at=job.get("finished_at"),
            logs=[],            # omis pour alléger la réponse de liste
            error=job.get("error"),
            result=job.get("result"),
        )
        for jid, job in _JOB_STORE.items()
    ]


@router.get(
    "/{job_id}",
    response_model=JobStatusResponse,
    summary="Statut et résultat d'un job d'audit",
)
async def get_job_status(job_id: str) -> JobStatusResponse:
    job = _JOB_STORE.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' introuvable.")
    return JobStatusResponse(
        job_id=job_id,
        status=job["status"],
        created_at=job["created_at"],
        started_at=job.get("started_at"),
        finished_at=job.get("finished_at"),
        logs=job.get("logs", []),
        error=job.get("error"),
        result=job.get("result"),
    )
