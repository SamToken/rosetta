"""
Tests for RelationExtractor — Pattern C (switch/case transitions and dispatch).
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
