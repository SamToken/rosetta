# Rapport d'Audit Fonctionnel Global
Généré le : 2026-04-26 09:46 | 10 contrôleur(s) analysé(s)

> Ce document est destiné au Product Owner. Il synthétise les règles métier identifiées, les comportements non définis et les questions nécessitant un arbitrage avant migration.

## 1. Résumé Exécutif

### Santé fonctionnelle globale : 🔴 Critique (0.0/100)

| Indicateur | Valeur |
|-----------|--------|
| Contrôleurs analysés | 10 |
| Actions/fonctionnalités | 1 |
| Points d'attention sécurité | 0 |
| Gaps de logique à arbitrer | 494 |
| Services tiers non documentés | 118 |
| Règles métier identifiées | 0 |

### Priorités de correction

| Catégorie | Flags | Action |
|-----------|-------|--------|
| 🔴 CRITICAL_CORRUPTION | 0 | Corriger avant toute MEP |
| 🟠 API_OVERLOAD | 0 | Corriger avant migration |
| 🟡 LOGIC_GAP | 648 | Arbitrage PO requis |

### Périmètre analysé

| Contrôleur | Actions | Points d'attention | Gaps | Score |
|-----------|---------|-------------------|------|-------|
| AbandonnerService | 0 | 0 | 60 | 🔴 0.0/100 |
| AgpService | 1 | 0 | 114 | 🔴 0.0/100 |
| ApiService | 0 | 0 | 35 | 🔴 0.0/100 |
| OceaneGetService | 0 | 0 | 107 | 🔴 0.0/100 |
| OceaneService | 0 | 0 | 71 | 🔴 0.0/100 |
| VariableService | 0 | 0 | 74 | 🔴 0.0/100 |
| AgirPiloterValidationService | 0 | 0 | 15 | 🔴 25.0/100 |
| AiguillageIntervenantService | 0 | 0 | 11 | 🔴 43.0/100 |
| VariableBaseService | 0 | 0 | 7 | 🟡 61.0/100 |
| ValidationService | 0 | 0 | 0 | 🟢 80.0/100 |

### Recommandations prioritaires

1. **🔢 1 code(s) situation hardcodé(s)** — Remplacer les constantes littérales (ex : 'H1', 'TP2') par des constantes nommées référencées depuis le référentiel Oracle. Risque de désynchronisation si Oracle modifie la codification.
2. **Arbitrage requis sur 494 gap(s) de logique** — Les comportements non définis identifiés dans la section 3 doivent être clarifiés par le Product Owner avant tout développement dans la cible.
3. **118 service(s) tiers non documenté(s)** — Chaque service tiers doit faire l'objet d'une fiche de spécification avant d'être intégré à la cible.

---

## 2. Règles Transverses & Redondances

*Aucune règle métier dupliquée détectée sur ce périmètre.*

---

## 3. Décisions requises avant migration

### 🟡 LOGIC_GAP — 648 flag(s)
> Arbitrage PO requis avant migration.

*(Voir `details/gaps_complets.md` pour la liste exhaustive des 494 comportement(s) à définir)*

---

## 4. Cartographie du Domaine

### 4.1 Termes Métier non documentés

Ces termes apparaissent dans la logique conditionnelle de plusieurs contrôleurs. Chacun doit être défini dans le référentiel métier de la cible.

| Terme | Contrôleurs | Signification probable |
|-------|------------|----------------------|
| `MIE` | AgpService, AiguillageIntervenantService, VariableService | ❓ À documenter |
| `typeRessource` | AgpService, AiguillageIntervenantService, VariableService | ❓ À documenter |
| `DSLAM` | AgpService, ApiService | ❓ À documenter |
| `TECHNO` | AgpService, AiguillageIntervenantService | ❓ À documenter |
| `TRONCABLE` | AgpService, VariableService | ❓ À documenter |
| `donnesTempsReel` | AgpService, VariableService | ❓ À documenter |
| `drcDate` | OceaneGetService, OceaneService | ❓ À documenter |
| `driDate` | OceaneGetService, OceaneService | ❓ À documenter |
| `intervenantInfos` | AgpService, AiguillageIntervenantService | ❓ À documenter |
| `libSite` | AgpService, VariableService | ❓ À documenter |
| `replaceValue` | AgpService, VariableService | ❓ À documenter |
| `resourceSpecification` | AgpService, VariableService | ❓ À documenter |
| `tabIdentifiants` | AgpService, VariableService | ❓ À documenter |

