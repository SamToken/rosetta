# ROSETTA KB — Prompt Claude Code

> **Projet** : Rosetta Knowledge Base — Couche sémantique pour migration ASO (Zend→Symfony)
> **Auteur** : Samah — Senior PHP Dev, Sofrecom (Orange)
> **Stack** : Python 3 / PyYAML / NixOS (Rosetta) + Windows (Astro/VS Code/Copilot)
> **Contrainte souveraineté** : Aucune donnée ASO ne sort vers un repo externe. Rosetta (perso) et Astro (corporate) sont deux dépôts séparés. Le KB reste local uniquement.

---

## 1. CONTEXTE

Rosetta est un analyseur AST statique pur (nikic/php-parser → JSON/Markdown) pour le legacy PHP ASO — un système de ticketing télécom 24/7 multidomaine. Le KB est la couche sémantique qui transforme l'inventaire structurel de Rosetta en **carte de connaissance métier exploitable**.

### Problème résolu

Dans ASO, la logique métier est enterrée dans trois couches :
1. **Constantes/codes PHP** — magic strings (`TP2`, `ST_OUV`) sans documentation
2. **Colonnes Oracle obscures** — noms cryptiques (`C_TYP_FLX`, `DT_ECH_CALC`, `N_SQ_TRT`)
3. **SQL complexe** — requêtes de 100+ lignes, vues imbriquées, constantes magiques dans les WHERE

Sans KB, chaque token ambigu coûte 30 min de reverse engineering ou un appel LLM. Avec KB, c'est un lookup instantané à 0 token.

### Architecture fichiers (séparation stricte)

```
~/projects/rosetta/              # Repo perso GitHub — OUTILS uniquement
├── rosetta_kb.py                # CLI KB v2
├── kb_import.py                 # Import fiches KB (.github/kb/ ou docs-kb/) → knowledge_base.yaml
├── llm_enricher.py              # Pipeline enrichissement AST → KB
├── aliases.sh                   # Aliases shell (kb-check, kb-sync, kb-import, kb-stats)
├── Makefile                     # Targets : kb-check, kb-sync, kb-import, kb-full
├── CLAUDE.md                    # CE FICHIER
└── .gitignore

~/projects/astro/                # Repo corporate Sofrecom — CODE ASO
├── application/src/             # Code PHP Zend/Symfony
└── .github/
    ├── rosetta/                 # Scripts anti-drift (appelés par Rosetta via aliases)
    │   ├── kb_drift_check.py    # Vérifie cohérence fiches KB ↔ source (hook pre-commit)
    │   ├── kb_update_anchors.py # Recalcule hash/commit dans frontmatter des fiches
    │   ├── install_hook.sh      # Installe le pre-commit hook dans Astro/.git/hooks/
    │   └── README.md
    └── kb/                      # Fiches KB par domaine (corporate — jamais pushées ailleurs)
        └── orchestra/           # Domaine : diagnostic Orchestra
            ├── code_ETX_CRITICALITY_STATUS.md
            ├── regle_CACHE_DIAGNOSIS_PRODUIT.md
            ├── regle_GUARD_DIAGNOSTIC_EN_COURS.md
            ├── regle_GUARD_EMPTY_AVANT_APPEL2.md
            └── requete_RQ_ORCHESTRA_ETX.md

~/rosetta-data/                  # Dossier LOCAL, hors tout repo
├── knowledge_base.yaml          # Source de vérité KB (données corporate)
└── docs-kb/                     # Docs générées par personas Copilot (format Oracle/SQL)
    ├── colonne_C_TYP_FLX.md
    ├── vue_V_TICKET_SLA.md
    └── requete_RQ_SLA_BREACH.md
```

Variable d'environnement : `ROSETTA_KB=~/rosetta-data/knowledge_base.yaml`

---

## 2. KNOWLEDGE BASE — SCHÉMA YAML

