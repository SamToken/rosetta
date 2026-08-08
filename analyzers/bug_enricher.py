"""
Bug Enricher — Détection de bugs sémantiques via grille LLM structurée
=======================================================================
Complémentaire au LLMEnricher (orienté règles métier PO).

Différence fondamentale :
- LLMEnricher : 1 appel par flag, fragment minimal → règle métier PO
- BugEnricher  : 1 appel par fichier, code source complet → grille de 13 bugs techniques

Les bugs sémantiques (précédence opérateurs, variable non initialisée, paramètres
inversés, side-effects récursifs) sont invisibles à l'AST car ils nécessitent
le contexte cross-méthodes que seul le fichier complet fournit.
"""

import json
import re
from typing import Optional, TYPE_CHECKING
from ir.schema import IRSchema, BugFinding, BugCategory, BugSeverity
from analyzers.llm_enricher import TokenUsage, PRICING
from analyzers.db_relevance import method_touches_db

if TYPE_CHECKING:
    from analyzers.kb_context import KBContextProvider

# Taille max du source envoyé au LLM (~8 000 tokens input) — par chunk
MAX_SOURCE_CHARS = 32_000

SYSTEM_PROMPT = """Tu es un expert en audit de code PHP, spécialisé dans la détection de bugs sémantiques et de risques de compatibilité dans du code legacy.

Ta mission : analyser le code PHP fourni selon une GRILLE DE VÉRIFICATION en 13 catégories et retourner UNIQUEMENT les anomalies réellement présentes dans le code soumis.

RÈGLE ABSOLUE : Ne pas inventer de bugs. Chaque bug signalé doit être directement lisible dans le fragment de code fourni. Si une catégorie ne présente aucun problème, ne pas l'inclure dans la réponse.

════════════════════════════════════════
GRILLE DE VÉRIFICATION — 13 CATÉGORIES
════════════════════════════════════════

Vérifie EXPLICITEMENT chacune des catégories suivantes :

[1] UNINIT_VAR
Pattern : une variable ($replaceValue, $result, etc.) est lue dans un case/bloc sans avoir été initialisée dans CE bloc. Elle peut contenir une valeur résiduelle d'un bloc précédent du même foreach/switch.
Exemple dangereux : switch($arg) { case 'A': if(cond) { $v = x; } /* pas de else */ if($v) {...} }

[2] PHP82_COMPAT
Pattern A — propriété dynamique : $this->propNonDeclaree = ... où la propriété n'est pas dans la liste des propriétés déclarées de la classe (protected/private/public $xxx).
Pattern B — accès indexé sur false/null : $var[0] ou $var['key'] où $var est initialisée à false ou null.
Critique en PHP 8.2 (deprecated → fatal en PHP 9).

[3] OPERATOR_PRECEDENCE
Pattern : condition avec au moins 3 opérandes booléens mélangeant && et || sans parenthèses explicites autour des sous-groupes.
Exemple : if (A || B || C && D) — PHP évalue comme if (A || B || (C && D)), ce qui peut différer de l'intention.
NE PAS signaler si les parenthèses sont déjà présentes.

[4] STRPOS_LOOSE
Pattern : résultat de strpos(), stripos(), strstr(), strrpos() utilisé dans un if sans comparaison === false ou !== false.
Exemple dangereux : if (strpos($str, '/')) { ... } — faux négatif si '/' est en position 0.

[5] DATE_FORMAT
Pattern : appel date() avec un format contenant des lettres non reconnues par PHP (ex: 'yyyymmdd', 'YYYY-MM-DD').
Lettres PHP valides : Y y m d H i s A a etc. 'y' = 2 chiffres, 'Y' = 4 chiffres. Répéter 'y' comme 'yyyy' ne donne PAS l'année sur 4 chiffres.

[6] SWITCH_FALLTHROUGH
Pattern : un case dans un switch qui se termine sans break, return ou exit, et dont le case suivant fait une opération différente (pas un simple regroupement de labels).
NE PAS signaler les regroupements intentionnels (case 'A': case 'B': même code).

[7] FOREACH_NULL
Pattern : foreach($var as ...) où $var peut valoir null selon un chemin d'exécution, sans vérification is_array($var) ou !empty($var) ou isset($var) avant la boucle.

[8] SLEEP_BLOCKING
Pattern : appel à sleep() ou usleep() dans un contexte PHP synchrone, particulièrement à l'intérieur d'une boucle do/while ou for. Bloque le worker PHP pendant toute la durée.

[9] STATE_MUTATION
Pattern : $this->propNom = $valeur à l'intérieur d'une méthode qui s'appelle elle-même récursivement, ou qui est appelée par plusieurs branches du même flux. La propriété d'instance est corrompue à chaque appel imbriqué.
Attention particulière aux méthodes qui font $this->typeRessource = $type ou $this->ticketId = $id au début de leur corps.

[10] NULL_DEREF
Pattern : $obj->methode() ou $obj->propriete où $obj peut être null si une condition préalable n'est pas satisfaite, sans vérification isset($obj) ou $obj !== null avant l'appel.

[11] ARRAY_UNCHECKED
Pattern : accès à $array['cle1']['cle2'] sur un tableau retourné par une API externe ou une requête DB, sans isset() ou array_key_exists() sur les clés intermédiaires.
NE PAS signaler les accès sur des tableaux construits localement avec des clés fixes connues.

[12] FINALLY_SCOPE
Pattern : code métier important (appel API, mise à jour DB, envoi de notification) placé APRÈS un bloc try/finally dans le même flux. Si une exception est levée dans le try, le finally s'exécute mais le code APRÈS finally ne s'exécute pas — l'opération est silencieusement ignorée.

[13] PARAM_ORDER
Pattern : appel de méthode/fonction où l'ordre des arguments dans l'appel semble inversé par rapport à la signature déclarée dans le même fichier. Détecter quand les noms des paramètres dans la signature suggèrent un ordre différent de celui utilisé dans l'appel.

════════════════════════════════════════
FORMAT DE RÉPONSE OBLIGATOIRE
════════════════════════════════════════

Réponds UNIQUEMENT en JSON valide, sans texte avant ni après, sans bloc markdown :
{
  "bugs": [
    {
      "category": "<une des 13 catégories en majuscules>",
      "severity": "critical|high|medium|low",
      "method": "<nom exact de la méthode PHP concernée>",
      "fragment": "<extrait de code exact du fichier, 1 à 3 lignes max>",
      "description": "<explication précise du bug en 1 à 2 phrases>",
      "fix": "<correction minimale suggérée en 1 phrase>"
    }
  ]
}

Règles de sévérité :
- critical : peut causer une erreur fatale, un crash ou une corruption silencieuse de données en production
- high : comportement incorrect silencieux ou résultat erroné produit sans erreur visible
- medium : warning PHP ou résultat inattendu seulement dans certaines conditions
- low : risque de régression uniquement lors d'une migration vers PHP 8.2+

Catégories valides (casse exacte requise) :
UNINIT_VAR, PHP82_COMPAT, OPERATOR_PRECEDENCE, STRPOS_LOOSE, DATE_FORMAT,
SWITCH_FALLTHROUGH, FOREACH_NULL, SLEEP_BLOCKING, STATE_MUTATION, NULL_DEREF,
ARRAY_UNCHECKED, FINALLY_SCOPE, PARAM_ORDER
"""

