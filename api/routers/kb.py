"""Rosetta API — Router /kb (Knowledge Base).

Tous les appels KBService (lecture YAML) sont délégués à asyncio.to_thread.

Endpoints lecture :
    GET /kb/stats
    GET /kb/lookup/{code}
    GET /kb/pending
    GET /kb/search
    GET /kb/export/markdown
    GET /kb/export/prompt
    GET /kb/export/human

Endpoints écriture :
    POST /kb/capture
    POST /kb/pending
    POST /kb/validate/{pending_id}
"""
from __future__ import annotations

import asyncio
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Response

from api.deps import KBServiceDep
from api.schemas import (
    AddPendingRequest,
    AddPendingResponse,
    CaptureRequest,
    CaptureResponse,
    KBStatsResponse,
    LookupResponse,
    PendingItemResponse,
    SearchResultResponse,
    ValidatePendingRequest,
    ValidatePendingResponse,
)

router = APIRouter(prefix="/kb", tags=["KB"])


# =============================================================================
# Lecture
# =============================================================================

@router.get(
    "/stats",
    response_model=KBStatsResponse,
    summary="Tableau de bord de la Knowledge Base",
)
async def get_stats(svc: KBServiceDep) -> KBStatsResponse:
    s = await asyncio.to_thread(svc.stats)
    return KBStatsResponse(
        projet=s.projet,
        version=s.version,
        last_updated=s.last_updated,
        maintainer=s.maintainer,
        codes=s.codes,
        regles=s.regles,
        schema_entries=s.schema,
        colonnes=s.colonnes,
        vues=s.vues,
        requetes=s.requetes,
        total=s.total,
        high=s.high,
        medium=s.medium,
        inferred=s.inferred,
        pending_total=s.pending_total,
        pending_high=s.pending_high,
    )


@router.get(
    "/lookup/{code}",
    response_model=LookupResponse,
    summary="Rechercher un token dans toutes les sections du KB",
    responses={404: {"description": "Token introuvable"}},
)
async def lookup(code: str, svc: KBServiceDep) -> LookupResponse:
    result = await asyncio.to_thread(svc.lookup, code)
    if not result.found:
        raise HTTPException(status_code=404, detail=f"Token '{code}' introuvable dans le KB.")
    return LookupResponse(
        found=result.found,
        code=result.code,
        section=result.section,
        entry=result.entry,
    )


@router.get(
    "/pending",
    response_model=list[PendingItemResponse],
    summary="File de validation PO",
)
async def list_pending(
    svc: KBServiceDep,
    priorite: Optional[str] = Query(
        None,
        description="Filtrer par priorité",
        pattern="^(high|medium|low)$",
    ),
) -> list[PendingItemResponse]:
    items = await asyncio.to_thread(svc.list_pending, priorite)
    return [
        PendingItemResponse(
            id=item.id,
            code=item.code,
            question=item.question,
            priorite=item.priorite,
            domaine=item.domaine,
            fichiers=item.fichiers,
            kb_type=item.kb_type,
            pending_type=item.pending_type,
            destination=item.destination,
        )
        for item in items
    ]


@router.get(
    "/search",
    response_model=list[SearchResultResponse],
    summary="Recherche textuelle dans tout le KB",
)
async def search(
    texte: str = Query(description="Texte à rechercher (insensible à la casse)"),
    svc: KBServiceDep = None,   # noqa: B008 — résolu par Depends via l'Annotated
) -> list[SearchResultResponse]:
    results = await asyncio.to_thread(svc.search, texte)
    return [
        SearchResultResponse(
            section=r.section,
            nom=r.nom,
            label=r.entry.get("label", "—"),
            confiance=r.entry.get("confiance", "?"),
        )
        for r in results
    ]


@router.get(
    "/export/markdown",
    summary="Exporter le KB complet en Markdown structuré",
    response_class=Response,
    responses={200: {"content": {"text/markdown": {}}}},
)
async def export_markdown(svc: KBServiceDep) -> Response:
    md = await asyncio.to_thread(svc.export_markdown)
    return Response(content=md, media_type="text/markdown; charset=utf-8")


