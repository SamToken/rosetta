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
from ir.schema import IRSchema, Flag, LLMInsight
from analyzers.llm_enricher import TokenUsage, PRICING


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
            methods = "/".join(ep.http_methods)
            lines.append(f"## Action : {ep.name}")
            lines.append(f"**Route** : {methods} {ep.route_pattern}")
            lines.append("")

            ep_flags = flags_by_location.get(ep.name, [])
            security_flags = [f for f in ep_flags if f.type == "security_risk"]
            business_flags = [f for f in ep_flags if f.type == "business_logic_unclear"]

            # --- Risques identifiés (déterministe + LLM si dispo) ---
            if security_flags:
                lines.append("### Risques identifiés")
                for flag in security_flags:
                    lines.append(f"- 🔴 [déterministe] `{flag.fragment}`")
                    insight = insights_by_flag.get(flag.id)
                    if insight:
                        label = _insight_label(insight)
                        lines.append(f"  - {label} {insight.business_rule}")
                lines.append("")

            # --- Règles métier (LLM ou non enrichi) ---
            if business_flags:
                lines.append("### Règles métier")
                for flag in business_flags:
                    insight = insights_by_flag.get(flag.id)
                    if insight:
                        label = _insight_label(insight)
                        lines.append(f"- {label} {insight.business_rule}")
                    else:
                        lines.append(f"- ❓ [non enrichi] {flag.question}")
                lines.append("")

            # --- À valider par un humain ---
            to_validate = _build_validation_list(ep_flags, insights_by_flag)
            if to_validate:
                lines.append("### À valider par un humain")
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
            lines.append("## Flux de contrôle — Zones ambiguës")
            seen_cf: set[tuple] = set()
            for flag in cf_flags:
                key = (flag.type, flag.fragment.strip())
                if key in seen_cf:
                    continue
                seen_cf.add(key)
                insight = insights_by_flag.get(flag.id)
                type_label = "branche manquante" if flag.type == "missing_branch" else "valeur magique"
                lines.append(f"- ⚠️ [{type_label}] `{flag.fragment}`")
                lines.append(f"  - {flag.question}")
                if insight:
                    label = _insight_label(insight)
                    lines.append(f"  - {label} {insight.business_rule}")
            lines.append("")

        # Opérations DB avec pagination manquante
        pagination_flags = [
            f for f in ir.flags
            if f.type == "business_logic_unclear" and f.location.startswith("op_")
        ]
        if pagination_flags:
            lines.append("## Requêtes DB — Volume non maîtrisé")
            for flag in pagination_flags:
                insight = insights_by_flag.get(flag.id)
                lines.append(f"- ⚠️ `{flag.fragment}`")
                lines.append(f"  - {flag.question}")
                if insight:
                    label = _insight_label(insight)
                    lines.append(f"  - {label} {insight.business_rule}")
            lines.append("")

        # Dépendances non mappées
        dep_flags = [f for f in ir.flags if f.type == "unmapped_dep"]
        if dep_flags:
            lines.append("## Dépendances non mappées")
            for flag in dep_flags:
                insight = insights_by_flag.get(flag.id)
                lines.append(f"- ❓ `{flag.location}` — {flag.question}")
                if insight:
                    label = _insight_label(insight)
                    lines.append(f"  - {label} {insight.business_rule}")
            lines.append("")

        lines.append("---")
        lines.append("**Légende :** ✅ Déterministe (confiance 1.0) | 🤖 LLM (confiance variable) | 🔴 Risque sécurité | ❓ Non enrichi")
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
        lines.append(f"Généré le : {now} | {len(ir.flags)} flags | {len(ir.llm_insights)} insights LLM")
        lines.append("")

        insights_by_flag = {ins.flag_id: ins for ins in ir.llm_insights}

        # Grouper par type pour faciliter la lecture
        groups = {
            "security_risk": ("🔴 Risques sécurité", []),
            "missing_branch": ("⚠️ Branches manquantes", []),
            "magic_value": ("🔍 Valeurs magiques", []),
            "business_logic_unclear": ("❓ Logique métier ambiguë", []),
            "unmapped_dep": ("📦 Dépendances non mappées", []),
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
            lines.append("")

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


def _insight_label(insight: LLMInsight) -> str:
    status = "validé" if insight.validated else "non validé"
    return f"🤖 [LLM - {insight.confidence:.2f} - {status}]"


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

    # business_logic_unclear en premier : le fragment peut contenir md5/etc. sans que ce soit l'enjeu
    if flag.type == "business_logic_unclear":
        if re.search(r'->insert\s*\(', frag) and re.search(r'Zend_Mail|\$mail|->send', frag):
            return 'mail_sync', "comportement si l'envoi échoue ?"
        q = flag.question
        if 'email' in q or 'mail' in q.lower():
            return 'mail_sync', "comportement si l'envoi échoue ?"
        if 'SELECT' in frag.upper():
            return 'select_all', "volume borné ou pagination nécessaire ?"

    # $_POST['field'] → field, validation en aval ?
    m = re.search(r"\$_POST\s*\[\s*'(\w+)'", frag)
    if m:
        return m.group(1), "validation ou sanitisation en aval ?"

    # md5(
    if re.search(r'\bmd5\s*\(', frag):
        return 'md5', "contrainte legacy documentée ou migration bcrypt prévue ?"

    # DELETE + SQL concat → cascade ?
    if re.search(r'->delete\s*\(', frag):
        return 'delete', "cascade sur clés étrangères ?"

    # SQL concat "id = " . ou 'id = ' .
    if re.search(r"""['"]id\s*=\s*['"]\s*\.""", frag):
        return 'sql_concat', "requête préparée possible ici ?"

    # $_SESSION
    if '$_SESSION' in frag:
        return 'session', "accès via un service d'authentification possible ?"

    # Fallback : premier $var du fragment
    m = re.search(r'\$(\w+)', frag)
    field = m.group(1) if m else 'check'
    return field, _first_sentence(flag.question)
