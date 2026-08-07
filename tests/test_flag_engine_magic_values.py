"""
Couverture des regex magic_value élargies (P1 - DÉFAUT B).

Avant : MAGIC_VALUE_PATTERNS n'utilisait que [a-z_]+ (minuscules) et \\d{2,}
→ le vocabulaire MAJUSCULE/PascalCase, les entiers à un chiffre ou quotés,
les in_array() et les case mixtes étaient invisibles. Le filtre de stop-words
écarte le bruit (0/1, booléens, chaîne vide, mono-caractère).

Tokens de test 100 % fictifs (règle CLAUDE.md #1) — les regex ne testent que
la forme des caractères, pas la sémantique métier.
"""

from pathlib import Path

import pytest

from analyzers.flag_engine import FlagEngine, _is_magic_noise
from extractors.php_extractor import extract_php

FIXTURE = Path(__file__).parent / "fixtures" / "php" / "MagicValueService.php"


@pytest.fixture(scope="module")
def magic_values():
    ir = extract_php(FIXTURE)
    flags = FlagEngine().analyze(ir)
    # union de tous les fragments magic_value pour recherche par sous-chaîne
    return "\n".join(
        f.fragment for f in flags
        if (f.type.value if hasattr(f.type, "value") else str(f.type)) == "magic_value"
    )


def test_chaine_pascalcase_captee(magic_values):
    assert "Wibbled" in magic_values


def test_chaine_majuscule_captee(magic_values):
    assert "ACMEREF" in magic_values


def test_entier_quote_un_chiffre_capte(magic_values):
    assert "== '3'" in magic_values


def test_entier_nonquote_un_chiffre_capte(magic_values):
    assert "== 7" in magic_values


def test_in_array_literal_capte(magic_values):
    assert "FLAG_ALPHA" in magic_values


def test_case_mixte_capte(magic_values):
    assert "Frobnik" in magic_values
    assert "STEP_TWO" in magic_values


def test_bruit_zero_un_filtre(magic_values):
    # '== 1' ne doit PAS produire de magic_value (0/1 sont des stop-words)
    assert "== 1" not in magic_values


def test_chaine_vide_filtree(magic_values):
    assert "''" not in magic_values


# --- filtre unitaire ---------------------------------------------------------

@pytest.mark.parametrize("noise", ["", "0", "1", "OK", "KO", "TRUE", "NULL", ";", "]"])
def test_is_magic_noise_ecarte(noise):
    assert _is_magic_noise(noise) is True


@pytest.mark.parametrize("signal", ["ACMEREF", "Wibbled", "TP2", "3", "7", "FLAG_ALPHA"])
def test_is_magic_noise_laisse_passer(signal):
    assert _is_magic_noise(signal) is False
