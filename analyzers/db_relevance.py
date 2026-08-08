"""Déclencheur d'injection de l'inventaire schéma Oracle dans un prompt LLM.

Isolé À DESSEIN. Quand `sql_analyzer` (#7) exposera les operations DB_READ /
DB_WRITE par méthode, remplacer le **corps** de `method_touches_db` par ce
signal propre — sans toucher à l'enricher : le site d'appel reste identique.

Pourquoi une heuristique durcie et pas `_SQL_DETECT` nu : mesuré sur 12 507
flags réels, `_SQL_DETECT(flag.fragment)` déclenche 0,1 % (mort — le SQL n'est
pas dans les fragments). Porté au `method_body`, `_SQL_DETECT` nu matcherait du
bruit : `FROM` / `JOIN` sont des mots anglais courants (commentaires, messages,
noms de variables). D'où trois signaux ancrés :

  1. **Verbe SQL ancré** — SELECT / INSERT / UPDATE / DELETE uniquement.
     `FROM` et `JOIN` seuls ne déclenchent plus.
  2. **Signal Zend DB** — ``->query(`` / ``->fetchAll(`` / ``->fetchRow(`` /
     ``->select(`` / ``->insert(`` / ``->update(`` / ``Zend_Db_``. En legacy
     Zend, une méthode qui tape la base passe presque toujours par là : c'est le
     marqueur le plus discriminant.
  3. **Table de l'inventaire présente** — un des noms de tables connus apparaît
     dans le corps (filtre gratuit puisque le catalogue est déjà résident).
     Comparaison **sensible à la casse** (les tables sont en MAJUSCULES) pour ne
     pas matcher les mots anglais minuscules homographes.

Déclenche si (1) OU (2) OU (3).
"""

from __future__ import annotations

import re
from typing import Iterable, Optional

# 1. Verbes DML ancrés — FROM/JOIN nus volontairement exclus.
_SQL_VERB = re.compile(r"\b(?:SELECT|INSERT|UPDATE|DELETE)\b", re.IGNORECASE)

# 2. Accès base à la Zend (méthodes DB adapter/table + préfixe de classe).
_ZEND_DB = re.compile(
    r"->\s*(?:query|fetchAll|fetchRow|fetchOne|fetchCol|fetchPairs|"
    r"select|insert|update|delete)\s*\("
    r"|Zend_Db_",
    re.IGNORECASE,
)


def build_table_matcher(known_tables: Iterable[str]) -> Optional[re.Pattern]:
    """Pré-compile un matcher de noms de tables (sensible à la casse, ancré mots).

    Renvoie ``None`` si l'inventaire est vide → le signal 3 est simplement neutre.
    """
    names = sorted({t.strip() for t in known_tables if t and t.strip()}, key=len, reverse=True)
    if not names:
        return None
    return re.compile(r"\b(?:" + "|".join(re.escape(n) for n in names) + r")\b")


def _signals_present(text: str, table_matcher: Optional[re.Pattern]) -> bool:
    if _SQL_VERB.search(text):
        return True
    if _ZEND_DB.search(text):
        return True
    if table_matcher is not None and table_matcher.search(text):
        return True
    return False


def method_touches_db(
    method_body: Optional[str],
    table_matcher: Optional[re.Pattern] = None,
    context_lines: Optional[str] = None,
) -> bool:
    """Vrai si la méthode a un footprint base (voir module docstring).

    Fenêtre de test : ``method_body`` si disponible, sinon **fallback** sur
    ``context_lines``. Rattrape les ~31 % de flags de bloc sans méthode connue
    (ex. flag dans un DAO) qui, sinon, ne déclencheraient jamais — ce n'est pas
    le comportement voulu par (a), qui exclut les méthodes non-DB, pas les flags
    dont on ignore la méthode. Le durcissement est identique ; seule la fenêtre
    change.

    ``table_matcher`` : produit par ``build_table_matcher`` (signal 3). Optionnel.

    NOTE substitution future : remplacer ce corps par la vérification des
    operations DB_READ/DB_WRITE de la méthode (sql_analyzer #7) — garder cette
    signature stable pour que l'enricher n'ait pas à changer.
    """
    text = method_body or context_lines
    if not text:
        return False
    return _signals_present(text, table_matcher)
