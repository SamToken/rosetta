# Rapport d'Audit Fonctionnel Global
Généré le : 2026-04-26 10:08 | 10 contrôleur(s) analysé(s)

> Ce document est destiné au Product Owner. Il synthétise les règles métier identifiées, les comportements non définis et les questions nécessitant un arbitrage avant migration.

## 1. Résumé Exécutif

### Santé fonctionnelle globale : 🔴 Critique (13.0/100)

| Indicateur | Valeur |
|-----------|--------|
| Contrôleurs analysés | 10 |
| Actions/fonctionnalités | 133 |
| Points d'attention sécurité | 9 |
| Gaps de logique à arbitrer | 211 |
| Services tiers non documentés | 118 |
| Règles métier identifiées | 0 |

### Priorités de correction

| Catégorie | Flags | Action |
|-----------|-------|--------|
| 🔴 CRITICAL_CORRUPTION | 53 | Corriger avant toute MEP |
| 🟠 API_OVERLOAD | 0 | Corriger avant migration |
| 🟡 LOGIC_GAP | 501 | Arbitrage PO requis |

### Périmètre analysé

| Contrôleur | Actions | Points d'attention | Gaps | Score |
|-----------|---------|-------------------|------|-------|
| Agp | 24 | 8 | 52 | 🔴 10.0/100 |
| Variable | 11 | 1 | 35 | 🔴 36.0/100 |
| Oceane | 11 | 0 | 41 | 🔴 40.0/100 |
| OceaneGet | 48 | 0 | 38 | 🔴 48.0/100 |
| Api | 13 | 0 | 14 | 🔴 52.0/100 |
| Abandonner | 16 | 0 | 8 | 🟡 64.0/100 |
| AgirPiloterValidation | 1 | 0 | 15 | 🟡 70.0/100 |
| Validation | 6 | 0 | 0 | 🟢 80.0/100 |
| VariableBase | 2 | 0 | 7 | 🟢 82.0/100 |
| AiguillageIntervenant | 1 | 0 | 1 | 🟢 96.0/100 |

### Recommandations prioritaires

1. **🔑 12 clé(s) de session dynamique(s)** — Vérifier le nettoyage explicite dans tous les chemins de transition de contexte (ASSEMBLEE→CABLE, EQUIPEMENT→CABLE, reclassification Océane). Risque de données périmées chargées silencieusement en production.
2. **🌊 32 lecture(s) d'état Oceane sans fallback** — Vérifier que chaque appel Oceane (getStatutEquipement, getEtatAbonnement…) est protégé par un fallback explicite en cas de timeout ou de réponse vide. Risque de null pointer ou de prise de décision sur donnée absente.
3. **🔢 137 code(s) situation hardcodé(s)** — Remplacer les constantes littérales (ex : 'H1', 'TP2') par des constantes nommées référencées depuis le référentiel Oracle. Risque de désynchronisation si Oracle modifie la codification.
4. **Arbitrage requis sur 211 gap(s) de logique** — Les comportements non définis identifiés dans la section 3 doivent être clarifiés par le Product Owner avant tout développement dans la cible.
5. **9 point(s) d'attention sécurité** — Les pratiques de protection des données identifiées nécessitent une décision sur la politique de sécurité applicable dans la nouvelle architecture.
6. **118 service(s) tiers non documenté(s)** — Chaque service tiers doit faire l'objet d'une fiche de spécification avant d'être intégré à la cible.

---

## 2. Règles Transverses & Redondances

*Aucune règle métier dupliquée détectée sur ce périmètre.*

---

## 3. Décisions requises avant migration

### 🔴 CRITICAL_CORRUPTION — 53 flag(s)
> Corriger avant toute MEP. Ces comportements peuvent corrompre silencieusement les données en production.

