"""
Recettes de migration Zend→Symfony (#2/9, tâche #11).

Vérifie le catalogue étendu (9→30), l'unicité des ids, le rendu par flag et
le handbook complet. Exemples 100 % génériques.
"""

import re

import pytest

from generators.migration_recipes import RecipeBook, _RECIPES
from ir.schema import Flag


def test_catalogue_30_recettes():
    assert len(_RECIPES) == 30


def test_ids_uniques():
    ids = [r.id for r in _RECIPES]
    assert len(ids) == len(set(ids)), "ids de recettes dupliqués"


def test_titres_uniques():
    titles = [r.title for r in _RECIPES]
    assert len(titles) == len(set(titles))


def test_patterns_compiles():
    for r in _RECIPES:
        assert isinstance(r.pattern, re.Pattern)


def test_effort_valide():
    for r in _RECIPES:
        assert r.effort in {"trivial", "modéré", "élevé"}, r.id


@pytest.mark.parametrize("token,expected_id", [
    ("new Zend_Form();", "zend_form"),
    ("Zend_Json::decode($x)", "zend_json"),
    ("new Zend_Http_Client($url)", "zend_http_client"),
    ("$logger = new Zend_Log();", "zend_log"),
    ("md5($password)", "md5_password"),
])
def test_render_par_flag(token, expected_id):
    book = RecipeBook()
    flag = Flag(id="f1", type="security_risk", location="m", fragment=token, question="?")
    recipe = book.find(flag)
    assert recipe is not None
    assert recipe.id == expected_id


def test_render_catalogue_complet():
    catalog = RecipeBook().render_catalog()
    assert "Catalogue des recettes de migration" in catalog
    assert "30 recette(s)" in catalog
    # chaque titre apparaît (index + bloc)
    for r in _RECIPES:
        assert r.title in catalog


def test_render_block_non_vide():
    book = RecipeBook()
    for r in book.all():
        flag = Flag(id="f", type=r.flag_type or "security_risk",
                    location="m", fragment="", question="?")
        block = book.render(flag) if r.pattern.search("") else None
        # au minimum le rendu direct du bloc n'est pas vide
        from generators.migration_recipes import _render_block
        assert _render_block(r).strip()
