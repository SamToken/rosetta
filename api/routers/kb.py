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
import json
import os
import re
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Response

from api.deps import KBServiceDep

from api.schemas import (
    AddPendingRequest,
    AddPendingResponse,
    CaptureRequest,
    CaptureResponse,
    DeleteKBEntryResponse,
    KBEntryResponse,
    KBStatsResponse,
    LookupResponse,
    PendingItemResponse,
    SearchResultResponse,
    UpdateConfianceRequest,
    UpdateConfianceResponse,
    ValidatePendingRequest,
    ValidatePendingResponse,
    ValidateRelationRequest,
    ValidateRelationResponse,
)

router = APIRouter(prefix="/kb", tags=["KB"])


# =============================================================================
# Relations sémantiques — agrégation depuis les IRs JSON
# =============================================================================

def _load_relations_from_irs() -> list[KBEntryResponse]:
    """Scanne tous les IRs JSON archivés et agrège les relations sémantiques."""
    base = Path(
        os.environ.get("ROSETTA_API_OUTPUT", "~/rosetta-data/api_jobs")
    ).expanduser()
    if not base.exists():
        return []

    seen: set[str] = set()
    entries: list[KBEntryResponse] = []

    for json_file in sorted(base.rglob("*_business_logic.json")):
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
        except Exception:
            continue
        for rel in data.get("relations", []):
            rid = rel.get("id", "")
            if not rid or rid in seen:
                continue
            seen.add(rid)
            from_e = rel.get("from_entity") or {}
            to_e = rel.get("to_entity") or {}
            fval = from_e.get("value", "?")
            tval = to_e.get("value", "?")
            kind = rel.get("kind", "?")
            entries.append(KBEntryResponse(
                code=f"{fval} → {tval}",
                label=f"{kind} — {fval} → {tval}",
                domaine=rel.get("domaine") or "—",
                confiance=rel.get("confiance") or "medium",
                section="relations",
                notes=rel.get("semantique") or "",
                source=rel.get("pattern") or "",
                pending_questions=0,
                lie_a=[],
                relation_kind=kind,
                relation_from=fval,
                relation_to=tval,
                relation_direction=rel.get("direction") or "one_way",
                trouve_dans=rel.get("trouvé_dans") or [],
            ))

    return entries


# =============================================================================
# Lecture
# =============================================================================

@router.get(
    "/stats",
    response_model=KBStatsResponse,
    summary="Tableau de bord de la Knowledge Base",
)
async def get_stats(svc: KBServiceDep) -> KBStatsResponse:
    s, rels = await asyncio.gather(
        asyncio.to_thread(svc.stats),
        asyncio.to_thread(_load_relations_from_irs),
    )
    rel_high     = sum(1 for r in rels if r.confiance == "high")
    rel_medium   = sum(1 for r in rels if r.confiance == "medium")
    rel_inferred = sum(1 for r in rels if r.confiance == "inferred")
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
        relations=len(rels),
        total=s.total + len(rels),
        high=s.high + rel_high,
        medium=s.medium + rel_medium,
        inferred=s.inferred + rel_inferred,
        pending_total=s.pending_total,
        pending_high=s.pending_high,
    )


_BASE_DOMAINS = {
    "commun", "ticketing", "sla", "diagnostic", "interco",
    "aircom", "airele", "orchestra", "scenario", "enrichissement-alarmes",
    "oceane", "referentiel", "supervision",
}


@router.get(
    "/domains",
    response_model=list[str],
    summary="Liste les domaines distincts du KB (ordre alphabétique)",
)
async def list_domains(svc: KBServiceDep) -> list[str]:
    data = await asyncio.to_thread(svc.load)
    sections = [
        data.get("codes", {}) or {},
        data.get("regles", {}) or {},
        ((data.get("sql_artifacts") or {}).get("colonnes") or {}),
        ((data.get("sql_artifacts") or {}).get("vues") or {}),
        ((data.get("sql_artifacts") or {}).get("requetes") or {}),
    ]
    domains: set[str] = set(_BASE_DOMAINS)
    for bucket in sections:
        for entry in bucket.values():
            if isinstance(entry, dict):
                d = entry.get("domaine", "")
                if d and d != "—":
                    domains.add(d)
    return sorted(domains)


