"""
Config DB Importer — Transitions paramétrables depuis exports Oracle.

Lit des CSV exportés des tables de configuration du système legacy et produit
des Relation avec pattern=config_db, fusionnées dans la KB et la cartographie.

Formats supportés :
  Format 1 — scenario_modules.csv     : transitions séquentielles entre modules
  Format 2 — parametres_transfert.csv : implications des paramètres de transfert
  Format 3 — automatisation_values.csv: situation → action selon contexte
"""
from __future__ import annotations

import csv
from pathlib import Path

from ir.schema import EntityRef, Relation


def _rel_dedup_key(r: Relation) -> tuple[str, str, str]:
    return (r.kind, r.from_entity.value, r.to_entity.value)


class ConfigDbImporter:
    """Importe des CSV Oracle et produit des Relation avec pattern='config_db'."""

    def __init__(self) -> None:
        self._counter = 0

    # ── Format 1 — Modules de scénario ─────────────────────────────────────

    def import_scenario_modules(self, csv_path: Path) -> list[Relation]:
        """Transitions séquentielles entre modules d'un scénario paramétrable.

        Colonnes attendues : id_scenario, ordre, code_module, valeur, id_param
        Ordre : si la colonne 'ordre' est présente elle prime ; sinon ordre CSV.
        """
        rows = self._read_csv(csv_path)
        by_scenario: dict[str, list[dict]] = {}
        for row in rows:
            sid = row.get("id_scenario", "").strip()
            if sid:
                by_scenario.setdefault(sid, []).append(row)

        relations: list[Relation] = []
        seen: set[tuple[str, str, str]] = set()

        for scenario_id, modules in by_scenario.items():
            try:
                modules.sort(key=lambda m: int(m.get("ordre", 0) or 0))
            except (ValueError, TypeError):
                pass

            domaine = self._guess_domaine(scenario_id)

            # Point d'entrée : scénario → premier module
            if modules:
                first_code = self._module_code(modules[0])
                rel = self._make_relation(
                    kind="requires",
                    from_e=EntityRef(type="code", value=scenario_id),
                    to_e=EntityRef(type="module", value=first_code),
                    domaine=domaine,
                    conditions=[f"premier module du scénario {scenario_id}"],
                )
                k = _rel_dedup_key(rel)
                if k not in seen:
                    relations.append(rel)
                    seen.add(k)

            # Transitions séquentielles
            for i in range(len(modules) - 1):
                from_code = self._module_code(modules[i])
                to_code = self._module_code(modules[i + 1])
                rel = self._make_relation(
                    kind="transitions_to",
                    from_e=EntityRef(type="module", value=from_code),
                    to_e=EntityRef(type="module", value=to_code),
                    domaine=domaine,
                    conditions=[f"scénario {scenario_id}, ordre {i + 1}→{i + 2}"],
                )
                k = _rel_dedup_key(rel)
                if k not in seen:
                    relations.append(rel)
                    seen.add(k)
                else:
                    # Même transition dans un autre scénario → enrichir les conditions
                    existing = next(r for r in relations if _rel_dedup_key(r) == k)
                    cond = f"scénario {scenario_id}, ordre {i + 1}→{i + 2}"
                    if cond not in existing.conditions:
                        existing.conditions.append(cond)

        return relations

    # ── Format 2 — Paramètres de transfert ─────────────────────────────────

    def import_parametres_transfert(self, csv_path: Path) -> list[Relation]:
        """Implications des paramètres de transfert de responsabilité.

        Colonnes attendues : id_param, mode_transfert,
          exec_dernier_module_cas_1_2, exec_dernier_module_cas_2_3
        """
        relations: list[Relation] = []
        seen: set[tuple[str, str, str]] = set()

        for row in self._read_csv(csv_path):
            param_id = f"id_param_{row.get('id_param', '').strip()}"
            if not row.get("id_param"):
                continue

            if row.get("mode_transfert", "").strip():
                rel = self._make_relation(
                    kind="implies",
                    from_e=EntityRef(type="code", value=param_id),
                    to_e=EntityRef(type="code", value=f"MODE_TRANSFERT={row['mode_transfert'].strip()}"),
                    domaine="configuration",
                    conditions=[],
                )
                k = _rel_dedup_key(rel)
                if k not in seen:
                    relations.append(rel)
                    seen.add(k)

            if row.get("exec_dernier_module_cas_1_2", "").strip() == "1":
                rel = self._make_relation(
                    kind="implies",
                    from_e=EntityRef(type="code", value=param_id),
                    to_e=EntityRef(type="event", value="saut vers dernier module (cas 1 ou 2)"),
                    domaine="configuration",
                    conditions=[],
                )
                k = _rel_dedup_key(rel)
                if k not in seen:
                    relations.append(rel)
                    seen.add(k)

            if row.get("exec_dernier_module_cas_2_3", "").strip() == "1":
                rel = self._make_relation(
                    kind="implies",
                    from_e=EntityRef(type="code", value=param_id),
                    to_e=EntityRef(type="event", value="saut vers dernier module (cas 2 ou 3)"),
                    domaine="configuration",
                    conditions=[],
                )
                k = _rel_dedup_key(rel)
                if k not in seen:
                    relations.append(rel)
                    seen.add(k)

        return relations

    # ── Format 3 — Valeurs d'automatisation (situation → action) ───────────

    def import_automatisation_values(self, csv_path: Path) -> list[Relation]:
        """Transitions situation → action selon contexte (code_detecteur, type_collecte).

        Colonnes attendues : code_detecteur, type_collecte, code_automatisation,
          situation, categorie, action
        Confirme ou complète les relations extraites par Pattern F du code PHP.
        """
        relations: list[Relation] = []
        seen: set[tuple[str, str, str]] = set()

        for row in self._read_csv(csv_path):
            situation = row.get("situation", "").strip()
            action = row.get("action", "").strip()
            if not situation or not action:
                continue

            conditions: list[str] = []
            code_auto = row.get("code_automatisation", "").strip()
            categorie = row.get("categorie", "").strip()
            if code_auto:
                conditions.append(f"code_auto={code_auto}")
            if categorie:
                conditions.append(f"categorie={categorie}")

            domaine = self._guess_domaine(code_auto)

            rel = self._make_relation(
                kind="transitions_to",
                from_e=EntityRef(type="situation", value=situation),
                to_e=EntityRef(type="event", value=action),
                domaine=domaine,
                conditions=conditions,
            )
            k = _rel_dedup_key(rel)
            if k not in seen:
                relations.append(rel)
                seen.add(k)

        return relations

    # ── Fusion code + config ────────────────────────────────────────────────

    def merge_with_code_relations(
        self,
        config_rels: list[Relation],
        code_rels: list[dict],
    ) -> tuple[list[dict], list[Relation]]:
        """Fusionne les relations config_db avec les relations code existantes.

        Quand une relation transitions_to(A, B) existe dans le code ET en config_db,
        la relation code est enrichie avec confirmed_by_both=True et confiance=high.

        Returns:
            (enriched_code_rels, new_config_rels)
            new_config_rels : relations config_db sans doublon dans le code
        """
        code_index: dict[tuple[str, str, str], int] = {}
        for i, r in enumerate(code_rels):
            fe = (r.get("from_entity") or {})
            te = (r.get("to_entity") or {})
            key = (r.get("kind", ""), fe.get("value", ""), te.get("value", ""))
            code_index[key] = i

        enriched_code = [dict(r) for r in code_rels]
        new_config: list[Relation] = []

        for rel in config_rels:
            key = (rel.kind, rel.from_entity.value, rel.to_entity.value)
            if key in code_index:
                idx = code_index[key]
                enriched_code[idx]["confirmed_by_both"] = True
                enriched_code[idx]["confiance"] = "high"
            else:
                new_config.append(rel)

        return enriched_code, new_config

    # ── Helpers ─────────────────────────────────────────────────────────────

    def _read_csv(self, path: Path) -> list[dict]:
        with path.open(encoding="utf-8-sig") as f:
            return list(csv.DictReader(f))

    def _make_relation(
        self,
        kind: str,
        from_e: EntityRef,
        to_e: EntityRef,
        domaine: str,
        conditions: list[str],
    ) -> Relation:
        self._counter += 1
        return Relation(
            id=f"cfg_{self._counter:04d}",
            kind=kind,
            from_entity=from_e,
            to_entity=to_e,
            direction="one_way",
            domaine=domaine,
            confiance="high",
            conditions=conditions,
            pattern="config_db",
            semantique="",
        )

    @staticmethod
    def _module_code(row: dict) -> str:
        """Préfère code_module sur valeur pour identifier un module."""
        code = row.get("code_module", "").strip()
        if code:
            return code
        return row.get("valeur", "").strip().upper().replace(" ", "_").replace("'", "")

    @staticmethod
    def _guess_domaine(identifier: str) -> str:
        ident = identifier.lower()
        if "dslam" in ident:
            return "automatisation-dslam"
        if "evt" in ident or "event" in ident:
            return "automatisation-evt"
        if "carte" in ident:
            return "automatisation-carte"
        if "commut" in ident:
            return "automatisation-commut"
        if "ventil" in ident:
            return "automatisation-ventilateur"
        if "scen" in ident:
            return "scenario"
        if "aircom" in ident:
            return "automatisation-dslam"
        return "configuration"
