"""
Migration Recipes — Zend Framework 1 → Symfony 6
==================================================
Pour chaque pattern legacy détecté par le FlagEngine, fournit un bloc
markdown actionnable : équivalent Symfony, diff PHP avant/après, impact
migration.

Source statique, déterministe, zéro LLM. Conçu pour transformer
`_flags.md` d'un rapport d'audit en outil de remédiation utilisable au
quotidien par un dev.

Intégration recommandée
-----------------------
Dans `generators/business_doc_generator.py` ou `generators/flags_doc_generator.py`,
ajouter pour chaque flag :

    from generators.migration_recipes import RecipeBook
    recipes = RecipeBook()

    # dans la boucle des flags :
    recipe_block = recipes.render(flag)
    if recipe_block:
        lines.append(recipe_block)

L'ordre des recettes dans `_RECIPES` est utilisé en cas de matchs multiples :
la première qui matche gagne. Les recettes plus spécifiques sont placées
avant les plus génériques.

Pour ajouter une recette, l'inscrire dans `_RECIPES` ci-dessous —
pas de YAML, pas de fichier externe en v1 : 30 patterns suffisent pour
couvrir 80% du codebase Astro.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from ir.schema import Flag


# =============================================================================
# Modèle
# =============================================================================

@dataclass(frozen=True)
class Recipe:
    """Une équivalence Zend → Symfony pour un pattern PHP donné."""
    id: str                          # identifiant stable, ex: "md5_password"
    title: str                       # titre court pour le markdown
    flag_type: Optional[str]         # None = match tous les types
    pattern: re.Pattern              # regex matchée contre flag.fragment
    zend_pattern: str                # description en français du pattern legacy
    symfony_equivalent: str          # description en français du remplacement
    diff_before: str                 # snippet PHP "avant" (sans préfixe -)
    diff_after: str                  # snippet PHP "après" (sans préfixe +)
    migration_notes: str             # impacts, pièges, prérequis
    effort: str                      # "trivial" | "modéré" | "élevé"


# =============================================================================
# Catalogue de recettes — ordre = priorité de match
# =============================================================================

_RECIPES: list[Recipe] = [

    # -------------------------------------------------------------------------
    # Sécurité — md5 password
    # -------------------------------------------------------------------------
    Recipe(
        id="md5_password",
        title="Hachage MD5 → UserPasswordHasherInterface",
        flag_type="security_risk",
        pattern=re.compile(r"\bmd5\s*\(\s*\$\w*(?:pass|pwd|mdp|secret)", re.IGNORECASE),
        zend_pattern="Hachage de mot de passe avec MD5 (obsolète, vulnérable aux rainbow tables)",
        symfony_equivalent="`UserPasswordHasherInterface::hashPassword()` avec algorithme `bcrypt` ou `argon2id`",
        diff_before="'password' => md5($password),",
        diff_after="'password' => $this->passwordHasher->hashPassword($user, $password),",
        migration_notes=(
            "Les hash existants en base sont MD5 et restent valides pour la vérification "
            "(`$hasher->isPasswordValid()` doit fallback sur md5 pendant la transition).\n"
            "Prévoir un re-hash transparent au prochain login (Doctrine listener ou "
            "EventSubscriber sur `LoginSuccessEvent`). Migration des hash existants "
            "impossible sans le mot de passe en clair."
        ),
        effort="modéré",
    ),

    # -------------------------------------------------------------------------
    # Sécurité — $_POST direct
    # -------------------------------------------------------------------------
    Recipe(
        id="post_direct_access",
        title="$_POST direct → Request::request",
        flag_type="security_risk",
        pattern=re.compile(r"\$_POST\s*\[\s*['\"](\w+)['\"]"),
        zend_pattern="Lecture directe de `$_POST` sans validation ni typage",
        symfony_equivalent="`Request::request->get()` + composant Form pour validation",
        diff_before="$nom = $_POST['nom'];",
        diff_after=(
            "// dans une action de contrôleur Symfony\n"
            "$nom = $request->request->get('nom');\n"
            "// ou mieux : utiliser un Form/DTO mappé"
        ),
        migration_notes=(
            "Recommandation forte : passer par un Form Symfony ou un DTO + Validator. "
            "L'accès direct via `$request->request->get()` ne valide rien, c'est juste "
            "un déplacement syntaxique. Identifier dans chaque action les champs attendus "
            "et créer le Type ou DTO correspondant."
        ),
        effort="modéré",
    ),

    # -------------------------------------------------------------------------
    # Sécurité — $_SESSION direct
    # -------------------------------------------------------------------------
    Recipe(
        id="session_direct_access",
        title="$_SESSION → SessionInterface / Security",
        flag_type="security_risk",
        pattern=re.compile(r"\$_SESSION\s*\["),
        zend_pattern="Accès direct à la superglobale `$_SESSION` pour authentification/rôles",
        symfony_equivalent=(
            "`Security::getUser()` pour l'utilisateur courant, "
            "`#[IsGranted('ROLE_X')]` pour les contrôles de rôle, "
            "`SessionInterface` pour les autres données de session"
        ),
        diff_before=(
            "if ($_SESSION['user']['role'] != 'admin') {\n"
            "    throw new Exception('Accès refusé');\n"
            "}"
        ),
        diff_after=(
            "#[IsGranted('ROLE_ADMIN')]\n"
            "public function action(): Response {\n"
            "    $user = $this->getUser();\n"
            "    // …\n"
            "}"
        ),
        migration_notes=(
            "Le mapping des rôles legacy (`'admin'`, `'user'`, codes Oracle…) vers "
            "les rôles Symfony (`ROLE_ADMIN`, `ROLE_USER`) doit être tranché AVANT la "
            "migration. Penser au `RoleHierarchy` si les rôles legacy sont imbriqués. "
            "Le `User` Symfony doit implémenter `UserInterface` et la liaison vers la "
            "table users legacy se fait via un `UserProvider` custom."
        ),
        effort="élevé",
    ),

    # -------------------------------------------------------------------------
    # Sécurité — Concaténation SQL
    # -------------------------------------------------------------------------
    Recipe(
        id="sql_concatenation",
        title="Concaténation SQL → Doctrine paramètres",
        flag_type="security_risk",
        pattern=re.compile(r"['\"][^'\"]*(?:WHERE|AND|OR)\s*\w+\s*=\s*['\"]\s*\.\s*\$", re.IGNORECASE),
        zend_pattern="Construction SQL par concaténation de chaînes (risque injection malgré le cast `(int)`)",
        symfony_equivalent="QueryBuilder Doctrine avec `setParameter()`, ou DQL paramétré",
        diff_before='$db->fetchAll("SELECT * FROM users WHERE id = " . (int)$id);',
        diff_after=(
            "$this->em->createQueryBuilder()\n"
            "    ->select('u')\n"
            "    ->from(User::class, 'u')\n"
            "    ->where('u.id = :id')\n"
            "    ->setParameter('id', $id)\n"
            "    ->getQuery()\n"
            "    ->getResult();"
        ),
        migration_notes=(
            "Le cast `(int)` actuel protège uniquement les ID numériques. "
            "Toute concaténation sur un champ string (nom, email, code métier) est une "
            "injection ouverte. Lister tous les `WHERE … . $` du fichier — pas seulement "
            "le `id =` actuellement détecté — avant de migrer.\n"
            "Côté repository Doctrine, préférer les méthodes nommées (`findBy*`, `findOneBy*`) "
            "pour les cas simples et le QueryBuilder pour les requêtes complexes."
        ),
        effort="modéré",
    ),

    # -------------------------------------------------------------------------
    # Mailer — envoi synchrone
    # -------------------------------------------------------------------------
    Recipe(
        id="zend_mail_sync",
        title="Zend_Mail synchrone → Symfony Mailer + Messenger",
        flag_type="business_logic_unclear",
        pattern=re.compile(r"(?:new\s+Zend_Mail|\$mail\s*->\s*send|->\s*sendMail)"),
        zend_pattern="Envoi d'email synchrone depuis le contrôleur, sans gestion d'échec",
        symfony_equivalent=(
            "`Symfony\\Component\\Mailer\\MailerInterface` "
            "(synchrone) ou envoi asynchrone via Messenger pour ne pas bloquer la requête"
        ),
        diff_before=(
            "$mail = new Zend_Mail();\n"
            "$mail->setSubject('Confirmation')\n"
            "     ->setBodyText($body)\n"
            "     ->addTo($user->email);\n"
            "$mail->send();"
        ),
        diff_after=(
            "// Sync (réplique du comportement actuel)\n"
            "$email = (new Email())\n"
            "    ->subject('Confirmation')\n"
            "    ->to($user->email)\n"
            "    ->text($body);\n"
            "$this->mailer->send($email);\n\n"
            "// Async (recommandé pour ne pas bloquer la réponse HTTP)\n"
            "$this->bus->dispatch(new SendConfirmationEmailMessage($user->id));"
        ),
        migration_notes=(
            "L'envoi est aujourd'hui SYNCHRONE — un timeout SMTP fait planter la requête. "
            "Profiter de la migration pour passer en asynchrone via Messenger (transport "
            "Redis ou Doctrine). Préserver la possibilité de fallback sync pour les "
            "environnements de dev/qualif.\n"
            "Vérifier si l'envoi conditionne la suite du traitement métier — si oui, "
            "le rester sync MAIS l'extraire dans un service dédié avec gestion d'erreur."
        ),
        effort="modéré",
    ),

    # -------------------------------------------------------------------------
    # SELECT * sans pagination
    # -------------------------------------------------------------------------
    Recipe(
        id="select_star_no_pagination",
        title="SELECT * sans LIMIT → Doctrine Paginator",
        flag_type="business_logic_unclear",
        pattern=re.compile(r"SELECT\s+\*", re.IGNORECASE),
        zend_pattern="Requête `SELECT *` sans clause `LIMIT` — volume non maîtrisé",
        symfony_equivalent=(
            "`Doctrine\\ORM\\Tools\\Pagination\\Paginator` pour la pagination native, "
            "ou `KnpPaginatorBundle` pour intégration Twig"
        ),
        diff_before='$db->fetchAll("SELECT * FROM enchainements WHERE statut = \'ACTIF\'");',
        diff_after=(
            "$query = $this->em->createQuery(\n"
            "    'SELECT e FROM App\\Entity\\Enchainement e WHERE e.statut = :statut'\n"
            ")->setParameter('statut', 'ACTIF')\n"
            " ->setFirstResult($offset)\n"
            " ->setMaxResults($pageSize);\n\n"
            "$paginator = new Paginator($query, fetchJoinCollection: true);\n"
            "$total = count($paginator);"
        ),
        migration_notes=(
            "Avant de migrer : mesurer le volume réel en production. Si <100 lignes "
            "toujours, une `findBy()` simple suffit. Si potentiellement >1000, "
            "Paginator obligatoire.\n"
            "Penser à exposer la pagination dans l'API/UI : sans changement côté front, "
            "la migration peut casser des écrans qui supposaient tout-en-un."
        ),
        effort="modéré",
    ),

    # -------------------------------------------------------------------------
    # Zend_Db_Adapter fetchAll/fetchRow
    # -------------------------------------------------------------------------
    Recipe(
        id="zend_db_adapter_fetch",
        title="Zend_Db fetchAll/fetchRow → Doctrine Repository",
        flag_type=None,  # peut apparaître dans plusieurs types de flags
        pattern=re.compile(r"->\s*(?:fetchAll|fetchRow|fetchOne|fetchCol)\s*\("),
        zend_pattern="Appel direct à `Zend_Db_Adapter` pour lecture (fetchAll/fetchRow)",
        symfony_equivalent="Méthode de Repository Doctrine (`findAll`, `findOneBy`, `findBy`, ou QueryBuilder)",
        diff_before=(
            "$row = $this->db->fetchRow(\n"
            "    'SELECT * FROM enchainements WHERE id = ?', $id\n"
            ");"
        ),
        diff_after="$enchainement = $this->enchainementRepository->find($id);",
        migration_notes=(
            "Étape préalable : créer l'entité Doctrine correspondante (`@Entity` + mapping "
            "vers la table Oracle existante). Préserver les noms de colonnes (`@Column(name='C_TYP_FLX')`) "
            "tant que la BD n'est pas migrée.\n"
            "Pour les requêtes complexes (joins multiples, agrégats), créer une méthode "
            "custom dans le Repository plutôt que de stuffer du DQL dans le contrôleur."
        ),
        effort="élevé",
    ),

    # -------------------------------------------------------------------------
    # Zend View (->view->X)
    # -------------------------------------------------------------------------
    Recipe(
        id="zend_view_assignment",
        title="$this->view->X → Twig + AbstractController::render",
        flag_type=None,
        pattern=re.compile(r"\$this\s*->\s*view\s*->\s*\w+\s*="),
        zend_pattern="Assignation de variables à la vue Zend (`$this->view->x = ...`)",
        symfony_equivalent="Tableau passé à `$this->render('template.html.twig', [...])`",
        diff_before=(
            "$this->view->enchainements = $enchainements;\n"
            "$this->view->total = count($enchainements);\n"
            "// vue rendue automatiquement par Zend"
        ),
        diff_after=(
            "return $this->render('enchainement/index.html.twig', [\n"
            "    'enchainements' => $enchainements,\n"
            "    'total' => count($enchainements),\n"
            "]);"
        ),
        migration_notes=(
            "Conversion des templates : .phtml → .html.twig n'est PAS automatique. "
            "La syntaxe Zend (`<?= $this->escape($x) ?>`) devient `{{ x }}` (échappement "
            "auto en Twig). Les helpers Zend custom doivent être réécrits en Twig functions/filters.\n"
            "Stratégie incrémentale possible : garder Zend_View comme template engine "
            "temporairement avec un bridge Symfony — non recommandé long terme."
        ),
        effort="élevé",
    ),

    # -------------------------------------------------------------------------
    # Zend_Registry
    # -------------------------------------------------------------------------
    Recipe(
        id="zend_registry",
        title="Zend_Registry → Symfony DI / ParameterBag",
        flag_type=None,
        pattern=re.compile(r"Zend_Registry\s*::\s*(?:get|set)\s*\("),
        zend_pattern="`Zend_Registry::get/set` comme bus global d'objets/config",
        symfony_equivalent=(
            "Injection de dépendances Symfony pour les services ; "
            "`ParameterBagInterface` pour la config statique ; "
            "`Stopwatch`/`Cache` pour les cas spécifiques"
        ),
        diff_before='$config = Zend_Registry::get("config");',
        diff_after=(
            "// dans le constructeur du service ou contrôleur\n"
            "public function __construct(\n"
            "    private ParameterBagInterface $params,\n"
            ") {}\n\n"
            "$value = $this->params->get('mon.parametre');"
        ),
        migration_notes=(
            "Lister tous les `Zend_Registry::set()` du projet — chaque clé devient soit "
            "un service injectable, soit un paramètre dans `services.yaml`. C'est "
            "l'occasion de tuer les anti-patterns service-locator implicites.\n"
            "Pour les objets stateful partagés (rare), envisager une classe dédiée "
            "injectée comme service singleton."
        ),
        effort="modéré",
    ),
]


# =============================================================================
# API publique
# =============================================================================

class RecipeBook:
    """Catalogue de recettes de migration Zend → Symfony."""

    def __init__(self):
        self._recipes = list(_RECIPES)

    def find(self, flag: Flag) -> Optional[Recipe]:
        """Retourne la première recette qui matche le flag, ou None."""
        for recipe in self._recipes:
            if recipe.flag_type and flag.type != recipe.flag_type:
                continue
            if recipe.pattern.search(flag.fragment):
                return recipe
        return None

    def render(self, flag: Flag) -> Optional[str]:
        """Rend le bloc markdown migration pour un flag, ou None si pas de recette."""
        recipe = self.find(flag)
        if not recipe:
            return None
        return _render_block(recipe)

    def all(self) -> list[Recipe]:
        """Toutes les recettes — utile pour générer un index ou les tester."""
        return list(self._recipes)


# =============================================================================
# Rendu markdown
# =============================================================================

def _render_block(recipe: Recipe) -> str:
    """Rend une recette en bloc markdown injectable dans _flags.md."""
    return (
        f"\n**🔧 {recipe.title}** *(effort: {recipe.effort})*\n\n"
        f"- *Pattern Zend détecté :* {recipe.zend_pattern}\n"
        f"- *Équivalent Symfony :* {recipe.symfony_equivalent}\n\n"
        f"*Diff suggéré :*\n"
        f"```diff\n"
        f"{_prefix_lines(recipe.diff_before, '- ')}\n"
        f"{_prefix_lines(recipe.diff_after, '+ ')}\n"
        f"```\n\n"
        f"*Impact migration :*\n"
        f"{recipe.migration_notes}\n"
    )


def _prefix_lines(text: str, prefix: str) -> str:
    """Préfixe chaque ligne (pour rendu diff)."""
    return "\n".join(prefix + line for line in text.splitlines())
