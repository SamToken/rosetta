"""
Dashboard Generator — HTML standalone depuis les IRs Rosetta
==============================================================
Lit un répertoire d'IRs JSON (produits par rosetta_analyze.py) et
optionnellement un _impact_index.json, puis génère un fichier HTML
unique et autonome (zéro dépendance serveur) qui agrège :

- Vue "Par fichier" : flags avec citations, recettes migration, see_also
- Vue "Impact tokens" : index cross-fichier avec barre de fréquence
- Vue "Par sévérité" : chart + liste des critiques
- Vue "Relations" : toutes les relations KB avec kind, from→to, confiance

Usage CLI (standalone) :
    python -m generators.dashboard_generator ./output/ -o ./output/dashboard.html

Usage programmatique (dans rosetta_analyze.py ou un script batch) :
    from generators.dashboard_generator import DashboardGenerator
    gen = DashboardGenerator()
    html = gen.generate(ir_dir=Path("./output/"), impact_index=Path("./output/_impact_index.json"))
    Path("./output/dashboard.html").write_text(html)

Intégration pipeline recommandée :
    Ajouter en fin de rosetta_analyze.py (après les generators existants) :
        if args.dashboard:
            from generators.dashboard_generator import DashboardGenerator
            gen = DashboardGenerator()
            html = gen.generate(ir_dir=output_dir, impact_index=output_dir / "_impact_index.json")
            (output_dir / "dashboard.html").write_text(html, encoding="utf-8")
            print(f"      ✓ Dashboard → {output_dir / 'dashboard.html'}")
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


# =============================================================================
# Extraction de données depuis les IRs JSON
# =============================================================================

def _load_irs(ir_dir: Path, pattern: str = "*_business_logic.json") -> list[dict]:
    """Charge tous les IRs JSON d'un répertoire."""
    irs = []
    for path in sorted(ir_dir.rglob(pattern)):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            irs.append(data)
        except Exception:
            continue
    return irs


