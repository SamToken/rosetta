"""
PHTML Analyzer — analyse des vues Zend (#6)
===========================================
Les vues .phtml sont hors du périmètre de l'extracteur (pas des classes) mais
portent de la logique, une surface XSS (sorties non échappées) et un coût de
migration Twig réel.

Analyse déterministe, zéro LLM. Produit, par vue :
- sorties non échappées (candidats XSS) — Twig échappe par défaut
- constructions logiques (if/foreach/…) à porter
- partials/render et view helpers à réécrire
- estimation d'effort de migration Twig
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

# Sorties : short-echo <?= … ?> et echo/print … ;
_RE_SHORT_ECHO = re.compile(r"<\?=(.*?)\?>", re.DOTALL)
_RE_ECHO = re.compile(r"\b(?:echo|print)\b(.*?);", re.DOTALL)

# Fonctions d'échappement qui neutralisent le risque XSS
_ESCAPE_FUNCS = re.compile(
    r"escape\s*\(|escapeHtml\s*\(|htmlspecialchars\s*\(|htmlentities\s*\(|strip_tags\s*\(",
    re.IGNORECASE,
)
_HAS_VAR = re.compile(r"\$\w")

_RE_LOGIC = re.compile(r"\b(?:if|elseif|foreach|for|while|switch)\s*\(")
_RE_TERNARY = re.compile(r"\?[^>]*?:")
_RE_PARTIAL = re.compile(r"->\s*(partial|partialLoop|render)\s*\(")
_RE_HELPER = re.compile(r"\$this\s*->\s*(\w+)\s*\(")


@dataclass
class PhtmlReport:
    """Analyse d'une vue .phtml."""
    path: str
    total_outputs: int = 0
    unescaped_outputs: int = 0
    escaped_outputs: int = 0
    logic_constructs: int = 0
    partials: int = 0
    helpers: list[str] = field(default_factory=list)
    sample_unescaped: list[str] = field(default_factory=list)

    @property
    def effort(self) -> str:
        score = self.unescaped_outputs + self.logic_constructs * 2 + self.partials * 2
        if score < 10:
            return "trivial"
        if score < 40:
            return "modéré"
        return "élevé"


def _is_output_unescaped(expr: str) -> bool:
    """True si l'expression sort une VARIABLE BRUTE (candidat XSS).

    Conservateur : une sortie n'est risquée que si elle contient une variable,
    n'est pas échappée, et n'est pas un appel de fonction/helper (`(`) — les
    helpers de vue (`$this->foo(...)`) gèrent en général leur propre rendu et ne
    sont pas la sortie brute `<?= $obj->prop ?>` typique du XSS Zend."""
    if not _HAS_VAR.search(expr):
        return False  # littéral pur
    if _ESCAPE_FUNCS.search(expr):
        return False  # échappement explicite
    if "(" in expr:
        return False  # appel de fonction/helper → hors du motif de sortie brute
    return True


def analyze_phtml(source: str, path: str = "") -> PhtmlReport:
    rep = PhtmlReport(path=path)

    outputs: list[str] = [m.group(1) for m in _RE_SHORT_ECHO.finditer(source)]
    outputs += [m.group(1) for m in _RE_ECHO.finditer(source)]
    rep.total_outputs = len(outputs)
    for expr in outputs:
        if _is_output_unescaped(expr):
            rep.unescaped_outputs += 1
            if len(rep.sample_unescaped) < 5:
                rep.sample_unescaped.append(" ".join(expr.split())[:100])
        else:
            rep.escaped_outputs += 1

    rep.logic_constructs = len(_RE_LOGIC.findall(source)) + len(_RE_TERNARY.findall(source))
    rep.partials = len(_RE_PARTIAL.findall(source))

    helpers = {
        m.group(1) for m in _RE_HELPER.finditer(source)
        if m.group(1) not in ("partial", "partialLoop", "render", "escape")
    }
    rep.helpers = sorted(helpers)
    return rep


def analyze_phtml_file(path: Path) -> PhtmlReport:
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        source = ""
    return analyze_phtml(source, str(path))
