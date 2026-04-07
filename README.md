# 🪨 Rosetta

**Migrateur PHP Legacy → Symfony avec IR (Intermediate Representation)**

Comme la pierre de Rosette qui a permis de déchiffrer les hiéroglyphes, Rosetta traduit ton code legacy en Symfony moderne.

## 🎯 Concept

```
PHP Legacy → [Extracteur] → IR JSON → [Générateur] → Prompt → [IA] → Symfony
     🏛️           🔍            📋          ✨          🤖         🚀
```

**Pourquoi ?**
- L'IA comprend mieux un prompt structuré qu'un fichier PHP de 800 lignes
- Tu gardes le contrôle sur l'extraction (pas de magie noire)
- Zéro perte de logique métier (le code brut est inclus)

## 📦 Structure

```
rosetta/
├── extractors/
│   └── php_extractor.py    # Parse PHP → IR (sans IA, juste regex)
├── ir/
│   └── schema.py           # Le format pivot (Pydantic)
├── generators/
│   └── symfony_generator.py # IR → Prompts Symfony
└── tests/
    ├── sample_controller.php
    └── demo_full_workflow.py
```

## 🚀 Utilisation rapide

```python
from extractors.php_extractor import extract_php
from generators.symfony_generator import generate_migration_prompt

# 1. Extraire l'IR
ir = extract_php('mon_controller.php')

# 2. Voir le résumé
print(ir.summary())

# 3. Générer un prompt pour une action
prompt = generate_migration_prompt(ir, 'edit')

# 4. Copier-coller dans Claude/Gemini
print(prompt)
```

## 🔧 Installation

```bash
pip install pydantic
```


## 📈 Roadmap

- [x] Extracteur PHP basique
- [x] Schéma IR Pydantic
- [x] Générateur de prompts Symfony
- [ ] CLI avec Typer
- [ ] Mode batch (plusieurs contrôleurs)
- [ ] Support des modèles Doctrine

---

**🪨 Rosetta — Déchiffre ton code legacy**
