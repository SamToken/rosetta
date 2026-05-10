"""Rosetta API — Router /audit (jobs d'analyse PHP).

Pattern :
    POST /audit/start  → crée un job (HTTP 202), lance en BackgroundTask
    GET  /audit/       → liste tous les jobs
    GET  /audit/roi    → dashboard ROI (métriques cumulées)
    GET  /audit/{id}   → état d'un job

Les appels bloquants (AuditPipeline) sont délégués à asyncio.to_thread
pour ne pas bloquer l'event loop.
Persistance : SQLite via SQLAlchemy (api/database.py + api/models.py).
"""
from __future__ import annotations

import asyncio
import json
import traceback
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query

from api.database import get_session
from api.models import Job, JobLog
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
# Helpers DB
# =============================================================================

def _job_output_dir(job_id: str) -> Path:
    import os
    base = Path(os.environ.get("ROSETTA_API_OUTPUT", "~/rosetta-data/api_jobs")).expanduser()
    return base / job_id


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _db_create_job(job_id: str) -> None:
    with get_session() as session:
        session.add(Job(id=job_id, status="queued", created_at=_now_iso()))
        session.commit()


def _db_update_status(job_id: str, status: str, **kwargs) -> None:
    """Met à jour statut + champs optionnels (started_at, finished_at, error, result_json)."""
    with get_session() as session:
        job = session.get(Job, job_id)
        if job is None:
            return
        job.status = status
        for k, v in kwargs.items():
            setattr(job, k, v)
        session.commit()


def _db_append_log(job_id: str, message: str) -> None:
    """Insère une ligne de log (idx = nombre de logs existants)."""
    with get_session() as session:
        count = session.query(JobLog).filter_by(job_id=job_id).count()
        session.add(JobLog(job_id=job_id, idx=count, message=message))
        session.commit()


def _job_to_response(job: Job, include_logs: bool = True) -> JobStatusResponse:
    result = None
    if job.result_json:
        try:
            result = AuditJobResult(**json.loads(job.result_json))
        except Exception:
            pass

    logs = [log.message for log in job.logs] if include_logs else []

    return JobStatusResponse(
        job_id=job.id,
        status=job.status,  # type: ignore[arg-type]
        created_at=job.created_at,
        started_at=job.started_at,
        finished_at=job.finished_at,
        logs=logs,
        error=job.error,
        result=result,
    )


# =============================================================================
# Tâche de fond
# =============================================================================

async def _execute_audit_job(
    job_id: str,
    php_files: list[Path],
    output_dir: Path,
    options: AuditOptions,
) -> None:
    """Lance AuditPipeline dans un thread pool et persiste les résultats en DB."""

    def _log(msg: str) -> None:
        _db_append_log(job_id, msg)

    _db_update_status(job_id, "running", started_at=_now_iso())

    pipeline = AuditPipeline(options, progress=_log)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        await asyncio.to_thread(pipeline.setup)
        batch = await asyncio.to_thread(pipeline.run_batch, php_files, output_dir)

        files_summary = []
        for r in batch.results:
            flag_counts: dict[str, int] = {}
            for f in r.ir.flags:
                flag_counts[f.type] = flag_counts.get(f.type, 0) + 1
            files_summary.append(AuditFileSummary(
                filename=r.php_path.name,
                file_size_lines=r.file_size_lines,
                processing_time_seconds=r.processing_time_seconds,
                flags_total=len(r.ir.flags),
                flag_types=flag_counts,
                insights_total=len(r.ir.llm_insights),
                llm_cost_usd=r.llm_cost_usd,
                status=r.status,
            ))

        result_obj = AuditJobResult(
            total_files=len(batch.php_paths),
            total_insights=batch.total_insights,
            total_cost_usd=batch.total_cost_usd,
            processing_time_seconds=batch.processing_time_seconds,
            health_score=getattr(batch.insights, "health_score", None),
            output_dir=str(output_dir),
            files=files_summary,
        )
        _db_update_status(
            job_id,
            "success",
            result_json=result_obj.model_dump_json(),
            finished_at=_now_iso(),
        )

    except Exception as exc:
        _db_update_status(
            job_id,
            "error",
            error=str(exc),
            finished_at=_now_iso(),
        )
        _log(f"[ERREUR] {exc}")
        _log(traceback.format_exc())


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

    # ── Construction des options ───────────────────────────────────────────
    try:
        options = AuditOptions(
            no_llm=request.no_llm,
            model=request.model,
            bug_check=request.bug_check,
            kb_root=Path(request.kb_root).expanduser() if request.kb_root else None,
            call_graph_root=(
                Path(request.call_graph_root).expanduser() if request.call_graph_root else None
            ),
            max_workers=min(request.max_workers, len(php_files)),
        )
    except EnvironmentError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    # ── Création du job en DB ──────────────────────────────────────────────
    job_id = str(uuid.uuid4())
    output_dir = _job_output_dir(job_id)
    _db_create_job(job_id)

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
    with get_session() as session:
        jobs = session.query(Job).order_by(Job.created_at.desc()).all()
        return [_job_to_response(j, include_logs=False) for j in jobs]


@router.get(
    "/{job_id}",
    response_model=JobStatusResponse,
    summary="Statut et résultat d'un job d'audit",
)
async def get_job_status(job_id: str) -> JobStatusResponse:
    with get_session() as session:
        job = session.get(Job, job_id)
        if job is None:
            raise HTTPException(status_code=404, detail=f"Job '{job_id}' introuvable.")
        # Charger les logs dans la même session avant de fermer
        _ = job.logs
        return _job_to_response(job, include_logs=True)
