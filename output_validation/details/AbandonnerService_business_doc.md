# AbandonnerController — Règles Métier
Extrait le : 2026-04-26 | Confiance extraction : 0.6000000000000001

## Méthode : informerClient()

---

## Méthode : displayReservation()

---

## Méthode : abandonnerProcessAuto()

### Questions ouvertes pour arbitrage
- [ ] abandonnerProcessAuto.oceaneApiData : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...

---

## Méthode : abandonnerProcess()

### Questions ouvertes pour arbitrage
- [ ] abandonnerProcess.oceaneApiData : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...

---

## Méthode : getValuePriorite()

---

## Méthode : getNatureImpactClientListe()

---

## Méthode : getOptionsHTML()

---

## Méthode : getCommentaireImpactClient()

### Questions ouvertes pour arbitrage
- [ ] getCommentaireImpactClient.this : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...
- [ ] getCommentaireImpactClient.dataAstro : Le code situation 'o' est hardcodé — vient-il d'une table de référence Oracle ?

---

## Méthode : getCommentaireImpactClientTvNum()

### Questions ouvertes pour arbitrage
- [ ] getCommentaireImpactClientTvNum.dataAstro : Le code situation 'o' est hardcodé — vient-il d'une table de référence Oracle ?

---

## Méthode : getCommentaireImpactClientTemplate()

---

## Méthode : confirmerBase()

### Questions ouvertes pour arbitrage
- [ ] confirmerBase.oceaneApiData : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...

---

## Méthode : abandonnerAuto()

### Questions ouvertes pour arbitrage
- [ ] abandonnerAuto.session_key : cette clé est-elle nettoyée dans tous les chemins de sortie ?

---

## Méthode : getPrioritePreconiseByClasite()

---

## Méthode : preconisationImpactPrioriteAdsl()

### Questions ouvertes pour arbitrage
- [ ] preconisationImpactPrioriteAdsl.session_key : cette clé est-elle nettoyée dans tous les chemins de sortie ?
- [ ] preconisationImpactPrioriteAdsl.arrMatricePrio : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...
- [ ] preconisationImpactPrioriteAdsl.nombreClientEntreprise : Le code situation 'oui' est hardcodé — vient-il d'une table de référence Orac...
- [ ] preconisationImpactPrioriteAdsl.isNetVpn : Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ?

---

## Méthode : preconisationPrioriteTrans()

### Questions ouvertes pour arbitrage
- [ ] preconisationPrioriteTrans.value : Le code situation 'PRIORITE' est hardcodé — vient-il d'une table de référence...
- [ ] preconisationPrioriteTrans.k : Le code situation '_TOTAL' est hardcodé — vient-il d'une table de référence O...

---

## Méthode : getSeuilsAdelia()

### Questions ouvertes pour arbitrage
- [ ] getSeuilsAdelia.this : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...

---

## Points de décision — Comportements non définis
- ⚠️ **Gap de logique**
  - Point de décision — 'incidentEnCours'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'dataAdelia'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'dataAdelia'['TOTAL_CLIENTS'] > 0. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — count('ticket'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !'droitTools'->isIncident('ticketId'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'isApi' égal à 1. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'nombreClientEntreprise' égal à 'oui' ou intval('nombreClientEntreprise') > 0. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !le champ 'adelia' est vide && key_exists('PRESTATIONS', $adelia). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !le champ 'adelia' est vide && !le champ 'prestations' est vide && $prestations != '' && key_exists('NETVPN', $prestations) && $prestations['NETVPN'] > 0. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_null('assemblee'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('CODE', 'value') et 'value'['CODE'] égal à 'PRIORITE'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !'isAssemblee' et !'isEquipementTrans'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array($dataPrioImpact) && !le champ 'dataPrioImpact' est vide && key_exists('impact_result', $dataPrioImpact). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('VoIP', 'dataPrioImpact'['impact_result']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !isset('dataPrioImpact'['impact_result']['service']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — isset('arrayDeclencher'['VoIP']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !is_null('dataPrioImpact') et key_exists('impact_result', 'dataPrioImpact'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'doneFlag' ou is_null('dataPrioImpact') ou !key_exists('impact_result', 'dataPrioImpact'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'doneFlag'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'v' >= 'val' et 'gtrOk' et 'hnoOk'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'v' <= 'val' et 'gtrOk' et 'hnoOk'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('gtr_final', 'dataPrioImpact') et 'dataPrioImpact'['gtr_final'] égal à 'gtr' et 'hnoOk'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'hnoOk'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !is_null('result'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Valeur de référence**
  - Valeur de référence non documentée — La décision « 'dataAstro'['ADELIA_MANUEL'] égal à 'o' » repose sur la valeur 'o'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?
- ⚠️ **Valeur de référence**
  - Valeur de référence non documentée — La décision « 'nombreClientEntreprise' égal à 'oui' ou intval('nombreClientEntreprise') > 0 » repose sur la valeur 'oui'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

## Services tiers non documentés
- ❓ **App\Repository\AbandonBatchRepository** — Service tiers non documenté — Le composant 'App\Repository\AbandonBatchRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Repository\AdeliaRepository** — Service tiers non documenté — Le composant 'App\Repository\AdeliaRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Repository\AssistantRepository** — Service tiers non documenté — Le composant 'App\Repository\AssistantRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Repository\AstroIhmSqlRepository** — Service tiers non documenté — Le composant 'App\Repository\AstroIhmSqlRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Repository\AstroLienRepository** — Service tiers non documenté — Le composant 'App\Repository\AstroLienRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Repository\AstroRepository** — Service tiers non documenté — Le composant 'App\Repository\AstroRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Repository\VerrouRepository** — Service tiers non documenté — Le composant 'App\Repository\VerrouRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Tools\OceaneAssistant** — Service tiers non documenté — Le composant 'App\Tools\OceaneAssistant' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Tools\Message** — Service tiers non documenté — Le composant 'App\Tools\Message' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Hbm\Common\Tools\StringTools** — Service tiers non documenté — Le composant 'Hbm\Common\Tools\StringTools' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Hbm\Globalapi\Service\Soap\OceaneUpd** — Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Soap\OceaneUpd' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Hbm\Globalapi\Service\Rest\Oceane** — Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Rest\Oceane' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\View\Helper\Adelia** — Service tiers non documenté — Le composant 'App\View\Helper\Adelia' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Oft\Mvc\Application** — Service tiers non documenté — Le composant 'Oft\Mvc\Application' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Tools\DroitAstroTools** — Service tiers non documenté — Le composant 'App\Tools\DroitAstroTools' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Hbm\Globalapi\Service\Rest\ApiOceane** — Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Rest\ApiOceane' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Message** — Service tiers non documenté — Le composant 'Message' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Oceane** — Service tiers non documenté — Le composant 'Oceane' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **OceaneAssistant** — Service tiers non documenté — Le composant 'OceaneAssistant' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Adelia** — Service tiers non documenté — Le composant 'Adelia' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **DroitAstroTools** — Service tiers non documenté — Le composant 'DroitAstroTools' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?

---
**Légende :** ✅ Règle confirmée | 🔴 Point d'attention | ⚠️ Gap à arbitrer | ❓ Service à documenter
