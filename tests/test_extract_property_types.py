"""
Résolution de type des propriétés (#1, étape A).

property_types mappe propriété → classe collaboratrice, déduite de l'injection
constructeur, des `new X()` et des docblocks @var. Base d'un vrai graphe d'appels
(remplace l'heuristique PascalCase). Fixtures 100 % fictives.
"""

from extractors.php_extractor import extract_php

SRC = """<?php
namespace App\\Service;

class FooService
{
    /** @var CacheService */
    private $cache;
    private $untyped;

    public function __construct(BarService $bar, \\Psr\\Log\\LoggerInterface $logger)
    {
        $this->bar = $bar;
        $this->logger = $logger;
        $this->local = new BazHelper();
    }
}
"""


def _types(tmp_path):
    f = tmp_path / "FooService.php"
    f.write_text(SRC, encoding="utf-8")
    return extract_php(f).metadata.property_types


def test_injection_constructeur(tmp_path):
    t = _types(tmp_path)
    assert t["bar"] == "BarService"


def test_type_qualifie_reduit_au_nom_court(tmp_path):
    t = _types(tmp_path)
    assert t["logger"] == "LoggerInterface"  # \Psr\Log\LoggerInterface → LoggerInterface


def test_new_local(tmp_path):
    t = _types(tmp_path)
    assert t["local"] == "BazHelper"


def test_docblock_var(tmp_path):
    t = _types(tmp_path)
    assert t["cache"] == "CacheService"


def test_propriete_non_typee_absente(tmp_path):
    t = _types(tmp_path)
    assert "untyped" not in t
