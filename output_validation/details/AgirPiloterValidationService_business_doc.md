# AgirPiloterValidationController — Règles Métier
Extrait le : 2026-04-26 | Confiance extraction : 0.6000000000000001

## Méthode : validateAgirPiloterForm()

### Questions ouvertes pour arbitrage
- [ ] validateAgirPiloterForm.regles : Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ?

---

## Points de décision — Comportements non définis
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('DATE_RETABLISSEMENT_DEMANDE_INTERVENTION', 'regles') et 'regles'['DATE_RETABLISSEMENT_DEMANDE_INTERVENTION']["OBLIGATOIRE"] égal à = '1'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !'this'->notEmpty('dateRetab'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'dateRetab' différent de = ''. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !'this'->isDate('dateRetab', "d/m/Y H:i"). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('DATE_COURS_EDS_DEMANDE_INTERVENTION', 'regles') et 'regles'['DATE_COURS_EDS_DEMANDE_INTERVENTION']["OBLIGATOIRE"] égal à = '1'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !'this'->notEmpty('actionCoursEds'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'actionCoursEds' différent de = ''. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !'this'->isDate('actionCoursEds', "d/m/Y H:i"). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('COMMENTAIRE_DEMANDE_INTERVENTION', 'regles') et 'regles'['COMMENTAIRE_DEMANDE_INTERVENTION']["OBLIGATOIRE"] égal à = '1'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !'this'->notEmpty('commentaire'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('ACTION_EN_COURS_EDS', 'regles') et 'regles'['ACTION_EN_COURS_EDS']["OBLIGATOIRE"] égal à = '1'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — key_exists('NIVEAU_URGENCE', 'regles') et 'regles'['NIVEAU_URGENCE']["OBLIGATOIRE"] égal à = '1'. Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !'result'. Quel est le comportement attendu dans le cas contraire ?

---
**Légende :** ✅ Règle confirmée | 🔴 Point d'attention | ⚠️ Gap à arbitrer | ❓ Service à documenter
