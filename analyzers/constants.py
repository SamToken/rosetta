"""
Constantes partagées entre analyzers (llm_enricher, relation_extractor, etc.).
"""

STOP_TOKENS: frozenset[str] = frozenset({
    # Booléens / nulls
    "NULL", "TRUE", "FALSE", "NONE",
    # Mots-clés SQL
    "SELECT", "FROM", "WHERE", "AND", "OR", "NOT", "IN", "IS", "AS",
    "ORDER", "BY", "GROUP", "HAVING", "JOIN", "LEFT", "RIGHT", "INNER",
    "OUTER", "ON", "DISTINCT", "COUNT", "SUM", "AVG", "MIN", "MAX",
    "LIMIT", "OFFSET", "VALUES", "SET", "INSERT", "UPDATE", "DELETE",
    "INTO", "BETWEEN", "LIKE", "EXISTS", "UNION", "ALL",
    # Types SQL
    "INT", "INTEGER", "VARCHAR", "TEXT", "DATE", "TIMESTAMP", "FLOAT",
    "DECIMAL", "BOOLEAN", "BLOB", "CLOB", "NUMBER",
    # HTTP
    "GET", "POST", "PUT", "PATCH", "HEAD", "OPTIONS",
    # PHP
    "ARRAY", "STRING", "OBJECT", "CLASS", "FUNCTION", "RETURN",
    "PUBLIC", "PRIVATE", "PROTECTED", "STATIC", "ABSTRACT", "FINAL",
    "THROW", "CATCH", "TRY", "FINALLY",
    # Trop courts / génériques
    "OK", "KO", "ID", "PK", "FK",
})