Le fichier `knowledge_base.yaml` a 6 sections :

```yaml
meta:
  projet: ASO
  version: "2.0.0"
  last_updated: "2025-01-14"
  maintainer: "Samah"

codes:           # Constantes/magic strings PHP
regles:          # Règles métier (SLA, escalades, seuils)
schema:          # Tables/champs clés Oracle
sql_artifacts:   # ← Section SQL complète
  colonnes:      #   Colonnes Oracle obscures
  vues:          #   Vues Oracle (jointures, pièges, migration)
  requetes:      #   Requêtes nommées 100+ lignes
pending_validation:  # File d'attente questions PO
```

### 2.1 Entrée `codes` (constantes métier)

```yaml
codes:
  TP2:
    label: "Intervention Prioritaire Orange"
    contextes:
      - champ: ticket_type
        semantique: "Déclenchement SLA niveau 2"
        table: T_TICKET
    domaine: ticketing
    source: "PO validé — réunion 2025-01-14"
    confiance: high        # high | medium | inferred
    lié_à: [SLA_P2]
    notes: ~
```

### 2.2 Entrée `sql_artifacts.colonnes`

```yaml
sql_artifacts:
  colonnes:
    C_TYP_FLX:
      label: "Type de Flux"
      table: T_FLUX_INTERCO
      type_oracle: VARCHAR2(1)
      semantique: "Discriminant principal de routage flux"
      valeurs:
        "I": "Flux Entrant"
        "O": "Flux Sortant"
        "T": "Transit inter-domaines"
      distinctions:
        C_TYP_FLX_BRUT: "Valeur brute sans calcul"
      trouvé_dans: ["flux_handler.php:L89", "V_FLUX_ACTIF"]
      migration_note: "Remplacer par Enum FluxType en Symfony"
      source: "PO validé — 2025-01-14"
      confiance: high
```

### 2.3 Entrée `sql_artifacts.vues`

```yaml
    vues:
      V_TICKET_SLA:
        label: "Vue Calcul SLA en cours"
        semantique: "Calcule en temps réel le délai restant avant breach"
        tables_source: [V_TICKET_ACTIF, T_SLA_MATRIX, T_CALENDRIER_OUVRE]
        filtre_principal: "statut_code NOT IN ('ST_CLO','ST_ANN')"
        jointures:
          - type: INNER JOIN
            table: T_SLA_MATRIX
            condition: "ticket_type = sla_type AND domaine_code = sla_domaine"
            raison: "Ticket sans SLA = anomalie bloquante"
          - type: LEFT JOIN
            table: T_CALENDRIER_OUVRE
            condition: "TRUNC(DT_ECH_CALC) = cal_date"
            raison: "LEFT JOIN intentionnel : si jour férié absent, calcul brut"
        piège_connu: "LEFT JOIN silencieux si T_CALENDRIER_OUVRE non à jour"
        utilisée_par: [V_RAPPORT_SLA, sla_dashboard.php]
        migration_note: "Refactoriser en SlaCalculatorService Symfony"
        confiance: high
```

### 2.4 Entrée `sql_artifacts.requetes`

```yaml
    requetes:
      RQ_SLA_BREACH_WEEKEND:
        label: "Calcul breach SLA week-end exclu"
        fichier_source: "reports/sla_breach_report.php"
        lignes: "L145-L287"
        semantique: "Calcule les breaches SLA en excluant heures non ouvrées"
        tables_impliquées: [V_TICKET_SLA, T_CALENDRIER_OUVRE, T_SLA_MATRIX]
        constantes_magiques:
          "8":  "Heure début journée ouvrable"
          "18": "Heure fin journée ouvrable"
          "6":  "Seuil alerte SLA P1 en heures ouvrées"
        concepts_métier:
          - "SLA effectif (heures ouvrées seulement)"
          - "Seuil breach paramétré par domaine"
        performance:
          index_critiques:
            - "IDX_TICKET_DT_ECH sur T_TICKET(DT_ECH_CALC)"
          risque_migration: "Sans index : 10x plus lent sur 500K tickets"
        migration_note: "SlaBreachService::computeEffectiveBreaches(DateRange)"
        confiance: high
```

