# OceaneController — Règles Métier
Extrait le : 2026-04-26 | Confiance extraction : 0.6000000000000001

## Méthode : findAndGetOceane()

---

## Méthode : checkOceane()

### Questions ouvertes pour arbitrage
- [ ] checkOceane.oceaneApiData : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...

---

## Méthode : updateOceane()

### Questions ouvertes pour arbitrage
- [ ] updateOceane.oceaneApiData : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...

---

## Méthode : updateOceaneConfirmer()

### Questions ouvertes pour arbitrage
- [ ] updateOceaneConfirmer.oceaneApiData : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...
- [ ] updateOceaneConfirmer.typeConfirmation : Le code situation 'TYPE2' est hardcodé — vient-il d'une table de référence Or...

---

## Méthode : updateOceaneConfirmerTrans()

### Questions ouvertes pour arbitrage
- [ ] updateOceaneConfirmerTrans.oceaneApiData : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...
- [ ] updateOceaneConfirmerTrans.actifDri : Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ?
- [ ] updateOceaneConfirmerTrans.confirmTowStep : Le code situation 'oui' est hardcodé — vient-il d'une table de référence Orac...

---

## Méthode : ajoutCommentaireConfirmerTrans()

### Questions ouvertes pour arbitrage
- [ ] ajoutCommentaireConfirmerTrans.oceaneApiData : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...

---

## Méthode : ajoutNbrClientImpacte()

### Questions ouvertes pour arbitrage
- [ ] ajoutNbrClientImpacte.oceaneApiData : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...

---

## Méthode : createComment()

### Questions ouvertes pour arbitrage
- [ ] createComment.data : Le code situation '4' est hardcodé — vient-il d'une table de référence Oracle ?

---

## Méthode : updateChampComplementaire()

### Questions ouvertes pour arbitrage
- [ ] updateChampComplementaire.oceaneApiData : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...

---

## Méthode : getUserId()

---

## Méthode : getResponseTicketClosure()

### Questions ouvertes pour arbitrage
- [ ] getResponseTicketClosure.session_key : cette clé est-elle nettoyée dans tous les chemins de sortie ?
- [ ] getResponseTicketClosure.oceaneApiData : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...

---

## Points de décision — Comportements non définis
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('result'->TroubleTicketResponse, 'TroubleTicketResponse'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('troubleTicketResponse'->InstalledResource, 'Parameters') et property_exists('troubleTicketResponse'->InstalledResource->Parameters, 'Parameter'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('val1', 'id') et 'CLASITE' égal à 'val1'->id. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — array_key_exists('2', 'troubleTicketResponse'->local_ComplementaryField) et isset('troubleTicketResponse'->local_ComplementaryField[2]->value). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — array_key_exists('5', 'troubleTicketResponse'->local_ComplementaryField) et isset('troubleTicketResponse'->local_ComplementaryField[5]->value). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — array_key_exists('4', 'troubleTicketResponse'->local_ComplementaryField) et isset('troubleTicketResponse'->local_ComplementaryField[4]->value). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('troubleTicketResponse', 'troubleTicketPriority'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('troubleTicketResponse', 'description'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('troubleTicketResponse', 'local_ShortLabel'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('troubleTicketResponse', 'TroubleCause'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('troubleTicketResponse'->TroubleCause, 'local_internalcomplement'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('troubleTicketResponse'->TroubleCause, 'troubleCauseCodeCategory'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('troubleTicketResponse'->TroubleCause, 'troubleCauseLabel'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('troubleTicketResponse'->TroubleCause, 'troubleCauseDescription'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'driDate' différent de ''. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('troubleTicketResponse', 'PartyRole'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !'checkInc'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('i', 'troubleTicketResponse'->PartyRole) et property_exists('troubleTicketResponse'->PartyRole['i'], 'PartyRoleSet') et property_exists('troubleTicketResponse'->PartyRole['i'], 'partyRoleType') et 'troubleTicketResponse'->PartyRole['i']->partyRoleType égal à 'TroubleResolutionLeader'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('troubleTicketResponse'->PartyRole['i']->PartyRoleSet, 'local_groupactioninprogress'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('troubleTicketResponse'->PartyRole['i']->PartyRoleSet, 'local_groupactioninprogressdate'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'checkIncDate' et 'checkIncAct'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('troubleTicketResponse', 'local_onbhfollowup'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('troubleTicketResponse', 'troubleTicketCategory'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — array_key_exists('ticket_id', 'data') et isset('data'['ticket_id']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — array_key_exists('astroid', 'data') et isset('data'['astroid']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — array_key_exists('party_role_party_ID', 'data') et isset('data'['party_role_party_ID']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — array_key_exists('postes_associe', 'data') et isset('data'['postes_associe']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — array_key_exists('niv_urgence', 'data') et isset('data'['niv_urgence']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — array_key_exists('action_eds', 'data') et isset('data'['action_eds']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — array_key_exists('commentaire_eds', 'data') et isset('data'['commentaire_eds']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — array_key_exists('eds_pilote', 'data') et isset('data'['eds_pilote']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — array_key_exists('local_commentaire', 'data') et isset('data'['local_commentaire']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — array_key_exists('nb_plaintes', 'data') et isset('data'['nb_plaintes']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — array_key_exists('description', 'data') et isset('data'['description']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — array_key_exists('trouble_type', 'data') et isset('data'['trouble_type']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — array_key_exists('trouble_severity', 'data') et isset('data'['trouble_severity']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — array_key_exists('party_set_ID', 'data') et isset('data'['party_set_ID']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !'generique'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'actifDri'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !key_exists('api', 'data'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Valeur de référence**
  - Valeur de référence non documentée — La décision « 'confirmTowStep' égal à 'oui' » repose sur la valeur 'oui'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

## Services tiers non documentés
- ❓ **App\Tools\OceaneTools** — Service tiers non documenté — Le composant 'App\Tools\OceaneTools' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Hbm\Globalapi\Service\Rest\ApiOceane** — Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Rest\ApiOceane' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Hbm\Globalapi\Service\Soap\OceaneUpd** — Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Soap\OceaneUpd' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Hbm\Globalapi\Service\Soap\OceaneFg** — Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Soap\OceaneFg' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Hbm\Globalapi\Service\Rest\Oceane** — Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Rest\Oceane' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Hbm\Common\Tools\StringTools** — Service tiers non documenté — Le composant 'Hbm\Common\Tools\StringTools' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **\Oft\Mvc\Application** — Service tiers non documenté — Le composant '\Oft\Mvc\Application' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Tools\OceaneAssistant** — Service tiers non documenté — Le composant 'App\Tools\OceaneAssistant' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **OceaneAssistant** — Service tiers non documenté — Le composant 'OceaneAssistant' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **OceaneFg** — Service tiers non documenté — Le composant 'OceaneFg' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Oceane** — Service tiers non documenté — Le composant 'Oceane' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **ApiOceane** — Service tiers non documenté — Le composant 'ApiOceane' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?

---
**Légende :** ✅ Règle confirmée | 🔴 Point d'attention | ⚠️ Gap à arbitrer | ❓ Service à documenter
