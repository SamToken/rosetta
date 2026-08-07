"""
Rosetta IR Schema
=================
Intermediate Representation pour la migration PHP Legacy → Symfony.

L'IR capture l'INTENTION du code, pas sa syntaxe.
"""

from datetime import datetime
from enum import Enum
from typing import Literal, Optional
from pydantic import BaseModel, Field


class SourceType(str, Enum):
    """Type de source supporté."""
    PHP = "php"
    ASM = "asm"  # Pour plus tard


class ImpactCategory(str, Enum):
    """Catégorie d'impact métier d'un flag."""
    CRITICAL_CORRUPTION = "CRITICAL_CORRUPTION"
    API_OVERLOAD        = "API_OVERLOAD"
    LOGIC_GAP           = "LOGIC_GAP"


class BugSeverity(str, Enum):
    """Sévérité d'un bug technique détecté par la grille LLM."""
    CRITICAL = "critical"  # erreur fatale / crash production possible
    HIGH     = "high"      # comportement incorrect silencieux ou donnée corrompue
    MEDIUM   = "medium"    # warning PHP ou résultat inattendu dans certains cas
    LOW      = "low"       # risque de régression migration PHP 8.2+


class BugCategory(str, Enum):
    """Catégories de bugs détectés par la grille structurée (BugEnricher)."""
    UNINIT_VAR           = "uninit_variable"       # variable réutilisée sans réinit entre cases
    PHP82_COMPAT         = "php82_compat"          # propriété dynamique, false[0], null['key']
    OPERATOR_PRECEDENCE  = "operator_precedence"   # &&/|| sans parenthèses dans condition complexe
    STRPOS_LOOSE         = "strpos_type_unsafe"    # strpos sans !== false
    DATE_FORMAT          = "date_format_invalid"   # date() avec format non-PHP
    SWITCH_FALLTHROUGH   = "switch_fallthrough"    # case sans break tombant dans le suivant
    FOREACH_NULL         = "foreach_null_guard"    # foreach sur variable potentiellement null
    SLEEP_BLOCKING       = "sleep_blocking"        # sleep() bloquant dans un worker PHP synchrone
    STATE_MUTATION       = "instance_state_mutation" # $this->x modifié dans méthode réentrante
    NULL_DEREF           = "null_dereference"      # appel méthode/propriété sur variable nullable
    ARRAY_UNCHECKED      = "array_access_unchecked" # accès $arr['k']['sub'] sans isset
    FINALLY_SCOPE        = "finally_scope_logic"   # code métier après finally non atteint si exception
    PARAM_ORDER          = "parameter_order"       # arguments inversés vs signature déclarée


class FlagType(str, Enum):
    """Types de flag — validation Pydantic garantit qu'aucun type inconnu ne peut être créé."""

    def __str__(self) -> str:
        return self.value

    MISSING_BRANCH          = "missing_branch"
    MAGIC_VALUE             = "magic_value"
    SECURITY_RISK           = "security_risk"
    UNMAPPED_DEP            = "unmapped_dep"
    BUSINESS_LOGIC_UNCLEAR  = "business_logic_unclear"
    SIDE_EFFECT             = "side_effect"
    DYNAMIC_SESSION_KEY     = "dynamic_session_key"
    CHAINED_API_CALL        = "chained_api_call"
    SITUATION_COVERAGE      = "situation_coverage"
    EXTERNAL_STATE_DEPENDENCY = "external_state_dependency"
    MODULE_EXECUTION_GAP    = "module_execution_gap"
    HARDCODED_SITUATION     = "hardcoded_situation_code"
    EMPTY_CATCH             = "empty_catch"
    STRONG_COUPLING         = "strong_coupling"
    CHAINED_METHOD_CALL     = "chained_method_call"


class Visibility(str, Enum):
    """Visibilité d'une méthode/fonction."""
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"


class OperationType(str, Enum):
    """Types d'opérations métier."""
    DB_READ = "db_read"
    DB_WRITE = "db_write"
    DB_DELETE = "db_delete"
    REDIRECT = "redirect"
    RENDER = "render"
    API_CALL = "api_call"
    CALCULATION = "calculation"
    VALIDATION = "validation"
    SESSION = "session"
    EMAIL = "email"
    FILE_IO = "file_io"
    UNKNOWN = "unknown"


# =============================================================================
# Blocs de base
# =============================================================================

class Parameter(BaseModel):
    """Paramètre d'une fonction/méthode."""
    name: str
    type_hint: Optional[str] = None
    default_value: Optional[str] = None


class EntryPoint(BaseModel):
    """Point d'entrée : une action de contrôleur."""
    name: str
    original_name: str  # editAction → edit
    visibility: Visibility = Visibility.PUBLIC
    parameters: list[Parameter] = Field(default_factory=list)
    route_pattern: Optional[str] = None  # /user/edit/:id
    http_methods: list[str] = Field(default_factory=lambda: ["GET"])
    
    # Code brut de l'action (pour que l'IA ait le contexte complet)
    raw_code: Optional[str] = None
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    
    # Opérations spécifiques à cette action (IDs)
    operation_ids: list[str] = Field(default_factory=list)

    # Score de risque calculé par le PHP Extractor
    risk_score: Optional[float] = None
    risk_details: Optional[dict] = None
    critical_risk: bool = False

    # Reachability (détection de code mort #4) — renseigné seulement si un call
    # graph est fourni (--call-graph-root). None = non évalué (pas de verdict).
    is_referenced: Optional[bool] = None
    dead_code_suspected: bool = False


