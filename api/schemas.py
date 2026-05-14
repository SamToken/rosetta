"""Rosetta API — Schémas Pydantic v2 (contrats request/response)."""
from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


# =============================================================================
# Audit — job d'analyse PHP
# =============================================================================

class AuditStartRequest(BaseModel):
    """Paramètres d'un job d'audit PHP."""

    php_paths: list[str] = Field(
        description="Chemins absolus vers les fichiers PHP ou répertoires à analyser"
    )
    no_llm: bool = Field(False, description="Mode déterministe uniquement (0 token, 0 €)")
    model: str = Field("claude-sonnet-4-6", description="Modèle LLM Anthropic")
    bug_check: bool = Field(False, description="Activer la grille bugs techniques (13 catégories)")
    kb_root: Optional[str] = Field(None, description="Répertoire de fiches KB (.md) à injecter dans le contexte LLM")
    call_graph_root: Optional[str] = Field(None, description="Répertoire source pour l'indexation du call graph")
    contexte: str = Field("", description="Label contextuel pour l'archivage (ex: 'US-1234')")
    max_workers: int = Field(4, ge=1, le=16, description="Fichiers analysés en parallèle (batch). 1 = séquentiel.")


class AuditFileSummary(BaseModel):
    """Résumé par fichier dans un job d'audit."""

    filename: str
    file_size_lines: int
    processing_time_seconds: float
    flags_total: int
    flag_types: dict[str, int] = Field(default_factory=dict, description="Nombre de flags par type (ex: {'missing_branch': 7})")
    insights_total: int
    llm_cost_usd: float
    status: str = Field(description="'success' | 'no_llm' | 'error'")


class AuditJobResult(BaseModel):
    """Résultats agrégés d'un job terminé."""

    total_files: int
    total_insights: int
    total_cost_usd: float
    processing_time_seconds: float
    health_score: Optional[int] = Field(None, description="Score santé global 0-100")
    output_dir: str = Field(description="Répertoire de sortie des fichiers générés")
    php_paths: list[str] = Field(default_factory=list, description="Chemins PHP analysés (pour relancer)")
    files: list[AuditFileSummary] = []


class OutputFile(BaseModel):
    """Fichier généré par un job (chemin relatif + libellé lisible)."""

    label: str
    path: str


class JobCreatedResponse(BaseModel):
    """Réponse immédiate après soumission d'un job (HTTP 202)."""

    job_id: str
    status: Literal["queued"] = "queued"
    message: str


class JobStatusResponse(BaseModel):
    """État complet d'un job d'audit."""

    job_id: str
    status: Literal["queued", "running", "success", "error"]
    created_at: str = Field(description="ISO-8601 UTC")
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    logs: list[str] = Field(default_factory=list, description="Messages de progression")
    error: Optional[str] = None
    result: Optional[AuditJobResult] = None
    has_dashboard: bool = Field(False, description="True si dashboard.html est disponible pour ce job")


# =============================================================================
# KB — Knowledge Base
# =============================================================================

class KBStatsResponse(BaseModel):
    """Tableau de bord de la Knowledge Base."""

    projet: str
    version: str
    last_updated: str
    maintainer: str
    # Sections
    codes: int
    regles: int = Field(0, description="Rétrocompat — entrées non migrées")
    regles_metier: int = Field(0, description="Règles métier validées PO")
    bugs_connus: int = Field(0, description="Bugs identifiés avant migration")
    observations: int = Field(0, description="Observations techniques")
    schema_entries: int = Field(description="Entrées schéma Oracle")
    colonnes: int
    vues: int
    requetes: int
    relations: int = Field(0)
    total: int
    high: int
    medium: int
    inferred: int
    pending_total: int
    pending_high: int
    pending_po: int = Field(0, description="Règles métier avec confiance != high (à valider PO)")


class LookupResponse(BaseModel):
    """Résultat d'un lookup dans le KB."""

    found: bool
    code: str
    section: Optional[str] = Field(None, description="codes | regles | sql_artifacts.colonnes | …")
    entry: Optional[dict[str, Any]] = Field(None, description="Contenu YAML de l'entrée")


class PendingItemResponse(BaseModel):
    """Question en attente de validation PO."""

    id: str = Field(description="Identifiant PV-NNN")
    code: str
    question: str
    priorite: str = Field(description="high | medium | low")
    domaine: Optional[str] = None
    fichiers: list[str] = []
    kb_type: Optional[str] = None
    pending_type: Optional[int] = Field(None, description="1=kb_upgrade 2=kb_new_entry 3=migration_notes")
    destination: Optional[str] = None


class SearchResultResponse(BaseModel):
    """Résultat d'une recherche textuelle dans le KB."""

    section: str
    nom: str
    label: str
    confiance: str


class KBEntryResponse(BaseModel):
    """Entrée KB — toutes sections confondues.

    Les champs relation_* sont renseignés uniquement pour section='relations'.
    """

    code: str
    label: str
    domaine: str
    confiance: str  # high | medium | inferred
    section: str    # codes | regles | sql_artifacts.colonnes | relations | …
    notes: str
    source: str
    pending_questions: int = Field(0, description="Nb de questions 'À valider PO' dans les notes")
    lie_a: list[str] = []
    # Champs spécifiques aux relations sémantiques (None pour les autres sections)
    relation_kind: Optional[str] = None
    relation_from: Optional[str] = None
    relation_to: Optional[str] = None
    relation_direction: Optional[str] = None
    trouve_dans: list[dict[str, Any]] = Field(default_factory=list)


