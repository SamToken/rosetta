"""
Call Graph Index — Index des signatures de méthodes PHP d'un répertoire
=======================================================================
Scanne un répertoire PHP et construit un index des signatures de méthodes.

Usage :
    from analyzers.call_graph import CallGraphIndex
    from pathlib import Path

    index = CallGraphIndex.build(Path("/src/Service"), cache_path=Path(".callgraph.json"))
    print(f"{len(index)} méthodes indexées")

    # Injecté dans BugEnricher : bundle des signatures appelées depuis un source
    bundle = index.bundle_for_source(php_source)

Valeur :
    - BugEnricher voit les signatures des dépendances → PARAM_ORDER, NULL_DEREF détectables
    - LLMEnricher voit le contexte complet de la méthode → règles métier mieux extraites
"""

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

import tree_sitter_php as tsphp
from tree_sitter import Language, Parser

_PHP_LANGUAGE = Language(tsphp.language_php())
_BODY_SNIPPET_LINES = 10   # Lignes du corps incluses dans le bundle
_MAX_BUNDLE_METHODS  = 8   # Max de méthodes par bundle LLM

# Version du schéma du cache .callgraph.json. Un bump force la réindexation au
# chargement (le format a changé). v2 ajoute called_names (index inverse code mort) ;
# v3 ajoute callers_by_target (arêtes inverses résolues « appelé par »).
_CACHE_SCHEMA_VERSION = 3

# Patterns d'extraction des appels de méthodes depuis un source PHP
_RE_PROP_CALL   = re.compile(r'\$this->(\w+)->(\w+)\s*\(')   # $this->svc->method(
_RE_SELF_CALL   = re.compile(r'\$this->(\w+)\s*\(')           # $this->method( (interne)
_RE_VAR_CALL    = re.compile(r'\$(?!this\b)(\w+)->(\w+)\s*\(')  # $var->method(
_RE_STATIC_CALL = re.compile(r'\b([A-Z][a-zA-Z0-9]+)::(\w+)\s*\(')  # Class::method(
_RE_DOCBLOCK    = re.compile(r'/\*\*.*?\*/', re.DOTALL)
_RE_CLASS_NAME  = re.compile(r'\bclass\s+(\w+)')


@dataclass
class MethodSignature:
    """Signature et fragment de corps d'une méthode PHP."""
    class_name: str
    method_name: str
    file_path: str
    signature: str          # "public function foo(string $a, int $b): bool"
    docblock: Optional[str] # Docblock /** ... */ précédant la méthode, si présent
    body_snippet: str       # Premières BODY_SNIPPET_LINES lignes du corps

    def to_compact(self, max_body_chars: int = 350) -> str:
        short_file = Path(self.file_path).name
        parts = [f"// {self.class_name} ({short_file})"]
        if self.docblock:
            doc = self.docblock.strip()
            if len(doc) > 160:
                doc = doc[:160] + " ..."
            parts.append(doc)
        parts.append(self.signature + " {")
        snippet = self.body_snippet.strip()[:max_body_chars]
        if snippet:
            parts.append(snippet)
        parts.append("    // ...")
        parts.append("}")
        return "\n".join(parts)