### 2.5 Niveaux de confiance

| Niveau     | Signification                          | Comportement llm_enricher       |
|------------|----------------------------------------|---------------------------------|
| `high`     | Validé PO, exploitable directement     | Enrichissement direct, 0 LLM   |
| `medium`   | Inféré ou partiellement validé         | Enrichir + flag "à valider PO" |
| `inferred` | Déduit par Rosetta/Copilot, non validé | Utiliser avec prudence + pending|

---

## 3. CLI `rosetta_kb.py` — COMMANDES

### Commandes métier

```bash
# Capturer un code validé PO
python rosetta_kb.py capture \
  --code TP2 --label "Intervention Prioritaire Orange" \
  --champ ticket_type --table T_TICKET \
  --source "PO validé — 2025-01-14" --confiance high

# Rechercher dans TOUTES les sections (codes, règles, colonnes, vues, requêtes)
python rosetta_kb.py lookup --code TP2
python rosetta_kb.py lookup --code C_TYP_FLX --json   # sortie JSON pour scripts

# Gérer la file PO
python rosetta_kb.py pending --priorite high
python rosetta_kb.py validate --id PV-001 --label "SLA 24h ouvrées"
python rosetta_kb.py add-pending --code TP3 \
  --question "TP3 est-il standard 24h ou sous-catégories ?" \
  --fichiers "ticket_handler.php:L247" --priorite medium
```

### Commandes SQL Oracle

```bash
# Colonne obscure
python rosetta_kb.py capture-colonne \
  --nom C_TYP_FLX --table T_FLUX_INTERCO \
  --label "Type de Flux" --type "VARCHAR2(1)" \
  --valeurs "I=Flux Entrant,O=Flux Sortant,T=Transit" \
  --distinctions "C_TYP_FLX_BRUT=Valeur brute non calculée" \
  --migration "Remplacer par Enum FluxType en Symfony"

# Vue Oracle avec pièges
python rosetta_kb.py capture-vue \
  --nom V_TICKET_SLA --label "Vue Calcul SLA en cours" \
  --tables "V_TICKET_ACTIF,T_SLA_MATRIX,T_CALENDRIER_OUVRE" \
  --piege "LEFT JOIN silencieux si calendrier non à jour" \
  --migration "Refactoriser en SlaCalculatorService"

# Requête complexe 100+ lignes
python rosetta_kb.py capture-requete \
  --nom RQ_SLA_BREACH_WEEKEND \
  --label "Calcul breach SLA week-end exclu" \
  --fichier "reports/sla_breach_report.php" --lignes "L145-L287" \
  --constantes "8=Heure début,18=Heure fin,6=Seuil P1" \
  --concepts "SLA effectif heures ouvrées,Exclusion fériés" \
  --index "IDX_TICKET_DT_ECH sur T_TICKET(DT_ECH_CALC)" \
  --risque "Sans index : 10x plus lent sur 500K tickets" \
  --migration "SlaBreachService::computeEffectiveBreaches()"
```

### Utilitaires

```bash
python rosetta_kb.py stats                         # dashboard KB
python rosetta_kb.py search --texte "calendrier"   # recherche textuelle
python rosetta_kb.py export --output rapport.md    # export Markdown
```

### API Python pour llm_enricher.py

```python
from rosetta_kb import lookup_for_enricher

result = lookup_for_enricher("C_TYP_FLX")

if result["found"] and result["confiance"] == "high":
    # 0 token LLM — enrichissement direct
    label   = result["label"]
    valeurs = result.get("valeurs", {})
elif result["found"] and result["confiance"] == "medium":
    # enrichir mais flagger pending PO
    pass
else:
    # escalader au LLM → puis add-pending pour validation PO
    pass
```

