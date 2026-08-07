"""
Appels cross-fichier résolus (#3, incrément 1).

resolve_strict ne renvoie une arête que sur match de classe exact (pas de
fallback par nom) → arêtes de feature fiables. Le doc métier affiche les
collaborateurs appelés. Fixtures 100 % fictives.
"""

from pathlib import Path

from analyzers.call_graph import CallGraphIndex, _extract_called_methods
from generators.business_doc_generator import BusinessDocGenerator
from ir.schema import create_ir, EntryPoint

FOO = """<?php
class FooService
{
    public function bar() { return 1; }
}
"""


def _index(tmp_path):
    (tmp_path / "foo_service.php").write_text(FOO, encoding="utf-8")
    return CallGraphIndex.build(tmp_path)


def test_resolve_strict_match_exact(tmp_path):
    idx = _index(tmp_path)
    sig = idx.resolve_strict("bar", "FooService")
    assert sig is not None and sig.class_name == "FooService"


def test_resolve_strict_pas_de_fallback_par_nom(tmp_path):
    idx = _index(tmp_path)
    # 'bar' existe mais pas sur la classe 'Autre' → aucune arête (vs resolve() qui
    # renverrait un candidat arbitraire)
    assert idx.resolve_strict("bar", "Autre") is None
    assert idx.resolve_strict("bar", None) is None


def test_resolution_arete_cross_fichier(tmp_path):
    idx = _index(tmp_path)
    calls = _extract_called_methods("$this->foo->bar();", {"foo": "FooService"})
    resolved = [idx.resolve_strict(m, h) for m, h in calls if h]
    resolved = [r for r in resolved if r]
    assert any(r.class_name == "FooService" and r.method_name == "bar" for r in resolved)


def test_callees_rendu_dans_doc():
    ir = create_ir(source_file="/fake/CallerService.php", controller_name="Caller")
    ir.entry_points = [
        EntryPoint(name="run", original_name="run",
                   risk_score=10.0, callees=["FooService::bar"]),
    ]
    doc = BusinessDocGenerator().generate(ir)
    assert "Appelle (cross-fichier)" in doc
    assert "FooService::bar" in doc
