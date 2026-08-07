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

    # -------------------------------------------------------------------------
    # Composants Zend Framework 1 → Symfony 6 (catalogue de référence)
    # Pattern = token de la classe Zend ; flag_type=None (tout flag).
    # -------------------------------------------------------------------------
    Recipe(
        id="zend_form",
        title="Zend_Form → Symfony Form",
        flag_type=None,
        pattern=re.compile(r"\bZend_Form\b"),
        zend_pattern="Formulaire construit avec `Zend_Form` (éléments, décorateurs, validation couplée)",
        symfony_equivalent="`AbstractType` + `FormBuilderInterface`, validation par contraintes sur un DTO/entité",
        diff_before=(
            "$form = new Zend_Form();\n"
            "$form->addElement('text', 'nom', ['required' => true]);"
        ),
        diff_after=(
            "$builder->add('nom', TextType::class, [\n"
            "    'constraints' => [new NotBlank()],\n"
            "]);"
        ),
        migration_notes=(
            "Les décorateurs Zend n'ont pas d'équivalent 1:1 — le rendu passe par des "
            "thèmes de formulaire Twig. Séparer la validation (contraintes) de la "
            "présentation (form theme). Un FormType par formulaire legacy."
        ),
        effort="élevé",
    ),
    Recipe(
        id="zend_auth",
        title="Zend_Auth → Security (authenticator)",
        flag_type=None,
        pattern=re.compile(r"\bZend_Auth\b"),
        zend_pattern="Authentification via `Zend_Auth` + adapter (identité stockée en session)",
        symfony_equivalent="Composant Security : `Authenticator`, `UserProvider`, `security.yaml`",
        diff_before=(
            "$auth = Zend_Auth::getInstance();\n"
            "$result = $auth->authenticate($adapter);"
        ),
        diff_after=(
            "# security.yaml : firewall + provider\n"
            "// login géré par un Authenticator custom ou form_login\n"
            "$user = $this->getUser();"
        ),
        migration_notes=(
            "Le `UserProvider` doit pointer vers la table users legacy. Prévoir le mapping "
            "des rôles (cf. recette $_SESSION). L'identité en session Zend est remplacée par "
            "le token de sécurité Symfony."
        ),
        effort="élevé",
    ),
    Recipe(
        id="zend_db_select",
        title="Zend_Db_Select → Doctrine QueryBuilder",
        flag_type=None,
        pattern=re.compile(r"Zend_Db_Select|->\s*select\s*\(\s*\)"),
        zend_pattern="Requête construite fluently avec `Zend_Db_Select` (`->from()->where()->join()`)",
        symfony_equivalent="`QueryBuilder` Doctrine (`createQueryBuilder`) avec paramètres nommés",
        diff_before=(
            "$select = $db->select()\n"
            "    ->from('enchainements')\n"
            "    ->where('statut = ?', $statut);"
        ),
        diff_after=(
            "$qb = $this->em->createQueryBuilder()\n"
            "    ->select('e')->from(Enchainement::class, 'e')\n"
            "    ->where('e.statut = :statut')->setParameter('statut', $statut);"
        ),
        migration_notes=(
            "Les `where('col = ?', $v)` positionnels deviennent des paramètres nommés. "
            "Attention aux `->join()` implicites Zend : les rendre explicites en DQL avec "
            "les associations d'entités."
        ),
        effort="modéré",
    ),
    Recipe(
        id="zend_log",
        title="Zend_Log → Monolog (LoggerInterface)",
        flag_type=None,
        pattern=re.compile(r"\bZend_Log\b"),
        zend_pattern="Journalisation via `Zend_Log` + writers configurés à la main",
        symfony_equivalent="`Psr\\Log\\LoggerInterface` (Monolog) injecté, canaux via `monolog.yaml`",
        diff_before=(
            "$logger = new Zend_Log(new Zend_Log_Writer_Stream($path));\n"
            "$logger->info('message');"
        ),
        diff_after=(
            "public function __construct(private LoggerInterface $logger) {}\n"
            "$this->logger->info('message');"
        ),
        migration_notes=(
            "Les writers Zend (stream, DB, mail) deviennent des handlers Monolog dans "
            "`monolog.yaml`. Définir un canal dédié par domaine métier pour garder la "
            "granularité des logs legacy."
        ),
        effort="trivial",
    ),
    Recipe(
        id="zend_cache",
        title="Zend_Cache → Symfony Cache (PSR-6/16)",
        flag_type=None,
        pattern=re.compile(r"\bZend_Cache\b"),
        zend_pattern="Cache applicatif via `Zend_Cache::factory()` (frontend/backend)",
        symfony_equivalent="`CacheInterface` (contrats) ou `Psr\\Cache\\CacheItemPoolInterface`, pools dans `cache.yaml`",
        diff_before=(
            "$cache = Zend_Cache::factory('Core', 'File', $fo, $bo);\n"
            "$data = $cache->load($id);"
        ),
        diff_after=(
            "$data = $this->cache->get($id, function (ItemInterface $item) {\n"
            "    $item->expiresAfter(3600);\n"
            "    return $this->computeData();\n"
            "});"
        ),
        migration_notes=(
            "Le pattern load/save Zend devient le callback `get()` (cache-aside natif). "
            "Choisir l'adapter (filesystem, Redis, APCu) selon l'infra cible. Invalider "
            "explicitement via des tags de cache si les clés legacy étaient purgées à la main."
        ),
        effort="modéré",
    ),
    Recipe(
        id="zend_translate",
        title="Zend_Translate → Translation component",
        flag_type=None,
        pattern=re.compile(r"\bZend_Translate\b"),
        zend_pattern="Internationalisation via `Zend_Translate` (adapters Array/Gettext/CSV)",
        symfony_equivalent="`TranslatorInterface` + catalogues `translations/*.yaml|xlf`",
        diff_before="$translate->_('cle.message');",
        diff_after="$this->translator->trans('cle.message');",
        migration_notes=(
            "Convertir les catalogues Zend (CSV/array) en XLIFF ou YAML. Les domaines de "
            "traduction Zend deviennent des domaines Symfony. Vérifier la locale par défaut "
            "et la stratégie de fallback."
        ),
        effort="modéré",
    ),
    Recipe(
        id="zend_validate",
        title="Zend_Validate → Validator (contraintes)",
        flag_type=None,
        pattern=re.compile(r"\bZend_Validate\b|->\s*addValidator\s*\("),
        zend_pattern="Validation impérative via `Zend_Validate_*` (`isValid()` appelé à la main)",
        symfony_equivalent="Contraintes `Symfony\\Component\\Validator\\Constraints` sur DTO/entité, `ValidatorInterface`",
        diff_before=(
            "$validator = new Zend_Validate_EmailAddress();\n"
            "if (!$validator->isValid($email)) { /* … */ }"
        ),
        diff_after=(
            "#[Assert\\Email]\n"
            "private string $email;\n"
            "// $violations = $this->validator->validate($dto);"
        ),
        migration_notes=(
            "Chaque `Zend_Validate_X` a une contrainte équivalente (Email, StringLength, "
            "Regex…). Les validateurs custom deviennent des contraintes custom + Validator. "
            "Regrouper la validation sur le DTO/Form plutôt que dispersée dans le contrôleur."
        ),
        effort="modéré",
    ),
    Recipe(
        id="zend_controller_plugin",
        title="Zend_Controller_Plugin → EventSubscriber",
        flag_type=None,
        pattern=re.compile(r"Zend_Controller_Plugin"),
        zend_pattern="Plugin front-controller (`preDispatch`/`postDispatch`) pour logique transverse",
        symfony_equivalent="`EventSubscriberInterface` sur les événements kernel (`kernel.request`, `kernel.controller`, `kernel.response`)",
        diff_before=(
            "class AuthPlugin extends Zend_Controller_Plugin_Abstract {\n"
            "    public function preDispatch($request) { /* … */ }\n"
            "}"
        ),
        diff_after=(
            "class AuthSubscriber implements EventSubscriberInterface {\n"
            "    public static function getSubscribedEvents(): array {\n"
            "        return [KernelEvents::CONTROLLER => 'onController'];\n"
            "    }\n"
            "}"
        ),
        migration_notes=(
            "Mapper les hooks Zend : `routeStartup/preDispatch` → `kernel.request`, "
            "`postDispatch` → `kernel.response`. La priorité des subscribers remplace "
            "l'ordre d'enregistrement des plugins."
        ),
        effort="modéré",
    ),
    Recipe(
        id="zend_action_helper",
        title="Zend_Controller_Action_Helper → service / argument resolver",
        flag_type=None,
        pattern=re.compile(r"Zend_Controller_Action_Helper|->\s*_helper\s*->"),
        zend_pattern="Action Helper Zend (`$this->_helper->X`) pour factoriser du code de contrôleur",
        symfony_equivalent="Service injecté, ou `ValueResolverInterface` (argument resolver) pour les besoins liés à la requête",
        diff_before="$this->_helper->redirector->gotoUrl('/cible');",
        diff_after="return $this->redirectToRoute('cible_route');",
        migration_notes=(
            "La plupart des helpers Zend (Redirector, FlashMessenger, Url) ont un équivalent "
            "natif dans `AbstractController`. Les helpers métier deviennent des services "
            "injectés dans le contrôleur."
        ),
        effort="modéré",
    ),
    Recipe(
        id="zend_paginator",
        title="Zend_Paginator → KnpPaginatorBundle / Doctrine Paginator",
        flag_type=None,
        pattern=re.compile(r"\bZend_Paginator\b"),
        zend_pattern="Pagination via `Zend_Paginator::factory()`",
        symfony_equivalent="`KnpPaginatorBundle` (intégration Twig) ou `Doctrine\\ORM\\Tools\\Pagination\\Paginator`",
        diff_before="$paginator = Zend_Paginator::factory($items);\n$paginator->setCurrentPageNumber($page);",
        diff_after="$pagination = $this->paginator->paginate($query, $page, 20);",
        migration_notes=(
            "KnpPaginator lit directement une Query Doctrine (pas de chargement complet en "
            "mémoire). Reporter les paramètres de page/limite depuis la requête. Le rendu "
            "pagination Twig remplace les vues de pagination Zend."
        ),
        effort="trivial",
    ),
    Recipe(
        id="zend_navigation",
        title="Zend_Navigation → KnpMenuBundle",
        flag_type=None,
        pattern=re.compile(r"\bZend_Navigation\b"),
        zend_pattern="Menus/breadcrumbs via `Zend_Navigation` (config XML/array + view helpers)",
        symfony_equivalent="`KnpMenuBundle` (MenuBuilder) + voters pour la visibilité par rôle",
        diff_before="$nav = new Zend_Navigation($config);\n// echo $this->navigation()->menu();",
        diff_after="// MenuBuilder::createMainMenu() + {{ knp_menu_render('main') }}",
        migration_notes=(
            "La config de navigation (XML/INI) devient un MenuBuilder PHP. Les ACL de "
            "visibilité Zend_Navigation deviennent des voters ou des tests `is_granted` "
            "dans le builder."
        ),
        effort="modéré",
    ),
    Recipe(
        id="zend_config_ini",
        title="Zend_Config_Ini → .env + services.yaml",
        flag_type=None,
        pattern=re.compile(r"Zend_Config(?:_Ini|_Xml)?\b"),
        zend_pattern="Configuration applicative via `Zend_Config_Ini` (`application.ini`, sections env)",
        symfony_equivalent="Variables `.env`/`.env.local`, `config/packages/*.yaml`, `ParameterBagInterface`",
        diff_before="$config = new Zend_Config_Ini('application.ini', APPLICATION_ENV);",
        diff_after="# .env : DATABASE_URL=...\n// $this->params->get('app.mon_param');",
        migration_notes=(
            "Les sections d'environnement (`production`, `staging`) de `application.ini` "
            "deviennent des fichiers `.env.<env>` et des `when@<env>` dans les YAML. Les "
            "secrets passent par le vault Symfony, pas dans le repo."
        ),
        effort="modéré",
    ),
    Recipe(
        id="zend_bootstrap",
        title="Zend_Application_Bootstrap → Kernel + bundles",
        flag_type=None,
        pattern=re.compile(r"Zend_Application(?:_Bootstrap)?\b"),
        zend_pattern="Amorçage applicatif via `Bootstrap.php` (`_initX()` méthodes)",
        symfony_equivalent="`Kernel`, `config/bundles.php`, compiler passes / services.yaml pour l'initialisation",
        diff_before="protected function _initDb() { /* setup manuel */ }",
        diff_after="// bundles.php + config/packages/doctrine.yaml (auto-wiring)",
        migration_notes=(
            "Chaque `_initX()` du Bootstrap correspond à un package config Symfony ou un "
            "service auto-configuré. L'ordre d'init Zend est remplacé par la résolution de "
            "dépendances du conteneur."
        ),
        effort="élevé",
    ),
    Recipe(
        id="zend_db_table",
        title="Zend_Db_Table → Doctrine Entity + Repository",
        flag_type=None,
        pattern=re.compile(r"Zend_Db_Table\b"),
        zend_pattern="Table Data Gateway `Zend_Db_Table_Abstract` (`$this->fetchAll()`, `$row->save()`)",
        symfony_equivalent="Entité Doctrine (mapping) + Repository ; persistance via `EntityManager`",
        diff_before=(
            "class Enchainements extends Zend_Db_Table_Abstract {\n"
            "    protected $_name = 'enchainements';\n"
            "}"
        ),
        diff_after=(
            "#[ORM\\Entity(repositoryClass: EnchainementRepository::class)]\n"
            "#[ORM\\Table(name: 'enchainements')]\n"
            "class Enchainement { /* … */ }"
        ),
        migration_notes=(
            "Le pattern Row/Rowset actif de Zend devient entité + EntityManager. Conserver "
            "les noms de colonnes Oracle via `#[ORM\\Column(name: '…')]` tant que la base "
            "n'est pas renommée. Les `save()` implicites deviennent `persist()`/`flush()` explicites."
        ),
        effort="élevé",
    ),
    Recipe(
        id="zend_session_namespace",
        title="Zend_Session_Namespace → SessionInterface (bags)",
        flag_type=None,
        pattern=re.compile(r"Zend_Session(?:_Namespace)?\b"),
        zend_pattern="État en session via `new Zend_Session_Namespace('x')`",
        symfony_equivalent="`RequestStack::getSession()` / `SessionInterface`, bags typés pour isoler les namespaces",
        diff_before="$ns = new Zend_Session_Namespace('panier');\n$ns->items = $items;",
        diff_after="$session = $this->requestStack->getSession();\n$session->set('panier.items', $items);",
        migration_notes=(
            "Les namespaces Zend deviennent des préfixes de clés ou des session bags dédiés. "
            "Éviter d'y stocker des objets métier lourds — préférer des identifiants "
            "rechargés depuis la base."
        ),
        effort="modéré",
    ),
    Recipe(
        id="zend_http_client",
        title="Zend_Http_Client → Symfony HttpClient",
        flag_type=None,
        pattern=re.compile(r"Zend_Http_Client\b"),
        zend_pattern="Appels HTTP sortants via `Zend_Http_Client` (souvent synchrones, sans retry)",
        symfony_equivalent="`Symfony\\Contracts\\HttpClient\\HttpClientInterface` (réponses lazy, retry, scoping)",
        diff_before=(
            "$client = new Zend_Http_Client($url);\n"
            "$response = $client->request('GET');\n"
            "$body = $response->getBody();"
        ),
        diff_after=(
            "$response = $this->httpClient->request('GET', $url);\n"
            "$data = $response->toArray();"
        ),
        migration_notes=(
            "Définir des clients scopés (`framework.http_client.scoped_clients`) par API "
            "externe (Oracle REST, services télécom). Activer retry_failed et timeouts "
            "explicites — le legacy n'en a probablement pas."
        ),
        effort="modéré",
    ),
    Recipe(
        id="zend_json",
        title="Zend_Json → json_encode/decode natif",
        flag_type=None,
        pattern=re.compile(r"Zend_Json\b"),
        zend_pattern="Sérialisation via `Zend_Json::encode/decode`",
        symfony_equivalent="`json_encode`/`json_decode` natif, ou `Serializer` pour les objets complexes",
        diff_before="$data = Zend_Json::decode($payload);",
        diff_after="$data = json_decode($payload, true, flags: JSON_THROW_ON_ERROR);",
        migration_notes=(
            "Remplacement quasi mécanique. Ajouter `JSON_THROW_ON_ERROR` pour ne plus avaler "
            "les erreurs de parsing silencieusement. Pour (dé)sérialiser des objets métier, "
            "passer par le composant Serializer."
        ),
        effort="trivial",
    ),
    Recipe(
        id="zend_date",
        title="Zend_Date → DateTimeImmutable",
        flag_type=None,
        pattern=re.compile(r"\bZend_Date\b"),
        zend_pattern="Manipulation de dates via `Zend_Date` (mutable, locale-aware)",
        symfony_equivalent="`DateTimeImmutable` + `IntlDateFormatter` (ou Carbon) pour le formatage localisé",
        diff_before="$date = new Zend_Date();\n$date->addDay(3);",
        diff_after="$date = (new DateTimeImmutable())->modify('+3 days');",
        migration_notes=(
            "Attention à la mutabilité : `Zend_Date` mute en place, `DateTimeImmutable` "
            "retourne une nouvelle instance. Le formatage localisé (mois en français) passe "
            "par IntlDateFormatter, pas par le format Zend."
        ),
        effort="modéré",
    ),
    Recipe(
        id="zend_filter",
        title="Zend_Filter → DataTransformer / callback",
        flag_type=None,
        pattern=re.compile(r"\bZend_Filter\b|->\s*addFilter\s*\("),
        zend_pattern="Filtrage/normalisation de valeurs via `Zend_Filter_*` (StringTrim, StripTags…)",
        symfony_equivalent="`DataTransformerInterface` (dans un Form) ou normalisation explicite dans un service/DTO",
        diff_before=(
            "$filter = new Zend_Filter_StringTrim();\n"
            "$clean = $filter->filter($input);"
        ),
        diff_after=(
            "// dans un Form : ->addModelTransformer(new TrimTransformer())\n"
            "$clean = trim($input);"
        ),
        migration_notes=(
            "Les filtres simples (trim, strtolower) deviennent des appels natifs. Les "
            "chaînes de filtres liées à un formulaire deviennent des DataTransformers. Ne "
            "pas confondre filtrage (transformation) et validation (rejet)."
        ),
        effort="modéré",
    ),
    Recipe(
        id="zend_acl",
        title="Zend_Acl → Security Voter",
        flag_type=None,
        pattern=re.compile(r"\bZend_Acl\b"),
        zend_pattern="Contrôle d'accès via `Zend_Acl` (rôles, ressources, `isAllowed()`)",
        symfony_equivalent="`Voter` Symfony + `#[IsGranted]` / `denyAccessUnlessGranted()`, `RoleHierarchy`",
        diff_before="if ($acl->isAllowed($role, 'enchainement', 'edit')) { /* … */ }",
        diff_after="$this->denyAccessUnlessGranted('EDIT', $enchainement);",
        migration_notes=(
            "Le triplet (rôle, ressource, privilège) de Zend_Acl devient un Voter qui reçoit "
            "l'attribut ('EDIT') et le sujet (l'entité). La hiérarchie de rôles Zend_Acl "
            "devient `security.role_hierarchy`."
        ),
        effort="élevé",
    ),
    Recipe(
        id="zend_layout",
        title="Zend_Layout → template Twig de base (blocks)",
        flag_type=None,
        pattern=re.compile(r"\bZend_Layout\b"),
        zend_pattern="Layout global via `Zend_Layout` (`layout.phtml` + `$this->layout()->content`)",
        symfony_equivalent="Template Twig de base (`base.html.twig`) + `{% extends %}` / `{% block %}`",
        diff_before="// layout.phtml : <?= $this->layout()->content ?>",
        diff_after="{# base.html.twig #}\n{% block body %}{% endblock %}",
        migration_notes=(
            "Le `layout()->content` Zend devient `{% block body %}`. Les placeholders "
            "(`headScript`, `headLink`) deviennent des blocks Twig dédiés. Migrer le layout "
            "en premier : toutes les vues en héritent."
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

    def render_catalog(self) -> str:
        """Rend le catalogue complet en Markdown — handbook de migration
        Zend→Symfony, indépendant des flags détectés. Sert de référence dev/PO."""
        by_effort = {"trivial": 0, "modéré": 0, "élevé": 0}
        for r in self._recipes:
            by_effort[r.effort] = by_effort.get(r.effort, 0) + 1

        lines = [
            "# Catalogue des recettes de migration — Zend Framework 1 → Symfony 6",
            "",
            f"{len(self._recipes)} recette(s) de référence "
            f"(effort : {by_effort.get('trivial', 0)} trivial · "
            f"{by_effort.get('modéré', 0)} modéré · {by_effort.get('élevé', 0)} élevé).",
            "",
            "> Guide déterministe, zéro LLM. Chaque bloc donne l'équivalent Symfony, "
            "un diff indicatif et les pièges de migration. Les exemples sont génériques.",
            "",
            "## Index",
            "",
        ]
        for r in self._recipes:
            lines.append(f"- **{r.title}** — effort {r.effort}")
        lines.append("")
        lines.append("---")
        for r in self._recipes:
            lines.append(_render_block(r))
        return "\n".join(lines)


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
