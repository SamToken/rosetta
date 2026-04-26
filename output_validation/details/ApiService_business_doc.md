# ApiController — Règles Métier
Extrait le : 2026-04-26 | Confiance extraction : 0.6000000000000001

## Méthode : initApi()

### Questions ouvertes pour arbitrage
- [ ] initApi.typeRessourceIadr : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...
- [ ] initApi.descriptionEvtIncident : Le code situation '64' est hardcodé — vient-il d'une table de référence Oracle ?

---

## Méthode : checkTicketType()

### Questions ouvertes pour arbitrage
- [ ] checkTicketType.category : Le code situation '64' est hardcodé — vient-il d'une table de référence Oracle ?

---

## Méthode : createTicket()

### Questions ouvertes pour arbitrage
- [ ] createTicket.oceaneUpdateUrl : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...
- [ ] createTicket.data : Le code situation 'DSLAM' est hardcodé — vient-il d'une table de référence Or...
- [ ] createTicket.data : Le code situation '64' est hardcodé — vient-il d'une table de référence Oracle ?
- [ ] createTicket.dataFg : Le code situation 'Open' est hardcodé — vient-il d'une table de référence Ora...
- [ ] createTicket.partyRole : Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ?
- [ ] createTicket.scenarioExist : Le code situation '0' est hardcodé — vient-il d'une table de référence Oracle ?
- [ ] createTicket.typeScenario : Le code situation 'legacy' est hardcodé — vient-il d'une table de référence O...

---

## Méthode : callEnchainementMethd()

---

## Méthode : callEnchainementCommutMethod()

---

## Méthode : getUserId()

---

## Méthode : updateDateActionEnCoursEds()

### Questions ouvertes pour arbitrage
- [ ] updateDateActionEnCoursEds.oceaneUpdateUrl : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...

---

## Méthode : getEDSActif()

### Questions ouvertes pour arbitrage
- [ ] getEDSActif.result : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...
- [ ] getEDSActif.partyRole : Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ?

---

## Méthode : getEDSPilote()

### Questions ouvertes pour arbitrage
- [ ] getEDSPilote.result : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...

---

## Méthode : getTraceScenarioApi()

---

## Méthode : verifierScenarioExist()

### Questions ouvertes pour arbitrage
- [ ] verifierScenarioExist.scenarioExist : Le code situation '0' est hardcodé — vient-il d'une table de référence Oracle ?

---

## Méthode : verifierActivationScenario()

### Questions ouvertes pour arbitrage
- [ ] verifierActivationScenario.etatScenario : Le code situation '0' est hardcodé — vient-il d'une table de référence Oracle ?

---

## Méthode : verifierTypeScenario()

### Questions ouvertes pour arbitrage
- [ ] verifierTypeScenario.typeScenario : Le code situation '0' est hardcodé — vient-il d'une table de référence Oracle ?
- [ ] verifierTypeScenario.typeScenario : Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ?

---

## Points de décision — Comportements non définis
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('id', 'resultatO'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'userData' et is_array('userData') et !key_exists('message', 'userData'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'data'['type_ressource'] égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'data'['evt_incident'] égal à '64'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'ressource'['ID_TYPE_RESSOURCE'] différent de '1' et 'ressource'['ID_TYPE_RESSOURCE'] différent de '9'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'enchainement' égal à 'TRAITEMENT_ALARME_ADSL'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !'preRequis'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('partyRole'['key']->Local_PartyIntervention->interventionStatus). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'partyRole'['key']->Local_PartyIntervention->interventionStatus['k']->status égal à "Requested" et 'partyRole'['key']->Local_PartyIntervention->interventionStatus['k' + 1]->status égal à "Accepted". Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Valeur de référence**
  - Valeur de référence non documentée — La décision « key_exists('code', 'resultatO') et 'resultatO'['code'] égal à 60 » repose sur la valeur '60'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?
- ⚠️ **Valeur de référence**
  - Valeur de référence non documentée — La décision « 'typeScenario' égal à '0' et 'scenarioType' égal à 'parametrable' » repose sur la valeur 'parametrable'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?
- ⚠️ **Valeur de référence**
  - Valeur de référence non documentée — La décision « 'typeScenario' égal à '1' et 'scenarioType' égal à 'legacy' » repose sur la valeur 'legacy'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

## Services tiers non documentés
- ❓ **App\ApiException\BadRequestException** — Service tiers non documenté — Le composant 'App\ApiException\BadRequestException' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\ApiException\ScenarioDesactiveException** — Service tiers non documenté — Le composant 'App\ApiException\ScenarioDesactiveException' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Tools\OceaneAssistant** — Service tiers non documenté — Le composant 'App\Tools\OceaneAssistant' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Hbm\Common\Tools\StringTools** — Service tiers non documenté — Le composant 'Hbm\Common\Tools\StringTools' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Hbm\Globalapi\Service\Soap\OceaneFg** — Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Soap\OceaneFg' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\ApiException\PreRequirementException** — Service tiers non documenté — Le composant 'App\ApiException\PreRequirementException' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Tools\Message** — Service tiers non documenté — Le composant 'App\Tools\Message' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Hbm\Globalapi\Service\Soap\OceaneUpd** — Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Soap\OceaneUpd' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\ApiException\UpdateOceaneException** — Service tiers non documenté — Le composant 'App\ApiException\UpdateOceaneException' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **OceaneAssistant** — Service tiers non documenté — Le composant 'OceaneAssistant' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Message** — Service tiers non documenté — Le composant 'Message' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **PreRequirementException** — Service tiers non documenté — Le composant 'PreRequirementException' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **BadRequestException** — Service tiers non documenté — Le composant 'BadRequestException' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **OceaneUpd** — Service tiers non documenté — Le composant 'OceaneUpd' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **UpdateOceaneException** — Service tiers non documenté — Le composant 'UpdateOceaneException' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **OceaneFg** — Service tiers non documenté — Le composant 'OceaneFg' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **ScenarioDesactiveException** — Service tiers non documenté — Le composant 'ScenarioDesactiveException' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?

---
**Légende :** ✅ Règle confirmée | 🔴 Point d'attention | ⚠️ Gap à arbitrer | ❓ Service à documenter
