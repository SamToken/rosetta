# AiguillageIntervenantController — Règles Métier
Extrait le : 2026-04-26 | Confiance extraction : 0.6000000000000001

## Méthode : getIntervenantInfos()

### Questions ouvertes pour arbitrage
- [ ] getIntervenantInfos.ok : Le code situation 'EVTFIXE' est hardcodé — vient-il d'une table de référence ...
- [ ] getIntervenantInfos.ok : Le code situation 'RS' est hardcodé — vient-il d'une table de référence Oracle ?
- [ ] getIntervenantInfos.typeRessource : Le code situation 'MIE' est hardcodé — vient-il d'une table de référence Orac...
- [ ] getIntervenantInfos.techno : Le code situation 'FH' est hardcodé — vient-il d'une table de référence Oracle ?

---

## Points de décision — Comportements non définis
- ⚠️ **Gap de logique**
  - Point de décision — le champ 'intervenantInfosList' est vide. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — strpos('checkVar', 'val') égal à = 0. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — strcmp('checkVar', 'val') égal à = 0. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — strpos('checkVar', 'val') différent de = false. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'ok'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !is_null('intervenantInfos'['TECHNO']) et 'intervenantInfos'['TECHNO'] différent de '' et 'ok'. Quel est le comportement attendu dans le cas contraire ?

## Services tiers non documentés
- ❓ **App\Repository\AstroRepository** — Service tiers non documenté — Le composant 'App\Repository\AstroRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?

---
**Légende :** ✅ Règle confirmée | 🔴 Point d'attention | ⚠️ Gap à arbitrer | ❓ Service à documenter