class Operation(BaseModel):
    """Une opération métier extraite du code."""
    id: str
    type: OperationType
    details: str  # Le SQL, l'URL, le template...
    source_line: Optional[int] = None
    raw_code: Optional[str] = None  # Le code PHP original (pour debug)


class ControlBlock(BaseModel):
    """Un bloc dans le graphe de contrôle."""
    id: str
    condition: Optional[str] = None  # None = bloc inconditionnel
    true_branch: Optional[str] = None
    false_branch: Optional[str] = None
    operations: list[str] = Field(default_factory=list)  # IDs des opérations
    source_line: Optional[int] = None    # ligne du if dans le fichier source
    raw_context: Optional[str] = None   # ±3 lignes autour pour le contexte
    business_context: Optional[str] = None  # commentaire PHP précédant le if


class DataFlow(BaseModel):
    """Flux de données : entrées et sorties."""
    inputs: list[str] = Field(default_factory=list)  # $_GET['id'], $request->get('id')
    outputs: list[str] = Field(default_factory=list)  # redirect, render, json
    session_reads: list[str] = Field(default_factory=list)
    session_writes: list[str] = Field(default_factory=list)


class Dependency(BaseModel):
    """Une dépendance externe."""
    name: str
    type: str  # "repository", "service", "helper", "model"
    suggested_symfony: Optional[str] = None  # Mapping vers Symfony


# =============================================================================
# Le schéma IR principal
# =============================================================================

class IRMetadata(BaseModel):
    """Métadonnées de l'extraction."""
    source_type: SourceType = SourceType.PHP
    source_file: str
    controller_name: str
    extracted_at: datetime = Field(default_factory=datetime.now)
    extractor_version: str = "0.1.0"
    confidence_score: float = 1.0  # 0-1, baisse si parsing incomplet
    file_type: str = "unknown"  # controller | service | helper | tools | repository | unknown

    # Structure d'héritage (#1/#2) — où vit réellement le comportement. La logique
    # métier legacy est souvent dans la classe parente ou des traits partagés.
    parent_class: Optional[str] = None       # extends X
    interfaces: list[str] = Field(default_factory=list)  # implements A, B
    traits: list[str] = Field(default_factory=list)      # use TraitX; dans le corps


class UnparsedSection(BaseModel):
    """Section que l'extracteur n'a pas pu parser."""
    start_line: int
    end_line: int
    reason: str
    raw_code: str


class Flag(BaseModel):
    """Zone ambiguë détectée mécaniquement — source déterministe, confiance 1.0."""
    id: str
    type: FlagType
    location: str  # nom de l'entry_point, block_id, op_id ou dep_name
    fragment: str  # le code brut minimal concerné
    question: str  # question précise à poser au LLM ou à un humain
    source_line: Optional[int] = None        # ligne absolue dans le fichier source
    method_name: Optional[str] = None        # nom de la méthode contenant le flag
    method_original_name: Optional[str] = None  # nom PHP original (ex: editAction)
    context_lines: Optional[str] = None     # ±3 lignes autour pour copier dans Copilot
    impact_category: ImpactCategory = ImpactCategory.LOGIC_GAP
    see_also: list[str] = Field(default_factory=list)  # IDs de Relation couvrant ce fragment
    # Rempli par ConfigCrossref quand la valeur est un fait de configuration Oracle :
    # {table, cle, label, conditions} — le LLM enricher skippe ces flags
    resolved_by_config: Optional[dict] = None


# =============================================================================
# Token KB typé (extrait par LLMEnricher pour lookup ciblé)
# =============================================================================

KBTokenKind = Literal[
    "literal",        # 'TP2', "ST_OUV" — tout littéral entre guillemets (MAJ ou camelCase)
    "constant",       # C_TYP_FLX — SCREAMING_SNAKE_CASE non quoté
    "column",         # colonne extraite d'un SELECT/WHERE/SET SQL
    "table",          # table extraite d'un FROM/JOIN/INTO/UPDATE SQL
    "service_method", # enchainementService.getEtat — appel de service
    "view_path",      # enchainement/index.phtml — chemin de vue Zend
    "magic_value",    # 2, 3 — valeur numérique comparée à une variable
]


class KBToken(BaseModel):
    """Token extrait d'un flag.fragment, typé pour un lookup KB ciblé."""
    value: str
    kind: KBTokenKind
    source_op_id: Optional[str] = None


# =============================================================================
# Relations sémantiques (extraites par RelationExtractor)
# =============================================================================

