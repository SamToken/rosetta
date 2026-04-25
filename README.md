# Rosetta

**Outil d'audit fonctionnel pour la migration de systèmes PHP legacy vers Symfony.**

Rosetta analyse des contrôleurs PHP et produit des livrables lisibles par un Product Owner : règles métier extraites, comportements non définis, services tiers, glossaire — sans aucun jargon technique dans les rapports finaux.

---

## Principe

Rosetta fonctionne en deux passes :

1. **Analyse déterministe** — le code PHP est parsé localement. Le Flag Engine détecte les zones ambiguës (branches manquantes, risques de sécurité, dépendances non documentées, volumes non bornés) et formule chaque point comme une question métier pour le PO.

2. **Enrichissement probabiliste** — seuls les fragments flaggés sont envoyés à Claude. Jamais le fichier complet. Le LLM traduit chaque fragment en règle métier en français, formulée pour un PO non-technique.

> **Deterministic by default, Probabilistic by necessity.**

---

## Installation

```bash
git clone <repo-url>
cd rosetta
python -m venv .venv
source .venv/bin/activate
pip install anthropic pydantic
```

Créer un fichier `.env` avec la clé API :

```
ANTHROPIC_API_KEY=sk-ant-...
```

---

## Usage

### Fichier unique

```bash
python rosetta_analyze.py UserController.php
python rosetta_analyze.py UserController.php --output-dir ./output
python rosetta_analyze.py UserController.php --no-llm
```

Produit 3 fichiers dans `--output-dir` :

| Fichier | Destinataire | Contenu |
|--------|-------------|---------|
| `<Nom>_business_doc.md` | Product Owner | Règles métier, points d'attention, questions ouvertes |
| `<Nom>_flags.md` | Product Owner / Tech Lead | Zones à valider, gaps de logique |
| `<Nom>_business_logic.json` | Développeurs | IR complet avec flags et insights LLM |

### Mode batch (répertoire complet)

```bash
python rosetta_analyze.py ./controllers/ --output-dir ./audit
python rosetta_analyze.py ./controllers/ --output-dir ./audit --no-llm
python rosetta_analyze.py ./controllers/ --output-dir ./audit --model claude-haiku-4-5-20251001
```

Produit :

```
audit/
├── global_audit.md          ← Synthèse globale (Product Owner)
└── details/
    ├── UserController_business_doc.md
    ├── UserController_flags.md
    ├── UserController_business_logic.json
    ├── ContractController_business_doc.md
    └── ...
```

### Options

| Option | Défaut | Description |
|--------|--------|-------------|
| `--output-dir DIR` | `.` | Répertoire de sortie |
| `--no-llm` | off | Analyse déterministe uniquement, sans appel API |
| `--model MODEL` | `claude-sonnet-4-6` | Modèle Anthropic à utiliser |

---

## Rapport global (`global_audit.md`)

En mode batch, Rosetta génère une synthèse transverse avec 4 sections :

1. **Résumé Exécutif** — score de santé global (0-100), tableau par contrôleur, recommandations prioritaires
2. **Règles Transverses** — règles métier présentes dans plusieurs contrôleurs, candidates à la centralisation
3. **Gaps de Documentation** — comportements sans cas contraire documenté, chacun représente une décision à prendre avant migration
4. **Cartographie du Domaine** — glossaire métier unifié + services tiers non documentés

---

## Architecture

```
rosetta_analyze.py          ← Point d'entrée CLI
│
├── extractors/
│   └── php_extractor.py    ← PHP → IRSchema (AST textuel)
│
├── analyzers/
│   ├── flag_engine.py      ← Détection déterministe des zones ambiguës
│   └── llm_enricher.py     ← Enrichissement Claude (fragments uniquement)
│
├── aggregators/
│   └── business_aggregator.py  ← Synthèse transverse de plusieurs IR
│
├── generators/
│   ├── business_doc_generator.py   ← Rapport par contrôleur (PO)
│   ├── global_audit_generator.py   ← Rapport global (PO)
│   └── symfony_generator.py        ← Squelette Symfony (développeurs)
│
└── ir/
    └── schema.py           ← IRSchema : format pivot PHP → Symfony
```

### IR Schema

`IRSchema` est le format pivot central. Il capture l'intention du code, pas sa syntaxe :

- `entry_points` — actions du contrôleur (routes, méthodes HTTP)
- `operations` — opérations métier (DB, email, redirect, calcul…)
- `dependencies` — services tiers avec mapping Symfony suggéré
- `flags` — zones ambiguës détectées (source déterministe, confiance 1.0)
- `llm_insights` — règles métier extraites par Claude (confiance < 1.0)

---

## Modèles supportés

| Modèle | Usage recommandé | Coût estimé / 100 flags |
|--------|----------------|------------------------|
| `claude-haiku-4-5-20251001` | Volumes importants, budget limité | ~$0.02 |
| `claude-sonnet-4-6` | Qualité production (défaut) | ~$0.15 |
| `claude-opus-4-7` | Cas complexes, arbitrage critique | ~$0.75 |

Le prompt système est mis en cache côté Anthropic (prompt caching). Sur un lot de 10 contrôleurs, l'économie de cache est typiquement supérieure au coût des tokens de sortie.

---

## Privacy

- Le fichier PHP complet n'est **jamais** transmis à l'API
- Seuls les fragments flaggés (extraits minimaux) sont envoyés
- L'analyse déterministe est 100% locale (`--no-llm` pour forcer ce mode)

---

## Structure des sorties

```
output/
└── audit_YYYY_MM_DD/
    ├── global_audit.md
    └── details/
        └── <Contrôleur>_business_doc.md
        └── <Contrôleur>_flags.md
        └── <Contrôleur>_business_logic.json
```

Le dossier `output/` est exclu du dépôt git (`.gitignore`).
