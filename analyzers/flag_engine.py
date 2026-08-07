"""
Flag Engine — Détection déterministe des zones ambiguës
=======================================================
Scanne le JSON IR et produit une liste de Flag.
Zéro LLM — 100% déterministe et testable sans réseau.
"""

import re
import tree_sitter_php as tsphp
from tree_sitter import Language, Parser
from analyzers.constants import STOP_TOKENS
from ir.schema import IRSchema, Flag, FlagType, ImpactCategory, OperationType

_PHP_LANGUAGE = Language(tsphp.language_php())


SECURITY_PATTERNS = [
    (r'md5\s*\(', "sécurisation legacy du secret d'authentification"),
    (r'\$_POST\s*\[', "saisie utilisateur"),
    (r'\$_SESSION\s*\[', "données de session"),
    (r'"id\s*=\s*"\s*\.', "construction dynamique de recherche par identifiant"),
    (r"'id\s*=\s*'\s*\.", "construction dynamique de recherche par identifiant"),
]

# Questions PO pour chaque pattern de risque sécurité
SECURITY_QUESTIONS = {
    r'md5\s*\(': (
        "Cette méthode de protection du secret d'authentification est ancienne et non conforme aux standards actuels. "
        "S'agit-il d'une contrainte documentée ou cette protection est-elle prévue pour évoluer lors de la migration ?"
    ),
    r'\$_POST\s*\[': (
        "Cette donnée saisie par l'utilisateur n'est pas validée à ce stade. "
        "Quelle règle métier définit le format ou les contraintes attendues pour cette donnée ?"
    ),
    r'\$_SESSION\s*\[': (
        "L'identité de l'agent connecté est lue directement depuis la session. "
        "L'habilitation est-elle vérifiée par un service centralisé ou uniquement à cet endroit ?"
    ),
    r'"id\s*=\s*"\s*\.': (
        "La recherche d'un dossier par identifiant est construite dynamiquement. "
        "Les standards de sécurité prévus dans la cible imposent-ils une protection paramétrique ?"
    ),
    r"'id\s*=\s*'\s*\.": (
        "La recherche d'un dossier par identifiant est construite dynamiquement. "
        "Les standards de sécurité prévus dans la cible imposent-ils une protection paramétrique ?"
    ),
}

# Traduction des conditions techniques en termes métier pour les Decision Points
CONDITION_TRANSLATIONS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\$_SESSION\s*\['user'\]\s*\['role'\]\s*!=\s*'admin'"),
     "l'agent connecté n'a pas l'habilitation Administrateur"),
    (re.compile(r"\$_SESSION\s*\['user'\]\s*\['role'\]\s*!=\s*'supervisor'"),
     "l'agent connecté n'a pas l'habilitation Superviseur"),
    (re.compile(r"\$_SESSION\s*\['user'\]\s*\['role'\]\s*==\s*'([^']+)'"),
     "l'agent connecté a le rôle '\\1'"),
    (re.compile(r"\$_SESSION\s*\['user'\]\s*\['role'\]"),
     "le rôle de l'agent connecté"),
    (re.compile(r"empty\s*\(\s*\$email\s*\)\s*\|\|\s*empty\s*\(\s*\$name\s*\)"),
     "l'adresse email ou le nom est absent"),
    (re.compile(r"empty\s*\(\s*\$([^)]+)\s*\)"),
     "le champ '\\1' est vide"),
    (re.compile(r"\$this\s*->\s*getRequest\s*\(\s*\)\s*->\s*isPost\s*\(\s*\)"),
     "le formulaire est soumis par l'utilisateur"),
    (re.compile(r"!\s*\$id\b"),
     "aucun identifiant d'entité fourni"),
    (re.compile(r"^\$id$"),
     "un identifiant d'entité est présent"),
    (re.compile(r"^\$existing$"),
     "un enregistrement correspondant existe déjà"),
    (re.compile(r"^\$user$"),
     "un compte utilisateur correspondant est trouvé"),
    (re.compile(r"^\$result$"),
     "un résultat a été obtenu"),
]

DYNAMIC_SESSION_PATTERNS = [
    r"->get\(['\"][\w]+['\"].*\.\s*\$",        # Session->get('key'. $var)
    r"cable_infos_",                             # clé dynamique composite
    r"_infos_\.\$",                              # pattern clé dynamique _infos_.$var
    r"_data_\.\$",                               # pattern clé dynamique _data_.$var
    r"key_exists\(['\"][\w]+['\"],.*\$session",  # key_exists sur variable session
    r"isset\(\$_SESSION\[.*\$",                  # isset sur clé de session dynamique
    r"session.*->get\(.*\$\w+\)",               # session->get($variable)
]

