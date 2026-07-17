"""
LLM Enricher — Enrichissement des flags via Claude
====================================================
Envoie chaque flag au LLM pour extraire la règle métier.

Principes :
- Le LLM ne reçoit JAMAIS le fichier PHP complet
- Il reçoit uniquement flag.fragment (fragment minimal)
- Chaque réponse est marquée source="llm" et validated=False
- Le prompt système est mis en cache (prompt caching Anthropic)
"""

import json
import re
from dataclasses import dataclass, field
from typing import Callable, Optional, TYPE_CHECKING
from ir.schema import IRSchema, Flag, LLMInsight, KBToken
from analyzers.constants import STOP_TOKENS

if TYPE_CHECKING:
    from analyzers.kb_context import KBContextProvider

SYSTEM_PROMPT = """Tu es un Business Analyst senior spécialisé en reverse engineering de logique métier sur des systèmes d'information télécom.

Ta mission unique : extraire la règle métier implicite qui se cache derrière chaque comportement observé dans ce système, et la formuler en langage compréhensible par un Product Owner non-technique.

Tu travailles dans le cadre d'un audit fonctionnel préparatoire à une migration de système. Le livrable de cet audit doit permettre à un Product Owner de prendre des décisions de priorisation sans avoir besoin de comprendre le code source.

Règles de conduite strictes :
- Tu n'es pas un développeur ; tu es un traducteur entre le système existant et les parties prenantes métier
- Tu ne mentionnes jamais de langage de programmation, de framework, ni de terme technique dans ta réponse
- Tu traduis chaque comportement observé en termes de processus, de règle ou de décision métier
- Tu ne fais jamais de recommandation d'amélioration technique
- Tu expliques uniquement le "quoi" et le "pourquoi" métier — jamais le "comment" technique
- Quand le contexte est insuffisant, tu poses une question ouverte adressée au Product Owner, comme dans un atelier de recueil des exigences

════════════════════════════════════════
CONTEXTE DU SYSTÈME AUDITÉ
════════════════════════════════════════

Tu analyses le système d'information d'un opérateur télécom multi-services en production depuis plus de dix ans.

Périmètre fonctionnel du système :
- Gestion des abonnés : création de comptes clients, modification des données personnelles, résiliation des abonnements
- Gestion des contrats : souscription aux offres commerciales (mobile, fixe, data, VoIP), modification, suspension temporaire ou définitive
- Facturation : calcul mensuel des consommations, génération et envoi des factures, suivi des paiements et des impayés
- Gestion des lignes téléphoniques : attribution des numéros, gestion des ressources réseau (cartes SIM, identifiants IMSI)
- Service après-vente : ouverture de tickets d'incident, suivi de l'avancement, résolution, clôture, enquête de satisfaction
- Administration interne : gestion des comptes agents, attribution et révocation des habilitations, paramétrage des valeurs de référence

Acteurs et habilitations du système :
- Abonné / Client : personne physique ou morale titulaire d'un ou plusieurs contrats de service télécom
- Agent commercial : habilité à créer et modifier les dossiers clients, souscrire ou résilier des offres
- Technicien réseau : habilité à intervenir sur les ressources techniques et à traiter les incidents de service
- Superviseur : accès en lecture élargi à toutes les données opérationnelles pour le pilotage et le reporting
- Administrateur système : habilitation maximale pour gérer les comptes agents et les paramètres de configuration

Flux métier principaux :
1. Souscription — Saisie des données client → Vérification d'éligibilité → Activation du service → Notification de bienvenue
2. Modification de dossier — Authentification agent → Sélection du dossier → Modification → Sauvegarde → Notification si requis
3. Résiliation — Demande initiée → Vérification des conditions contractuelles → Clôture du contrat → Archivage ou suppression
4. Traitement d'incident — Déclaration → Diagnostic → Intervention technique → Clôture → Satisfaction client
5. Administration — Connexion administrateur → Gestion des agents → Attribution des rôles → Audit des actions

════════════════════════════════════════
LEXIQUE DE TRADUCTION MÉTIER
════════════════════════════════════════

Traduis chaque comportement observé en utilisant ce lexique. Ne mentionne jamais le terme technique dans ta réponse.

Saisies et données d'entrée :
- Champ "email" → "adresse de contact de l'abonné ou de l'agent"
- Champ "name" ou "nom" → "dénomination de l'entité créée ou modifiée"
- Champ "password" → "secret d'authentification de l'agent"
- Champ "role" → "niveau d'habilitation attribué à l'agent"
- Champ "status" → "état du dossier, du contrat ou de l'abonnement"
- Champ "id" → "référence unique de l'entité cible de l'action"

Accès aux informations de l'agent connecté :
- Lecture du rôle en session → "vérification de l'habilitation de l'agent en cours de traitement"
- Lecture de l'identifiant en session → "identification de l'agent responsable de l'action"

Opérations sur les données du système :
- Création d'un enregistrement → "enregistrement d'un nouveau dossier dans le système"
- Lecture sans filtre de volume → "chargement de la liste complète sans limitation de résultats"
- Mise à jour d'un enregistrement → "modification des informations du dossier existant"
- Suppression d'un enregistrement → "suppression définitive ou clôture du dossier"

Contrôles d'accès et décisions :
- Vérification du rôle "admin" → "accès conditionné à l'habilitation Administrateur"
- Vérification du rôle "supervisor" → "accès conditionné à l'habilitation Superviseur"
- Vérification de la présence d'un identifiant → "contrôle d'existence de l'entité cible avant traitement"
- Vérification de champs obligatoires → "contrôle de complétude des données avant déclenchement du traitement"
- Vérification du mode de déclenchement → "traitement conditionné à une action explicite de l'utilisateur"

Notifications et effets de bord :
- Envoi d'email immédiat après une opération → "notification automatique envoyée de façon synchrone après le traitement"
- Envoi sans confirmation de réception → "notification sans garantie de délivrance ni possibilité de rejeu"

Sécurité et contraintes legacy :
- Hachage par algorithme ancien (MD5) → "protection du secret d'authentification par méthode legacy non conforme aux standards actuels"
- Construction dynamique de requête → "accès aux données par construction de la recherche au moment de l'exécution, sans protection paramétrique"

════════════════════════════════════════
COMMENT FORMULER LES QUESTIONS POUR LE PRODUCT OWNER
════════════════════════════════════════

Quand le contexte est insuffisant, formule une question ouverte permettant au Product Owner de donner un arbitrage métier.

Exemples de questions bien formulées pour un PO :
- "Que se passe-t-il pour un agent qui n'a pas l'habilitation requise : est-il redirigé, notifié ou simplement bloqué ?"
- "Si la notification d'activation ne peut pas être envoyée, l'abonnement est-il tout de même considéré comme actif ?"
- "La suppression d'un dossier client entraîne-t-elle la suppression de ses contrats et factures associés ?"
- "La liste des abonnés actifs est-elle destinée à un export ponctuel ou à un affichage temps réel nécessitant une pagination ?"
- "Le secret d'authentification est-il soumis à une politique de complexité définie dans le cahier des charges ?"
- "Quel est le comportement attendu lorsqu'un agent tente de modifier un dossier déjà en cours de traitement par un autre agent ?"
- "L'attribution du rôle peut-elle être effectuée par l'agent lui-même ou uniquement par un administrateur ?"

════════════════════════════════════════
FORMAT DE RÉPONSE OBLIGATOIRE
════════════════════════════════════════

Réponds UNIQUEMENT en JSON valide, sans texte avant ni après, sans markdown :
{
  "business_rule": "1 à 2 phrases max, en français simple pour un Product Owner",
  "confidence": 0.00,
  "missing_context": "1 seule question ouverte formulée pour un Product Owner — ou null"
}

Règles strictes :
- business_rule : décrit le comportement métier, jamais le code ni le technique ; 1 à 2 phrases max ; jamais de liste
- missing_context : 1 seule question ouverte pour le PO, formulée comme dans un atelier de recueil, ou null
- confidence : float entre 0.01 et 0.99, jamais 1.0 ; si contexte insuffisant, mettre < 0.30

Niveaux de confidence :
- 0.01-0.20 : comportement trop partiel, impossible de déduire la règle métier
- 0.21-0.40 : règle probable mais le processus exact est inconnu
- 0.41-0.60 : règle déductible avec réserves selon le contexte métier
- 0.61-0.80 : règle métier identifiable avec bonne confiance dans ce contexte télécom
- 0.81-0.99 : règle métier certaine pour cet opérateur télécom

INTERDICTIONS ABSOLUES dans business_rule :
- Mentionner PHP, SQL, session, formulaire, base de données, framework, variable, fonction, classe
- Formuler une recommandation d'amélioration ou de refactoring
- Dépasser 2 phrases, utiliser des listes à puces ou de la numérotation
- Commencer par "Ce fragment", "Ce code", "Cette ligne" ou tout terme technique similaire
"""

