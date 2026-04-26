# AiguillageIntervenantController — Zones à valider
Généré le : 2026-04-26 14:32 | 12 flags | 0 insights LLM

## 🔢 Code situation hardcodé — risque désynchronisation
- [ ] **[getIntervenantInfos]** ⬜ non enrichi
  - Fragment : `$ok = ($intervenantInfos['TECHNO'] == 'EVTFIXE');`
  - Question : Le code situation 'EVTFIXE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?
- [ ] **[getIntervenantInfos]** ⬜ non enrichi
  - Fragment : `$ok = ($intervenantInfos['TECHNO'] == 'RS');`
  - Question : Le code situation 'RS' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?
- [ ] **[getIntervenantInfos]** ⬜ non enrichi
  - Fragment : `if ($typeRessource == 'MIE') {`
  - Question : Le code situation 'MIE' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?
- [ ] **[getIntervenantInfos]** ⬜ non enrichi
  - Fragment : `if ($techno == 'FH') {`
  - Question : Le code situation 'FH' est hardcodé — vient-il d'une table de référence Oracle ? Est-il synchronisé avec les enchaînements configurés dans l'interface admin ? Existe-t-il une constante PHP correspondante ?

## ⚠️ Gaps de logique — Comportements non définis
- [ ] **[block_1]** ⬜ non enrichi
  - Fragment : `empty($intervenantInfosList)`
  - Question : Point de décision — le champ 'intervenantInfosList' est vide. Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_3]** ⬜ non enrichi
  - Fragment : `strpos($checkVar, $val) === 0`
  - Question : Point de décision — strpos('checkVar', 'val') égal à = 0. Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_4]** ⬜ non enrichi
  - Fragment : `strcmp($checkVar, $val) === 0`
  - Question : Point de décision — strcmp('checkVar', 'val') égal à = 0. Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_5]** ⬜ non enrichi
  - Fragment : `strpos($checkVar, $val) !== false`
  - Question : Point de décision — strpos('checkVar', 'val') différent de = false. Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_6]** ⬜ non enrichi
  - Fragment : `$ok`
  - Question : Point de décision — 'ok'. Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_7]** ⬜ non enrichi
  - Fragment : `!is_null($intervenantInfos['TECHNO']) && $intervenantInfos['TECHNO'] != '' && $ok`
  - Question : Point de décision — !is_null('intervenantInfos'['TECHNO']) et 'intervenantInfos'['TECHNO'] différent de '' et 'ok'. Quel est le comportement attendu dans le cas contraire ?
- [ ] **[block_11]** ⬜ non enrichi
  - Fragment : `$ok`
  - Question : Point de décision — 'ok'. Quel est le comportement attendu dans le cas contraire ?

## 📦 Services tiers non documentés
- [ ] **[App\Repository\AstroRepository]** ⬜ non enrichi
  - Fragment : `use: App\Repository\AstroRepository`
  - Question : Service tiers non documenté — Le composant 'App\Repository\AstroRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