class CaptureRequest(BaseModel):
    """Paramètres pour capturer un code/constante métier."""

    code: str
    label: str
    source: str
    confiance: Literal["high", "medium", "inferred"] = "high"
    domain: str = "commun"
    champ: Optional[str] = None
    table: Optional[str] = None
    lie_a: Optional[str] = Field(None, description="Codes liés, séparés par virgule")
    notes: Optional[str] = None
    force: bool = Field(False, description="Écraser si confiance high existante")


class CaptureResponse(BaseModel):
    """Résultat d'une opération de capture."""

    success: bool
    code: str
    confiance: str
    domain: str
    action: str = Field(description="created | updated | skipped_high")
    file_path: Optional[str] = Field(None, description="Fichier domaine cible (mode répertoire)")
    message: str


class DeleteKBEntryResponse(BaseModel):
    success: bool
    code: str
    message: str


class UpdateConfianceRequest(BaseModel):
    confiance: Literal["high", "medium", "inferred"]


class UpdateConfianceResponse(BaseModel):
    success: bool
    code: str
    confiance: str
    message: str


class ValidateRelationRequest(BaseModel):
    relation_from: str
    relation_to: str
    relation_kind: str
    confiance: Literal["high", "medium", "inferred"] = "high"


class ValidateRelationResponse(BaseModel):
    success: bool
    updated: int
    message: str


class AddPendingRequest(BaseModel):
    """Paramètres pour ajouter une question dans la file PO."""

    code: str
    question: str
    priorite: Literal["high", "medium", "low"] = "medium"
    fichiers: Optional[str] = Field(None, description="Fichiers source, séparés par virgule")
    kb_type: str = Field("code", description="code | regle | colonne | vue | requete")
    domaine: Optional[str] = None


class AddPendingResponse(BaseModel):
    """Résultat d'un ajout en pending."""

    pending_id: str
    code: str
    priorite: str
    destination: str = Field(description="kb_upgrade | kb_new_entry | migration_notes")


class ValidatePendingRequest(BaseModel):
    """Paramètres de validation d'une question PO."""

    label: Optional[str] = None
    source: Optional[str] = Field(None, description="Défaut : 'PO validé — YYYY-MM-DD'")
    notes: Optional[str] = None
    domaine: Optional[str] = Field(None, description="Domaine cible (mode répertoire)")


class ValidatePendingResponse(BaseModel):
    """Résultat d'une validation PO."""

    success: bool
    pending_id: str
    code: str
    action: str = Field(description="created | updated")
    domain: str
    error: Optional[str] = None


# =============================================================================
# Flags + recettes migration
# =============================================================================

class RecipeOut(BaseModel):
    """Recette de migration Zend → Symfony associée à un flag."""

    id: str
    title: str
    effort: str
    zend_pattern: str
    symfony_equivalent: str
    diff_before: str
    diff_after: str
    migration_notes: str


class FlagOut(BaseModel):
    """Flag d'analyse avec recette migration optionnelle."""

    id: str
    type: str
    fragment: str = ""
    location: str = ""
    source_line: Optional[int] = None
    method_name: Optional[str] = None
    question: str = ""
    impact_category: str = ""
    recipe: Optional[RecipeOut] = None


# =============================================================================
# Impact cross-fichier
# =============================================================================

class ImpactOccurrence(BaseModel):
    """Une occurrence d'un token dans un fichier source."""

    fichier: str
    methode: str = ""
    ligne: Optional[int] = None
    source: str = Field("relation", description="relation | flag | operation")


class ImpactTokenOut(BaseModel):
    """Données d'impact d'un token KB à travers tous les fichiers analysés."""

    total_occurrences: int
    distinct_files: int
    kb_known: bool
    sources: list[str] = Field(default_factory=list)
    occurrences: list[ImpactOccurrence] = Field(default_factory=list)


class ImpactIndexOut(BaseModel):
    """Index d'impact cross-fichier — tous les tokens."""

    ir_count: int
    token_count: int
    tokens: dict[str, ImpactTokenOut]


# =============================================================================
# Télémétrie ROI
# =============================================================================

class ROISummaryResponse(BaseModel):
    """Dashboard ROI Rosetta."""

    total_runs: int
    total_lines_analyzed: int
    total_human_hours_saved: float
    financial_saving_eur: float
    total_llm_cost_usd: float
    total_machine_seconds: float
    success_rate_pct: float
    avg_processing_seconds: float
    lines_per_hour_constant: int
    hourly_rate_eur: float


class ROIDayResponse(BaseModel):
    """Métriques agrégées pour un jour donné (courbe 7 jours)."""

    date: str = Field(description="Date ISO YYYY-MM-DD")
    runs: int
    lines_analyzed: int
    hours_saved: float
    cost_usd: float


class DepNode(BaseModel):
    """Nœud du graphe de dépendances (= un fichier PHP analysé)."""

    id: str = Field(description="Identifiant unique (controller_name)")
    label: str = Field(description="Nom court affiché")
    file_type: str = Field(description="controller | service | unknown")
    flags: int = Field(description="Nombre de flags détectés")
    confidence: float = Field(description="Score de confiance 0-1")
    file_path: str = Field(description="Chemin source PHP")


class DepEdge(BaseModel):
    """Arête dirigée source → target."""

    source: str
    target: str
    dep_type: str = Field(description="use | service | instantiation")


class DependencyGraph(BaseModel):
    """Graphe de dépendances complet pour un job."""

    nodes: list[DepNode]
    edges: list[DepEdge]
