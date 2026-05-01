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
from typing import Optional, TYPE_CHECKING
from ir.schema import IRSchema, Flag, LLMInsight

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


class LLMEnricher:
    """Enrichit les flags d'un IRSchema avec des insights LLM."""

    def __init__(
        self,
        model: str = "claude-sonnet-4-6",
        kb_provider: Optional["KBContextProvider"] = None,
    ):
        import anthropic
        self.client = anthropic.Anthropic()
        self.model = model
        self.usage = TokenUsage()
        self.kb_provider = kb_provider

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
                continue
            method_body = (
                method_bodies.get(flag.method_original_name or "")
                or method_bodies.get(flag.method_name or "")
            )
            try:
                insight = self._ask_llm(flag, method_body, kb_context)
                ir.llm_insights.append(insight)
            except Exception as e:
                print(f"  ⚠ Échec pour flag {flag.id} : {e}")

        if self.usage.skipped_flags:
            print(f"  ↷ {self.usage.skipped_flags} flag(s) skipped (fragment trop minimal)")
        return ir

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
    ) -> LLMInsight:
        user_message = self._build_prompt(flag, method_body, kb_context)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=200,
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
    ) -> str:
        parts: list[str] = []
        if kb_context:
            parts.append(kb_context)
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
        raw = re.sub(r'^```\w*\s*', '', raw.strip())
        raw = re.sub(r'\s*```$', '', raw.strip())
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            raw = json_match.group(0)

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return LLMInsight(
                flag_id=flag_id,
                business_rule=f"[Erreur parsing LLM] Réponse brute : {raw[:200]}",
                confidence=0.1,
            )

        business_rule = str(data.get("business_rule", "Aucune règle extraite"))
        confidence = min(float(data.get("confidence", 0.5)), 0.99)
        missing = data.get("missing_context") or None

        return LLMInsight(
            flag_id=flag_id,
            business_rule=business_rule,
            missing_context=missing,
            confidence=confidence,
        )
