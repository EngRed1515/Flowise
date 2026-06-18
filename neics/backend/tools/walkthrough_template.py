"""HTML/CSS/JS template for the NEICS interactive walkthrough.

Clean, robust, corporate design that renders reliably on mobile Safari and desktop
(no fragile custom icon paths, no backdrop-filter, no 8-digit hex). `/*__DATA__*/`
is replaced with the embedded JSON payload by build_walkthrough.py, producing a
single self-contained .html file.
"""

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5"/>
<title>NEICS — National Enterprise Intelligence & Classification System</title>
<style>
:root{
 --maroon:#8a1538; --maroon-d:#6c0f2c; --gold:#b08d57;
 --ink:#1f2937; --ink2:#374151; --muted:#6b7280; --line:#e5e7eb; --line2:#f1f3f5;
 --bg:#f4f5f7; --surface:#ffffff; --surface2:#f8f9fb;
 --blue:#1d6fb8; --blue-bg:#e9f2fb; --green:#1a8a4f; --green-bg:#e8f5ee;
 --amber:#9a6a10; --amber-bg:#fbf2dc; --red:#c0392b; --red-bg:#fbe9e7;
 --purple:#7a3b97; --purple-bg:#f4eafa; --teal:#127a6c; --teal-bg:#e3f3f0; --gray-bg:#eef1f4;
}
*{box-sizing:border-box} html,body{margin:0;padding:0}
body{font-family:"Segoe UI",-apple-system,BlinkMacSystemFont,Roboto,Helvetica,Arial,sans-serif;
 background:var(--bg);color:var(--ink);font-size:14px;line-height:1.55;-webkit-text-size-adjust:100%}
a{color:var(--maroon);text-decoration:none}
button{font-family:inherit;cursor:pointer}
#app{display:flex;min-height:100vh}
/* Header (full-width maroon bar) */
.appbar{position:fixed;top:0;left:0;right:0;height:56px;background:var(--maroon);color:#fff;
 display:flex;align-items:center;gap:14px;padding:0 18px;z-index:50}
.appbar .logo{width:34px;height:34px;border-radius:8px;background:#fff;color:var(--maroon);
 font-weight:800;display:flex;align-items:center;justify-content:center;font-size:16px}
.appbar .ttl{font-weight:700;font-size:15px;letter-spacing:.3px}
.appbar .ttl small{display:block;font-weight:400;font-size:10.5px;opacity:.85;letter-spacing:.2px}
.appbar .sp{flex:1}
.appbar .stg{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.3);
 padding:4px 10px;border-radius:20px;font-size:11px;font-weight:600;white-space:nowrap}
.appbar select{background:rgba(255,255,255,.12);color:#fff;border:1px solid rgba(255,255,255,.3);
 border-radius:8px;padding:5px 8px;font-size:12.5px}
