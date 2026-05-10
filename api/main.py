"""Rosetta API v3 — Application FastAPI.

Lancer :
    cd ~/projects/rosetta
    .venv/bin/uvicorn api.main:app --reload --port 8765 --host 127.0.0.1

Swagger :  http://localhost:8765/docs
ReDoc   :  http://localhost:8765/redoc
Health  :  http://localhost:8765/

Variables d'environnement :
    ROSETTA_KB              Chemin KB (fichier ou répertoire)
    ANTHROPIC_API_KEY       Requis pour les jobs LLM
    ROSETTA_API_OUTPUT      Répertoire de sortie des jobs (défaut: ~/rosetta-data/api_jobs)
"""
from __future__ import annotations

import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Bootstrap — permet les imports relatifs depuis la racine Rosetta
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.routers import audit, kb

# =============================================================================
# Description OpenAPI
# =============================================================================

_DESCRIPTION = """
## Rosetta API — Audit statique PHP + Knowledge Base

### /audit — Pipeline d'analyse

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/audit/start` | Soumettre un job (HTTP 202, async) |
| `GET` | `/audit/{job_id}` | État + résultats d'un job |
| `GET` | `/audit/` | Liste tous les jobs |
| `GET` | `/audit/roi` | Dashboard ROI (métriques cumulées) |

### /kb — Knowledge Base

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/kb/stats` | Dashboard KB |
| `GET` | `/kb/lookup/{code}` | Lookup d'un token |
| `GET` | `/kb/pending` | File de validation PO |
| `GET` | `/kb/search` | Recherche textuelle |
| `GET` | `/kb/export/markdown` | Export Markdown structuré |
| `GET` | `/kb/export/prompt` | Export compact pour injection LLM |
| `GET` | `/kb/export/human` | Dossier de fusion lisible humain |
| `POST` | `/kb/capture` | Capturer un code métier |
| `POST` | `/kb/pending` | Ajouter une question PO |
| `POST` | `/kb/validate/{id}` | Valider (confiance → high) |

### Stratégie async

Les services Rosetta sont synchrones. Les appels bloquants (pipeline LLM, lecture YAML)
sont exécutés via `asyncio.to_thread` pour ne pas bloquer l'event loop.
Les jobs d'audit long-running utilisent `BackgroundTasks`.
"""


# =============================================================================
# Lifespan
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup — vérification non bloquante de la config
    import os
    kb_path = os.environ.get("ROSETTA_KB", "~/rosetta-data/kb")
    resolved = Path(kb_path).expanduser()
    if not resolved.exists():
        print(
            f"[Rosetta API] ⚠  KB introuvable : {resolved}\n"
            f"  Exporter ROSETTA_KB=<chemin> ou créer le répertoire.",
            file=sys.stderr,
        )
    yield
    # Shutdown — rien à nettoyer (jobs en mémoire, connexions stateless)


# =============================================================================
# Factory
# =============================================================================

def create_app() -> FastAPI:
    app = FastAPI(
        title="Rosetta API",
        description=_DESCRIPTION,
        version="3.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_tags=[
            {
                "name": "Audit",
                "description": "Pipeline d'analyse PHP — jobs asynchrones",
            },
            {
                "name": "KB",
                "description": "Knowledge Base — lecture et écriture YAML",
            },
        ],
    )

    # CORS — accès local (VS Code, Copilot, navigateur)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    app.include_router(audit.router)
    app.include_router(kb.router)

    # Dashboard UI — servi sur /dashboard (aiofiles requis)
    ui_dir = Path(__file__).parent.parent / "ui"
    if ui_dir.exists():
        app.mount("/dashboard", StaticFiles(directory=str(ui_dir), html=True), name="ui")

    @app.get("/", tags=["Santé"], summary="Health check")
    async def health() -> dict:
        import os
        return {
            "status": "ok",
            "version": "3.0.0",
            "service": "Rosetta API",
            "kb": os.environ.get("ROSETTA_KB", "~/rosetta-data/kb"),
        }

    return app


app = create_app()