---

## 4. PIPELINE COPILOT → KB (alimentation automatisée)

### 4.1 Format de sortie à demander aux personas Copilot

Chaque persona doit générer un fichier Markdown avec **frontmatter YAML + sections conventionnelles**. Un fichier = une entrée KB.

````markdown
---
kb_type: colonne
kb_nom: C_TYP_FLX
kb_table: T_FLUX_INTERCO
kb_type_oracle: VARCHAR2(1)
kb_confiance: medium
kb_source: "Persona API — généré 2025-01-20"
kb_domaine: interco
kb_migration: "Remplacer par Enum FluxType en Symfony"
---

## Label
Type de Flux

## Semantique
Discriminant principal pour router un flux vers la cellule compétente.
Utilisé dans 23 requêtes identifiées.

## Valeurs
| Valeur | Signification          |
|--------|------------------------|
| I      | Flux Entrant (Inbound) |
| O      | Flux Sortant (Outbound)|
| T      | Transit inter-domaines |

## Distinctions
| Colonne        | Différence                    |
|----------------|-------------------------------|
| C_TYP_FLX_BRUT | Valeur brute sans calcul     |

## Trouvé dans
- flux_handler.php:L89
- V_FLUX_ACTIF (vue Oracle)

## Notes
Aucune.
````

**Types supportés pour `kb_type`** :

| kb_type   | Section KB cible          | Champs frontmatter requis            |
|-----------|---------------------------|--------------------------------------|
| `code`    | `codes`                   | kb_nom, kb_domaine                   |
| `regle`   | `regles`                  | kb_nom                               |
| `colonne` | `sql_artifacts.colonnes`  | kb_nom, kb_table                     |
| `vue`     | `sql_artifacts.vues`      | kb_nom                               |
| `requete` | `sql_artifacts.requetes`  | kb_nom, kb_fichier, kb_lignes        |

**Nommage fichier** : `{kb_type}_{kb_nom}.md` → `colonne_C_TYP_FLX.md`

### 4.2 Script `kb_import.py`

```
Entrée  : ~/rosetta-data/docs-kb/*.md  (docs Copilot Oracle/SQL)
          — OU —
          ~/projects/astro/.github/kb/ (fiches KB Astro avec anchors drift)
Sortie  : ~/rosetta-data/knowledge_base.yaml (enrichi)
Librairie : python-frontmatter + pyyaml
```

**Comportement attendu** :

1. Parcourir `docs-kb/` récursivement pour les `.md` avec frontmatter `kb_type`
2. Parser le frontmatter YAML et les sections `##`
3. Router vers la bonne section KB selon `kb_type`
4. **Règle de confiance** : tout import Copilot entre en `confiance: medium` max, même si le frontmatter dit `high` — seul le PO peut monter en `high` via `rosetta_kb.py validate`
5. **Règle de collision** : si l'entrée existe déjà en KB avec confiance `high`, ne PAS écraser. Logger un warning. Si elle existe en `medium` ou `inferred`, mettre à jour.
6. Produire un résumé d'import : `N ajoutées, N mises à jour, N ignorées (high existant), N erreurs`

**Parseurs de sections** :

- `## Valeurs` → parser tableau Markdown `| Valeur | Signification |` → dict
- `## Distinctions` → parser tableau → dict
- `## Trouvé dans` → parser liste `- fichier:ligne` → list
- `## Label` / `## Semantique` / `## Notes` → texte brut
- `## Conditions` → parser liste → list (pour les règles)
- `## Concepts` → parser liste → list (pour les requêtes)
- `## Constantes` → parser tableau `| Valeur | Signification |` → dict

### 4.3 Instruction à injecter dans les personas Copilot

