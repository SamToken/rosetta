"""
Business Doc Generator — Documentation métier lisible par un PO
================================================================
Transforme un IRSchema enrichi (flags + llm_insights) en Markdown.

Deux sorties :
- generate()             → doc complète par action
- generate_flags_summary() → liste des zones à valider
"""

import re
from datetime import datetime
from typing import Optional
from ir.schema import IRSchema, Flag, LLMInsight, BugSeverity
from analyzers.llm_enricher import TokenUsage, PRICING
from analyzers.bug_enricher import format_bug_findings_md

FLAG_LABELS: dict[str, str] = {
    "missing_branch":        "⚠️  Branche manquante",
    "magic_value":           "🔢 Valeur de référence non documentée",
    "security_risk":         "🔴 Risque sécurité",
    "unmapped_dep":          "❓ Service non mappé",
    "business_logic_unclear": "❓ Logique métier ambiguë",
    "side_effect":           "⚡ Effet de bord",
    "dynamic_session_key":      "🔑 Session dynamique — risque stale",
    "chained_api_call":         "🔗 Appels API chaînés — risque payload vide",
    "situation_coverage":       "🎯 Situation non couverte — comportement indéfini",
    "oceane_state_dependency":  "🌊 Dépendance Oceane temps réel — pas de fallback",
    "module_execution_gap":     "⚙️  Module séquentiel — échec silencieux possible",
    "hardcoded_situation_code": "🔢 Code situation hardcodé — risque désynchronisation",
    "empty_catch":              "🕳️ Exception ignorée — erreur silencieuse",
    "strong_coupling":          "🔧 Couplage fort — méthode non testable",
    "chained_method_call":      "⛓️ Appel chaîné — risque null pointer",
}

# Traductions fragment technique → terme métier (dans l'ordre de priorité)
TECH_TO_BUSINESS: list[tuple[str, str]] = [
    (r"\$_SESSION\s*\['user'\]\s*\['role'\]\s*!=\s*'admin'", "vérification habilitation Administrateur"),
    (r"\$_SESSION\s*\['user'\]\s*\['role'\]\s*!=\s*'([^']+)'", r"vérification habilitation \1"),
    (r"\$_SESSION\s*\['user'\]\s*\['role'\]", "habilitation de l'agent connecté"),
    (r"\$_SESSION\b[^;]*", "données de l'agent connecté"),
    (r"\$_POST\s*\[\s*'email'\s*\][^;]*", "saisie de l'adresse de contact"),
    (r"\$_POST\s*\[\s*'name'\s*\][^;]*", "saisie de la dénomination"),
    (r"\$_POST\s*\[\s*'password'\s*\][^;]*", "saisie du secret d'authentification"),
    (r"\$_POST\s*\[\s*'role'\s*\][^;]*", "saisie du niveau d'habilitation"),
    (r"\$_POST\s*\[\s*'([^']+)'\s*\][^;]*", r"saisie du champ « \1 »"),
    (r"'password'\s*=>\s*md5\s*\([^)]+\)[^,;]*", "sécurisation legacy du secret d'authentification"),
    (r"\$db\s*->\s*delete\s*\(\s*'([^']+)'[^)]*\)", r"suppression définitive dans « \1 »"),
    (r"SELECT \* FROM (\w+)", r"chargement complet de la liste « \1 »"),
    (r"\$db\s*->\s*insert\s*\([^)]*\)", "enregistrement d'un nouveau dossier"),
    (r"\$db\s*->\s*update\s*\([^)]*\)", "modification du dossier existant"),
]


