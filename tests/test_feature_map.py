"""
Carte de feature cross-fichier (#3 incrément 3).

walk_downstream assemble les arêtes avant résolues en chaîne
controller→service→repo, avec garde anti-cycle. Le générateur rend l'arbre
indenté. Fixtures 100 % fictives.
"""

import json
from pathlib import Path

from analyzers.call_graph import CallGraphIndex, _CACHE_SCHEMA_VERSION
from generators.feature_map_generator import FeatureMapGenerator
from ir.schema import create_ir, EntryPoint

CTRL = """<?php
class CtrlService
{
    public function __construct(MidService $mid) { $this->mid = $mid; }
    public function run() { return $this->mid->step(); }
}
"""

MID = """<?php
class MidService
{
    public function __construct(RepoService $repo) { $this->repo = $repo; }
    public function step() { return $this->repo->find(); }
}
"""

REPO = """<?php
class RepoService
{
    public function find() { return 1; }
}
"""

# Cycle : A::a -> B::b -> A::a
CYCLE_A = """<?php
class AService
{
    public function __construct(BService $b) { $this->b = $b; }
    public function a() { return $this->b->b(); }
}
"""
CYCLE_B = """<?php
class BService
{
    public function __construct(AService $a) { $this->a = $a; }
    public function b() { return $this->a->a(); }
}
"""


def _chain_index(tmp_path):
    (tmp_path / "ctrl_service.php").write_text(CTRL, encoding="utf-8")
    (tmp_path / "mid_service.php").write_text(MID, encoding="utf-8")
    (tmp_path / "repo_service.php").write_text(REPO, encoding="utf-8")
    return CallGraphIndex.build(tmp_path)


def test_walk_downstream_chaine(tmp_path):
    idx = _chain_index(tmp_path)
    chain = idx.walk_downstream("CtrlService::run")
    assert chain == [(1, "MidService::step"), (2, "RepoService::find")]


def test_callees_of(tmp_path):
    idx = _chain_index(tmp_path)
    assert idx.callees_of("CtrlService", "run") == ["MidService::step"]


def test_walk_coupe_les_cycles(tmp_path):
    (tmp_path / "a_service.php").write_text(CYCLE_A, encoding="utf-8")
    (tmp_path / "b_service.php").write_text(CYCLE_B, encoding="utf-8")
    idx = CallGraphIndex.build(tmp_path)
    chain = idx.walk_downstream("AService::a")
    # A::a (root, visité) → B::b → A::a (déjà visité, stop). Pas de boucle infinie.
    assert chain == [(1, "BService::b"), (2, "AService::a")]


def test_cache_v4_preserve_forward(tmp_path):
    cache = tmp_path / ".callgraph.json"
    (tmp_path / "ctrl_service.php").write_text(CTRL, encoding="utf-8")
    (tmp_path / "mid_service.php").write_text(MID, encoding="utf-8")
    (tmp_path / "repo_service.php").write_text(REPO, encoding="utf-8")
    CallGraphIndex.build(tmp_path, cache_path=cache)
    data = json.loads(cache.read_text(encoding="utf-8"))
    assert data["schema_version"] == _CACHE_SCHEMA_VERSION
    assert data["callees_by_source"]["CtrlService::run"] == ["MidService::step"]
    reloaded = CallGraphIndex._load(cache)
    assert reloaded.walk_downstream("CtrlService::run") == [
        (1, "MidService::step"), (2, "RepoService::find")
    ]


def test_generateur_rend_arbre(tmp_path):
    idx = _chain_index(tmp_path)
    ir = create_ir(source_file="/x/CtrlService.php", controller_name="Ctrl")
    ir.entry_points = [EntryPoint(name="run", original_name="run")]
    out = FeatureMapGenerator().generate([ir], idx)
    assert "## CtrlService" in out
    assert "### run()" in out
    assert "`MidService::step()`" in out
    assert "  - `RepoService::find()`" in out  # indenté à la profondeur 2