```
=== INSTRUCTION KB ROSETTA ===

Quand tu documentes un élément technique ASO (colonne Oracle, vue SQL,
code métier, règle, requête complexe), génère TOUJOURS un fichier
Markdown séparé avec ce format :

1. Frontmatter YAML obligatoire :
   - kb_type: colonne | vue | requete | code | regle
   - kb_nom: nom technique exact (ex: C_TYP_FLX, V_TICKET_SLA)
   - kb_table: table Oracle propriétaire (si colonne)
   - kb_confiance: toujours "medium" (la validation PO se fait ailleurs)
   - kb_source: "Persona {NomPersona} — généré {date}"
   - kb_domaine: domaine ASO concerné
   - kb_migration: note de refactorisation Symfony (si applicable)

2. Sections ## obligatoires : Label, Semantique
3. Sections ## optionnelles : Valeurs, Distinctions, Trouvé dans,
   Conditions, Constantes, Concepts, Notes

4. Un fichier par élément. Nommage : {kb_type}_{kb_nom}.md
5. Les tableaux de valeurs utilisent le format Markdown standard.
6. Ne jamais mettre confiance "high" — seul le PO peut valider.

=== FIN INSTRUCTION ===
```

### 4.4 Workflow quotidien

```bash
# 1. Sur Windows (VS Code + Copilot) — pendant le travail sur Astro
#    Copilot génère des docs KB → sauvées dans ~/rosetta-data/docs-kb/
#    ou dans ~/projects/astro/.github/kb/{domaine}/

# 2a. Import depuis docs-kb/ (fiches Oracle/SQL)
python3 ~/projects/rosetta/kb_import.py ~/rosetta-data/docs-kb/
# Résumé : 12 ajoutées, 3 mises à jour, 1 ignorée (high), 0 erreurs

# 2b. Import depuis Astro .github/kb/ (fiches PHP avec anchors drift)
python3 ~/projects/rosetta/kb_import.py ~/projects/astro/.github/kb/
# ou via alias :
kb-import

# 3. Vérification
python3 ~/projects/rosetta/rosetta_kb.py stats
# [MEDIUM] 28 entrées  ← Copilot/Astro
# [HIGH]   19 entrées  ← validé PO

# 4. Préparation session PO
python3 ~/projects/rosetta/rosetta_kb.py pending
python3 ~/projects/rosetta/rosetta_kb.py search --texte "SLA"

# 5. Après la session PO
python3 ~/projects/rosetta/rosetta_kb.py validate --id PV-014 --label "..." --source "PO validé"
```

---

## 5. PIPELINE llm_enricher.py — LOGIQUE DE DÉCISION

```
Rosetta analyse le PHP (AST)
        │
        ▼
  Token inconnu détecté
  (constante, colonne, magic string)
        │
        ▼
  lookup_for_enricher(token)
        │
        ├── found + high    → enrichissement direct, 0 token LLM
        ├── found + medium  → enrichissement + flag pending PO
        ├── found + inferred→ enrichissement prudent + pending PO priorité high
        └── not found       → LLM génère :
                               1. Suggestion sémantique
                               2. Question structurée pour le PO
                               3. Auto-ajout en pending via add-pending
                               4. Sauvegarde en KB avec confiance "inferred"
```

---

## 6. SCRIPTS `.github/rosetta/` — ANTI-DRIFT

Ces scripts vivent dans le repo Astro mais sont appelés depuis Rosetta via `aliases.sh` / `Makefile`. Ils ne touchent que `.github/` — zéro écriture dans le code source ASO.

### `kb_drift_check.py`

Vérifie la cohérence entre chaque fiche KB et son fichier source. Pour chaque fiche :
- Lit `kb_fichier` dans le frontmatter → vérifie que le fichier existe dans Astro
- Si `kb_anchor_method` présent → vérifie que cette chaîne existe dans le fichier source
- Si `kb_anchor_logic` présent → vérifie que ce fragment de code existe dans le fichier source
- Si `kb_source_file_hash` présent (format `sha256:<hex>`) → compare avec le hash actuel du fichier