# Tarifs Anthropic en $ par million de tokens
# cache_read ≈ 10% du prix input (lecture depuis le cache de prompt)
PRICING: dict[str, dict[str, float]] = {
    "claude-haiku-4-5-20251001": {"input": 0.80,  "output": 4.00,  "cache_read": 0.08},
    "claude-sonnet-4-6":         {"input": 3.00,  "output": 15.00, "cache_read": 0.30},
    "claude-sonnet-4-20250514":  {"input": 3.00,  "output": 15.00, "cache_read": 0.30},
    "claude-opus-4-7":           {"input": 15.00, "output": 75.00, "cache_read": 1.50},
}


@dataclass
class KBCoverageReport:
    """Coverage stats from one enrichment session — KB hits vs LLM calls."""
    tokens_tried: int = 0
    tokens_found_high: int = 0
    tokens_found_medium: int = 0
    flags_kb_resolved: int = 0
    flags_llm_needed: int = 0
    flags_skipped: int = 0
    missing_tokens: dict = field(default_factory=dict)
    tokens_extracted_by_kind: dict = field(default_factory=dict)
    tokens_hit_by_kind: dict = field(default_factory=dict)

    @property
    def coverage_pct(self) -> float:
        total = self.flags_kb_resolved + self.flags_llm_needed
        return round(100.0 * self.flags_kb_resolved / total, 1) if total else 0.0

    @property
    def top_candidates(self) -> list:
        return sorted(self.missing_tokens.items(), key=lambda x: -x[1])[:10]


