# OceaneGetController — Règles Métier
Extrait le : 2026-04-26 | Confiance extraction : 0.6000000000000001

## Méthode : getOceaneData()

### Questions ouvertes pour arbitrage
- [ ] getOceaneData.oceaneApiData : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...

---

## Méthode : getRessourceIds()

---

## Méthode : getProductIds()

---

## Méthode : getRessourceType()

---

## Méthode : getProductType()

---

## Méthode : getTicketCharacteristics()

---

## Méthode : getPriority()

---

## Méthode : getUrgency()

---

## Méthode : getCreationDate()

---

## Méthode : getDetectionDate()

---

## Méthode : getDetailProblem()

---

## Méthode : getPilotGroup()

---

## Méthode : getOriginatorGroup()

---

## Méthode : getActionEds()

---

## Méthode : getActifGroup()

---

## Méthode : getInterventionStatus()

---

## Méthode : getStatus()

---

## Méthode : getTicketType()

---

## Méthode : getOrigin()

---

## Méthode : getInstalledRessourceId()

---

## Méthode : getTicketParamsAttribute()

---

## Méthode : getDescription()

---

## Méthode : getId()

---

## Méthode : getHno()

---

## Méthode : getPartyId()

---

## Méthode : getTicketCause()

---

## Méthode : getPosteAssocie()

---

## Méthode : getLibelleSuccinct()

---

## Méthode : isRessource()

---

## Méthode : isChild()

### Questions ouvertes pour arbitrage
- [ ] isChild.oceaneApiData : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...
- [ ] isChild.resultChild : Le code situation 'isParent' est hardcodé — vient-il d'une table de référence...

---

## Méthode : isActivationRequested()

---

## Méthode : getRestorationDate()

---

## Méthode : getResolutionDate()

---

## Méthode : getCategory()

---

## Méthode : getLibelleImputation()

---

## Méthode : isActivationAccpeted()

### Questions ouvertes pour arbitrage
- [ ] isActivationAccpeted.activationAccepted : Le code situation 'Accepted' est hardcodé — vient-il d'une table de référence...

---

## Méthode : activationIdsAndRoles()

### Questions ouvertes pour arbitrage
- [ ] activationIdsAndRoles.activationAccepted : Le code situation 'Accepted' est hardcodé — vient-il d'une table de référence...

---

## Méthode : getCriticity()

---

## Méthode : getTargetRestorationDate()

---

## Méthode : getPlannedRestorationDate()

---

## Méthode : getDateActionInProgress()

---

## Méthode : getActionInProgress()

---

## Méthode : getEdsActionInProgress()

---

## Méthode : getDrDate()

---

## Méthode : getClasitePrio()

### Questions ouvertes pour arbitrage
- [ ] getClasitePrio.value : Le code situation 'CLASITE' est hardcodé — vient-il d'une table de référence ...

---

## Méthode : getRelatedRessource()

---

## Méthode : getUserId()

---

## Méthode : getLogin()

---

