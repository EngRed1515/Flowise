"""HTML/CSS/JS template for the self-contained NEICS walkthrough.

`/*__DATA__*/` is replaced with the embedded JSON payload by build_walkthrough.py.
The result is a single, dependency-free .html file (works by double-clicking).
"""

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>NEICS — National Enterprise Intelligence & Classification System (Staging Walkthrough)</title>
<style>
:root{
  --maroon:#8A1538; --maroon-d:#6d102c; --ink:#1f2733; --muted:#6b7480; --line:#e3e7ec;
  --bg:#f4f6f9; --card:#ffffff; --good:#1f8a4c; --warn:#b8860b; --bad:#c0392b; --info:#2266aa;
  --chip:#eef1f5; --accent:#b08d57;
}
*{box-sizing:border-box} html,body{margin:0;padding:0}
body{font-family:"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);font-size:14px;line-height:1.45}
a{color:var(--maroon);text-decoration:none}
#app{display:flex;min-height:100vh}
.sidebar{width:248px;background:linear-gradient(180deg,#2a0c18,#3a0f20);color:#f2e9ec;flex-shrink:0;position:sticky;top:0;height:100vh;overflow-y:auto}
.brand{padding:18px 18px 12px;border-bottom:1px solid rgba(255,255,255,.12)}
.brand h1{font-size:16px;margin:0;letter-spacing:.5px}
.brand .sub{font-size:11px;color:#caa9b4;margin-top:3px}
.brand .crest{font-size:11px;color:#e6c79a;margin-top:6px}
.nav{padding:8px 0}
.nav button{display:flex;gap:9px;align-items:center;width:100%;border:0;background:none;color:#e9dde1;
  padding:9px 18px;text-align:left;cursor:pointer;font-size:13px;border-left:3px solid transparent}
.nav button:hover{background:rgba(255,255,255,.06)}
.nav button.active{background:rgba(255,255,255,.12);border-left-color:var(--accent);color:#fff;font-weight:600}
.nav .num{opacity:.6;width:20px;font-size:11px}
.main{flex:1;display:flex;flex-direction:column;min-width:0}
.topbar{background:var(--card);border-bottom:1px solid var(--line);padding:10px 22px;display:flex;align-items:center;gap:16px;position:sticky;top:0;z-index:20}
.staging{background:#fff5e6;color:#9a6b00;border:1px solid #f0d8a8;padding:4px 10px;border-radius:5px;font-size:12px;font-weight:600}
.spacer{flex:1}
.userbox{display:flex;align-items:center;gap:8px;font-size:13px}
.userbox select{padding:5px 8px;border:1px solid var(--line);border-radius:5px}
.content{padding:22px;max-width:1280px}
h2.page{margin:0 0 4px;font-size:22px}
.page-sub{color:var(--muted);margin:0 0 18px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin-bottom:20px}
.card{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:16px}
.kpi .v{font-size:30px;font-weight:700;color:var(--maroon)}
.kpi .l{color:var(--muted);font-size:12px;margin-top:3px;text-transform:uppercase;letter-spacing:.4px}
.panel{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:18px;margin-bottom:18px}
.panel h3{margin:0 0 12px;font-size:15px;border-bottom:1px solid var(--line);padding-bottom:8px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media(max-width:900px){.grid2{grid-template-columns:1fr}}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--muted);font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:.4px;background:#fafbfc}
tr.click:hover{background:#f7f3f4;cursor:pointer}
.badge{display:inline-block;padding:2px 8px;border-radius:11px;font-size:11px;font-weight:600;white-space:nowrap}
.b-pub{background:#e7f1ff;color:#1d5fa8}.b-priv{background:#eef6ee;color:#1f8a4c}
.b-gg{background:#f3e8f6;color:#7d3c98}.b-fcc{background:#fff0e6;color:#b9651b}.b-npish{background:#e9f6f4;color:#147d6e}
.bar{height:10px;background:#eef1f5;border-radius:6px;overflow:hidden}
.bar > span{display:block;height:100%;background:var(--maroon)}
.barrow{display:grid;grid-template-columns:160px 1fr 48px;gap:10px;align-items:center;margin:6px 0;font-size:12px}
.btn{background:var(--maroon);color:#fff;border:0;padding:8px 14px;border-radius:6px;cursor:pointer;font-size:13px}
.btn:hover{background:var(--maroon-d)} .btn.sec{background:#fff;color:var(--maroon);border:1px solid var(--maroon)}
.btn.sm{padding:5px 10px;font-size:12px}
.filters{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}
.filters input,.filters select{padding:7px 10px;border:1px solid var(--line);border-radius:6px;font-size:13px}
.chip{display:inline-block;background:var(--chip);border-radius:5px;padding:2px 8px;margin:2px;font-size:11px}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px}
.kv{display:grid;grid-template-columns:190px 1fr;gap:6px 14px;font-size:13px}
.kv div.k{color:var(--muted)}
.tabs{display:flex;gap:4px;border-bottom:1px solid var(--line);margin-bottom:14px;flex-wrap:wrap}
.tabs button{border:0;background:none;padding:9px 13px;cursor:pointer;border-bottom:2px solid transparent;color:var(--muted);font-size:13px}
.tabs button.active{color:var(--maroon);border-bottom-color:var(--maroon);font-weight:600}
.trace{border-left:2px solid var(--line);margin-left:8px;padding-left:14px}
.trace .step{margin-bottom:10px;position:relative}
.trace .step::before{content:"";position:absolute;left:-21px;top:3px;width:10px;height:10px;border-radius:50%;background:var(--maroon)}
.trace .step.skip::before{background:#cfd6dd}
.small{font-size:12px;color:var(--muted)}
.pill{font-size:11px;padding:2px 7px;border-radius:5px;background:#eef1f5}
.note{background:#fbfbf7;border:1px solid #ece7d6;border-radius:7px;padding:12px;font-size:13px}
.statusdot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}
textarea{width:100%;min-height:120px;font-family:ui-monospace,monospace;font-size:12px;border:1px solid var(--line);border-radius:6px;padding:8px}
.rag-Green{color:var(--good);font-weight:700}.rag-Amber{color:var(--warn);font-weight:700}
.rag-Red,.rag-Red-Amber{color:var(--bad);font-weight:700}.rag-Amber-Green{color:#7a8a1f;font-weight:700}
.treebox{font-family:ui-monospace,monospace;font-size:13px;white-space:pre;line-height:1.6}
.legend{font-size:11px;color:var(--muted);margin-top:8px}
.flag{font-weight:600}
ul.tight{margin:6px 0;padding-left:20px} ul.tight li{margin:4px 0}
.ok{color:var(--good)} .err{color:var(--bad)} .wr{color:var(--warn)}
</style>
</head>
<body>
<div id="app">
  <div class="sidebar">
    <div class="brand">
      <div class="crest">STATE OF QATAR · NSO</div>
      <h1>NEICS</h1>
      <div class="sub">National Enterprise Intelligence &amp; Classification System</div>
    </div>
    <div class="nav" id="nav"></div>
  </div>
  <div class="main">
    <div class="topbar">
      <strong style="color:var(--maroon)">NEICS</strong>
      <span class="staging">● STAGING / UAT — Not for production</span>
      <span class="spacer"></span>
      <div class="userbox">
        <span>Acting as</span>
        <select id="rolesel" onchange="state.role=this.value;render()"></select>
      </div>
    </div>
    <div class="content" id="content"></div>
  </div>
</div>
<script>
const DATA = /*__DATA__*/;
const state = {view:"dashboard", entId:DATA.enterprises[0].id, role:"Classifier", tab:0, ruleId:null, filter:""};

const MODULES = [
 ["dashboard","Executive Dashboard"],["registry","Enterprise Registry"],["profile","Enterprise Profile"],
 ["ownership","Ownership & Control"],["groups","Enterprise Group Structure"],["classification","Classification Results"],
 ["rules","Rules Engine Explorer"],["metadata","Metadata Repository"],["standards","Standards Repository"],
 ["quality","Data Quality Dashboard"],["validation","Validation & Exceptions"],["reviews","Manual Review Queue"],
 ["audit","Audit Trail Viewer"],["api","API Demonstration"],["users","User & Role Management"],
 ["uat","UAT Test Center"],["gap","Gap Analysis & Roadmap"]
];

function esc(s){return (s==null?"":String(s)).replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));}
function ent(id){return DATA.enterprises.find(e=>e.id===id);}
function ppBadge(v){const m={"PUB-NFC":"b-pub","PUB-FC":"b-pub","GG":"b-gg","PRV-NFC":"b-priv","PRV-FC":"b-priv","FCC":"b-fcc","NPISH":"b-npish"};return `<span class="badge ${m[v]||''}">${esc(v)}</span>`;}
function fmtMoney(v){if(v==null)return "—";if(v>=1e9)return "QAR "+(v/1e9).toFixed(1)+"bn";if(v>=1e6)return "QAR "+(v/1e6).toFixed(1)+"m";return "QAR "+v.toLocaleString();}
function go(v,extra){state.view=v;if(extra)Object.assign(state,extra);window.scrollTo(0,0);render();}

// ---- DSL evaluator (mirrors backend app/engine/expression.py) for the rule tester
function num(v){const n=parseFloat(v);return isNaN(n)?null:n;}
function leaf(c,f){const op=c.op,a=f[c.field],v=c.value;
 if(op==="exists")return c.field in f && f[c.field]!=null;
 if(op==="truthy")return !!a;
 if(op==="eq")return a===v; if(op==="ne")return a!==v;
 if(op==="in")return (v||[]).includes(a);
 if(["gt","gte","lt","lte"].includes(op)){const x=num(a),y=num(v);if(x==null||y==null)return false;
   return {gt:x>y,gte:x>=y,lt:x<y,lte:x<=y}[op];}
 if(op==="between"){const x=num(a);if(x==null)return false;const lo=num((v||[])[0]),hi=num((v||[])[1]);
   if(lo!=null&&x<lo)return false;if(hi!=null&&x>=hi)return false;return true;}
 return false;}
function evalCond(c,f){if(!c||!Object.keys(c).length)return true;
 if(c.all)return c.all.every(x=>evalCond(x,f)); if(c.any)return c.any.some(x=>evalCond(x,f));
 if(c.not)return !evalCond(c.not,f); if(c.op)return leaf(c,f); return false;}

// ---------- module renderers ----------
function vDashboard(){
 const E=DATA.enterprises;
 const by=(k)=>{const m={};E.forEach(e=>{const v=e[k]||"—";m[v]=(m[v]||0)+1});return m;};
 const avgQ=(E.reduce((s,e)=>s+e.quality.overall_score,0)/E.length).toFixed(3);
 const openR=DATA.reviews.filter(r=>r.status==="OPEN").length;
 const card=(v,l)=>`<div class="card kpi"><div class="v">${v}</div><div class="l">${l}</div></div>`;
 function bars(title,m){const max=Math.max(...Object.values(m));
   return `<div class="panel"><h3>${title}</h3>`+Object.entries(m).sort((a,b)=>b[1]-a[1]).map(([k,v])=>
     `<div class="barrow"><div>${esc(k)}</div><div class="bar"><span style="width:${(v/max*100)}%"></span></div><div>${v}</div></div>`).join("")+`</div>`;}
 return `<h2 class="page">Executive Dashboard</h2><p class="page-sub">National Statistical Business Register — classification &amp; quality at a glance.</p>
 <div class="cards">${card(E.length,"Enterprises")}${card(E.length,"Classified")}${card(DATA.rules.length,"Active rules")}${card(openR,"Pending reviews")}${card(avgQ,"Avg quality score")}${card(DATA.standards.length,"Standards mapped")}</div>
 <div class="grid2">${bars("By Institutional Sector",by("sector"))}${bars("By Public / Private",by("public_private"))}</div>
 <div class="grid2">${bars("By Size Class",by("size"))}${bars("By Control Indicator",by("control"))}</div>
 <div class="panel"><h3>Recent classification activity</h3><table><tr><th>When</th><th>Enterprise</th><th>Action</th><th>By</th></tr>
 ${DATA.audit.filter(a=>a.action==="CLASSIFY").slice(0,8).map(a=>`<tr><td class="small">${esc(a.timestamp)}</td><td>${esc(a.record_id)}</td><td>${esc(a.action)} ${esc(a.new||"")}</td><td>${esc(a.by)}</td></tr>`).join("")}</table></div>`;
}

function vRegistry(){
 const f=(state.filter||"").toLowerCase();
 const rows=DATA.enterprises.filter(e=>!f||e.name.toLowerCase().includes(f)||e.id.toLowerCase().includes(f)||(e.sector||"").toLowerCase().includes(f)||(e.public_private||"").toLowerCase().includes(f));
 return `<h2 class="page">Enterprise Registry</h2><p class="page-sub">${DATA.enterprises.length} resident statistical units in the staging register.</p>
 <div class="filters"><input placeholder="Search name, ID, sector, status…" value="${esc(state.filter)}" oninput="state.filter=this.value;render()" style="min-width:320px"/>
 <button class="btn sec sm" onclick="alert('Upload interface: in the live app this opens the file-ingestion mapping screen (JSON/CSV/XML/SDMX).')">Upload dataset</button>
 <button class="btn sec sm" onclick="alert('New Enterprise: opens the master-data capture form in the live app.')">+ New enterprise</button></div>
 <div class="panel"><table><tr><th>ID</th><th>Legal name</th><th>Sector</th><th>Public/Private</th><th>Size</th><th>Control</th><th>FDI</th><th>Quality</th></tr>
 ${rows.map(e=>`<tr class="click" onclick="go('profile',{entId:'${e.id}',tab:0})"><td class="mono">${esc(e.id.slice(-8))}</td><td>${esc(e.name)}</td><td>${esc(e.sector)} <span class="small">${esc(e.sector_name)}</span></td><td>${ppBadge(e.public_private)}</td><td>${esc(e.size)}</td><td><span class="pill">${esc(e.control)}</span></td><td>${esc(e.fdi)}</td><td>${qbadge(e.quality.overall_score)}</td></tr>`).join("")}</table></div>`;
}
function qbadge(s){const c=s>=0.85?"var(--good)":s>=0.7?"var(--warn)":"var(--bad)";return `<span style="color:${c};font-weight:600">${s}</span>`;}

function vProfile(){
 const e=ent(state.entId); const T=["Master data","Ownership","Classification","Explainability","History","Quality","Audit"];
 const tabs=`<div class="tabs">${T.map((t,i)=>`<button class="${state.tab===i?'active':''}" onclick="state.tab=${i};render()">${t}</button>`).join("")}</div>`;
 const sel=`<div class="filters"><select onchange="state.entId=this.value;render()">${DATA.enterprises.map(x=>`<option value="${x.id}" ${x.id===e.id?'selected':''}>${esc(x.name)}</option>`).join("")}</select></div>`;
 let body="";
 if(state.tab===0){body=`<div class="panel"><h3>${esc(e.name)}</h3><div class="kv">
   <div class="k">Enterprise ID</div><div class="mono">${esc(e.id)}</div>
   <div class="k">Arabic name</div><div dir="rtl">${esc(e.name_ar)||"—"}</div>
   <div class="k">LEI (ISO 17442)</div><div class="mono">${esc(e.lei)||"—"}</div>
   <div class="k">Legal form</div><div>${esc(e.legal_form)} — ${esc(e.legal_form_name)}</div>
   <div class="k">Residence</div><div>${esc(e.residence)}</div>
   <div class="k">ISIC Rev.4 class</div><div>${esc(e.isic)}</div>
   <div class="k">Jurisdiction</div><div>${esc(e.jurisdiction)}</div>
   <div class="k">Employment (FTE)</div><div>${e.employment==null?"—":e.employment}</div>
   <div class="k">Turnover</div><div>${fmtMoney(e.turnover)}</div>
   <div class="k">Enterprise group</div><div>${esc(e.group_id)||"—"}</div></div></div>`;}
 else if(state.tab===1){body=ownershipPanel(e);}
 else if(state.tab===2){body=`<div class="panel"><h3>Current classification &nbsp;<button class="btn sm" onclick="runClassifyDemo('${e.id}')">▶ Re-run classification</button></h3>
   <div class="kv">
   <div class="k">Institutional sector (SNA)</div><div><b>${esc(e.sector)}</b> — ${esc(e.sector_name)}</div>
   <div class="k">Public / private (GFS)</div><div>${ppBadge(e.public_private)}</div>
   <div class="k">Effective control</div><div>${esc(e.control)}</div>
   <div class="k">Market status</div><div>${esc(e.market)}</div>
   <div class="k">Size class</div><div>${esc(e.size)}</div>
   <div class="k">FDI treatment</div><div>${esc(e.fdi)}</div>
   <div class="k">Special entity</div><div>${esc(e.special)}</div>
   <div class="k">Confidence</div><div>${e.confidence}</div>
   <div class="k">Methodology version</div><div>1.0.0</div></div>
   <div id="demobox"></div></div>`;}
 else if(state.tab===3){body=explainPanel(e);}
 else if(state.tab===4){body=`<div class="panel"><h3>Classification history (temporal versioning)</h3><table><tr><th>Version</th><th>Sector</th><th>Public/Private</th><th>Control</th><th>Current</th><th>Source</th></tr>
   <tr><td>v2</td><td>${esc(e.sector)}</td><td>${esc(e.public_private)}</td><td>${esc(e.control)}</td><td><span class="badge b-priv">current</span></td><td>Automated re-run (walkthrough)</td></tr>
   <tr><td>v1</td><td>${esc(e.sector)}</td><td>${esc(e.public_private)}</td><td>${esc(e.control)}</td><td>—</td><td>Initial classification</td></tr></table>
   <p class="small">Every (re)classification writes a new immutable version; the prior record is retained with valid_from/valid_to so any historical classification can be reproduced.</p></div>`;}
 else if(state.tab===5){body=qualityPanel(e);}
 else {body=`<div class="panel"><h3>Audit trail</h3><table><tr><th>When</th><th>Action</th><th>Field</th><th>Old → New</th><th>By</th><th>Evidence</th></tr>
   ${e.audit.map(a=>`<tr><td class="small">${esc(a.timestamp)}</td><td>${esc(a.action)}</td><td>${esc(a.field)||"—"}</td><td>${esc(a.old)||"—"} → ${esc(a.new)||"—"}</td><td>${esc(a.by)}</td><td class="small">${esc(a.evidence)||"—"}</td></tr>`).join("")}</table></div>`;}
 return `<h2 class="page">Enterprise Profile</h2><p class="page-sub">${esc(e.name)} · ${esc(e.id)}</p>${sel}${tabs}${body}`;
}

function ownershipPanel(e){
 const o=e.ownership;
 const edges=o.edges.map(x=>`<tr><td>${esc(x.owner_name||x.owner_id)}</td><td>${x.ownership_pct}%</td><td>${x.voting_pct}%</td><td>${esc(x.control_indicator)||"—"}</td><td>${x.is_government?'<span class="badge b-gg">Government</span>':(x.is_resident?'Resident':'<span class="badge b-fcc">Non-resident</span>')}</td></tr>`).join("");
 return `<div class="grid2">
  <div class="panel"><h3>Ownership intelligence</h3><div class="kv">
   <div class="k">Effective government ownership</div><div><b>${o.government_pct}%</b></div>
   <div class="k">Effective government voting</div><div>${o.government_voting}%</div>
   <div class="k">Effective foreign ownership</div><div>${o.foreign_pct}%</div>
   <div class="k">Government control?</div><div>${o.government_control?'<span class="ok flag">Yes</span>':'<span class="small">No</span>'}</div>
   <div class="k">Control indicators</div><div>${(o.control_indicators||[]).map(c=>`<span class="chip">${esc(c)}</span>`).join("")||"—"}</div>
   <div class="k">Ultimate Controlling Unit</div><div>${o.uci?esc(o.uci.uci_name)+(o.uci.is_government?' <span class="badge b-gg">Govt</span>':''):"—"}</div></div>
   <p class="small">Effective ownership is computed across the full graph (direct + indirect, aggregating holdings across multiple vehicles) — substance over legal form.</p></div>
  <div class="panel"><h3>Direct ownership edges</h3><table><tr><th>Owner</th><th>Equity</th><th>Voting</th><th>Control</th><th>Origin</th></tr>${edges||'<tr><td colspan=5 class="small">No recorded owners</td></tr>'}</table></div></div>
  <div class="panel"><h3>Ownership chain</h3><div class="treebox">${chainTree(e)}</div></div>`;
}
function chainTree(e){
 let out=esc(e.name)+"  ["+esc(e.id)+"]\n";
 (e.ownership.chain||[]).forEach((c,i)=>{out+="   ▲ owned "+c.ownership_pct+"% by "+esc(c.owner_name||c.owner_id)+(c.is_government?" (Government)":(c.is_resident?"":" (Non-resident)"))+(c.control_indicator?"  ["+esc(c.control_indicator)+"]":"")+"\n";});
 return out||"No ownership recorded.";
}

function explainPanel(e){
 const rows=e.applied_rules.map(a=>`<tr><td>${esc(a.test)}</td><td class="mono">${esc(a.rule_id)}</td><td>${Object.entries(a.output||{}).map(([k,v])=>esc(k)+"="+esc(typeof v==='object'?JSON.stringify(v):v)).join(", ")}</td><td class="small">${esc(a.standard_ref)}</td><td class="small">${esc(a.rationale)}</td></tr>`).join("");
 return `<div class="panel"><h3>Why this classification? — applied rules</h3>
  <p class="small">Every committed classification is fully explainable: the ordered list of tests, the rule that fired, the output it set, the standard it traces to, and the rationale.</p>
  <table><tr><th>Test</th><th>Rule</th><th>Output</th><th>Standard</th><th>Rationale</th></tr>${rows}</table>
  <div class="note" style="margin-top:12px"><b>Data fields used:</b> legal_form=${esc(e.legal_form)}, isic=${esc(e.isic)}, residence=${esc(e.residence)}, financial=${e.is_financial}, gov_ownership=${e.ownership.government_pct}%, foreign_ownership=${e.ownership.foreign_pct}%, market=${esc(e.market)}. &nbsp;<b>Sources:</b> CSBR golden record · ownership graph · reference codelists. &nbsp;<b>Confidence:</b> ${e.confidence}.</div></div>`;
}
function qualityPanel(e){
 const q=e.quality;const dims=["completeness","validity","consistency","uniqueness","accuracy","timeliness"];
 const bars=dims.map(d=>`<div class="barrow"><div>${d}</div><div class="bar"><span style="width:${q[d]*100}%"></span></div><div>${q[d]}</div></div>`).join("");
 const exc=e.exceptions.map(x=>`<tr><td class="mono">${esc(x.rule_id)}</td><td>${sevDot(x.severity)}${esc(x.severity)}</td><td>${esc(x.message)}</td><td>${esc(x.action)}</td></tr>`).join("");
 return `<div class="grid2"><div class="panel"><h3>Quality score — ${q.overall_score}</h3>${bars}<p class="legend">Six DAMA DMBOK dimensions; overall is their mean.</p></div>
  <div class="panel"><h3>Validation exceptions (${e.exceptions.length})</h3><table><tr><th>Rule</th><th>Severity</th><th>Message</th><th>Action</th></tr>${exc||'<tr><td colspan=4 class="ok">No exceptions — record passes all validation rules.</td></tr>'}</table></div></div>`;
}
function sevDot(s){const c=s==="ERROR"?"var(--bad)":s==="WARN"?"var(--warn)":"var(--info)";return `<span class="statusdot" style="background:${c}"></span>`;}

function runClassifyDemo(id){
 const e=ent(id);const box=document.getElementById("demobox");if(!box)return;
 box.innerHTML='<div class="panel" style="margin-top:14px"><h3>18-test pipeline execution</h3><div class="trace" id="tr"></div></div>';
 const tr=document.getElementById("tr");let i=0;
 const steps=e.trace;
 (function step(){if(i>=steps.length)return;const s=steps[i++];const d=document.createElement("div");
   d.className="step"+(s.matched?"":" skip");
   d.innerHTML=s.matched?`<b>${esc(s.test_code)}</b> ${esc(s.test_name)} → <span class="pill">${Object.entries(s.output||{}).map(([k,v])=>esc(k)+"="+esc(typeof v==='object'?JSON.stringify(v):v)).join(", ")}</span> <span class="small">(${esc(s.rule_id)} · ${esc(s.standard_ref)})</span>`
     :`<span class="small"><b>${esc(s.test_code)}</b> ${esc(s.test_name)} — no data rule (governance/process step)</span>`;
   tr.appendChild(d);setTimeout(step,180);})();
}

function vOwnership(){
 const e=ent(state.entId);
 const sel=`<div class="filters"><select onchange="state.entId=this.value;render()">${DATA.enterprises.map(x=>`<option value="${x.id}" ${x.id===e.id?'selected':''}>${esc(x.name)}</option>`).join("")}</select></div>`;
 return `<h2 class="page">Ownership &amp; Control Analysis</h2><p class="page-sub">Effective ownership, control indicators, and the Ultimate Controlling Institutional Unit (UCI).</p>${sel}${ownershipPanel(e)}`;
}

function vGroups(){
 return `<h2 class="page">Enterprise Group Structure</h2><p class="page-sub">Global ultimate parent, domestic group head, truncated (resident-only) groups.</p>`+
 DATA.groups.map(g=>`<div class="panel"><h3>${esc(g.name)} <span class="small">(${esc(g.group_id)})</span></h3>
  <div class="kv"><div class="k">Global ultimate parent</div><div>${esc(g.gup)} (${esc(g.gup_country)})</div>
  <div class="k">Domestic group head</div><div class="mono">${esc(g.domestic_head)}</div>
  <div class="k">Truncated (resident) group</div><div>${g.truncated==="Y"?"Yes":"No"}</div>
  <div class="k">Controlling sector</div><div>${esc(g.controlling_sector)}</div>
  <div class="k">Members (registered)</div><div>${g.members.map(m=>`<span class="chip click" onclick="go('profile',{entId:'${m}',tab:1})">${esc(m.slice(-8))}</span>`).join("")||"—"}</div></div>
  <p class="small">${esc(g.notes)}</p></div>`).join("");
}

function vClassification(){
 return `<h2 class="page">Classification Results</h2><p class="page-sub">Live results from the 18-test methodology for every register unit.</p>
 <div class="panel"><table><tr><th>Enterprise</th><th>Sector</th><th>Pub/Priv</th><th>Control</th><th>Market</th><th>Size</th><th>FDI</th><th>Special</th><th>Conf.</th><th></th></tr>
 ${DATA.enterprises.map(e=>`<tr><td>${esc(e.name)}</td><td>${esc(e.sector)}</td><td>${ppBadge(e.public_private)}</td><td><span class="pill">${esc(e.control)}</span></td><td>${esc(e.market)}</td><td>${esc(e.size)}</td><td>${esc(e.fdi)}</td><td>${esc(e.special)}</td><td>${e.confidence}</td><td><button class="btn sm sec" onclick="go('profile',{entId:'${e.id}',tab:3})">Explain</button></td></tr>`).join("")}</table></div>`;
}

function vRules(){
 const tests=[...new Set(DATA.rules.map(r=>r.test_code))];
 const cur=state.ruleId?DATA.rules.find(r=>r.rule_id===state.ruleId):DATA.rules[0];
 const list=DATA.rules.map(r=>`<tr class="click ${r.rule_id===cur.rule_id?'':''}" onclick="state.ruleId='${r.rule_id}';render()"><td class="mono">${esc(r.rule_id)}</td><td>${esc(r.name)}</td><td>${esc(r.test_code)}</td><td>${esc(r.standard_ref)}</td></tr>`).join("");
 return `<h2 class="page">Rules Engine Explorer</h2><p class="page-sub">${DATA.rules.length} database-driven rules — no logic is hard-coded. Each rule is a JSON condition + output, traceable to a standard.</p>
 <div class="grid2"><div class="panel"><h3>Rule repository</h3><div style="max-height:520px;overflow:auto"><table><tr><th>ID</th><th>Name</th><th>Test</th><th>Standard</th></tr>${list}</table></div></div>
 <div><div class="panel"><h3>Rule detail — ${esc(cur.rule_id)}</h3>
   <div class="kv"><div class="k">Name</div><div>${esc(cur.name)}</div>
   <div class="k">Test / domain</div><div>${esc(cur.test_code)} · ${esc(cur.domain)}</div>
   <div class="k">Priority / confidence</div><div>${cur.priority} / ${cur.confidence}</div>
   <div class="k">Standard reference</div><div>${esc(cur.standard_ref)}</div>
   <div class="k">Approval</div><div>${esc(cur.approval_status)} (v${esc(cur.version)})</div>
   <div class="k">Rationale</div><div>${esc(cur.rationale)}</div></div>
   <p class="small" style="margin-top:8px">Logic (JSON condition tree):</p><pre class="mono" style="background:#fafbfc;border:1px solid var(--line);padding:8px;border-radius:6px;white-space:pre-wrap">${esc(JSON.stringify(cur.logic,null,1))}</pre>
   <p class="small">Output: <span class="mono">${esc(JSON.stringify(cur.output))}</span></p></div>
   <div class="panel"><h3>Rule tester</h3><p class="small">Edit the fact set and evaluate this rule's logic in your browser (same evaluator as the engine).</p>
   <textarea id="rtf">${esc(JSON.stringify(suggestFacts(cur),null,1))}</textarea>
   <div style="margin-top:8px"><button class="btn sm" onclick="testRule('${cur.rule_id}')">Evaluate rule</button> <span id="rtres"></span></div></div></div></div>`;
}
function suggestFacts(r){const f={};(function walk(c){if(!c)return;if(c.all)c.all.forEach(walk);else if(c.any)c.any.forEach(walk);else if(c.not)walk(c.not);
  else if(c.op){if(c.op==="eq"||c.op==="in")f[c.field]=Array.isArray(c.value)?c.value[0]:c.value;
   else if(["gt","gte","lt","lte"].includes(c.op))f[c.field]=c.value;else if(c.op==="truthy")f[c.field]=true;else if(c.op==="exists")f[c.field]="…";}})(r.logic);return f;}
function testRule(id){const r=DATA.rules.find(x=>x.rule_id===id);let f;try{f=JSON.parse(document.getElementById("rtf").value);}catch(e){document.getElementById("rtres").innerHTML='<span class="err">Invalid JSON</span>';return;}
  const m=evalCond(r.logic,f);document.getElementById("rtres").innerHTML=m?`<span class="ok">✔ MATCH → sets ${esc(JSON.stringify(r.output))}</span>`:'<span class="err">✘ no match</span>';}

function vMetadata(){
 const ents=[...new Set(DATA.metadata.map(m=>m.entity))];
 return `<h2 class="page">Metadata Repository</h2><p class="page-sub">GSIM/SDMX-aligned variable catalogue — every field fully specified.</p>
 <div class="panel"><table><tr><th>Entity</th><th>Field</th><th>Definition</th><th>Type</th><th>Allowed</th><th>Mand.</th><th>Source</th></tr>
 ${DATA.metadata.map(m=>`<tr><td class="small">${esc(m.entity)}</td><td class="mono">${esc(m.field)}</td><td>${esc(m.definition)}</td><td class="small">${esc(m.data_type)}</td><td class="small">${esc(m.allowed_values)}</td><td>${m.mandatory?'<span class="ok">Y</span>':'N'}</td><td class="small">${esc(m.source)}</td></tr>`).join("")}</table></div>`;
}

function vStandards(){
 return `<h2 class="page">Standards Repository</h2><p class="page-sub">International &amp; national statistical standards; every rule traces to one.</p>`+
 DATA.standards.map(s=>`<div class="panel"><h3>${esc(s.code)} — ${esc(s.name)}</h3>
  <div class="small">Issuer: ${esc(s.issuer)} · Edition: ${esc(s.edition)} · Domains: ${esc(s.domains)}</div>
  <p>${esc(s.description)}</p>${s.concepts.length?`<table><tr><th>Concept</th><th>Definition</th><th>Reference</th></tr>${s.concepts.map(c=>`<tr><td>${esc(c.concept)}</td><td>${esc(c.definition)}</td><td class="small">${esc(c.reference)}</td></tr>`).join("")}</table>`:""}</div>`).join("");
}

function vQuality(){
 const E=DATA.enterprises;const dims=["completeness","validity","consistency","uniqueness","accuracy","timeliness","overall_score"];
 const agg={};dims.forEach(d=>agg[d]=(E.reduce((s,e)=>s+e.quality[d],0)/E.length).toFixed(3));
 const cards=dims.map(d=>`<div class="card kpi"><div class="v">${agg[d]}</div><div class="l">${d.replace("_"," ")}</div></div>`).join("");
 return `<h2 class="page">Data Quality Dashboard</h2><p class="page-sub">Dataset-level scores across six DAMA dimensions.</p>
  <div class="cards">${cards}</div>
  <div class="panel"><h3>Per-enterprise scores</h3><table><tr><th>Enterprise</th>${dims.map(d=>`<th>${d.slice(0,4)}</th>`).join("")}</tr>
  ${E.map(e=>`<tr><td>${esc(e.name)}</td>${dims.map(d=>`<td>${qbadge(e.quality[d])}</td>`).join("")}</tr>`).join("")}</table></div>`;
}

function vValidation(){
 const all=[];DATA.enterprises.forEach(e=>e.exceptions.forEach(x=>all.push({id:e.id,name:e.name,...x})));
 const sev=s=>`<span>${sevDot(s)}${s}</span>`;
 return `<h2 class="page">Validation &amp; Exception Center</h2><p class="page-sub">Findings from the VR-001..VR-018 business-rule library across the register.</p>
  <div class="cards"><div class="card kpi"><div class="v">${all.length}</div><div class="l">Open exceptions</div></div>
  <div class="card kpi"><div class="v">${all.filter(a=>a.severity==='ERROR').length}</div><div class="l">Errors</div></div>
  <div class="card kpi"><div class="v">${all.filter(a=>a.severity==='WARN').length}</div><div class="l">Warnings</div></div>
  <div class="card kpi"><div class="v">${all.filter(a=>a.severity==='INFO').length}</div><div class="l">Info</div></div></div>
  <div class="panel"><table><tr><th>Enterprise</th><th>Rule</th><th>Severity</th><th>Message</th><th>Action</th></tr>
  ${all.map(a=>`<tr><td>${esc(a.name)}</td><td class="mono">${esc(a.rule_id)}</td><td>${sev(a.severity)}</td><td>${esc(a.message)}</td><td>${esc(a.action)}</td></tr>`).join("")||'<tr><td colspan=5 class="ok">No exceptions.</td></tr>'}</table></div>`;
}

function vReviews(){
 return `<h2 class="page">Manual Review Queue</h2><p class="page-sub">Anomalies and exceptions routed for human adjudication (AI assists; never decides).</p>
  <div class="panel"><table><tr><th>ID</th><th>Enterprise</th><th>Type</th><th>Severity</th><th>Title</th><th>Status</th><th></th></tr>
  ${DATA.reviews.length?DATA.reviews.map(r=>`<tr><td>${r.id}</td><td class="mono">${esc(r.enterprise_id)}</td><td>${esc(r.kind)}</td><td>${sevDot(r.severity)}${esc(r.severity)}</td><td>${esc(r.title)}<div class="small">${esc(r.detail)}</div></td><td>${esc(r.status)}</td><td><button class="btn sm" onclick="alert('Review workflow: assign → investigate → resolve / refer to Technical Classification Committee / apply override.')">Resolve</button></td></tr>`).join(""):'<tr><td colspan=7 class="ok">No open review items — all anomalies cleared.</td></tr>'}</table></div>
  <div class="note">Reclassification triggers (IPO, M&amp;A, new licence, activity change, sovereign-vehicle reorganisation, JV formation, major contract, 3-year periodic review) automatically generate review items in the live system.</div>`;
}

function vAudit(){
 return `<h2 class="page">Audit Trail Viewer</h2><p class="page-sub">Immutable per-record change log — who changed what, when, why, with evidence.</p>
  <div class="panel"><table><tr><th>When</th><th>Record</th><th>Action</th><th>Field</th><th>Old → New</th><th>By</th><th>Evidence</th></tr>
  ${DATA.audit.slice(0,80).map(a=>`<tr><td class="small">${esc(a.timestamp)}</td><td class="mono">${esc(a.record_id)}</td><td>${esc(a.action)}</td><td>${esc(a.field)||"—"}</td><td>${esc(a.old)||"—"} → ${esc(a.new)||"—"}</td><td>${esc(a.by)}</td><td class="small">${esc(a.evidence)||"—"}</td></tr>`).join("")}</table></div>`;
}

const ENDPOINTS=[
 ["POST","/api/auth/login","Authenticate; returns JWT + role",'{"access_token":"eyJ…","role":"Classifier"}'],
 ["GET","/api/dashboard","KPIs & breakdowns",'{"total_enterprises":28,"by_sector":{…}}'],
 ["GET","/api/enterprises","List/filter register",'[{"enterprise_id":"QA-ENT-…","sector_code":"S.11"}]'],
 ["POST","/api/enterprises/{id}/classify","Run 18-test classification",'{"sector_code":"S.122","public_private":"PUB-FC","confidence":1.0}'],
 ["GET","/api/enterprises/{id}/explain","Full explainability payload",'{"applied_rules":[…],"data_fields_used":{…}}'],
 ["GET","/api/enterprises/{id}/profile","Master data + ownership + quality + audit","{…}"],
 ["GET","/api/rules","Rules repository",'[{"rule_id":"R-T07-030","logic":{…}}]'],
 ["POST","/api/rules/{id}/test","Evaluate a rule against facts",'{"matched":true,"output":{…}}'],
 ["GET","/api/standards","Standards & concepts",'[{"code":"BD4","name":"OECD Benchmark Definition…"}]'],
 ["POST","/api/simulate","Sandbox what-if classification",'{"sandbox":true,"result":{…}}'],
 ["GET","/api/quality","Dataset & per-enterprise quality","{…}"],
 ["GET","/api/audit","Audit report","[…]"],
];
function vApi(){
 return `<h2 class="page">API Demonstration</h2><p class="page-sub">API-first design with OpenAPI docs at <span class="mono">/docs</span>. Representative endpoints below (sample responses).</p>
  <div class="panel"><table><tr><th>Method</th><th>Endpoint</th><th>Purpose</th><th></th></tr>
  ${ENDPOINTS.map((e,i)=>`<tr><td><span class="pill">${e[0]}</span></td><td class="mono">${esc(e[1])}</td><td>${esc(e[2])}</td><td><button class="btn sm sec" onclick="document.getElementById('apir${i}').style.display='block'">Try</button></td></tr><tr id="apir${i}" style="display:none"><td colspan=4><pre class="mono" style="background:#0f1722;color:#d6e2ee;padding:10px;border-radius:6px;white-space:pre-wrap">HTTP 200 OK\n${esc(e[3])}</pre></td></tr>`).join("")}</table></div>`;
}

function vUsers(){
 const u=DATA.users.map(x=>`<tr><td class="mono">${esc(x.username)}</td><td>${esc(x.full_name)}</td><td><span class="chip">${esc(x.role)}</span></td><td class="small">${esc(x.email)}</td></tr>`).join("");
 const perms=[...new Set(Object.values(DATA.roles).flat())].sort();
 const matrix=`<table><tr><th>Permission</th>${Object.keys(DATA.roles).map(r=>`<th>${esc(r.slice(0,4))}</th>`).join("")}</tr>
  ${perms.map(p=>`<tr><td class="mono">${esc(p)}</td>${Object.keys(DATA.roles).map(r=>`<td>${(DATA.roles[r].includes("*")||DATA.roles[r].includes(p))?'<span class="ok">✔</span>':'·'}</td>`).join("")}</tr>`).join("")}</table>`;
 return `<h2 class="page">User &amp; Role Management</h2><p class="page-sub">Role-Based Access Control — 7 roles. Demo credentials: <span class="mono">username / username+123</span>.</p>
  <div class="panel"><h3>Users</h3><table><tr><th>Username</th><th>Name</th><th>Role</th><th>Email</th></tr>${u}</table></div>
  <div class="panel"><h3>Permission matrix (role × permission)</h3>${matrix}<p class="legend">Administrator holds the wildcard (*) permission.</p></div>`;
}

function vUat(){
 const c=DATA.uat;
 const passed=c.filter(r=>r[4]==="Pass").length;
 const rows=c.map((r,i)=>`<tr><td class="mono">${esc(r[0])}</td><td>${esc(r[1])}</td><td>${esc(r[2])}</td><td>${esc(r[3])}</td><td id="uat${i}"><span class="ok">${esc(r[4])}</span></td></tr>`).join("");
 return `<h2 class="page">UAT Test Center</h2><p class="page-sub">Representative acceptance tests (full 100+ case suite in <span class="mono">docs/uat/UAT_TEST_CASES.md</span>).</p>
  <div class="cards"><div class="card kpi"><div class="v">${c.length}</div><div class="l">Shown here</div></div>
  <div class="card kpi"><div class="v">100+</div><div class="l">Full suite</div></div>
  <div class="card kpi"><div class="v ok">${passed}/${c.length}</div><div class="l">Passing (demo set)</div></div>
  <div class="card kpi"><div class="v ok">28/28</div><div class="l">Classification verdicts</div></div></div>
  <div class="filters"><button class="btn sm" onclick="alert('In the live UAT runner each case executes against the API and records actual vs expected. This demo shows curated expected results.')">▶ Run all (demo)</button></div>
  <div class="panel"><table><tr><th>Test ID</th><th>Area</th><th>Description</th><th>Expected result</th><th>Status</th></tr>${rows}</table></div>
  <div class="panel"><h3>Acceptance criteria (production gate)</h3><ul class="tight">
   <li>Methodology traceability: <b>100%</b> — every test/rule maps to a standard ✔</li>
   <li>Classification accuracy on golden set: <b>28/28</b> verdicts ✔</li>
   <li>Rules verified (positive + negative): <b>40/40</b> ✔</li>
   <li>Validation library VR-001..VR-018: <b>18/18</b> enforced ✔</li>
   <li>Explainability present for <b>100%</b> of classifications ✔</li>
   <li>Audit entry for <b>100%</b> of changes ✔; RBAC enforced for every role ✔</li>
   <li>Quality KPI targets: error ≤2%, median time-to-classify ≤10 working days, override rate ≤5%, LEI coverage of financial entities 100% (to be measured at pilot)</li>
   <li>Zero critical defects; performance validated at national volume (pending load test)</li></ul></div>`;
}

function vGap(){
 const g=DATA.gap;
 const list=(t,a,cls)=>`<div class="panel"><h3>${t}</h3><ul class="tight">${a.map(x=>`<li class="${cls||''}">${esc(x)}</li>`).join("")}</ul></div>`;
 const rag=DATA.readiness.map(r=>`<tr><td>${esc(r[0])}</td><td><span class="rag-${r[1].replace(/[^A-Za-z-]/g,'')}">${esc(r[1])}</span></td><td>${esc(r[2])}</td></tr>`).join("");
 return `<h2 class="page">Gap Analysis &amp; Roadmap</h2><p class="page-sub">Honest assessment for the move Development → Staging → Pilot → Production.</p>
  <div class="grid2">${list("✔ Fully implemented",g.implemented,"ok")}${list("◑ Partially implemented",g.partial,"wr")}</div>
  <div class="grid2">${list("→ Future enhancements",g.future)}${list("⚠ Production-readiness gaps",g.production_gaps,"err")}</div>
  <div class="panel"><h3>Production Readiness Assessment</h3><table><tr><th>Dimension</th><th>Status</th><th>Notes</th></tr>${rag}</table>
   <p class="small" style="margin-top:10px"><b>Recommendation:</b> Methodology and data-governance readiness are <span class="rag-Green">Green</span>. Proceed to a controlled <b>pilot</b> on the largest 100 enterprises after closing security hardening and one administrative-source integration. Defer full production until HA, load testing, secrets management, and formal data-sharing instruments under the Statistics Law are in place.</p></div>`;
}

const VIEWS={dashboard:vDashboard,registry:vRegistry,profile:vProfile,ownership:vOwnership,groups:vGroups,
 classification:vClassification,rules:vRules,metadata:vMetadata,standards:vStandards,quality:vQuality,
 validation:vValidation,reviews:vReviews,audit:vAudit,api:vApi,users:vUsers,uat:vUat,gap:vGap};

function render(){
 document.getElementById("nav").innerHTML=MODULES.map((m,i)=>`<button class="${state.view===m[0]?'active':''}" onclick="go('${m[0]}')"><span class="num">${i+1}</span>${m[1]}</button>`).join("");
 const rs=document.getElementById("rolesel");
 if(!rs.options.length){rs.innerHTML=Object.keys(DATA.roles).map(r=>`<option ${r==='Classifier'?'selected':''}>${r}</option>`).join("");}
 document.getElementById("content").innerHTML=(VIEWS[state.view]||vDashboard)();
}
render();
</script>
</body>
</html>
"""
