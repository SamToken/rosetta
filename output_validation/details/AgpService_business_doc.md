# AgpController — Règles Métier
Extrait le : 2026-04-26 | Confiance extraction : 0.6000000000000001

## Méthode : initAgp()

### Questions ouvertes pour arbitrage
- [ ] initAgp.session_key : cette clé est-elle nettoyée dans tous les chemins de sortie ?

---

## Méthode : displayAgp1()

### Questions ouvertes pour arbitrage
- [ ] displayAgp1.session_key : cette clé est-elle nettoyée dans tous les chemins de sortie ?
- [ ] displayAgp1.maitreDeport : Le code situation 'ok' est hardcodé — vient-il d'une table de référence Oracle ?
- [ ] displayAgp1.maitreDeport : Le code situation 'nok' est hardcodé — vient-il d'une table de référence Orac...
- [ ] displayAgp1.typeRessource : Le code situation 'DSLAM' est hardcodé — vient-il d'une table de référence Or...

---

## Méthode : displayAGP2()

---

## Méthode : displayAGP3()

### Points d'attention
- 🔴 **// 'Alarme'=>données de l'agent connecté**
  - L'identité de l'agent connecté est lue directement depuis la session. L'habilitation est-elle vérifiée par un service centralisé ou uniquement à cet endroit ?

### Questions ouvertes pour arbitrage
- [ ] displayAGP3.session : l'habilitation est-elle vérifiée par un service centralisé ?
- [ ] displayAGP3.session_key : cette clé est-elle nettoyée dans tous les chemins de sortie ?

---

## Méthode : getOptionsActions()

---

## Méthode : displayAgp1Generique()

### Questions ouvertes pour arbitrage
- [ ] displayAgp1Generique.session_key : cette clé est-elle nettoyée dans tous les chemins de sortie ?
- [ ] displayAgp1Generique.typeRessource : Le code situation 'DSLAM' est hardcodé — vient-il d'une table de référence Or...
- [ ] displayAgp1Generique.maitreDeport : Le code situation 'ok' est hardcodé — vient-il d'une table de référence Oracle ?
- [ ] displayAgp1Generique.maitreDeport : Le code situation 'nok' est hardcodé — vient-il d'une table de référence Orac...
- [ ] displayAgp1Generique.typeRessource : Le code situation 'MIE' est hardcodé — vient-il d'une table de référence Orac...
- [ ] displayAgp1Generique.typeRessource : Le code situation 'SLN' est hardcodé — vient-il d'une table de référence Orac...

---

## Méthode : getCommentaireByType()

---

## Méthode : getOptionsCommentaireGenerique()

---

## Méthode : getOptionsActionsGenerique()

### Questions ouvertes pour arbitrage
- [ ] getOptionsActionsGenerique.typeRessource : Le code situation 'COMMUT' est hardcodé — vient-il d'une table de référence O...
- [ ] getOptionsActionsGenerique.typeRessource : Le code situation 'DSLAM' est hardcodé — vient-il d'une table de référence Or...

---

## Méthode : displayPiloterGenerique()

### Questions ouvertes pour arbitrage
- [ ] displayPiloterGenerique.session_key : cette clé est-elle nettoyée dans tous les chemins de sortie ?
- [ ] displayPiloterGenerique.idUrgenceOceane : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...
- [ ] displayPiloterGenerique.data : Le code situation 'HO' est hardcodé — vient-il d'une table de référence Oracle ?
- [ ] displayPiloterGenerique.data : Le code situation 'HNO' est hardcodé — vient-il d'une table de référence Orac...
- [ ] displayPiloterGenerique.data : Le code situation 'DiagSDH' est hardcodé — vient-il d'une table de référence ...

---

## Méthode : getCommentaireAgp2Generique()

### Questions ouvertes pour arbitrage
- [ ] getCommentaireAgp2Generique.session_key : cette clé est-elle nettoyée dans tous les chemins de sortie ?
- [ ] getCommentaireAgp2Generique.variables : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...

---

