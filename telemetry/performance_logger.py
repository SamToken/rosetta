"""Rosetta — Logger de métriques ROI.

Chaque exécution du pipeline est enregistrée atomiquement dans un fichier JSONL.
Les métriques permettent de prouver l'économie de temps réalisée par rapport
à une revue manuelle.

Constante métier :
    LINES_PER_HOUR_HUMAN = 1000
    → 1 heure de travail humain ≈ 1000 lignes de code auditées manuellement.
    → Ajustable via la variable d'environnement ROSETTA_LINES_PER_HOUR.
"""
import json
import os
import threading
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

LINES_PER_HOUR_HUMAN: int = int(os.environ.get("ROSETTA_LINES_PER_HOUR", "1000"))


@dataclass
class AuditRun:
    """Enregistrement d'une exécution pipeline pour un fichier PHP."""

    timestamp: str                          # ISO-8601 UTC
    filename: str
    file_size_lines: int
    processing_time_seconds: float
    model_used: str                         # "claude-sonnet-4-6" | "--no-llm"
    status: str                             # "success" | "no_llm" | "error"
    flags_total: int = 0
    insights_total: int = 0
    llm_cost_usd: float = 0.0
    kb_coverage_pct: float = 0.0
    human_hours_saved: float = field(init=False)

    def __post_init__(self) -> None:
        self.human_hours_saved = round(self.file_size_lines / LINES_PER_HOUR_HUMAN, 2)


class PerformanceLogger:
    """Enregistre et agrège les métriques ROI des audits Rosetta.

    Usage :
        logger = PerformanceLogger()
        logger.record(AuditRun(...))
        logger.print_summary()
    """

    _write_lock = threading.Lock()  # protège les écritures concurrentes en mode batch parallèle

    def __init__(self, log_path: Optional[Path] = None) -> None:
        from config import settings
        self.log_path = log_path or settings.telemetry_path

    # ── Écriture ─────────────────────────────────────────────────────────────

    def record(self, run: AuditRun) -> None:
        """Ajoute un enregistrement au fichier JSONL (thread-safe)."""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        entry = json.dumps(asdict(run), ensure_ascii=False)
        with PerformanceLogger._write_lock:
            with open(self.log_path, "a", encoding="utf-8") as fh:
                fh.write(entry + "\n")
                fh.flush()

    # ── Lecture ──────────────────────────────────────────────────────────────

    def load_runs(self) -> list[dict]:
        """Charge tous les enregistrements depuis le JSONL."""
        if not self.log_path.exists():
            return []
        lines = self.log_path.read_text(encoding="utf-8").splitlines()
        return [json.loads(ln) for ln in lines if ln.strip()]

    # ── Calculs ROI ──────────────────────────────────────────────────────────

    def human_time_saved(self, file_size_lines: int) -> float:
        """Heures de travail humain évitées pour N lignes de code."""
        return round(file_size_lines / LINES_PER_HOUR_HUMAN, 2)

    def summary(self) -> dict:
        """Calcule les statistiques ROI agrégées."""
        runs = self.load_runs()
        if not runs:
            return {"total_runs": 0}

        successful = [r for r in runs if r["status"] in ("success", "no_llm")]
        total_lines = sum(r["file_size_lines"] for r in runs)
        total_hours_saved = sum(r["human_hours_saved"] for r in runs)
        total_cost = sum(r["llm_cost_usd"] for r in runs)
        total_machine_sec = sum(r["processing_time_seconds"] for r in runs)
        success_rate = len(successful) / len(runs) * 100 if runs else 0.0

        # Économie financière : 75 €/h pour un développeur senior
        hourly_rate_eur = float(os.environ.get("ROSETTA_HOURLY_RATE_EUR", "75"))
        financial_saving_eur = total_hours_saved * hourly_rate_eur

        return {
            "total_runs": len(runs),
            "total_lines_analyzed": total_lines,
            "total_human_hours_saved": round(total_hours_saved, 1),
            "financial_saving_eur": round(financial_saving_eur, 0),
            "total_llm_cost_usd": round(total_cost, 4),
            "total_machine_seconds": round(total_machine_sec, 1),
            "success_rate_pct": round(success_rate, 1),
            "avg_processing_seconds": round(
                total_machine_sec / len(runs) if runs else 0, 1
            ),
            "lines_per_hour_constant": LINES_PER_HOUR_HUMAN,
            "hourly_rate_eur": hourly_rate_eur,
        }

    # ── Affichage ────────────────────────────────────────────────────────────

    def print_summary(self) -> None:
        """Affiche le dashboard ROI dans la console."""
        s = self.summary()
        if s["total_runs"] == 0:
            print("📊 Aucun audit enregistré. Lancer rosetta_analyze.py pour commencer.")
            return

        machine_h = s["total_machine_seconds"] // 3600
        machine_m = (s["total_machine_seconds"] % 3600) // 60
        machine_s = s["total_machine_seconds"] % 60
        machine_str = (
            f"{int(machine_h)}h {int(machine_m)}min {int(machine_s)}s"
            if machine_h
            else f"{int(machine_m)}min {int(machine_s)}s"
        )

        # Largeur intérieure = label (28) + valeur (12) = 40
        # Ligne complète : "│ " (2) + 40 + " │" (2) = 46 chars
        W = 40  # largeur intérieure
        L = 28  # largeur colonne label
        V = 12  # largeur colonne valeur

        def row(label: str, value: str) -> str:
            return f"│ {label:<{L}}{value:>{V}} │"

        def sep() -> str:
            return "│ " + "─" * W + " │"

        print()
        print("┌" + "─" * (W + 2) + "┐")
        print(f"│ {'Rosetta ROI Dashboard':<{W}} │")
        print(sep())
        print(row("Audits effectués",             str(s["total_runs"])))
        print(row("Lignes PHP auditées",          f"{s['total_lines_analyzed']:,}"))
        print(row("Temps machine total",          machine_str))
        print(sep())
        print(row("Heures humaines economisees",  f"{s['total_human_hours_saved']:.1f} h"))
        print(row(f"  @ {LINES_PER_HOUR_HUMAN} lignes/heure", ""))
        print(row("Economie financiere estimee",  f"{s['financial_saving_eur']:.0f} EUR"))
        print(row(f"  @ {int(s['hourly_rate_eur'])} EUR/h dev senior", ""))
        print(sep())
        print(row("Cout LLM total",               f"${s['total_llm_cost_usd']:.4f}"))
        print(row("Taux de succes",               f"{s['success_rate_pct']:.1f} %"))
        print(row("Temps moyen / fichier",        f"{s['avg_processing_seconds']:.1f} s"))
        print("└" + "─" * (W + 2) + "┘")
        print(f"  Donnees : {self.log_path}")
        print()

    def print_roi_line(self, run: AuditRun) -> None:
        """Affiche une ligne ROI inline après chaque analyse."""
        h = int(run.human_hours_saved)
        m = int((run.human_hours_saved - h) * 60)
        time_str = f"{h}h{m:02d}" if h else f"{m}min"
        print(
            f"  ⏱ ROI : {run.file_size_lines:,} lignes → "
            f"{run.human_hours_saved:.1f}h humaines économisées "
            f"({run.processing_time_seconds:.1f}s machine)"
        )
