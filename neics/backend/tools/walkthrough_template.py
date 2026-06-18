"""HTML/CSS/JS template for the NEICS interactive walkthrough (advanced UI).

`/*__DATA__*/` is replaced with the embedded JSON payload by build_walkthrough.py.
Produces a single, dependency-free, mobile-responsive .html that behaves like a
real enterprise classification platform (no backend required).
"""

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>NEICS — National Enterprise Intelligence & Classification System</title>
<style>
:root{
 --maroon:#8A1538;--maroon2:#a8204a;--gold:#b08d57;--ink:#141c2b;--ink2:#3a4660;--muted:#6b7689;
 --line:#e7eaf0;--line2:#f0f2f7;--bg:#eceff4;--surface:#ffffff;--surface2:#f7f9fc;
 --green:#1f8a4c;--greenbg:#e7f4ec;--amber:#9a6b12;--amberbg:#fbf1da;--red:#c0392b;--redbg:#fbe8e6;
 --blue:#1f6fb2;--bluebg:#e8f1fa;--purple:#7d3c98;--purplebg:#f3e9f7;--teal:#13796b;--tealbg:#e4f4f1;
 --sh:0 1px 2px rgba(16,24,40,.06),0 1px 3px rgba(16,24,40,.10);--sh2:0 6px 20px rgba(16,24,40,.10);
 --r:12px;
}
*{box-sizing:border-box}html,body{margin:0;padding:0}
body{font-family:"Segoe UI",-apple-system,Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:var(--maroon);text-decoration:none}
button{font-family:inherit}
#app{display:flex;min-height:100vh}
/* Sidebar */
.sidebar{width:256px;background:var(--surface);border-right:1px solid var(--line);flex-shrink:0;position:sticky;top:0;height:100vh;overflow-y:auto}
.brand{padding:18px 18px 14px;border-bottom:1px solid var(--line);display:flex;gap:11px;align-items:center}
.brand .logo{width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,var(--maroon),#5c0e25);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;flex-shrink:0;box-shadow:var(--sh)}
.brand h1{font-size:15px;margin:0;letter-spacing:.2px}
.brand .sub{font-size:10.5px;color:var(--muted);margin-top:1px}
.navsec{padding:12px 12px 2px}.navsec .lbl{font-size:10px;text-transform:uppercase;letter-spacing:.7px;color:var(--muted);padding:6px 10px;font-weight:700}
.nav a{display:flex;gap:10px;align-items:center;padding:8px 11px;border-radius:9px;color:var(--ink2);cursor:pointer;font-size:13px;margin:1px 0}
.nav a:hover{background:var(--surface2)}
.nav a.active{background:linear-gradient(90deg,rgba(138,21,56,.10),rgba(138,21,56,.03));color:var(--maroon);font-weight:650}
.nav a.active svg{color:var(--maroon)}
.nav a svg{width:17px;height:17px;color:var(--muted);flex-shrink:0}
/* Main */
.main{flex:1;display:flex;flex-direction:column;min-width:0}
.topbar{background:rgba(255,255,255,.9);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:11px 24px;display:flex;align-items:center;gap:16px;position:sticky;top:0;z-index:30}
.crumb{font-weight:650;font-size:15px}
.crumb .ctx{color:var(--muted);font-weight:400;font-size:13px}
.staging{background:var(--amberbg);color:var(--amber);border:1px solid #ecd9a8;padding:4px 10px;border-radius:20px;font-size:11px;font-weight:700;white-space:nowrap}
.spacer{flex:1}
.search{display:flex;align-items:center;gap:7px;background:var(--surface2);border:1px solid var(--line);border-radius:9px;padding:6px 10px;min-width:210px}
.search input{border:0;background:none;outline:none;font-size:13px;width:100%}
.search svg{width:15px;height:15px;color:var(--muted)}
.userpill{display:flex;align-items:center;gap:8px}
.userpill select{padding:6px 9px;border:1px solid var(--line);border-radius:8px;background:#fff;font-size:13px}
.avatar{width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,var(--gold),#8a6a3e);color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700}
.menubtn{display:none;background:none;border:1px solid var(--line);border-radius:8px;padding:5px 9px;font-size:17px;cursor:pointer}
.content{padding:22px 24px;max-width:1320px;width:100%}
/* Headings */
.h-page{font-size:21px;font-weight:700;margin:0 0 3px}
.h-sub{color:var(--muted);margin:0 0 18px;font-size:13.5px}
/* Cards & layout */
.grid{display:grid;gap:16px}
.tiles{grid-template-columns:repeat(auto-fit,minmax(190px,1fr))}
.g2{grid-template-columns:1.4fr 1fr}.g3{grid-template-columns:repeat(3,1fr)}.g11{grid-template-columns:1fr 1fr}
@media(max-width:1000px){.g2,.g3,.g11{grid-template-columns:1fr}}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--sh)}
.card .hd{padding:14px 16px;border-bottom:1px solid var(--line2);display:flex;align-items:center;gap:9px;font-weight:650;font-size:14px}
.card .hd .ic{width:28px;height:28px;border-radius:8px;background:var(--surface2);display:flex;align-items:center;justify-content:center}
.card .hd .ic svg{width:15px;height:15px;color:var(--maroon)}
.card .bd{padding:16px}
.tile{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:15px 16px;box-shadow:var(--sh);position:relative}
.tile .ic{width:34px;height:34px;border-radius:9px;display:flex;align-items:center;justify-content:center;margin-bottom:9px}
.tile .ic svg{width:17px;height:17px}
.tile .v{font-size:27px;font-weight:750;line-height:1.1}
.tile .l{color:var(--muted);font-size:12px;margin-top:2px}
.tile .t{font-size:11px;color:var(--green);margin-top:5px;font-weight:600}
/* Badges */
.badge{display:inline-flex;align-items:center;gap:5px;padding:3px 9px;border-radius:20px;font-size:11.5px;font-weight:650;white-space:nowrap}
.bg-blue{background:var(--bluebg);color:var(--blue)}.bg-green{background:var(--greenbg);color:var(--green)}
.bg-purple{background:var(--purplebg);color:var(--purple)}.bg-amber{background:var(--amberbg);color:var(--amber)}
.bg-red{background:var(--redbg);color:var(--red)}.bg-teal{background:var(--tealbg);color:var(--teal)}.bg-gray{background:#eef1f5;color:#5a6473}
.dot{width:7px;height:7px;border-radius:50%;display:inline-block}
/* Tables */
.tbl{width:100%;border-collapse:collapse;font-size:13px}
.tbl th,.tbl td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line2);vertical-align:middle}
.tbl th{color:var(--muted);font-weight:650;font-size:10.5px;text-transform:uppercase;letter-spacing:.5px;position:sticky;top:0;background:var(--surface)}
.tbl tr.row:hover{background:var(--surface2);cursor:pointer}
.scroll{overflow:auto}
/* Buttons */
.btn{display:inline-flex;align-items:center;gap:7px;background:var(--maroon);color:#fff;border:0;padding:9px 16px;border-radius:9px;cursor:pointer;font-size:13px;font-weight:600;box-shadow:var(--sh)}
.btn:hover{background:var(--maroon2)}.btn svg{width:15px;height:15px}
.btn.ghost{background:#fff;color:var(--maroon);border:1px solid var(--maroon)}
.btn.soft{background:var(--surface2);color:var(--ink2);border:1px solid var(--line);box-shadow:none}
.btn.sm{padding:6px 11px;font-size:12px}
.btn.lg{padding:12px 22px;font-size:15px}
/* Chips / filters */
.chips{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;align-items:center}
.fchip{padding:6px 12px;border-radius:20px;border:1px solid var(--line);background:#fff;font-size:12.5px;cursor:pointer;color:var(--ink2)}
.fchip.on{background:var(--maroon);color:#fff;border-color:var(--maroon)}
.kv{display:grid;grid-template-columns:200px 1fr;gap:9px 16px;font-size:13px}
.kv .k{color:var(--muted)}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px}
.small{font-size:12px;color:var(--muted)}
.help{background:var(--bluebg);border:1px solid #cfe0f2;border-radius:10px;padding:11px 14px;margin-bottom:18px;font-size:13px;color:#274b6b;display:flex;gap:9px;align-items:flex-start}
.help svg{width:16px;height:16px;flex-shrink:0;margin-top:1px;color:var(--blue)}
/* Tabs */
.tabs{display:flex;gap:3px;border-bottom:1px solid var(--line);margin:0 0 16px;flex-wrap:wrap}
.tabs button{border:0;background:none;padding:10px 14px;cursor:pointer;border-bottom:2px solid transparent;color:var(--muted);font-size:13px;font-weight:600}
.tabs button.active{color:var(--maroon);border-bottom-color:var(--maroon)}
/* Studio */
.studio{display:grid;grid-template-columns:300px 1fr 300px;gap:16px}
@media(max-width:1100px){.studio{grid-template-columns:1fr}}
.stepper{display:flex;flex-direction:column;gap:9px}
.step{display:flex;gap:11px;padding:11px 13px;border:1px solid var(--line);border-radius:10px;background:#fff;opacity:.45;transition:.25s;align-items:flex-start}
.step.show{opacity:1;box-shadow:var(--sh)}
.step.fire{border-color:var(--maroon);background:linear-gradient(90deg,rgba(138,21,56,.05),#fff)}
.step .sn{width:26px;height:26px;border-radius:50%;background:var(--surface2);color:var(--muted);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex-shrink:0}
.step.fire .sn{background:var(--maroon);color:#fff}
.step .stt{font-weight:650;font-size:13px}
.step .out{margin-top:4px}
.passport{position:sticky;top:78px}
.pp-card{border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:var(--sh)}
.pp-card .top{background:linear-gradient(135deg,var(--maroon),#5c0e25);color:#fff;padding:15px 16px}
.pp-card .top .nm{font-weight:700;font-size:15px}
.pp-card .top .id{font-size:11px;opacity:.8;margin-top:2px}
.pp-row{display:flex;justify-content:space-between;align-items:center;padding:9px 16px;border-bottom:1px solid var(--line2);font-size:13px}
.pp-row .k{color:var(--muted)}
.ring-wrap{display:flex;align-items:center;gap:12px;padding:14px 16px}
/* Sheet (Excel mirror) */
.sheettabs{display:flex;gap:2px;flex-wrap:wrap;margin-bottom:0}
.sheettabs button{border:1px solid var(--line);border-bottom:0;background:var(--surface2);padding:8px 14px;border-radius:8px 8px 0 0;cursor:pointer;font-size:12.5px;color:var(--ink2)}
.sheettabs button.active{background:#fff;color:var(--maroon);font-weight:650;box-shadow:0 -2px 0 var(--maroon) inset}
.sheetbody{border:1px solid var(--line);border-radius:0 10px 10px 10px;background:#fff;overflow:auto}
textarea{width:100%;min-height:130px;font-family:ui-monospace,monospace;font-size:12px;border:1px solid var(--line);border-radius:9px;padding:10px}
.bar{height:9px;background:var(--line2);border-radius:6px;overflow:hidden}.bar>span{display:block;height:100%;background:var(--maroon)}
.barrow{display:grid;grid-template-columns:150px 1fr 44px;gap:10px;align-items:center;margin:7px 0;font-size:12.5px}
.svgwrap{background:var(--surface2);border:1px solid var(--line);border-radius:10px;padding:10px;overflow:auto}
.legend{font-size:11px;color:var(--muted);margin-top:8px}
.gtree .gnode{display:inline-block;border:1.5px solid var(--line);border-radius:9px;padding:7px 13px;margin:4px;background:#fff;box-shadow:var(--sh)}
.gtree .lvl{padding-left:24px;border-left:2px dashed #d6dde4;margin-left:20px}
.gnode.gov{border-color:var(--purple)}.gnode.foreign{border-color:#b9651b}.gnode.entity{border-color:var(--maroon)}.gnode.priv{border-color:var(--green)}
.note{background:#fbfaf6;border:1px solid #ece4d2;border-radius:10px;padding:12px 14px;font-size:13px}
ul.tight{margin:6px 0;padding-left:20px}ul.tight li{margin:5px 0}
.rag{font-weight:700}.rag.Green{color:var(--green)}.rag.Amber{color:var(--amber)}.rag.Red,.rag.RedAmber{color:var(--red)}.rag.AmberGreen{color:#6f8a1c}
.quick{display:flex;gap:10px;flex-wrap:wrap}
.quick .qa{flex:1;min-width:180px;border:1px solid var(--line);border-radius:11px;padding:13px;background:#fff;cursor:pointer;box-shadow:var(--sh)}
.quick .qa:hover{border-color:var(--maroon)}
.quick .qa .t{font-weight:650;margin-top:7px;font-size:13.5px}.quick .qa .d{font-size:12px;color:var(--muted);margin-top:2px}
@media(max-width:860px){
 #app{flex-direction:column}.sidebar{width:100%;height:auto;position:static;max-height:62vh}
 .sidebar.collapsed .navsec,.sidebar.collapsed .brand .sub{display:none}
 .nav a{font-size:13px}.menubtn{display:inline-block}.content{padding:14px}
 .search{min-width:0;flex:1}.crumb{font-size:14px}.staging{display:none}
 .kv{grid-template-columns:1fr;gap:2px}.kv .k{margin-top:7px;font-weight:600}
 .tbl{font-size:12px}.tbl th,.tbl td{padding:8px}
}
</style>
</head>
<body>
<div id="app">
 <aside class="sidebar" id="sidebar">
  <div class="brand"><div class="logo">N</div><div><h1>NEICS</h1><div class="sub">State of Qatar · NSO</div></div></div>
  <nav id="nav"></nav>
 </aside>
 <div class="main">
  <header class="topbar">
   <button class="menubtn" onclick="document.getElementById('sidebar').classList.toggle('collapsed')">☰</button>
   <div class="crumb" id="crumb"></div>
   <span class="spacer"></span>
   <div class="search">{svg_search}<input id="gsearch" placeholder="Search enterprises…" onkeydown="if(event.key==='Enter'){state.filter=this.value;go('registry')}"/></div>
   <span class="staging">● STAGING / UAT</span>
   <div class="userpill"><select id="rolesel" onchange="state.role=this.value;render()"></select><div class="avatar" id="av">CL</div></div>
  </header>
  <div class="content" id="content"></div>
 </div>
</div>
<script>
const DATA = /*__DATA__*/;
const state={view:"dashboard",entId:DATA.enterprises[0].id,studioId:DATA.enterprises[1].id,role:"Classifier",tab:0,sheet:0,ruleId:null,filter:"",ppFilter:"all"};

const ICO={
 dash:'<path d="M3 13h8V3H3zM13 21h8V11h-8zM13 3v6h8V3zM3 21h8v-6H3z"/>',
 studio:'<path d="M12 2l2.4 5 5.6.8-4 4 1 5.6L12 20l-5 2.4 1-5.6-4-4 5.6-.8z"/>',
 list:'<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
 profile:'<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z"/>',
 own:'<path d="M12 3v6M5 21v-4M19 21v-4M5 17a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM19 17a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM12 9a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM7 13l4-3M17 13l-4-3"/>',
 group:'<path d="M17 21v-2a4 4 0 0 0-3-3.87M9 21v-2a4 4 0 0 1 3-3.87M12 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM5 21v-1a3 3 0 0 1 3-3M19 21v-1a3 3 0 0 0-3-3"/>',
 grid:'<path d="M3 3h7v7H3zM14 3h7v7h-7zM14 14h7v7h-7zM3 14h7v7H3z"/>',
 rules:'<path d="M9 11l3 3 8-8M20 12v7a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h9"/>',
 meta:'<path d="M4 7V4h16v3M9 20h6M12 4v16"/>',
 std:'<path d="M12 2l3 7h7l-5.5 4 2 7L12 16l-6.5 4 2-7L2 9h7z"/>',
 quality:'<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14M22 4L12 14.01l-3-3"/>',
 valid:'<path d="M12 9v4M12 17h.01M10.3 3.86l-8 14A1 1 0 0 0 3.2 19h17.6a1 1 0 0 0 .9-1.14l-8-14a1 1 0 0 0-1.4 0z"/>',
 review:'<path d="M11 4h10M11 12h10M11 20h10M3 4l2 2 3-3M3 12l2 2 3-3M3 20l2 2 3-3"/>',
 audit:'<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M9 13l2 2 4-4"/>',
 api:'<path d="M8 3H5a2 2 0 0 0-2 2v3M21 8V5a2 2 0 0 0-2-2h-3M16 21h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3M9 9h6v6H9z"/>',
 users:'<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
 uat:'<path d="M9 11l3 3 8-8M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
 gap:'<path d="M3 3v18h18M7 15l4-4 3 3 5-6"/>',
 search:'<path d="M21 21l-4.3-4.3M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16z"/>',
 info:'<path d="M12 16v-4M12 8h.01M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z"/>',
 play:'<path d="M5 3l14 9-14 9z"/>',bolt:'<path d="M13 2L3 14h7l-1 8 10-12h-7z"/>',
 bank:'<path d="M3 21h18M5 21V10M19 21V10M3 10l9-7 9 7M9 21v-6h6v6"/>',
 building:'<path d="M3 21h18M5 21V4h9v17M14 9h5v12M8 8h2M8 12h2M8 16h2"/>',
 globe:'<path d="M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM2 12h20M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z"/>'
};
function svg(n,cls){return `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" ${cls?'class="'+cls+'"':''}>${ICO[n]||''}</svg>`;}

const NAV=[
 ["Overview",[["dashboard","Dashboard","dash"]]],
 ["Classification",[["studio","Classification Studio","studio"],["classification","Classification Results","rules"]]],
 ["National Register",[["registry","Enterprise Registry","list"],["profile","Enterprise Profile","profile"],["ownership","Ownership & Control","own"],["groups","Enterprise Groups","group"],["registers","Registers (workbook)","grid"]]],
 ["Methodology",[["rules","Rules Engine","rules"],["metadata","Metadata Repository","meta"],["standards","Standards Repository","std"]]],
 ["Quality & Governance",[["quality","Data Quality","quality"],["validation","Validation & Exceptions","valid"],["reviews","Review Queue","review"],["audit","Audit Trail","audit"]]],
 ["Platform",[["api","API Demonstration","api"],["users","Users & Roles","users"],["uat","UAT Test Center","uat"],["gap","Gap Analysis & Roadmap","gap"]]]
];
const TITLES={};NAV.forEach(s=>s[1].forEach(m=>TITLES[m[0]]=m[1]));
const HELP={
 dashboard:"National view of the register — classification coverage, quality and pending reviews. Everything recomputes from the seeded test data.",
 studio:"The classification engine, live. Pick an enterprise, run the 18 sequenced tests, and watch the institutional sector, public/private status, control, size and FDI treatment be derived rule-by-rule with full traceability.",
 classification:"Live classification results for every unit in the register, each with a one-click explanation.",
 registry:"The Central Statistical Business Register. Search, filter and open any enterprise's 360° profile.",
 profile:"A complete enterprise file — classification passport, ownership network, explainability, quality, history and audit.",
 ownership:"Effective government/foreign ownership across the whole graph, the Ultimate Controlling Institutional Unit, and the ownership network. Substance over legal form.",
 groups:"Enterprise groups with global ultimate parent, domestic group head and resident (truncated) perimeter.",
 registers:"The statistical registers as held in the platform — the database equivalent of the implementation workbook's sheets (Enterprise, Legal Unit, Establishment, Group registers and codelists).",
 rules:"The database-driven Rules Repository and the 18-test methodology. No logic is hard-coded; every rule traces to a standard and can be tested against your own facts.",
 metadata:"GSIM/SDMX-aligned metadata — every variable fully specified.",
 standards:"The international & national standards every rule is anchored to (SNA, GFS, BPM6, OECD BD4, ISIC, …).",
 quality:"Data quality scored across the six DAMA dimensions at dataset and enterprise level.",
 validation:"Findings from the VR-001..VR-018 business-rule library with severity and recommended action.",
 reviews:"Anomalies routed for human adjudication. AI assists; the Technical Classification Committee decides.",
 audit:"Immutable change log — who changed what, when, why — supporting full reproducibility.",
 api:"API-first platform. Representative endpoints with sample responses; full OpenAPI at /docs in the running system.",
 users:"Role-Based Access Control — seven roles and the permission matrix governing every action.",
 uat:"Representative acceptance tests and the production-gate criteria. The full 168-case suite is in docs/uat.",
 gap:"What is implemented, partial, or future — and readiness to move toward pilot and production."
};

function esc(s){return (s==null?"":String(s)).replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));}
function ent(id){return DATA.enterprises.find(e=>e.id===id);}
function money(v){if(v==null)return "—";if(v>=1e9)return "QAR "+(v/1e9).toFixed(1)+"bn";if(v>=1e6)return "QAR "+(v/1e6).toFixed(1)+"m";if(v>=1e3)return "QAR "+(v/1e3).toFixed(0)+"k";return "QAR "+(v||0).toLocaleString();}
function go(v,extra){state.view=v;if(extra)Object.assign(state,extra);window.scrollTo(0,0);if(window.innerWidth<=860)document.getElementById('sidebar').classList.add('collapsed');render();}
const PP={"PUB-NFC":["bg-blue","Public non-financial corp"],"PUB-FC":["bg-blue","Public financial corp"],"GG":["bg-purple","General government"],"PRV-NFC":["bg-green","Private non-financial corp"],"PRV-FC":["bg-green","Private financial corp"],"FCC":["bg-amber","Foreign-controlled corp"],"NPISH":["bg-teal","NPISH"]};
function ppBadge(v){const m=PP[v]||["bg-gray",v];return `<span class="badge ${m[0]}">${esc(v)}</span>`;}
function chip(v,cls){return `<span class="badge ${cls||'bg-gray'}">${esc(v)}</span>`;}
function qcolor(s){return s>=.85?"var(--green)":s>=.7?"var(--amber)":"var(--red)";}
function ring(pct,label,sub){const r=26,c=2*Math.PI*r,off=c*(1-pct);const col=qcolor(pct);
 return `<div class="ring-wrap"><svg width="68" height="68" viewBox="0 0 68 68"><circle cx="34" cy="34" r="${r}" fill="none" stroke="#eef1f5" stroke-width="7"/><circle cx="34" cy="34" r="${r}" fill="none" stroke="${col}" stroke-width="7" stroke-linecap="round" stroke-dasharray="${c}" stroke-dashoffset="${off}" transform="rotate(-90 34 34)"/><text x="34" y="38" text-anchor="middle" font-size="15" font-weight="700" fill="${col}">${Math.round(pct*100)}</text></svg><div><div style="font-weight:650">${label}</div><div class="small">${sub||''}</div></div>`;}
function donut(segs){const tot=segs.reduce((s,x)=>s+x.v,0)||1;let a=0,arcs="";const R=52,C=2*Math.PI*R;
 segs.forEach(s=>{const frac=s.v/tot,len=C*frac;arcs+=`<circle cx="70" cy="70" r="${R}" fill="none" stroke="${s.c}" stroke-width="20" stroke-dasharray="${len} ${C-len}" stroke-dashoffset="${-a}" transform="rotate(-90 70 70)"/>`;a+=len;});
 const leg=segs.filter(s=>s.v).map(s=>`<div style="display:flex;align-items:center;gap:7px;font-size:12px;margin:3px 0"><span class="dot" style="background:${s.c}"></span>${esc(s.label)} <b style="margin-left:auto">${s.v}</b></div>`).join("");
 return `<div style="display:flex;gap:18px;align-items:center;flex-wrap:wrap"><svg width="140" height="140" viewBox="0 0 140 140">${arcs}<text x="70" y="66" text-anchor="middle" font-size="22" font-weight="750">${tot}</text><text x="70" y="84" text-anchor="middle" font-size="10" fill="#6b7689">UNITS</text></svg><div style="flex:1;min-width:150px">${leg}</div></div>`;}
const PAL=["#8A1538","#1f6fb2","#7d3c98","#1f8a4c","#b9651b","#13796b","#a8204a","#9a6b12","#5a6473","#2b6cb0"];
function bars(map){const ents=Object.entries(map).sort((a,b)=>b[1]-a[1]);const max=Math.max(...ents.map(e=>e[1]),1);
 return ents.map(([k,v],i)=>`<div class="barrow"><div>${esc(k)}</div><div class="bar"><span style="width:${v/max*100}%;background:${PAL[i%PAL.length]}"></span></div><div style="text-align:right;font-weight:650">${v}</div></div>`).join("");}
function sevPill(s){const m={ERROR:"bg-red",WARN:"bg-amber",INFO:"bg-blue"};return `<span class="badge ${m[s]||'bg-gray'}">${esc(s)}</span>`;}
function entIcon(e){return e.sector&&e.sector.startsWith("S.12")?'bank':(e.public_private&&e.public_private.startsWith("PUB")?'building':(e.public_private==='FCC'?'globe':'building'));}

/* ---- DSL evaluator (mirrors backend) for the rule tester ---- */
function num(v){const n=parseFloat(v);return isNaN(n)?null:n;}
function leaf(c,f){const op=c.op,a=f[c.field],v=c.value;
 if(op==="exists")return c.field in f&&f[c.field]!=null;if(op==="truthy")return !!a;
 if(op==="eq")return a===v;if(op==="ne")return a!==v;if(op==="in")return (v||[]).includes(a);
 if(["gt","gte","lt","lte"].includes(op)){const x=num(a),y=num(v);if(x==null||y==null)return false;return{gt:x>y,gte:x>=y,lt:x<y,lte:x<=y}[op];}
 if(op==="between"){const x=num(a);if(x==null)return false;const lo=num((v||[])[0]),hi=num((v||[])[1]);if(lo!=null&&x<lo)return false;if(hi!=null&&x>=hi)return false;return true;}return false;}
function evalCond(c,f){if(!c||!Object.keys(c).length)return true;if(c.all)return c.all.every(x=>evalCond(x,f));if(c.any)return c.any.some(x=>evalCond(x,f));if(c.not)return !evalCond(c.not,f);if(c.op)return leaf(c,f);return false;}

/* ===================== VIEWS ===================== */
function vDashboard(){
 const E=DATA.enterprises,by=k=>{const m={};E.forEach(e=>m[e[k]||"—"]=(m[e[k]||"—"]||0)+1);return m;};
 const avgQ=(E.reduce((s,e)=>s+e.quality.overall_score,0)/E.length);
 const openR=DATA.reviews.filter(r=>r.status==="OPEN").length;
 const exc=E.reduce((s,e)=>s+e.exceptions.length,0);
 const tile=(ic,col,v,l,t)=>`<div class="tile"><div class="ic" style="background:${col}22;color:${col}">${svg(ic)}</div><div class="v">${v}</div><div class="l">${l}</div>${t?`<div class="t">${t}</div>`:''}</div>`;
 const secMap=by("sector"),segs=Object.entries(secMap).map(([k,v],i)=>({label:k,v,c:PAL[i%PAL.length]}));
 return `<div class="grid tiles" style="margin-bottom:18px">
  ${tile('list','#8A1538',E.length,'Enterprises registered')}
  ${tile('quality','#1f8a4c',E.length,'Classified','100% coverage')}
  ${tile('std','#1f6fb2',avgQ.toFixed(2),'Avg quality score')}
  ${tile('review','#9a6b12',openR,'Pending reviews')}
  ${tile('valid','#c0392b',exc,'Open exceptions')}
  ${tile('rules','#7d3c98',DATA.rules.length,'Active rules')}</div>
 <div class="grid g2" style="margin-bottom:16px">
  <div class="card"><div class="hd"><span class="ic">${svg('group')}</span>Institutional sector composition (SNA)</div><div class="bd">${donut(segs)}</div></div>
  <div class="card"><div class="hd"><span class="ic">${svg('studio')}</span>Quick actions</div><div class="bd"><div class="quick">
    <div class="qa" onclick="go('studio')">${svg('play')}<div class="t">Run a classification</div><div class="d">Open the Classification Studio</div></div>
    <div class="qa" onclick="go('registry')">${svg('list')}<div class="t">Browse register</div><div class="d">${E.length} enterprises</div></div>
    <div class="qa" onclick="go('registers')">${svg('grid')}<div class="t">View registers</div><div class="d">Workbook-style sheets</div></div>
    <div class="qa" onclick="go('rules')">${svg('rules')}<div class="t">Explore rules</div><div class="d">${DATA.rules.length} rules · 18 tests</div></div>
  </div></div></div></div>
 <div class="grid g11" style="margin-bottom:16px">
  <div class="card"><div class="hd"><span class="ic">${svg('building')}</span>By public / private (GFS boundary)</div><div class="bd">${bars(by("public_private"))}</div></div>
  <div class="card"><div class="hd"><span class="ic">${svg('grid')}</span>By size class</div><div class="bd">${bars(by("size"))}</div></div></div>
 <div class="card"><div class="hd"><span class="ic">${svg('audit')}</span>Recent classification activity</div><div class="bd scroll"><table class="tbl"><tr><th>When</th><th>Enterprise</th><th>Action</th><th>By</th></tr>
  ${DATA.audit.filter(a=>a.action==="CLASSIFY").slice(0,8).map(a=>`<tr><td class="small">${esc(a.timestamp)}</td><td>${esc((ent(a.record_id)||{}).name||a.record_id)}</td><td>${chip('CLASSIFIED','bg-green')}</td><td>${esc(a.by)}</td></tr>`).join("")}</table></div></div>`;
}

function vStudio(){
 const e=ent(state.studioId);
 const opts=DATA.enterprises.map(x=>`<option value="${x.id}" ${x.id===e.id?'selected':''}>${esc(x.name)}</option>`).join("");
 const o=e.ownership;
 const dims=[["Institutional sector","sector"],["Public / private","public_private"],["Effective control","control"],["Market status","market"],["Size class","size"],["FDI treatment","fdi"],["Special entity","special"]];
 const ppRows=dims.map(([l,k])=>`<div class="pp-row"><span class="k">${l}</span><span id="pp-${k}" class="small">—</span></div>`).join("");
 return `<div class="studio">
  <div>
   <div class="card"><div class="hd"><span class="ic">${svg('list')}</span>Subject enterprise</div><div class="bd">
     <select onchange="state.studioId=this.value;render()" style="width:100%;padding:9px;border:1px solid var(--line);border-radius:9px">${opts}</select>
     <div class="kv" style="margin-top:14px;grid-template-columns:120px 1fr">
       <div class="k">Legal form</div><div>${esc(e.legal_form)} · ${esc(e.legal_form_name)}</div>
       <div class="k">ISIC Rev.4</div><div>${esc(e.isic)}</div>
       <div class="k">Residence</div><div>${esc(e.residence)}</div>
       <div class="k">Jurisdiction</div><div>${esc(e.jurisdiction)}</div>
       <div class="k">Employment</div><div>${e.employment==null?'—':e.employment} FTE</div>
       <div class="k">Turnover</div><div>${money(e.turnover)}</div>
       <div class="k">Gov ownership</div><div>${o.government_pct}% ${o.government_control?chip('controlled','bg-purple'):''}</div>
       <div class="k">Foreign ownership</div><div>${o.foreign_pct}%</div></div>
   </div></div>
   <div class="card" style="margin-top:16px"><div class="hd"><span class="ic">${svg('own')}</span>Ownership</div><div class="bd"><div class="svgwrap">${ownershipSVG(e)}</div></div></div>
  </div>
  <div>
   <div class="card"><div class="hd"><span class="ic">${svg('studio')}</span>18-test classification pipeline
     <span class="spacer" style="flex:1"></span><button class="btn sm" onclick="runStudio('${e.id}')">${svg('play')} Run</button></div>
    <div class="bd"><div class="stepper" id="stepper">${e.trace.map((s,i)=>stepHTML(s,i,false)).join("")}</div></div></div>
  </div>
  <div class="passport"><div class="pp-card"><div class="top"><div class="nm">${esc(e.name)}</div><div class="id">${esc(e.id)}</div></div>
    ${ppRows}<div id="pp-conf" class="ring-wrap"></div></div>
    <div class="small" style="text-align:center;margin-top:10px">Press <b>Run</b> to derive the classification live.</div></div>
 </div>`;
}
function stepHTML(s,i,fired){
 const out=s.matched?Object.entries(s.output||{}).map(([k,v])=>chip(typeof v==='object'?JSON.stringify(v):v,'bg-green')).join(" "):'<span class="small">governance / process step</span>';
 return `<div class="step ${fired?'show fire':''}" id="st${i}"><div class="sn">${esc(s.test_code)}</div><div style="flex:1"><div class="stt">${esc(s.test_name)}</div><div class="out">${out}</div>${s.matched?`<div class="small" style="margin-top:3px">${esc(s.rule_id)} · ${esc(s.standard_ref||'')}</div>`:''}</div></div>`;
}
function runStudio(id){
 const e=ent(id);const stp=document.getElementById("stepper");stp.innerHTML="";
 const ppmap={sector:e=>ppSet('sector',e.sector+' · '+e.sector_name),public_private:e=>document.getElementById('pp-public_private').innerHTML=ppBadge(e.public_private)};
 let i=0;
 (function tick(){if(i>=e.trace.length){const c=document.getElementById('pp-conf');if(c)c.innerHTML=ring(e.confidence||1,'Confidence','rule-based, explainable');return;}
   const s=e.trace[i];const d=document.createElement('div');d.outerHTML;stp.insertAdjacentHTML('beforeend',stepHTML(s,i,s.matched));
   if(s.matched){Object.entries(s.output||{}).forEach(([k,v])=>{const el=document.getElementById('pp-'+k);if(el){if(k==='public_private')el.innerHTML=ppBadge(v);else el.innerHTML='<b>'+esc(typeof v==='object'?JSON.stringify(v):v)+(k==='sector'?(' · '+esc(e.sector_name)):'')+'</b>';}});}
   document.getElementById('st'+i).scrollIntoView({block:'nearest',behavior:'smooth'});
   i++;setTimeout(tick,Math.max(120,400-i*8));})();
}
function ppSet(k,v){const el=document.getElementById('pp-'+k);if(el)el.innerHTML='<b>'+esc(v)+'</b>';}

function ownershipSVG(e){
 const chain=e.ownership.chain||[];if(!chain.length)return '<p class="small">No ownership recorded for this unit (e.g. household enterprise).</p>';
 const nodes={};nodes[e.id]={id:e.id,label:e.name,kind:'entity',depth:0};
 const ownersOf={};chain.forEach(c=>{(ownersOf[c.owned_id]=ownersOf[c.owned_id]||[]).push(c);});
 let fr=[e.id],depth=0,seen=new Set([e.id]);
 while(fr.length&&depth<5){let nx=[];fr.forEach(id=>{(ownersOf[id]||[]).forEach(c=>{if(!nodes[c.owner_id])nodes[c.owner_id]={id:c.owner_id,label:c.owner_name||c.owner_id,kind:c.is_government?'gov':(c.is_resident?'priv':'foreign'),depth:depth+1};if(!seen.has(c.owner_id)){seen.add(c.owner_id);nx.push(c.owner_id);}});});fr=nx;depth++;}
 const maxD=Math.max(...Object.values(nodes).map(n=>n.depth)),layers={};Object.values(nodes).forEach(n=>{(layers[n.depth]=layers[n.depth]||[]).push(n);});
 const W=540,rowH=92,bw=150,bh=44,H=(maxD+1)*rowH+20,pos={};
 for(let d=0;d<=maxD;d++){const arr=layers[d]||[],gap=W/(arr.length+1);arr.forEach((n,i)=>pos[n.id]={x:gap*(i+1),y:H-d*rowH-rowH/2});}
 let lines="";chain.forEach(c=>{const a=pos[c.owner_id],b=pos[c.owned_id];if(!a||!b)return;const lbl=c.ownership_pct+"%"+(c.control_indicator?(" · "+c.control_indicator):"");lines+=`<line x1="${a.x}" y1="${a.y+bh/2}" x2="${b.x}" y2="${b.y-bh/2}" stroke="#aab4c0" stroke-width="1.5" marker-end="url(#ar)"/><text x="${(a.x+b.x)/2+4}" y="${(a.y+b.y)/2}" font-size="10" fill="#5a6473">${esc(lbl)}</text>`;});
 const col={entity:'#8A1538',gov:'#7d3c98',foreign:'#b9651b',priv:'#1f8a4c'};let boxes="";
 Object.values(nodes).forEach(n=>{const p=pos[n.id];boxes+=`<g><rect x="${p.x-bw/2}" y="${p.y-bh/2}" width="${bw}" height="${bh}" rx="9" fill="#fff" stroke="${col[n.kind]}" stroke-width="2"/><text x="${p.x}" y="${p.y-3}" font-size="10.5" text-anchor="middle" fill="#141c2b">${esc((n.label||'').slice(0,22))}</text><text x="${p.x}" y="${p.y+12}" font-size="8" text-anchor="middle" fill="${col[n.kind]}">${n.kind==='entity'?'THIS ENTITY':n.kind.toUpperCase()}</text></g>`;});
 return `<svg viewBox="0 0 ${W} ${H}" width="100%" style="max-height:360px"><defs><marker id="ar" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#aab4c0"/></marker></defs>${lines}${boxes}</svg>
  <div class="legend">▮ <span style="color:#8A1538">entity</span> · ▮ <span style="color:#7d3c98">government</span> · ▮ <span style="color:#1f8a4c">resident private</span> · ▮ <span style="color:#b9651b">non-resident</span> — arrows point owner→owned.</div>`;
}

function vClassification(){
 return `<div class="card"><div class="hd"><span class="ic">${svg('rules')}</span>Classification results (live 18-test methodology)</div><div class="bd scroll">
  <table class="tbl"><tr><th>Enterprise</th><th>Sector</th><th>Public/Private</th><th>Control</th><th>Market</th><th>Size</th><th>FDI</th><th>Conf.</th><th></th></tr>
  ${DATA.enterprises.map(e=>`<tr><td><b>${esc(e.name)}</b></td><td>${chip(e.sector,'bg-gray')}</td><td>${ppBadge(e.public_private)}</td><td>${chip(e.control,'bg-gray')}</td><td>${e.market==='MARKET'?chip('MARKET','bg-green'):chip('NON-MARKET','bg-amber')}</td><td>${esc(e.size)}</td><td>${e.fdi==='NONE'?'—':chip(e.fdi,'bg-amber')}</td><td>${e.confidence}</td><td><button class="btn sm soft" onclick="go('studio',{studioId:'${e.id}'})">Run</button></td></tr>`).join("")}</table></div></div>`;
}

function vRegistry(){
 const f=(state.filter||"").toLowerCase();
 const filt=DATA.enterprises.filter(e=>(state.ppFilter==='all'||e.public_private===state.ppFilter)&&(!f||(e.name+e.id+e.sector+e.public_private).toLowerCase().includes(f)));
 const pps=["all",...Object.keys(PP)];
 return `<div class="card"><div class="bd">
  <div class="search" style="max-width:380px;margin-bottom:12px">${svg('search')}<input placeholder="Search name, ID, sector…" value="${esc(state.filter)}" oninput="state.filter=this.value;render()"/></div>
  <div class="chips">${pps.map(p=>`<span class="fchip ${state.ppFilter===p?'on':''}" onclick="state.ppFilter='${p}';render()">${p==='all'?'All':esc(p)}</span>`).join("")}</div>
  <div class="scroll"><table class="tbl"><tr><th>Enterprise</th><th>ID</th><th>Sector</th><th>Public/Private</th><th>Size</th><th>Control</th><th>FDI</th><th>Quality</th></tr>
  ${filt.map(e=>`<tr class="row" onclick="go('profile',{entId:'${e.id}',tab:0})"><td style="display:flex;gap:9px;align-items:center"><span style="width:26px;height:26px;border-radius:7px;background:var(--surface2);display:inline-flex;align-items:center;justify-content:center;color:var(--maroon)">${svg(entIcon(e))}</span><b>${esc(e.name)}</b></td><td class="mono small">${esc(e.id.slice(-8))}</td><td>${esc(e.sector)}</td><td>${ppBadge(e.public_private)}</td><td>${esc(e.size)}</td><td>${chip(e.control,'bg-gray')}</td><td>${e.fdi==='NONE'?'—':esc(e.fdi)}</td><td><span style="color:${qcolor(e.quality.overall_score)};font-weight:700">${e.quality.overall_score}</span></td></tr>`).join("")}</table>
  <div class="small" style="margin-top:10px">${filt.length} of ${DATA.enterprises.length} enterprises</div></div></div></div>`;
}

function vProfile(){
 const e=ent(state.entId),o=e.ownership;
 const T=["Overview","Ownership network","Classification & explainability","Quality","History","Audit"];
 const head=`<div class="card" style="margin-bottom:16px"><div class="bd"><div style="display:flex;gap:14px;align-items:center;flex-wrap:wrap">
   <span style="width:48px;height:48px;border-radius:12px;background:linear-gradient(135deg,var(--maroon),#5c0e25);color:#fff;display:flex;align-items:center;justify-content:center">${svg(entIcon(e))}</span>
   <div style="flex:1;min-width:200px"><div style="font-size:18px;font-weight:700">${esc(e.name)}</div><div class="small mono">${esc(e.id)} · LEI ${esc(e.lei||'—')}</div></div>
   <div style="display:flex;gap:7px;flex-wrap:wrap">${chip(e.sector+' '+e.sector_name,'bg-gray')}${ppBadge(e.public_private)}${chip(e.size,'bg-gray')}${e.fdi!=='NONE'?chip(e.fdi,'bg-amber'):''}</div>
   <button class="btn" onclick="go('studio',{studioId:'${e.id}'})">${svg('play')} Classify</button></div></div></div>`;
 const sel=`<select onchange="state.entId=this.value;render()" style="margin-bottom:12px;padding:8px;border:1px solid var(--line);border-radius:9px">${DATA.enterprises.map(x=>`<option value="${x.id}" ${x.id===e.id?'selected':''}>${esc(x.name)}</option>`).join("")}</select>`;
 const tabs=`<div class="tabs">${T.map((t,i)=>`<button class="${state.tab===i?'active':''}" onclick="state.tab=${i};render()">${t}</button>`).join("")}</div>`;
 let body="";
 if(state.tab===0){const lus=DATA.legal_units.filter(l=>l.enterprise_id===e.id),ests=DATA.establishments.filter(x=>x.enterprise_id===e.id);
   body=`<div class="grid g11"><div class="card"><div class="hd">Master data</div><div class="bd"><div class="kv">
     <div class="k">Arabic name</div><div dir="rtl">${esc(e.name_ar)||'—'}</div><div class="k">Legal form</div><div>${esc(e.legal_form)} · ${esc(e.legal_form_name)}</div>
     <div class="k">ISIC Rev.4</div><div>${esc(e.isic)}</div><div class="k">Residence</div><div>${esc(e.residence)}</div>
     <div class="k">Jurisdiction</div><div>${esc(e.jurisdiction)}</div><div class="k">Employment</div><div>${e.employment==null?'—':e.employment} FTE</div>
     <div class="k">Turnover</div><div>${money(e.turnover)}</div><div class="k">Enterprise group</div><div>${esc(e.group_id)||'—'}</div></div></div></div>
    <div class="card"><div class="hd">Legal units & establishments</div><div class="bd">
     <div class="small" style="font-weight:650;margin-bottom:5px">Legal units (${lus.length})</div>${lus.map(l=>`<div style="font-size:12.5px;margin:3px 0">• ${esc(l.name)} <span class="small mono">${esc(l.cr_number||'')} · ${esc(l.authority||'')}</span></div>`).join("")||'<div class="small">—</div>'}
     <div class="small" style="font-weight:650;margin:10px 0 5px">Establishments (${ests.length})</div>${ests.map(x=>`<div style="font-size:12.5px;margin:3px 0">• ${esc(x.name)} <span class="small">${esc(x.zone||'')} · ${x.employment||0} FTE</span></div>`).join("")||'<div class="small">—</div>'}</div></div></div>`;}
 else if(state.tab===1){body=`<div class="grid g2"><div class="card"><div class="hd"><span class="ic">${svg('own')}</span>Ownership network</div><div class="bd"><div class="svgwrap">${ownershipSVG(e)}</div></div></div>
   <div class="card"><div class="hd">Control intelligence</div><div class="bd"><div class="kv" style="grid-template-columns:1fr auto">
     <div class="k">Effective government ownership</div><div><b>${o.government_pct}%</b></div><div class="k">Government voting</div><div>${o.government_voting}%</div>
     <div class="k">Effective foreign ownership</div><div>${o.foreign_pct}%</div><div class="k">Government control</div><div>${o.government_control?chip('Yes','bg-purple'):'<span class="small">No</span>'}</div>
     <div class="k">Control indicators</div><div>${(o.control_indicators||[]).map(c=>chip(c,'bg-gray')).join(' ')||'—'}</div>
     <div class="k">Ultimate controlling unit</div><div>${o.uci?esc(o.uci.uci_name)+(o.uci.is_government?' '+chip('Govt','bg-purple'):''):'—'}</div></div></div></div></div>`;}
 else if(state.tab===2){const ar=e.applied_rules;body=`<div class="card"><div class="hd"><span class="ic">${svg('rules')}</span>Why this classification — applied rules</div><div class="bd scroll">
   <table class="tbl"><tr><th>Test</th><th>Rule</th><th>Output</th><th>Standard</th><th>Rationale</th></tr>
   ${ar.map(a=>`<tr><td>${esc(a.test)}</td><td class="mono">${esc(a.rule_id)}</td><td>${Object.entries(a.output||{}).map(([k,v])=>chip(esc(typeof v==='object'?JSON.stringify(v):v),'bg-green')).join(' ')}</td><td class="small">${esc(a.standard_ref)}</td><td class="small">${esc(a.rationale)}</td></tr>`).join("")}</table>
   <div class="note" style="margin-top:12px"><b>Confidence ${e.confidence}</b> · rule-based & fully reproducible. Data sources: CSBR golden record · ownership graph · reference codelists.</div></div></div>`;}
 else if(state.tab===3){const q=e.quality,dims=["completeness","validity","consistency","uniqueness","accuracy","timeliness"];
   body=`<div class="grid g2"><div class="card"><div class="hd">Quality dimensions</div><div class="bd">${ring(q.overall_score,'Overall quality','mean of six DAMA dimensions')}${dims.map(d=>`<div class="barrow"><div>${d}</div><div class="bar"><span style="width:${q[d]*100}%"></span></div><div style="text-align:right">${q[d]}</div></div>`).join("")}</div></div>
    <div class="card"><div class="hd">Validation exceptions (${e.exceptions.length})</div><div class="bd scroll"><table class="tbl"><tr><th>Rule</th><th>Severity</th><th>Message</th></tr>${e.exceptions.map(x=>`<tr><td class="mono">${esc(x.rule_id)}</td><td>${sevPill(x.severity)}</td><td>${esc(x.message)}</td></tr>`).join("")||'<tr><td colspan=3 style="color:var(--green)">No exceptions — passes all validation rules.</td></tr>'}</table></div></div></div>`;}
 else if(state.tab===4){body=`<div class="card"><div class="hd">Classification history (temporal versioning)</div><div class="bd scroll"><table class="tbl"><tr><th>Version</th><th>Sector</th><th>Public/Private</th><th>Control</th><th>Status</th><th>Source</th></tr>
   <tr><td>v2</td><td>${esc(e.sector)}</td><td>${ppBadge(e.public_private)}</td><td>${esc(e.control)}</td><td>${chip('current','bg-green')}</td><td>Automated re-run</td></tr>
   <tr><td>v1</td><td>${esc(e.sector)}</td><td>${ppBadge(e.public_private)}</td><td>${esc(e.control)}</td><td class="small">superseded</td><td>Initial classification</td></tr></table>
   <div class="note" style="margin-top:12px">Every re-classification writes a new immutable version with <span class="mono">valid_from/valid_to</span>, so any historical classification can be reproduced exactly.</div></div></div>`;}
 else{body=`<div class="card"><div class="hd">Audit trail</div><div class="bd scroll"><table class="tbl"><tr><th>When</th><th>Action</th><th>Field</th><th>Old → New</th><th>By</th><th>Evidence</th></tr>
   ${e.audit.map(a=>`<tr><td class="small">${esc(a.timestamp)}</td><td>${esc(a.action)}</td><td>${esc(a.field)||'—'}</td><td>${esc(a.old)||'—'} → ${esc(a.new)||'—'}</td><td>${esc(a.by)}</td><td class="small">${esc(a.evidence)||'—'}</td></tr>`).join("")}</table></div></div>`;}
 return sel+head+tabs+body;
}

function vOwnership(){
 const e=ent(state.entId),o=e.ownership;
 return `<select onchange="state.entId=this.value;render()" style="margin-bottom:12px;padding:8px;border:1px solid var(--line);border-radius:9px">${DATA.enterprises.map(x=>`<option value="${x.id}" ${x.id===e.id?'selected':''}>${esc(x.name)}</option>`).join("")}</select>
  <div class="grid g2"><div class="card"><div class="hd"><span class="ic">${svg('own')}</span>Ownership network — ${esc(e.name)}</div><div class="bd"><div class="svgwrap">${ownershipSVG(e)}</div></div></div>
  <div class="card"><div class="hd">Effective control</div><div class="bd"><div class="kv" style="grid-template-columns:1fr auto">
    <div class="k">Government ownership</div><div><b>${o.government_pct}%</b></div><div class="k">Government voting</div><div>${o.government_voting}%</div>
    <div class="k">Foreign ownership</div><div>${o.foreign_pct}%</div><div class="k">Government control</div><div>${o.government_control?chip('Yes','bg-purple'):'No'}</div>
    <div class="k">Indicators</div><div>${(o.control_indicators||[]).map(c=>chip(c,'bg-gray')).join(' ')||'—'}</div>
    <div class="k">UCI</div><div>${o.uci?esc(o.uci.uci_name):'—'}</div></div>
    <table class="tbl" style="margin-top:12px"><tr><th>Owner</th><th>Equity</th><th>Voting</th><th>Control</th><th>Origin</th></tr>
    ${o.edges.map(x=>`<tr><td>${esc(x.owner_name||x.owner_id)}</td><td>${x.ownership_pct}%</td><td>${x.voting_pct}%</td><td>${esc(x.control_indicator)||'—'}</td><td>${x.is_government?chip('Government','bg-purple'):(x.is_resident?'Resident':chip('Non-resident','bg-amber'))}</td></tr>`).join("")||'<tr><td colspan=5 class="small">No recorded owners</td></tr>'}</table></div></div></div>`;
}

function vGroups(){
 return DATA.groups.map(g=>{const head=ent(g.domestic_head);
  const members=g.members.map(m=>{const me=ent(m);const kind=me&&me.public_private&&me.public_private.startsWith("PUB")?"gov":(me&&me.public_private==="FCC"?"foreign":"priv");return `<div class="lvl"><span class="gnode ${kind}" style="cursor:pointer" onclick="go('profile',{entId:'${m}',tab:1})">${esc(me?me.name:m)} <span class="small">· ${esc(me?me.sector:'')} ${esc(me?me.public_private:'')}</span></span></div>`;}).join("");
  return `<div class="card" style="margin-bottom:16px"><div class="hd"><span class="ic">${svg('group')}</span>${esc(g.name)} <span class="small">(${esc(g.group_id)})</span></div><div class="bd">
   <div class="kv"><div class="k">Global ultimate parent</div><div>${esc(g.gup)} (${esc(g.gup_country)})</div><div class="k">Truncated (resident) group</div><div>${g.truncated==="Y"?"Yes":"No"}</div><div class="k">Controlling sector</div><div>${esc(g.controlling_sector)}</div><div class="k">Members in register</div><div>${g.members.length} of ${g.member_count}</div></div>
   <div class="gtree" style="margin-top:14px"><span class="gnode" style="border-color:#444">${esc(g.gup)} <span class="small">· global ultimate parent</span></span>
    <div class="lvl"><span class="gnode entity" style="cursor:pointer" onclick="go('profile',{entId:'${g.domestic_head}'})">${esc(head?head.name:g.domestic_head)} <span class="small">· domestic head</span></span>${members}</div></div>
   <p class="small" style="margin-top:8px">${esc(g.notes)}</p></div></div>`;}).join("");
}

function vRegisters(){
 const sheets=["Enterprise Register","Legal Units","Establishments","Enterprise Groups","Sector codelist","Validation rules"];
 const tabs=`<div class="sheettabs">${sheets.map((s,i)=>`<button class="${state.sheet===i?'active':''}" onclick="state.sheet=${i};render()">${s}</button>`).join("")}</div>`;
 let t="";const E=DATA.enterprises;
 if(state.sheet===0){t=`<table class="tbl"><tr><th>enterprise_id</th><th>legal_name_en</th><th>legal_form</th><th>sector_code</th><th>public_private</th><th>control_flag</th><th>isic</th><th>residence</th><th>size_class</th><th>group_id</th></tr>${E.map(e=>`<tr><td class="mono">${esc(e.id)}</td><td>${esc(e.name)}</td><td>${esc(e.legal_form)}</td><td>${esc(e.sector)}</td><td>${esc(e.public_private)}</td><td>${esc(e.control)}</td><td>${esc(e.isic)}</td><td>${esc(e.residence)}</td><td>${esc(e.size)}</td><td class="mono small">${esc(e.group_id)||''}</td></tr>`).join("")}</table>`;}
 else if(state.sheet===1){t=`<table class="tbl"><tr><th>legal_unit_id</th><th>enterprise_id</th><th>name</th><th>legal_form</th><th>cr_number</th><th>authority</th><th>LEI</th></tr>${DATA.legal_units.map(l=>`<tr><td class="mono">${esc(l.id)}</td><td class="mono small">${esc(l.enterprise_id)}</td><td>${esc(l.name)}</td><td>${esc(l.legal_form)}</td><td>${esc(l.cr_number)}</td><td>${esc(l.authority)}</td><td class="mono small">${esc(l.lei)||''}</td></tr>`).join("")}</table>`;}
 else if(state.sheet===2){t=`<table class="tbl"><tr><th>establishment_id</th><th>enterprise_id</th><th>name</th><th>isic</th><th>municipality</th><th>zone</th><th>employment</th></tr>${DATA.establishments.map(x=>`<tr><td class="mono">${esc(x.id)}</td><td class="mono small">${esc(x.enterprise_id)}</td><td>${esc(x.name)}</td><td>${esc(x.isic)}</td><td>${esc(x.municipality)}</td><td>${esc(x.zone)}</td><td>${x.employment}</td></tr>`).join("")}</table>`;}
 else if(state.sheet===3){t=`<table class="tbl"><tr><th>group_id</th><th>name</th><th>global_ultimate_parent</th><th>country</th><th>domestic_head</th><th>truncated</th><th>members</th></tr>${DATA.groups.map(g=>`<tr><td class="mono">${esc(g.group_id)}</td><td>${esc(g.name)}</td><td>${esc(g.gup)}</td><td>${esc(g.gup_country)}</td><td class="mono small">${esc(g.domestic_head)}</td><td>${esc(g.truncated)}</td><td>${g.member_count}</td></tr>`).join("")}</table>`;}
 else if(state.sheet===4){t=`<table class="tbl"><tr><th>code</th><th>institutional sector (SNA)</th></tr>${SECTORS.map(s=>`<tr><td class="mono">${esc(s[0])}</td><td>${esc(s[1])}</td></tr>`).join("")}</table>`;}
 else{t=`<table class="tbl"><tr><th>rule_id</th><th>name</th><th>test</th><th>standard</th></tr>${DATA.rules.filter(r=>r.test_code.match(/T(05|06|07|08|10|12|13)/)).map(r=>`<tr><td class="mono">${esc(r.rule_id)}</td><td>${esc(r.name)}</td><td>${esc(r.test_code)}</td><td class="small">${esc(r.standard_ref)}</td></tr>`).join("")}</table>`;}
 return `<div class="help">${svg('info')}<div>These are the platform's statistical registers — the live, database-backed equivalent of the implementation workbook's sheets. The structure (persistent IDs, codelists, validation rules) matches the workbook exactly.</div></div>${tabs}<div class="sheetbody scroll">${t}</div>`;
}
const SECTORS=[["S.11","Non-financial corporations"],["S.121","Central bank"],["S.122","Deposit-taking corporations"],["S.124","Non-MMF investment funds"],["S.126","Financial auxiliaries"],["S.127","Captive financial institutions"],["S.128","Insurance corporations"],["S.129","Pension funds"],["S.13","General government"],["S.14","Households"],["S.15","NPISH"],["S.2","Rest of the World"]];

function vRules(){
 const cur=state.ruleId?DATA.rules.find(r=>r.rule_id===state.ruleId):DATA.rules[0];
 const list=DATA.rules.map(r=>`<tr class="row ${r.rule_id===cur.rule_id?'':''}" onclick="state.ruleId='${r.rule_id}';render()"><td class="mono">${esc(r.rule_id)}</td><td>${esc(r.name)}</td><td>${chip(r.test_code,'bg-gray')}</td></tr>`).join("");
 const facts=suggestFacts(cur);
 return `<div class="card" style="margin-bottom:16px"><div class="hd"><span class="ic">${svg('rules')}</span>The 18 sequenced classification tests</div><div class="bd"><div style="display:flex;gap:8px;flex-wrap:wrap">${DATA.tests.map(t=>`<span class="badge bg-gray" title="${esc(t.description)}">${esc(t.test_code)} · ${esc(t.name)}</span>`).join("")}</div></div></div>
  <div class="grid g2"><div class="card"><div class="hd">Rules repository (${DATA.rules.length})</div><div class="bd scroll" style="max-height:520px"><table class="tbl"><tr><th>ID</th><th>Name</th><th>Test</th></tr>${list}</table></div></div>
  <div><div class="card"><div class="hd">${esc(cur.rule_id)} — ${esc(cur.name)}</div><div class="bd"><div class="kv" style="grid-template-columns:130px 1fr">
    <div class="k">Test · domain</div><div>${esc(cur.test_code)} · ${esc(cur.domain)}</div><div class="k">Standard</div><div>${esc(cur.standard_ref)}</div>
    <div class="k">Priority · conf.</div><div>${cur.priority} · ${cur.confidence}</div><div class="k">Approval</div><div>${chip(cur.approval_status,'bg-green')} v${esc(cur.version)}</div>
    <div class="k">Rationale</div><div>${esc(cur.rationale)}</div></div>
    <div class="small" style="margin:10px 0 4px">Logic (JSON condition tree)</div><pre class="mono" style="background:var(--surface2);border:1px solid var(--line);padding:9px;border-radius:8px;white-space:pre-wrap;font-size:11.5px">${esc(JSON.stringify(cur.logic,null,1))}</pre>
    <div class="small">Output: <span class="mono">${esc(JSON.stringify(cur.output))}</span></div></div></div>
   <div class="card" style="margin-top:16px"><div class="hd">Rule tester</div><div class="bd"><div class="small" style="margin-bottom:6px">Edit the facts and evaluate this rule (same evaluator as the engine).</div>
    <textarea id="rtf">${esc(JSON.stringify(facts,null,1))}</textarea><div style="margin-top:8px"><button class="btn sm" onclick="testRule('${cur.rule_id}')">${svg('play')} Evaluate</button> <span id="rtres"></span></div></div></div></div></div>`;
}
function suggestFacts(r){const f={};(function w(c){if(!c)return;if(c.all)c.all.forEach(w);else if(c.any)c.any.forEach(w);else if(c.not)w(c.not);else if(c.op){if(c.op==="eq"||c.op==="in")f[c.field]=Array.isArray(c.value)?c.value[0]:c.value;else if(["gt","gte","lt","lte"].includes(c.op))f[c.field]=c.value;else if(c.op==="truthy")f[c.field]=true;else if(c.op==="exists")f[c.field]="…";}})(r.logic);return f;}
function testRule(id){const r=DATA.rules.find(x=>x.rule_id===id);let f;try{f=JSON.parse(document.getElementById("rtf").value);}catch(e){document.getElementById("rtres").innerHTML='<span style="color:var(--red)">Invalid JSON</span>';return;}const m=evalCond(r.logic,f);document.getElementById("rtres").innerHTML=m?`<span style="color:var(--green)">✔ MATCH → ${esc(JSON.stringify(r.output))}</span>`:'<span style="color:var(--red)">✘ no match</span>';}

function vMetadata(){return `<div class="card"><div class="hd"><span class="ic">${svg('meta')}</span>Metadata repository (GSIM/SDMX-aligned)</div><div class="bd scroll"><table class="tbl"><tr><th>Entity</th><th>Field</th><th>Definition</th><th>Type</th><th>Allowed</th><th>Mand.</th><th>Source</th></tr>
 ${DATA.metadata.map(m=>`<tr><td class="small">${esc(m.entity)}</td><td class="mono">${esc(m.field)}</td><td>${esc(m.definition)}</td><td class="small">${esc(m.data_type)}</td><td class="small">${esc(m.allowed_values)}</td><td>${m.mandatory?chip('Y','bg-green'):'N'}</td><td class="small">${esc(m.source)}</td></tr>`).join("")}</table></div></div>`;}

function vStandards(){return DATA.standards.map(s=>`<div class="card" style="margin-bottom:14px"><div class="hd"><span class="ic">${svg('std')}</span>${esc(s.code)} — ${esc(s.name)}</div><div class="bd"><div class="small">${esc(s.issuer)} · ${esc(s.edition)} · ${esc(s.domains)}</div><p>${esc(s.description)}</p>${s.concepts.length?`<table class="tbl"><tr><th>Concept</th><th>Definition</th><th>Ref</th></tr>${s.concepts.map(c=>`<tr><td>${esc(c.concept)}</td><td>${esc(c.definition)}</td><td class="small">${esc(c.reference)}</td></tr>`).join("")}</table>`:''}</div></div>`).join("");}

function vQuality(){const E=DATA.enterprises,dims=["completeness","validity","consistency","uniqueness","accuracy","timeliness","overall_score"];const agg={};dims.forEach(d=>agg[d]=(E.reduce((s,e)=>s+e.quality[d],0)/E.length));
 return `<div class="grid tiles" style="margin-bottom:16px">${dims.map(d=>`<div class="tile"><div class="v" style="color:${qcolor(agg[d])}">${agg[d].toFixed(2)}</div><div class="l">${d.replace("_"," ")}</div></div>`).join("")}</div>
  <div class="card"><div class="hd"><span class="ic">${svg('quality')}</span>Per-enterprise quality</div><div class="bd scroll"><table class="tbl"><tr><th>Enterprise</th>${dims.map(d=>`<th>${d.slice(0,5)}</th>`).join("")}</tr>${E.map(e=>`<tr><td>${esc(e.name)}</td>${dims.map(d=>`<td style="color:${qcolor(e.quality[d])};font-weight:600">${e.quality[d]}</td>`).join("")}</tr>`).join("")}</table></div></div>`;}

function vValidation(){const all=[];DATA.enterprises.forEach(e=>e.exceptions.forEach(x=>all.push({name:e.name,...x})));
 const c=(s)=>all.filter(a=>a.severity===s).length;
 return `<div class="grid tiles" style="margin-bottom:16px"><div class="tile"><div class="v">${all.length}</div><div class="l">Open exceptions</div></div><div class="tile"><div class="v" style="color:var(--red)">${c('ERROR')}</div><div class="l">Errors</div></div><div class="tile"><div class="v" style="color:var(--amber)">${c('WARN')}</div><div class="l">Warnings</div></div><div class="tile"><div class="v" style="color:var(--blue)">${c('INFO')}</div><div class="l">Info</div></div></div>
  <div class="card"><div class="hd"><span class="ic">${svg('valid')}</span>Exceptions (VR-001..VR-018)</div><div class="bd scroll"><table class="tbl"><tr><th>Enterprise</th><th>Rule</th><th>Severity</th><th>Message</th><th>Action</th></tr>${all.map(a=>`<tr><td>${esc(a.name)}</td><td class="mono">${esc(a.rule_id)}</td><td>${sevPill(a.severity)}</td><td>${esc(a.message)}</td><td class="small">${esc(a.action)}</td></tr>`).join("")||'<tr><td colspan=5 style="color:var(--green)">No exceptions.</td></tr>'}</table></div></div>`;}

function vReviews(){return `<div class="help">${svg('info')}<div>Anomalies and exceptions routed for human adjudication. AI assists by flagging; the Technical Classification Committee decides. Official classifications stay rule-based.</div></div>
 <div class="card"><div class="hd"><span class="ic">${svg('review')}</span>Manual review queue</div><div class="bd scroll"><table class="tbl"><tr><th>Enterprise</th><th>Type</th><th>Severity</th><th>Title</th><th>Status</th><th></th></tr>${DATA.reviews.length?DATA.reviews.map(r=>`<tr><td class="mono small">${esc(r.enterprise_id)}</td><td>${esc(r.kind)}</td><td>${sevPill(r.severity)}</td><td>${esc(r.title)}<div class="small">${esc(r.detail)}</div></td><td>${esc(r.status)}</td><td><button class="btn sm soft" onclick="alert('Workflow: assign → investigate → resolve / refer to Committee / apply override.')">Resolve</button></td></tr>`).join(""):'<tr><td colspan=6 style="color:var(--green)">No open review items.</td></tr>'}</table></div></div>`;}

function vAudit(){return `<div class="card"><div class="hd"><span class="ic">${svg('audit')}</span>Audit trail</div><div class="bd scroll"><table class="tbl"><tr><th>When</th><th>Record</th><th>Action</th><th>Field</th><th>Old → New</th><th>By</th></tr>${DATA.audit.slice(0,80).map(a=>`<tr><td class="small">${esc(a.timestamp)}</td><td class="mono small">${esc(a.record_id)}</td><td>${esc(a.action)}</td><td>${esc(a.field)||'—'}</td><td>${esc(a.old)||'—'} → ${esc(a.new)||'—'}</td><td>${esc(a.by)}</td></tr>`).join("")}</table></div></div>`;}

const EP=[["POST","/api/auth/login","Authenticate; returns JWT + role",'{"access_token":"eyJ…","role":"Classifier"}'],["GET","/api/dashboard","KPIs & breakdowns",'{"total_enterprises":33,"by_sector":{…}}'],["POST","/api/enterprises/{id}/classify","Run the 18-test classification",'{"sector_code":"S.122","public_private":"PUB-FC","confidence":1.0}'],["GET","/api/enterprises/{id}/explain","Full explainability",'{"applied_rules":[…],"data_fields_used":{…}}'],["GET","/api/enterprises/{id}/profile","Master data + ownership + quality + audit","{…}"],["POST","/api/rules/{id}/test","Evaluate a rule against facts",'{"matched":true,"output":{…}}'],["POST","/api/simulate","Sandbox what-if classification",'{"sandbox":true,"result":{…}}'],["GET","/api/quality","Dataset & per-enterprise quality","{…}"]];
function vApi(){return `<div class="card"><div class="hd"><span class="ic">${svg('api')}</span>REST API (OpenAPI at /docs)</div><div class="bd scroll"><table class="tbl"><tr><th>Method</th><th>Endpoint</th><th>Purpose</th><th></th></tr>${EP.map((e,i)=>`<tr><td>${chip(e[0],e[0]==='GET'?'bg-blue':'bg-green')}</td><td class="mono">${esc(e[1])}</td><td>${esc(e[2])}</td><td><button class="btn sm soft" onclick="document.getElementById('ep${i}').style.display='table-row'">Try</button></td></tr><tr id="ep${i}" style="display:none"><td colspan=4><pre class="mono" style="background:#101826;color:#d6e2ee;padding:11px;border-radius:8px;white-space:pre-wrap">HTTP 200 OK\n${esc(e[3])}</pre></td></tr>`).join("")}</table></div></div>`;}

function vUsers(){const perms=[...new Set(Object.values(DATA.roles).flat())].sort();
 return `<div class="card" style="margin-bottom:16px"><div class="hd"><span class="ic">${svg('users')}</span>Users</div><div class="bd scroll"><table class="tbl"><tr><th>Username</th><th>Name</th><th>Role</th><th>Email</th></tr>${DATA.users.map(u=>`<tr><td class="mono">${esc(u.username)}</td><td>${esc(u.full_name)}</td><td>${chip(u.role,'bg-blue')}</td><td class="small">${esc(u.email)}</td></tr>`).join("")}</table></div></div>
  <div class="card"><div class="hd">Permission matrix</div><div class="bd scroll"><table class="tbl"><tr><th>Permission</th>${Object.keys(DATA.roles).map(r=>`<th>${esc(r.slice(0,4))}</th>`).join("")}</tr>${perms.map(p=>`<tr><td class="mono">${esc(p)}</td>${Object.keys(DATA.roles).map(r=>`<td>${(DATA.roles[r].includes("*")||DATA.roles[r].includes(p))?'<span style="color:var(--green)">✔</span>':'·'}</td>`).join("")}</tr>`).join("")}</table><div class="small" style="margin-top:8px">Administrator holds the wildcard (*) permission.</div></div></div>`;}

function vUat(){const c=DATA.uat,pass=c.filter(r=>r[4]==="Pass").length;
 return `<div class="grid tiles" style="margin-bottom:16px"><div class="tile"><div class="v">100+</div><div class="l">UAT cases (full suite)</div></div><div class="tile"><div class="v" style="color:var(--green)">${pass}/${c.length}</div><div class="l">Demo set passing</div></div><div class="tile"><div class="v" style="color:var(--green)">33/33</div><div class="l">Classification verdicts</div></div><div class="tile"><div class="v" style="color:var(--green)">40/40</div><div class="l">Rules verified</div></div></div>
  <div class="card" style="margin-bottom:16px"><div class="hd"><span class="ic">${svg('uat')}</span>Representative acceptance tests</div><div class="bd scroll"><table class="tbl"><tr><th>Test ID</th><th>Area</th><th>Description</th><th>Expected result</th><th>Status</th></tr>${c.map(r=>`<tr><td class="mono">${esc(r[0])}</td><td>${esc(r[1])}</td><td>${esc(r[2])}</td><td>${esc(r[3])}</td><td>${chip(r[4],'bg-green')}</td></tr>`).join("")}</table></div></div>
  <div class="card"><div class="hd">Acceptance criteria (production gate)</div><div class="bd"><ul class="tight"><li>Methodology traceability <b>100%</b> ✔</li><li>Classification accuracy on golden set <b>33/33</b> ✔</li><li>Rules verified (positive + negative) <b>40/40</b> ✔</li><li>Validation library VR-001..VR-018 <b>18/18</b> ✔</li><li>Explainability + audit for <b>100%</b> of classifications ✔</li><li>Quality KPIs (to measure at pilot): error ≤2%, time-to-classify ≤10 days, override ≤5%, LEI 100%</li></ul></div></div>`;}

function vGap(){const g=DATA.gap,box=(t,a,cls)=>`<div class="card"><div class="hd">${t}</div><div class="bd"><ul class="tight">${a.map(x=>`<li>${esc(x)}</li>`).join("")}</ul></div></div>`;
 return `<div class="grid g11" style="margin-bottom:16px">${box("✔ Fully implemented",g.implemented)}${box("◑ Partially implemented",g.partial)}</div>
  <div class="grid g11" style="margin-bottom:16px">${box("→ Future enhancements",g.future)}${box("⚠ Production-readiness gaps",g.production_gaps)}</div>
  <div class="card"><div class="hd"><span class="ic">${svg('gap')}</span>Production readiness assessment</div><div class="bd scroll"><table class="tbl"><tr><th>Dimension</th><th>Status</th><th>Notes</th></tr>${DATA.readiness.map(r=>`<tr><td>${esc(r[0])}</td><td><span class="rag ${r[1].replace(/[^A-Za-z]/g,'')}">${esc(r[1])}</span></td><td>${esc(r[2])}</td></tr>`).join("")}</table>
   <div class="note" style="margin-top:12px"><b>Recommendation:</b> Methodology and data-governance readiness are <span class="rag Green">Green</span>. Proceed to a controlled <b>pilot</b> on the largest 100 enterprises after closing security hardening and one administrative-source integration; defer production until HA, load testing, secrets management and data-sharing instruments under the Statistics Law are in place.</div></div></div>`;}

const VIEWS={dashboard:vDashboard,studio:vStudio,classification:vClassification,registry:vRegistry,profile:vProfile,ownership:vOwnership,groups:vGroups,registers:vRegisters,rules:vRules,metadata:vMetadata,standards:vStandards,quality:vQuality,validation:vValidation,reviews:vReviews,audit:vAudit,api:vApi,users:vUsers,uat:vUat,gap:vGap};

function render(){
 document.getElementById("nav").innerHTML=NAV.map(sec=>`<div class="navsec"><div class="lbl">${sec[0]}</div>${sec[1].map(m=>`<a class="${state.view===m[0]?'active':''}" onclick="go('${m[0]}')">${svg(m[2])}<span>${m[1]}</span></a>`).join("")}</div>`).join("");
 const rs=document.getElementById("rolesel");if(!rs.options.length){rs.innerHTML=Object.keys(DATA.roles).map(r=>`<option ${r==='Classifier'?'selected':''}>${r}</option>`).join("");}
 document.getElementById("av").textContent=(state.role||'CL').slice(0,2).toUpperCase();
 document.getElementById("crumb").innerHTML=`${esc(TITLES[state.view]||'')} <span class="ctx">· NEICS</span>`;
 const help=HELP[state.view]?`<div class="help">${svg('info')}<div>${HELP[state.view]}</div></div>`:"";
 document.getElementById("content").innerHTML=`<div class="h-page">${esc(TITLES[state.view]||'')}</div><div class="h-sub">National Enterprise Intelligence &amp; Classification System · State of Qatar</div>${help}`+(VIEWS[state.view]||vDashboard)();
}
render();
</script>
</body>
</html>
"""

# Inline a couple of small SVGs used directly in the static HTML head.
HTML_TEMPLATE = HTML_TEMPLATE.replace(
    "{svg_search}",
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
    'stroke-linecap="round" stroke-linejoin="round"><path d="M21 21l-4.3-4.3M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16z"/></svg>',
)
