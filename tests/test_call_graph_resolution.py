"""
Résolution de type dans le call graph (#1 étape B).

property_types transforme $this->prop->method() en une classe certaine, ce qui
départage les collisions de noms de méthodes. Fixtures 100 % fictives.
"""

from pathlib import Path

import pytest

from analyzers.call_graph import CallGraphIndex, _extract_called_methods

HELPER_IMPL = """<?php
class HelperImpl
{
    public function doStuff() { return 'right'; }
}
"""

WRONG_IMPL = """<?php
class WrongImpl
{
    public function doStuff() { return 'wrong'; }
}
"""

CALLER = """<?php
class Caller
{
    public function __construct(HelperImpl $h)
    {
        $this->h = $h;
    }
    public function run()
    {
        return $this->h->doStuff();
    }
}
"""


def test_hint_type_certain_si_connu():
    calls = _extract_called_methods("$this->h->doStuff();", {"h": "HelperImpl"})
    assert ("doStuff", "HelperImpl") in calls


def test_fallback_pascalcase_si_inconnu():
    calls = _extract_called_methods("$this->h->doStuff();")
    assert ("doStuff", "H") in calls


def test_bundle_departage_collision(tmp_path):
    (tmp_path / "helper_impl.php").write_text(HELPER_IMPL, encoding="utf-8")
    (tmp_path / "wrong_impl.php").write_text(WRONG_IMPL, encoding="utf-8")
    idx = CallGraphIndex.build(tmp_path)

    # Les deux classes ont doStuff() → collision. La résolution de type doit
    # choisir HelperImpl (le type injecté), pas un candidat arbitraire.
    bundle = idx.bundle_for_source(CALLER)
    assert "HelperImpl" in bundle
    assert "WrongImpl" not in bundle
