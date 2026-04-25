"""
Business Aggregator — Synthèse transverse de plusieurs IRSchema
===============================================================
Collecte les IRSchema de l'ensemble du périmètre analysé et en
extrait la logique transverse selon trois axes :
  1. Logiques dupliquées entre contrôleurs
  2. Glossaire unifié des champs de données
  3. Dépendances tierces communes

Produit un AggregatedInsights utilisé par GlobalAuditGenerator.
"""

import re
from dataclasses import dataclass, field
from typing import Optional
from ir.schema import IRSchema, Flag, LLMInsight
from analyzers.llm_enricher import TokenUsage

_GLOSSARY_GENERIC = frozenset({
    'data', 'result', 'this', 'value', 'type', 'key', 'label', 'val', 'id',
    'name', 'error', 'return', 'action', 'status', 'objet', 'objets', 'ok',
    'true', 'false', 'null', 'class', 'message', 'count', 'item', 'obj',
    'date', 'time', 'code', 'info', 'user', 'text', 'url', 'list', 'tab',
})


# =============================================================================
# Structures de données agrégées
# =============================================================================

@dataclass
class DuplicateRule:
    """Règle métier identique détectée dans plusieurs contrôleurs."""
    rule_key: str           # clé normalisée (premiers 60 chars)
    example_rule: str       # texte complet de l'exemple
    controllers: list[str]  # noms des contrôleurs concernés
    count: int


@dataclass
class GlossaryEntry:
    """Terme du glossaire présent dans un ou plusieurs contrôleurs."""
    field_name: str         # nom du champ ou de l'entité
    controllers: list[str]  # contrôleurs qui l'utilisent
    count: int
    contexts: list[str]     # fragments de contexte (pour le PO)


@dataclass
class CommonDependency:
    """Service tiers utilisé dans plusieurs contrôleurs."""
    name: str
    dep_type: str
    controllers: list[str]
    count: int


@dataclass
class DecisionGap:
    """Gap de logique nécessitant un arbitrage PO."""
    condition_fragment: str   # condition technique brute
    condition_business: str   # formulation métier (question du flag)
    controller: str
    location: str
    flag_type: str = "missing_branch"
    flag_id: str = ""
    confidence: float = 0.0   # confiance LLM (0 si pas d'insight)


@dataclass
class ControllerSummary:
    """Résumé santé d'un contrôleur."""
    controller_name: str
    source_file: str
    actions: int
    risk_count: int
    gap_count: int
    unmapped_deps: int
    health_score: float       # 0-100


@dataclass
class AggregatedInsights:
    """Synthèse transverse de l'ensemble du périmètre analysé."""
    controllers: list[str] = field(default_factory=list)
    total_actions: int = 0
    total_flags: int = 0
    total_insights: int = 0

    duplicate_rules: list[DuplicateRule] = field(default_factory=list)
    glossary: list[GlossaryEntry] = field(default_factory=list)
    magic_glossary: list[GlossaryEntry] = field(default_factory=list)
    common_deps: list[CommonDependency] = field(default_factory=list)
    decision_gaps: list[DecisionGap] = field(default_factory=list)  # missing_branch uniquement
    all_flags: list[DecisionGap] = field(default_factory=list)      # tous types, pour top-5 PO
    controller_summaries: list[ControllerSummary] = field(default_factory=list)

    health_score: float = 100.0    # score global 0-100
    risk_count: int = 0
    gap_count: int = 0
    dep_count: int = 0

    total_usage: Optional[TokenUsage] = None


# =============================================================================
# Agrégateur
# =============================================================================

