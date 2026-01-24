"""
Rosetta IR Schema
=================
Intermediate Representation pour la migration PHP Legacy → Symfony.

L'IR capture l'INTENTION du code, pas sa syntaxe.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class SourceType(str, Enum):
    """Type de source supporté."""
    PHP = "php"
    ASM = "asm"  # Pour plus tard


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


class UnparsedSection(BaseModel):
    """Section que l'extracteur n'a pas pu parser."""
    start_line: int
    end_line: int
    reason: str
    raw_code: str


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
