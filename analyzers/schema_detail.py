"""Couche 2 — détail de schéma Oracle injecté à la demande, par fichier.

Complète l'inventaire résident (couche 1) : quand un fichier touche la base, on
ajoute les colonnes des tables qu'il référence. Bon marché (~61 tok médian/fichier
mesuré) donc plafond confortable, pas serré.

VERROU GLOBAL (jamais par table) : si la source du sidecar détail diffère de celle
de l'inventaire, la couche 2 est coupée pour TOUT le run (couche 1 seule) avec
warning. Un refus par table donnerait un contexte où certaines tables ont leur
détail et d'autres non — l'absence se lit « table sans colonnes », pire que rien.
Un détail périmé face à un inventaire régénéré = types faux dans du code généré
qui compile → invisible.

EXTRACTION : tables = source ∩ inventaire, frontière de mot + longueur ≥ 4 (les
noms courts d'Oracle — ID, TYPE… — sont des homographes PHP fréquents).

FK profondeur 1 (partielle) : table directe → colonnes (plafond
``COL_CAP`` + marqueur explicite) ; cible de FK → stub PK+rôle. **CONDITIONNÉE À
LA RÉ-EXTRACTION ENRICHIE** : en mode dégradé ``fk == PK_UNKNOWN`` → l'expansion
ne tourne pas. Ce chemin FK n'a JAMAIS été exercé (aucune donnée de contrainte à
ce jour) — à revalider dès que le TSV enrichi arrive.

DIAGNOSTIC MIGRATION : tables référencées en position SQL mais absentes de
l'inventaire → « morte » (candidat suppression) ou « dynamique » (refactoring
Doctrine obligatoire), écrites dans un fichier de sortie exploitable
(``write_migration_signals``), pas noyées dans les logs.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from services.kb_service import KBService, _estimate_tokens

COL_CAP = 40                 # plafond colonnes/table (validé — borne TICKET_ASTRO 51 col)
_MIN_TABLE_LEN = 4           # frontière anti-homographe (précision 2)
_PK_UNKNOWN = KBService.PK_UNKNOWN

# Références de table en position SQL (littérales) — pour le diagnostic morte/dyn.
_SQL_TABLE_REF = re.compile(
    r"(?:FROM|JOIN|INTO|UPDATE)\s+[\"']?([A-Za-z][A-Za-z0-9_]{3,})[\"']?",
    re.IGNORECASE,
)
# Construction dynamique de nom de table (concaténation / variable après FROM…).
_DYNAMIC_TABLE = re.compile(
    r"(?:FROM|JOIN|INTO|UPDATE)\s+(?:\$\w+|[\"'][A-Za-z0-9_]*[\"']\s*\.)",
    re.IGNORECASE,
)


class SchemaDetailProvider:
    """Construit le bloc détail couche 2 d'un fichier + accumule les diagnostics."""

    def __init__(
        self,
        detail_tables: dict,
        inventory: dict,
        active: bool,
        disabled_reason: str = "",
        col_cap: int = COL_CAP,
    ):
        self._detail = detail_tables or {}
        self._inventory = inventory or {}
        self.active = active
        self.disabled_reason = disabled_reason
        self._col_cap = col_cap
        # Matcher des tables connues, frontière de mot + longueur ≥ 4, casse
        # préservée (les noms sont en MAJUSCULES → pas de match sur du PHP minuscule).
        names = sorted(
            (t for t in self._detail if len(t) >= _MIN_TABLE_LEN),
            key=len, reverse=True,
        )
        self._matcher = (
            re.compile(r"\b(?:" + "|".join(re.escape(n) for n in names) + r")\b")
            if names else None
        )
        # Diagnostics accumulés sur le run
        self.injected_counts: list[int] = []        # tables injectées / fichier
        self.dead_tables: dict[str, set] = {}        # table absente → {fichiers}
        self.dynamic_files: set[str] = set()         # fichiers avec nom dynamique
        self._fk_degraded_seen = False

    # ── Factory ───────────────────────────────────────────────────────────────
    @classmethod
    def from_kb_service(cls, svc: KBService, col_cap: int = COL_CAP) -> "SchemaDetailProvider":
        detail = svc.schema_detail_all()
        inventory = svc.load().get("schema", {}) or {}
        if not detail:
            return cls({}, inventory, active=False,
                       disabled_reason="pas de sidecar détail (couche 2 vide)")
        # VERROU : source unique de l'inventaire == source du sidecar.
        inv_sources = svc.schema_sources()
        det_source = svc.schema_detail_meta().get("source")
        if len(inv_sources) != 1 or not det_source or det_source not in inv_sources:
            reason = (
                f"mismatch source couche 1/2 — inventaire={sorted(inv_sources)} "
                f"vs détail={det_source!r}. Couche 2 coupée (couche 1 seule)."
            )
            return cls(detail, inventory, active=False, disabled_reason=reason)
        return cls(detail, inventory, active=True, col_cap=col_cap)

    # ── Rendu du bloc détail d'un fichier ──────────────────────────────────────
    def detail_block_for(self, source: str, filename: str = "") -> str:
        """Bloc détail des tables référencées dans ``source`` (un fichier)."""
        if not self.active or not source or not self._matcher:
            return ""

        present = sorted(set(self._matcher.findall(source)))
        self.injected_counts.append(len(present))
        self._record_diagnostics(source, present, filename)
        if not present:
            return ""

        lines = ["## Détail schéma — tables de ce fichier"]
        fk_targets: set[str] = set()
        for tbl in present:
            lines.extend(self._render_direct(tbl))
            fk_targets |= self._fk_targets(tbl)

        # Stubs FK profondeur 1 (cibles pas déjà en direct). Vide en dégradé.
        stubs = sorted(fk_targets - set(present))
        if stubs:
            lines.append("Réf. FK (profondeur 1) :")
            for tgt in stubs:
                lines.append(self._render_stub(tgt))

        return "\n".join(lines)

    def _render_direct(self, tbl: str) -> list[str]:
        t = self._detail.get(tbl, {})
        cols = t.get("colonnes", {}) or {}
        pk = t.get("pk", _PK_UNKNOWN)
        out = [f"### {tbl} (PK {pk})"]
        items = list(cols.items())
        for col, meta in items[: self._col_cap]:
            nn = "" if meta.get("nullable", True) else " NOT NULL"
            out.append(f"  {col}: {meta.get('type', '?')}{nn}")
        if len(items) > self._col_cap:
            # Marqueur de troncature EXPLICITE, jamais silencieux.
            out.append(
                f"  [+{len(items) - self._col_cap} colonnes tronquées — "
                f"{tbl} fait {len(items)} col, voir sidecar]"
            )
        return out

    def _fk_targets(self, tbl: str) -> set[str]:
        fk = self._detail.get(tbl, {}).get("fk")
        if fk == _PK_UNKNOWN or not isinstance(fk, dict):
            # Dégradé : contraintes pas extraites → pas d'expansion FK.
            self._fk_degraded_seen = True
            return set()
        return set(fk.values())

    def _render_stub(self, tbl: str) -> str:
        e = self._inventory.get(tbl, {})
        role = e.get("label", "")
        role_part = f" — {role}" if role and role != f"Table {tbl}" else ""
        return f"  {tbl} [PK {e.get('pk', _PK_UNKNOWN)}]{role_part}"

    # ── Diagnostic morte / dynamique ───────────────────────────────────────────
    def _record_diagnostics(self, source: str, present: list[str], filename: str) -> None:
        # Référencée en position SQL, absente de l'inventaire → table morte.
        for ref in _SQL_TABLE_REF.findall(source):
            up = ref.upper()
            if up not in self._inventory and up not in present:
                self.dead_tables.setdefault(up, set()).add(filename or "?")
        # Nom construit dynamiquement → refactoring Doctrine obligatoire.
        if _DYNAMIC_TABLE.search(source):
            self.dynamic_files.add(filename or "?")

    # ── Sortie exploitable ─────────────────────────────────────────────────────
    def injected_rate(self) -> float:
        return (sum(self.injected_counts) / len(self.injected_counts)) if self.injected_counts else 0.0

    def has_signals(self) -> bool:
        return bool(self.dead_tables or self.dynamic_files)

    def write_migration_signals(self, path: Path) -> None:
        """Écrit les signaux migration (tables mortes / noms dynamiques) en Markdown."""
        lines = ["# Signaux migration — schéma", ""]
        lines.append("## Tables référencées absentes de l'inventaire (candidats suppression)")
        if self.dead_tables:
            for tbl in sorted(self.dead_tables):
                files = ", ".join(sorted(self.dead_tables[tbl])) or "?"
                lines.append(f"- **{tbl}** — {files}")
        else:
            lines.append("_Aucune._")
        lines += ["", "## Noms de tables construits dynamiquement (refactoring Doctrine obligatoire)"]
        if self.dynamic_files:
            for f in sorted(self.dynamic_files):
                lines.append(f"- {f}")
        else:
            lines.append("_Aucun._")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
