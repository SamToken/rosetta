# 🚀 Rosetta

**Rosetta est un outil professionnel de migration PHP Legacy vers Symfony, strictement dédié à l'extraction de la logique métier.**

Cette branche se concentre sur la traduction du code legacy en spécifications fonctionnelles lisibles pour les Product Owners et les stakeholders. Le principal livrable est le Business Doc Generator : un document métier Markdown produit à partir des fragments de code analysés.

## Installation

```bash
git clone <repo-url>
cd rosetta
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate sur Windows
pip install -r requirements.txt
```

## Usage

```bash
python rosetta_analyze.py <target_file.php> --output-dir ./output
```

Options importantes :

- `--output-dir ./output` : dossier de sortie pour les JSON et Markdown
- `--no-llm` : exécute uniquement l'analyse déterministe, sans appel à Claude
- `--model <model-name>` : sélectionne le modèle LLM à utiliser pour l'enrichissement

## Business Doc Generator

Le Business Doc Generator est le livrable principal de Rosetta sur cette branche. Il produit un document Markdown orienté métier qui traduit les fragments PHP legacy en spécifications fonctionnelles compréhensibles par les PO et les parties prenantes.

Le JSON IR reste un artefact technique secondaire, utile pour les développeurs et pour les flux de migration automatisée.

## Architecture du pipeline

Rosetta fonctionne en deux phases complémentaires :

1. **Analyse déterministe**
   - Le moteur statique parse le fichier PHP et construit une représentation intermédiaire (IR).
   - Le Flag Engine applique des règles déterministes pour détecter les problèmes évidents.
2. **Enrichissement probabiliste**
   - Le LLM Enricher ne traite que les fragments flaggés.
   - Seuls les extraits concernés sont envoyés à l'API, jamais le fichier complet.

## Flag Engine

Le Flag Engine analyse le code selon 6 règles déterministes :

- valeurs magiques
- branches manquantes
- sécurité SQL (SQL unsafe)
- dépendances non mappées
- conditions non couvertes
- fragments métier non explicites

## Architecture du rapport

Le Business Doc Generator structure les sorties métier pour faciliter l'audit et la prise de décision :

- 🔴 **Risques** : éléments à prioriser et à corriger rapidement.
- ⚠️ **Ambiguïtés / Branches manquantes** : zones où la logique conditionnelle est partielle ou incertaine.
- 🤖 **Insights LLM** : commentaires métier générés par l'IA avec score de confiance.

## Sovereignty / Privacy-First

Rosetta est conçu pour protéger les données :

- seuls les fragments flaggés sont transmis à l'API LLM,
- le fichier PHP complet reste toujours local,
- l'enrichissement est réservé aux zones nécessitant une interprétation métier.

## Performance & coût

Pour les projets volumineux, Rosetta optimise les coûts avec :

- prompt caching Anthropic,
- réduction des appels LLM d'environ 66%,
- priorisation de l'analyse déterministe pour les cas simples.

## Philosophy

**Deterministic by default, Probabilistic by necessity.**

Rosetta privilégie d'abord une analyse locale fiable, puis applique l'intelligence artificielle uniquement lorsque le contexte métier l'exige.
