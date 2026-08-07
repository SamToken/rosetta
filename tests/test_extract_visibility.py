"""
Périmètre d'extraction des entry points sur une classe *Service.

Avant le fix : seules les méthodes publiques (hors magic) devenaient des
entry points → les privées/protégées, où vit ~15 % de la logique métier ASO,
étaient invisibles. Le fix les inclut par défaut, avec un opt-out via
include_nonpublic_methods=False (ou ROSETTA_EXTRACT_NONPUBLIC=false).
"""

from pathlib import Path

from extractors.php_extractor import extract_php
from ir.schema import Visibility

FIXTURE = Path(__file__).parent / "fixtures" / "php" / "VisibilityService.php"

# Méthodes de la fixture par visibilité (hors magic __construct)
PUBLIC = {"getPublicOne", "getPublicTwo", "buildLabel"}
PRIVATE = {"helperCompute"}
PROTECTED = {"guardAccess"}


def _names(ir):
    return {ep.original_name for ep in ir.entry_points}


def test_inclut_privees_et_protegees_par_defaut():
    ir = extract_php(FIXTURE, include_nonpublic_methods=True)
    names = _names(ir)
    assert PUBLIC <= names, f"publiques manquantes : {PUBLIC - names}"
    assert PRIVATE <= names, "méthode privée non extraite"
    assert PROTECTED <= names, "méthode protégée non extraite"


def test_magic_toujours_exclue():
    ir = extract_php(FIXTURE, include_nonpublic_methods=True)
    assert "__construct" not in _names(ir)


def test_optout_ancien_comportement_publiques_seulement():
    ir = extract_php(FIXTURE, include_nonpublic_methods=False)
    names = _names(ir)
    assert names == PUBLIC, f"attendu {PUBLIC}, obtenu {names}"


def test_visibilite_correctement_taggee():
    ir = extract_php(FIXTURE, include_nonpublic_methods=True)
    by_name = {ep.original_name: ep.visibility for ep in ir.entry_points}
    assert by_name["helperCompute"] == Visibility.PRIVATE
    assert by_name["guardAccess"] == Visibility.PROTECTED
    assert by_name["getPublicOne"] == Visibility.PUBLIC