### 4.2 Champs de données partagés

*Aucun champ partagé extrait sur ce périmètre.*

### 4.3 Services Tiers Identifiés

Ces composants sont utilisés dans le périmètre analysé sans équivalent identifié dans la cible. Chacun nécessite une fiche de spécification.

| Service | Type | Contrôleurs | Priorité |
|--------|------|------------|---------|
| `Hbm\Common\Tools\StringTools` | use | AbandonnerService, AgpService, ApiService, OceaneGetService, OceaneService, VariableService | 🔴 Haute |
| `Oft\Mvc\Application` | use | AbandonnerService, AgpService, OceaneGetService, VariableBaseService, VariableService | 🔴 Haute |
| `Hbm\Globalapi\Service\Rest\ApiOceane` | use | AbandonnerService, AgpService, OceaneGetService, OceaneService, VariableService | 🔴 Haute |
| `App\Tools\OceaneTools` | use | AgpService, OceaneGetService, OceaneService, VariableBaseService, VariableService | 🔴 Haute |
| `App\Repository\AstroRepository` | use | AbandonnerService, AgpService, AiguillageIntervenantService, VariableService | 🔴 Haute |
| `App\Tools\OceaneAssistant` | use | AbandonnerService, AgpService, ApiService, OceaneService | 🔴 Haute |
| `OceaneAssistant` | instantiation | AbandonnerService, AgpService, ApiService, OceaneService | 🔴 Haute |
| `ApiOceane` | instantiation | AgpService, OceaneGetService, OceaneService, VariableService | 🔴 Haute |
| `App\Tools\Message` | use | AbandonnerService, AgpService, ApiService | 🔴 Haute |
| `Hbm\Globalapi\Service\Soap\OceaneUpd` | use | AbandonnerService, ApiService, OceaneService | 🔴 Haute |
| `Message` | instantiation | AbandonnerService, AgpService, ApiService | 🔴 Haute |
| `Zend\Json\Json` | use | AgpService, OceaneGetService, VariableService | 🔴 Haute |
| `App\Repository\AstroIhmSqlRepository` | use | AbandonnerService, AgpService | 🔴 Haute |
| `App\Repository\AstroLienRepository` | use | AbandonnerService, AgpService | 🔴 Haute |
| `Hbm\Globalapi\Service\Rest\Oceane` | use | AbandonnerService, OceaneService | 🔴 Haute |
| `App\Tools\DroitAstroTools` | use | AbandonnerService, AgpService | 🔴 Haute |
| `Oceane` | instantiation | AbandonnerService, OceaneService | 🔴 Haute |
| `DroitAstroTools` | instantiation | AbandonnerService, AgpService | 🔴 Haute |
| `App\Repository\GlobalApiRepository` | use | AgpService, VariableService | 🔴 Haute |
| `Hbm\Globalapi\Service\Soap\OceaneFg` | use | ApiService, OceaneService | 🔴 Haute |
| `OceaneFg` | instantiation | ApiService, OceaneService | 🔴 Haute |
| `App\Repository\AbandonBatchRepository` | use | AbandonnerService | 🟡 Normale |
| `App\Repository\AdeliaRepository` | use | AbandonnerService | 🟡 Normale |
| `App\Repository\AssistantRepository` | use | AbandonnerService | 🟡 Normale |
| `App\Repository\VerrouRepository` | use | AbandonnerService | 🟡 Normale |
| `App\View\Helper\Adelia` | use | AbandonnerService | 🟡 Normale |
| `Adelia` | instantiation | AbandonnerService | 🟡 Normale |
| `App\Repository\AgpGeneriqueRepository` | use | AgpService | 🟡 Normale |
| `App\Repository\AgpRepository` | use | AgpService | 🟡 Normale |
| `App\Repository\EdrRepository` | use | AgpService | 🟡 Normale |
| `\App\View\Helper\Edr` | use | AgpService | 🟡 Normale |
| `App\Tools\AgpCC` | use | AgpService | 🟡 Normale |
| `App\Form\DemandeInterventionForm` | use | AgpService | 🟡 Normale |
| `App\Form\DemandeInterventionGeneriqueForm` | use | AgpService | 🟡 Normale |
| `App\Form\DemandeInterventionSecondForm` | use | AgpService | 🟡 Normale |
| `App\Form\CreaTicketTransForm` | use | AgpService | 🟡 Normale |
| `App\Form\CreaTicketAdslForm` | use | AgpService | 🟡 Normale |
| `Hbm\Common\Service\LinkService` | use | AgpService | 🟡 Normale |
| `App\View\Helper\DemandeIntervention` | use | AgpService | 🟡 Normale |
| `DemandeIntervention` | instantiation | AgpService | 🟡 Normale |
| `Edr` | instantiation | AgpService | 🟡 Normale |
| `DemandeInterventionForm` | instantiation | AgpService | 🟡 Normale |
| `DemandeInterventionSecondForm` | instantiation | AgpService | 🟡 Normale |
| `AgpCC` | instantiation | AgpService | 🟡 Normale |
| `DemandeInterventionGeneriqueForm` | instantiation | AgpService | 🟡 Normale |
| `CreaTicketTransForm` | instantiation | AgpService | 🟡 Normale |
| `CreaTicketAdslForm` | instantiation | AgpService | 🟡 Normale |
| `LinkService` | instantiation | AgpService | 🟡 Normale |
| `App\ApiException\BadRequestException` | use | ApiService | 🟡 Normale |
| `App\ApiException\ScenarioDesactiveException` | use | ApiService | 🟡 Normale |
| `App\ApiException\PreRequirementException` | use | ApiService | 🟡 Normale |
| `App\ApiException\UpdateOceaneException` | use | ApiService | 🟡 Normale |
| `PreRequirementException` | instantiation | ApiService | 🟡 Normale |
| `BadRequestException` | instantiation | ApiService | 🟡 Normale |
| `OceaneUpd` | instantiation | ApiService | 🟡 Normale |
| `UpdateOceaneException` | instantiation | ApiService | 🟡 Normale |
| `ScenarioDesactiveException` | instantiation | ApiService | 🟡 Normale |
| `\Oft\Mvc\Application` | use | OceaneService | 🟡 Normale |
| `Zend\Validator\NotEmpty` | use | ValidationService | 🟡 Normale |
| `Zend\Validator\Digits` | use | ValidationService | 🟡 Normale |
| `Zend\Validator\Date` | use | ValidationService | 🟡 Normale |
| `Zend\Validator\Regex` | use | ValidationService | 🟡 Normale |
| `Zend\I18n\Validator\IsInt` | use | ValidationService | 🟡 Normale |
| `NotEmpty` | instantiation | ValidationService | 🟡 Normale |
| `Digits` | instantiation | ValidationService | 🟡 Normale |
| `Date` | instantiation | ValidationService | 🟡 Normale |
| `Regex` | instantiation | ValidationService | 🟡 Normale |
| `IsInt` | instantiation | ValidationService | 🟡 Normale |
| `App\Repository\RefsitesRepository` | use | VariableService | 🟡 Normale |
| `App\Repository\VariableRepository` | use | VariableService | 🟡 Normale |
| `Hbm\Globalapi\Factory\Pariv2Factory` | use | VariableService | 🟡 Normale |
| `Pariv2Factory` | instantiation | VariableService | 🟡 Normale |

---