class BusinessDocGenerator:
    """Génère la documentation métier depuis un IRSchema enrichi."""

    def generate(
        self,
        ir: IRSchema,
        usage: Optional[TokenUsage] = None,
        model: str = "",
    ) -> str:
        """Doc complète organisée par action, lisible par un PO."""
        lines: list[str] = []

        controller = ir.metadata.controller_name
        extracted_at = ir.metadata.extracted_at.strftime("%Y-%m-%d")
        confidence = ir.metadata.confidence_score

        lines.append(f"# {controller}Controller — Règles Métier")
        lines.append(f"Extrait le : {extracted_at} | Confiance extraction : {confidence}")
        lines.append("")

        # Index de recherche rapide
        flags_by_location: dict[str, list[Flag]] = {}
        for flag in ir.flags:
            flags_by_location.setdefault(flag.location, []).append(flag)

        insights_by_flag: dict[str, LLMInsight] = {
            ins.flag_id: ins for ins in ir.llm_insights
        }

        # =====================================================================
        # Une section par action
        # =====================================================================
        for ep in ir.entry_points:
            if ir.metadata.file_type == "controller":
                methods = "/".join(ep.http_methods)
                lines.append(f"## Action : {ep.name}")
                lines.append(f"**Route** : {methods} {ep.route_pattern}")
            else:
                lines.append(f"## Méthode : {ep.name}()")

            if ep.risk_score is not None and ep.risk_score > 0:
                badge = "🔴" if ep.critical_risk else ("🟡" if ep.risk_score > 40 else "🟢")
                lines.append(f"**Risque : {badge} {ep.risk_score}/100**")
                if ep.risk_details:
                    d = ep.risk_details
                    cyclo, coupling, magic, l, raw = (
                        d.get('cyclomatic_complexity', 0),
                        d.get('strong_coupling', 0),
                        d.get('magic_values', 0),
                        d.get('method_lines', 0),
                        d.get('raw_score', 0),
                    )
                    lines.append("")
                    lines.append("| Facteur | Valeur | Poids |")
                    lines.append("|---------|--------|-------|")
                    lines.append(f"| Complexité cyclomatique | {cyclo} | ×2 = {cyclo * 2} |")
                    lines.append(f"| Couplage fort (→app→get) | {coupling} | ×5 = {coupling * 5} |")
                    lines.append(f"| Valeurs magiques | {magic} | ×3 = {magic * 3} |")
                    lines.append(f"| Longueur ({l} lignes) | {l // 50} tranches | ×1 = {l // 50} |")
                    lines.append(f"| **Score brut** | | **{raw}** |")
                    lines.append(f"| **Score normalisé** | | **{ep.risk_score}/100** {badge} |")
            lines.append("")

            ep_flags = flags_by_location.get(ep.name, [])
            security_flags = [f for f in ep_flags if f.type == "security_risk"]
            business_flags = [f for f in ep_flags if f.type == "business_logic_unclear"]

            # --- Points d'attention ---
            if security_flags:
                lines.append("### Points d'attention")
                for flag in security_flags:
                    business_label = _translate_fragment(flag.fragment)
                    insight = insights_by_flag.get(flag.id)
                    if insight:
                        conf_pct = f"{insight.confidence:.0%}"
                        lines.append(f"- 🔴 **{business_label}** *(confiance {conf_pct})*")
                        lines.append(f"  - {insight.business_rule}")
                    else:
                        lines.append(f"- 🔴 **{business_label}**")
                        lines.append(f"  - {flag.question}")
                lines.append("")

            # --- Règles métier ---
            if business_flags:
                lines.append("### Règles métier")
                for flag in business_flags:
                    insight = insights_by_flag.get(flag.id)
                    if insight:
                        conf_pct = f"{insight.confidence:.0%}"
                        lines.append(f"- ✅ *(confiance {conf_pct})* {insight.business_rule}")
                    else:
                        lines.append(f"- ❓ {flag.question}")
                lines.append("")

            # --- Questions ouvertes pour arbitrage ---
            to_validate = _build_validation_list(ep_flags, insights_by_flag)
            if to_validate:
                lines.append("### Questions ouvertes pour arbitrage")
                for item in to_validate:
                    lines.append(f"- [ ] {item}")
                lines.append("")

            lines.append("---")
            lines.append("")

        # =====================================================================
        # Sections globales
        # =====================================================================

        # Flux de contrôle (conditions, branches manquantes, valeurs magiques)
        cf_flags = [
            f for f in ir.flags
            if f.type in ("missing_branch", "magic_value")
            and f.location.startswith("block_")
        ]
        if cf_flags:
            lines.append("## Points de décision — Comportements non définis")
            seen_cf: set[tuple] = set()
            for flag in cf_flags:
                key = (flag.type, flag.fragment.strip())
                if key in seen_cf:
                    continue
                seen_cf.add(key)
                insight = insights_by_flag.get(flag.id)
                type_label = "Gap de logique" if flag.type == "missing_branch" else "Valeur de référence"
                lines.append(f"- ⚠️ **{type_label}**")
                lines.append(f"  - {flag.question}")
                if insight:
                    conf_pct = f"{insight.confidence:.0%}"
                    lines.append(f"  - *(confiance {conf_pct})* {insight.business_rule}")
            lines.append("")

        # Volumes non bornés
        pagination_flags = [
            f for f in ir.flags
            if f.type == "business_logic_unclear" and f.location.startswith("op_")
        ]
        if pagination_flags:
            lines.append("## Volumes non bornés — Règle de limitation à préciser")
            for flag in pagination_flags:
                insight = insights_by_flag.get(flag.id)
                business_label = _translate_fragment(flag.fragment)
                lines.append(f"- ⚠️ **{business_label}**")
                lines.append(f"  - {flag.question}")
                if insight:
                    conf_pct = f"{insight.confidence:.0%}"
                    lines.append(f"  - *(confiance {conf_pct})* {insight.business_rule}")
            lines.append("")

        # Services tiers non documentés
        dep_flags = [f for f in ir.flags if f.type == "unmapped_dep"]
        if dep_flags:
            lines.append("## Services tiers non documentés")
            for flag in dep_flags:
                insight = insights_by_flag.get(flag.id)
                lines.append(f"- ❓ **{flag.location}** — {flag.question}")
                if insight:
                    conf_pct = f"{insight.confidence:.0%}"
                    lines.append(f"  - *(confiance {conf_pct})* {insight.business_rule}")
            lines.append("")

        lines.append("---")
        lines.append("**Légende :** ✅ Règle confirmée | 🔴 Point d'attention | ⚠️ Gap à arbitrer | ❓ Service à documenter")
        lines.append("")

        if usage is not None:
            lines.append(_generate_footer(usage, model))

        return "\n".join(lines)

    def generate_flags_summary(self, ir: IRSchema) -> str:
        """Liste focalisée de tous les flags en attente de validation humaine."""
        lines: list[str] = []

        controller = ir.metadata.controller_name
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        lines.append(f"# {controller}Controller — Zones à valider")
        bug_count = len(ir.bug_findings)
        bug_suffix = f" | {bug_count} bug(s) techniques" if bug_count else ""
        lines.append(f"Généré le : {now} | {len(ir.flags)} flags | {len(ir.llm_insights)} insights LLM{bug_suffix}")
        lines.append("")

        insights_by_flag = {ins.flag_id: ins for ins in ir.llm_insights}

        # Grouper par type pour faciliter la lecture
        groups = {
            "security_risk":         ("🔴 Points d'attention sécurité", []),
            "dynamic_session_key":   ("🔑 Session dynamique — risque stale", []),
            "chained_api_call":         ("🔗 Appels API chaînés — risque payload vide", []),
            "situation_coverage":       ("🎯 Situation non couverte — comportement indéfini", []),
            "oceane_state_dependency":  ("🌊 Dépendance Oceane temps réel — pas de fallback", []),
            "module_execution_gap":     ("⚙️  Module séquentiel — échec silencieux possible", []),
            "hardcoded_situation_code": ("🔢 Code situation hardcodé — risque désynchronisation", []),
            "empty_catch":              ("🕳️ Exception ignorée — erreur silencieuse", []),
            "strong_coupling":          ("🔧 Couplage fort — méthode non testable", []),
            "chained_method_call":      ("⛓️ Appel chaîné — risque null pointer", []),
            "missing_branch":           ("⚠️ Gaps de logique — Comportements non définis", []),
            "magic_value":           ("🔍 Valeurs de référence non documentées", []),
            "business_logic_unclear": ("❓ Règles métier à préciser", []),
            "unmapped_dep":          ("📦 Services tiers non documentés", []),
        }

        for flag in ir.flags:
            if flag.type in groups:
                groups[flag.type][1].append(flag)

        for flag_type, (section_title, flags) in groups.items():
            if not flags:
                continue
            lines.append(f"## {section_title}")
            for flag in flags:
                insight = insights_by_flag.get(flag.id)
                status = "✅ enrichi" if insight else "⬜ non enrichi"
                validated = " ✔ validé" if (insight and insight.validated) else ""
                lines.append(f"- [ ] **[{flag.location}]** {status}{validated}")
                lines.append(f"  - Fragment : `{flag.fragment[:100]}`")
                lines.append(f"  - Question : {flag.question}")
                if insight:
                    lines.append(
                        f"  - Règle LLM ({insight.confidence:.0%}) : {insight.business_rule}"
                    )
                    if insight.missing_context:
                        lines.append(f"  - ❓ Contexte manquant : {insight.missing_context}")
            lines.append("")

        # Section bugs techniques (si --bug-check a été lancé)
        if ir.bug_findings:
            lines.append(format_bug_findings_md(ir.bug_findings))

        return "\n".join(lines)