## Points de décision — Comportements non définis
- ⚠️ **Gap de logique**
  - Point de décision — 'this'->app->get('AstroBase')->isJson('detailTicketJson'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource']) et key_exists('resourceSpecCharacteristic', 'this'->oceaneData['relatedResource']) et is_array('this'->oceaneData['relatedResource']['resourceSpecCharacteristic']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('relatedService', 'this'->oceaneData) et is_array('this'->oceaneData['relatedService']) et key_exists('serviceSpecCharacteristic', 'this'->oceaneData['relatedService']) et is_array('this'->oceaneData['relatedService']['serviceSpecCharacteristic']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource']) et key_exists('resourceSpecification', 'this'->oceaneData['relatedResource']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('relatedService', 'this'->oceaneData) et is_array('this'->oceaneData['relatedService']) et key_exists('serviceSpecification', 'this'->oceaneData['relatedService']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('troubleTicketCharacteristic', 'this'->oceaneData) et is_array('this'->oceaneData['troubleTicketCharacteristic']) et count('this'->oceaneData['troubleTicketCharacteristic']) > 0. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('priority', 'this'->oceaneData) et is_array('this'->oceaneData['priority']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('urgency', 'this'->oceaneData) et is_array('this'->oceaneData['urgency']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('creationDate', 'this'->oceaneData). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('detectionDate', 'this'->oceaneData). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('troubleCause', 'this'->oceaneData) et is_array('this'->oceaneData['troubleCause']) et count('this'->oceaneData['troubleCause']) > 0. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('value') et key_exists('problemDetail', 'value') et key_exists('id', 'value'['problemDetail']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('relatedParty', 'this'->oceaneData) et is_array('this'->oceaneData['relatedParty']) et count('this'->oceaneData['relatedParty']) > 0. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('value') et key_exists('role', 'value') et 'value'['role'] égal à 'TroubleResolutionLeader' et key_exists('id', 'value'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('value') et key_exists('role', 'value') et 'value'['role'] égal à 'troubleTicketOriginator' et key_exists('id', 'value'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyIntervention']) et count('this'->oceaneData['partyIntervention']) > 0. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('value'['relatedParty']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('valueRelatedParty') et key_exists('actionInProgress', 'valueRelatedParty') et 'valueRelatedParty'['role'] égal à 'TroubleResolutionLeader'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('valueRelatedParty'['actionInProgress']) et key_exists('description', 'valueRelatedParty'['actionInProgress']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('value') et key_exists('role', 'value') et 'value'['role'] égal à 'TroubleResolutionContributor' et key_exists('id', 'value'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyIntervention']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('interventionStatus', 'value') et is_array('value'['interventionStatus']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — (is_array('status') et key_exists('status', 'status')). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('status', 'this'->oceaneData) et is_array('this'->oceaneData['status']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('isCurrentStatus', 'value') et 'value'['isCurrentStatus'] égal à 1. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('ticketType', 'this'->oceaneData) et is_array('this'->oceaneData['ticketType']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('origin', 'this'->oceaneData) et is_array('this'->oceaneData['origin']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource']) et key_exists('id', 'this'->oceaneData['relatedResource']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource']) et key_exists('resourceCharacteristic', 'this'->oceaneData['relatedResource']) et is_array('this'->oceaneData['relatedResource']['resourceCharacteristic']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('value') et key_exists('@type', 'value') et 'value'['@type'] égal à 'param' et key_exists('id', 'value') et 'value'['id'] égal à 'name'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('value') et key_exists('familyName', 'value') et key_exists('id', 'value'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('troubleCause', 'this'->oceaneData) et is_array('this'->oceaneData['troubleCause']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('value') et key_exists('role', 'value') et 'value'['role'] égal à 'WorkingGroup' et key_exists('id', 'value'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('reason', 'value'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'this'->app->get('AstroBase')->isJson('resultChild'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array($resultChild) && !le champ 'resultChild' est vide && !key_exists('code', $resultChild) && key_exists('type', $resultChild[0]) && $resultChild[0]['type'] == 'isParent'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('value') et key_exists('relatedParty', 'value') et is_array('value'['relatedParty']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('party') et key_exists('@referredType', 'party') et 'party'['@referredType'] égal à 'Organisation' et key_exists('role', 'party') et 'party'['role'] égal à 'TroubleResolutionContributor' et key_exists('id', 'party') et 'party'['id'] égal à 'eds'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'isContributor' et key_exists('interventionStatus', 'value') et is_array('value'['interventionStatus']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'activationRequested'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('code', 'value') et 'value'['code'] égal à "Restored". Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('startDate', 'value'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('code', 'value') et 'value'['code'] égal à "Resolved". Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('category', 'this'->oceaneData) et is_array('this'->oceaneData['category']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('party') et key_exists('@referredType', 'party') et 'party'['@referredType'] égal à 'Organisation' et key_exists('role', 'party') et 'party'['role'] égal à 'TroubleResolutionContributor' et key_exists('id', 'party'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'activationAccepted'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('criticity', 'this'->oceaneData) et is_array('this'->oceaneData['criticity']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('targetRestorationDate', 'this'->oceaneData). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('plannedRestorationDate', 'this'->oceaneData). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('relatedParty', 'this'->oceaneData['partyIntervention'][0]) et is_array('this'->oceaneData['partyIntervention'][0]['relatedParty']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('value') et key_exists('actionInProgress', 'value') et key_exists('startDate', 'value'['actionInProgress']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('value') et key_exists('actionInProgress', 'value') et key_exists('description', 'value'['actionInProgress']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('value') et key_exists('id', 'value'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('resourceCharacteristic', 'this'->oceaneData['relatedResource']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('value') et key_exists('id', 'value') et 'value'['id'] égal à 'CLASITE'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('value', 'value'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource']) et key_exists('resourceSpecCharacteristic', 'this'->oceaneData['relatedResource']). Quel est le comportement attendu dans le cas contraire ?

## Services tiers non documentés
- ❓ **Hbm\Common\Tools\StringTools** — Service tiers non documenté — Le composant 'Hbm\Common\Tools\StringTools' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Hbm\Globalapi\Service\Rest\ApiOceane** — Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Rest\ApiOceane' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Oft\Mvc\Application** — Service tiers non documenté — Le composant 'Oft\Mvc\Application' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Zend\Json\Json** — Service tiers non documenté — Le composant 'Zend\Json\Json' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Tools\OceaneTools** — Service tiers non documenté — Le composant 'App\Tools\OceaneTools' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **ApiOceane** — Service tiers non documenté — Le composant 'ApiOceane' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?

---
**Légende :** ✅ Règle confirmée | 🔴 Point d'attention | ⚠️ Gap à arbitrer | ❓ Service à documenter
