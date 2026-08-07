"""
Analyse des vues .phtml (#6) — XSS + effort Twig + helpers.

Détecte les sorties non échappées (candidats XSS), la logique et les helpers à
migrer vers Twig. Exemples 100 % fictifs.
"""

from analyzers.phtml_analyzer import analyze_phtml, PhtmlReport
from generators.views_report_generator import ViewsReportGenerator

VIEW = """<div>
  <h1><?= $ticket->titre ?></h1>
  <span><?= $this->escape($ticket->auteur) ?></span>
  <em><?= htmlspecialchars($ticket->note) ?></em>
  <b><?= 'Statut fixe' ?></b>
  <?php if ($ticket->ouvert): ?>
    <ul>
    <?php foreach ($lignes as $ligne): ?>
      <li><?= $ligne->libelle ?></li>
    <?php endforeach; ?>
    </ul>
  <?php endif; ?>
  <?= $this->partial('bloc.phtml', $data) ?>
  <?= $this->formatDate($ticket->date) ?>
</div>
"""


def test_sorties_non_echappees():
    r = analyze_phtml(VIEW, "ticket.phtml")
    # $ticket->titre et $ligne->libelle → non échappés (variable, pas d'escape)
    assert r.unescaped_outputs == 2, r.sample_unescaped


def test_sorties_echappees_non_comptees():
    r = analyze_phtml(VIEW, "ticket.phtml")
    # escape(), htmlspecialchars(), littéral 'Statut fixe', helpers → non risqués
    assert r.escaped_outputs >= 3


def test_logique_comptee():
    r = analyze_phtml(VIEW, "ticket.phtml")
    assert r.logic_constructs >= 2  # if + foreach


def test_partials_et_helpers():
    r = analyze_phtml(VIEW, "ticket.phtml")
    assert r.partials == 1
    assert "formatDate" in r.helpers
    assert "escape" not in r.helpers  # escape exclu (échappement, pas helper métier)


def test_effort_property():
    r = PhtmlReport(path="x", unescaped_outputs=0, logic_constructs=0, partials=0)
    assert r.effort == "trivial"
    r2 = PhtmlReport(path="x", unescaped_outputs=30, logic_constructs=10, partials=5)
    assert r2.effort == "élevé"


def test_generateur_rapport():
    reports = [analyze_phtml(VIEW, "ticket.phtml")]
    out = ViewsReportGenerator().generate(reports)
    assert "Surface XSS" in out
    assert "non échappée" in out
    assert "formatDate" in out
    assert "ticket.phtml" in out


def test_generateur_vide():
    out = ViewsReportGenerator().generate([])
    assert "Aucune vue" in out
