"""
Détection de code mort (#4) — Phase 1 : index inverse du call graph.

Un entry point est candidat « code mort » si son nom n'apparaît comme cible
d'appel nulle part dans l'arbre indexé. Heuristique conservatrice (résolution
par nom). Cache versionné : un schéma antérieur force la réindexation.

Arbre PHP 100 % fictif (règle CLAUDE.md #1).
"""

import json
from pathlib import Path

import pytest

from analyzers.call_graph import CallGraphIndex, _CACHE_SCHEMA_VERSION

ALPHA = """<?php
class AlphaService
{
    public function used($x)
    {
        return $x + 1;
    }

    public function orphan($y)
    {
        return $y - 1;
    }
}
"""

BETA = """<?php
class BetaService
{
    public function run()
    {
        return $this->alpha->used(42);
    }
}
"""


@pytest.fixture()
def tree(tmp_path):
    (tmp_path / "alpha_service.php").write_text(ALPHA, encoding="utf-8")
    (tmp_path / "beta_service.php").write_text(BETA, encoding="utf-8")
    return tmp_path


def _names(sigs):
    return {s.method_name for s in sigs}


def test_is_referenced(tree):
    idx = CallGraphIndex.build(tree)
    assert idx.is_referenced("used") is True
    assert idx.is_referenced("orphan") is False
    assert idx.is_referenced("run") is False


def test_is_referenced_insensible_casse(tree):
    idx = CallGraphIndex.build(tree)
    assert idx.is_referenced("USED") is True


def test_dead_code_candidates(tree):
    idx = CallGraphIndex.build(tree)
    cands = _names(idx.dead_code_candidates())
    assert "orphan" in cands
    assert "run" in cands       # run() défini mais jamais appelé
    assert "used" not in cands  # used() appelé depuis BetaService


def test_dead_code_candidates_exclut_entrypoints(tree):
    idx = CallGraphIndex.build(tree)
    # Simule l'exclusion des points d'entrée framework (ici : run comme "action")
    cands = _names(idx.dead_code_candidates(is_entrypoint=lambda s: s.method_name == "run"))
    assert cands == {"orphan"}


def test_cache_roundtrip_preserve_called_names(tree, tmp_path):
    cache = tmp_path / ".callgraph.json"
    CallGraphIndex.build(tree, cache_path=cache)
    assert cache.exists()
    data = json.loads(cache.read_text(encoding="utf-8"))
    assert data["schema_version"] == _CACHE_SCHEMA_VERSION
    assert "used" in data["called_names"]

    reloaded = CallGraphIndex._load(cache)
    assert reloaded.is_referenced("used") is True
    assert reloaded.is_referenced("orphan") is False


def test_cache_schema_antérieur_force_reindex(tree, tmp_path):
    # Cache "v1" : pas de schema_version ni called_names → doit être ignoré.
    old_cache = tmp_path / ".callgraph.json"
    old_cache.write_text(json.dumps({"by_method": {}, "by_class_method": {}}), encoding="utf-8")

    with pytest.raises(ValueError):
        CallGraphIndex._load(old_cache)

    # build() rattrape : réindexe depuis l'arbre et repeuple l'index inverse.
    idx = CallGraphIndex.build(tree, cache_path=old_cache)
    assert idx.is_referenced("used") is True
    data = json.loads(old_cache.read_text(encoding="utf-8"))
    assert data["schema_version"] == _CACHE_SCHEMA_VERSION
