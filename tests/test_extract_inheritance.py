"""
Extraction de la structure d'héritage (#1/#2, phase héritage/traits).

parent_class / interfaces / traits doivent être capturés dans ir.metadata pour
signaler où vit réellement le comportement (classe parente, traits partagés).
Fixtures 100 % fictives.
"""

from extractors.php_extractor import extract_php

WITH_INHERITANCE = """<?php
namespace App\\Service;

class FooService extends AbstractBaseService implements FooInterface, BarInterface
{
    use LoggableTrait;
    use TimestampableTrait, SoftDeleteTrait;

    public function doThing()
    {
        return 1;
    }
}
"""

PLAIN = """<?php
class PlainService
{
    public function doThing()
    {
        return 1;
    }
}
"""


def _extract(tmp_path, src, name="X.php"):
    f = tmp_path / name
    f.write_text(src, encoding="utf-8")
    return extract_php(f)


def test_parent_class(tmp_path):
    ir = _extract(tmp_path, WITH_INHERITANCE)
    assert ir.metadata.parent_class == "AbstractBaseService"


def test_interfaces(tmp_path):
    ir = _extract(tmp_path, WITH_INHERITANCE)
    assert ir.metadata.interfaces == ["FooInterface", "BarInterface"]


def test_traits(tmp_path):
    ir = _extract(tmp_path, WITH_INHERITANCE)
    assert ir.metadata.traits == ["LoggableTrait", "TimestampableTrait", "SoftDeleteTrait"]


def test_classe_sans_heritage(tmp_path):
    ir = _extract(tmp_path, PLAIN)
    assert ir.metadata.parent_class is None
    assert ir.metadata.interfaces == []
    assert ir.metadata.traits == []


def test_note_heritage_dans_doc(tmp_path):
    from generators.business_doc_generator import BusinessDocGenerator
    ir = _extract(tmp_path, WITH_INHERITANCE)
    doc = BusinessDocGenerator().generate(ir)
    assert "Héritage" in doc
    assert "AbstractBaseService" in doc
    assert "LoggableTrait" in doc