_CATEGORY_MAP: dict[str, BugCategory] = {
    "UNINIT_VAR":          BugCategory.UNINIT_VAR,
    "PHP82_COMPAT":        BugCategory.PHP82_COMPAT,
    "OPERATOR_PRECEDENCE": BugCategory.OPERATOR_PRECEDENCE,
    "STRPOS_LOOSE":        BugCategory.STRPOS_LOOSE,
    "DATE_FORMAT":         BugCategory.DATE_FORMAT,
    "SWITCH_FALLTHROUGH":  BugCategory.SWITCH_FALLTHROUGH,
    "FOREACH_NULL":        BugCategory.FOREACH_NULL,
    "SLEEP_BLOCKING":      BugCategory.SLEEP_BLOCKING,
    "STATE_MUTATION":      BugCategory.STATE_MUTATION,
    "NULL_DEREF":          BugCategory.NULL_DEREF,
    "ARRAY_UNCHECKED":     BugCategory.ARRAY_UNCHECKED,
    "FINALLY_SCOPE":       BugCategory.FINALLY_SCOPE,
    "PARAM_ORDER":         BugCategory.PARAM_ORDER,
}

_SEVERITY_MAP: dict[str, BugSeverity] = {
    "critical": BugSeverity.CRITICAL,
    "high":     BugSeverity.HIGH,
    "medium":   BugSeverity.MEDIUM,
    "low":      BugSeverity.LOW,
}

