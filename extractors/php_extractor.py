"""
PHP Extractor — AST-based via tree-sitter
==========================================
Extrait l'IR depuis des fichiers PHP legacy (Controllers, Services, Helpers…)
en utilisant un vrai AST, pas du regex sur le texte brut.

Contrat avec le reste du système : IRSchema inchangé.
Les opérations SQL, data_flow et dépendances restent en regex (fiables, rapides).
"""

import re
from pathlib import Path
from typing import Optional

import tree_sitter_php as tsphp
from tree_sitter import Language, Parser

from ir.schema import (
    IRSchema, IRMetadata, SourceType,
    EntryPoint, Parameter, Visibility,
    Operation, OperationType,
    ControlBlock, DataFlow, Dependency,
    UnparsedSection, create_ir
)

PHP_LANGUAGE = Language(tsphp.language_php())


class PHPExtractor:
    """
    Extracteur de code PHP legacy basé sur tree-sitter.

    Principe : AST pour la structure (méthodes, control flow),
    regex pour les patterns de données (SQL, session, services).
    """

    # =========================================================================
    # Patterns regex — opérations SQL et data flow (inchangés)
    # =========================================================================

    PATTERN_SQL_QUERY    = re.compile(r'->query\s*\(\s*(["\'])(.*?)\1', re.DOTALL)
    PATTERN_SQL_FETCHALL = re.compile(r'->fetchAll\s*\(\s*(["\'])(.*?)\1', re.DOTALL)
    PATTERN_SQL_FETCHROW = re.compile(r'->fetchRow\s*\(\s*(["\'])(.*?)\1', re.DOTALL)
    PATTERN_SQL_INSERT   = re.compile(r'->insert\s*\(\s*["\'](\w+)["\']')
    PATTERN_SQL_UPDATE   = re.compile(r'->update\s*\(\s*["\'](\w+)["\']')
    PATTERN_SQL_DELETE   = re.compile(r'->delete\s*\(\s*["\'](\w+)["\']')

    PATTERN_GET     = re.compile(r'\$_GET\s*\[\s*["\'](\w+)["\']\s*\]')
    PATTERN_POST    = re.compile(r'\$_POST\s*\[\s*["\'](\w+)["\']\s*\]')
    PATTERN_REQUEST = re.compile(r'\$_REQUEST\s*\[\s*["\'](\w+)["\']\s*\]')
    PATTERN_PARAM   = re.compile(r'(?:getParam|_getParam|getRequest\(\)->getParam)\s*\(\s*["\'](\w+)["\']')

    PATTERN_SESSION_READ  = re.compile(r'\$_SESSION\s*\[\s*["\'](\w+)["\']\s*\](?!\s*=)')
    PATTERN_SESSION_WRITE = re.compile(r'\$_SESSION\s*\[\s*["\'](\w+)["\']\s*\]\s*=')

    PATTERN_REDIRECT    = re.compile(r'(?:_redirect|redirect|gotoUrl|gotoRoute)\s*\(\s*["\']?([^"\')\s,]+)')
    PATTERN_RENDER      = re.compile(r'(?:render|renderScript)\s*\(\s*["\']([^"\']+)["\']')
    PATTERN_VIEW_ASSIGN = re.compile(r'\$this->view->(\w+)\s*=')

    PATTERN_USE     = re.compile(r'^use\s+(.+);', re.MULTILINE)
    PATTERN_NEW     = re.compile(r'new\s+(\w+)\s*\(')
    PATTERN_SERVICE = re.compile(r'\$this->(\w+)->(?!view)')

    def __init__(self, encoding: str = 'utf-8'):
        self.encoding = encoding
        self._parser = Parser(PHP_LANGUAGE)
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
        source_path = Path(source_path)
        content = self._read_file(source_path)
        file_type = self._detect_file_type(content, source_path)
        class_name = self._extract_class_name(content, source_path)

        ir = create_ir(source_file=str(source_path), controller_name=class_name)
        ir.metadata.file_type = file_type

        self._operation_counter = 0
        self._block_counter = 0

        content_bytes = content.encode('utf-8')
        tree = self._parser.parse(content_bytes)
        root = tree.root_node

        ir.entry_points = self._extract_entry_points_ast(root, content_bytes, content, file_type)
        ir.control_flow = self._extract_control_flow_ast(root, content_bytes, content)
        ir.operations   = self._extract_operations(content)
        ir.data_flow    = self._extract_data_flow(content)
        ir.dependencies = self._extract_dependencies(content)

        ir.metadata.confidence_score = self._calculate_confidence(ir, content)

        return ir

    def _read_file(self, path: Path) -> str:
        try:
            return path.read_text(encoding=self.encoding)
        except UnicodeDecodeError:
            return path.read_text(encoding='iso-8859-1')

    def _detect_file_type(self, content: str, path: Path) -> str:
        stem = path.stem
        if 'Controller' in stem: return 'controller'
        if 'Service'    in stem: return 'service'
        if 'Helper'     in stem: return 'helper'
        if 'Tools'      in stem or 'Tool' in stem: return 'tools'
        if 'Repository' in stem: return 'repository'
        return 'unknown'

    def _extract_class_name(self, content: str, path: Path) -> str:
        for pattern in (
            r'class\s+(\w+)Controller\s+extends',
            r'class\s+(\w+)Service\b',
            r'class\s+(\w+)\b',
        ):
            m = re.search(pattern, content)
            if m:
                return m.group(1)
        return path.stem.replace('Controller', '').replace('Service', '')

    # =========================================================================
    # AST helpers
    # =========================================================================

    def _find_nodes(self, node, node_type: str) -> list:
        """Parcours récursif — retourne tous les nœuds du type demandé."""
        results = []
        if node.type == node_type:
            results.append(node)
        for child in node.children:
            results.extend(self._find_nodes(child, node_type))
        return results

    def _get_visibility(self, method_node) -> str:
        for child in method_node.children:
            if child.type == 'visibility_modifier':
                return child.text.decode('utf-8')
        return 'public'

    def _node_text(self, node, content_bytes: bytes) -> str:
        return content_bytes[node.start_byte:node.end_byte].decode('utf-8', errors='replace')

    # =========================================================================
    # Entry points — AST
    # =========================================================================

    def _extract_entry_points_ast(
        self,
        root_node,
        content_bytes: bytes,
        content: str,
        file_type: str,
    ) -> list[EntryPoint]:
        entry_points = []

        for method in self._find_nodes(root_node, 'method_declaration'):
            name_node = next(
                (c for c in method.children if c.type == 'name'), None
            )
            if not name_node:
                continue
            method_name = self._node_text(name_node, content_bytes)

            # Méthodes magic → ignorées partout
            if method_name.startswith('__'):
                continue

            visibility = self._get_visibility(method)

            if file_type == 'controller':
                # Seulement les *Action(), n'importe quelle visibilité
                if not method_name.endswith('Action'):
                    continue
                clean_name = method_name[:-len('Action')]
            else:
                # Services/Helpers/Tools : méthodes publiques uniquement
                if visibility != 'public':
                    continue
                clean_name = method_name

            raw_code = self._node_text(method, content_bytes)
            start_line = method.start_point[0] + 1
            end_line   = method.end_point[0] + 1

            if file_type == 'controller':
                route   = self._guess_route(clean_name)
                methods = self._guess_http_methods(method, content_bytes, clean_name)
            else:
                route   = None
                methods = []

            entry_points.append(EntryPoint(
                name=clean_name,
                original_name=method_name,
                visibility=Visibility(visibility),
                parameters=self._extract_params_ast(method, content_bytes),
                route_pattern=route,
                http_methods=methods,
                raw_code=raw_code,
                start_line=start_line,
                end_line=end_line,
            ))

        return entry_points

    def _extract_params_ast(self, method_node, content_bytes: bytes) -> list[Parameter]:
        params = []
        fp = next(
            (c for c in method_node.children if c.type == 'formal_parameters'),
            None,
        )
        if not fp:
            return params
        for p in fp.children:
            if p.type != 'simple_parameter':
                continue
            var_node = next(
                (c for c in p.children if c.type == 'variable_name'), None
            )
            if not var_node:
                continue
            name = self._node_text(var_node, content_bytes).lstrip('$')

            type_node = next(
                (c for c in p.children
                 if c.type in ('primitive_type', 'named_type', 'optional_type',
                               'union_type', 'intersection_type')),
                None,
            )
            type_hint = self._node_text(type_node, content_bytes) if type_node else None

            eq_idx = next(
                (i for i, c in enumerate(p.children) if c.type == '='), -1
            )
            default = None
            if eq_idx != -1 and eq_idx + 1 < len(p.children):
                default = self._node_text(p.children[eq_idx + 1], content_bytes)

            params.append(Parameter(name=name, type_hint=type_hint, default_value=default))
        return params

    def _guess_route(self, action_name: str) -> str:
        return '/' if action_name == 'index' else f'/{action_name.lower()}'

    def _guess_http_methods(self, method_node, content_bytes: bytes, action_name: str) -> list[str]:
        body_text = self._node_text(method_node, content_bytes)
        if 'isPost()' in body_text or '$_POST' in body_text:
            return ['GET', 'POST']
        post_actions = ('save', 'create', 'update', 'delete', 'submit', 'process')
        if any(action_name.lower().startswith(p) for p in post_actions):
            return ['POST']
        return ['GET']

    # =========================================================================
    # Control flow — AST
    # =========================================================================

    def _extract_control_flow_ast(
        self,
        root_node,
        content_bytes: bytes,
        content: str,
    ) -> list[ControlBlock]:
        blocks = []
        all_lines = content.split('\n')

        for node in self._find_nodes(root_node, 'if_statement'):
            cond_node = node.child_by_field_name('condition')
            if not cond_node:
                continue

            # Condition sans parenthèses externes
            condition = self._node_text(cond_node, content_bytes).strip()
            if condition.startswith('(') and condition.endswith(')'):
                condition = condition[1:-1].strip()
            condition = ' '.join(condition.split())

            # true_branch — toujours présent si le nœud existe
            body_node = node.child_by_field_name('body')
            true_branch = "défini" if body_node else None

            # false_branch — else_clause ou else_if_clause
            false_branch = None
            for child in node.children:
                if child.type in ('else_clause', 'else_if_clause'):
                    false_branch = "défini"
                    break

            line_num = node.start_point[0] + 1
            ctx_start = max(0, line_num - 3)
            ctx_end   = min(len(all_lines), line_num + 3)
            raw_context = '\n'.join(all_lines[ctx_start:ctx_end])

            blocks.append(ControlBlock(
                id=self._next_block_id(),
                condition=condition,
                true_branch=true_branch,
                false_branch=false_branch,
                source_line=line_num,
                raw_context=raw_context,
            ))

        return blocks

    # =========================================================================
    # Opérations, data flow, dépendances — regex (inchangés)
    # =========================================================================

    def _extract_operations(self, content: str) -> list[Operation]:
        operations = []

        for pattern in (self.PATTERN_SQL_QUERY, self.PATTERN_SQL_FETCHALL, self.PATTERN_SQL_FETCHROW):
            for match in pattern.finditer(content):
                operations.append(Operation(
                    id=self._next_op_id(),
                    type=OperationType.DB_READ,
                    details=match.group(2).strip(),
                    source_line=content[:match.start()].count('\n') + 1,
                ))

        for match in self.PATTERN_SQL_INSERT.finditer(content):
            operations.append(Operation(
                id=self._next_op_id(),
                type=OperationType.DB_WRITE,
                details=f"INSERT INTO {match.group(1)}",
                source_line=content[:match.start()].count('\n') + 1,
            ))

        for match in self.PATTERN_SQL_UPDATE.finditer(content):
            operations.append(Operation(
                id=self._next_op_id(),
                type=OperationType.DB_WRITE,
                details=f"UPDATE {match.group(1)}",
                source_line=content[:match.start()].count('\n') + 1,
            ))

        for match in self.PATTERN_SQL_DELETE.finditer(content):
            operations.append(Operation(
                id=self._next_op_id(),
                type=OperationType.DB_DELETE,
                details=f"DELETE FROM {match.group(1)}",
                source_line=content[:match.start()].count('\n') + 1,
            ))

        for match in self.PATTERN_REDIRECT.finditer(content):
            operations.append(Operation(
                id=self._next_op_id(),
                type=OperationType.REDIRECT,
                details=match.group(1),
                source_line=content[:match.start()].count('\n') + 1,
            ))

        for match in self.PATTERN_RENDER.finditer(content):
            operations.append(Operation(
                id=self._next_op_id(),
                type=OperationType.RENDER,
                details=match.group(1),
                source_line=content[:match.start()].count('\n') + 1,
            ))

        return operations

    def _extract_data_flow(self, content: str) -> DataFlow:
        inputs, outputs, session_reads, session_writes = set(), set(), set(), set()

        for pattern in (self.PATTERN_GET, self.PATTERN_POST, self.PATTERN_REQUEST, self.PATTERN_PARAM):
            for match in pattern.finditer(content):
                inputs.add(match.group(1))

        for match in self.PATTERN_SESSION_READ.finditer(content):
            session_reads.add(match.group(1))
        for match in self.PATTERN_SESSION_WRITE.finditer(content):
            session_writes.add(match.group(1))

        for match in self.PATTERN_VIEW_ASSIGN.finditer(content):
            outputs.add(f"view.{match.group(1)}")
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
            session_writes=sorted(session_writes),
        )

    def _extract_dependencies(self, content: str) -> list[Dependency]:
        dependencies = []
        seen: set[str] = set()

        for match in self.PATTERN_USE.finditer(content):
            dep_name = match.group(1).strip()
            if dep_name not in seen:
                seen.add(dep_name)
                dependencies.append(Dependency(name=dep_name, type="use"))

        for match in self.PATTERN_NEW.finditer(content):
            class_name = match.group(1)
            if class_name not in seen and not class_name.startswith('Zend_'):
                seen.add(class_name)
                dependencies.append(Dependency(
                    name=class_name,
                    type="instantiation",
                    suggested_symfony=self._suggest_symfony_equivalent(class_name),
                ))

        for match in self.PATTERN_SERVICE.finditer(content):
            service_name = match.group(1)
            if service_name not in seen and service_name != 'view':
                seen.add(service_name)
                dependencies.append(Dependency(
                    name=service_name,
                    type="service",
                    suggested_symfony=f"{service_name.title()}Service",
                ))

        return dependencies

    def _suggest_symfony_equivalent(self, zend_class: str) -> Optional[str]:
        mapping = {
            'Zend_Mail':  'Symfony\\Component\\Mailer\\Mailer',
            'Zend_Form':  'Symfony\\Component\\Form\\FormInterface',
            'Zend_Db':    'Doctrine\\DBAL\\Connection',
            'Zend_Cache': 'Symfony\\Contracts\\Cache\\CacheInterface',
            'Zend_Log':   'Psr\\Log\\LoggerInterface',
        }
        for prefix, equiv in mapping.items():
            if zend_class.startswith(prefix):
                return equiv
        return None

    # =========================================================================
    # Score de confiance
    # =========================================================================

    def _calculate_confidence(self, ir: IRSchema, content: str) -> float:
        score = 1.0
        if not ir.entry_points:
            score -= 0.3
        if not ir.operations:
            score -= 0.2
        total_lines = content.count('\n')
        if total_lines > 0:
            ratio = len(ir.operations) / (total_lines / 50)
            if ratio < 0.5:
                score -= 0.2
        return max(0.0, min(1.0, score))


# =============================================================================
# Fonction utilitaire
# =============================================================================

def extract_php(file_path: str | Path, encoding: str = 'utf-8') -> IRSchema:
    return PHPExtractor(encoding=encoding).extract(file_path)
