"""Rosetta API — Injection de dépendances FastAPI."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated

from fastapi import Depends

from services.kb_service import KBService


def get_kb_service() -> KBService:
    """Crée un KBService pointant sur $ROSETTA_KB (fichier ou répertoire)."""
    raw = os.environ.get("ROSETTA_KB", "~/rosetta-data/kb")
    return KBService(Path(raw).expanduser().resolve())


# Type alias — usage : `svc: KBServiceDep` dans les handlers
KBServiceDep = Annotated[KBService, Depends(get_kb_service)]