CHAINED_API_PATTERNS = [
    r"scenarioCode.*\d+.*scenarioCode.*\d+",      # même scenarioCode appelé 2× avec IDs distincts
    r"getSecondCall\w+\(\)",                      # méthodes chaînées séquentielles
    r"lancer\w+\(\)",                             # déclencheurs API externes
    r"(\$\w+Service).*call.*\n.*\1.*call",        # même service appelé 2×
    r"getFirst\w+.*\n(?!.*empty).*getSecond\w+",       # getFirst→getSecond sans empty check
    r"\$payload\s*=.*\$result\w*\n(?!.*empty).*->call", # payload depuis résultat sans guard
]

SITUATION_PATTERNS = [
    r"if\s*\(\s*\$situation\s*===?\s*['\"]",
    r"if\s*\(\s*\$scenario\s*===?\s*['\"]",
    r"if\s*\(\s*\$etape\s*===?\s*['\"]",
    r"if\s*\(\s*\$typeEncha[iî]nement\s*===?\s*['\"]",
    r"===?\s*['\"][A-Z][0-9]{1,2}['\"]",
    r"===?\s*['\"][HSTPpP][0-9]+['\"]",
]

EXTERNAL_STATE_PATTERNS = [
    r"\$\w+Service->get\w+Ticket",
    r"\$\w+Service->get\w+Etat",
    r"\$\w+Service->get\w+Statut",
    r"\$\w+Service->get\w+Situation",
    r"get\w+Array\b",
    r"\$\w+->get(?!.*if\s*\(.*null)",
    r"\$\w+->fetch(?!.*empty)",
]

MODULE_SEQUENCE_PATTERNS = [
    r"retablir\s*\(\)",
    r"cloture[rR]\s*\(\)",
    r"demandeIntervention\s*\(\)",
    r"qualifier\s*\(\)",
    r"piloter\s*\(\)",
    r"diagnostiquer\s*\(\)",
    r"rendre\s*\(\)",
    r"->execute\w+\(\)[\s\n]+(?!if|try|\$result).*->execute\w+\(\)",
]

HARDCODED_SITUATION_PATTERNS = [
    r"===?\s*['\"][A-Z]{1,2}[0-9]{1,2}['\"]",
    r"\$(situation|scenario|etape|module)\s*===?\s*['\"][^'\"]{1,5}['\"]",
    r"===?\s*'(?!self::|CONST_)[A-Z0-9_]{1,8}'",
]

IMPACT_CATEGORY_MAP: dict[str, ImpactCategory] = {
    "security_risk":             ImpactCategory.CRITICAL_CORRUPTION,
    "dynamic_session_key":       ImpactCategory.CRITICAL_CORRUPTION,
    "situation_coverage":        ImpactCategory.CRITICAL_CORRUPTION,
    "external_state_dependency":  ImpactCategory.CRITICAL_CORRUPTION,
    "chained_api_call":          ImpactCategory.API_OVERLOAD,
    "side_effect":               ImpactCategory.API_OVERLOAD,
    "business_logic_unclear":    ImpactCategory.API_OVERLOAD,
    "module_execution_gap":      ImpactCategory.API_OVERLOAD,
    "missing_branch":            ImpactCategory.LOGIC_GAP,
    "magic_value":               ImpactCategory.LOGIC_GAP,
    "unmapped_dep":              ImpactCategory.LOGIC_GAP,
    "hardcoded_situation_code":  ImpactCategory.LOGIC_GAP,
    "empty_catch":               ImpactCategory.CRITICAL_CORRUPTION,
    "strong_coupling":           ImpactCategory.API_OVERLOAD,
    "chained_method_call":       ImpactCategory.CRITICAL_CORRUPTION,
}

# Valeurs exclues du flag magic_value par décision explicite — 'OK'/'KO' et les
# mots-clés SQL/PHP sortent via cette liste, jamais par accident de regex.
MAGIC_VALUE_STOPWORDS: frozenset[str] = STOP_TOKENS

# Stop-words numériques triviaux, appliqués APRÈS match — 0/1 sont des drapeaux
# booléens déguisés, pas des valeurs de référence métier.
MAGIC_VALUE_NUMERIC_STOPWORDS: frozenset[str] = frozenset({"0", "1"})


def _is_magic_noise(value: str) -> bool:
    """True si la valeur matchée est du bruit à écarter du flag magic_value.

    Écarte : chaîne vide, stopwords SQL/PHP/booléens, 0/1, et tout littéral
    d'un seul caractère non alphanumérique. Sans ce filtre, le volume de flags
    rend les rapports illisibles."""
    v = value.strip()
    if not v:
        return True
    if v.upper() in MAGIC_VALUE_STOPWORDS:
        return True
    if v in MAGIC_VALUE_NUMERIC_STOPWORDS:
        return True
    if len(v) == 1 and not v.isalnum():
        return True
    return False