| Contrôleur | Méthode | Ligne | Question |
|-----------|---------|-------|---------|
| Abandonner | `abandonnerAuto()` | 561 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins … |
| Abandonner | `preconisationImpactPrioriteAdsl()` | 618 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins … |
| Abandonner | `abandonnerProcessAuto()` | 210 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Abandonner | `abandonnerProcess()` | 293 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Abandonner | `getCommentaireImpactClient()` | 388 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Abandonner | `confirmerBase()` | 507 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Abandonner | `preconisationImpactPrioriteAdsl()` | 652 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Abandonner | `getSeuilsAdelia()` | 948 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Agp | `initAgp()` | 1368 | Cette méthode de protection du secret d'authentification est ancienne et non conforme aux standards … |
| Agp | `initAgp()` | 458 | L'identité de l'agent connecté est lue directement depuis la session. L'habilitation est-elle vérifi… |
| Agp | `displayAgp1()` | 1368 | Cette méthode de protection du secret d'authentification est ancienne et non conforme aux standards … |
| Agp | `displayAgp1()` | 458 | L'identité de l'agent connecté est lue directement depuis la session. L'habilitation est-elle vérifi… |
| Agp | `displayAGP3()` | 458 | L'identité de l'agent connecté est lue directement depuis la session. L'habilitation est-elle vérifi… |
| Agp | `displayAgp2Generique()` | 963 | L'identité de l'agent connecté est lue directement depuis la session. L'habilitation est-elle vérifi… |
| Agp | `displayCreationTocTrans()` | 1368 | Cette méthode de protection du secret d'authentification est ancienne et non conforme aux standards … |
| Agp | `replaceTagsChaineEnchainement()` | 1368 | Cette méthode de protection du secret d'authentification est ancienne et non conforme aux standards … |
| Agp | `initAgp()` | 171 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins … |
| Agp | `displayAgp1()` | 227 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins … |
| Agp | `displayAGP3()` | 413 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins … |
| Agp | `displayAgp1Generique()` | 528 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins … |
| Agp | `displayPiloterGenerique()` | 732 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins … |
| Agp | `getCommentaireAgp2Generique()` | 811 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins … |
| Agp | `displayAgp2Generique()` | 841 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins … |
| Agp | `displayCreationTocTrans()` | 1057 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins … |
| Agp | `displayCreationTocAdsl()` | 1130 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins … |
| Agp | `initAgp()` | 1082 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Agp | `displayAgp1()` | 1082 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Agp | `displayPiloterGenerique()` | 762 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Agp | `getCommentaireAgp2Generique()` | 831 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Agp | `displayAgp2Generique()` | 868 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Agp | `displayCreationTocTrans()` | 1082 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Agp | `creerTicketRessourceAdsl()` | 1150 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Agp | `replaceTagsChaineEnchainement()` | 1316 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Api | `initApi()` | 101 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Api | `createTicket()` | 387 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Api | `updateDateActionEnCoursEds()` | 387 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Api | `getEDSActif()` | 418 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Api | `getEDSPilote()` | 452 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| OceaneGet | `getOceaneData()` | 42 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| OceaneGet | `isChild()` | 471 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Oceane | `getResponseTicketClosure()` | 777 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins … |
| Oceane | `checkOceane()` | 342 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Oceane | `updateOceane()` | 367 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Oceane | `updateOceaneConfirmer()` | 541 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Oceane | `updateOceaneConfirmerTrans()` | 589 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Oceane | `ajoutCommentaireConfirmerTrans()` | 669 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Oceane | `ajoutNbrClientImpacte()` | 699 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Oceane | `updateChampComplementaire()` | 757 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Oceane | `getResponseTicketClosure()` | 784 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Variable | `replaceTagsChaine()` | 265 | Cette méthode de protection du secret d'authentification est ancienne et non conforme aux standards … |
| Variable | `replaceTagsChaine()` | 688 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Variable | `replaceTagsChainePrimoAiguillageTroncon()` | 472 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |
| Variable | `getDataPariv2()` | 688 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Ocean… |

---

### 🟡 LOGIC_GAP — 501 flag(s)
> Arbitrage PO requis avant migration.

