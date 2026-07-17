"""
Tests for RelationExtractor — Pattern C (switch/case), Pattern F (if/elseif trees),
and Pattern G (variable assigned from call, then tested).
"""

import pytest

from analyzers.relation_extractor import RelationExtractor
from ir.schema import EntryPoint, IRMetadata, IRSchema


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------

_PHP_FIXTURE = """<?php
class TestController {
    public function executeAction() {
        switch ($situation) {
            case 'H1': $next = 'H2'; break;
            case 'H2': $next = 'H3'; break;
            case 'H3': $next = 'ST_FIN'; break;
            default: $next = 'ST_ERR'; break;
        }
        switch ($typeScenario) {
            case 'DSLAM': $service = $this->automatisationDslamService; break;
            case 'COMMUT': $service = $this->automatisationCommutService; break;
        }
    }
}
"""

_KB_TOKENS = {"H1", "H2", "H3", "ST_FIN", "DSLAM", "COMMUT"}


def _make_ir(code: str) -> IRSchema:
    return IRSchema(
        metadata=IRMetadata(source_file="test.php", controller_name="TestController"),
        entry_points=[
            EntryPoint(
                name="executeAction",
                original_name="executeAction",
                raw_code=code,
            )
        ],
    )


def _pattern_c_rels(ir: IRSchema, kb=None):
    """Extract all pattern_c relations from an IR."""
    if kb is None:
        kb = lambda t: t in _KB_TOKENS
    extractor = RelationExtractor(kb)
    all_rels = extractor.extract(ir)
    return [r for r in all_rels if r.pattern == "pattern_c"]


# ---------------------------------------------------------------------------
# Test 1: state transitions
# ---------------------------------------------------------------------------

def test_pattern_c_state_transitions():
    ir = _make_ir(_PHP_FIXTURE)
    rels = _pattern_c_rels(ir)

    trans = [r for r in rels if r.kind == "transitions_to"]
    assert len(trans) == 3, f"Expected 3 transitions_to, got {len(trans)}: {[(r.from_entity.value, r.to_entity.value) for r in trans]}"

    pairs = {(r.from_entity.value, r.to_entity.value) for r in trans}
    assert ("H1", "H2") in pairs
    assert ("H2", "H3") in pairs
    assert ("H3", "ST_FIN") in pairs


# ---------------------------------------------------------------------------
# Test 2: no relation from 'default' case
# ---------------------------------------------------------------------------

def test_pattern_c_no_default():
    ir = _make_ir(_PHP_FIXTURE)
    rels = _pattern_c_rels(ir)

    from_values = {r.from_entity.value for r in rels}
    assert "default" not in from_values, "default case should produce no relations"
    # Also check no 'ST_ERR' target appeared (it's in default body only)
    to_values = {r.to_entity.value for r in rels}
    assert "ST_ERR" not in to_values, "ST_ERR from default case should not appear"


# ---------------------------------------------------------------------------
# Test 3: service property dispatch
# ---------------------------------------------------------------------------

def test_pattern_c_service_dispatch():
    ir = _make_ir(_PHP_FIXTURE)
    rels = _pattern_c_rels(ir)

    requires = [r for r in rels if r.kind == "requires"]
    assert len(requires) == 2, f"Expected 2 requires, got {len(requires)}: {[(r.from_entity.value, r.to_entity.value) for r in requires]}"

    pairs = {(r.from_entity.value, r.to_entity.value) for r in requires}
    assert ("DSLAM", "automatisationDslamService") in pairs
    assert ("COMMUT", "automatisationCommutService") in pairs


# ---------------------------------------------------------------------------
# Test 4: dispatch kinds are "requires" not "transitions_to"
# ---------------------------------------------------------------------------

def test_pattern_c_service_dispatch_kinds():
    ir = _make_ir(_PHP_FIXTURE)
    rels = _pattern_c_rels(ir)

    # The service dispatch relations must be "requires"
    svc_rels = [
        r for r in rels
        if r.to_entity.type == "module"
    ]
    for r in svc_rels:
        assert r.kind == "requires", (
            f"Service dispatch relation should be 'requires', got '{r.kind}' "
            f"for {r.from_entity.value} → {r.to_entity.value}"
        )
    # And none of them should be "transitions_to"
    trans_to_modules = [
        r for r in rels
        if r.kind == "transitions_to" and r.to_entity.type == "module"
    ]
    assert len(trans_to_modules) == 0