MAGIC_VALUE_PATTERNS = [
    # comparaison == / != avec chaîne quotée — identifiant mixte (A-Za-z0-9_) :
    # couvre minuscules ('admin'), MAJUSCULES ('CODE_X'), PascalCase et chiffres.
    re.compile(r"""[=!]=\s*['"]([A-Za-z_][A-Za-z0-9_]*)['"]"""),
    # comparaison == / != avec entier, quoté ou non, un chiffre ou plus :
    # couvre == 47, == '3', != 2 (l'ancien \d{2,} ratait chiffres uniques et quotés).
    re.compile(r"[=!]=\s*'?(\d+)'?"),
    # littéral en MAJUSCULES quoté hors contexte de comparaison (SQL, valeurs) :
    # 'H1', "TP2", 'ST_OUV', 'C_TYP_FLX'. Lookaround anti-bruit : exclut les
    # sous-scripts de tableau ['CLÉ'] (accès structurel, pas valeur métier) —
    # la vraie valeur d'une comparaison $x['CLÉ'] == 'VAL' reste captée par le
    # pattern de comparaison ci-dessus.
    re.compile(r"""(?<!\[)['"]([A-Z][A-Z0-9_]{1,})['"](?!\])"""),
]

# case 'H1': / in_array('CODE_X', …) — codes situation absents du control_flow
# (l'extracteur ne produit des ControlBlocks que pour les if). Scannés sur raw_code.
CASE_LITERAL_PATTERN = re.compile(r"""case\s+['"]([A-Za-z_][A-Za-z0-9_]*)['"]""")
IN_ARRAY_LITERAL_PATTERN = re.compile(
    r"""in_array\s*\(\s*['"]([A-Za-z_][A-Za-z0-9_]*)['"]"""
)

