"""
SQL Analyzer — extracteur structurel léger (#7)
===============================================
Transforme une chaîne SQL (captée en brut dans Operation.details) en faits
exploitables : tables lues/écrites, colonnes, jointures, drapeaux.

Contrainte projet : ZÉRO dépendance lourde (pas de sqlparse). Regex best-effort,
jamais présenté comme exhaustif. Sur du SQL dynamique concaténé, les clauses
FROM/JOIN du préfixe statique restent en général récupérables.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_KEYWORDS = frozenset({
    "SELECT", "FROM", "WHERE", "JOIN", "INNER", "LEFT", "RIGHT", "OUTER", "FULL",
    "ON", "AND", "OR", "GROUP", "ORDER", "BY", "HAVING", "AS", "IN", "NOT",
    "IS", "NULL", "LIKE", "BETWEEN", "EXISTS", "UNION", "ALL", "DISTINCT",
    "INSERT", "INTO", "UPDATE", "DELETE", "SET", "VALUES", "CONNECT",
})

_ID = r"[A-Za-z_][A-Za-z0-9_$.]*"

_RE_JOIN = re.compile(rf"\bJOIN\s+({_ID})", re.IGNORECASE)
_RE_JOIN_ON = re.compile(
    rf"\bJOIN\s+({_ID})(?:\s+{_ID})?\s+ON\s+(.+?)"
    r"(?=\bJOIN\b|\bWHERE\b|\bGROUP\b|\bORDER\b|\bHAVING\b|$)",
    re.IGNORECASE | re.DOTALL,
)
_RE_INSERT = re.compile(rf"\bINSERT\s+INTO\s+({_ID})", re.IGNORECASE)
_RE_UPDATE = re.compile(rf"\bUPDATE\s+({_ID})", re.IGNORECASE)
_RE_DELETE = re.compile(rf"\bDELETE\s+FROM\s+({_ID})", re.IGNORECASE)
_RE_FROM = re.compile(
    r"\bFROM\b(.*?)(?:\bWHERE\b|\bGROUP\b|\bORDER\b|\bHAVING\b|\bCONNECT\b|\bJOIN\b|$)",
    re.IGNORECASE | re.DOTALL,
)
_RE_SELECT = re.compile(r"\bSELECT\b(.*?)\bFROM\b", re.IGNORECASE | re.DOTALL)
_RE_WHERE = re.compile(
    r"\bWHERE\b(.*?)(?:\bGROUP\b|\bORDER\b|\bHAVING\b|\bCONNECT\b|$)",
    re.IGNORECASE | re.DOTALL,
)
_RE_WHERE_COL = re.compile(
    rf"({_ID})\s*(?:=|!=|<>|<=|>=|<|>|\bLIKE\b|\bIN\b|\bIS\b|\bBETWEEN\b)",
    re.IGNORECASE,
)


def _norm_table(tok: str) -> str:
    """Nom de table normalisé (majuscules, sans alias/schéma préfixe conservé)."""
    return tok.strip().strip(",").upper()


def _first_token(expr: str) -> str:
    """Premier identifiant d'une expression 'table alias' → 'table'."""
    parts = expr.strip().split()
    return parts[0] if parts else ""


@dataclass
class SqlFacts:
    tables_read: list[str] = field(default_factory=list)
    tables_written: list[str] = field(default_factory=list)
    columns: list[str] = field(default_factory=list)
    joins: list[str] = field(default_factory=list)     # "TABLE ON condition"
    where_columns: list[str] = field(default_factory=list)
    select_star: bool = False
    subquery: bool = False
    oracle_outer_join: bool = False  # présence de (+)

    @property
    def is_empty(self) -> bool:
        return not (self.tables_read or self.tables_written)


def _dedup(seq) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for x in seq:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out


def parse_sql(sql: str) -> SqlFacts:
    """Extrait les faits structurels d'une chaîne SQL. Best-effort, tolérant au
    SQL partiel/dynamique."""
    facts = SqlFacts()
    if not sql:
        return facts
    s = " ".join(sql.split())

    if not re.search(r"\b(SELECT|INSERT|UPDATE|DELETE)\b", s, re.IGNORECASE):
        return facts

    # Tables écrites
    for rx in (_RE_INSERT, _RE_UPDATE, _RE_DELETE):
        for m in rx.finditer(s):
            facts.tables_written.append(_norm_table(m.group(1)))

    # Tables lues : FROM (hors JOIN) + JOIN
    from_m = _RE_FROM.search(s)
    if from_m:
        for part in from_m.group(1).split(","):
            tok = _first_token(part)
            if tok:
                facts.tables_read.append(_norm_table(tok))
    for m in _RE_JOIN.finditer(s):
        facts.tables_read.append(_norm_table(m.group(1)))

    # Jointures explicites (table + condition)
    for m in _RE_JOIN_ON.finditer(s):
        cond = " ".join(m.group(2).split())[:120]
        facts.joins.append(f"{_norm_table(m.group(1))} ON {cond}")

    # Colonnes du SELECT
    sel_m = _RE_SELECT.search(s)
    if sel_m:
        sel = sel_m.group(1).strip()
        if "*" in sel:
            facts.select_star = True
        else:
            for col in sel.split(","):
                name = _first_token(col.replace("(", " ").strip())
                if name and name.upper() not in _KEYWORDS:
                    facts.columns.append(name)

    # Colonnes de filtrage (WHERE)
    where_m = _RE_WHERE.search(s)
    if where_m:
        for m in _RE_WHERE_COL.finditer(where_m.group(1)):
            col = m.group(1)
            if col.upper() not in _KEYWORDS:
                facts.where_columns.append(col)

    # Drapeaux
    facts.oracle_outer_join = "(+)" in s
    facts.subquery = len(re.findall(r"\bSELECT\b", s, re.IGNORECASE)) > 1

    facts.tables_read = _dedup(facts.tables_read)
    facts.tables_written = _dedup(facts.tables_written)
    facts.columns = _dedup(facts.columns)
    facts.where_columns = _dedup(facts.where_columns)
    facts.joins = _dedup(facts.joins)
    return facts
