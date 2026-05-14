---
description: Workflow complet Rosetta KB — analyse PHP LLM/no-LLM, enrichissement KB, pending PO, sync, stats, export
---

# Skill : Workflow Rosetta complet

Tu es en mode opérateur Rosetta KB. Lis l'argument passé et exécute le workflow correspondant.
Si aucun argument n'est fourni, affiche le menu ci-dessous et attends le choix de l'utilisateur.

---

## MENU (si pas d'argument)

```
Rosetta — Que veux-tu faire ?

  1. analyse      — Lancer l'analyse LLM sur un ou plusieurs fichiers PHP
  2. no-llm       — Triage rapide sans LLM (gratuit)
  3. enrichir     — Ajouter un token au KB (route 1 CLI / route 2 fiche .md)
  4. pending      — Ajouter une question pour le PO
  5. sync         — Synchroniser anchors + importer KB (kb-sync + kb-import)
  6. stats        — Dashboard KB + couverture
  7. lookup       — Chercher un token dans le KB
  8. export       — Exporter le KB en Markdown lisible humain
  9. bugs         — Voir les bugs enrichis non remontés dans les docs
```

Réponds par le numéro ou le mot-clé.

---

## PRÉREQUIS TOUJOURS VRAIS

- Répertoire de travail : `~/projects/rosetta/`
- Python : `.venv/bin/python3`
- Chemin Astro (NixOS local) : `/home/nixos/projects/astro/application/src/`
- Chemin Astro (Windows WSL) : `/mnt/c/wamp/www/Infocentre/astro/application/src/`
- Avant toute analyse sur un fichier Astro : vérifier sync avec `wc -l` des deux versions
- KB path : `$ROSETTA_KB` ou `~/rosetta-data/knowledge_base.yaml`

---

## 1. ANALYSE LLM

Demande à l'utilisateur :
1. Fichier(s) PHP cible (un ou plusieurs chemins)
2. Contexte / label (ex : "US-1234 RetablirCloturer")
3. Options spéciales : `--bug-check` ? `--from-json` ?

Puis construis et exécute :

```bash
cd ~/projects/rosetta && .venv/bin/python3 rosetta_analyze.py \
  <FICHIER(S)> \
  --output-dir ./output \
  --archive \
  --kb-root /home/nixos/projects/astro/.github/kb/ \
  --call-graph-root /home/nixos/projects/astro/application/src/ \
  --contexte "<LABEL>"
```

Après l'analyse, lis le résumé et signale :
- Couverture KB (`📊 Couverture KB : X%`)
- Tokens à enrichir listés dans le résumé
- Bugs détectés si `--bug-check`
- Fichier d'archive créé dans `~/rosetta-memory/audits/`

---

## 2. TRIAGE NO-LLM

Demande le fichier cible. Exécute :

```bash
cd ~/projects/rosetta && .venv/bin/python3 rosetta_analyze.py \
  <FICHIER> \
  --no-llm \
  --output-dir ./output
```

Résultat : inventaire structurel uniquement, 0 coût LLM. Utiliser pour dresser la liste des tokens avant de décider quoi envoyer en LLM.

---

## 3. ENRICHIR LE KB

Demande le token à enrichir et sa sémantique connue.

### Route 1 — CLI direct (sémantique connue, confiance high ou medium)

```bash
cd ~/projects/rosetta && .venv/bin/python3 rosetta_kb.py capture \
  --code <TOKEN> \
  --label "<Label métier>" \
  --domaine <domaine> \
  --notes "<Contexte, format, couplages, cache...>" \
  --lie-a "<AUTRE_TOKEN>" \
  --source "<PO validé / Analyse Rosetta — YYYY-MM-DD>" \
  --confiance <high|medium>
```

Vérifier après : `.venv/bin/python3 rosetta_kb.py lookup --code <TOKEN>`

### Route 2 — Fiche .md dans `.github/kb/{domaine}/` (token PHP ancré)

