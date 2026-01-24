"""
Symfony Prompt Generator
========================
Génère des prompts optimisés pour migrer du PHP legacy vers Symfony 6.

L'idée : on donne à l'IA un prompt structuré avec l'IR + le code brut,
elle génère le code Symfony correspondant.
"""

from pathlib import Path
from typing import Optional
from ir.schema import IRSchema, EntryPoint, OperationType


class SymfonyPromptGenerator:
    """
    Génère des prompts de migration PHP → Symfony.
    
    Stratégie :
    - Un prompt par ACTION (pas par contrôleur entier)
    - L'IA reçoit l'IR structuré + le code brut
    - Tokens optimisés, contexte préservé
    """
    
    def __init__(self, symfony_version: str = "6.4"):
        self.symfony_version = symfony_version
    
    # =========================================================================
    # Génération de prompt pour une action
    # =========================================================================
    
    def generate_action_prompt(
        self, 
        ir: IRSchema, 
        action_name: str,
        include_raw_code: bool = True
    ) -> str:
        """
        Génère un prompt pour migrer UNE action spécifique.
        
        Args:
            ir: L'IR complet du contrôleur
            action_name: Nom de l'action (ex: "edit")
            include_raw_code: Inclure le code PHP brut
            
        Returns:
            Le prompt optimisé pour l'IA
        """
        # Trouver l'action
        action = self._find_action(ir, action_name)
        if not action:
            raise ValueError(f"Action '{action_name}' non trouvée dans l'IR")
        
        # Construire le prompt
        prompt_parts = []
        
        # 1. Contexte
        prompt_parts.append(self._build_context_section(ir, action))
        
        # 2. Structure extraite (l'IR)
        prompt_parts.append(self._build_ir_section(ir, action))
        
        # 3. Code source (si demandé)
        if include_raw_code and action.raw_code:
            prompt_parts.append(self._build_raw_code_section(action))
        
        # 4. Instructions de génération
        prompt_parts.append(self._build_instructions_section(ir, action))
        
        return "\n\n".join(prompt_parts)
    
    def _find_action(self, ir: IRSchema, action_name: str) -> Optional[EntryPoint]:
        """Trouve une action par son nom."""
        for ep in ir.entry_points:
            if ep.name == action_name or ep.original_name == action_name:
                return ep
        return None
    
    def _build_context_section(self, ir: IRSchema, action: EntryPoint) -> str:
        """Construit la section de contexte."""
        return f"""## Contexte de migration

**Source:** Contrôleur Zend Framework 1 `{ir.metadata.controller_name}Controller`
**Action:** `{action.original_name}` (lignes {action.start_line}-{action.end_line})
**Cible:** Symfony {self.symfony_version} avec Doctrine ORM

**Objectif:** Générer le code Symfony équivalent en préservant TOUTE la logique métier."""
    
    def _build_ir_section(self, ir: IRSchema, action: EntryPoint) -> str:
        """Construit la section IR (structure extraite)."""
        
        # Filtrer les opérations liées à cette action (par numéro de ligne)
        action_ops = []
        if action.start_line and action.end_line:
            for op in ir.operations:
                if op.source_line and action.start_line <= op.source_line <= action.end_line:
                    action_ops.append(op)
        
        # Construire les listes
        db_reads = [op for op in action_ops if op.type == OperationType.DB_READ]
        db_writes = [op for op in action_ops if op.type in [OperationType.DB_WRITE, OperationType.DB_DELETE]]
        redirects = [op for op in action_ops if op.type == OperationType.REDIRECT]
        renders = [op for op in action_ops if op.type == OperationType.RENDER]
        
        section = f"""## Structure extraite automatiquement

### Route
- **Pattern:** `{action.route_pattern}`
- **Méthodes HTTP:** {', '.join(action.http_methods)}

### Entrées de données
- **Inputs:** {', '.join(ir.data_flow.inputs) or 'Aucun'}
- **Session lue:** {', '.join(ir.data_flow.session_reads) or 'Aucune'}

### Opérations base de données"""
        
        if db_reads:
            section += "\n**Lectures:**"
            for op in db_reads:
                section += f"\n- `{op.details}`"
        
        if db_writes:
            section += "\n**Écritures:**"
            for op in db_writes:
                section += f"\n- `{op.details}`"
        
        if redirects:
            section += "\n\n### Redirections"
            for op in redirects:
                section += f"\n- `{op.details}`"
        
        if renders:
            section += "\n\n### Rendus de template"
            for op in renders:
                section += f"\n- `{op.details}.html.twig`"
        
        return section
    
    def _build_raw_code_section(self, action: EntryPoint) -> str:
        """Construit la section avec le code PHP brut."""
        return f"""## Code source PHP (pour référence)

```php
{action.raw_code}
```

⚠️ **Important:** Ce code contient la logique métier COMPLÈTE. 
Assure-toi de migrer CHAQUE comportement, y compris :
- Les validations
- Les conditions (guards)
- Les messages d'erreur
- L'ordre des opérations"""
    
    def _build_instructions_section(self, ir: IRSchema, action: EntryPoint) -> str:
        """Construit les instructions de génération."""
        
        deps = [d.name for d in ir.dependencies if d.type in ("service", "instantiation")]
        
        return f"""## Instructions de génération

Génère un contrôleur Symfony {self.symfony_version} avec :

### Structure attendue
```php
<?php

namespace App\\Controller;

use Symfony\\Bundle\\FrameworkBundle\\Controller\\AbstractController;
use Symfony\\Component\\HttpFoundation\\Request;
use Symfony\\Component\\HttpFoundation\\Response;
use Symfony\\Component\\Routing\\Annotation\\Route;
use Doctrine\\ORM\\EntityManagerInterface;
// ... autres imports nécessaires

#[Route('/user')]
class {ir.metadata.controller_name}Controller extends AbstractController
{{
    public function __construct(
        private EntityManagerInterface $em,
        // ... autres dépendances
    ) {{}}
    
    #[Route('{action.route_pattern}', name: '{ir.metadata.controller_name.lower()}_{action.name}', methods: {action.http_methods})]
    public function {action.name}(Request $request): Response
    {{
        // Code migré ici
    }}
}}
```

### Règles de migration
1. **Session** → Utilise `$this->getUser()` ou le service Security
2. **$_GET/$_POST** → Utilise `$request->query->get()` / `$request->request->get()`
3. **Zend_Db** → Utilise Doctrine Repository ou QueryBuilder
4. **$this->view->** → Passe les variables à `$this->render()`
5. **$this->_redirect()** → Utilise `$this->redirectToRoute()`
6. **Validation** → Utilise les contraintes Symfony ou un Form

### Dépendances détectées à injecter
{chr(10).join(f'- {d}' for d in deps) if deps else '- Aucune détectée'}

### Format de sortie
Génère UNIQUEMENT le code PHP, sans explications."""
    
    # =========================================================================
    # Génération pour tout le contrôleur
    # =========================================================================
    
    def generate_controller_prompts(
        self, 
        ir: IRSchema,
        include_raw_code: bool = True
    ) -> dict[str, str]:
        """
        Génère un prompt pour CHAQUE action du contrôleur.
        
        Returns:
            Dict {action_name: prompt}
        """
        prompts = {}
        for action in ir.entry_points:
            prompts[action.name] = self.generate_action_prompt(
                ir, 
                action.name,
                include_raw_code
            )
        return prompts
    
    def estimate_tokens(self, prompt: str) -> int:
        """Estime le nombre de tokens d'un prompt."""
        return len(prompt) // 4
    
    # =========================================================================
    # Export
    # =========================================================================
    
    def save_prompts(
        self, 
        ir: IRSchema, 
        output_dir: Path | str,
        include_raw_code: bool = True
    ) -> list[Path]:
        """
        Sauvegarde les prompts dans des fichiers .md
        
        Returns:
            Liste des fichiers créés
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        created_files = []
        prompts = self.generate_controller_prompts(ir, include_raw_code)
        
        for action_name, prompt in prompts.items():
            filename = f"{ir.metadata.controller_name}_{action_name}_migration.md"
            filepath = output_dir / filename
            filepath.write_text(prompt)
            created_files.append(filepath)
        
        return created_files


# =============================================================================
# Fonction utilitaire
# =============================================================================

def generate_migration_prompt(ir: IRSchema, action_name: str) -> str:
    """
    Raccourci pour générer un prompt de migration.
    
    Usage:
        ir = extract_php('UserController.php')
        prompt = generate_migration_prompt(ir, 'edit')
        # Envoie le prompt à Claude/Gemini
    """
    generator = SymfonyPromptGenerator()
    return generator.generate_action_prompt(ir, action_name)