@router.get(
    "/entries",
    response_model=list[KBEntryResponse],
    summary="Liste toutes les entrées KB (toutes sections)",
)
async def list_entries(svc: KBServiceDep) -> list[KBEntryResponse]:
    data, rels = await asyncio.gather(
        asyncio.to_thread(svc.load),
        asyncio.to_thread(_load_relations_from_irs),
    )
    sections = [
        ("codes",                  data.get("codes", {}) or {}),
        ("regles",                 data.get("regles", {}) or {}),
        ("sql_artifacts.colonnes", (data.get("sql_artifacts") or {}).get("colonnes", {}) or {}),
        ("sql_artifacts.vues",     (data.get("sql_artifacts") or {}).get("vues", {}) or {}),
        ("sql_artifacts.requetes", (data.get("sql_artifacts") or {}).get("requetes", {}) or {}),
    ]
    entries: list[KBEntryResponse] = []
    for section, bucket in sections:
        for code, entry in bucket.items():
            if not isinstance(entry, dict):
                continue
            notes = str(entry.get("notes") or "")
            pending_q = len(re.findall(r"[Àà]\s*valider\s*PO\s*:", notes, re.IGNORECASE))
            lie_a = entry.get("lié_à") or entry.get("lie_a") or []
            entries.append(KBEntryResponse(
                code=code,
                label=str(entry.get("label") or "—"),
                domaine=str(entry.get("domaine") or "—"),
                confiance=str(entry.get("confiance") or "inferred"),
                section=section,
                notes=notes,
                source=str(entry.get("source") or ""),
                pending_questions=pending_q,
                lie_a=lie_a if isinstance(lie_a, list) else [lie_a],
            ))
    entries.extend(rels)
    # Tri : high en tête, puis alphabétique par code
    order = {"high": 0, "medium": 1, "inferred": 2}
    entries.sort(key=lambda e: (order.get(e.confiance, 3), e.code.lower()))
    return entries


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


@router.patch(
    "/relation/validate",
    response_model=ValidateRelationResponse,
    summary="Valider une relation sémantique (met à jour la confiance dans les JSON sources)",
)
async def validate_relation(body: ValidateRelationRequest) -> ValidateRelationResponse:
    base = Path(os.environ.get("ROSETTA_API_OUTPUT", "~/rosetta-data/api_jobs")).expanduser()
    if not base.exists():
        raise HTTPException(status_code=404, detail="Dossier jobs introuvable")

    updated = 0

    def _update_jsons() -> int:
        count = 0
        for json_file in base.rglob("*_business_logic.json"):
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
            except Exception:
                continue
            changed = False
            for rel in data.get("relations", []):
                fv = (rel.get("from_entity") or {}).get("value", "")
                tv = (rel.get("to_entity") or {}).get("value", "")
                kind = rel.get("kind", "")
                if fv == body.relation_from and tv == body.relation_to and kind == body.relation_kind:
                    rel["confiance"] = body.confiance
                    changed = True
                    count += 1
            if changed:
                json_file.write_text(
                    json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
                )
        return count

    updated = await asyncio.to_thread(_update_jsons)
    if updated == 0:
        raise HTTPException(status_code=404, detail="Relation introuvable dans les jobs archivés")
    return ValidateRelationResponse(
        success=True, updated=updated,
        message=f"{updated} occurrence(s) mises à jour → {body.confiance}",
    )


@router.patch(
    "/{code}/confiance",
    response_model=UpdateConfianceResponse,
    summary="Mettre à jour la confiance d'une entrée KB YAML",
    responses={404: {"description": "Entrée introuvable"}},
)
async def update_confiance(
    code: str,
    body: UpdateConfianceRequest,
    section: str = Query(..., description="Section KB cible"),
    svc: KBServiceDep = None,
) -> UpdateConfianceResponse:
    updated = await asyncio.to_thread(svc.update_confiance, code, section, body.confiance)
    if not updated:
        raise HTTPException(status_code=404, detail=f"'{code}' introuvable dans '{section}'")
    return UpdateConfianceResponse(
        success=True, code=code, confiance=body.confiance,
        message=f"'{code}' → {body.confiance}",
    )


@router.delete(
    "/{code}",
    response_model=DeleteKBEntryResponse,
    summary="Supprimer une entrée KB",
    responses={404: {"description": "Entrée introuvable"}},
)
async def delete_kb_entry(
    code: str,
    section: str = Query(..., description="Section KB : codes | regles | sql_artifacts.colonnes | …"),
    svc: KBServiceDep = None,
) -> DeleteKBEntryResponse:
    deleted = await asyncio.to_thread(svc.delete, code, section)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Entrée '{code}' introuvable dans '{section}'")
    return DeleteKBEntryResponse(success=True, code=code, message=f"'{code}' supprimé de {section}")


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
