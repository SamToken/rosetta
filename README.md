# ?? Rosetta

**Hybrid Analysis pour migrer PHP Legacy vers Symfony avec extraction de logique métier et enrichissement LLM sécurisé.**

## Why Rosetta?

Le legacy PHP d?Astro contient de la logique métier enfouie dans des contrôleurs, des branches conditionnelles et des requêtes SQL peu lisibles. Rosetta transforme ce code en une base d?analyse fiable en combinant :

- une extraction statique déterministe pour capturer l?IR métier sans interprétation aléatoire,
- un enrichissement LLM ciblé pour expliquer l?intention métier des fragments les plus ambigus.

## How it works

Rosetta s?exécute comme un pipeline de migration hybride :

1. **Extract**
   - Parse un fichier PHP (contrôleur, service, repository, etc.) et génère une représentation intermédiaire JSON (IR).
2. **Flag**
   - Détecte les fragments suspects avec le Flag Engine : valeurs magiques, branches manquantes, SQL unsafe, dépendances non mappées, etc.
3. **Enrich**
   - Envoie uniquement les fragments flaggés à Claude Sonnet 3.5/4.
   - Le fichier PHP complet ne sort jamais : souveraineté des données garantie.
4. **Report**
   - Génère une documentation Markdown orientée PO et un schéma JSON exploitable par les développeurs.

## Key Features

- ? **Hybrid Analysis** : déterministe par défaut, probabiliste par nécessité.
- ?? **Extraction PHP ? IR** : parseur dédié, format JSON structuré.
- ?? **Flag Engine** : 6 règles déterministes pour détecter :
  - valeurs magiques,
  - branches manquantes,
  - requêtes SQL dangereuses,
  - dépendances non mappées,
  - conditions non couvertes,
  - fragments métier non explicites.
- ?? **Coût maîtrisé** : prompt caching intensif pour réduire les frais LLM de ~66%.
- ??? **Auditabilité** : chaque insight LLM est accompagné d?un score de confiance et reste soumis à validation humaine.
- ?? **Outputs professionnels** : documentation business en Markdown + IR JSON pour les développeurs.

## Developer Experience

Rosetta est conçu pour être simple à utiliser en CLI :

```bash
cd /home/nixos/projects/rosetta
source .venv/bin/activate
python rosetta_analyze.py tests/AdminAiguillageController.php --output-dir ./output
```

Tu peux analyser n'importe quel fichier PHP de legacy : contrôleur, service, repository, etc.

```bash
python rosetta_analyze.py src/Service/SampleService.php --output-dir ./output
python rosetta_analyze.py src/Repository/ContractRepository.php --output-dir ./output
```

### Options clés

- `--output-dir ./output` : dossier de sortie pour JSON et Markdown
- `--no-llm` : exécute le pipeline déterministe sans appel Claude

## Security & Data Privacy

Rosetta est construit autour de la sécurité des données :

- seul le fragment de code flaggé est transmis au modèle,
- le contrôleur complet ne quitte jamais le périmètre local,
- l?enrichissement LLM est réservé aux zones nécessitant une interprétation métier.

## Philosophy

**Déterministe par défaut, probabiliste par nécessité.**

Rosetta privilégie d?abord l?analyse locale 100% fiable, puis applique l?IA de manière ciblée pour compléter les zones où la sémantique métier reste incertaine.

---

**Rosetta ? Décoder l?intention métier du legacy PHP, avec rigueur et confiance.**
