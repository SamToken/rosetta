# AgirPiloterValidationController — Zones à valider
Généré le : 2026-04-26 10:07 | 16 flags | 0 insights LLM

## 🔢 Code situation hardcodé — risque désynchronisation
- [ ] **[validateAgirPiloterForm]** ⬜ non enrichi
  - Fragment : `$regles) && $regles['DATE_RETABLISSEMENT_DEMANDE_INTERVENTION']["OBLIGATOIRE"] === '1') {`
  - Question : Le code situation '1' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

## ⚠️ Gaps de logique — Comportements non définis
- [ ] **[block_1]** ⬜ non enrichi
  - Fragment : `key_exists('DATE_RETABLISSEMENT_DEMANDE_INTERVENTION', $regles) && $regles['DATE_RETABLISSEMENT_DEMA`
  - Question : Point de décision — key_exists('DATE_RETABLISSEMENT_DEMANDE_INTERVENTION', 'regles') et 'regles'['DATE_RETABLISSEMENT_DEMANDE_INTERVENTION']["OBLIGATOIRE"] égal à = '1'. Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_2]** ⬜ non enrichi
  - Fragment : `!$this->notEmpty($dateRetab)`
  - Question : Point de décision — !'this'->notEmpty('dateRetab'). Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_3]** ⬜ non enrichi
  - Fragment : `$dateRetab !== ''`
  - Question : Point de décision — 'dateRetab' différent de = ''. Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_4]** ⬜ non enrichi
  - Fragment : `!$this->isDate($dateRetab, "d/m/Y H:i")`
  - Question : Point de décision — !'this'->isDate('dateRetab', "d/m/Y H:i"). Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_5]** ⬜ non enrichi
  - Fragment : `key_exists('DATE_COURS_EDS_DEMANDE_INTERVENTION', $regles) && $regles['DATE_COURS_EDS_DEMANDE_INTERV`
  - Question : Point de décision — key_exists('DATE_COURS_EDS_DEMANDE_INTERVENTION', 'regles') et 'regles'['DATE_COURS_EDS_DEMANDE_INTERVENTION']["OBLIGATOIRE"] égal à = '1'. Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_6]** ⬜ non enrichi
  - Fragment : `!$this->notEmpty($actionCoursEds)`
  - Question : Point de décision — !'this'->notEmpty('actionCoursEds'). Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_7]** ⬜ non enrichi
  - Fragment : `$actionCoursEds !== ''`
  - Question : Point de décision — 'actionCoursEds' différent de = ''. Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_8]** ⬜ non enrichi
  - Fragment : `!$this->isDate($actionCoursEds, "d/m/Y H:i")`
  - Question : Point de décision — !'this'->isDate('actionCoursEds', "d/m/Y H:i"). Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_9]** ⬜ non enrichi
  - Fragment : `key_exists('COMMENTAIRE_DEMANDE_INTERVENTION', $regles) && $regles['COMMENTAIRE_DEMANDE_INTERVENTION`
  - Question : Point de décision — key_exists('COMMENTAIRE_DEMANDE_INTERVENTION', 'regles') et 'regles'['COMMENTAIRE_DEMANDE_INTERVENTION']["OBLIGATOIRE"] égal à = '1'. Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_10]** ⬜ non enrichi
  - Fragment : `!$this->notEmpty($commentaire)`
  - Question : Point de décision — !'this'->notEmpty('commentaire'). Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_11]** ⬜ non enrichi
  - Fragment : `key_exists('ACTION_EN_COURS_EDS', $regles) && $regles['ACTION_EN_COURS_EDS']["OBLIGATOIRE"] === '1'`
  - Question : Point de décision — key_exists('ACTION_EN_COURS_EDS', 'regles') et 'regles'['ACTION_EN_COURS_EDS']["OBLIGATOIRE"] égal à = '1'. Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_12]** ⬜ non enrichi
  - Fragment : `!$this->notEmpty($actionCoursEds)`
  - Question : Point de décision — !'this'->notEmpty('actionCoursEds'). Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_13]** ⬜ non enrichi
  - Fragment : `key_exists('NIVEAU_URGENCE', $regles) && $regles['NIVEAU_URGENCE']["OBLIGATOIRE"] === '1'`
  - Question : Point de décision — key_exists('NIVEAU_URGENCE', 'regles') et 'regles'['NIVEAU_URGENCE']["OBLIGATOIRE"] égal à = '1'. Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_14]** ⬜ non enrichi
  - Fragment : `!$this->notEmpty($actionCoursEds)`
  - Question : Point de décision — !'this'->notEmpty('actionCoursEds'). Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_15]** ⬜ non enrichi
  - Fragment : `!$result`
  - Question : Point de décision — !'result'. Quel est le comportement attendu dans le cas contraire ?
