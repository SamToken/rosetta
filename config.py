"""Rosetta — Configuration centralisée et gestion des secrets."""
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Chargement .env (sans dépendance externe — compatible NixOS/WSL)
# ---------------------------------------------------------------------------
_env_path = Path(__file__).parent / ".env"
if _env_path.exists():
    for _line in _env_path.read_text(encoding="utf-8").splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _key, _, _val = _line.partition("=")
            os.environ.setdefault(_key.strip(), _val.strip())


def _require(key: str) -> str:
    """Retourne la valeur d'une variable obligatoire ou lève une erreur explicite."""
    val = os.environ.get(key, "").strip()
    if not val:
        raise EnvironmentError(
            f"\n[Rosetta] Variable d'environnement obligatoire manquante : {key}\n"
            f"  1. Copier .env.example → .env\n"
            f"  2. Renseigner la valeur réelle dans .env\n"
            f"  3. OU exporter directement : export {key}=<valeur>\n"
        )
    return val


class Settings:
    """Accès centralisé aux secrets et chemins configurables.

    Toutes les valeurs sont lues depuis l'environnement (priorité .env < os.environ).
    Aucune valeur sensible n'est hardcodée.
    """

    # ── Clés LLM ────────────────────────────────────────────────────────────

    @property
    def anthropic_api_key(self) -> str:
        return _require("ANTHROPIC_API_KEY")

    @property
    def google_api_key(self) -> str | None:
        return os.environ.get("GOOGLE_API_KEY") or None

    # ── Modèle par défaut ────────────────────────────────────────────────────

    @property
    def default_model(self) -> str:
        return os.environ.get("ROSETTA_DEFAULT_MODEL", "claude-sonnet-4-6")

    # ── Chemins opérationnels ────────────────────────────────────────────────

    @property
    def kb_path(self) -> Path:
        raw = os.environ.get("ROSETTA_KB", "~/rosetta-data/kb")
        return Path(raw).expanduser()

    @property
    def memory_base(self) -> Path:
        raw = os.environ.get("ROSETTA_MEMORY", "~/rosetta-memory")
        return Path(raw).expanduser()

    @property
    def telemetry_path(self) -> Path:
        raw = os.environ.get("ROSETTA_TELEMETRY", "~/rosetta-data/roi_metrics.jsonl")
        return Path(raw).expanduser()

    # ── Validation au démarrage ──────────────────────────────────────────────

    def validate_for_llm(self) -> None:
        """Lève EnvironmentError si les variables LLM obligatoires sont absentes.

        Appeler avant tout appel au LLM, pas au démarrage global.
        """
        self.anthropic_api_key  # déclenche _require()


settings = Settings()