class CallGraphIndex:
    """
    Index des signatures de méthodes d'un répertoire source PHP.

    Construction : `CallGraphIndex.build(php_root)` — scan récursif des .php.
    Lookup :       `index.resolve(method_name, class_hint)` → MethodSignature | None
    Bundle :       `index.bundle_for_source(php_source)` → bloc texte pour prompt LLM
    """

    def __init__(self) -> None:
        # method_name.lower() → [MethodSignature, ...]  (plusieurs classes peuvent avoir la même)
        self._by_method: dict[str, list[MethodSignature]] = {}
        # "ClassName::methodName" → MethodSignature  (unicité)
        self._by_class_method: dict[str, MethodSignature] = {}
        # Index inverse : noms de méthodes (lower) apparaissant comme CIBLE d'appel
        # quelque part dans l'arbre. Base de la détection de code mort (#4).
        self._called_names: set[str] = set()
        # Arêtes inverses résolues : "TargetClass::method" → {"CallerClass::method"}.
        # Base du « appelé par » et de la vue par feature (#3).
        self._callers_by_target: dict[str, set[str]] = {}

    # =========================================================================
    # Construction
    # =========================================================================

    @classmethod
    def build(
        cls,
        php_root: Path,
        cache_path: Optional[Path] = None,
        force_rebuild: bool = False,
    ) -> "CallGraphIndex":
        """
        Scanne php_root récursivement, indexe toutes les méthodes PHP.
        Si cache_path fourni et non-vide, charge depuis le cache sauf si force_rebuild.
        """
        if not force_rebuild and cache_path and cache_path.exists():
            try:
                return cls._load(cache_path)
            except Exception:
                pass  # cache corrompu → rebuild

        idx = cls()
        parser = Parser(_PHP_LANGUAGE)

        php_files = sorted(php_root.rglob("*.php"))
        # Passe 1 : indexer les définitions (nécessaire avant de résoudre les arêtes)
        for php_file in php_files:
            try:
                idx._index_file(php_file, parser)
            except Exception:
                pass  # ignore les fichiers non parsables
        # Passe 2 : arêtes inverses « appelé par » — resolve_strict a besoin de
        # l'index complet (les cibles peuvent être dans d'autres fichiers).
        for php_file in php_files:
            try:
                idx._index_edges(php_file, parser)
            except Exception:
                pass

        if cache_path:
            try:
                idx._save(cache_path)
            except Exception:
                pass

        return idx

    def _index_file(self, path: Path, parser: Parser) -> None:
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return

        # Index inverse : accumuler les cibles d'appel de CE fichier, qu'il
        # définisse une classe ou non (un fichier peut n'appeler que des méthodes).
        for called_method, _hint in _extract_called_methods(content):
            self._called_names.add(called_method.lower())

        class_name = _extract_class_name(content)
        if not class_name:
            return

        content_bytes = content.encode("utf-8")
        tree = parser.parse(content_bytes)

        for node in _find_nodes(tree.root_node, "method_declaration"):
            sig = self._extract_signature(node, content_bytes, class_name, str(path))
            if sig is None:
                continue
            key_method = sig.method_name.lower()
            key_cm = f"{class_name}::{sig.method_name}"
            self._by_method.setdefault(key_method, []).append(sig)
            self._by_class_method[key_cm] = sig

    def _index_edges(self, path: Path, parser: Parser) -> None:
        """Passe 2 : arêtes inverses résolues. Pour chaque méthode, résout ses
        appels typés vers une classe certaine et enregistre l'arête inverse
        target ← caller. À n'appeler qu'après l'indexation complète des définitions."""
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return
        class_name = _extract_class_name(content)
        if not class_name:
            return

        from extractors.php_extractor import extract_property_types_from_source
        try:
            property_types = extract_property_types_from_source(content)
        except Exception:
            property_types = {}

        content_bytes = content.encode("utf-8")
        tree = parser.parse(content_bytes)

        for node in _find_nodes(tree.root_node, "method_declaration"):
            name_node = next((c for c in node.children if c.type == "name"), None)
            if name_node is None:
                continue
            caller_method = content_bytes[name_node.start_byte:name_node.end_byte].decode("utf-8")
            if caller_method.startswith("__"):
                continue
            body = content_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="replace")
            caller = f"{class_name}::{caller_method}"
            for method, hint in _extract_called_methods(body, property_types):
                if not hint:
                    continue
                sig = self.resolve_strict(method, hint)
                if sig is None:
                    continue
                target = f"{sig.class_name}::{sig.method_name}"
                if target == caller:
                    continue  # ignore la récursion directe
                self._callers_by_target.setdefault(target, set()).add(caller)

    def _extract_signature(
        self,
        node,
        content_bytes: bytes,
        class_name: str,
        file_path: str,
    ) -> Optional[MethodSignature]:
        name_node = next((c for c in node.children if c.type == "name"), None)
        if not name_node:
            return None
        method_name = content_bytes[name_node.start_byte:name_node.end_byte].decode("utf-8")
        if method_name.startswith("__"):
            return None  # magic methods non pertinentes

        body_node = next((c for c in node.children if c.type == "compound_statement"), None)
        if body_node:
            raw_sig = content_bytes[node.start_byte:body_node.start_byte].decode("utf-8", errors="replace")
            body_text = content_bytes[body_node.start_byte:body_node.end_byte].decode("utf-8", errors="replace")
            body_lines = body_text.split("\n")[1 : _BODY_SNIPPET_LINES + 1]  # skip "{"
            body_snippet = "\n".join(body_lines)
        else:
            raw_sig = content_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="replace")
            body_snippet = ""

        # Normalise les espaces dans la signature
        signature = re.sub(r"\s+", " ", raw_sig.strip())[:300]

        # Docblock précédant la méthode (cherche dans les 400 chars précédents)
        method_start = node.start_byte
        preceding = content_bytes[max(0, method_start - 400):method_start].decode("utf-8", errors="replace")
        docblock = None
        for m in _RE_DOCBLOCK.finditer(preceding):
            docblock = m.group(0)  # dernier match = le plus proche

        return MethodSignature(
            class_name=class_name,
            method_name=method_name,
            file_path=file_path,
            signature=signature,
            docblock=docblock,
            body_snippet=body_snippet[:600],
        )

    # =========================================================================
    # Lookup
    # =========================================================================

    def resolve(
        self,
        method_name: str,
        class_hint: Optional[str] = None,
    ) -> Optional[MethodSignature]:
        """
        Résout un appel de méthode.

        class_hint : nom de classe supposé (depuis l'appel Class::method ou depuis
                     la heuristique propName → PropName).
        """
        if class_hint:
            # Cherche d'abord la correspondance exacte ClassName::methodName
            key = f"{class_hint}::{method_name}"
            if key in self._by_class_method:
                return self._by_class_method[key]
            # Suffixes courants : Service, Repository, Helper, Manager
            for suffix in ("Service", "Repository", "Helper", "Manager", "Tools"):
                key = f"{class_hint}{suffix}::{method_name}"
                if key in self._by_class_method:
                    return self._by_class_method[key]

        candidates = self._by_method.get(method_name.lower(), [])
        if not candidates:
            return None
        return candidates[0]

    def resolve_strict(
        self,
        method_name: str,
        class_hint: Optional[str],
    ) -> Optional[MethodSignature]:
        """Comme resolve() mais SANS fallback par nom : ne renvoie une signature
        que si la classe correspond exactement (+ suffixes courants). Utilisé pour
        les arêtes d'appel cross-fichier fiables (vue par feature #3) — mieux vaut
        aucune arête qu'une arête fausse."""
        if not class_hint:
            return None
        key = f"{class_hint}::{method_name}"
        if key in self._by_class_method:
            return self._by_class_method[key]
        for suffix in ("Service", "Repository", "Helper", "Manager", "Tools"):
            key = f"{class_hint}{suffix}::{method_name}"
            if key in self._by_class_method:
                return self._by_class_method[key]
        return None

    def __len__(self) -> int:
        return len(self._by_class_method)

    def __bool__(self) -> bool:
        return len(self._by_class_method) > 0

    # =========================================================================
    # Reachability — détection de code mort (#4)
    # =========================================================================

    def is_referenced(self, method_name: str) -> bool:
        """True si method_name apparaît comme cible d'appel quelque part dans l'arbre.

        Résolution par NOM (pas par type) : volontairement conservateur. Tout
        `->method(` compte comme référence, y compris les appels polymorphes via
        interface. On sous-signale le code mort (sûr) plutôt que de le sur-signaler.
        """
        return method_name.lower() in self._called_names

    def callers_of(self, class_name: str, method_name: str) -> list[str]:
        """« Appelé par » (#3) : liste triée des "Class::method" qui appellent
        `class_name::method_name`, via les arêtes résolues (match de type exact)."""
        return sorted(self._callers_by_target.get(f"{class_name}::{method_name}", set()))

    def dead_code_candidates(
        self,
        is_entrypoint=None,
    ) -> list[MethodSignature]:
        """Méthodes DÉFINIES mais jamais appelées dans l'arbre indexé.

        is_entrypoint(sig) -> bool : prédicat optionnel pour exclure les points
        d'entrée framework (ex : *Action appelés par le routing, magic __*) qui
        sont invoqués hors code et ne sont donc jamais de vraies références.

        Heuristique conservatrice — un candidat est « suspecté » mort, pas certain :
        le dispatch dynamique, les templates .phtml et la DI peuvent référencer une
        méthode sans site d'appel statique visible.
        """
        candidates: list[MethodSignature] = []
        for sig in self._by_class_method.values():
            if is_entrypoint is not None and is_entrypoint(sig):
                continue
            if not self.is_referenced(sig.method_name):
                candidates.append(sig)
        return candidates


    # =========================================================================
    # Bundle pour injection dans le prompt LLM
    # =========================================================================

    def bundle_for_source(
        self,
        php_source: str,
        max_methods: int = _MAX_BUNDLE_METHODS,
    ) -> str:
        """
        Extrait les appels de méthodes du source PHP, résout leurs signatures
        depuis l'index et retourne un bloc texte prêt pour injection dans un prompt.

        Retourne une chaîne vide si aucune dépendance n'est résoluble.
        """
        # Résolution de type des propriétés (#1 étape B) : $this->prop->method()
        # devient une classe certaine plutôt que PascalCase(prop) approximatif.
        try:
            from extractors.php_extractor import extract_property_types_from_source
            property_types = extract_property_types_from_source(php_source)
        except Exception:
            property_types = {}
        calls = _extract_called_methods(php_source, property_types)

        resolved: dict[str, MethodSignature] = {}
        for method_name, class_hint in calls:
            if method_name in resolved:
                continue
            sig = self.resolve(method_name, class_hint)
            if sig:
                resolved[method_name] = sig
            if len(resolved) >= max_methods:
                break

        if not resolved:
            return ""

        lines = [
            "==== SIGNATURES DES MÉTHODES APPELÉES ====",
            f"[{len(resolved)} méthode(s) résolue(s) depuis l'index du codebase]",
            "",
        ]
        for sig in resolved.values():
            lines.append(sig.to_compact())
            lines.append("")

        return "\n".join(lines)

    # =========================================================================
    # Persistance (cache JSON)
    # =========================================================================

    def _save(self, path: Path) -> None:
        data = {
            "schema_version": _CACHE_SCHEMA_VERSION,
            "by_method": {
                k: [asdict(s) for s in v]
                for k, v in self._by_method.items()
            },
            "by_class_method": {
                k: asdict(v)
                for k, v in self._by_class_method.items()
            },
            "called_names": sorted(self._called_names),
            "callers_by_target": {
                k: sorted(v) for k, v in self._callers_by_target.items()
            },
        }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def _load(cls, path: Path) -> "CallGraphIndex":
        data = json.loads(path.read_text(encoding="utf-8"))
        # Cache d'un schéma antérieur (ex : sans called_names) → on refuse, build()
        # rattrape en réindexant. Évite un index inverse silencieusement vide.
        if data.get("schema_version") != _CACHE_SCHEMA_VERSION:
            raise ValueError(
                f"cache callgraph schéma v{data.get('schema_version')} "
                f"≠ v{_CACHE_SCHEMA_VERSION} attendu — réindexation requise"
            )
        idx = cls()
        for k, sigs in data["by_method"].items():
            idx._by_method[k] = [MethodSignature(**s) for s in sigs]
        for k, sig in data["by_class_method"].items():
            idx._by_class_method[k] = MethodSignature(**sig)
        idx._called_names = set(data.get("called_names", []))
        idx._callers_by_target = {
            k: set(v) for k, v in data.get("callers_by_target", {}).items()
        }
        return idx


