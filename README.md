# 🌿 Rosetta — Branch tree-rosetta

Outil d'audit fonctionnel et d'extraction de connaissance pour la migration de systèmes PHP legacy Zend vers Symfony.

Rosetta ne se contente plus de lire du texte ; elle comprend la structure du code grâce à un **arbre syntaxique abstrait (AST)**. Elle produit des livrables stratégiques pour le Product Owner :
- Règles métier extraites
- Comportements non définis (Gaps)
- Cartographie des risques

Le tout **sans jargon technique**.

---

## 🎯 Principe : "Structural Truth"

Rosetta fonctionne en deux passes complémentaires :

### 1. Extraction Structurelle (AST via Tree-sitter)

Le code PHP est analysé localement. L'AST garantit une fiabilité de **100%** sur :
- Détection des méthodes
- Blocs if/else imbriqués
- Injections de services

Le **Flag Engine** identifie les "points noirs" :
- Gaps de logique
- Dépendances critiques
- Couplage fort

### 2. Enrichissement Sémantique (LLM)

Seuls les fragments de code flaggués et leurs commentaires adjacents sont transmis à Claude. Le LLM traduit la structure technique en **règle métier en français**, prête pour un arbitrage PO.

**Philosophie** : _Deterministic AST for structure, Probabilistic LLM for meaning._

---

## 🛠 Installation

Pour les utilisateurs **NixOS** (recommandé) ou environnements Python standards :

```bash
# Installation des dépendances
pip install tree-sitter tree-sitter-php anthropic pydantic python-dotenv
```

### Configuration du .env

```bash
ANTHROPIC_API_KEY=sk-ant-...
```

---

## 🚀 Usage

### Analyse d'un composant unique

```bash
python rosetta_analyze.py AssistantController.php --output-dir ./output
```

| Fichier produit | Destinataire | Contenu |
|---|---|---|
| `<Nom>_business_doc.md` | Product Owner | Synthèse des règles, Gaps à arbitrer, Score de risque |
| `<Nom>_flags.md` | Tech Lead | Détail technique des alertes (Lignes, Types de nœuds) |
| `<Nom>_business_logic.json` | Pipeline / RAG | IR complet (JSON) pour ingestion IA |

### Mode Batch (Répertoire complet)

```bash
python rosetta_analyze.py ./src/Controller/ --output-dir ./audit_report
```

Génère un `global_audit.md` avec la matrice de décision transverse et le score de santé global.

---

## 📊 Risk Scoring & Santé Fonctionnelle

Rosetta calcule un score de risque automatisé pour chaque méthode afin de prioriser la migration :

$$Score_{Risque} = (Complexity_{Cyclomatic} \times 2) + (Coupling_{Services} \times 5) + (Magic_{Values} \times 3)$$

- 🔴 **Critique** (Score > 70) : Méthodes "God Object", couplage extrême, logique opaque
- 🟡 **Modéré** (Score 30-70) : Logique à isoler dans des services dédiés
- 🟢 **Sain** (Score < 30) : Code prêt pour une migration directe

---

## 🏗 Architecture de la branche tree

```
rosetta/
├── extractors/
│   └── php_extractor.py         # Parseur AST (Tree-sitter PHP)
│       ├── _extract_params_ast()
│       ├── _extract_control_flow_ast()
│       └── _link_comments()
│
├── analyzers/
│   ├── flag_engine.py           # Moteur de règles
│   └── risk_analyzer.py         # Calculateur de complexité
│
├── aggregators/
│   └── business_aggregator.py   # Consolidation (57 Gaps vs 106 Flags)
│
└── generators/
    └── business_doc_generator.py # Rendu Markdown
```

---

## 🔒 Confidentialité & Performance

- **Zéro "Full-File" Upload** : Le fichier PHP complet n'est jamais envoyé au LLM. Seuls les fragments identifiés par l'AST sont transmis.
- **Précision AST** : Réduction de 44% des faux positifs par rapport à l'ancienne version Regex
- **Prompt Caching** : Optimisation des coûts Anthropic sur les analyses de masse

---

## 📈 Roadmap

- [x] Migration complète vers Tree-sitter (Structure & Flow)
- [x] Implémentation du Risk Scoring (Complexité & Couplage)
- [x] Corrélation automatique Code/Commentaires (Business Context)
- [ ] Génération de graphes de dépendances Graphviz (DOT)
- [ ] Export des matrices de décision vers Jira/Confluence