@dataclass
class TokenUsage:
    """Consommation de tokens pour une session d'enrichissement."""
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_creation_tokens: int = 0
    skipped_flags: int = 0
    enriched_flags: int = 0

    def costs(self, model: str) -> tuple[float, float, float]:
        """Retourne (coût_input_total, coût_output, économie_cache) en dollars.

        coût_input_total inclut : tokens input normaux + écriture cache + lecture cache.
        économie_cache = ce qu'on aurait payé en input normal vs lecture cache.
        """
        pricing = PRICING.get(model, PRICING["claude-sonnet-4-6"])
        input_price      = pricing["input"]
        output_price     = pricing["output"]
        cache_read_price = pricing.get("cache_read", input_price * 0.1)

        input_cost        = (self.input_tokens          / 1_000_000) * input_price
        cache_create_cost = (self.cache_creation_tokens / 1_000_000) * input_price
        cache_read_cost   = (self.cache_read_tokens     / 1_000_000) * cache_read_price
        output_cost       = (self.output_tokens         / 1_000_000) * output_price
        cache_economy     = (self.cache_read_tokens     / 1_000_000) * (input_price - cache_read_price)

        return input_cost + cache_create_cost + cache_read_cost, output_cost, cache_economy

    def total_cost(self, model: str) -> float:
        input_cost, output_cost, _ = self.costs(model)
        return input_cost + output_cost


