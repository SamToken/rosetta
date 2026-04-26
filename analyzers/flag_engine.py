"""
Flag Engine — Détection déterministe des zones ambiguës
=======================================================
Scanne le JSON IR et produit une liste de Flag.
Zéro LLM — 100% déterministe et testable sans réseau.
"""

import re
from ir.schema import IRSchema, Flag, ImpactCategory, OperationType


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
    r"cable_infos_",                             # clé Astro spécifique
    r"_infos_\.\$",                              # pattern clé dynamique _infos_.$var
    r"_data_\.\$",                               # pattern clé dynamique _data_.$var
    r"key_exists\(['\"][\w]+['\"],.*\$session",  # key_exists sur variable session
    r"isset\(\$_SESSION\[.*\$",                  # isset sur clé de session dynamique
    r"session.*->get\(.*\$\w+\)",               # session->get($variable)
]

CHAINED_API_PATTERNS = [
    r"scenarioCode.*71.*scenarioCode.*10389",    # scénarios Orchestra connus
    r"getSecondCall\w+\(\)",                      # méthodes chaînées Astro
    r"lancerEtx\w+\(\)",                         # déclencheurs ETX Astro
    r"(orchestra|oceane|adelia).*call.*\n.*\1.*call",  # même service appelé 2×
    r"getFirst\w+.*\n(?!.*empty).*getSecond\w+",       # getFirst→getSecond sans empty check
    r"\$payload\s*=.*\$result\w*\n(?!.*empty).*->call", # payload depuis résultat sans guard
]

IMPACT_CATEGORY_MAP: dict[str, ImpactCategory] = {
    "security_risk":         ImpactCategory.CRITICAL_CORRUPTION,
    "dynamic_session_key":   ImpactCategory.CRITICAL_CORRUPTION,
    "chained_api_call":      ImpactCategory.API_OVERLOAD,
    "side_effect":           ImpactCategory.API_OVERLOAD,
    "business_logic_unclear": ImpactCategory.API_OVERLOAD,
    "missing_branch":        ImpactCategory.LOGIC_GAP,
    "magic_value":           ImpactCategory.LOGIC_GAP,
    "unmapped_dep":          ImpactCategory.LOGIC_GAP,
}

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
        flags.extend(self._detect_dynamic_session_key(ir))
        flags.extend(self._detect_chained_api_call(ir))
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
                flags.append(Flag(
                    id=self._next_id("missing_branch"),
                    type="missing_branch",
                    location=block.id,
                    fragment=block.condition,
                    question=(
                        f"Point de décision — {condition_business}. "
                        f"Quel est le comportement attendu dans le cas contraire ?"
                    ),
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
                        type="business_logic_unclear",
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
    # Règle 7 — Clés de session dynamiques (Astro — stale data)
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
    # Règle 8 — Appels API séquentiels sans validation (Astro — payload vide)
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
