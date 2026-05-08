#!/usr/bin/env python3
"""
inject_pending.py — Cluster les insights LLM et injecte dans pending_validation

Usage:
    python tools/inject_pending.py <business_logic.json> [options]

Options:
    --domaine   Domaine KB cible (défaut: slug du fichier JSON)
    --kb-path   Chemin vers le KB (défaut: $ROSETTA_KB)
    --replace   Remplace toutes les entrées du domaine (au lieu d'upsert)
    --dry-run   Affiche sans écrire

Algorithme de clustering:
    CLUSTER_A (magic_value, hardcoded_situation_code)
        → clé = (type, littéral extrait du fragment)
        → représentant = insight avec confidence la plus basse (le moins sûr)

    CLUSTER_B (missing_branch, external_state_dependency, dynamic_session_key)
        → clé = (type, method_name)
        → représentant = insight avec confidence la plus basse

    unmapped_dep, strong_coupling → ignorés (pas de valeur pour le PO)
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from rosetta_kb import _load_pending, _save_pending, _resolve_kb, _load_kb, _detect_pending_type

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

CLUSTER_A_TYPES = {"magic_value", "hardcoded_situation_code"}
CLUSTER_B_TYPES = {"missing_branch", "external_state_dependency", "dynamic_session_key"}
SKIP_TYPES = {"unmapped_dep", "strong_coupling"}

CONF_TO_PRIORITY = {
    "high":   "high",    # confidence LLM ≥ 0.8
    "medium": "medium",  # confidence LLM ≥ 0.5
    "low":    "low",     # confidence LLM < 0.5
}


# ---------------------------------------------------------------------------
# Extraction de littéral depuis un fragment PHP
# ---------------------------------------------------------------------------

def _extract_literal(fragment: str) -> str:
    """Extrait le premier littéral string significatif du fragment."""
    # Chaînes entre guillemets simples ou doubles (non vides, non triviales)
    for m in re.finditer(r"""['"]([^'"]{2,})['"]""", fragment):
        val = m.group(1)
        if val not in ("", " ", "\n"):
            return val
    # Constante PHP (UPPER_CASE)
    for m in re.finditer(r'\b([A-Z][A-Z0-9_]{2,})\b', fragment):
        return m.group(1)
    # Nombre seul
    for m in re.finditer(r'\b(\d+)\b', fragment):
        return m.group(1)
    return fragment[:40].strip()


def _confidence_to_priority(confidence: float) -> str:
    if confidence >= 0.75:
        return "high"
    if confidence >= 0.5:
        return "medium"
    return "low"


# ---------------------------------------------------------------------------
# Clustering
# ---------------------------------------------------------------------------

def _cluster_key(flag: dict) -> tuple[str, str] | None:
    ftype = flag["type"]
    if ftype in CLUSTER_A_TYPES:
        literal = _extract_literal(flag.get("fragment", ""))
        return (ftype, literal)
    if ftype in CLUSTER_B_TYPES:
        method = flag.get("method_name", flag.get("location", "unknown"))
        return (ftype, method)
    return None  # SKIP_TYPES and others


def cluster_insights(flags: list[dict], insights: dict[str, dict]) -> list[dict]:
    """
    Retourne une liste d'entrées clustérisées.

    Chaque entrée représente un concept unique.
    Le représentant est le membre du cluster avec la confidence la plus basse
    (le moins sûr → le plus utile à valider par le PO).
    """
    groups: dict[tuple, list[dict]] = defaultdict(list)

    for flag in flags:
        key = _cluster_key(flag)
        if key is None:
            continue
        insight = insights.get(flag["id"])
        groups[key].append({
            "flag": flag,
            "insight": insight,
            "confidence": insight["confidence"] if insight else 0.0,
        })

    result = []
    for (ftype, value), members in groups.items():
        # Représentant = confidence la plus basse (plus incertain = plus utile pour PO)
        representative = min(members, key=lambda m: m["confidence"])
        flag = representative["flag"]
        insight = representative["insight"]

        # Rassemble tous les fichiers/lignes
        fichiers = sorted({
            f"{m['flag']['method_name']}:{m['flag']['source_line']}"
            for m in members
            if m["flag"].get("method_name") and m["flag"].get("source_line")
        })

        # Priorité = max des confidences (si au moins un très sûr → question importante)
        max_conf = max(m["confidence"] for m in members)
        priorite = _confidence_to_priority(max_conf)

        # Question : celle de l'insight représentant, ou celle du flag
        question = ""
        contexte = ""
        if insight:
            question = insight.get("missing_context", "")
            business_rule = insight.get("business_rule", "")
            contexte = _first_sentence(business_rule)
        if not question:
            question = flag.get("question", f"Comportement attendu pour {repr(value)} ?")

        # Code unique: type--valeur normalisée
        safe_value = re.sub(r"[^\w-]", "_", str(value))[:40]
        code = f"DI-{ftype}--{safe_value}"

        result.append({
            "code": code,
            "concept": f"{ftype}::{value}",
            "question": question,
            "contexte": contexte,
            "fichiers": fichiers,
            "priorite": priorite,
            "domaine": flag.get("domaine", ""),
            "flag_type": ftype,
            "occurrences": len(members),
            "type": "po_question",
        })

    # Tri: priorité descendante, puis occurrences descendantes
    PRIO_ORDER = {"high": 0, "medium": 1, "low": 2}
    result.sort(key=lambda e: (PRIO_ORDER.get(e["priorite"], 9), -e["occurrences"]))
    return result


def _first_sentence(text: str, max_len: int = 220) -> str:
    if not text:
        return ""
    m = re.search(r'[.!?]', text)
    end = m.start() + 1 if m else len(text)
    result = text[:end].strip()
    if len(result) <= max_len:
        return result
    # Couper au dernier espace avant max_len pour ne pas tronquer en plein mot
    cut = result.rfind(' ', 0, max_len)
    return result[:cut] + '…' if cut > 0 else result[:max_len]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Cluster insights et injecte dans pending_validation")
    parser.add_argument("json_file", help="Fichier business_logic.json")
    parser.add_argument("--domaine", default=None, help="Domaine KB cible")
    parser.add_argument("--kb-path", default=os.environ.get("ROSETTA_KB", "~/rosetta-data/kb"))
    parser.add_argument("--replace", action="store_true", help="Remplace toutes les entrées du domaine")
    parser.add_argument("--dry-run", action="store_true", help="Affiche sans écrire")
    args = parser.parse_args()

    json_path = Path(args.json_file)
    if not json_path.exists():
        print(f"[ERR] Fichier introuvable : {json_path}", file=sys.stderr)
        return 1

    data = json.loads(json_path.read_text(encoding="utf-8"))

    flags = data.get("flags", [])
    raw_insights = data.get("llm_insights", [])
    insights_by_id = {i["flag_id"]: i for i in raw_insights}

    # Domaine par défaut : slug du nom de fichier (sans suffixes)
    domaine = args.domaine
    if not domaine:
        stem = json_path.stem  # ex: DemandeInterventionService_business_logic
        stem = re.sub(r"_business_logic$", "", stem)
        domaine = re.sub(r"([A-Z])", r"-\1", stem).lstrip("-").lower()

    print(f"📂 Fichier      : {json_path.name}")
    print(f"🏷️  Domaine      : {domaine}")
    print(f"📊 Flags total  : {len(flags)}")

    clusters = cluster_insights(flags, insights_by_id)

    # Statistiques par type
    from collections import Counter
    type_counts = Counter(c["flag_type"] for c in clusters)
    prio_counts = Counter(c["priorite"] for c in clusters)
    total_flags_covered = sum(c["occurrences"] for c in clusters)

    print(f"🔀 Clusters     : {len(clusters)} concepts uniques ({total_flags_covered} flags couverts)")
    print(f"   Par type     : {dict(type_counts)}")
    print(f"   Par priorité : {dict(prio_counts)}")

    if args.dry_run:
        print("\n[DRY-RUN] Aperçu des 5 premiers clusters :")
        for c in clusters[:5]:
            print(f"  [{c['priorite'].upper():6}] {c['code']} (×{c['occurrences']})")
            print(f"         concept : {c['concept']}")
            print(f"         question: {c['question'][:80]}...")
        return 0

    kb_path = _resolve_kb(args.kb_path)
    pending = _load_pending(kb_path)
    kb_data = _load_kb(kb_path)

    added = updated = skipped = 0

    if args.replace:
        # Supprimer les entrées de ce domaine
        to_delete = [k for k, v in pending.items() if v.get("domaine") == domaine]
        for k in to_delete:
            del pending[k]
        print(f"🗑️  {len(to_delete)} entrées du domaine '{domaine}' supprimées")

    for cluster in clusters:
        code = cluster["code"]
        ptype, dest = _detect_pending_type(code, kb_data, flag_type=cluster["flag_type"])
        entry = {
            "code": code,
            "concept": cluster["concept"],
            "question": cluster["question"],
            "contexte": cluster["contexte"],
            "fichiers": cluster["fichiers"],
            "priorite": cluster["priorite"],
            "domaine": domaine,
            "flag_type": cluster["flag_type"],
            "occurrences": cluster["occurrences"],
            "type": "po_question",
            "pending_type": ptype,
            "destination": dest,
        }

        if code in pending:
            # Ne pas écraser une entrée déjà validée (priorite high depuis PO)
            existing = pending[code]
            if existing.get("validated"):
                skipped += 1
                continue
            pending[code] = entry
            updated += 1
        else:
            pending[code] = entry
            added += 1

    _save_pending(kb_path, pending)

    print(f"\n✅ Injection terminée :")
    print(f"   {added} ajoutée(s)     {updated} mise(s) à jour     {skipped} ignorée(s) (validée)")
    print(f"   KB : {kb_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
