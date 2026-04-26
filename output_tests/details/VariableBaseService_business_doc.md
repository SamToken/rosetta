# VariableBaseServiceController — Règles Métier
Extrait le : 2026-04-26 | Confiance extraction : 0.29999999999999993

## Points de décision — Comportements non définis
- ⚠️ **Gap de logique**
  - Point de décision — is_null('this'->findAndGet). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('this'->findAndGet['installed_resource']->Parameters, 'Parameter'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — !is_null('res'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — property_exists('this'->findAndGet['installed_resource']->Attributes, 'Attribute'). Quel est le comportement attendu dans le cas contraire ?
- ⚠️ **Gap de logique**
  - Point de décision — 'this'->id1. Quel est le comportement attendu dans le cas contraire ?

## Services tiers non documentés
- ❓ **App\Tools\OceaneTools** — Service tiers non documenté — Le composant 'App\Tools\OceaneTools' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?
- ❓ **Oft\Mvc\Application** — Service tiers non documenté — Le composant 'Oft\Mvc\Application' est utilisé dans ce périmètre sans équivalent identifié dans la cible. Quel est son rôle fonctionnel et quelles données échange-t-il avec le système ?

---
**Légende :** ✅ Règle confirmée | 🔴 Point d'attention | ⚠️ Gap à arbitrer | ❓ Service à documenter