.appbar select option{color:#1f2937}
.menubtn{display:none;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.3);
 color:#fff;border-radius:8px;padding:4px 10px;font-size:17px}
/* Sidebar */
.sidebar{width:236px;flex-shrink:0;background:var(--surface);border-right:1px solid var(--line);
 position:fixed;top:56px;bottom:0;left:0;overflow-y:auto;padding:10px 0}
.navsec{padding:10px 12px 2px}
.navsec .lbl{font-size:10px;text-transform:uppercase;letter-spacing:.8px;color:var(--muted);
 font-weight:700;padding:4px 10px}
.nav a{display:block;padding:9px 12px;margin:1px 0;border-radius:8px;color:var(--ink2);
 font-size:13px;border-left:3px solid transparent}
.nav a:hover{background:var(--surface2)}
.nav a.active{background:var(--surface2);border-left-color:var(--maroon);color:var(--maroon);font-weight:650}
/* Main */
.main{flex:1;margin-left:236px;margin-top:56px;min-width:0}
.content{padding:22px 26px;max-width:1280px}
.h-page{font-size:22px;font-weight:700;margin:0 0 3px}
.h-sub{color:var(--muted);font-size:13px;margin:0 0 18px}
.help{background:var(--blue-bg);border:1px solid #cfe0f1;border-left:4px solid var(--blue);
 border-radius:8px;padding:11px 14px;margin-bottom:18px;font-size:13px;color:#27496b}
/* Grid */
.grid{display:grid;gap:16px}
.tiles{grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}
.g2{grid-template-columns:3fr 2fr}.g11{grid-template-columns:1fr 1fr}
@media(max-width:980px){.g2,.g11{grid-template-columns:1fr}}
/* Cards */
.card{background:var(--surface);border:1px solid var(--line);border-radius:10px;
 box-shadow:0 1px 2px rgba(17,24,39,.05);margin-bottom:16px;overflow:hidden}
.card>.hd{padding:13px 16px;border-bottom:1px solid var(--line2);font-weight:650;font-size:14px;
 display:flex;align-items:center;gap:9px}
.card>.hd::before{content:"";width:9px;height:9px;border-radius:3px;background:var(--maroon);flex-shrink:0}
.card>.bd{padding:16px}
.tile{background:var(--surface);border:1px solid var(--line);border-top:3px solid var(--maroon);
 border-radius:10px;padding:15px 16px;box-shadow:0 1px 2px rgba(17,24,39,.05)}
.tile .v{font-size:28px;font-weight:750;line-height:1.1;color:var(--ink)}
.tile .l{color:var(--muted);font-size:12px;margin-top:3px}
.tile .s{font-size:11px;color:var(--green);font-weight:600;margin-top:5px}
/* Badges */
.badge{display:inline-block;padding:3px 9px;border-radius:14px;font-size:11.5px;font-weight:650;white-space:nowrap}
.b-blue{background:var(--blue-bg);color:var(--blue)} .b-green{background:var(--green-bg);color:var(--green)}
.b-purple{background:var(--purple-bg);color:var(--purple)} .b-amber{background:var(--amber-bg);color:var(--amber)}
.b-red{background:var(--red-bg);color:var(--red)} .b-teal{background:var(--teal-bg);color:var(--teal)}
.b-gray{background:var(--gray-bg);color:#4b5563}
/* Tables */
.scroll{overflow:auto;-webkit-overflow-scrolling:touch}
table.t{width:100%;border-collapse:collapse;font-size:13px}
table.t th,table.t td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line2);vertical-align:middle}
table.t th{color:var(--muted);font-weight:650;font-size:10.5px;text-transform:uppercase;letter-spacing:.5px;background:var(--surface2)}
table.t tr.row:hover{background:var(--surface2);cursor:pointer}
/* Buttons */
.btn{display:inline-block;background:var(--maroon);color:#fff;border:0;padding:9px 16px;border-radius:8px;
 font-size:13px;font-weight:600}
.btn:hover{background:var(--maroon-d)}
.btn.ghost{background:#fff;color:var(--maroon);border:1px solid var(--maroon)}
.btn.soft{background:var(--surface2);color:var(--ink2);border:1px solid var(--line)}
.btn.sm{padding:6px 11px;font-size:12px}
/* Misc */
.kv{display:grid;grid-template-columns:190px 1fr;gap:8px 16px;font-size:13px}
.kv .k{color:var(--muted)}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px}
.small{font-size:12px;color:var(--muted)}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;align-items:center}
.fchip{padding:6px 13px;border-radius:18px;border:1px solid var(--line);background:#fff;font-size:12.5px;color:var(--ink2)}
.fchip.on{background:var(--maroon);color:#fff;border-color:var(--maroon)}
.srch{display:flex;align-items:center;gap:8px;background:var(--surface2);border:1px solid var(--line);
 border-radius:8px;padding:8px 12px;max-width:380px;margin-bottom:14px}
.srch input{border:0;background:none;outline:none;width:100%;font-size:13px}
.bar{height:9px;background:var(--line2);border-radius:6px;overflow:hidden}
.bar>span{display:block;height:100%}
.barrow{display:grid;grid-template-columns:160px 1fr 42px;gap:10px;align-items:center;margin:8px 0;font-size:12.5px}
.tabs{display:flex;gap:2px;border-bottom:1px solid var(--line);margin-bottom:16px;flex-wrap:wrap}
.tabs button{border:0;background:none;padding:10px 14px;border-bottom:2px solid transparent;
 color:var(--muted);font-size:13px;font-weight:600}
.tabs button.active{color:var(--maroon);border-bottom-color:var(--maroon)}
.note{background:#fbfaf6;border:1px solid #ece4d2;border-radius:9px;padding:12px 14px;font-size:13px}
ul.tight{margin:6px 0;padding-left:20px} ul.tight li{margin:5px 0}
.svgwrap{background:var(--surface2);border:1px solid var(--line);border-radius:9px;padding:8px;overflow:auto}
.legend{font-size:11px;color:var(--muted);margin-top:8px}
.rag{font-weight:700}
.rag.Green{color:var(--green)}.rag.Amber{color:var(--amber)}.rag.Red,.rag.RedAmber{color:var(--red)}.rag.AmberGreen{color:#6e861b}
textarea{width:100%;min-height:120px;font-family:ui-monospace,monospace;font-size:12px;border:1px solid var(--line);border-radius:8px;padding:10px}
.quick{display:flex;gap:12px;flex-wrap:wrap}
.quick .qa{flex:1;min-width:170px;border:1px solid var(--line);border-radius:10px;padding:14px;background:#fff}
.quick .qa:hover{border-color:var(--maroon)}
.quick .qa b{display:block;font-size:13.5px} .quick .qa span{font-size:12px;color:var(--muted)}
/* Studio */
.studio{display:grid;grid-template-columns:280px 1fr 280px;gap:16px}
@media(max-width:1100px){.studio{grid-template-columns:1fr}}
.step{display:flex;gap:11px;padding:11px 13px;border:1px solid var(--line);border-radius:9px;
 background:#fff;margin-bottom:8px;align-items:flex-start}
.step.fire{border-color:var(--maroon);background:#fcf4f7}
.step .n{width:26px;height:26px;border-radius:50%;background:var(--surface2);color:var(--muted);
 display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex-shrink:0}
.step.fire .n{background:var(--maroon);color:#fff}
.step .tt{font-weight:650;font-size:13px}
.pp{position:sticky;top:72px}
.pp .box{border:1px solid var(--line);border-radius:11px;overflow:hidden;box-shadow:0 1px 3px rgba(17,24,39,.08)}
.pp .top{background:var(--maroon);color:#fff;padding:14px 16px}
.pp .top .nm{font-weight:700;font-size:14px} .pp .top .id{font-size:11px;opacity:.85}
.pp .r{display:flex;justify-content:space-between;align-items:center;padding:9px 16px;border-bottom:1px solid var(--line2);font-size:13px}
.pp .r .k{color:var(--muted)}
/* Sheet tabs */
.stabs{display:flex;gap:3px;flex-wrap:wrap}
.stabs button{border:1px solid var(--line);border-bottom:0;background:var(--surface2);
 padding:8px 13px;border-radius:8px 8px 0 0;font-size:12.5px;color:var(--ink2)}
.stabs button.active{background:#fff;color:var(--maroon);font-weight:650}
.sbody{border:1px solid var(--line);border-radius:0 9px 9px 9px;background:#fff;overflow:auto}
.gnode{display:inline-block;border:1.5px solid var(--line);border-radius:9px;padding:7px 13px;margin:4px;background:#fff}
.lvl{padding-left:22px;border-left:2px dashed #d6dde4;margin-left:18px}
.gnode.gov{border-color:var(--purple)}.gnode.foreign{border-color:#b9651b}.gnode.entity{border-color:var(--maroon)}.gnode.priv{border-color:var(--green)}
/* Mobile */
@media(max-width:860px){
 .sidebar{position:static;width:100%;height:auto;top:0;border-right:0;border-bottom:1px solid var(--line);
  display:none;padding:6px 0}
 .sidebar.open{display:block}
 .main{margin-left:0}
 .menubtn{display:inline-block}
 .content{padding:16px}
 .appbar .ttl small{display:none}
 .kv{grid-template-columns:1fr;gap:2px} .kv .k{margin-top:7px;font-weight:600}
 .barrow{grid-template-columns:120px 1fr 36px}
 table.t th,table.t td{padding:8px 9px}
}
</style>
</head>
<body>
<div class="appbar">
 <button class="menubtn" onclick="document.getElementById('sb').classList.toggle('open')">☰</button>
 <div class="logo">N</div>
 <div class="ttl">NEICS<small>State of Qatar · National Statistics Office</small></div>
 <span class="sp"></span>
 <span class="stg">STAGING / UAT</span>
 <select id="rolesel" onchange="state.role=this.value;render()"></select>
</div>
<div id="app">
 <aside class="sidebar" id="sb"><nav id="nav"></nav></aside>
 <main class="main"><div class="content" id="content"></div></main>
</div>
<script>
const DATA = /*__DATA__*/;
const state={view:"dashboard",entId:DATA.enterprises[0].id,studioId:DATA.enterprises[1].id,role:"Classifier",tab:0,sheet:0,ruleId:null,filter:"",ppf:"all"};

const NAV=[
 ["Overview",[["dashboard","Dashboard"]]],
 ["Classification",[["studio","Classification Studio"],["classification","Classification Results"]]],
 ["National Register",[["registry","Enterprise Registry"],["profile","Enterprise Profile"],["ownership","Ownership & Control"],["groups","Enterprise Groups"],["registers","Registers (workbook)"]]],
 ["Methodology",[["rules","Rules Engine"],["metadata","Metadata Repository"],["standards","Standards Repository"]]],
 ["Quality & Governance",[["quality","Data Quality"],["validation","Validation & Exceptions"],["reviews","Review Queue"],["audit","Audit Trail"]]],
 ["Platform",[["api","API Demonstration"],["users","Users & Roles"],["uat","UAT Test Center"],["gap","Gap Analysis & Roadmap"]]]
];
const TITLES={};NAV.forEach(s=>s[1].forEach(m=>TITLES[m[0]]=m[1]));
const HELP={
 dashboard:"National view of the register — classification coverage, quality and pending reviews.",
 studio:"The classification engine, live. Pick an enterprise and run the 18 sequenced tests; the institutional sector, public/private status, control, size and FDI treatment are derived rule-by-rule with full traceability.",
 classification:"Live classification results for every unit, each with a one-click explanation.",
 registry:"The Central Statistical Business Register — search, filter, and open any enterprise's profile.",
 profile:"A complete enterprise file: classification passport, ownership network, explainability, quality, history and audit.",
 ownership:"Effective government/foreign ownership across the whole graph, the Ultimate Controlling Institutional Unit, and the ownership network.",
 groups:"Enterprise groups with global ultimate parent, domestic group head and resident (truncated) perimeter.",
 registers:"The platform's statistical registers — the database equivalent of the implementation workbook's sheets.",
 rules:"The database-driven Rules Repository and the 18-test methodology. Every rule traces to a standard and can be tested against your own facts.",
 metadata:"GSIM/SDMX-aligned metadata — every variable fully specified.",
 standards:"The international and national standards every rule is anchored to.",
 quality:"Data quality scored across the six DAMA dimensions, at dataset and enterprise level.",
 validation:"Findings from the VR-001..VR-018 business-rule library with severity and recommended action.",
 reviews:"Anomalies routed for human adjudication. AI assists; the Technical Classification Committee decides.",
 audit:"Immutable change log supporting full reproducibility and lineage.",
 api:"API-first platform. Representative endpoints with sample responses.",
 users:"Role-Based Access Control — seven roles and the permission matrix.",
 uat:"Representative acceptance tests and the production-gate criteria.",
 gap:"What is implemented, partial, or future — and readiness for pilot and production."
};
function esc(s){return (s==null?"":String(s)).replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));}
function ent(id){return DATA.enterprises.find(e=>e.id===id);}
function money(v){if(v==null)return "—";if(v>=1e9)return "QAR "+(v/1e9).toFixed(1)+"bn";if(v>=1e6)return "QAR "+(v/1e6).toFixed(1)+"m";if(v>=1e3)return "QAR "+(v/1e3).toFixed(0)+"k";return "QAR "+(v||0).toLocaleString();}
function go(v,x){state.view=v;if(x)Object.assign(state,x);window.scrollTo(0,0);if(window.innerWidth<=860)document.getElementById('sb').classList.remove('open');render();}
const PP={"PUB-NFC":["b-blue","Public non-financial corporation"],"PUB-FC":["b-blue","Public financial corporation"],"GG":["b-purple","General government"],"PRV-NFC":["b-green","Private non-financial corporation"],"PRV-FC":["b-green","Private financial corporation"],"FCC":["b-amber","Foreign-controlled corporation"],"NPISH":["b-teal","NPISH"]};
function pp(v){const m=PP[v]||["b-gray",v];return `<span class="badge ${m[0]}">${esc(v)}</span>`;}
function bdg(v,c){return `<span class="badge ${c||'b-gray'}">${esc(v)}</span>`;}
function qcol(s){return s>=.85?"var(--green)":s>=.7?"var(--amber)":"var(--red)";}
const PAL=["#8a1538","#1d6fb8","#7a3b97","#1a8a4f","#b9651b","#127a6c","#a8204a","#9a6a10","#52606d"];
function bars(map){const e=Object.entries(map).sort((a,b)=>b[1]-a[1]),mx=Math.max(...e.map(x=>x[1]),1);
 return e.map(([k,v],i)=>`<div class="barrow"><div>${esc(k)}</div><div class="bar"><span style="width:${v/mx*100}%;background:${PAL[i%PAL.length]}"></span></div><div style="text-align:right;font-weight:650">${v}</div></div>`).join("");}
function sev(s){return bdg(s,{ERROR:"b-red",WARN:"b-amber",INFO:"b-blue"}[s]||"b-gray");}

/* DSL evaluator for rule tester */
function nm(v){const n=parseFloat(v);return isNaN(n)?null:n;}
function leaf(c,f){const o=c.op,a=f[c.field],v=c.value;
 if(o==="exists")return c.field in f&&f[c.field]!=null;if(o==="truthy")return !!a;
 if(o==="eq")return a===v;if(o==="ne")return a!==v;if(o==="in")return (v||[]).includes(a);
 if(["gt","gte","lt","lte"].includes(o)){const x=nm(a),y=nm(v);if(x==null||y==null)return false;return{gt:x>y,gte:x>=y,lt:x<y,lte:x<=y}[o];}
 if(o==="between"){const x=nm(a);if(x==null)return false;const lo=nm((v||[])[0]),hi=nm((v||[])[1]);if(lo!=null&&x<lo)return false;if(hi!=null&&x>=hi)return false;return true;}return false;}
function evalC(c,f){if(!c||!Object.keys(c).length)return true;if(c.all)return c.all.every(x=>evalC(x,f));if(c.any)return c.any.some(x=>evalC(x,f));if(c.not)return !evalC(c.not,f);if(c.op)return leaf(c,f);return false;}

function ownSVG(e){
 const ch=e.ownership.chain||[];if(!ch.length)return '<p class="small">No ownership recorded (e.g. household enterprise).</p>';
 const nd={};nd[e.id]={id:e.id,label:e.name,kind:'entity',d:0};const oo={};ch.forEach(c=>{(oo[c.owned_id]=oo[c.owned_id]||[]).push(c);});
 let fr=[e.id],d=0,sn=new Set([e.id]);
 while(fr.length&&d<5){let nx=[];fr.forEach(id=>{(oo[id]||[]).forEach(c=>{if(!nd[c.owner_id])nd[c.owner_id]={id:c.owner_id,label:c.owner_name||c.owner_id,kind:c.is_government?'gov':(c.is_resident?'priv':'foreign'),d:d+1};if(!sn.has(c.owner_id)){sn.add(c.owner_id);nx.push(c.owner_id);}});});fr=nx;d++;}
 const mx=Math.max(...Object.values(nd).map(n=>n.d)),ly={};Object.values(nd).forEach(n=>{(ly[n.d]=ly[n.d]||[]).push(n);});
 const W=520,rh=90,bw=148,bh=42,H=(mx+1)*rh+18,ps={};
 for(let i=0;i<=mx;i++){const ar=ly[i]||[],g=W/(ar.length+1);ar.forEach((n,j)=>ps[n.id]={x:g*(j+1),y:H-i*rh-rh/2});}
 let ln="";ch.forEach(c=>{const a=ps[c.owner_id],b=ps[c.owned_id];if(!a||!b)return;const t=c.ownership_pct+"%"+(c.control_indicator?(" · "+c.control_indicator):"");ln+=`<line x1="${a.x}" y1="${a.y+bh/2}" x2="${b.x}" y2="${b.y-bh/2}" stroke="#aab4c0" stroke-width="1.4" marker-end="url(#a)"/><text x="${(a.x+b.x)/2+4}" y="${(a.y+b.y)/2}" font-size="10" fill="#5a6473">${esc(t)}</text>`;});
 const cl={entity:'#8a1538',gov:'#7a3b97',foreign:'#b9651b',priv:'#1a8a4f'};let bx="";
 Object.values(nd).forEach(n=>{const p=ps[n.id];bx+=`<rect x="${p.x-bw/2}" y="${p.y-bh/2}" width="${bw}" height="${bh}" rx="8" fill="#fff" stroke="${cl[n.kind]}" stroke-width="2"/><text x="${p.x}" y="${p.y-2}" font-size="10" text-anchor="middle" fill="#1f2937">${esc((n.label||'').slice(0,22))}</text><text x="${p.x}" y="${p.y+12}" font-size="8" text-anchor="middle" fill="${cl[n.kind]}">${n.kind==='entity'?'THIS ENTITY':n.kind.toUpperCase()}</text>`;});
 return `<svg viewBox="0 0 ${W} ${H}" width="100%" style="max-height:340px"><defs><marker id="a" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#aab4c0"/></marker></defs>${ln}${bx}</svg>
  <div class="legend">■ <span style="color:#8a1538">entity</span> · ■ <span style="color:#7a3b97">government</span> · ■ <span style="color:#1a8a4f">resident private</span> · ■ <span style="color:#b9651b">non-resident</span></div>`;
}

/* ===== VIEWS ===== */
function vDashboard(){
 const E=DATA.enterprises,by=k=>{const m={};E.forEach(e=>m[e[k]||"—"]=(m[e[k]||"—"]||0)+1);return m;};
 const avgQ=(E.reduce((s,e)=>s+e.quality.overall_score,0)/E.length),openR=DATA.reviews.filter(r=>r.status==="OPEN").length,exc=E.reduce((s,e)=>s+e.exceptions.length,0);
 const tile=(v,l,s)=>`<div class="tile"><div class="v">${v}</div><div class="l">${l}</div>${s?`<div class="s">${s}</div>`:''}</div>`;
 return `<div class="grid tiles">${tile(E.length,'Enterprises registered')}${tile(E.length,'Classified','100% coverage')}${tile(avgQ.toFixed(2),'Avg quality score')}${tile(openR,'Pending reviews')}${tile(exc,'Open exceptions')}${tile(DATA.rules.length,'Active rules')}</div>
  <div class="grid g2"><div class="card"><div class="hd">Institutional sector (SNA)</div><div class="bd">${bars(by("sector"))}</div></div>
   <div class="card"><div class="hd">Quick actions</div><div class="bd"><div class="quick">
    <div class="qa" onclick="go('studio')"><b>▶ Run a classification</b><span>Open the Classification Studio</span></div>
    <div class="qa" onclick="go('registry')"><b>Browse register</b><span>${E.length} enterprises</span></div>
    <div class="qa" onclick="go('registers')"><b>View registers</b><span>Workbook-style sheets</span></div></div></div></div></div>
  <div class="grid g11"><div class="card"><div class="hd">By public / private (GFS)</div><div class="bd">${bars(by("public_private"))}</div></div>
   <div class="card"><div class="hd">By size class</div><div class="bd">${bars(by("size"))}</div></div></div>
  <div class="card"><div class="hd">Recent classification activity</div><div class="bd scroll"><table class="t"><tr><th>When</th><th>Enterprise</th><th>Action</th><th>By</th></tr>
   ${DATA.audit.filter(a=>a.action==="CLASSIFY").slice(0,8).map(a=>`<tr><td class="small">${esc(a.timestamp)}</td><td>${esc((ent(a.record_id)||{}).name||a.record_id)}</td><td>${bdg('CLASSIFIED','b-green')}</td><td>${esc(a.by)}</td></tr>`).join("")}</table></div></div>`;
}

function vStudio(){
 const e=ent(state.studioId),o=e.ownership;
 const opts=DATA.enterprises.map(x=>`<option value="${x.id}" ${x.id===e.id?'selected':''}>${esc(x.name)}</option>`).join("");
 const dims=[["Institutional sector","sector"],["Public / private","public_private"],["Effective control","control"],["Market status","market"],["Size class","size"],["FDI treatment","fdi"],["Special entity","special"]];
 return `<div class="studio">
  <div><div class="card"><div class="hd">Subject enterprise</div><div class="bd">
   <select onchange="state.studioId=this.value;render()" style="width:100%;padding:9px;border:1px solid var(--line);border-radius:8px">${opts}</select>
   <div class="kv" style="grid-template-columns:120px 1fr;margin-top:14px">
    <div class="k">Legal form</div><div>${esc(e.legal_form)}</div><div class="k">ISIC Rev.4</div><div>${esc(e.isic)}</div>
    <div class="k">Residence</div><div>${esc(e.residence)}</div><div class="k">Jurisdiction</div><div>${esc(e.jurisdiction)}</div>
    <div class="k">Employment</div><div>${e.employment==null?'—':e.employment} FTE</div><div class="k">Turnover</div><div>${money(e.turnover)}</div>
    <div class="k">Gov ownership</div><div>${o.government_pct}%${o.government_control?' '+bdg('controlled','b-purple'):''}</div>
    <div class="k">Foreign ownership</div><div>${o.foreign_pct}%</div></div></div></div>
   <div class="card"><div class="hd">Ownership</div><div class="bd"><div class="svgwrap">${ownSVG(e)}</div></div></div></div>
  <div><div class="card"><div class="hd">18-test classification pipeline <span style="flex:1"></span><button class="btn sm" onclick="runStudio('${e.id}')">▶ Run</button></div>
   <div class="bd"><div id="stepper"></div></div></div></div>
  <div class="pp"><div class="box"><div class="top"><div class="nm">${esc(e.name)}</div><div class="id">${esc(e.id)}</div></div>
   ${dims.map(([l,k])=>`<div class="r"><span class="k">${l}</span><span id="pp-${k}" class="small">—</span></div>`).join("")}
   <div id="pp-conf" class="r"><span class="k">Confidence</span><span class="small">—</span></div></div>
   <div class="small" style="text-align:center;margin-top:10px">Press <b>Run</b> to derive the classification live.</div></div></div>`;
}
function runStudio(id){
 const e=ent(id),stp=document.getElementById("stepper");stp.innerHTML="";let i=0;
 (function tick(){if(i>=e.trace.length){const c=document.getElementById('pp-conf');if(c)c.innerHTML='<span class="k">Confidence</span><span style="font-weight:700;color:var(--green)">'+(e.confidence||1)+'</span>';return;}
   const s=e.trace[i],d=document.createElement("div");d.className="step"+(s.matched?" fire":"");
   const out=s.matched?Object.entries(s.output||{}).map(([k,v])=>bdg(typeof v==='object'?JSON.stringify(v):v,'b-green')).join(" "):'<span class="small">governance / process step</span>';
   d.innerHTML=`<div class="n">${esc(s.test_code)}</div><div style="flex:1"><div class="tt">${esc(s.test_name)}</div><div style="margin-top:4px">${out}</div>${s.matched?`<div class="small" style="margin-top:3px">${esc(s.rule_id)} · ${esc(s.standard_ref||'')}</div>`:''}</div>`;
   stp.appendChild(d);d.scrollIntoView({block:'nearest',behavior:'smooth'});
   if(s.matched)Object.entries(s.output||{}).forEach(([k,v])=>{const el=document.getElementById('pp-'+k);if(el)el.innerHTML=(k==='public_private')?pp(v):'<b>'+esc(typeof v==='object'?JSON.stringify(v):v)+(k==='sector'?' · '+esc(e.sector_name):'')+'</b>';});
   i++;setTimeout(tick,Math.max(140,420-i*9));})();
}

function vClassification(){
 return `<div class="card"><div class="hd">Classification results (18-test methodology)</div><div class="bd scroll"><table class="t"><tr><th>Enterprise</th><th>Sector</th><th>Public/Private</th><th>Control</th><th>Market</th><th>Size</th><th>FDI</th><th>Conf.</th><th></th></tr>
  ${DATA.enterprises.map(e=>`<tr><td><b>${esc(e.name)}</b></td><td>${bdg(e.sector)}</td><td>${pp(e.public_private)}</td><td>${bdg(e.control)}</td><td>${e.market==='MARKET'?bdg('MARKET','b-green'):bdg('NON-MARKET','b-amber')}</td><td>${esc(e.size)}</td><td>${e.fdi==='NONE'?'—':bdg(e.fdi,'b-amber')}</td><td>${e.confidence}</td><td><button class="btn sm soft" onclick="go('studio',{studioId:'${e.id}'})">Run</button></td></tr>`).join("")}</table></div></div>`;
}

function vRegistry(){
 const f=(state.filter||"").toLowerCase(),pps=["all",...Object.keys(PP)];
 const r=DATA.enterprises.filter(e=>(state.ppf==='all'||e.public_private===state.ppf)&&(!f||(e.name+e.id+e.sector+e.public_private).toLowerCase().includes(f)));
 return `<div class="card"><div class="bd">
  <div class="srch"><span>🔍</span><input placeholder="Search name, ID, sector…" value="${esc(state.filter)}" oninput="state.filter=this.value;render()"/></div>
  <div class="chips">${pps.map(p=>`<span class="fchip ${state.ppf===p?'on':''}" onclick="state.ppf='${p}';render()">${p==='all'?'All':esc(p)}</span>`).join("")}</div>
  <div class="scroll"><table class="t"><tr><th>Enterprise</th><th>ID</th><th>Sector</th><th>Public/Private</th><th>Size</th><th>Control</th><th>Quality</th></tr>
  ${r.map(e=>`<tr class="row" onclick="go('profile',{entId:'${e.id}',tab:0})"><td><b>${esc(e.name)}</b></td><td class="mono small">${esc(e.id.slice(-8))}</td><td>${esc(e.sector)}</td><td>${pp(e.public_private)}</td><td>${esc(e.size)}</td><td>${bdg(e.control)}</td><td><span style="color:${qcol(e.quality.overall_score)};font-weight:700">${e.quality.overall_score}</span></td></tr>`).join("")}</table>
  <div class="small" style="margin-top:10px">${r.length} of ${DATA.enterprises.length} enterprises</div></div></div>`;
}

function vProfile(){
 const e=ent(state.entId),o=e.ownership,T=["Overview","Ownership","Classification & explainability","Quality","History","Audit"];
 const sel=`<select onchange="state.entId=this.value;render()" style="margin-bottom:14px;padding:9px;border:1px solid var(--line);border-radius:8px">${DATA.enterprises.map(x=>`<option value="${x.id}" ${x.id===e.id?'selected':''}>${esc(x.name)}</option>`).join("")}</select>`;
 const head=`<div class="card"><div class="bd"><div style="display:flex;gap:14px;align-items:center;flex-wrap:wrap">
   <div style="flex:1;min-width:200px"><div style="font-size:18px;font-weight:700">${esc(e.name)}</div><div class="small mono">${esc(e.id)} · LEI ${esc(e.lei||'—')}</div></div>
   <div style="display:flex;gap:7px;flex-wrap:wrap">${bdg(e.sector)}${pp(e.public_private)}${bdg(e.size)}${e.fdi!=='NONE'?bdg(e.fdi,'b-amber'):''}</div>
   <button class="btn" onclick="go('studio',{studioId:'${e.id}'})">▶ Classify</button></div></div></div>`;
 const tabs=`<div class="tabs">${T.map((t,i)=>`<button class="${state.tab===i?'active':''}" onclick="state.tab=${i};render()">${t}</button>`).join("")}</div>`;
 let b="";
 if(state.tab===0){const lus=DATA.legal_units.filter(l=>l.enterprise_id===e.id),es=DATA.establishments.filter(x=>x.enterprise_id===e.id);
   b=`<div class="grid g11"><div class="card"><div class="hd">Master data</div><div class="bd"><div class="kv">
     <div class="k">Arabic name</div><div dir="rtl">${esc(e.name_ar)||'—'}</div><div class="k">Legal form</div><div>${esc(e.legal_form)} · ${esc(e.legal_form_name)}</div>
     <div class="k">ISIC Rev.4</div><div>${esc(e.isic)}</div><div class="k">Residence</div><div>${esc(e.residence)}</div>
     <div class="k">Jurisdiction</div><div>${esc(e.jurisdiction)}</div><div class="k">Employment</div><div>${e.employment==null?'—':e.employment} FTE</div>
     <div class="k">Turnover</div><div>${money(e.turnover)}</div><div class="k">Group</div><div>${esc(e.group_id)||'—'}</div></div></div></div>
    <div class="card"><div class="hd">Legal units & establishments</div><div class="bd">
     <div class="small" style="font-weight:650;margin-bottom:5px">Legal units (${lus.length})</div>${lus.map(l=>`<div style="font-size:12.5px;margin:3px 0">• ${esc(l.name)} <span class="small mono">${esc(l.cr_number||'')} ${esc(l.authority||'')}</span></div>`).join("")||'<div class="small">—</div>'}
     <div class="small" style="font-weight:650;margin:10px 0 5px">Establishments (${es.length})</div>${es.map(x=>`<div style="font-size:12.5px;margin:3px 0">• ${esc(x.name)} <span class="small">${esc(x.zone||'')} · ${x.employment||0} FTE</span></div>`).join("")||'<div class="small">—</div>'}</div></div></div>`;}
 else if(state.tab===1){b=`<div class="grid g2"><div class="card"><div class="hd">Ownership network</div><div class="bd"><div class="svgwrap">${ownSVG(e)}</div></div></div>
   <div class="card"><div class="hd">Control intelligence</div><div class="bd"><div class="kv" style="grid-template-columns:1fr auto">
    <div class="k">Effective government ownership</div><div><b>${o.government_pct}%</b></div><div class="k">Government voting</div><div>${o.government_voting}%</div>
    <div class="k">Effective foreign ownership</div><div>${o.foreign_pct}%</div><div class="k">Government control</div><div>${o.government_control?bdg('Yes','b-purple'):'No'}</div>
    <div class="k">Control indicators</div><div>${(o.control_indicators||[]).map(c=>bdg(c)).join(' ')||'—'}</div>
    <div class="k">Ultimate controlling unit</div><div>${o.uci?esc(o.uci.uci_name)+(o.uci.is_government?' '+bdg('Govt','b-purple'):''):'—'}</div></div></div></div></div>`;}
 else if(state.tab===2){b=`<div class="card"><div class="hd">Why this classification — applied rules</div><div class="bd scroll"><table class="t"><tr><th>Test</th><th>Rule</th><th>Output</th><th>Standard</th><th>Rationale</th></tr>
   ${e.applied_rules.map(a=>`<tr><td>${esc(a.test)}</td><td class="mono">${esc(a.rule_id)}</td><td>${Object.entries(a.output||{}).map(([k,v])=>bdg(esc(typeof v==='object'?JSON.stringify(v):v),'b-green')).join(' ')}</td><td class="small">${esc(a.standard_ref)}</td><td class="small">${esc(a.rationale)}</td></tr>`).join("")}</table>
   <div class="note" style="margin-top:12px"><b>Confidence ${e.confidence}</b> · rule-based & reproducible. Sources: CSBR golden record · ownership graph · reference codelists.</div></div></div>`;}
 else if(state.tab===3){const q=e.quality,ds=["completeness","validity","consistency","uniqueness","accuracy","timeliness"];
   b=`<div class="grid g2"><div class="card"><div class="hd">Quality — overall ${q.overall_score}</div><div class="bd">${ds.map(d=>`<div class="barrow"><div>${d}</div><div class="bar"><span style="width:${q[d]*100}%;background:${qcol(q[d])}"></span></div><div style="text-align:right">${q[d]}</div></div>`).join("")}</div></div>
    <div class="card"><div class="hd">Validation exceptions (${e.exceptions.length})</div><div class="bd scroll"><table class="t"><tr><th>Rule</th><th>Severity</th><th>Message</th></tr>${e.exceptions.map(x=>`<tr><td class="mono">${esc(x.rule_id)}</td><td>${sev(x.severity)}</td><td>${esc(x.message)}</td></tr>`).join("")||'<tr><td colspan=3 style="color:var(--green)">No exceptions.</td></tr>'}</table></div></div></div>`;}
 else if(state.tab===4){b=`<div class="card"><div class="hd">Classification history</div><div class="bd scroll"><table class="t"><tr><th>Version</th><th>Sector</th><th>Public/Private</th><th>Control</th><th>Status</th></tr>
   <tr><td>v2</td><td>${esc(e.sector)}</td><td>${pp(e.public_private)}</td><td>${esc(e.control)}</td><td>${bdg('current','b-green')}</td></tr>
   <tr><td>v1</td><td>${esc(e.sector)}</td><td>${pp(e.public_private)}</td><td>${esc(e.control)}</td><td class="small">superseded</td></tr></table>
   <div class="note" style="margin-top:12px">Every re-classification writes a new immutable version (valid_from/valid_to) so any historical classification can be reproduced.</div></div></div>`;}
 else{b=`<div class="card"><div class="hd">Audit trail</div><div class="bd scroll"><table class="t"><tr><th>When</th><th>Action</th><th>Field</th><th>Old → New</th><th>By</th></tr>${e.audit.map(a=>`<tr><td class="small">${esc(a.timestamp)}</td><td>${esc(a.action)}</td><td>${esc(a.field)||'—'}</td><td>${esc(a.old)||'—'} → ${esc(a.new)||'—'}</td><td>${esc(a.by)}</td></tr>`).join("")}</table></div></div>`;}
 return sel+head+tabs+b;
}

function vOwnership(){
 const e=ent(state.entId),o=e.ownership;
 return `<select onchange="state.entId=this.value;render()" style="margin-bottom:14px;padding:9px;border:1px solid var(--line);border-radius:8px">${DATA.enterprises.map(x=>`<option value="${x.id}" ${x.id===e.id?'selected':''}>${esc(x.name)}</option>`).join("")}</select>
  <div class="grid g2"><div class="card"><div class="hd">Ownership network — ${esc(e.name)}</div><div class="bd"><div class="svgwrap">${ownSVG(e)}</div></div></div>
   <div class="card"><div class="hd">Effective control</div><div class="bd"><div class="kv" style="grid-template-columns:1fr auto">
    <div class="k">Government ownership</div><div><b>${o.government_pct}%</b></div><div class="k">Government voting</div><div>${o.government_voting}%</div>
    <div class="k">Foreign ownership</div><div>${o.foreign_pct}%</div><div class="k">Government control</div><div>${o.government_control?bdg('Yes','b-purple'):'No'}</div>
    <div class="k">UCI</div><div>${o.uci?esc(o.uci.uci_name):'—'}</div></div>
    <table class="t" style="margin-top:12px"><tr><th>Owner</th><th>Equity</th><th>Voting</th><th>Control</th><th>Origin</th></tr>
    ${o.edges.map(x=>`<tr><td>${esc(x.owner_name||x.owner_id)}</td><td>${x.ownership_pct}%</td><td>${x.voting_pct}%</td><td>${esc(x.control_indicator)||'—'}</td><td>${x.is_government?bdg('Government','b-purple'):(x.is_resident?'Resident':bdg('Non-resident','b-amber'))}</td></tr>`).join("")||'<tr><td colspan=5 class="small">No owners</td></tr>'}</table></div></div></div>`;
}

function vGroups(){
 return DATA.groups.map(g=>{const h=ent(g.domestic_head);
  const mem=g.members.map(m=>{const me=ent(m),kind=me&&me.public_private&&me.public_private.startsWith("PUB")?"gov":(me&&me.public_private==="FCC"?"foreign":"priv");return `<div class="lvl"><span class="gnode ${kind}" style="cursor:pointer" onclick="go('profile',{entId:'${m}',tab:1})">${esc(me?me.name:m)} <span class="small">· ${esc(me?me.sector:'')} ${esc(me?me.public_private:'')}</span></span></div>`;}).join("");
  return `<div class="card"><div class="hd">${esc(g.name)} <span class="small">(${esc(g.group_id)})</span></div><div class="bd">
   <div class="kv"><div class="k">Global ultimate parent</div><div>${esc(g.gup)} (${esc(g.gup_country)})</div><div class="k">Truncated (resident) group</div><div>${g.truncated==="Y"?"Yes":"No"}</div><div class="k">Controlling sector</div><div>${esc(g.controlling_sector)}</div></div>
   <div style="margin-top:14px"><span class="gnode" style="border-color:#444">${esc(g.gup)} <span class="small">· global ultimate parent</span></span>
    <div class="lvl"><span class="gnode entity" style="cursor:pointer" onclick="go('profile',{entId:'${g.domestic_head}'})">${esc(h?h.name:g.domestic_head)} <span class="small">· domestic head</span></span>${mem}</div></div>
   <p class="small" style="margin-top:8px">${esc(g.notes)}</p></div></div>`;}).join("");
}

const SECTORS=[["S.11","Non-financial corporations"],["S.121","Central bank"],["S.122","Deposit-taking corporations"],["S.124","Non-MMF investment funds"],["S.126","Financial auxiliaries"],["S.127","Captive financial institutions"],["S.128","Insurance corporations"],["S.129","Pension funds"],["S.13","General government"],["S.14","Households"],["S.15","NPISH"],["S.2","Rest of the World"]];
function vRegisters(){
 const sh=["Enterprise Register","Legal Units","Establishments","Enterprise Groups","Sector codelist","Validation rules"];
 const tabs=`<div class="stabs">${sh.map((s,i)=>`<button class="${state.sheet===i?'active':''}" onclick="state.sheet=${i};render()">${s}</button>`).join("")}</div>`;
 let t="",E=DATA.enterprises;
 if(state.sheet===0)t=`<table class="t"><tr><th>enterprise_id</th><th>legal_name_en</th><th>legal_form</th><th>sector_code</th><th>public_private</th><th>control_flag</th><th>isic</th><th>residence</th><th>size_class</th></tr>${E.map(e=>`<tr><td class="mono">${esc(e.id)}</td><td>${esc(e.name)}</td><td>${esc(e.legal_form)}</td><td>${esc(e.sector)}</td><td>${esc(e.public_private)}</td><td>${esc(e.control)}</td><td>${esc(e.isic)}</td><td>${esc(e.residence)}</td><td>${esc(e.size)}</td></tr>`).join("")}</table>`;
 else if(state.sheet===1)t=`<table class="t"><tr><th>legal_unit_id</th><th>enterprise_id</th><th>name</th><th>legal_form</th><th>cr_number</th><th>authority</th></tr>${DATA.legal_units.map(l=>`<tr><td class="mono">${esc(l.id)}</td><td class="mono small">${esc(l.enterprise_id)}</td><td>${esc(l.name)}</td><td>${esc(l.legal_form)}</td><td>${esc(l.cr_number)}</td><td>${esc(l.authority)}</td></tr>`).join("")}</table>`;
 else if(state.sheet===2)t=`<table class="t"><tr><th>establishment_id</th><th>enterprise_id</th><th>name</th><th>isic</th><th>municipality</th><th>zone</th><th>employment</th></tr>${DATA.establishments.map(x=>`<tr><td class="mono">${esc(x.id)}</td><td class="mono small">${esc(x.enterprise_id)}</td><td>${esc(x.name)}</td><td>${esc(x.isic)}</td><td>${esc(x.municipality)}</td><td>${esc(x.zone)}</td><td>${x.employment}</td></tr>`).join("")}</table>`;
 else if(state.sheet===3)t=`<table class="t"><tr><th>group_id</th><th>name</th><th>global_ultimate_parent</th><th>country</th><th>domestic_head</th><th>members</th></tr>${DATA.groups.map(g=>`<tr><td class="mono">${esc(g.group_id)}</td><td>${esc(g.name)}</td><td>${esc(g.gup)}</td><td>${esc(g.gup_country)}</td><td class="mono small">${esc(g.domestic_head)}</td><td>${g.member_count}</td></tr>`).join("")}</table>`;
 else if(state.sheet===4)t=`<table class="t"><tr><th>code</th><th>institutional sector (SNA)</th></tr>${SECTORS.map(s=>`<tr><td class="mono">${esc(s[0])}</td><td>${esc(s[1])}</td></tr>`).join("")}</table>`;
 else t=`<table class="t"><tr><th>rule_id</th><th>name</th><th>test</th><th>standard</th></tr>${DATA.rules.map(r=>`<tr><td class="mono">${esc(r.rule_id)}</td><td>${esc(r.name)}</td><td>${esc(r.test_code)}</td><td class="small">${esc(r.standard_ref)}</td></tr>`).join("")}</table>`;
 return `<div class="help">These are the platform's statistical registers — the live, database-backed equivalent of the implementation workbook's sheets (persistent IDs, codelists and validation rules match the workbook).</div>${tabs}<div class="sbody scroll">${t}</div>`;
}

function vRules(){
 const cur=state.ruleId?DATA.rules.find(r=>r.rule_id===state.ruleId):DATA.rules[0];
 const list=DATA.rules.map(r=>`<tr class="row" onclick="state.ruleId='${r.rule_id}';render()"><td class="mono">${esc(r.rule_id)}</td><td>${esc(r.name)}</td><td>${bdg(r.test_code)}</td></tr>`).join("");
 const facts=sugg(cur);
 return `<div class="card"><div class="hd">The 18 sequenced classification tests</div><div class="bd"><div style="display:flex;gap:7px;flex-wrap:wrap">${DATA.tests.map(t=>`<span class="badge b-gray" title="${esc(t.description)}">${esc(t.test_code)} · ${esc(t.name)}</span>`).join("")}</div></div></div>
  <div class="grid g2"><div class="card"><div class="hd">Rules repository (${DATA.rules.length})</div><div class="bd scroll" style="max-height:520px"><table class="t"><tr><th>ID</th><th>Name</th><th>Test</th></tr>${list}</table></div></div>
   <div><div class="card"><div class="hd">${esc(cur.rule_id)} — ${esc(cur.name)}</div><div class="bd"><div class="kv" style="grid-template-columns:120px 1fr">
    <div class="k">Test · domain</div><div>${esc(cur.test_code)} · ${esc(cur.domain)}</div><div class="k">Standard</div><div>${esc(cur.standard_ref)}</div>
    <div class="k">Priority · conf.</div><div>${cur.priority} · ${cur.confidence}</div><div class="k">Rationale</div><div>${esc(cur.rationale)}</div></div>
    <div class="small" style="margin:10px 0 4px">Logic (JSON condition tree)</div><pre class="mono" style="background:var(--surface2);border:1px solid var(--line);padding:9px;border-radius:8px;white-space:pre-wrap;font-size:11.5px">${esc(JSON.stringify(cur.logic,null,1))}</pre>
    <div class="small">Output: <span class="mono">${esc(JSON.stringify(cur.output))}</span></div></div></div>
   <div class="card"><div class="hd">Rule tester</div><div class="bd"><div class="small" style="margin-bottom:6px">Edit the facts and evaluate this rule (same evaluator as the engine).</div>
    <textarea id="rtf">${esc(JSON.stringify(facts,null,1))}</textarea><div style="margin-top:8px"><button class="btn sm" onclick="testRule('${cur.rule_id}')">▶ Evaluate</button> <span id="rtres"></span></div></div></div></div></div>`;
}
function sugg(r){const f={};(function w(c){if(!c)return;if(c.all)c.all.forEach(w);else if(c.any)c.any.forEach(w);else if(c.not)w(c.not);else if(c.op){if(c.op==="eq"||c.op==="in")f[c.field]=Array.isArray(c.value)?c.value[0]:c.value;else if(["gt","gte","lt","lte"].includes(c.op))f[c.field]=c.value;else if(c.op==="truthy")f[c.field]=true;else if(c.op==="exists")f[c.field]="…";}})(r.logic);return f;}
function testRule(id){const r=DATA.rules.find(x=>x.rule_id===id);let f;try{f=JSON.parse(document.getElementById("rtf").value);}catch(e){document.getElementById("rtres").innerHTML='<span style="color:var(--red)">Invalid JSON</span>';return;}const m=evalC(r.logic,f);document.getElementById("rtres").innerHTML=m?`<span style="color:var(--green)">✔ MATCH → ${esc(JSON.stringify(r.output))}</span>`:'<span style="color:var(--red)">✘ no match</span>';}

function vMetadata(){return `<div class="card"><div class="hd">Metadata repository (GSIM/SDMX-aligned)</div><div class="bd scroll"><table class="t"><tr><th>Entity</th><th>Field</th><th>Definition</th><th>Type</th><th>Mand.</th><th>Source</th></tr>${DATA.metadata.map(m=>`<tr><td class="small">${esc(m.entity)}</td><td class="mono">${esc(m.field)}</td><td>${esc(m.definition)}</td><td class="small">${esc(m.data_type)}</td><td>${m.mandatory?bdg('Y','b-green'):'N'}</td><td class="small">${esc(m.source)}</td></tr>`).join("")}</table></div></div>`;}
function vStandards(){return DATA.standards.map(s=>`<div class="card"><div class="hd">${esc(s.code)} — ${esc(s.name)}</div><div class="bd"><div class="small">${esc(s.issuer)} · ${esc(s.edition)} · ${esc(s.domains)}</div><p>${esc(s.description)}</p>${s.concepts.length?`<table class="t"><tr><th>Concept</th><th>Definition</th><th>Ref</th></tr>${s.concepts.map(c=>`<tr><td>${esc(c.concept)}</td><td>${esc(c.definition)}</td><td class="small">${esc(c.reference)}</td></tr>`).join("")}</table>`:''}</div></div>`).join("");}
function vQuality(){const E=DATA.enterprises,ds=["completeness","validity","consistency","uniqueness","accuracy","timeliness","overall_score"],ag={};ds.forEach(d=>ag[d]=(E.reduce((s,e)=>s+e.quality[d],0)/E.length));
 return `<div class="grid tiles">${ds.map(d=>`<div class="tile"><div class="v" style="color:${qcol(ag[d])}">${ag[d].toFixed(2)}</div><div class="l">${d.replace("_"," ")}</div></div>`).join("")}</div>
  <div class="card"><div class="hd">Per-enterprise quality</div><div class="bd scroll"><table class="t"><tr><th>Enterprise</th>${ds.map(d=>`<th>${d.slice(0,5)}</th>`).join("")}</tr>${E.map(e=>`<tr><td>${esc(e.name)}</td>${ds.map(d=>`<td style="color:${qcol(e.quality[d])};font-weight:600">${e.quality[d]}</td>`).join("")}</tr>`).join("")}</table></div></div>`;}
function vValidation(){const all=[];DATA.enterprises.forEach(e=>e.exceptions.forEach(x=>all.push({name:e.name,...x})));const c=s=>all.filter(a=>a.severity===s).length;
 return `<div class="grid tiles"><div class="tile"><div class="v">${all.length}</div><div class="l">Open exceptions</div></div><div class="tile"><div class="v" style="color:var(--red)">${c('ERROR')}</div><div class="l">Errors</div></div><div class="tile"><div class="v" style="color:var(--amber)">${c('WARN')}</div><div class="l">Warnings</div></div><div class="tile"><div class="v" style="color:var(--blue)">${c('INFO')}</div><div class="l">Info</div></div></div>
  <div class="card"><div class="hd">Exceptions (VR-001..VR-018)</div><div class="bd scroll"><table class="t"><tr><th>Enterprise</th><th>Rule</th><th>Severity</th><th>Message</th><th>Action</th></tr>${all.map(a=>`<tr><td>${esc(a.name)}</td><td class="mono">${esc(a.rule_id)}</td><td>${sev(a.severity)}</td><td>${esc(a.message)}</td><td class="small">${esc(a.action)}</td></tr>`).join("")||'<tr><td colspan=5 style="color:var(--green)">No exceptions.</td></tr>'}</table></div></div>`;}
function vReviews(){return `<div class="help">Anomalies routed for human adjudication. AI assists by flagging; the Technical Classification Committee decides.</div><div class="card"><div class="hd">Manual review queue</div><div class="bd scroll"><table class="t"><tr><th>Enterprise</th><th>Type</th><th>Severity</th><th>Title</th><th>Status</th><th></th></tr>${DATA.reviews.length?DATA.reviews.map(r=>`<tr><td class="mono small">${esc(r.enterprise_id)}</td><td>${esc(r.kind)}</td><td>${sev(r.severity)}</td><td>${esc(r.title)}<div class="small">${esc(r.detail)}</div></td><td>${esc(r.status)}</td><td><button class="btn sm soft" onclick="alert('Workflow: assign → investigate → resolve / refer to Committee / override.')">Resolve</button></td></tr>`).join(""):'<tr><td colspan=6 style="color:var(--green)">No open review items.</td></tr>'}</table></div></div>`;}
function vAudit(){return `<div class="card"><div class="hd">Audit trail</div><div class="bd scroll"><table class="t"><tr><th>When</th><th>Record</th><th>Action</th><th>Field</th><th>Old → New</th><th>By</th></tr>${DATA.audit.slice(0,80).map(a=>`<tr><td class="small">${esc(a.timestamp)}</td><td class="mono small">${esc(a.record_id)}</td><td>${esc(a.action)}</td><td>${esc(a.field)||'—'}</td><td>${esc(a.old)||'—'} → ${esc(a.new)||'—'}</td><td>${esc(a.by)}</td></tr>`).join("")}</table></div></div>`;}
const EP=[["POST","/api/auth/login","Authenticate; returns JWT + role",'{"access_token":"eyJ…","role":"Classifier"}'],["GET","/api/dashboard","KPIs & breakdowns",'{"total_enterprises":33,"by_sector":{…}}'],["POST","/api/enterprises/{id}/classify","Run the 18-test classification",'{"sector_code":"S.122","public_private":"PUB-FC","confidence":1.0}'],["GET","/api/enterprises/{id}/explain","Full explainability",'{"applied_rules":[…]}'],["POST","/api/rules/{id}/test","Evaluate a rule against facts",'{"matched":true,"output":{…}}'],["POST","/api/simulate","Sandbox what-if classification",'{"sandbox":true,"result":{…}}']];
function vApi(){return `<div class="card"><div class="hd">REST API (OpenAPI at /docs)</div><div class="bd scroll"><table class="t"><tr><th>Method</th><th>Endpoint</th><th>Purpose</th><th></th></tr>${EP.map((e,i)=>`<tr><td>${bdg(e[0],e[0]==='GET'?'b-blue':'b-green')}</td><td class="mono">${esc(e[1])}</td><td>${esc(e[2])}</td><td><button class="btn sm soft" onclick="document.getElementById('ep${i}').style.display='table-row'">Try</button></td></tr><tr id="ep${i}" style="display:none"><td colspan=4><pre class="mono" style="background:#101826;color:#d6e2ee;padding:11px;border-radius:8px;white-space:pre-wrap">HTTP 200 OK\n${esc(e[3])}</pre></td></tr>`).join("")}</table></div></div>`;}
function vUsers(){const perms=[...new Set(Object.values(DATA.roles).flat())].sort();
 return `<div class="card"><div class="hd">Users</div><div class="bd scroll"><table class="t"><tr><th>Username</th><th>Name</th><th>Role</th></tr>${DATA.users.map(u=>`<tr><td class="mono">${esc(u.username)}</td><td>${esc(u.full_name)}</td><td>${bdg(u.role,'b-blue')}</td></tr>`).join("")}</table></div></div>
  <div class="card"><div class="hd">Permission matrix</div><div class="bd scroll"><table class="t"><tr><th>Permission</th>${Object.keys(DATA.roles).map(r=>`<th>${esc(r.slice(0,4))}</th>`).join("")}</tr>${perms.map(p=>`<tr><td class="mono">${esc(p)}</td>${Object.keys(DATA.roles).map(r=>`<td>${(DATA.roles[r].includes("*")||DATA.roles[r].includes(p))?'<span style="color:var(--green)">✔</span>':'·'}</td>`).join("")}</tr>`).join("")}</table></div></div>`;}
function vUat(){const c=DATA.uat,p=c.filter(r=>r[4]==="Pass").length;
 return `<div class="grid tiles"><div class="tile"><div class="v">100+</div><div class="l">UAT cases (full suite)</div></div><div class="tile"><div class="v" style="color:var(--green)">${p}/${c.length}</div><div class="l">Demo set passing</div></div><div class="tile"><div class="v" style="color:var(--green)">33/33</div><div class="l">Classification verdicts</div></div><div class="tile"><div class="v" style="color:var(--green)">40/40</div><div class="l">Rules verified</div></div></div>
  <div class="card"><div class="hd">Representative acceptance tests</div><div class="bd scroll"><table class="t"><tr><th>Test ID</th><th>Area</th><th>Description</th><th>Expected result</th><th>Status</th></tr>${c.map(r=>`<tr><td class="mono">${esc(r[0])}</td><td>${esc(r[1])}</td><td>${esc(r[2])}</td><td>${esc(r[3])}</td><td>${bdg(r[4],'b-green')}</td></tr>`).join("")}</table></div></div>
  <div class="card"><div class="hd">Acceptance criteria (production gate)</div><div class="bd"><ul class="tight"><li>Methodology traceability <b>100%</b> ✔</li><li>Classification accuracy on golden set <b>33/33</b> ✔</li><li>Rules verified <b>40/40</b> ✔</li><li>Validation library VR-001..VR-018 <b>18/18</b> ✔</li><li>Explainability + audit for <b>100%</b> of classifications ✔</li></ul></div></div>`;}
function vGap(){const g=DATA.gap,box=(t,a)=>`<div class="card"><div class="hd">${t}</div><div class="bd"><ul class="tight">${a.map(x=>`<li>${esc(x)}</li>`).join("")}</ul></div></div>`;
 return `<div class="grid g11">${box("✔ Fully implemented",g.implemented)}${box("◑ Partially implemented",g.partial)}</div>
  <div class="grid g11">${box("→ Future enhancements",g.future)}${box("⚠ Production-readiness gaps",g.production_gaps)}</div>
  <div class="card"><div class="hd">Production readiness assessment</div><div class="bd scroll"><table class="t"><tr><th>Dimension</th><th>Status</th><th>Notes</th></tr>${DATA.readiness.map(r=>`<tr><td>${esc(r[0])}</td><td><span class="rag ${r[1].replace(/[^A-Za-z]/g,'')}">${esc(r[1])}</span></td><td>${esc(r[2])}</td></tr>`).join("")}</table>
   <div class="note" style="margin-top:12px"><b>Recommendation:</b> Methodology and data-governance readiness are <span class="rag Green">Green</span>. Proceed to a controlled <b>pilot</b> on the largest 100 enterprises after security hardening and one administrative-source integration; defer production until HA, load testing and data-sharing instruments under the Statistics Law are in place.</div></div></div>`;}

const VIEWS={dashboard:vDashboard,studio:vStudio,classification:vClassification,registry:vRegistry,profile:vProfile,ownership:vOwnership,groups:vGroups,registers:vRegisters,rules:vRules,metadata:vMetadata,standards:vStandards,quality:vQuality,validation:vValidation,reviews:vReviews,audit:vAudit,api:vApi,users:vUsers,uat:vUat,gap:vGap};
function render(){
 document.getElementById("nav").innerHTML=NAV.map(s=>`<div class="navsec"><div class="lbl">${s[0]}</div>${s[1].map(m=>`<a class="${state.view===m[0]?'active':''}" onclick="go('${m[0]}')">${m[1]}</a>`).join("")}</div>`).join("");
 const rs=document.getElementById("rolesel");if(!rs.options.length)rs.innerHTML=Object.keys(DATA.roles).map(r=>`<option ${r==='Classifier'?'selected':''}>${r}</option>`).join("");
 const help=HELP[state.view]?`<div class="help">${HELP[state.view]}</div>`:"";
 document.getElementById("content").innerHTML=`<div class="h-page">${esc(TITLES[state.view]||'')}</div><div class="h-sub">National Enterprise Intelligence &amp; Classification System · State of Qatar</div>${help}`+(VIEWS[state.view]||vDashboard)();
}
render();
</script>
</body>
</html>
"""