*(Voir `details/gaps_complets.md` pour la liste exhaustive des 211 comportement(s) à définir)*

---

## 4. Cartographie du Domaine

### 4.1 Termes Métier non documentés

Ces termes apparaissent dans la logique conditionnelle de plusieurs contrôleurs. Chacun doit être défini dans le référentiel métier de la cible.

| Terme | Contrôleurs | Signification probable |
|-------|------------|----------------------|
| `DSLAM` | Agp, Api | ❓ À documenter |
| `TRONCABLE` | Agp, Variable | ❓ À documenter |
| `donnesTempsReel` | Agp, Variable | ❓ À documenter |
| `driDate` | Oceane, OceaneGet | ❓ À documenter |
| `libSite` | Agp, Variable | ❓ À documenter |
| `replaceValue` | Agp, Variable | ❓ À documenter |
| `resourceSpecification` | Agp, Variable | ❓ À documenter |
| `tabIdentifiants` | Agp, Variable | ❓ À documenter |

### 4.2 Champs de données partagés

*Aucun champ partagé extrait sur ce périmètre.*

### 4.3 Services Tiers Identifiés

Ces composants sont utilisés dans le périmètre analysé sans équivalent identifié dans la cible. Chacun nécessite une fiche de spécification.

| Service | Type | Contrôleurs | Priorité |
|--------|------|------------|---------|
| `Hbm\Common\Tools\StringTools` | use | Abandonner, Agp, Api, Oceane, OceaneGet, Variable | 🔴 Haute |
| `Oft\Mvc\Application` | use | Abandonner, Agp, OceaneGet, Variable, VariableBase | 🔴 Haute |
| `Hbm\Globalapi\Service\Rest\ApiOceane` | use | Abandonner, Agp, Oceane, OceaneGet, Variable | 🔴 Haute |
| `App\Tools\OceaneTools` | use | Agp, Oceane, OceaneGet, Variable, VariableBase | 🔴 Haute |
| `App\Repository\AstroRepository` | use | Abandonner, Agp, AiguillageIntervenant, Variable | 🔴 Haute |
| `App\Tools\OceaneAssistant` | use | Abandonner, Agp, Api, Oceane | 🔴 Haute |
| `OceaneAssistant` | instantiation | Abandonner, Agp, Api, Oceane | 🔴 Haute |
| `ApiOceane` | instantiation | Agp, Oceane, OceaneGet, Variable | 🔴 Haute |
| `App\Tools\Message` | use | Abandonner, Agp, Api | 🔴 Haute |
| `Hbm\Globalapi\Service\Soap\OceaneUpd` | use | Abandonner, Api, Oceane | 🔴 Haute |
| `Message` | instantiation | Abandonner, Agp, Api | 🔴 Haute |
| `Zend\Json\Json` | use | Agp, OceaneGet, Variable | 🔴 Haute |
| `App\Repository\AstroIhmSqlRepository` | use | Abandonner, Agp | 🔴 Haute |
| `App\Repository\AstroLienRepository` | use | Abandonner, Agp | 🔴 Haute |
| `Hbm\Globalapi\Service\Rest\Oceane` | use | Abandonner, Oceane | 🔴 Haute |
| `App\Tools\DroitAstroTools` | use | Abandonner, Agp | 🔴 Haute |
| `Oceane` | instantiation | Abandonner, Oceane | 🔴 Haute |
| `DroitAstroTools` | instantiation | Abandonner, Agp | 🔴 Haute |
| `App\Repository\GlobalApiRepository` | use | Agp, Variable | 🔴 Haute |
| `Hbm\Globalapi\Service\Soap\OceaneFg` | use | Api, Oceane | 🔴 Haute |
| `OceaneFg` | instantiation | Api, Oceane | 🔴 Haute |
| `App\Repository\AbandonBatchRepository` | use | Abandonner | 🟡 Normale |
| `App\Repository\AdeliaRepository` | use | Abandonner | 🟡 Normale |
| `App\Repository\AssistantRepository` | use | Abandonner | 🟡 Normale |
| `App\Repository\VerrouRepository` | use | Abandonner | 🟡 Normale |
| `App\View\Helper\Adelia` | use | Abandonner | 🟡 Normale |
| `Adelia` | instantiation | Abandonner | 🟡 Normale |
| `App\Repository\AgpGeneriqueRepository` | use | Agp | 🟡 Normale |
| `App\Repository\AgpRepository` | use | Agp | 🟡 Normale |
| `App\Repository\EdrRepository` | use | Agp | 🟡 Normale |
| `\App\View\Helper\Edr` | use | Agp | 🟡 Normale |
| `App\Tools\AgpCC` | use | Agp | 🟡 Normale |
| `App\Form\DemandeInterventionForm` | use | Agp | 🟡 Normale |
| `App\Form\DemandeInterventionGeneriqueForm` | use | Agp | 🟡 Normale |
| `App\Form\DemandeInterventionSecondForm` | use | Agp | 🟡 Normale |
| `App\Form\CreaTicketTransForm` | use | Agp | 🟡 Normale |
| `App\Form\CreaTicketAdslForm` | use | Agp | 🟡 Normale |
| `Hbm\Common\Service\LinkService` | use | Agp | 🟡 Normale |
| `App\View\Helper\DemandeIntervention` | use | Agp | 🟡 Normale |
| `DemandeIntervention` | instantiation | Agp | 🟡 Normale |
| `Edr` | instantiation | Agp | 🟡 Normale |
| `DemandeInterventionForm` | instantiation | Agp | 🟡 Normale |
| `DemandeInterventionSecondForm` | instantiation | Agp | 🟡 Normale |
| `AgpCC` | instantiation | Agp | 🟡 Normale |
| `DemandeInterventionGeneriqueForm` | instantiation | Agp | 🟡 Normale |
| `CreaTicketTransForm` | instantiation | Agp | 🟡 Normale |
| `CreaTicketAdslForm` | instantiation | Agp | 🟡 Normale |
| `LinkService` | instantiation | Agp | 🟡 Normale |
| `App\ApiException\BadRequestException` | use | Api | 🟡 Normale |
| `App\ApiException\ScenarioDesactiveException` | use | Api | 🟡 Normale |
| `App\ApiException\PreRequirementException` | use | Api | 🟡 Normale |
| `App\ApiException\UpdateOceaneException` | use | Api | 🟡 Normale |
| `PreRequirementException` | instantiation | Api | 🟡 Normale |
| `BadRequestException` | instantiation | Api | 🟡 Normale |
| `OceaneUpd` | instantiation | Api | 🟡 Normale |
| `UpdateOceaneException` | instantiation | Api | 🟡 Normale |
| `ScenarioDesactiveException` | instantiation | Api | 🟡 Normale |
| `\Oft\Mvc\Application` | use | Oceane | 🟡 Normale |
| `Zend\Validator\NotEmpty` | use | Validation | 🟡 Normale |
| `Zend\Validator\Digits` | use | Validation | 🟡 Normale |
| `Zend\Validator\Date` | use | Validation | 🟡 Normale |
| `Zend\Validator\Regex` | use | Validation | 🟡 Normale |
| `Zend\I18n\Validator\IsInt` | use | Validation | 🟡 Normale |
| `NotEmpty` | instantiation | Validation | 🟡 Normale |
| `Digits` | instantiation | Validation | 🟡 Normale |
| `Date` | instantiation | Validation | 🟡 Normale |
| `Regex` | instantiation | Validation | 🟡 Normale |
| `IsInt` | instantiation | Validation | 🟡 Normale |
| `App\Repository\RefsitesRepository` | use | Variable | 🟡 Normale |
| `App\Repository\VariableRepository` | use | Variable | 🟡 Normale |
| `Hbm\Globalapi\Factory\Pariv2Factory` | use | Variable | 🟡 Normale |
| `Pariv2Factory` | instantiation | Variable | 🟡 Normale |

---
