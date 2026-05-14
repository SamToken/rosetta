"""Rosetta API — Router /impact (index d'impact cross-fichier).

Agrège les tokens KB référencés dans tous les IRs JSON archivés et expose
leur distribution (fichiers, méthodes, lignes) pour visualisation dans le Cockpit.

Source principale : ir.relations (from_entity + to_entity) — tokens KB propres.
Cross-référencé avec la KB YAML pour le flag kb_known.
"""
from __future__ import annotations

import asyncio
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from api.schemas import ImpactIndexOut, ImpactOccurrence, ImpactTokenOut

router = APIRouter(prefix="/impact", tags=["Impact"])


# =============================================================================
# Agrégateur
# =============================================================================

def _build_impact_index(base: Path, known_tokens: frozenset[str]) -> dict:
    """
    Scanne tous les *_business_logic.json dans base/**/details/ et agrège
    les tokens référencés dans ir.relations (from_entity + to_entity).

    Retourne un dict {token_name → {total_occurrences, distinct_files, kb_known,
                                     sources, occurrences}}.
    """
    if not base.exists():
        return {}

    # token → {fichiers, occurrences}
    token_data: dict[str, dict] = defaultdict(lambda: {
        "fichiers": set(),
        "occurrences": [],
        "sources": set(),
    })

    ir_count = 0

    for json_path in sorted(base.rglob("*_business_logic.json")):
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception:
            continue

        ir_count += 1

        for rel in data.get("relations", []):
            kind = rel.get("kind", "relation")
            for entity_key in ("from_entity", "to_entity"):
                entity = rel.get(entity_key) or {}
                token = entity.get("value", "").strip()
                # Filtrer les valeurs composites (variables PHP, flèches, etc.)
                if not token or len(token) < 2 or "$" in token or "→" in token or " " in token:
                    continue

                td = token_data[token]
                td["sources"].add(kind)

                for ref in rel.get("trouvé_dans") or []:
                    fichier = ref.get("fichier", "")
                    methode = ref.get("methode", "")
                    ligne = ref.get("ligne")
                    if fichier:
                        td["fichiers"].add(fichier)
                    td["occurrences"].append({
                        "fichier": fichier,
                        "methode": methode,
                        "ligne": ligne,
                        "source": kind,
                    })

                # Fallback si trouvé_dans vide : compter quand même
                if not rel.get("trouvé_dans"):
                    td["occurrences"].append({
                        "fichier": json_path.stem.replace("_business_logic", ""),
                        "methode": "",
                        "ligne": None,
                        "source": kind,
                    })
                    td["fichiers"].add(json_path.stem.replace("_business_logic", ""))

    return {
        "ir_count": ir_count,
        "tokens": {
            token: {
                "total_occurrences": len(d["occurrences"]),
                "distinct_files":    len(d["fichiers"]),
                "kb_known":          token in known_tokens,
                "sources":           sorted(d["sources"]),
                "occurrences":       d["occurrences"],
            }
            for token, d in token_data.items()
            if d["occurrences"]
        },
    }


def _get_known_tokens() -> frozenset[str]:
    try:
        from rosetta_kb import DEFAULT_KB_PATH
        from services.kb_service import KBService
        kb_path = Path(DEFAULT_KB_PATH).expanduser().resolve()
        if kb_path.exists():
            return KBService(kb_path).list_known_tokens()
    except Exception:
        pass
    return frozenset()


def _impact_base() -> Path:
    return Path(
        os.environ.get("ROSETTA_API_OUTPUT", "~/rosetta-data/api_jobs")
    ).expanduser()


# =============================================================================
# Endpoints
# =============================================================================

@router.get(
    "/tokens",
    response_model=ImpactIndexOut,
    summary="Index d'impact cross-fichier — tokens KB dans tous les IRs",
)
async def list_impact_tokens(
    min_occurrences: int = Query(1, ge=1, description="Seuil minimum d'occurrences"),
    max_tokens: int = Query(200, ge=1, le=1000, description="Nombre max de tokens retournés"),
    search: Optional[str] = Query(None, description="Filtre sur le nom du token (insensible à la casse)"),
) -> ImpactIndexOut:
    known = await asyncio.to_thread(_get_known_tokens)
    base  = _impact_base()
    raw   = await asyncio.to_thread(_build_impact_index, base, known)

    tokens = raw.get("tokens", {})
    ir_count = raw.get("ir_count", 0)

    # Filtres
    if search:
        q = search.lower()
        tokens = {k: v for k, v in tokens.items() if q in k.lower()}
    tokens = {k: v for k, v in tokens.items() if v["total_occurrences"] >= min_occurrences}

    # Tri par occurrences décroissantes, puis limite
    sorted_tokens = dict(
        sorted(tokens.items(), key=lambda x: -x[1]["total_occurrences"])[:max_tokens]
    )

    return ImpactIndexOut(
        ir_count=ir_count,
        token_count=len(sorted_tokens),
        tokens={
            name: ImpactTokenOut(
                total_occurrences=d["total_occurrences"],
                distinct_files=d["distinct_files"],
                kb_known=d["kb_known"],
                sources=d["sources"],
                occurrences=[ImpactOccurrence(**o) for o in d["occurrences"]],
            )
            for name, d in sorted_tokens.items()
        },
    )


@router.get(
    "/tokens/{token}",
    response_model=ImpactTokenOut,
    summary="Détail d'impact d'un token (toutes occurrences)",
    responses={404: {"description": "Token introuvable dans les IRs"}},
)
async def get_token_impact(token: str) -> ImpactTokenOut:
    known = await asyncio.to_thread(_get_known_tokens)
    base  = _impact_base()
    raw   = await asyncio.to_thread(_build_impact_index, base, known)

    tokens = raw.get("tokens", {})

    # Lookup exact puis case-insensitive
    data = tokens.get(token)
    if not data:
        for k, v in tokens.items():
            if k.lower() == token.lower():
                data = v
                break

    if not data:
        raise HTTPException(status_code=404, detail=f"Token '{token}' introuvable dans les IRs.")

    return ImpactTokenOut(
        total_occurrences=data["total_occurrences"],
        distinct_files=data["distinct_files"],
        kb_known=data["kb_known"],
        sources=data["sources"],
        occurrences=[ImpactOccurrence(**o) for o in data["occurrences"]],
    )