# ---------------------------------------------------------------------------
# Test 5: KB filter — empty KB produces 0 relations
# ---------------------------------------------------------------------------

def test_pattern_c_kb_filter():
    ir = _make_ir(_PHP_FIXTURE)
    empty_kb = lambda t: False
    rels = _pattern_c_rels(ir, kb=empty_kb)

    assert len(rels) == 0, (
        f"With empty KB, expected 0 pattern_c relations, got {len(rels)}"
    )


# ===========================================================================
# Pattern F — arbres de décision if/elseif → return returnLongLabel
# ===========================================================================

_PHP_FIXTURE_F = """<?php
class TestService {
    public function process($input) {
        if ($input == 'I1') {
            if ($subState == 'H0') {
                return ['returnLongLabel' => 'ARRET ENCHAINEMENT'];
            } else {
                return ['returnLongLabel' => 'CONFIRMATION DEMANDE INTERVENTION'];
            }
        } else {
            return $this->subProcess($input);
        }
    }

    private function subProcess($state) {
        if ($state == 'H1') {
            return $this->abandon();
        } elseif ($state == 'H2' || $state == 'H3') {
            return ['returnLongLabel' => 'CONFIRMATION DEMANDE INTERVENTION'];
        } elseif ($state == 'H4') {
            return ['returnLongLabel' => 'TRAITEMENT H4 SPECIFIQUE'];
        }
    }
}
"""


def _pattern_f_rels(ir: IRSchema, kb=None):
    """Extract all pattern_f relations from an IR."""
    if kb is None:
        kb = lambda t: False  # situation codes are accepted without KB
    extractor = RelationExtractor(kb)
    return [r for r in extractor.extract(ir) if r.pattern == "pattern_f"]


# ---------------------------------------------------------------------------
# Test F-1: situation codes produce transitions_to to returnLongLabel values
# ---------------------------------------------------------------------------

def test_pattern_f_situation_code_transitions():
    """I1, H0, H2, H3, H4 produce transitions_to from their if-blocks."""
    ir = _make_ir(_PHP_FIXTURE_F)
    rels = _pattern_f_rels(ir)

    trans = {(r.from_entity.value, r.to_entity.value) for r in rels if r.kind == "transitions_to"}

    # outer if ($input == 'I1') sees both nested return labels
    assert ("I1", "ARRET ENCHAINEMENT") in trans, f"Missing I1→ARRET; got {trans}"
    assert ("I1", "CONFIRMATION DEMANDE INTERVENTION") in trans

    # nested if ($subState == 'H0')
    assert ("H0", "ARRET ENCHAINEMENT") in trans

    # elseif ($state == 'H2' || $state == 'H3') captures both vars
    assert ("H2", "CONFIRMATION DEMANDE INTERVENTION") in trans
    assert ("H3", "CONFIRMATION DEMANDE INTERVENTION") in trans

    # elseif ($state == 'H4')
    assert ("H4", "TRAITEMENT H4 SPECIFIQUE") in trans


# ---------------------------------------------------------------------------
# Test F-2: delegate call when no label present
# ---------------------------------------------------------------------------

def test_pattern_f_delegate_call():
    """H1 block has no returnLongLabel → requires(H1, this.abandon)."""
    ir = _make_ir(_PHP_FIXTURE_F)
    rels = _pattern_f_rels(ir)

    reqs = {(r.from_entity.value, r.to_entity.value) for r in rels if r.kind == "requires"}
    assert ("H1", "this.abandon") in reqs, f"Expected requires(H1, this.abandon); got {reqs}"


# ---------------------------------------------------------------------------
# Test F-3: KB not required for situation codes
# ---------------------------------------------------------------------------

def test_pattern_f_no_kb_for_situation_codes():
    """Situation codes (H0–H4, I1…) are extracted without any KB entry."""
    ir = _make_ir(_PHP_FIXTURE_F)
    rels = _pattern_f_rels(ir, kb=lambda t: False)
    assert len(rels) > 0, "Pattern F must fire on [A-Z]\\d codes without KB"


# ---------------------------------------------------------------------------
# Test F-4: pattern field is set correctly
# ---------------------------------------------------------------------------

