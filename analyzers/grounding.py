"""
Grounding — garde anti-hallucination des insights LLM (#8)
==========================================================
Vérifie que les artefacts « code » cités par un insight LLM (variables $x,
constantes TP2/C_TYP_FLX, identifiants camelCase, colonnes snake_case, valeurs
quotées) existent bien dans le source réellement fourni au LLM (fragment +
corps de méthode). Un artefact cité mais absent = hallucination probable.

Déterministe, zéro réseau. Volontairement conservateur : ne cible que les
tokens manifestement « code » (contenant `_`, un chiffre, ou une casse mixte),
pour éviter de flaguer la prose métier légitime ou les acronymes (SLA, API…).
"""

from __future__ import annotations

import re

# Acronymes/mots que le LLM emploie légitimement sans qu'ils soient dans le code.
_STOPWORDS = frozenset({
    "SLA", "API", "APIS", "URL", "HTTP", "HTTPS", "SQL", "BDD", "REST",
    "PO", "IHM", "UI", "ORM", "DTO", "JSON", "XML", "CSV",
})


def _is_code_like(token: str) -> bool:
    """True si le token ressemble à du code (pas de la prose)."""
    t = token.strip().strip("`").strip("'\"").lstrip("$")
    if len(t) < 3 or t.upper() in _STOPWORDS:
        return False
    if "_" in t:
        return True
    if any(c.isdigit() for c in t):
        return True
    # casse INTERNE (camelCase getToken, PascalCase FooService) → identifiant.
    # Une simple majuscule initiale (Client, Ticket) = prose, pas du code.
    return any(c.isupper() for c in t[1:]) and any(c.islower() for c in t)


def extract_cited_artifacts(text: str) -> set[str]:
    """Artefacts « code » cités dans un texte d'insight."""
    if not text:
        return set()
    arts: set[str] = set()

    # Variables PHP — toujours retenues (le sigil $ marque le code)
    for m in re.finditer(r"\$[A-Za-z_]\w*", text):
        arts.add(m.group(0))

    # Contenu entre backticks
    for m in re.finditer(r"`([^`]+)`", text):
        inner = m.group(1).strip()
        if _is_code_like(inner):
            arts.add(inner)

    # Littéraux quotés (valeurs métier : 'TP2', "ST_OUV")
    for m in re.finditer(r"""['"]([A-Za-z0-9_]+)['"]""", text):
        if _is_code_like(m.group(1)):
            arts.add(m.group(1))

    # Identifiants nus code-like (TP2, C_TYP_FLX, getToken, snake_case)
    for m in re.finditer(r"\b[A-Za-z_][A-Za-z0-9_]{2,}\b", text):
        if _is_code_like(m.group(0)):
            arts.add(m.group(0))

    return arts


def check_grounding(insight_text: str, source_text: str) -> list[str]:
    """Retourne les artefacts cités par l'insight mais ABSENTS du source.

    Liste vide = insight ancré. Comparaison insensible à la casse, par
    sous-chaîne (conservateur : on préfère rater une hallucination que d'en
    inventer une)."""
    source_low = (source_text or "").lower()
    if not source_low:
        return []
    ungrounded: list[str] = []
    for art in extract_cited_artifacts(insight_text):
        needle = art.lstrip("$").strip("`").strip("'\"").lower()
        if needle and needle not in source_low:
            ungrounded.append(art)
    return sorted(ungrounded)
