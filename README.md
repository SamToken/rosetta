# Rosetta — Knowledge Base & Anti-Drift Pipeline

Outil privé de cartographie des règles métier d'un legacy PHP 7.3.

## Architecture

```
~/projects/rosetta/          (privé — ce repo)
├── kb/
│   └── <domaine>/           ← fiches KB par domaine métier
├── kb_import.py             ← import fiches → knowledge_base.yaml
├── rosetta_kb.py            ← CLI KB (lookup, stats, validate...)
├── aliases.sh               ← kb-import, kb-stats, kb-check, kb-sync
└── Makefile                 ← kb-full, kb-import, kb-check

~/rosetta-data/              (local uniquement, hors repo)
└── knowledge_base.yaml      ← source de vérité KB
```

**Principe** : les fiches KB (`kb/`) restent dans ce repo privé.
`knowledge_base.yaml` reste local, jamais versionné.

---

## Setup NixOS (une seule fois)

```bash
nix-shell   # installe pyyaml + python-frontmatter
```

---

## Usage quotidien

```bash
# Importer toutes les fiches dans knowledge_base.yaml
kb-import
# ou : python3 kb_import.py

# Dashboard KB
kb-stats
# ou : python3 rosetta_kb.py stats

# Pipeline complet (import + stats)
make kb-full
```

### Recherche & validation

```bash
python3 rosetta_kb.py lookup --code MA_REGLE_METIER
python3 rosetta_kb.py search --texte "SLA"
python3 rosetta_kb.py pending
python3 rosetta_kb.py validate --id PV-001 --label "..." --source "PO validé"
```

---

## Ce qu'on partage / ce qu'on garde

| Élément | Partagé ? |
|---------|-----------|
| Fiches KB (`kb/`) | ❌ Repo privé uniquement |
| `knowledge_base.yaml` | ❌ Local uniquement |
| Scripts Rosetta | ❌ Repo privé uniquement |

---

*Rosetta — Knowledge Base pipeline · Samah Toutouh · 2026*