def test_pattern_f_pattern_field():
    """Every Pattern F relation carries pattern='pattern_f'."""
    ir = _make_ir(_PHP_FIXTURE_F)
    for r in _pattern_f_rels(ir):
        assert r.pattern == "pattern_f", f"Bad pattern: {r.pattern!r}"


# ---------------------------------------------------------------------------
# Test F-5: conditions are populated
# ---------------------------------------------------------------------------

def test_pattern_f_conditions_present():
    """Each Pattern F relation records the triggering condition.

    Branches if/elseif → condition '==' ; branche else finale → 'sinon'
    (heuristique du else implicite, cf. _extract_pattern_f_else).
    """
    ir = _make_ir(_PHP_FIXTURE_F)
    for r in _pattern_f_rels(ir):
        assert r.conditions, f"No conditions on {r.from_entity.value} → {r.to_entity.value}"
        assert any("==" in c or c.startswith("sinon") for c in r.conditions), (
            f"Condition should contain '==' or 'sinon': {r.conditions}"
        )


# ---------------------------------------------------------------------------
# Test F-6: entity types
# ---------------------------------------------------------------------------

def test_pattern_f_entity_types():
    """transitions_to: from=situation,to=event. requires: from=situation,to=module.

    Exception : la branche else sans code situation inférable produit un
    from_entity 'sinon' de type event (heuristique else implicite).
    """
    ir = _make_ir(_PHP_FIXTURE_F)
    for r in _pattern_f_rels(ir):
        if r.from_entity.value == "sinon":
            assert r.from_entity.type == "event", (
                f"else implicite : from_entity.type should be 'event', "
                f"got {r.from_entity.type!r}"
            )
        else:
            assert r.from_entity.type == "situation", (
                f"from_entity.type should be 'situation', got {r.from_entity.type!r} "
                f"for {r.from_entity.value} → {r.to_entity.value}"
            )
        if r.kind == "transitions_to":
            assert r.to_entity.type == "event", (
                f"to_entity.type should be 'event', got {r.to_entity.type!r}"
            )
        elif r.kind == "requires":
            assert r.to_entity.type == "module"


# ---------------------------------------------------------------------------
# Test F-7: elseif with || captures both sides
# ---------------------------------------------------------------------------

def test_pattern_f_or_condition():
    """elseif ($x == 'H2' || $x == 'H3') emits relations for both H2 and H3."""
    ir = _make_ir(_PHP_FIXTURE_F)
    rels = _pattern_f_rels(ir)

    froms = {r.from_entity.value for r in rels if r.kind == "transitions_to"}
    assert "H2" in froms and "H3" in froms, f"Expected H2 and H3 in froms; got {froms}"


# ===========================================================================
# Pattern G — variable assigned from service call, then tested
# ===========================================================================

_PHP_FIXTURE_G = """<?php
class TestService {
    public function process() {
        $informationEdr = $this->app->get('Edr')->setInformationBloc();
        if (!isset($informationEdr)) {
            return ['returnLongLabel' => 'Echec EDR'];
        }

        $checkAdelia = $this->historiqueService->checkDerangementAdelia();
        if (is_array($checkAdelia) && $checkAdelia['code'] == 500) {
            return ['returnLongLabel' => 'Echec Adelia'];
        }

        $situationImpact = $this->analyseImpact();
        if ($situationImpact == 'I1') {
            return ['returnLongLabel' => 'CONFIRMATION I1'];
        }

        $situationHistorique = $this->analyseHsitorique();
        if ($situationHistorique == 'H1') {
            return $this->abandon();
        }

        $result = $this->someService->someMethod();
        if ($result == 'I2') {
            return [];
        }
    }
}"""


def _pattern_g_rels(kb=None):
    if kb is None:
        kb = lambda t: False
    ir = _make_ir(_PHP_FIXTURE_G)
    extractor = RelationExtractor(kb)
    return [r for r in extractor.extract(ir) if r.pattern == "pattern_g"]


# ---------------------------------------------------------------------------
# Test G-1: requires emitted for each assign→test pair
# ---------------------------------------------------------------------------

