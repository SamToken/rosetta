"""
Arêtes inverses « appelé par » (#3 incrément 2).

Le call graph construit un index inverse résolu par type : qui appelle
Class::method. Cache versionné (v3). Fixtures 100 % fictives.
"""

import json
from pathlib import Path

from analyzers.call_graph import CallGraphIndex, _CACHE_SCHEMA_VERSION
from generators.business_doc_generator import BusinessDocGenerator
from ir.schema import create_ir, EntryPoint

FOO = """<?php
class FooService
{
    public function bar() { return 1; }
}
"""

CALLER = """<?php
class CallerService
{
    public function __construct(FooService $foo)
    {
        $this->foo = $foo;
    }
    public function run()
    {
        return $this->foo->bar();
    }
}
"""


def _tree(tmp_path):
    (tmp_path / "foo_service.php").write_text(FOO, encoding="utf-8")
    (tmp_path / "caller_service.php").write_text(CALLER, encoding="utf-8")
    return tmp_path


def test_callers_of(tmp_path):
    idx = CallGraphIndex.build(_tree(tmp_path))
    assert idx.callers_of("FooService", "bar") == ["CallerService::run"]


def test_callers_of_vide_si_personne(tmp_path):
    idx = CallGraphIndex.build(_tree(tmp_path))
    assert idx.callers_of("CallerService", "run") == []


def test_cache_v3_preserve_aretes(tmp_path):
    cache = tmp_path / ".callgraph.json"
    CallGraphIndex.build(_tree(tmp_path), cache_path=cache)
    data = json.loads(cache.read_text(encoding="utf-8"))
    assert data["schema_version"] == _CACHE_SCHEMA_VERSION
    assert data["callers_by_target"]["FooService::bar"] == ["CallerService::run"]

    reloaded = CallGraphIndex._load(cache)
    assert reloaded.callers_of("FooService", "bar") == ["CallerService::run"]


def test_called_by_rendu_dans_doc():
    ir = create_ir(source_file="/fake/FooService.php", controller_name="Foo")
    ir.entry_points = [
        EntryPoint(name="bar", original_name="bar",
                   risk_score=5.0, called_by=["CallerService::run"]),
    ]
    doc = BusinessDocGenerator().generate(ir)
    assert "Appelé par (cross-fichier)" in doc
    assert "CallerService::run" in doc
