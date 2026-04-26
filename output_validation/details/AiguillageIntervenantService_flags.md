# AiguillageIntervenantController — Zones à valider
Généré le : 2026-04-26 10:08 | 6 flags | 0 insights LLM

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
- [ ] **[block_11]** ⬜ non enrichi
  - Fragment : `$ok`
  - Question : Point de décision — 'ok'. Quel est le comportement attendu dans le cas contraire ?

## 📦 Services tiers non documentés
- [ ] **[App\Repository\AstroRepository]** ⬜ non enrichi
  - Fragment : `use: App\Repository\AstroRepository`
  - Question : Service tiers non documenté — Le composant 'App\Repository\AstroRepository' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
