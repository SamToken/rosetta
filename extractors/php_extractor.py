"""
PHP Extractor pour Zend Framework 1
====================================
Extrait l'IR depuis des contrôleurs PHP legacy SANS utiliser d'IA.
Que du regex et du parsing basique.
"""

import re
from pathlib import Path
from typing import Optional
from ir.schema import (
    IRSchema, IRMetadata, SourceType,
    EntryPoint, Parameter, Visibility,
    Operation, OperationType,
    ControlBlock, DataFlow, Dependency,
    UnparsedSection, create_ir
)


class PHPExtractor:
    """
    Extracteur de code PHP legacy (Zend Framework 1).
    
    Principe : extraire le MAXIMUM sans IA, logger ce qu'on ne comprend pas.
    """
    
    # =========================================================================
    # Patterns Regex
    # =========================================================================
    
    # Classe et méthodes
    PATTERN_CLASS = re.compile(r'class\s+(\w+)Controller\s+extends')
    PATTERN_ACTION = re.compile(r'(public|protected|private)?\s*function\s+(\w+)Action\s*\(([^)]*)\)')
    
    # Base de données (Zend_Db style)
    # Backreference \1 garantit que le même type de quote ouvre et ferme la chaîne,
    # évitant la troncature sur les quotes internes du SQL (ex: WHERE status = 'active').
    PATTERN_SQL_QUERY = re.compile(r'->query\s*\(\s*(["\'])(.*?)\1', re.DOTALL)
    PATTERN_SQL_FETCHALL = re.compile(r'->fetchAll\s*\(\s*(["\'])(.*?)\1', re.DOTALL)
    PATTERN_SQL_FETCHROW = re.compile(r'->fetchRow\s*\(\s*(["\'])(.*?)\1', re.DOTALL)
    PATTERN_SQL_INSERT = re.compile(r'->insert\s*\(\s*["\'](\w+)["\']')
    PATTERN_SQL_UPDATE = re.compile(r'->update\s*\(\s*["\'](\w+)["\']')
    PATTERN_SQL_DELETE = re.compile(r'->delete\s*\(\s*["\'](\w+)["\']')
    
    # Entrées utilisateur
    PATTERN_GET = re.compile(r'\$_GET\s*\[\s*["\'](\w+)["\']\s*\]')
    PATTERN_POST = re.compile(r'\$_POST\s*\[\s*["\'](\w+)["\']\s*\]')
    PATTERN_REQUEST = re.compile(r'\$_REQUEST\s*\[\s*["\'](\w+)["\']\s*\]')
    PATTERN_PARAM = re.compile(r'(?:getParam|_getParam|getRequest\(\)->getParam)\s*\(\s*["\'](\w+)["\']')
    
    # Session
    PATTERN_SESSION_READ = re.compile(r'\$_SESSION\s*\[\s*["\'](\w+)["\']\s*\](?!\s*=)')
    PATTERN_SESSION_WRITE = re.compile(r'\$_SESSION\s*\[\s*["\'](\w+)["\']\s*\]\s*=')
    
    # Sorties
    PATTERN_REDIRECT = re.compile(r'(?:_redirect|redirect|gotoUrl|gotoRoute)\s*\(\s*["\']?([^"\')\s,]+)')
    PATTERN_RENDER = re.compile(r'(?:render|renderScript)\s*\(\s*["\']([^"\']+)["\']')
    PATTERN_VIEW_ASSIGN = re.compile(r'\$this->view->(\w+)\s*=')
    
    # Dépendances
    PATTERN_USE = re.compile(r'^use\s+(.+);', re.MULTILINE)
    PATTERN_NEW = re.compile(r'new\s+(\w+)\s*\(')
    PATTERN_SERVICE = re.compile(r'\$this->(\w+)->(?!view)')
    
    # Control flow
    PATTERN_IF = re.compile(r'if\s*\((.+?)\)\s*{', re.DOTALL)
    PATTERN_FOREACH = re.compile(r'foreach\s*\((.+?)\s+as\s+')
    
    # Pattern pour extraire le corps complet d'une action
    PATTERN_ACTION_BODY = re.compile(
        r'((?:public|protected|private)?\s*function\s+(\w+)Action\s*\([^)]*\)\s*\{)',
        re.DOTALL
    )
    
    def __init__(self, encoding: str = 'utf-8'):
        """
        Args:
            encoding: Encodage des fichiers PHP (utf-8 ou iso-8859-1 pour legacy Oracle)
        """
        self.encoding = encoding
        self._operation_counter = 0
        self._block_counter = 0
    
    def _next_op_id(self) -> str:
        self._operation_counter += 1
        return f"op_{self._operation_counter}"
    
    def _next_block_id(self) -> str:
        self._block_counter += 1
        return f"block_{self._block_counter}"
    
    # =========================================================================
    # Extraction principale
    # =========================================================================
    
    def extract(self, source_path: Path | str) -> IRSchema:
        """
        Extrait l'IR complet d'un fichier contrôleur PHP.
        
        Args:
            source_path: Chemin vers le fichier .php
            
        Returns:
            IRSchema rempli avec ce qu'on a pu extraire
        """
        source_path = Path(source_path)
        
        # Lire le fichier avec gestion encodage
        content = self._read_file(source_path)
        
        # Extraire le nom du contrôleur
        controller_name = self._extract_controller_name(content, source_path)
        
        # Créer l'IR de base
        ir = create_ir(
            source_file=str(source_path),
            controller_name=controller_name
        )
        
        # Reset counters
        self._operation_counter = 0
        self._block_counter = 0
        
        # Remplir l'IR
        ir.entry_points = self._extract_entry_points(content)
        ir.operations = self._extract_operations(content)
        ir.data_flow = self._extract_data_flow(content)
        ir.dependencies = self._extract_dependencies(content)
        ir.control_flow = self._extract_control_flow(content)
        
        # Calculer le score de confiance
        ir.metadata.confidence_score = self._calculate_confidence(ir, content)
        
        return ir
    
    def _read_file(self, path: Path) -> str:
        """Lit un fichier avec fallback sur encodage legacy."""
        try:
            return path.read_text(encoding=self.encoding)
        except UnicodeDecodeError:
            # Fallback sur ISO-8859-1 (legacy Oracle)
            return path.read_text(encoding='iso-8859-1')
    
    def _extract_controller_name(self, content: str, path: Path) -> str:
        """Extrait le nom du contrôleur."""
        match = self.PATTERN_CLASS.search(content)
        if match:
            return match.group(1)
        # Fallback sur le nom du fichier
        return path.stem.replace('Controller', '')
    
    # =========================================================================
    # Extraction des entry points (actions)
    # =========================================================================
    
    def _extract_entry_points(self, content: str) -> list[EntryPoint]:
        """Extrait toutes les actions du contrôleur avec leur code brut."""
        entry_points = []
        
        for match in self.PATTERN_ACTION.finditer(content):
            visibility_str = match.group(1) or 'public'
            action_name = match.group(2)
            params_str = match.group(3)
            
            # Parser les paramètres
            parameters = self._parse_parameters(params_str)
            
            # Deviner la route
            route_pattern = self._guess_route(action_name)
            
            # Extraire le code brut de l'action
            start_pos = match.start()
            start_line = content[:start_pos].count('\n') + 1
            raw_code, end_line = self._extract_function_body(content, start_pos)
            
            entry_point = EntryPoint(
                name=action_name,
                original_name=f"{action_name}Action",
                visibility=Visibility(visibility_str),
                parameters=parameters,
                route_pattern=route_pattern,
                http_methods=self._guess_http_methods(action_name, raw_code or content),
                raw_code=raw_code,
                start_line=start_line,
                end_line=end_line
            )
            entry_points.append(entry_point)
        
        return entry_points
    
    def _extract_function_body(self, content: str, start_pos: int) -> tuple[str, int]:
        """
        Extrait le corps complet d'une fonction en comptant les accolades.
        
        Returns:
            Tuple (code_brut, ligne_fin)
        """
        # Trouver la première accolade ouvrante
        brace_pos = content.find('{', start_pos)
        if brace_pos == -1:
            return None, 0
        
        # Compter les accolades pour trouver la fin
        depth = 0
        in_string = False
        string_char = None
        i = brace_pos
        
        while i < len(content):
            char = content[i]
            
            # Gestion des strings (ignorer les accolades dans les strings)
            if char in ('"', "'") and (i == 0 or content[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
            
            # Compter les accolades (hors strings)
            if not in_string:
                if char == '{':
                    depth += 1
                elif char == '}':
                    depth -= 1
                    if depth == 0:
                        # Trouvé la fin de la fonction
                        raw_code = content[start_pos:i+1]
                        end_line = content[:i+1].count('\n') + 1
                        return raw_code, end_line
            
            i += 1
        
        # Pas trouvé la fin (erreur de syntaxe dans le fichier source)
        return content[start_pos:], content.count('\n')
    
    def _parse_parameters(self, params_str: str) -> list[Parameter]:
        """Parse les paramètres d'une fonction."""
        if not params_str.strip():
            return []
        
        parameters = []
        for param in params_str.split(','):
            param = param.strip()
            if not param:
                continue
            
            # Pattern: ?TypeHint $name = default
            parts = param.split('=')
            name_part = parts[0].strip()
            default = parts[1].strip() if len(parts) > 1 else None
            
            # Extraire type hint et nom
            tokens = name_part.split()
            if len(tokens) >= 2:
                type_hint = tokens[0].lstrip('?')
                name = tokens[1].lstrip('$')
            else:
                type_hint = None
                name = tokens[0].lstrip('$')
            
            parameters.append(Parameter(
                name=name,
                type_hint=type_hint,
                default_value=default
            ))
        
        return parameters
    
    def _guess_route(self, action_name: str) -> str:
        """Devine la route à partir du nom de l'action."""
        # indexAction → /
        if action_name == 'index':
            return '/'
        # editAction → /edit
        return f'/{action_name.lower()}'
    
    def _guess_http_methods(self, action_name: str, content: str) -> list[str]:
        """Devine les méthodes HTTP."""
        # Si l'action contient des checks POST
        action_pattern = rf'function\s+{action_name}Action.*?(?=function\s+\w+Action|\Z)'
        action_match = re.search(action_pattern, content, re.DOTALL)
        
        if action_match:
            action_content = action_match.group(0)
            if 'isPost()' in action_content or '$_POST' in action_content:
                return ['GET', 'POST']
        
        # Actions qui suggèrent POST
        post_actions = ['save', 'create', 'update', 'delete', 'submit', 'process']
        if any(action_name.lower().startswith(p) for p in post_actions):
            return ['POST']
        
        return ['GET']
    
    # =========================================================================
    # Extraction des opérations
    # =========================================================================
    
    def _extract_operations(self, content: str) -> list[Operation]:
        """Extrait toutes les opérations métier."""
        operations = []
        
        # Opérations DB - SELECT
        for pattern in [self.PATTERN_SQL_QUERY, self.PATTERN_SQL_FETCHALL, self.PATTERN_SQL_FETCHROW]:
            for match in pattern.finditer(content):
                sql = match.group(2).strip()  # group 1 = quote char, group 2 = SQL
                operations.append(Operation(
                    id=self._next_op_id(),
                    type=OperationType.DB_READ,
                    details=sql,
                    source_line=content[:match.start()].count('\n') + 1
                ))
        
        # Opérations DB - INSERT
        for match in self.PATTERN_SQL_INSERT.finditer(content):
            operations.append(Operation(
                id=self._next_op_id(),
                type=OperationType.DB_WRITE,
                details=f"INSERT INTO {match.group(1)}",
                source_line=content[:match.start()].count('\n') + 1
            ))
        
        # Opérations DB - UPDATE
        for match in self.PATTERN_SQL_UPDATE.finditer(content):
            operations.append(Operation(
                id=self._next_op_id(),
                type=OperationType.DB_WRITE,
                details=f"UPDATE {match.group(1)}",
                source_line=content[:match.start()].count('\n') + 1
            ))
        
        # Opérations DB - DELETE
        for match in self.PATTERN_SQL_DELETE.finditer(content):
            operations.append(Operation(
                id=self._next_op_id(),
                type=OperationType.DB_DELETE,
                details=f"DELETE FROM {match.group(1)}",
                source_line=content[:match.start()].count('\n') + 1
            ))
        
        # Redirections
        for match in self.PATTERN_REDIRECT.finditer(content):
            operations.append(Operation(
                id=self._next_op_id(),
                type=OperationType.REDIRECT,
                details=match.group(1),
                source_line=content[:match.start()].count('\n') + 1
            ))
        
        # Rendus de template
        for match in self.PATTERN_RENDER.finditer(content):
            operations.append(Operation(
                id=self._next_op_id(),
                type=OperationType.RENDER,
                details=match.group(1),
                source_line=content[:match.start()].count('\n') + 1
            ))
        
        return operations
    
    # =========================================================================
    # Extraction du data flow
    # =========================================================================
    
    def _extract_data_flow(self, content: str) -> DataFlow:
        """Extrait les entrées/sorties de données."""
        inputs = set()
        outputs = set()
        session_reads = set()
        session_writes = set()
        
        # Inputs
        for pattern in [self.PATTERN_GET, self.PATTERN_POST, self.PATTERN_REQUEST, self.PATTERN_PARAM]:
            for match in pattern.finditer(content):
                inputs.add(match.group(1))
        
        # Session
        for match in self.PATTERN_SESSION_READ.finditer(content):
            session_reads.add(match.group(1))
        
        for match in self.PATTERN_SESSION_WRITE.finditer(content):
            session_writes.add(match.group(1))
        
        # Outputs (variables passées à la vue)
        for match in self.PATTERN_VIEW_ASSIGN.finditer(content):
            outputs.add(f"view.{match.group(1)}")
        
        # Types de réponse
        if self.PATTERN_REDIRECT.search(content):
            outputs.add("redirect")
        if self.PATTERN_RENDER.search(content):
            outputs.add("render")
        if 'json' in content.lower() or 'Json' in content:
            outputs.add("json")
        
        return DataFlow(
            inputs=sorted(inputs),
            outputs=sorted(outputs),
            session_reads=sorted(session_reads),
            session_writes=sorted(session_writes)
        )
    
    # =========================================================================
    # Extraction des dépendances
    # =========================================================================
    
    def _extract_dependencies(self, content: str) -> list[Dependency]:
        """Extrait les dépendances externes."""
        dependencies = []
        seen = set()
        
        # Use statements
        for match in self.PATTERN_USE.finditer(content):
            dep_name = match.group(1).strip()
            if dep_name not in seen:
                seen.add(dep_name)
                dependencies.append(Dependency(
                    name=dep_name,
                    type="use"
                ))
        
        # new ClassName()
        for match in self.PATTERN_NEW.finditer(content):
            class_name = match.group(1)
            if class_name not in seen and not class_name.startswith('Zend_'):
                seen.add(class_name)
                dependencies.append(Dependency(
                    name=class_name,
                    type="instantiation",
                    suggested_symfony=self._suggest_symfony_equivalent(class_name)
                ))
        
        # $this->service->
        for match in self.PATTERN_SERVICE.finditer(content):
            service_name = match.group(1)
            if service_name not in seen and service_name != 'view':
                seen.add(service_name)
                dependencies.append(Dependency(
                    name=service_name,
                    type="service",
                    suggested_symfony=f"{service_name.title()}Service"
                ))
        
        return dependencies
    
    def _suggest_symfony_equivalent(self, zend_class: str) -> Optional[str]:
        """Suggère l'équivalent Symfony d'une classe Zend."""
        mapping = {
            'Zend_Mail': 'Symfony\\Component\\Mailer\\Mailer',
            'Zend_Form': 'Symfony\\Component\\Form\\FormInterface',
            'Zend_Db': 'Doctrine\\DBAL\\Connection',
            'Zend_Cache': 'Symfony\\Contracts\\Cache\\CacheInterface',
            'Zend_Log': 'Psr\\Log\\LoggerInterface',
        }
        
        for zend_prefix, symfony_class in mapping.items():
            if zend_class.startswith(zend_prefix):
                return symfony_class
        
        return None
    
    # =========================================================================
    # Extraction du control flow (basique)
    # =========================================================================
    
    def _extract_control_flow(self, content: str) -> list[ControlBlock]:
        """Extrait un control flow simplifié."""
        blocks = []
        
        # Pour l'instant, on extrait juste les conditions principales
        for match in self.PATTERN_IF.finditer(content):
            condition = match.group(1).strip()
            # Nettoyer la condition
            condition = ' '.join(condition.split())  # Normaliser les espaces
            
            blocks.append(ControlBlock(
                id=self._next_block_id(),
                condition=condition
            ))
        
        return blocks
    
    # =========================================================================
    # Score de confiance
    # =========================================================================
    
    def _calculate_confidence(self, ir: IRSchema, content: str) -> float:
        """
        Calcule un score de confiance basé sur ce qu'on a pu extraire.
        
        1.0 = tout extrait
        0.5 = moitié extraite
        0.0 = rien extrait
        """
        score = 1.0
        
        # Pénalité si pas d'actions trouvées
        if not ir.entry_points:
            score -= 0.3
        
        # Pénalité si pas d'opérations
        if not ir.operations:
            score -= 0.2
        
        # Pénalité si beaucoup de code non parsé
        total_lines = content.count('\n')
        if total_lines > 0:
            # Heuristique : si on a trouvé peu d'opérations par rapport au nombre de lignes
            operations_ratio = len(ir.operations) / (total_lines / 50)  # ~1 op per 50 lines
            if operations_ratio < 0.5:
                score -= 0.2
        
        return max(0.0, min(1.0, score))


# =============================================================================
# Fonction utilitaire pour usage rapide
# =============================================================================

def extract_php(file_path: str | Path, encoding: str = 'utf-8') -> IRSchema:
    """
    Raccourci pour extraire un fichier PHP.
    
    Usage:
        ir = extract_php('controllers/UserController.php')
        print(ir.summary())
    """
    extractor = PHPExtractor(encoding=encoding)
    return extractor.extract(file_path)