# =============================================================================
# Helpers
# =============================================================================

def _generate_footer(usage: TokenUsage, model: str) -> str:
    pricing = PRICING.get(model, PRICING["claude-sonnet-4-6"])
    input_cost, output_cost, cache_economy = usage.costs(model)
    total_cost = input_cost + output_cost
    cache_saved_cost = (usage.cache_read_tokens / 1_000_000) * pricing["input"] * 0.9
    cache_active = usage.cache_read_tokens > 0

    lines = [
        "## Rapport de consommation",
        "",
        "| Métrique | Valeur |",
        "|----------|--------|",
        f"| Flags enrichis par LLM | {usage.enriched_flags} |",
        f"| Flags skippés (fragment minimal) | {usage.skipped_flags} |",
        f"| Tokens input | {usage.input_tokens:,} |",
        f"| Tokens output | {usage.output_tokens:,} |",
        f"| Tokens écrits en cache | {usage.cache_creation_tokens:,} |",
        f"| Tokens lus depuis cache | {usage.cache_read_tokens:,} |",
        f"| **Coût estimé** | **${total_cost:.4f}** |",
        f"| **Économie cache** | **${cache_saved_cost:.4f}** |",
        "",
        f"*Modèle : {model or 'inconnu'} "
        f"| Input ${pricing['input']:.2f}/1M · Output ${pricing['output']:.2f}/1M"
        f" | Cache actif : {'oui' if cache_active else 'non — system prompt < 1024 tokens ?'}*",
        "",
    ]
    return "\n".join(lines)


