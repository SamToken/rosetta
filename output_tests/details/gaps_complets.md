# Gaps de Documentation — Liste Exhaustive

*Généré le 2026-04-26 09:46 — 494 comportement(s) à définir sur 10 contrôleur(s)*

> Chaque ligne correspond à un comportement du système actuel dont le cas contraire n'est pas documenté.

| # | Contrôleur | Méthode | Ligne | Question métier | Contexte | Statut |
|---|-----------|---------|-------|----------------|----------|--------|
| 1 | AbandonnerService | — | L.123 | Point de décision — 'isLocked' égal à = true. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 2 | AbandonnerService | — | L.135 | Point de décision — 'impact' différent de ''. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 3 | AbandonnerService | — | L.169 | Point de décision — 'labelFinal' égal à ''. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 4 | AbandonnerService | — | L.172 | Point de décision — 'isMe'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 5 | AbandonnerService | — | L.239 | Point de décision — array_key_exists('message', 'result') et array_key_exists('code', 'result') et array_key_exists('… | [voir bloc] | ⬜ |
| 6 | AbandonnerService | — | L.241 | Point de décision — 'result'['message'] égal à 'Functional error: Ticket in closed status'. Quel est le comportement … | [voir bloc] | ⬜ |
| 7 | AbandonnerService | — | L.266 | Point de décision — 'incidentEnCours'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 8 | AbandonnerService | — | L.319 | Point de décision — array_key_exists('message', 'result') et array_key_exists('code', 'result') et array_key_exists('… | [voir bloc] | ⬜ |
| 9 | AbandonnerService | — | L.391 | Point de décision — 'dataAdelia'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 10 | AbandonnerService | — | L.407 | Point de décision — 'dataAdelia'['TOTAL_CLIENTS'] > 0. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 11 | AbandonnerService | — | L.408 | Point de décision — 'dataAstro'['ADELIA_MANUEL'] égal à 'o'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 12 | AbandonnerService | — | L.410 | Point de décision — 'dataAdeliaManuel'['BEGIN_DATE'] différent de '' et 'dataAdeliaManuel'['SEUIL_GRAVE'] différent d… | [voir bloc] | ⬜ |
| 13 | AbandonnerService | — | L.435 | Point de décision — 'dataAdelia'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 14 | AbandonnerService | — | L.449 | Point de décision — 'dataAdelia'['TOTAL_CLIENTS'] > 0. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 15 | AbandonnerService | — | L.450 | Point de décision — 'dataAstro'['ADELIA_MANUEL'] égal à 'o'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 16 | AbandonnerService | — | L.452 | Point de décision — 'dataAdeliaManuel'['BEGIN_DATE'] différent de '' et 'dataAdeliaManuel'['SEUIL_GRAVE'] différent d… | [voir bloc] | ⬜ |
| 17 | AbandonnerService | — | L.461 | Point de décision — count('ticket'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 18 | AbandonnerService | — | L.534 | Point de décision — key_exists('code', 'result') et key_exists('message', 'result'). Quel est le comportement attendu… | [voir bloc] | ⬜ |
| 19 | AbandonnerService | — | L.566 | Point de décision — 'result' égal à 1. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 20 | AbandonnerService | — | L.570 | Point de décision — 'result' égal à 2. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 21 | AbandonnerService | — | L.583 | Point de décision — 'nbKo' égal à 0. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 22 | AbandonnerService | — | L.586 | Point de décision — 'nbOk' > 0. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 23 | AbandonnerService | — | L.617 | Point de décision — !'droitTools'->isIncident('ticketId'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 24 | AbandonnerService | — | L.625 | Point de décision — 'isApi' égal à 1. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 25 | AbandonnerService | — | L.633 | Point de décision — 'nombreClientEntreprise' égal à 'oui' ou intval('nombreClientEntreprise') > 0. Quel est le compor… | [voir bloc] | ⬜ |
| 26 | AbandonnerService | — | L.639 | Point de décision — !le champ 'adelia' est vide && key_exists('PRESTATIONS', $adelia). Quel est le comportement atten… | [voir bloc] | ⬜ |
| 27 | AbandonnerService | — | L.643 | Point de décision — !le champ 'adelia' est vide && !le champ 'prestations' est vide && $prestations != '' && key_exis… | [voir bloc] | ⬜ |
| 28 | AbandonnerService | — | L.646 | Point de décision — 'isNetVpn' égal à '1' et 'isNetVpnAdelia' égal à 1. Quel est le comportement attendu dans le cas … | [voir bloc] | ⬜ |
| 29 | AbandonnerService | — | L.661 | Point de décision — 'gtr' et strtolower('informerClient'['label']) égal à "coupure franche". Quel est le comportement… | [voir bloc] | ⬜ |
| 30 | AbandonnerService | — | L.665 | Point de décision — 'informerClient'['priorite'] égal à '-'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 31 | AbandonnerService | — | L.705 | Point de décision — !is_null('value'['typeKey']). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 32 | AbandonnerService | — | L.733 | Point de décision — is_null('assemblee'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 33 | AbandonnerService | — | L.768 | Point de décision — key_exists('CODE', 'value') et 'value'['CODE'] égal à 'PRIORITE'. Quel est le comportement attend… | [voir bloc] | ⬜ |
| 34 | AbandonnerService | — | L.792 | Point de décision — !'isAssemblee' et !'isEquipementTrans'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 35 | AbandonnerService | — | L.801 | Point de décision — is_array($dataPrioImpact) && !le champ 'dataPrioImpact' est vide && key_exists('impact_result', $… | [voir bloc] | ⬜ |
| 36 | AbandonnerService | — | L.802 | Point de décision — key_exists('VoIP', 'dataPrioImpact'['impact_result']). Quel est le comportement attendu dans le c… | [voir bloc] | ⬜ |
| 37 | AbandonnerService | — | L.806 | Point de décision — !is_null('countByService') et ((key_exists('gtrs1', 'countByService') et 'countByService'['gtrs1'… | [voir bloc] | ⬜ |
| 38 | AbandonnerService | — | L.808 | Point de décision — !is_null('dataPrioImpact') et key_exists('impact_result', 'dataPrioImpact'). Quel est le comporte… | [voir bloc] | ⬜ |
| 39 | AbandonnerService | — | L.816 | Point de décision — !isset('dataPrioImpact'['impact_result']['service']). Quel est le comportement attendu dans le ca… | [voir bloc] | ⬜ |
| 40 | AbandonnerService | — | L.822 | Point de décision — isset('arrayDeclencher'['VoIP']). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 41 | AbandonnerService | — | L.826 | Point de décision — !is_null('dataPrioImpact') et key_exists('impact_result', 'dataPrioImpact'). Quel est le comporte… | [voir bloc] | ⬜ |
| 42 | AbandonnerService | — | L.829 | Point de décision — ('k' égal à 'value2'['TYPE'] ou 'value2'['TYPE'] égal à '_TOTAL') et !'decDone'. Quel est le comp… | [voir bloc] | ⬜ |
| 43 | AbandonnerService | — | L.834 | Point de décision — 'op' égal à '>='. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 44 | AbandonnerService | — | L.835 | Point de décision — 'v' >= 'val' et 'gtrOk' et !'decDone'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 45 | AbandonnerService | — | L.841 | Point de décision — 'op' égal à '<='. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 46 | AbandonnerService | — | L.842 | Point de décision — 'v' <= 'val' et 'gtrOk' et !'decDone'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 47 | AbandonnerService | — | L.849 | Point de décision — is_null('value2'['TYPE']) et !is_null('value2'['GTR']). Quel est le comportement attendu dans le … | [voir bloc] | ⬜ |
| 48 | AbandonnerService | — | L.850 | Point de décision — key_exists('gtr_final', 'dataPrioImpact') et 'dataPrioImpact'['gtr_final'] égal à 'value2'['GTR']… | [voir bloc] | ⬜ |
| 49 | AbandonnerService | — | L.856 | Point de décision — is_null('value2'['TYPE']) et is_null('value2'['GTR']) et !'decDone'. Quel est le comportement att… | [voir bloc] | ⬜ |
| 50 | AbandonnerService | — | L.879 | Point de décision — 'doneFlag' ou is_null('dataPrioImpact') ou !key_exists('impact_result', 'dataPrioImpact'). Quel e… | [voir bloc] | ⬜ |
| 51 | AbandonnerService | — | L.884 | Point de décision — 'doneFlag') break; if ('k' égal à 'value2'['TYPE'] ou 'value2'['TYPE'] égal à '_TOTAL'. Quel est … | [voir bloc] | ⬜ |
| 52 | AbandonnerService | — | L.893 | Point de décision — 'op' égal à '>='. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 53 | AbandonnerService | — | L.894 | Point de décision — 'v' >= 'val' et 'gtrOk' et 'hnoOk'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 54 | AbandonnerService | — | L.898 | Point de décision — 'op' égal à '<='. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 55 | AbandonnerService | — | L.899 | Point de décision — 'v' <= 'val' et 'gtrOk' et 'hnoOk'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 56 | AbandonnerService | — | L.904 | Point de décision — is_null('value2'['TYPE']) et !is_null('value2'['GTR']). Quel est le comportement attendu dans le … | [voir bloc] | ⬜ |
| 57 | AbandonnerService | — | L.909 | Point de décision — key_exists('gtr_final', 'dataPrioImpact') et 'dataPrioImpact'['gtr_final'] égal à 'gtr' et 'hnoOk… | [voir bloc] | ⬜ |
| 58 | AbandonnerService | — | L.913 | Point de décision — is_null('value2'['TYPE']) et is_null('value2'['GTR']). Quel est le comportement attendu dans le c… | [voir bloc] | ⬜ |
| 59 | AbandonnerService | — | L.917 | Point de décision — 'hnoOk'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 60 | AbandonnerService | — | L.953 | Point de décision — !is_null('result'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 61 | AgirPiloterValidationService | — | L.23 | Point de décision — key_exists('DATE_RETABLISSEMENT_DEMANDE_INTERVENTION', 'regles') et 'regles'['DATE_RETABLISSEMENT… | [voir bloc] | ⬜ |
| 62 | AgirPiloterValidationService | — | L.25 | Point de décision — !'this'->notEmpty('dateRetab'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 63 | AgirPiloterValidationService | — | L.30 | Point de décision — 'dateRetab' différent de = ''. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 64 | AgirPiloterValidationService | — | L.31 | Point de décision — !'this'->isDate('dateRetab', "d/m/Y H:i"). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 65 | AgirPiloterValidationService | — | L.40 | Point de décision — key_exists('DATE_COURS_EDS_DEMANDE_INTERVENTION', 'regles') et 'regles'['DATE_COURS_EDS_DEMANDE_I… | [voir bloc] | ⬜ |
| 66 | AgirPiloterValidationService | — | L.42 | Point de décision — !'this'->notEmpty('actionCoursEds'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 67 | AgirPiloterValidationService | — | L.47 | Point de décision — 'actionCoursEds' différent de = ''. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 68 | AgirPiloterValidationService | — | L.48 | Point de décision — !'this'->isDate('actionCoursEds', "d/m/Y H:i"). Quel est le comportement attendu dans le cas cont… | [voir bloc] | ⬜ |
| 69 | AgirPiloterValidationService | — | L.56 | Point de décision — key_exists('COMMENTAIRE_DEMANDE_INTERVENTION', 'regles') et 'regles'['COMMENTAIRE_DEMANDE_INTERVE… | [voir bloc] | ⬜ |
| 70 | AgirPiloterValidationService | — | L.58 | Point de décision — !'this'->notEmpty('commentaire'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 71 | AgirPiloterValidationService | — | L.66 | Point de décision — key_exists('ACTION_EN_COURS_EDS', 'regles') et 'regles'['ACTION_EN_COURS_EDS']["OBLIGATOIRE"] éga… | [voir bloc] | ⬜ |
| 72 | AgirPiloterValidationService | — | L.68 | Point de décision — !'this'->notEmpty('actionCoursEds'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 73 | AgirPiloterValidationService | — | L.75 | Point de décision — key_exists('NIVEAU_URGENCE', 'regles') et 'regles'['NIVEAU_URGENCE']["OBLIGATOIRE"] égal à = '1'.… | [voir bloc] | ⬜ |
| 74 | AgirPiloterValidationService | — | L.77 | Point de décision — !'this'->notEmpty('actionCoursEds'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 75 | AgirPiloterValidationService | — | L.83 | Point de décision — !'result'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 76 | AgpService | — | L.176 | Point de décision — 'this'->edrRepository->testDataInfo('astroId') égal à 0. Quel est le comportement attendu dans le… | [voir bloc] | ⬜ |
| 77 | AgpService | — | L.234 | Point de décision — count('deports') > 0. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 78 | AgpService | — | L.237 | Point de décision — 'maitreDeport'['status'] égal à 'ok'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 79 | AgpService | — | L.245 | Point de décision — 'master' différent de '' et 'master' différent de 'dslamName'. Quel est le comportement attendu d… | [voir bloc] | ⬜ |
| 80 | AgpService | — | L.248 | Point de décision — 'maitreDeport'['status'] égal à 'nok'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 81 | AgpService | — | L.258 | Point de décision — 'alarme' différent de 'dslamName'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 82 | AgpService | — | L.273 | Point de décision — 'typeRessource' égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 83 | AgpService | — | L.318 | Point de décision — 'typeRessource' égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 84 | AgpService | — | L.531 | Point de décision — 'typeRessource' égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 85 | AgpService | — | L.541 | Point de décision — 'typeRessource' égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 86 | AgpService | — | L.551 | Point de décision — 'typeRessource' égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 87 | AgpService | — | L.570 | Point de décision — 'alarme' différent de 'dslamName'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 88 | AgpService | — | L.575 | Point de décision — count('deports') > 0. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 89 | AgpService | — | L.578 | Point de décision — 'maitreDeport'['status'] égal à 'ok'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 90 | AgpService | — | L.586 | Point de décision — 'master' différent de '' et 'master' différent de 'dslamName'. Quel est le comportement attendu d… | [voir bloc] | ⬜ |
| 91 | AgpService | — | L.589 | Point de décision — 'maitreDeport'['status'] égal à 'nok'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 92 | AgpService | — | L.598 | Point de décision — !is_null('chassisCarte') et 'chassisCarte' et key_exists('CHASSIS', 'chassisCarte'). Quel est le … | [voir bloc] | ⬜ |
| 93 | AgpService | — | L.606 | Point de décision — 'typeRessource' égal à 'MIE'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 94 | AgpService | — | L.611 | Point de décision — 'typeRessource' égal à 'SLN' ou 'typeRessource' égal à 'WDM_SID'. Quel est le comportement attend… | [voir bloc] | ⬜ |
| 95 | AgpService | — | L.617 | Point de décision — 'typeRessource' égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 96 | AgpService | — | L.653 | Point de décision — 'typeRessource' égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 97 | AgpService | — | L.708 | Point de décision — 'typeRessource' égal à 'COMMUT' ou 'typeRessource' égal à 'UNIRACC' ou 'typeRessource' égal à 'CO… | [voir bloc] | ⬜ |
| 98 | AgpService | — | L.712 | Point de décision — ('typeRessource' égal à 'DSLAM' ou 'typeRessource' égal à 'DSLAMDERCO') et 'data'['id_rsc'] diffé… | [voir bloc] | ⬜ |
| 99 | AgpService | — | L.717 | Point de décision — !le champ 'ressource' est vide. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 100 | AgpService | — | L.731 | Point de décision — !'api'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 101 | AgpService | — | L.742 | Point de décision — 'oceaneData'['herite_oceane_hno'] égal à 1. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 102 | AgpService | — | L.747 | Point de décision — key_exists('oceaneData'['oceane_priority'], 'priorityHoHno'). Quel est le comportement attendu da… | [voir bloc] | ⬜ |
| 103 | AgpService | — | L.748 | Point de décision — 'data'['agp_ho_hno_generique'] égal à 'HO' et 'priorityHoHno'['oceaneData'['oceane_priority']]['a… | [voir bloc] | ⬜ |
| 104 | AgpService | — | L.750 | Point de décision — 'data'['agp_ho_hno_generique'] égal à 'HNO' et 'priorityHoHno'['oceaneData'['oceane_priority']]['… | [voir bloc] | ⬜ |
| 105 | AgpService | — | L.763 | Point de décision — key_exists('herite_oceane_date_action_en_cours', 'oceaneData'). Quel est le comportement attendu … | [voir bloc] | ⬜ |
| 106 | AgpService | — | L.775 | Point de décision — !le champ 'blocs' est vide && key_exists(0, $blocs). Quel est le comportement attendu dans le cas… | [voir bloc] | ⬜ |
| 107 | AgpService | — | L.777 | Point de décision — 'blocName' différent de 'choix_de_carte_trans' et 'blocName' différent de 'Types_Carte' et 'blocN… | [voir bloc] | ⬜ |
| 108 | AgpService | — | L.783 | Point de décision — is_string('data'['id_commentaire']) et 'data'['id_commentaire'] égal à 'DiagSDH'. Quel est le com… | [voir bloc] | ⬜ |
| 109 | AgpService | — | L.840 | Point de décision — !'api'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 110 | AgpService | — | L.853 | Point de décision — 'oceaneData'['herite_oceane_hno'] égal à 1. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 111 | AgpService | — | L.858 | Point de décision — key_exists('oceaneData'['oceane_priority'], 'priorityHoHno'). Quel est le comportement attendu da… | [voir bloc] | ⬜ |
| 112 | AgpService | — | L.859 | Point de décision — 'data'['agp_ho_hno_generique'] égal à 'HO' et 'priorityHoHno'['oceaneData'['oceane_priority']]['a… | [voir bloc] | ⬜ |
| 113 | AgpService | — | L.861 | Point de décision — 'data'['agp_ho_hno_generique'] égal à 'HNO' et 'priorityHoHno'['oceaneData'['oceane_priority']]['… | [voir bloc] | ⬜ |
| 114 | AgpService | — | L.881 | Point de décision — key_exists('herite_oceane_date_action_en_cours', 'oceaneData'). Quel est le comportement attendu … | [voir bloc] | ⬜ |
| 115 | AgpService | — | L.890 | Point de décision — key_exists('intervenant', 'data') et 'data'['intervenant'] différent de ''. Quel est le comportem… | [voir bloc] | ⬜ |
| 116 | AgpService | — | L.892 | Point de décision — is_array('segComment') et isset('segComment'['SECOND_COMMENT']) et trim('segComment'['SECOND_COMM… | [voir bloc] | ⬜ |
| 117 | AgpService | — | L.903 | Point de décision — 'api'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 118 | AgpService | — | L.904 | Point de décision — 'data'['type_ressource'] égal à 'DSLAM' ou 'data'['type_ressource'] égal à 'DSLAMDERCO'. Quel est… | [voir bloc] | ⬜ |
| 119 | AgpService | — | L.910 | Point de décision — 'astroSession'['type'] égal à 'DSLAM' ou 'astroSession'['type'] égal à 'DSLAMDERCO'. Quel est le … | [voir bloc] | ⬜ |
| 120 | AgpService | — | L.917 | Point de décision — !le champ 'blocs' est vide && key_exists(0, $blocs). Quel est le comportement attendu dans le cas… | [voir bloc] | ⬜ |
| 121 | AgpService | — | L.919 | Point de décision — 'isDslamTest'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 122 | AgpService | — | L.923 | Point de décision — 'blocName' différent de 'choix_de_carte_trans' et 'blocName' différent de 'Types_Carte' et 'blocN… | [voir bloc] | ⬜ |
| 123 | AgpService | — | L.929 | Point de décision — is_string('data'['id_commentaire']) et 'data'['id_commentaire'] égal à 'DiagSDH'. Quel est le com… | [voir bloc] | ⬜ |
| 124 | AgpService | — | L.941 | Point de décision — 'isDslamTest'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 125 | AgpService | — | L.967 | Point de décision — 'idRscDslam' différent de = null et 'idRscDslam' différent de = ''. Quel est le comportement atte… | [voir bloc] | ⬜ |
| 126 | AgpService | — | L.974 | Point de décision — 'api'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 127 | AgpService | — | L.983 | Point de décision — 'data'['agp_ecran'] égal à 0. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 128 | AgpService | — | L.990 | Point de décision — !'idUrgenceOceane'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 129 | AgpService | — | L.1017 | Point de décision — in_array('input', 'carteArray') ou (('input' égal à 'alarme') et ('hasChassis' égal à 'false')). … | [voir bloc] | ⬜ |
| 130 | AgpService | — | L.1029 | Point de décision — 'dslamArray'['racks']['k']['rackName'] égal à 'chassis'. Quel est le comportement attendu dans le… | [voir bloc] | ⬜ |
| 131 | AgpService | — | L.1033 | Point de décision — isset('vv'['category']) et 'vv'['category'] différent de 'carte ligne'. Quel est le comportement … | [voir bloc] | ⬜ |
| 132 | AgpService | — | L.1037 | Point de décision — 'test'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 133 | AgpService | — | L.1074 | Point de décision — !is_null('this'->getOceane). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 134 | AgpService | — | L.1087 | Point de décision — 'data'['type'] égal à 'TRCCABLE' ou 'data'['type'] égal à 'TRONCABLE' ou 'data'['type'] égal à 'C… | [voir bloc] | ⬜ |
| 135 | AgpService | — | L.1093 | Point de décision — 'data'['type'] égal à 'SDH' ou 'data'['type'] égal à 'SLN' ou 'data'['type'] égal à 'PDH' ou 'dat… | [voir bloc] | ⬜ |
| 136 | AgpService | — | L.1096 | Point de décision — 'data'['type'] égal à 'MIE'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 137 | AgpService | — | L.1158 | Point de décision — 'choixCreation' égal à "DSLAM". Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 138 | AgpService | — | L.1160 | Point de décision — 'choixCreation' égal à "Chassis". Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 139 | AgpService | — | L.1162 | Point de décision — 'choixCreation' égal à "Carte". Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 140 | AgpService | — | L.1215 | Point de décision — is_array('retourCreation') et key_exists('id', 'retourCreation'). Quel est le comportement attend… | [voir bloc] | ⬜ |
| 141 | AgpService | — | L.1292 | Point de décision — 'astroId' égal à ''. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 142 | AgpService | — | L.1298 | Point de décision — !'this'->getOceane. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 143 | AgpService | — | L.1301 | Point de décision — 'this'->ticketId et 'this'->getOceane. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 144 | AgpService | — | L.1309 | Point de décision — 'arg' égal à 'Temperature' ou 'arg' égal à 'Etat_batterie' ou 'arg' égal à 'Tension_batterie' ou … | [voir bloc] | ⬜ |
| 145 | AgpService | — | L.1317 | Point de décision — 'libSite' différent de "". Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 146 | AgpService | — | L.1333 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 147 | AgpService | — | L.1339 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 148 | AgpService | — | L.1346 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 149 | AgpService | — | L.1354 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 150 | AgpService | — | L.1362 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 151 | AgpService | — | L.1374 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 152 | AgpService | — | L.1379 | Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le compo… | [voir bloc] | ⬜ |
| 153 | AgpService | — | L.1387 | Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le compo… | [voir bloc] | ⬜ |
| 154 | AgpService | — | L.1394 | Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le compo… | [voir bloc] | ⬜ |
| 155 | AgpService | — | L.1401 | Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le compo… | [voir bloc] | ⬜ |
| 156 | AgpService | — | L.1416 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 157 | AgpService | — | L.1423 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 158 | AgpService | — | L.1433 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 159 | AgpService | — | L.1440 | Point de décision — !is_null('codeDetecteur'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 160 | AgpService | — | L.1444 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 161 | AgpService | — | L.1466 | Point de décision — OceaneTools::isValidVariable('replaceValue') et gettype('replaceValue') différent de 'boolean'. Q… | [voir bloc] | ⬜ |
| 162 | AgpService | — | L.1471 | Point de décision — 'this'->typeRessource égal à 'TRONCABLE'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 163 | AgpService | — | L.1477 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 164 | AgpService | — | L.1484 | Point de décision — 'this'->globalApiRepository->isVariableAdminExist('arg', 'type'). Quel est le comportement attend… | [voir bloc] | ⬜ |
| 165 | AgpService | — | L.1488 | Point de décision — 'resourceSpecification'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 166 | AgpService | — | L.1491 | Point de décision — count('tabIdentifiants') > 0 et 'this'->ticketId différent de = null. Quel est le comportement at… | [voir bloc] | ⬜ |
| 167 | AgpService | — | L.1493 | Point de décision — isset('replaceValue'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 168 | AgpService | — | L.1524 | Point de décision — le champ 'intervenantInfos' est vide || ($intervenantInfos['TECHNO'] == null || $intervenantInfos… | [voir bloc] | ⬜ |
| 169 | AgpService | — | L.1525 | Point de décision — 'intervenant' différent de 'ORANGE'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 170 | AgpService | — | L.1546 | Point de décision — is_array('intervenantArray') et key_exists('INTERVENANT', 'intervenantArray'). Quel est le compor… | [voir bloc] | ⬜ |
| 171 | AgpService | — | L.1557 | Point de décision — is_array('intervenantInfos'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 172 | AgpService | — | L.1569 | Point de décision — !is_null('allEcransValues') et is_array('allEcransValues'). Quel est le comportement attendu dans… | [voir bloc] | ⬜ |
| 173 | AgpService | — | L.1587 | Point de décision — 'Carte_EAN' égal à 'blocName' et key_exists('donnee_cartes', 'allEcranValuesArray'). Quel est le … | [voir bloc] | ⬜ |
| 174 | AgpService | — | L.1600 | Point de décision — 'keyVariable' différent de 'donnee_cartes' et 'keyVariable' différent de 'CODE_EAN' et 'keyVariab… | [voir bloc] | ⬜ |
| 175 | AgpService | — | L.1603 | Point de décision — 'keyVariable' égal à 'CODE_EAN'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 176 | AgpService | — | L.1607 | Point de décision — 'keyTag' égal à 'CODE_EAN'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 177 | AgpService | — | L.1615 | Point de décision — 'keyVariable' égal à 'Type_Equipement'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 178 | AgpService | — | L.1619 | Point de décision — 'keyTag' égal à 'TYPE_EQUIPEMENT'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 179 | AgpService | — | L.1627 | Point de décision — 'keyVariable' égal à 'Nom_Carte'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 180 | AgpService | — | L.1631 | Point de décision — 'keyTag' égal à 'NOM_CARTE'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 181 | AgpService | — | L.1642 | Point de décision — $keyVariable == 'donnee_cartes' && !le champ 'blocs' est vide && $blocName == 'choix_de_carte_tra… | [voir bloc] | ⬜ |
| 182 | AgpService | — | L.1649 | Point de décision — 'keyTag' égal à 'ean'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 183 | AgpService | — | L.1650 | Point de décision — 'dataTag' égal à 'True'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 184 | AgpService | — | L.1665 | Point de décision — $keyVariable != 'donnee_cartes' && !le champ 'blocs' est vide && ($blocName == 'defaut_constate_t… | [voir bloc] | ⬜ |
| 185 | AgpService | — | L.1675 | Point de décision — 'keyVariable2' différent de 'donnee_cartes'. Quel est le comportement attendu dans le cas contrai… | [voir bloc] | ⬜ |
| 186 | AgpService | `aiguillageCommentaire()` | L.1692 | Point de décision — 'astroData'['type'] égal à 'DSLAM' ou 'astroData'['type'] égal à 'DSLAMDERCO'. Quel est le compor… | [voir bloc] | ⬜ |
| 187 | AgpService | `aiguillageCommentaire()` | L.1695 | Point de décision — 'isDslamTest'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 188 | AgpService | `aiguillageCommentaire()` | L.1704 | Point de décision — key_exists('intervenant', 'data') et 'data'['intervenant'] différent de ''. Quel est le comportem… | [voir bloc] | ⬜ |
| 189 | AgpService | `aiguillageCommentaire()` | L.1706 | Point de décision — is_array('segComment') et isset('segComment'['SECOND_COMMENT']) et trim('segComment'['SECOND_COMM… | [voir bloc] | ⬜ |
| 190 | AiguillageIntervenantService | — | L.48 | Point de décision — le champ 'intervenantInfosList' est vide. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 191 | AiguillageIntervenantService | — | L.52 | Point de décision — 'intervenantInfos'['VARIABLE_ADMIN'] différent de '* Variables *' et !is_null('intervenantInfos'[… | [voir bloc] | ⬜ |
| 192 | AiguillageIntervenantService | — | L.62 | Point de décision — strpos('checkVar', 'val') égal à = 0) 'ok' = true; break; case 'equal': if (strcmp('checkVar', 'v… | [voir bloc] | ⬜ |
| 193 | AiguillageIntervenantService | — | L.80 | Point de décision — 'intervenantInfos'['VARIABLE_ADMIN'] égal à '* Variables *' et (!is_null('intervenantInfos'['COND… | [voir bloc] | ⬜ |
| 194 | AiguillageIntervenantService | — | L.82 | Point de décision — 'intervenantInfos'['VARIABLE_ADMIN'] égal à '* Variables *' et (is_null('intervenantInfos'['CONDI… | [voir bloc] | ⬜ |
| 195 | AiguillageIntervenantService | — | L.85 | Point de décision — !is_null('intervenantInfos'['TECHNO']) et 'intervenantInfos'['TECHNO'] différent de '' et 'ok'. Q… | [voir bloc] | ⬜ |
| 196 | AiguillageIntervenantService | — | L.109 | Point de décision — 'typeRessource' égal à 'MIE'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 197 | AiguillageIntervenantService | — | L.112 | Point de décision — 'ext' égal à 'tabs_action_ext1'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 198 | AiguillageIntervenantService | — | L.114 | Point de décision — 'ext' égal à 'tabs_action_ext2'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 199 | AiguillageIntervenantService | — | L.122 | Point de décision — 'techno' égal à 'FH'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 200 | AiguillageIntervenantService | — | L.134 | Point de décision — 'ok'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 201 | ApiService | — | L.78 | Point de décision — key_exists('code', 'resultatO') et 'resultatO'['code'] différent de 60. Quel est le comportement … | [voir bloc] | ⬜ |
| 202 | ApiService | — | L.80 | Point de décision — key_exists('code', 'resultatO') et 'resultatO'['code'] égal à 60. Quel est le comportement attend… | [voir bloc] | ⬜ |
| 203 | ApiService | — | L.82 | Point de décision — key_exists('id', 'resultatO'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 204 | ApiService | — | L.125 | Point de décision — 'userData' et is_array('userData') et !key_exists('message', 'userData'). Quel est le comportemen… | [voir bloc] | ⬜ |
| 205 | ApiService | — | L.209 | Point de décision — in_array('category', 'listIncident'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 206 | ApiService | — | L.214 | Point de décision — 'category' égal à '64'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 207 | ApiService | — | L.227 | Point de décision — 'data'['type_ressource'] égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 208 | ApiService | — | L.233 | Point de décision — 'data'['evt_incident'] égal à '64'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 209 | ApiService | — | L.240 | Point de décision — 'data'['type_ressource'] égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 210 | ApiService | — | L.242 | Point de décision — 'ressource'['ID_TYPE_RESSOURCE'] différent de '1' et 'ressource'['ID_TYPE_RESSOURCE'] différent d… | [voir bloc] | ⬜ |
| 211 | ApiService | — | L.263 | Point de décision — 'enchainement' égal à 'TRAITEMENT_ALARME_ADSL'. Quel est le comportement attendu dans le cas cont… | [voir bloc] | ⬜ |
| 212 | ApiService | — | L.273 | Point de décision — !'preRequis'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 213 | ApiService | — | L.284 | Point de décision — !'preRequis'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 214 | ApiService | — | L.304 | Point de décision — !'preRequis'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 215 | ApiService | — | L.315 | Point de décision — !'preRequis'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 216 | ApiService | — | L.326 | Point de décision — !'preRequis'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 217 | ApiService | — | L.351 | Point de décision — !'preRequis'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 218 | ApiService | — | L.370 | Point de décision — 'code' égal à 'TRAITEMENT_ALARME_CARTES_CLIENTS' ou 'code' égal à 'TRAITEMENT_ALARME_EVT' ou 'cod… | [voir bloc] | ⬜ |
| 219 | ApiService | — | L.401 | Point de décision — key_exists('faultstring', 'result') et 'result'->faultstring différent de '' et key_exists('detai… | [voir bloc] | ⬜ |
| 220 | ApiService | — | L.408 | Point de décision — 'ticketID'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 221 | ApiService | — | L.419 | Point de décision — isset('result'->TroubleTicketResponse->TroubleTicketResponse). Quel est le comportement attendu d… | [voir bloc] | ⬜ |
| 222 | ApiService | — | L.424 | Point de décision — 'partyRole'['key']->partyRoleType égal à "TroubleResolutionContributor" et property_exists('party… | [voir bloc] | ⬜ |
| 223 | ApiService | — | L.425 | Point de décision — is_object('partyRole'['key']->Local_PartyIntervention->interventionStatus) et 'partyRole'['key']-… | [voir bloc] | ⬜ |
| 224 | ApiService | — | L.427 | Point de décision — is_object('partyRole'['key']->Local_PartyIntervention->interventionStatus) et 'partyRole'['key']-… | [voir bloc] | ⬜ |
| 225 | ApiService | — | L.429 | Point de décision — is_array('partyRole'['key']->Local_PartyIntervention->interventionStatus). Quel est le comporteme… | [voir bloc] | ⬜ |
| 226 | ApiService | — | L.431 | Point de décision — 'partyRole'['key']->Local_PartyIntervention->interventionStatus['k']->status égal à "Requested" e… | [voir bloc] | ⬜ |
| 227 | ApiService | — | L.453 | Point de décision — isset('result'->TroubleTicketResponse->TroubleTicketResponse). Quel est le comportement attendu d… | [voir bloc] | ⬜ |
| 228 | ApiService | — | L.458 | Point de décision — 'partyRole'['key']->partyRoleType égal à "TroubleResolutionLeader" et property_exists('partyRole'… | [voir bloc] | ⬜ |
| 229 | ApiService | — | L.459 | Point de décision — is_object('partyRole'['key']->Local_PartyIntervention->interventionStatus) et 'partyRole'['key']-… | [voir bloc] | ⬜ |
| 230 | ApiService | — | L.461 | Point de décision — is_array('partyRole'['key']->Local_PartyIntervention->interventionStatus). Quel est le comporteme… | [voir bloc] | ⬜ |
| 231 | ApiService | — | L.463 | Point de décision — 'partyRole'['key']->Local_PartyIntervention->interventionStatus['k']->status égal à "Requested" e… | [voir bloc] | ⬜ |
| 232 | ApiService | — | L.506 | Point de décision — 'scenarioExist' égal à '0'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 233 | ApiService | — | L.517 | Point de décision — 'etatScenario' égal à '0'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 234 | ApiService | — | L.528 | Point de décision — 'typeScenario' égal à '0' et 'scenarioType' égal à 'parametrable'. Quel est le comportement atten… | [voir bloc] | ⬜ |
| 235 | ApiService | — | L.532 | Point de décision — 'typeScenario' égal à '1' et 'scenarioType' égal à 'legacy'. Quel est le comportement attendu dan… | [voir bloc] | ⬜ |
| 236 | OceaneGetService | — | L.54 | Point de décision — 'this'->app->get('AstroBase')->isJson('detailTicketJson'). Quel est le comportement attendu dans … | [voir bloc] | ⬜ |
| 237 | OceaneGetService | — | L.68 | Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource… | [voir bloc] | ⬜ |
| 238 | OceaneGetService | — | L.70 | Point de décision — is_array('value') et key_exists('index', 'value') et !is_null('id') et (intval('value'['index']) … | [voir bloc] | ⬜ |
| 239 | OceaneGetService | — | L.72 | Point de décision — is_array('value') et key_exists('index', 'value') et key_exists('value', 'value'). Quel est le co… | [voir bloc] | ⬜ |
| 240 | OceaneGetService | — | L.88 | Point de décision — key_exists('relatedService', 'this'->oceaneData) et is_array('this'->oceaneData['relatedService']… | [voir bloc] | ⬜ |
| 241 | OceaneGetService | — | L.90 | Point de décision — is_array('value') et key_exists('index', 'value') et !is_null('id') et (intval('value'['index']) … | [voir bloc] | ⬜ |
| 242 | OceaneGetService | — | L.92 | Point de décision — is_array('value') et key_exists('index', 'value') et key_exists('value', 'value'). Quel est le co… | [voir bloc] | ⬜ |
| 243 | OceaneGetService | — | L.107 | Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource… | [voir bloc] | ⬜ |
| 244 | OceaneGetService | — | L.109 | Point de décision — 'idAndName'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 245 | OceaneGetService | — | L.129 | Point de décision — key_exists('relatedService', 'this'->oceaneData) et is_array('this'->oceaneData['relatedService']… | [voir bloc] | ⬜ |
| 246 | OceaneGetService | — | L.131 | Point de décision — 'idAndName'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 247 | OceaneGetService | — | L.152 | Point de décision — key_exists('troubleTicketCharacteristic', 'this'->oceaneData) et is_array('this'->oceaneData['tro… | [voir bloc] | ⬜ |
| 248 | OceaneGetService | — | L.154 | Point de décision — is_array('value') et key_exists('index', 'value') et !is_null('champ') et (intval('value'['index'… | [voir bloc] | ⬜ |
| 249 | OceaneGetService | — | L.156 | Point de décision — is_array('value') et key_exists('index', 'value') et key_exists('value', 'value'). Quel est le co… | [voir bloc] | ⬜ |
| 250 | OceaneGetService | — | L.171 | Point de décision — key_exists('priority', 'this'->oceaneData) et is_array('this'->oceaneData['priority']). Quel est … | [voir bloc] | ⬜ |
| 251 | OceaneGetService | — | L.173 | Point de décision — 'idAndLabel'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 252 | OceaneGetService | — | L.193 | Point de décision — key_exists('urgency', 'this'->oceaneData) et is_array('this'->oceaneData['urgency']). Quel est le… | [voir bloc] | ⬜ |
| 253 | OceaneGetService | — | L.195 | Point de décision — 'idAndLabel'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 254 | OceaneGetService | — | L.215 | Point de décision — key_exists('creationDate', 'this'->oceaneData). Quel est le comportement attendu dans le cas cont… | [voir bloc] | ⬜ |
| 255 | OceaneGetService | — | L.216 | Point de décision — !is_null('format'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 256 | OceaneGetService | — | L.231 | Point de décision — key_exists('detectionDate', 'this'->oceaneData). Quel est le comportement attendu dans le cas con… | [voir bloc] | ⬜ |
| 257 | OceaneGetService | — | L.232 | Point de décision — !is_null('format'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 258 | OceaneGetService | — | L.243 | Point de décision — key_exists('troubleCause', 'this'->oceaneData) et is_array('this'->oceaneData['troubleCause']) et… | [voir bloc] | ⬜ |
| 259 | OceaneGetService | — | L.245 | Point de décision — is_array('value') et key_exists('problemDetail', 'value') et key_exists('id', 'value'['problemDet… | [voir bloc] | ⬜ |
| 260 | OceaneGetService | — | L.259 | Point de décision — key_exists('relatedParty', 'this'->oceaneData) et is_array('this'->oceaneData['relatedParty']) et… | [voir bloc] | ⬜ |
| 261 | OceaneGetService | — | L.261 | Point de décision — is_array('value') et key_exists('role', 'value') et 'value'['role'] égal à 'TroubleResolutionLead… | [voir bloc] | ⬜ |
| 262 | OceaneGetService | — | L.270 | Point de décision — key_exists('relatedParty', 'this'->oceaneData) et is_array('this'->oceaneData['relatedParty']) et… | [voir bloc] | ⬜ |
| 263 | OceaneGetService | — | L.272 | Point de décision — is_array('value') et key_exists('role', 'value') et 'value'['role'] égal à 'troubleTicketOriginat… | [voir bloc] | ⬜ |
| 264 | OceaneGetService | — | L.282 | Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyInterven… | [voir bloc] | ⬜ |
| 265 | OceaneGetService | — | L.284 | Point de décision — is_array('value'['relatedParty']). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 266 | OceaneGetService | — | L.286 | Point de décision — is_array('valueRelatedParty') et key_exists('actionInProgress', 'valueRelatedParty') et 'valueRel… | [voir bloc] | ⬜ |
| 267 | OceaneGetService | — | L.287 | Point de décision — is_array('valueRelatedParty'['actionInProgress']) et key_exists('description', 'valueRelatedParty… | [voir bloc] | ⬜ |
| 268 | OceaneGetService | — | L.298 | Point de décision — key_exists('relatedParty', 'this'->oceaneData) et is_array('this'->oceaneData['relatedParty']) et… | [voir bloc] | ⬜ |
| 269 | OceaneGetService | — | L.300 | Point de décision — is_array('value') et key_exists('role', 'value') et 'value'['role'] égal à 'TroubleResolutionCont… | [voir bloc] | ⬜ |
| 270 | OceaneGetService | — | L.310 | Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyInterven… | [voir bloc] | ⬜ |
| 271 | OceaneGetService | — | L.312 | Point de décision — key_exists('interventionStatus', 'value') et is_array('value'['interventionStatus']). Quel est le… | [voir bloc] | ⬜ |
| 272 | OceaneGetService | — | L.314 | Point de décision — (is_array('status') et key_exists('status', 'status')). Quel est le comportement attendu dans le … | [voir bloc] | ⬜ |
| 273 | OceaneGetService | — | L.326 | Point de décision — key_exists('status', 'this'->oceaneData) et is_array('this'->oceaneData['status']). Quel est le c… | [voir bloc] | ⬜ |
| 274 | OceaneGetService | — | L.328 | Point de décision — key_exists('isCurrentStatus', 'value') et 'value'['isCurrentStatus'] égal à 1. Quel est le compor… | [voir bloc] | ⬜ |
| 275 | OceaneGetService | — | L.338 | Point de décision — key_exists('ticketType', 'this'->oceaneData) et is_array('this'->oceaneData['ticketType']). Quel … | [voir bloc] | ⬜ |
| 276 | OceaneGetService | — | L.340 | Point de décision — 'idAndLabel'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 277 | OceaneGetService | — | L.355 | Point de décision — key_exists('origin', 'this'->oceaneData) et is_array('this'->oceaneData['origin']). Quel est le c… | [voir bloc] | ⬜ |
| 278 | OceaneGetService | — | L.357 | Point de décision — 'idAndLabel'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 279 | OceaneGetService | — | L.373 | Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource… | [voir bloc] | ⬜ |
| 280 | OceaneGetService | — | L.382 | Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource… | [voir bloc] | ⬜ |
| 281 | OceaneGetService | — | L.384 | Point de décision — is_array('value') et key_exists('@type', 'value') et 'value'['@type'] égal à 'param' et key_exist… | [voir bloc] | ⬜ |
| 282 | OceaneGetService | — | L.407 | Point de décision — key_exists('relatedParty', 'this'->oceaneData) et is_array('this'->oceaneData['relatedParty']) et… | [voir bloc] | ⬜ |
| 283 | OceaneGetService | — | L.409 | Point de décision — is_array('value') et key_exists('familyName', 'value') et key_exists('id', 'value'). Quel est le … | [voir bloc] | ⬜ |
| 284 | OceaneGetService | — | L.419 | Point de décision — key_exists('troubleCause', 'this'->oceaneData) et is_array('this'->oceaneData['troubleCause']). Q… | [voir bloc] | ⬜ |
| 285 | OceaneGetService | — | L.427 | Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyInterven… | [voir bloc] | ⬜ |
| 286 | OceaneGetService | — | L.428 | Point de décision — key_exists('relatedParty', 'this'->oceaneData) et is_array('this'->oceaneData['relatedParty']) et… | [voir bloc] | ⬜ |
| 287 | OceaneGetService | — | L.430 | Point de décision — is_array('value') et key_exists('role', 'value') et 'value'['role'] égal à 'WorkingGroup' et key_… | [voir bloc] | ⬜ |
| 288 | OceaneGetService | — | L.441 | Point de décision — key_exists('status', 'this'->oceaneData) et is_array('this'->oceaneData['status']). Quel est le c… | [voir bloc] | ⬜ |
| 289 | OceaneGetService | — | L.443 | Point de décision — key_exists('reason', 'value'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 290 | OceaneGetService | — | L.457 | Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource… | [voir bloc] | ⬜ |
| 291 | OceaneGetService | — | L.479 | Point de décision — 'this'->app->get('AstroBase')->isJson('resultChild'). Quel est le comportement attendu dans le ca… | [voir bloc] | ⬜ |
| 292 | OceaneGetService | — | L.481 | Point de décision — is_array($resultChild) && !le champ 'resultChild' est vide && !key_exists('code', $resultChild) &… | [voir bloc] | ⬜ |
| 293 | OceaneGetService | — | L.497 | Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyInterven… | [voir bloc] | ⬜ |
| 294 | OceaneGetService | — | L.499 | Point de décision — is_array('value') et key_exists('relatedParty', 'value') et is_array('value'['relatedParty']). Qu… | [voir bloc] | ⬜ |
| 295 | OceaneGetService | — | L.501 | Point de décision — is_array('party') et key_exists('@referredType', 'party') et 'party'['@referredType'] égal à 'Org… | [voir bloc] | ⬜ |
| 296 | OceaneGetService | — | L.506 | Point de décision — 'isContributor' et key_exists('interventionStatus', 'value') et is_array('value'['interventionSta… | [voir bloc] | ⬜ |
| 297 | OceaneGetService | — | L.513 | Point de décision — 'activationRequested'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 298 | OceaneGetService | — | L.522 | Point de décision — key_exists('status', 'this'->oceaneData) et is_array('this'->oceaneData['status']). Quel est le c… | [voir bloc] | ⬜ |
| 299 | OceaneGetService | — | L.524 | Point de décision — key_exists('code', 'value') et 'value'['code'] égal à "Restored". Quel est le comportement attend… | [voir bloc] | ⬜ |
| 300 | OceaneGetService | — | L.525 | Point de décision — key_exists('startDate', 'value'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 301 | OceaneGetService | — | L.526 | Point de décision — !is_null('format'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 302 | OceaneGetService | — | L.539 | Point de décision — key_exists('status', 'this'->oceaneData) et is_array('this'->oceaneData['status']). Quel est le c… | [voir bloc] | ⬜ |
| 303 | OceaneGetService | — | L.541 | Point de décision — key_exists('code', 'value') et 'value'['code'] égal à "Resolved". Quel est le comportement attend… | [voir bloc] | ⬜ |
| 304 | OceaneGetService | — | L.542 | Point de décision — key_exists('startDate', 'value'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 305 | OceaneGetService | — | L.543 | Point de décision — !is_null('format'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 306 | OceaneGetService | — | L.561 | Point de décision — key_exists('category', 'this'->oceaneData) et is_array('this'->oceaneData['category']). Quel est … | [voir bloc] | ⬜ |
| 307 | OceaneGetService | — | L.563 | Point de décision — 'idAndLabel'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 308 | OceaneGetService | — | L.577 | Point de décision — key_exists('troubleCause', 'this'->oceaneData) et is_array('this'->oceaneData['troubleCause']). Q… | [voir bloc] | ⬜ |
| 309 | OceaneGetService | — | L.588 | Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyInterven… | [voir bloc] | ⬜ |
| 310 | OceaneGetService | — | L.590 | Point de décision — is_array('value') et key_exists('relatedParty', 'value') et is_array('value'['relatedParty']). Qu… | [voir bloc] | ⬜ |
| 311 | OceaneGetService | — | L.592 | Point de décision — is_array('party') et key_exists('@referredType', 'party') et 'party'['@referredType'] égal à 'Org… | [voir bloc] | ⬜ |
| 312 | OceaneGetService | — | L.597 | Point de décision — 'isContributor' et key_exists('interventionStatus', 'value') et is_array('value'['interventionSta… | [voir bloc] | ⬜ |
| 313 | OceaneGetService | — | L.604 | Point de décision — 'activationAccepted'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 314 | OceaneGetService | — | L.618 | Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyInterven… | [voir bloc] | ⬜ |
| 315 | OceaneGetService | — | L.620 | Point de décision — is_array('value') et key_exists('relatedParty', 'value') et is_array('value'['relatedParty']). Qu… | [voir bloc] | ⬜ |
| 316 | OceaneGetService | — | L.622 | Point de décision — is_array('party') et key_exists('@referredType', 'party') et 'party'['@referredType'] égal à 'Org… | [voir bloc] | ⬜ |
| 317 | OceaneGetService | — | L.627 | Point de décision — 'isContributor' et key_exists('interventionStatus', 'value') et is_array('value'['interventionSta… | [voir bloc] | ⬜ |
| 318 | OceaneGetService | — | L.631 | Point de décision — 'activationAccepted'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 319 | OceaneGetService | — | L.647 | Point de décision — key_exists('criticity', 'this'->oceaneData) et is_array('this'->oceaneData['criticity']). Quel es… | [voir bloc] | ⬜ |
| 320 | OceaneGetService | — | L.649 | Point de décision — 'idAndLabel'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 321 | OceaneGetService | — | L.668 | Point de décision — key_exists('targetRestorationDate', 'this'->oceaneData). Quel est le comportement attendu dans le… | [voir bloc] | ⬜ |
| 322 | OceaneGetService | — | L.669 | Point de décision — !is_null('format'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 323 | OceaneGetService | — | L.684 | Point de décision — key_exists('plannedRestorationDate', 'this'->oceaneData). Quel est le comportement attendu dans l… | [voir bloc] | ⬜ |
| 324 | OceaneGetService | — | L.685 | Point de décision — !is_null('format'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 325 | OceaneGetService | — | L.695 | Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyInterven… | [voir bloc] | ⬜ |
| 326 | OceaneGetService | — | L.696 | Point de décision — key_exists('relatedParty', 'this'->oceaneData['partyIntervention'][0]) et is_array('this'->oceane… | [voir bloc] | ⬜ |
| 327 | OceaneGetService | — | L.698 | Point de décision — is_array('value') et key_exists('actionInProgress', 'value') et key_exists('startDate', 'value'['… | [voir bloc] | ⬜ |
| 328 | OceaneGetService | — | L.700 | Point de décision — !is_null('format'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 329 | OceaneGetService | — | L.713 | Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyInterven… | [voir bloc] | ⬜ |
| 330 | OceaneGetService | — | L.714 | Point de décision — key_exists('relatedParty', 'this'->oceaneData['partyIntervention'][0]) et is_array('this'->oceane… | [voir bloc] | ⬜ |
| 331 | OceaneGetService | — | L.716 | Point de décision — is_array('value') et key_exists('actionInProgress', 'value') et key_exists('description', 'value'… | [voir bloc] | ⬜ |
| 332 | OceaneGetService | — | L.728 | Point de décision — key_exists('partyIntervention', 'this'->oceaneData) et is_array('this'->oceaneData['partyInterven… | [voir bloc] | ⬜ |
| 333 | OceaneGetService | — | L.729 | Point de décision — key_exists('relatedParty', 'this'->oceaneData['partyIntervention'][0]) et is_array('this'->oceane… | [voir bloc] | ⬜ |
| 334 | OceaneGetService | — | L.731 | Point de décision — is_array('value') et key_exists('id', 'value'). Quel est le comportement attendu dans le cas cont… | [voir bloc] | ⬜ |
| 335 | OceaneGetService | — | L.743 | Point de décision — 'driDate' différent de '' et 'drcDate' différent de ''. Quel est le comportement attendu dans le … | [voir bloc] | ⬜ |
| 336 | OceaneGetService | — | L.746 | Point de décision — 'drcDate' différent de ''. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 337 | OceaneGetService | — | L.749 | Point de décision — 'driDate' différent de ''. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 338 | OceaneGetService | — | L.756 | Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource… | [voir bloc] | ⬜ |
| 339 | OceaneGetService | — | L.757 | Point de décision — key_exists('resourceCharacteristic', 'this'->oceaneData['relatedResource']). Quel est le comporte… | [voir bloc] | ⬜ |
| 340 | OceaneGetService | — | L.759 | Point de décision — is_array('value') et key_exists('id', 'value') et 'value'['id'] égal à 'CLASITE'. Quel est le com… | [voir bloc] | ⬜ |
| 341 | OceaneGetService | — | L.760 | Point de décision — key_exists('value', 'value'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 342 | OceaneGetService | — | L.771 | Point de décision — key_exists('relatedResource', 'this'->oceaneData) et is_array('this'->oceaneData['relatedResource… | [voir bloc] | ⬜ |
| 343 | OceaneService | — | L.97 | Point de décision — property_exists('result', 'faultstring') et 'result'->faultstring différent de ''. Quel est le co… | [voir bloc] | ⬜ |
| 344 | OceaneService | — | L.99 | Point de décision — property_exists('result', 'returnedRecordsNumber') et 'result'->returnedRecordsNumber égal à 0. Q… | [voir bloc] | ⬜ |
| 345 | OceaneService | — | L.101 | Point de décision — property_exists('result'->TroubleTicketResponse, 'TroubleTicketResponse'). Quel est le comporteme… | [voir bloc] | ⬜ |
| 346 | OceaneService | — | L.104 | Point de décision — property_exists('troubleTicketResponse'->InstalledResource, 'Parameters') et property_exists('tro… | [voir bloc] | ⬜ |
| 347 | OceaneService | — | L.106 | Point de décision — property_exists('val1', 'id') et 'CLASITE' égal à 'val1'->id. Quel est le comportement attendu da… | [voir bloc] | ⬜ |
| 348 | OceaneService | — | L.125 | Point de décision — property_exists('troubleTicketResponse'->TroubleTicketStatus, 'statusCode'). Quel est le comporte… | [voir bloc] | ⬜ |
| 349 | OceaneService | — | L.128 | Point de décision — property_exists('troubleTicketResponse', 'local_ComplementaryField'). Quel est le comportement at… | [voir bloc] | ⬜ |
| 350 | OceaneService | — | L.130 | Point de décision — is_array('troubleTicketResponse'->local_ComplementaryField). Quel est le comportement attendu dan… | [voir bloc] | ⬜ |
| 351 | OceaneService | — | L.131 | Point de décision — array_key_exists('3', 'troubleTicketResponse'->local_ComplementaryField) et isset('troubleTicketR… | [voir bloc] | ⬜ |
| 352 | OceaneService | — | L.135 | Point de décision — 'troubleTicketResponse'->local_ComplementaryField[3]->value égal à "" et is_array('troubleTicketR… | [voir bloc] | ⬜ |
| 353 | OceaneService | — | L.142 | Point de décision — array_key_exists('2', 'troubleTicketResponse'->local_ComplementaryField) et isset('troubleTicketR… | [voir bloc] | ⬜ |
| 354 | OceaneService | — | L.146 | Point de décision — array_key_exists('5', 'troubleTicketResponse'->local_ComplementaryField) et isset('troubleTicketR… | [voir bloc] | ⬜ |
| 355 | OceaneService | — | L.150 | Point de décision — array_key_exists('4', 'troubleTicketResponse'->local_ComplementaryField) et isset('troubleTicketR… | [voir bloc] | ⬜ |
| 356 | OceaneService | — | L.157 | Point de décision — property_exists('troubleTicketResponse', 'troubleTicketPriority'). Quel est le comportement atten… | [voir bloc] | ⬜ |
| 357 | OceaneService | — | L.161 | Point de décision — property_exists('troubleTicketResponse', 'description'). Quel est le comportement attendu dans le… | [voir bloc] | ⬜ |
| 358 | OceaneService | — | L.164 | Point de décision — property_exists('troubleTicketResponse', 'local_ShortLabel'). Quel est le comportement attendu da… | [voir bloc] | ⬜ |
| 359 | OceaneService | — | L.167 | Point de décision — property_exists('troubleTicketResponse', 'TroubleCause'). Quel est le comportement attendu dans l… | [voir bloc] | ⬜ |
| 360 | OceaneService | — | L.168 | Point de décision — property_exists('troubleTicketResponse'->TroubleCause, 'local_internalcomplement'). Quel est le c… | [voir bloc] | ⬜ |
| 361 | OceaneService | — | L.171 | Point de décision — property_exists('troubleTicketResponse'->TroubleCause, 'troubleCauseCodeCategory'). Quel est le c… | [voir bloc] | ⬜ |
| 362 | OceaneService | — | L.174 | Point de décision — property_exists('troubleTicketResponse'->TroubleCause, 'troubleCauseLabel'). Quel est le comporte… | [voir bloc] | ⬜ |
| 363 | OceaneService | — | L.177 | Point de décision — property_exists('troubleTicketResponse'->TroubleCause, 'troubleCauseDescription'). Quel est le co… | [voir bloc] | ⬜ |
| 364 | OceaneService | — | L.180 | Point de décision — property_exists('troubleTicketResponse'->TroubleCause, 'troubleCauseCodeCategory'). Quel est le c… | [voir bloc] | ⬜ |
| 365 | OceaneService | — | L.185 | Point de décision — property_exists('troubleTicketResponse', 'troubleType'). Quel est le comportement attendu dans le… | [voir bloc] | ⬜ |
| 366 | OceaneService | — | L.192 | Point de décision — 'posteAssocie' égal à ''. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 367 | OceaneService | — | L.196 | Point de décision — !is_null('connectedEds') et 'value'->partyRoleType égal à "TroubleResolutionContributor" et prope… | [voir bloc] | ⬜ |
| 368 | OceaneService | — | L.199 | Point de décision — key_exists(2, 'value'->Local_PartyIntervention->interventionStatus). Quel est le comportement att… | [voir bloc] | ⬜ |
| 369 | OceaneService | — | L.203 | Point de décision — 'value'->Local_PartyIntervention->level égal à 1 et 'interventionStatus' et 'value'->PartyRoleSet… | [voir bloc] | ⬜ |
| 370 | OceaneService | — | L.207 | Point de décision — 'value'->Local_PartyIntervention->level égal à 2 et 'interventionStatus' et 'value'->PartyRoleSet… | [voir bloc] | ⬜ |
| 371 | OceaneService | — | L.215 | Point de décision — !is_null('connectedEds') et 'value'->partyRoleType égal à "TroubleResolutionContributor" et prope… | [voir bloc] | ⬜ |
| 372 | OceaneService | — | L.216 | Point de décision — 'value'->Local_PartyIntervention->interventionStatus->status égal à 'Requested'. Quel est le comp… | [voir bloc] | ⬜ |
| 373 | OceaneService | — | L.226 | Point de décision — 'driDate' différent de '' et 'drcDate' différent de ''. Quel est le comportement attendu dans le … | [voir bloc] | ⬜ |
| 374 | OceaneService | — | L.229 | Point de décision — 'drcDate' différent de ''. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 375 | OceaneService | — | L.232 | Point de décision — 'driDate' différent de ''. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 376 | OceaneService | — | L.240 | Point de décision — property_exists('troubleTicketResponse', 'PartyRole'). Quel est le comportement attendu dans le c… | [voir bloc] | ⬜ |
| 377 | OceaneService | — | L.244 | Point de décision — !'checkInc'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 378 | OceaneService | — | L.245 | Point de décision — key_exists('i', 'troubleTicketResponse'->PartyRole) et property_exists('troubleTicketResponse'->P… | [voir bloc] | ⬜ |
| 379 | OceaneService | — | L.247 | Point de décision — property_exists('troubleTicketResponse'->PartyRole['i']->PartyRoleSet, 'local_groupactioninprogre… | [voir bloc] | ⬜ |
| 380 | OceaneService | — | L.253 | Point de décision — property_exists('troubleTicketResponse'->PartyRole['i']->PartyRoleSet, 'local_groupactioninprogre… | [voir bloc] | ⬜ |
| 381 | OceaneService | — | L.258 | Point de décision — 'checkIncDate' et 'checkIncAct'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 382 | OceaneService | — | L.266 | Point de décision — property_exists('troubleTicketResponse', 'local_onbhfollowup'). Quel est le comportement attendu … | [voir bloc] | ⬜ |
| 383 | OceaneService | — | L.270 | Point de décision — property_exists('troubleTicketResponse', 'troubleTicketCategory'). Quel est le comportement atten… | [voir bloc] | ⬜ |
| 384 | OceaneService | — | L.377 | Point de décision — array_key_exists('trouble_ticket_priority', 'data') et isset('data'['trouble_ticket_priority']). … | [voir bloc] | ⬜ |
| 385 | OceaneService | — | L.382 | Point de décision — array_key_exists('ticket_id', 'data') et isset('data'['ticket_id']). Quel est le comportement att… | [voir bloc] | ⬜ |
| 386 | OceaneService | — | L.386 | Point de décision — array_key_exists('astroid', 'data') et isset('data'['astroid']). Quel est le comportement attendu… | [voir bloc] | ⬜ |
| 387 | OceaneService | — | L.390 | Point de décision — array_key_exists('party_role_party_ID', 'data') et isset('data'['party_role_party_ID']). Quel est… | [voir bloc] | ⬜ |
| 388 | OceaneService | — | L.394 | Point de décision — array_key_exists('postes_associe', 'data') et isset('data'['postes_associe']). Quel est le compor… | [voir bloc] | ⬜ |
| 389 | OceaneService | — | L.398 | Point de décision — array_key_exists('niv_urgence', 'data') et isset('data'['niv_urgence']). Quel est le comportement… | [voir bloc] | ⬜ |
| 390 | OceaneService | — | L.402 | Point de décision — array_key_exists('action_eds', 'data') et isset('data'['action_eds']). Quel est le comportement a… | [voir bloc] | ⬜ |
| 391 | OceaneService | — | L.406 | Point de décision — array_key_exists('commentaire_eds', 'data') et isset('data'['commentaire_eds']). Quel est le comp… | [voir bloc] | ⬜ |
| 392 | OceaneService | — | L.410 | Point de décision — array_key_exists('eds_pilote', 'data') et isset('data'['eds_pilote']). Quel est le comportement a… | [voir bloc] | ⬜ |
| 393 | OceaneService | — | L.420 | Point de décision — array_key_exists('local_commentaire', 'data') et isset('data'['local_commentaire']). Quel est le … | [voir bloc] | ⬜ |
| 394 | OceaneService | — | L.423 | Point de décision — array_key_exists('nb_plaintes', 'data') et isset('data'['nb_plaintes']). Quel est le comportement… | [voir bloc] | ⬜ |
| 395 | OceaneService | — | L.433 | Point de décision — array_key_exists('description', 'data') et isset('data'['description']). Quel est le comportement… | [voir bloc] | ⬜ |
| 396 | OceaneService | — | L.436 | Point de décision — array_key_exists('trouble_type', 'data') et isset('data'['trouble_type']). Quel est le comporteme… | [voir bloc] | ⬜ |
| 397 | OceaneService | — | L.439 | Point de décision — array_key_exists('trouble_severity', 'data') et isset('data'['trouble_severity']). Quel est le co… | [voir bloc] | ⬜ |
| 398 | OceaneService | — | L.442 | Point de décision — array_key_exists('party_set_ID', 'data') et isset('data'['party_set_ID']). Quel est le comporteme… | [voir bloc] | ⬜ |
| 399 | OceaneService | — | L.446 | Point de décision — array_key_exists('requested_date', 'data') et isset('data'['requested_date']). Quel est le compor… | [voir bloc] | ⬜ |
| 400 | OceaneService | — | L.456 | Point de décision — 'nbCellules' <= 'maxImapct'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 401 | OceaneService | — | L.483 | Point de décision — array_key_exists('description', 'data') et isset('data'['description']). Quel est le comportement… | [voir bloc] | ⬜ |
| 402 | OceaneService | — | L.486 | Point de décision — array_key_exists('trouble_type', 'data') et isset('data'['trouble_type']). Quel est le comporteme… | [voir bloc] | ⬜ |
| 403 | OceaneService | — | L.489 | Point de décision — array_key_exists('trouble_severity', 'data') et isset('data'['trouble_severity']). Quel est le co… | [voir bloc] | ⬜ |
| 404 | OceaneService | — | L.492 | Point de décision — array_key_exists('party_set_ID', 'data') et isset('data'['party_set_ID']). Quel est le comporteme… | [voir bloc] | ⬜ |
| 405 | OceaneService | — | L.517 | Point de décision — !'generique'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 406 | OceaneService | — | L.535 | Point de décision — 'actifDri'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 407 | OceaneService | — | L.622 | Point de décision — 'data'['donnee_complementaire'] différent de ''. Quel est le comportement attendu dans le cas con… | [voir bloc] | ⬜ |
| 408 | OceaneService | — | L.625 | Point de décision — ('actifDri' égal à '1') ou (key_exists('api', 'this'->app->config) et 'this'->app->config['api'])… | [voir bloc] | ⬜ |
| 409 | OceaneService | — | L.630 | Point de décision — 'confirmTowStep' égal à 'oui'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 410 | OceaneService | — | L.638 | Point de décision — key_exists('code', 'retourUpdate'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 411 | OceaneService | — | L.646 | Point de décision — !key_exists('api', 'data'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 412 | OceaneService | — | L.728 | Point de décision — 'data'['priorite_commentaire'] égal à ''. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 413 | OceaneService | — | L.732 | Point de décision — 'data'['priorite_commentaire'] égal à '4'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 414 | VariableBaseService | — | L.27 | Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 415 | VariableBaseService | — | L.39 | Point de décision — property_exists('this'->findAndGet['installed_resource']->Parameters, 'Parameter'). Quel est le c… | [voir bloc] | ⬜ |
| 416 | VariableBaseService | — | L.42 | Point de décision — !is_null('res'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 417 | VariableBaseService | — | L.48 | Point de décision — property_exists('this'->findAndGet['installed_resource']->Attributes, 'Attribute'). Quel est le c… | [voir bloc] | ⬜ |
| 418 | VariableBaseService | — | L.51 | Point de décision — !is_null('res'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 419 | VariableBaseService | — | L.59 | Point de décision — !is_null('res'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 420 | VariableBaseService | — | L.79 | Point de décision — 'this'->id1. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 421 | VariableService | — | L.123 | Point de décision — 'arg' égal à 'Temperature' ou 'arg' égal à 'Etat_batterie' ou 'arg' égal à 'Tension_batterie' ou … | [voir bloc] | ⬜ |
| 422 | VariableService | — | L.131 | Point de décision — property_exists('parameters', 'Parameter'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 423 | VariableService | — | L.133 | Point de décision — property_exists('val1', 'id') et 'val1'->id égal à 'LIBSITE'. Quel est le comportement attendu da… | [voir bloc] | ⬜ |
| 424 | VariableService | — | L.137 | Point de décision — 'libSite' différent de "". Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 425 | VariableService | — | L.142 | Point de décision — 'arg' égal à 'DSLAM_PRODUIT_DSLAM' ou 'arg' égal à 'DSLAM_PRODUIT_CHASSIS' ou 'arg' égal à 'DSLAM… | [voir bloc] | ⬜ |
| 426 | VariableService | — | L.143 | Point de décision — is_null('this'->variableRepository). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 427 | VariableService | — | L.147 | Point de décision — !'replaceValue'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 428 | VariableService | — | L.149 | Point de décision — 'replaceValue' différent de '' et !is_null('replaceValue') et !is_array('replaceValue'). Quel est… | [voir bloc] | ⬜ |
| 429 | VariableService | — | L.153 | Point de décision — OceaneTools::isValidVariable('replaceValue') et !is_array('replaceValue'). Quel est le comporteme… | [voir bloc] | ⬜ |
| 430 | VariableService | — | L.165 | Point de décision — is_null('this'->transitoolService). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 431 | VariableService | — | L.171 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 432 | VariableService | — | L.178 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 433 | VariableService | — | L.185 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 434 | VariableService | — | L.195 | Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le compo… | [voir bloc] | ⬜ |
| 435 | VariableService | — | L.203 | Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le compo… | [voir bloc] | ⬜ |
| 436 | VariableService | — | L.210 | Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le compo… | [voir bloc] | ⬜ |
| 437 | VariableService | — | L.217 | Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le compo… | [voir bloc] | ⬜ |
| 438 | VariableService | — | L.226 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 439 | VariableService | — | L.234 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 440 | VariableService | — | L.242 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 441 | VariableService | — | L.251 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 442 | VariableService | — | L.259 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 443 | VariableService | — | L.270 | Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 444 | VariableService | — | L.276 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 445 | VariableService | — | L.284 | Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 446 | VariableService | — | L.287 | Point de décision — !isset('this'->findAndGet['message']) et !is_null('this'->findAndGet['installed_resource']) et pr… | [voir bloc] | ⬜ |
| 447 | VariableService | — | L.291 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 448 | VariableService | — | L.297 | Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 449 | VariableService | — | L.301 | Point de décision — !isset('this'->findAndGet['message']) et !is_null('this'->findAndGet['rd_plus']). Quel est le com… | [voir bloc] | ⬜ |
| 450 | VariableService | — | L.304 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 451 | VariableService | — | L.310 | Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 452 | VariableService | — | L.314 | Point de décision — !isset('this'->findAndGet['message']) et !is_null('this'->findAndGet['description']). Quel est le… | [voir bloc] | ⬜ |
| 453 | VariableService | — | L.317 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 454 | VariableService | — | L.323 | Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 455 | VariableService | — | L.326 | Point de décision — !isset('this'->findAndGet['message']) et !is_null('this'->findAndGet['code_detecteur']). Quel est… | [voir bloc] | ⬜ |
| 456 | VariableService | — | L.327 | Point de décision — !is_null('this'->findAndGet['code_detecteur']). Quel est le comportement attendu dans le cas cont… | [voir bloc] | ⬜ |
| 457 | VariableService | — | L.333 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 458 | VariableService | — | L.347 | Point de décision — in_array('type', 'this'->arrayRessourcesTransAvecExt). Quel est le comportement attendu dans le c… | [voir bloc] | ⬜ |
| 459 | VariableService | — | L.353 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 460 | VariableService | — | L.375 | Point de décision — OceaneTools::isValidVariable('replaceValue') et gettype('replaceValue') différent de 'boolean'. Q… | [voir bloc] | ⬜ |
| 461 | VariableService | — | L.402 | Point de décision — 'this'->typeRessource égal à 'TRONCABLE'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 462 | VariableService | — | L.405 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 463 | VariableService | — | L.415 | Point de décision — !is_null('resultColumn') et 'resultColumn' différent de ''. Quel est le comportement attendu dans… | [voir bloc] | ⬜ |
| 464 | VariableService | — | L.418 | Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contra… | [voir bloc] | ⬜ |
| 465 | VariableService | — | L.424 | Point de décision — 'this'->globalApiRepository->isVariableAdminExist('arg', 'type'). Quel est le comportement attend… | [voir bloc] | ⬜ |
| 466 | VariableService | — | L.426 | Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 467 | VariableService | — | L.429 | Point de décision — !isset('this'->findAndGet['message']). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 468 | VariableService | — | L.431 | Point de décision — !is_null('this'->findAndGet['installed_resource']) et property_exists('this'->findAndGet['install… | [voir bloc] | ⬜ |
| 469 | VariableService | — | L.434 | Point de décision — !is_null('this'->findAndGet['installed_service']) et property_exists('this'->findAndGet['installe… | [voir bloc] | ⬜ |
| 470 | VariableService | — | L.440 | Point de décision — 'resourceSpecification' différent de "". Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 471 | VariableService | — | L.446 | Point de décision — count('tabIdentifiants') > 0. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 472 | VariableService | — | L.448 | Point de décision — isset('replaceValue'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 473 | VariableService | — | L.478 | Point de décision — 'this'->transcodage('ext1')); 'isSitePassifext2' = 'this'->refSiteRepository->isSitePassif('this'… | [voir bloc] | ⬜ |
| 474 | VariableService | — | L.489 | Point de décision — 'ext1_status' égal à 0. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 475 | VariableService | — | L.493 | Point de décision — 'ext1_status' égal à 1 et 'ext2_status' égal à 0. Quel est le comportement attendu dans le cas co… | [voir bloc] | ⬜ |
| 476 | VariableService | — | L.497 | Point de décision — 'ext1_status' égal à -1. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 477 | VariableService | — | L.501 | Point de décision — 'ext2_status' égal à -1. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 478 | VariableService | — | L.513 | Point de décision — 'typeRessource' égal à 'TRONCABLE'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 479 | VariableService | — | L.519 | Point de décision — 'variable' différent de ''. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 480 | VariableService | — | L.527 | Point de décision — 'intervenantMatriceRefsite' différent de "###'variableAdministree'###". Quel est le comportement … | [voir bloc] | ⬜ |
| 481 | VariableService | — | L.563 | Point de décision — 'typeRessource' égal à 'MIE'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 482 | VariableService | — | L.566 | Point de décision — 'ext' égal à 'tabs_action_ext1'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 483 | VariableService | — | L.568 | Point de décision — 'ext' égal à 'tabs_action_ext2'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 484 | VariableService | — | L.577 | Point de décision — 'techno' égal à 'FH'. Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 485 | VariableService | — | L.592 | Point de décision — gettype('resultQuery') différent de 'boolean' et 'resultQuery' différent de '' et is_array('resul… | [voir bloc] | ⬜ |
| 486 | VariableService | — | L.594 | Point de décision — key_exists('ID', 'resultQuery'). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 487 | VariableService | — | L.605 | Point de décision — strpos('intervenantMatriceRefsite', "/"). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 488 | VariableService | — | L.616 | Point de décision — strpos('value', "/"). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 489 | VariableService | — | L.657 | Point de décision — !in_array('infraContextePari', ["###'variableAdministree'###", '']). Quel est le comportement att… | [voir bloc] | ⬜ |
| 490 | VariableService | — | L.658 | Point de décision — is_null('this'->dataPariv2). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 491 | VariableService | — | L.661 | Point de décision — 'this'->app->get('AstroBase')->isJson('dataJson'). Quel est le comportement attendu dans le cas c… | [voir bloc] | ⬜ |
| 492 | VariableService | — | L.670 | Point de décision — OceaneTools::isValidVariable('replaceValue') et gettype('replaceValue') différent de 'boolean'. Q… | [voir bloc] | ⬜ |
| 493 | VariableService | — | L.756 | Point de décision — isset('mapping'['variable']). Quel est le comportement attendu dans le cas contraire ? | [voir bloc] | ⬜ |
| 494 | VariableService | — | L.760 | Point de décision — is_array('value') et key_exists('key', 'value'). Quel est le comportement attendu dans le cas con… | [voir bloc] | ⬜ |

*494 gap(s) — chaque case ⬜ représente une décision à prendre avant migration.*

---

## Contexte Code — Copier dans Copilot

---

**Gap #1 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 123
Contexte   :
```php

        $isLocked = $this->verrouRepository->isLocked($astroId, "confirmerIncident", true, $loginId);
        if ($isLocked === true) {
            $messageVerrou = $this->verrouRepository->getLabelVerrou($astroId, 'confirmerIncident');
        } else {
            $messageVerrou = '';
```

Question métier : Point de décision — 'isLocked' égal à = true. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #2 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 135
Contexte   :
```php

        $impact = $dataASTRO['ID_IMPACT_CLIENT_PRECONISE'];
        if ($impact != '') {
            $label = $this->astroRepository->getLabelPrio($dataASTRO['ID_IMPACT_CLIENT_PRECONISE']);
            $libelleImpactClient = $this->astroRepository->getLibelleImpactClient($dataASTRO['ID_IMPACT_CLIENT_PRECONISE']);

```

Question métier : Point de décision — 'impact' différent de ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #3 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 169
Contexte   :
```php
        $isMe = $this->verrouRepository->isLockedByMe($astroId, $label);
        $labelFinal = $this->verrouRepository->getLabelReservation($astroId, $label, $isMe);
        if ($labelFinal == '') {
            $imageName = 'doigt_vert';
        } else {
            if ($isMe) {
```

Question métier : Point de décision — 'labelFinal' égal à ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #4 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 172
Contexte   :
```php
            $imageName = 'doigt_vert';
        } else {
            if ($isMe) {
                $imageName = 'doigt_violet';
            } else {
                $imageName = 'doigt_rouge';
```

Question métier : Point de décision — 'isMe'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #5 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 239
Contexte   :
```php
        $this->app->get('TraceRepository')->setTrace($astroId, "RETOUR OCEANE AJOUT COMMENTAIRE ABANDON EVENEMENT AUTO", $retourUpdate, $this->sessId, $ticketId);

        if (array_key_exists('message', $result) && array_key_exists('code', $result) && array_key_exists('description', $result)) {

            if ($result['message'] == 'Functional error: Ticket in closed status') {
                $this->abandonBatchRepository->updateTicketEtat($ticketId);
```

Question métier : Point de décision — array_key_exists('message', 'result') et array_key_exists('code', 'result') et array_key_exists('description', 'result'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #6 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 241
Contexte   :
```php
        if (array_key_exists('message', $result) && array_key_exists('code', $result) && array_key_exists('description', $result)) {

            if ($result['message'] == 'Functional error: Ticket in closed status') {
                $this->abandonBatchRepository->updateTicketEtat($ticketId);
                return 2;
            } else {
```

Question métier : Point de décision — 'result'['message'] égal à 'Functional error: Ticket in closed status'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #7 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 266
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

**Gap #8 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 319
Contexte   :
```php
        $this->app->get('TraceRepository')->setTrace($astroId, "RETOUR OCEANE AJOUT COMMENTAIRE ABANDON EVENEMENT", $retourUpdate, $this->sessId, $ticketId);

        if (array_key_exists('message', $result) && array_key_exists('code', $result) && array_key_exists('description', $result)) {
            $message = 'code  :' . $result['code'] . 'message  :' . $result['message'] . '  description : ' . $result['description'];
            $code = $incidentEnCours ? 'E_ABANDON_EVENEMENT' : 'API_E_ABANDON_CARTE_BRASIL_ETEINTE';
            return array(
```

Question métier : Point de décision — array_key_exists('message', 'result') et array_key_exists('code', 'result') et array_key_exists('description', 'result'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #9 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 391
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

**Gap #10 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 407
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

**Gap #11 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 408
Contexte   :
```php
        }
        if ($dataAdelia['TOTAL_CLIENTS'] > 0) {
            if ($dataAstro['ADELIA_MANUEL'] == 'o') {
                $dataAdeliaManuel = $this->adeliaRepository->getDataBlobManuel($dataAstro['ID_TICKET_ASTRO']);
                if ($dataAdeliaManuel['BEGIN_DATE'] != '' && $dataAdeliaManuel['SEUIL_GRAVE'] != '' && $dataAdeliaManuel['SEUIL_MAJEUR'] != '') {
                    $commentaire .= 'grave à partir du ' . $this->adeliaService->getDateSeuil($dataAdeliaManuel['BEGIN_DATE'], $dataAdeliaManuel['SEUIL_GRAVE'], true) . $rc;
```

Question métier : Point de décision — 'dataAstro'['ADELIA_MANUEL'] égal à 'o'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #12 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 410
Contexte   :
```php
            if ($dataAstro['ADELIA_MANUEL'] == 'o') {
                $dataAdeliaManuel = $this->adeliaRepository->getDataBlobManuel($dataAstro['ID_TICKET_ASTRO']);
                if ($dataAdeliaManuel['BEGIN_DATE'] != '' && $dataAdeliaManuel['SEUIL_GRAVE'] != '' && $dataAdeliaManuel['SEUIL_MAJEUR'] != '') {
                    $commentaire .= 'grave à partir du ' . $this->adeliaService->getDateSeuil($dataAdeliaManuel['BEGIN_DATE'], $dataAdeliaManuel['SEUIL_GRAVE'], true) . $rc;
                    $commentaire .= 'majeur à partir du ' . $this->adeliaService->getDateSeuil($dataAdeliaManuel['BEGIN_DATE'], $dataAdeliaManuel['SEUIL_MAJEUR'], true) . $rc;
                } else {
```

Question métier : Point de décision — 'dataAdeliaManuel'['BEGIN_DATE'] différent de '' et 'dataAdeliaManuel'['SEUIL_GRAVE'] différent de '' et 'dataAdeliaManuel'['SEUIL_MAJEUR'] différent de ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #13 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 435
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

**Gap #14 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 449
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

**Gap #15 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 450
Contexte   :
```php

        if ($dataAdelia['TOTAL_CLIENTS'] > 0) {
            if ($dataAstro['ADELIA_MANUEL'] == 'o') {
                $dataAdeliaManuel = $this->adeliaRepository->getDataBlobManuel($dataAstro['ID_TICKET_ASTRO']);
                if ($dataAdeliaManuel['BEGIN_DATE'] != '' && $dataAdeliaManuel['SEUIL_GRAVE'] != '' && $dataAdeliaManuel['SEUIL_MAJEUR'] != '') {
                    $commentaire .= 'grave à partir du ' . $this->adeliaService->getDateSeuil($dataAdeliaManuel['BEGIN_DATE'], $dataAdeliaManuel['SEUIL_GRAVE'], true) . $rc;
```

Question métier : Point de décision — 'dataAstro'['ADELIA_MANUEL'] égal à 'o'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #16 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 452
Contexte   :
```php
            if ($dataAstro['ADELIA_MANUEL'] == 'o') {
                $dataAdeliaManuel = $this->adeliaRepository->getDataBlobManuel($dataAstro['ID_TICKET_ASTRO']);
                if ($dataAdeliaManuel['BEGIN_DATE'] != '' && $dataAdeliaManuel['SEUIL_GRAVE'] != '' && $dataAdeliaManuel['SEUIL_MAJEUR'] != '') {
                    $commentaire .= 'grave à partir du ' . $this->adeliaService->getDateSeuil($dataAdeliaManuel['BEGIN_DATE'], $dataAdeliaManuel['SEUIL_GRAVE'], true) . $rc;
                    $commentaire .= 'majeur à partir du ' . $this->adeliaService->getDateSeuil($dataAdeliaManuel['BEGIN_DATE'], $dataAdeliaManuel['SEUIL_MAJEUR'], true) . $rc;
                } else {
```

Question métier : Point de décision — 'dataAdeliaManuel'['BEGIN_DATE'] différent de '' et 'dataAdeliaManuel'['SEUIL_GRAVE'] différent de '' et 'dataAdeliaManuel'['SEUIL_MAJEUR'] différent de ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #17 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 461
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

**Gap #18 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 534
Contexte   :
```php
        $this->app->get('TraceRepository')->setTrace($astroId, "OCEANE REPONSE", $result, $idUtilisateur, $ticketId);

        if (key_exists('code', $result) && key_exists('message', $result)) {
            $message = $result['code'] . ' ' . $result['message'];
            $errorOceane = $messageManager->setMessage('E_CONFIRM', $message);
            return array(
```

Question métier : Point de décision — key_exists('code', 'result') et key_exists('message', 'result'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #19 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 566
Contexte   :
```php

            $result = $this->abandonnerProcessAuto($ticket['ID_JEU_PARAM'], $ticket['TICKETOCEANEID'], $ticket['ID_TICKET_ASTRO'], $ticket['TYPE_RESSOURCE'], '', $loginId);
            if ($result == 1) {
                $this->abandonBatchRepository->updateTicketEtat($ticket['TICKETOCEANEID']);
                $nbOk++;
                echo $ticket['TICKETOCEANEID'] . " : abandon OK <br /> ";
```

Question métier : Point de décision — 'result' égal à 1. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #20 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 570
Contexte   :
```php
                $nbOk++;
                echo $ticket['TICKETOCEANEID'] . " : abandon OK <br /> ";
            } elseif ($result == 2) {
                $this->abandonBatchRepository->updateTicketEtat($ticket['TICKETOCEANEID']);
                $nbKo++;
                echo $ticket['TICKETOCEANEID'] . " : échec abandon <br /> \n";
```

Question métier : Point de décision — 'result' égal à 2. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #21 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 583
Contexte   :
```php
              Nombre de tickets non abandonnés (échec) :  $nbKo <br /> \n";

        if ($nbKo == 0) {
            echo "<b> Traitement OK</b> <br /> \n";
        } else {
            if ($nbOk > 0) {
```

Question métier : Point de décision — 'nbKo' égal à 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #22 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 586
Contexte   :
```php
            echo "<b> Traitement OK</b> <br /> \n";
        } else {
            if ($nbOk > 0) {
                echo "<b> Traitement OK partiel </b> <br /> \n";
            } else {
                echo "<b> Traitement KO</b> <br /> \n";
```

Question métier : Point de décision — 'nbOk' > 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #23 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 617
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

**Gap #24 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 625
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

**Gap #25 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 633
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

**Gap #26 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 639
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

**Gap #27 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 643
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

**Gap #28 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 646
Contexte   :
```php
                $isNetVpnAdelia = 1;
            }
            if ($isNetVpn == '1' && $isNetVpnAdelia == 1) {
                $isNetVpnFinal = '1';
            } else {
                $isNetVpnFinal = '';
```

Question métier : Point de décision — 'isNetVpn' égal à '1' et 'isNetVpnAdelia' égal à 1. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #29 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 661
Contexte   :
```php


            if ($gtr && strtolower($informerClient['label']) == "coupure franche"){
                $priorite = 'P1';
                $impactPreconise = 'Service interrompu';
            } else {
```

Question métier : Point de décision — 'gtr' et strtolower('informerClient'['label']) égal à "coupure franche". Quel est le comportement attendu dans le cas contraire ?

---

**Gap #30 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 665
Contexte   :
```php
                $impactPreconise = 'Service interrompu';
            } else {
                if ($informerClient['priorite'] == '-') {
                    $priorite = (in_array('PRECONISATION_PRIORITE_ADSL', $fonctions)) ? $informerClient['priorite'] : $this->astroRepository->getLibPriorite($astroSession['priority']);
                } else {
                    $priorite = (in_array('PRECONISATION_PRIORITE_ADSL', $fonctions)) ? 'P' . $arrMatricePrio[$idValeurImpactPreconise] : $this->astroRepository->getLibPriorite($astroSession['priority']);
```

Question métier : Point de décision — 'informerClient'['priorite'] égal à '-'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #31 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 705
Contexte   :
```php
    {
        foreach ($data as $k => $value) {
            if (!is_null($value[$typeKey])) {
                $explodeData = explode(' ', $value[$typeKey]);
                $type = $explodeData[0];
                $explodeDataValue = preg_split('/(?=\d)/', $explodeData[1], 2);
```

Question métier : Point de décision — !is_null('value'['typeKey']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #32 — AbandonnerService**

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

**Gap #33 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 768
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

**Gap #34 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 792
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

**Gap #35 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 801
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

**Gap #36 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 802
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

**Gap #37 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 806
Contexte   :
```php
            }
        }
        if (!is_null($countByService) && ((key_exists('gtrs1', $countByService) && $countByService['gtrs1']) || (key_exists('gtrs2', $countByService) && $countByService['gtrs2']))) {
            $dataPrioImpact['gtr_final'] = 'oui';
        } elseif (!is_null($dataPrioImpact) && key_exists('impact_result', $dataPrioImpact)) {
            $dataPrioImpact['gtr_final'] = 'non';
```

Question métier : Point de décision — !is_null('countByService') et ((key_exists('gtrs1', 'countByService') et 'countByService'['gtrs1']) ou (key_exists('gtrs2', 'countByService') et 'countByService'['gtrs2'])). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #38 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 808
Contexte   :
```php
        if (!is_null($countByService) && ((key_exists('gtrs1', $countByService) && $countByService['gtrs1']) || (key_exists('gtrs2', $countByService) && $countByService['gtrs2']))) {
            $dataPrioImpact['gtr_final'] = 'oui';
        } elseif (!is_null($dataPrioImpact) && key_exists('impact_result', $dataPrioImpact)) {
            $dataPrioImpact['gtr_final'] = 'non';
        }
        $dataPrioImpact['impact_result']['TOTAL'] = (is_array($dataPrioImpact) && !empty($dataPrioImpact) && key_exists('impact_result', $dataPrioImpact)) ? array_sum($dataPrioImpact['impact_result']) : 0;
```

Question métier : Point de décision — !is_null('dataPrioImpact') et key_exists('impact_result', 'dataPrioImpact'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #39 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 816
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

**Gap #40 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 822
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

**Gap #41 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 826
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

**Gap #42 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 829
Contexte   :
```php
            foreach ($arrayDeclencher as $k => $v) {
                foreach ($decData as $value2) {
                    if (($k == $value2['TYPE'] || $value2['TYPE'] == '_TOTAL') && !$decDone) {
                        $op = $value2['OPERATOR'];
                        $val = intval($value2['OPERATOR_VALUE']);
                        $gtr = $value2['GTR'] ?? null;
```

Question métier : Point de décision — ('k' égal à 'value2'['TYPE'] ou 'value2'['TYPE'] égal à '_TOTAL') et !'decDone'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #43 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 834
Contexte   :
```php
                        $gtr = $value2['GTR'] ?? null;
                        $gtrOk = is_null($gtr) || (key_exists('gtr_final', $dataPrioImpact) && $dataPrioImpact['gtr_final'] == $gtr);
                        if ($op == '>=') {
                            if ($v >= $val && $gtrOk && !$decDone) {
                                $decStat = true;
                                $decDone = true;
```

Question métier : Point de décision — 'op' égal à '>='. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #44 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 835
Contexte   :
```php
                        $gtrOk = is_null($gtr) || (key_exists('gtr_final', $dataPrioImpact) && $dataPrioImpact['gtr_final'] == $gtr);
                        if ($op == '>=') {
                            if ($v >= $val && $gtrOk && !$decDone) {
                                $decStat = true;
                                $decDone = true;
                            } else {
```

Question métier : Point de décision — 'v' >= 'val' et 'gtrOk' et !'decDone'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #45 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 841
Contexte   :
```php
                                $decStat = false;
                            }
                        } elseif ($op == '<=') {
                            if ($v <= $val && $gtrOk && !$decDone) {
                                $decStat = true;
                                $decDone = true;
```

Question métier : Point de décision — 'op' égal à '<='. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #46 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 842
Contexte   :
```php
                            }
                        } elseif ($op == '<=') {
                            if ($v <= $val && $gtrOk && !$decDone) {
                                $decStat = true;
                                $decDone = true;
                            } else {
```

Question métier : Point de décision — 'v' <= 'val' et 'gtrOk' et !'decDone'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #47 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 849
Contexte   :
```php
                            }
                        }
                    } elseif (is_null($value2['TYPE']) && !is_null($value2['GTR'])) {
                        if (key_exists('gtr_final', $dataPrioImpact) && $dataPrioImpact['gtr_final'] == $value2['GTR'] && !$decDone) {
                            $decStat = true;
                            $decDone = true;
```

Question métier : Point de décision — is_null('value2'['TYPE']) et !is_null('value2'['GTR']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #48 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 850
Contexte   :
```php
                        }
                    } elseif (is_null($value2['TYPE']) && !is_null($value2['GTR'])) {
                        if (key_exists('gtr_final', $dataPrioImpact) && $dataPrioImpact['gtr_final'] == $value2['GTR'] && !$decDone) {
                            $decStat = true;
                            $decDone = true;
                        } else {
```

Question métier : Point de décision — key_exists('gtr_final', 'dataPrioImpact') et 'dataPrioImpact'['gtr_final'] égal à 'value2'['GTR'] et !'decDone'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #49 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 856
Contexte   :
```php
                            $decStat = false;
                        }
                    } elseif (is_null($value2['TYPE']) && is_null($value2['GTR']) && !$decDone) {
                        $decStat = true;
                        $decDone = true;
                    }
```

Question métier : Point de décision — is_null('value2'['TYPE']) et is_null('value2'['GTR']) et !'decDone'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #50 — AbandonnerService**

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

**Gap #51 — AbandonnerService**

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

Question métier : Point de décision — 'doneFlag') break; if ('k' égal à 'value2'['TYPE'] ou 'value2'['TYPE'] égal à '_TOTAL'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #52 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 893
Contexte   :
```php
                    $hnoOk = is_null($hno) || (key_exists('HNO', $dataPrioImpact) && $dataPrioImpact['HNO'] == $hno);
                    $gtrOk = is_null($gtr) || (key_exists('gtr_final', $dataPrioImpact) && $dataPrioImpact['gtr_final'] == $gtr);
                    if ($op == '>=') {
                        if ($v >= $val && $gtrOk && $hnoOk) {
                            $doneFlag = true;
                            return 'P' . $prio;
```

Question métier : Point de décision — 'op' égal à '>='. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #53 — AbandonnerService**

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

**Gap #54 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 898
Contexte   :
```php
                            return 'P' . $prio;
                        }
                    } elseif ($op == '<=') {
                        if ($v <= $val && $gtrOk && $hnoOk) {
                            $doneFlag = true;
                            return 'P' . $prio;
```

Question métier : Point de décision — 'op' égal à '<='. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #55 — AbandonnerService**

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

**Gap #56 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 904
Contexte   :
```php
                        }
                    }
                } elseif (is_null($value2['TYPE']) && !is_null($value2['GTR'])) {
                    $gtr = $value2['GTR'];
                    $hno = $value2['HNO'] ?? null;
                    $prio = $value2['PRIORITE'] ?? null;
```

Question métier : Point de décision — is_null('value2'['TYPE']) et !is_null('value2'['GTR']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #57 — AbandonnerService**

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

**Gap #58 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 913
Contexte   :
```php
                        return 'P' . $prio;
                    }
                } elseif (is_null($value2['TYPE']) && is_null($value2['GTR'])) {
                    $hno = $value2['HNO'] ?? null;
                    $prio = $value2['PRIORITE'] ?? null;
                    $hnoOk = is_null($hno) || (key_exists('HNO', $dataPrioImpact) && $dataPrioImpact['HNO'] == $hno);
```

Question métier : Point de décision — is_null('value2'['TYPE']) et is_null('value2'['GTR']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #59 — AbandonnerService**

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

**Gap #60 — AbandonnerService**

**→ Copier dans Copilot**

Fichier    : AbandonnerService.php
Méthode    : ligne 953
Contexte   :
```php
        $dataAdeliaSavedFirst = $this->adeliaService->saveAdeliaDataFirst( true,$dataAdeliaArraySimulate, $data['ID_TICKET_ASTRO']);

        if (!is_null($result)) {
            $dataAdeliaArray = json_decode($result);
            $dataAdeliaSaved = $this->adeliaService->saveAdeliaData($dataAdeliaArray, $data['ID_TICKET_ASTRO'],array(),true);

```

Question métier : Point de décision — !is_null('result'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #61 — AgirPiloterValidationService**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : ligne 23
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

**Gap #62 — AgirPiloterValidationService**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : ligne 25
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

**Gap #63 — AgirPiloterValidationService**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : ligne 30
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

**Gap #64 — AgirPiloterValidationService**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : ligne 31
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

**Gap #65 — AgirPiloterValidationService**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : ligne 40
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

**Gap #66 — AgirPiloterValidationService**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : ligne 42
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

**Gap #67 — AgirPiloterValidationService**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : ligne 47
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

**Gap #68 — AgirPiloterValidationService**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : ligne 48
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

**Gap #69 — AgirPiloterValidationService**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : ligne 56
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

**Gap #70 — AgirPiloterValidationService**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : ligne 58
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

**Gap #71 — AgirPiloterValidationService**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : ligne 66
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

**Gap #72 — AgirPiloterValidationService**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : ligne 68
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

**Gap #73 — AgirPiloterValidationService**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : ligne 75
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

**Gap #74 — AgirPiloterValidationService**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : ligne 77
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

**Gap #75 — AgirPiloterValidationService**

**→ Copier dans Copilot**

Fichier    : AgirPiloterValidationService.php
Méthode    : ligne 83
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

**Gap #76 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 176
Contexte   :
```php
        $idRscDslam = $rsc['ID_RESSOURCE_DSLAM'];

        if ($this->edrRepository->testDataInfo($astroId) == 0) {
            $msg = $this->interventionHelper->getIndispoMessage();
            return array(
                'msg' => $msg
```

Question métier : Point de décision — 'this'->edrRepository->testDataInfo('astroId') égal à 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #77 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 234
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

**Gap #78 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 237
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

**Gap #79 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 245
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

**Gap #80 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 248
Contexte   :
```php
            $maitreDeport = $this->edrService->getDataMaitreDeport($master, false);
            $idRscMaster = $maitreDeport['id_rsc'];
            if ($maitreDeport['status'] == 'nok') {
                $hMaster = $this->interventionHelper->getHMaster($master, true, $droitEds['guest']);
            } else {
                $hMaster = $this->interventionHelper->getHMaster($master, false, $droitEds['guest']);
```

Question métier : Point de décision — 'maitreDeport'['status'] égal à 'nok'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #81 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 258
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

**Gap #82 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 273
Contexte   :
```php
        $isCarteLigne = (isset($chassisCarte['CARTE']) && in_array($chassisCarte['CARTE'], $listCartes)) ? 'true' : 'false';

        if ($typeRessource == 'DSLAM') {
            $demandeInterventionForm = new DemandeInterventionForm(null, array(
                'app' => $this->app,
                'agp_entite' => $agpEds,
```

Question métier : Point de décision — 'typeRessource' égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #83 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 318
Contexte   :
```php

        }
        if ($typeRessource == 'DSLAM') {
            return array(
                'form' => $demandeInterventionForm,
                'cmd' => $cmd,
```

Question métier : Point de décision — 'typeRessource' égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #84 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 531
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

**Gap #85 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 541
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

**Gap #86 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 551
Contexte   :
```php
        $agpEntite = $this->agpGeneriqueRepository->getEntiteByJeuFamille($idJeuParam, $astroSession['type']);

        if ($typeRessource == 'DSLAM') {

            $alarme = $helper->getIntituleAla($rsc, false);

```

Question métier : Point de décision — 'typeRessource' égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #87 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 570
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

**Gap #88 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 575
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

**Gap #89 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 578
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

**Gap #90 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 586
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

**Gap #91 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 589
Contexte   :
```php
                $maitreDeport = $this->edrService->getDataMaitreDeport($master, false);
                $idRscMaster = $maitreDeport['id_rsc'];
                if ($maitreDeport['status'] == 'nok') {
                    $hMaster = $this->interventionHelper->getHMaster($master, true, $droitEds['guest']);
                } else {
                    $hMaster = $this->interventionHelper->getHMaster($master, false, $droitEds['guest']);
```

Question métier : Point de décision — 'maitreDeport'['status'] égal à 'nok'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #92 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 598
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

**Gap #93 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 606
Contexte   :
```php
        }

        if ($typeRessource == 'MIE') {
            $args[] = 'FG_NOMNAEQP';

        }
```

Question métier : Point de décision — 'typeRessource' égal à 'MIE'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #94 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 611
Contexte   :
```php
        }

        if ($typeRessource == 'SLN' || $typeRessource == 'WDM_SID') {
            $args[] = 'FG_E1NOMNAEQP';

            $args[] = 'FG_E2NOMNAEQP';
```

Question métier : Point de décision — 'typeRessource' égal à 'SLN' ou 'typeRessource' égal à 'WDM_SID'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #95 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 617
Contexte   :
```php
        }

        if ($typeRessource == 'DSLAM') {
            $demandeInterventionGeneriqueForm = new DemandeInterventionGeneriqueForm(null, array(
                'app' => $this->app,
                'agp_famille' => $agpFamille,
```

Question métier : Point de décision — 'typeRessource' égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #96 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 653
Contexte   :
```php
            ));
        }
        if ($typeRessource == 'DSLAM') {
            return array(
                'form' => $demandeInterventionGeneriqueForm,
                'cmd' => $cmd,
```

Question métier : Point de décision — 'typeRessource' égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #97 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 708
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

**Gap #98 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 712
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

**Gap #99 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 717
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

**Gap #100 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 731
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

**Gap #101 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 742
Contexte   :
```php
        $agpSuivreHno = 0;

        if ($oceaneData['herite_oceane_hno'] == 1) {
            $agpSuivreHno = $oceaneData['herite_oceane_hno'] == 1 ? $oceaneData['herite_oceane_hno'] : 0;
        } else {
            $priorityHoHno = $this->agpGeneriqueRepository->getActivationHoHnoByJeu($idJeuParam, $oceaneData['oceane_priority']);
```

Question métier : Point de décision — 'oceaneData'['herite_oceane_hno'] égal à 1. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #102 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 747
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

**Gap #103 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 748
Contexte   :
```php

            if (key_exists($oceaneData['oceane_priority'], $priorityHoHno)) {
                if ($data['agp_ho_hno_generique'] == 'HO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_ho'] == '1') {
                    $agpSuivreHno = 0;
                } elseif ($data['agp_ho_hno_generique'] == 'HNO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_hno'] == '1') {
                    $agpSuivreHno = 1;
```

Question métier : Point de décision — 'data'['agp_ho_hno_generique'] égal à 'HO' et 'priorityHoHno'['oceaneData'['oceane_priority']]['activation_ho'] égal à '1'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #104 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 750
Contexte   :
```php
                if ($data['agp_ho_hno_generique'] == 'HO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_ho'] == '1') {
                    $agpSuivreHno = 0;
                } elseif ($data['agp_ho_hno_generique'] == 'HNO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_hno'] == '1') {
                    $agpSuivreHno = 1;
                }
            }
```

Question métier : Point de décision — 'data'['agp_ho_hno_generique'] égal à 'HNO' et 'priorityHoHno'['oceaneData'['oceane_priority']]['activation_hno'] égal à '1'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #105 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 763
Contexte   :
```php

        $idUrgenceOceane = $this->agpGeneriqueRepository->getIdentifiantUrgenceByValeurParametres($idJeuParam, 'NIVEAU_URGENCE', $oceaneData['herite_oceane_niveau_urgence']);
        if (key_exists('herite_oceane_date_action_en_cours', $oceaneData)) {
            $agpDtEnCoursOceane = $oceaneData['herite_oceane_date_action_en_cours'];
        } else {
            $agpDtEnCoursOceane = '';
```

Question métier : Point de décision — key_exists('herite_oceane_date_action_en_cours', 'oceaneData'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #106 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 775
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

**Gap #107 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 777
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

**Gap #108 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 783
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

**Gap #109 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 840
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

**Gap #110 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 853
Contexte   :
```php
        $agpTransferer = 0;

        if ($oceaneData['herite_oceane_hno'] == 1) {
            $agpSuivreHno = $oceaneData['herite_oceane_hno'] == 1 ? $oceaneData['herite_oceane_hno'] : 0;
        } else {
            $priorityHoHno = $this->agpGeneriqueRepository->getActivationHoHnoByJeu($idJeuParam, $oceaneData['oceane_priority']);
```

Question métier : Point de décision — 'oceaneData'['herite_oceane_hno'] égal à 1. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #111 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 858
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

**Gap #112 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 859
Contexte   :
```php

            if (key_exists($oceaneData['oceane_priority'], $priorityHoHno)) {
                if ($data['agp_ho_hno_generique'] == 'HO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_ho'] == '1') {
                    $agpSuivreHno = 0;
                } elseif ($data['agp_ho_hno_generique'] == 'HNO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_hno'] == '1') {
                    $agpSuivreHno = 1;
```

Question métier : Point de décision — 'data'['agp_ho_hno_generique'] égal à 'HO' et 'priorityHoHno'['oceaneData'['oceane_priority']]['activation_ho'] égal à '1'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #113 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 861
Contexte   :
```php
                if ($data['agp_ho_hno_generique'] == 'HO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_ho'] == '1') {
                    $agpSuivreHno = 0;
                } elseif ($data['agp_ho_hno_generique'] == 'HNO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_hno'] == '1') {
                    $agpSuivreHno = 1;
                }
            }
```

Question métier : Point de décision — 'data'['agp_ho_hno_generique'] égal à 'HNO' et 'priorityHoHno'['oceaneData'['oceane_priority']]['activation_hno'] égal à '1'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #114 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 881
Contexte   :
```php
        $idUrgenceOceane = $this->agpGeneriqueRepository->getIdentifiantUrgenceByValeurParametres($idJeuParam, 'NIVEAU_URGENCE', $oceaneData['herite_oceane_niveau_urgence']);
        $agpDtEnCours = $this->agpGeneriqueRepository->calcDateOuvreeGenerique($oceaneData['oceane_priority'], $data['id_entite'], $data['hno']);
        if (key_exists('herite_oceane_date_action_en_cours', $oceaneData)) {
            $agpDtEnCoursOceane = $oceaneData['herite_oceane_date_action_en_cours'];
        } else {
            $agpDtEnCoursOceane = '';
```

Question métier : Point de décision — key_exists('herite_oceane_date_action_en_cours', 'oceaneData'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #115 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 890
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

**Gap #116 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 892
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

**Gap #117 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 903
Contexte   :
```php

        $isDslamTest = false;
        if ($api) {
            if ($data['type_ressource'] == 'DSLAM' || $data['type_ressource'] == 'DSLAMDERCO') {
                $isDslamTest = true;
            }
```

Question métier : Point de décision — 'api'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #118 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 904
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

**Gap #119 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 910
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

**Gap #120 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 917
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

**Gap #121 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 919
Contexte   :
```php
        if (!empty($blocs) && key_exists(0, $blocs)) {
            foreach ($blocs as $blocName) {
                if ($isDslamTest) {
                    $blocVariable = $this->agpGeneriqueRepository->getBlocVariable($blocName);
                    $blocVariableContent = $refCom['' . $blocVariable . ''];
                    $commentaire = str_replace('##bloc_' . $blocName . '##', $blocVariableContent, $commentaire);
```

Question métier : Point de décision — 'isDslamTest'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #122 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 923
Contexte   :
```php
                    $blocVariableContent = $refCom['' . $blocVariable . ''];
                    $commentaire = str_replace('##bloc_' . $blocName . '##', $blocVariableContent, $commentaire);
                } elseif ($blocName != 'choix_de_carte_trans' && $blocName != 'Types_Carte' && $blocName != 'Types' && $blocName != 'Carte_EAN' && $blocName != 'Complet') {
                    $blocVariable = $this->agpGeneriqueRepository->getBlocVariable($blocName);
                    $commentaire = str_replace('##bloc_' . $blocName . '##', $blocVariable, $commentaire);
                }
```

Question métier : Point de décision — 'blocName' différent de 'choix_de_carte_trans' et 'blocName' différent de 'Types_Carte' et 'blocName' différent de 'Types' et 'blocName' différent de 'Carte_EAN' et 'blocName' différent de 'Complet'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #123 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 929
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

**Gap #124 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 941
Contexte   :
```php


        if ($isDslamTest) {
            $agpIdAstro = key_exists('agp_id_astro', $data) ? $data['agp_id_astro'] : null;
            $agpIdRsc = key_exists('agp_id_rsc', $data) ? $data['agp_id_rsc'] : null;
            $agpIdAction = key_exists('agp_id_action', $data) ? $data['agp_id_action'] : null;
```

Question métier : Point de décision — 'isDslamTest'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #125 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 967
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

**Gap #126 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 974
Contexte   :
```php
        }
        $variables = OceaneTools::getContents($commentaire, '###', '###');
        if ($api) {
            $this->ticketId = $ticketId;
            $this->typeRessource = key_exists('type_ressource', $data) ? $data['type_ressource'] : '';
            $data['id3'] = key_exists('id3', $oceaneData) ? $oceaneData['id3'] : '';
```

Question métier : Point de décision — 'api'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #127 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 983
Contexte   :
```php
        }

        if ($data['agp_ecran'] == 0) {

            $commentaire = preg_replace('/###[\s\S]+?###/ ', '', $commentaire);
        }
```

Question métier : Point de décision — 'data'['agp_ecran'] égal à 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #128 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 990
Contexte   :
```php
        $agpCommentaire['COMMENTAIRE'] = $commentaire;

        if (!$idUrgenceOceane) {
            $idUrgenceOceane = $idUrgence;
        }

```

Question métier : Point de décision — !'idUrgenceOceane'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #129 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1017
Contexte   :
```php
        $carteArray = array("dslam", "master", "deport");

        if (in_array($input, $carteArray) || (($input == 'alarme') && ($hasChassis == 'false'))) {
            return 517;
        } else {
            return 518;
```

Question métier : Point de décision — in_array('input', 'carteArray') ou (('input' égal à 'alarme') et ('hasChassis' égal à 'false')). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #130 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1029
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

**Gap #131 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1033
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

**Gap #132 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1037
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

**Gap #133 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1074
Contexte   :
```php

        $this->airele = $this->app->get('Airele');
        if (!is_null($this->getOceane)) {
            // Récupération des données du ticket Océane (impacts, priorité, dates)
            $data['impact_technique'] = $this->astroLienRepository->getImpactTechniqueById($this->getOceane->getCategory());
            $data['impact_client'] = $this->astroLienRepository->getImpactClientLibById($this->getOceane->getCriticity());
```

Question métier : Point de décision — !is_null('this'->getOceane). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #134 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1087
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

**Gap #135 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1093
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

**Gap #136 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1096
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

**Gap #137 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1158
Contexte   :
```php
        );

        if ($choixCreation == "DSLAM") {
            $champComp3 = "dslam";
        } elseif ($choixCreation == "Chassis") {
            $champComp3 = "dslamSubRack";
```

Question métier : Point de décision — 'choixCreation' égal à "DSLAM". Quel est le comportement attendu dans le cas contraire ?

---

**Gap #138 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1160
Contexte   :
```php
        if ($choixCreation == "DSLAM") {
            $champComp3 = "dslam";
        } elseif ($choixCreation == "Chassis") {
            $champComp3 = "dslamSubRack";
        } elseif ($choixCreation == "Carte") {
            $champComp3 = "dslamSlot";
```

Question métier : Point de décision — 'choixCreation' égal à "Chassis". Quel est le comportement attendu dans le cas contraire ?

---

**Gap #139 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1162
Contexte   :
```php
        } elseif ($choixCreation == "Chassis") {
            $champComp3 = "dslamSubRack";
        } elseif ($choixCreation == "Carte") {
            $champComp3 = "dslamSlot";
        }
        $choixValeur = explode(")", explode("(", "$choixValeur")[1])[0];
```

Question métier : Point de décision — 'choixCreation' égal à "Carte". Quel est le comportement attendu dans le cas contraire ?

---

**Gap #140 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1215
Contexte   :
```php
        $this->app->get('TraceRepository')->setTrace($astroId, "CREATION TOC RESSOURCE REPONSE", $retourCreation, $this->app->get('Session')->getUtilisateurId(), $ticketId);

        if (is_array($retourCreation) && key_exists('id', $retourCreation)) {
            $paramUrlOceane = array(
                'RUNURLGENOK' => '1',
                'APPLI' => 'HBM',
```

Question métier : Point de décision — is_array('retourCreation') et key_exists('id', 'retourCreation'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #141 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1292
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

**Gap #142 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1298
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

**Gap #143 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1301
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

**Gap #144 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1309
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

**Gap #145 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1317
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

**Gap #146 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1333
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

**Gap #147 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1339
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

**Gap #148 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1346
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

**Gap #149 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1354
Contexte   :
```php
                    $replaceValue = (!is_null($this->eds)) ? $this->eds : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #150 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1362
Contexte   :
```php
                    $replaceValue = (!is_null($this->typeRessource)) ? $this->typeRessource : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #151 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1374
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

**Gap #152 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1379
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

**Gap #153 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1387
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

**Gap #154 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1394
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

**Gap #155 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1401
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

**Gap #156 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1416
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

**Gap #157 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1423
Contexte   :
```php
                    $replaceValue = $this->getOceane->getClosedTicketQuantity();

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #158 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1433
Contexte   :
```php
                    $replaceValue = ($description != '') ? $description : null;

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #159 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1440
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

**Gap #160 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1444
Contexte   :
```php
                    }

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #161 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1466
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

**Gap #162 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1471
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

**Gap #163 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1477
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

**Gap #164 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1484
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

**Gap #165 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1488
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

**Gap #166 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1491
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

**Gap #167 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1493
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

**Gap #168 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1524
Contexte   :
```php

        //3349
        if (empty($intervenantInfos) || ($intervenantInfos['TECHNO'] == null || $intervenantInfos['TECHNO'] == '') || (($intervenantInfos['TECHNO'] != null && $intervenantInfos['TECHNO'] != '') && $intervenantInfos['TECHNO'] == $technoComp)) {
            if ($intervenant != 'ORANGE') {
                $this->variableService = $this->app->get('Variable');

```

Question métier : Point de décision — le champ 'intervenantInfos' est vide || ($intervenantInfos['TECHNO'] == null || $intervenantInfos['TECHNO'] == '') || (($intervenantInfos['TECHNO'] != null && $intervenantInfos['TECHNO'] != '') && $intervenantInfos['TECHNO'] == $technoComp). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #169 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1525
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

**Gap #170 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1546
Contexte   :
```php
                }
                $this->refsiteRepository = $this->app->get('RefsitesRepository');
                if (is_array($intervenantArray) && key_exists('INTERVENANT', $intervenantArray)) {
                    $intervenant = $intervenantArray['INTERVENANT'];
                    $this->refsiteRepository->UpdateTicketAstroWithIdRefsite($ticketId, $intervenantArray['ID']);
                } else {
```

Question métier : Point de décision — is_array('intervenantArray') et key_exists('INTERVENANT', 'intervenantArray'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #171 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1557
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

**Gap #172 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1569
Contexte   :
```php
        $dataAiguillageManuel['commentaire'] = $this->aiguillageCommentaireAction($dataAiguillageManuel, $astroData);

        if (!is_null($allEcransValues) && is_array($allEcransValues)) {
            $dataAiguillageManuel['commentaire'] = $this->aiguillageCommentaireRemplaceBloc($dataAiguillageManuel, $allEcransValues);
        }

```

Question métier : Point de décision — !is_null('allEcransValues') et is_array('allEcransValues'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #173 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1587
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

**Gap #174 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1600
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

**Gap #175 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1603
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

**Gap #176 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1607
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

**Gap #177 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1615
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

**Gap #178 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1619
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

**Gap #179 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1627
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

**Gap #180 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1631
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

**Gap #181 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1642
Contexte   :
```php
            foreach ($blocs as $blocName) {

                if ($keyVariable == 'donnee_cartes' && !empty($blocs) && $blocName == 'choix_de_carte_trans') {
                    // Remplacer bloc_choix_de_carte_trans par les donnes des cartes selection?es
                    $blocDonneeCarte = '';
                    foreach ($valueVariable as $dataCarte) {
```

Question métier : Point de décision — $keyVariable == 'donnee_cartes' && !le champ 'blocs' est vide && $blocName == 'choix_de_carte_trans'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #182 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1649
Contexte   :
```php

                        foreach ($dataCarte as $keyTag => $dataTag) {
                            if ($keyTag == 'ean') {
                                if ($dataTag == 'True') {
                                    $blocVariable = str_replace('###crochet_ouvrant###', '[', $blocVariable);
                                    $blocVariable = str_replace('###crochet_fermant###', ']', $blocVariable);
```

Question métier : Point de décision — 'keyTag' égal à 'ean'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #183 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1650
Contexte   :
```php
                        foreach ($dataCarte as $keyTag => $dataTag) {
                            if ($keyTag == 'ean') {
                                if ($dataTag == 'True') {
                                    $blocVariable = str_replace('###crochet_ouvrant###', '[', $blocVariable);
                                    $blocVariable = str_replace('###crochet_fermant###', ']', $blocVariable);
                                } else {
```

Question métier : Point de décision — 'dataTag' égal à 'True'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #184 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1665
Contexte   :
```php
                    }
                    $commentaire = str_replace('##bloc_choix_de_carte_trans##', $blocDonneeCarte, $commentaire);
                } elseif ($keyVariable != 'donnee_cartes' && !empty($blocs) && ($blocName == 'defaut_constate_trans' || $blocName == 'action_a_realiser_trans' || $blocName == 'Types_Carte' || $blocName == 'Types' || $blocName == 'Carte_EAN' || $blocName == 'Complet')) {
                    // Remplacer bloc par les donnes des cartes selection?es
                    $blocDonneeCarte = '';

```

Question métier : Point de décision — $keyVariable != 'donnee_cartes' && !le champ 'blocs' est vide && ($blocName == 'defaut_constate_trans' || $blocName == 'action_a_realiser_trans' || $blocName == 'Types_Carte' || $blocName == 'Types' || $blocName == 'Carte_EAN' || $blocName == 'Complet'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #185 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : ligne 1675
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

**Gap #186 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaire() — ligne 1692
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

**Gap #187 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaire() — ligne 1695
Contexte   :
```php
            $isDslamTest = true;
        }
        if ($isDslamTest) {
            $data['idJeu'] = $data['idJeuParam'];

            $agpResult = $this->getCommentaireAgp2Generique($data);
```

Question métier : Point de décision — 'isDslamTest'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #188 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaire() — ligne 1704
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

**Gap #189 — AgpService**

**→ Copier dans Copilot**

Fichier    : AgpService.php
Méthode    : aiguillageCommentaire() — ligne 1706
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

**Gap #190 — AiguillageIntervenantService**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : ligne 48
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

**Gap #191 — AiguillageIntervenantService**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : ligne 52
Contexte   :
```php
        }
        foreach ($intervenantInfosList as $intervenantInfos) {
            if ($intervenantInfos['VARIABLE_ADMIN'] != '* Variables *' && !is_null($intervenantInfos['CONDITION']) && !is_null($intervenantInfos['VALEUR_CONDITION'])) {
                $ok = false;
                $variable = $intervenantInfos['VARIABLE_ADMIN'];
                $argsVariableGlobal = array();
```

Question métier : Point de décision — 'intervenantInfos'['VARIABLE_ADMIN'] différent de '* Variables *' et !is_null('intervenantInfos'['CONDITION']) et !is_null('intervenantInfos'['VALEUR_CONDITION']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #192 — AiguillageIntervenantService**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : ligne 62
Contexte   :
```php
                    switch ($intervenantInfos['CONDITION']) {
                        case 'begin_with':
                            if (strpos($checkVar, $val) === 0) $ok = true;
                            break;
                        case 'equal':
                            if (strcmp($checkVar, $val) === 0) $ok = true;///valeurs admin case Sensitive
```

Question métier : Point de décision — strpos('checkVar', 'val') égal à = 0) 'ok' = true; break; case 'equal': if (strcmp('checkVar', 'val') égal à = 0) 'ok' = true;///valeurs admin case Sensitive break; case 'contains': if (strpos('checkVar', 'val') différent de = false) 'ok' = true; break; case '': 'ok' = true; break; } if ('ok') break; } } elseif ('intervenantInfos'['VARIABLE_ADMIN'] différent de '* Variables *' et (is_null('intervenantInfos'['CONDITION']) ou is_null('intervenantInfos'['VALEUR_CONDITION'])). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #193 — AiguillageIntervenantService**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : ligne 80
Contexte   :
```php
            } elseif ($intervenantInfos['VARIABLE_ADMIN'] != '* Variables *' && (is_null($intervenantInfos['CONDITION']) || is_null($intervenantInfos['VALEUR_CONDITION']))) {
                $ok = false;
            } elseif ($intervenantInfos['VARIABLE_ADMIN'] == '* Variables *' && (!is_null($intervenantInfos['CONDITION']) || !is_null($intervenantInfos['VALEUR_CONDITION']))) {
                $ok = false;
            } elseif($intervenantInfos['VARIABLE_ADMIN'] == '* Variables *' && (is_null($intervenantInfos['CONDITION']) || is_null($intervenantInfos['VALEUR_CONDITION']))) {
                $ok = true;
```

Question métier : Point de décision — 'intervenantInfos'['VARIABLE_ADMIN'] égal à '* Variables *' et (!is_null('intervenantInfos'['CONDITION']) ou !is_null('intervenantInfos'['VALEUR_CONDITION'])). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #194 — AiguillageIntervenantService**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : ligne 82
Contexte   :
```php
            } elseif ($intervenantInfos['VARIABLE_ADMIN'] == '* Variables *' && (!is_null($intervenantInfos['CONDITION']) || !is_null($intervenantInfos['VALEUR_CONDITION']))) {
                $ok = false;
            } elseif($intervenantInfos['VARIABLE_ADMIN'] == '* Variables *' && (is_null($intervenantInfos['CONDITION']) || is_null($intervenantInfos['VALEUR_CONDITION']))) {
                $ok = true;
            }
            if (!is_null($intervenantInfos['TECHNO']) && $intervenantInfos['TECHNO'] != '' && $ok) {
```

Question métier : Point de décision — 'intervenantInfos'['VARIABLE_ADMIN'] égal à '* Variables *' et (is_null('intervenantInfos'['CONDITION']) ou is_null('intervenantInfos'['VALEUR_CONDITION'])). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #195 — AiguillageIntervenantService**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : ligne 85
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

**Gap #196 — AiguillageIntervenantService**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : ligne 109
Contexte   :
```php
                    case 'SDH':
                    case 'MIE':
                        if ($typeRessource == 'MIE') {
                            $extremiteTechno = 'TECHNO';
                        } else {
                            if ($ext == 'tabs_action_ext1') {
```

Question métier : Point de décision — 'typeRessource' égal à 'MIE'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #197 — AiguillageIntervenantService**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : ligne 112
Contexte   :
```php
                            $extremiteTechno = 'TECHNO';
                        } else {
                            if ($ext == 'tabs_action_ext1') {
                                $extremiteTechno = 'EXT1_TECHNO';
                            } elseif ($ext == 'tabs_action_ext2') {
                                $extremiteTechno = 'EXT2_TECHNO';
```

Question métier : Point de décision — 'ext' égal à 'tabs_action_ext1'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #198 — AiguillageIntervenantService**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : ligne 114
Contexte   :
```php
                            if ($ext == 'tabs_action_ext1') {
                                $extremiteTechno = 'EXT1_TECHNO';
                            } elseif ($ext == 'tabs_action_ext2') {
                                $extremiteTechno = 'EXT2_TECHNO';
                            }
                        }
```

Question métier : Point de décision — 'ext' égal à 'tabs_action_ext2'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #199 — AiguillageIntervenantService**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : ligne 122
Contexte   :
```php
                        $techno = $this->app->get('Variable')->replaceTagsChaine("###$extremiteTechno###", $argsVariableGlobal1, $typeRessource, $ticketId);

                        if ($techno == 'FH') {
                            // FH
                            $ok = ($intervenantInfos['TECHNO'] == 'FH');
                        } else {
```

Question métier : Point de décision — 'techno' égal à 'FH'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #200 — AiguillageIntervenantService**

**→ Copier dans Copilot**

Fichier    : AiguillageIntervenantService.php
Méthode    : ligne 134
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

**Gap #201 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 78
Contexte   :
```php
            //Get FindAndGet Data
            //Check if fg is well received
            if (key_exists('code', $resultatO) && $resultatO['code'] != 60) {
                $message = $resultatO['message'] . ' ' . $resultatO['code'];
            } elseif (key_exists('code', $resultatO) && $resultatO['code'] == 60) {
                $message = 'Ticket ' . $ticketId . ' est inexistant dans océane !';
```

Question métier : Point de décision — key_exists('code', 'resultatO') et 'resultatO'['code'] différent de 60. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #202 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 80
Contexte   :
```php
            if (key_exists('code', $resultatO) && $resultatO['code'] != 60) {
                $message = $resultatO['message'] . ' ' . $resultatO['code'];
            } elseif (key_exists('code', $resultatO) && $resultatO['code'] == 60) {
                $message = 'Ticket ' . $ticketId . ' est inexistant dans océane !';
            } elseif (key_exists('id', $resultatO)) {
                //Hno
```

Question métier : Point de décision — key_exists('code', 'resultatO') et 'resultatO'['code'] égal à 60. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #203 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 82
Contexte   :
```php
            } elseif (key_exists('code', $resultatO) && $resultatO['code'] == 60) {
                $message = 'Ticket ' . $ticketId . ' est inexistant dans océane !';
            } elseif (key_exists('id', $resultatO)) {
                //Hno
                $hno = $this->getOceane->getHno();
                //TIKETOCEANEID
```

Question métier : Point de décision — key_exists('id', 'resultatO'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #204 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 125
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

**Gap #205 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 209
Contexte   :
```php
        $listIncident = array(15, 1, 4);
        //incident
        if (in_array($category, $listIncident)) {
            $this->assistantRepository->evtToIncident($astroId, 'incident');
            $value = 'incident';
        } // evenement
```

Question métier : Point de décision — in_array('category', 'listIncident'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #206 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 214
Contexte   :
```php
        } // evenement
        else {
            if ($category == '64') {
                $this->assistantRepository->evtToIncident($astroId, 'événement');
                $value = 'événement';
            } else {
```

Question métier : Point de décision — 'category' égal à '64'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #207 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 227
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

**Gap #208 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 233
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

**Gap #209 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 240
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

**Gap #210 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 242
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

**Gap #211 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 263
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

**Gap #212 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 273
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

**Gap #213 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 284
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

**Gap #214 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 304
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

**Gap #215 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 315
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

**Gap #216 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 326
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

**Gap #217 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 351
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

**Gap #218 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 370
Contexte   :
```php
    {
        $dataFg = $this->initApi($idTicket, $connectedGroup);
        if ($code == 'TRAITEMENT_ALARME_CARTES_CLIENTS' || $code == 'TRAITEMENT_ALARME_EVT' || $code == 'TRAITEMENT_RENDRE_MAIN_EVT') {
            return ($dataFg['eds_pilote'] == $connectedGroup && $dataFg['evt_incident'] == '64' && ($dataFg['status'] == 'Open' || $dataFg['status'] == 'InProgress' || $dataFg['status'] == 'OnHold'));
        } else {
            return true;
```

Question métier : Point de décision — 'code' égal à 'TRAITEMENT_ALARME_CARTES_CLIENTS' ou 'code' égal à 'TRAITEMENT_ALARME_EVT' ou 'code' égal à 'TRAITEMENT_RENDRE_MAIN_EVT'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #219 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 401
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

**Gap #220 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 408
Contexte   :
```php
    }

    public function getEDSActif($ticketID)
    {
        $conf = $this->app->config;
        $env = $conf['ENV'];
```

Question métier : Point de décision — 'ticketID'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #221 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 419
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

**Gap #222 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 424
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

**Gap #223 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 425
Contexte   :
```php
            foreach ($partyRole as $key => $value) {
                if ($partyRole[$key]->partyRoleType == "TroubleResolutionContributor" && property_exists($partyRole[$key], 'Local_PartyIntervention')) {
                    if (is_object($partyRole[$key]->Local_PartyIntervention->interventionStatus) && $partyRole[$key]->Local_PartyIntervention->interventionStatus->status == "Accepted") {
                        return $partyRole[$key]->PartyRoleSet->partyRoleSetID;
                    } else if (is_object($partyRole[$key]->Local_PartyIntervention->interventionStatus) && $partyRole[$key]->Local_PartyIntervention->interventionStatus->status == "Requested" && $partyRole[$key]->Local_PartyIntervention->level == '1') {
                        return $partyRole[$key]->PartyRoleSet->partyRoleSetID;
```

Question métier : Point de décision — is_object('partyRole'['key']->Local_PartyIntervention->interventionStatus) et 'partyRole'['key']->Local_PartyIntervention->interventionStatus->status égal à "Accepted". Quel est le comportement attendu dans le cas contraire ?

---

**Gap #224 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 427
Contexte   :
```php
                    if (is_object($partyRole[$key]->Local_PartyIntervention->interventionStatus) && $partyRole[$key]->Local_PartyIntervention->interventionStatus->status == "Accepted") {
                        return $partyRole[$key]->PartyRoleSet->partyRoleSetID;
                    } else if (is_object($partyRole[$key]->Local_PartyIntervention->interventionStatus) && $partyRole[$key]->Local_PartyIntervention->interventionStatus->status == "Requested" && $partyRole[$key]->Local_PartyIntervention->level == '1') {
                        return $partyRole[$key]->PartyRoleSet->partyRoleSetID;
                    } else if (is_array($partyRole[$key]->Local_PartyIntervention->interventionStatus)) {
                        foreach ($partyRole[$key]->Local_PartyIntervention->interventionStatus as $k => $v) {
```

Question métier : Point de décision — is_object('partyRole'['key']->Local_PartyIntervention->interventionStatus) et 'partyRole'['key']->Local_PartyIntervention->interventionStatus->status égal à "Requested" et 'partyRole'['key']->Local_PartyIntervention->level égal à '1'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #225 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 429
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

**Gap #226 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 431
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

**Gap #227 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 453
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

**Gap #228 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 458
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

**Gap #229 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 459
Contexte   :
```php
            foreach ($partyRole as $key => $value) {
                if ($partyRole[$key]->partyRoleType == "TroubleResolutionLeader" && property_exists($partyRole[$key], 'Local_PartyIntervention')) {
                    if (is_object($partyRole[$key]->Local_PartyIntervention->interventionStatus) && $partyRole[$key]->Local_PartyIntervention->interventionStatus->status == "Accepted") {
                        return $partyRole[$key]->PartyRoleSet->partyRoleSetID;
                    } else if (is_array($partyRole[$key]->Local_PartyIntervention->interventionStatus)) {
                        foreach ($partyRole[$key]->Local_PartyIntervention->interventionStatus as $k => $v) {
```

Question métier : Point de décision — is_object('partyRole'['key']->Local_PartyIntervention->interventionStatus) et 'partyRole'['key']->Local_PartyIntervention->interventionStatus->status égal à "Accepted". Quel est le comportement attendu dans le cas contraire ?

---

**Gap #230 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 461
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

**Gap #231 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 463
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

**Gap #232 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 506
Contexte   :
```php
    {
        $scenarioExist = $this->enchainementRepo->verifierScenarioExist($idScenario);
        if($scenarioExist == '0')
        {
            $badRequestException = new BadRequestException('scenarioId does not exist');
            return $badRequestException();
```

Question métier : Point de décision — 'scenarioExist' égal à '0'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #233 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 517
Contexte   :
```php
    {
        $etatScenario = $this->enchainementRepo->verifierActivationScenario($idScenario);
        if($etatScenario == '0')
        {
            $scenarioDesactiveException = new ScenarioDesactiveException();
            return $scenarioDesactiveException();
```

Question métier : Point de décision — 'etatScenario' égal à '0'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #234 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 528
Contexte   :
```php
    {
        $typeScenario = $this->enchainementRepo->verifierTypeScenario($idScenario);
        if($typeScenario == '0' && $scenarioType == 'parametrable')
        {
            $scenarioTypeException = new BadRequestException("Ce scenarioId n'est pas un scenario parametrable");
            return $scenarioTypeException();
```

Question métier : Point de décision — 'typeScenario' égal à '0' et 'scenarioType' égal à 'parametrable'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #235 — ApiService**

**→ Copier dans Copilot**

Fichier    : ApiService.php
Méthode    : ligne 532
Contexte   :
```php
            $scenarioTypeException = new BadRequestException("Ce scenarioId n'est pas un scenario parametrable");
            return $scenarioTypeException();
        }elseif($typeScenario == '1' && $scenarioType == 'legacy')
        {
            $scenarioTypeException = new BadRequestException("Ce scenarioId n'est pas un scenario legacy");
            return $scenarioTypeException();
```

Question métier : Point de décision — 'typeScenario' égal à '1' et 'scenarioType' égal à 'legacy'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #236 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 54
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

**Gap #237 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 68
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

**Gap #238 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 70
Contexte   :
```php
        if (key_exists('relatedResource', $this->oceaneData) && is_array($this->oceaneData['relatedResource']) && key_exists('resourceSpecCharacteristic', $this->oceaneData['relatedResource']) && is_array($this->oceaneData['relatedResource']['resourceSpecCharacteristic'])) {
            foreach ($this->oceaneData['relatedResource']['resourceSpecCharacteristic'] as $value) {
                if (is_array($value) && key_exists('index', $value) && !is_null($id) && (intval($value['index']) == $id) && key_exists('value', $value)) {
                    return $value['value'];
                } elseif (is_array($value) && key_exists('index', $value) && key_exists('value', $value)) {
                    $ids[$value['index']] = $value['value'];
```

Question métier : Point de décision — is_array('value') et key_exists('index', 'value') et !is_null('id') et (intval('value'['index']) égal à 'id') et key_exists('value', 'value'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #239 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 72
Contexte   :
```php
                if (is_array($value) && key_exists('index', $value) && !is_null($id) && (intval($value['index']) == $id) && key_exists('value', $value)) {
                    return $value['value'];
                } elseif (is_array($value) && key_exists('index', $value) && key_exists('value', $value)) {
                    $ids[$value['index']] = $value['value'];
                }
            }
```

Question métier : Point de décision — is_array('value') et key_exists('index', 'value') et key_exists('value', 'value'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #240 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 88
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

**Gap #241 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 90
Contexte   :
```php
        if (key_exists('relatedService', $this->oceaneData) && is_array($this->oceaneData['relatedService']) && key_exists('serviceSpecCharacteristic', $this->oceaneData['relatedService']) && is_array($this->oceaneData['relatedService']['serviceSpecCharacteristic'])) {
            foreach ($this->oceaneData['relatedService']['serviceSpecCharacteristic'] as $value) {
                if (is_array($value) && key_exists('index', $value) && !is_null($id) && (intval($value['index']) == $id) && key_exists('value', $value)) {
                    return $value['value'];
                } elseif (is_array($value) && key_exists('index', $value) && key_exists('value', $value)) {
                    $ids[$value['index']] = $value['value'];
```

Question métier : Point de décision — is_array('value') et key_exists('index', 'value') et !is_null('id') et (intval('value'['index']) égal à 'id') et key_exists('value', 'value'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #242 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 92
Contexte   :
```php
                if (is_array($value) && key_exists('index', $value) && !is_null($id) && (intval($value['index']) == $id) && key_exists('value', $value)) {
                    return $value['value'];
                } elseif (is_array($value) && key_exists('index', $value) && key_exists('value', $value)) {
                    $ids[$value['index']] = $value['value'];
                }
            }
```

Question métier : Point de décision — is_array('value') et key_exists('index', 'value') et key_exists('value', 'value'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #243 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 107
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

**Gap #244 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 109
Contexte   :
```php
        if (key_exists('relatedResource', $this->oceaneData) && is_array($this->oceaneData['relatedResource']) && key_exists('resourceSpecification', $this->oceaneData['relatedResource'])) {
            $id = key_exists('id', $this->oceaneData['relatedResource']['resourceSpecification']) ? $this->oceaneData['relatedResource']['resourceSpecification']['id'] : null;
            if ($idAndName) {
                $name = key_exists('name', $this->oceaneData['relatedResource']['resourceSpecification']) ? $this->oceaneData['relatedResource']['resourceSpecification']['name'] : null;
                return [
                    'id' => $id,
```

Question métier : Point de décision — 'idAndName'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #245 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 129
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

**Gap #246 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 131
Contexte   :
```php
        if (key_exists('relatedService', $this->oceaneData) && is_array($this->oceaneData['relatedService']) && key_exists('serviceSpecification', $this->oceaneData['relatedService'])) {
            $id = key_exists('id', $this->oceaneData['relatedService']['serviceSpecification']) ? $this->oceaneData['relatedService']['serviceSpecification']['id'] : null;
            if ($idAndName) {
                $name = key_exists('name', $this->oceaneData['relatedService']['serviceSpecification']) ? $this->oceaneData['relatedService']['serviceSpecification']['name'] : null;
                return [
                    'id' => $id,
```

Question métier : Point de décision — 'idAndName'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #247 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 152
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

**Gap #248 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 154
Contexte   :
```php
        if (key_exists('troubleTicketCharacteristic', $this->oceaneData) && is_array($this->oceaneData['troubleTicketCharacteristic']) && count($this->oceaneData['troubleTicketCharacteristic']) > 0) {
            foreach ($this->oceaneData['troubleTicketCharacteristic'] as $value) {
                if (is_array($value) && key_exists('index', $value) && !is_null($champ) && (intval($value['index']) == $champ) && key_exists('value', $value)) {
                    return $value['value'];
                } elseif (is_array($value) && key_exists('index', $value) && key_exists('value', $value)) {
                    $characteristic[$value['index']] = $value['value'];
```

Question métier : Point de décision — is_array('value') et key_exists('index', 'value') et !is_null('champ') et (intval('value'['index']) égal à 'champ') et key_exists('value', 'value'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #249 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 156
Contexte   :
```php
                if (is_array($value) && key_exists('index', $value) && !is_null($champ) && (intval($value['index']) == $champ) && key_exists('value', $value)) {
                    return $value['value'];
                } elseif (is_array($value) && key_exists('index', $value) && key_exists('value', $value)) {
                    $characteristic[$value['index']] = $value['value'];
                }
            }
```

Question métier : Point de décision — is_array('value') et key_exists('index', 'value') et key_exists('value', 'value'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #250 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 171
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

**Gap #251 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 173
Contexte   :
```php
        if (key_exists('priority', $this->oceaneData) && is_array($this->oceaneData['priority'])) {
            $id = key_exists('id', $this->oceaneData['priority']) ? $this->oceaneData['priority']['id'] : null;
            if ($idAndLabel) {
                $label = key_exists('label', $this->oceaneData['priority']) ? $this->oceaneData['priority']['label'] : null;
                return [
                    'id' => $id,
```

Question métier : Point de décision — 'idAndLabel'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #252 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 193
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

**Gap #253 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 195
Contexte   :
```php
        if (key_exists('urgency', $this->oceaneData) && is_array($this->oceaneData['urgency'])) {
            $id = key_exists('id', $this->oceaneData['urgency']) ? $this->oceaneData['urgency']['id'] : null;
            if ($idAndLabel) {
                $label = key_exists('label', $this->oceaneData['urgency']) ? $this->oceaneData['urgency']['label'] : null;
                return [
                    'id' => $id,
```

Question métier : Point de décision — 'idAndLabel'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #254 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 215
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

**Gap #255 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 216
Contexte   :
```php
    {
        if (key_exists('creationDate', $this->oceaneData)) {
            if (!is_null($format)) {
                return $this->app->get('AstroBase')->formatDate($this->oceaneData['creationDate'], 'Y-m-d\TH:i:s\Z', $format);
            } else {
                return $this->oceaneData['creationDate'];
```

Question métier : Point de décision — !is_null('format'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #256 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 231
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

**Gap #257 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 232
Contexte   :
```php
    {
        if (key_exists('detectionDate', $this->oceaneData)) {
            if (!is_null($format)) {
                return $this->app->get('AstroBase')->formatDate($this->oceaneData['detectionDate'], 'Y-m-d\TH:i:s\Z', $format);
            } else {
                return $this->oceaneData['detectionDate'];
```

Question métier : Point de décision — !is_null('format'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #258 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 243
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

**Gap #259 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 245
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

**Gap #260 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 259
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

**Gap #261 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 261
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

**Gap #262 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 270
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

**Gap #263 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 272
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

**Gap #264 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 282
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

**Gap #265 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 284
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

**Gap #266 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 286
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

**Gap #267 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 287
Contexte   :
```php
                    foreach ($value['relatedParty'] as $valueRelatedParty) {
                        if (is_array($valueRelatedParty) && key_exists('actionInProgress', $valueRelatedParty) && $valueRelatedParty['role'] == 'TroubleResolutionLeader') {
                            if (is_array($valueRelatedParty['actionInProgress']) && key_exists('description', $valueRelatedParty['actionInProgress']))
                                return $valueRelatedParty['actionInProgress']['description'];
                        }
                    }
```

Question métier : Point de décision — is_array('valueRelatedParty'['actionInProgress']) et key_exists('description', 'valueRelatedParty'['actionInProgress'])) return 'valueRelatedParty'['actionInProgress']['description']; } } } } } return null; } public function getActifGroup(. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #268 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 298
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

**Gap #269 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 300
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

**Gap #270 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 310
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

**Gap #271 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 312
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

**Gap #272 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 314
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

**Gap #273 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 326
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

**Gap #274 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 328
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

**Gap #275 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 338
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

**Gap #276 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 340
Contexte   :
```php
        if (key_exists('ticketType', $this->oceaneData) && is_array($this->oceaneData['ticketType'])) {
            $id = key_exists('id', $this->oceaneData['ticketType']) ? $this->oceaneData['ticketType']['id'] : null;
            if ($idAndLabel) {
                $label = key_exists('label', $this->oceaneData['ticketType']) ? $this->oceaneData['ticketType']['label'] : null;
                return [
                    'id' => $id,
```

Question métier : Point de décision — 'idAndLabel'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #277 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 355
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

**Gap #278 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 357
Contexte   :
```php
        if (key_exists('origin', $this->oceaneData) && is_array($this->oceaneData['origin'])) {
            $id = key_exists('id', $this->oceaneData['origin']) ? $this->oceaneData['origin']['id'] : null;
            if ($idAndLabel) {
                $label = key_exists('label', $this->oceaneData['origin']) ? $this->oceaneData['origin']['label'] : null;
                return [
                    'id' => $id,
```

Question métier : Point de décision — 'idAndLabel'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #279 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 373
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

**Gap #280 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 382
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

**Gap #281 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 384
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

**Gap #282 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 407
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

**Gap #283 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 409
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

**Gap #284 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 419
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

**Gap #285 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 427
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

**Gap #286 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 428
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

**Gap #287 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 430
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

**Gap #288 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 441
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

**Gap #289 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 443
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

**Gap #290 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 457
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

**Gap #291 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 479
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

**Gap #292 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 481
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

**Gap #293 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 497
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

**Gap #294 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 499
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

**Gap #295 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 501
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

**Gap #296 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 506
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

**Gap #297 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 513
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

**Gap #298 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 522
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

**Gap #299 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 524
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

**Gap #300 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 525
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

**Gap #301 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 526
Contexte   :
```php
                if (key_exists('code', $value) && $value['code'] == "Restored") {
                    if (key_exists('startDate', $value)) {
                        if (!is_null($format)) {
                            return $this->app->get('AstroBase')->formatDate($value['startDate'], 'Y-m-d\TH:i:s\Z', $format);
                        } else {
                            return $value['startDate'];
```

Question métier : Point de décision — !is_null('format'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #302 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 539
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

**Gap #303 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 541
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

**Gap #304 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 542
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

**Gap #305 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 543
Contexte   :
```php
                if (key_exists('code', $value) && $value['code'] == "Resolved") {
                    if (key_exists('startDate', $value)) {
                        if (!is_null($format)) {
                            return $this->app->get('AstroBase')->formatDate($value['startDate'], 'Y-m-d\TH:i:s\Z', $format);
                        } else {
                            return $value['startDate'];
```

Question métier : Point de décision — !is_null('format'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #306 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 561
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

**Gap #307 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 563
Contexte   :
```php
        if (key_exists('category', $this->oceaneData) && is_array($this->oceaneData['category'])) {
            $id = key_exists('id', $this->oceaneData['category']) ? $this->oceaneData['category']['id'] : null;
            if ($idAndLabel) {
                $label = key_exists('label', $this->oceaneData['category']) ? $this->oceaneData['category']['label'] : null;
                return [
                    'id' => $id,
```

Question métier : Point de décision — 'idAndLabel'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #308 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 577
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

**Gap #309 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 588
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

**Gap #310 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 590
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

**Gap #311 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 592
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

**Gap #312 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 597
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

**Gap #313 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 604
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

**Gap #314 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 618
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

**Gap #315 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 620
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

**Gap #316 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 622
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

**Gap #317 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 627
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

**Gap #318 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 631
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

**Gap #319 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 647
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

**Gap #320 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 649
Contexte   :
```php
        if (key_exists('criticity', $this->oceaneData) && is_array($this->oceaneData['criticity'])) {
            $id = key_exists('id', $this->oceaneData['criticity']) ? $this->oceaneData['criticity']['id'] : null;
            if ($idAndLabel) {
                $label = key_exists('label', $this->oceaneData['criticity']) ? $this->oceaneData['criticity']['label'] : null;
                return [
                    'id' => $id,
```

Question métier : Point de décision — 'idAndLabel'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #321 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 668
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

**Gap #322 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 669
Contexte   :
```php
    {
        if (key_exists('targetRestorationDate', $this->oceaneData)) {
            if (!is_null($format)) {
                return $this->app->get('AstroBase')->formatDate($this->oceaneData['targetRestorationDate'], 'Y-m-d\TH:i:s\Z', $format);
            } else {
                return rtrim($this->oceaneData['targetRestorationDate'],"Z");
```

Question métier : Point de décision — !is_null('format'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #323 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 684
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

**Gap #324 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 685
Contexte   :
```php
    {
        if (key_exists('plannedRestorationDate', $this->oceaneData)) {
            if (!is_null($format)) {
                return $this->app->get('AstroBase')->formatDate($this->oceaneData['plannedRestorationDate'], 'Y-m-d\TH:i:s\Z', $format);
            } else {
                return rtrim($this->oceaneData['plannedRestorationDate'],"Z");
```

Question métier : Point de décision — !is_null('format'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #325 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 695
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

**Gap #326 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 696
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

**Gap #327 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 698
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

**Gap #328 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 700
Contexte   :
```php
                    if (is_array($value) && key_exists('actionInProgress', $value) &&  key_exists('startDate', $value['actionInProgress'])) {

                        if (!is_null($format)) {
                            return $this->app->get('AstroBase')->formatDate($value['actionInProgress']['startDate'], 'Y-m-d\TH:i:s\Z', $format);
                        } else {
                            return rtrim($value['actionInProgress']['startDate'],"Z");
```

Question métier : Point de décision — !is_null('format'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #329 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 713
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

**Gap #330 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 714
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

**Gap #331 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 716
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

**Gap #332 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 728
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

**Gap #333 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 729
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

**Gap #334 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 731
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

**Gap #335 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 743
Contexte   :
```php
        $driDate = $this->getTargetRestorationDate();
        $drcDate = $this->getPlannedRestorationDate();
        if ($driDate != '' && $drcDate != '') {
            $type = "DRI / DRC";
            $drDate = OceaneTools::changeUTCToDate('d/m/Y H:i', $drcDate);
        } elseif ($drcDate != '') {
```

Question métier : Point de décision — 'driDate' différent de '' et 'drcDate' différent de ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #336 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 746
Contexte   :
```php
            $type = "DRI / DRC";
            $drDate = OceaneTools::changeUTCToDate('d/m/Y H:i', $drcDate);
        } elseif ($drcDate != '') {
            $type = "DRC";
            $drDate = OceaneTools::changeUTCToDate('d/m/Y H:i', $drcDate);
        } elseif ($driDate != '') {
```

Question métier : Point de décision — 'drcDate' différent de ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #337 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 749
Contexte   :
```php
            $type = "DRC";
            $drDate = OceaneTools::changeUTCToDate('d/m/Y H:i', $drcDate);
        } elseif ($driDate != '') {
            $type = "DRI";
            $drDate = OceaneTools::changeUTCToDate('d/m/Y H:i', $driDate);
        }
```

Question métier : Point de décision — 'driDate' différent de ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #338 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 756
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

**Gap #339 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 757
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

**Gap #340 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 759
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

**Gap #341 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 760
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

**Gap #342 — OceaneGetService**

**→ Copier dans Copilot**

Fichier    : OceaneGetService.php
Méthode    : ligne 771
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

**Gap #343 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 97
Contexte   :
```php
            $result = $findAndGetResult->getResponseFindandGetTroubleTicket($ticketId);

            if (property_exists($result, 'faultstring') && $result->faultstring != '') {
                $message = $result->faultstring . ' ' . $result->faultcode;
            } elseif (property_exists($result, 'returnedRecordsNumber') && $result->returnedRecordsNumber == 0) {
                $message = 'Ticket ' . $ticketId . ' est inexistant dans océane !';
```

Question métier : Point de décision — property_exists('result', 'faultstring') et 'result'->faultstring différent de ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #344 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 99
Contexte   :
```php
            if (property_exists($result, 'faultstring') && $result->faultstring != '') {
                $message = $result->faultstring . ' ' . $result->faultcode;
            } elseif (property_exists($result, 'returnedRecordsNumber') && $result->returnedRecordsNumber == 0) {
                $message = 'Ticket ' . $ticketId . ' est inexistant dans océane !';
            } elseif (property_exists($result->TroubleTicketResponse, 'TroubleTicketResponse')) {
                $troubleTicketResponse = $result->TroubleTicketResponse->TroubleTicketResponse;
```

Question métier : Point de décision — property_exists('result', 'returnedRecordsNumber') et 'result'->returnedRecordsNumber égal à 0. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #345 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 101
Contexte   :
```php
            } elseif (property_exists($result, 'returnedRecordsNumber') && $result->returnedRecordsNumber == 0) {
                $message = 'Ticket ' . $ticketId . ' est inexistant dans océane !';
            } elseif (property_exists($result->TroubleTicketResponse, 'TroubleTicketResponse')) {
                $troubleTicketResponse = $result->TroubleTicketResponse->TroubleTicketResponse;

                if (property_exists($troubleTicketResponse->InstalledResource, 'Parameters') && property_exists($troubleTicketResponse->InstalledResource->Parameters, 'Parameter')) {
```

Question métier : Point de décision — property_exists('result'->TroubleTicketResponse, 'TroubleTicketResponse'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #346 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 104
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

**Gap #347 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 106
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

**Gap #348 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 125
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

**Gap #349 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 128
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

**Gap #350 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 130
Contexte   :
```php
                if (property_exists($troubleTicketResponse, 'local_ComplementaryField')) {

                    if (is_array($troubleTicketResponse->local_ComplementaryField)) {
                        if (array_key_exists('3', $troubleTicketResponse->local_ComplementaryField) && isset($troubleTicketResponse->local_ComplementaryField[3]->value)) {

                            $champComplementaire4 = $troubleTicketResponse->local_ComplementaryField[3]->value;
```

Question métier : Point de décision — is_array('troubleTicketResponse'->local_ComplementaryField). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #351 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 131
Contexte   :
```php

                    if (is_array($troubleTicketResponse->local_ComplementaryField)) {
                        if (array_key_exists('3', $troubleTicketResponse->local_ComplementaryField) && isset($troubleTicketResponse->local_ComplementaryField[3]->value)) {

                            $champComplementaire4 = $troubleTicketResponse->local_ComplementaryField[3]->value;

```

Question métier : Point de décision — array_key_exists('3', 'troubleTicketResponse'->local_ComplementaryField) et isset('troubleTicketResponse'->local_ComplementaryField[3]->value). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #352 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 135
Contexte   :
```php
                            $champComplementaire4 = $troubleTicketResponse->local_ComplementaryField[3]->value;

                            if ($troubleTicketResponse->local_ComplementaryField[3]->value == "" && is_array($troubleTicketResponse->InstalledResource->ResourceSpecCharacteristic)) {
                                $ressource = $troubleTicketResponse->InstalledResource->ResourceSpecCharacteristic[0]->InstalledResourceCharValue->resourceCharacteristicValue;
                            } else {
                                $ressource = $troubleTicketResponse->local_ComplementaryField[3]->value;
```

Question métier : Point de décision — 'troubleTicketResponse'->local_ComplementaryField[3]->value égal à "" et is_array('troubleTicketResponse'->InstalledResource->ResourceSpecCharacteristic). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #353 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 142
Contexte   :
```php
                        }

                        if (array_key_exists('2', $troubleTicketResponse->local_ComplementaryField) && isset($troubleTicketResponse->local_ComplementaryField[2]->value)) {
                            $typeRessource = $troubleTicketResponse->local_ComplementaryField[2]->value;
                        }

```

Question métier : Point de décision — array_key_exists('2', 'troubleTicketResponse'->local_ComplementaryField) et isset('troubleTicketResponse'->local_ComplementaryField[2]->value). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #354 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 146
Contexte   :
```php
                        }

                        if (array_key_exists('5', $troubleTicketResponse->local_ComplementaryField) && isset($troubleTicketResponse->local_ComplementaryField[5]->value)) {
                            $libelleTechnique = $troubleTicketResponse->local_ComplementaryField[5]->value;
                        }

```

Question métier : Point de décision — array_key_exists('5', 'troubleTicketResponse'->local_ComplementaryField) et isset('troubleTicketResponse'->local_ComplementaryField[5]->value). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #355 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 150
Contexte   :
```php
                        }

                        if (array_key_exists('4', $troubleTicketResponse->local_ComplementaryField) && isset($troubleTicketResponse->local_ComplementaryField[4]->value)) {
                            $codeDetecteur = $troubleTicketResponse->local_ComplementaryField[4]->value;
                        }

```

Question métier : Point de décision — array_key_exists('4', 'troubleTicketResponse'->local_ComplementaryField) et isset('troubleTicketResponse'->local_ComplementaryField[4]->value). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #356 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 157
Contexte   :
```php
                }

                if (property_exists($troubleTicketResponse, 'troubleTicketPriority')) {
                    $priority = StringTools::convertEncoding($troubleTicketResponse->troubleTicketPriority, 'ISO-8859-15', 'UTF-8');
                }

```

Question métier : Point de décision — property_exists('troubleTicketResponse', 'troubleTicketPriority'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #357 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 161
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

**Gap #358 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 164
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

**Gap #359 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 167
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

**Gap #360 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 168
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

**Gap #361 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 171
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

**Gap #362 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 174
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

**Gap #363 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 177
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

**Gap #364 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 180
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

**Gap #365 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 185
Contexte   :
```php
                }

                if (property_exists($troubleTicketResponse, 'troubleType')) {
                    $troubleType = StringTools::convertEncoding($troubleTicketResponse->troubleType, 'ISO-8859-1', 'UTF-8');
                }

```

Question métier : Point de décision — property_exists('troubleTicketResponse', 'troubleType'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #366 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 192
Contexte   :
```php

                foreach ($partyRole as $value) {
                    if ($posteAssocie == '') {
                        $posteAssocie = (!empty($value->Party) && isset($value->Party->Local_occupationCode)) ? $value->Party->Local_occupationCode : '';
                    }

```

Question métier : Point de décision — 'posteAssocie' égal à ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #367 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 196
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

**Gap #368 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 199
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

**Gap #369 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 203
Contexte   :
```php
                        }

                        if ($value->Local_PartyIntervention->level == 1 && $interventionStatus && $value->PartyRoleSet->partyRoleSetID == $connectedEds) {
                            $actif = 1;
                            $edsActif = $value->PartyRoleSet->partyRoleSetID;
                            break;
```

Question métier : Point de décision — 'value'->Local_PartyIntervention->level égal à 1 et 'interventionStatus' et 'value'->PartyRoleSet->partyRoleSetID égal à 'connectedEds'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #370 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 207
Contexte   :
```php
                            $edsActif = $value->PartyRoleSet->partyRoleSetID;
                            break;
                        } elseif ($value->Local_PartyIntervention->level == 2 && $interventionStatus && $value->PartyRoleSet->partyRoleSetID == $connectedEds) {
                            $actif = 1;
                            $edsActifNiveau2 = $value->PartyRoleSet->partyRoleSetID;
                            break;
```

Question métier : Point de décision — 'value'->Local_PartyIntervention->level égal à 2 et 'interventionStatus' et 'value'->PartyRoleSet->partyRoleSetID égal à 'connectedEds'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #371 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 215
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

**Gap #372 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 216
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

**Gap #373 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 226
Contexte   :
```php
                $niveauUrgence = property_exists($troubleTicketResponse, 'troubleUrgency') ? $troubleTicketResponse->troubleUrgency : '';

                if ($driDate != '' && $drcDate != '') {
                    $type = "DRI / DRC";
                    $drDate = OceaneTools::changeUTCToDate('d/m/Y H:i', $drcDate);
                } elseif ($drcDate != '') {
```

Question métier : Point de décision — 'driDate' différent de '' et 'drcDate' différent de ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #374 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 229
Contexte   :
```php
                    $type = "DRI / DRC";
                    $drDate = OceaneTools::changeUTCToDate('d/m/Y H:i', $drcDate);
                } elseif ($drcDate != '') {
                    $type = "DRC";
                    $drDate = OceaneTools::changeUTCToDate('d/m/Y H:i', $drcDate);
                } elseif ($driDate != '') {
```

Question métier : Point de décision — 'drcDate' différent de ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #375 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 232
Contexte   :
```php
                    $type = "DRC";
                    $drDate = OceaneTools::changeUTCToDate('d/m/Y H:i', $drcDate);
                } elseif ($driDate != '') {
                    $type = "DRI";
                    $drDate = OceaneTools::changeUTCToDate('d/m/Y H:i', $driDate);
                }
```

Question métier : Point de décision — 'driDate' différent de ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #376 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 240
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

**Gap #377 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 244
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

**Gap #378 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 245
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

**Gap #379 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 247
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

**Gap #380 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 253
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

**Gap #381 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 258
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

**Gap #382 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 266
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

**Gap #383 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 270
Contexte   :
```php
                }

                if (property_exists($troubleTicketResponse, 'troubleTicketCategory')) {
                    $evtIncident = $troubleTicketResponse->troubleTicketCategory;
                }

```

Question métier : Point de décision — property_exists('troubleTicketResponse', 'troubleTicketCategory'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #384 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 377
Contexte   :
```php
        $oceaneApi = new Oceane($token, $headerConfig);

        if (array_key_exists('trouble_ticket_priority', $data) && isset($data['trouble_ticket_priority'])) {
            $values['TROUBLE_TICKET_PRIORITY'] = intval($data['trouble_ticket_priority']);
        } else {
            $values['TROUBLE_TICKET_PRIORITY'] = '0';
```

Question métier : Point de décision — array_key_exists('trouble_ticket_priority', 'data') et isset('data'['trouble_ticket_priority']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #385 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 382
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

**Gap #386 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 386
Contexte   :
```php
        }

        if (array_key_exists('astroid', $data) && isset($data['astroid'])) {
            $values['astroid'] = $data['astroid'];
        }

```

Question métier : Point de décision — array_key_exists('astroid', 'data') et isset('data'['astroid']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #387 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 390
Contexte   :
```php
        }

        if (array_key_exists('party_role_party_ID', $data) && isset($data['party_role_party_ID'])) {
            $values['PARTYROLE_PARTY_ID'] = $data['party_role_party_ID'];
        }

```

Question métier : Point de décision — array_key_exists('party_role_party_ID', 'data') et isset('data'['party_role_party_ID']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #388 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 394
Contexte   :
```php
        }

        if (array_key_exists('postes_associe', $data) && isset($data['postes_associe'])) {
            $values['POSTE_ASSOCIE_ID'] = $data['postes_associe'];
        }

```

Question métier : Point de décision — array_key_exists('postes_associe', 'data') et isset('data'['postes_associe']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #389 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 398
Contexte   :
```php
        }

        if (array_key_exists('niv_urgence', $data) && isset($data['niv_urgence'])) {
            $values['NIV_URGENCE_ID'] = $data['niv_urgence'];
        }

```

Question métier : Point de décision — array_key_exists('niv_urgence', 'data') et isset('data'['niv_urgence']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #390 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 402
Contexte   :
```php
        }

        if (array_key_exists('action_eds', $data) && isset($data['action_eds'])) {
            $values['ACTION_EDS_IN_PROGRESS'] = $data['action_eds'];
        }

```

Question métier : Point de décision — array_key_exists('action_eds', 'data') et isset('data'['action_eds']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #391 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 406
Contexte   :
```php
        }

        if (array_key_exists('commentaire_eds', $data) && isset($data['commentaire_eds'])) {
            $values['LOCAL_COMEMENTAIRE'] = $data['commentaire_eds'];
        }

```

Question métier : Point de décision — array_key_exists('commentaire_eds', 'data') et isset('data'['commentaire_eds']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #392 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 410
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

**Gap #393 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 420
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

**Gap #394 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 423
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

**Gap #395 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 433
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

**Gap #396 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 436
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

**Gap #397 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 439
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

**Gap #398 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 442
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

**Gap #399 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 446
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

**Gap #400 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 456
Contexte   :
```php
                ini_set('default_socket_timeout', 60);

                if ($nbCellules <= $maxImapct) {
                    $this->app->get('TraceRepository')->setTrace($values['astroid'], "QUALIFIER OCEANE ENVOI ALL_CELLULES", $values, $this->app->get('Session')->getUtilisateurId(), $values['ticketId']);
                    $result = json_decode($oceaneApi->updateMobileImpactRessources($oceaneApiData['url'], $values['ticketId'], $values , true), true);
                    json_decode($oceaneApi->ajoutCommentaireMobile($oceaneApiData['url'], $values), true);
```

Question métier : Point de décision — 'nbCellules' <= 'maxImapct'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #401 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 483
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

**Gap #402 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 486
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

**Gap #403 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 489
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

**Gap #404 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 492
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

**Gap #405 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 517
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

**Gap #406 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 535
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

**Gap #407 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 622
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

**Gap #408 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 625
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

**Gap #409 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 630
Contexte   :
```php
        }

        if ($confirmTowStep == 'oui') {
            $dataUpdateFirstStep = array(
                'detectionDate' => $dateDebutIncidentUTCZulu
            );
```

Question métier : Point de décision — 'confirmTowStep' égal à 'oui'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #410 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 638
Contexte   :
```php
            $this->app->get('TraceRepository')->setTrace($astroId, "RETOUR OCEANE CONFIRMER TRANS 1 STEP", $retourUpdate, $this->sessId, $ticketId);

            if (key_exists('code', $retourUpdate)) {
                return $retourUpdate;
            } else {
                $this->app->get('TraceRepository')->setTrace($astroId, "ENVOI OCEANE CONFIRMER TRANS 2 STEP", $dataUpdate, $this->sessId, $ticketId);
```

Question métier : Point de décision — key_exists('code', 'retourUpdate'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #411 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 646
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

**Gap #412 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 728
Contexte   :
```php
        $data['commentaire_impact_client'] = isset($data['commentaire_impact_client']) ? $data['commentaire_impact_client'] : '';
        $data['priorite_commentaire'] = isset($data['priorite_commentaire']) ? $data['priorite_commentaire'] : '';
        if ($data['priorite_commentaire'] == '') {
            $priorityComment = '# priorité #' . $rc . 'priorité calculée : P' . $data['priorite'] . $rc;
        } else {
            $priorityComment = '# priorité #' . $rc . 'priorité modifiée : P' . $data['priorite'] . $rc;
```

Question métier : Point de décision — 'data'['priorite_commentaire'] égal à ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #413 — OceaneService**

**→ Copier dans Copilot**

Fichier    : OceaneService.php
Méthode    : ligne 732
Contexte   :
```php
        } else {
            $priorityComment = '# priorité #' . $rc . 'priorité modifiée : P' . $data['priorite'] . $rc;
            if ($data['priorite_commentaire'] == '4') {
                $priorityComment .= ($data['commentaire1']);
            } else {
                $priorityComment .= StringTools::convertEncoding($data['priorite_commentaire'], 'ISO-8859-15', 'UTF-8');
```

Question métier : Point de décision — 'data'['priorite_commentaire'] égal à '4'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #414 — VariableBaseService**

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

**Gap #415 — VariableBaseService**

**→ Copier dans Copilot**

Fichier    : VariableBaseService.php
Méthode    : ligne 39
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

**Gap #416 — VariableBaseService**

**→ Copier dans Copilot**

Fichier    : VariableBaseService.php
Méthode    : ligne 42
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

**Gap #417 — VariableBaseService**

**→ Copier dans Copilot**

Fichier    : VariableBaseService.php
Méthode    : ligne 48
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

**Gap #418 — VariableBaseService**

**→ Copier dans Copilot**

Fichier    : VariableBaseService.php
Méthode    : ligne 51
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

**Gap #419 — VariableBaseService**

**→ Copier dans Copilot**

Fichier    : VariableBaseService.php
Méthode    : ligne 59
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

**Gap #420 — VariableBaseService**

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

**Gap #421 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 123
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

**Gap #422 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 131
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

**Gap #423 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 133
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

**Gap #424 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 137
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

**Gap #425 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 142
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

**Gap #426 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 143
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

**Gap #427 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 147
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

**Gap #428 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 149
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

**Gap #429 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 153
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

**Gap #430 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 165
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

**Gap #431 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 171
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

**Gap #432 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 178
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

**Gap #433 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 185
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

**Gap #434 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 195
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

**Gap #435 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 203
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

**Gap #436 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 210
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

**Gap #437 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 217
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

**Gap #438 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 226
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

**Gap #439 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 234
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

**Gap #440 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 242
Contexte   :
```php
                    $replaceValue = (!is_null($this->getDslam('MIN'))) ? $this->getDslam('MIN') : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #441 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 251
Contexte   :
```php
                    $replaceValue = (!is_null($this->eds)) ? $this->eds : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #442 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 259
Contexte   :
```php
                    $replaceValue = (!is_null($this->typeRessource)) ? $this->typeRessource : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #443 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 270
Contexte   :
```php

                case 'DATE':
                    if (is_null($this->findAndGet)) {
                        $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
                    }

```

Question métier : Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #444 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 276
Contexte   :
```php
                    $replaceValue = isset($this->findAndGet['fg_date']) ? $this->findAndGet['fg_date'] : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #445 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 284
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

**Gap #446 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 287
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

**Gap #447 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 291
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

**Gap #448 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 297
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

**Gap #449 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 301
Contexte   :
```php
                    }

                    if (!isset($this->findAndGet['message']) && !is_null($this->findAndGet['rd_plus'])) {
                        $replaceValue = (!is_null($this->findAndGet['rd_plus'])) ? $this->findAndGet['rd_plus'] : null;

                        if (OceaneTools::isValidVariable($replaceValue)) {
```

Question métier : Point de décision — !isset('this'->findAndGet['message']) et !is_null('this'->findAndGet['rd_plus']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #450 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 304
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

**Gap #451 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 310
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

**Gap #452 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 314
Contexte   :
```php
                    }

                    if (!isset($this->findAndGet['message']) && !is_null($this->findAndGet['description'])) {
                        $replaceValue = (!is_null($this->findAndGet['description'])) ? $this->findAndGet['description'] : null;

                        if (OceaneTools::isValidVariable($replaceValue)) {
```

Question métier : Point de décision — !isset('this'->findAndGet['message']) et !is_null('this'->findAndGet['description']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #453 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 317
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

**Gap #454 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 323
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

**Gap #455 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 326
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

**Gap #456 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 327
Contexte   :
```php
                    }
                    if (!isset($this->findAndGet['message']) && !is_null($this->findAndGet['code_detecteur'])) {
                        if (!is_null($this->findAndGet['code_detecteur'])) {
                            $replaceValue = ($this->findAndGet['code_detecteur'] != "ORANGE") ? $this->findAndGet['code_detecteur'] : "UI";
                        } else {
                            $replaceValue = null;
```

Question métier : Point de décision — !is_null('this'->findAndGet['code_detecteur']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #457 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 333
Contexte   :
```php
                        }

                        if (OceaneTools::isValidVariable($replaceValue)) {
                            $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                        }

```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #458 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 347
Contexte   :
```php

                case 'INTERVENANT_REFSITES':
                    if (in_array($type, $this->arrayRessourcesTransAvecExt)) {
                        $replaceValue = $this->getIntervenant($type, $variable, $extrimite);
                    } else {
                        $replaceValue = $this->getIntervenant($type);
```

Question métier : Point de décision — in_array('type', 'this'->arrayRessourcesTransAvecExt). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #459 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 353
Contexte   :
```php
                    }

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);

                    }
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #460 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 375
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

**Gap #461 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 402
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

**Gap #462 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 405
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

**Gap #463 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 415
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

**Gap #464 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 418
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

**Gap #465 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 424
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

**Gap #466 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 426
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

**Gap #467 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 429
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

**Gap #468 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 431
Contexte   :
```php
                        if (!isset($this->findAndGet['message'])) {

                            if (!is_null($this->findAndGet['installed_resource']) && property_exists($this->findAndGet['installed_resource'], 'ResourceSpecification') && property_exists($this->findAndGet['installed_resource']->ResourceSpecification,
                                    'resourceSpecificationCode')) {
                                $resourceSpecification = $this->findAndGet['installed_resource']->ResourceSpecification->resourceSpecificationCode;
                            } elseif (!is_null($this->findAndGet['installed_service']) && property_exists($this->findAndGet['installed_service'], 'ServiceSpecification') && property_exists($this->findAndGet['installed_service']->ServiceSpecification,
```

Question métier : Point de décision — !is_null('this'->findAndGet['installed_resource']) et property_exists('this'->findAndGet['installed_resource'], 'ResourceSpecification') et property_exists('this'->findAndGet['installed_resource']->ResourceSpecification, 'resourceSpecificationCode'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #469 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 434
Contexte   :
```php
                                    'resourceSpecificationCode')) {
                                $resourceSpecification = $this->findAndGet['installed_resource']->ResourceSpecification->resourceSpecificationCode;
                            } elseif (!is_null($this->findAndGet['installed_service']) && property_exists($this->findAndGet['installed_service'], 'ServiceSpecification') && property_exists($this->findAndGet['installed_service']->ServiceSpecification,
                                    'serviceSpecificationCode')) {
                                $resourceSpecification = $this->findAndGet['installed_service']->ServiceSpecification->serviceSpecificationCode;
                            }
```

Question métier : Point de décision — !is_null('this'->findAndGet['installed_service']) et property_exists('this'->findAndGet['installed_service'], 'ServiceSpecification') et property_exists('this'->findAndGet['installed_service']->ServiceSpecification, 'serviceSpecificationCode'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #470 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 440
Contexte   :
```php


                            if ($resourceSpecification != "") {
                                $data = array(
                                    'type' => $resourceSpecification,
                                    'nom' => $arg
```

Question métier : Point de décision — 'resourceSpecification' différent de "". Quel est le comportement attendu dans le cas contraire ?

---

**Gap #471 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 446
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

**Gap #472 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 448
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

**Gap #473 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 478
Contexte   :
```php
        $ext2 = $this->getOceane->getRessourceIds(2);

        $isSitePassifext1 = $this->refSiteRepository->isSitePassif($this->transcodage($ext1));
        $isSitePassifext2 = $this->refSiteRepository->isSitePassif($this->transcodage($ext2));

        return $this->selectExtension($ext1, $isSitePassifext1, $ext2, $isSitePassifext2);
```

Question métier : Point de décision — 'this'->transcodage('ext1')); 'isSitePassifext2' = 'this'->refSiteRepository->isSitePassif('this'->transcodage('ext2')); return 'this'->selectExtension('ext1', 'isSitePassifext1', 'ext2', 'isSitePassifext2'); } public function selectExtension('ext1', 'ext1_status', 'ext2', 'ext2_status'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #474 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 489
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

**Gap #475 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 493
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

**Gap #476 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 497
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

**Gap #477 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 501
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

**Gap #478 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 513
Contexte   :
```php
        $this->refSiteRepository = $this->app->get('RefsitesRepository');
        $resultQuery = false;
        if ($typeRessource == 'TRONCABLE') { // Si le type de ressource est TRONCABLE, on récupère la valeur de la variable PRIMO_AIGUILLAGE_TRONCON
            $variableAdministree = 'PRIMO_AIGUILLAGE_TRONCON';
        } else {
            $variableAdministree = 'INTERVENANT_MATRICE_REFSITES';
```

Question métier : Point de décision — 'typeRessource' égal à 'TRONCABLE'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #479 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 519
Contexte   :
```php
        }

        if ($variable != '') {
            $intervenantMatriceRefsite = $variable;
        } else {
            $argsVariableGlobal = array();
```

Question métier : Point de décision — 'variable' différent de ''. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #480 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 527
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

**Gap #481 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 563
Contexte   :
```php
                    $refsiteFirst = preg_replace('/\s\s+/', ' ', trim($refsiteFirst));
                    $refsiteFirst = str_replace("!", "/", $refsiteFirst);
                    if ($typeRessource == 'MIE') {
                        $extremiteTechno = 'TECHNO';
                    } else {
                        if ($ext == 'tabs_action_ext1') {
```

Question métier : Point de décision — 'typeRessource' égal à 'MIE'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #482 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 566
Contexte   :
```php
                        $extremiteTechno = 'TECHNO';
                    } else {
                        if ($ext == 'tabs_action_ext1') {
                            $extremiteTechno = 'EXT1_TECHNO';
                        } elseif ($ext == 'tabs_action_ext2') {
                            $extremiteTechno = 'EXT2_TECHNO';
```

Question métier : Point de décision — 'ext' égal à 'tabs_action_ext1'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #483 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 568
Contexte   :
```php
                        if ($ext == 'tabs_action_ext1') {
                            $extremiteTechno = 'EXT1_TECHNO';
                        } elseif ($ext == 'tabs_action_ext2') {
                            $extremiteTechno = 'EXT2_TECHNO';
                        }
                    }
```

Question métier : Point de décision — 'ext' égal à 'tabs_action_ext2'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #484 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 577
Contexte   :
```php
                    $techno = $this->replaceTagsChaine("###$extremiteTechno###", $argsVariableGlobal1, $typeRessource, $this->ticketId);

                    if ($techno == 'FH') {
                        $resultQuery = $this->refSiteRepository->getFhByAppelationIr($refsiteFirst);
                    } else {
                        $resultQuery = $this->refSiteRepository->getRsByAppelationIr($refsiteFirst);
```

Question métier : Point de décision — 'techno' égal à 'FH'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #485 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 592
Contexte   :
```php
        }

        if (gettype($resultQuery) != 'boolean' && $resultQuery != '' && is_array($resultQuery)) {
            $intervenant = key_exists('INTERVENANT', $resultQuery) ? $resultQuery['INTERVENANT'] : '';
            if (key_exists('ID', $resultQuery)) {
                $this->refSiteRepository->UpdateTicketAstroWithIdRefsite($this->ticketId, $resultQuery['ID']);
```

Question métier : Point de décision — gettype('resultQuery') différent de 'boolean' et 'resultQuery' différent de '' et is_array('resultQuery'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #486 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 594
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

**Gap #487 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 605
Contexte   :
```php
    public function replaceCaractRefSite($intervenantMatriceRefsite)
    {
        if (strpos($intervenantMatriceRefsite, "/")) {
            $refsiteFirst = substr($intervenantMatriceRefsite, 0, -strlen(strrchr($intervenantMatriceRefsite, '/')));
            $refsiteFirst = preg_replace('/\s\s+/', ' ', trim($refsiteFirst));
        } else {
```

Question métier : Point de décision — strpos('intervenantMatriceRefsite', "/"). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #488 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 616
Contexte   :
```php
    public function replaceCaractRefSiteAgglo($value)
    {
        if (strpos($value, "/")) {
            $refsiteFirst = substr($value, 0, -strlen(strrchr($value, '/')));
            $refsiteFirst = str_replace(":", " ", $refsiteFirst);
            $refsiteFirst = str_replace("!", "/", $refsiteFirst);
```

Question métier : Point de décision — strpos('value', "/"). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #489 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 657
Contexte   :
```php
        $infraContextePari = $this->replaceTagsChaine("###$variableAdministree###", $argsVariableGlobal, $typeRessource, $ticketId);

        if (!in_array($infraContextePari, ["###$variableAdministree###", ''])) {
            if (is_null($this->dataPariv2)) {
                $dataJson = $this->getDataPariv2($ticketId, $typeRessource, $infraContextePari);

```

Question métier : Point de décision — !in_array('infraContextePari', ["###'variableAdministree'###", '']). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #490 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 658
Contexte   :
```php

        if (!in_array($infraContextePari, ["###$variableAdministree###", ''])) {
            if (is_null($this->dataPariv2)) {
                $dataJson = $this->getDataPariv2($ticketId, $typeRessource, $infraContextePari);

                if ($this->app->get('AstroBase')->isJson($dataJson)) {
```

Question métier : Point de décision — is_null('this'->dataPariv2). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #491 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 661
Contexte   :
```php
                $dataJson = $this->getDataPariv2($ticketId, $typeRessource, $infraContextePari);

                if ($this->app->get('AstroBase')->isJson($dataJson)) {
                    $this->dataPariv2 = Json::decode($dataJson, JSON::TYPE_ARRAY);
                    $this->app->get('TraceRepository')->setTrace($astroId, "PARI V2 REPONSE", $this->dataPariv2, $this->sessId, $ticketId);
                } else {
```

Question métier : Point de décision — 'this'->app->get('AstroBase')->isJson('dataJson'). Quel est le comportement attendu dans le cas contraire ?

---

**Gap #492 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 670
Contexte   :
```php

            $replaceValue = $this->getReplaceValue($this->dataPariv2, $variable);
            if (OceaneTools::isValidVariable($replaceValue) && gettype($replaceValue) != 'boolean') {
                $chaine = str_replace('###' . $variable . '###', $replaceValue, $chaine);
            } else {
                $chaine = str_replace('###' . $variable . '###', '', $chaine);
```

Question métier : Point de décision — OceaneTools::isValidVariable('replaceValue') et gettype('replaceValue') différent de 'boolean'. Quel est le comportement attendu dans le cas contraire ?

---

**Gap #493 — VariableService**

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

**Gap #494 — VariableService**

**→ Copier dans Copilot**

Fichier    : VariableService.php
Méthode    : ligne 760
Contexte   :
```php
            $value = $data;
            foreach ($keys as $key) {
                if (is_array($value) && key_exists($key, $value)) {
                    $value = $value[$key];
                } else {
                    return null;
```

Question métier : Point de décision — is_array('value') et key_exists('key', 'value'). Quel est le comportement attendu dans le cas contraire ?