# Requêtes SQL construites dynamiquement — complète les patterns "id =" . de SECURITY_PATTERNS
SQL_KEYWORD_PATTERN = re.compile(r'\b(?:SELECT|INSERT|UPDATE|DELETE)\b', re.IGNORECASE)
QUOTED_STRING_PATTERN = re.compile(r'''(["'])((?:\\.|(?!\1).)*)\1''', re.DOTALL)
SQL_CONCAT_QUESTION = (
    "La requête d'accès aux données est construite dynamiquement à partir de valeurs "
    "variables. Les standards de sécurité prévus dans la cible imposent-ils une "
    "protection paramétrique pour cet accès ?"
)

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
        self._parser = Parser(_PHP_LANGUAGE)

    def _find_nodes(self, node, node_type: str) -> list:
        """Parcours itératif — évite RecursionError sur les gros fichiers."""
        results = []
        stack = [node]
        while stack:
            current = stack.pop()
            if current.type == node_type:
                results.append(current)
            stack.extend(current.children)
        return results

    def _next_id(self, prefix: str) -> str:
        self._counter += 1
        return f"{prefix}_{self._counter}"

    def analyze(self, ir: IRSchema) -> list[Flag]:
        """Point d'entrée principal. Retourne tous les flags détectés.

        Toute méthode-règle (_check_* / _detect_*) DOIT être appelée ici —
        une règle volontairement désactivée reste listée, commentée avec
        ``# DISABLED: raison``. Le test tests/test_flag_engine_coverage.py
        vérifie cette exhaustivité par introspection.
        """
        self._counter = 0
        flags: list[Flag] = []
        flags.extend(self._check_missing_branches(ir))
        flags.extend(self._check_magic_values(ir))
        flags.extend(self._check_security_risks(ir))
        flags.extend(self._detect_sql_concat(ir))
        flags.extend(self._check_unmapped_deps(ir))
        flags.extend(self._check_db_without_pagination(ir))
        flags.extend(self._check_side_effects_after_write(ir))
        flags.extend(self._detect_dynamic_session_key(ir))
        flags.extend(self._detect_chained_api_call(ir))
        flags.extend(self._detect_situation_coverage(ir))
        flags.extend(self._detect_external_state_dependency(ir))
        flags.extend(self._detect_module_execution_gap(ir))
        flags.extend(self._detect_hardcoded_situation_code(ir))
        flags.extend(self._detect_empty_catch(ir))
        flags.extend(self._detect_strong_coupling(ir))
        flags.extend(self._detect_chained_method_calls(ir))
        for flag in flags:
            flag.impact_category = IMPACT_CATEGORY_MAP.get(flag.type, ImpactCategory.LOGIC_GAP)
        return flags

    # =========================================================================
    # Helpers
    # =========================================================================

    @staticmethod
    def _find_method_for_line(source_line: int, entry_points) -> tuple[str, str]:
        """Retourne (name, original_name) de l'entry_point qui contient source_line."""
        for ep in entry_points:
            if (ep.start_line and ep.end_line
                    and ep.start_line <= source_line <= ep.end_line):
                return ep.name, ep.original_name
        return "unknown", "unknown"

    # =========================================================================
    # Règle 1 — Branches manquantes dans control_flow
    # =========================================================================

    def _check_missing_branches(self, ir: IRSchema) -> list[Flag]:
        flags = []
        for block in ir.control_flow:
            if not block.condition:
                continue
            if block.true_branch is None or block.false_branch is None:
                condition_business = _translate_condition(block.condition)
                method_name, method_orig = (
                    self._find_method_for_line(block.source_line, ir.entry_points)
                    if block.source_line else ("unknown", "unknown")
                )
                if block.business_context:
                    question = (
                        f"Règle documentée : « {block.business_context} ». "
                        f"Le cas contraire n'est pas géré — "
                        f"quel est le comportement attendu ?"
                    )
                else:
                    question = (
                        f"Point de décision — {condition_business}. "
                        f"Quel est le comportement attendu dans le cas contraire ?"
                    )
                flags.append(Flag(
                    id=self._next_id("missing_branch"),
                    type="missing_branch",
                    location=block.id,
                    fragment=block.condition,
                    question=question,
                    source_line=block.source_line,
                    method_name=method_name,
                    method_original_name=method_orig,
                    context_lines=block.raw_context,
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
                    if _is_magic_noise(value):
                        continue
                    key = (block.id, value)
                    if key in seen:
                        continue
                    seen.add(key)
                    condition_business = _translate_condition(block.condition)
                    method_name, method_orig = (
                        self._find_method_for_line(block.source_line, ir.entry_points)
                        if block.source_line else ("unknown", "unknown")
                    )
                    flags.append(Flag(
                        id=self._next_id("magic_value"),
                        type="magic_value",
                        location=block.id,
                        fragment=block.condition,
                        question=(
                            f"Valeur de référence non documentée — La décision « {condition_business} » "
                            f"repose sur la valeur '{value}'. "
                            f"D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?"
                        ),
                        source_line=block.source_line,
                        method_name=method_name,
                        method_original_name=method_orig,
                        context_lines=block.raw_context,
                    ))

        # Scan les details des opérations DB (SQL partiel)
        for op in ir.operations:
            if not op.details:
                continue
            for pattern in MAGIC_VALUE_PATTERNS:
                for match in pattern.finditer(op.details):
                    value = match.group(1)
                    if _is_magic_noise(value):
                        continue
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
                            f"La valeur '{value}' est utilisée comme filtre de sélection des données. "
                            f"Quelle est la règle métier derrière ce filtre ? "
                            f"Cette valeur est-elle susceptible d'évoluer ?"
                        ),
                    ))

        # Scan raw_code : case des switch et in_array('CODE_X', …) — codes situation
        # courts ('H1', 'TP2', …) absents du control_flow qui ne couvre que les if.
        raw_scans = (
            (CASE_LITERAL_PATTERN,
             "une branche de traitement est dédiée au cas '{value}'"),
            (IN_ARRAY_LITERAL_PATTERN,
             "une appartenance à une liste est testée sur la valeur '{value}'"),
        )
        for ep in ir.entry_points:
            if not ep.raw_code:
                continue
            for pattern, phrase in raw_scans:
                for match in pattern.finditer(ep.raw_code):
                    value = match.group(1)
                    if _is_magic_noise(value):
                        continue
                    key = (ep.name, value)
                    if key in seen:
                        continue
                    seen.add(key)
                    abs_line = (ep.start_line or 0) + ep.raw_code[:match.start()].count('\n')
                    flags.append(Flag(
                        id=self._next_id("magic_value"),
                        type="magic_value",
                        location=ep.name,
                        fragment=self._extract_line(ep.raw_code, match.start()),
                        question=(
                            f"Valeur de référence non documentée — {phrase.format(value=value)}. "
                            f"D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?"
                        ),
                        source_line=abs_line if ep.start_line else None,
                        method_name=ep.name,
                        method_original_name=ep.original_name,
                        context_lines=self._extract_context_lines(ep.raw_code, match.start(), max_lines=5),
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
                    question = SECURITY_QUESTIONS.get(pattern_str, (
                        f"Ce point d'attention ({description}) a été identifié. "
                        f"Existe-t-il une règle métier documentée qui justifie ce comportement ?"
                    ))
                    abs_line = (ep.start_line or 0) + ep.raw_code[:match.start()].count('\n')
                    context = self._extract_context_lines(ep.raw_code, match.start(), max_lines=7)
                    flags.append(Flag(
                        id=self._next_id("security"),
                        type="security_risk",
                        location=ep.name,
                        fragment=fragment,
                        question=question,
                        source_line=abs_line if ep.start_line else None,
                        method_name=ep.name,
                        method_original_name=ep.original_name,
                        context_lines=context,
                    ))

        return flags

    # =========================================================================
    # Règle 3b — Requêtes SQL construites dynamiquement
    # Couvre : "SELECT…" . $var, sprintf("…%s…"), variable concaténée
    # puis passée à query()/fetchAll()/fetchRow()
    # =========================================================================

    def _detect_sql_concat(self, ir: IRSchema) -> list[Flag]:
        flags = []
        seen: set[tuple] = set()
        for ep in ir.entry_points:
            code = ep.raw_code
            if not code:
                continue

            sites: list[int] = []

            # Cas 1 — concaténation directe : "SELECT …" . $var
            for m in QUOTED_STRING_PATTERN.finditer(code):
                if not SQL_KEYWORD_PATTERN.search(m.group(2)):
                    continue
                if re.match(r'\s*\.\s*\$', code[m.end():m.end() + 20]):
                    sites.append(m.start())

            # Cas 2 — sprintf("SELECT … %s …", $var)
            for m in re.finditer(r'sprintf\s*\(\s*(["\'])((?:\\.|(?!\1).)*)\1', code, re.DOTALL):
                if SQL_KEYWORD_PATTERN.search(m.group(2)) and '%s' in m.group(2):
                    sites.append(m.start())

            # Cas 3 — variable SQL concaténée puis réutilisée dans query()/fetchAll()
            sql_vars: set[str] = set()
            for m in re.finditer(r'\$(\w+)\s*\.?=\s*(["\'])((?:\\.|(?!\2).)*)\2', code, re.DOTALL):
                if SQL_KEYWORD_PATTERN.search(m.group(3)):
                    sql_vars.add(m.group(1))
            for var in sql_vars:
                concatenated = (
                    re.search(rf'\${var}\s*\.=', code)
                    or re.search(rf'\${var}\s*=\s*[^;]*\.\s*\$', code)
                )
                used = re.search(rf'->(?:query|fetchAll|fetchRow)\s*\(\s*\${var}\b', code)
                if concatenated and used:
                    sites.append(used.start())

            for pos in sites:
                fragment = self._extract_line(code, pos)
                key = (ep.name, fragment)
                if key in seen:
                    continue
                seen.add(key)
                abs_line = (ep.start_line or 0) + code[:pos].count('\n')
                flags.append(Flag(
                    id=self._next_id("security"),
                    type="security_risk",
                    location=ep.name,
                    fragment=fragment,
                    question=SQL_CONCAT_QUESTION,
                    source_line=abs_line if ep.start_line else None,
                    method_name=ep.name,
                    method_original_name=ep.original_name,
                    context_lines=self._extract_context_lines(code, pos, max_lines=7),
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
                        f"Service tiers non documenté — Le composant '{dep.name}' est utilisé "
                        f"dans ce périmètre sans équivalent identifié dans la cible. "
                        f"Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?"
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
                        f"Volume non borné — Ce chargement ramène potentiellement l'intégralité des données "
                        f"sans limitation de volume. Quelle est la règle métier sur le nombre d'éléments attendus ? "
                        f"Un affichage paginé ou un export par lot est-il prévu ?"
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
                        type="side_effect",
                        location=ep.name,
                        fragment=fragment,
                        question=(
                            f"Notification automatique — Après l'enregistrement des données, {email_desc}. "
                            f"Si cette notification ne peut pas être envoyée, l'opération est-elle annulée ou "
                            f"considérée comme réussie malgré tout ?"
                        ),
                    ))
                    break  # une seule flag par (entry_point, write_op)

        return flags

    # =========================================================================
    # Règle 7 — Clés de session dynamiques (stale data)
    # =========================================================================

    def _detect_dynamic_session_key(self, ir: IRSchema) -> list[Flag]:
        flags = []
        for ep in ir.entry_points:
            if not ep.raw_code:
                continue
            for pattern in DYNAMIC_SESSION_PATTERNS:
                match = re.search(pattern, ep.raw_code, re.IGNORECASE)
                if not match:
                    continue
                fragment = self._extract_line(ep.raw_code, match.start())
                context = self._extract_context_lines(ep.raw_code, match.start(), max_lines=7)
                abs_line = (ep.start_line or 0) + ep.raw_code[:match.start()].count('\n')
                flags.append(Flag(
                    id=self._next_id("dynamic_session_key"),
                    type="dynamic_session_key",
                    location=ep.name,
                    fragment=fragment,
                    question=(
                        "Clé de session dynamique détectée — "
                        "cette clé est-elle nettoyée explicitement "
                        "dans TOUS les chemins de sortie ? "
                        "(transitions : ASSEMBLEE→CABLE, "
                        "EQUIPEMENT→CABLE, reclassification Océane)"
                    ),
                    source_line=abs_line if ep.start_line else None,
                    method_name=ep.name,
                    method_original_name=ep.original_name,
                    context_lines=context,
                ))
                break  # 1 flag par entry_point max
        return flags

    # =========================================================================
    # Règle 8 — Appels API séquentiels sans validation (payload vide)
    # =========================================================================

    def _detect_chained_api_call(self, ir: IRSchema) -> list[Flag]:
        flags = []
        for ep in ir.entry_points:
            if not ep.raw_code:
                continue
            for pattern in CHAINED_API_PATTERNS:
                match = re.search(pattern, ep.raw_code, re.IGNORECASE | re.DOTALL)
                if not match:
                    continue
                fragment = self._extract_line(ep.raw_code, match.start())
                context = self._extract_context_lines(ep.raw_code, match.start(), max_lines=7)
                abs_line = (ep.start_line or 0) + ep.raw_code[:match.start()].count('\n')
                flags.append(Flag(
                    id=self._next_id("chained_api_call"),
                    type="chained_api_call",
                    location=ep.name,
                    fragment=fragment,
                    question=(
                        "Appels API séquentiels détectés — "
                        "le résultat de l'appel 1 est-il validé "
                        "(!empty / null check) avant d'être utilisé "
                        "comme payload de l'appel 2 ? "
                        "(risque 400 Invalid request "
                        "si prestation inconnue ou service indisponible)"
                    ),
                    source_line=abs_line if ep.start_line else None,
                    method_name=ep.name,
                    method_original_name=ep.original_name,
                    context_lines=context,
                ))
                break  # 1 flag par entry_point max
        return flags

    # =========================================================================
    # Règle 9 — Situation Oracle non couverte (pas de else final)
    # =========================================================================

    def _detect_situation_coverage(self, ir: IRSchema) -> list[Flag]:
        flags = []
        for ep in ir.entry_points:
            if not ep.raw_code:
                continue
            for pattern in SITUATION_PATTERNS:
                match = re.search(pattern, ep.raw_code, re.IGNORECASE)
                if not match:
                    continue
                if self._has_final_else(ep.raw_code, match.start()):
                    continue  # ce pattern est couvert par un else → passer au suivant
                segment = ep.raw_code[match.start():match.start() + 1000]
                covered = re.findall(r"===?\s*['\"]([^'\"]+)['\"]", segment)
                covered_str = ", ".join(f"'{v}'" for v in covered[:5]) if covered else "?"
                fragment = self._extract_line(ep.raw_code, match.start())
                context = self._extract_context_lines(ep.raw_code, match.start(), max_lines=7)
                abs_line = (ep.start_line or 0) + ep.raw_code[:match.start()].count('\n')
                flags.append(Flag(
                    id=self._next_id("situation_coverage"),
                    type="situation_coverage",
                    location=ep.name,
                    fragment=fragment,
                    question=(
                        f"{len(covered)} situation(s) couverte(s) explicitement ({covered_str}). "
                        "Que se passe-t-il si le service externe retourne une valeur non listée dans ce code ? "
                        "Existe-t-il une situation par défaut ?"
                    ),
                    source_line=abs_line if ep.start_line else None,
                    method_name=ep.name,
                    method_original_name=ep.original_name,
                    context_lines=context,
                ))
                break  # 1 flag par entry_point max
        return flags

    # =========================================================================
    # Règle 10 — Dépendance service externe temps réel sans fallback
    # =========================================================================

    def _detect_external_state_dependency(self, ir: IRSchema) -> list[Flag]:
        flags = []
        for ep in ir.entry_points:
            if not ep.raw_code:
                continue
            for pattern in EXTERNAL_STATE_PATTERNS:
                match = re.search(pattern, ep.raw_code, re.IGNORECASE)
                if not match:
                    continue
                fragment = self._extract_line(ep.raw_code, match.start())
                context = self._extract_context_lines(ep.raw_code, match.start(), max_lines=7)
                abs_line = (ep.start_line or 0) + ep.raw_code[:match.start()].count('\n')
                flags.append(Flag(
                    id=self._next_id("external_state_dependency"),
                    type="external_state_dependency",
                    location=ep.name,
                    fragment=fragment,
                    question=(
                        "L'état est lu depuis un service externe en temps réel à cette étape — "
                        "3 cas non documentés : "
                        "(1) Service externe indisponible → que faire ? "
                        "(2) Service externe retourne null → continuer ou bloquer ? "
                        "(3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?"
                    ),
                    source_line=abs_line if ep.start_line else None,
                    method_name=ep.name,
                    method_original_name=ep.original_name,
                    context_lines=context,
                ))
                break  # 1 flag par entry_point max
        return flags

    # =========================================================================
    # Règle 11 — Modules séquentiels sans vérification d'échec
    # =========================================================================

    def _detect_module_execution_gap(self, ir: IRSchema) -> list[Flag]:
        flags = []
        simple_pats = MODULE_SEQUENCE_PATTERNS[:7]
        generic_pats = MODULE_SEQUENCE_PATTERNS[7:]
        for ep in ir.entry_points:
            if not ep.raw_code:
                continue
            match = None
            for pattern in generic_pats:
                m = re.search(pattern, ep.raw_code, re.IGNORECASE | re.DOTALL)
                if m:
                    match = m
                    break
            if not match:
                hits = [(p, re.search(p, ep.raw_code, re.IGNORECASE)) for p in simple_pats]
                hits = [(p, m) for p, m in hits if m]
                if len(hits) >= 2:
                    match = hits[0][1]
            if not match:
                continue
            module_names = [
                re.search(r'\w+', p).group()
                for p in simple_pats
                if re.search(p, ep.raw_code, re.IGNORECASE)
            ]
            modules_str = " → ".join(module_names[:3]) if module_names else "module(s)"
            fragment = self._extract_line(ep.raw_code, match.start())
            context = self._extract_context_lines(ep.raw_code, match.start(), max_lines=7)
            abs_line = (ep.start_line or 0) + ep.raw_code[:match.start()].count('\n')
            flags.append(Flag(
                id=self._next_id("module_execution_gap"),
                type="module_execution_gap",
                location=ep.name,
                fragment=fragment,
                question=(
                    f"Ces modules s'exécutent en séquence ({modules_str}) — "
                    "si l'un d'eux échoue ou retourne une erreur, "
                    "le suivant est-il déclenché quand même ? "
                    "Quel est le comportement attendu en cas d'échec partiel de l'enchaînement ?"
                ),
                source_line=abs_line if ep.start_line else None,
                method_name=ep.name,
                method_original_name=ep.original_name,
                context_lines=context,
            ))
        return flags

    # =========================================================================
    # Règle 12 — Code situation hardcodé (désynchronisation Oracle possible)
    # =========================================================================

    def _detect_hardcoded_situation_code(self, ir: IRSchema) -> list[Flag]:
        flags = []
        seen: set[tuple] = set()
        for ep in ir.entry_points:
            if not ep.raw_code:
                continue
            for pattern in HARDCODED_SITUATION_PATTERNS:
                for match in re.finditer(pattern, ep.raw_code, re.IGNORECASE):
                    raw_val = re.search(r"['\"]([^'\"]+)['\"]", match.group())
                    value = raw_val.group(1) if raw_val else match.group().strip("=? '\"")
                    # Un code situation est court et en MAJUSCULES (H1, TP2, ST_OUV).
                    # Filtre le bruit : minuscules ('ko', 'ligne'), chiffres seuls
                    # ('0'), stopwords ('OK') — ils noyaient le signal des rapports.
                    if not re.fullmatch(r"[A-Z][A-Z0-9_]{0,7}", value):
                        continue
                    if value in MAGIC_VALUE_STOPWORDS:
                        continue
                    key = (ep.name, value)
                    if key in seen:
                        continue
                    seen.add(key)
                    fragment = self._extract_line(ep.raw_code, match.start())
                    context = self._extract_context_lines(ep.raw_code, match.start(), max_lines=5)
                    abs_line = (ep.start_line or 0) + ep.raw_code[:match.start()].count('\n')
                    flags.append(Flag(
                        id=self._next_id("hardcoded_situation_code"),
                        type="hardcoded_situation_code",
                        location=ep.name,
                        fragment=fragment,
                        question=(
                            f"Le code situation '{value}' est hardcodé — "
                            "vient-il d'une table de référence Oracle ? "
                            "Est-il synchronisé avec les enchaînements configurés "
                            "dans l'interface admin ? "
                            "Existe-t-il une constante PHP correspondante ?"
                        ),
                        source_line=abs_line if ep.start_line else None,
                        method_name=ep.name,
                        method_original_name=ep.original_name,
                        context_lines=context,
                    ))
        return flags

    # =========================================================================
    # Règle 13 — Catch vide (erreur silencieuse)
    # =========================================================================

    def _detect_empty_catch(self, ir: IRSchema) -> list[Flag]:
        flags = []
        for ep in ir.entry_points:
            if not ep.raw_code:
                continue
            raw_bytes = ep.raw_code.encode('utf-8')
            tree = self._parser.parse(raw_bytes)
            for catch in self._find_nodes(tree.root_node, 'catch_clause'):
                body = catch.child_by_field_name('body')
                if not body:
                    continue
                non_trivial = [c for c in body.children if c.type not in ('{', '}', 'comment')]
                if non_trivial:
                    continue
                fragment = raw_bytes[catch.start_byte:min(catch.end_byte, catch.start_byte + 80)].decode('utf-8', errors='replace').strip()
                abs_line = (ep.start_line or 0) + catch.start_point[0]
                context = self._extract_context_lines(ep.raw_code, catch.start_byte, max_lines=5)
                flags.append(Flag(
                    id=self._next_id("empty_catch"),
                    type=FlagType.EMPTY_CATCH,
                    location=ep.name,
                    fragment=fragment,
                    question=(
                        "Exception capturée mais ignorée — "
                        "que doit faire le système si cette erreur survient ?"
                    ),
                    source_line=abs_line if ep.start_line else None,
                    method_name=ep.name,
                    method_original_name=ep.original_name,
                    context_lines=context,
                ))
        return flags

    # =========================================================================
    # Règle 14 — Couplage fort ($this->app->get)
    # =========================================================================

    def _detect_strong_coupling(self, ir: IRSchema) -> list[Flag]:
        flags = []
        for ep in ir.entry_points:
            if not ep.raw_code:
                continue
            count = ep.raw_code.count("->app->get(")
            if count < 5:
                continue
            match = re.search(r'->app->get\([^)]+\)', ep.raw_code)
            fragment = match.group(0) if match else f"->app->get() ×{count}"
            abs_line = (ep.start_line or 0) + ep.raw_code[:match.start()].count('\n') if match else ep.start_line
            flags.append(Flag(
                id=self._next_id("strong_coupling"),
                type=FlagType.STRONG_COUPLING,
                location=ep.name,
                fragment=fragment,
                question=(
                    f"{count} services injectés manuellement dans cette méthode — "
                    "ce couplage fort rend la méthode non testable "
                    "et fragile en cas de migration."
                ),
                source_line=abs_line if ep.start_line else None,
                method_name=ep.name,
                method_original_name=ep.original_name,
            ))
        return flags

    # =========================================================================
    # Règle 15 — Appels chaînés sans garde-fou null
    # =========================================================================

    def _detect_chained_method_calls(self, ir: IRSchema) -> list[Flag]:
        flags = []
        for ep in ir.entry_points:
            if not ep.raw_code:
                continue
            raw_bytes = ep.raw_code.encode('utf-8')
            tree = self._parser.parse(raw_bytes)
            seen_frags: set[str] = set()
            for chain in self._find_nodes(tree.root_node, 'member_call_expression'):
                obj = chain.child_by_field_name('object')
                if not obj or obj.type != 'member_call_expression':
                    continue
                fragment = raw_bytes[chain.start_byte:min(chain.end_byte, chain.start_byte + 120)].decode('utf-8', errors='replace')
                key = fragment[:60]
                if key in seen_frags:
                    continue
                seen_frags.add(key)
                abs_line = (ep.start_line or 0) + chain.start_point[0]
                context = self._extract_context_lines(ep.raw_code, chain.start_byte, max_lines=3)
                flags.append(Flag(
                    id=self._next_id("chained_method_call"),
                    type=FlagType.CHAINED_METHOD_CALL,
                    location=ep.name,
                    fragment=fragment.strip(),
                    question=(
                        "Appel chaîné détecté — "
                        "si le premier appel retourne null, "
                        "le second provoque une erreur fatale."
                    ),
                    source_line=abs_line if ep.start_line else None,
                    method_name=ep.name,
                    method_original_name=ep.original_name,
                    context_lines=context,
                ))
        return flags

    # =========================================================================
    # Helpers
    # =========================================================================

    @staticmethod
    def _has_final_else(raw_code: str, start: int, window: int = 2000) -> bool:
        """Vérifie si la chaîne if/elseif à partir de start se termine par un else."""
        segment = raw_code[start:start + window]
        return bool(re.search(r'\}\s*else\s*(?!\s*if\b)', segment, re.IGNORECASE))

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


# =============================================================================
# Helpers module-level
# =============================================================================

def _translate_condition(condition: str) -> str:
    """Traduit une condition technique en formulation métier pour un PO."""
    cond = condition.strip()
    for pattern, translation in CONDITION_TRANSLATIONS:
        m = pattern.search(cond)
        if m:
            try:
                return pattern.sub(translation, cond)
            except re.error:
                return translation
    # Fallback : retirer les signes $ et simplifier
    clean = re.sub(r'\$_(?:POST|GET|SESSION|REQUEST)\s*\[[^\]]+\]', 'donnée saisie', cond)
    clean = re.sub(r'\$(\w+)', r"'\1'", clean)
    clean = re.sub(r'\s*!=\s*', ' différent de ', clean)
    clean = re.sub(r'\s*==\s*', ' égal à ', clean)
    clean = re.sub(r'\s*\|\|\s*', ' ou ', clean)
    clean = re.sub(r'\s*&&\s*', ' et ', clean)
    return clean