## Méthode : displayAgp2Generique()

### Points d'attention
- 🔴 **// 'Alarme'=>données de l'agent connecté**
  - L'identité de l'agent connecté est lue directement depuis la session. L'habilitation est-elle vérifiée par un service centralisé ou uniquement à cet endroit ?

### Questions ouvertes pour arbitrage
- [ ] displayAgp2Generique.session : l'habilitation est-elle vérifiée par un service centralisé ?
- [ ] displayAgp2Generique.session_key : cette clé est-elle nettoyée dans tous les chemins de sortie ?
- [ ] displayAgp2Generique.isValeurNiveauUrgenceHeriteeOceane : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...
- [ ] displayAgp2Generique.data : Le code situation 'HO' est hardcodé — vient-il d'une table de référence Oracle ?
- [ ] displayAgp2Generique.data : Le code situation 'HNO' est hardcodé — vient-il d'une table de référence Orac...
- [ ] displayAgp2Generique.data : Le code situation 'DSLAM' est hardcodé — vient-il d'une table de référence Or...
- [ ] displayAgp2Generique.data : Le code situation 'DiagSDH' est hardcodé — vient-il d'une table de référence ...

---

## Méthode : checkActionInput()

### Questions ouvertes pour arbitrage
- [ ] checkActionInput.input : Le code situation 'alarme' est hardcodé — vient-il d'une table de référence O...

---

## Méthode : getCartesLignes()

---

## Méthode : displayCreationTocTrans()

### Questions ouvertes pour arbitrage
- [ ] displayCreationTocTrans.session_key : cette clé est-elle nettoyée dans tous les chemins de sortie ?
- [ ] displayCreationTocTrans.data : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...
- [ ] displayCreationTocTrans.data : Le code situation 'TRCCABLE' est hardcodé — vient-il d'une table de référence...
- [ ] displayCreationTocTrans.data : Le code situation 'SDH' est hardcodé — vient-il d'une table de référence Orac...
- [ ] displayCreationTocTrans.data : Le code situation 'MIE' est hardcodé — vient-il d'une table de référence Orac...

---

## Méthode : displayCreationTocAdsl()

### Questions ouvertes pour arbitrage
- [ ] displayCreationTocAdsl.session_key : cette clé est-elle nettoyée dans tous les chemins de sortie ?

---

## Méthode : creerTicketRessourceAdsl()

### Questions ouvertes pour arbitrage
- [ ] creerTicketRessourceAdsl.oceaneApiData : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...

---

## Méthode : displayEcranChx()

---

## Méthode : replaceTagsChaineEnchainement()

### Points d'attention
- 🔴 **token = base64_encode(md5(date('yyyymmdd') . 'link_astro_charter'))**
  - Cette méthode de protection du secret d'authentification est ancienne et non conforme aux standards actuels. S'agit-il d'une contrainte documentée ou cette protection est-elle prévue pour évoluer lors de la migration ?

### Questions ouvertes pour arbitrage
- [ ] replaceTagsChaineEnchainement.md5 : cette méthode de protection est-elle une contrainte documentée ?
- [ ] replaceTagsChaineEnchainement.libSite : L'état du ticket est lu depuis Oceane en temps réel à cette étape — 3 cas non...
- [ ] replaceTagsChaineEnchainement.donnesTempsReel : Le code situation 'ok' est hardcodé — vient-il d'une table de référence Oracle ?

---

## Méthode : getUserId()

---

## Méthode : aiguillageManuel()

---

## Méthode : aiguillageCommentaireRemplaceBloc()

### Questions ouvertes pour arbitrage
- [ ] aiguillageCommentaireRemplaceBloc.keyVariable : Le code situation 'CODE_EAN' est hardcodé — vient-il d'une table de référence...
- [ ] aiguillageCommentaireRemplaceBloc.keyTag : Le code situation 'ean' est hardcodé — vient-il d'une table de référence Orac...
- [ ] aiguillageCommentaireRemplaceBloc.dataTag : Le code situation 'True' est hardcodé — vient-il d'une table de référence Ora...
- [ ] aiguillageCommentaireRemplaceBloc.keyVariable : Le code situation 'Types' est hardcodé — vient-il d'une table de référence Or...