Statuts de sortie :
- `[OK]` — fiche synchronisée
- `[DRIFT]` — anchor ou hash obsolète (le code a changé sans que la fiche soit mise à jour)
- `[MISSING]` — `kb_fichier` introuvable dans Astro

Exit code 1 si au moins un drift — **bloque `git commit`** via le hook pre-commit.

### `kb_update_anchors.py`

Recalcule et réécrit dans le frontmatter de chaque fiche :
- `kb_source_commit` — SHA du dernier commit touchant `kb_fichier`
- `kb_source_commit_date` — date ISO de ce commit
- `kb_source_file_hash` — `sha256:<hex>` du fichier actuel
- `kb_anchor_method_found` — `true`/`false` selon présence dans le fichier

N'écrit que dans `.github/kb/`. À lancer après toute modification du code source référencé.

### `install_hook.sh`

Installe dans `~/projects/astro/.git/hooks/pre-commit` un hook qui appelle `kb_drift_check.py` avant chaque commit. Un seul `bash .github/rosetta/install_hook.sh` depuis Astro.

### Format frontmatter des fiches Astro (`.github/kb/{domaine}/*.md`)

Différent des fiches Copilot (Oracle/SQL) — les fiches Astro ancrent le PHP source :

```yaml
---
kb_type: requete|regle|code
kb_nom: NOM_COURT
kb_fichier: application/src/Service/OrchestraService.php  # relatif à Astro root
kb_lignes: "108-138"
kb_source_commit: <git SHA>
kb_source_commit_date: <date ISO>
kb_anchor_method: testProduitEtx       # doit exister dans kb_fichier
kb_anchor_logic: getEtxStatus          # fragment de code pivot (doit exister)
kb_anchor_method_found: true|false     # mis à jour par kb_update_anchors.py
kb_source_file_hash: sha256:<hex>      # mis à jour par kb_update_anchors.py
kb_confiance: medium                   # jamais high en automatique
kb_source: orchestra
kb_domaine: diagnostic
kb_migration: non|partiel|requis
---
```

---

## 7. PIPELINE ANTI-DRIFT — WORKFLOW EXACT

```bash
# ── Après modification du code PHP dans Astro ──────────────────────────────

# 1. Mettre à jour les anchors (recalcule hash + commits dans les fiches)
kb-sync
# = python3 ~/projects/astro/.github/rosetta/kb_update_anchors.py ~/projects/astro
# Sortie : [UPDATED] orchestra/regle_CACHE_DIAGNOSIS_PRODUIT.md (kb_source_file_hash,...)

# 2. Vérifier qu'il n'y a plus de drift
kb-check
# = python3 ~/projects/astro/.github/rosetta/kb_drift_check.py ~/projects/astro
# Sortie attendue : [PASS] Toutes les fiches KB sont synchronisées.

# 3. Importer dans le KB local (knowledge_base.yaml)
kb-import
# = python3 ~/projects/rosetta/kb_import.py ~/projects/astro/.github/kb/
# Sortie : 5 ajoutée(s), 0 mise(s) à jour, 0 ignorée(s), 0 erreur(s)

# 4. Vérifier le KB
kb-stats
# = python3 ~/projects/rosetta/rosetta_kb.py stats

# ── Workflow complet en une commande ───────────────────────────────────────
cd ~/projects/rosetta && make kb-full
# = kb-sync + kb-import + stats

# ── Installation du hook pre-commit (une seule fois) ──────────────────────
cd ~/projects/astro && bash .github/rosetta/install_hook.sh
```

**Règle anti-drift** : si tu modifies `OrchestraService.php`, le hook bloque le commit si `kb_source_file_hash` est obsolète. Lance `kb-sync` puis recommite.

---

## 8. RÈGLES POUR CLAUDE CODE

Quand tu travailles sur ce projet :

