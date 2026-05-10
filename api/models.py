"""Rosetta API — Modèles SQLAlchemy 2.0.

Tables :
    job      — un enregistrement par job d'audit (statut, résultat JSON)
    job_log  — messages de progression, append-only O(1)
"""
from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database import Base


class Job(Base):
    __tablename__ = "job"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="queued")
    created_at: Mapped[str] = mapped_column(String(32), nullable=False)
    started_at: Mapped[str | None] = mapped_column(String(32), nullable=True)
    finished_at: Mapped[str | None] = mapped_column(String(32), nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Résultat sérialisé en JSON — None tant que le job n'est pas terminé
    result_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    logs: Mapped[list[JobLog]] = relationship(
        "JobLog", back_populates="job", order_by="JobLog.idx", cascade="all, delete-orphan"
    )


class JobLog(Base):
    __tablename__ = "job_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("job.id", ondelete="CASCADE"), nullable=False)
    idx: Mapped[int] = mapped_column(Integer, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)

    job: Mapped[Job] = relationship("Job", back_populates="logs")