class EntityRef(BaseModel):
    """Référence à une entité métier dans une relation."""
    type: str   # "code" | "column_value" | "situation" | "module" | "event"
    value: str  # ex: "TP2", "C_TYP_FLX = 2", "H1"


class CodeRef(BaseModel):
    """Référence à un emplacement dans le code source."""
    fichier: str
    methode: str = ""
    ligne: Optional[int] = None


class Relation(BaseModel):
    """Relation sémantique entre deux entités métier, extraite statiquement.

    Les relations complètent les fiches KB atomiques : elles capturent les
    liens implicites (implication, synonymie, transition) que le LLM rate
    quand il ne reçoit qu'une fiche isolée.
    """
    id: str
    kind: str           # "implies" | "transitions_to" | "requires" | "synonym_of"
    from_entity: EntityRef
    to_entity: EntityRef
    direction: str = "one_way"      # "one_way" | "bidirectional"
    domaine: str = ""
    confiance: str = "medium"       # "high" | "medium" | "inferred"
    conditions: list[str] = Field(default_factory=list)
    trouvé_dans: list[CodeRef] = Field(default_factory=list)
    semantique: str = ""
    pattern: str = ""  # "pattern_a" | "pattern_b" — trace de l'origine


class LLMInsight(BaseModel):
    """Enrichissement LLM d'un flag — confiance < 1.0, toujours à valider."""
    flag_id: str
    business_rule: str  # explication en français pour le PO
    missing_context: Optional[str] = None  # question ouverte si contexte insuffisant
    confidence: float  # jamais 1.0
    source: str = "llm"
    needs_human_validation: bool = True
    validated: bool = False
    validated_by: Optional[str] = None


class BugFinding(BaseModel):
    """Bug technique détecté par la grille structurée BugEnricher (source LLM, 1 appel/fichier)."""
    category: BugCategory
    severity: BugSeverity
    method_name: Optional[str] = None   # méthode PHP concernée
    fragment: str                        # extrait de code exact (1-3 lignes)
    description: str                     # explication précise du bug
    fix: Optional[str] = None           # correction minimale suggérée
    source: str = "llm_bug_check"


class IRSchema(BaseModel):
    """
    Intermediate Representation complète d'un contrôleur.
    
    C'est LE format pivot entre PHP legacy et Symfony.
    """
    metadata: IRMetadata
    entry_points: list[EntryPoint] = Field(default_factory=list)
    operations: list[Operation] = Field(default_factory=list)
    control_flow: list[ControlBlock] = Field(default_factory=list)
    data_flow: DataFlow = Field(default_factory=DataFlow)
    dependencies: list[Dependency] = Field(default_factory=list)
    
    # Ce qu'on n'a pas pu parser (pour passe IA ultérieure)
    unparsed_sections: list[UnparsedSection] = Field(default_factory=list)

    # Zones ambiguës détectées mécaniquement (déterministe, confiance 1.0)
    flags: list[Flag] = Field(default_factory=list)

    # Enrichissements LLM (confiance < 1.0, toujours séparés)
    llm_insights: list[LLMInsight] = Field(default_factory=list)

    # Bugs techniques détectés par grille structurée (1 appel LLM/fichier, --bug-check)
    bug_findings: list[BugFinding] = Field(default_factory=list)

    # Relations sémantiques extraites statiquement par RelationExtractor
    relations: list[Relation] = Field(default_factory=list)

    # ==========================================================================
    # Méthodes utilitaires
    # ==========================================================================
    
    def to_json(self, indent: int = 2) -> str:
        """Exporte l'IR en JSON."""
        return self.model_dump_json(indent=indent)
    
    @classmethod
    def from_json(cls, json_str: str) -> "IRSchema":
        """Charge l'IR depuis JSON."""
        return cls.model_validate_json(json_str)
    
    def token_estimate(self) -> int:
        """
        Estime le nombre de tokens pour envoyer cet IR à un LLM.
        Règle approximative : 1 token ≈ 4 caractères.
        """
        json_str = self.to_json(indent=0)
        return len(json_str) // 4
    
    def summary(self) -> dict:
        """Résumé rapide de l'IR."""
        return {
            "controller": self.metadata.controller_name,
            "actions": len(self.entry_points),
            "operations": len(self.operations),
            "db_operations": len([o for o in self.operations if o.type in [OperationType.DB_READ, OperationType.DB_WRITE, OperationType.DB_DELETE]]),
            "unparsed": len(self.unparsed_sections),
            "flags": len(self.flags),
            "llm_insights": len(self.llm_insights),
            "relations": len(self.relations),
            "confidence": self.metadata.confidence_score,
            "estimated_tokens": self.token_estimate()
        }


# =============================================================================
# Factory pour créer facilement des IR
# =============================================================================

def create_ir(
    source_file: str,
    controller_name: str,
    source_type: SourceType = SourceType.PHP
) -> IRSchema:
    """Crée un IR vide prêt à être rempli."""
    return IRSchema(
        metadata=IRMetadata(
            source_type=source_type,
            source_file=source_file,
            controller_name=controller_name
        )
    )