Crée le fichier `~/projects/astro/.github/kb/<domaine>/<kb_type>_<TOKEN>.md` :

```yaml
---
kb_type: regle          # code | regle | requete | colonne | vue | bug
kb_nom: <TOKEN>
kb_fichier: application/src/Service/<MonService>.php
kb_anchor_method: <maMethode>
kb_anchor_logic: <fragment_pivot>
kb_confiance: medium    # jamais high en automatique
kb_source: "Analyse Rosetta + Samah — <date>"
kb_domaine: <domaine>
kb_migration: <non|partiel|requis>
---
## Label
## Sémantique
## Concepts / Conditions / Constantes
## Trouvé dans
```

Puis importer : `.venv/bin/python3 rosetta_kb.py import ~/projects/astro/.github/kb/`

**Règle confiance** : un script ne monte jamais à `high`. Seul le PO/Samah valide via `rosetta_kb.py validate`.

---

## 4. PENDING PO

Demande : token/sujet, question, priorité, fichier source.

```bash
cd ~/projects/rosetta && .venv/bin/python3 rosetta_kb.py add-pending \
  --code <NOM_QUESTION> \
  --question "<Question détaillée pour le PO>" \
  --priorite <high|medium|low> \
  --fichiers "<application/src/Service/Foo.php:123>" \
  --kb-type <regle|code|colonne|vue|requete> \
  --domaine <domaine>
```

---

## 5. SYNC (anchors + import)

```bash
# 1. Recalcule hash + commits dans les fiches
python3 ~/projects/astro/.github/rosetta/kb_update_anchors.py ~/projects/astro

# 2. Vérifie qu'il n'y a plus de drift
python3 ~/projects/astro/.github/rosetta/kb_drift_check.py ~/projects/astro

# 3. Importe dans knowledge_base.yaml
cd ~/projects/rosetta && .venv/bin/python3 rosetta_kb.py import ~/projects/astro/.github/kb/
```

Équivalent alias : `kb-sync && kb-import`

---

## 6. STATS

```bash
cd ~/projects/rosetta && .venv/bin/python3 rosetta_kb.py stats
```

Lis la sortie et résume :
- Nombre d'entrées par niveau de confiance (high / medium / inferred)
- Nombre de pending par priorité
- Couverture globale

---

## 7. LOOKUP

Demande le token à chercher.

```bash
cd ~/projects/rosetta && .venv/bin/python3 rosetta_kb.py lookup --code <TOKEN>
```

Si non trouvé → propose de créer une entrée (route 1 ou 2) ou un pending PO.

---

## 8. EXPORT HUMAN

```bash
cd ~/projects/rosetta && .venv/bin/python3 export_human.py \
  --kb ~/rosetta-data/knowledge_base.yaml \
  --output ~/rosetta-data/export_human_<date>.md
```

Le fichier généré est lisible en réunion PO. Ne pas pousser sur le repo — données corporate.

---

## 9. BUGS

Vérifie pourquoi les entrées `kb_type: bug` n'apparaissent pas dans les docs générés :

```bash
cd ~/projects/rosetta
grep -r "kb_type: bug" ~/projects/astro/.github/kb/ | head -20
.venv/bin/python3 rosetta_kb.py lookup --code <BUG_TOKEN>
```

Statut connu : `kb_type: bug` est importé mais pas encore injecté dans le contexte KB LLM ni dans les documents générés. Bloquant pour la démo.

---

## RÈGLES TOUJOURS ACTIVES

1. Jamais de données ASO en clair dans le code pushé — exemples fictifs uniquement.
2. Le KB reste local — jamais pushé vers un repo externe.
3. `confiance: high` = humain uniquement. Les scripts restent à `medium` max.
4. Si un fichier PHP > 32K : le chunking par méthode est automatique dans `bug_enricher.py`.
5. Si le crédit LLM s'épuise en cours d'analyse : relancer l'analyse complète (pas `--retry-failed`).
6. Vérifier toujours le sync NixOS ↔ Windows avant d'analyser un fichier Astro.