def _load_impact_index(path: Path) -> Optional[dict]:
    """Charge l'impact index JSON s'il existe."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _severity(flag: dict) -> str:
    """Classifie un flag en crit/warn/info."""
    ftype = flag.get("type", "")
    if ftype == "security_risk":
        return "crit"
    if ftype in ("missing_branch", "magic_value", "hardcoded_situation_code"):
        return "warn"
    return "info"


def _extract_dashboard_data(irs: list[dict], impact: Optional[dict]) -> dict:
    """Transforme les IRs bruts en structure JSON pour le dashboard HTML."""

    files = []
    all_relations = []

    for ir in irs:
        meta = ir.get("metadata", {})
        source = meta.get("source_file", "")
        name = Path(source).name if source else meta.get("controller_name", "unknown") + ".php"

        flags_raw = ir.get("flags", [])
        insights_by_id = {ins["flag_id"]: ins for ins in ir.get("llm_insights", [])}

        flags = []
        for f in flags_raw:
            sev = _severity(f)
            loc_parts = f.get("location", "")
            line = ""
            # Tenter d'extraire la ligne depuis source_line ou start_line
            for ep in ir.get("entry_points", []):
                if ep.get("name") == loc_parts and ep.get("start_line"):
                    line = str(ep["start_line"])
                    break
            for op in ir.get("operations", []):
                if op.get("id") == loc_parts and op.get("source_line"):
                    line = str(op["source_line"])
                    break

            loc_display = f"{loc_parts}:{line}" if line else loc_parts

            insight = insights_by_id.get(f.get("id", ""))
            recipe = None
            # On ne peut pas appeler RecipeBook ici (pas de dépendance)
            # Le recipe matching sera fait côté HTML via le type de flag

            flag_data = {
                "type": f.get("type", "unknown"),
                "loc": loc_display,
                "frag": (f.get("fragment", "") or "")[:200],
                "sev": sev,
                "question": f.get("question", ""),
                "see_also": f.get("see_also", []),
                "insight": None,
            }

            if insight:
                flag_data["insight"] = {
                    "rule": insight.get("business_rule", ""),
                    "conf": insight.get("confidence", 0),
                    "source": insight.get("source", "llm"),
                    "validated": insight.get("validated", False),
                }

            flags.append(flag_data)

        # Relations
        relations_raw = ir.get("relations", [])
        kb_hits = 0
        # Compter les insights source=kb
        for ins in ir.get("llm_insights", []):
            if ins.get("source", "").startswith("kb"):
                kb_hits += 1

        file_data = {
            "name": name,
            "flags": flags,
            "relations": len(relations_raw),
            "kbHits": kb_hits,
        }
        files.append(file_data)

        for rel in relations_raw:
            from_e = rel.get("from_entity", {})
            to_e = rel.get("to_entity", {})
            trouve = rel.get("trouvé_dans", rel.get("trouve_dans", []))
            ref_file = trouve[0].get("fichier", name) if trouve else name
            ref_line = str(trouve[0].get("ligne", "")) if trouve else ""
            all_relations.append({
                "from": from_e.get("value", "?"),
                "to": to_e.get("value", "?"),
                "kind": rel.get("kind", "?"),
                "conf": rel.get("confiance", "medium"),
                "file": f"{ref_file}:{ref_line}" if ref_line else ref_file,
            })

    # Tokens depuis l'impact index
    tokens = []
    if impact and "tokens" in impact:
        for name, data in impact["tokens"].items():
            tokens.append({
                "name": name,
                "occ": data.get("total_occurrences", 0),
                "files": data.get("distinct_files", 0),
                "kb": data.get("kb_known", False),
                "sources": data.get("sources", []),
            })
        # Trier par occurrences descendantes, max 100
        tokens.sort(key=lambda t: -t["occ"])
        tokens = tokens[:100]

    return {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "files": files,
        "tokens": tokens,
        "relations": all_relations,
    }


# =============================================================================
# Template HTML
# =============================================================================

# Le template est inlined ici plutôt que dans un fichier séparé
# pour que le dashboard soit vraiment standalone (un seul .py, un seul .html)

_HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Rosetta v3 — Dashboard</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.6.0/dist/tabler-icons.min.css">
<style>
:root {
  --bg: #ffffff; --bg2: #f5f5f0; --bg3: #eeeee8;
  --tx: #1a1a1a; --tx2: #666660; --tx3: #99998f;
  --bd: rgba(0,0,0,0.12); --bd2: rgba(0,0,0,0.06);
  --acc: #534AB7; --acc-bg: #EEEDFE; --acc-tx: #3C3489;
  --red: #E24B4A; --red-bg: #FCEBEB; --red-tx: #791F1F;
  --amber: #EF9F27; --amber-bg: #FAEEDA; --amber-tx: #633806;
  --blue: #378ADD; --blue-bg: #E6F1FB; --blue-tx: #0C447C;
  --green: #1D9E75; --green-bg: #E1F5EE; --green-tx: #085041;
  --font: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  --mono: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
  --radius: 8px; --radius-lg: 12px;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1a1a1e; --bg2: #26262a; --bg3: #32323a;
    --tx: #e8e8e0; --tx2: #a0a098; --tx3: #707068;
    --bd: rgba(255,255,255,0.12); --bd2: rgba(255,255,255,0.06);
    --acc-bg: #26215C; --acc-tx: #AFA9EC;
    --red-bg: #501313; --red-tx: #F09595;
    --amber-bg: #412402; --amber-tx: #FAC775;
    --blue-bg: #042C53; --blue-tx: #85B7EB;
    --green-bg: #04342C; --green-tx: #5DCAA5;
  }
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font); color: var(--tx); background: var(--bg); line-height: 1.5; }
.wrap { max-width: 960px; margin: 0 auto; padding: 2rem 1.5rem; }
h1 { font-size: 22px; font-weight: 500; }
.sub { font-size: 13px; color: var(--tx2); margin-left: 12px; }
.header { display: flex; align-items: baseline; gap: 8px; margin-bottom: 1.5rem; flex-wrap: wrap; }
.metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-bottom: 1.5rem; }
.metric { background: var(--bg2); border-radius: var(--radius); padding: 14px 16px; }
.metric-l { font-size: 12px; color: var(--tx2); margin-bottom: 2px; }
.metric-v { font-size: 22px; font-weight: 500; }
.metric-d { font-size: 11px; color: var(--green-tx); margin-top: 2px; }
.tabs { display: flex; border-bottom: 1px solid var(--bd); margin-bottom: 1.5rem; gap: 0; overflow-x: auto; }
.tab { padding: 8px 16px; font-size: 13px; color: var(--tx2); cursor: pointer; border: none; background: none;
       border-bottom: 2px solid transparent; font-family: var(--font); white-space: nowrap; }
.tab:hover { color: var(--tx); }
.tab.active { color: var(--tx); border-bottom-color: var(--acc); font-weight: 500; }
.view { display: none; } .view.active { display: block; }
.sr { display: flex; gap: 8px; margin-bottom: 1rem; }
.sr input, .sr select { font-family: var(--font); font-size: 13px; padding: 7px 12px;
  border: 1px solid var(--bd); border-radius: var(--radius); background: var(--bg);
  color: var(--tx); outline: none; }
.sr input { flex: 1; } .sr select { min-width: 140px; }
.sr input:focus, .sr select:focus { border-color: var(--acc); }
.fc { background: var(--bg); border: 0.5px solid var(--bd); border-radius: var(--radius-lg);
  padding: 14px 18px; margin-bottom: 8px; cursor: pointer; transition: border-color .15s; }
.fc:hover { border-color: var(--acc); }
.fc-h { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; }
.fc-n { font-size: 15px; font-weight: 500; }
.fc-b { display: flex; gap: 5px; flex-wrap: wrap; }
.badge { font-size: 10px; padding: 2px 8px; border-radius: var(--radius); font-weight: 500; }
.b-c { background: var(--red-bg); color: var(--red-tx); }
.b-w { background: var(--amber-bg); color: var(--amber-tx); }
.b-i { background: var(--blue-bg); color: var(--blue-tx); }
.b-g { background: var(--green-bg); color: var(--green-tx); }
.fc-s { display: flex; gap: 16px; font-size: 12px; color: var(--tx2); margin-top: 6px; }
.fl { margin-top: 10px; display: none; flex-direction: column; gap: 5px; }
.fi { display: flex; align-items: flex-start; gap: 8px; font-size: 13px;
  padding: 8px 10px; background: var(--bg2); border-radius: var(--radius); }
.dot { flex-shrink: 0; width: 7px; height: 7px; border-radius: 50%; margin-top: 6px; }
.dot-c { background: var(--red); } .dot-w { background: var(--amber); } .dot-i { background: var(--blue); }
.fi-loc { font-family: var(--mono); font-size: 11px; color: var(--blue-tx); white-space: nowrap; }
.fi-type { font-size: 11px; color: var(--tx3); margin-left: 6px; }
.fi-sa { font-size: 10px; color: var(--acc-tx); margin-left: 4px; }
.fi-frag { color: var(--tx2); font-size: 12px; margin-top: 2px; word-break: break-word; }
.fi-ins { font-size: 12px; margin-top: 4px; padding: 6px 8px; background: var(--bg);
  border: 0.5px solid var(--bd2); border-radius: var(--radius); }
.fi-ins-src { font-size: 10px; color: var(--tx3); }
.recipe { margin-top: 6px; padding: 8px; background: var(--bg); border: 0.5px solid var(--bd);
  border-radius: var(--radius); font-size: 12px; }
.recipe-t { font-weight: 500; color: var(--green-tx); margin-bottom: 3px; }
.tr { display: flex; align-items: center; gap: 10px; padding: 8px 12px; font-size: 13px;
  background: var(--bg); border: 0.5px solid var(--bd); border-radius: var(--radius); margin-bottom: 5px; }
.tr-n { font-family: var(--mono); font-weight: 500; min-width: 140px; }
.tr-bar { flex: 1; height: 5px; background: var(--bg3); border-radius: 3px; overflow: hidden; }
.tr-fill { height: 100%; border-radius: 3px; background: var(--acc); }
.tr-c { font-size: 12px; color: var(--tx2); min-width: 90px; text-align: right; }
.tr-kb { font-size: 12px; min-width: 18px; }
.rr { display: flex; align-items: center; gap: 8px; padding: 8px 12px; font-size: 13px;
  background: var(--bg); border: 0.5px solid var(--bd); border-radius: var(--radius); margin-bottom: 5px; flex-wrap: wrap; }
.rr-kind { font-size: 10px; padding: 2px 8px; border-radius: var(--radius); font-weight: 500;
  background: var(--blue-bg); color: var(--blue-tx); min-width: 72px; text-align: center; }
.rr-arrow { color: var(--tx3); }
.rr-conf { font-size: 11px; color: var(--tx3); margin-left: auto; }
.empty { text-align: center; padding: 3rem 1rem; color: var(--tx3); font-size: 14px; }
.chart-wrap { position: relative; width: 100%; height: 240px; margin-bottom: 1.5rem; }
.sev-head { font-size: 14px; font-weight: 500; color: var(--red-tx); margin-bottom: 8px; }
</style>
</head>
<body>
<div class="wrap">
  <div class="header">
    <h1>Rosetta v3</h1>
    <span class="sub" id="genDate"></span>
  </div>
  <div class="metrics" id="metrics"></div>
  <div class="tabs" id="tabs">
    <button class="tab active" data-v="files"><i class="ti ti-file-code" style="font-size:14px;margin-right:3px;vertical-align:-1px"></i>Par fichier</button>
    <button class="tab" data-v="tokens"><i class="ti ti-search" style="font-size:14px;margin-right:3px;vertical-align:-1px"></i>Impact tokens</button>
    <button class="tab" data-v="sev"><i class="ti ti-alert-triangle" style="font-size:14px;margin-right:3px;vertical-align:-1px"></i>Par sévérité</button>
    <button class="tab" data-v="rels"><i class="ti ti-arrows-split" style="font-size:14px;margin-right:3px;vertical-align:-1px"></i>Relations</button>
  </div>
  <div class="view active" id="v-files">
    <div class="sr"><input id="fs" placeholder="Rechercher…"><select id="ff">
      <option value="all">Tous</option><option value="security_risk">security_risk</option>
      <option value="missing_branch">missing_branch</option><option value="magic_value">magic_value</option>
      <option value="business_logic_unclear">business_logic</option></select></div>
    <div id="flist"></div>
  </div>
  <div class="view" id="v-tokens">
    <div class="sr"><input id="ts" placeholder="Rechercher un token…"></div>
    <div id="tlist"></div>
  </div>
  <div class="view" id="v-sev">
    <div class="chart-wrap"><canvas id="sevC" role="img" aria-label="Distribution flags par sévérité"></canvas></div>
    <div id="slist"></div>
  </div>
  <div class="view" id="v-rels">
    <div class="sr"><input id="rs" placeholder="Rechercher une relation…"></div>
    <div id="rlist"></div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script>
// ===== DATA INJECTION POINT =====
const DATA = %%DATA_JSON%%;
// ===== END DATA =====

const esc = s => { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; };

// Metrics
const tF = DATA.files.reduce((s,f) => s + f.flags.length, 0);
const tC = DATA.files.reduce((s,f) => s + f.flags.filter(x => x.sev==='crit').length, 0);
const tR = DATA.relations.length;
const tK = DATA.files.reduce((s,f) => s + f.kbHits, 0);
document.getElementById('genDate').textContent = DATA.generated_at;
document.getElementById('metrics').innerHTML = [
  {l:'Fichiers',v:DATA.files.length},{l:'Flags',v:tF},{l:'Critiques',v:tC},
  {l:'Relations KB',v:tR},{l:'KB hits',v:tK,d:tK?`~$${(tK*0.008).toFixed(2)} éco.`:null},
].map(m=>`<div class="metric"><div class="metric-l">${m.l}</div><div class="metric-v">${m.v}</div>${m.d?`<div class="metric-d">${m.d}</div>`:''}</div>`).join('');

// Tabs
document.querySelectorAll('.tab').forEach(t => t.onclick = () => {
  document.querySelectorAll('.tab').forEach(x => x.classList.remove('active'));
  document.querySelectorAll('.view').forEach(x => x.classList.remove('active'));
  t.classList.add('active');
  document.getElementById('v-'+t.dataset.v).classList.add('active');
  if(t.dataset.v==='sev' && !window._sc) renderSev();
});

// Files view
function renderFiles(filter, search) {
  let html = '';
  DATA.files.forEach(f => {
    let flags = f.flags;
    if(filter && filter!=='all') flags = flags.filter(x => x.type===filter);
    if(search) {
      const q = search.toLowerCase();
      const nm = f.name.toLowerCase().includes(q);
      const fm = flags.some(x => x.frag.toLowerCase().includes(q) || x.type.includes(q));
      if(!nm && !fm) return;
      if(!nm) flags = flags.filter(x => x.frag.toLowerCase().includes(q) || x.type.includes(q));
    }
    if(!flags.length && filter && filter!=='all') return;
    const cs = flags.filter(x=>x.sev==='crit').length;
    const ws = flags.filter(x=>x.sev==='warn').length;
    const is = flags.filter(x=>x.sev==='info').length;
    html += `<div class="fc" onclick="const fl=this.querySelector('.fl');fl.style.display=fl.style.display==='flex'?'none':'flex'">
      <div class="fc-h"><span class="fc-n"><i class="ti ti-file-code" style="font-size:15px;margin-right:4px;vertical-align:-2px;color:var(--tx2)"></i>${esc(f.name)}</span>
      <div class="fc-b">${cs?`<span class="badge b-c">${cs} crit.</span>`:''}${ws?`<span class="badge b-w">${ws} warn.</span>`:''}${is?`<span class="badge b-i">${is} info</span>`:''}${f.relations?`<span class="badge b-g">${f.relations} rel.</span>`:''}</div></div>
      <div class="fc-s"><span>${flags.length} flags</span><span>${f.kbHits} KB hits</span></div>
      <div class="fl">${flags.map(fl => {
        const sa = fl.see_also && fl.see_also.length ? fl.see_also.join(', ') : '';
        return `<div class="fi"><div class="dot dot-${fl.sev}"></div><div style="flex:1">
          <div><span class="fi-loc">${esc(fl.loc)}</span><span class="fi-type">${esc(fl.type)}</span>${sa?`<span class="fi-sa">↗ ${esc(sa)}</span>`:''}</div>
          <div class="fi-frag">${esc(fl.frag)}</div>
          ${fl.insight?`<div class="fi-ins">${esc(fl.insight.rule)} <span class="fi-ins-src">(${fl.insight.source} ${Math.round(fl.insight.conf*100)}%${fl.insight.validated?' ✔':''})</span></div>`:''}
        </div></div>`;
      }).join('')}</div></div>`;
  });
  document.getElementById('flist').innerHTML = html || '<div class="empty">Aucun fichier trouvé</div>';
}
document.getElementById('fs').oninput = e => renderFiles(document.getElementById('ff').value, e.target.value);
document.getElementById('ff').onchange = e => renderFiles(e.target.value, document.getElementById('fs').value);
renderFiles('all','');

// Tokens view
function renderTokens(search) {
  const maxO = Math.max(...DATA.tokens.map(t=>t.occ), 1);
  let toks = DATA.tokens;
  if(search) { const q=search.toLowerCase(); toks=toks.filter(t=>t.name.toLowerCase().includes(q)); }
  document.getElementById('tlist').innerHTML = toks.length ? toks.map(t =>
    `<div class="tr"><span class="tr-kb">${t.kb?'📚':''}</span><span class="tr-n">${esc(t.name)}</span>
    <div class="tr-bar"><div class="tr-fill" style="width:${Math.round(t.occ/maxO*100)}%"></div></div>
    <span class="tr-c">${t.occ} occ. / ${t.files} fich.</span></div>`
  ).join('') : '<div class="empty">Aucun token</div>';
}
document.getElementById('ts').oninput = e => renderTokens(e.target.value);
renderTokens('');

// Severity view
function renderSev() {
  window._sc = true;
  const types = {};
  DATA.files.forEach(f => f.flags.forEach(fl => {
    if(!types[fl.type]) types[fl.type] = {crit:0,warn:0,info:0};
    types[fl.type][fl.sev]++;
  }));
  const labels = Object.keys(types);
  if(labels.length) {
    new Chart(document.getElementById('sevC'), {
      type:'bar', data:{ labels,
        datasets:[
          {label:'Critique',data:labels.map(l=>types[l].crit),backgroundColor:'#E24B4A'},
          {label:'Warning',data:labels.map(l=>types[l].warn),backgroundColor:'#EF9F27'},
          {label:'Info',data:labels.map(l=>types[l].info),backgroundColor:'#378ADD'},
        ]},
      options:{ responsive:true, maintainAspectRatio:false,
        scales:{x:{stacked:true,ticks:{autoSkip:false,maxRotation:30}},y:{stacked:true,beginAtZero:true}},
        plugins:{legend:{display:false}} }
    });
  }
  const crits = [];
  DATA.files.forEach(f => f.flags.filter(fl=>fl.sev==='crit').forEach(fl => crits.push({...fl,file:f.name})));
  document.getElementById('slist').innerHTML = (crits.length ?
    `<div class="sev-head"><i class="ti ti-alert-circle" style="font-size:15px;margin-right:4px;vertical-align:-2px"></i>${crits.length} flag(s) critique(s)</div>` : '') +
    crits.map(fl => `<div class="fi" style="margin-bottom:5px"><div class="dot dot-c"></div><div style="flex:1">
      <div><span class="fi-loc">${esc(fl.file)}:${esc(fl.loc.split(':')[1]||'')}</span><span class="fi-type">${esc(fl.type)}</span></div>
      <div class="fi-frag">${esc(fl.frag)}</div></div></div>`).join('');
}

// Relations view
function renderRels(search) {
  let rels = DATA.relations;
  if(search) { const q=search.toLowerCase(); rels=rels.filter(r=>r.from.toLowerCase().includes(q)||r.to.toLowerCase().includes(q)||r.kind.includes(q)); }
  document.getElementById('rlist').innerHTML = rels.length ? rels.map(r =>
    `<div class="rr"><span class="rr-kind">${esc(r.kind)}</span>
    <span style="font-family:var(--mono);font-weight:500">${esc(r.from)}</span>
    <span class="rr-arrow">→</span>
    <span style="font-family:var(--mono)">${esc(r.to)}</span>
    <span class="rr-conf">${esc(r.conf)} · ${esc(r.file)}</span></div>`
  ).join('') : '<div class="empty">Aucune relation</div>';
}
document.getElementById('rs').oninput = e => renderRels(e.target.value);
renderRels('');
</script>
</body>
</html>"""