class BusinessAggregator:
    """Synthétise un ensemble d'IRSchema en AggregatedInsights."""

    def aggregate(
        self,
        irs: list[IRSchema],
        usages: Optional[list[Optional[TokenUsage]]] = None,
    ) -> AggregatedInsights:
        result = AggregatedInsights()

        result.controllers = [ir.metadata.controller_name for ir in irs]
        result.total_actions = sum(len(ir.entry_points) for ir in irs)
        result.total_flags = sum(len(ir.flags) for ir in irs)
        result.total_insights = sum(len(ir.llm_insights) for ir in irs)

        result.duplicate_rules = self._find_duplicate_rules(irs)
        result.glossary = self._build_glossary(irs)
        result.magic_glossary = self._build_magic_glossary(irs)
        result.common_deps = self._map_common_deps(irs)
        result.decision_gaps = self._collect_decision_gaps(irs)
        result.all_flags = self._collect_all_flags(irs)
        result.controller_summaries = self._build_summaries(irs)

        result.risk_count = sum(
            len([f for f in ir.flags if f.type == "security_risk"]) for ir in irs
        )
        result.gap_count = sum(
            len([f for f in ir.flags if f.type == "missing_branch"]) for ir in irs
        )
        result.dep_count = sum(
            len([f for f in ir.flags if f.type == "unmapped_dep"]) for ir in irs
        )
        result.health_score = self._compute_health(result)

        if usages:
            result.total_usage = self._aggregate_usage(
                [u for u in usages if u is not None]
            )

        return result

    # -------------------------------------------------------------------------
    # 1. Logiques dupliquées
    # -------------------------------------------------------------------------

    def _find_duplicate_rules(self, irs: list[IRSchema]) -> list[DuplicateRule]:
        """Groupe les insights LLM dont la règle métier normalisée est identique."""
        key_map: dict[str, list[tuple[str, str]]] = {}  # key -> [(controller, rule)]

        for ir in irs:
            controller = ir.metadata.controller_name
            for insight in ir.llm_insights:
                if insight.business_rule.startswith("[Erreur"):
                    continue
                key = _normalize_rule(insight.business_rule)
                if key not in key_map:
                    key_map[key] = []
                key_map[key].append((controller, insight.business_rule))

        duplicates = []
        for key, occurrences in key_map.items():
            controllers = list({c for c, _ in occurrences})
            if len(controllers) >= 2:
                duplicates.append(DuplicateRule(
                    rule_key=key,
                    example_rule=occurrences[0][1],
                    controllers=controllers,
                    count=len(controllers),
                ))

        return sorted(duplicates, key=lambda d: d.count, reverse=True)

    # -------------------------------------------------------------------------
    # 2. Glossaire unifié
    # -------------------------------------------------------------------------

    def _build_glossary(self, irs: list[IRSchema]) -> list[GlossaryEntry]:
        """Extrait les noms de champs POST et colonnes SQL à travers tous les IR."""
        field_map: dict[str, dict] = {}  # field_name -> {controllers, contexts}

        for ir in irs:
            controller = ir.metadata.controller_name
            for flag in ir.flags:
                if flag.type != "security_risk":
                    continue
                # Extraire les champs POST
                for m in re.finditer(r"\$_POST\s*\[\s*'(\w+)'", flag.fragment):
                    fname = m.group(1)
                    if fname not in field_map:
                        field_map[fname] = {"controllers": set(), "contexts": []}
                    field_map[fname]["controllers"].add(controller)
                    if flag.fragment not in field_map[fname]["contexts"]:
                        field_map[fname]["contexts"].append(flag.fragment[:80])

            # Extraire les colonnes dans les opérations DB
            for op in ir.operations:
                if not op.details:
                    continue
                for m in re.finditer(r"WHERE\s+(\w+)\s*=", op.details, re.IGNORECASE):
                    col = m.group(1).lower()
                    if col in ("id", "1") or len(col) <= 1:
                        continue
                    if col not in field_map:
                        field_map[col] = {"controllers": set(), "contexts": []}
                    field_map[col]["controllers"].add(controller)

        entries = []
        for fname, data in sorted(field_map.items()):
            controllers = sorted(data["controllers"])
            entries.append(GlossaryEntry(
                field_name=fname,
                controllers=controllers,
                count=len(controllers),
                contexts=data["contexts"][:3],
            ))

        return sorted(entries, key=lambda e: e.count, reverse=True)

    # -------------------------------------------------------------------------
    # 2b. Glossaire des termes métier (constantes, variables business)
    # -------------------------------------------------------------------------

    def _build_magic_glossary(self, irs: list[IRSchema]) -> list[GlossaryEntry]:
        """Extrait les constantes et variables métier depuis les flags."""
        term_map: dict[str, dict] = {}

        def _add(term: str, ctrl: str, frag: str) -> None:
            if term.lower() in _GLOSSARY_GENERIC or len(term) < 3:
                return
            if term not in term_map:
                term_map[term] = {"controllers": set(), "contexts": []}
            term_map[term]["controllers"].add(ctrl)
            if frag and frag[:60] not in term_map[term]["contexts"]:
                term_map[term]["contexts"].append(frag[:60])

        for ir in irs:
            ctrl = ir.metadata.controller_name
            for flag in ir.flags:
                if flag.type not in ("magic_value", "missing_branch"):
                    continue
                frag = flag.fragment
                # Valeurs UPPERCASE comparées : == 'DSLAM', == 'GTR'
                for m in re.finditer(r"(?:==|!=|!==|===)\s*['\"]([A-Z][A-Z0-9_]{2,})['\"]", frag):
                    _add(m.group(1), ctrl, frag)
                # Clés de tableau UPPERCASE : ['GTR'], ['ADELIA_MANUEL']
                for m in re.finditer(r"\['([A-Z][A-Z0-9_]{2,})'\]", frag):
                    _add(m.group(1), ctrl, frag)
                # Constantes de classe : self::DSLAM
                for m in re.finditer(r"self::([A-Z][A-Z0-9_]{2,})", frag):
                    _add(m.group(1), ctrl, frag)
                # Variables camelCase métier (≥ 5 chars)
                for m in re.finditer(r"\$([a-z][a-z0-9]*[A-Z][a-zA-Z0-9]*)", frag):
                    var = m.group(1)
                    if len(var) >= 5 and var.lower() not in _GLOSSARY_GENERIC:
                        _add(var, ctrl, frag)

        entries = []
        for term, data in sorted(term_map.items()):
            controllers = sorted(data["controllers"])
            if len(controllers) >= 2:
                entries.append(GlossaryEntry(
                    field_name=term,
                    controllers=controllers,
                    count=len(controllers),
                    contexts=data["contexts"][:2],
                ))
        return sorted(entries, key=lambda e: (-e.count, e.field_name))

    # -------------------------------------------------------------------------
    # 3. Dépendances communes
    # -------------------------------------------------------------------------

    def _map_common_deps(self, irs: list[IRSchema]) -> list[CommonDependency]:
        """Cartographie les dépendances legacy les plus sollicitées."""
        dep_map: dict[str, dict] = {}

        for ir in irs:
            controller = ir.metadata.controller_name
            for dep in ir.dependencies:
                if dep.suggested_symfony is not None:
                    continue  # dépendances déjà mappées, pas d'intérêt ici
                if dep.name not in dep_map:
                    dep_map[dep.name] = {"type": dep.type, "controllers": set()}
                dep_map[dep.name]["controllers"].add(controller)

        result = []
        for name, data in dep_map.items():
            controllers = sorted(data["controllers"])
            result.append(CommonDependency(
                name=name,
                dep_type=data["type"],
                controllers=controllers,
                count=len(controllers),
            ))

        return sorted(result, key=lambda d: d.count, reverse=True)

    # -------------------------------------------------------------------------
    # 4. Gaps de décision
    # -------------------------------------------------------------------------

    def _collect_decision_gaps(self, irs: list[IRSchema]) -> list[DecisionGap]:
        """Collecte tous les points de décision sans branche définie (missing_branch)."""
        gaps = []
        for ir in irs:
            controller = ir.metadata.controller_name
            confidence_map = {ins.flag_id: ins.confidence for ins in ir.llm_insights}
            for flag in ir.flags:
                if flag.type != "missing_branch":
                    continue
                gaps.append(DecisionGap(
                    condition_fragment=flag.fragment,
                    condition_business=flag.question,
                    controller=controller,
                    location=flag.location,
                    flag_type=flag.type,
                    flag_id=flag.id,
                    confidence=confidence_map.get(flag.id, 0.0),
                ))
        return gaps

    def _collect_all_flags(self, irs: list[IRSchema]) -> list[DecisionGap]:
        """Collecte tous les flags (tous types) avec leur confiance LLM, pour le top-5 PO."""
        flags = []
        for ir in irs:
            controller = ir.metadata.controller_name
            confidence_map = {ins.flag_id: ins.confidence for ins in ir.llm_insights}
            for flag in ir.flags:
                flags.append(DecisionGap(
                    condition_fragment=flag.fragment,
                    condition_business=flag.question,
                    controller=controller,
                    location=flag.location,
                    flag_type=flag.type,
                    flag_id=flag.id,
                    confidence=confidence_map.get(flag.id, 0.0),
                ))
        return flags

    # -------------------------------------------------------------------------
    # 5. Résumés par contrôleur
    # -------------------------------------------------------------------------

    def _build_summaries(self, irs: list[IRSchema]) -> list[ControllerSummary]:
        summaries = []
        for ir in irs:
            risk = len([f for f in ir.flags if f.type == "security_risk"])
            gap = len([f for f in ir.flags if f.type == "missing_branch"])
            dep = len([f for f in ir.flags if f.type == "unmapped_dep"])
            score = max(0.0, 100.0 - risk * 4 - gap * 5 - dep * 2)
            summaries.append(ControllerSummary(
                controller_name=ir.metadata.controller_name,
                source_file=ir.metadata.source_file,
                actions=len(ir.entry_points),
                risk_count=risk,
                gap_count=gap,
                unmapped_deps=dep,
                health_score=round(score, 1),
            ))
        return sorted(summaries, key=lambda s: s.health_score)

    # -------------------------------------------------------------------------
    # 6. Score de santé global
    # -------------------------------------------------------------------------

    @staticmethod
    def _compute_health(ins: AggregatedInsights) -> float:
        if not ins.controllers:
            return 100.0
        score = 100.0 - ins.risk_count * 3 - ins.gap_count * 4 - ins.dep_count * 2
        return round(max(0.0, score), 1)

    # -------------------------------------------------------------------------
    # 7. Cumul des usages LLM
    # -------------------------------------------------------------------------

    @staticmethod
    def _aggregate_usage(usages: list[TokenUsage]) -> Optional[TokenUsage]:
        if not usages:
            return None
        total = TokenUsage()
        for u in usages:
            total.input_tokens += u.input_tokens
            total.output_tokens += u.output_tokens
            total.cache_read_tokens += u.cache_read_tokens
            total.cache_creation_tokens += u.cache_creation_tokens
            total.skipped_flags += u.skipped_flags
            total.enriched_flags += u.enriched_flags
        return total


# =============================================================================
# Helpers
# =============================================================================

def _normalize_rule(rule: str) -> str:
    """Clé de normalisation pour détecter des règles similaires."""
    clean = rule.lower()
    clean = re.sub(r'\[contexte manquant.*?\]', '', clean)
    clean = re.sub(r'\s+', ' ', clean)
    clean = re.sub(r'[^\w\s]', '', clean)
    return clean[:60].strip()
