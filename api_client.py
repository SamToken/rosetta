"""Rosetta API Client — mode Remote (--api <url>).

Utilisé exclusivement quand --api est passé à rosetta_analyze.py.
httpx est importé en lazy pour ne pas bloquer le mode local
(qui n'a pas besoin de FastAPI ni de ce module).
"""
from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Optional


class RosettaClient:
    """Client HTTP pour l'API Rosetta — soumet un job et streame les logs."""

    POLL_INTERVAL = 2.0   # secondes entre deux GET /audit/{id}
    POLL_TIMEOUT = 1800   # 30 minutes — abandon si le job ne termine pas

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self._httpx = self._require_httpx()

    # ── Dépendance lazy (le mode local reste 0-dépendance httpx) ─────────────

    @staticmethod
    def _require_httpx():
        try:
            import httpx  # noqa: PLC0415
            return httpx
        except ImportError:
            print(
                "Erreur : le mode --api requiert le package httpx.\n"
                "  pip install httpx",
                file=sys.stderr,
            )
            sys.exit(1)

    # ── Point d'entrée public ─────────────────────────────────────────────────

    def run(
        self,
        php_files: list[Path],
        *,
        no_llm: bool = False,
        model: str = "claude-sonnet-4-6",
        bug_check: bool = False,
        kb_root: Optional[Path] = None,
        call_graph_root: Optional[Path] = None,
        contexte: str = "",
    ) -> dict:
        """Soumet le job, poll jusqu'à 'success'/'error', retourne la réponse complète."""
        n = len(php_files)
        print(f"\n📡 Mode Remote — {n} fichier(s) PHP → {self.base_url}")

        job_id = self._start_job(
            php_files,
            no_llm=no_llm,
            model=model,
            bug_check=bug_check,
            kb_root=kb_root,
            call_graph_root=call_graph_root,
            contexte=contexte,
        )
        print(f"🚀 Job soumis  : {job_id}")
        print(f"   Suivi live → {self.base_url}/audit/{job_id}")
        print()

        return self._poll(job_id)

    # ── Soumission ────────────────────────────────────────────────────────────

    def _start_job(
        self,
        php_files: list[Path],
        *,
        no_llm: bool,
        model: str,
        bug_check: bool,
        kb_root: Optional[Path],
        call_graph_root: Optional[Path],
        contexte: str,
    ) -> str:
        """POST /audit/start → job_id."""
        payload: dict = {
            "php_paths": [str(p.resolve()) for p in php_files],
            "no_llm": no_llm,
            "model": model,
            "bug_check": bug_check,
            "contexte": contexte,
        }
        if kb_root:
            payload["kb_root"] = str(kb_root)
        if call_graph_root:
            payload["call_graph_root"] = str(call_graph_root)

        try:
            with self._httpx.Client(timeout=30) as client:
                resp = client.post(f"{self.base_url}/audit/start", json=payload)
                resp.raise_for_status()
                return resp.json()["job_id"]
        except self._httpx.ConnectError:
            print(
                f"Erreur : impossible de joindre l'API Rosetta à {self.base_url}\n"
                "  Vérifier que le serveur est démarré :\n"
                "    cd ~/projects/rosetta\n"
                "    ROSETTA_KB=~/rosetta-data/knowledge_base.yaml \\\n"
                "      .venv/bin/uvicorn api.main:app --reload --port 8765 --host 127.0.0.1",
                file=sys.stderr,
            )
            sys.exit(1)
        except self._httpx.HTTPStatusError as exc:
            detail = exc.response.text[:400]
            print(
                f"Erreur API {exc.response.status_code} lors de la soumission :\n  {detail}",
                file=sys.stderr,
            )
            sys.exit(1)

    # ── Polling avec affichage des logs en temps réel ─────────────────────────

    def _poll(self, job_id: str) -> dict:
        """GET /audit/{job_id} en boucle jusqu'à 'success' ou 'error'."""
        seen_logs = 0
        elapsed = 0.0

        try:
            with self._httpx.Client(timeout=15) as client:
                while elapsed < self.POLL_TIMEOUT:
                    resp = client.get(f"{self.base_url}/audit/{job_id}")
                    resp.raise_for_status()
                    data: dict = resp.json()

                    # Afficher uniquement les nouveaux messages de log
                    logs: list[str] = data.get("logs", [])
                    for msg in logs[seen_logs:]:
                        print(f"  {msg}")
                    seen_logs = len(logs)

                    status: str = data.get("status", "")
                    if status in ("success", "error"):
                        return data

                    time.sleep(self.POLL_INTERVAL)
                    elapsed += self.POLL_INTERVAL

        except KeyboardInterrupt:
            print(f"\n⚠  Interruption — job {job_id} toujours en cours sur le serveur.")
            sys.exit(130)
        except self._httpx.ConnectError:
            print("\nErreur : connexion perdue avec l'API en cours de polling.", file=sys.stderr)
            sys.exit(1)

        print(
            f"\nTimeout : le job {job_id} n'a pas terminé en {self.POLL_TIMEOUT}s.",
            file=sys.stderr,
        )
        sys.exit(1)