# =============================================================================
# Classe principale
# =============================================================================

class DashboardGenerator:
    """Génère un dashboard HTML standalone depuis les IRs Rosetta."""

    def generate(
        self,
        ir_dir: Path,
        impact_index: Optional[Path] = None,
        ir_pattern: str = "*_business_logic.json",
    ) -> str:
        """
        Charge les IRs et l'impact index, produit le HTML complet.

        Args:
            ir_dir: répertoire contenant les fichiers *_ir.json
            impact_index: chemin vers _impact_index.json (optionnel)
            ir_pattern: glob pour les fichiers IR

        Returns:
            string HTML complète prête à écrire dans un fichier
        """
        irs = _load_irs(ir_dir, pattern=ir_pattern)
        impact = _load_impact_index(impact_index) if impact_index else None
        data = _extract_dashboard_data(irs, impact)

        # Injecter le JSON dans le template
        data_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        html = _HTML_TEMPLATE.replace("%%DATA_JSON%%", data_json)

        return html

    def generate_from_irs(
        self,
        irs: list[dict],
        impact: Optional[dict] = None,
    ) -> str:
        """
        Variante programmatique : prend les IRs déjà chargés en mémoire.
        Utile pour l'intégration dans le pipeline sans re-lecture disque.
        """
        data = _extract_dashboard_data(irs, impact)
        data_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        return _HTML_TEMPLATE.replace("%%DATA_JSON%%", data_json)