---

## Méthode : aiguillageCommentaireAction()

### Questions ouvertes pour arbitrage
- [ ] aiguillageCommentaireAction.astroData : Le code situation 'DSLAM' est hardcodé — vient-il d'une table de référence Or...

---

## Méthode : getLogin()

---

## Points de décision — Comportements non définis
- ⚠️ **Gap de logique**
  - Point de décision — count('deports') > 0. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'maitreDeport'['status'] égal à 'ok'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'master' différent de '' et 'master' différent de 'dslamName'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'alarme' différent de 'dslamName'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'typeRessource' égal à 'DSLAM'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !is_null('chassisCarte') et 'chassisCarte' et key_exists('CHASSIS', 'chassisCarte'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'typeRessource' égal à 'MIE'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'typeRessource' égal à 'SLN' ou 'typeRessource' égal à 'WDM_SID'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'typeRessource' égal à 'COMMUT' ou 'typeRessource' égal à 'UNIRACC' ou 'typeRessource' égal à 'CONNUM' ou 'typeRessource' égal à 'MICBPNCSN' ou 'typeRessource' égal à 'MICBPNCAA' ou 'typeRessource' égal à 'MICBPNCOM'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — ('typeRessource' égal à 'DSLAM' ou 'typeRessource' égal à 'DSLAMDERCO') et 'data'['id_rsc'] différent de '' et 'data'['id_rsc_dslam'] différent de ''. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !le champ 'ressource' est vide. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !'api'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('oceaneData'['oceane_priority'], 'priorityHoHno'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !le champ 'blocs' est vide && key_exists(0, $blocs). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'blocName' différent de 'choix_de_carte_trans' et 'blocName' différent de 'Types_Carte' et 'blocName' différent de 'Types' et 'blocName' différent de 'Carte_EAN' et 'blocName' différent de 'Complet'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_string('data'['id_commentaire']) et 'data'['id_commentaire'] égal à 'DiagSDH'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('intervenant', 'data') et 'data'['intervenant'] différent de ''. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('segComment') et isset('segComment'['SECOND_COMMENT']) et trim('segComment'['SECOND_COMMENT']) différent de = ''. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'data'['type_ressource'] égal à 'DSLAM' ou 'data'['type_ressource'] égal à 'DSLAMDERCO'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'astroSession'['type'] égal à 'DSLAM' ou 'astroSession'['type'] égal à 'DSLAMDERCO'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'isDslamTest'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'idRscDslam' différent de = null et 'idRscDslam' différent de = ''. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'data'['agp_ecran'] égal à 0. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !'idUrgenceOceane'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'dslamArray'['racks']['k']['rackName'] égal à 'chassis'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — isset('vv'['category']) et 'vv'['category'] différent de 'carte ligne'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'test'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'data'['type'] égal à 'TRCCABLE' ou 'data'['type'] égal à 'TRONCABLE' ou 'data'['type'] égal à 'CABLE'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'data'['type'] égal à 'SDH' ou 'data'['type'] égal à 'SLN' ou 'data'['type'] égal à 'PDH' ou 'data'['type'] égal à 'ETH' ou 'data'['type'] égal à 'OCH' ou 'data'['type'] égal à 'WDM_SID'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'data'['type'] égal à 'MIE'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'astroId' égal à ''. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !'this'->getOceane. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'this'->ticketId et 'this'->getOceane. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'arg' égal à 'Temperature' ou 'arg' égal à 'Etat_batterie' ou 'arg' égal à 'Tension_batterie' ou 'arg' égal à 'Element_HS'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'libSite' différent de "". Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — OceaneTools::isValidVariable('replaceValue'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !is_null('codeDetecteur'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — OceaneTools::isValidVariable('replaceValue') et gettype('replaceValue') différent de 'boolean'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'this'->typeRessource égal à 'TRONCABLE'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'this'->globalApiRepository->isVariableAdminExist('arg', 'type'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'resourceSpecification'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — count('tabIdentifiants') > 0 et 'this'->ticketId différent de = null. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — isset('replaceValue'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'intervenant' différent de 'ORANGE'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — is_array('intervenantInfos'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !is_null('allEcransValues') et is_array('allEcransValues'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'Carte_EAN' égal à 'blocName' et key_exists('donnee_cartes', 'allEcranValuesArray'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'keyVariable' différent de 'donnee_cartes' et 'keyVariable' différent de 'CODE_EAN' et 'keyVariable' différent de 'Nom_Carte' et 'keyVariable' différent de 'Type_Equipement'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'keyVariable' égal à 'CODE_EAN'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'keyTag' égal à 'CODE_EAN'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'keyVariable' égal à 'Type_Equipement'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'keyTag' égal à 'TYPE_EQUIPEMENT'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'keyVariable' égal à 'Nom_Carte'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'keyTag' égal à 'NOM_CARTE'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'keyVariable2' différent de 'donnee_cartes'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'astroData'['type'] égal à 'DSLAM' ou 'astroData'['type'] égal à 'DSLAMDERCO'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Valeur de référence**
  - Valeur de référence non documentée — La décision « 'maitreDeport'['status'] égal à 'ok' » repose sur la valeur 'ok'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?
- ⚠️ **Valeur de référence**
  - Valeur de référence non documentée — La décision « 'maitreDeport'['status'] égal à 'nok' » repose sur la valeur 'nok'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?
- ⚠️ **Valeur de référence**
  - Valeur de référence non documentée — La décision « 'blocName' différent de 'choix_de_carte_trans' et 'blocName' différent de 'Types_Carte' et 'blocName' différent de 'Types' et 'blocName' différent de 'Carte_EAN' et 'blocName' différent de 'Complet' » repose sur la valeur 'choix_de_carte_trans'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?
- ⚠️ **Valeur de référence**
  - Valeur de référence non documentée — La décision « in_array('input', 'carteArray') ou (('input' égal à 'alarme') et ('hasChassis' égal à 'false')) » repose sur la valeur 'alarme'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?
- ⚠️ **Valeur de référence**
  - Valeur de référence non documentée — La décision « key_exists('etat', 'donnesTempsReel') et 'donnesTempsReel'['etat'] égal à 'ok' » repose sur la valeur 'ok'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?
- ⚠️ **Valeur de référence**
  - Valeur de référence non documentée — La décision « OceaneTools::isValidVariable('replaceValue') et gettype('replaceValue') différent de 'boolean' » repose sur la valeur 'boolean'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?
- ⚠️ **Valeur de référence**
  - Valeur de référence non documentée — La décision « 'keyVariable' différent de 'donnee_cartes' et 'keyVariable' différent de 'CODE_EAN' et 'keyVariable' différent de 'Nom_Carte' et 'keyVariable' différent de 'Type_Equipement' » repose sur la valeur 'donnee_cartes'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?
- ⚠️ **Valeur de référence**
  - Valeur de référence non documentée — La décision « $keyVariable == 'donnee_cartes' && !le champ 'blocs' est vide && $blocName == 'choix_de_carte_trans' » repose sur la valeur 'donnee_cartes'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?
- ⚠️ **Valeur de référence**
  - Valeur de référence non documentée — La décision « 'keyTag' égal à 'ean' » repose sur la valeur 'ean'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?
- ⚠️ **Valeur de référence**
  - Valeur de référence non documentée — La décision « 'keyVariable2' différent de 'donnee_cartes' » repose sur la valeur 'donnee_cartes'. D'où vient cette valeur ? Fait-elle partie d'une liste de référence définie dans le cahier des charges ?

## Services tiers non documentés
- ❓ **App\Repository\AgpGeneriqueRepository** — Service tiers non documenté — Le composant 'App\Repository\AgpGeneriqueRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Repository\AgpRepository** — Service tiers non documenté — Le composant 'App\Repository\AgpRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Repository\AstroIhmSqlRepository** — Service tiers non documenté — Le composant 'App\Repository\AstroIhmSqlRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Repository\AstroLienRepository** — Service tiers non documenté — Le composant 'App\Repository\AstroLienRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Repository\AstroRepository** — Service tiers non documenté — Le composant 'App\Repository\AstroRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Repository\EdrRepository** — Service tiers non documenté — Le composant 'App\Repository\EdrRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Repository\GlobalApiRepository** — Service tiers non documenté — Le composant 'App\Repository\GlobalApiRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Tools\Message** — Service tiers non documenté — Le composant 'App\Tools\Message' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **\App\View\Helper\Edr** — Service tiers non documenté — Le composant '\App\View\Helper\Edr' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Tools\OceaneAssistant** — Service tiers non documenté — Le composant 'App\Tools\OceaneAssistant' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Tools\AgpCC** — Service tiers non documenté — Le composant 'App\Tools\AgpCC' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Form\DemandeInterventionForm** — Service tiers non documenté — Le composant 'App\Form\DemandeInterventionForm' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Form\DemandeInterventionGeneriqueForm** — Service tiers non documenté — Le composant 'App\Form\DemandeInterventionGeneriqueForm' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Form\DemandeInterventionSecondForm** — Service tiers non documenté — Le composant 'App\Form\DemandeInterventionSecondForm' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Form\CreaTicketTransForm** — Service tiers non documenté — Le composant 'App\Form\CreaTicketTransForm' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Form\CreaTicketAdslForm** — Service tiers non documenté — Le composant 'App\Form\CreaTicketAdslForm' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Hbm\Globalapi\Service\Rest\ApiOceane** — Service tiers non documenté — Le composant 'Hbm\Globalapi\Service\Rest\ApiOceane' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Hbm\Common\Service\LinkService** — Service tiers non documenté — Le composant 'Hbm\Common\Service\LinkService' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\View\Helper\DemandeIntervention** — Service tiers non documenté — Le composant 'App\View\Helper\DemandeIntervention' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Tools\DroitAstroTools** — Service tiers non documenté — Le composant 'App\Tools\DroitAstroTools' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **App\Tools\OceaneTools** — Service tiers non documenté — Le composant 'App\Tools\OceaneTools' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Hbm\Common\Tools\StringTools** — Service tiers non documenté — Le composant 'Hbm\Common\Tools\StringTools' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Oft\Mvc\Application** — Service tiers non documenté — Le composant 'Oft\Mvc\Application' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Zend\Json\Json** — Service tiers non documenté — Le composant 'Zend\Json\Json' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **DemandeIntervention** — Service tiers non documenté — Le composant 'DemandeIntervention' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Edr** — Service tiers non documenté — Le composant 'Edr' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **DroitAstroTools** — Service tiers non documenté — Le composant 'DroitAstroTools' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **DemandeInterventionForm** — Service tiers non documenté — Le composant 'DemandeInterventionForm' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **DemandeInterventionSecondForm** — Service tiers non documenté — Le composant 'DemandeInterventionSecondForm' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **AgpCC** — Service tiers non documenté — Le composant 'AgpCC' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **DemandeInterventionGeneriqueForm** — Service tiers non documenté — Le composant 'DemandeInterventionGeneriqueForm' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **OceaneAssistant** — Service tiers non documenté — Le composant 'OceaneAssistant' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **CreaTicketTransForm** — Service tiers non documenté — Le composant 'CreaTicketTransForm' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **CreaTicketAdslForm** — Service tiers non documenté — Le composant 'CreaTicketAdslForm' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **ApiOceane** — Service tiers non documenté — Le composant 'ApiOceane' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **LinkService** — Service tiers non documenté — Le composant 'LinkService' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Message** — Service tiers non documenté — Le composant 'Message' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?

---
**Légende :** ✅ Règle confirmée | 🔴 Point d'attention | ⚠️ Gap à arbitrer | ❓ Service à documenter
