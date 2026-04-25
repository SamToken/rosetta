"""
Flag Engine — Détection déterministe des zones ambiguës
=======================================================
Scanne le JSON IR et produit une liste de Flag.
Zéro LLM — 100% déterministe et testable sans réseau.
"""

import re
from ir.schema import IRSchema, Flag, OperationType


SECURITY_PATTERNS = [
    (r'md5\s*\(', "md5 — algorithme de hachage obsolète pour les mots de passe"),
    (r'\$_POST\s*\[', "$_POST direct — pas de validation Zend/Symfony"),
    (r'\$_SESSION\s*\[', "Session accédée directement — à abstraire"),
    (r'"id\s*=\s*"\s*\.', "Concaténation SQL directe — risque injection"),
    (r"'id\s*=\s*'\s*\.", "Concaténation SQL directe — risque injection"),
]

MAGIC_VALUE_PATTERNS = [
    re.compile(r"!=\s*'([a-z_]+)'"),   # != 'admin'
    re.compile(r"==\s*'([a-z_]+)'"),   # == 'active'
    re.compile(r"=\s*'([a-z_]+)'"),    # = 'active' (assignment or comparison)
    re.compile(r"==\s*(\d{2,})"),      # == 47 (multi-digit integer literals)
]

EMAIL_AFTER_WRITE_PATTERNS = [
    (r'\$mail\s*->\s*send\s*\(', "un email est envoyé"),
    (r'new\s+Zend_Mail\s*\(', "un objet mail Zend est créé"),
    (r'->sendMail\s*\(', "sendMail est appelé"),
    (r'mailer\s*->\s*send\s*\(', "le mailer est appelé"),
]

DB_WRITE_PATTERNS = [
    r'->insert\s*\(',
    r'->update\s*\(',
]