def _first_sentence(text: str, max_len: int = 80) -> str:
    """Première question du texte, tronquée à max_len."""
    idx = text.find('?')
    if idx != -1:
        q = text[:idx + 1].strip()
        return q if len(q) <= max_len else q[:max_len - 3] + '...'
    return text[:max_len].strip()


def _translate_fragment(fragment: str) -> str:
    """Traduit un fragment technique en terme métier lisible par un PO."""
    for pattern_str, replacement in TECH_TO_BUSINESS:
        try:
            result = re.sub(pattern_str, replacement, fragment, flags=re.IGNORECASE)
            if result != fragment:
                return _clean_translated(result)
        except re.error:
            continue
    # Fallback : nettoyer les artefacts PHP les plus visibles
    clean = re.sub(r'\$_POST\s*\[', 'saisie[', fragment)
    clean = re.sub(r'\$_SESSION\s*\[', 'session[', clean)
    clean = re.sub(r'\$(\w+)', r'\1', clean)
    return _clean_translated(clean)


def _clean_translated(text: str) -> str:
    """Retire les artefacts d'affectation PHP autour d'une traduction."""
    # Retirer les préfixes d'affectation : $var = ... ; → ...
    text = re.sub(r'^\$\w+\s*=\s*', '', text.strip())
    # Retirer les suffixes techniques (;, ,, {, })
    text = text.rstrip(' ;,{').strip()
    # Retirer les résidus de variable non traduits en début
    text = re.sub(r'^\$\w+\s*', '', text)
    return text.strip()


def _build_validation_list(
    ep_flags: list[Flag],
    insights_by_flag: dict[str, LLMInsight],
) -> list[str]:
    """Retourne des cases à cocher courtes : location.field : question courte."""
    items: list[str] = []
    seen: set[str] = set()
    for flag in ep_flags:
        key = flag.fragment.strip()
        if key in seen:
            continue
        seen.add(key)
        field, question = _field_and_question(flag)
        items.append(f"{flag.location}.{field} : {question}")
    return items


def _field_and_question(flag: Flag) -> tuple[str, str]:
    """Dérive un nom de champ court et une question actionnable depuis un flag."""
    frag = flag.fragment

    if flag.type == "dynamic_session_key":
        return 'session_key', "cette clé est-elle nettoyée dans tous les chemins de sortie ?"
    if flag.type == "chained_api_call":
        return 'api_chain', "le résultat intermédiaire est-il validé avant le second appel ?"

    # business_logic_unclear en premier : le fragment peut contenir md5/etc. sans que ce soit l'enjeu
    if flag.type == "business_logic_unclear":
        if re.search(r'->insert\s*\(', frag) and re.search(r'Zend_Mail|\$mail|->send', frag):
            return 'mail_sync', "comportement si l'envoi échoue ?"
        q = flag.question
        if 'email' in q or 'mail' in q.lower():
            return 'mail_sync', "comportement si l'envoi échoue ?"
        if 'SELECT' in frag.upper():
            return 'select_all', "volume borné ou pagination nécessaire ?"

    # $_POST['field'] → field, règle de validation ?
    m = re.search(r"\$_POST\s*\[\s*'(\w+)'", frag)
    if m:
        return m.group(1), "une règle de validation est-elle définie pour cette donnée ?"

    # md5(
    if re.search(r'\bmd5\s*\(', frag):
        return 'md5', "cette méthode de protection est-elle une contrainte documentée ?"

    # DELETE + SQL concat → effets sur données liées ?
    if re.search(r'->delete\s*\(', frag):
        return 'delete', "la suppression entraîne-t-elle des effets sur les données liées ?"

    # SQL concat "id = " . ou 'id = ' .
    if re.search(r"""['"]id\s*=\s*['"]\s*\.""", frag):
        return 'recherche_id', "la protection de cette recherche est-elle conforme aux standards prévus ?"

    # $_SESSION
    if '$_SESSION' in frag:
        return 'session', "l'habilitation est-elle vérifiée par un service centralisé ?"

    # Fallback : premier $var du fragment
    m = re.search(r'\$(\w+)', frag)
    field = m.group(1) if m else 'check'
    return field, _first_sentence(flag.question)
