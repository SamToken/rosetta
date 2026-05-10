"""Rosetta API — Couche SQLite (SQLAlchemy 2.0, mode synchrone).

Stratégie :
- WAL mode + synchronous=NORMAL → lectures concurrentes, écritures sérialisées
- check_same_thread=False → sessions partagées entre threads BackgroundTask
- Chaque opération ouvre sa propre session via `get_session()` (no global state)
"""
from __future__ import annotations

import os
from pathlib import Path

from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# =============================================================================
# Chemin DB
# =============================================================================

def _db_path() -> Path:
    base = Path(os.environ.get("ROSETTA_API_OUTPUT", "~/rosetta-data/api_jobs")).expanduser()
    base.mkdir(parents=True, exist_ok=True)
    return base / "rosetta.db"


# =============================================================================
# Engine
# =============================================================================

def _create_engine():
    db_url = f"sqlite:///{_db_path()}"
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False},
        # pool_pre_ping évite les connexions stale après hibernation
        pool_pre_ping=True,
    )

    @event.listens_for(engine, "connect")
    def _set_pragmas(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine


engine = _create_engine()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# =============================================================================
# Base déclarative
# =============================================================================

class Base(DeclarativeBase):
    pass


# =============================================================================
# Initialisation des tables
# =============================================================================

def create_tables() -> None:
    """Crée les tables si elles n'existent pas (idempotent)."""
    from api.models import Job, JobLog  # import local pour éviter circulaire
    Base.metadata.create_all(engine)


def get_session() -> Session:
    """Retourne une session SQLAlchemy — à utiliser comme context manager."""
    return SessionLocal()
