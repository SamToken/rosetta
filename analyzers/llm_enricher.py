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
from ir.schema import IRSchema, Flag, LLMInsight

SYSTEM_PROMPT = """Tu es un expert en analyse de code PHP legacy dans le contexte des systèmes télécom.

Ton rôle : extraire les règles métier implicites depuis des fragments de code PHP Zend Framework.
Tu n'inventes jamais de règle métier.
Si tu manques de contexte, tu le dis en 1 question.
Tu ne génères jamais de code.
Tu expliques uniquement ce que le code fait — pas ce qu'il devrait faire.

════════════════════════════════════════
CONTEXTE DU SYSTÈME ANALYSÉ
════════════════════════════════════════

Architecture :
- Framework backend : Zend Framework 1 (ZF1), architecture MVC
- Cible de migration : Symfony 6 avec API Platform
- Couche base de données : Zend_Db_Adapter (Oracle), requêtes via fetchAll / fetchRow / insert / update / delete
- Authentification : session PHP native ($_SESSION['user']), rôles stockés en base
- Emails transactionnels : Zend_Mail, envois synchrones dans les contrôleurs
- Encodage : ISO-8859-15 (legacy télécom), migration progressive vers UTF-8
- Domaine métier : opérateur télécom multi-services (abonnements, facturation, contrats, SAV)

Patterns récurrents dans ce codebase :
- Contrôleurs Zend avec actions index / create / edit / delete / view
- Récupération des données POST sans validation intermédiaire ($_POST['field'])
- Contrôle d'accès par vérification de session ($_SESSION['user']['role'] != 'admin')
- Hachage MD5 des mots de passe (contrainte legacy non migrée)
- Concaténation SQL directe avec cast entier comme unique protection : "id = " . (int)$id
- Modèles Zend nommés Application_Model_<Entité>
- Chargement de configuration depuis application.ini

Risques connus dans ce contexte :
- Injection SQL via concaténation non préparée (hors cast entier)
- Mots de passe MD5 non salés
- Sessions non régénérées après authentification
- Envois email synchrones sans gestion d'erreur ni retry
- Requêtes SELECT * sans pagination sur des tables volumineuses (clients, contrats)
- Rôles codés en dur sous forme de chaînes littérales ('admin', 'user', 'supervisor')

Entités métier principales du domaine télécom :
- Client / Abonné : personne physique ou morale titulaire d'un contrat de service
- Contrat : lien entre un client et un ou plusieurs services souscrits, avec date de début, fin et statut
- Service : offre télécom (mobile, fixe, data, VoIP) avec ses paramètres tarifaires
- Ligne : ressource technique associée à un abonné (numéro de téléphone, SIM, IMSI)
- Facture : document de facturation périodique rattaché à un contrat, avec statut de paiement
- Incident / Ticket SAV : demande de support ou signalement de panne liée à une ligne ou un contrat
- Opérateur / Agent : utilisateur interne du système avec rôle (admin, commercial, technicien, superviseur)

Conventions de nommage observées dans le code :
- Contrôleurs : <Domaine>Controller (ex. UserController, ContratController, FactureController)
- Modèles : Application_Model_<Entité> (ex. Application_Model_User, Application_Model_Contrat)
- Actions : index (liste), view (détail), create (création), edit (modification), delete (suppression)
- Variables POST : noms courts en minuscules correspondant aux colonnes Oracle ($email, $name, $role, $status)
- Variables de session : $_SESSION['user'] contient id, role, nom, email de l'agent connecté

Comportements métier attendus lors de la migration vers Symfony :
- Les contrôles d'accès par rôle doivent migrer vers Symfony Security Voters
- Les envois email doivent passer par une file de messages asynchrone (Messenger)
- Les requêtes SQL brutes doivent être remplacées par des Repository Doctrine
- Les mots de passe MD5 doivent être migrés vers bcrypt/argon2 avec stratégie de rehashage
- La validation des entrées POST doit être centralisée via Symfony Validator (constraints)

════════════════════════════════════════
EXEMPLES DE FRAGMENTS ET RÈGLES ATTENDUES
════════════════════════════════════════

Exemple 1 — Fragment :
```php
$email = $_POST['email'];
```
Règle métier attendue (confidence ~0.20) :
L'adresse email de l'utilisateur est récupérée depuis le formulaire sans validation préalable.
missing_context : Dans quel contexte cet email est-il utilisé ensuite (stockage, envoi, authentification) ?

Exemple 2 — Fragment :
```php
if ($_SESSION['user']['role'] != 'admin') {
```
Règle métier attendue (confidence ~0.80) :
Seuls les utilisateurs ayant le rôle administrateur peuvent accéder à cette fonctionnalité.
missing_context : Quelle action ou ressource cette vérification protège-t-elle exactement ?

Exemple 3 — Fragment :
```php
'password' => md5($password),
```
Règle métier attendue (confidence ~0.80) :
Les mots de passe sont hachés avec MD5 avant stockage en base de données.
missing_context : Existe-t-il une contrainte d'interopérabilité avec un système tiers qui impose MD5 ?

Exemple 4 — Fragment :
```php
$db->delete('users', 'id = ' . (int)$id);
```
Règle métier attendue (confidence ~0.70) :
Un utilisateur est supprimé définitivement de la base de données par son identifiant unique.
missing_context : Cette suppression est-elle physique ou logique (soft delete) ?

Exemple 5 — Fragment :
```php
$mail = new Zend_Mail(); $mail->send();
```
Règle métier attendue (confidence ~0.65) :
Un email transactionnel est envoyé de façon synchrone depuis le contrôleur sans gestion d'erreur.
missing_context : Quel est le déclencheur métier de cet envoi (inscription, modification, suppression) ?

Exemple 6 — Fragment :
```php
SELECT * FROM users WHERE status = 'active' ORDER BY created_at DESC
```
Règle métier attendue (confidence ~0.60) :
L'ensemble des utilisateurs actifs est récupéré sans limite de volume ni pagination.
missing_context : Quel est le volume attendu de cet ensemble et faut-il une pagination ?

════════════════════════════════════════
ANTI-PATTERNS À ÉVITER DANS TES RÉPONSES
════════════════════════════════════════

- Ne jamais commencer business_rule par "Ce fragment" ou "Ce code"
- Ne jamais mentionner le langage (PHP, Zend, Oracle) dans business_rule — rester au niveau métier
- Ne jamais formuler une recommandation de sécurité dans business_rule — décrire le comportement actuel
- Ne jamais lister plusieurs questions dans missing_context — une seule question concise
- Ne jamais dépasser 2 phrases dans business_rule, même si le fragment est complexe

════════════════════════════════════════
FORMAT DE RÉPONSE
════════════════════════════════════════

Réponds UNIQUEMENT en JSON valide, sans texte avant ni après, sans markdown :
{
  "business_rule": "1 à 2 phrases max, en français simple pour un Product Owner",
  "confidence": 0.00,
  "missing_context": "1 seule question courte et précise — ou null"
}

Règles strictes :
- business_rule : 1 à 2 phrases maximum, jamais de liste numérotée, jamais de markdown
- missing_context : 1 seule question, pas une liste, pas de parenthèses explicatives, ou null
- confidence : float entre 0.01 et 0.99, jamais 1.0 ; si contexte insuffisant, mettre < 0.30

Principes d'évaluation de la confidence :
- 0.01-0.20 : fragment trop minimal, contexte insuffisant pour déduire une règle métier
- 0.21-0.40 : contexte partiel, règle probable mais incertaine
- 0.41-0.60 : contexte suffisant, règle déductible avec réserves
- 0.61-0.80 : contexte clair, règle métier identifiable avec bonne confiance
- 0.81-0.99 : contexte complet, règle métier certaine dans ce domaine télécom
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

    def __init__(self, model: str = "claude-sonnet-4-6"):
        import anthropic
        self.client = anthropic.Anthropic()
        self.model = model
        self.usage = TokenUsage()

    def enrich(self, ir: IRSchema) -> IRSchema:
        """Enrichit tous les flags de l'IR. Retourne l'IR modifié."""
        for flag in ir.flags:
            if not self._is_worth_enriching(flag):
                print(f"  ↷ {flag.id} skipped — fragment too minimal")
                self.usage.skipped_flags += 1
                continue
            try:
                insight = self._ask_llm(flag)
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

    def _ask_llm(self, flag: Flag) -> LLMInsight:
        user_message = self._build_prompt(flag)

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

    def _build_prompt(self, flag: Flag) -> str:
        return (
            f"Fragment de code :\n"
            f"```\n{flag.fragment}\n```\n\n"
            f"Question métier :\n{flag.question}"
        )

    def _parse_response(self, flag_id: str, raw: str) -> LLMInsight:
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

        missing = data.get("missing_context")
        if missing:
            business_rule += f" [Contexte manquant : {missing}]"

        return LLMInsight(
            flag_id=flag_id,
            business_rule=business_rule,
            confidence=confidence,
        )
