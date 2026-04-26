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

import re
from datetime import datetime
from typing import Optional
from aggregators.business_aggregator import AggregatedInsights, DecisionGap
from analyzers.llm_enricher import TokenUsage, PRICING

_TECHNICAL_NOISE = [r'\$_POST', r'\bmd5\b', r'SELECT\s*\*']
_PRIORITY_KEYWORDS = ("oceane", "adelia", "oceaneassistant")

# Correction 2 — traduction des termes techniques → langage PO
# L'ordre compte : les patterns combinés avant les patterns simples
_PO_CONDITION_TRANSLATIONS = [
    # Combinés d'abord
    (r"is_array\('([^']+)'\)\s*et\s*count\('[^']+'\)\s*>\s*0",
     r"plusieurs '\1' existent"),
    (r"gettype\('[^']+'\)\s*différent de\s*['\"]boolean['\"]",
     "la valeur reçue est invalide"),
    # is_null / null — conserver le nom de l'entité
    (r"is_null\('([^']+)'\)",
     r"l'information '\1' est absente"),
    (r"'([^']+)'\s*égal à null",
     r"l'information '\1' est absente"),
    (r"'([^']+)'\s*différent de null",
     r"l'information '\1' est présente"),
    # is_array / count — conserver le nom de l'entité
    (r"is_array\('([^']+)'\)",
     r"plusieurs '\1' sont présents"),
    (r"count\('([^']+)'\)\s*>\s*0",
     r"des '\1' existent"),
    (r"count\('([^']+)'\)",
     r"le nombre de '\1'"),
    (r"key_exists\('(\w+)',\s*'[^']+'\)",
     r"l'information '\1' est disponible"),
    (r"property_exists\('[^']+',\s*'(\w+)'\)",
     r"l'objet contient '\1'"),
    (r"isset\('([^']+)'\)",
     r"'\1' est défini"),
    (r"!([A-Z][a-zA-Z0-9]+)::[a-zA-Z]+\([^)]*\)",
     r"le service \1 ne répond pas"),
    (r"([A-Z][a-zA-Z0-9]+)::[a-zA-Z]+\([^)]*\)",
     r"le service \1 répond"),
    (r"!'([^']+)'->[a-zA-Z]+\([^)]*\)",
     r"le service \1 ne répond pas"),
    (r"'([^']+)'->[a-zA-Z]+\([^)]*\)",
     r"le service \1 répond"),
    (r"strpos\([^)]+\)\s*!==\s*false", "la valeur est trouvée"),
    (r"strpos\([^)]+\)\s*===\s*false", "la valeur n'est pas trouvée"),
    (r"intval\(([^()]+)\)", r"\1"),
    (r"strtolower\(([^()]+)\)", r"\1"),
    (r"strlen\(([^()]+)\)", r"\1"),
]


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

        lines.append("### Priorités de correction")
        lines.append("")
        lines.append("| Catégorie | Flags | Action |")
        lines.append("|-----------|-------|--------|")
        lines.append(f"| 🔴 CRITICAL_CORRUPTION | {ins.critical_count} | Corriger avant toute MEP |")
        lines.append(f"| 🟠 API_OVERLOAD | {ins.overload_count} | Corriger avant migration |")
        lines.append(f"| 🟡 LOGIC_GAP | {ins.logic_gap_count} | Arbitrage PO requis |")
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
        n = 0

        # Comptage par type pour les recommandations spécifiques Astro
        count_by_type: dict[str, int] = {}
        for f in ins.all_flags:
            count_by_type[f.flag_type] = count_by_type.get(f.flag_type, 0) + 1

        if count_by_type.get("dynamic_session_key", 0) > 0:
            n += 1
            c = count_by_type["dynamic_session_key"]
            lines.append(
                f"{n}. **🔑 {c} clé(s) de session dynamique(s)** — "
                "Vérifier le nettoyage explicite dans tous les chemins de transition "
                "de contexte (ASSEMBLEE→CABLE, EQUIPEMENT→CABLE, reclassification Océane). "
                "Risque de données périmées chargées silencieusement en production."
            )
        if count_by_type.get("chained_api_call", 0) > 0:
            n += 1
            c = count_by_type["chained_api_call"]
            lines.append(
                f"{n}. **🔗 {c} appel(s) API séquentiel(s)** — "
                "Vérifier la validation du résultat intermédiaire (!empty / null check) "
                "avant chaque appel suivant. "
                "Risque 400 Invalid request si prestation inconnue ou service indisponible."
            )
        if count_by_type.get("situation_coverage", 0) > 0:
            n += 1
            c = count_by_type["situation_coverage"]
            lines.append(
                f"{n}. **🎯 {c} situation(s) Oracle sans couverture exhaustive** — "
                "Vérifier que chaque branche `if ($situation === ...)` dispose d'un `else` "
                "documentant le comportement par défaut. "
                "Risque de comportement indéfini si Oracle introduit un nouveau code situation."
            )
        if count_by_type.get("oceane_state_dependency", 0) > 0:
            n += 1
            c = count_by_type["oceane_state_dependency"]
            lines.append(
                f"{n}. **🌊 {c} lecture(s) d'état Oceane sans fallback** — "
                "Vérifier que chaque appel Oceane (getStatutEquipement, getEtatAbonnement…) "
                "est protégé par un fallback explicite en cas de timeout ou de réponse vide. "
                "Risque de null pointer ou de prise de décision sur donnée absente."
            )
        if count_by_type.get("module_execution_gap", 0) > 0:
            n += 1
            c = count_by_type["module_execution_gap"]
            lines.append(
                f"{n}. **⚙️ {c} enchaînement(s) de modules sans vérification d'échec** — "
                "Vérifier que chaque module séquentiel (execute, run, process…) vérifie "
                "le retour du précédent avant d'appeler le suivant. "
                "Risque d'échec silencieux propagé jusqu'en bout de chaîne."
            )
        if count_by_type.get("hardcoded_situation_code", 0) > 0:
            n += 1
            c = count_by_type["hardcoded_situation_code"]
            lines.append(
                f"{n}. **🔢 {c} code(s) situation hardcodé(s)** — "
                "Remplacer les constantes littérales (ex : 'H1', 'TP2') par des constantes "
                "nommées référencées depuis le référentiel Oracle. "
                "Risque de désynchronisation si Oracle modifie la codification."
            )
        if ins.gap_count > 0:
            n += 1
            lines.append(
                f"{n}. **Arbitrage requis sur {ins.gap_count} gap(s) de logique** — "
                "Les comportements non définis identifiés dans la section 3 doivent être "
                "clarifiés par le Product Owner avant tout développement dans la cible."
            )
        if ins.risk_count > 0:
            n += 1
            lines.append(
                f"{n}. **{ins.risk_count} point(s) d'attention sécurité** — "
                "Les pratiques de protection des données identifiées nécessitent une "
                "décision sur la politique de sécurité applicable dans la nouvelle architecture."
            )
        if ins.duplicate_rules:
            n += 1
            lines.append(
                f"{n}. **{len(ins.duplicate_rules)} règle(s) transverse(s) détectée(s)** — "
                "Ces règles, présentes dans plusieurs contrôleurs, sont candidates à la "
                "centralisation dans des services partagés de la cible Symfony."
            )
        if ins.dep_count > 0:
            n += 1
            lines.append(
                f"{n}. **{ins.dep_count} service(s) tiers non documenté(s)** — "
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
    # 3. Décisions requises avant migration (vue PO — top 5 par contrôleur)
    # =========================================================================

    def _section_decision_gaps(self, ins: AggregatedInsights) -> list[str]:
        lines = ["## 3. Décisions requises avant migration", ""]

        pool = ins.all_flags if ins.all_flags else ins.decision_gaps
        if not pool:
            lines.append("*Aucun flag identifié sur ce périmètre.*")
            lines.append("")
            lines.append("---")
            lines.append("")
            return lines

        # Grouper par catégorie
        flags_by_cat: dict[str, list[DecisionGap]] = {}
        for f in pool:
            flags_by_cat.setdefault(f.impact_category, []).append(f)

        critical = flags_by_cat.get("CRITICAL_CORRUPTION", [])
        overload = flags_by_cat.get("API_OVERLOAD", [])
        logic = flags_by_cat.get("LOGIC_GAP", [])

        # ── 🔴 CRITICAL_CORRUPTION ─────────────────────────────────────────
        if critical:
            lines.append(f"### 🔴 CRITICAL_CORRUPTION — {len(critical)} flag(s)")
            lines.append(
                "> Corriger avant toute MEP. "
                "Ces comportements peuvent corrompre silencieusement les données en production."
            )
            lines.append("")
            lines.append("| Contrôleur | Méthode | Ligne | Question |")
            lines.append("|-----------|---------|-------|---------|")
            for f in critical:
                method_col = f"`{f.method_name}()`" if f.method_name and f.method_name != "unknown" else "—"
                line_col = str(f.source_line) if f.source_line else "—"
                q = f.condition_business.replace("\n", " ").strip()
                q = q[:100] + "…" if len(q) > 100 else q
                lines.append(f"| {f.controller} | {method_col} | {line_col} | {q} |")
            lines.append("")
            lines.append("---")
            lines.append("")

        # ── 🟠 API_OVERLOAD ────────────────────────────────────────────────
        if overload:
            lines.append(f"### 🟠 API_OVERLOAD — {len(overload)} flag(s)")
            lines.append("> Risque de surcharge ou d'erreur API silencieuse.")
            lines.append("")
            lines.append("| Contrôleur | Méthode | Ligne | Question |")
            lines.append("|-----------|---------|-------|---------|")
            for f in overload:
                method_col = f"`{f.method_name}()`" if f.method_name and f.method_name != "unknown" else "—"
                line_col = str(f.source_line) if f.source_line else "—"
                q = f.condition_business.replace("\n", " ").strip()
                q = q[:100] + "…" if len(q) > 100 else q
                lines.append(f"| {f.controller} | {method_col} | {line_col} | {q} |")
            lines.append("")
            lines.append("---")
            lines.append("")

        # ── 🟡 LOGIC_GAP ───────────────────────────────────────────────────
        lines.append(f"### 🟡 LOGIC_GAP — {len(logic)} flag(s)")
        lines.append("> Arbitrage PO requis avant migration.")
        lines.append("")
        lines.append(
            f"*(Voir `details/gaps_complets.md` pour la liste exhaustive "
            f"des {ins.gap_count} comportement(s) à définir)*"
        )
        lines.append("")
        lines.append("---")
        lines.append("")
        return lines

    @staticmethod
    def _gap_priority(gap: DecisionGap) -> tuple:
        text = (gap.condition_fragment + " " + gap.condition_business).lower()
        return (
            0 if gap.confidence > 0.6 else 1,
            0 if gap.flag_type == "business_logic_unclear" else 1,
            0 if any(kw in text for kw in _PRIORITY_KEYWORDS) else 1,
            0 if gap.flag_type == "magic_value" else 1,
        )

    @staticmethod
    def _is_technical_noise(gap: DecisionGap) -> bool:
        text = gap.condition_fragment + " " + gap.condition_business
        return any(re.search(p, text, re.IGNORECASE) for p in _TECHNICAL_NOISE)

    @staticmethod
    def _po_translate_question(question: str) -> str:
        """Traduit la condition technique d'un 'Point de décision' en langage PO."""
        prefix = "Point de décision — "
        if not question.startswith(prefix):
            return question
        rest = question[len(prefix):]
        suffix = "Quel est le comportement attendu dans le cas contraire ?"
        if suffix in rest:
            condition = rest[:rest.index(suffix)].rstrip(". ")
            tail = " " + suffix
        else:
            condition = rest
            tail = ""
        for pattern, replacement in _PO_CONDITION_TRANSLATIONS:
            condition = re.sub(pattern, replacement, condition, flags=re.IGNORECASE)
        condition = condition.strip().rstrip(".")
        return f"{prefix}{condition}.{tail}" if tail else f"{prefix}{condition}"

    @staticmethod
    def _truncate_sentence(text: str, limit: int) -> str:
        """Tronque au dernier '?' ou '.' avant la limite, sinon coupe net."""
        if len(text) <= limit:
            return text
        # Chercher le dernier terminateur de phrase dans la fenêtre
        window = text[:limit]
        for sep in ("?", "."):
            pos = window.rfind(sep)
            if pos > limit // 2:
                return text[:pos + 1]
        return window.rstrip() + "…"

    def _select_top5(self, flags: list[DecisionGap]) -> list[tuple[DecisionGap, int]]:
        """Retourne jusqu'à 5 gaps dédupliqués, triés par priorité, avec comptage."""
        filtered = [f for f in flags if not self._is_technical_noise(f)]
        if not filtered:
            filtered = flags
        filtered.sort(key=self._gap_priority)
        # Déduplication par texte normalisé, en conservant le compte
        from collections import Counter
        counts: Counter = Counter(f.condition_business.strip()[:120] for f in filtered)
        seen: set[str] = set()
        result: list[tuple[DecisionGap, int]] = []
        for gap in filtered:
            key = gap.condition_business.strip()[:120]
            if key not in seen:
                seen.add(key)
                result.append((gap, counts[key]))
                if len(result) >= 5:
                    break
        return result

    # =========================================================================
    # gaps_complets.md — liste exhaustive (vue dev)
    # =========================================================================

    def generate_gaps_detail(self, ins: AggregatedInsights) -> str:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        lines = [
            "# Gaps de Documentation — Liste Exhaustive",
            "",
            f"*Généré le {now} — {ins.gap_count} comportement(s) à définir "
            f"sur {len(ins.controllers)} contrôleur(s)*",
            "",
            "> Chaque ligne correspond à un comportement du système actuel dont "
            "le cas contraire n'est pas documenté.",
            "",
            "| # | Contrôleur | Méthode | Ligne | Question métier | Contexte | Statut |",
            "|---|-----------|---------|-------|----------------|----------|--------|",
        ]
        for i, gap in enumerate(ins.decision_gaps, 1):
            question = gap.condition_business.replace("\n", " ").strip()
            if len(question) > 120:
                question = question[:117] + "…"
            line_col = f"L.{gap.source_line}" if gap.source_line else "—"
            method_col = f"`{gap.method_name}()`" if gap.method_name and gap.method_name != "unknown" else "—"
            has_ctx = "[voir bloc]" if gap.source_line and gap.context_lines else "—"
            lines.append(
                f"| {i} | {gap.controller} | {method_col} | {line_col} | {question} | {has_ctx} | ⬜ |"
            )
        lines.append("")
        lines.append(
            f"*{ins.gap_count} gap(s) — chaque case ⬜ représente "
            "une décision à prendre avant migration.*"
        )
        lines.append("")

        # Blocs Copilot — un par gap ayant un contexte de code
        copilot_blocks = [(i, g) for i, g in enumerate(ins.decision_gaps, 1)
                          if g.source_line and g.context_lines]
        if copilot_blocks:
            lines.append("---")
            lines.append("")
            lines.append("## Contexte Code — Copier dans Copilot")
            lines.append("")
            for i, gap in copilot_blocks:
                question = gap.condition_business.replace("\n", " ").strip()
                method_display = (
                    f"{gap.method_name}() — ligne {gap.source_line}"
                    if gap.method_name and gap.method_name != "unknown"
                    else f"ligne {gap.source_line}"
                )
                lines.append("---")
                lines.append("")
                lines.append(f"**Gap #{i} — {gap.controller}**")
                lines.append("")
                lines.append("**→ Copier dans Copilot**")
                lines.append("")
                lines.append(f"Fichier    : {gap.source_file}")
                lines.append(f"Méthode    : {method_display}")
                lines.append("Contexte   :")
                lines.append("```php")
                lines.append(gap.context_lines)
                lines.append("```")
                lines.append("")
                lines.append(f"Question métier : {question}")
                lines.append("")

        return "\n".join(lines)

    # =========================================================================
    # 4. Cartographie du Domaine
    # =========================================================================

    def _section_domain_mapping(self, ins: AggregatedInsights) -> list[str]:
        lines = ["## 4. Cartographie du Domaine", ""]

        # 4.1 Termes métier non documentés (constantes, variables business)
        lines.append("### 4.1 Termes Métier non documentés")
        lines.append("")
        if not ins.magic_glossary:
            lines.append("*Aucun terme métier transverse identifié sur ce périmètre.*")
        else:
            lines.append(
                "Ces termes apparaissent dans la logique conditionnelle de plusieurs contrôleurs. "
                "Chacun doit être défini dans le référentiel métier de la cible."
            )
            lines.append("")
            lines.append("| Terme | Contrôleurs | Signification probable |")
            lines.append("|-------|------------|----------------------|")
            for entry in ins.magic_glossary:
                controllers_str = ", ".join(entry.controllers)
                lines.append(f"| `{entry.field_name}` | {controllers_str} | ❓ À documenter |")
        lines.append("")

        # 4.2 Champs de données partagés (POST fields + SQL)
        lines.append("### 4.2 Champs de données partagés")
        lines.append("")
        if not ins.glossary:
            lines.append("*Aucun champ partagé extrait sur ce périmètre.*")
        else:
            lines.append(
                "Ces champs de saisie et colonnes de données sont utilisés dans plusieurs contrôleurs. "
                "Leur définition doit être stable et partagée dans la cible."
            )
            lines.append("")
            lines.append("| Champ | Contrôleurs | Occurrences |")
            lines.append("|------|------------|-------------|")
            for entry in ins.glossary:
                controllers_str = ", ".join(entry.controllers)
                marker = " ⚠️" if entry.count > 1 else ""
                lines.append(f"| `{entry.field_name}` | {controllers_str} | {entry.count}{marker} |")
        lines.append("")

        # 4.3 Services tiers
        lines.append("### 4.3 Services Tiers Identifiés")
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
