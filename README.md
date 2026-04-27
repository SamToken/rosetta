# Rosetta — Knowledge Base & Anti-Drift Pipeline

Outil privé de cartographie des règles métier du projet ASTRO (legacy PHP 7.3).

## Architecture

```
~/repos/rosetta/  (privé — ton repo)        ~/repos/astro/  (corporate — read-only)
─────────────────────────────────────        ──────────────────────────────────────
config.yaml       ← pointe vers astro       .github/copilot-skills/  ← versionné
kb/                                            (rien d'autre de Rosetta ici)
  orchestra/      ← 5 fiches
  airele/         ← 8 fiches
  enrichissement-alarmes/ ← 6 fiches
scripts/
  kb_drift_check.py
  kb_update_anchors.py
  install_hook.sh
audits/           ← rapports partagés en réunion
```

**Principe** : Rosetta ne vit JAMAIS dans le repo corporate.
Les scripts lisent le code source Astro via `config.yaml → source_repo`.

---

## Setup NixOS (une seule fois)

```bash
# 1. Cloner Astro (si pas déjà fait)
git clone <astro_corporate_url> ~/repos/astro

# 2. Installer le hook (dans .git/hooks d'Astro, pas versionné)
bash ~/repos/rosetta/scripts/install_hook.sh

# 3. Tester
python3 ~/repos/rosetta/scripts/kb_drift_check.py
```

Prérequis : `python3`, `git` — aucune dépendance pip.

---

## Usage quotidien

### Vérifier les drifts
```bash
cd ~/repos/rosetta
python3 scripts/kb_drift_check.py
```

### Mettre à jour les ancres (hash, commit)
```bash
python3 scripts/kb_update_anchors.py              # dry-run
python3 scripts/kb_update_anchors.py --apply       # applique
python3 scripts/kb_update_anchors.py --apply --file kb/airele/regle_FALLBACK_OCEANE_GISEMENT.md
```

### Workflow post-MR
```
1. Collègue merge une MR sur Astro
2. Sur NixOS : cd ~/repos/astro && git pull
3. cd ~/repos/rosetta && python3 scripts/kb_drift_check.py
4. Si drift → python3 scripts/kb_update_anchors.py --apply
5. Si anchor_method a changé → mettre à jour la fiche manuellement
6. git add kb/ && git commit -m "KB: sync post-MR"
```

---

## config.yaml

| Champ | Rôle |
|-------|------|
| `source_repo` | Chemin vers le clone Astro corporate |
| `kb_dir` | Dossier des fiches KB (dans ce repo) |
| `drift.max_age_days` | Warning si fiche plus ancienne que N jours |
| `drift.block_on_drift` | Le hook bloque le commit si `true` |
| `drift.allow_simulated_hash` | Accepter les `sha256:simul*` |
| `domains.*` | Mapping domaine → fichiers PHP source |

---

## Ce qu'on partage / ce qu'on garde

| Élément | Partagé ? | Comment |
|---------|-----------|---------|
| Audits (rapports) | ✅ Oui | PDF/MD en réunion |
| Fiches KB | ❌ Non | Restent dans ce repo privé |
| Scripts Rosetta | ❌ Non | Propriété personnelle |
| Skills Copilot | ✅ Oui | Dans `.github/copilot-skills/` d'Astro |

---

*Rosetta — outil d'audit statique PHP · Samah Toutouh · 2026*
