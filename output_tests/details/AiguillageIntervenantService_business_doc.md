# AiguillageIntervenantServiceController — Règles Métier
Extrait le : 2026-04-26 | Confiance extraction : 0.29999999999999993

## Points de décision — Comportements non définis
- ⚠️ **Gap de logique**
  - Point de décision — le champ 'intervenantInfosList' est vide. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'intervenantInfos'['VARIABLE_ADMIN'] différent de '* Variables *' et !is_null('intervenantInfos'['CONDITION']) et !is_null('intervenantInfos'['VALEUR_CONDITION']). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — strpos('checkVar', 'val') égal à = 0) 'ok' = true; break; case 'equal': if (strcmp('checkVar', 'val') égal à = 0) 'ok' = true;///valeurs admin case Sensitive break; case 'contains': if (strpos('checkVar', 'val') différent de = false) 'ok' = true; break; case '': 'ok' = true; break; } if ('ok') break; } } elseif ('intervenantInfos'['VARIABLE_ADMIN'] différent de '* Variables *' et (is_null('intervenantInfos'['CONDITION']) ou is_null('intervenantInfos'['VALEUR_CONDITION'])). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'intervenantInfos'['VARIABLE_ADMIN'] égal à '* Variables *' et (!is_null('intervenantInfos'['CONDITION']) ou !is_null('intervenantInfos'['VALEUR_CONDITION'])). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'intervenantInfos'['VARIABLE_ADMIN'] égal à '* Variables *' et (is_null('intervenantInfos'['CONDITION']) ou is_null('intervenantInfos'['VALEUR_CONDITION'])). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !is_null('intervenantInfos'['TECHNO']) et 'intervenantInfos'['TECHNO'] différent de '' et 'ok'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'typeRessource' égal à 'MIE'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'ext' égal à 'tabs_action_ext1'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'ext' égal à 'tabs_action_ext2'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'techno' égal à 'FH'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'ok'. Quel est le comportement attendu dans le cas contraire ?

## Services tiers non documentés
- ❓ **App\Repository\AstroRepository** — Service tiers non documenté — Le composant 'App\Repository\AstroRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?

---
**Légende :** ✅ Règle confirmée | 🔴 Point d'attention | ⚠️ Gap à arbitrer | ❓ Service à documenter