class FlagEngine:
    """
    Analyse un IRSchema et produit une liste de Flag.
    Chaque règle est indépendante et peut être testée séparément.
    """

    def __init__(self):
        self._counter = 0

    def _next_id(self, prefix: str) -> str:
        self._counter += 1
        return f"{prefix}_{self._counter}"

    def analyze(self, ir: IRSchema) -> list[Flag]:
        """Point d'entrée principal. Retourne tous les flags détectés."""
        self._counter = 0
        flags: list[Flag] = []
        flags.extend(self._check_missing_branches(ir))
        flags.extend(self._check_magic_values(ir))
        flags.extend(self._check_security_risks(ir))
        flags.extend(self._check_unmapped_deps(ir))
        flags.extend(self._check_db_without_pagination(ir))
        flags.extend(self._check_side_effects_after_write(ir))
        return flags

    # =========================================================================
    # Règle 1 — Branches manquantes dans control_flow
    # =========================================================================

    def _check_missing_branches(self, ir: IRSchema) -> list[Flag]:
        flags = []
        for block in ir.control_flow:
            if not block.condition:
                continue
            if block.true_branch is None or block.false_branch is None:
                missing = []
                if block.true_branch is None:
                    missing.append("branche vraie")
                if block.false_branch is None:
                    missing.append("branche fausse")
                flags.append(Flag(
                    id=self._next_id("missing_branch"),
                    type="missing_branch",
                    location=block.id,
                    fragment=block.condition,
                    question=(
                        f"La condition « {block.condition} » n'a pas de "
                        f"{' ni '.join(missing)} explicite dans le graphe de contrôle. "
                        f"Quel est le comportement attendu dans le cas contraire ?"
                    ),
                ))
        return flags

    # =========================================================================
    # Règle 2 — Magic values (strings et entiers non nommés)
    # =========================================================================

    def _check_magic_values(self, ir: IRSchema) -> list[Flag]:
        flags = []
        seen: set[tuple] = set()

        # Scan conditions dans le control_flow
        for block in ir.control_flow:
            if not block.condition:
                continue
            for pattern in MAGIC_VALUE_PATTERNS:
                for match in pattern.finditer(block.condition):
                    value = match.group(1)
                    key = (block.id, value)
                    if key in seen:
                        continue
                    seen.add(key)
                    flags.append(Flag(
                        id=self._next_id("magic_value"),
                        type="magic_value",
                        location=block.id,
                        fragment=block.condition,
                        question=(
                            f"La valeur littérale '{value}' apparaît directement dans la condition. "
                            f"D'où vient cette valeur ? Est-elle définie dans une constante, "
                            f"un enum ou une table de référence ?"
                        ),
                    ))

        # Scan les details des opérations DB (SQL partiel)
        for op in ir.operations:
            if not op.details:
                continue
            for pattern in MAGIC_VALUE_PATTERNS:
                for match in pattern.finditer(op.details):
                    value = match.group(1)
                    key = (op.id, value)
                    if key in seen:
                        continue
                    seen.add(key)
                    flags.append(Flag(
                        id=self._next_id("magic_value"),
                        type="magic_value",
                        location=op.id,
                        fragment=op.details,
                        question=(
                            f"La valeur '{value}' est filtrée directement dans la requête SQL. "
                            f"Quelle est la règle métier derrière ce filtre ?"
                        ),
                    ))

        return flags

    # =========================================================================
    # Règle 3 — Risques sécurité détectables statiquement
    # =========================================================================

    def _check_security_risks(self, ir: IRSchema) -> list[Flag]:
        flags = []
        seen: set[tuple] = set()

        for ep in ir.entry_points:
            if not ep.raw_code:
                continue
            for pattern_str, description in SECURITY_PATTERNS:
                compiled = re.compile(pattern_str)
                for match in compiled.finditer(ep.raw_code):
                    fragment = self._extract_line(ep.raw_code, match.start())
                    key = (ep.name, pattern_str, fragment)
                    if key in seen:
                        continue
                    seen.add(key)
                    flags.append(Flag(
                        id=self._next_id("security"),
                        type="security_risk",
                        location=ep.name,
                        fragment=fragment,
                        question=(
                            f"Risque sécurité : {description}. "
                            f"Quelle contrainte métier ou technique justifie ce code ?"
                        ),
                    ))

        return flags

    # =========================================================================
    # Règle 4 — Dépendances sans mapping Symfony
    # =========================================================================

    def _check_unmapped_deps(self, ir: IRSchema) -> list[Flag]:
        flags = []
        for dep in ir.dependencies:
            if dep.suggested_symfony is None:
                flags.append(Flag(
                    id=self._next_id("unmapped_dep"),
                    type="unmapped_dep",
                    location=dep.name,
                    fragment=f"{dep.type}: {dep.name}",
                    question=(
                        f"La dépendance '{dep.name}' (type : {dep.type}) n'a pas "
                        f"de correspondance Symfony connue. Quel est son rôle fonctionnel ?"
                    ),
                ))
        return flags

    # =========================================================================
    # Règle 5 — Opérations DB sans pagination
    # =========================================================================

    def _check_db_without_pagination(self, ir: IRSchema) -> list[Flag]:
        flags = []
        for op in ir.operations:
            if (
                op.type == OperationType.DB_READ
                and "SELECT *" in op.details.upper()
                and "LIMIT" not in op.details.upper()
                and "WHERE ID" not in op.details.upper()  # single-row lookups don't need pagination
            ):
                flags.append(Flag(
                    id=self._next_id("pagination"),
                    type="business_logic_unclear",
                    location=op.id,
                    fragment=op.details,
                    question=(
                        f"Cette requête retourne potentiellement tous les enregistrements "
                        f"({op.details}). Quelle est la règle métier sur le volume attendu ? "
                        f"Une pagination est-elle nécessaire ?"
                    ),
                ))
        return flags

    # =========================================================================
    # Règle 6 — Effets de bord après écriture (email, appel externe)
    # =========================================================================

    def _check_side_effects_after_write(self, ir: IRSchema) -> list[Flag]:
        flags = []

        for ep in ir.entry_points:
            if not ep.raw_code:
                continue

            for write_pattern in DB_WRITE_PATTERNS:
                write_match = re.search(write_pattern, ep.raw_code)
                if not write_match:
                    continue

                code_after_write = ep.raw_code[write_match.start():]

                for email_pattern, email_desc in EMAIL_AFTER_WRITE_PATTERNS:
                    if not re.search(email_pattern, code_after_write):
                        continue

                    fragment = self._extract_context_lines(
                        ep.raw_code, write_match.start(), max_lines=12
                    )
                    flags.append(Flag(
                        id=self._next_id("side_effect"),
                        type="business_logic_unclear",
                        location=ep.name,
                        fragment=fragment,
                        question=(
                            f"Après une opération d'écriture en base, {email_desc}. "
                            f"Est-ce synchrone par design ou une contrainte legacy ? "
                            f"Que se passe-t-il si cet effet de bord échoue ?"
                        ),
                    ))
                    break  # une seule flag par (entry_point, write_op)

        return flags

    # =========================================================================
    # Helpers
    # =========================================================================

    @staticmethod
    def _extract_line(code: str, pos: int) -> str:
        """Extrait la ligne contenant la position donnée."""
        start = code.rfind('\n', 0, pos) + 1
        end = code.find('\n', pos)
        if end == -1:
            end = len(code)
        return code[start:end].strip()

    @staticmethod
    def _extract_context_lines(code: str, pos: int, max_lines: int = 10) -> str:
        """Extrait jusqu'à max_lines lignes à partir de la position donnée."""
        start = code.rfind('\n', 0, pos) + 1
        lines = code[start:].split('\n')
        return '\n'.join(line.rstrip() for line in lines[:max_lines])
