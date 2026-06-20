"""Render a single self-contained, CLICKABLE HTML demo of the dashboard.

Bakes the seeded data into one .html file with the navigation handled by
in-page JavaScript — so you can tap cards, open project detail (with the score
breakdown), filter the board, and view the map, with NO server and NO Python.
Opens in any browser: iOS Safari, Android Chrome, desktop. Works offline
except the map tiles (OpenStreetMap), which need internet.

This is an interactive PREVIEW of seeded data — add/edit/import need the live
app. Generate with:

    python -m scripts.make_demo        # writes docs/dashboard_demo.html
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db import SessionLocal, init_db  # noqa: E402
from app.main import PIPELINE_STATUSES, _kpis  # noqa: E402
from app.models import Project  # noqa: E402

BASE = Path(__file__).resolve().parent.parent
CSS = (BASE / "app" / "web" / "static" / "style.css").read_text()
OUT = BASE / "docs" / "dashboard_demo.html"


def project_dict(p: Project) -> dict:
    return {
        "project_id": p.project_id,
        "project_name": p.project_name,
        "country": p.country,
        "city": p.city,
        "project_type": p.project_type,
        "status": p.status,
        "pipeline_status": p.pipeline_status,
        "score": p.score,
        "tier": p.tier,
        "estimated_door_demand": p.estimated_door_demand,
        "fire_rating_relevant": p.fire_rating_relevant,
        "reachable_before_procurement": p.reachable_before_procurement,
        "value_estimate": p.value_estimate,
        "value_currency": p.value_currency,
        "unit_count": p.unit_count,
        "floor_area": p.floor_area,
        "latitude": p.latitude,
        "longitude": p.longitude,
        "stakeholders": [
            {"role": s.role, "organisation": s.organisation, "contact_name": s.contact_name,
             "email": s.email, "phone": s.phone}
            for s in p.stakeholders
        ],
        "sources": [{"source": s.source, "id": s.source_record_id} for s in p.source_refs],
        "breakdown": p.score_breakdown,
    }


def main() -> None:
    init_db()
    session = SessionLocal()
    try:
        projects = session.query(Project).order_by(Project.score.desc()).all()
        if not projects:
            print("No data. Run `python -m scripts.seed` first.")
            return
        data = [project_dict(p) for p in projects]
        kpis = _kpis(session)
        ctx = {
            "projects": data,
            "kpis": {"pipeline_value": kpis["pipeline_value"]},
            "pipeline_statuses": PIPELINE_STATUSES,
        }
        page = TEMPLATE.replace("/*__CSS__*/", CSS).replace(
            "__DATA__", json.dumps(ctx, separators=(",", ":"))
        )
        OUT.write_text(page)
        print(f"Wrote {OUT} ({len(page):,} bytes, {len(projects)} projects, fully clickable).")
    finally:
        session.close()


TEMPLATE = r"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<title>GCC Door Intel — Interactive Demo</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>
/*__CSS__*/
.banner{background:#fff7e6;border:1px solid #f0d9a8;color:#7a5b12;padding:10px 14px;
  border-radius:8px;margin:14px 0;font-size:13px;}
.topbar nav a{cursor:pointer;}
.topbar nav a.active{color:#fff;font-weight:700;}
.view{display:none;} .view.on{display:block;}
#map{height:70vh;border-radius:8px;}
.back{cursor:pointer;}
.disabled{opacity:.45;}
@media(max-width:640px){.detail{grid-template-columns:1fr;} .board{flex-direction:column;}
  .col{min-width:0;} main{padding:14px;}}
</style></head>
<body>
<header class="topbar">
  <div class="brand">SBK · GCC Door Intelligence <span class="internal">INTERNAL · DEMO</span></div>
  <nav>
    <a id="nav-board" onclick="show('board')">Pipeline</a>
    <a id="nav-map" onclick="show('map')">Map</a>
    <a class="disabled" title="Available in the live app">+ Add lead</a>
    <a class="disabled" title="Available in the live app">Import file</a>
  </nav>
</header>
<main>
  <div class="banner"><b>Interactive demo</b> — real seeded data, fully clickable on phone or desktop.
  Tap a project card to see its score breakdown. (Add/Edit/Import work in the live app.)</div>

  <!-- BOARD -->
  <section id="view-board" class="view on">
    <section class="kpis" id="kpis"></section>
    <form class="filters" onsubmit="return false">
      <select id="f-country"><option value="">All countries</option></select>
      <select id="f-tier"><option value="">All tiers</option><option>A</option><option>B</option><option>C</option></select>
      <select id="f-type"><option value="">All types</option></select>
      <input id="f-score" type="number" placeholder="Min score">
      <button type="button" onclick="renderBoard()">Filter</button>
      <button type="button" onclick="clearFilters()">Reset</button>
    </form>
    <div class="board" id="board"></div>
  </section>

  <!-- PROJECT DETAIL -->
  <section id="view-project" class="view">
    <a class="back" onclick="show('board')">← Pipeline</a>
    <div id="project-detail"></div>
  </section>

  <!-- MAP -->
  <section id="view-map" class="view">
    <h2>Active projects</h2>
    <div id="map"></div>
  </section>
</main>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const CTX = __DATA__;
const PROJECTS = CTX.projects;
const STATUSES = CTX.pipeline_statuses;
const esc = s => (s==null?'':String(s)).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
let map=null;

function show(v){
  document.querySelectorAll('.view').forEach(e=>e.classList.remove('on'));
  document.getElementById('view-'+v).classList.add('on');
  document.getElementById('nav-board').classList.toggle('active',v==='board');
  document.getElementById('nav-map').classList.toggle('active',v==='map');
  window.scrollTo(0,0);
  if(v==='map') initMap();
}

function initFilters(){
  const countries=[...new Set(PROJECTS.map(p=>p.country).filter(Boolean))].sort();
  const types=[...new Set(PROJECTS.map(p=>p.project_type).filter(Boolean))].sort();
  document.getElementById('f-country').insertAdjacentHTML('beforeend',
    countries.map(c=>`<option>${esc(c)}</option>`).join(''));
  document.getElementById('f-type').insertAdjacentHTML('beforeend',
    types.map(t=>`<option>${esc(t)}</option>`).join(''));
}
function clearFilters(){
  ['f-country','f-tier','f-type'].forEach(id=>document.getElementById(id).value='');
  document.getElementById('f-score').value=''; renderBoard();
}
function filtered(){
  const c=document.getElementById('f-country').value;
  const t=document.getElementById('f-tier').value;
  const ty=document.getElementById('f-type').value;
  const ms=parseFloat(document.getElementById('f-score').value);
  return PROJECTS.filter(p=>(!c||p.country===c)&&(!t||p.tier===t)&&(!ty||p.project_type===ty)
    &&(isNaN(ms)||(p.score||0)>=ms));
}

function renderKpis(){
  const a=PROJECTS.filter(p=>p.tier==='A').length, b=PROJECTS.filter(p=>p.tier==='B').length;
  const pre=PROJECTS.filter(p=>['concept','design','pre-tender'].includes(p.status)).length;
  const post=PROJECTS.filter(p=>['tender','awarded','under-construction'].includes(p.status)).length;
  document.getElementById('kpis').innerHTML=`
    <div class="kpi"><span class="num">${PROJECTS.length}</span><span class="lbl">Projects</span></div>
    <div class="kpi"><span class="num tierA">${a}</span><span class="lbl">Tier A</span></div>
    <div class="kpi"><span class="num tierB">${b}</span><span class="lbl">Tier B</span></div>
    <div class="kpi"><span class="num">${CTX.kpis.pipeline_value.toLocaleString()}</span><span class="lbl">Pipeline value</span></div>
    <div class="kpi"><span class="num">${pre}/${post}</span><span class="lbl">Pre / post tender</span></div>`;
}

function renderBoard(){
  const rows=filtered();
  const cols=STATUSES.map(st=>{
    const items=rows.filter(p=>p.pipeline_status===st);
    const cards=items.map(p=>`
      <a class="card tier-${p.tier}" onclick="openProject('${p.project_id}')">
        <div class="card-top"><span class="tier-badge tier-${p.tier}">${p.tier}</span><span class="score">${p.score}</span></div>
        <div class="card-name">${esc(p.project_name)}</div>
        <div class="card-meta">${esc(p.country)||'?'} · ${esc(p.project_type)}</div>
        <div class="card-meta">${esc(p.status)} · doors~${p.estimated_door_demand||'?'}${p.fire_rating_relevant?' · 🔥':''}</div>
      </a>`).join('');
    return `<div class="col"><h3>${st} <span class="count">${items.length}</span></h3>${cards}</div>`;
  }).join('');
  document.getElementById('board').innerHTML=cols;
}

function openProject(id){
  const p=PROJECTS.find(x=>x.project_id===id); if(!p) return;
  const val=p.value_estimate?`${esc(p.value_currency)} ${p.value_estimate.toLocaleString()}`:'—';
  const sh=p.stakeholders.length?p.stakeholders.map(s=>`<tr><td>${esc(s.role)}</td>
    <td>${esc(s.organisation)||'—'}</td><td>${esc(s.contact_name)} ${esc(s.email)} ${esc(s.phone)}</td></tr>`).join('')
    :'<tr><td colspan=3>No stakeholders recorded.</td></tr>';
  const srcs=p.sources.map(s=>`<li><b>${esc(s.source)}</b> · ${esc(s.id)}</li>`).join('');
  let bd;
  if(p.breakdown && p.breakdown.disqualified){
    bd=`<p class="disq">Auto-disqualified — ${esc(p.breakdown.reason)}</p>`;
  }else{
    const f=(p.breakdown&&p.breakdown.factors)||{};
    bd=`<table class="kv small"><tr><th>Factor</th><th>norm</th><th>pts</th></tr>`+
      Object.keys(f).map(k=>`<tr><td>${k}</td><td>${f[k].normalized}</td><td>${f[k].points} / ${f[k].weight}</td></tr>`).join('')+`</table>`;
  }
  document.getElementById('project-detail').innerHTML=`
   <div class="detail">
    <div class="detail-main">
     <h1>${esc(p.project_name)} <span class="tier-badge tier-${p.tier}">Tier ${p.tier} · ${p.score}</span></h1>
     <p class="sub">${esc(p.country)} · ${esc(p.city)} · ${esc(p.project_type)} · ${esc(p.status)}</p>
     <h3>Project</h3>
     <table class="kv">
      <tr><th>Value estimate</th><td>${val}</td></tr>
      <tr><th>Units / Floor area</th><td>${p.unit_count||'—'} units · ${p.floor_area||'—'} sqm</td></tr>
      <tr><th>Estimated door demand</th><td>${p.estimated_door_demand||'—'}</td></tr>
      <tr><th>Fire-rating relevant</th><td>${p.fire_rating_relevant?'✓ yes':'no'}</td></tr>
      <tr><th>Reachable before procurement</th><td>${p.reachable_before_procurement?'✓ yes':'no'}</td></tr>
     </table>
     <h3>Stakeholders</h3><table class="kv"><tr><th>Role</th><th>Organisation</th><th>Contact</th></tr>${sh}</table>
     <h3>Source references</h3><ul class="sources">${srcs}</ul>
    </div>
    <aside class="detail-side"><h3>Why this score?</h3>${bd}</aside>
   </div>`;
  show('project');
}

function initMap(){
  if(map) { setTimeout(()=>map.invalidateSize(),100); return; }
  map=L.map('map').setView([25,50],5);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap',maxZoom:18}).addTo(map);
  const colors={A:'#1a8f3c',B:'#c98a00',C:'#999'};
  PROJECTS.filter(p=>p.latitude).forEach(p=>{
    L.circleMarker([p.latitude,p.longitude],{radius:8,color:colors[p.tier]||'#666',fillOpacity:.7})
     .addTo(map).on('click',()=>openProject(p.project_id))
     .bindPopup(`<b>${esc(p.project_name)}</b><br>${esc(p.country)} · ${esc(p.project_type)}<br>Tier ${p.tier} · ${p.score}`);
  });
  setTimeout(()=>map.invalidateSize(),200);
}

initFilters(); renderKpis(); renderBoard();
</script>
</body></html>"""


if __name__ == "__main__":
    main()
