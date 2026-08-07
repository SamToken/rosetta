"""
Code mort (#4) — Phase 2 : intégration aggregator + section rapport.

Un EntryPoint marqué dead_code_suspected doit remonter dans
AggregatedInsights.dead_code et produire la section « ## 6. Code mort suspecté »
du rapport global. Données 100 % fictives.
"""

from aggregators.business_aggregator import BusinessAggregator
from generators.global_audit_generator import GlobalAuditGenerator
from ir.schema import create_ir, EntryPoint


def _ir_with(entry_points):
    ir = create_ir(source_file="/fake/FooService.php", controller_name="FooService")
    ir.entry_points = entry_points
    return ir


def test_dead_code_remonte_dans_insights():
    ir = _ir_with([
        EntryPoint(name="used", original_name="used", dead_code_suspected=False),
        EntryPoint(name="orphan", original_name="orphan",
                   dead_code_suspected=True, start_line=42),
    ])
    insights = BusinessAggregator().aggregate([ir])
    methods = {d.method for d in insights.dead_code}
    assert methods == {"orphan"}
    assert insights.dead_code[0].source_line == 42


def test_section_rapport_rendue():
    ir = _ir_with([
        EntryPoint(name="orphan", original_name="orphan",
                   dead_code_suspected=True, start_line=42),
    ])
    insights = BusinessAggregator().aggregate([ir])
    report = GlobalAuditGenerator().generate(insights)
    assert "## 6. Code mort suspecté" in report
    assert "`orphan()`" in report
    # disclaimer faux positifs présent
    assert ".phtml" in report


def test_pas_de_section_si_aucun_mort():
    ir = _ir_with([
        EntryPoint(name="used", original_name="used", dead_code_suspected=False),
    ])
    insights = BusinessAggregator().aggregate([ir])
    assert insights.dead_code == []
    report = GlobalAuditGenerator().generate(insights)
    assert "## 6. Code mort" not in report
