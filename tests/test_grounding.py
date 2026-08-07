"""
Garde anti-hallucination des insights LLM (#8).

check_grounding signale les artefacts « code » cités par un insight mais absents
du source. Conservateur : n'attrape que le code (pas la prose ni les acronymes).
Exemples 100 % fictifs.
"""

import pytest

from analyzers.grounding import extract_cited_artifacts, check_grounding, _is_code_like


@pytest.mark.parametrize("tok,expected", [
    ("TP2", True),
    ("C_TYP_FLX", True),
    ("getToken", True),
    ("statut_code", True),
    ("SLA", False),      # acronyme légitime
    ("API", False),
    ("le", False),       # trop court
    ("client", False),   # mot de prose minuscule
    ("Client", False),   # PascalCase mono-mot sans autre signal → prose capitalisée
])
def test_is_code_like(tok, expected):
    assert _is_code_like(tok) is expected


def test_extract_variables_et_constantes():
    text = "La valeur $statut vaut 'TP2' et la colonne C_TYP_FLX pilote getToken."
    arts = extract_cited_artifacts(text)
    assert "$statut" in arts
    assert "TP2" in arts
    assert "C_TYP_FLX" in arts
    assert "getToken" in arts


def test_extract_ignore_prose_et_acronymes():
    text = "Le SLA impose une réponse rapide selon la règle métier définie."
    assert extract_cited_artifacts(text) == set()


def test_grounding_ok_si_present():
    insight = "La décision repose sur la valeur 'TP2' du champ $statut."
    source = "if ($statut == 'TP2') { escalade(); }"
    assert check_grounding(insight, source) == []


def test_grounding_signale_absent():
    insight = "Le code 'TP2' déclenche un traitement via C_TYP_FLX."
    source = "if ($statut == 'ST_OUV') { fermer(); }"  # ni TP2 ni C_TYP_FLX
    ungrounded = check_grounding(insight, source)
    assert "TP2" in ungrounded
    assert "C_TYP_FLX" in ungrounded


def test_grounding_variable_absente():
    assert check_grounding("dépend de $inexistant", "return $autre;") == ["$inexistant"]


def test_source_vide_ne_flag_rien():
    assert check_grounding("cite 'TP2'", "") == []


def test_badge_doc_insight_non_ancre():
    from generators.business_doc_generator import _grounding_suffix
    from ir.schema import LLMInsight
    ko = LLMInsight(flag_id="f", business_rule="x", confidence=0.3,
                    grounded=False, ungrounded_terms=["TP2", "C_TYP_FLX"])
    suffix = _grounding_suffix(ko)
    assert "à vérifier" in suffix and "TP2" in suffix
    ok = LLMInsight(flag_id="f", business_rule="x", confidence=0.9)
    assert _grounding_suffix(ok) == ""
    assert _grounding_suffix(None) == ""
