# Rosetta — Audit PHP + Knowledge Base (v3)

Outil privé d'analyse statique et de cartographie sémantique d'un legacy PHP 7.3.
Couche CLI, API FastAPI et dashboard ROI — architecture SOLID, 0 donnée métier pushée.

---

## Architecture v3

```
rosetta_analyze.py        ← CLI audit PHP (mode Local ou Remote --api)
rosetta_kb.py             ← CLI Knowledge Base
api_client.py             ← Client HTTP mode Remote (polling live)
config.py                 ← Settings centralisés

services/
  audit_service.py        ← AuditPipeline, AuditOptions
  kb_service.py           ← KBService + 10 dataclasses

analyzers/
  llm_enricher.py         ← Enrichissement LLM (KB → LLM → pending)
  bug_enricher.py         ← Grille 13 catégories bugs + chunking >32K
  flag_engine.py          ← Détection flags déterministes
  call_graph.py           ← Indexation cross-fichiers (3500+ méthodes)
  kb_context.py           ← Injection fiches KB dans les prompts LLM

api/
  main.py                 ← FastAPI + CORS + StaticFiles /dashboard
  schemas.py              ← 18 modèles Pydantic v2
  routers/audit.py        ← POST /audit/start · GET /audit/{id} · ROI
  routers/kb.py           ← 10 endpoints KB lecture + écriture

telemetry/
  performance_logger.py   ← JSONL ROI, dashboard métriques cumulées

ui/index.html             ← Dashboard ROI (Tailwind + Chart.js, dark)

~/rosetta-data/           ← LOCAL UNIQUEMENT — jamais versionné
  knowledge_base.yaml     ← Source de vérité KB
  api_jobs/               ← Sorties jobs API
  roi_metrics.jsonl       ← Métriques cumulées
```

---

## Setup NixOS (une seule fois)

```bash
cd ~/projects/rosetta
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

> **NixOS** : ne pas utiliser `uvicorn` ou `python3` directement — ils ne sont pas dans le PATH.
> Toujours préfixer avec `.venv/bin/` : `.venv/bin/uvicorn`, `.venv/bin/python3`.

---

## Analyse PHP — mode Local

```bash
# Fichier unique avec LLM
cd ~/projects/rosetta && .venv/bin/python3 rosetta_analyze.py \
  /chemin/vers/MonService.php \
  --output-dir ./output \
  --archive \
  --kb-root /chemin/vers/kb/ \
  --call-graph-root /chemin/vers/src/ \
  --contexte "US-1234"

# Mode déterministe gratuit
.venv/bin/python3 rosetta_analyze.py MonService.php --no-llm --output-dir ./output

# Avec grille bugs techniques (13 catégories)
.venv/bin/python3 rosetta_analyze.py MonService.php --bug-check --output-dir ./output
```

## Analyse PHP — mode Remote (API)

```bash
# 1. Démarrer l'API (terminal séparé)
cd ~/projects/rosetta
ROSETTA_KB=~/rosetta-data/knowledge_base.yaml \
  .venv/bin/uvicorn api.main:app --reload --port 8765 --host 127.0.0.1

# 2. Lancer l'analyse via le client Remote
.venv/bin/python3 rosetta_analyze.py MonService.php \
  --api http://localhost:8765 \
  --kb-root /chemin/vers/kb/ \
  --call-graph-root /chemin/vers/src/ \
  --contexte "US-1234"
```

Le client soumet le job, affiche les logs en temps réel, puis propose d'ouvrir les rapports.

---

## API FastAPI

```bash
# Démarrer
ROSETTA_KB=~/rosetta-data/knowledge_base.yaml \
  .venv/bin/uvicorn api.main:app --reload --port 8765 --host 127.0.0.1

# Health check
curl -s http://127.0.0.1:8765/ | python3 -m json.tool

# Swagger interactif
http://localhost:8765/docs
```

| Variable d'env | Rôle |
|----------------|------|
| `ROSETTA_KB` | Chemin KB (fichier ou répertoire) — **obligatoire** |
| `ANTHROPIC_API_KEY` | Clé Claude — obligatoire si jobs LLM |
| `ROSETTA_API_OUTPUT` | Répertoire sorties jobs (défaut : `~/rosetta-data/api_jobs`) |
| `ROSETTA_ROI_METRICS` | Fichier métriques ROI (défaut : `~/rosetta-data/roi_metrics.jsonl`) |

### Endpoints principaux

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/audit/start` | Soumettre un job PHP (HTTP 202, async) |
| `GET` | `/audit/{job_id}` | État + logs + résultats d'un job |
| `GET` | `/audit/roi` | Dashboard ROI cumulé |
| `GET` | `/kb/stats` | Dashboard KB |
| `GET` | `/kb/lookup/{code}` | Lookup token |
| `GET` | `/kb/export/human` | Dossier de fusion (réunion PO) |
| `GET` | `/dashboard` | Dashboard ROI (UI Tailwind) |

---

## Knowledge Base — CLI

```bash
# Capturer un token validé PO
.venv/bin/python3 rosetta_kb.py capture \
  --code MON_TOKEN --label "Label métier" \
  --domaine aircom --source "PO validé — 2026-05-10" --confiance high

# Lookup
.venv/bin/python3 rosetta_kb.py lookup --code MON_TOKEN

# Dashboard KB
.venv/bin/python3 rosetta_kb.py stats

# Ajouter une question PO
.venv/bin/python3 rosetta_kb.py add-pending \
  --code MON_TOKEN --question "Que signifie X dans ce contexte ?" \
  --priorite high --kb-type regle --domaine aircom

# Export dossier de fusion (réunion PO)
.venv/bin/python3 rosetta_kb.py export-human \
  --domaine "RetablirCloturer,OrchestraService" \
  --output ~/rosetta-data/export_human_2026-05-10.md
```

---

## Dashboard ROI

URL : `http://localhost:8765/dashboard` (API active requise)

Affiche : temps humain économisé · lignes analysées · économie financière · coût LLM · graphique 7 jours.

---

## Règles de sécurité

| Règle | Détail |
|-------|--------|
| **0 donnée métier pushée** | `knowledge_base.yaml`, `~/rosetta-data/` → jamais dans le repo |
| **Secrets via `.env`** | `ANTHROPIC_API_KEY` uniquement dans `.env` (ignoré par git) |
| **Confiance `high` = humain** | Scripts restent à `medium` max — seul le PO valide |
| **NixOS** | Toujours `.venv/bin/python3` et `.venv/bin/uvicorn` |

---

*Rosetta v3 — Samah Toutouh · 2026*