# =============================================================================
# Helpers module-level
# =============================================================================

def _extract_class_name(content: str) -> Optional[str]:
    m = _RE_CLASS_NAME.search(content)
    return m.group(1) if m else None


def _find_nodes(node, node_type: str) -> list:
    results = []
    stack = [node]
    while stack:
        current = stack.pop()
        if current.type == node_type:
            results.append(current)
        stack.extend(current.children)
    return results


def _extract_called_methods(
    source: str,
    property_types: Optional[dict[str, str]] = None,
) -> list[tuple[str, Optional[str]]]:
    """
    Retourne une liste de (method_name, class_hint_or_None).

    Patterns détectés :
    - $this->svc->method(  → class_hint = property_types[svc] si connu (type
                             certain, #1 étape B), sinon heuristique PascalCase(svc)
    - Class::method(       → class_hint = Class
    - $var->method(        → class_hint = None
    """
    property_types = property_types or {}
    seen: set[str] = set()
    results: list[tuple[str, Optional[str]]] = []

    def _add(method: str, hint: Optional[str]) -> None:
        if method not in seen:
            seen.add(method)
            results.append((method, hint))

    # $this->propName->methodName( — type résolu si connu, sinon PascalCase
    prop_names: set[str] = set()
    for m in _RE_PROP_CALL.finditer(source):
        prop, method = m.group(1), m.group(2)
        prop_names.add(prop)
        class_hint = property_types.get(prop)
        if not class_hint:
            class_hint = prop[0].upper() + prop[1:] if prop else None
        _add(method, class_hint)

    # $this->method( — appels internes (pas une propriété two-level)
    for m in _RE_SELF_CALL.finditer(source):
        method = m.group(1)
        if method not in prop_names:  # exclure $this->svc (qui n'est pas un appel direct)
            _add(method, None)

    # ClassName::staticMethod(
    for m in _RE_STATIC_CALL.finditer(source):
        class_name, method = m.group(1), m.group(2)
        if class_name not in ("parent", "self", "static"):
            _add(method, class_name)

    # $var->method( (hors $this)
    for m in _RE_VAR_CALL.finditer(source):
        method = m.group(2)
        _add(method, None)

    return results
