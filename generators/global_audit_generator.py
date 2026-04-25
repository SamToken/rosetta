"""
Global Audit Generator — Rapport d'audit fonctionnel global
============================================================
Produit un fichier global_audit.md lisible par un Product Owner,
à partir d'un AggregatedInsights couvrant l'ensemble du périmètre.

Structure du livrable :
  1. Résumé Exécutif
  2. Règles Transverses & Redondances
  3. Gaps de Documentation (CRITIQUE)
  4. Cartographie du Domaine
     4.1 Glossaire Métier Unifié
     4.2 Services Tiers Identifiés
"""

from datetime import datetime
from typing import Optional
from aggregators.business_aggregator import AggregatedInsights
from analyzers.llm_enricher import TokenUsage, PRICING


class GlobalAuditGenerator:
    """Génère le rapport d'audit global lisible par un Product Owner."""

    def generate(
        self,
        insights: AggregatedInsights,
        model: str = "",
    ) -> str:
        lines: list[str] = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        lines.append("# Rapport d'Audit Fonctionnel Global")
        lines.append(f"Généré le : {now} | {len(insights.controllers)} contrôleur(s) analysé(s)")
        lines.append("")
        lines.append(
            "> Ce document est destiné au Product Owner. "
            "Il synthétise les règles métier identifiées, les comportements non définis "
            "et les questions nécessitant un arbitrage avant migration."
        )
        lines.append("")

        lines.extend(self._section_executive_summary(insights))
        lines.extend(self._section_transverse_rules(insights))
        lines.extend(self._section_decision_gaps(insights))
        lines.extend(self._section_domain_mapping(insights))

        if insights.total_usage and model:
            lines.extend(self._section_cost_report(insights.total_usage, model, insights))

        return "\n".join(lines)

    # =========================================================================
    # 1. Résumé Exécutif
    # =========================================================================

    def _section_executive_summary(self, ins: AggregatedInsights) -> list[str]:
        lines = ["## 1. Résumé Exécutif", ""]

        # Jauge de santé
        score = ins.health_score
        if score >= 80:
            health_label, health_icon = "Bon", "🟢"
        elif score >= 55:
            health_label, health_icon = "Dégradé", "🟡"
        else:
            health_label, health_icon = "Critique", "🔴"

        lines.append(f"### Santé fonctionnelle globale : {health_icon} {health_label} ({score}/100)")
        lines.append("")
        lines.append("| Indicateur | Valeur |")
        lines.append("|-----------|--------|")
        lines.append(f"| Contrôleurs analysés | {len(ins.controllers)} |")
        lines.append(f"| Actions/fonctionnalités | {ins.total_actions} |")
        lines.append(f"| Points d'attention sécurité | {ins.risk_count} |")
        lines.append(f"| Gaps de logique à arbitrer | {ins.gap_count} |")
        lines.append(f"| Services tiers non documentés | {ins.dep_count} |")
        lines.append(f"| Règles métier identifiées | {ins.total_insights} |")
        lines.append("")

        # Périmètre analysé
        lines.append("### Périmètre analysé")
        lines.append("")
        lines.append("| Contrôleur | Actions | Points d'attention | Gaps | Score |")
        lines.append("|-----------|---------|-------------------|------|-------|")
        for s in ins.controller_summaries:
            badge = "🔴" if s.health_score < 55 else ("🟡" if s.health_score < 80 else "🟢")
            lines.append(
                f"| {s.controller_name} | {s.actions} | {s.risk_count} | {s.gap_count} | {badge} {s.health_score}/100 |"
            )
        lines.append("")

        # Recommandations prioritaires
        lines.append("### Recommandations prioritaires")
        lines.append("")
        if ins.gap_count > 0:
            lines.append(
                f"1. **Arbitrage requis sur {ins.gap_count} gap(s) de logique** — "
                "Les comportements non définis identifiés dans la section 3 doivent être "
                "clarifiés par le Product Owner avant tout développement dans la cible."
            )
        if ins.risk_count > 0:
            lines.append(
                f"2. **{ins.risk_count} point(s) d'attention sécurité** — "
                "Les pratiques de protection des données identifiées nécessitent une "
                "décision sur la politique de sécurité applicable dans la nouvelle architecture."
            )
        if ins.duplicate_rules:
            lines.append(
                f"3. **{len(ins.duplicate_rules)} règle(s) transverse(s) détectée(s)** — "
                "Ces règles, présentes dans plusieurs contrôleurs, sont candidates à la "
                "centralisation dans des services partagés de la cible Symfony."
            )
        if ins.dep_count > 0:
            lines.append(
                f"4. **{ins.dep_count} service(s) tiers non documenté(s)** — "
                "Chaque service tiers doit faire l'objet d'une fiche de spécification "
                "avant d'être intégré à la cible."
            )
        lines.append("")
        lines.append("---")
        lines.append("")
        return lines

    # =========================================================================
    # 2. Règles Transverses & Redondances
    # =========================================================================

    def _section_transverse_rules(self, ins: AggregatedInsights) -> list[str]:
        lines = ["## 2. Règles Transverses & Redondances", ""]

        if not ins.duplicate_rules:
            lines.append("*Aucune règle métier dupliquée détectée sur ce périmètre.*")
            lines.append("")
            lines.append("---")
            lines.append("")
            return lines

        lines.append(
            "Les règles suivantes sont présentes dans plusieurs contrôleurs. "
            "Elles sont candidates à la centralisation dans des services partagés."
        )
        lines.append("")
        lines.append("| Règle métier | Contrôleurs concernés | Occurrences |")
        lines.append("|-------------|----------------------|-------------|")
        for dup in ins.duplicate_rules:
            controllers_str = ", ".join(dup.controllers)
            rule_short = dup.example_rule[:100].rstrip()
            if len(dup.example_rule) > 100:
                rule_short += "…"
            lines.append(f"| {rule_short} | {controllers_str} | {dup.count} |")
        lines.append("")
        lines.append("---")
        lines.append("")
        return lines

    # =========================================================================
    # 3. Gaps de Documentation — CRITIQUE
    # =========================================================================

    def _section_decision_gaps(self, ins: AggregatedInsights) -> list[str]:
        lines = ["## 3. Gaps de Documentation — CRITIQUE", ""]

        if not ins.decision_gaps:
            lines.append("*Aucun gap de logique identifié sur ce périmètre.*")
            lines.append("")
            lines.append("---")
            lines.append("")
            return lines

        lines.append(
            "> **Ces points nécessitent un arbitrage métier avant de commencer le développement "
            "dans la cible.** Chaque ligne correspond à un comportement du système actuel dont "
            "le cas contraire n'est pas documenté."
        )
        lines.append("")
        lines.append("| # | Contrôleur | Question métier | Statut |")
        lines.append("|---|-----------|----------------|--------|")
        for i, gap in enumerate(ins.decision_gaps, 1):
            # Extraire la question lisible depuis le champ question du flag
            question = gap.condition_business.replace("\n", " ").strip()
            # Tronquer si trop long
            if len(question) > 120:
                question = question[:117] + "…"
            lines.append(f"| {i} | {gap.controller} | {question} | ⬜ À arbitrer |")
        lines.append("")
        lines.append(
            f"*{len(ins.decision_gaps)} gap(s) identifié(s) — chaque case ⬜ représente "
            "une décision à prendre avant migration.*"
        )
        lines.append("")
        lines.append("---")
        lines.append("")
        return lines

    # =========================================================================
    # 4. Cartographie du Domaine
    # =========================================================================

    def _section_domain_mapping(self, ins: AggregatedInsights) -> list[str]:
        lines = ["## 4. Cartographie du Domaine", ""]

        # 4.1 Glossaire métier unifié
        lines.append("### 4.1 Glossaire Métier Unifié")
        lines.append("")
        if not ins.glossary:
            lines.append("*Aucun terme de glossaire extrait sur ce périmètre.*")
        else:
            lines.append(
                "Les termes suivants apparaissent dans les échanges de données du système. "
                "Un même terme utilisé dans plusieurs contrôleurs doit avoir une définition "
                "stable et partagée dans la cible."
            )
            lines.append("")
            lines.append("| Terme | Contrôleurs | Occurrences |")
            lines.append("|------|------------|-------------|")
            for entry in ins.glossary:
                controllers_str = ", ".join(entry.controllers)
                marker = " ⚠️" if entry.count > 1 else ""
                lines.append(f"| `{entry.field_name}` | {controllers_str} | {entry.count}{marker} |")
        lines.append("")

        # 4.2 Services tiers
        lines.append("### 4.2 Services Tiers Identifiés")
        lines.append("")
        if not ins.common_deps:
            lines.append("*Aucun service tiers non documenté identifié.*")
        else:
            lines.append(
                "Ces composants sont utilisés dans le périmètre analysé sans équivalent "
                "identifié dans la cible. Chacun nécessite une fiche de spécification."
            )
            lines.append("")
            lines.append("| Service | Type | Contrôleurs | Priorité |")
            lines.append("|--------|------|------------|---------|")
            for dep in ins.common_deps:
                controllers_str = ", ".join(dep.controllers)
                priority = "🔴 Haute" if dep.count > 1 else "🟡 Normale"
                lines.append(f"| `{dep.name}` | {dep.dep_type} | {controllers_str} | {priority} |")
        lines.append("")
        lines.append("---")
        lines.append("")
        return lines

    # =========================================================================
    # Rapport de coût LLM
    # =========================================================================

    def _section_cost_report(self, usage: TokenUsage, model: str, insights: "AggregatedInsights" = None) -> list[str]:
        pricing = PRICING.get(model, PRICING["claude-sonnet-4-6"])
        input_cost, output_cost, cache_economy = usage.costs(model)
        total_cost = input_cost + output_cost
        cache_saved = (usage.cache_read_tokens / 1_000_000) * pricing["input"] * 0.9
        cache_active = usage.cache_read_tokens > 0

        lines = [
            "## Rapport de Consommation LLM",
            "",
            "| Métrique | Valeur |",
            "|----------|--------|",
            f"| Contrôleurs analysés | {len(insights.controllers) if insights else '—'} |",
            f"| Flags enrichis par LLM | {usage.enriched_flags} |",
            f"| Flags skippés (fragment minimal) | {usage.skipped_flags} |",
            f"| Tokens input | {usage.input_tokens:,} |",
            f"| Tokens output | {usage.output_tokens:,} |",
            f"| Tokens écrits en cache | {usage.cache_creation_tokens:,} |",
            f"| Tokens lus depuis cache | {usage.cache_read_tokens:,} |",
            f"| **Coût total estimé** | **${total_cost:.4f}** |",
            f"| **Économie cache** | **${cache_saved:.4f}** |",
            "",
            f"*Modèle : {model} | Input ${pricing['input']:.2f}/1M · Output ${pricing['output']:.2f}/1M"
            f" | Cache actif : {'oui' if cache_active else 'non'}*",
            "",
        ]
        return lines