def test_pattern_g_requires_emitted():
    """requires(var, call) emitted for each variable assigned from a call and later tested."""
    rels = _pattern_g_rels()
    req = {(r.from_entity.value, r.to_entity.value)
           for r in rels if r.kind == "requires"}

    assert ("informationEdr", "Edr.setInformationBloc") in req, f"Missing informationEdr req; got {req}"
    assert ("checkAdelia", "historiqueService.checkDerangementAdelia") in req
    assert ("situationImpact", "this.analyseImpact") in req
    assert ("situationHistorique", "this.analyseHsitorique") in req


# ---------------------------------------------------------------------------
# Test G-2: validity tests → produces with synthetic value
# ---------------------------------------------------------------------------

def test_pattern_g_produces_validity():
    """`!isset($var)` → produces(call, absent); `is_array($var)` → produces(call, array)."""
    rels = _pattern_g_rels()
    prod = {(r.from_entity.value, r.to_entity.value)
            for r in rels if r.kind == "produces"}

    assert ("Edr.setInformationBloc", "absent") in prod, \
        f"!isset should produce 'absent'; got {prod}"
    assert ("historiqueService.checkDerangementAdelia", "array") in prod, \
        f"is_array should produce 'array'; got {prod}"


# ---------------------------------------------------------------------------
# Test G-3: equality tests on situation codes → produces
# ---------------------------------------------------------------------------

def test_pattern_g_produces_situation_codes():
    """`$var == 'I1'` and `$var == 'H1'` emit produces(call, situation_code)."""
    rels = _pattern_g_rels()
    prod = {(r.from_entity.value, r.to_entity.value)
            for r in rels if r.kind == "produces"}

    assert ("this.analyseImpact", "I1") in prod, f"Missing analyseImpact→I1; got {prod}"
    assert ("this.analyseHsitorique", "H1") in prod, f"Missing analyseHsitorique→H1; got {prod}"


# ---------------------------------------------------------------------------
# Test G-4: call normalization — three variants
# ---------------------------------------------------------------------------

def test_pattern_g_call_normalization():
    """app->get('Svc')->method( → 'Svc.method' | svc->method( → 'svc.method' | method( → 'this.method'."""
    rels = _pattern_g_rels()
    calls = {r.to_entity.value for r in rels if r.kind == "requires"}

    assert "Edr.setInformationBloc" in calls, \
        f"app->get('Edr')->setInformationBloc → 'Edr.setInformationBloc'; got {calls}"
    assert "historiqueService.checkDerangementAdelia" in calls, \
        f"$this->historiqueService->method → 'historiqueService.method'; got {calls}"
    assert "this.analyseImpact" in calls, \
        f"$this->method → 'this.method'; got {calls}"


# ---------------------------------------------------------------------------
# Test G-5: trivial var names are filtered out
# ---------------------------------------------------------------------------

def test_pattern_g_trivial_vars_filtered():
    """`$result = $this->service->method()` — $result in TRIVIAL_VARS → no relation."""
    rels = _pattern_g_rels()
    req_vars = {r.from_entity.value for r in rels if r.kind == "requires"}

    assert "result" not in req_vars, \
        f"Trivial var 'result' should be filtered; got requires vars: {req_vars}"


# ---------------------------------------------------------------------------
# Test G-6: pattern field and kinds are correct
# ---------------------------------------------------------------------------

def test_pattern_g_pattern_field_and_kinds():
    """All Pattern G rels carry pattern='pattern_g' and kind in (requires, produces)."""
    rels = _pattern_g_rels()
    assert rels, "Expected at least some Pattern G relations"
    for r in rels:
        assert r.pattern == "pattern_g", f"Bad pattern: {r.pattern!r}"
        assert r.kind in ("requires", "produces"), f"Unexpected kind: {r.kind!r}"


# ---------------------------------------------------------------------------
# Test G-7: no regression on Pattern F from same entry_point
# ---------------------------------------------------------------------------

def test_pattern_g_no_regression_f():
    """Pattern F still fires on fixture G (I1 → 'CONFIRMATION I1')."""
    ir = _make_ir(_PHP_FIXTURE_G)
    extractor = RelationExtractor(lambda t: False)
    all_rels = extractor.extract(ir)
    f_rels = [r for r in all_rels if r.pattern == "pattern_f"]
    trans = {(r.from_entity.value, r.to_entity.value)
             for r in f_rels if r.kind == "transitions_to"}
    assert ("I1", "CONFIRMATION I1") in trans, \
        f"Pattern F should still fire; transitions_to = {trans}"
