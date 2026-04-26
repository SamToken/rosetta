# VariableController — Règles Métier
Extrait le : 2026-04-26 | Confiance extraction : 0.6000000000000001

## Méthode : replaceTagsChaine()

### Points d'attention
- 🔴 **token = base64_encode(md5(date('yyyymmdd') . 'link_astro_charter'))**
  - Cette méthode de protection du secret d'authentification est ancienne et non conforme aux standards actuels. S'agit-il d'une contrainte documentée ou cette protection est-elle prévue pour évoluer lors de la migration ?

### Questions ouvertes pour arbitrage
- [ ] replaceTagsChaine.md5 : cette méthode de protection est-elle une contrainte documentée ?
- [ ] replaceTagsChaine.complementaryField6 : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...
- [ ] replaceTagsChaine.val1 : Le code situation 'LIBSITE' est hardcodé — vient-il d'une table de référence ...
- [ ] replaceTagsChaine.donnesTempsReel : Le code situation 'ok' est hardcodé — vient-il d'une table de référence Oracle ?
- [ ] replaceTagsChaine.replaceValue : Le code situation 'ORANGE' est hardcodé — vient-il d'une table de référence O...
- [ ] replaceTagsChaine.typeRessource : Le code situation 'MIE' est hardcodé — vient-il d'une table de référence Orac...
- [ ] replaceTagsChaine.techno : Le code situation 'FH' est hardcodé — vient-il d'une table de référence Oracle ?

---

## Méthode : transcodage()

---

## Méthode : replaceTagsChainePrimoAiguillageTroncon()

### Questions ouvertes pour arbitrage
- [ ] replaceTagsChainePrimoAiguillageTroncon.this : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...

---

## Méthode : selectExtension()

---

## Méthode : getIntervenant()

### Questions ouvertes pour arbitrage
- [ ] getIntervenant.typeRessource : Le code situation 'MIE' est hardcodé — vient-il d'une table de référence Orac...
- [ ] getIntervenant.techno : Le code situation 'FH' est hardcodé — vient-il d'une table de référence Oracle ?

---

## Méthode : replaceCaractRefSite()

---

## Méthode : replaceCaractRefSiteAgglo()

---

## Méthode : getRefSiteByData()

---

## Méthode : getRefSiteBySGTQS()

---

## Méthode : replaceTagsChainePariV2()

---

## Méthode : getDataPariv2()

### Questions ouvertes pour arbitrage
- [ ] getDataPariv2.complementaryField6 : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...

---

## Points de décision — Comportements non définis
- ⚠️ **Gap de logique**
  - Point de décision — 'arg' égal à 'Temperature' ou 'arg' égal à 'Etat_batterie' ou 'arg' égal à 'Tension_batterie' ou 'arg' égal à 'Element_HS'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('parameters', 'Parameter'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('val1', 'id') et 'val1'->id égal à 'LIBSITE'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'libSite' différent de "". Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'arg' égal à 'DSLAM_PRODUIT_DSLAM' ou 'arg' égal à 'DSLAM_PRODUIT_CHASSIS' ou 'arg' égal à 'DSLAM_PRODUIT_CARTE' ou 'arg' égal à 'DSLAM_PRODUIT_PORT' ou 'arg' égal à 'DSLAM_PRODUIT_PM'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_null('this'->variableRepository). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !'replaceValue'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'replaceValue' différent de '' et !is_null('replaceValue') et !is_array('replaceValue'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — OceaneTools::isValidVariable('replaceValue') et !is_array('replaceValue'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_null('this'->transitoolService). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !isset('this'->findAndGet['message']) et !is_null('this'->findAndGet['installed_resource']) et property_exists('this'->findAndGet['installed_resource'], 'Parameters') et property_exists('this'->findAndGet['installed_resource']->Parameters, 'Parameter'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — OceaneTools::isValidVariable('replaceValue') et gettype('replaceValue') différent de 'boolean'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'this'->typeRessource égal à 'TRONCABLE'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !is_null('this'->findAndGet['installed_service']) et property_exists('this'->findAndGet['installed_service'], 'ServiceSpecification') et property_exists('this'->findAndGet['installed_service']->ServiceSpecification, 'serviceSpecificationCode'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'resourceSpecification' différent de "". Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — count('tabIdentifiants') > 0. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — isset('replaceValue'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'intervenantMatriceRefsite' différent de "###'variableAdministree'###". Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Valeur de référence**
  - Valeur de référence non documentée — La décision « key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok' » repose sur la valeur 'ok'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?
- ⚠️ **Valeur de référence**
  - Valeur de référence non documentée — La décision « OceaneTools::isValidVariable('replaceValue') et gettype('replaceValue') différent de 'boolean' » repose sur la valeur 'boolean'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?
- ⚠️ **Valeur de référence**
  - Valeur de référence non documentée — La décision « gettype('resultQuery') différent de 'boolean' et 'resultQuery' différent de '' et is_array('resultQuery') » repose sur la valeur 'boolean'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

## Services tiers non documentés
- ❓ **App\Repository\AstroRepository** — Service tiers non documenté — Le composant 'App\Repository\AstroRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Repository\RefsitesRepository** — Service tiers non documenté — Le composant 'App\Repository\RefsitesRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Repository\VariableRepository** — Service tiers non documenté — Le composant 'App\Repository\VariableRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Repository\GlobalApiRepository** — Service tiers non documenté — Le composant 'App\Repository\GlobalApiRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Tools\OceaneTools** — Service tiers non documenté — Le composant 'App\Tools\OceaneTools' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Hbm\Common\Tools\StringTools** — Service tiers non documenté — Le composant 'Hbm\Common\Tools\StringTools' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Hbm\Globalapi\Factory\Pariv2Factory** — Service tiers non documenté — Le composant 'Hbm\Globalapi\Factory\Pariv2Factory' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Hbm\Globalapi\Service\Rest\ApiOceane** — Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Rest\ApiOceane' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Oft\Mvc\Application** — Service tiers non documenté — Le composant 'Oft\Mvc\Application' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Zend\Json\Json** — Service tiers non documenté — Le composant 'Zend\Json\Json' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **ApiOceane** — Service tiers non documenté — Le composant 'ApiOceane' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Pariv2Factory** — Service tiers non documenté — Le composant 'Pariv2Factory' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?

---
**Légende :** ✅ Règle confirmée | 🔴 Point d'attention | ⚠️ Gap à arbitrer | ❓ Service à documenter