1. **Ne jamais hardcoder de données ASO** dans le code pushé. Les exemples dans les docstrings et tests utilisent des données fictives.
2. **Le KB est toujours local** — référencé par `$ROSETTA_KB` ou argument `--kb-path`.
3. **Le frontmatter est le contrat** entre Copilot et Rosetta. Si tu modifies le schéma, mets à jour l'instruction persona (section 4.3).
4. **Confiance descendante uniquement automatisée** : un script peut baisser la confiance, jamais la monter à `high`. Seul un humain (PO/Samah) monte en `high`.
5. **Compatibilité arrière** : `kb_import.py` doit ignorer silencieusement les champs frontmatter inconnus et les sections `##` non reconnues.
6. **0 dépendance lourde** : PyYAML + python-frontmatter max. Pas de framework, pas de base de données.
7. **Tests** : chaque nouvelle fonctionnalité a un test avec un KB temporaire en `/tmp/`.

---

## 9. LANCER ROSETTA — RÉFÉRENCE RAPIDE

### Mode LLM enrichissement (défaut)

```bash
cd ~/projects/rosetta

# Fichier unique
.venv/bin/python3 rosetta_analyze.py \
  /chemin/vers/MonService.php \
  --output-dir ./output \
  --archive \
  --kb-root ~/projects/astro/.github/kb/ \
  --call-graph-root ~/projects/astro/application/src/

# Plusieurs fichiers (multi-fichiers)
.venv/bin/python3 rosetta_analyze.py \
  /chemin/A.php /chemin/B.php \
  --output-dir ./output \
  --archive \
  --kb-root ~/projects/astro/.github/kb/ \
  --call-graph-root ~/projects/astro/application/src/

# Répertoire complet
.venv/bin/python3 rosetta_analyze.py \
  ~/projects/astro/application/src/Service/ \
  --output-dir ./output \
  --archive \
  --kb-root ~/projects/astro/.github/kb/ \
  --call-graph-root ~/projects/astro/application/src/
```

### Mode no-LLM (déterministe, gratuit)

```bash
.venv/bin/python3 rosetta_analyze.py MonService.php --no-llm --output-dir ./output
```

### Options utiles

| Option | Rôle |
|--------|------|
| `--archive` | Archiver dans `~/rosetta-memory/audits/` + index.md |
| `--contexte "US-1234"` | Label pour l'archive |
| `--kb-root <dir>` | Injecter fiches KB dans les prompts LLM |
| `--call-graph-root <dir>` | Indexer les méthodes cross-fichiers (3500+ méthodes) |
| `--bug-check` | Grille bugs techniques LLM (13 catégories) |
| `--no-llm` | Mode déterministe uniquement, 0 coût |
| `--from-json <ir.json>` | Régénérer docs sans relancer l'extraction |
| `--retry-failed` | Relancer uniquement les insights en erreur |

**Chemin Astro Windows (WSL)** : `/mnt/c/wamp/www/Infocentre/astro/application/src/Service/`
(pas `/mnt/wamp/...` — le lecteur `c/` est requis)

---

### Enrichir le KB après analyse

Les tokens non résolus apparaissent dans le résumé :
```
📊 Couverture KB : 0.0% (0/21 flags résolus sans LLM)
   → À enrichir en KB : Gatape(2×), criticality(2×)
```

#### Route 1 — CLI direct (sémantique connue, confiance `high`)

```bash
.venv/bin/python3 rosetta_kb.py capture \
  --code MON_TOKEN \
  --label "Label métier clair" \
  --domaine aircom \
  --notes "Contexte, format, cache, couplages..." \
  --lie-a "AUTRE_TOKEN" \
  --source "US Jira + Samah — YYYY-MM-DD" \
  --confiance high
```

#### Route 2 — Fiche `.md` dans `.github/kb/{domaine}/` (token PHP ancré)

Nommage : `regle_NOM.md` ou `code_NOM.md`

