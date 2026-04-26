# Gaps de Documentation — Liste Exhaustive

*Généré le 2026-04-26 14:32 — 353 comportement(s) à définir sur 10 contrôleur(s)*

> Chaque ligne correspond à un comportement du système actuel dont le cas contraire n'est pas documenté.

| # | Contrôleur | Méthode | Ligne | Question métier | Contexte | Statut |
|---|-----------|---------|-------|----------------|----------|--------|
| 1 | Abandonner | `abandonnerAuto()` | L.561 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (tran… | [voir bloc] | ⬜ |
| 2 | Abandonner | `preconisationImpactPrioriteAdsl()` | L.618 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (tran… | [voir bloc] | ⬜ |
| 3 | Abandonner | `abandonnerProcessAuto()` | L.210 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 4 | Abandonner | `abandonnerProcess()` | L.293 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 5 | Abandonner | `getCommentaireImpactClient()` | L.388 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 6 | Abandonner | `confirmerBase()` | L.507 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 7 | Abandonner | `preconisationImpactPrioriteAdsl()` | L.652 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 8 | Abandonner | `getSeuilsAdelia()` | L.948 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 9 | Agp | `displayAGP3()` | L.458 | L'identité de l'agent connecté est lue directement depuis la session. L'habilitation est-elle vérifiée par un service… | [voir bloc] | ⬜ |
| 10 | Agp | `displayAgp2Generique()` | L.963 | L'identité de l'agent connecté est lue directement depuis la session. L'habilitation est-elle vérifiée par un service… | [voir bloc] | ⬜ |
| 11 | Agp | `replaceTagsChaineEnchainement()` | L.1368 | Cette méthode de protection du secret d'authentification est ancienne et non conforme aux standards actuels. S'agit-i… | [voir bloc] | ⬜ |
| 12 | Agp | `initAgp()` | L.171 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (tran… | [voir bloc] | ⬜ |
| 13 | Agp | `displayAgp1()` | L.227 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (tran… | [voir bloc] | ⬜ |
| 14 | Agp | `displayAGP3()` | L.413 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (tran… | [voir bloc] | ⬜ |
| 15 | Agp | `displayAgp1Generique()` | L.528 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (tran… | [voir bloc] | ⬜ |
| 16 | Agp | `displayPiloterGenerique()` | L.732 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (tran… | [voir bloc] | ⬜ |
| 17 | Agp | `getCommentaireAgp2Generique()` | L.811 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (tran… | [voir bloc] | ⬜ |
| 18 | Agp | `displayAgp2Generique()` | L.841 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (tran… | [voir bloc] | ⬜ |
| 19 | Agp | `displayCreationTocTrans()` | L.1057 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (tran… | [voir bloc] | ⬜ |
| 20 | Agp | `displayCreationTocAdsl()` | L.1130 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (tran… | [voir bloc] | ⬜ |
| 21 | Agp | `displayPiloterGenerique()` | L.762 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 22 | Agp | `getCommentaireAgp2Generique()` | L.831 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 23 | Agp | `displayAgp2Generique()` | L.868 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 24 | Agp | `displayCreationTocTrans()` | L.1082 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 25 | Agp | `creerTicketRessourceAdsl()` | L.1150 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 26 | Agp | `replaceTagsChaineEnchainement()` | L.1316 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 27 | Api | `initApi()` | L.101 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 28 | Api | `updateDateActionEnCoursEds()` | L.387 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 29 | Api | `getEDSActif()` | L.418 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 30 | Api | `getEDSPilote()` | L.452 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 31 | OceaneGet | `getOceaneData()` | L.42 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 32 | OceaneGet | `isChild()` | L.471 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 33 | Oceane | `getResponseTicketClosure()` | L.777 | Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (tran… | [voir bloc] | ⬜ |
| 34 | Oceane | `checkOceane()` | L.342 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 35 | Oceane | `updateOceane()` | L.367 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 36 | Oceane | `updateOceaneConfirmer()` | L.541 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 37 | Oceane | `updateOceaneConfirmerTrans()` | L.589 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 38 | Oceane | `ajoutCommentaireConfirmerTrans()` | L.669 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 39 | Oceane | `ajoutNbrClientImpacte()` | L.699 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 40 | Oceane | `updateChampComplementaire()` | L.757 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 41 | Oceane | `getResponseTicketClosure()` | L.784 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 42 | Variable | `replaceTagsChaine()` | L.265 | Cette méthode de protection du secret d'authentification est ancienne et non conforme aux standards actuels. S'agit-i… | [voir bloc] | ⬜ |
| 43 | Variable | `replaceTagsChaine()` | L.114 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 44 | Variable | `replaceTagsChainePrimoAiguillageTroncon()` | L.472 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 45 | Variable | `getDataPariv2()` | L.688 | L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → … | [voir bloc] | ⬜ |
| 46 | Abandonner | `abandonnerProcess()` | L.266 | Point de décision — 'incidentEnCours'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 47 | Abandonner | `getCommentaireImpactClient()` | L.391 | Point de décision — 'dataAdelia'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 48 | Abandonner | `getCommentaireImpactClient()` | L.407 | Point de décision — 'dataAdelia'['TOTAL_CLIENTS'] > 0. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 49 | Abandonner | `getCommentaireImpactClientTvNum()` | L.435 | Point de décision — 'dataAdelia'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 50 | Abandonner | `getCommentaireImpactClientTvNum()` | L.449 | Point de décision — 'dataAdelia'['TOTAL_CLIENTS'] > 0. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 51 | Abandonner | `getCommentaireImpactClientTvNum()` | L.461 | Point de décision — count('ticket'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 52 | Abandonner | `preconisationImpactPrioriteAdsl()` | L.617 | Point de décision — !'droitTools'->isIncident('ticketId'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 53 | Abandonner | `preconisationImpactPrioriteAdsl()` | L.625 | Point de décision — 'isApi' égal à 1. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 54 | Abandonner | `preconisationImpactPrioriteAdsl()` | L.633 | Point de décision — 'nombreClientEntreprise' égal à 'oui' ou intval('nombreClientEntreprise') > 0. Quel est le compor… | [voir bloc] | ⬜ |
| 55 | Abandonner | `preconisationImpactPrioriteAdsl()` | L.639 | Point de décision — !le champ 'adelia' est vide && key_exists('PRESTATIONS', $adelia). Quel est le comportement atten… | [voir bloc] | ⬜ |
| 56 | Abandonner | `preconisationImpactPrioriteAdsl()` | L.643 | Point de décision — !le champ 'adelia' est vide && !le champ 'prestations' est vide && $prestations != '' && key_exis… | [voir bloc] | ⬜ |
| 57 | Abandonner | — | L.733 | Point de décision — is_null('assemblee'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 58 | Abandonner | `preconisationPrioriteTrans()` | L.768 | Point de décision — key_exists('CODE', 'value') et 'value'['CODE'] égal à 'PRIORITE'. Quel est le comportement attend… | [voir bloc] | ⬜ |
| 59 | Abandonner | `preconisationPrioriteTrans()` | L.792 | Point de décision — !'isAssemblee' et !'isEquipementTrans'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 60 | Abandonner | `preconisationPrioriteTrans()` | L.801 | Point de décision — is_array($dataPrioImpact) && !le champ 'dataPrioImpact' est vide && key_exists('impact_result', $… | [voir bloc] | ⬜ |
| 61 | Abandonner | `preconisationPrioriteTrans()` | L.802 | Point de décision — key_exists('VoIP', 'dataPrioImpact'['impact_result']). Quel est le comportement attendu dans le c… | [voir bloc] | ⬜ |
| 62 | Abandonner | `preconisationPrioriteTrans()` | L.816 | Point de décision — !isset('dataPrioImpact'['impact_result']['service']). Quel est le comportement attendu dans le ca… | [voir bloc] | ⬜ |
| 63 | Abandonner | `preconisationPrioriteTrans()` | L.822 | Point de décision — isset('arrayDeclencher'['VoIP']). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 64 | Abandonner | `preconisationPrioriteTrans()` | L.826 | Point de décision — !is_null('dataPrioImpact') et key_exists('impact_result', 'dataPrioImpact'). Quel est le comporte… | [voir bloc] | ⬜ |
| 65 | Abandonner | — | L.879 | Point de décision — 'doneFlag' ou is_null('dataPrioImpact') ou !key_exists('impact_result', 'dataPrioImpact'). Quel e… | [voir bloc] | ⬜ |
| 66 | Abandonner | — | L.884 | Point de décision — 'doneFlag'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 67 | Abandonner | — | L.894 | Point de décision — 'v' >= 'val' et 'gtrOk' et 'hnoOk'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 68 | Abandonner | — | L.899 | Point de décision — 'v' <= 'val' et 'gtrOk' et 'hnoOk'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 69 | Abandonner | — | L.909 | Point de décision — key_exists('gtr_final', 'dataPrioImpact') et 'dataPrioImpact'['gtr_final'] égal à 'gtr' et 'hnoOk… | [voir bloc] | ⬜ |
| 70 | Abandonner | — | L.917 | Point de décision — 'hnoOk'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 71 | Abandonner | `getSeuilsAdelia()` | L.953 | Point de décision — !is_null('result'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 72 | Abandonner | `getCommentaireImpactClient()` | L.408 | Valeur de référence non documentée — La décision « 'dataAstro'['ADELIA_MANUEL'] égal à 'o' » repose sur la valeur 'o'… | [voir bloc] | ⬜ |
| 73 | Abandonner | `getCommentaireImpactClientTvNum()` | L.450 | Valeur de référence non documentée — La décision « 'dataAstro'['ADELIA_MANUEL'] égal à 'o' » repose sur la valeur 'o'… | [voir bloc] | ⬜ |
| 74 | Abandonner | `preconisationImpactPrioriteAdsl()` | L.633 | Valeur de référence non documentée — La décision « 'nombreClientEntreprise' égal à 'oui' ou intval('nombreClientEntre… | [voir bloc] | ⬜ |
| 75 | Abandonner | — | — | Service tiers non documenté — Le composant 'App\Repository\AbandonBatchRepository' est utilisé dans ce périmètre sans… | — | ⬜ |
| 76 | Abandonner | — | — | Service tiers non documenté — Le composant 'App\Repository\AdeliaRepository' est utilisé dans ce périmètre sans équiv… | — | ⬜ |
| 77 | Abandonner | — | — | Service tiers non documenté — Le composant 'App\Repository\AssistantRepository' est utilisé dans ce périmètre sans éq… | — | ⬜ |
| 78 | Abandonner | — | — | Service tiers non documenté — Le composant 'App\Repository\AstroIhmSqlRepository' est utilisé dans ce périmètre sans … | — | ⬜ |
| 79 | Abandonner | — | — | Service tiers non documenté — Le composant 'App\Repository\AstroLienRepository' est utilisé dans ce périmètre sans éq… | — | ⬜ |
| 80 | Abandonner | — | — | Service tiers non documenté — Le composant 'App\Repository\AstroRepository' est utilisé dans ce périmètre sans équiva… | — | ⬜ |
| 81 | Abandonner | — | — | Service tiers non documenté — Le composant 'App\Repository\VerrouRepository' est utilisé dans ce périmètre sans équiv… | — | ⬜ |
| 82 | Abandonner | — | — | Service tiers non documenté — Le composant 'App\Tools\OceaneAssistant' est utilisé dans ce périmètre sans équivalent … | — | ⬜ |
| 83 | Abandonner | — | — | Service tiers non documenté — Le composant 'App\Tools\Message' est utilisé dans ce périmètre sans équivalent identifi… | — | ⬜ |
| 84 | Abandonner | — | — | Service tiers non documenté — Le composant 'Hbm\Common\Tools\StringTools' est utilisé dans ce périmètre sans équivale… | — | ⬜ |
| 85 | Abandonner | — | — | Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Soap\OceaneUpd' est utilisé dans ce périmètre sans … | — | ⬜ |
| 86 | Abandonner | — | — | Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Rest\Oceane' est utilisé dans ce périmètre sans équ… | — | ⬜ |
| 87 | Abandonner | — | — | Service tiers non documenté — Le composant 'App\View\Helper\Adelia' est utilisé dans ce périmètre sans équivalent ide… | — | ⬜ |
| 88 | Abandonner | — | — | Service tiers non documenté — Le composant 'Oft\Mvc\Application' est utilisé dans ce périmètre sans équivalent identi… | — | ⬜ |
| 89 | Abandonner | — | — | Service tiers non documenté — Le composant 'App\Tools\DroitAstroTools' est utilisé dans ce périmètre sans équivalent … | — | ⬜ |
| 90 | Abandonner | — | — | Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Rest\ApiOceane' est utilisé dans ce périmètre sans … | — | ⬜ |
| 91 | Abandonner | — | — | Service tiers non documenté — Le composant 'Message' est utilisé dans ce périmètre sans équivalent identifié dans la … | — | ⬜ |
| 92 | Abandonner | — | — | Service tiers non documenté — Le composant 'Oceane' est utilisé dans ce périmètre sans équivalent identifié dans la c… | — | ⬜ |
| 93 | Abandonner | — | — | Service tiers non documenté — Le composant 'OceaneAssistant' est utilisé dans ce périmètre sans équivalent identifié … | — | ⬜ |
| 94 | Abandonner | — | — | Service tiers non documenté — Le composant 'Adelia' est utilisé dans ce périmètre sans équivalent identifié dans la c… | — | ⬜ |
| 95 | Abandonner | — | — | Service tiers non documenté — Le composant 'DroitAstroTools' est utilisé dans ce périmètre sans équivalent identifié … | — | ⬜ |
| 96 | Abandonner | `getCommentaireImpactClient()` | L.408 | Le code situation 'o' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînem… | [voir bloc] | ⬜ |
| 97 | Abandonner | `getCommentaireImpactClientTvNum()` | L.450 | Le code situation 'o' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînem… | [voir bloc] | ⬜ |
| 98 | Abandonner | `preconisationImpactPrioriteAdsl()` | L.633 | Le code situation 'oui' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîn… | [voir bloc] | ⬜ |
| 99 | Abandonner | `preconisationImpactPrioriteAdsl()` | L.646 | Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînem… | [voir bloc] | ⬜ |
| 100 | Abandonner | `preconisationPrioriteTrans()` | L.768 | Le code situation 'PRIORITE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les en… | [voir bloc] | ⬜ |
| 101 | Abandonner | `preconisationPrioriteTrans()` | L.829 | Le code situation '_TOTAL' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les ench… | [voir bloc] | ⬜ |
| 102 | AgirPiloterValidation | `validateAgirPiloterForm()` | L.23 | Point de décision — key_exists('DATE_RETABLISSEMENT_DEMANDE_INTERVENTION', 'regles') et 'regles'['DATE_RETABLISSEMENT… | [voir bloc] | ⬜ |
| 103 | AgirPiloterValidation | `validateAgirPiloterForm()` | L.25 | Point de décision — !'this'->notEmpty('dateRetab'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 104 | AgirPiloterValidation | `validateAgirPiloterForm()` | L.30 | Point de décision — 'dateRetab' différent de = ''. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 105 | AgirPiloterValidation | `validateAgirPiloterForm()` | L.31 | Point de décision — !'this'->isDate('dateRetab', "d/m/Y H:i"). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 106 | AgirPiloterValidation | `validateAgirPiloterForm()` | L.40 | Point de décision — key_exists('DATE_COURS_EDS_DEMANDE_INTERVENTION', 'regles') et 'regles'['DATE_COURS_EDS_DEMANDE_I… | [voir bloc] | ⬜ |
| 107 | AgirPiloterValidation | `validateAgirPiloterForm()` | L.42 | Point de décision — !'this'->notEmpty('actionCoursEds'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 108 | AgirPiloterValidation | `validateAgirPiloterForm()` | L.47 | Point de décision — 'actionCoursEds' différent de = ''. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 109 | AgirPiloterValidation | `validateAgirPiloterForm()` | L.48 | Point de décision — !'this'->isDate('actionCoursEds', "d/m/Y H:i"). Quel est le comportement attendu dans le cas cont… | [voir bloc] | ⬜ |
| 110 | AgirPiloterValidation | `validateAgirPiloterForm()` | L.56 | Point de décision — key_exists('COMMENTAIRE_DEMANDE_INTERVENTION', 'regles') et 'regles'['COMMENTAIRE_DEMANDE_INTERVE… | [voir bloc] | ⬜ |
| 111 | AgirPiloterValidation | `validateAgirPiloterForm()` | L.58 | Point de décision — !'this'->notEmpty('commentaire'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 112 | AgirPiloterValidation | `validateAgirPiloterForm()` | L.66 | Point de décision — key_exists('ACTION_EN_COURS_EDS', 'regles') et 'regles'['ACTION_EN_COURS_EDS']["OBLIGATOIRE"] éga… | [voir bloc] | ⬜ |
| 113 | AgirPiloterValidation | `validateAgirPiloterForm()` | L.68 | Point de décision — !'this'->notEmpty('actionCoursEds'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 114 | AgirPiloterValidation | `validateAgirPiloterForm()` | L.75 | Point de décision — key_exists('NIVEAU_URGENCE', 'regles') et 'regles'['NIVEAU_URGENCE']["OBLIGATOIRE"] égal à = '1'.… | [voir bloc] | ⬜ |
| 115 | AgirPiloterValidation | `validateAgirPiloterForm()` | L.77 | Point de décision — !'this'->notEmpty('actionCoursEds'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 116 | AgirPiloterValidation | `validateAgirPiloterForm()` | L.83 | Point de décision — !'result'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 117 | AgirPiloterValidation | `validateAgirPiloterForm()` | L.24 | Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînem… | [voir bloc] | ⬜ |
| 118 | Agp | `displayAgp1()` | L.234 | Point de décision — count('deports') > 0. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 119 | Agp | `displayAgp1()` | L.237 | Point de décision — 'maitreDeport'['status'] égal à 'ok'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 120 | Agp | `displayAgp1()` | L.245 | Point de décision — 'master' différent de '' et 'master' différent de 'dslamName'. Quel est le comportement attendu d… | [voir bloc] | ⬜ |
| 121 | Agp | `displayAgp1()` | L.258 | Point de décision — 'alarme' différent de 'dslamName'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 122 | Agp | `displayAgp1Generique()` | L.531 | Point de décision — 'typeRessource' égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 123 | Agp | `displayAgp1Generique()` | L.541 | Point de décision — 'typeRessource' égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 124 | Agp | `displayAgp1Generique()` | L.551 | Point de décision — 'typeRessource' égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 125 | Agp | `displayAgp1Generique()` | L.570 | Point de décision — 'alarme' différent de 'dslamName'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 126 | Agp | `displayAgp1Generique()` | L.575 | Point de décision — count('deports') > 0. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 127 | Agp | `displayAgp1Generique()` | L.578 | Point de décision — 'maitreDeport'['status'] égal à 'ok'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 128 | Agp | `displayAgp1Generique()` | L.586 | Point de décision — 'master' différent de '' et 'master' différent de 'dslamName'. Quel est le comportement attendu d… | [voir bloc] | ⬜ |
| 129 | Agp | `displayAgp1Generique()` | L.598 | Point de décision — !is_null('chassisCarte') et 'chassisCarte' et key_exists('CHASSIS', 'chassisCarte'). Quel est le … | [voir bloc] | ⬜ |
| 130 | Agp | `displayAgp1Generique()` | L.606 | Point de décision — 'typeRessource' égal à 'MIE'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 131 | Agp | `displayAgp1Generique()` | L.611 | Point de décision — 'typeRessource' égal à 'SLN' ou 'typeRessource' égal à 'WDM_SID'. Quel est le comportement attend… | [voir bloc] | ⬜ |
| 132 | Agp | `getOptionsActionsGenerique()` | L.708 | Point de décision — 'typeRessource' égal à 'COMMUT' ou 'typeRessource' égal à 'UNIRACC' ou 'typeRessource' égal à 'CO… | [voir bloc] | ⬜ |
| 133 | Agp | `getOptionsActionsGenerique()` | L.712 | Point de décision — ('typeRessource' égal à 'DSLAM' ou 'typeRessource' égal à 'DSLAMDERCO') et 'data'['id_rsc'] diffé… | [voir bloc] | ⬜ |
| 134 | Agp | `getOptionsActionsGenerique()` | L.717 | Point de décision — !le champ 'ressource' est vide. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 135 | Agp | `displayPiloterGenerique()` | L.731 | Point de décision — !'api'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 136 | Agp | `displayPiloterGenerique()` | L.747 | Point de décision — key_exists('oceaneData'['oceane_priority'], 'priorityHoHno'). Quel est le comportement attendu da… | [voir bloc] | ⬜ |
| 137 | Agp | `displayPiloterGenerique()` | L.775 | Point de décision — !le champ 'blocs' est vide && key_exists(0, $blocs). Quel est le comportement attendu dans le cas… | [voir bloc] | ⬜ |
| 138 | Agp | `displayPiloterGenerique()` | L.777 | Point de décision — 'blocName' différent de 'choix_de_carte_trans' et 'blocName' différent de 'Types_Carte' et 'blocN… | [voir bloc] | ⬜ |
| 139 | Agp | `displayPiloterGenerique()` | L.783 | Point de décision — is_string('data'['id_commentaire']) et 'data'['id_commentaire'] égal à 'DiagSDH'. Quel est le com… | [voir bloc] | ⬜ |
| 140 | Agp | `displayAgp2Generique()` | L.840 | Point de décision — !'api'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 141 | Agp | `displayAgp2Generique()` | L.858 | Point de décision — key_exists('oceaneData'['oceane_priority'], 'priorityHoHno'). Quel est le comportement attendu da… | [voir bloc] | ⬜ |
| 142 | Agp | `displayAgp2Generique()` | L.890 | Point de décision — key_exists('intervenant', 'data') et 'data'['intervenant'] différent de ''. Quel est le comportem… | [voir bloc] | ⬜ |
| 143 | Agp | `displayAgp2Generique()` | L.892 | Point de décision — is_array('segComment') et isset('segComment'['SECOND_COMMENT']) et trim('segComment'['SECOND_COMM… | [voir bloc] | ⬜ |
| 144 | Agp | `displayAgp2Generique()` | L.904 | Point de décision — 'data'['type_ressource'] égal à 'DSLAM' ou 'data'['type_ressource'] égal à 'DSLAMDERCO'. Quel est… | [voir bloc] | ⬜ |
| 145 | Agp | `displayAgp2Generique()` | L.910 | Point de décision — 'astroSession'['type'] égal à 'DSLAM' ou 'astroSession'['type'] égal à 'DSLAMDERCO'. Quel est le … | [voir bloc] | ⬜ |
| 146 | Agp | `displayAgp2Generique()` | L.917 | Point de décision — !le champ 'blocs' est vide && key_exists(0, $blocs). Quel est le comportement attendu dans le cas… | [voir bloc] | ⬜ |
| 147 | Agp | `displayAgp2Generique()` | L.929 | Point de décision — is_string('data'['id_commentaire']) et 'data'['id_commentaire'] égal à 'DiagSDH'. Quel est le com… | [voir bloc] | ⬜ |
| 148 | Agp | `displayAgp2Generique()` | L.941 | Point de décision — 'isDslamTest'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 149 | Agp | `displayAgp2Generique()` | L.967 | Point de décision — 'idRscDslam' différent de = null et 'idRscDslam' différent de = ''. Quel est le comportement atte… | [voir bloc] | ⬜ |
| 150 | Agp | `displayAgp2Generique()` | L.983 | Point de décision — 'data'['agp_ecran'] égal à 0. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 151 | Agp | `displayAgp2Generique()` | L.990 | Point de décision — !'idUrgenceOceane'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 152 | Agp | `getCartesLignes()` | L.1029 | Point de décision — 'dslamArray'['racks']['k']['rackName'] égal à 'chassis'. Quel est le comportement attendu dans le… | [voir bloc] | ⬜ |
| 153 | Agp | `getCartesLignes()` | L.1033 | Point de décision — isset('vv'['category']) et 'vv'['category'] différent de 'carte ligne'. Quel est le comportement … | [voir bloc] | ⬜ |
| 154 | Agp | `getCartesLignes()` | L.1037 | Point de décision — 'test'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 155 | Agp | `displayCreationTocTrans()` | L.1087 | Point de décision — 'data'['type'] égal à 'TRCCABLE' ou 'data'['type'] égal à 'TRONCABLE' ou 'data'['type'] égal à 'C… | [voir bloc] | ⬜ |
| 156 | Agp | `displayCreationTocTrans()` | L.1093 | Point de décision — 'data'['type'] égal à 'SDH' ou 'data'['type'] égal à 'SLN' ou 'data'['type'] égal à 'PDH' ou 'dat… | [voir bloc] | ⬜ |
| 157 | Agp | `displayCreationTocTrans()` | L.1096 | Point de décision — 'data'['type'] égal à 'MIE'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 158 | Agp | `replaceTagsChaineEnchainement()` | L.1292 | Point de décision — 'astroId' égal à ''. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 159 | Agp | `replaceTagsChaineEnchainement()` | L.1298 | Point de décision — !'this'->getOceane. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 160 | Agp | `replaceTagsChaineEnchainement()` | L.1301 | Point de décision — 'this'->ticketId et 'this'->getOceane. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 161 | Agp | `replaceTagsChaineEnchainement()` | L.1309 | Point de décision — 'arg' égal à 'Temperature' ou 'arg' égal à 'Etat_batterie' ou 'arg' égal à 'Tension_batterie' ou … | [voir bloc] | ⬜ |
| 162 | Agp | `replaceTagsChaineEnchainement()` | L.1317 | Point de décision — 'libSite' différent de "". Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 163 | Agp | `replaceTagsChaineEnchainement()` | L.1333 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 164 | Agp | `replaceTagsChaineEnchainement()` | L.1339 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 165 | Agp | `replaceTagsChaineEnchainement()` | L.1346 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 166 | Agp | `replaceTagsChaineEnchainement()` | L.1354 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 167 | Agp | `replaceTagsChaineEnchainement()` | L.1362 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 168 | Agp | `replaceTagsChaineEnchainement()` | L.1374 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 169 | Agp | `replaceTagsChaineEnchainement()` | L.1379 | Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le compo… | [voir bloc] | ⬜ |
| 170 | Agp | `replaceTagsChaineEnchainement()` | L.1387 | Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le compo… | [voir bloc] | ⬜ |
| 171 | Agp | `replaceTagsChaineEnchainement()` | L.1394 | Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le compo… | [voir bloc] | ⬜ |
| 172 | Agp | `replaceTagsChaineEnchainement()` | L.1401 | Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le compo… | [voir bloc] | ⬜ |
| 173 | Agp | `replaceTagsChaineEnchainement()` | L.1416 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 174 | Agp | `replaceTagsChaineEnchainement()` | L.1423 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 175 | Agp | `replaceTagsChaineEnchainement()` | L.1433 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 176 | Agp | `replaceTagsChaineEnchainement()` | L.1440 | Point de décision — !is_null('codeDetecteur'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 177 | Agp | `replaceTagsChaineEnchainement()` | L.1444 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 178 | Agp | `replaceTagsChaineEnchainement()` | L.1466 | Point de décision — OceaneTools::isValidVariable('replaceValue') et gettype('replaceValue') différent de 'boolean'. Q… | [voir bloc] | ⬜ |
| 179 | Agp | `replaceTagsChaineEnchainement()` | L.1471 | Point de décision — 'this'->typeRessource égal à 'TRONCABLE'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 180 | Agp | `replaceTagsChaineEnchainement()` | L.1477 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 181 | Agp | `replaceTagsChaineEnchainement()` | L.1484 | Point de décision — 'this'->globalApiRepository->isVariableAdminExist('arg', 'type'). Quel est le comportement attend… | [voir bloc] | ⬜ |
| 182 | Agp | `replaceTagsChaineEnchainement()` | L.1488 | Point de décision — 'resourceSpecification'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 183 | Agp | `replaceTagsChaineEnchainement()` | L.1491 | Point de décision — count('tabIdentifiants') > 0 et 'this'->ticketId différent de = null. Quel est le comportement at… | [voir bloc] | ⬜ |
| 184 | Agp | `replaceTagsChaineEnchainement()` | L.1493 | Point de décision — isset('replaceValue'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 185 | Agp | `aiguillageManuel()` | L.1525 | Point de décision — 'intervenant' différent de 'ORANGE'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 186 | Agp | `aiguillageManuel()` | L.1557 | Point de décision — is_array('intervenantInfos'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 187 | Agp | `aiguillageManuel()` | L.1569 | Point de décision — !is_null('allEcransValues') et is_array('allEcransValues'). Quel est le comportement attendu dans… | [voir bloc] | ⬜ |
| 188 | Agp | `aiguillageCommentaireRemplaceBloc()` | L.1587 | Point de décision — 'Carte_EAN' égal à 'blocName' et key_exists('donnee_cartes', 'allEcranValuesArray'). Quel est le … | [voir bloc] | ⬜ |
| 189 | Agp | `aiguillageCommentaireRemplaceBloc()` | L.1600 | Point de décision — 'keyVariable' différent de 'donnee_cartes' et 'keyVariable' différent de 'CODE_EAN' et 'keyVariab… | [voir bloc] | ⬜ |
| 190 | Agp | `aiguillageCommentaireRemplaceBloc()` | L.1603 | Point de décision — 'keyVariable' égal à 'CODE_EAN'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 191 | Agp | `aiguillageCommentaireRemplaceBloc()` | L.1607 | Point de décision — 'keyTag' égal à 'CODE_EAN'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 192 | Agp | `aiguillageCommentaireRemplaceBloc()` | L.1615 | Point de décision — 'keyVariable' égal à 'Type_Equipement'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 193 | Agp | `aiguillageCommentaireRemplaceBloc()` | L.1619 | Point de décision — 'keyTag' égal à 'TYPE_EQUIPEMENT'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 194 | Agp | `aiguillageCommentaireRemplaceBloc()` | L.1627 | Point de décision — 'keyVariable' égal à 'Nom_Carte'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 195 | Agp | `aiguillageCommentaireRemplaceBloc()` | L.1631 | Point de décision — 'keyTag' égal à 'NOM_CARTE'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 196 | Agp | `aiguillageCommentaireRemplaceBloc()` | L.1675 | Point de décision — 'keyVariable2' différent de 'donnee_cartes'. Quel est le comportement attendu dans le cas contrai… | [voir bloc] | ⬜ |
| 197 | Agp | `aiguillageCommentaireAction()` | L.1692 | Point de décision — 'astroData'['type'] égal à 'DSLAM' ou 'astroData'['type'] égal à 'DSLAMDERCO'. Quel est le compor… | [voir bloc] | ⬜ |
| 198 | Agp | `aiguillageCommentaireAction()` | L.1704 | Point de décision — key_exists('intervenant', 'data') et 'data'['intervenant'] différent de ''. Quel est le comportem… | [voir bloc] | ⬜ |
| 199 | Agp | `aiguillageCommentaireAction()` | L.1706 | Point de décision — is_array('segComment') et isset('segComment'['SECOND_COMMENT']) et trim('segComment'['SECOND_COMM… | [voir bloc] | ⬜ |
| 200 | Agp | `displayAgp1()` | L.237 | Valeur de référence non documentée — La décision « 'maitreDeport'['status'] égal à 'ok' » repose sur la valeur 'ok'. … | [voir bloc] | ⬜ |
| 201 | Agp | `displayAgp1()` | L.248 | Valeur de référence non documentée — La décision « 'maitreDeport'['status'] égal à 'nok' » repose sur la valeur 'nok'… | [voir bloc] | ⬜ |
| 202 | Agp | `displayAgp1Generique()` | L.578 | Valeur de référence non documentée — La décision « 'maitreDeport'['status'] égal à 'ok' » repose sur la valeur 'ok'. … | [voir bloc] | ⬜ |
| 203 | Agp | `displayAgp1Generique()` | L.589 | Valeur de référence non documentée — La décision « 'maitreDeport'['status'] égal à 'nok' » repose sur la valeur 'nok'… | [voir bloc] | ⬜ |
| 204 | Agp | `displayPiloterGenerique()` | L.777 | Valeur de référence non documentée — La décision « 'blocName' différent de 'choix_de_carte_trans' et 'blocName' diffé… | [voir bloc] | ⬜ |
| 205 | Agp | `checkActionInput()` | L.1017 | Valeur de référence non documentée — La décision « in_array('input', 'carteArray') ou (('input' égal à 'alarme') et (… | [voir bloc] | ⬜ |
| 206 | Agp | `checkActionInput()` | L.1017 | Valeur de référence non documentée — La décision « in_array('input', 'carteArray') ou (('input' égal à 'alarme') et (… | [voir bloc] | ⬜ |
| 207 | Agp | `replaceTagsChaineEnchainement()` | L.1379 | Valeur de référence non documentée — La décision « key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat']… | [voir bloc] | ⬜ |
| 208 | Agp | `replaceTagsChaineEnchainement()` | L.1387 | Valeur de référence non documentée — La décision « key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat']… | [voir bloc] | ⬜ |
| 209 | Agp | `replaceTagsChaineEnchainement()` | L.1394 | Valeur de référence non documentée — La décision « key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat']… | [voir bloc] | ⬜ |
| 210 | Agp | `replaceTagsChaineEnchainement()` | L.1401 | Valeur de référence non documentée — La décision « key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat']… | [voir bloc] | ⬜ |
| 211 | Agp | `replaceTagsChaineEnchainement()` | L.1466 | Valeur de référence non documentée — La décision « OceaneTools::isValidVariable('replaceValue') et gettype('replaceVa… | [voir bloc] | ⬜ |
| 212 | Agp | `aiguillageCommentaireRemplaceBloc()` | L.1600 | Valeur de référence non documentée — La décision « 'keyVariable' différent de 'donnee_cartes' et 'keyVariable' différ… | [voir bloc] | ⬜ |
| 213 | Agp | `aiguillageCommentaireRemplaceBloc()` | L.1642 | Valeur de référence non documentée — La décision « $keyVariable == 'donnee_cartes' && !le champ 'blocs' est vide && $… | [voir bloc] | ⬜ |
| 214 | Agp | `aiguillageCommentaireRemplaceBloc()` | L.1642 | Valeur de référence non documentée — La décision « $keyVariable == 'donnee_cartes' && !le champ 'blocs' est vide && $… | [voir bloc] | ⬜ |
| 215 | Agp | `aiguillageCommentaireRemplaceBloc()` | L.1649 | Valeur de référence non documentée — La décision « 'keyTag' égal à 'ean' » repose sur la valeur 'ean'. D'où vient cet… | [voir bloc] | ⬜ |
| 216 | Agp | `aiguillageCommentaireRemplaceBloc()` | L.1675 | Valeur de référence non documentée — La décision « 'keyVariable2' différent de 'donnee_cartes' » repose sur la valeur… | [voir bloc] | ⬜ |
| 217 | Agp | — | — | Service tiers non documenté — Le composant 'App\Repository\AgpGeneriqueRepository' est utilisé dans ce périmètre sans… | — | ⬜ |
| 218 | Agp | — | — | Service tiers non documenté — Le composant 'App\Repository\AgpRepository' est utilisé dans ce périmètre sans équivale… | — | ⬜ |
| 219 | Agp | — | — | Service tiers non documenté — Le composant 'App\Repository\AstroIhmSqlRepository' est utilisé dans ce périmètre sans … | — | ⬜ |
| 220 | Agp | — | — | Service tiers non documenté — Le composant 'App\Repository\AstroLienRepository' est utilisé dans ce périmètre sans éq… | — | ⬜ |
| 221 | Agp | — | — | Service tiers non documenté — Le composant 'App\Repository\AstroRepository' est utilisé dans ce périmètre sans équiva… | — | ⬜ |
| 222 | Agp | — | — | Service tiers non documenté — Le composant 'App\Repository\EdrRepository' est utilisé dans ce périmètre sans équivale… | — | ⬜ |
| 223 | Agp | — | — | Service tiers non documenté — Le composant 'App\Repository\GlobalApiRepository' est utilisé dans ce périmètre sans éq… | — | ⬜ |
| 224 | Agp | — | — | Service tiers non documenté — Le composant 'App\Tools\Message' est utilisé dans ce périmètre sans équivalent identifi… | — | ⬜ |
| 225 | Agp | — | — | Service tiers non documenté — Le composant '\App\View\Helper\Edr' est utilisé dans ce périmètre sans équivalent ident… | — | ⬜ |
| 226 | Agp | — | — | Service tiers non documenté — Le composant 'App\Tools\OceaneAssistant' est utilisé dans ce périmètre sans équivalent … | — | ⬜ |
| 227 | Agp | — | — | Service tiers non documenté — Le composant 'App\Tools\AgpCC' est utilisé dans ce périmètre sans équivalent identifié … | — | ⬜ |
| 228 | Agp | — | — | Service tiers non documenté — Le composant 'App\Form\DemandeInterventionForm' est utilisé dans ce périmètre sans équi… | — | ⬜ |
| 229 | Agp | — | — | Service tiers non documenté — Le composant 'App\Form\DemandeInterventionGeneriqueForm' est utilisé dans ce périmètre … | — | ⬜ |
| 230 | Agp | — | — | Service tiers non documenté — Le composant 'App\Form\DemandeInterventionSecondForm' est utilisé dans ce périmètre san… | — | ⬜ |
| 231 | Agp | — | — | Service tiers non documenté — Le composant 'App\Form\CreaTicketTransForm' est utilisé dans ce périmètre sans équivale… | — | ⬜ |
| 232 | Agp | — | — | Service tiers non documenté — Le composant 'App\Form\CreaTicketAdslForm' est utilisé dans ce périmètre sans équivalen… | — | ⬜ |
| 233 | Agp | — | — | Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Rest\ApiOceane' est utilisé dans ce périmètre sans … | — | ⬜ |
| 234 | Agp | — | — | Service tiers non documenté — Le composant 'Hbm\Common\Service\LinkService' est utilisé dans ce périmètre sans équiva… | — | ⬜ |
| 235 | Agp | — | — | Service tiers non documenté — Le composant 'App\View\Helper\DemandeIntervention' est utilisé dans ce périmètre sans é… | — | ⬜ |
| 236 | Agp | — | — | Service tiers non documenté — Le composant 'App\Tools\DroitAstroTools' est utilisé dans ce périmètre sans équivalent … | — | ⬜ |
| 237 | Agp | — | — | Service tiers non documenté — Le composant 'App\Tools\OceaneTools' est utilisé dans ce périmètre sans équivalent iden… | — | ⬜ |
| 238 | Agp | — | — | Service tiers non documenté — Le composant 'Hbm\Common\Tools\StringTools' est utilisé dans ce périmètre sans équivale… | — | ⬜ |
| 239 | Agp | — | — | Service tiers non documenté — Le composant 'Oft\Mvc\Application' est utilisé dans ce périmètre sans équivalent identi… | — | ⬜ |
| 240 | Agp | — | — | Service tiers non documenté — Le composant 'Zend\Json\Json' est utilisé dans ce périmètre sans équivalent identifié d… | — | ⬜ |
| 241 | Agp | — | — | Service tiers non documenté — Le composant 'DemandeIntervention' est utilisé dans ce périmètre sans équivalent identi… | — | ⬜ |
| 242 | Agp | — | — | Service tiers non documenté — Le composant 'Edr' est utilisé dans ce périmètre sans équivalent identifié dans la cibl… | — | ⬜ |
| 243 | Agp | — | — | Service tiers non documenté — Le composant 'DroitAstroTools' est utilisé dans ce périmètre sans équivalent identifié … | — | ⬜ |
| 244 | Agp | — | — | Service tiers non documenté — Le composant 'DemandeInterventionForm' est utilisé dans ce périmètre sans équivalent id… | — | ⬜ |
| 245 | Agp | — | — | Service tiers non documenté — Le composant 'DemandeInterventionSecondForm' est utilisé dans ce périmètre sans équival… | — | ⬜ |
| 246 | Agp | — | — | Service tiers non documenté — Le composant 'AgpCC' est utilisé dans ce périmètre sans équivalent identifié dans la ci… | — | ⬜ |
| 247 | Agp | — | — | Service tiers non documenté — Le composant 'DemandeInterventionGeneriqueForm' est utilisé dans ce périmètre sans équi… | — | ⬜ |
| 248 | Agp | — | — | Service tiers non documenté — Le composant 'OceaneAssistant' est utilisé dans ce périmètre sans équivalent identifié … | — | ⬜ |
| 249 | Agp | — | — | Service tiers non documenté — Le composant 'CreaTicketTransForm' est utilisé dans ce périmètre sans équivalent identi… | — | ⬜ |
| 250 | Agp | — | — | Service tiers non documenté — Le composant 'CreaTicketAdslForm' est utilisé dans ce périmètre sans équivalent identif… | — | ⬜ |
| 251 | Agp | — | — | Service tiers non documenté — Le composant 'ApiOceane' est utilisé dans ce périmètre sans équivalent identifié dans l… | — | ⬜ |
| 252 | Agp | — | — | Service tiers non documenté — Le composant 'LinkService' est utilisé dans ce périmètre sans équivalent identifié dans… | — | ⬜ |
| 253 | Agp | — | — | Service tiers non documenté — Le composant 'Message' est utilisé dans ce périmètre sans équivalent identifié dans la … | — | ⬜ |
| 254 | Agp | `displayAgp1()` | L.237 | Le code situation 'ok' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîne… | [voir bloc] | ⬜ |
| 255 | Agp | `displayAgp1()` | L.248 | Le code situation 'nok' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîn… | [voir bloc] | ⬜ |
| 256 | Agp | `displayAgp1()` | L.273 | Le code situation 'DSLAM' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les encha… | [voir bloc] | ⬜ |
| 257 | Agp | `displayAgp1Generique()` | L.531 | Le code situation 'DSLAM' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les encha… | [voir bloc] | ⬜ |
| 258 | Agp | `displayAgp1Generique()` | L.578 | Le code situation 'ok' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîne… | [voir bloc] | ⬜ |
| 259 | Agp | `displayAgp1Generique()` | L.589 | Le code situation 'nok' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîn… | [voir bloc] | ⬜ |
| 260 | Agp | `displayAgp1Generique()` | L.606 | Le code situation 'MIE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîn… | [voir bloc] | ⬜ |
| 261 | Agp | `displayAgp1Generique()` | L.611 | Le code situation 'SLN' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîn… | [voir bloc] | ⬜ |
| 262 | Agp | `displayAgp1Generique()` | L.611 | Le code situation 'WDM_SID' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enc… | [voir bloc] | ⬜ |
| 263 | Agp | `getOptionsActionsGenerique()` | L.708 | Le code situation 'COMMUT' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les ench… | [voir bloc] | ⬜ |
| 264 | Agp | `getOptionsActionsGenerique()` | L.708 | Le code situation 'UNIRACC' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enc… | [voir bloc] | ⬜ |
| 265 | Agp | `getOptionsActionsGenerique()` | L.708 | Le code situation 'CONNUM' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les ench… | [voir bloc] | ⬜ |
| 266 | Agp | `getOptionsActionsGenerique()` | L.712 | Le code situation 'DSLAM' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les encha… | [voir bloc] | ⬜ |
| 267 | Agp | `displayPiloterGenerique()` | L.748 | Le code situation 'HO' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîne… | [voir bloc] | ⬜ |
| 268 | Agp | `displayPiloterGenerique()` | L.748 | Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînem… | [voir bloc] | ⬜ |
| 269 | Agp | `displayPiloterGenerique()` | L.750 | Le code situation 'HNO' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîn… | [voir bloc] | ⬜ |
| 270 | Agp | `displayPiloterGenerique()` | L.783 | Le code situation 'DiagSDH' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enc… | [voir bloc] | ⬜ |
| 271 | Agp | `displayAgp2Generique()` | L.859 | Le code situation 'HO' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîne… | [voir bloc] | ⬜ |
| 272 | Agp | `displayAgp2Generique()` | L.859 | Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînem… | [voir bloc] | ⬜ |
| 273 | Agp | `displayAgp2Generique()` | L.861 | Le code situation 'HNO' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîn… | [voir bloc] | ⬜ |
| 274 | Agp | `displayAgp2Generique()` | L.904 | Le code situation 'DSLAM' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les encha… | [voir bloc] | ⬜ |
| 275 | Agp | `displayAgp2Generique()` | L.929 | Le code situation 'DiagSDH' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enc… | [voir bloc] | ⬜ |
| 276 | Agp | `checkActionInput()` | L.1017 | Le code situation 'alarme' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les ench… | [voir bloc] | ⬜ |
| 277 | Agp | `checkActionInput()` | L.1017 | Le code situation 'false' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les encha… | [voir bloc] | ⬜ |
| 278 | Agp | `displayCreationTocTrans()` | L.1087 | Le code situation 'TRCCABLE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les en… | [voir bloc] | ⬜ |
| 279 | Agp | `displayCreationTocTrans()` | L.1087 | Le code situation 'CABLE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les encha… | [voir bloc] | ⬜ |
| 280 | Agp | `displayCreationTocTrans()` | L.1093 | Le code situation 'SDH' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîn… | [voir bloc] | ⬜ |
| 281 | Agp | `displayCreationTocTrans()` | L.1093 | Le code situation 'SLN' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîn… | [voir bloc] | ⬜ |
| 282 | Agp | `displayCreationTocTrans()` | L.1093 | Le code situation 'PDH' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîn… | [voir bloc] | ⬜ |
| 283 | Agp | `displayCreationTocTrans()` | L.1093 | Le code situation 'ETH' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîn… | [voir bloc] | ⬜ |
| 284 | Agp | `displayCreationTocTrans()` | L.1093 | Le code situation 'OCH' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîn… | [voir bloc] | ⬜ |
| 285 | Agp | `displayCreationTocTrans()` | L.1093 | Le code situation 'WDM_SID' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enc… | [voir bloc] | ⬜ |
| 286 | Agp | `displayCreationTocTrans()` | L.1096 | Le code situation 'MIE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîn… | [voir bloc] | ⬜ |
| 287 | Agp | `replaceTagsChaineEnchainement()` | L.1379 | Le code situation 'ok' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîne… | [voir bloc] | ⬜ |
| 288 | Agp | `aiguillageCommentaireRemplaceBloc()` | L.1603 | Le code situation 'CODE_EAN' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les en… | [voir bloc] | ⬜ |
| 289 | Agp | `aiguillageCommentaireRemplaceBloc()` | L.1649 | Le code situation 'ean' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîn… | [voir bloc] | ⬜ |
| 290 | Agp | `aiguillageCommentaireRemplaceBloc()` | L.1650 | Le code situation 'True' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaî… | [voir bloc] | ⬜ |
| 291 | Agp | `aiguillageCommentaireRemplaceBloc()` | L.1665 | Le code situation 'Types' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les encha… | [voir bloc] | ⬜ |
| 292 | Agp | `aiguillageCommentaireRemplaceBloc()` | L.1665 | Le code situation 'Complet' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enc… | [voir bloc] | ⬜ |
| 293 | Agp | `aiguillageCommentaireAction()` | L.1692 | Le code situation 'DSLAM' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les encha… | [voir bloc] | ⬜ |
| 294 | AiguillageIntervenant | `getIntervenantInfos()` | L.48 | Point de décision — le champ 'intervenantInfosList' est vide. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 295 | AiguillageIntervenant | `getIntervenantInfos()` | L.62 | Point de décision — strpos('checkVar', 'val') égal à = 0. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 296 | AiguillageIntervenant | `getIntervenantInfos()` | L.65 | Point de décision — strcmp('checkVar', 'val') égal à = 0. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 297 | AiguillageIntervenant | `getIntervenantInfos()` | L.68 | Point de décision — strpos('checkVar', 'val') différent de = false. Quel est le comportement attendu dans le cas cont… | [voir bloc] | ⬜ |
| 298 | AiguillageIntervenant | `getIntervenantInfos()` | L.75 | Point de décision — 'ok'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 299 | AiguillageIntervenant | `getIntervenantInfos()` | L.85 | Point de décision — !is_null('intervenantInfos'['TECHNO']) et 'intervenantInfos'['TECHNO'] différent de '' et 'ok'. Q… | [voir bloc] | ⬜ |
| 300 | AiguillageIntervenant | `getIntervenantInfos()` | L.134 | Point de décision — 'ok'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 301 | AiguillageIntervenant | — | — | Service tiers non documenté — Le composant 'App\Repository\AstroRepository' est utilisé dans ce périmètre sans équiva… | — | ⬜ |
| 302 | AiguillageIntervenant | `getIntervenantInfos()` | L.92 | Le code situation 'EVTFIXE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enc… | [voir bloc] | ⬜ |
| 303 | AiguillageIntervenant | `getIntervenantInfos()` | L.103 | Le code situation 'RS' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîne… | [voir bloc] | ⬜ |
| 304 | AiguillageIntervenant | `getIntervenantInfos()` | L.109 | Le code situation 'MIE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîn… | [voir bloc] | ⬜ |
| 305 | AiguillageIntervenant | `getIntervenantInfos()` | L.122 | Le code situation 'FH' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîne… | [voir bloc] | ⬜ |
| 306 | Api | `initApi()` | L.125 | Point de décision — 'userData' et is_array('userData') et !key_exists('message', 'userData'). Quel est le comportemen… | [voir bloc] | ⬜ |
| 307 | Api | `createTicket()` | L.227 | Point de décision — 'data'['type_ressource'] égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 308 | Api | `createTicket()` | L.233 | Point de décision — 'data'['evt_incident'] égal à '64'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 309 | Api | `createTicket()` | L.240 | Point de décision — 'data'['type_ressource'] égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 310 | Api | `createTicket()` | L.242 | Point de décision — 'ressource'['ID_TYPE_RESSOURCE'] différent de '1' et 'ressource'['ID_TYPE_RESSOURCE'] différent d… | [voir bloc] | ⬜ |
| 311 | Api | `callEnchainementMethd()` | L.263 | Point de décision — 'enchainement' égal à 'TRAITEMENT_ALARME_ADSL'. Quel est le comportement attendu dans le cas cont… | [voir bloc] | ⬜ |
| 312 | Api | `callEnchainementMethd()` | L.273 | Point de décision — !'preRequis'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 313 | Api | `callEnchainementMethd()` | L.284 | Point de décision — !'preRequis'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 314 | Api | `callEnchainementMethd()` | L.304 | Point de décision — !'preRequis'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 315 | Api | `callEnchainementMethd()` | L.315 | Point de décision — !'preRequis'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 316 | Api | `callEnchainementMethd()` | L.326 | Point de décision — !'preRequis'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 317 | Api | `callEnchainementCommutMethod()` | L.351 | Point de décision — !'preRequis'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 318 | Api | `updateDateActionEnCoursEds()` | L.401 | Point de décision — key_exists('faultstring', 'result') et 'result'->faultstring différent de '' et key_exists('detai… | [voir bloc] | ⬜ |
| 319 | Api | `getEDSActif()` | L.419 | Point de décision — isset('result'->TroubleTicketResponse->TroubleTicketResponse). Quel est le comportement attendu d… | [voir bloc] | ⬜ |
| 320 | Api | `getEDSActif()` | L.424 | Point de décision — 'partyRole'['key']->partyRoleType égal à "TroubleResolutionContributor" et property_exists('party… | [voir bloc] | ⬜ |
| 321 | Api | `getEDSActif()` | L.429 | Point de décision — is_array('partyRole'['key']->Local_PartyIntervention->interventionStatus). Quel est le comporteme… | [voir bloc] | ⬜ |
| 322 | Api | `getEDSActif()` | L.431 | Point de décision — 'partyRole'['key']->Local_PartyIntervention->interventionStatus['k']->status égal à "Requested" e… | [voir bloc] | ⬜ |
| 323 | Api | `getEDSPilote()` | L.453 | Point de décision — isset('result'->TroubleTicketResponse->TroubleTicketResponse). Quel est le comportement attendu d… | [voir bloc] | ⬜ |
| 324 | Api | `getEDSPilote()` | L.458 | Point de décision — 'partyRole'['key']->partyRoleType égal à "TroubleResolutionLeader" et property_exists('partyRole'… | [voir bloc] | ⬜ |
| 325 | Api | `getEDSPilote()` | L.461 | Point de décision — is_array('partyRole'['key']->Local_PartyIntervention->interventionStatus). Quel est le comporteme… | [voir bloc] | ⬜ |
| 326 | Api | `getEDSPilote()` | L.463 | Point de décision — 'partyRole'['key']->Local_PartyIntervention->interventionStatus['k']->status égal à "Requested" e… | [voir bloc] | ⬜ |
| 327 | Api | `verifierTypeScenario()` | L.528 | Valeur de référence non documentée — La décision « 'typeScenario' égal à '0' et 'scenarioType' égal à 'parametrable' … | [voir bloc] | ⬜ |
| 328 | Api | — | — | Service tiers non documenté — Le composant 'App\ApiException\BadRequestException' est utilisé dans ce périmètre sans … | — | ⬜ |
| 329 | Api | — | — | Service tiers non documenté — Le composant 'App\ApiException\ScenarioDesactiveException' est utilisé dans ce périmètr… | — | ⬜ |
| 330 | Api | — | — | Service tiers non documenté — Le composant 'App\Tools\OceaneAssistant' est utilisé dans ce périmètre sans équivalent … | — | ⬜ |
| 331 | Api | — | — | Service tiers non documenté — Le composant 'Hbm\Common\Tools\StringTools' est utilisé dans ce périmètre sans équivale… | — | ⬜ |
| 332 | Api | — | — | Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Soap\OceaneFg' est utilisé dans ce périmètre sans é… | — | ⬜ |
| 333 | Api | — | — | Service tiers non documenté — Le composant 'App\ApiException\PreRequirementException' est utilisé dans ce périmètre s… | — | ⬜ |
| 334 | Api | — | — | Service tiers non documenté — Le composant 'App\Tools\Message' est utilisé dans ce périmètre sans équivalent identifi… | — | ⬜ |
| 335 | Api | — | — | Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Soap\OceaneUpd' est utilisé dans ce périmètre sans … | — | ⬜ |
| 336 | Api | — | — | Service tiers non documenté — Le composant 'App\ApiException\UpdateOceaneException' est utilisé dans ce périmètre san… | — | ⬜ |
| 337 | Api | — | — | Service tiers non documenté — Le composant 'OceaneAssistant' est utilisé dans ce périmètre sans équivalent identifié … | — | ⬜ |
| 338 | Api | — | — | Service tiers non documenté — Le composant 'Message' est utilisé dans ce périmètre sans équivalent identifié dans la … | — | ⬜ |
| 339 | Api | — | — | Service tiers non documenté — Le composant 'PreRequirementException' est utilisé dans ce périmètre sans équivalent id… | — | ⬜ |
| 340 | Api | — | — | Service tiers non documenté — Le composant 'BadRequestException' est utilisé dans ce périmètre sans équivalent identi… | — | ⬜ |
| 341 | Api | — | — | Service tiers non documenté — Le composant 'OceaneUpd' est utilisé dans ce périmètre sans équivalent identifié dans l… | — | ⬜ |
| 342 | Api | — | — | Service tiers non documenté — Le composant 'UpdateOceaneException' est utilisé dans ce périmètre sans équivalent iden… | — | ⬜ |
| 343 | Api | — | — | Service tiers non documenté — Le composant 'OceaneFg' est utilisé dans ce périmètre sans équivalent identifié dans la… | — | ⬜ |
| 344 | Api | — | — | Service tiers non documenté — Le composant 'ScenarioDesactiveException' est utilisé dans ce périmètre sans équivalent… | — | ⬜ |
| 345 | Api | `initApi()` | L.120 | Le code situation '64' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîne… | [voir bloc] | ⬜ |
| 346 | Api | `checkTicketType()` | L.214 | Le code situation '64' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîne… | [voir bloc] | ⬜ |
| 347 | Api | `createTicket()` | L.227 | Le code situation 'DSLAM' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les encha… | [voir bloc] | ⬜ |
| 348 | Api | `createTicket()` | L.233 | Le code situation '64' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîne… | [voir bloc] | ⬜ |
| 349 | Api | `getEDSActif()` | L.427 | Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînem… | [voir bloc] | ⬜ |
| 350 | Api | `verifierScenarioExist()` | L.506 | Le code situation '0' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînem… | [voir bloc] | ⬜ |
| 351 | Api | `verifierActivationScenario()` | L.517 | Le code situation '0' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînem… | [voir bloc] | ⬜ |
| 352 | Api | `verifierTypeScenario()` | L.528 | Le code situation '0' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînem… | [voir bloc] | ⬜ |
| 353 | Api | `verifierTypeScenario()` | L.532 | Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînem… | [voir bloc] | ⬜ |
| 354 | Api | `verifierTypeScenario()` | L.532 | Le code situation 'legacy' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les ench… | [voir bloc] | ⬜ |
| 355 | OceaneGet | `getOceaneData()` | L.54 | Point de décision — 'this'->app->get('AstroBase')->isJson('detailTicketJson'). Quel est le comportement attendu dans … | [voir bloc] | ⬜ |
| 356 | OceaneGet | `getRessourceIds()` | L.68 | Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource… | [voir bloc] | ⬜ |
| 357 | OceaneGet | `getProductIds()` | L.88 | Point de décision — key_exists('relatedService', 'this'->oceaneData) et is_array('this'->oceaneData['relatedService']… | [voir bloc] | ⬜ |
| 358 | OceaneGet | `getRessourceType()` | L.107 | Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource… | [voir bloc] | ⬜ |
| 359 | OceaneGet | `getProductType()` | L.129 | Point de décision — key_exists('relatedService', 'this'->oceaneData) et is_array('this'->oceaneData['relatedService']… | [voir bloc] | ⬜ |
| 360 | OceaneGet | `getTicketCharacteristics()` | L.152 | Point de décision — key_exists('troubleTicketCharacteristic', 'this'->oceaneData) et is_array('this'->oceaneData['tro… | [voir bloc] | ⬜ |
| 361 | OceaneGet | `getPriority()` | L.171 | Point de décision — key_exists('priority', 'this'->oceaneData) et is_array('this'->oceaneData['priority']). Quel est … | [voir bloc] | ⬜ |
| 362 | OceaneGet | `getUrgency()` | L.193 | Point de décision — key_exists('urgency', 'this'->oceaneData) et is_array('this'->oceaneData['urgency']). Quel est le… | [voir bloc] | ⬜ |
| 363 | OceaneGet | `getCreationDate()` | L.215 | Point de décision — key_exists('creationDate', 'this'->oceaneData). Quel est le comportement attendu dans le cas cont… | [voir bloc] | ⬜ |
| 364 | OceaneGet | `getDetectionDate()` | L.231 | Point de décision — key_exists('detectionDate', 'this'->oceaneData). Quel est le comportement attendu dans le cas con… | [voir bloc] | ⬜ |
| 365 | OceaneGet | `getDetailProblem()` | L.243 | Point de décision — key_exists('troubleCause', 'this'->oceaneData) et is_array('this'->oceaneData['troubleCause']) et… | [voir bloc] | ⬜ |
| 366 | OceaneGet | `getDetailProblem()` | L.245 | Point de décision — is_array('value') et key_exists('problemDetail', 'value') et key_exists('id', 'value'['problemDet… | [voir bloc] | ⬜ |
| 367 | OceaneGet | `getPilotGroup()` | L.259 | Point de décision — key_exists('relatedParty', 'this'->oceaneData) et is_array('this'->oceaneData['relatedParty']) et… | [voir bloc] | ⬜ |
| 368 | OceaneGet | `getPilotGroup()` | L.261 | Point de décision — is_array('value') et key_exists('role', 'value') et 'value'['role'] égal à 'TroubleResolutionLead… | [voir bloc] | ⬜ |
| 369 | OceaneGet | `getOriginatorGroup()` | L.270 | Point de décision — key_exists('relatedParty', 'this'->oceaneData) et is_array('this'->oceaneData['relatedParty']) et… | [voir bloc] | ⬜ |
| 370 | OceaneGet | `getOriginatorGroup()` | L.272 | Point de décision — is_array('value') et key_exists('role', 'value') et 'value'['role'] égal à 'troubleTicketOriginat… | [voir bloc] | ⬜ |
| 371 | OceaneGet | `getActionEds()` | L.282 | Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyInterven… | [voir bloc] | ⬜ |
| 372 | OceaneGet | `getActionEds()` | L.284 | Point de décision — is_array('value'['relatedParty']). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 373 | OceaneGet | `getActionEds()` | L.286 | Point de décision — is_array('valueRelatedParty') et key_exists('actionInProgress', 'valueRelatedParty') et 'valueRel… | [voir bloc] | ⬜ |
| 374 | OceaneGet | `getActionEds()` | L.287 | Point de décision — is_array('valueRelatedParty'['actionInProgress']) et key_exists('description', 'valueRelatedParty… | [voir bloc] | ⬜ |
| 375 | OceaneGet | `getActifGroup()` | L.298 | Point de décision — key_exists('relatedParty', 'this'->oceaneData) et is_array('this'->oceaneData['relatedParty']) et… | [voir bloc] | ⬜ |
| 376 | OceaneGet | `getActifGroup()` | L.300 | Point de décision — is_array('value') et key_exists('role', 'value') et 'value'['role'] égal à 'TroubleResolutionCont… | [voir bloc] | ⬜ |
| 377 | OceaneGet | `getInterventionStatus()` | L.310 | Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyInterven… | [voir bloc] | ⬜ |
| 378 | OceaneGet | `getInterventionStatus()` | L.312 | Point de décision — key_exists('interventionStatus', 'value') et is_array('value'['interventionStatus']). Quel est le… | [voir bloc] | ⬜ |
| 379 | OceaneGet | `getInterventionStatus()` | L.314 | Point de décision — (is_array('status') et key_exists('status', 'status')). Quel est le comportement attendu dans le … | [voir bloc] | ⬜ |
| 380 | OceaneGet | `getStatus()` | L.326 | Point de décision — key_exists('status', 'this'->oceaneData) et is_array('this'->oceaneData['status']). Quel est le c… | [voir bloc] | ⬜ |
| 381 | OceaneGet | `getStatus()` | L.328 | Point de décision — key_exists('isCurrentStatus', 'value') et 'value'['isCurrentStatus'] égal à 1. Quel est le compor… | [voir bloc] | ⬜ |
| 382 | OceaneGet | `getTicketType()` | L.338 | Point de décision — key_exists('ticketType', 'this'->oceaneData) et is_array('this'->oceaneData['ticketType']). Quel … | [voir bloc] | ⬜ |
| 383 | OceaneGet | `getOrigin()` | L.355 | Point de décision — key_exists('origin', 'this'->oceaneData) et is_array('this'->oceaneData['origin']). Quel est le c… | [voir bloc] | ⬜ |
| 384 | OceaneGet | `getInstalledRessourceId()` | L.373 | Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource… | [voir bloc] | ⬜ |
| 385 | OceaneGet | `getTicketParamsAttribute()` | L.382 | Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource… | [voir bloc] | ⬜ |
| 386 | OceaneGet | `getTicketParamsAttribute()` | L.384 | Point de décision — is_array('value') et key_exists('@type', 'value') et 'value'['@type'] égal à 'param' et key_exist… | [voir bloc] | ⬜ |
| 387 | OceaneGet | `getPartyId()` | L.407 | Point de décision — key_exists('relatedParty', 'this'->oceaneData) et is_array('this'->oceaneData['relatedParty']) et… | [voir bloc] | ⬜ |
| 388 | OceaneGet | `getPartyId()` | L.409 | Point de décision — is_array('value') et key_exists('familyName', 'value') et key_exists('id', 'value'). Quel est le … | [voir bloc] | ⬜ |
| 389 | OceaneGet | `getTicketCause()` | L.419 | Point de décision — key_exists('troubleCause', 'this'->oceaneData) et is_array('this'->oceaneData['troubleCause']). Q… | [voir bloc] | ⬜ |
| 390 | OceaneGet | `getPosteAssocie()` | L.427 | Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyInterven… | [voir bloc] | ⬜ |
| 391 | OceaneGet | `getPosteAssocie()` | L.428 | Point de décision — key_exists('relatedParty', 'this'->oceaneData) et is_array('this'->oceaneData['relatedParty']) et… | [voir bloc] | ⬜ |
| 392 | OceaneGet | `getPosteAssocie()` | L.430 | Point de décision — is_array('value') et key_exists('role', 'value') et 'value'['role'] égal à 'WorkingGroup' et key_… | [voir bloc] | ⬜ |
| 393 | OceaneGet | `getLibelleSuccinct()` | L.441 | Point de décision — key_exists('status', 'this'->oceaneData) et is_array('this'->oceaneData['status']). Quel est le c… | [voir bloc] | ⬜ |
| 394 | OceaneGet | `getLibelleSuccinct()` | L.443 | Point de décision — key_exists('reason', 'value'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 395 | OceaneGet | `isRessource()` | L.457 | Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource… | [voir bloc] | ⬜ |
| 396 | OceaneGet | `isChild()` | L.479 | Point de décision — 'this'->app->get('AstroBase')->isJson('resultChild'). Quel est le comportement attendu dans le ca… | [voir bloc] | ⬜ |
| 397 | OceaneGet | `isChild()` | L.481 | Point de décision — is_array($resultChild) && !le champ 'resultChild' est vide && !key_exists('code', $resultChild) &… | [voir bloc] | ⬜ |
| 398 | OceaneGet | `isActivationRequested()` | L.497 | Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyInterven… | [voir bloc] | ⬜ |
| 399 | OceaneGet | `isActivationRequested()` | L.499 | Point de décision — is_array('value') et key_exists('relatedParty', 'value') et is_array('value'['relatedParty']). Qu… | [voir bloc] | ⬜ |
| 400 | OceaneGet | `isActivationRequested()` | L.501 | Point de décision — is_array('party') et key_exists('@referredType', 'party') et 'party'['@referredType'] égal à 'Org… | [voir bloc] | ⬜ |
| 401 | OceaneGet | `isActivationRequested()` | L.506 | Point de décision — 'isContributor' et key_exists('interventionStatus', 'value') et is_array('value'['interventionSta… | [voir bloc] | ⬜ |
| 402 | OceaneGet | `isActivationRequested()` | L.513 | Point de décision — 'activationRequested'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 403 | OceaneGet | `getRestorationDate()` | L.522 | Point de décision — key_exists('status', 'this'->oceaneData) et is_array('this'->oceaneData['status']). Quel est le c… | [voir bloc] | ⬜ |
| 404 | OceaneGet | `getRestorationDate()` | L.524 | Point de décision — key_exists('code', 'value') et 'value'['code'] égal à "Restored". Quel est le comportement attend… | [voir bloc] | ⬜ |
| 405 | OceaneGet | `getRestorationDate()` | L.525 | Point de décision — key_exists('startDate', 'value'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 406 | OceaneGet | `getResolutionDate()` | L.539 | Point de décision — key_exists('status', 'this'->oceaneData) et is_array('this'->oceaneData['status']). Quel est le c… | [voir bloc] | ⬜ |
| 407 | OceaneGet | `getResolutionDate()` | L.541 | Point de décision — key_exists('code', 'value') et 'value'['code'] égal à "Resolved". Quel est le comportement attend… | [voir bloc] | ⬜ |
| 408 | OceaneGet | `getResolutionDate()` | L.542 | Point de décision — key_exists('startDate', 'value'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 409 | OceaneGet | `getCategory()` | L.561 | Point de décision — key_exists('category', 'this'->oceaneData) et is_array('this'->oceaneData['category']). Quel est … | [voir bloc] | ⬜ |
| 410 | OceaneGet | `getLibelleImputation()` | L.577 | Point de décision — key_exists('troubleCause', 'this'->oceaneData) et is_array('this'->oceaneData['troubleCause']). Q… | [voir bloc] | ⬜ |
| 411 | OceaneGet | `isActivationAccpeted()` | L.588 | Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyInterven… | [voir bloc] | ⬜ |
| 412 | OceaneGet | `isActivationAccpeted()` | L.590 | Point de décision — is_array('value') et key_exists('relatedParty', 'value') et is_array('value'['relatedParty']). Qu… | [voir bloc] | ⬜ |
| 413 | OceaneGet | `isActivationAccpeted()` | L.592 | Point de décision — is_array('party') et key_exists('@referredType', 'party') et 'party'['@referredType'] égal à 'Org… | [voir bloc] | ⬜ |
| 414 | OceaneGet | `isActivationAccpeted()` | L.597 | Point de décision — 'isContributor' et key_exists('interventionStatus', 'value') et is_array('value'['interventionSta… | [voir bloc] | ⬜ |
| 415 | OceaneGet | `isActivationAccpeted()` | L.604 | Point de décision — 'activationAccepted'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 416 | OceaneGet | `activationIdsAndRoles()` | L.618 | Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyInterven… | [voir bloc] | ⬜ |
| 417 | OceaneGet | `activationIdsAndRoles()` | L.620 | Point de décision — is_array('value') et key_exists('relatedParty', 'value') et is_array('value'['relatedParty']). Qu… | [voir bloc] | ⬜ |
| 418 | OceaneGet | `activationIdsAndRoles()` | L.622 | Point de décision — is_array('party') et key_exists('@referredType', 'party') et 'party'['@referredType'] égal à 'Org… | [voir bloc] | ⬜ |
| 419 | OceaneGet | `activationIdsAndRoles()` | L.627 | Point de décision — 'isContributor' et key_exists('interventionStatus', 'value') et is_array('value'['interventionSta… | [voir bloc] | ⬜ |
| 420 | OceaneGet | `activationIdsAndRoles()` | L.631 | Point de décision — 'activationAccepted'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 421 | OceaneGet | `getCriticity()` | L.647 | Point de décision — key_exists('criticity', 'this'->oceaneData) et is_array('this'->oceaneData['criticity']). Quel es… | [voir bloc] | ⬜ |
| 422 | OceaneGet | `getTargetRestorationDate()` | L.668 | Point de décision — key_exists('targetRestorationDate', 'this'->oceaneData). Quel est le comportement attendu dans le… | [voir bloc] | ⬜ |
| 423 | OceaneGet | `getPlannedRestorationDate()` | L.684 | Point de décision — key_exists('plannedRestorationDate', 'this'->oceaneData). Quel est le comportement attendu dans l… | [voir bloc] | ⬜ |
| 424 | OceaneGet | `getDateActionInProgress()` | L.695 | Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyInterven… | [voir bloc] | ⬜ |
| 425 | OceaneGet | `getDateActionInProgress()` | L.696 | Point de décision — key_exists('relatedParty', 'this'->oceaneData['partyIntervention'][0]) et is_array('this'->oceane… | [voir bloc] | ⬜ |
| 426 | OceaneGet | `getDateActionInProgress()` | L.698 | Point de décision — is_array('value') et key_exists('actionInProgress', 'value') et key_exists('startDate', 'value'['… | [voir bloc] | ⬜ |
| 427 | OceaneGet | `getActionInProgress()` | L.713 | Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyInterven… | [voir bloc] | ⬜ |
| 428 | OceaneGet | `getActionInProgress()` | L.714 | Point de décision — key_exists('relatedParty', 'this'->oceaneData['partyIntervention'][0]) et is_array('this'->oceane… | [voir bloc] | ⬜ |
| 429 | OceaneGet | `getActionInProgress()` | L.716 | Point de décision — is_array('value') et key_exists('actionInProgress', 'value') et key_exists('description', 'value'… | [voir bloc] | ⬜ |
| 430 | OceaneGet | `getEdsActionInProgress()` | L.728 | Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyInterven… | [voir bloc] | ⬜ |
| 431 | OceaneGet | `getEdsActionInProgress()` | L.729 | Point de décision — key_exists('relatedParty', 'this'->oceaneData['partyIntervention'][0]) et is_array('this'->oceane… | [voir bloc] | ⬜ |
| 432 | OceaneGet | `getEdsActionInProgress()` | L.731 | Point de décision — is_array('value') et key_exists('id', 'value'). Quel est le comportement attendu dans le cas cont… | [voir bloc] | ⬜ |
| 433 | OceaneGet | `getClasitePrio()` | L.756 | Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource… | [voir bloc] | ⬜ |
| 434 | OceaneGet | `getClasitePrio()` | L.757 | Point de décision — key_exists('resourceCharacteristic', 'this'->oceaneData['relatedResource']). Quel est le comporte… | [voir bloc] | ⬜ |
| 435 | OceaneGet | `getClasitePrio()` | L.759 | Point de décision — is_array('value') et key_exists('id', 'value') et 'value'['id'] égal à 'CLASITE'. Quel est le com… | [voir bloc] | ⬜ |
| 436 | OceaneGet | `getClasitePrio()` | L.760 | Point de décision — key_exists('value', 'value'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 437 | OceaneGet | `getRelatedRessource()` | L.771 | Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource… | [voir bloc] | ⬜ |
| 438 | OceaneGet | — | — | Service tiers non documenté — Le composant 'Hbm\Common\Tools\StringTools' est utilisé dans ce périmètre sans équivale… | — | ⬜ |
| 439 | OceaneGet | — | — | Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Rest\ApiOceane' est utilisé dans ce périmètre sans … | — | ⬜ |
| 440 | OceaneGet | — | — | Service tiers non documenté — Le composant 'Oft\Mvc\Application' est utilisé dans ce périmètre sans équivalent identi… | — | ⬜ |
| 441 | OceaneGet | — | — | Service tiers non documenté — Le composant 'Zend\Json\Json' est utilisé dans ce périmètre sans équivalent identifié d… | — | ⬜ |
| 442 | OceaneGet | — | — | Service tiers non documenté — Le composant 'App\Tools\OceaneTools' est utilisé dans ce périmètre sans équivalent iden… | — | ⬜ |
| 443 | OceaneGet | — | — | Service tiers non documenté — Le composant 'ApiOceane' est utilisé dans ce périmètre sans équivalent identifié dans l… | — | ⬜ |
| 444 | OceaneGet | `isChild()` | L.481 | Le code situation 'isParent' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les en… | [voir bloc] | ⬜ |
| 445 | OceaneGet | `isActivationAccpeted()` | L.599 | Le code situation 'Accepted' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les en… | [voir bloc] | ⬜ |
| 446 | OceaneGet | `activationIdsAndRoles()` | L.629 | Le code situation 'Accepted' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les en… | [voir bloc] | ⬜ |
| 447 | OceaneGet | `getClasitePrio()` | L.759 | Le code situation 'CLASITE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enc… | [voir bloc] | ⬜ |
| 448 | Oceane | `findAndGetOceane()` | L.104 | Point de décision — property_exists('troubleTicketResponse'->InstalledResource, 'Parameters') et property_exists('tro… | [voir bloc] | ⬜ |
| 449 | Oceane | `findAndGetOceane()` | L.106 | Point de décision — property_exists('val1', 'id') et 'CLASITE' égal à 'val1'->id. Quel est le comportement attendu da… | [voir bloc] | ⬜ |
| 450 | Oceane | `findAndGetOceane()` | L.125 | Point de décision — property_exists('troubleTicketResponse'->TroubleTicketStatus, 'statusCode'). Quel est le comporte… | [voir bloc] | ⬜ |
| 451 | Oceane | `findAndGetOceane()` | L.128 | Point de décision — property_exists('troubleTicketResponse', 'local_ComplementaryField'). Quel est le comportement at… | [voir bloc] | ⬜ |
| 452 | Oceane | `findAndGetOceane()` | L.130 | Point de décision — is_array('troubleTicketResponse'->local_ComplementaryField). Quel est le comportement attendu dan… | [voir bloc] | ⬜ |
| 453 | Oceane | `findAndGetOceane()` | L.131 | Point de décision — array_key_exists('3', 'troubleTicketResponse'->local_ComplementaryField) et isset('troubleTicketR… | [voir bloc] | ⬜ |
| 454 | Oceane | `findAndGetOceane()` | L.142 | Point de décision — array_key_exists('2', 'troubleTicketResponse'->local_ComplementaryField) et isset('troubleTicketR… | [voir bloc] | ⬜ |
| 455 | Oceane | `findAndGetOceane()` | L.146 | Point de décision — array_key_exists('5', 'troubleTicketResponse'->local_ComplementaryField) et isset('troubleTicketR… | [voir bloc] | ⬜ |
| 456 | Oceane | `findAndGetOceane()` | L.150 | Point de décision — array_key_exists('4', 'troubleTicketResponse'->local_ComplementaryField) et isset('troubleTicketR… | [voir bloc] | ⬜ |
| 457 | Oceane | `findAndGetOceane()` | L.157 | Point de décision — property_exists('troubleTicketResponse', 'troubleTicketPriority'). Quel est le comportement atten… | [voir bloc] | ⬜ |
| 458 | Oceane | `findAndGetOceane()` | L.161 | Point de décision — property_exists('troubleTicketResponse', 'description'). Quel est le comportement attendu dans le… | [voir bloc] | ⬜ |
| 459 | Oceane | `findAndGetOceane()` | L.164 | Point de décision — property_exists('troubleTicketResponse', 'local_ShortLabel'). Quel est le comportement attendu da… | [voir bloc] | ⬜ |
| 460 | Oceane | `findAndGetOceane()` | L.167 | Point de décision — property_exists('troubleTicketResponse', 'TroubleCause'). Quel est le comportement attendu dans l… | [voir bloc] | ⬜ |
| 461 | Oceane | `findAndGetOceane()` | L.168 | Point de décision — property_exists('troubleTicketResponse'->TroubleCause, 'local_internalcomplement'). Quel est le c… | [voir bloc] | ⬜ |
| 462 | Oceane | `findAndGetOceane()` | L.171 | Point de décision — property_exists('troubleTicketResponse'->TroubleCause, 'troubleCauseCodeCategory'). Quel est le c… | [voir bloc] | ⬜ |
| 463 | Oceane | `findAndGetOceane()` | L.174 | Point de décision — property_exists('troubleTicketResponse'->TroubleCause, 'troubleCauseLabel'). Quel est le comporte… | [voir bloc] | ⬜ |
| 464 | Oceane | `findAndGetOceane()` | L.177 | Point de décision — property_exists('troubleTicketResponse'->TroubleCause, 'troubleCauseDescription'). Quel est le co… | [voir bloc] | ⬜ |
| 465 | Oceane | `findAndGetOceane()` | L.180 | Point de décision — property_exists('troubleTicketResponse'->TroubleCause, 'troubleCauseCodeCategory'). Quel est le c… | [voir bloc] | ⬜ |
| 466 | Oceane | `findAndGetOceane()` | L.185 | Point de décision — property_exists('troubleTicketResponse', 'troubleType'). Quel est le comportement attendu dans le… | [voir bloc] | ⬜ |
| 467 | Oceane | `findAndGetOceane()` | L.192 | Point de décision — 'posteAssocie' égal à ''. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 468 | Oceane | `findAndGetOceane()` | L.196 | Point de décision — !is_null('connectedEds') et 'value'->partyRoleType égal à "TroubleResolutionContributor" et prope… | [voir bloc] | ⬜ |
| 469 | Oceane | `findAndGetOceane()` | L.199 | Point de décision — key_exists(2, 'value'->Local_PartyIntervention->interventionStatus). Quel est le comportement att… | [voir bloc] | ⬜ |
| 470 | Oceane | `findAndGetOceane()` | L.215 | Point de décision — !is_null('connectedEds') et 'value'->partyRoleType égal à "TroubleResolutionContributor" et prope… | [voir bloc] | ⬜ |
| 471 | Oceane | `findAndGetOceane()` | L.216 | Point de décision — 'value'->Local_PartyIntervention->interventionStatus->status égal à 'Requested'. Quel est le comp… | [voir bloc] | ⬜ |
| 472 | Oceane | `findAndGetOceane()` | L.240 | Point de décision — property_exists('troubleTicketResponse', 'PartyRole'). Quel est le comportement attendu dans le c… | [voir bloc] | ⬜ |
| 473 | Oceane | `findAndGetOceane()` | L.244 | Point de décision — !'checkInc'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 474 | Oceane | `findAndGetOceane()` | L.245 | Point de décision — key_exists('i', 'troubleTicketResponse'->PartyRole) et property_exists('troubleTicketResponse'->P… | [voir bloc] | ⬜ |
| 475 | Oceane | `findAndGetOceane()` | L.247 | Point de décision — property_exists('troubleTicketResponse'->PartyRole['i']->PartyRoleSet, 'local_groupactioninprogre… | [voir bloc] | ⬜ |
| 476 | Oceane | `findAndGetOceane()` | L.253 | Point de décision — property_exists('troubleTicketResponse'->PartyRole['i']->PartyRoleSet, 'local_groupactioninprogre… | [voir bloc] | ⬜ |
| 477 | Oceane | `findAndGetOceane()` | L.258 | Point de décision — 'checkIncDate' et 'checkIncAct'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 478 | Oceane | `findAndGetOceane()` | L.266 | Point de décision — property_exists('troubleTicketResponse', 'local_onbhfollowup'). Quel est le comportement attendu … | [voir bloc] | ⬜ |
| 479 | Oceane | `findAndGetOceane()` | L.270 | Point de décision — property_exists('troubleTicketResponse', 'troubleTicketCategory'). Quel est le comportement atten… | [voir bloc] | ⬜ |
| 480 | Oceane | `updateOceane()` | L.382 | Point de décision — array_key_exists('ticket_id', 'data') et isset('data'['ticket_id']). Quel est le comportement att… | [voir bloc] | ⬜ |
| 481 | Oceane | `updateOceane()` | L.386 | Point de décision — array_key_exists('astroid', 'data') et isset('data'['astroid']). Quel est le comportement attendu… | [voir bloc] | ⬜ |
| 482 | Oceane | `updateOceane()` | L.390 | Point de décision — array_key_exists('party_role_party_ID', 'data') et isset('data'['party_role_party_ID']). Quel est… | [voir bloc] | ⬜ |
| 483 | Oceane | `updateOceane()` | L.394 | Point de décision — array_key_exists('postes_associe', 'data') et isset('data'['postes_associe']). Quel est le compor… | [voir bloc] | ⬜ |
| 484 | Oceane | `updateOceane()` | L.398 | Point de décision — array_key_exists('niv_urgence', 'data') et isset('data'['niv_urgence']). Quel est le comportement… | [voir bloc] | ⬜ |
| 485 | Oceane | `updateOceane()` | L.402 | Point de décision — array_key_exists('action_eds', 'data') et isset('data'['action_eds']). Quel est le comportement a… | [voir bloc] | ⬜ |
| 486 | Oceane | `updateOceane()` | L.406 | Point de décision — array_key_exists('commentaire_eds', 'data') et isset('data'['commentaire_eds']). Quel est le comp… | [voir bloc] | ⬜ |
| 487 | Oceane | `updateOceane()` | L.410 | Point de décision — array_key_exists('eds_pilote', 'data') et isset('data'['eds_pilote']). Quel est le comportement a… | [voir bloc] | ⬜ |
| 488 | Oceane | `updateOceane()` | L.420 | Point de décision — array_key_exists('local_commentaire', 'data') et isset('data'['local_commentaire']). Quel est le … | [voir bloc] | ⬜ |
| 489 | Oceane | `updateOceane()` | L.423 | Point de décision — array_key_exists('nb_plaintes', 'data') et isset('data'['nb_plaintes']). Quel est le comportement… | [voir bloc] | ⬜ |
| 490 | Oceane | `updateOceane()` | L.433 | Point de décision — array_key_exists('description', 'data') et isset('data'['description']). Quel est le comportement… | [voir bloc] | ⬜ |
| 491 | Oceane | `updateOceane()` | L.436 | Point de décision — array_key_exists('trouble_type', 'data') et isset('data'['trouble_type']). Quel est le comporteme… | [voir bloc] | ⬜ |
| 492 | Oceane | `updateOceane()` | L.439 | Point de décision — array_key_exists('trouble_severity', 'data') et isset('data'['trouble_severity']). Quel est le co… | [voir bloc] | ⬜ |
| 493 | Oceane | `updateOceane()` | L.442 | Point de décision — array_key_exists('party_set_ID', 'data') et isset('data'['party_set_ID']). Quel est le comporteme… | [voir bloc] | ⬜ |
| 494 | Oceane | `updateOceane()` | L.446 | Point de décision — array_key_exists('requested_date', 'data') et isset('data'['requested_date']). Quel est le compor… | [voir bloc] | ⬜ |
| 495 | Oceane | `updateOceane()` | L.483 | Point de décision — array_key_exists('description', 'data') et isset('data'['description']). Quel est le comportement… | [voir bloc] | ⬜ |
| 496 | Oceane | `updateOceane()` | L.486 | Point de décision — array_key_exists('trouble_type', 'data') et isset('data'['trouble_type']). Quel est le comporteme… | [voir bloc] | ⬜ |
| 497 | Oceane | `updateOceane()` | L.489 | Point de décision — array_key_exists('trouble_severity', 'data') et isset('data'['trouble_severity']). Quel est le co… | [voir bloc] | ⬜ |
| 498 | Oceane | `updateOceane()` | L.492 | Point de décision — array_key_exists('party_set_ID', 'data') et isset('data'['party_set_ID']). Quel est le comporteme… | [voir bloc] | ⬜ |
| 499 | Oceane | `updateOceaneConfirmer()` | L.517 | Point de décision — !'generique'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 500 | Oceane | `updateOceaneConfirmer()` | L.535 | Point de décision — 'actifDri'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 501 | Oceane | `updateOceaneConfirmerTrans()` | L.622 | Point de décision — 'data'['donnee_complementaire'] différent de ''. Quel est le comportement attendu dans le cas con… | [voir bloc] | ⬜ |
| 502 | Oceane | `updateOceaneConfirmerTrans()` | L.625 | Point de décision — ('actifDri' égal à '1') ou (key_exists('api', 'this'->app->config) et 'this'->app->config['api'])… | [voir bloc] | ⬜ |
| 503 | Oceane | `updateOceaneConfirmerTrans()` | L.646 | Point de décision — !key_exists('api', 'data'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 504 | Oceane | `updateOceaneConfirmerTrans()` | L.630 | Valeur de référence non documentée — La décision « 'confirmTowStep' égal à 'oui' » repose sur la valeur 'oui'. D'où v… | [voir bloc] | ⬜ |
| 505 | Oceane | — | — | Service tiers non documenté — Le composant 'App\Tools\OceaneTools' est utilisé dans ce périmètre sans équivalent iden… | — | ⬜ |
| 506 | Oceane | — | — | Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Rest\ApiOceane' est utilisé dans ce périmètre sans … | — | ⬜ |
| 507 | Oceane | — | — | Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Soap\OceaneUpd' est utilisé dans ce périmètre sans … | — | ⬜ |
| 508 | Oceane | — | — | Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Soap\OceaneFg' est utilisé dans ce périmètre sans é… | — | ⬜ |
| 509 | Oceane | — | — | Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Rest\Oceane' est utilisé dans ce périmètre sans équ… | — | ⬜ |
| 510 | Oceane | — | — | Service tiers non documenté — Le composant 'Hbm\Common\Tools\StringTools' est utilisé dans ce périmètre sans équivale… | — | ⬜ |
| 511 | Oceane | — | — | Service tiers non documenté — Le composant '\Oft\Mvc\Application' est utilisé dans ce périmètre sans équivalent ident… | — | ⬜ |
| 512 | Oceane | — | — | Service tiers non documenté — Le composant 'App\Tools\OceaneAssistant' est utilisé dans ce périmètre sans équivalent … | — | ⬜ |
| 513 | Oceane | — | — | Service tiers non documenté — Le composant 'OceaneAssistant' est utilisé dans ce périmètre sans équivalent identifié … | — | ⬜ |
| 514 | Oceane | — | — | Service tiers non documenté — Le composant 'OceaneFg' est utilisé dans ce périmètre sans équivalent identifié dans la… | — | ⬜ |
| 515 | Oceane | — | — | Service tiers non documenté — Le composant 'Oceane' est utilisé dans ce périmètre sans équivalent identifié dans la c… | — | ⬜ |
| 516 | Oceane | — | — | Service tiers non documenté — Le composant 'ApiOceane' est utilisé dans ce périmètre sans équivalent identifié dans l… | — | ⬜ |
| 517 | Oceane | `updateOceaneConfirmer()` | L.528 | Le code situation 'TYPE2' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les encha… | [voir bloc] | ⬜ |
| 518 | Oceane | `updateOceaneConfirmerTrans()` | L.625 | Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînem… | [voir bloc] | ⬜ |
| 519 | Oceane | `updateOceaneConfirmerTrans()` | L.630 | Le code situation 'oui' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîn… | [voir bloc] | ⬜ |
| 520 | Oceane | `createComment()` | L.732 | Le code situation '4' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînem… | [voir bloc] | ⬜ |
| 521 | Validation | — | — | Service tiers non documenté — Le composant 'Zend\Validator\NotEmpty' est utilisé dans ce périmètre sans équivalent id… | — | ⬜ |
| 522 | Validation | — | — | Service tiers non documenté — Le composant 'Zend\Validator\Digits' est utilisé dans ce périmètre sans équivalent iden… | — | ⬜ |
| 523 | Validation | — | — | Service tiers non documenté — Le composant 'Zend\Validator\Date' est utilisé dans ce périmètre sans équivalent identi… | — | ⬜ |
| 524 | Validation | — | — | Service tiers non documenté — Le composant 'Zend\Validator\Regex' est utilisé dans ce périmètre sans équivalent ident… | — | ⬜ |
| 525 | Validation | — | — | Service tiers non documenté — Le composant 'Zend\I18n\Validator\IsInt' est utilisé dans ce périmètre sans équivalent … | — | ⬜ |
| 526 | Validation | — | — | Service tiers non documenté — Le composant 'NotEmpty' est utilisé dans ce périmètre sans équivalent identifié dans la… | — | ⬜ |
| 527 | Validation | — | — | Service tiers non documenté — Le composant 'Digits' est utilisé dans ce périmètre sans équivalent identifié dans la c… | — | ⬜ |
| 528 | Validation | — | — | Service tiers non documenté — Le composant 'Date' est utilisé dans ce périmètre sans équivalent identifié dans la cib… | — | ⬜ |
| 529 | Validation | — | — | Service tiers non documenté — Le composant 'Regex' est utilisé dans ce périmètre sans équivalent identifié dans la ci… | — | ⬜ |
| 530 | Validation | — | — | Service tiers non documenté — Le composant 'IsInt' est utilisé dans ce périmètre sans équivalent identifié dans la ci… | — | ⬜ |
| 531 | VariableBase | — | L.27 | Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 532 | VariableBase | `getVariableAdminValue()` | L.39 | Point de décision — property_exists('this'->findAndGet['installed_resource']->Parameters, 'Parameter'). Quel est le c… | [voir bloc] | ⬜ |
| 533 | VariableBase | `getVariableAdminValue()` | L.42 | Point de décision — !is_null('res'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 534 | VariableBase | `getVariableAdminValue()` | L.48 | Point de décision — property_exists('this'->findAndGet['installed_resource']->Attributes, 'Attribute'). Quel est le c… | [voir bloc] | ⬜ |
| 535 | VariableBase | `getVariableAdminValue()` | L.51 | Point de décision — !is_null('res'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 536 | VariableBase | `getVariableAdminValue()` | L.59 | Point de décision — !is_null('res'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 537 | VariableBase | — | L.79 | Point de décision — 'this'->id1. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 538 | VariableBase | — | — | Service tiers non documenté — Le composant 'App\Tools\OceaneTools' est utilisé dans ce périmètre sans équivalent iden… | — | ⬜ |
| 539 | VariableBase | — | — | Service tiers non documenté — Le composant 'Oft\Mvc\Application' est utilisé dans ce périmètre sans équivalent identi… | — | ⬜ |
| 540 | Variable | `replaceTagsChaine()` | L.123 | Point de décision — 'arg' égal à 'Temperature' ou 'arg' égal à 'Etat_batterie' ou 'arg' égal à 'Tension_batterie' ou … | [voir bloc] | ⬜ |
| 541 | Variable | `replaceTagsChaine()` | L.131 | Point de décision — property_exists('parameters', 'Parameter'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 542 | Variable | `replaceTagsChaine()` | L.133 | Point de décision — property_exists('val1', 'id') et 'val1'->id égal à 'LIBSITE'. Quel est le comportement attendu da… | [voir bloc] | ⬜ |
| 543 | Variable | `replaceTagsChaine()` | L.137 | Point de décision — 'libSite' différent de "". Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 544 | Variable | `replaceTagsChaine()` | L.142 | Point de décision — 'arg' égal à 'DSLAM_PRODUIT_DSLAM' ou 'arg' égal à 'DSLAM_PRODUIT_CHASSIS' ou 'arg' égal à 'DSLAM… | [voir bloc] | ⬜ |
| 545 | Variable | `replaceTagsChaine()` | L.143 | Point de décision — is_null('this'->variableRepository). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 546 | Variable | `replaceTagsChaine()` | L.147 | Point de décision — !'replaceValue'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 547 | Variable | `replaceTagsChaine()` | L.149 | Point de décision — 'replaceValue' différent de '' et !is_null('replaceValue') et !is_array('replaceValue'). Quel est… | [voir bloc] | ⬜ |
| 548 | Variable | `replaceTagsChaine()` | L.153 | Point de décision — OceaneTools::isValidVariable('replaceValue') et !is_array('replaceValue'). Quel est le comporteme… | [voir bloc] | ⬜ |
| 549 | Variable | `replaceTagsChaine()` | L.165 | Point de décision — is_null('this'->transitoolService). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 550 | Variable | `replaceTagsChaine()` | L.171 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 551 | Variable | `replaceTagsChaine()` | L.178 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 552 | Variable | `replaceTagsChaine()` | L.185 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 553 | Variable | `replaceTagsChaine()` | L.195 | Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le compo… | [voir bloc] | ⬜ |
| 554 | Variable | `replaceTagsChaine()` | L.203 | Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le compo… | [voir bloc] | ⬜ |
| 555 | Variable | `replaceTagsChaine()` | L.210 | Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le compo… | [voir bloc] | ⬜ |
| 556 | Variable | `replaceTagsChaine()` | L.217 | Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le compo… | [voir bloc] | ⬜ |
| 557 | Variable | `replaceTagsChaine()` | L.226 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 558 | Variable | `replaceTagsChaine()` | L.234 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 559 | Variable | `replaceTagsChaine()` | L.242 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 560 | Variable | `replaceTagsChaine()` | L.251 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 561 | Variable | `replaceTagsChaine()` | L.259 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 562 | Variable | `replaceTagsChaine()` | L.270 | Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 563 | Variable | `replaceTagsChaine()` | L.276 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 564 | Variable | `replaceTagsChaine()` | L.284 | Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 565 | Variable | `replaceTagsChaine()` | L.287 | Point de décision — !isset('this'->findAndGet['message']) et !is_null('this'->findAndGet['installed_resource']) et pr… | [voir bloc] | ⬜ |
| 566 | Variable | `replaceTagsChaine()` | L.291 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 567 | Variable | `replaceTagsChaine()` | L.297 | Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 568 | Variable | `replaceTagsChaine()` | L.301 | Point de décision — !isset('this'->findAndGet['message']) et !is_null('this'->findAndGet['rd_plus']). Quel est le com… | [voir bloc] | ⬜ |
| 569 | Variable | `replaceTagsChaine()` | L.304 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 570 | Variable | `replaceTagsChaine()` | L.310 | Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 571 | Variable | `replaceTagsChaine()` | L.314 | Point de décision — !isset('this'->findAndGet['message']) et !is_null('this'->findAndGet['description']). Quel est le… | [voir bloc] | ⬜ |
| 572 | Variable | `replaceTagsChaine()` | L.317 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 573 | Variable | `replaceTagsChaine()` | L.323 | Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 574 | Variable | `replaceTagsChaine()` | L.326 | Point de décision — !isset('this'->findAndGet['message']) et !is_null('this'->findAndGet['code_detecteur']). Quel est… | [voir bloc] | ⬜ |
| 575 | Variable | `replaceTagsChaine()` | L.333 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 576 | Variable | `replaceTagsChaine()` | L.353 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 577 | Variable | `replaceTagsChaine()` | L.375 | Point de décision — OceaneTools::isValidVariable('replaceValue') et gettype('replaceValue') différent de 'boolean'. Q… | [voir bloc] | ⬜ |
| 578 | Variable | `replaceTagsChaine()` | L.402 | Point de décision — 'this'->typeRessource égal à 'TRONCABLE'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 579 | Variable | `replaceTagsChaine()` | L.405 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 580 | Variable | `replaceTagsChaine()` | L.415 | Point de décision — !is_null('resultColumn') et 'resultColumn' différent de ''. Quel est le comportement attendu dans… | [voir bloc] | ⬜ |
| 581 | Variable | `replaceTagsChaine()` | L.418 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 582 | Variable | `replaceTagsChaine()` | L.424 | Point de décision — 'this'->globalApiRepository->isVariableAdminExist('arg', 'type'). Quel est le comportement attend… | [voir bloc] | ⬜ |
| 583 | Variable | `replaceTagsChaine()` | L.426 | Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 584 | Variable | `replaceTagsChaine()` | L.429 | Point de décision — !isset('this'->findAndGet['message']). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 585 | Variable | `replaceTagsChaine()` | L.440 | Point de décision — 'resourceSpecification' différent de "". Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 586 | Variable | `replaceTagsChaine()` | L.446 | Point de décision — count('tabIdentifiants') > 0. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 587 | Variable | `replaceTagsChaine()` | L.448 | Point de décision — isset('replaceValue'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 588 | Variable | `selectExtension()` | L.489 | Point de décision — 'ext1_status' égal à 0. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 589 | Variable | `selectExtension()` | L.493 | Point de décision — 'ext1_status' égal à 1 et 'ext2_status' égal à 0. Quel est le comportement attendu dans le cas co… | [voir bloc] | ⬜ |
| 590 | Variable | `selectExtension()` | L.497 | Point de décision — 'ext1_status' égal à -1. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 591 | Variable | `selectExtension()` | L.501 | Point de décision — 'ext2_status' égal à -1. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 592 | Variable | `getIntervenant()` | L.527 | Point de décision — 'intervenantMatriceRefsite' différent de "###'variableAdministree'###". Quel est le comportement … | [voir bloc] | ⬜ |
| 593 | Variable | `getIntervenant()` | L.594 | Point de décision — key_exists('ID', 'resultQuery'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 594 | Variable | `replaceTagsChainePariV2()` | L.658 | Point de décision — is_null('this'->dataPariv2). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 595 | Variable | — | L.756 | Point de décision — isset('mapping'['variable']). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 596 | Variable | `replaceTagsChaine()` | L.195 | Valeur de référence non documentée — La décision « key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat']… | [voir bloc] | ⬜ |
| 597 | Variable | `replaceTagsChaine()` | L.203 | Valeur de référence non documentée — La décision « key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat']… | [voir bloc] | ⬜ |
| 598 | Variable | `replaceTagsChaine()` | L.210 | Valeur de référence non documentée — La décision « key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat']… | [voir bloc] | ⬜ |
| 599 | Variable | `replaceTagsChaine()` | L.217 | Valeur de référence non documentée — La décision « key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat']… | [voir bloc] | ⬜ |
| 600 | Variable | `replaceTagsChaine()` | L.375 | Valeur de référence non documentée — La décision « OceaneTools::isValidVariable('replaceValue') et gettype('replaceVa… | [voir bloc] | ⬜ |
| 601 | Variable | `getIntervenant()` | L.592 | Valeur de référence non documentée — La décision « gettype('resultQuery') différent de 'boolean' et 'resultQuery' dif… | [voir bloc] | ⬜ |
| 602 | Variable | `replaceTagsChainePariV2()` | L.670 | Valeur de référence non documentée — La décision « OceaneTools::isValidVariable('replaceValue') et gettype('replaceVa… | [voir bloc] | ⬜ |
| 603 | Variable | — | — | Service tiers non documenté — Le composant 'App\Repository\AstroRepository' est utilisé dans ce périmètre sans équiva… | — | ⬜ |
| 604 | Variable | — | — | Service tiers non documenté — Le composant 'App\Repository\RefsitesRepository' est utilisé dans ce périmètre sans équ… | — | ⬜ |
| 605 | Variable | — | — | Service tiers non documenté — Le composant 'App\Repository\VariableRepository' est utilisé dans ce périmètre sans équ… | — | ⬜ |
| 606 | Variable | — | — | Service tiers non documenté — Le composant 'App\Repository\GlobalApiRepository' est utilisé dans ce périmètre sans éq… | — | ⬜ |
| 607 | Variable | — | — | Service tiers non documenté — Le composant 'App\Tools\OceaneTools' est utilisé dans ce périmètre sans équivalent iden… | — | ⬜ |
| 608 | Variable | — | — | Service tiers non documenté — Le composant 'Hbm\Common\Tools\StringTools' est utilisé dans ce périmètre sans équivale… | — | ⬜ |
| 609 | Variable | — | — | Service tiers non documenté — Le composant 'Hbm\Globalapi\Factory\Pariv2Factory' est utilisé dans ce périmètre sans é… | — | ⬜ |
| 610 | Variable | — | — | Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Rest\ApiOceane' est utilisé dans ce périmètre sans … | — | ⬜ |
| 611 | Variable | — | — | Service tiers non documenté — Le composant 'Oft\Mvc\Application' est utilisé dans ce périmètre sans équivalent identi… | — | ⬜ |
| 612 | Variable | — | — | Service tiers non documenté — Le composant 'Zend\Json\Json' est utilisé dans ce périmètre sans équivalent identifié d… | — | ⬜ |
| 613 | Variable | — | — | Service tiers non documenté — Le composant 'ApiOceane' est utilisé dans ce périmètre sans équivalent identifié dans l… | — | ⬜ |
| 614 | Variable | — | — | Service tiers non documenté — Le composant 'Pariv2Factory' est utilisé dans ce périmètre sans équivalent identifié da… | — | ⬜ |
| 615 | Variable | `replaceTagsChaine()` | L.133 | Le code situation 'LIBSITE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enc… | [voir bloc] | ⬜ |
| 616 | Variable | `replaceTagsChaine()` | L.195 | Le code situation 'ok' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîne… | [voir bloc] | ⬜ |
| 617 | Variable | `replaceTagsChaine()` | L.416 | Le code situation 'ORANGE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les ench… | [voir bloc] | ⬜ |
| 618 | Variable | `getIntervenant()` | L.563 | Le code situation 'MIE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîn… | [voir bloc] | ⬜ |
| 619 | Variable | `getIntervenant()` | L.577 | Le code situation 'FH' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaîne… | [voir bloc] | ⬜ |

*353 gap(s) — chaque case ⬜ représente une décision à prendre avant migration.*

---

## Contexte Code — Copier dans Copilot

---

**Gap #1 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : abandonnerAuto() — ligne 561
Contexte   :
```php
            $astroSession = $this->app->get('Session')->get('astroOft' . $ticket['TICKETOCEANEID']);
            $connectedGroup = key_exists('connectedgroup',$astroSession) ? $astroSession['connectedgroup'] : '';
            $loginId = $this->astroRepository->getCompteMachine($connectedGroup);

            $result = $this->abandonnerProcessAuto($ticket['ID_JEU_PARAM'], $ticket['TICKETOCEANEID'], $ticket['ID_TICKET_ASTRO'], $ticket['TYPE_RESSOURCE'], '', $loginId);
            if ($result == 1) {
                $this->abandonBatchRepository->updateTicketEtat($ticket['TICKETOCEANEID']);
```

Question métier : Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (transitions : ASSEMBLEE→CABLE, EQUIPEMENT→CABLE, reclassification Océane)

---

**Gap #2 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : preconisationImpactPrioriteAdsl() — ligne 618
Contexte   :
```php
            $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
            $astroId = $astroSession['astroid'];
            $type = $astroSession['type'];
            $idBandeau = $this->astroRepository->getBandeauId($astroSession['bandeau']);

            $fonctions = $droitTools->getDroitFonction($idBandeau);
            $droitEds = $droitTools->droitEds($ticketId, $astroSession['connectedgroup'], $astroSession['pilotgroup']);
```

Question métier : Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (transitions : ASSEMBLEE→CABLE, EQUIPEMENT→CABLE, reclassification Océane)

---

**Gap #3 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : abandonnerProcessAuto() — ligne 210
Contexte   :
```php
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $this->hbmLogin",
            "X-HTTP-Method-Override: PATCH"
        );
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #4 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : abandonnerProcess() — ligne 293
Contexte   :
```php
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $this->hbmLogin",
            "X-HTTP-Method-Override: PATCH"
        );
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #5 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : getCommentaireImpactClient() — ligne 388
Contexte   :
```php
        $this->getOceane->getOceaneData($dataAstro['ID_TICKET_ASTRO'],  $this->loginId);
        $detectionDate = $this->getOceane->getDetectionDate();
        $oceaneAssistant = new OceaneAssistant($this->app);
        if ($dataAdelia) {
            $dataAdelia['SEUIL_GRAVE'] = intval($dataAdelia['SEUIL_GRAVE']);
            $dataAdelia['SEUIL_MAJEUR'] = intval($dataAdelia['SEUIL_MAJEUR']);
        }
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #6 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : confirmerBase() — ligne 507
Contexte   :
```php
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');
        $headerConfig = array(
            "X-Client-User-Id: $this->loginId",
            "X-HTTP-Method-Override: PATCH",
        );

```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #7 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : preconisationImpactPrioriteAdsl() — ligne 652
Contexte   :
```php
            $arrMatricePrio = $oceaneAssistant->getMatricePrioGenerique($idJeuParam, $totalClients, 'TYPE1', $isClientEntreprise, false, $isNetVpnFinal);


            $idValeurImpactPreconise = $this->astroIhmSqlRepository->getIdValeurConfirmerIncidentByChampAndLibelle($idJeuParam, 'NATURE_IMPACT_CLIENT', $informerClient['libelle_impact_client']);

            $presenceGtr = $this->app->get('Airele')->getImpactByAireleDSLAM($astroSession['id1']);
            $gtr = in_array('GTRS1', $presenceGtr) || in_array('GTRS2', $presenceGtr);
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #8 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : getSeuilsAdelia() — ligne 948
Contexte   :
```php
        $this->getOceane->getOceaneData($data['TICKETOCEANEID'],  $this->loginId);

        $dataAdeliaArraySimulate = json_decode($resultSimulate);
        $dataAdeliaSavedFirst = $this->adeliaService->saveAdeliaDataFirst( true,$dataAdeliaArraySimulate, $data['ID_TICKET_ASTRO']);

        if (!is_null($result)) {
            $dataAdeliaArray = json_decode($result);
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #9 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAGP3() — ligne 458
Contexte   :
```php
            // 'Alarme'=>$_SESSION['astro'.$data['agp_id_astro']]['ressource'] )
        ));
        $agpCommentaire = $commentaire->getCommentaire();
        return array(
            'agp_entite_activee' => $agpEntiteActivee,
            'agp_mode_activation' => $agpModeActivation,
            'agp_activation' => $agpActivation,
```

Question métier : L'identité de l'agent connecté est lue directement depuis la session. L'habilitation est-elle vérifiée par un service centralisé ou uniquement à cet endroit ?

---

**Gap #10 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 963
Contexte   :
```php
                        // 'Alarme'=>$_SESSION['astro'.$data['agp_id_astro']]['ressource'] )
                    ), $idJeuParam);
                    $agpCCResult = $comm->getCommentaire();
                    // Ne remplacer le commentaire que si $idRscDslam est non vide
                    if ($idRscDslam !== null && $idRscDslam !== '') {
                        $commentaire = $agpCCResult;
                    }
```

Question métier : L'identité de l'agent connecté est lue directement depuis la session. L'habilitation est-elle vérifiée par un service centralisé ou uniquement à cet endroit ?

---

**Gap #11 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1368
Contexte   :
```php
                    $token = base64_encode(md5(date('yyyymmdd') . 'link_astro_charter'));
                    $chaine = str_replace('###' . $arg . '###', $token, $chaine);
                    break;

                case 'DATE':
                    $replaceValue = rtrim($this->getOceane->getCreationDate(), 'Z');
                    if (OceaneTools::isValidVariable($replaceValue)) {
```

Question métier : Cette méthode de protection du secret d'authentification est ancienne et non conforme aux standards actuels. S'agit-il d'une contrainte documentée ou cette protection est-elle prévue pour évoluer lors de la migration ?

---

**Gap #12 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : initAgp() — ligne 171
Contexte   :
```php
        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $idRessource = $astroSession['id_ressource'];
        $rsc = $this->astroRepository->getRessource($idRessource);
        $idRscDslam = $rsc['ID_RESSOURCE_DSLAM'];

        if ($this->edrRepository->testDataInfo($astroId) == 0) {
            $msg = $this->interventionHelper->getIndispoMessage();
```

Question métier : Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (transitions : ASSEMBLEE→CABLE, EQUIPEMENT→CABLE, reclassification Océane)

---

**Gap #13 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1() — ligne 227
Contexte   :
```php
        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);

        $typeRessource = $astroSession['type_ressource'];

        $droitAstro = new DroitAstroTools($this->app);
        $droitEds = $droitAstro->droitEds($ticketId, $astroSession['connectedgroup'], $astroSession['pilotgroup']);

```

Question métier : Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (transitions : ASSEMBLEE→CABLE, EQUIPEMENT→CABLE, reclassification Océane)

---

**Gap #14 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAGP3() — ligne 413
Contexte   :
```php
        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);

        $agpEntiteActivee = $data['entite'];
        $agpModeActivation = (strpos($data['activation'], 'EDS ') !== false ? 'EDS' : $data['activation']);
        $agpActivation = $data['activation'];
        $agpEds = str_replace(array(
            'CADI',
```

Question métier : Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (transitions : ASSEMBLEE→CABLE, EQUIPEMENT→CABLE, reclassification Océane)

---

**Gap #15 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1Generique() — ligne 528
Contexte   :
```php
        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $typeRessource = $astroSession['type_ressource'];

        if ($typeRessource == 'DSLAM') {
            $idRscMaster = '';
            $dslam = '';
            $helper = new Edr();
```

Question métier : Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (transitions : ASSEMBLEE→CABLE, EQUIPEMENT→CABLE, reclassification Océane)

---

**Gap #16 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayPiloterGenerique() — ligne 732
Contexte   :
```php
            $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        }
        $oceaneAssistant = new OceaneAssistant($this->app);
        $agpEntiteActivee = StringTools::convertEncoding($data['entite'], self::ISO_8859_15, 'UTF-8');
        $modeActivation = explode(" ", $data['activation']);
        $agpModeActivation = (strpos($data['activation'], 'EDS ') !== false) ? 'EDS' : $modeActivation[0];
        $agpActivation = $data['activation'];
```

Question métier : Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (transitions : ASSEMBLEE→CABLE, EQUIPEMENT→CABLE, reclassification Océane)

---

**Gap #17 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : getCommentaireAgp2Generique() — ligne 811
Contexte   :
```php
        $astroSession = $this->app->get('Session')->get('astroOft' . $data['ticketId']);
        $agpIdAstro = key_exists('agp_id_astro', $data) ? $data['agp_id_astro'] : null;
        $agpIdRsc = key_exists('agp_id_rsc', $data) ? $data['agp_id_rsc'] : null;
        $agpIdAction = key_exists('agp_id_action', $data) ? $data['agp_id_action'] : null;
        $agpChassis = key_exists('agp_chassis', $data) ? $data['agp_chassis'] : null;
        $agpCarte = key_exists('agp_carte', $data) ? $data['agp_carte'] : null;
        $agpPeriph = key_exists('agp_periph', $data) ? $data['agp_periph'] : null;
```

Question métier : Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (transitions : ASSEMBLEE→CABLE, EQUIPEMENT→CABLE, reclassification Océane)

---

**Gap #18 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 841
Contexte   :
```php
            $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
            $data['connected_group'] = $astroSession['connectedgroup'];
        }
        $oceaneAssistant = new OceaneAssistant($this->app);
        $agpEntiteActivee = StringTools::convertEncoding($data['entite'], self::ISO_8859_15, 'UTF-8');
        $modeActivation = explode(" ", $data['activation']);
        $agpModeActivation = (strpos($data['activation'], 'EDS ') !== false) ? 'EDS' : $modeActivation[0];
```

Question métier : Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (transitions : ASSEMBLEE→CABLE, EQUIPEMENT→CABLE, reclassification Océane)

---

**Gap #19 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayCreationTocTrans() — ligne 1057
Contexte   :
```php
        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $sessionId = $this->app->get('Session')->getUtilisateurId();
        $astroId = $astroSession['astroid'];
        // Chargement des données Océane du ticket

        $this->getOceane->getOceaneData($ticketId, $this->loginId);
        $oceaneAssistant = new OceaneAssistant($this->app);
```

Question métier : Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (transitions : ASSEMBLEE→CABLE, EQUIPEMENT→CABLE, reclassification Océane)

---

**Gap #20 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayCreationTocAdsl() — ligne 1130
Contexte   :
```php
        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $astroId = $astroSession['astroid'];

        $creaTicketAdslForm = new CreaTicketAdslForm(null, array(
            'app' => $this->app,
            'ticket_id' => $ticketId
        ));
```

Question métier : Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (transitions : ASSEMBLEE→CABLE, EQUIPEMENT→CABLE, reclassification Océane)

---

**Gap #21 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayPiloterGenerique() — ligne 762
Contexte   :
```php
        $idUrgenceOceane = $this->agpGeneriqueRepository->getIdentifiantUrgenceByValeurParametres($idJeuParam, 'NIVEAU_URGENCE', $oceaneData['herite_oceane_niveau_urgence']);
        if (key_exists('herite_oceane_date_action_en_cours', $oceaneData)) {
            $agpDtEnCoursOceane = $oceaneData['herite_oceane_date_action_en_cours'];
        } else {
            $agpDtEnCoursOceane = '';
        }
        $agpIdAction = key_exists('agp_action_generique', $data) ? $data['agp_action_generique'] : null;
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #22 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : getCommentaireAgp2Generique() — ligne 831
Contexte   :
```php
        $variables = OceaneTools::getContents($comm->getCommentaire(), '###', '###');
        $commentaire = $this->app->get('Variable')->replaceTagsChaine($comm->getCommentaire(), $variables, $astroSession['type'], $data['ticketId']);
        $comm->setCommentaire($commentaire);
        return $comm;

    }
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #23 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 868
Contexte   :
```php
        $isValeurNiveauUrgenceHeriteeOceane = $this->agpGeneriqueRepository->getValeurHeriteeOceaneByJeuParam($idJeuParam, 'NIVEAU_URGENCE');

        // Niveau d'urgence suivant l'entité et la Priorité Océane
        $paramsUrgence = $this->agpGeneriqueRepository->getParamsUrgence($data['id_entite'], $data['hno'], $idJeuParam);
        $agpUrgence = $this->agpGeneriqueRepository->getValeurParametres($idJeuParam, 'NIVEAU_URGENCE');
        $agpActionEds = $this->agpGeneriqueRepository->getValeurParametres($idJeuParam, 'ACTION_EN_COURS_EDS');
        $idActionEnCoursEds = ($oceaneData['is_action_eds_heritee_oceane'] == 1) ? $oceaneData['herite_oceane_action_en_cours'] : $paramsUrgence[$oceaneData['oceane_priority']]['id_action_en_cours_eds'];
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #24 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayCreationTocTrans() — ligne 1082
Contexte   :
```php
            $data['type_ticket'] = $this->getOceane->getTicketType();
            $data['origin'] = $this->getOceane->getOrigin();
            $assemblee = $this->app->get('AnalyseImpact')->getNomAssemblee($astroSession['type'], $ticketId);
            // Récupération des assemblées niveau 1 selon le type de ressource

            if ($data['type'] == 'TRCCABLE' || $data['type'] == 'TRONCABLE' || $data['type'] == 'CABLE') {
                $assembleeNiveauUn = $this->airele->getDataTronconNiveauUn($astroSession ['id3']);
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #25 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : creerTicketRessourceAdsl() — ligne 1150
Contexte   :
```php
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $this->loginId",
            "X-HTTP-Method-Override: PATCH"
        );
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #26 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1316
Contexte   :
```php
                $libSite = $this->getOceane->getTicketParamsAttribute('Parameter', 'LIBSITE');
                if ($libSite != "") {
                    $donnesTempsReel = $this->app->get('Cia')->getDataSite($libSite, $traceData);
                }

            }

```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #27 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : initApi() — ligne 101
Contexte   :
```php
                $typeRessourceIadr = $this->getOceane->getTicketCharacteristics(3);
                //CODE_DETECTEUR_IADR
                $codeDetecteur = $this->getOceane->getTicketCharacteristics(5);
                //RESSOURCE_IADR controle a verifier
                $ressource = $this->getOceane->getTicketCharacteristics(4);
                $libelleTechnique = StringTools::convertEncoding($this->getOceane->getTicketCharacteristics(6), 'ISO-8859-15', 'UTF-8');

```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #28 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : updateDateActionEnCoursEds() — ligne 387
Contexte   :
```php
        $oceaneUpdateUrl = $this->globalApiUrlService->getUrlApi('OCEANE_UPT');

        $troubleTicketUpdate = new OceaneUpd($connexionDataUrl, $oceaneUpdateUrl);
        $oceaneAssistant = new OceaneAssistant($this->app);
        $dateActionEnCoursEds = $oceaneAssistant->changeDateToUTCoceane(date("d/m/Y H:i", strtotime("+30 minutes")));

        $values = array(
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #29 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : getEDSActif() — ligne 418
Contexte   :
```php
        $result = $OceaneFg->getResponseFindandGetTroubleTicket($ticketID);
        if (isset($result->TroubleTicketResponse->TroubleTicketResponse)) {
            $troubleTicketResponse = $result->TroubleTicketResponse->TroubleTicketResponse;

            $partyRole = $troubleTicketResponse->PartyRole;
            foreach ($partyRole as $key => $value) {
                if ($partyRole[$key]->partyRoleType == "TroubleResolutionContributor" && property_exists($partyRole[$key], 'Local_PartyIntervention')) {
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #30 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : getEDSPilote() — ligne 452
Contexte   :
```php
        $result = $OceaneFg->getResponseFindandGetTroubleTicket($ticketID);
        if (isset($result->TroubleTicketResponse->TroubleTicketResponse)) {
            $troubleTicketResponse = $result->TroubleTicketResponse->TroubleTicketResponse;

            $partyRole = $troubleTicketResponse->PartyRole;
            foreach ($partyRole as $key => $value) {
                if ($partyRole[$key]->partyRoleType == "TroubleResolutionLeader" && property_exists($partyRole[$key], 'Local_PartyIntervention')) {
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #31 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getOceaneData() — ligne 42
Contexte   :
```php
        $oceaneApiData = $this->app->get('GlobalApiUrlService')->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');
        $astroId = $this->app->get('AstroRepository')->getAstroIdByTicket($ticketId);

        $headerConfig = array(
            "X-Client-User-Id: $cuiId"
        );
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #32 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : isChild() — ligne 471
Contexte   :
```php
        $oceaneApiData = $this->app->get('GlobalApiUrlService')->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $cuiId"
        );
        $oceaneApi = new ApiOceane($token, $headerConfig);
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #33 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : getResponseTicketClosure() — ligne 777
Contexte   :
```php
        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $connectedGroup = key_exists('connectedgroup',$astroSession) ? $astroSession['connectedgroup'] : '';

        $loginUser = (key_exists('api', $this->app->config) && $this->app->config['api']) ? $this->app->get('AstroRepository')->getCompteMachine($connectedGroup) : strtoupper($this->app->get('Session')->getUtilisateurLogin());

        $this->hbmLogin = $loginUser;
        $this->getapeService = $this->app->get('Gatape');
```

Question métier : Clé de session dynamique détectée — cette clé est-elle nettoyée explicitement dans TOUS les chemins de sortie ? (transitions : ASSEMBLEE→CABLE, EQUIPEMENT→CABLE, reclassification Océane)

---

**Gap #34 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : checkOceane() — ligne 342
Contexte   :
```php
        $oceaneApiData = $this->app->get('GlobalApiUrlService')->getUrlApi('API_OCEANE');
        $token = $this->app->get('Gatape')->getToken($oceaneApiData, 'inside');
        $this->loginId = (key_exists('api', $this->app->config) && $this->app->config['api']) ? $this->getLogin() : $this->app->get('Session')->getUtilisateurLogin();
        $headerConfig = array(
            "X-Client-User-Id: $this->loginId",
            "X-HTTP-Method-Override: PATCH"
        );
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #35 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 367
Contexte   :
```php
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');
        $login = $this->app->get('Session')->getUtilisateurLogin();

        $headerConfig = array(
            "X-Client-User-Id: $login",
            "X-HTTP-Method-Override: PATCH"
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #36 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceaneConfirmer() — ligne 541
Contexte   :
```php
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $this->hbmLogin",
            "X-HTTP-Method-Override: PATCH"
        );
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #37 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceaneConfirmerTrans() — ligne 589
Contexte   :
```php
        $oceaneApiData = $this->globalApiUrlService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $loginUser",
            "X-HTTP-Method-Override: PATCH"
        );
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #38 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ajoutCommentaireConfirmerTrans() — ligne 669
Contexte   :
```php
        $oceaneApiData = $this->globalApiUrlService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $loginUser",
            "X-HTTP-Method-Override: PATCH"
        );
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #39 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ajoutNbrClientImpacte() — ligne 699
Contexte   :
```php
        $oceaneApiData = $this->globalApiUrlService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $loginUser",
            "X-HTTP-Method-Override: PATCH"
        );
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #40 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateChampComplementaire() — ligne 757
Contexte   :
```php
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $this->hbmLogin",
            "X-HTTP-Method-Override: PATCH"
        );
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #41 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : getResponseTicketClosure() — ligne 784
Contexte   :
```php
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $this->hbmLogin",
            "X-HTTP-Method-Override: PATCH"
        );
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #42 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 265
Contexte   :
```php
                    $token = base64_encode(md5(date('yyyymmdd') . 'link_astro_charter'));
                    $chaine = str_replace('###' . $arg . '###', $token, $chaine);
                    break;

                case 'DATE':
                    if (is_null($this->findAndGet)) {
                        $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
```

Question métier : Cette méthode de protection du secret d'authentification est ancienne et non conforme aux standards actuels. S'agit-il d'une contrainte documentée ou cette protection est-elle prévue pour évoluer lors de la migration ?

---

**Gap #43 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 114
Contexte   :
```php
        $this->getOceane = $this->app->get('OceaneGet');
        $this->getOceane->getOceaneData($ticketId, $this->loginId);
        $this->id1 = $this->getOceane->getRessourceIds(1);
        $this->id2 = $this->getOceane->getRessourceIds(2);
        $this->id3 = $this->getOceane->getRessourceIds(3);
        $resourceSpecification = "";
        $libSite = "";
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #44 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChainePrimoAiguillageTroncon() — ligne 472
Contexte   :
```php
        $this->getOceane = $this->app->get('OceaneGet');
        $this->getOceane->getOceaneData($ticketId, $this->loginId);

        $ext1 = $this->getOceane->getRessourceIds(1);//sans $this->transcodage()
        $ext2 = $this->getOceane->getRessourceIds(2);

        $isSitePassifext1 = $this->refSiteRepository->isSitePassif($this->transcodage($ext1));
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #45 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : getDataPariv2() — ligne 688
Contexte   :
```php
        $complementaryField6 = $this->getOceane->getTicketCharacteristics(6);

        $this->globalApiService = $this->app->get('GlobalApiUrlService');
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');

        $this->getapeService = $this->app->get('Gatape');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');
```

Question métier : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non documentés : (1) Oceane indisponible → que faire ? (2) Oceane retourne null → continuer ou bloquer ? (3) État retourné non prévu par l'enchaînement → quelle situation déclenchée ?

---

**Gap #46 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : abandonnerProcess() — ligne 266
Contexte   :
```php
        $detailProbleme = $this->astroIhmSqlRepository->getDetailFamilleProblemeValues($idJeu, $typeRessourceProd);

        if($incidentEnCours){
            $data['detail_cause_abandon'] = StringTools::convertEncoding($data['detail_cause_abandon'], 'ISO-8859-15', 'UTF-8');
        }
        $abandonMessage = new Message($this->app, $astroId, $messageFile, $sessId);
```

Question métier : Point de décision — 'incidentEnCours'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #47 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : getCommentaireImpactClient() — ligne 391
Contexte   :
```php
        $detectionDate = $this->getOceane->getDetectionDate();
        $oceaneAssistant = new OceaneAssistant($this->app);
        if ($dataAdelia) {
            $dataAdelia['SEUIL_GRAVE'] = intval($dataAdelia['SEUIL_GRAVE']);
            $dataAdelia['SEUIL_MAJEUR'] = intval($dataAdelia['SEUIL_MAJEUR']);
        }
```

Question métier : Point de décision — 'dataAdelia'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #48 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : getCommentaireImpactClient() — ligne 407
Contexte   :
```php

        }
        if ($dataAdelia['TOTAL_CLIENTS'] > 0) {
            if ($dataAstro['ADELIA_MANUEL'] == 'o') {
                $dataAdeliaManuel = $this->adeliaRepository->getDataBlobManuel($dataAstro['ID_TICKET_ASTRO']);
                if ($dataAdeliaManuel['BEGIN_DATE'] != '' && $dataAdeliaManuel['SEUIL_GRAVE'] != '' && $dataAdeliaManuel['SEUIL_MAJEUR'] != '') {
```

Question métier : Point de décision — 'dataAdelia'['TOTAL_CLIENTS'] > 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #49 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : getCommentaireImpactClientTvNum() — ligne 435
Contexte   :
```php
        $idRessource = '';
        $oceaneAssistant = new OceaneAssistant($this->app);
        if ($dataAdelia) {
            $dataAdelia['SEUIL_GRAVE'] =  intval($dataAdelia['SEUIL_GRAVE']);
            $dataAdelia['SEUIL_MAJEUR'] = intval($dataAdelia['SEUIL_MAJEUR']);
        }
```

Question métier : Point de décision — 'dataAdelia'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #50 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : getCommentaireImpactClientTvNum() — ligne 449
Contexte   :
```php
        $commentaire .= 'TVNUM'.':'.$dataFiltered['TVNUM'] . $rc;

        if ($dataAdelia['TOTAL_CLIENTS'] > 0) {
            if ($dataAstro['ADELIA_MANUEL'] == 'o') {
                $dataAdeliaManuel = $this->adeliaRepository->getDataBlobManuel($dataAstro['ID_TICKET_ASTRO']);
                if ($dataAdeliaManuel['BEGIN_DATE'] != '' && $dataAdeliaManuel['SEUIL_GRAVE'] != '' && $dataAdeliaManuel['SEUIL_MAJEUR'] != '') {
```

Question métier : Point de décision — 'dataAdelia'['TOTAL_CLIENTS'] > 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #51 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : getCommentaireImpactClientTvNum() — ligne 461
Contexte   :
```php
            } else {
                $ticket = $this->astroRepository->getTicket($dataAstro['ID_TICKET_ASTRO']);
                if (count($ticket)) {
                    $idRessource = $ticket[0]['ID_RESSOURCE'];
                }
                $result = $this->getSeuilsAdelia($idRessource, $adeliaId ,$dataAstro, $compteMachine);
```

Question métier : Point de décision — count('ticket'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #52 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : preconisationImpactPrioriteAdsl() — ligne 617
Contexte   :
```php
        $prestations = '';
        $isNetVpnFinal = '';
        if (!$droitTools->isIncident($ticketId)) {
            $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
            $astroId = $astroSession['astroid'];
            $type = $astroSession['type'];
```

Question métier : Point de décision — !'droitTools'->isIncident('ticketId'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #53 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : preconisationImpactPrioriteAdsl() — ligne 625
Contexte   :
```php
            $fonctions = $droitTools->getDroitFonction($idBandeau);
            $droitEds = $droitTools->droitEds($ticketId, $astroSession['connectedgroup'], $astroSession['pilotgroup']);
            if ($isApi == 1) {
                $astroId = $astrId;
            }
            $informerClient = $this->informerClient($astroId, $login);
```

Question métier : Point de décision — 'isApi' égal à 1. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #54 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : preconisationImpactPrioriteAdsl() — ligne 633
Contexte   :
```php
            $totalClients = (is_array($adelia) && key_exists('TOTAL_CLIENTS', $adelia)) ? intval($adelia['TOTAL_CLIENTS']) : 0;
            $nombreClientEntreprise = (is_array($adelia) && key_exists('CLIENTS_ENTREPRISE', $adelia)) ? $adelia['CLIENTS_ENTREPRISE'] : '';
            if ($nombreClientEntreprise == 'oui' || intval($nombreClientEntreprise) > 0) {
                $isClientEntreprise = true;
            }
            $oceaneAssistant = new OceaneAssistant($this->app);
```

Question métier : Point de décision — 'nombreClientEntreprise' égal à 'oui' ou intval('nombreClientEntreprise') > 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #55 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : preconisationImpactPrioriteAdsl() — ligne 639
Contexte   :
```php
            $idJeuParam = $this->astroRepository->getJeuParamByBandeauFonction($idBandeau, 'CONFIRMER_GENERIQUE');
            $isNetVpn = $this->astroRepository->checkNetVpn($idJeuParam);
            if (!empty($adelia) && key_exists('PRESTATIONS', $adelia)) {
                $prestations = key_exists('PRESTATIONS', $adelia) ? json_decode($adelia['PRESTATIONS'], true) : '';
            }

```

Question métier : Point de décision — !le champ 'adelia' est vide && key_exists('PRESTATIONS', $adelia). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #56 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : preconisationImpactPrioriteAdsl() — ligne 643
Contexte   :
```php
            }

            if (!empty($adelia) && !empty($prestations) && $prestations != '' && key_exists('NETVPN', $prestations) && $prestations['NETVPN'] > 0) {
                $isNetVpnAdelia = 1;
            }
            if ($isNetVpn == '1' && $isNetVpnAdelia == 1) {
```

Question métier : Point de décision — !le champ 'adelia' est vide && !le champ 'prestations' est vide && $prestations != '' && key_exists('NETVPN', $prestations) && $prestations['NETVPN'] > 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #57 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 733
Contexte   :
```php
    private function recupererDonneesTicket(string $ticketId, string $typeRessource, bool $api, $assemblee): array
    {
        if(is_null($assemblee)) {
            $assemblee = $this->analyseService->getNomAssemblee($typeRessource, $ticketId);
        }

```

Question métier : Point de décision — is_null('assemblee'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #58 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : preconisationPrioriteTrans() — ligne 768
Contexte   :
```php
        $idChampJeuParam = null;
        foreach ($listChamps as $value) {
            if (key_exists('CODE', $value) && $value['CODE'] == 'PRIORITE') {
                $idChampJeuParam = $value['ID_CHAMP_JEU_PARAM'];
                break;
            }
```

Question métier : Point de décision — key_exists('CODE', 'value') et 'value'['CODE'] égal à 'PRIORITE'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #59 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : preconisationPrioriteTrans() — ligne 792
Contexte   :
```php
        $isAssemblee = $retourCountByService['is_assemblee'] ?? false;
        $isEquipementTrans = $retourCountByService['is_equipement_trans'] ?? false;
        if (!$isAssemblee && !$isEquipementTrans) {
            $countByService['troncon_id'] = $troncon;
        }
        $countByService['impact_result'] = $countByService['result'];
```

Question métier : Point de décision — !'isAssemblee' et !'isEquipementTrans'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #60 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : preconisationPrioriteTrans() — ligne 801
Contexte   :
```php
        $dataPrioImpact = $countByService;
        $dataPrioImpact['HNO'] = $isHno ? 'HNO' : 'HO';
        if (is_array($dataPrioImpact) && !empty($dataPrioImpact) && key_exists('impact_result', $dataPrioImpact)) {
            if (key_exists('VoIP', $dataPrioImpact['impact_result'])) {
                unset($dataPrioImpact['impact_result']['VoIP']);
            }
```

Question métier : Point de décision — is_array($dataPrioImpact) && !le champ 'dataPrioImpact' est vide && key_exists('impact_result', $dataPrioImpact). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #61 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : preconisationPrioriteTrans() — ligne 802
Contexte   :
```php
        $dataPrioImpact['HNO'] = $isHno ? 'HNO' : 'HO';
        if (is_array($dataPrioImpact) && !empty($dataPrioImpact) && key_exists('impact_result', $dataPrioImpact)) {
            if (key_exists('VoIP', $dataPrioImpact['impact_result'])) {
                unset($dataPrioImpact['impact_result']['VoIP']);
            }
        }
```

Question métier : Point de décision — key_exists('VoIP', 'dataPrioImpact'['impact_result']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #62 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : preconisationPrioriteTrans() — ligne 816
Contexte   :
```php
            'Internet', 'NETVPN', 'LL=2M', 'LL>2M', 'TDSL', 'T2'
        ] as $service) {
            if (!isset($dataPrioImpact['impact_result'][$service])) {
                $dataPrioImpact['impact_result'][$service] = 0;
            }
        }
```

Question métier : Point de décision — !isset('dataPrioImpact'['impact_result']['service']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #63 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : preconisationPrioriteTrans() — ligne 822
Contexte   :
```php
        $arrayDeclencher = $dataPrioImpact['impact_result'] ?? [];
        // Nettoyage VoIP
        if (isset($arrayDeclencher['VoIP'])) {
            unset($arrayDeclencher['VoIP']);
        }
        // Calcul DEC
```

Question métier : Point de décision — isset('arrayDeclencher'['VoIP']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #64 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : preconisationPrioriteTrans() — ligne 826
Contexte   :
```php
        }
        // Calcul DEC
        if (!is_null($dataPrioImpact) && key_exists('impact_result', $dataPrioImpact)) {
            foreach ($arrayDeclencher as $k => $v) {
                foreach ($decData as $value2) {
                    if (($k == $value2['TYPE'] || $value2['TYPE'] == '_TOTAL') && !$decDone) {
```

Question métier : Point de décision — !is_null('dataPrioImpact') et key_exists('impact_result', 'dataPrioImpact'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #65 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 879
Contexte   :
```php
    private function getPrioriteFromData($dataPrioImpact, $data, &$doneFlag)
    {
        if ($doneFlag || is_null($dataPrioImpact) || !key_exists('impact_result', $dataPrioImpact)) {
            return '-';
        }
        foreach ($dataPrioImpact['impact_result'] as $k => $v) {
```

Question métier : Point de décision — 'doneFlag' ou is_null('dataPrioImpact') ou !key_exists('impact_result', 'dataPrioImpact'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #66 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 884
Contexte   :
```php
        foreach ($dataPrioImpact['impact_result'] as $k => $v) {
            foreach ($data as $value2) {
                if ($doneFlag) break;
                if ($k == $value2['TYPE'] || $value2['TYPE'] == '_TOTAL') {
                    $op = $value2['OPERATOR'];
                    $val = intval($value2['OPERATOR_VALUE']);
```

Question métier : Point de décision — 'doneFlag'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #67 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 894
Contexte   :
```php
                    $gtrOk = is_null($gtr) || (key_exists('gtr_final', $dataPrioImpact) && $dataPrioImpact['gtr_final'] == $gtr);
                    if ($op == '>=') {
                        if ($v >= $val && $gtrOk && $hnoOk) {
                            $doneFlag = true;
                            return 'P' . $prio;
                        }
```

Question métier : Point de décision — 'v' >= 'val' et 'gtrOk' et 'hnoOk'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #68 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 899
Contexte   :
```php
                        }
                    } elseif ($op == '<=') {
                        if ($v <= $val && $gtrOk && $hnoOk) {
                            $doneFlag = true;
                            return 'P' . $prio;
                        }
```

Question métier : Point de décision — 'v' <= 'val' et 'gtrOk' et 'hnoOk'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #69 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 909
Contexte   :
```php
                    $prio = $value2['PRIORITE'] ?? null;
                    $hnoOk = is_null($hno) || (key_exists('HNO', $dataPrioImpact) && $dataPrioImpact['HNO'] == $hno);
                    if (key_exists('gtr_final', $dataPrioImpact) && $dataPrioImpact['gtr_final'] == $gtr && $hnoOk) {
                        $doneFlag = true;
                        return 'P' . $prio;
                    }
```

Question métier : Point de décision — key_exists('gtr_final', 'dataPrioImpact') et 'dataPrioImpact'['gtr_final'] égal à 'gtr' et 'hnoOk'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #70 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 917
Contexte   :
```php
                    $prio = $value2['PRIORITE'] ?? null;
                    $hnoOk = is_null($hno) || (key_exists('HNO', $dataPrioImpact) && $dataPrioImpact['HNO'] == $hno);
                    if ($hnoOk) {
                        $doneFlag = true;
                        return 'P' . $prio;
                    }
```

Question métier : Point de décision — 'hnoOk'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #71 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : getSeuilsAdelia() — ligne 953
Contexte   :
```php
        $dataAdeliaSavedFirst = $this->adeliaService->saveAdeliaDataFirst( true,$dataAdeliaArraySimulate, $data['ID_TICKET_ASTRO']);

        if (!is_null($result)) {
            $dataAdeliaArray = json_decode($result);
            $dataAdeliaSaved = $this->adeliaService->saveAdeliaData($dataAdeliaArray, $data['ID_TICKET_ASTRO'],array(),true);

```

Question métier : Point de décision — !is_null('result'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #72 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : getCommentaireImpactClient() — ligne 408
Contexte   :
```php
        }
        if ($dataAdelia['TOTAL_CLIENTS'] > 0) {
            if ($dataAstro['ADELIA_MANUEL'] == 'o') {
                $dataAdeliaManuel = $this->adeliaRepository->getDataBlobManuel($dataAstro['ID_TICKET_ASTRO']);
                if ($dataAdeliaManuel['BEGIN_DATE'] != '' && $dataAdeliaManuel['SEUIL_GRAVE'] != '' && $dataAdeliaManuel['SEUIL_MAJEUR'] != '') {
                    $commentaire .= 'grave à partir du ' . $this->adeliaService->getDateSeuil($dataAdeliaManuel['BEGIN_DATE'], $dataAdeliaManuel['SEUIL_GRAVE'], true) . $rc;
```

Question métier : Valeur de référence non documentée — La décision « 'dataAstro'['ADELIA_MANUEL'] égal à 'o' » repose sur la valeur 'o'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #73 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : getCommentaireImpactClientTvNum() — ligne 450
Contexte   :
```php

        if ($dataAdelia['TOTAL_CLIENTS'] > 0) {
            if ($dataAstro['ADELIA_MANUEL'] == 'o') {
                $dataAdeliaManuel = $this->adeliaRepository->getDataBlobManuel($dataAstro['ID_TICKET_ASTRO']);
                if ($dataAdeliaManuel['BEGIN_DATE'] != '' && $dataAdeliaManuel['SEUIL_GRAVE'] != '' && $dataAdeliaManuel['SEUIL_MAJEUR'] != '') {
                    $commentaire .= 'grave à partir du ' . $this->adeliaService->getDateSeuil($dataAdeliaManuel['BEGIN_DATE'], $dataAdeliaManuel['SEUIL_GRAVE'], true) . $rc;
```

Question métier : Valeur de référence non documentée — La décision « 'dataAstro'['ADELIA_MANUEL'] égal à 'o' » repose sur la valeur 'o'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #74 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : preconisationImpactPrioriteAdsl() — ligne 633
Contexte   :
```php
            $totalClients = (is_array($adelia) && key_exists('TOTAL_CLIENTS', $adelia)) ? intval($adelia['TOTAL_CLIENTS']) : 0;
            $nombreClientEntreprise = (is_array($adelia) && key_exists('CLIENTS_ENTREPRISE', $adelia)) ? $adelia['CLIENTS_ENTREPRISE'] : '';
            if ($nombreClientEntreprise == 'oui' || intval($nombreClientEntreprise) > 0) {
                $isClientEntreprise = true;
            }
            $oceaneAssistant = new OceaneAssistant($this->app);
```

Question métier : Valeur de référence non documentée — La décision « 'nombreClientEntreprise' égal à 'oui' ou intval('nombreClientEntreprise') > 0 » repose sur la valeur 'oui'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #96 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : getCommentaireImpactClient() — ligne 408
Contexte   :
```php
            if ($dataAstro['ADELIA_MANUEL'] == 'o') {
                $dataAdeliaManuel = $this->adeliaRepository->getDataBlobManuel($dataAstro['ID_TICKET_ASTRO']);
                if ($dataAdeliaManuel['BEGIN_DATE'] != '' && $dataAdeliaManuel['SEUIL_GRAVE'] != '' && $dataAdeliaManuel['SEUIL_MAJEUR'] != '') {
                    $commentaire .= 'grave à partir du ' . $this->adeliaService->getDateSeuil($dataAdeliaManuel['BEGIN_DATE'], $dataAdeliaManuel['SEUIL_GRAVE'], true) . $rc;
                    $commentaire .= 'majeur à partir du ' . $this->adeliaService->getDateSeuil($dataAdeliaManuel['BEGIN_DATE'], $dataAdeliaManuel['SEUIL_MAJEUR'], true) . $rc;
```

Question métier : Le code situation 'o' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #97 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : getCommentaireImpactClientTvNum() — ligne 450
Contexte   :
```php
            if ($dataAstro['ADELIA_MANUEL'] == 'o') {
                $dataAdeliaManuel = $this->adeliaRepository->getDataBlobManuel($dataAstro['ID_TICKET_ASTRO']);
                if ($dataAdeliaManuel['BEGIN_DATE'] != '' && $dataAdeliaManuel['SEUIL_GRAVE'] != '' && $dataAdeliaManuel['SEUIL_MAJEUR'] != '') {
                    $commentaire .= 'grave à partir du ' . $this->adeliaService->getDateSeuil($dataAdeliaManuel['BEGIN_DATE'], $dataAdeliaManuel['SEUIL_GRAVE'], true) . $rc;
                    $commentaire .= 'majeur à partir du ' . $this->adeliaService->getDateSeuil($dataAdeliaManuel['BEGIN_DATE'], $dataAdeliaManuel['SEUIL_MAJEUR'], true) . $rc;
```

Question métier : Le code situation 'o' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #98 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : preconisationImpactPrioriteAdsl() — ligne 633
Contexte   :
```php
            if ($nombreClientEntreprise == 'oui' || intval($nombreClientEntreprise) > 0) {
                $isClientEntreprise = true;
            }
            $oceaneAssistant = new OceaneAssistant($this->app);
            $idJeuParam = $this->astroRepository->getJeuParamByBandeauFonction($idBandeau, 'CONFIRMER_GENERIQUE');
```

Question métier : Le code situation 'oui' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #99 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : preconisationImpactPrioriteAdsl() — ligne 646
Contexte   :
```php
            if ($isNetVpn == '1' && $isNetVpnAdelia == 1) {
                $isNetVpnFinal = '1';
            } else {
                $isNetVpnFinal = '';
            }
```

Question métier : Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #100 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : preconisationPrioriteTrans() — ligne 768
Contexte   :
```php
            if (key_exists('CODE', $value) && $value['CODE'] == 'PRIORITE') {
                $idChampJeuParam = $value['ID_CHAMP_JEU_PARAM'];
                break;
            }
        }
```

Question métier : Le code situation 'PRIORITE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #101 — Abandonner**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : preconisationPrioriteTrans() — ligne 829
Contexte   :
```php
                    if (($k == $value2['TYPE'] || $value2['TYPE'] == '_TOTAL') && !$decDone) {
                        $op = $value2['OPERATOR'];
                        $val = intval($value2['OPERATOR_VALUE']);
                        $gtr = $value2['GTR'] ?? null;
                        $gtrOk = is_null($gtr) || (key_exists('gtr_final', $dataPrioImpact) && $dataPrioImpact['gtr_final'] == $gtr);
```

Question métier : Le code situation '_TOTAL' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #102 — AgirPiloterValidation**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : validateAgirPiloterForm() — ligne 23
Contexte   :
```php
        $dateRetab = key_exists('agp_dtretab', $data) ? $data['agp_dtretab'] : '';

        if (key_exists('DATE_RETABLISSEMENT_DEMANDE_INTERVENTION',
                $regles) && $regles['DATE_RETABLISSEMENT_DEMANDE_INTERVENTION']["OBLIGATOIRE"] === '1') {
            if (!$this->notEmpty($dateRetab)) {
                $result = false;
```

Question métier : Point de décision — key_exists('DATE_RETABLISSEMENT_DEMANDE_INTERVENTION', 'regles') et 'regles'['DATE_RETABLISSEMENT_DEMANDE_INTERVENTION']["OBLIGATOIRE"] égal à = '1'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #103 — AgirPiloterValidation**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : validateAgirPiloterForm() — ligne 25
Contexte   :
```php
        if (key_exists('DATE_RETABLISSEMENT_DEMANDE_INTERVENTION',
                $regles) && $regles['DATE_RETABLISSEMENT_DEMANDE_INTERVENTION']["OBLIGATOIRE"] === '1') {
            if (!$this->notEmpty($dateRetab)) {
                $result = false;
                $message[] = 'Champ date rétablissement requis';
            }
```

Question métier : Point de décision — !'this'->notEmpty('dateRetab'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #104 — AgirPiloterValidation**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : validateAgirPiloterForm() — ligne 30
Contexte   :
```php
            }
        }
        if ($dateRetab !== '') {
            if (!$this->isDate($dateRetab, "d/m/Y H:i")) {
                $result = false;
                $message[] = 'Format date rétablissement invalide';
```

Question métier : Point de décision — 'dateRetab' différent de = ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #105 — AgirPiloterValidation**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : validateAgirPiloterForm() — ligne 31
Contexte   :
```php
        }
        if ($dateRetab !== '') {
            if (!$this->isDate($dateRetab, "d/m/Y H:i")) {
                $result = false;
                $message[] = 'Format date rétablissement invalide';
            }
```

Question métier : Point de décision — !'this'->isDate('dateRetab', "d/m/Y H:i"). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #106 — AgirPiloterValidation**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : validateAgirPiloterForm() — ligne 40
Contexte   :
```php
        $actionCoursEds = key_exists('agp_dtencours', $data) ? $data['agp_dtencours'] : '';

        if (key_exists('DATE_COURS_EDS_DEMANDE_INTERVENTION',
                $regles) && $regles['DATE_COURS_EDS_DEMANDE_INTERVENTION']["OBLIGATOIRE"] === '1') {
            if (!$this->notEmpty($actionCoursEds)) {
                $result = false;
```

Question métier : Point de décision — key_exists('DATE_COURS_EDS_DEMANDE_INTERVENTION', 'regles') et 'regles'['DATE_COURS_EDS_DEMANDE_INTERVENTION']["OBLIGATOIRE"] égal à = '1'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #107 — AgirPiloterValidation**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : validateAgirPiloterForm() — ligne 42
Contexte   :
```php
        if (key_exists('DATE_COURS_EDS_DEMANDE_INTERVENTION',
                $regles) && $regles['DATE_COURS_EDS_DEMANDE_INTERVENTION']["OBLIGATOIRE"] === '1') {
            if (!$this->notEmpty($actionCoursEds)) {
                $result = false;
                $message[] = 'Champ date action en cours requis';
            }
```

Question métier : Point de décision — !'this'->notEmpty('actionCoursEds'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #108 — AgirPiloterValidation**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : validateAgirPiloterForm() — ligne 47
Contexte   :
```php
            }
        }
        if ($actionCoursEds !== '') {
            if (!$this->isDate($actionCoursEds, "d/m/Y H:i")) {
                $result = false;
                $message[] = 'Format date action en cours invalide';
```

Question métier : Point de décision — 'actionCoursEds' différent de = ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #109 — AgirPiloterValidation**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : validateAgirPiloterForm() — ligne 48
Contexte   :
```php
        }
        if ($actionCoursEds !== '') {
            if (!$this->isDate($actionCoursEds, "d/m/Y H:i")) {
                $result = false;
                $message[] = 'Format date action en cours invalide';
            }
```

Question métier : Point de décision — !'this'->isDate('actionCoursEds', "d/m/Y H:i"). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #110 — AgirPiloterValidation**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : validateAgirPiloterForm() — ligne 56
Contexte   :
```php
        // Validation Commentaire charté
        $commentaire = key_exists('agp_commentaire', $data) ? $data['agp_commentaire'] : '';
        if (key_exists('COMMENTAIRE_DEMANDE_INTERVENTION',
                $regles) && $regles['COMMENTAIRE_DEMANDE_INTERVENTION']["OBLIGATOIRE"] === '1') {
            if (!$this->notEmpty($commentaire)) {
                $result = false;
```

Question métier : Point de décision — key_exists('COMMENTAIRE_DEMANDE_INTERVENTION', 'regles') et 'regles'['COMMENTAIRE_DEMANDE_INTERVENTION']["OBLIGATOIRE"] égal à = '1'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #111 — AgirPiloterValidation**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : validateAgirPiloterForm() — ligne 58
Contexte   :
```php
        if (key_exists('COMMENTAIRE_DEMANDE_INTERVENTION',
                $regles) && $regles['COMMENTAIRE_DEMANDE_INTERVENTION']["OBLIGATOIRE"] === '1') {
            if (!$this->notEmpty($commentaire)) {
                $result = false;
                $message[] = 'Champ commentaire requis';
            }
```

Question métier : Point de décision — !'this'->notEmpty('commentaire'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #112 — AgirPiloterValidation**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : validateAgirPiloterForm() — ligne 66
Contexte   :
```php
        // Validation Action en cours EDS
        $actionCoursEds = key_exists('agp_action_eds', $data) ? $data['agp_action_eds'] : '';
        if (key_exists('ACTION_EN_COURS_EDS',
                $regles) && $regles['ACTION_EN_COURS_EDS']["OBLIGATOIRE"] === '1') {
            if (!$this->notEmpty($actionCoursEds)) {
                $result = false;
```

Question métier : Point de décision — key_exists('ACTION_EN_COURS_EDS', 'regles') et 'regles'['ACTION_EN_COURS_EDS']["OBLIGATOIRE"] égal à = '1'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #113 — AgirPiloterValidation**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : validateAgirPiloterForm() — ligne 68
Contexte   :
```php
        if (key_exists('ACTION_EN_COURS_EDS',
                $regles) && $regles['ACTION_EN_COURS_EDS']["OBLIGATOIRE"] === '1') {
            if (!$this->notEmpty($actionCoursEds)) {
                $result = false;
                $message[] = 'Champ action en cours EDS requis';
            }
```

Question métier : Point de décision — !'this'->notEmpty('actionCoursEds'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #114 — AgirPiloterValidation**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : validateAgirPiloterForm() — ligne 75
Contexte   :
```php
        // Validation du Niveau d'urgence
        $actionCoursEds = key_exists('niveau_urgence', $data) ? $data['niveau_urgence'] : '';
        if (key_exists('NIVEAU_URGENCE',
                $regles) && $regles['NIVEAU_URGENCE']["OBLIGATOIRE"] === '1') {
            if (!$this->notEmpty($actionCoursEds)) {
                $result = false;
```

Question métier : Point de décision — key_exists('NIVEAU_URGENCE', 'regles') et 'regles'['NIVEAU_URGENCE']["OBLIGATOIRE"] égal à = '1'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #115 — AgirPiloterValidation**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : validateAgirPiloterForm() — ligne 77
Contexte   :
```php
        if (key_exists('NIVEAU_URGENCE',
                $regles) && $regles['NIVEAU_URGENCE']["OBLIGATOIRE"] === '1') {
            if (!$this->notEmpty($actionCoursEds)) {
                $result = false;
                $message[] = 'Champ niveau d\'urgence requis';
            }
```

Question métier : Point de décision — !'this'->notEmpty('actionCoursEds'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #116 — AgirPiloterValidation**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : validateAgirPiloterForm() — ligne 83
Contexte   :
```php
        }

        if (!$result) {
            return $message;
        }
        return true;
```

Question métier : Point de décision — !'result'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #117 — AgirPiloterValidation**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : validateAgirPiloterForm() — ligne 24
Contexte   :
```php
                $regles) && $regles['DATE_RETABLISSEMENT_DEMANDE_INTERVENTION']["OBLIGATOIRE"] === '1') {
            if (!$this->notEmpty($dateRetab)) {
                $result = false;
                $message[] = 'Champ date rétablissement requis';
            }
```

Question métier : Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #118 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1() — ligne 234
Contexte   :
```php
        $droitEds = $droitAstro->droitEds($ticketId, $astroSession['connectedgroup'], $astroSession['pilotgroup']);

        if (count($deports) > 0) {
            foreach ($deports as $v) {
                $maitreDeport = $this->edrService->getDataMaitreDeport($v, false);
                if ($maitreDeport['status'] == 'ok') {
```

Question métier : Point de décision — count('deports') > 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #119 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1() — ligne 237
Contexte   :
```php
            foreach ($deports as $v) {
                $maitreDeport = $this->edrService->getDataMaitreDeport($v, false);
                if ($maitreDeport['status'] == 'ok') {
                    $tDeports[$maitreDeport['id_rsc']] = $v;
                }
            }
```

Question métier : Point de décision — 'maitreDeport'['status'] égal à 'ok'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #120 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1() — ligne 245
Contexte   :
```php

        $hMaster = '';
        if ($master != '' && $master != $dslamName) {
            $maitreDeport = $this->edrService->getDataMaitreDeport($master, false);
            $idRscMaster = $maitreDeport['id_rsc'];
            if ($maitreDeport['status'] == 'nok') {
```

Question métier : Point de décision — 'master' différent de '' et 'master' différent de 'dslamName'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #121 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1() — ligne 258
Contexte   :
```php
        $alarme = $helper->getIntituleAla($rsc, false);
        $dslam = '';
        if ($alarme != $dslamName) {
            $dslam = $this->interventionHelper->getDslamNameInput($dslamName, $droitEds['guest']);
        }
        $dslam .= $this->interventionHelper->getDslamAlarmeInput($alarme, $droitEds['guest']);
```

Question métier : Point de décision — 'alarme' différent de 'dslamName'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #122 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1Generique() — ligne 531
Contexte   :
```php
        $typeRessource = $astroSession['type_ressource'];

        if ($typeRessource == 'DSLAM') {
            $idRscMaster = '';
            $dslam = '';
            $helper = new Edr();
```

Question métier : Point de décision — 'typeRessource' égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #123 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1Generique() — ligne 541
Contexte   :
```php
        }

        if ($typeRessource == 'DSLAM') {
            $idRessource = $astroSession['id_ressource'];
            $rsc = $this->astroRepository->getRessource($idRessource);
            $idRscDslam = $rsc['ID_RESSOURCE_DSLAM'];
```

Question métier : Point de décision — 'typeRessource' égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #124 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1Generique() — ligne 551
Contexte   :
```php
        $agpEntite = $this->agpGeneriqueRepository->getEntiteByJeuFamille($idJeuParam, $astroSession['type']);

        if ($typeRessource == 'DSLAM') {

            $alarme = $helper->getIntituleAla($rsc, false);

```

Question métier : Point de décision — 'typeRessource' égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #125 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1Generique() — ligne 570
Contexte   :
```php
            $dslamName = (isset($result['equipmentName']) ? $result['equipmentName'] : '');

            if ($alarme != $dslamName) {
                $dslam = $this->interventionHelper->getDslamNameInput($dslamName, $droitEds['guest']);
            }
            $dslam .= $this->interventionHelper->getDslamAlarmeInput($alarme, $droitEds['guest']);
```

Question métier : Point de décision — 'alarme' différent de 'dslamName'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #126 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1Generique() — ligne 575
Contexte   :
```php
            $dslam .= $this->interventionHelper->getDslamAlarmeInput($alarme, $droitEds['guest']);

            if (count($deports) > 0) {
                foreach ($deports as $v) {
                    $maitreDeport = $this->edrService->getDataMaitreDeport($v, false);
                    if ($maitreDeport['status'] == 'ok') {
```

Question métier : Point de décision — count('deports') > 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #127 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1Generique() — ligne 578
Contexte   :
```php
                foreach ($deports as $v) {
                    $maitreDeport = $this->edrService->getDataMaitreDeport($v, false);
                    if ($maitreDeport['status'] == 'ok') {
                        $tDeports[$maitreDeport['id_rsc']] = $v;
                    }
                }
```

Question métier : Point de décision — 'maitreDeport'['status'] égal à 'ok'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #128 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1Generique() — ligne 586
Contexte   :
```php

            $hMaster = '';
            if ($master != '' && $master != $dslamName) {
                $maitreDeport = $this->edrService->getDataMaitreDeport($master, false);
                $idRscMaster = $maitreDeport['id_rsc'];
                if ($maitreDeport['status'] == 'nok') {
```

Question métier : Point de décision — 'master' différent de '' et 'master' différent de 'dslamName'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #129 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1Generique() — ligne 598
Contexte   :
```php
            $chassisCarte = $this->astroRepository->getCarteTicket($ticketId);

            if (!is_null($chassisCarte) && $chassisCarte && key_exists('CHASSIS', $chassisCarte)) {
                $listCartes = $this->getCartesLignes($chassisCarte['CHASSIS'], $result);
                $isCarteLigne = (isset($chassisCarte['CARTE']) && in_array($chassisCarte['CARTE'], $listCartes)) ? 'true' : 'false';
            }
```

Question métier : Point de décision — !is_null('chassisCarte') et 'chassisCarte' et key_exists('CHASSIS', 'chassisCarte'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #130 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1Generique() — ligne 606
Contexte   :
```php
        }

        if ($typeRessource == 'MIE') {
            $args[] = 'FG_NOMNAEQP';

        }
```

Question métier : Point de décision — 'typeRessource' égal à 'MIE'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #131 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1Generique() — ligne 611
Contexte   :
```php
        }

        if ($typeRessource == 'SLN' || $typeRessource == 'WDM_SID') {
            $args[] = 'FG_E1NOMNAEQP';

            $args[] = 'FG_E2NOMNAEQP';
```

Question métier : Point de décision — 'typeRessource' égal à 'SLN' ou 'typeRessource' égal à 'WDM_SID'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #132 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : getOptionsActionsGenerique() — ligne 708
Contexte   :
```php
        $dataDslam = array();

        if ($typeRessource == 'COMMUT' || $typeRessource == 'UNIRACC' || $typeRessource == 'CONNUM' || $typeRessource == 'MICBPNCSN' || $typeRessource == 'MICBPNCAA' || $typeRessource == 'MICBPNCOM') {
            $this->commutationRessource = $this->app->get('CommutationRessource');
            $filtre = $this->commutationRessource->varSystemeCommut($identifiants, $typeRessource);
        }
```

Question métier : Point de décision — 'typeRessource' égal à 'COMMUT' ou 'typeRessource' égal à 'UNIRACC' ou 'typeRessource' égal à 'CONNUM' ou 'typeRessource' égal à 'MICBPNCSN' ou 'typeRessource' égal à 'MICBPNCAA' ou 'typeRessource' égal à 'MICBPNCOM'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #133 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : getOptionsActionsGenerique() — ligne 712
Contexte   :
```php
            $filtre = $this->commutationRessource->varSystemeCommut($identifiants, $typeRessource);
        }
        if (($typeRessource == 'DSLAM' || $typeRessource == 'DSLAMDERCO') && $data['id_rsc'] != '' && $data['id_rsc_dslam'] != '') {
            $idRsc = $data['id_rsc'];
            $dataEdr = $this->edrRepository->getBlobDslam($data['id_rsc_dslam'])['BLOBDATA'];
            $ressource = $this->astroRepository->getRessource($data['id_rsc_dslam'] != $data['id_rsc'] ? $data['id_rsc'] : $data['id_rsc_dslam']);
```

Question métier : Point de décision — ('typeRessource' égal à 'DSLAM' ou 'typeRessource' égal à 'DSLAMDERCO') et 'data'['id_rsc'] différent de '' et 'data'['id_rsc_dslam'] différent de ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #134 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : getOptionsActionsGenerique() — ligne 717
Contexte   :
```php
            $ressource = $this->astroRepository->getRessource($data['id_rsc_dslam'] != $data['id_rsc'] ? $data['id_rsc'] : $data['id_rsc_dslam']);
            $ressource = is_array($ressource) && key_exists('DSLAM', $ressource) ? $ressource['DSLAM'] : '';
            if (!empty($ressource)) {
                $edrDslEquipe = $this->edrRepository->getDslEquipement($ressource);
            }
            $typeNro = is_array($edrDslEquipe) && key_exists('TYPE_NRO', $edrDslEquipe) && isset($edrDslEquipe['TYPE_NRO']) ? $edrDslEquipe['TYPE_NRO'] : '';
```

Question métier : Point de décision — !le champ 'ressource' est vide. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #135 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayPiloterGenerique() — ligne 731
Contexte   :
```php
    public function displayPiloterGenerique($data, $oceaneData, $ticketId, $idJeuParam, $api = false)
    {
        if (!$api) {
            $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        }
        $oceaneAssistant = new OceaneAssistant($this->app);
```

Question métier : Point de décision — !'api'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #136 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayPiloterGenerique() — ligne 747
Contexte   :
```php
            $priorityHoHno = $this->agpGeneriqueRepository->getActivationHoHnoByJeu($idJeuParam, $oceaneData['oceane_priority']);

            if (key_exists($oceaneData['oceane_priority'], $priorityHoHno)) {
                if ($data['agp_ho_hno_generique'] == 'HO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_ho'] == '1') {
                    $agpSuivreHno = 0;
                } elseif ($data['agp_ho_hno_generique'] == 'HNO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_hno'] == '1') {
```

Question métier : Point de décision — key_exists('oceaneData'['oceane_priority'], 'priorityHoHno'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #137 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayPiloterGenerique() — ligne 775
Contexte   :
```php

        $blocs = OceaneTools::getContents($agpCommentaire['COMMENTAIRE'], '##bloc_', '##');
        if (!empty($blocs) && key_exists(0, $blocs)) {
            foreach ($blocs as $blocName) {
                if ($blocName != 'choix_de_carte_trans' && $blocName != 'Types_Carte' && $blocName != 'Types' && $blocName != 'Carte_EAN' && $blocName != 'Complet') {
                    $blocVariable = $this->agpGeneriqueRepository->getBlocVariable($blocName);
```

Question métier : Point de décision — !le champ 'blocs' est vide && key_exists(0, $blocs). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #138 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayPiloterGenerique() — ligne 777
Contexte   :
```php
        if (!empty($blocs) && key_exists(0, $blocs)) {
            foreach ($blocs as $blocName) {
                if ($blocName != 'choix_de_carte_trans' && $blocName != 'Types_Carte' && $blocName != 'Types' && $blocName != 'Carte_EAN' && $blocName != 'Complet') {
                    $blocVariable = $this->agpGeneriqueRepository->getBlocVariable($blocName);
                    $commentaire = str_replace('##bloc_' . $blocName . '##', $blocVariable, $commentaire);
                }
```

Question métier : Point de décision — 'blocName' différent de 'choix_de_carte_trans' et 'blocName' différent de 'Types_Carte' et 'blocName' différent de 'Types' et 'blocName' différent de 'Carte_EAN' et 'blocName' différent de 'Complet'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #139 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayPiloterGenerique() — ligne 783
Contexte   :
```php
            }
        }
        if (is_string($data['id_commentaire']) && $data['id_commentaire'] == 'DiagSDH') {
            $accessNumber = $this->diagSdh->getAccessNumber($astroSession);
            $diagSdhData = $this->diagSdh->getDiagSdhInfos($accessNumber);
            $commentaire = is_array($diagSdhData) && !key_exists('message', $diagSdhData) ? $this->diagSdh->getCommentaireCharteActivationUiTicket($diagSdhData) : '';
```

Question métier : Point de décision — is_string('data'['id_commentaire']) et 'data'['id_commentaire'] égal à 'DiagSDH'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #140 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 840
Contexte   :
```php
    public function displayAgp2Generique($data, $oceaneData, $ticketId, $idJeuParam, $api = false)
    {
        if (!$api) {
            $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
            $data['connected_group'] = $astroSession['connectedgroup'];
        }
```

Question métier : Point de décision — !'api'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #141 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 858
Contexte   :
```php
            $priorityHoHno = $this->agpGeneriqueRepository->getActivationHoHnoByJeu($idJeuParam, $oceaneData['oceane_priority']);

            if (key_exists($oceaneData['oceane_priority'], $priorityHoHno)) {
                if ($data['agp_ho_hno_generique'] == 'HO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_ho'] == '1') {
                    $agpSuivreHno = 0;
                } elseif ($data['agp_ho_hno_generique'] == 'HNO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_hno'] == '1') {
```

Question métier : Point de décision — key_exists('oceaneData'['oceane_priority'], 'priorityHoHno'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #142 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 890
Contexte   :
```php
        $agpCommentaire = $this->agpGeneriqueRepository->getCommentaireByAction($idJeuParam, $agpIdAction);
        $data['id_valeur'] = $agpCommentaire['ID_COMMENTAIRE'];
        if (key_exists('intervenant', $data) && $data['intervenant'] != '') {
            $segComment = $this->app->get('AdminCommentaireRepository')->getCommentaireSecondaireByIntervenant($data);
            if (is_array($segComment) && isset($segComment['SECOND_COMMENT']) && trim($segComment['SECOND_COMMENT']) !== '') {
                $agpCommentaire['COMMENTAIRE'] = $segComment['SECOND_COMMENT'];
```

Question métier : Point de décision — key_exists('intervenant', 'data') et 'data'['intervenant'] différent de ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #143 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 892
Contexte   :
```php
        if (key_exists('intervenant', $data) && $data['intervenant'] != '') {
            $segComment = $this->app->get('AdminCommentaireRepository')->getCommentaireSecondaireByIntervenant($data);
            if (is_array($segComment) && isset($segComment['SECOND_COMMENT']) && trim($segComment['SECOND_COMMENT']) !== '') {
                $agpCommentaire['COMMENTAIRE'] = $segComment['SECOND_COMMENT'];
            }

```

Question métier : Point de décision — is_array('segComment') et isset('segComment'['SECOND_COMMENT']) et trim('segComment'['SECOND_COMMENT']) différent de = ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #144 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 904
Contexte   :
```php
        $isDslamTest = false;
        if ($api) {
            if ($data['type_ressource'] == 'DSLAM' || $data['type_ressource'] == 'DSLAMDERCO') {
                $isDslamTest = true;
            }
            $astroSession['type'] = $data['type_ressource'];
```

Question métier : Point de décision — 'data'['type_ressource'] égal à 'DSLAM' ou 'data'['type_ressource'] égal à 'DSLAMDERCO'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #145 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 910
Contexte   :
```php
            $astroSession['ticketid'] = $ticketId;
        } else {
            if ($astroSession['type'] == 'DSLAM' || $astroSession['type'] == 'DSLAMDERCO') {
                $isDslamTest = true;
            }
        }
```

Question métier : Point de décision — 'astroSession'['type'] égal à 'DSLAM' ou 'astroSession'['type'] égal à 'DSLAMDERCO'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #146 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 917
Contexte   :
```php
        $blocs = OceaneTools::getContents($agpCommentaire['COMMENTAIRE'], '##bloc_', '##');

        if (!empty($blocs) && key_exists(0, $blocs)) {
            foreach ($blocs as $blocName) {
                if ($isDslamTest) {
                    $blocVariable = $this->agpGeneriqueRepository->getBlocVariable($blocName);
```

Question métier : Point de décision — !le champ 'blocs' est vide && key_exists(0, $blocs). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #147 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 929
Contexte   :
```php
            }
        }
        if (is_string($data['id_commentaire']) && $data['id_commentaire'] == 'DiagSDH') {
            $astroSession['class'] = $oceaneData['class'];
            $astroSession['id1'] = $oceaneData['id1'];
            $astroSession['id2'] = $oceaneData['id2'];
```

Question métier : Point de décision — is_string('data'['id_commentaire']) et 'data'['id_commentaire'] égal à 'DiagSDH'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #148 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 941
Contexte   :
```php


        if ($isDslamTest) {
            $agpIdAstro = key_exists('agp_id_astro', $data) ? $data['agp_id_astro'] : null;
            $agpIdRsc = key_exists('agp_id_rsc', $data) ? $data['agp_id_rsc'] : null;
            $agpIdAction = key_exists('agp_id_action', $data) ? $data['agp_id_action'] : null;
```

Question métier : Point de décision — 'isDslamTest'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #149 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 967
Contexte   :
```php
                    $agpCCResult = $comm->getCommentaire();
                    // Ne remplacer le commentaire que si $idRscDslam est non vide
                    if ($idRscDslam !== null && $idRscDslam !== '') {
                        $commentaire = $agpCCResult;
                    }

```

Question métier : Point de décision — 'idRscDslam' différent de = null et 'idRscDslam' différent de = ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #150 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 983
Contexte   :
```php
        }

        if ($data['agp_ecran'] == 0) {

            $commentaire = preg_replace('/###[\s\S]+?###/ ', '', $commentaire);
        }
```

Question métier : Point de décision — 'data'['agp_ecran'] égal à 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #151 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 990
Contexte   :
```php
        $agpCommentaire['COMMENTAIRE'] = $commentaire;

        if (!$idUrgenceOceane) {
            $idUrgenceOceane = $idUrgence;
        }

```

Question métier : Point de décision — !'idUrgenceOceane'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #152 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : getCartesLignes() — ligne 1029
Contexte   :
```php

        foreach ($dslamArray['racks'] as $k => $v) {
            if ($dslamArray['racks'][$k]['rackName'] == $chassis) {
                foreach ($dslamArray['racks'][$k]['cards'] as $vv) {
                    $test = true;
                    // Carte dans la bonne catégorie ?
```

Question métier : Point de décision — 'dslamArray'['racks']['k']['rackName'] égal à 'chassis'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #153 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : getCartesLignes() — ligne 1033
Contexte   :
```php
                    $test = true;
                    // Carte dans la bonne catégorie ?
                    if (isset($vv['category']) && $vv['category'] != 'carte ligne') {
                        $test = false;
                    }

```

Question métier : Point de décision — isset('vv'['category']) et 'vv'['category'] différent de 'carte ligne'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #154 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : getCartesLignes() — ligne 1037
Contexte   :
```php
                    }

                    if ($test) {
                        $cartes[$vv['cardNumber']] = $vv['cardNumber'];
                    }
                }
```

Question métier : Point de décision — 'test'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #155 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayCreationTocTrans() — ligne 1087
Contexte   :
```php
            // Récupération des assemblées niveau 1 selon le type de ressource

            if ($data['type'] == 'TRCCABLE' || $data['type'] == 'TRONCABLE' || $data['type'] == 'CABLE') {
                $assembleeNiveauUn = $this->airele->getDataTronconNiveauUn($astroSession ['id3']);
                usort($assembleeNiveauUn, function ($a, $b) {
                    return (int)$a['fibre'] > (int)$b['fibre'];
```

Question métier : Point de décision — 'data'['type'] égal à 'TRCCABLE' ou 'data'['type'] égal à 'TRONCABLE' ou 'data'['type'] égal à 'CABLE'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #156 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayCreationTocTrans() — ligne 1093
Contexte   :
```php
                });
            }
            if ($data['type'] == 'SDH' || $data['type'] == 'SLN' || $data['type'] == 'PDH' || $data['type'] == 'ETH' || $data['type'] == 'OCH' || $data['type'] == 'WDM_SID') {
                $assembleeNiveauUn = $this->airele->getDataAssembleeNiveauUn($assemblee, $sessionId, $ticketId);
            }
            if ($data['type'] == 'MIE') {
```

Question métier : Point de décision — 'data'['type'] égal à 'SDH' ou 'data'['type'] égal à 'SLN' ou 'data'['type'] égal à 'PDH' ou 'data'['type'] égal à 'ETH' ou 'data'['type'] égal à 'OCH' ou 'data'['type'] égal à 'WDM_SID'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #157 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayCreationTocTrans() — ligne 1096
Contexte   :
```php
                $assembleeNiveauUn = $this->airele->getDataAssembleeNiveauUn($assemblee, $sessionId, $ticketId);
            }
            if ($data['type'] == 'MIE') {
                $nomEqpt1 = $this->getOceane->getTicketParamsAttribute('Parameter', 'NOMEQPT1');
                $assembleeNiveauUn = $this->airele->getDataAssembleeNiveauUn($nomEqpt1, $sessionId, $ticketId);
            }
```

Question métier : Point de décision — 'data'['type'] égal à 'MIE'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #158 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1292
Contexte   :
```php

        $astroId = $data['astroid'] ?? '';
        if ($astroId == '') {
            $astroId = $this->astroRepository->getAstroIdByTicket($this->ticketId);
        }
        $id3 = $data['id3'] ?? '';
```

Question métier : Point de décision — 'astroId' égal à ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #159 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1298
Contexte   :
```php
        $this->typeRessource = $type;

        if (!$this->getOceane) {
            $this->getOceane = $this->app->get('OceaneGet');
        }
        if ($this->ticketId && $this->getOceane) {
```

Question métier : Point de décision — !'this'->getOceane. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #160 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1301
Contexte   :
```php
            $this->getOceane = $this->app->get('OceaneGet');
        }
        if ($this->ticketId && $this->getOceane) {
            $this->getOceane->getOceaneData($this->ticketId, $this->loginId);
        }

```

Question métier : Point de décision — 'this'->ticketId et 'this'->getOceane. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #161 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1309
Contexte   :
```php
        $libSite = "";
        foreach ($args as $arg) {
            if ($arg == 'Temperature' || $arg == 'Etat_batterie' || $arg == 'Tension_batterie' || $arg == 'Element_HS') {
                $this->sessId = (key_exists('api', $this->app->config) && $this->app->config['api']) ? $this->getUserId() : $this->app->get('Session')->getUtilisateurId();
                $traceData = array(
                    'astro_id' => $this->astroRepository->getAstroIdByTicket($this->ticketId),
```

Question métier : Point de décision — 'arg' égal à 'Temperature' ou 'arg' égal à 'Etat_batterie' ou 'arg' égal à 'Tension_batterie' ou 'arg' égal à 'Element_HS'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #162 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1317
Contexte   :
```php
                );
                $libSite = $this->getOceane->getTicketParamsAttribute('Parameter', 'LIBSITE');
                if ($libSite != "") {
                    $donnesTempsReel = $this->app->get('Cia')->getDataSite($libSite, $traceData);
                }

```

Question métier : Point de décision — 'libSite' différent de "". Quel est le comportement attendu dans le cas contraire ?

---

**Gap #163 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1333
Contexte   :
```php
                    $replaceValue = $this->app->get('Transitool')->getValueTronconTransitool($arg, $id3, $this->typeRessource, $astroId);

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #164 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1339
Contexte   :
```php
                case 'CUID':
                    $replaceValue = $this->cuidUpdate;
                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #165 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1346
Contexte   :
```php
                case 'TICKETID':
                    $replaceValue = (!is_null($this->ticketId)) ? $this->ticketId : '';
                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #166 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1354
Contexte   :
```php
                    $replaceValue = (!is_null($this->eds)) ? $this->eds : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #167 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1362
Contexte   :
```php
                    $replaceValue = (!is_null($this->typeRessource)) ? $this->typeRessource : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #168 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1374
Contexte   :
```php
                case 'DATE':
                    $replaceValue = rtrim($this->getOceane->getCreationDate(), 'Z');
                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #169 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1379
Contexte   :
```php
                    break;
                case 'Etat_batterie':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {

                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['mode_fonctionnement_batterie'], $chaine);
```

Question métier : Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #170 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1387
Contexte   :
```php
                    break;
                case 'Element_HS':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {
                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['element_equipement_panne_tronc'], $chaine);
                    }
```

Question métier : Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #171 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1394
Contexte   :
```php
                    break;
                case 'Tension_batterie':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {
                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['tension'], $chaine);
                    }
```

Question métier : Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #172 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1401
Contexte   :
```php
                    break;
                case 'Temperature':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {
                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['temperature'], $chaine);
                    }
```

Question métier : Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #173 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1416
Contexte   :
```php
                    ];
                    $replaceValue = $this->getOceane->getTicketParamsAttribute('Parameter', $fgParameterMapping[$arg]);
                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #174 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1423
Contexte   :
```php
                    $replaceValue = $this->getOceane->getClosedTicketQuantity();

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #175 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1433
Contexte   :
```php
                    $replaceValue = ($description != '') ? $description : null;

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #176 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1440
Contexte   :
```php
                case 'Intervenant_EVT':
                    $codeDetecteur = StringTools::convertEncoding($this->getOceane->getTicketCharacteristics(5), 'ISO-8859-15', 'UTF-8');
                    if (!is_null($codeDetecteur)) {
                        $replaceValue = ($codeDetecteur != "ORANGE") ? $codeDetecteur : "UI";
                    }

```

Question métier : Point de décision — !is_null('codeDetecteur'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #177 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1444
Contexte   :
```php
                    }

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #178 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1466
Contexte   :
```php
                    $replaceValue = $this->refSiteRepository->getRefsiteColumn($arrayRefSite[$arg], $this->ticketId);

                    if (OceaneTools::isValidVariable($replaceValue) && gettype($replaceValue) != 'boolean') {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue') et gettype('replaceValue') différent de 'boolean'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #179 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1471
Contexte   :
```php
                    break;
                case 'PRIMO_AIGUILLAGE_TRONCON':
                    if ($this->typeRessource == 'TRONCABLE') {
                        $this->variableService = $this->app->get('Variable');

                        $replaceValue = $this->variableService->replaceTagsChainePrimoAiguillageTroncon($this->ticketId);
```

Question métier : Point de décision — 'this'->typeRessource égal à 'TRONCABLE'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #180 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1477
Contexte   :
```php
                        $replaceValue = preg_replace('/\s+/', ' ', $replaceValue);

                        if (OceaneTools::isValidVariable($replaceValue)) {
                            $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                        }
                        break;
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #181 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1484
Contexte   :
```php
                default:
                    $this->globalApiRepository = $this->app->get('GlobalApiRepository');
                    if ($this->globalApiRepository->isVariableAdminExist($arg, $type)) {
                        $resourceSpecification = ($this->getOceane->getRessourceType() !== null)
                            ? $this->getOceane->getRessourceType()
                            : $this->getOceane->getProductType();
```

Question métier : Point de décision — 'this'->globalApiRepository->isVariableAdminExist('arg', 'type'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #182 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1488
Contexte   :
```php
                            ? $this->getOceane->getRessourceType()
                            : $this->getOceane->getProductType();
                        if ($resourceSpecification) {
                            $dataIdentifiantsAdmin = ['type' => $resourceSpecification, 'nom' => $arg];
                            $tabIdentifiants = $this->globalApiRepository->getIdentifiantsAdmin($dataIdentifiantsAdmin);
                            if (count($tabIdentifiants) > 0 && $this->ticketId !== null) {
```

Question métier : Point de décision — 'resourceSpecification'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #183 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1491
Contexte   :
```php
                            $dataIdentifiantsAdmin = ['type' => $resourceSpecification, 'nom' => $arg];
                            $tabIdentifiants = $this->globalApiRepository->getIdentifiantsAdmin($dataIdentifiantsAdmin);
                            if (count($tabIdentifiants) > 0 && $this->ticketId !== null) {
                                $replaceValue = $this->app->get('Variable')->getVariableAdminValue($tabIdentifiants, $this->ticketId);
                                if (isset($replaceValue)) {
                                    $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
```

Question métier : Point de décision — count('tabIdentifiants') > 0 et 'this'->ticketId différent de = null. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #184 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1493
Contexte   :
```php
                            if (count($tabIdentifiants) > 0 && $this->ticketId !== null) {
                                $replaceValue = $this->app->get('Variable')->getVariableAdminValue($tabIdentifiants, $this->ticketId);
                                if (isset($replaceValue)) {
                                    $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                                }
                            }
```

Question métier : Point de décision — isset('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #185 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageManuel() — ligne 1525
Contexte   :
```php
        //3349
        if (empty($intervenantInfos) || ($intervenantInfos['TECHNO'] == null || $intervenantInfos['TECHNO'] == '') || (($intervenantInfos['TECHNO'] != null && $intervenantInfos['TECHNO'] != '') && $intervenantInfos['TECHNO'] == $technoComp)) {
            if ($intervenant != 'ORANGE') {
                $this->variableService = $this->app->get('Variable');

                switch ($competence) {
```

Question métier : Point de décision — 'intervenant' différent de 'ORANGE'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #186 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageManuel() — ligne 1557
Contexte   :
```php
        }

        if (is_array($intervenantInfos)) {
            $dataAiguillageManuel['agp_eds'] = key_exists('EDS', $intervenantInfos) ? $intervenantInfos['EDS'] : '';
            $dataAiguillageManuel['selected_eds'] = key_exists('EDS', $intervenantInfos) ? $intervenantInfos['EDS'] : '';
            $dataAiguillageManuel['agp_activation'] = 'EDS ' . $dataAiguillageManuel['agp_eds'];
```

Question métier : Point de décision — is_array('intervenantInfos'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #187 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageManuel() — ligne 1569
Contexte   :
```php
        $dataAiguillageManuel['commentaire'] = $this->aiguillageCommentaireAction($dataAiguillageManuel, $astroData);

        if (!is_null($allEcransValues) && is_array($allEcransValues)) {
            $dataAiguillageManuel['commentaire'] = $this->aiguillageCommentaireRemplaceBloc($dataAiguillageManuel, $allEcransValues);
        }

```

Question métier : Point de décision — !is_null('allEcransValues') et is_array('allEcransValues'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #188 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireRemplaceBloc() — ligne 1587
Contexte   :
```php
        $blocs = OceaneTools::getContents($commentaire, '##bloc_', '##');
        foreach ($blocs as $blocName) {
            if ('Carte_EAN' == $blocName && key_exists('donnee_cartes', $allEcranValuesArray)) {
                $blocDonneeCarte = '<br />';
                foreach ($allEcranValuesArray['donnee_cartes'] as $dataCarte) {
                    $blocVariable = $this->agpGeneriqueRepository->getBlocVariable('Carte_EAN');
```

Question métier : Point de décision — 'Carte_EAN' égal à 'blocName' et key_exists('donnee_cartes', 'allEcranValuesArray'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #189 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireRemplaceBloc() — ligne 1600
Contexte   :
```php
        }
        foreach ($allEcranValuesArray as $keyVariable => $valueVariable) {
            if ($keyVariable != 'donnee_cartes' && $keyVariable != 'CODE_EAN' && $keyVariable != 'Nom_Carte' && $keyVariable != 'Type_Equipement') {
                $commentaire = str_replace('###' . $keyVariable . '###', $valueVariable, $commentaire);
            }
            if ($keyVariable == 'CODE_EAN') {
```

Question métier : Point de décision — 'keyVariable' différent de 'donnee_cartes' et 'keyVariable' différent de 'CODE_EAN' et 'keyVariable' différent de 'Nom_Carte' et 'keyVariable' différent de 'Type_Equipement'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #190 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireRemplaceBloc() — ligne 1603
Contexte   :
```php
                $commentaire = str_replace('###' . $keyVariable . '###', $valueVariable, $commentaire);
            }
            if ($keyVariable == 'CODE_EAN') {
                $blocDonneeVariable = '';
                foreach ($allEcranValuesArray['donnee_cartes'] as $dataCarte) {
                    foreach ($dataCarte as $keyTag => $dataTag) {
```

Question métier : Point de décision — 'keyVariable' égal à 'CODE_EAN'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #191 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireRemplaceBloc() — ligne 1607
Contexte   :
```php
                foreach ($allEcranValuesArray['donnee_cartes'] as $dataCarte) {
                    foreach ($dataCarte as $keyTag => $dataTag) {
                        if ($keyTag == 'CODE_EAN') {
                            $dataVariable = $dataTag;
                        }
                    }
```

Question métier : Point de décision — 'keyTag' égal à 'CODE_EAN'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #192 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireRemplaceBloc() — ligne 1615
Contexte   :
```php
                $commentaire = str_replace("###$keyVariable###", $blocDonneeVariable, $commentaire);
            }
            if ($keyVariable == 'Type_Equipement') {
                $blocDonneeVariable = '';
                foreach ($allEcranValuesArray['donnee_cartes'] as $dataCarte) {
                    foreach ($dataCarte as $keyTag => $dataTag) {
```

Question métier : Point de décision — 'keyVariable' égal à 'Type_Equipement'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #193 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireRemplaceBloc() — ligne 1619
Contexte   :
```php
                foreach ($allEcranValuesArray['donnee_cartes'] as $dataCarte) {
                    foreach ($dataCarte as $keyTag => $dataTag) {
                        if ($keyTag == 'TYPE_EQUIPEMENT') {
                            $dataVariable = $dataTag;
                        }
                    }
```

Question métier : Point de décision — 'keyTag' égal à 'TYPE_EQUIPEMENT'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #194 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireRemplaceBloc() — ligne 1627
Contexte   :
```php
                $commentaire = str_replace("###$keyVariable###", $blocDonneeVariable, $commentaire);
            }
            if ($keyVariable == 'Nom_Carte') {
                $blocDonneeVariable = '';
                foreach ($allEcranValuesArray['donnee_cartes'] as $dataCarte) {
                    foreach ($dataCarte as $keyTag => $dataTag) {
```

Question métier : Point de décision — 'keyVariable' égal à 'Nom_Carte'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #195 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireRemplaceBloc() — ligne 1631
Contexte   :
```php
                foreach ($allEcranValuesArray['donnee_cartes'] as $dataCarte) {
                    foreach ($dataCarte as $keyTag => $dataTag) {
                        if ($keyTag == 'NOM_CARTE') {
                            $dataVariable = $dataTag;
                        }
                    }
```

Question métier : Point de décision — 'keyTag' égal à 'NOM_CARTE'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #196 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireRemplaceBloc() — ligne 1675
Contexte   :
```php
                    $commentaire = str_replace("##bloc_$blocName##", $blocDonneeCarte, $commentaire);
                    foreach ($allEcranValuesArray as $keyVariable2 => $valueVariable2) {
                        if ($keyVariable2 != 'donnee_cartes') {
                            $commentaire = str_replace("###$keyVariable2###", $valueVariable2, $commentaire);
                        }

```

Question métier : Point de décision — 'keyVariable2' différent de 'donnee_cartes'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #197 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireAction() — ligne 1692
Contexte   :
```php
        $isDslamTest = false;

        if ($astroData['type'] == 'DSLAM' || $astroData['type'] == 'DSLAMDERCO') {
            $isDslamTest = true;
        }
        if ($isDslamTest) {
```

Question métier : Point de décision — 'astroData'['type'] égal à 'DSLAM' ou 'astroData'['type'] égal à 'DSLAMDERCO'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #198 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireAction() — ligne 1704
Contexte   :
```php
            $agpCommentaire = $this->agpGeneriqueRepository->getCommentaireByAction($data['idJeuParam'], $data['agp_id_action']);
            $data['id_valeur'] = $agpCommentaire['ID_COMMENTAIRE'];
            if (key_exists('intervenant', $data) && $data['intervenant'] != '') {
                $segComment = $this->app->get('AdminCommentaireRepository')->getCommentaireSecondaireByIntervenant($data);
                if (is_array($segComment) && isset($segComment['SECOND_COMMENT']) && trim($segComment['SECOND_COMMENT']) !== '') {
                    $agpCommentaire['COMMENTAIRE'] = $segComment['SECOND_COMMENT'];
```

Question métier : Point de décision — key_exists('intervenant', 'data') et 'data'['intervenant'] différent de ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #199 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireAction() — ligne 1706
Contexte   :
```php
            if (key_exists('intervenant', $data) && $data['intervenant'] != '') {
                $segComment = $this->app->get('AdminCommentaireRepository')->getCommentaireSecondaireByIntervenant($data);
                if (is_array($segComment) && isset($segComment['SECOND_COMMENT']) && trim($segComment['SECOND_COMMENT']) !== '') {
                    $agpCommentaire['COMMENTAIRE'] = $segComment['SECOND_COMMENT'];
                }
            }
```

Question métier : Point de décision — is_array('segComment') et isset('segComment'['SECOND_COMMENT']) et trim('segComment'['SECOND_COMMENT']) différent de = ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #200 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1() — ligne 237
Contexte   :
```php
            foreach ($deports as $v) {
                $maitreDeport = $this->edrService->getDataMaitreDeport($v, false);
                if ($maitreDeport['status'] == 'ok') {
                    $tDeports[$maitreDeport['id_rsc']] = $v;
                }
            }
```

Question métier : Valeur de référence non documentée — La décision « 'maitreDeport'['status'] égal à 'ok' » repose sur la valeur 'ok'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #201 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1() — ligne 248
Contexte   :
```php
            $maitreDeport = $this->edrService->getDataMaitreDeport($master, false);
            $idRscMaster = $maitreDeport['id_rsc'];
            if ($maitreDeport['status'] == 'nok') {
                $hMaster = $this->interventionHelper->getHMaster($master, true, $droitEds['guest']);
            } else {
                $hMaster = $this->interventionHelper->getHMaster($master, false, $droitEds['guest']);
```

Question métier : Valeur de référence non documentée — La décision « 'maitreDeport'['status'] égal à 'nok' » repose sur la valeur 'nok'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #202 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1Generique() — ligne 578
Contexte   :
```php
                foreach ($deports as $v) {
                    $maitreDeport = $this->edrService->getDataMaitreDeport($v, false);
                    if ($maitreDeport['status'] == 'ok') {
                        $tDeports[$maitreDeport['id_rsc']] = $v;
                    }
                }
```

Question métier : Valeur de référence non documentée — La décision « 'maitreDeport'['status'] égal à 'ok' » repose sur la valeur 'ok'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #203 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1Generique() — ligne 589
Contexte   :
```php
                $maitreDeport = $this->edrService->getDataMaitreDeport($master, false);
                $idRscMaster = $maitreDeport['id_rsc'];
                if ($maitreDeport['status'] == 'nok') {
                    $hMaster = $this->interventionHelper->getHMaster($master, true, $droitEds['guest']);
                } else {
                    $hMaster = $this->interventionHelper->getHMaster($master, false, $droitEds['guest']);
```

Question métier : Valeur de référence non documentée — La décision « 'maitreDeport'['status'] égal à 'nok' » repose sur la valeur 'nok'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #204 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayPiloterGenerique() — ligne 777
Contexte   :
```php
        if (!empty($blocs) && key_exists(0, $blocs)) {
            foreach ($blocs as $blocName) {
                if ($blocName != 'choix_de_carte_trans' && $blocName != 'Types_Carte' && $blocName != 'Types' && $blocName != 'Carte_EAN' && $blocName != 'Complet') {
                    $blocVariable = $this->agpGeneriqueRepository->getBlocVariable($blocName);
                    $commentaire = str_replace('##bloc_' . $blocName . '##', $blocVariable, $commentaire);
                }
```

Question métier : Valeur de référence non documentée — La décision « 'blocName' différent de 'choix_de_carte_trans' et 'blocName' différent de 'Types_Carte' et 'blocName' différent de 'Types' et 'blocName' différent de 'Carte_EAN' et 'blocName' différent de 'Complet' » repose sur la valeur 'choix_de_carte_trans'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #205 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : checkActionInput() — ligne 1017
Contexte   :
```php
        $carteArray = array("dslam", "master", "deport");

        if (in_array($input, $carteArray) || (($input == 'alarme') && ($hasChassis == 'false'))) {
            return 517;
        } else {
            return 518;
```

Question métier : Valeur de référence non documentée — La décision « in_array('input', 'carteArray') ou (('input' égal à 'alarme') et ('hasChassis' égal à 'false')) » repose sur la valeur 'alarme'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #206 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : checkActionInput() — ligne 1017
Contexte   :
```php
        $carteArray = array("dslam", "master", "deport");

        if (in_array($input, $carteArray) || (($input == 'alarme') && ($hasChassis == 'false'))) {
            return 517;
        } else {
            return 518;
```

Question métier : Valeur de référence non documentée — La décision « in_array('input', 'carteArray') ou (('input' égal à 'alarme') et ('hasChassis' égal à 'false')) » repose sur la valeur 'false'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #207 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1379
Contexte   :
```php
                    break;
                case 'Etat_batterie':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {

                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['mode_fonctionnement_batterie'], $chaine);
```

Question métier : Valeur de référence non documentée — La décision « key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok' » repose sur la valeur 'ok'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #208 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1387
Contexte   :
```php
                    break;
                case 'Element_HS':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {
                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['element_equipement_panne_tronc'], $chaine);
                    }
```

Question métier : Valeur de référence non documentée — La décision « key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok' » repose sur la valeur 'ok'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #209 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1394
Contexte   :
```php
                    break;
                case 'Tension_batterie':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {
                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['tension'], $chaine);
                    }
```

Question métier : Valeur de référence non documentée — La décision « key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok' » repose sur la valeur 'ok'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #210 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1401
Contexte   :
```php
                    break;
                case 'Temperature':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {
                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['temperature'], $chaine);
                    }
```

Question métier : Valeur de référence non documentée — La décision « key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok' » repose sur la valeur 'ok'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #211 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1466
Contexte   :
```php
                    $replaceValue = $this->refSiteRepository->getRefsiteColumn($arrayRefSite[$arg], $this->ticketId);

                    if (OceaneTools::isValidVariable($replaceValue) && gettype($replaceValue) != 'boolean') {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
```

Question métier : Valeur de référence non documentée — La décision « OceaneTools::isValidVariable('replaceValue') et gettype('replaceValue') différent de 'boolean' » repose sur la valeur 'boolean'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #212 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireRemplaceBloc() — ligne 1600
Contexte   :
```php
        }
        foreach ($allEcranValuesArray as $keyVariable => $valueVariable) {
            if ($keyVariable != 'donnee_cartes' && $keyVariable != 'CODE_EAN' && $keyVariable != 'Nom_Carte' && $keyVariable != 'Type_Equipement') {
                $commentaire = str_replace('###' . $keyVariable . '###', $valueVariable, $commentaire);
            }
            if ($keyVariable == 'CODE_EAN') {
```

Question métier : Valeur de référence non documentée — La décision « 'keyVariable' différent de 'donnee_cartes' et 'keyVariable' différent de 'CODE_EAN' et 'keyVariable' différent de 'Nom_Carte' et 'keyVariable' différent de 'Type_Equipement' » repose sur la valeur 'donnee_cartes'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #213 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireRemplaceBloc() — ligne 1642
Contexte   :
```php
            foreach ($blocs as $blocName) {

                if ($keyVariable == 'donnee_cartes' && !empty($blocs) && $blocName == 'choix_de_carte_trans') {
                    // Remplacer bloc_choix_de_carte_trans par les donnes des cartes selection?es
                    $blocDonneeCarte = '';
                    foreach ($valueVariable as $dataCarte) {
```

Question métier : Valeur de référence non documentée — La décision « $keyVariable == 'donnee_cartes' && !le champ 'blocs' est vide && $blocName == 'choix_de_carte_trans' » repose sur la valeur 'donnee_cartes'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #214 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireRemplaceBloc() — ligne 1642
Contexte   :
```php
            foreach ($blocs as $blocName) {

                if ($keyVariable == 'donnee_cartes' && !empty($blocs) && $blocName == 'choix_de_carte_trans') {
                    // Remplacer bloc_choix_de_carte_trans par les donnes des cartes selection?es
                    $blocDonneeCarte = '';
                    foreach ($valueVariable as $dataCarte) {
```

Question métier : Valeur de référence non documentée — La décision « $keyVariable == 'donnee_cartes' && !le champ 'blocs' est vide && $blocName == 'choix_de_carte_trans' » repose sur la valeur 'choix_de_carte_trans'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #215 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireRemplaceBloc() — ligne 1649
Contexte   :
```php

                        foreach ($dataCarte as $keyTag => $dataTag) {
                            if ($keyTag == 'ean') {
                                if ($dataTag == 'True') {
                                    $blocVariable = str_replace('###crochet_ouvrant###', '[', $blocVariable);
                                    $blocVariable = str_replace('###crochet_fermant###', ']', $blocVariable);
```

Question métier : Valeur de référence non documentée — La décision « 'keyTag' égal à 'ean' » repose sur la valeur 'ean'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #216 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireRemplaceBloc() — ligne 1675
Contexte   :
```php
                    $commentaire = str_replace("##bloc_$blocName##", $blocDonneeCarte, $commentaire);
                    foreach ($allEcranValuesArray as $keyVariable2 => $valueVariable2) {
                        if ($keyVariable2 != 'donnee_cartes') {
                            $commentaire = str_replace("###$keyVariable2###", $valueVariable2, $commentaire);
                        }

```

Question métier : Valeur de référence non documentée — La décision « 'keyVariable2' différent de 'donnee_cartes' » repose sur la valeur 'donnee_cartes'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #254 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1() — ligne 237
Contexte   :
```php
                if ($maitreDeport['status'] == 'ok') {
                    $tDeports[$maitreDeport['id_rsc']] = $v;
                }
            }
            $hDeports .= $this->interventionHelper->getDeports($tDeports, 'agp_deport', '90', '', 'choisir', $droitEds['guest']);
```

Question métier : Le code situation 'ok' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #255 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1() — ligne 248
Contexte   :
```php
            if ($maitreDeport['status'] == 'nok') {
                $hMaster = $this->interventionHelper->getHMaster($master, true, $droitEds['guest']);
            } else {
                $hMaster = $this->interventionHelper->getHMaster($master, false, $droitEds['guest']);
            }
```

Question métier : Le code situation 'nok' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #256 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1() — ligne 273
Contexte   :
```php
        if ($typeRessource == 'DSLAM') {
            $demandeInterventionForm = new DemandeInterventionForm(null, array(
                'app' => $this->app,
                'agp_entite' => $agpEds,
                'agp_id_astro' => $astroId,
```

Question métier : Le code situation 'DSLAM' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #257 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1Generique() — ligne 531
Contexte   :
```php
        if ($typeRessource == 'DSLAM') {
            $idRscMaster = '';
            $dslam = '';
            $helper = new Edr();
            $hDeports = '';
```

Question métier : Le code situation 'DSLAM' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #258 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1Generique() — ligne 578
Contexte   :
```php
                    if ($maitreDeport['status'] == 'ok') {
                        $tDeports[$maitreDeport['id_rsc']] = $v;
                    }
                }
                $hDeports .= $this->interventionHelper->getDeports($tDeports, 'agp_deport', '90', '', 'choisir', $droitEds['guest']);
```

Question métier : Le code situation 'ok' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #259 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1Generique() — ligne 589
Contexte   :
```php
                if ($maitreDeport['status'] == 'nok') {
                    $hMaster = $this->interventionHelper->getHMaster($master, true, $droitEds['guest']);
                } else {
                    $hMaster = $this->interventionHelper->getHMaster($master, false, $droitEds['guest']);
                }
```

Question métier : Le code situation 'nok' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #260 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1Generique() — ligne 606
Contexte   :
```php
        if ($typeRessource == 'MIE') {
            $args[] = 'FG_NOMNAEQP';

        }

```

Question métier : Le code situation 'MIE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #261 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1Generique() — ligne 611
Contexte   :
```php
        if ($typeRessource == 'SLN' || $typeRessource == 'WDM_SID') {
            $args[] = 'FG_E1NOMNAEQP';

            $args[] = 'FG_E2NOMNAEQP';
        }
```

Question métier : Le code situation 'SLN' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #262 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp1Generique() — ligne 611
Contexte   :
```php
        if ($typeRessource == 'SLN' || $typeRessource == 'WDM_SID') {
            $args[] = 'FG_E1NOMNAEQP';

            $args[] = 'FG_E2NOMNAEQP';
        }
```

Question métier : Le code situation 'WDM_SID' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #263 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : getOptionsActionsGenerique() — ligne 708
Contexte   :
```php
        if ($typeRessource == 'COMMUT' || $typeRessource == 'UNIRACC' || $typeRessource == 'CONNUM' || $typeRessource == 'MICBPNCSN' || $typeRessource == 'MICBPNCAA' || $typeRessource == 'MICBPNCOM') {
            $this->commutationRessource = $this->app->get('CommutationRessource');
            $filtre = $this->commutationRessource->varSystemeCommut($identifiants, $typeRessource);
        }
        if (($typeRessource == 'DSLAM' || $typeRessource == 'DSLAMDERCO') && $data['id_rsc'] != '' && $data['id_rsc_dslam'] != '') {
```

Question métier : Le code situation 'COMMUT' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #264 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : getOptionsActionsGenerique() — ligne 708
Contexte   :
```php
        if ($typeRessource == 'COMMUT' || $typeRessource == 'UNIRACC' || $typeRessource == 'CONNUM' || $typeRessource == 'MICBPNCSN' || $typeRessource == 'MICBPNCAA' || $typeRessource == 'MICBPNCOM') {
            $this->commutationRessource = $this->app->get('CommutationRessource');
            $filtre = $this->commutationRessource->varSystemeCommut($identifiants, $typeRessource);
        }
        if (($typeRessource == 'DSLAM' || $typeRessource == 'DSLAMDERCO') && $data['id_rsc'] != '' && $data['id_rsc_dslam'] != '') {
```

Question métier : Le code situation 'UNIRACC' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #265 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : getOptionsActionsGenerique() — ligne 708
Contexte   :
```php
        if ($typeRessource == 'COMMUT' || $typeRessource == 'UNIRACC' || $typeRessource == 'CONNUM' || $typeRessource == 'MICBPNCSN' || $typeRessource == 'MICBPNCAA' || $typeRessource == 'MICBPNCOM') {
            $this->commutationRessource = $this->app->get('CommutationRessource');
            $filtre = $this->commutationRessource->varSystemeCommut($identifiants, $typeRessource);
        }
        if (($typeRessource == 'DSLAM' || $typeRessource == 'DSLAMDERCO') && $data['id_rsc'] != '' && $data['id_rsc_dslam'] != '') {
```

Question métier : Le code situation 'CONNUM' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #266 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : getOptionsActionsGenerique() — ligne 712
Contexte   :
```php
        if (($typeRessource == 'DSLAM' || $typeRessource == 'DSLAMDERCO') && $data['id_rsc'] != '' && $data['id_rsc_dslam'] != '') {
            $idRsc = $data['id_rsc'];
            $dataEdr = $this->edrRepository->getBlobDslam($data['id_rsc_dslam'])['BLOBDATA'];
            $ressource = $this->astroRepository->getRessource($data['id_rsc_dslam'] != $data['id_rsc'] ? $data['id_rsc'] : $data['id_rsc_dslam']);
            $ressource = is_array($ressource) && key_exists('DSLAM', $ressource) ? $ressource['DSLAM'] : '';
```

Question métier : Le code situation 'DSLAM' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #267 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayPiloterGenerique() — ligne 748
Contexte   :
```php
                if ($data['agp_ho_hno_generique'] == 'HO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_ho'] == '1') {
                    $agpSuivreHno = 0;
                } elseif ($data['agp_ho_hno_generique'] == 'HNO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_hno'] == '1') {
                    $agpSuivreHno = 1;
                }
```

Question métier : Le code situation 'HO' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #268 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayPiloterGenerique() — ligne 748
Contexte   :
```php
                if ($data['agp_ho_hno_generique'] == 'HO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_ho'] == '1') {
                    $agpSuivreHno = 0;
                } elseif ($data['agp_ho_hno_generique'] == 'HNO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_hno'] == '1') {
                    $agpSuivreHno = 1;
                }
```

Question métier : Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #269 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayPiloterGenerique() — ligne 750
Contexte   :
```php
                } elseif ($data['agp_ho_hno_generique'] == 'HNO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_hno'] == '1') {
                    $agpSuivreHno = 1;
                }
            }
        }
```

Question métier : Le code situation 'HNO' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #270 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayPiloterGenerique() — ligne 783
Contexte   :
```php
        if (is_string($data['id_commentaire']) && $data['id_commentaire'] == 'DiagSDH') {
            $accessNumber = $this->diagSdh->getAccessNumber($astroSession);
            $diagSdhData = $this->diagSdh->getDiagSdhInfos($accessNumber);
            $commentaire = is_array($diagSdhData) && !key_exists('message', $diagSdhData) ? $this->diagSdh->getCommentaireCharteActivationUiTicket($diagSdhData) : '';

```

Question métier : Le code situation 'DiagSDH' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #271 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 859
Contexte   :
```php
                if ($data['agp_ho_hno_generique'] == 'HO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_ho'] == '1') {
                    $agpSuivreHno = 0;
                } elseif ($data['agp_ho_hno_generique'] == 'HNO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_hno'] == '1') {
                    $agpSuivreHno = 1;
                }
```

Question métier : Le code situation 'HO' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #272 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 859
Contexte   :
```php
                if ($data['agp_ho_hno_generique'] == 'HO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_ho'] == '1') {
                    $agpSuivreHno = 0;
                } elseif ($data['agp_ho_hno_generique'] == 'HNO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_hno'] == '1') {
                    $agpSuivreHno = 1;
                }
```

Question métier : Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #273 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 861
Contexte   :
```php
                } elseif ($data['agp_ho_hno_generique'] == 'HNO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_hno'] == '1') {
                    $agpSuivreHno = 1;
                }
            }
        }
```

Question métier : Le code situation 'HNO' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #274 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 904
Contexte   :
```php
            if ($data['type_ressource'] == 'DSLAM' || $data['type_ressource'] == 'DSLAMDERCO') {
                $isDslamTest = true;
            }
            $astroSession['type'] = $data['type_ressource'];
            $astroSession['ticketid'] = $ticketId;
```

Question métier : Le code situation 'DSLAM' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #275 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayAgp2Generique() — ligne 929
Contexte   :
```php
        if (is_string($data['id_commentaire']) && $data['id_commentaire'] == 'DiagSDH') {
            $astroSession['class'] = $oceaneData['class'];
            $astroSession['id1'] = $oceaneData['id1'];
            $astroSession['id2'] = $oceaneData['id2'];
            $astroSession['id3'] = $oceaneData['id3'];
```

Question métier : Le code situation 'DiagSDH' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #276 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : checkActionInput() — ligne 1017
Contexte   :
```php
        if (in_array($input, $carteArray) || (($input == 'alarme') && ($hasChassis == 'false'))) {
            return 517;
        } else {
            return 518;
        }
```

Question métier : Le code situation 'alarme' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #277 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : checkActionInput() — ligne 1017
Contexte   :
```php
        if (in_array($input, $carteArray) || (($input == 'alarme') && ($hasChassis == 'false'))) {
            return 517;
        } else {
            return 518;
        }
```

Question métier : Le code situation 'false' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #278 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayCreationTocTrans() — ligne 1087
Contexte   :
```php
            if ($data['type'] == 'TRCCABLE' || $data['type'] == 'TRONCABLE' || $data['type'] == 'CABLE') {
                $assembleeNiveauUn = $this->airele->getDataTronconNiveauUn($astroSession ['id3']);
                usort($assembleeNiveauUn, function ($a, $b) {
                    return (int)$a['fibre'] > (int)$b['fibre'];
                });
```

Question métier : Le code situation 'TRCCABLE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #279 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayCreationTocTrans() — ligne 1087
Contexte   :
```php
            if ($data['type'] == 'TRCCABLE' || $data['type'] == 'TRONCABLE' || $data['type'] == 'CABLE') {
                $assembleeNiveauUn = $this->airele->getDataTronconNiveauUn($astroSession ['id3']);
                usort($assembleeNiveauUn, function ($a, $b) {
                    return (int)$a['fibre'] > (int)$b['fibre'];
                });
```

Question métier : Le code situation 'CABLE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #280 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayCreationTocTrans() — ligne 1093
Contexte   :
```php
            if ($data['type'] == 'SDH' || $data['type'] == 'SLN' || $data['type'] == 'PDH' || $data['type'] == 'ETH' || $data['type'] == 'OCH' || $data['type'] == 'WDM_SID') {
                $assembleeNiveauUn = $this->airele->getDataAssembleeNiveauUn($assemblee, $sessionId, $ticketId);
            }
            if ($data['type'] == 'MIE') {
                $nomEqpt1 = $this->getOceane->getTicketParamsAttribute('Parameter', 'NOMEQPT1');
```

Question métier : Le code situation 'SDH' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #281 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayCreationTocTrans() — ligne 1093
Contexte   :
```php
            if ($data['type'] == 'SDH' || $data['type'] == 'SLN' || $data['type'] == 'PDH' || $data['type'] == 'ETH' || $data['type'] == 'OCH' || $data['type'] == 'WDM_SID') {
                $assembleeNiveauUn = $this->airele->getDataAssembleeNiveauUn($assemblee, $sessionId, $ticketId);
            }
            if ($data['type'] == 'MIE') {
                $nomEqpt1 = $this->getOceane->getTicketParamsAttribute('Parameter', 'NOMEQPT1');
```

Question métier : Le code situation 'SLN' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #282 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayCreationTocTrans() — ligne 1093
Contexte   :
```php
            if ($data['type'] == 'SDH' || $data['type'] == 'SLN' || $data['type'] == 'PDH' || $data['type'] == 'ETH' || $data['type'] == 'OCH' || $data['type'] == 'WDM_SID') {
                $assembleeNiveauUn = $this->airele->getDataAssembleeNiveauUn($assemblee, $sessionId, $ticketId);
            }
            if ($data['type'] == 'MIE') {
                $nomEqpt1 = $this->getOceane->getTicketParamsAttribute('Parameter', 'NOMEQPT1');
```

Question métier : Le code situation 'PDH' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #283 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayCreationTocTrans() — ligne 1093
Contexte   :
```php
            if ($data['type'] == 'SDH' || $data['type'] == 'SLN' || $data['type'] == 'PDH' || $data['type'] == 'ETH' || $data['type'] == 'OCH' || $data['type'] == 'WDM_SID') {
                $assembleeNiveauUn = $this->airele->getDataAssembleeNiveauUn($assemblee, $sessionId, $ticketId);
            }
            if ($data['type'] == 'MIE') {
                $nomEqpt1 = $this->getOceane->getTicketParamsAttribute('Parameter', 'NOMEQPT1');
```

Question métier : Le code situation 'ETH' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #284 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayCreationTocTrans() — ligne 1093
Contexte   :
```php
            if ($data['type'] == 'SDH' || $data['type'] == 'SLN' || $data['type'] == 'PDH' || $data['type'] == 'ETH' || $data['type'] == 'OCH' || $data['type'] == 'WDM_SID') {
                $assembleeNiveauUn = $this->airele->getDataAssembleeNiveauUn($assemblee, $sessionId, $ticketId);
            }
            if ($data['type'] == 'MIE') {
                $nomEqpt1 = $this->getOceane->getTicketParamsAttribute('Parameter', 'NOMEQPT1');
```

Question métier : Le code situation 'OCH' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #285 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayCreationTocTrans() — ligne 1093
Contexte   :
```php
            if ($data['type'] == 'SDH' || $data['type'] == 'SLN' || $data['type'] == 'PDH' || $data['type'] == 'ETH' || $data['type'] == 'OCH' || $data['type'] == 'WDM_SID') {
                $assembleeNiveauUn = $this->airele->getDataAssembleeNiveauUn($assemblee, $sessionId, $ticketId);
            }
            if ($data['type'] == 'MIE') {
                $nomEqpt1 = $this->getOceane->getTicketParamsAttribute('Parameter', 'NOMEQPT1');
```

Question métier : Le code situation 'WDM_SID' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #286 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : displayCreationTocTrans() — ligne 1096
Contexte   :
```php
            if ($data['type'] == 'MIE') {
                $nomEqpt1 = $this->getOceane->getTicketParamsAttribute('Parameter', 'NOMEQPT1');
                $assembleeNiveauUn = $this->airele->getDataAssembleeNiveauUn($nomEqpt1, $sessionId, $ticketId);
            }
            // Création du formulaire avec les données récupérées
```

Question métier : Le code situation 'MIE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #287 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : replaceTagsChaineEnchainement() — ligne 1379
Contexte   :
```php
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {

                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['mode_fonctionnement_batterie'], $chaine);
                    }
```

Question métier : Le code situation 'ok' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #288 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireRemplaceBloc() — ligne 1603
Contexte   :
```php
            if ($keyVariable == 'CODE_EAN') {
                $blocDonneeVariable = '';
                foreach ($allEcranValuesArray['donnee_cartes'] as $dataCarte) {
                    foreach ($dataCarte as $keyTag => $dataTag) {
                        if ($keyTag == 'CODE_EAN') {
```

Question métier : Le code situation 'CODE_EAN' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #289 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireRemplaceBloc() — ligne 1649
Contexte   :
```php
                            if ($keyTag == 'ean') {
                                if ($dataTag == 'True') {
                                    $blocVariable = str_replace('###crochet_ouvrant###', '[', $blocVariable);
                                    $blocVariable = str_replace('###crochet_fermant###', ']', $blocVariable);
                                } else {
```

Question métier : Le code situation 'ean' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #290 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireRemplaceBloc() — ligne 1650
Contexte   :
```php
                                if ($dataTag == 'True') {
                                    $blocVariable = str_replace('###crochet_ouvrant###', '[', $blocVariable);
                                    $blocVariable = str_replace('###crochet_fermant###', ']', $blocVariable);
                                } else {
                                    $blocVariable = str_replace('###crochet_ouvrant###', '', $blocVariable);
```

Question métier : Le code situation 'True' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #291 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireRemplaceBloc() — ligne 1665
Contexte   :
```php
                } elseif ($keyVariable != 'donnee_cartes' && !empty($blocs) && ($blocName == 'defaut_constate_trans' || $blocName == 'action_a_realiser_trans' || $blocName == 'Types_Carte' || $blocName == 'Types' || $blocName == 'Carte_EAN' || $blocName == 'Complet')) {
                    // Remplacer bloc par les donnes des cartes selection?es
                    $blocDonneeCarte = '';

                    $blocVariable = $this->agpGeneriqueRepository->getBlocVariable($blocName);
```

Question métier : Le code situation 'Types' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #292 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireRemplaceBloc() — ligne 1665
Contexte   :
```php
                } elseif ($keyVariable != 'donnee_cartes' && !empty($blocs) && ($blocName == 'defaut_constate_trans' || $blocName == 'action_a_realiser_trans' || $blocName == 'Types_Carte' || $blocName == 'Types' || $blocName == 'Carte_EAN' || $blocName == 'Complet')) {
                    // Remplacer bloc par les donnes des cartes selection?es
                    $blocDonneeCarte = '';

                    $blocVariable = $this->agpGeneriqueRepository->getBlocVariable($blocName);
```

Question métier : Le code situation 'Complet' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #293 — Agp**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaireAction() — ligne 1692
Contexte   :
```php
        if ($astroData['type'] == 'DSLAM' || $astroData['type'] == 'DSLAMDERCO') {
            $isDslamTest = true;
        }
        if ($isDslamTest) {
            $data['idJeu'] = $data['idJeuParam'];
```

Question métier : Le code situation 'DSLAM' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #294 — AiguillageIntervenant**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : getIntervenantInfos() — ligne 48
Contexte   :
```php
        $ok = true;

        if (empty($intervenantInfosList)) {
            return $intervenantInfosList;
        }
        foreach ($intervenantInfosList as $intervenantInfos) {
```

Question métier : Point de décision — le champ 'intervenantInfosList' est vide. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #295 — AiguillageIntervenant**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : getIntervenantInfos() — ligne 62
Contexte   :
```php
                    switch ($intervenantInfos['CONDITION']) {
                        case 'begin_with':
                            if (strpos($checkVar, $val) === 0) $ok = true;
                            break;
                        case 'equal':
                            if (strcmp($checkVar, $val) === 0) $ok = true;///valeurs admin case Sensitive
```

Question métier : Point de décision — strpos('checkVar', 'val') égal à = 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #296 — AiguillageIntervenant**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : getIntervenantInfos() — ligne 65
Contexte   :
```php
                            break;
                        case 'equal':
                            if (strcmp($checkVar, $val) === 0) $ok = true;///valeurs admin case Sensitive
                            break;
                        case 'contains':
                            if (strpos($checkVar, $val) !== false) $ok = true;
```

Question métier : Point de décision — strcmp('checkVar', 'val') égal à = 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #297 — AiguillageIntervenant**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : getIntervenantInfos() — ligne 68
Contexte   :
```php
                            break;
                        case 'contains':
                            if (strpos($checkVar, $val) !== false) $ok = true;
                            break;
                        case '':
                            $ok = true;
```

Question métier : Point de décision — strpos('checkVar', 'val') différent de = false. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #298 — AiguillageIntervenant**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : getIntervenantInfos() — ligne 75
Contexte   :
```php

                    }
                    if ($ok) break;

                }
            } elseif ($intervenantInfos['VARIABLE_ADMIN'] != '* Variables *' && (is_null($intervenantInfos['CONDITION']) || is_null($intervenantInfos['VALEUR_CONDITION']))) {
```

Question métier : Point de décision — 'ok'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #299 — AiguillageIntervenant**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : getIntervenantInfos() — ligne 85
Contexte   :
```php
                $ok = true;
            }
            if (!is_null($intervenantInfos['TECHNO']) && $intervenantInfos['TECHNO'] != '' && $ok) {
                switch ($typeRessource) {
                    case 'CA-CASW':
                    case 'S-SUP':
```

Question métier : Point de décision — !is_null('intervenantInfos'['TECHNO']) et 'intervenantInfos'['TECHNO'] différent de '' et 'ok'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #300 — AiguillageIntervenant**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : getIntervenantInfos() — ligne 134
Contexte   :
```php
                }
            }
            if($ok) {
                return array(
                    'ID_AIGUILLAGE' => $intervenantInfos['ID'],
                    'EDS' => $intervenantInfos['EDS'],
```

Question métier : Point de décision — 'ok'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #302 — AiguillageIntervenant**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : getIntervenantInfos() — ligne 92
Contexte   :
```php
                        $ok = ($intervenantInfos['TECHNO'] == 'EVTFIXE');
                        break;
                    case 'DSLAM':
                    case 'ROUTEURGE':
                    case 'SWTIP':
```

Question métier : Le code situation 'EVTFIXE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #303 — AiguillageIntervenant**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : getIntervenantInfos() — ligne 103
Contexte   :
```php
                        $ok = ($intervenantInfos['TECHNO'] == 'RS');
                        break;
                    case 'WDM_SID':
                    case 'SLN':
                    case 'SDH':
```

Question métier : Le code situation 'RS' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #304 — AiguillageIntervenant**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : getIntervenantInfos() — ligne 109
Contexte   :
```php
                        if ($typeRessource == 'MIE') {
                            $extremiteTechno = 'TECHNO';
                        } else {
                            if ($ext == 'tabs_action_ext1') {
                                $extremiteTechno = 'EXT1_TECHNO';
```

Question métier : Le code situation 'MIE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #305 — AiguillageIntervenant**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : getIntervenantInfos() — ligne 122
Contexte   :
```php
                        if ($techno == 'FH') {
                            // FH
                            $ok = ($intervenantInfos['TECHNO'] == 'FH');
                        } else {
                            // RS
```

Question métier : Le code situation 'FH' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #306 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : initApi() — ligne 125
Contexte   :
```php
                $userData = $this->ihmUserRepository->getByLogin($cuidLow);

                if ($userData && is_array($userData) && !key_exists('message', $userData)) {
                    $idUser = $userData['ID_UTILISATEUR'];
                }
                //URL DATA
```

Question métier : Point de décision — 'userData' et is_array('userData') et !key_exists('message', 'userData'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #307 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : createTicket() — ligne 227
Contexte   :
```php
    {
        $idJeuParam = '';
        if ($data['type_ressource'] == 'DSLAM') {
            $ressource = $this->oceaneAssistant->detailMateriel($data['ressource'], $data['type_ressource_iadr'], $data['code_detecteur'], $data['description'], $data['id1']);
            $idRessource = $this->astroRepository->createRessource($ressource);
            $data['id_ressource'] = $idRessource;
```

Question métier : Point de décision — 'data'['type_ressource'] égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #308 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : createTicket() — ligne 233
Contexte   :
```php
        }

        if ($data['evt_incident'] == '64') {
            $idJeuParam = $this->astroRepository->getJeuParamByBandeauFonction($data['bandeau_id'], 'ABONDONNER');
        }
        $data['id_jeu_param'] = $idJeuParam;
```

Question métier : Point de décision — 'data'['evt_incident'] égal à '64'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #309 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : createTicket() — ligne 240
Contexte   :
```php
        $astroId = $this->astroRepository->getAstroIdByTicket($data['ticketoceaneid']);

        if ($data['type_ressource'] == 'DSLAM') {
            // Si autre chose qu'un DSLAM, on doit créer la ressource du DSLAM uniquement
            if ($ressource['ID_TYPE_RESSOURCE'] != '1' && $ressource['ID_TYPE_RESSOURCE'] != '9') {
                $inj['ID_TYPE_RESSOURCE'] = '1';
```

Question métier : Point de décision — 'data'['type_ressource'] égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #310 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : createTicket() — ligne 242
Contexte   :
```php
        if ($data['type_ressource'] == 'DSLAM') {
            // Si autre chose qu'un DSLAM, on doit créer la ressource du DSLAM uniquement
            if ($ressource['ID_TYPE_RESSOURCE'] != '1' && $ressource['ID_TYPE_RESSOURCE'] != '9') {
                $inj['ID_TYPE_RESSOURCE'] = '1';
                $inj['DSLAM'] = $ressource['DSLAM'];
                $idRessourceDslam = $this->astroRepository->createRessource($inj);
```

Question métier : Point de décision — 'ressource'['ID_TYPE_RESSOURCE'] différent de '1' et 'ressource'['ID_TYPE_RESSOURCE'] différent de '9'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #311 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : callEnchainementMethd() — ligne 263
Contexte   :
```php
        $astroId = $this->astroRepository->getAstroIdByTicket($idTicket);
        $message = new Message($this->app, $astroId, $this->messageFile, $this->sessId);
        if ($enchainement == 'TRAITEMENT_ALARME_ADSL') {
            $checkIfTAADSL = true;
            $dataAuto = $this->app->get('AutomatisationRepository')->getCodeAndEnchainementAutomaisation($codeDetecteur);
            $enchainement = $dataAuto['ENCHAINEMENT'];
```

Question métier : Point de décision — 'enchainement' égal à 'TRAITEMENT_ALARME_ADSL'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #312 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : callEnchainementMethd() — ligne 273
Contexte   :
```php
                $this->updateDateActionEnCoursEds($idTicket, $connectedGroup);
                $preRequis = $this->checkPreRequirementEnchainement($idTicket, $enchainement, $connectedGroup);
                if (!$preRequis) {
                    $message->setMessageComplexe("E_AUTOMATE_ENCHAINEMENT", array('###DETAIL###' => "ECHEC AUTOMATE : l'état actuel du ticket ne permet pas le lancement de l'enchaînement"));
                    $preRequirementException = new PreRequirementException();
                    return $preRequirementException();
```

Question métier : Point de décision — !'preRequis'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #313 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : callEnchainementMethd() — ligne 284
Contexte   :
```php
                $this->updateDateActionEnCoursEds($idTicket, $connectedGroup);
                $preRequis = $this->checkPreRequirementEnchainement($idTicket, $enchainement, $connectedGroup);
                if (!$preRequis) {
                    $message->setMessageComplexe("E_AUTOMATE_ENCHAINEMENT", array('###DETAIL###' => "ECHEC AUTOMATE : l'état actuel du ticket ne permet pas le lancement de l'enchaînement"));
                    $preRequirementException = new PreRequirementException();
                    return $preRequirementException();
```

Question métier : Point de décision — !'preRequis'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #314 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : callEnchainementMethd() — ligne 304
Contexte   :
```php
                $this->updateDateActionEnCoursEds($idTicket, $connectedGroup);
                $preRequis = $this->checkPreRequirementEnchainement($idTicket, $enchainement, $connectedGroup);
                if (!$preRequis) {
                    $message->setMessageComplexe("E_AUTOMATE_ENCHAINEMENT", array('###DETAIL###' => "ECHEC AUTOMATE : l'état actuel du ticket ne permet pas le lancement de l'enchaînement"));
                    $preRequirementException = new PreRequirementException();
                    return $preRequirementException();
```

Question métier : Point de décision — !'preRequis'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #315 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : callEnchainementMethd() — ligne 315
Contexte   :
```php
                $this->updateDateActionEnCoursEds($idTicket, $connectedGroup);
                $preRequis = $this->checkPreRequirementEnchainement($idTicket, $enchainement, $connectedGroup);
                if (!$preRequis) {
                    $message->setMessageComplexe("E_AUTOMATE_ENCHAINEMENT", array('###DETAIL###' => "ECHEC AUTOMATE : l'état actuel du ticket ne permet pas le lancement de l'enchaînement"));
                    $preRequirementException = new PreRequirementException();
                    return $preRequirementException();
```

Question métier : Point de décision — !'preRequis'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #316 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : callEnchainementMethd() — ligne 326
Contexte   :
```php
                $this->updateDateActionEnCoursEds($idTicket, $connectedGroup);
                $preRequis = $this->checkPreRequirementEnchainement($idTicket, $enchainement, $connectedGroup);
                if (!$preRequis) {
                    $message->setMessageComplexe("E_AUTOMATE_ENCHAINEMENT", array('###DETAIL###' => "ECHEC AUTOMATE : l'état actuel du ticket ne permet pas le lancement de l'enchaînement"));
                    $preRequirementException = new PreRequirementException();
                    return $preRequirementException();
```

Question métier : Point de décision — !'preRequis'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #317 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : callEnchainementCommutMethod() — ligne 351
Contexte   :
```php
                $this->updateDateActionEnCoursEds($idTicket, $connectedGroup);
                $preRequis = $this->checkPreRequirementEnchainement($idTicket, $enchainement, $connectedGroup);
                if (!$preRequis) {
                    $message->setMessageComplexe("E_AUTOMATE_ENCHAINEMENT", array('###DETAIL###' => "ECHEC AUTOMATE : l'état actuel du ticket ne permet pas le lancement de l'enchaînement"));
                    $preRequirementException = new PreRequirementException();
                    return $preRequirementException();
```

Question métier : Point de décision — !'preRequis'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #318 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : updateDateActionEnCoursEds() — ligne 401
Contexte   :
```php
        );
        $result = $troubleTicketUpdate->getResponseUpdateDateActionEdsEnchainement($ticketId, $values);
        if (key_exists('faultstring', $result) && $result->faultstring != '' && key_exists('detail', $result)) {
            $updateOceaneException = new UpdateOceaneException();
            return $updateOceaneException();
        }
```

Question métier : Point de décision — key_exists('faultstring', 'result') et 'result'->faultstring différent de '' et key_exists('detail', 'result'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #319 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : getEDSActif() — ligne 419
Contexte   :
```php
        $EDSActif = array();
        $result = $OceaneFg->getResponseFindandGetTroubleTicket($ticketID);
        if (isset($result->TroubleTicketResponse->TroubleTicketResponse)) {
            $troubleTicketResponse = $result->TroubleTicketResponse->TroubleTicketResponse;

            $partyRole = $troubleTicketResponse->PartyRole;
```

Question métier : Point de décision — isset('result'->TroubleTicketResponse->TroubleTicketResponse). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #320 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : getEDSActif() — ligne 424
Contexte   :
```php
            $partyRole = $troubleTicketResponse->PartyRole;
            foreach ($partyRole as $key => $value) {
                if ($partyRole[$key]->partyRoleType == "TroubleResolutionContributor" && property_exists($partyRole[$key], 'Local_PartyIntervention')) {
                    if (is_object($partyRole[$key]->Local_PartyIntervention->interventionStatus) && $partyRole[$key]->Local_PartyIntervention->interventionStatus->status == "Accepted") {
                        return $partyRole[$key]->PartyRoleSet->partyRoleSetID;
                    } else if (is_object($partyRole[$key]->Local_PartyIntervention->interventionStatus) && $partyRole[$key]->Local_PartyIntervention->interventionStatus->status == "Requested" && $partyRole[$key]->Local_PartyIntervention->level == '1') {
```

Question métier : Point de décision — 'partyRole'['key']->partyRoleType égal à "TroubleResolutionContributor" et property_exists('partyRole'['key'], 'Local_PartyIntervention'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #321 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : getEDSActif() — ligne 429
Contexte   :
```php
                    } else if (is_object($partyRole[$key]->Local_PartyIntervention->interventionStatus) && $partyRole[$key]->Local_PartyIntervention->interventionStatus->status == "Requested" && $partyRole[$key]->Local_PartyIntervention->level == '1') {
                        return $partyRole[$key]->PartyRoleSet->partyRoleSetID;
                    } else if (is_array($partyRole[$key]->Local_PartyIntervention->interventionStatus)) {
                        foreach ($partyRole[$key]->Local_PartyIntervention->interventionStatus as $k => $v) {
                            if ($partyRole[$key]->Local_PartyIntervention->interventionStatus[$k]->status == "Requested" && $partyRole[$key]->Local_PartyIntervention->interventionStatus[$k + 1]->status == "Accepted") {
                                return $partyRole[$key]->PartyRoleSet->partyRoleSetID;
```

Question métier : Point de décision — is_array('partyRole'['key']->Local_PartyIntervention->interventionStatus). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #322 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : getEDSActif() — ligne 431
Contexte   :
```php
                    } else if (is_array($partyRole[$key]->Local_PartyIntervention->interventionStatus)) {
                        foreach ($partyRole[$key]->Local_PartyIntervention->interventionStatus as $k => $v) {
                            if ($partyRole[$key]->Local_PartyIntervention->interventionStatus[$k]->status == "Requested" && $partyRole[$key]->Local_PartyIntervention->interventionStatus[$k + 1]->status == "Accepted") {
                                return $partyRole[$key]->PartyRoleSet->partyRoleSetID;
                            }
                        }
```

Question métier : Point de décision — 'partyRole'['key']->Local_PartyIntervention->interventionStatus['k']->status égal à "Requested" et 'partyRole'['key']->Local_PartyIntervention->interventionStatus['k' + 1]->status égal à "Accepted". Quel est le comportement attendu dans le cas contraire ?

---

**Gap #323 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : getEDSPilote() — ligne 453
Contexte   :
```php
        $EDSPilote = array();
        $result = $OceaneFg->getResponseFindandGetTroubleTicket($ticketID);
        if (isset($result->TroubleTicketResponse->TroubleTicketResponse)) {
            $troubleTicketResponse = $result->TroubleTicketResponse->TroubleTicketResponse;

            $partyRole = $troubleTicketResponse->PartyRole;
```

Question métier : Point de décision — isset('result'->TroubleTicketResponse->TroubleTicketResponse). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #324 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : getEDSPilote() — ligne 458
Contexte   :
```php
            $partyRole = $troubleTicketResponse->PartyRole;
            foreach ($partyRole as $key => $value) {
                if ($partyRole[$key]->partyRoleType == "TroubleResolutionLeader" && property_exists($partyRole[$key], 'Local_PartyIntervention')) {
                    if (is_object($partyRole[$key]->Local_PartyIntervention->interventionStatus) && $partyRole[$key]->Local_PartyIntervention->interventionStatus->status == "Accepted") {
                        return $partyRole[$key]->PartyRoleSet->partyRoleSetID;
                    } else if (is_array($partyRole[$key]->Local_PartyIntervention->interventionStatus)) {
```

Question métier : Point de décision — 'partyRole'['key']->partyRoleType égal à "TroubleResolutionLeader" et property_exists('partyRole'['key'], 'Local_PartyIntervention'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #325 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : getEDSPilote() — ligne 461
Contexte   :
```php
                    if (is_object($partyRole[$key]->Local_PartyIntervention->interventionStatus) && $partyRole[$key]->Local_PartyIntervention->interventionStatus->status == "Accepted") {
                        return $partyRole[$key]->PartyRoleSet->partyRoleSetID;
                    } else if (is_array($partyRole[$key]->Local_PartyIntervention->interventionStatus)) {
                        foreach ($partyRole[$key]->Local_PartyIntervention->interventionStatus as $k => $v) {
                            if ($partyRole[$key]->Local_PartyIntervention->interventionStatus[$k]->status == "Requested" && $partyRole[$key]->Local_PartyIntervention->interventionStatus[$k + 1]->status == "Accepted") {
                                return $partyRole[$key]->PartyRoleSet->partyRoleSetID;
```

Question métier : Point de décision — is_array('partyRole'['key']->Local_PartyIntervention->interventionStatus). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #326 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : getEDSPilote() — ligne 463
Contexte   :
```php
                    } else if (is_array($partyRole[$key]->Local_PartyIntervention->interventionStatus)) {
                        foreach ($partyRole[$key]->Local_PartyIntervention->interventionStatus as $k => $v) {
                            if ($partyRole[$key]->Local_PartyIntervention->interventionStatus[$k]->status == "Requested" && $partyRole[$key]->Local_PartyIntervention->interventionStatus[$k + 1]->status == "Accepted") {
                                return $partyRole[$key]->PartyRoleSet->partyRoleSetID;
                            }
                        }
```

Question métier : Point de décision — 'partyRole'['key']->Local_PartyIntervention->interventionStatus['k']->status égal à "Requested" et 'partyRole'['key']->Local_PartyIntervention->interventionStatus['k' + 1]->status égal à "Accepted". Quel est le comportement attendu dans le cas contraire ?

---

**Gap #327 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : verifierTypeScenario() — ligne 528
Contexte   :
```php
    {
        $typeScenario = $this->enchainementRepo->verifierTypeScenario($idScenario);
        if($typeScenario == '0' && $scenarioType == 'parametrable')
        {
            $scenarioTypeException = new BadRequestException("Ce scenarioId n'est pas un scenario parametrable");
            return $scenarioTypeException();
```

Question métier : Valeur de référence non documentée — La décision « 'typeScenario' égal à '0' et 'scenarioType' égal à 'parametrable' » repose sur la valeur 'parametrable'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #345 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : initApi() — ligne 120
Contexte   :
```php
                $descriptionEvtIncident = ($evtIncident == '64') ? 1 : 0;
                //ID_CREATEUR
                $cuidLow = strtolower($cuid);
                $userData = $this->ihmUserRepository->getByLogin($cuidLow);

```

Question métier : Le code situation '64' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #346 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : checkTicketType() — ligne 214
Contexte   :
```php
            if ($category == '64') {
                $this->assistantRepository->evtToIncident($astroId, 'événement');
                $value = 'événement';
            } else {
                $value = '';
```

Question métier : Le code situation '64' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #347 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : createTicket() — ligne 227
Contexte   :
```php
        if ($data['type_ressource'] == 'DSLAM') {
            $ressource = $this->oceaneAssistant->detailMateriel($data['ressource'], $data['type_ressource_iadr'], $data['code_detecteur'], $data['description'], $data['id1']);
            $idRessource = $this->astroRepository->createRessource($ressource);
            $data['id_ressource'] = $idRessource;
        }
```

Question métier : Le code situation 'DSLAM' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #348 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : createTicket() — ligne 233
Contexte   :
```php
        if ($data['evt_incident'] == '64') {
            $idJeuParam = $this->astroRepository->getJeuParamByBandeauFonction($data['bandeau_id'], 'ABONDONNER');
        }
        $data['id_jeu_param'] = $idJeuParam;
        $this->astroRepository->addTicket($data['ticketoceaneid'], $data['status'], $data);
```

Question métier : Le code situation '64' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #349 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : getEDSActif() — ligne 427
Contexte   :
```php
                    } else if (is_object($partyRole[$key]->Local_PartyIntervention->interventionStatus) && $partyRole[$key]->Local_PartyIntervention->interventionStatus->status == "Requested" && $partyRole[$key]->Local_PartyIntervention->level == '1') {
                        return $partyRole[$key]->PartyRoleSet->partyRoleSetID;
                    } else if (is_array($partyRole[$key]->Local_PartyIntervention->interventionStatus)) {
                        foreach ($partyRole[$key]->Local_PartyIntervention->interventionStatus as $k => $v) {
                            if ($partyRole[$key]->Local_PartyIntervention->interventionStatus[$k]->status == "Requested" && $partyRole[$key]->Local_PartyIntervention->interventionStatus[$k + 1]->status == "Accepted") {
```

Question métier : Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #350 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : verifierScenarioExist() — ligne 506
Contexte   :
```php
        if($scenarioExist == '0')
        {
            $badRequestException = new BadRequestException('scenarioId does not exist');
            return $badRequestException();
        }else {
```

Question métier : Le code situation '0' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #351 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : verifierActivationScenario() — ligne 517
Contexte   :
```php
        if($etatScenario == '0')
        {
            $scenarioDesactiveException = new ScenarioDesactiveException();
            return $scenarioDesactiveException();
        }else {
```

Question métier : Le code situation '0' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #352 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : verifierTypeScenario() — ligne 528
Contexte   :
```php
        if($typeScenario == '0' && $scenarioType == 'parametrable')
        {
            $scenarioTypeException = new BadRequestException("Ce scenarioId n'est pas un scenario parametrable");
            return $scenarioTypeException();
        }elseif($typeScenario == '1' && $scenarioType == 'legacy')
```

Question métier : Le code situation '0' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #353 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : verifierTypeScenario() — ligne 532
Contexte   :
```php
        }elseif($typeScenario == '1' && $scenarioType == 'legacy')
        {
            $scenarioTypeException = new BadRequestException("Ce scenarioId n'est pas un scenario legacy");
            return $scenarioTypeException();
        }else  {
```

Question métier : Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #354 — Api**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : verifierTypeScenario() — ligne 532
Contexte   :
```php
        }elseif($typeScenario == '1' && $scenarioType == 'legacy')
        {
            $scenarioTypeException = new BadRequestException("Ce scenarioId n'est pas un scenario legacy");
            return $scenarioTypeException();
        }else  {
```

Question métier : Le code situation 'legacy' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #355 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getOceaneData() — ligne 54
Contexte   :
```php
        $this->app->get('TraceRepository')->setTrace($astroId, "RETOUR GET OCEANE DATA", $detailTicketJson, $this->sessId, $ticketId);

        if ($this->app->get('AstroBase')->isJson($detailTicketJson)) {
            $this->oceaneData = Json::decode($detailTicketJson, Json::TYPE_ARRAY);
        }
        return $this->oceaneData;
```

Question métier : Point de décision — 'this'->app->get('AstroBase')->isJson('detailTicketJson'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #356 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getRessourceIds() — ligne 68
Contexte   :
```php
    {
        $ids = [];
        if (key_exists('relatedResource', $this->oceaneData) && is_array($this->oceaneData['relatedResource']) && key_exists('resourceSpecCharacteristic', $this->oceaneData['relatedResource']) && is_array($this->oceaneData['relatedResource']['resourceSpecCharacteristic'])) {
            foreach ($this->oceaneData['relatedResource']['resourceSpecCharacteristic'] as $value) {
                if (is_array($value) && key_exists('index', $value) && !is_null($id) && (intval($value['index']) == $id) && key_exists('value', $value)) {
                    return $value['value'];
```

Question métier : Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource']) et key_exists('resourceSpecCharacteristic', 'this'->oceaneData['relatedResource']) et is_array('this'->oceaneData['relatedResource']['resourceSpecCharacteristic']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #357 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getProductIds() — ligne 88
Contexte   :
```php
    {
        $ids = [];
        if (key_exists('relatedService', $this->oceaneData) && is_array($this->oceaneData['relatedService']) && key_exists('serviceSpecCharacteristic', $this->oceaneData['relatedService']) && is_array($this->oceaneData['relatedService']['serviceSpecCharacteristic'])) {
            foreach ($this->oceaneData['relatedService']['serviceSpecCharacteristic'] as $value) {
                if (is_array($value) && key_exists('index', $value) && !is_null($id) && (intval($value['index']) == $id) && key_exists('value', $value)) {
                    return $value['value'];
```

Question métier : Point de décision — key_exists('relatedService', 'this'->oceaneData) et is_array('this'->oceaneData['relatedService']) et key_exists('serviceSpecCharacteristic', 'this'->oceaneData['relatedService']) et is_array('this'->oceaneData['relatedService']['serviceSpecCharacteristic']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #358 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getRessourceType() — ligne 107
Contexte   :
```php
    public function getRessourceType($idAndName = false)
    {
        if (key_exists('relatedResource', $this->oceaneData) && is_array($this->oceaneData['relatedResource']) && key_exists('resourceSpecification', $this->oceaneData['relatedResource'])) {
            $id = key_exists('id', $this->oceaneData['relatedResource']['resourceSpecification']) ? $this->oceaneData['relatedResource']['resourceSpecification']['id'] : null;
            if ($idAndName) {
                $name = key_exists('name', $this->oceaneData['relatedResource']['resourceSpecification']) ? $this->oceaneData['relatedResource']['resourceSpecification']['name'] : null;
```

Question métier : Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource']) et key_exists('resourceSpecification', 'this'->oceaneData['relatedResource']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #359 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getProductType() — ligne 129
Contexte   :
```php
    public function getProductType($idAndName = false)
    {
        if (key_exists('relatedService', $this->oceaneData) && is_array($this->oceaneData['relatedService']) && key_exists('serviceSpecification', $this->oceaneData['relatedService'])) {
            $id = key_exists('id', $this->oceaneData['relatedService']['serviceSpecification']) ? $this->oceaneData['relatedService']['serviceSpecification']['id'] : null;
            if ($idAndName) {
                $name = key_exists('name', $this->oceaneData['relatedService']['serviceSpecification']) ? $this->oceaneData['relatedService']['serviceSpecification']['name'] : null;
```

Question métier : Point de décision — key_exists('relatedService', 'this'->oceaneData) et is_array('this'->oceaneData['relatedService']) et key_exists('serviceSpecification', 'this'->oceaneData['relatedService']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #360 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getTicketCharacteristics() — ligne 152
Contexte   :
```php
    {
        $characteristic = [];
        if (key_exists('troubleTicketCharacteristic', $this->oceaneData) && is_array($this->oceaneData['troubleTicketCharacteristic']) && count($this->oceaneData['troubleTicketCharacteristic']) > 0) {
            foreach ($this->oceaneData['troubleTicketCharacteristic'] as $value) {
                if (is_array($value) && key_exists('index', $value) && !is_null($champ) && (intval($value['index']) == $champ) && key_exists('value', $value)) {
                    return $value['value'];
```

Question métier : Point de décision — key_exists('troubleTicketCharacteristic', 'this'->oceaneData) et is_array('this'->oceaneData['troubleTicketCharacteristic']) et count('this'->oceaneData['troubleTicketCharacteristic']) > 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #361 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getPriority() — ligne 171
Contexte   :
```php
    public function getPriority($idAndLabel = false)
    {
        if (key_exists('priority', $this->oceaneData) && is_array($this->oceaneData['priority'])) {
            $id = key_exists('id', $this->oceaneData['priority']) ? $this->oceaneData['priority']['id'] : null;
            if ($idAndLabel) {
                $label = key_exists('label', $this->oceaneData['priority']) ? $this->oceaneData['priority']['label'] : null;
```

Question métier : Point de décision — key_exists('priority', 'this'->oceaneData) et is_array('this'->oceaneData['priority']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #362 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getUrgency() — ligne 193
Contexte   :
```php
    public function getUrgency($idAndLabel = false)
    {
        if (key_exists('urgency', $this->oceaneData) && is_array($this->oceaneData['urgency'])) {
            $id = key_exists('id', $this->oceaneData['urgency']) ? $this->oceaneData['urgency']['id'] : null;
            if ($idAndLabel) {
                $label = key_exists('label', $this->oceaneData['urgency']) ? $this->oceaneData['urgency']['label'] : null;
```

Question métier : Point de décision — key_exists('urgency', 'this'->oceaneData) et is_array('this'->oceaneData['urgency']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #363 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getCreationDate() — ligne 215
Contexte   :
```php
    public function getCreationDate($format = null)
    {
        if (key_exists('creationDate', $this->oceaneData)) {
            if (!is_null($format)) {
                return $this->app->get('AstroBase')->formatDate($this->oceaneData['creationDate'], 'Y-m-d\TH:i:s\Z', $format);
            } else {
```

Question métier : Point de décision — key_exists('creationDate', 'this'->oceaneData). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #364 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getDetectionDate() — ligne 231
Contexte   :
```php
    public function getDetectionDate($format = null)
    {
        if (key_exists('detectionDate', $this->oceaneData)) {
            if (!is_null($format)) {
                return $this->app->get('AstroBase')->formatDate($this->oceaneData['detectionDate'], 'Y-m-d\TH:i:s\Z', $format);
            } else {
```

Question métier : Point de décision — key_exists('detectionDate', 'this'->oceaneData). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #365 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getDetailProblem() — ligne 243
Contexte   :
```php
    public function getDetailProblem()
    {
        if (key_exists('troubleCause', $this->oceaneData) && is_array($this->oceaneData['troubleCause']) && count($this->oceaneData['troubleCause']) > 0) {
            foreach ($this->oceaneData['troubleCause'] as $value) {
                if (is_array($value) && key_exists('problemDetail', $value) && key_exists('id', $value['problemDetail'])){
                    return $value['problemDetail']['id'];
```

Question métier : Point de décision — key_exists('troubleCause', 'this'->oceaneData) et is_array('this'->oceaneData['troubleCause']) et count('this'->oceaneData['troubleCause']) > 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #366 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getDetailProblem() — ligne 245
Contexte   :
```php
        if (key_exists('troubleCause', $this->oceaneData) && is_array($this->oceaneData['troubleCause']) && count($this->oceaneData['troubleCause']) > 0) {
            foreach ($this->oceaneData['troubleCause'] as $value) {
                if (is_array($value) && key_exists('problemDetail', $value) && key_exists('id', $value['problemDetail'])){
                    return $value['problemDetail']['id'];
                }
            }
```

Question métier : Point de décision — is_array('value') et key_exists('problemDetail', 'value') et key_exists('id', 'value'['problemDetail']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #367 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getPilotGroup() — ligne 259
Contexte   :
```php
    public function getPilotGroup()
    {
        if (key_exists('relatedParty', $this->oceaneData) && is_array($this->oceaneData['relatedParty']) && count($this->oceaneData['relatedParty']) > 0) {
            foreach ($this->oceaneData['relatedParty'] as $value) {
                if (is_array($value) && key_exists('role', $value) && $value['role'] == 'TroubleResolutionLeader' && key_exists('id', $value)) {
                    return $value['id'];
```

Question métier : Point de décision — key_exists('relatedParty', 'this'->oceaneData) et is_array('this'->oceaneData['relatedParty']) et count('this'->oceaneData['relatedParty']) > 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #368 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getPilotGroup() — ligne 261
Contexte   :
```php
        if (key_exists('relatedParty', $this->oceaneData) && is_array($this->oceaneData['relatedParty']) && count($this->oceaneData['relatedParty']) > 0) {
            foreach ($this->oceaneData['relatedParty'] as $value) {
                if (is_array($value) && key_exists('role', $value) && $value['role'] == 'TroubleResolutionLeader' && key_exists('id', $value)) {
                    return $value['id'];
                }
            }
```

Question métier : Point de décision — is_array('value') et key_exists('role', 'value') et 'value'['role'] égal à 'TroubleResolutionLeader' et key_exists('id', 'value'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #369 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getOriginatorGroup() — ligne 270
Contexte   :
```php
    public function getOriginatorGroup()
    {
        if (key_exists('relatedParty', $this->oceaneData) && is_array($this->oceaneData['relatedParty']) && count($this->oceaneData['relatedParty']) > 0) {
            foreach ($this->oceaneData['relatedParty'] as $value) {
                if (is_array($value) && key_exists('role', $value) && $value['role'] == 'troubleTicketOriginator' && key_exists('id', $value)) {
                    return $value['id'];
```

Question métier : Point de décision — key_exists('relatedParty', 'this'->oceaneData) et is_array('this'->oceaneData['relatedParty']) et count('this'->oceaneData['relatedParty']) > 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #370 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getOriginatorGroup() — ligne 272
Contexte   :
```php
        if (key_exists('relatedParty', $this->oceaneData) && is_array($this->oceaneData['relatedParty']) && count($this->oceaneData['relatedParty']) > 0) {
            foreach ($this->oceaneData['relatedParty'] as $value) {
                if (is_array($value) && key_exists('role', $value) && $value['role'] == 'troubleTicketOriginator' && key_exists('id', $value)) {
                    return $value['id'];
                }
            }
```

Question métier : Point de décision — is_array('value') et key_exists('role', 'value') et 'value'['role'] égal à 'troubleTicketOriginator' et key_exists('id', 'value'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #371 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getActionEds() — ligne 282
Contexte   :
```php
    public function getActionEds()
    {
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention']) && count($this->oceaneData['partyIntervention']) > 0) {
            foreach ($this->oceaneData['partyIntervention'] as $value) {
                if (is_array($value['relatedParty'])) {
                    foreach ($value['relatedParty'] as $valueRelatedParty) {
```

Question métier : Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyIntervention']) et count('this'->oceaneData['partyIntervention']) > 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #372 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getActionEds() — ligne 284
Contexte   :
```php
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention']) && count($this->oceaneData['partyIntervention']) > 0) {
            foreach ($this->oceaneData['partyIntervention'] as $value) {
                if (is_array($value['relatedParty'])) {
                    foreach ($value['relatedParty'] as $valueRelatedParty) {
                        if (is_array($valueRelatedParty) && key_exists('actionInProgress', $valueRelatedParty) && $valueRelatedParty['role'] == 'TroubleResolutionLeader') {
                            if (is_array($valueRelatedParty['actionInProgress']) && key_exists('description', $valueRelatedParty['actionInProgress']))
```

Question métier : Point de décision — is_array('value'['relatedParty']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #373 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getActionEds() — ligne 286
Contexte   :
```php
                if (is_array($value['relatedParty'])) {
                    foreach ($value['relatedParty'] as $valueRelatedParty) {
                        if (is_array($valueRelatedParty) && key_exists('actionInProgress', $valueRelatedParty) && $valueRelatedParty['role'] == 'TroubleResolutionLeader') {
                            if (is_array($valueRelatedParty['actionInProgress']) && key_exists('description', $valueRelatedParty['actionInProgress']))
                                return $valueRelatedParty['actionInProgress']['description'];
                        }
```

Question métier : Point de décision — is_array('valueRelatedParty') et key_exists('actionInProgress', 'valueRelatedParty') et 'valueRelatedParty'['role'] égal à 'TroubleResolutionLeader'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #374 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getActionEds() — ligne 287
Contexte   :
```php
                    foreach ($value['relatedParty'] as $valueRelatedParty) {
                        if (is_array($valueRelatedParty) && key_exists('actionInProgress', $valueRelatedParty) && $valueRelatedParty['role'] == 'TroubleResolutionLeader') {
                            if (is_array($valueRelatedParty['actionInProgress']) && key_exists('description', $valueRelatedParty['actionInProgress']))
                                return $valueRelatedParty['actionInProgress']['description'];
                        }
                    }
```

Question métier : Point de décision — is_array('valueRelatedParty'['actionInProgress']) et key_exists('description', 'valueRelatedParty'['actionInProgress']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #375 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getActifGroup() — ligne 298
Contexte   :
```php
    public function getActifGroup()
    {
        if (key_exists('relatedParty', $this->oceaneData) && is_array($this->oceaneData['relatedParty']) && count($this->oceaneData['relatedParty']) > 0) {
            foreach ($this->oceaneData['relatedParty'] as $value) {
                if (is_array($value) && key_exists('role', $value) && $value['role'] == 'TroubleResolutionContributor' && key_exists('id', $value)) {
                    return $value['id'];
```

Question métier : Point de décision — key_exists('relatedParty', 'this'->oceaneData) et is_array('this'->oceaneData['relatedParty']) et count('this'->oceaneData['relatedParty']) > 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #376 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getActifGroup() — ligne 300
Contexte   :
```php
        if (key_exists('relatedParty', $this->oceaneData) && is_array($this->oceaneData['relatedParty']) && count($this->oceaneData['relatedParty']) > 0) {
            foreach ($this->oceaneData['relatedParty'] as $value) {
                if (is_array($value) && key_exists('role', $value) && $value['role'] == 'TroubleResolutionContributor' && key_exists('id', $value)) {
                    return $value['id'];
                }
            }
```

Question métier : Point de décision — is_array('value') et key_exists('role', 'value') et 'value'['role'] égal à 'TroubleResolutionContributor' et key_exists('id', 'value'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #377 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getInterventionStatus() — ligne 310
Contexte   :
```php
    public function getInterventionStatus()
    {
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            foreach ($this->oceaneData['partyIntervention'] as $value) {
                    if (key_exists('interventionStatus', $value) && is_array($value['interventionStatus'])) {
                        foreach ($value['interventionStatus'] as $status) {
```

Question métier : Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyIntervention']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #378 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getInterventionStatus() — ligne 312
Contexte   :
```php
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            foreach ($this->oceaneData['partyIntervention'] as $value) {
                    if (key_exists('interventionStatus', $value) && is_array($value['interventionStatus'])) {
                        foreach ($value['interventionStatus'] as $status) {
                            if((is_array($status) && key_exists('status', $status))){
                                return $status['status'];
```

Question métier : Point de décision — key_exists('interventionStatus', 'value') et is_array('value'['interventionStatus']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #379 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getInterventionStatus() — ligne 314
Contexte   :
```php
                    if (key_exists('interventionStatus', $value) && is_array($value['interventionStatus'])) {
                        foreach ($value['interventionStatus'] as $status) {
                            if((is_array($status) && key_exists('status', $status))){
                                return $status['status'];
                            }
                        }
```

Question métier : Point de décision — (is_array('status') et key_exists('status', 'status')). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #380 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getStatus() — ligne 326
Contexte   :
```php
    public function getStatus()
    {
        if (key_exists('status', $this->oceaneData) && is_array($this->oceaneData['status'])) {
            foreach ($this->oceaneData['status'] as $value) {
                if (key_exists('isCurrentStatus', $value) && $value['isCurrentStatus'] == 1) {
                    return $value['code'];
```

Question métier : Point de décision — key_exists('status', 'this'->oceaneData) et is_array('this'->oceaneData['status']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #381 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getStatus() — ligne 328
Contexte   :
```php
        if (key_exists('status', $this->oceaneData) && is_array($this->oceaneData['status'])) {
            foreach ($this->oceaneData['status'] as $value) {
                if (key_exists('isCurrentStatus', $value) && $value['isCurrentStatus'] == 1) {
                    return $value['code'];
                }
            }
```

Question métier : Point de décision — key_exists('isCurrentStatus', 'value') et 'value'['isCurrentStatus'] égal à 1. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #382 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getTicketType() — ligne 338
Contexte   :
```php
    public function getTicketType($idAndLabel = false)
    {
        if (key_exists('ticketType', $this->oceaneData) && is_array($this->oceaneData['ticketType'])) {
            $id = key_exists('id', $this->oceaneData['ticketType']) ? $this->oceaneData['ticketType']['id'] : null;
            if ($idAndLabel) {
                $label = key_exists('label', $this->oceaneData['ticketType']) ? $this->oceaneData['ticketType']['label'] : null;
```

Question métier : Point de décision — key_exists('ticketType', 'this'->oceaneData) et is_array('this'->oceaneData['ticketType']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #383 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getOrigin() — ligne 355
Contexte   :
```php
    public function getOrigin($idAndLabel = false)
    {
        if (key_exists('origin', $this->oceaneData) && is_array($this->oceaneData['origin'])) {
            $id = key_exists('id', $this->oceaneData['origin']) ? $this->oceaneData['origin']['id'] : null;
            if ($idAndLabel) {
                $label = key_exists('label', $this->oceaneData['origin']) ? $this->oceaneData['origin']['label'] : null;
```

Question métier : Point de décision — key_exists('origin', 'this'->oceaneData) et is_array('this'->oceaneData['origin']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #384 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getInstalledRessourceId() — ligne 373
Contexte   :
```php
    public function getInstalledRessourceId()
    {
        if (key_exists('relatedResource', $this->oceaneData) && is_array($this->oceaneData['relatedResource']) && key_exists('id', $this->oceaneData['relatedResource'])) {
            return $this->oceaneData['relatedResource']['id'];
        }
        return null;
```

Question métier : Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource']) et key_exists('id', 'this'->oceaneData['relatedResource']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #385 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getTicketParamsAttribute() — ligne 382
Contexte   :
```php
    public function getTicketParamsAttribute($param,$name)
    {
        if (key_exists('relatedResource', $this->oceaneData) && is_array($this->oceaneData['relatedResource']) && key_exists('resourceCharacteristic', $this->oceaneData['relatedResource']) && is_array($this->oceaneData['relatedResource']['resourceCharacteristic'])) {
            foreach ($this->oceaneData['relatedResource']['resourceCharacteristic'] as $value) {
                if (is_array($value) && key_exists('@type', $value) && $value['@type'] == $param && key_exists('id', $value) && $value['id'] == $name) {
                    return $value['value'];
```

Question métier : Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource']) et key_exists('resourceCharacteristic', 'this'->oceaneData['relatedResource']) et is_array('this'->oceaneData['relatedResource']['resourceCharacteristic']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #386 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getTicketParamsAttribute() — ligne 384
Contexte   :
```php
        if (key_exists('relatedResource', $this->oceaneData) && is_array($this->oceaneData['relatedResource']) && key_exists('resourceCharacteristic', $this->oceaneData['relatedResource']) && is_array($this->oceaneData['relatedResource']['resourceCharacteristic'])) {
            foreach ($this->oceaneData['relatedResource']['resourceCharacteristic'] as $value) {
                if (is_array($value) && key_exists('@type', $value) && $value['@type'] == $param && key_exists('id', $value) && $value['id'] == $name) {
                    return $value['value'];
                }
            }
```

Question métier : Point de décision — is_array('value') et key_exists('@type', 'value') et 'value'['@type'] égal à 'param' et key_exists('id', 'value') et 'value'['id'] égal à 'name'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #387 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getPartyId() — ligne 407
Contexte   :
```php
    public function getPartyId()
    {
        if (key_exists('relatedParty', $this->oceaneData) && is_array($this->oceaneData['relatedParty']) && count($this->oceaneData['relatedParty']) > 0) {
            foreach ($this->oceaneData['relatedParty'] as $value) {
                if (is_array($value) && key_exists('familyName', $value) && key_exists('id', $value)) {
                    return $value['id'];
```

Question métier : Point de décision — key_exists('relatedParty', 'this'->oceaneData) et is_array('this'->oceaneData['relatedParty']) et count('this'->oceaneData['relatedParty']) > 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #388 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getPartyId() — ligne 409
Contexte   :
```php
        if (key_exists('relatedParty', $this->oceaneData) && is_array($this->oceaneData['relatedParty']) && count($this->oceaneData['relatedParty']) > 0) {
            foreach ($this->oceaneData['relatedParty'] as $value) {
                if (is_array($value) && key_exists('familyName', $value) && key_exists('id', $value)) {
                    return $value['id'];
                }
            }
```

Question métier : Point de décision — is_array('value') et key_exists('familyName', 'value') et key_exists('id', 'value'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #389 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getTicketCause() — ligne 419
Contexte   :
```php
    public function getTicketCause()
    {
        if (key_exists('troubleCause', $this->oceaneData) && is_array($this->oceaneData['troubleCause'])) {
            return key_exists('internalComplement', $this->oceaneData['troubleCause']) ? $this->oceaneData['troubleCause']['internalComplement'] : '';
        }
        return null;
```

Question métier : Point de décision — key_exists('troubleCause', 'this'->oceaneData) et is_array('this'->oceaneData['troubleCause']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #390 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getPosteAssocie() — ligne 427
Contexte   :
```php
    public function getPosteAssocie()
    {
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            if (key_exists('relatedParty', $this->oceaneData) && is_array($this->oceaneData['relatedParty']) && count($this->oceaneData['relatedParty']) > 0) {
                foreach ($this->oceaneData['relatedParty'] as $value) {
                    if (is_array($value) && key_exists('role', $value) && $value['role'] == 'WorkingGroup' && key_exists('id', $value)) {
```

Question métier : Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyIntervention']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #391 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getPosteAssocie() — ligne 428
Contexte   :
```php
    {
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            if (key_exists('relatedParty', $this->oceaneData) && is_array($this->oceaneData['relatedParty']) && count($this->oceaneData['relatedParty']) > 0) {
                foreach ($this->oceaneData['relatedParty'] as $value) {
                    if (is_array($value) && key_exists('role', $value) && $value['role'] == 'WorkingGroup' && key_exists('id', $value)) {
                        return $value['id'];
```

Question métier : Point de décision — key_exists('relatedParty', 'this'->oceaneData) et is_array('this'->oceaneData['relatedParty']) et count('this'->oceaneData['relatedParty']) > 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #392 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getPosteAssocie() — ligne 430
Contexte   :
```php
            if (key_exists('relatedParty', $this->oceaneData) && is_array($this->oceaneData['relatedParty']) && count($this->oceaneData['relatedParty']) > 0) {
                foreach ($this->oceaneData['relatedParty'] as $value) {
                    if (is_array($value) && key_exists('role', $value) && $value['role'] == 'WorkingGroup' && key_exists('id', $value)) {
                        return $value['id'];
                    }
                }
```

Question métier : Point de décision — is_array('value') et key_exists('role', 'value') et 'value'['role'] égal à 'WorkingGroup' et key_exists('id', 'value'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #393 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getLibelleSuccinct() — ligne 441
Contexte   :
```php
    public function getLibelleSuccinct()
    {
        if (key_exists('status', $this->oceaneData) && is_array($this->oceaneData['status'])) {
            foreach ($this->oceaneData['status'] as $value) {
                if (key_exists('reason', $value)) {
                    return $value['reason'];
```

Question métier : Point de décision — key_exists('status', 'this'->oceaneData) et is_array('this'->oceaneData['status']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #394 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getLibelleSuccinct() — ligne 443
Contexte   :
```php
        if (key_exists('status', $this->oceaneData) && is_array($this->oceaneData['status'])) {
            foreach ($this->oceaneData['status'] as $value) {
                if (key_exists('reason', $value)) {
                    return $value['reason'];
                }
            }
```

Question métier : Point de décision — key_exists('reason', 'value'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #395 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : isRessource() — ligne 457
Contexte   :
```php
    public function isRessource()
    {
        if (key_exists('relatedResource', $this->oceaneData) && is_array($this->oceaneData['relatedResource']) && key_exists('resourceSpecification', $this->oceaneData['relatedResource'])) {
            return true;
        }
        return false;
```

Question métier : Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource']) et key_exists('resourceSpecification', 'this'->oceaneData['relatedResource']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #396 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : isChild() — ligne 479
Contexte   :
```php
        $oceaneApi = new ApiOceane($token, $headerConfig);
        $resultChild = $oceaneApi->getParent($oceaneApiData['url'], $ticketId);
        if ($this->app->get('AstroBase')->isJson($resultChild)) {
            $resultChild = Json::decode($resultChild, Json::TYPE_ARRAY);
            if (is_array($resultChild) && !empty($resultChild) && !key_exists('code', $resultChild) && key_exists('type', $resultChild[0]) && $resultChild[0]['type'] == 'isParent') {
                return true;
```

Question métier : Point de décision — 'this'->app->get('AstroBase')->isJson('resultChild'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #397 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : isChild() — ligne 481
Contexte   :
```php
        if ($this->app->get('AstroBase')->isJson($resultChild)) {
            $resultChild = Json::decode($resultChild, Json::TYPE_ARRAY);
            if (is_array($resultChild) && !empty($resultChild) && !key_exists('code', $resultChild) && key_exists('type', $resultChild[0]) && $resultChild[0]['type'] == 'isParent') {
                return true;
            }
        }
```

Question métier : Point de décision — is_array($resultChild) && !le champ 'resultChild' est vide && !key_exists('code', $resultChild) && key_exists('type', $resultChild[0]) && $resultChild[0]['type'] == 'isParent'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #398 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : isActivationRequested() — ligne 497
Contexte   :
```php
        $activationRequested = false;
        $isContributor = false;
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            foreach ($this->oceaneData['partyIntervention'] as $value) {
                if (is_array($value) && key_exists('relatedParty', $value) && is_array($value['relatedParty'])) {
                    foreach ($value['relatedParty'] as $party) {
```

Question métier : Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyIntervention']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #399 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : isActivationRequested() — ligne 499
Contexte   :
```php
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            foreach ($this->oceaneData['partyIntervention'] as $value) {
                if (is_array($value) && key_exists('relatedParty', $value) && is_array($value['relatedParty'])) {
                    foreach ($value['relatedParty'] as $party) {
                        if (is_array($party) && key_exists('@referredType', $party) && $party['@referredType'] == 'Organisation' && key_exists('role', $party) && $party['role'] == 'TroubleResolutionContributor' && key_exists('id', $party) && $party['id'] == $eds) {
                            $isContributor = true;
```

Question métier : Point de décision — is_array('value') et key_exists('relatedParty', 'value') et is_array('value'['relatedParty']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #400 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : isActivationRequested() — ligne 501
Contexte   :
```php
                if (is_array($value) && key_exists('relatedParty', $value) && is_array($value['relatedParty'])) {
                    foreach ($value['relatedParty'] as $party) {
                        if (is_array($party) && key_exists('@referredType', $party) && $party['@referredType'] == 'Organisation' && key_exists('role', $party) && $party['role'] == 'TroubleResolutionContributor' && key_exists('id', $party) && $party['id'] == $eds) {
                            $isContributor = true;
                            break;
                        }
```

Question métier : Point de décision — is_array('party') et key_exists('@referredType', 'party') et 'party'['@referredType'] égal à 'Organisation' et key_exists('role', 'party') et 'party'['role'] égal à 'TroubleResolutionContributor' et key_exists('id', 'party') et 'party'['id'] égal à 'eds'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #401 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : isActivationRequested() — ligne 506
Contexte   :
```php
                        }
                    }
                    if ($isContributor && key_exists('interventionStatus', $value) && is_array($value['interventionStatus'])) {
                        foreach ($value['interventionStatus'] as $status) {
                            $activationRequested = (is_array($status) && key_exists('status', $status) && $status['status'] == 'Requested');
                        }
```

Question métier : Point de décision — 'isContributor' et key_exists('interventionStatus', 'value') et is_array('value'['interventionStatus']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #402 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : isActivationRequested() — ligne 513
Contexte   :
```php
                    }
                }
                if ($activationRequested) {
                    return true;
                }
            }
```

Question métier : Point de décision — 'activationRequested'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #403 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getRestorationDate() — ligne 522
Contexte   :
```php
    public function getRestorationDate($format = null)
    {
        if (key_exists('status', $this->oceaneData) && is_array($this->oceaneData['status'])) {
            foreach ($this->oceaneData['status'] as $value) {
                if (key_exists('code', $value) && $value['code'] == "Restored") {
                    if (key_exists('startDate', $value)) {
```

Question métier : Point de décision — key_exists('status', 'this'->oceaneData) et is_array('this'->oceaneData['status']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #404 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getRestorationDate() — ligne 524
Contexte   :
```php
        if (key_exists('status', $this->oceaneData) && is_array($this->oceaneData['status'])) {
            foreach ($this->oceaneData['status'] as $value) {
                if (key_exists('code', $value) && $value['code'] == "Restored") {
                    if (key_exists('startDate', $value)) {
                        if (!is_null($format)) {
                            return $this->app->get('AstroBase')->formatDate($value['startDate'], 'Y-m-d\TH:i:s\Z', $format);
```

Question métier : Point de décision — key_exists('code', 'value') et 'value'['code'] égal à "Restored". Quel est le comportement attendu dans le cas contraire ?

---

**Gap #405 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getRestorationDate() — ligne 525
Contexte   :
```php
            foreach ($this->oceaneData['status'] as $value) {
                if (key_exists('code', $value) && $value['code'] == "Restored") {
                    if (key_exists('startDate', $value)) {
                        if (!is_null($format)) {
                            return $this->app->get('AstroBase')->formatDate($value['startDate'], 'Y-m-d\TH:i:s\Z', $format);
                        } else {
```

Question métier : Point de décision — key_exists('startDate', 'value'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #406 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getResolutionDate() — ligne 539
Contexte   :
```php
    public function getResolutionDate($format = null)
    {
        if (key_exists('status', $this->oceaneData) && is_array($this->oceaneData['status'])) {
            foreach ($this->oceaneData['status'] as $value) {
                if (key_exists('code', $value) && $value['code'] == "Resolved") {
                    if (key_exists('startDate', $value)) {
```

Question métier : Point de décision — key_exists('status', 'this'->oceaneData) et is_array('this'->oceaneData['status']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #407 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getResolutionDate() — ligne 541
Contexte   :
```php
        if (key_exists('status', $this->oceaneData) && is_array($this->oceaneData['status'])) {
            foreach ($this->oceaneData['status'] as $value) {
                if (key_exists('code', $value) && $value['code'] == "Resolved") {
                    if (key_exists('startDate', $value)) {
                        if (!is_null($format)) {
                            return $this->app->get('AstroBase')->formatDate($value['startDate'], 'Y-m-d\TH:i:s\Z', $format);
```

Question métier : Point de décision — key_exists('code', 'value') et 'value'['code'] égal à "Resolved". Quel est le comportement attendu dans le cas contraire ?

---

**Gap #408 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getResolutionDate() — ligne 542
Contexte   :
```php
            foreach ($this->oceaneData['status'] as $value) {
                if (key_exists('code', $value) && $value['code'] == "Resolved") {
                    if (key_exists('startDate', $value)) {
                        if (!is_null($format)) {
                            return $this->app->get('AstroBase')->formatDate($value['startDate'], 'Y-m-d\TH:i:s\Z', $format);
                        } else {
```

Question métier : Point de décision — key_exists('startDate', 'value'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #409 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getCategory() — ligne 561
Contexte   :
```php
    public function getCategory($idAndLabel = false)
    {
        if (key_exists('category', $this->oceaneData) && is_array($this->oceaneData['category'])) {
            $id = key_exists('id', $this->oceaneData['category']) ? $this->oceaneData['category']['id'] : null;
            if ($idAndLabel) {
                $label = key_exists('label', $this->oceaneData['category']) ? $this->oceaneData['category']['label'] : null;
```

Question métier : Point de décision — key_exists('category', 'this'->oceaneData) et is_array('this'->oceaneData['category']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #410 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getLibelleImputation() — ligne 577
Contexte   :
```php
     public function getLibelleImputation(){

             if (key_exists('troubleCause', $this->oceaneData) && is_array($this->oceaneData['troubleCause'])) {
                 return key_exists('label', $this->oceaneData['troubleCause']) ? $this->oceaneData['troubleCause']['label'] : '';
             }
             return null;
```

Question métier : Point de décision — key_exists('troubleCause', 'this'->oceaneData) et is_array('this'->oceaneData['troubleCause']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #411 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : isActivationAccpeted() — ligne 588
Contexte   :
```php
        $activationAccepted = false;
        $isContributor = false;
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            foreach ($this->oceaneData['partyIntervention'] as $value) {
                if (is_array($value) && key_exists('relatedParty', $value) && is_array($value['relatedParty'])) {
                    foreach ($value['relatedParty'] as $party) {
```

Question métier : Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyIntervention']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #412 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : isActivationAccpeted() — ligne 590
Contexte   :
```php
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            foreach ($this->oceaneData['partyIntervention'] as $value) {
                if (is_array($value) && key_exists('relatedParty', $value) && is_array($value['relatedParty'])) {
                    foreach ($value['relatedParty'] as $party) {
                        if (is_array($party) && key_exists('@referredType', $party) && $party['@referredType'] == 'Organisation' && key_exists('role', $party) && $party['role'] == 'TroubleResolutionContributor' && key_exists('id', $party)) {
                            $isContributor = true;
```

Question métier : Point de décision — is_array('value') et key_exists('relatedParty', 'value') et is_array('value'['relatedParty']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #413 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : isActivationAccpeted() — ligne 592
Contexte   :
```php
                if (is_array($value) && key_exists('relatedParty', $value) && is_array($value['relatedParty'])) {
                    foreach ($value['relatedParty'] as $party) {
                        if (is_array($party) && key_exists('@referredType', $party) && $party['@referredType'] == 'Organisation' && key_exists('role', $party) && $party['role'] == 'TroubleResolutionContributor' && key_exists('id', $party)) {
                            $isContributor = true;
                            break;
                        }
```

Question métier : Point de décision — is_array('party') et key_exists('@referredType', 'party') et 'party'['@referredType'] égal à 'Organisation' et key_exists('role', 'party') et 'party'['role'] égal à 'TroubleResolutionContributor' et key_exists('id', 'party'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #414 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : isActivationAccpeted() — ligne 597
Contexte   :
```php
                        }
                    }
                    if ($isContributor && key_exists('interventionStatus', $value) && is_array($value['interventionStatus'])) {
                        foreach ($value['interventionStatus'] as $status) {
                            $activationAccepted = (is_array($status) && key_exists('status', $status) && $status['status'] == 'Accepted' || $status['status'] == 'Completed');
                        }
```

Question métier : Point de décision — 'isContributor' et key_exists('interventionStatus', 'value') et is_array('value'['interventionStatus']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #415 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : isActivationAccpeted() — ligne 604
Contexte   :
```php
                    }
                }
                if ($activationAccepted) {
                    return 1;
                }
            }
```

Question métier : Point de décision — 'activationAccepted'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #416 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : activationIdsAndRoles() — ligne 618
Contexte   :
```php
        $eds_nom = [];
        $eds_code = [];
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            foreach ($this->oceaneData['partyIntervention'] as $value) {
                if (is_array($value) && key_exists('relatedParty', $value) && is_array($value['relatedParty'])) {
                    foreach ($value['relatedParty'] as $party) {
```

Question métier : Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyIntervention']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #417 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : activationIdsAndRoles() — ligne 620
Contexte   :
```php
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            foreach ($this->oceaneData['partyIntervention'] as $value) {
                if (is_array($value) && key_exists('relatedParty', $value) && is_array($value['relatedParty'])) {
                    foreach ($value['relatedParty'] as $party) {
                        if (is_array($party) && key_exists('@referredType', $party) && $party['@referredType'] == 'Organisation' && key_exists('role', $party) && $party['role'] == 'TroubleResolutionContributor' && key_exists('id', $party)) {
                            $isContributor = true;
```

Question métier : Point de décision — is_array('value') et key_exists('relatedParty', 'value') et is_array('value'['relatedParty']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #418 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : activationIdsAndRoles() — ligne 622
Contexte   :
```php
                if (is_array($value) && key_exists('relatedParty', $value) && is_array($value['relatedParty'])) {
                    foreach ($value['relatedParty'] as $party) {
                        if (is_array($party) && key_exists('@referredType', $party) && $party['@referredType'] == 'Organisation' && key_exists('role', $party) && $party['role'] == 'TroubleResolutionContributor' && key_exists('id', $party)) {
                            $isContributor = true;
                            break;
                        }
```

Question métier : Point de décision — is_array('party') et key_exists('@referredType', 'party') et 'party'['@referredType'] égal à 'Organisation' et key_exists('role', 'party') et 'party'['role'] égal à 'TroubleResolutionContributor' et key_exists('id', 'party'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #419 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : activationIdsAndRoles() — ligne 627
Contexte   :
```php
                        }
                    }
                    if ($isContributor && key_exists('interventionStatus', $value) && is_array($value['interventionStatus'])) {
                        foreach ($value['interventionStatus'] as $status) {
                            $activationAccepted = (is_array($status) && key_exists('status', $status) && $status['status'] == 'Accepted' || $status['status'] == 'Completed');
                        }
```

Question métier : Point de décision — 'isContributor' et key_exists('interventionStatus', 'value') et is_array('value'['interventionStatus']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #420 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : activationIdsAndRoles() — ligne 631
Contexte   :
```php
                            $activationAccepted = (is_array($status) && key_exists('status', $status) && $status['status'] == 'Accepted' || $status['status'] == 'Completed');
                        }
                        if ($activationAccepted) {
                            array_push($eds_code, $party['id']);
                            array_push($eds_nom, $party['label']);
                        }
```

Question métier : Point de décision — 'activationAccepted'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #421 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getCriticity() — ligne 647
Contexte   :
```php
    public function getCriticity($idAndLabel = false)
    {
        if (key_exists('criticity', $this->oceaneData) && is_array($this->oceaneData['criticity'])) {
            $id = key_exists('id', $this->oceaneData['criticity']) ? $this->oceaneData['criticity']['id'] : null;
            if ($idAndLabel) {
                $label = key_exists('label', $this->oceaneData['criticity']) ? $this->oceaneData['criticity']['label'] : null;
```

Question métier : Point de décision — key_exists('criticity', 'this'->oceaneData) et is_array('this'->oceaneData['criticity']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #422 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getTargetRestorationDate() — ligne 668
Contexte   :
```php
    public function getTargetRestorationDate($format = null)
    {
        if (key_exists('targetRestorationDate', $this->oceaneData)) {
            if (!is_null($format)) {
                return $this->app->get('AstroBase')->formatDate($this->oceaneData['targetRestorationDate'], 'Y-m-d\TH:i:s\Z', $format);
            } else {
```

Question métier : Point de décision — key_exists('targetRestorationDate', 'this'->oceaneData). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #423 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getPlannedRestorationDate() — ligne 684
Contexte   :
```php
    public function getPlannedRestorationDate($format = null)
    {
        if (key_exists('plannedRestorationDate', $this->oceaneData)) {
            if (!is_null($format)) {
                return $this->app->get('AstroBase')->formatDate($this->oceaneData['plannedRestorationDate'], 'Y-m-d\TH:i:s\Z', $format);
            } else {
```

Question métier : Point de décision — key_exists('plannedRestorationDate', 'this'->oceaneData). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #424 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getDateActionInProgress() — ligne 695
Contexte   :
```php
    public function getDateActionInProgress($format = null)
    {
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            if (key_exists('relatedParty', $this->oceaneData['partyIntervention'][0]) && is_array($this->oceaneData['partyIntervention'][0]['relatedParty'])) {
                foreach ($this->oceaneData['partyIntervention'][0]['relatedParty'] as $value) {
                    if (is_array($value) && key_exists('actionInProgress', $value) &&  key_exists('startDate', $value['actionInProgress'])) {
```

Question métier : Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyIntervention']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #425 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getDateActionInProgress() — ligne 696
Contexte   :
```php
    {
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            if (key_exists('relatedParty', $this->oceaneData['partyIntervention'][0]) && is_array($this->oceaneData['partyIntervention'][0]['relatedParty'])) {
                foreach ($this->oceaneData['partyIntervention'][0]['relatedParty'] as $value) {
                    if (is_array($value) && key_exists('actionInProgress', $value) &&  key_exists('startDate', $value['actionInProgress'])) {

```

Question métier : Point de décision — key_exists('relatedParty', 'this'->oceaneData['partyIntervention'][0]) et is_array('this'->oceaneData['partyIntervention'][0]['relatedParty']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #426 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getDateActionInProgress() — ligne 698
Contexte   :
```php
            if (key_exists('relatedParty', $this->oceaneData['partyIntervention'][0]) && is_array($this->oceaneData['partyIntervention'][0]['relatedParty'])) {
                foreach ($this->oceaneData['partyIntervention'][0]['relatedParty'] as $value) {
                    if (is_array($value) && key_exists('actionInProgress', $value) &&  key_exists('startDate', $value['actionInProgress'])) {

                        if (!is_null($format)) {
                            return $this->app->get('AstroBase')->formatDate($value['actionInProgress']['startDate'], 'Y-m-d\TH:i:s\Z', $format);
```

Question métier : Point de décision — is_array('value') et key_exists('actionInProgress', 'value') et key_exists('startDate', 'value'['actionInProgress']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #427 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getActionInProgress() — ligne 713
Contexte   :
```php
    public function getActionInProgress()
    {
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            if (key_exists('relatedParty', $this->oceaneData['partyIntervention'][0]) && is_array($this->oceaneData['partyIntervention'][0]['relatedParty'])) {
                foreach ($this->oceaneData['partyIntervention'][0]['relatedParty'] as $value) {
                    if (is_array($value) && key_exists('actionInProgress', $value) &&  key_exists('description', $value['actionInProgress'])) {
```

Question métier : Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyIntervention']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #428 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getActionInProgress() — ligne 714
Contexte   :
```php
    {
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            if (key_exists('relatedParty', $this->oceaneData['partyIntervention'][0]) && is_array($this->oceaneData['partyIntervention'][0]['relatedParty'])) {
                foreach ($this->oceaneData['partyIntervention'][0]['relatedParty'] as $value) {
                    if (is_array($value) && key_exists('actionInProgress', $value) &&  key_exists('description', $value['actionInProgress'])) {
                     return $value['actionInProgress']['description'];
```

Question métier : Point de décision — key_exists('relatedParty', 'this'->oceaneData['partyIntervention'][0]) et is_array('this'->oceaneData['partyIntervention'][0]['relatedParty']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #429 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getActionInProgress() — ligne 716
Contexte   :
```php
            if (key_exists('relatedParty', $this->oceaneData['partyIntervention'][0]) && is_array($this->oceaneData['partyIntervention'][0]['relatedParty'])) {
                foreach ($this->oceaneData['partyIntervention'][0]['relatedParty'] as $value) {
                    if (is_array($value) && key_exists('actionInProgress', $value) &&  key_exists('description', $value['actionInProgress'])) {
                     return $value['actionInProgress']['description'];

                    }
```

Question métier : Point de décision — is_array('value') et key_exists('actionInProgress', 'value') et key_exists('description', 'value'['actionInProgress']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #430 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getEdsActionInProgress() — ligne 728
Contexte   :
```php
    public function getEdsActionInProgress()
    {
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            if (key_exists('relatedParty', $this->oceaneData['partyIntervention'][0]) && is_array($this->oceaneData['partyIntervention'][0]['relatedParty'])) {
                foreach ($this->oceaneData['partyIntervention'][0]['relatedParty'] as $value) {
                    if (is_array($value) && key_exists('id', $value)) {
```

Question métier : Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyIntervention']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #431 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getEdsActionInProgress() — ligne 729
Contexte   :
```php
    {
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            if (key_exists('relatedParty', $this->oceaneData['partyIntervention'][0]) && is_array($this->oceaneData['partyIntervention'][0]['relatedParty'])) {
                foreach ($this->oceaneData['partyIntervention'][0]['relatedParty'] as $value) {
                    if (is_array($value) && key_exists('id', $value)) {
                        return $value['id'];
```

Question métier : Point de décision — key_exists('relatedParty', 'this'->oceaneData['partyIntervention'][0]) et is_array('this'->oceaneData['partyIntervention'][0]['relatedParty']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #432 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getEdsActionInProgress() — ligne 731
Contexte   :
```php
            if (key_exists('relatedParty', $this->oceaneData['partyIntervention'][0]) && is_array($this->oceaneData['partyIntervention'][0]['relatedParty'])) {
                foreach ($this->oceaneData['partyIntervention'][0]['relatedParty'] as $value) {
                    if (is_array($value) && key_exists('id', $value)) {
                        return $value['id'];
                    }
                }
```

Question métier : Point de décision — is_array('value') et key_exists('id', 'value'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #433 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getClasitePrio() — ligne 756
Contexte   :
```php
    }
    public function getClasitePrio(){
        if (key_exists('relatedResource', $this->oceaneData) && is_array($this->oceaneData['relatedResource'])) {
            if (key_exists('resourceCharacteristic', $this->oceaneData['relatedResource'])){
                foreach ($this->oceaneData['relatedResource']['resourceCharacteristic'] as $value) {
                    if (is_array($value) && key_exists('id', $value) && $value['id'] == 'CLASITE') {
```

Question métier : Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #434 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getClasitePrio() — ligne 757
Contexte   :
```php
    public function getClasitePrio(){
        if (key_exists('relatedResource', $this->oceaneData) && is_array($this->oceaneData['relatedResource'])) {
            if (key_exists('resourceCharacteristic', $this->oceaneData['relatedResource'])){
                foreach ($this->oceaneData['relatedResource']['resourceCharacteristic'] as $value) {
                    if (is_array($value) && key_exists('id', $value) && $value['id'] == 'CLASITE') {
                        if (key_exists('value', $value)) {
```

Question métier : Point de décision — key_exists('resourceCharacteristic', 'this'->oceaneData['relatedResource']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #435 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getClasitePrio() — ligne 759
Contexte   :
```php
            if (key_exists('resourceCharacteristic', $this->oceaneData['relatedResource'])){
                foreach ($this->oceaneData['relatedResource']['resourceCharacteristic'] as $value) {
                    if (is_array($value) && key_exists('id', $value) && $value['id'] == 'CLASITE') {
                        if (key_exists('value', $value)) {
                            return $value['value'];
                        }
```

Question métier : Point de décision — is_array('value') et key_exists('id', 'value') et 'value'['id'] égal à 'CLASITE'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #436 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getClasitePrio() — ligne 760
Contexte   :
```php
                foreach ($this->oceaneData['relatedResource']['resourceCharacteristic'] as $value) {
                    if (is_array($value) && key_exists('id', $value) && $value['id'] == 'CLASITE') {
                        if (key_exists('value', $value)) {
                            return $value['value'];
                        }
                    }
```

Question métier : Point de décision — key_exists('value', 'value'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #437 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getRelatedRessource() — ligne 771
Contexte   :
```php
    public function getRelatedRessource()
    {
        if (key_exists('relatedResource', $this->oceaneData) && is_array($this->oceaneData['relatedResource']) && key_exists('resourceSpecCharacteristic', $this->oceaneData['relatedResource'])) {
            return $this->oceaneData['relatedResource']['resourceSpecCharacteristic'][0]['value'];
        }
        return null;
```

Question métier : Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource']) et key_exists('resourceSpecCharacteristic', 'this'->oceaneData['relatedResource']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #444 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : isChild() — ligne 481
Contexte   :
```php
            if (is_array($resultChild) && !empty($resultChild) && !key_exists('code', $resultChild) && key_exists('type', $resultChild[0]) && $resultChild[0]['type'] == 'isParent') {
                return true;
            }
        }
        return false;
```

Question métier : Le code situation 'isParent' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #445 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : isActivationAccpeted() — ligne 599
Contexte   :
```php
                            $activationAccepted = (is_array($status) && key_exists('status', $status) && $status['status'] == 'Accepted' || $status['status'] == 'Completed');
                        }

                    }
                }
```

Question métier : Le code situation 'Accepted' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #446 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : activationIdsAndRoles() — ligne 629
Contexte   :
```php
                            $activationAccepted = (is_array($status) && key_exists('status', $status) && $status['status'] == 'Accepted' || $status['status'] == 'Completed');
                        }
                        if ($activationAccepted) {
                            array_push($eds_code, $party['id']);
                            array_push($eds_nom, $party['label']);
```

Question métier : Le code situation 'Accepted' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #447 — OceaneGet**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : getClasitePrio() — ligne 759
Contexte   :
```php
                    if (is_array($value) && key_exists('id', $value) && $value['id'] == 'CLASITE') {
                        if (key_exists('value', $value)) {
                            return $value['value'];
                        }
                    }
```

Question métier : Le code situation 'CLASITE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #448 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 104
Contexte   :
```php
                $troubleTicketResponse = $result->TroubleTicketResponse->TroubleTicketResponse;

                if (property_exists($troubleTicketResponse->InstalledResource, 'Parameters') && property_exists($troubleTicketResponse->InstalledResource->Parameters, 'Parameter')) {
                    foreach ($troubleTicketResponse->InstalledResource->Parameters->Parameter as $val1) {
                        if (property_exists($val1, 'id') && 'CLASITE' == $val1->id) {
                            $clasitePrio = $val1->value;
```

Question métier : Point de décision — property_exists('troubleTicketResponse'->InstalledResource, 'Parameters') et property_exists('troubleTicketResponse'->InstalledResource->Parameters, 'Parameter'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #449 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 106
Contexte   :
```php
                if (property_exists($troubleTicketResponse->InstalledResource, 'Parameters') && property_exists($troubleTicketResponse->InstalledResource->Parameters, 'Parameter')) {
                    foreach ($troubleTicketResponse->InstalledResource->Parameters->Parameter as $val1) {
                        if (property_exists($val1, 'id') && 'CLASITE' == $val1->id) {
                            $clasitePrio = $val1->value;
                            break;
                        }
```

Question métier : Point de décision — property_exists('val1', 'id') et 'CLASITE' égal à 'val1'->id. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #450 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 125
Contexte   :
```php
                $simulationMaestro = 'n';

                if (property_exists($troubleTicketResponse->TroubleTicketStatus, 'statusCode')) {
                    $status = StringTools::convertEncoding($troubleTicketResponse->TroubleTicketStatus->statusCode, 'ISO-8859-15', 'UTF-8');
                }
                if (property_exists($troubleTicketResponse, 'local_ComplementaryField')) {
```

Question métier : Point de décision — property_exists('troubleTicketResponse'->TroubleTicketStatus, 'statusCode'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #451 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 128
Contexte   :
```php
                    $status = StringTools::convertEncoding($troubleTicketResponse->TroubleTicketStatus->statusCode, 'ISO-8859-15', 'UTF-8');
                }
                if (property_exists($troubleTicketResponse, 'local_ComplementaryField')) {

                    if (is_array($troubleTicketResponse->local_ComplementaryField)) {
                        if (array_key_exists('3', $troubleTicketResponse->local_ComplementaryField) && isset($troubleTicketResponse->local_ComplementaryField[3]->value)) {
```

Question métier : Point de décision — property_exists('troubleTicketResponse', 'local_ComplementaryField'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #452 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 130
Contexte   :
```php
                if (property_exists($troubleTicketResponse, 'local_ComplementaryField')) {

                    if (is_array($troubleTicketResponse->local_ComplementaryField)) {
                        if (array_key_exists('3', $troubleTicketResponse->local_ComplementaryField) && isset($troubleTicketResponse->local_ComplementaryField[3]->value)) {

                            $champComplementaire4 = $troubleTicketResponse->local_ComplementaryField[3]->value;
```

Question métier : Point de décision — is_array('troubleTicketResponse'->local_ComplementaryField). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #453 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 131
Contexte   :
```php

                    if (is_array($troubleTicketResponse->local_ComplementaryField)) {
                        if (array_key_exists('3', $troubleTicketResponse->local_ComplementaryField) && isset($troubleTicketResponse->local_ComplementaryField[3]->value)) {

                            $champComplementaire4 = $troubleTicketResponse->local_ComplementaryField[3]->value;

```

Question métier : Point de décision — array_key_exists('3', 'troubleTicketResponse'->local_ComplementaryField) et isset('troubleTicketResponse'->local_ComplementaryField[3]->value). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #454 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 142
Contexte   :
```php
                        }

                        if (array_key_exists('2', $troubleTicketResponse->local_ComplementaryField) && isset($troubleTicketResponse->local_ComplementaryField[2]->value)) {
                            $typeRessource = $troubleTicketResponse->local_ComplementaryField[2]->value;
                        }

```

Question métier : Point de décision — array_key_exists('2', 'troubleTicketResponse'->local_ComplementaryField) et isset('troubleTicketResponse'->local_ComplementaryField[2]->value). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #455 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 146
Contexte   :
```php
                        }

                        if (array_key_exists('5', $troubleTicketResponse->local_ComplementaryField) && isset($troubleTicketResponse->local_ComplementaryField[5]->value)) {
                            $libelleTechnique = $troubleTicketResponse->local_ComplementaryField[5]->value;
                        }

```

Question métier : Point de décision — array_key_exists('5', 'troubleTicketResponse'->local_ComplementaryField) et isset('troubleTicketResponse'->local_ComplementaryField[5]->value). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #456 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 150
Contexte   :
```php
                        }

                        if (array_key_exists('4', $troubleTicketResponse->local_ComplementaryField) && isset($troubleTicketResponse->local_ComplementaryField[4]->value)) {
                            $codeDetecteur = $troubleTicketResponse->local_ComplementaryField[4]->value;
                        }

```

Question métier : Point de décision — array_key_exists('4', 'troubleTicketResponse'->local_ComplementaryField) et isset('troubleTicketResponse'->local_ComplementaryField[4]->value). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #457 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 157
Contexte   :
```php
                }

                if (property_exists($troubleTicketResponse, 'troubleTicketPriority')) {
                    $priority = StringTools::convertEncoding($troubleTicketResponse->troubleTicketPriority, 'ISO-8859-15', 'UTF-8');
                }

```

Question métier : Point de décision — property_exists('troubleTicketResponse', 'troubleTicketPriority'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #458 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 161
Contexte   :
```php
                }

                if (property_exists($troubleTicketResponse, 'description')) {
                    $description = $troubleTicketResponse->description;
                }
                if (property_exists($troubleTicketResponse, 'local_ShortLabel')) {
```

Question métier : Point de décision — property_exists('troubleTicketResponse', 'description'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #459 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 164
Contexte   :
```php
                    $description = $troubleTicketResponse->description;
                }
                if (property_exists($troubleTicketResponse, 'local_ShortLabel')) {
                    $lbSuccint = $troubleTicketResponse->local_ShortLabel;
                }
                if (property_exists($troubleTicketResponse, 'TroubleCause')) {
```

Question métier : Point de décision — property_exists('troubleTicketResponse', 'local_ShortLabel'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #460 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 167
Contexte   :
```php
                    $lbSuccint = $troubleTicketResponse->local_ShortLabel;
                }
                if (property_exists($troubleTicketResponse, 'TroubleCause')) {
                    if (property_exists($troubleTicketResponse->TroubleCause, 'local_internalcomplement')) {
                        $causeDepassementDelai = $troubleTicketResponse->TroubleCause->local_internalcomplement;
                    }
```

Question métier : Point de décision — property_exists('troubleTicketResponse', 'TroubleCause'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #461 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 168
Contexte   :
```php
                }
                if (property_exists($troubleTicketResponse, 'TroubleCause')) {
                    if (property_exists($troubleTicketResponse->TroubleCause, 'local_internalcomplement')) {
                        $causeDepassementDelai = $troubleTicketResponse->TroubleCause->local_internalcomplement;
                    }
                    if (property_exists($troubleTicketResponse->TroubleCause, 'troubleCauseCodeCategory')) {
```

Question métier : Point de décision — property_exists('troubleTicketResponse'->TroubleCause, 'local_internalcomplement'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #462 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 171
Contexte   :
```php
                        $causeDepassementDelai = $troubleTicketResponse->TroubleCause->local_internalcomplement;
                    }
                    if (property_exists($troubleTicketResponse->TroubleCause, 'troubleCauseCodeCategory')) {
                        $natureFinale = StringTools::convertEncoding($troubleTicketResponse->TroubleCause->troubleCauseCodeCategory, 'ISO-8859-15', 'UTF-8');
                    }
                    if (property_exists($troubleTicketResponse->TroubleCause, 'troubleCauseLabel')) {
```

Question métier : Point de décision — property_exists('troubleTicketResponse'->TroubleCause, 'troubleCauseCodeCategory'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #463 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 174
Contexte   :
```php
                        $natureFinale = StringTools::convertEncoding($troubleTicketResponse->TroubleCause->troubleCauseCodeCategory, 'ISO-8859-15', 'UTF-8');
                    }
                    if (property_exists($troubleTicketResponse->TroubleCause, 'troubleCauseLabel')) {
                        $libelleImputation = $troubleTicketResponse->TroubleCause->troubleCauseLabel;
                    }
                    if (property_exists($troubleTicketResponse->TroubleCause, 'troubleCauseDescription')) {
```

Question métier : Point de décision — property_exists('troubleTicketResponse'->TroubleCause, 'troubleCauseLabel'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #464 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 177
Contexte   :
```php
                        $libelleImputation = $troubleTicketResponse->TroubleCause->troubleCauseLabel;
                    }
                    if (property_exists($troubleTicketResponse->TroubleCause, 'troubleCauseDescription')) {
                        $detailProbleme = StringTools::convertEncoding($troubleTicketResponse->TroubleCause->troubleCauseDescription, 'ISO-8859-1', 'UTF-8');
                    }
                    if (property_exists($troubleTicketResponse->TroubleCause, 'troubleCauseCodeCategory')) {
```

Question métier : Point de décision — property_exists('troubleTicketResponse'->TroubleCause, 'troubleCauseDescription'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #465 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 180
Contexte   :
```php
                        $detailProbleme = StringTools::convertEncoding($troubleTicketResponse->TroubleCause->troubleCauseDescription, 'ISO-8859-1', 'UTF-8');
                    }
                    if (property_exists($troubleTicketResponse->TroubleCause, 'troubleCauseCodeCategory')) {
                        $troubleCauseCodeCategory = StringTools::convertEncoding($troubleTicketResponse->TroubleCause->troubleCauseCodeCategory, 'ISO-8859-1', 'UTF-8');
                    }
                }
```

Question métier : Point de décision — property_exists('troubleTicketResponse'->TroubleCause, 'troubleCauseCodeCategory'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #466 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 185
Contexte   :
```php
                }

                if (property_exists($troubleTicketResponse, 'troubleType')) {
                    $troubleType = StringTools::convertEncoding($troubleTicketResponse->troubleType, 'ISO-8859-1', 'UTF-8');
                }

```

Question métier : Point de décision — property_exists('troubleTicketResponse', 'troubleType'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #467 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 192
Contexte   :
```php

                foreach ($partyRole as $value) {
                    if ($posteAssocie == '') {
                        $posteAssocie = (!empty($value->Party) && isset($value->Party->Local_occupationCode)) ? $value->Party->Local_occupationCode : '';
                    }

```

Question métier : Point de décision — 'posteAssocie' égal à ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #468 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 196
Contexte   :
```php
                    }

                    if (!is_null($connectedEds) && $value->partyRoleType == "TroubleResolutionContributor" && property_exists($value, 'Local_PartyIntervention') && is_array($value->Local_PartyIntervention->interventionStatus)) {
                        $interventionStatus = ($value->Local_PartyIntervention->interventionStatus[0]->status == "Requested" &&
                            $value->Local_PartyIntervention->interventionStatus[1]->status == "Accepted");
                        if (key_exists(2, $value->Local_PartyIntervention->interventionStatus)) {
```

Question métier : Point de décision — !is_null('connectedEds') et 'value'->partyRoleType égal à "TroubleResolutionContributor" et property_exists('value', 'Local_PartyIntervention') et is_array('value'->Local_PartyIntervention->interventionStatus). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #469 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 199
Contexte   :
```php
                        $interventionStatus = ($value->Local_PartyIntervention->interventionStatus[0]->status == "Requested" &&
                            $value->Local_PartyIntervention->interventionStatus[1]->status == "Accepted");
                        if (key_exists(2, $value->Local_PartyIntervention->interventionStatus)) {
                            $interventionStatus = $value->Local_PartyIntervention->interventionStatus[2]->status != 'Completed';
                        }

```

Question métier : Point de décision — key_exists(2, 'value'->Local_PartyIntervention->interventionStatus). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #470 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 215
Contexte   :
```php
                    foreach ($partyRole as $value) {

                        if (!is_null($connectedEds) && $value->partyRoleType == "TroubleResolutionContributor" && property_exists($value, 'Local_PartyIntervention') && is_object($value->Local_PartyIntervention->interventionStatus) && !property_exists($value->Local_PartyIntervention->interventionStatus, 'interventionStatus')) {
                            if ($value->Local_PartyIntervention->interventionStatus->status == 'Requested') {
                                $aacquitte = 1;
                                break;
```

Question métier : Point de décision — !is_null('connectedEds') et 'value'->partyRoleType égal à "TroubleResolutionContributor" et property_exists('value', 'Local_PartyIntervention') et is_object('value'->Local_PartyIntervention->interventionStatus) et !property_exists('value'->Local_PartyIntervention->interventionStatus, 'interventionStatus'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #471 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 216
Contexte   :
```php

                        if (!is_null($connectedEds) && $value->partyRoleType == "TroubleResolutionContributor" && property_exists($value, 'Local_PartyIntervention') && is_object($value->Local_PartyIntervention->interventionStatus) && !property_exists($value->Local_PartyIntervention->interventionStatus, 'interventionStatus')) {
                            if ($value->Local_PartyIntervention->interventionStatus->status == 'Requested') {
                                $aacquitte = 1;
                                break;
                            }
```

Question métier : Point de décision — 'value'->Local_PartyIntervention->interventionStatus->status égal à 'Requested'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #472 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 240
Contexte   :
```php
                $checkIncDate = false;

                if (property_exists($troubleTicketResponse, 'PartyRole')) {
                    $countArr = count($troubleTicketResponse->PartyRole);
                    $inc = range(0, $countArr);
                    foreach ($inc as $i) {
```

Question métier : Point de décision — property_exists('troubleTicketResponse', 'PartyRole'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #473 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 244
Contexte   :
```php
                    $inc = range(0, $countArr);
                    foreach ($inc as $i) {
                        if (!$checkInc) {
                            if (key_exists($i, $troubleTicketResponse->PartyRole) && property_exists($troubleTicketResponse->PartyRole[$i], 'PartyRoleSet')
                                && property_exists($troubleTicketResponse->PartyRole[$i], 'partyRoleType') && $troubleTicketResponse->PartyRole[$i]->partyRoleType == 'TroubleResolutionLeader') {
                                if (property_exists($troubleTicketResponse->PartyRole[$i]->PartyRoleSet, 'local_groupactioninprogress')) {
```

Question métier : Point de décision — !'checkInc'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #474 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 245
Contexte   :
```php
                    foreach ($inc as $i) {
                        if (!$checkInc) {
                            if (key_exists($i, $troubleTicketResponse->PartyRole) && property_exists($troubleTicketResponse->PartyRole[$i], 'PartyRoleSet')
                                && property_exists($troubleTicketResponse->PartyRole[$i], 'partyRoleType') && $troubleTicketResponse->PartyRole[$i]->partyRoleType == 'TroubleResolutionLeader') {
                                if (property_exists($troubleTicketResponse->PartyRole[$i]->PartyRoleSet, 'local_groupactioninprogress')) {
                                    $checkIncAct = true;
```

Question métier : Point de décision — key_exists('i', 'troubleTicketResponse'->PartyRole) et property_exists('troubleTicketResponse'->PartyRole['i'], 'PartyRoleSet') et property_exists('troubleTicketResponse'->PartyRole['i'], 'partyRoleType') et 'troubleTicketResponse'->PartyRole['i']->partyRoleType égal à 'TroubleResolutionLeader'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #475 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 247
Contexte   :
```php
                            if (key_exists($i, $troubleTicketResponse->PartyRole) && property_exists($troubleTicketResponse->PartyRole[$i], 'PartyRoleSet')
                                && property_exists($troubleTicketResponse->PartyRole[$i], 'partyRoleType') && $troubleTicketResponse->PartyRole[$i]->partyRoleType == 'TroubleResolutionLeader') {
                                if (property_exists($troubleTicketResponse->PartyRole[$i]->PartyRoleSet, 'local_groupactioninprogress')) {
                                    $checkIncAct = true;
                                    $actionEnCours = $troubleTicketResponse->PartyRole[$i]->PartyRoleSet->local_groupactioninprogress;
                                    $edsActionEnCours = $troubleTicketResponse->PartyRole[$i]->PartyRoleSet->partyRoleSetID;
```

Question métier : Point de décision — property_exists('troubleTicketResponse'->PartyRole['i']->PartyRoleSet, 'local_groupactioninprogress'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #476 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 253
Contexte   :
```php

                                }
                                if (property_exists($troubleTicketResponse->PartyRole[$i]->PartyRoleSet, 'local_groupactioninprogressdate')) {
                                    $checkIncDate = true;
                                    $dateActionEnCours = $troubleTicketResponse->PartyRole[$i]->PartyRoleSet->local_groupactioninprogressdate;
                                    $edsActionEnCours = $troubleTicketResponse->PartyRole[$i]->PartyRoleSet->partyRoleSetID;
```

Question métier : Point de décision — property_exists('troubleTicketResponse'->PartyRole['i']->PartyRoleSet, 'local_groupactioninprogressdate'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #477 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 258
Contexte   :
```php
                                    $edsActionEnCours = $troubleTicketResponse->PartyRole[$i]->PartyRoleSet->partyRoleSetID;
                                }
                                if ($checkIncDate && $checkIncAct) {
                                    $checkInc = true;
                                }
                                break;
```

Question métier : Point de décision — 'checkIncDate' et 'checkIncAct'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #478 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 266
Contexte   :
```php
                    }
                }
                if (property_exists($troubleTicketResponse, 'local_onbhfollowup')) {
                    $hno = 1;
                }

```

Question métier : Point de décision — property_exists('troubleTicketResponse', 'local_onbhfollowup'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #479 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : findAndGetOceane() — ligne 270
Contexte   :
```php
                }

                if (property_exists($troubleTicketResponse, 'troubleTicketCategory')) {
                    $evtIncident = $troubleTicketResponse->troubleTicketCategory;
                }

```

Question métier : Point de décision — property_exists('troubleTicketResponse', 'troubleTicketCategory'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #480 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 382
Contexte   :
```php
            $values['TROUBLE_TICKET_PRIORITY'] = '0';
        }
        if (array_key_exists('ticket_id', $data) && isset($data['ticket_id'])) {
            $values['ticketId'] = $data['ticket_id'];
        }

```

Question métier : Point de décision — array_key_exists('ticket_id', 'data') et isset('data'['ticket_id']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #481 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 386
Contexte   :
```php
        }

        if (array_key_exists('astroid', $data) && isset($data['astroid'])) {
            $values['astroid'] = $data['astroid'];
        }

```

Question métier : Point de décision — array_key_exists('astroid', 'data') et isset('data'['astroid']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #482 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 390
Contexte   :
```php
        }

        if (array_key_exists('party_role_party_ID', $data) && isset($data['party_role_party_ID'])) {
            $values['PARTYROLE_PARTY_ID'] = $data['party_role_party_ID'];
        }

```

Question métier : Point de décision — array_key_exists('party_role_party_ID', 'data') et isset('data'['party_role_party_ID']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #483 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 394
Contexte   :
```php
        }

        if (array_key_exists('postes_associe', $data) && isset($data['postes_associe'])) {
            $values['POSTE_ASSOCIE_ID'] = $data['postes_associe'];
        }

```

Question métier : Point de décision — array_key_exists('postes_associe', 'data') et isset('data'['postes_associe']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #484 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 398
Contexte   :
```php
        }

        if (array_key_exists('niv_urgence', $data) && isset($data['niv_urgence'])) {
            $values['NIV_URGENCE_ID'] = $data['niv_urgence'];
        }

```

Question métier : Point de décision — array_key_exists('niv_urgence', 'data') et isset('data'['niv_urgence']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #485 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 402
Contexte   :
```php
        }

        if (array_key_exists('action_eds', $data) && isset($data['action_eds'])) {
            $values['ACTION_EDS_IN_PROGRESS'] = $data['action_eds'];
        }

```

Question métier : Point de décision — array_key_exists('action_eds', 'data') et isset('data'['action_eds']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #486 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 406
Contexte   :
```php
        }

        if (array_key_exists('commentaire_eds', $data) && isset($data['commentaire_eds'])) {
            $values['LOCAL_COMEMENTAIRE'] = $data['commentaire_eds'];
        }

```

Question métier : Point de décision — array_key_exists('commentaire_eds', 'data') et isset('data'['commentaire_eds']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #487 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 410
Contexte   :
```php
        }

        if (array_key_exists('eds_pilote', $data) && isset($data['eds_pilote'])) {
            $values['EDS_PILOTE'] = $data['eds_pilote'];
        }
        $values['party_id'] = $login;
```

Question métier : Point de décision — array_key_exists('eds_pilote', 'data') et isset('data'['eds_pilote']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #488 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 420
Contexte   :
```php
            case 'MAJ_PRIORITE_COMMENTAIRE':

                if (array_key_exists('local_commentaire', $data) && isset($data['local_commentaire'])) {
                    $values['LOCAL_COMEMENTAIRE'] = $data['local_commentaire'];
                }
                if (array_key_exists('nb_plaintes', $data) && isset($data['nb_plaintes'])) {
```

Question métier : Point de décision — array_key_exists('local_commentaire', 'data') et isset('data'['local_commentaire']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #489 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 423
Contexte   :
```php
                    $values['LOCAL_COMEMENTAIRE'] = $data['local_commentaire'];
                }
                if (array_key_exists('nb_plaintes', $data) && isset($data['nb_plaintes'])) {
                    $values['LOCAL_SIGNALISATION_NUMBER'] = intval($data['nb_plaintes']);
                }
                $result = json_decode($oceaneApi->updateMobileMajPrioriteCommentaire($oceaneApiData['url'], $values['ticketId']), true);
```

Question métier : Point de décision — array_key_exists('nb_plaintes', 'data') et isset('data'['nb_plaintes']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #490 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 433
Contexte   :
```php
            case 'MAJ_PRIORITE_IMPACT_RESSOURCES':

                if (array_key_exists('description', $data) && isset($data['description'])) {
                    $values['DESCRIPTION'] = StringTools::convertEncoding($data['description'], 'ISO-8859-15', 'UTF-8');
                }
                if (array_key_exists('trouble_type', $data) && isset($data['trouble_type'])) {
```

Question métier : Point de décision — array_key_exists('description', 'data') et isset('data'['description']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #491 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 436
Contexte   :
```php
                    $values['DESCRIPTION'] = StringTools::convertEncoding($data['description'], 'ISO-8859-15', 'UTF-8');
                }
                if (array_key_exists('trouble_type', $data) && isset($data['trouble_type'])) {
                    $values['TROUBLE_TYPE'] = $data['trouble_type'];
                }
                if (array_key_exists('trouble_severity', $data) && isset($data['trouble_severity'])) {
```

Question métier : Point de décision — array_key_exists('trouble_type', 'data') et isset('data'['trouble_type']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #492 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 439
Contexte   :
```php
                    $values['TROUBLE_TYPE'] = $data['trouble_type'];
                }
                if (array_key_exists('trouble_severity', $data) && isset($data['trouble_severity'])) {
                    $values['TROUBLE_SEVERITY'] = $data['trouble_severity'];
                }
                if (array_key_exists('party_set_ID', $data) && isset($data['party_set_ID'])) {
```

Question métier : Point de décision — array_key_exists('trouble_severity', 'data') et isset('data'['trouble_severity']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #493 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 442
Contexte   :
```php
                    $values['TROUBLE_SEVERITY'] = $data['trouble_severity'];
                }
                if (array_key_exists('party_set_ID', $data) && isset($data['party_set_ID'])) {
                    $values['PARTY_SET_ID'] = $data['party_set_ID'];
                }

```

Question métier : Point de décision — array_key_exists('party_set_ID', 'data') et isset('data'['party_set_ID']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #494 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 446
Contexte   :
```php
                }

                if (array_key_exists('requested_date', $data) && isset($data['requested_date'])) {
                    $values['REQUESTED_DATE'] = $data['requested_date'];
                    $requestedDate = strtotime($data['requested_date']);
                    $values['requestedRestorationDateZulu'] = gmdate('Y-m-d\TH:i:s\Z', $requestedDate);
```

Question métier : Point de décision — array_key_exists('requested_date', 'data') et isset('data'['requested_date']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #495 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 483
Contexte   :
```php
            // Mise à jour de la priorité et l'impact client
            case 'MAJ_PRIORITE_IMPACT':
                if (array_key_exists('description', $data) && isset($data['description'])) {
                    $values['DESCRIPTION'] = StringTools::convertEncoding($data['description'], 'ISO-8859-15', 'UTF-8');
                }
                if (array_key_exists('trouble_type', $data) && isset($data['trouble_type'])) {
```

Question métier : Point de décision — array_key_exists('description', 'data') et isset('data'['description']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #496 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 486
Contexte   :
```php
                    $values['DESCRIPTION'] = StringTools::convertEncoding($data['description'], 'ISO-8859-15', 'UTF-8');
                }
                if (array_key_exists('trouble_type', $data) && isset($data['trouble_type'])) {
                    $values['TROUBLE_TYPE'] = $data['trouble_type'];
                }
                if (array_key_exists('trouble_severity', $data) && isset($data['trouble_severity'])) {
```

Question métier : Point de décision — array_key_exists('trouble_type', 'data') et isset('data'['trouble_type']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #497 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 489
Contexte   :
```php
                    $values['TROUBLE_TYPE'] = $data['trouble_type'];
                }
                if (array_key_exists('trouble_severity', $data) && isset($data['trouble_severity'])) {
                    $values['TROUBLE_SEVERITY'] = $data['trouble_severity'];
                }
                if (array_key_exists('party_set_ID', $data) && isset($data['party_set_ID'])) {
```

Question métier : Point de décision — array_key_exists('trouble_severity', 'data') et isset('data'['trouble_severity']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #498 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceane() — ligne 492
Contexte   :
```php
                    $values['TROUBLE_SEVERITY'] = $data['trouble_severity'];
                }
                if (array_key_exists('party_set_ID', $data) && isset($data['party_set_ID'])) {
                    $values['PARTY_SET_ID'] = $data['party_set_ID'];
                }
                $result = json_decode($oceaneApi->updateMobileMajPrioriteImpact($oceaneApiData['url'], $values['ticketId'], $values), true);
```

Question métier : Point de décision — array_key_exists('party_set_ID', 'data') et isset('data'['party_set_ID']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #499 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceaneConfirmer() — ligne 517
Contexte   :
```php
        $oceaneAssistant = new OceaneAssistant($this->app);
        $actifDri = key_exists('actif_dri', $data) ? $data['actif_dri'] : '';
        if (!$generique) {
            $data['nature_impact_client'] = $this->astroIhmSqlRepository->getImpactClientOceane($data['nature_impact_client']);
        }
        $typeConfirmation = (key_exists('hidden_type_confirmation', $data) && !is_null($data['hidden_type_confirmation'])) ? $data['hidden_type_confirmation'] : 'TYPE1';
```

Question métier : Point de décision — !'generique'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #500 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceaneConfirmer() — ligne 535
Contexte   :
```php
        );
        // Enchainement param OU IHM OU Enchainement LEGACY
        if ($actifDri) {
            $v['requestedRestorationDate'] = $dateRetablissementUTC;
        }

```

Question métier : Point de décision — 'actifDri'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #501 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceaneConfirmerTrans() — ligne 622
Contexte   :
```php

        );
        if ($data['donnee_complementaire'] != '') {
            $dataUpdate['name'] = $data['donnee_complementaire'];
        }
        if (($actifDri == '1') || (key_exists('api', $this->app->config) && $this->app->config['api'])) {
```

Question métier : Point de décision — 'data'['donnee_complementaire'] différent de ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #502 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceaneConfirmerTrans() — ligne 625
Contexte   :
```php
            $dataUpdate['name'] = $data['donnee_complementaire'];
        }
        if (($actifDri == '1') || (key_exists('api', $this->app->config) && $this->app->config['api'])) {
            $dataUpdate['targetRestorationDate'] = $dateRetablissementUTCZulu;
            $dataUpdate['detectionDate'] = $dateDebutIncidentUTCZulu;
        }
```

Question métier : Point de décision — ('actifDri' égal à '1') ou (key_exists('api', 'this'->app->config) et 'this'->app->config['api']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #503 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceaneConfirmerTrans() — ligne 646
Contexte   :
```php
            }
        } else {
            if(!key_exists('api', $data))
            {
                $dataUpdate['detectionDate'] = $dateDebutIncidentUTCZulu;
            }
```

Question métier : Point de décision — !key_exists('api', 'data'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #504 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceaneConfirmerTrans() — ligne 630
Contexte   :
```php
        }

        if ($confirmTowStep == 'oui') {
            $dataUpdateFirstStep = array(
                'detectionDate' => $dateDebutIncidentUTCZulu
            );
```

Question métier : Valeur de référence non documentée — La décision « 'confirmTowStep' égal à 'oui' » repose sur la valeur 'oui'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #517 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceaneConfirmer() — ligne 528
Contexte   :
```php
            'localCommentLabel' => ($typeConfirmation === 'TYPE2') ? $comments : $this->createComment($data),
            'localCommentPartyID' => $loginUser,
            'partyRolePartyID' => $loginUser,
            'tagHNO' => (key_exists('hno', $data)) ? (bool)$data['hno'] : '0',
            'troubleTicketPriority' => $data['priorite'],
```

Question métier : Le code situation 'TYPE2' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #518 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceaneConfirmerTrans() — ligne 625
Contexte   :
```php
        if (($actifDri == '1') || (key_exists('api', $this->app->config) && $this->app->config['api'])) {
            $dataUpdate['targetRestorationDate'] = $dateRetablissementUTCZulu;
            $dataUpdate['detectionDate'] = $dateDebutIncidentUTCZulu;
        }

```

Question métier : Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #519 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : updateOceaneConfirmerTrans() — ligne 630
Contexte   :
```php
        if ($confirmTowStep == 'oui') {
            $dataUpdateFirstStep = array(
                'detectionDate' => $dateDebutIncidentUTCZulu
            );
            $this->app->get('TraceRepository')->setTrace($astroId, "ENVOI OCEANE CONFIRMER TRANS 1 STEP", $dataUpdateFirstStep, $this->sessId, $ticketId);
```

Question métier : Le code situation 'oui' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #520 — Oceane**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : createComment() — ligne 732
Contexte   :
```php
            if ($data['priorite_commentaire'] == '4') {
                $priorityComment .= ($data['commentaire1']);
            } else {
                $priorityComment .= StringTools::convertEncoding($data['priorite_commentaire'], 'ISO-8859-15', 'UTF-8');
            }
```

Question métier : Le code situation '4' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #531 — VariableBase**

**→ Copier dans Copilot**

Fichier    : VariableBaseService.php
Méthode    : ligne 27
Contexte   :
```php
    {
        $this->app = $app;
        if (is_null($this->findAndGet)) {
            $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
        }
    }
```

Question métier : Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #532 — VariableBase**

**→ Copier dans Copilot**

Fichier    : VariableBaseService.php
Méthode    : getVariableAdminValue() — ligne 39
Contexte   :
```php
            switch ($identifiant['SOURCE_GLOBALE']) {
                case 'PARAMETRE':
                    if (property_exists($this->findAndGet['installed_resource']->Parameters, 'Parameter')) {
                        $res = OceaneTools::searchValueInFindAndGet($identifiant['SOURCE'], $this->findAndGet['installed_resource']->Parameters->Parameter);
                        $res = ($identifiant['MIN_MAJ'] == "MIN") ? strtolower($res) : strtoupper($res);
                        if (!is_null($res)) {
```

Question métier : Point de décision — property_exists('this'->findAndGet['installed_resource']->Parameters, 'Parameter'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #533 — VariableBase**

**→ Copier dans Copilot**

Fichier    : VariableBaseService.php
Méthode    : getVariableAdminValue() — ligne 42
Contexte   :
```php
                        $res = OceaneTools::searchValueInFindAndGet($identifiant['SOURCE'], $this->findAndGet['installed_resource']->Parameters->Parameter);
                        $res = ($identifiant['MIN_MAJ'] == "MIN") ? strtolower($res) : strtoupper($res);
                        if (!is_null($res)) {
                            return $res;
                        }
                    }
```

Question métier : Point de décision — !is_null('res'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #534 — VariableBase**

**→ Copier dans Copilot**

Fichier    : VariableBaseService.php
Méthode    : getVariableAdminValue() — ligne 48
Contexte   :
```php
                    break;
                case 'ATTRIBUT':
                    if (property_exists($this->findAndGet['installed_resource']->Attributes, 'Attribute')) {
                        $res = OceaneTools::searchValueInFindAndGet($identifiant['SOURCE'], $this->findAndGet['installed_resource']->Attributes->Attribute);
                        $res = ($identifiant['MIN_MAJ'] == "MIN") ? strtolower($res) : strtoupper($res);
                        if (!is_null($res)) {
```

Question métier : Point de décision — property_exists('this'->findAndGet['installed_resource']->Attributes, 'Attribute'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #535 — VariableBase**

**→ Copier dans Copilot**

Fichier    : VariableBaseService.php
Méthode    : getVariableAdminValue() — ligne 51
Contexte   :
```php
                        $res = OceaneTools::searchValueInFindAndGet($identifiant['SOURCE'], $this->findAndGet['installed_resource']->Attributes->Attribute);
                        $res = ($identifiant['MIN_MAJ'] == "MIN") ? strtolower($res) : strtoupper($res);
                        if (!is_null($res)) {
                            return $res;
                        }
                    }
```

Question métier : Point de décision — !is_null('res'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #536 — VariableBase**

**→ Copier dans Copilot**

Fichier    : VariableBaseService.php
Méthode    : getVariableAdminValue() — ligne 59
Contexte   :
```php
                    $res = $this->adminFonction->getDataFromId($identifiant, $this->ticketId);
                    $res = ($identifiant['MIN_MAJ'] == "MIN") ? strtolower($res) : strtoupper($res);
                    if (!is_null($res)) {
                        return $res;
                    }
                    break;
```

Question métier : Point de décision — !is_null('res'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #537 — VariableBase**

**→ Copier dans Copilot**

Fichier    : VariableBaseService.php
Méthode    : ligne 79
Contexte   :
```php
    {
        $monDslam = false;
        if ($this->id1) {
            $dslam = substr($this->id1, 0, 8);
            switch ($type) {
                case 'MAJ':
```

Question métier : Point de décision — 'this'->id1. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #540 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 123
Contexte   :
```php
        $donnesTempsReel = array();
        foreach ($args as $arg) {
            if ($arg == 'Temperature' || $arg == 'Etat_batterie' || $arg == 'Tension_batterie' || $arg == 'Element_HS') {
                $traceData = array(
                    'astro_id' => $this->astroId,
                    'ticket_id' => $this->ticketId,
```

Question métier : Point de décision — 'arg' égal à 'Temperature' ou 'arg' égal à 'Etat_batterie' ou 'arg' égal à 'Tension_batterie' ou 'arg' égal à 'Element_HS'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #541 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 131
Contexte   :
```php
                $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
                $parameters = (key_exists('installed_resource', $this->findAndGet) && property_exists($this->findAndGet['installed_resource'], 'Parameters')) ? $this->findAndGet['installed_resource']->Parameters : array();
                if (property_exists($parameters, 'Parameter')) {
                    foreach ($parameters->Parameter as $val1) {
                        if (property_exists($val1, 'id') && $val1->id == 'LIBSITE') {
                            $libSite = $val1->value;
```

Question métier : Point de décision — property_exists('parameters', 'Parameter'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #542 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 133
Contexte   :
```php
                if (property_exists($parameters, 'Parameter')) {
                    foreach ($parameters->Parameter as $val1) {
                        if (property_exists($val1, 'id') && $val1->id == 'LIBSITE') {
                            $libSite = $val1->value;
                        }
                    }
```

Question métier : Point de décision — property_exists('val1', 'id') et 'val1'->id égal à 'LIBSITE'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #543 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 137
Contexte   :
```php
                        }
                    }
                    if ($libSite != "") {
                        $donnesTempsReel = $this->app->get('Cia')->getDataSite($libSite, $traceData);
                    }
                }
```

Question métier : Point de décision — 'libSite' différent de "". Quel est le comportement attendu dans le cas contraire ?

---

**Gap #544 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 142
Contexte   :
```php
                }
            }
            if ($arg == 'DSLAM_PRODUIT_DSLAM' || $arg == 'DSLAM_PRODUIT_CHASSIS' || $arg == 'DSLAM_PRODUIT_CARTE' || $arg == 'DSLAM_PRODUIT_PORT' || $arg == 'DSLAM_PRODUIT_PM') {
                if (is_null($this->variableRepository)) {
                    $this->variableRepository = $this->app->get('VariableRepository');
                }
```

Question métier : Point de décision — 'arg' égal à 'DSLAM_PRODUIT_DSLAM' ou 'arg' égal à 'DSLAM_PRODUIT_CHASSIS' ou 'arg' égal à 'DSLAM_PRODUIT_CARTE' ou 'arg' égal à 'DSLAM_PRODUIT_PORT' ou 'arg' égal à 'DSLAM_PRODUIT_PM'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #545 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 143
Contexte   :
```php
            }
            if ($arg == 'DSLAM_PRODUIT_DSLAM' || $arg == 'DSLAM_PRODUIT_CHASSIS' || $arg == 'DSLAM_PRODUIT_CARTE' || $arg == 'DSLAM_PRODUIT_PORT' || $arg == 'DSLAM_PRODUIT_PM') {
                if (is_null($this->variableRepository)) {
                    $this->variableRepository = $this->app->get('VariableRepository');
                }
                $replaceValue = $this->variableRepository->getVarsNonAdministree($this->ticketId, $arg);
```

Question métier : Point de décision — is_null('this'->variableRepository). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #546 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 147
Contexte   :
```php
                }
                $replaceValue = $this->variableRepository->getVarsNonAdministree($this->ticketId, $arg);
                if (!$replaceValue) {
                    $replaceValue = $this->app->get('AssistantService')->getInfoTicketAdeliaByPrestation($this->ticketId, $arg);
                    if ($replaceValue != '' && !is_null($replaceValue) && !is_array($replaceValue)) {
                        $this->variableRepository->insertVarsNonAdministree($this->ticketId, $arg, $replaceValue);
```

Question métier : Point de décision — !'replaceValue'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #547 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 149
Contexte   :
```php
                if (!$replaceValue) {
                    $replaceValue = $this->app->get('AssistantService')->getInfoTicketAdeliaByPrestation($this->ticketId, $arg);
                    if ($replaceValue != '' && !is_null($replaceValue) && !is_array($replaceValue)) {
                        $this->variableRepository->insertVarsNonAdministree($this->ticketId, $arg, $replaceValue);
                    }
                }
```

Question métier : Point de décision — 'replaceValue' différent de '' et !is_null('replaceValue') et !is_array('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #548 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 153
Contexte   :
```php
                    }
                }
                if (OceaneTools::isValidVariable($replaceValue) && !is_array($replaceValue)) {
                    $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue') et !is_array('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #549 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 165
Contexte   :
```php
                case 'transitool_tronc_longueur':
                case 'transitool_tronc_paire':
                    if (is_null($this->transitoolService)) {
                        $this->transitoolService = $this->app->get('Transitool');
                    }

```

Question métier : Point de décision — is_null('this'->transitoolService). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #550 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 171
Contexte   :
```php
                    $replaceValue = $this->transitoolService->getValueTronconTransitool($arg, $this->id3, $this->typeRessource, $this->astroId);

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #551 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 178
Contexte   :
```php
                case 'CUID':
                    $replaceValue = (!is_null($this->loginId)) ? $this->loginId : '';
                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #552 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 185
Contexte   :
```php
                    $replaceValue = (!is_null($this->ticketId)) ? $this->ticketId : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #553 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 195
Contexte   :
```php
                    break;
                case 'Etat_batterie':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {

                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['mode_fonctionnement_batterie'], $chaine);
```

Question métier : Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #554 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 203
Contexte   :
```php
                    break;
                case 'Element_HS':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {
                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['element_equipement_panne_tronc'], $chaine);
                    }
```

Question métier : Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #555 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 210
Contexte   :
```php
                    break;
                case 'Tension_batterie':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {
                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['tension'], $chaine);
                    }
```

Question métier : Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #556 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 217
Contexte   :
```php
                    break;
                case 'Temperature':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {
                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['temperature'], $chaine);
                    }
```

Question métier : Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #557 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 226
Contexte   :
```php
                    $replaceValue = (!is_null($this->getCodeNidt())) ? $this->getCodeNidt() : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #558 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 234
Contexte   :
```php
                    $replaceValue = (!is_null($this->getDslam('MAJ'))) ? $this->getDslam('MAJ') : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #559 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 242
Contexte   :
```php
                    $replaceValue = (!is_null($this->getDslam('MIN'))) ? $this->getDslam('MIN') : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #560 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 251
Contexte   :
```php
                    $replaceValue = (!is_null($this->eds)) ? $this->eds : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #561 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 259
Contexte   :
```php
                    $replaceValue = (!is_null($this->typeRessource)) ? $this->typeRessource : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #562 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 270
Contexte   :
```php

                case 'DATE':
                    if (is_null($this->findAndGet)) {
                        $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
                    }

```

Question métier : Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #563 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 276
Contexte   :
```php
                    $replaceValue = isset($this->findAndGet['fg_date']) ? $this->findAndGet['fg_date'] : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #564 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 284
Contexte   :
```php
                case 'FG_E1NOMNAEQP':
                case 'FG_E2NOMNAEQP':
                    if (is_null($this->findAndGet)) {
                        $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
                    }
                    if (!isset($this->findAndGet['message']) && !is_null($this->findAndGet['installed_resource']) && property_exists($this->findAndGet['installed_resource'],
```

Question métier : Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #565 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 287
Contexte   :
```php
                        $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
                    }
                    if (!isset($this->findAndGet['message']) && !is_null($this->findAndGet['installed_resource']) && property_exists($this->findAndGet['installed_resource'],
                            'Parameters') && property_exists($this->findAndGet['installed_resource']->Parameters, 'Parameter')) {
                        $result = OceaneTools::searchValueInFindAndGet(substr($arg, 3), $this->findAndGet['installed_resource']->Parameters->Parameter);
                        $replaceValue = (!is_null($result)) ? $result : '';
```

Question métier : Point de décision — !isset('this'->findAndGet['message']) et !is_null('this'->findAndGet['installed_resource']) et property_exists('this'->findAndGet['installed_resource'], 'Parameters') et property_exists('this'->findAndGet['installed_resource']->Parameters, 'Parameter'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #566 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 291
Contexte   :
```php
                        $result = OceaneTools::searchValueInFindAndGet(substr($arg, 3), $this->findAndGet['installed_resource']->Parameters->Parameter);
                        $replaceValue = (!is_null($result)) ? $result : '';
                        if (OceaneTools::isValidVariable($replaceValue)) {
                            $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                        }
                    }
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #567 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 297
Contexte   :
```php
                    break;
                case 'RD3+':
                    if (is_null($this->findAndGet)) {
                        $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
                    }

```

Question métier : Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #568 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 301
Contexte   :
```php
                    }

                    if (!isset($this->findAndGet['message']) && !is_null($this->findAndGet['rd_plus'])) {
                        $replaceValue = (!is_null($this->findAndGet['rd_plus'])) ? $this->findAndGet['rd_plus'] : null;

                        if (OceaneTools::isValidVariable($replaceValue)) {
```

Question métier : Point de décision — !isset('this'->findAndGet['message']) et !is_null('this'->findAndGet['rd_plus']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #569 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 304
Contexte   :
```php
                        $replaceValue = (!is_null($this->findAndGet['rd_plus'])) ? $this->findAndGet['rd_plus'] : null;

                        if (OceaneTools::isValidVariable($replaceValue)) {
                            $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                        }
                    }
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #570 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 310
Contexte   :
```php
                    break;
                case 'DESCRIPTION':
                    if (is_null($this->findAndGet)) {
                        $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
                    }

```

Question métier : Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #571 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 314
Contexte   :
```php
                    }

                    if (!isset($this->findAndGet['message']) && !is_null($this->findAndGet['description'])) {
                        $replaceValue = (!is_null($this->findAndGet['description'])) ? $this->findAndGet['description'] : null;

                        if (OceaneTools::isValidVariable($replaceValue)) {
```

Question métier : Point de décision — !isset('this'->findAndGet['message']) et !is_null('this'->findAndGet['description']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #572 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 317
Contexte   :
```php
                        $replaceValue = (!is_null($this->findAndGet['description'])) ? $this->findAndGet['description'] : null;

                        if (OceaneTools::isValidVariable($replaceValue)) {
                            $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                        }
                    }
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #573 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 323
Contexte   :
```php
                    break;
                case 'Intervenant_EVT':
                    if (is_null($this->findAndGet)) {
                        $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
                    }
                    if (!isset($this->findAndGet['message']) && !is_null($this->findAndGet['code_detecteur'])) {
```

Question métier : Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #574 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 326
Contexte   :
```php
                        $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
                    }
                    if (!isset($this->findAndGet['message']) && !is_null($this->findAndGet['code_detecteur'])) {
                        if (!is_null($this->findAndGet['code_detecteur'])) {
                            $replaceValue = ($this->findAndGet['code_detecteur'] != "ORANGE") ? $this->findAndGet['code_detecteur'] : "UI";
                        } else {
```

Question métier : Point de décision — !isset('this'->findAndGet['message']) et !is_null('this'->findAndGet['code_detecteur']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #575 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 333
Contexte   :
```php
                        }

                        if (OceaneTools::isValidVariable($replaceValue)) {
                            $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                        }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #576 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 353
Contexte   :
```php
                    }

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);

                    }
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #577 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 375
Contexte   :
```php
                    $replaceValue = $this->refSiteRepository->getRefsiteColumn($arrayRefSite[$arg], $ticketId);

                    if (OceaneTools::isValidVariable($replaceValue) && gettype($replaceValue) != 'boolean') {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue') et gettype('replaceValue') différent de 'boolean'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #578 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 402
Contexte   :
```php
                    break;
                case 'PRIMO_AIGUILLAGE_TRONCON':
                    if ($this->typeRessource == 'TRONCABLE') {

                        $replaceValue = $this->replaceTagsChainePrimoAiguillageTroncon($ticketId);
                        if (OceaneTools::isValidVariable($replaceValue)) {
```

Question métier : Point de décision — 'this'->typeRessource égal à 'TRONCABLE'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #579 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 405
Contexte   :
```php

                        $replaceValue = $this->replaceTagsChainePrimoAiguillageTroncon($ticketId);
                        if (OceaneTools::isValidVariable($replaceValue)) {
                            $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                        }
                        break;
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #580 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 415
Contexte   :
```php

                    $replaceValue = '';
                    if (!is_null($resultColumn) && $resultColumn != '') {
                        $replaceValue = ($resultColumn == 'ORANGE') ? 'Non' : 'Oui';
                    }
                    if (OceaneTools::isValidVariable($replaceValue)) {
```

Question métier : Point de décision — !is_null('resultColumn') et 'resultColumn' différent de ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #581 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 418
Contexte   :
```php
                        $replaceValue = ($resultColumn == 'ORANGE') ? 'Non' : 'Oui';
                    }
                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #582 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 424
Contexte   :
```php
                default:
                    $this->globalApiRepository = $this->app->get('GlobalApiRepository');
                    if ($this->globalApiRepository->isVariableAdminExist($arg, $type)) {

                        if (is_null($this->findAndGet)) {
                            $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
```

Question métier : Point de décision — 'this'->globalApiRepository->isVariableAdminExist('arg', 'type'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #583 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 426
Contexte   :
```php
                    if ($this->globalApiRepository->isVariableAdminExist($arg, $type)) {

                        if (is_null($this->findAndGet)) {
                            $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
                        }
                        if (!isset($this->findAndGet['message'])) {
```

Question métier : Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #584 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 429
Contexte   :
```php
                            $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
                        }
                        if (!isset($this->findAndGet['message'])) {

                            if (!is_null($this->findAndGet['installed_resource']) && property_exists($this->findAndGet['installed_resource'], 'ResourceSpecification') && property_exists($this->findAndGet['installed_resource']->ResourceSpecification,
                                    'resourceSpecificationCode')) {
```

Question métier : Point de décision — !isset('this'->findAndGet['message']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #585 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 440
Contexte   :
```php


                            if ($resourceSpecification != "") {
                                $data = array(
                                    'type' => $resourceSpecification,
                                    'nom' => $arg
```

Question métier : Point de décision — 'resourceSpecification' différent de "". Quel est le comportement attendu dans le cas contraire ?

---

**Gap #586 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 446
Contexte   :
```php
                                );
                                $tabIdentifiants = $this->globalApiRepository->getIdentifiantsAdmin($data);
                                if (count($tabIdentifiants) > 0) {
                                    $replaceValue = $this->getVariableAdminValue($tabIdentifiants);
                                    if (isset($replaceValue)) {
                                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
```

Question métier : Point de décision — count('tabIdentifiants') > 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #587 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 448
Contexte   :
```php
                                if (count($tabIdentifiants) > 0) {
                                    $replaceValue = $this->getVariableAdminValue($tabIdentifiants);
                                    if (isset($replaceValue)) {
                                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                                    }
                                }
```

Question métier : Point de décision — isset('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #588 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : selectExtension() — ligne 489
Contexte   :
```php
        // actif=>0, passif=>1

        if ($ext1_status == 0) {
            return $ext1;
        }
        // Si EXT1 est passif et EXT2 est actif
```

Question métier : Point de décision — 'ext1_status' égal à 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #589 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : selectExtension() — ligne 493
Contexte   :
```php
        }
        // Si EXT1 est passif et EXT2 est actif
        if ($ext1_status == 1 && $ext2_status == 0) {
            return $ext2;
        }
        // si EXT1 n'existe pas sur refsites
```

Question métier : Point de décision — 'ext1_status' égal à 1 et 'ext2_status' égal à 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #590 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : selectExtension() — ligne 497
Contexte   :
```php
        }
        // si EXT1 n'existe pas sur refsites
        if($ext1_status == -1){
            return $ext2;
        }
        // si EXT2 n'existe pas sur refsites
```

Question métier : Point de décision — 'ext1_status' égal à -1. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #591 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : selectExtension() — ligne 501
Contexte   :
```php
        }
        // si EXT2 n'existe pas sur refsites
        if($ext2_status == -1) {
            return $ext1;
        }
        // Dans tous les autres cas, on retourne EXT1
```

Question métier : Point de décision — 'ext2_status' égal à -1. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #592 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : getIntervenant() — ligne 527
Contexte   :
```php
        }

        if ($intervenantMatriceRefsite != "###$variableAdministree###") {
            switch ($typeRessource) {
                case 'CA-CASW':
                case 'S-SUP':
```

Question métier : Point de décision — 'intervenantMatriceRefsite' différent de "###'variableAdministree'###". Quel est le comportement attendu dans le cas contraire ?

---

**Gap #593 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : getIntervenant() — ligne 594
Contexte   :
```php
        if (gettype($resultQuery) != 'boolean' && $resultQuery != '' && is_array($resultQuery)) {
            $intervenant = key_exists('INTERVENANT', $resultQuery) ? $resultQuery['INTERVENANT'] : '';
            if (key_exists('ID', $resultQuery)) {
                $this->refSiteRepository->UpdateTicketAstroWithIdRefsite($this->ticketId, $resultQuery['ID']);
            }
        } else {
```

Question métier : Point de décision — key_exists('ID', 'resultQuery'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #594 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChainePariV2() — ligne 658
Contexte   :
```php

        if (!in_array($infraContextePari, ["###$variableAdministree###", ''])) {
            if (is_null($this->dataPariv2)) {
                $dataJson = $this->getDataPariv2($ticketId, $typeRessource, $infraContextePari);

                if ($this->app->get('AstroBase')->isJson($dataJson)) {
```

Question métier : Point de décision — is_null('this'->dataPariv2). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #595 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 756
Contexte   :
```php
        ];

        if (isset($mapping[$variable])) {
            $keys = $mapping[$variable];
            $value = $data;
            foreach ($keys as $key) {
```

Question métier : Point de décision — isset('mapping'['variable']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #596 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 195
Contexte   :
```php
                    break;
                case 'Etat_batterie':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {

                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['mode_fonctionnement_batterie'], $chaine);
```

Question métier : Valeur de référence non documentée — La décision « key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok' » repose sur la valeur 'ok'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #597 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 203
Contexte   :
```php
                    break;
                case 'Element_HS':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {
                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['element_equipement_panne_tronc'], $chaine);
                    }
```

Question métier : Valeur de référence non documentée — La décision « key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok' » repose sur la valeur 'ok'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #598 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 210
Contexte   :
```php
                    break;
                case 'Tension_batterie':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {
                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['tension'], $chaine);
                    }
```

Question métier : Valeur de référence non documentée — La décision « key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok' » repose sur la valeur 'ok'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #599 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 217
Contexte   :
```php
                    break;
                case 'Temperature':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {
                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['temperature'], $chaine);
                    }
```

Question métier : Valeur de référence non documentée — La décision « key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok' » repose sur la valeur 'ok'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #600 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 375
Contexte   :
```php
                    $replaceValue = $this->refSiteRepository->getRefsiteColumn($arrayRefSite[$arg], $ticketId);

                    if (OceaneTools::isValidVariable($replaceValue) && gettype($replaceValue) != 'boolean') {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
```

Question métier : Valeur de référence non documentée — La décision « OceaneTools::isValidVariable('replaceValue') et gettype('replaceValue') différent de 'boolean' » repose sur la valeur 'boolean'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #601 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : getIntervenant() — ligne 592
Contexte   :
```php
        }

        if (gettype($resultQuery) != 'boolean' && $resultQuery != '' && is_array($resultQuery)) {
            $intervenant = key_exists('INTERVENANT', $resultQuery) ? $resultQuery['INTERVENANT'] : '';
            if (key_exists('ID', $resultQuery)) {
                $this->refSiteRepository->UpdateTicketAstroWithIdRefsite($this->ticketId, $resultQuery['ID']);
```

Question métier : Valeur de référence non documentée — La décision « gettype('resultQuery') différent de 'boolean' et 'resultQuery' différent de '' et is_array('resultQuery') » repose sur la valeur 'boolean'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #602 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChainePariV2() — ligne 670
Contexte   :
```php

            $replaceValue = $this->getReplaceValue($this->dataPariv2, $variable);
            if (OceaneTools::isValidVariable($replaceValue) && gettype($replaceValue) != 'boolean') {
                $chaine = str_replace('###' . $variable . '###', $replaceValue, $chaine);
            } else {
                $chaine = str_replace('###' . $variable . '###', '', $chaine);
```

Question métier : Valeur de référence non documentée — La décision « OceaneTools::isValidVariable('replaceValue') et gettype('replaceValue') différent de 'boolean' » repose sur la valeur 'boolean'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

---

**Gap #615 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 133
Contexte   :
```php
                        if (property_exists($val1, 'id') && $val1->id == 'LIBSITE') {
                            $libSite = $val1->value;
                        }
                    }
                    if ($libSite != "") {
```

Question métier : Le code situation 'LIBSITE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #616 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 195
Contexte   :
```php
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {

                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['mode_fonctionnement_batterie'], $chaine);
                    }
```

Question métier : Le code situation 'ok' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #617 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : replaceTagsChaine() — ligne 416
Contexte   :
```php
                        $replaceValue = ($resultColumn == 'ORANGE') ? 'Non' : 'Oui';
                    }
                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
```

Question métier : Le code situation 'ORANGE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #618 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : getIntervenant() — ligne 563
Contexte   :
```php
                    if ($typeRessource == 'MIE') {
                        $extremiteTechno = 'TECHNO';
                    } else {
                        if ($ext == 'tabs_action_ext1') {
                            $extremiteTechno = 'EXT1_TECHNO';
```

Question métier : Le code situation 'MIE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

---

**Gap #619 — Variable**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : getIntervenant() — ligne 577
Contexte   :
```php
                    if ($techno == 'FH') {
                        $resultQuery = $this->refSiteRepository->getFhByAppelationIr($refsiteFirst);
                    } else {
                        $resultQuery = $this->refSiteRepository->getRsByAppelationIr($refsiteFirst);
                    }
```

Question métier : Le code situation 'FH' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?