def _recover_partial_json(raw: str) -> dict | None:
    """
    Récupère les champs d'un JSON tronqué par max_tokens.
    Extrait business_rule, confidence et missing_context par regex
    même si le JSON n'est pas fermé correctement.
    """
    rule_m = re.search(r'"business_rule"\s*:\s*"((?:[^"\\]|\\.)*)', raw, re.DOTALL)
    if not rule_m:
        return None
    rule = rule_m.group(1).rstrip('\\').strip()
    # Nettoyer une éventuelle fin tronquée (phrase incomplète sans ponctuation)
    if rule and rule[-1] not in '.!?»"':
        last_end = max(rule.rfind('.'), rule.rfind('!'), rule.rfind('?'))
        if last_end > len(rule) // 2:
            rule = rule[:last_end + 1]

    conf_m = re.search(r'"confidence"\s*:\s*([0-9.]+)', raw)
    confidence = float(conf_m.group(1)) if conf_m else 0.1

    ctx_m = re.search(r'"missing_context"\s*:\s*"((?:[^"\\]|\\.)*)"', raw, re.DOTALL)
    missing = ctx_m.group(1).strip() if ctx_m else None

    return {"business_rule": rule, "confidence": confidence, "missing_context": missing}


class LLMEnricher:
    """Enrichit les flags d'un IRSchema avec des insights LLM."""

    def __init__(
        self,
        model: str = "claude-sonnet-4-6",
        kb_provider: Optional["KBContextProvider"] = None,
        kb_lookup: Optional[Callable[[str], dict]] = None,
        kb_trust_medium: bool = False,
    ):
        import anthropic
        self.client = anthropic.Anthropic()
        self.model = model
        self.usage = TokenUsage()
        self.kb_provider = kb_provider
        self._kb_lookup = kb_lookup
        self.kb_trust_medium = kb_trust_medium
        self._kb_hits = 0
        self._kb_medium_hits = 0
        self.coverage = KBCoverageReport()

    @property
    def kb_hits(self) -> int:
        """Flags résolus par le KB sans appel LLM."""
        return self._kb_hits

    @property
    def kb_medium_hits(self) -> int:
        """Tokens medium rencontrés (injectés en contexte, ou résolus si kb_trust_medium)."""
        return self._kb_medium_hits

    def enrich(self, ir: IRSchema) -> IRSchema:
        """Enrichit tous les flags de l'IR. Retourne l'IR modifié."""
        # Index des corps de méthodes depuis l'IR — contexte complet pour le LLM
        method_bodies: dict[str, str] = {}
        for ep in ir.entry_points:
            if ep.raw_code:
                body = ep.raw_code[:2500]  # ~500 lignes max
                if ep.original_name:
                    method_bodies[ep.original_name] = body
                if ep.name and ep.name != ep.original_name:
                    method_bodies[ep.name] = body

        # Contexte KB une seule fois par fichier (évite N appels identiques)
        kb_context = ""
        if self.kb_provider:
            kb_context = self.kb_provider.context_for(
                ir.metadata.controller_name or ""
            )
            if kb_context:
                print(f"  [KB] Contexte injecté : {kb_context.count('[') - kb_context.count('[KB')} règle(s) KB")

        for flag in ir.flags:
            if not self._is_worth_enriching(flag):
                print(f"  ↷ {flag.id} skipped — fragment too minimal")
                self.usage.skipped_flags += 1
                self.coverage.flags_skipped += 1
                continue

            # Tentative KB avant LLM (0 token)
            kb_insight, kb_medium_ctx = self._try_kb_insight(flag)
            if kb_insight:
                ir.llm_insights.append(kb_insight)
                self._kb_hits += 1
                if kb_insight.source == "kb_medium":
                    self._kb_medium_hits += 1
                self.coverage.flags_kb_resolved += 1
                continue
            if kb_medium_ctx:
                self._kb_medium_hits += 1

            self.coverage.flags_llm_needed += 1
            if self._kb_lookup:
                for tok in self._extract_kb_tokens(flag):
                    self.coverage.missing_tokens[tok.value] = (
                        self.coverage.missing_tokens.get(tok.value, 0) + 1
                    )

            method_body = (
                method_bodies.get(flag.method_original_name or "")
                or method_bodies.get(flag.method_name or "")
            )
            try:
                insight = self._ask_llm(flag, method_body, kb_context, kb_medium_ctx)
                ir.llm_insights.append(insight)
            except Exception as e:
                print(f"  ⚠ Échec pour flag {flag.id} : {e}")

        if self.usage.skipped_flags:
            print(f"  ↷ {self.usage.skipped_flags} flag(s) skipped (fragment trop minimal)")
        if self._kb_hits:
            print(f"  📚 {self._kb_hits} flag(s) résolus depuis le KB (0 token LLM)")

        if self.coverage.tokens_extracted_by_kind:
            total_ex = sum(self.coverage.tokens_extracted_by_kind.values())
            kind_parts = ", ".join(
                f"{v} {k}"
                for k, v in self.coverage.tokens_extracted_by_kind.items()
                if v > 0
            )
            print(f"  ✓ KB tokens extraits : {total_ex} ({kind_parts})")

        if self.coverage.tokens_hit_by_kind:
            total_hits = sum(self.coverage.tokens_hit_by_kind.values())
            kind_parts = ", ".join(
                f"{v} {k}"
                for k, v in self.coverage.tokens_hit_by_kind.items()
                if v > 0
            )
            print(f"  ✓ KB hits : {total_hits} ({kind_parts})")

        return ir

    # Mots SQL détectant la présence de SQL dans un fragment
    _SQL_DETECT = re.compile(
        r'\b(SELECT|INSERT|UPDATE|DELETE|FROM|JOIN)\b', re.IGNORECASE
    )
    # Tables : après FROM, JOIN, INTO, UPDATE, DELETE FROM
    _SQL_TABLES = re.compile(
        r'(?:FROM|JOIN|INTO|UPDATE|DELETE\s+FROM)\s+["\']?(\w+)["\']?',
        re.IGNORECASE,
    )
    # Colonnes : mots en MAJUSCULES hors stop-list dans un contexte SQL
    _SQL_COLUMNS = re.compile(r'\b([A-Z][A-Z0-9_]{2,})\b')
    # Appels de service/repository/helper
    _SERVICE_CALL = re.compile(
        r'\$(?:this->)?(\w+(?:Service|Manager|Repository|Helper|Mapper))\s*->\s*(\w+)',
        re.IGNORECASE,
    )
    # Chemins de vue Zend
    _VIEW_PATH = re.compile(
        r'(?:render|renderScript)\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'
    )
    # Magic values numériques dans une comparaison
    _MAGIC_NUM_L = re.compile(r'\$\w+\s*(?:===?|!==?|>=?|<=?)\s*(\d+)')
    _MAGIC_NUM_R = re.compile(r'(\d+)\s*(?:===?|!==?)\s*\$\w+')

    # Ordre de recherche dans _try_kb_insight (du plus au moins fiable)
    _KIND_ORDER = ["literal", "constant", "column", "table",
                   "service_method", "view_path", "magic_value"]

    def _extract_kb_tokens(self, flag: Flag) -> list[KBToken]:
        """Extrait les tokens lookupables dans le KB depuis flag.fragment.

        Retourne une liste dédupliquée par (value, kind), dans l'ordre d'apparition.
        """
        raw = flag.fragment
        candidates: list[KBToken] = []

        # 1. Littéraux MAJ entre guillemets
        for m in re.finditer(r"""['"]([A-Z][A-Z0-9_]+)['"]""", raw):
            val = m.group(1)
            if val not in STOP_TOKENS:
                candidates.append(KBToken(value=val, kind="literal"))

        # 2. Constantes MAJUSCULES non quotées — underscore non requis, pour
        #    couvrir les codes courts (H1, TP2) comme C_TYP_FLX ; STOP_TOKENS filtre
        for m in re.finditer(r'\b([A-Z][A-Z0-9_]{1,})\b', raw):
            val = m.group(1)
            if val not in STOP_TOKENS:
                candidates.append(KBToken(value=val, kind="constant"))

        # 3. Colonnes et tables SQL
        if self._SQL_DETECT.search(raw):
            for m in self._SQL_TABLES.finditer(raw):
                val = m.group(1).upper()
                if val not in STOP_TOKENS:
                    candidates.append(KBToken(value=val, kind="table"))
            for m in self._SQL_COLUMNS.finditer(raw):
                val = m.group(1)
                if val not in STOP_TOKENS and len(val) >= 3:
                    candidates.append(KBToken(value=val, kind="column"))

        # 4. Appels de service
        for m in self._SERVICE_CALL.finditer(raw):
            candidates.append(
                KBToken(value=f"{m.group(1)}.{m.group(2)}", kind="service_method")
            )

        # 5. Chemins de vue Zend
        for m in self._VIEW_PATH.finditer(raw):
            candidates.append(KBToken(value=m.group(1), kind="view_path"))

        # 6. Magic values numériques (hors 0 et 1)
        for pat in (self._MAGIC_NUM_L, self._MAGIC_NUM_R):
            for m in pat.finditer(raw):
                val = m.group(1)
                if val not in ("0", "1"):
                    candidates.append(KBToken(value=val, kind="magic_value"))

        # Déduplication par (value, kind)
        seen: set[tuple[str, str]] = set()
        result: list[KBToken] = []
        for t in candidates:
            key = (t.value, t.kind)
            if key not in seen:
                seen.add(key)
                result.append(t)

        # Compteurs par kind (pour observabilité)
        for t in result:
            self.coverage.tokens_extracted_by_kind[t.kind] = (
                self.coverage.tokens_extracted_by_kind.get(t.kind, 0) + 1
            )

        return result

    def _try_kb_insight(self, flag: Flag) -> tuple[Optional[LLMInsight], str]:
        """Résout un flag depuis le KB YAML sans appel LLM.

        Retourne (insight, contexte_medium) :
        - high → (LLMInsight source="kb", "") — court-circuite le LLM ;
        - medium → court-circuite uniquement si kb_trust_medium ; sinon la fiche
          part en contexte du prompt LLM (2e élément) au lieu de le remplacer ;
        - non trouvé / inferred → (None, "").
        """
        if not self._kb_lookup:
            return None, ""

        medium_context = ""
        tokens = self._extract_kb_tokens(flag)
        # Recherche dans l'ordre de fiabilité décroissante
        kind_priority = {k: i for i, k in enumerate(self._KIND_ORDER)}
        tokens_sorted = sorted(tokens, key=lambda t: kind_priority.get(t.kind, 99))

        for token in tokens_sorted:
            self.coverage.tokens_tried += 1
            result = self._kb_lookup(token.value)
            if not result.get("found"):
                continue
            confiance = result.get("confiance", "inferred")
            if confiance == "high":
                self.coverage.tokens_found_high += 1
                self.coverage.tokens_hit_by_kind[token.kind] = (
                    self.coverage.tokens_hit_by_kind.get(token.kind, 0) + 1
                )
            elif confiance == "medium":
                self.coverage.tokens_found_medium += 1
                self.coverage.tokens_hit_by_kind[token.kind] = (
                    self.coverage.tokens_hit_by_kind.get(token.kind, 0) + 1
                )
            if confiance == "inferred":
                continue  # pas fiable — laisser le LLM gérer
            label = result.get("label") or token.value
            semantique = (result.get("semantique") or "").strip()
            if confiance == "high":
                if semantique:
                    end = max(semantique.find('.'), semantique.find('!'), semantique.find('?'))
                    if 0 < end < 250:
                        semantique = semantique[:end + 1]
                rule = f"{label}. {semantique}".strip() if semantique else label
                return LLMInsight(
                    flag_id=flag.id,
                    business_rule=rule,
                    confidence=0.92,
                    source="kb",
                    needs_human_validation=False,
                ), ""
            elif confiance == "medium":
                if self.kb_trust_medium:
                    return LLMInsight(
                        flag_id=flag.id,
                        business_rule=f"{label} (à confirmer en session PO).",
                        confidence=0.55,
                        source="kb_medium",
                        needs_human_validation=True,
                    ), ""
                # 0.55 trop généreux pour court-circuiter : la fiche part en
                # contexte du prompt, et on continue à chercher un token high
                if not medium_context:
                    medium_context = f"{token.value} : {label}"
                    if semantique:
                        medium_context += f" — {semantique}"
        return None, medium_context

    def _is_worth_enriching(self, flag: Flag) -> bool:
        """Retourne False si le fragment est trop minimal pour apporter de la valeur."""
        fragment = flag.fragment.strip()

        if len(fragment) < 10:
            return False

        # Juste un nom de variable seul
        if re.match(r'^\$[a-zA-Z_]+$', fragment):
            return False

        # Variables isolées sans opérateur ni appel
        if fragment in ('$id', '$existing', '$user', '$data', '$result'):
            return False

        return True

    def _ask_llm(
        self,
        flag: Flag,
        method_body: Optional[str] = None,
        kb_context: str = "",
        kb_medium_context: str = "",
    ) -> LLMInsight:
        user_message = self._build_prompt(flag, method_body, kb_context, kb_medium_context)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=450,
            system=[{
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": user_message}],
        )

        # Comptabiliser les tokens
        self.usage.input_tokens           += response.usage.input_tokens
        self.usage.output_tokens          += response.usage.output_tokens
        self.usage.cache_read_tokens      += getattr(response.usage, "cache_read_input_tokens", 0)
        self.usage.cache_creation_tokens  += getattr(response.usage, "cache_creation_input_tokens", 0)
        self.usage.enriched_flags         += 1

        raw = response.content[0].text.strip()
        return self._parse_response(flag.id, raw)

    def _build_prompt(
        self,
        flag: Flag,
        method_body: Optional[str] = None,
        kb_context: str = "",
        kb_medium_context: str = "",
    ) -> str:
        parts: list[str] = []
        if kb_context:
            parts.append(kb_context)
        if kb_medium_context:
            parts.append(
                "Indication issue de la base de connaissance (fiabilité moyenne, "
                "non validée — à confirmer, ne pas la considérer comme certaine) :\n"
                f"{kb_medium_context}"
            )
        if method_body:
            parts.append(
                f"Méthode complète ({flag.method_name or flag.method_original_name}) :\n"
                f"```php\n{method_body}\n```"
            )
        parts.append(
            f"Fragment concerné :\n"
            f"```\n{flag.fragment}\n```\n\n"
            f"Question métier :\n{flag.question}"
        )
        return "\n\n".join(parts)

    def _parse_response(self, flag_id: str, raw: str) -> LLMInsight:
        # Supprimer les blocs markdown si le modèle en ajoute malgré l'instruction
        cleaned = re.sub(r'^```\w*\s*', '', raw.strip())
        cleaned = re.sub(r'\s*```$', '', cleaned.strip())
        json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
        if json_match:
            cleaned = json_match.group(0)

        data: dict | None = None

        # Tentative 1 : JSON valide
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        # Tentative 2 : JSON tronqué par max_tokens — extraction par regex
        if data is None:
            data = _recover_partial_json(cleaned)

        if data is None:
            return LLMInsight(
                flag_id=flag_id,
                business_rule=f"[Erreur parsing LLM] Réponse brute : {raw[:200]}",
                confidence=0.1,
            )

        business_rule = str(data.get("business_rule", "Aucune règle extraite")).strip()
        confidence = min(float(data.get("confidence", 0.5)), 0.99)
        missing = data.get("missing_context") or None
        if isinstance(missing, str):
            missing = missing.strip() or None

        return LLMInsight(
            flag_id=flag_id,
            business_rule=business_rule,
            missing_context=missing,
            confidence=confidence,
        )