```yaml
---
kb_type: regle          # code | regle | requete | colonne | vue
kb_nom: NOM_TOKEN
kb_fichier: application/src/Service/MonService.php
kb_anchor_method: maMethode
kb_anchor_logic: fragment_pivot
kb_confiance: medium    # jamais high en automatique
kb_source: "Analyse Rosetta + Samah — YYYY-MM-DD"
kb_domaine: nomdomaine
kb_migration: partiel   # non | partiel | requis
---
## Label
## Sémantique
## Concepts / Conditions / Constantes
## Trouvé dans
```

Puis importer :
```bash
.venv/bin/python3 rosetta_kb.py import ~/projects/astro/.github/kb/
```

#### Route 3 — Fiche docs-kb/ (colonnes/vues Oracle, format Copilot)

```bash
# Créer ~/rosetta-data/docs-kb/colonne_NOM.md avec frontmatter kb_type
.venv/bin/python3 rosetta_kb.py import ~/rosetta-data/docs-kb/
```

#### Vérifier après import

```bash
.venv/bin/python3 rosetta_kb.py stats
.venv/bin/python3 rosetta_kb.py lookup --code MON_TOKEN
```

---

## 10. TÂCHES PRÊTES À CODER

### ✅ Déjà livrées

- [x] `kb_import.py` — parser frontmatter + sections, router vers KB, résumé d'import
- [x] `tests/test_kb_import.py` — 24 tests unitaires (fixtures .md dans `tests/fixtures/docs-kb/`)
- [x] Scripts anti-drift dans Astro `.github/rosetta/` (kb_drift_check.py, kb_update_anchors.py)
- [x] `install_hook.sh` — hook pre-commit Astro installé
- [x] `aliases.sh` — kb-check, kb-sync, kb-import, kb-stats
- [x] `Makefile` — kb-check, kb-sync, kb-import, kb-full
- [x] Wrapper `rosetta_kb.py import <dir>` — sous-commande CLI, mode fichier unique et répertoire
- [x] Branchement `lookup_for_enricher()` dans `llm_enricher.py` — KB avant LLM, fallback automatique
- [x] Export KB au format prompt LLM — `export-prompt` + `format_kb_for_prompt()`, alias `kb-prompt`
- [x] `kb_type: bug` supporté dans l'importeur — `_IMPORT_TYPE_ROUTES` + `_import_build_entry` + label `[BUG]`
- [x] `kb_domaine` aligné PascalCase — `scripts/kb_update_domaines.py` + 52 fiches MD mises à jour
- [x] Réorganisation KB par service PHP — `scripts/kb_migrate_by_service.py` + 6 renommages + fusion orchestra+diagnostic
- [x] `pending_type` + `destination` auto sur nouveaux pending — `_detect_pending_type()` dans `rosetta_kb.py` et `inject_pending.py`

---

### 🔴 Bloquant pour la démo

- [ ] Vérifier pourquoi les bugs ConfigScenarioService n'apparaissent pas encore dans les sorties démo — `kb_type: bug` codé mais les entrées ne remontent pas encore dans les documents générés ni dans le contexte KB LLM

---

### 🟡 Important mais pas bloquant

- [ ] Migration rétroactive des pending existants — ajouter `pending_type` + `destination` aux ~115 entrées dans `_global.yaml` sans ces champs (commande explicite `rosetta_kb.py migrate-pending`)
- [ ] Rate limiting mesuré — quantifier combien de fichiers PHP Rosetta peut traiter en une session sans corruption KB ni timeout LLM

---

### 🔵 Plus tard

- [ ] Endpoint API — exposer Rosetta hors CLI (HTTP REST ou socket) pour intégration VS Code / Copilot
- [ ] Brief PO cross-domaine — regrouper les pending par domaine métier (pas par fichier PHP) : tout ce qui touche OCEANE ensemble, tout ce qui touche les modules ensemble, etc.