@router.get(
    "/export/prompt",
    summary="Exporter le KB en bloc compact pour injection LLM",
    response_class=Response,
    responses={200: {"content": {"text/plain": {}}}},
)
async def export_prompt(
    svc: KBServiceDep,
    domaine: Optional[str] = Query(None, description="Filtrer par domaine (ex: RetablirCloturer)"),
    confiance_min: str = Query(
        "medium",
        description="Confiance minimale à inclure",
        pattern="^(high|medium|inferred)$",
    ),
    max_chars: int = Query(4000, ge=500, le=50000, description="Limite en caractères"),
) -> Response:
    block = await asyncio.to_thread(svc.export_prompt, domaine, confiance_min, max_chars)
    if not block:
        return Response(
            content="(KB vide ou aucune entrée ne correspond aux filtres)",
            media_type="text/plain; charset=utf-8",
        )
    return Response(content=block, media_type="text/plain; charset=utf-8")


@router.get(
    "/export/human",
    summary="Dossier de fusion lisible humain (réunion PO, migration)",
    response_class=Response,
    responses={200: {"content": {"text/markdown": {}}}},
)
async def export_human(
    svc: KBServiceDep,
    domaine: str = Query(
        description="Domaine(s) à exporter, séparés par virgule (ex: RetablirCloturerController)"
    ),
    sources: Optional[str] = Query(
        None,
        description="Fichiers PHP à citer en en-tête, séparés par virgule",
    ),
) -> Response:
    domaines = [d.strip() for d in domaine.split(",") if d.strip()]
    sources_list = [s.strip() for s in (sources or "").split(",") if s.strip()]
    md = await asyncio.to_thread(svc.export_human, domaines, sources_list)
    return Response(content=md, media_type="text/markdown; charset=utf-8")


# =============================================================================
# Écriture
# =============================================================================

@router.post(
    "/capture",
    response_model=CaptureResponse,
    status_code=201,
    summary="Capturer un code/constante métier",
)
async def capture(body: CaptureRequest, svc: KBServiceDep) -> CaptureResponse:
    result = await asyncio.to_thread(
        svc.capture,
        code=body.code,
        label=body.label,
        source=body.source,
        confiance=body.confiance,
        domain=body.domain,
        champ=body.champ,
        table=body.table,
        lie_a=body.lie_a,
        notes=body.notes,
        force=body.force,
    )
    if result.action == "skipped_high":
        return CaptureResponse(
            success=False,
            code=result.code,
            confiance=result.confiance,
            domain=result.domain,
            action=result.action,
            file_path=result.file_path,
            message=f"'{result.code}' existe déjà avec confiance high. Utiliser force=true pour écraser.",
        )
    verb = "créé" if result.action == "created" else "mis à jour"
    return CaptureResponse(
        success=True,
        code=result.code,
        confiance=result.confiance,
        domain=result.domain,
        action=result.action,
        file_path=result.file_path,
        message=f"Code '{result.code}' {verb} (confiance: {result.confiance})",
    )


@router.post(
    "/pending",
    response_model=AddPendingResponse,
    status_code=201,
    summary="Ajouter une question dans la file PO",
)
async def add_pending(body: AddPendingRequest, svc: KBServiceDep) -> AddPendingResponse:
    result = await asyncio.to_thread(
        svc.add_pending,
        code=body.code,
        question=body.question,
        priorite=body.priorite,
        fichiers=body.fichiers,
        kb_type=body.kb_type,
        domaine=body.domaine,
    )
    return AddPendingResponse(
        pending_id=result.pending_id,
        code=result.code,
        priorite=result.priorite,
        destination=result.destination,
    )


@router.post(
    "/validate/{pending_id}",
    response_model=ValidatePendingResponse,
    summary="Valider une question PO (monte en confiance high)",
    responses={404: {"description": "ID pending introuvable"}},
)
async def validate_pending(
    pending_id: str,
    body: ValidatePendingRequest,
    svc: KBServiceDep,
) -> ValidatePendingResponse:
    result = await asyncio.to_thread(
        svc.validate_pending,
        pending_id=pending_id,
        label=body.label,
        source=body.source,
        notes=body.notes,
        domaine=body.domaine,
    )
    if not result.success:
        raise HTTPException(status_code=404, detail=result.error)
    return ValidatePendingResponse(
        success=True,
        pending_id=result.pending_id,
        code=result.code,
        action=result.action,
        domain=result.domain,
    )