_SEVERITY_EMOJI: dict[BugSeverity, str] = {
    BugSeverity.CRITICAL: "🔴",
    BugSeverity.HIGH:     "🟠",
    BugSeverity.MEDIUM:   "🟡",
    BugSeverity.LOW:      "🔵",
}


class BugEnricher:
    """
    Analyse le code source PHP complet avec une grille de 13 catégories de bugs techniques.
    1 appel LLM par fichier — plus efficace que flag-par-flag pour les bugs cross-méthodes.
    """

    def __init__(
        self,
        model: str = "claude-sonnet-4-6",
        kb_provider: Optional["KBContextProvider"] = None,
        table_matcher: Optional["re.Pattern"] = None,
    ):
        import anthropic
        self.client = anthropic.Anthropic()
        self.model = model
        self.usage = TokenUsage()
        self.kb_provider = kb_provider
        #: Matcher des tables de l'inventaire (même déclencheur DB que llm_enricher).
        self._table_matcher = table_matcher

    def enrich(
        self,
        ir: IRSchema,
        php_source: str,
        call_graph: Optional["CallGraphIndex"] = None,  # type: ignore[name-defined]
    ) -> IRSchema:
        """Analyse le source complet et ajoute les BugFinding à ir.bug_findings.

        Les fichiers > MAX_SOURCE_CHARS sont découpés en chunks par méthode PHP
        pour garantir qu'aucune méthode n'est silencieusement tronquée.
        """
        chunks = _chunk_source(php_source)
        bundle = call_graph.bundle_for_source(php_source) if call_graph else ""
        # Deux variantes de contexte KB (une fois par fichier) ; le choix se fait
        # par CHUNK selon son footprint DB — même déclencheur isolé que llm_enricher.
        # Ici le chunk EST ce que voit le prompt (pas de troncature 2500) : fenêtre
        # du test = fenêtre du prompt.
        kb_context = ""
        kb_context_schema = ""
        if self.kb_provider:
            filename = ir.metadata.controller_name or ""
            kb_context = self.kb_provider.context_for(filename)
            # Couche 2 : détail des tables scannées sur le source complet du fichier.
            kb_context_schema = self.kb_provider.context_for(
                filename, include_schema=True, detail_for_source=php_source
            )

        if len(chunks) > 1:
            print(f"  ⚡ Fichier volumineux — analyse en {len(chunks)} chunks "
                  f"({len(php_source):,} chars / {len(chunks)} × ≤{MAX_SOURCE_CHARS:,})")

        all_findings: list[BugFinding] = []
        for i, chunk in enumerate(chunks):
            label = ir.metadata.controller_name
            if len(chunks) > 1:
                label = f"{ir.metadata.controller_name} [chunk {i + 1}/{len(chunks)}]"
            chunk_ctx = kb_context
            if kb_context_schema and method_touches_db(chunk, self._table_matcher):
                chunk_ctx = kb_context_schema
            findings = self._analyze(chunk, label, bundle, chunk_ctx)
            all_findings.extend(findings)

        # Dédupliquer par fragment (même bug peut apparaître dans le contexte chevauchant)
        seen: set[str] = set()
        for finding in all_findings:
            key = finding.fragment[:80]
            if key not in seen:
                seen.add(key)
                ir.bug_findings.append(finding)

        return ir

    def _analyze(
        self,
        source: str,
        filename: str,
        dep_bundle: str = "",
        kb_context: str = "",
    ) -> list[BugFinding]:
        dep_section = f"\n\n{dep_bundle}" if dep_bundle else ""
        kb_section = f"\n\n{kb_context}" if kb_context else ""
        user_message = (
            f"Fichier : {filename}.php\n\n"
            f"```php\n{source}\n```"
            f"{dep_section}"
            f"{kb_section}\n\n"
            "Applique la grille complète (13 catégories). "
            "Retourne uniquement les bugs réellement présents dans CE code."
        )

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            system=[{
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": user_message}],
        )

        self.usage.input_tokens          += response.usage.input_tokens
        self.usage.output_tokens         += response.usage.output_tokens
        self.usage.cache_read_tokens     += getattr(response.usage, "cache_read_input_tokens", 0)
        self.usage.cache_creation_tokens += getattr(response.usage, "cache_creation_input_tokens", 0)

        return _parse_response(response.content[0].text.strip())


def _find_method_boundaries(lines: list[str]) -> list[tuple[int, int]]:
    """
    Retourne les (start_idx, end_idx) 0-basés de chaque méthode PHP dans le source.
    Détecte toutes les visibilités : public/private/protected/abstract/static/final.
    """
    method_re = re.compile(
        r"^\s+(?:(?:public|private|protected|abstract|static|final)\s+)*function\s+\w+"
    )
    starts = [i for i, ln in enumerate(lines) if method_re.match(ln)]
    if not starts:
        return []
    spans = []
    for i, start in enumerate(starts):
        end = starts[i + 1] - 1 if i + 1 < len(starts) else len(lines) - 1
        spans.append((start, end))
    return spans


def _chunk_source(source: str) -> list[str]:
    """
    Découpe le source PHP en chunks par méthode, chacun ≤ MAX_SOURCE_CHARS.

    Garantit qu'aucune méthode n'est tronquée en milieu de corps.
    Si une méthode seule dépasse MAX_SOURCE_CHARS, elle passe entière dans son chunk
    (on ne peut pas couper à l'intérieur d'une méthode sans perdre du contexte).
    Retourne [source] si le fichier tient en un chunk.
    """
    if len(source) <= MAX_SOURCE_CHARS:
        return [source]

    lines = source.splitlines(keepends=True)
    spans = _find_method_boundaries(lines)

    if not spans:
        # Aucune méthode détectée — fallback sur la limite dure avec marqueur
        cutoff = source.rfind("\n", 0, MAX_SOURCE_CHARS)
        if cutoff == -1:
            cutoff = MAX_SOURCE_CHARS
        return [source[:cutoff] + "\n\n// [... fichier tronqué — analyse partielle ...]"]

    # En-tête de classe = tout ce qui précède la première méthode
    header = "".join(lines[: spans[0][0]])
    header_len = len(header)

    chunks: list[str] = []
    current_parts: list[str] = []
    current_len = header_len

    for start, end in spans:
        method_text = "".join(lines[start : end + 1])
        method_len = len(method_text)

        if current_parts and current_len + method_len > MAX_SOURCE_CHARS:
            chunks.append(header + "".join(current_parts) + "}\n")
            current_parts = []
            current_len = header_len

        current_parts.append(method_text)
        current_len += method_len

    if current_parts:
        chunks.append(header + "".join(current_parts) + "}\n")

    return chunks if chunks else [source]


def _parse_response(raw: str) -> list[BugFinding]:
    raw = re.sub(r"^```\w*\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw.strip())
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if m:
        raw = m.group(0)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []

    findings: list[BugFinding] = []
    for item in data.get("bugs", []):
        cat_key = str(item.get("category", "")).strip().upper()
        category = _CATEGORY_MAP.get(cat_key)
        if category is None:
            continue
        sev_key = str(item.get("severity", "medium")).strip().lower()
        findings.append(BugFinding(
            category=category,
            severity=_SEVERITY_MAP.get(sev_key, BugSeverity.MEDIUM),
            method_name=item.get("method") or None,
            fragment=str(item.get("fragment", ""))[:500],
            description=str(item.get("description", "")),
            fix=item.get("fix") or None,
        ))
    return findings


def format_bug_findings_md(findings: list[BugFinding], title: str = "Bugs techniques détectés") -> str:
    """Formate la liste de BugFinding en Markdown (réutilisable par les générateurs)."""
    if not findings:
        return ""

    lines: list[str] = [f"## 🐛 {title}", ""]

    # Grouper par sévérité
    by_severity: dict[BugSeverity, list[BugFinding]] = {}
    for f in findings:
        by_severity.setdefault(f.severity, []).append(f)

    for sev in (BugSeverity.CRITICAL, BugSeverity.HIGH, BugSeverity.MEDIUM, BugSeverity.LOW):
        group = by_severity.get(sev, [])
        if not group:
            continue
        emoji = _SEVERITY_EMOJI[sev]
        lines.append(f"### {emoji} {sev.value.capitalize()} ({len(group)})")
        lines.append("")
        for bug in group:
            method = f"`{bug.method_name}()`" if bug.method_name else "méthode inconnue"
            cat_label = bug.category.value.replace("_", " ").title()
            lines.append(f"- **[{cat_label}]** dans {method}")
            lines.append(f"  - {bug.description}")
            lines.append(f"  - Fragment : `{bug.fragment[:120]}`")
            if bug.fix:
                lines.append(f"  - 💡 Fix : {bug.fix}")
        lines.append("")

    return "\n".join(lines)