# =============================================================================
# CLI standalone
# =============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="dashboard_generator",
        description="Génère un dashboard HTML depuis les IRs Rosetta v3",
    )
    parser.add_argument(
        "ir_dir",
        help="Répertoire contenant les fichiers *_ir.json",
    )
    parser.add_argument(
        "-o", "--output",
        default="./output/dashboard.html",
        help="Chemin du fichier HTML de sortie",
    )
    parser.add_argument(
        "--impact-index",
        default=None,
        help="Chemin vers _impact_index.json (optionnel)",
    )
    parser.add_argument(
        "--pattern",
        default="*_business_logic.json",
        help="Glob des fichiers IR (défaut: *_business_logic.json)",
    )

    args = parser.parse_args()

    ir_dir = Path(args.ir_dir)
    if not ir_dir.exists():
        print(f"Erreur : répertoire introuvable : {ir_dir}", file=sys.stderr)
        return 1

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    impact_path = Path(args.impact_index) if args.impact_index else ir_dir / "_impact_index.json"

    gen = DashboardGenerator()
    html = gen.generate(
        ir_dir=ir_dir,
        impact_index=impact_path,
        ir_pattern=args.pattern,
    )

    output_path.write_text(html, encoding="utf-8")
    print(f"✓ Dashboard généré → {output_path}")
    print(f"  {len(_load_irs(ir_dir, args.pattern))} fichiers, "
          f"ouvrir dans un navigateur : file://{output_path.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
