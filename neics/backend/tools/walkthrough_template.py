"""Single-file clickable prototype: Qatar Enterprise Classification Platform.

`/*__DATA__*/` is replaced by build_walkthrough.py with the embedded JSON (data,
rules, the 18 tests, standards, sectors, ISIC, integration sources, governance —
all extracted from the source files). A faithful in-browser port of the backend
classification engine computes every result live. One file, inline CSS/JS, no
external dependencies — runs by double-clicking.
"""

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Qatar Enterprise Classification Platform — UAT Prototype</title>
<style>
:root{
 --navy:#1B2A41;--maroon:#8A1538;--gold:#C9A961;--green:#2E7D6B;--blue:#2C5F8A;
 --paper:#F4F4F6;--rule:#D8D8DD;--ink:#222633;--muted:#5f6675;--white:#fff;
 --navy-2:#24364f;--maroon-d:#6f1029;
}
*{box-sizing:border-box}
body{margin:0;font-family:Arial,Helvetica,sans-serif;background:var(--paper);color:var(--ink);font-size:14px;line-height:1.55;-webkit-text-size-adjust:100%}
h1,h2,h3,.serif,.title{font-family:Georgia,"Times New Roman",serif}
a{color:var(--maroon);text-decoration:none;cursor:pointer}
button{font-family:inherit;cursor:pointer}
input,select,textarea{font-family:inherit;font-size:13.5px}
/* Header + banner */
.header{background:var(--navy);color:#fff;display:flex;align-items:center;gap:14px;padding:10px 18px;position:sticky;top:0;z-index:60}
.header .crest{width:38px;height:38px;border-radius:6px;background:var(--gold);color:var(--navy);font-weight:800;display:flex;align-items:center;justify-content:center;font-family:Georgia,serif;font-size:18px}
.header .ttl{font-family:Georgia,serif;font-size:17px;font-weight:700;letter-spacing:.2px}
.header .ttl small{display:block;font-family:Arial;font-weight:400;font-size:10.5px;color:#c7cedb;letter-spacing:.3px}
.header .sp{flex:1}
.menubtn{display:none;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.3);color:#fff;border-radius:6px;padding:5px 10px;font-size:17px}
.banner{background:var(--maroon);color:#fff;text-align:center;font-size:12px;font-weight:700;letter-spacing:.4px;padding:6px 10px;position:sticky;top:58px;z-index:55}
.layout{display:flex;min-height:calc(100vh - 90px)}
.side{width:248px;flex-shrink:0;background:var(--navy);color:#dfe4ee;position:sticky;top:90px;height:calc(100vh - 90px);overflow-y:auto}
.side .grp{padding:10px 14px 2px;font-size:10px;text-transform:uppercase;letter-spacing:.8px;color:var(--gold)}
.side a{display:flex;align-items:center;gap:9px;padding:9px 16px;color:#dfe4ee;font-size:13px;border-left:3px solid transparent}
.side a .ix{width:22px;height:22px;border-radius:5px;background:rgba(255,255,255,.08);display:flex;align-items:center;justify-content:center;font-size:11px;color:var(--gold);flex-shrink:0}
.side a:hover{background:var(--navy-2)}
.side a.active{background:var(--navy-2);border-left-color:var(--gold);color:#fff;font-weight:600}
.main{flex:1;min-width:0;padding:24px 26px;max-width:1200px}
.pt{font-family:Georgia,serif;font-size:24px;font-weight:700;margin:0 0 3px;color:var(--navy)}
.ps{color:var(--muted);font-size:13.5px;margin:0 0 18px;max-width:880px}
.lead{background:#fff;border:1px solid var(--rule);border-left:4px solid var(--blue);border-radius:8px;padding:12px 15px;margin-bottom:18px;font-size:13.5px}
.principle{background:#fbf4ef;border:1px solid #ecdcc9;border-left:4px solid var(--gold);border-radius:8px;padding:12px 15px;margin-bottom:18px;font-size:13.5px}
/* grid + cards */
.grid{display:grid;gap:16px}
.auto{grid-template-columns:repeat(auto-fit,minmax(190px,1fr))}
.c2{grid-template-columns:1fr 1fr}.c23{grid-template-columns:3fr 2fr}.c12{grid-template-columns:1fr 2fr}
@media(max-width:960px){.c2,.c23,.c12{grid-template-columns:1fr}}
.card{background:#fff;border:1px solid var(--rule);border-radius:10px;margin-bottom:16px}
.card>.hd{padding:13px 16px;border-bottom:1px solid var(--rule);font-family:Georgia,serif;font-weight:700;color:var(--navy);display:flex;align-items:center;gap:9px}
.card>.hd::before{content:"";width:8px;height:18px;border-radius:2px;background:var(--maroon)}
.card>.bd{padding:16px}
.kpi{background:#fff;border:1px solid var(--rule);border-top:3px solid var(--navy);border-radius:10px;padding:16px}
.kpi .n{font-family:Georgia,serif;font-size:27px;font-weight:700;color:var(--navy)}
.kpi .l{color:var(--muted);font-size:12px;margin-top:5px}
/* badges */
.bdg{display:inline-block;padding:3px 9px;border-radius:4px;font-size:11.5px;font-weight:700;white-space:nowrap;border:1px solid transparent}
.b-navy{background:#e7ebf2;color:var(--navy)}.b-maroon{background:#f6e6ec;color:var(--maroon)}
.b-gold{background:#f6efe0;color:#8a6d২e;color:#8a6a2e}.b-green{background:#e3f0ec;color:var(--green)}
.b-blue{background:#e7f0f8;color:var(--blue)}.b-gray{background:#eceef2;color:#4b5563}
.b-red{background:#fbe9e7;color:#bf372a}.b-amber{background:#fbf2da;color:#946610}
/* tables */
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--rule);border-radius:8px}
table.t{width:100%;border-collapse:collapse;font-size:13px;background:#fff}
table.t th,table.t td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--rule)}
table.t th{background:#f0f1f4;color:var(--navy);font-size:10.5px;text-transform:uppercase;letter-spacing:.5px;font-family:Arial}
table.t tr:last-child td{border-bottom:0}
table.t tr.row:hover{background:#f6f7f9;cursor:pointer}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px}
.muted{color:var(--muted)}.small{font-size:12.5px;color:var(--muted)}
.kv{display:grid;grid-template-columns:200px 1fr;gap:8px 16px;font-size:13.5px}
.kv .k{color:var(--muted)}
@media(max-width:620px){.kv{grid-template-columns:1fr;gap:2px}.kv .k{margin-top:7px;font-weight:600}}
/* buttons */
.btn{display:inline-block;background:var(--maroon);color:#fff;border:0;padding:10px 18px;border-radius:7px;font-size:13.5px;font-weight:700}
.btn:hover{background:var(--maroon-d)}
.btn.navy{background:var(--navy)}.btn.navy:hover{background:var(--navy-2)}
.btn.ghost{background:#fff;color:var(--maroon);border:1px solid var(--maroon)}
.btn.soft{background:#eceef2;color:var(--navy);border:1px solid var(--rule)}
.btn.sm{padding:6px 12px;font-size:12px}
/* fields */
.field{margin-bottom:11px}.field label{display:block;font-size:11.5px;color:var(--muted);font-weight:700;margin-bottom:4px}
.field input,.field select{width:100%;padding:8px 10px;border:1px solid var(--rule);border-radius:7px;background:#fff}
.frow{display:grid;grid-template-columns:1fr 1fr;gap:11px}
/* demo cards */
.demos{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.demo{border:1px solid var(--rule);border-left:4px solid var(--gold);border-radius:9px;background:#fff;padding:12px 13px;cursor:pointer;transition:.12s}
.demo:hover{border-left-color:var(--maroon);box-shadow:0 3px 10px rgba(27,42,65,.10);transform:translateY(-1px)}
.demo .dt{font-weight:700;color:var(--navy);font-size:13.5px}
.demo .dd{font-size:12px;color:var(--muted);margin-top:3px}
.demo .run{margin-top:9px;font-size:11.5px;color:var(--maroon);font-weight:700}
/* profile / passport */
.profile{border:1px solid var(--rule);border-radius:11px;overflow:hidden}
.profile .top{background:linear-gradient(135deg,var(--navy),#0f1c30);color:#fff;padding:15px 17px}
.profile .top .nm{font-family:Georgia,serif;font-weight:700;font-size:16px}
.profile .top .id{font-size:11px;color:#c7cedb}
.profile .r{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:10px 17px;border-bottom:1px solid var(--rule);font-size:13.5px}
.profile .r:last-child{border-bottom:0}.profile .r .k{color:var(--muted)}
.summary{background:#eef5f2;border:1px solid #cfe3db;border-left:4px solid var(--green);border-radius:8px;padding:12px 15px;font-size:13.5px;margin-top:14px}
.warn{background:#fbf2da;border:1px solid #ecdca8;border-left:4px solid var(--gold);border-radius:8px;padding:10px 14px;font-size:13px;margin:8px 0}
.svgwrap{background:#fff;border:1px solid var(--rule);border-radius:9px;padding:9px;overflow:auto}
.legend{font-size:11.5px;color:var(--muted);margin-top:8px}
.timeline{border-left:3px solid var(--rule);margin-left:13px;padding-left:20px}
.tstep{position:relative;margin-bottom:10px;background:#fff;border:1px solid var(--rule);border-radius:9px;padding:11px 13px}
.tstep.fire{border-color:var(--maroon)}
.tstep .bt{position:absolute;left:-33px;top:11px;width:26px;height:26px;border-radius:50%;background:#c4ccd6;color:#fff;font-size:10px;font-weight:700;display:flex;align-items:center;justify-content:center;border:3px solid var(--paper)}
.tstep.fire .bt{background:var(--maroon)} .tstep .nm{font-weight:700;font-size:13px;color:var(--navy)}
.flow{display:flex;flex-direction:column;gap:10px;align-items:center}
.fnode{width:100%;max-width:520px;border:1px solid var(--rule);border-top:4px solid var(--navy);border-radius:10px;background:#fff;padding:12px 14px;cursor:pointer}
.fnode:hover{border-color:var(--maroon)} .fnode .ft{font-weight:700;color:var(--navy)} .fnode .fd{font-size:12px;color:var(--muted)}
.farrow{color:var(--maroon);font-size:18px}
.steps{display:flex;flex-wrap:wrap;gap:6px}
.stagebar{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:8px}
@media(max-width:760px){.stagebar{grid-template-columns:1fr 1fr}}
.stage{border:1px solid var(--rule);border-radius:9px;background:#fff;padding:11px;border-top:4px solid var(--gold)}
.stage .sn{font-family:Georgia,serif;font-weight:700;color:var(--navy)}
.note{background:#fbfaf6;border:1px solid #ece4d2;border-radius:9px;padding:12px 14px;font-size:13px}
ul.tight{margin:6px 0;padding-left:20px}ul.tight li{margin:5px 0}
pre.code{background:#0f1c30;color:#d6e2ee;padding:12px;border-radius:8px;overflow:auto;font-size:12px;white-space:pre-wrap;word-break:break-word}
.gnode{display:inline-block;border:1.5px solid var(--rule);border-radius:8px;padding:6px 11px;margin:4px;background:#fff;font-size:12.5px}
.lvl{padding-left:20px;border-left:2px dashed var(--rule);margin-left:16px}
.gnode.gov{border-color:var(--blue)}.gnode.foreign{border-color:var(--gold)}.gnode.entity{border-color:var(--maroon)}.gnode.priv{border-color:var(--green)}
.foot{padding:22px 26px;color:var(--muted);font-size:12px;border-top:1px solid var(--rule);background:#fff}
.bar{height:9px;background:#eceef2;border-radius:6px;overflow:hidden}.bar>span{display:block;height:100%}
.barrow{display:grid;grid-template-columns:180px 1fr 44px;gap:11px;align-items:center;margin:8px 0;font-size:12.5px}
@media(max-width:620px){.barrow{grid-template-columns:120px 1fr 36px}}
.barrow .lbl{cursor:pointer} .barrow .lbl:hover{color:var(--maroon);text-decoration:underline}
/* header search */
.hsearch{position:relative}
.hsearch input{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.3);color:#fff;border-radius:7px;padding:7px 10px;width:230px;font-size:12.5px}
.hsearch input::placeholder{color:#c7cedb}
.hsearch .res{position:absolute;top:38px;left:0;right:0;background:#fff;border:1px solid var(--rule);border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,.2);max-height:300px;overflow:auto;z-index:90}
.hsearch .res div{padding:8px 11px;font-size:12.5px;color:var(--ink);cursor:pointer;border-bottom:1px solid var(--rule)}
.hsearch .res div:hover{background:var(--paper)}
.tourbtn{background:var(--gold);color:var(--navy);border:0;border-radius:7px;padding:7px 12px;font-weight:700;font-size:12.5px}
/* sliders */
.slider{width:100%}
input[type=range]{accent-color:var(--maroon)}
.simrow{display:grid;grid-template-columns:160px 1fr 70px;gap:10px;align-items:center;margin:9px 0;font-size:13px}
@media(max-width:620px){.simrow{grid-template-columns:110px 1fr 56px}}
.simrow .v{font-weight:700;color:var(--navy);text-align:right}
.flip{background:#eef5f2;border:1px solid #cfe3db;border-radius:8px;padding:10px 13px;margin-top:10px;font-size:13px}
/* compare */
.cmpgrid{display:grid;gap:0;border:1px solid var(--rule);border-radius:9px;overflow:hidden}
.cmpgrid>div{padding:9px 12px;border-bottom:1px solid var(--rule);font-size:13px}
/* modal / tour */
.modal{position:fixed;inset:0;background:rgba(15,28,48,.55);z-index:200;display:flex;align-items:center;justify-content:center;padding:18px}
.modal .box{background:#fff;border-radius:12px;max-width:560px;width:100%;box-shadow:0 20px 60px rgba(0,0,0,.35);overflow:hidden}
.modal .top{background:var(--navy);color:#fff;padding:14px 18px;font-family:Georgia,serif;font-weight:700;display:flex;align-items:center;gap:10px}
.modal .top .step{margin-left:auto;font-family:Arial;font-size:12px;color:#c7cedb;font-weight:400}
.modal .bd{padding:18px}
.modal .ft{padding:12px 18px;border-top:1px solid var(--rule);display:flex;gap:10px;justify-content:flex-end}
/* before/after */
.ba{display:grid;grid-template-columns:1fr 40px 1fr;gap:10px;align-items:center}
@media(max-width:620px){.ba{grid-template-columns:1fr}}
.ba .col{border:1px solid var(--rule);border-radius:9px;overflow:hidden}
.ba .col .h{padding:8px 12px;font-weight:700;color:#fff;font-size:12.5px}
.ba .col.before .h{background:#7a8597}.ba .col.after .h{background:var(--green)}
.ba .col .r{display:flex;justify-content:space-between;padding:7px 12px;border-bottom:1px solid var(--rule);font-size:12.5px}
.ba .col .r:last-child{border-bottom:0}.ba .arrow{text-align:center;color:var(--maroon);font-size:22px}
.chgd{background:#fff7e6}
@media print{
 .header,.banner,.side,.foot,#tour,.demo,.tourbtn,.hsearch{display:none!important}
 .main{padding:0;max-width:none} .card{break-inside:avoid;box-shadow:none}
 body{background:#fff}
}
@media(max-width:880px){
 .side{position:fixed;left:0;top:90px;bottom:0;z-index:40;transform:translateX(-100%);transition:.2s;box-shadow:0 0 30px rgba(0,0,0,.3)}
 .side.open{transform:translateX(0)} .menubtn{display:inline-block} .main{padding:16px}
 .demos{grid-template-columns:1fr 1fr} .header .ttl small{display:none} .hsearch input{width:130px}
}
</style>
</head>
<body>
<div class="header">
 <button class="menubtn" onclick="document.getElementById('side').classList.toggle('open')">☰</button>
 <div class="crest">Q</div>
 <div class="ttl">Qatar Enterprise Classification Platform<small>State of Qatar · National Planning Council · National Statistics Center</small></div>
 <span class="sp"></span>
 <div class="hsearch"><input id="gsearch" placeholder="Search any enterprise…" oninput="gsearch(this.value)" onfocus="gsearch(this.value)" autocomplete="off"/><div id="gsres"></div></div>
 <button class="tourbtn" onclick="tourStart()">★ Guided tour</button>
 <span class="bdg b-gold" style="background:rgba(201,169,97,.2);color:#f4e6c6;border-color:rgba(201,169,97,.5)">UAT</span>
</div>
<div class="banner">DEMONSTRATION PROTOTYPE — UAT ENVIRONMENT — not for public deployment.</div>
<div class="layout">
 <aside class="side" id="side"><nav id="nav"></nav></aside>
 <main class="main" id="content"></main>
</div>
<div class="foot" id="foot"></div>
<div id="tour"></div>
<script>
"use strict";
var DATA = /*__DATA__*/;

/* ===================== ENGINE — faithful port of the backend rules engine ===================== */
var CONTROL_PRIORITY=["MAJ-VOTE","GOLDEN","BOARD","KEY-PERS","CONTRACT","REGULATORY","FINANCING","DOMINANT","BO-CHAIN"];
function _num(v){var n=parseFloat(v);return isNaN(n)?null:n;}
function leaf(c,f){var op=c.op,a=f[c.field],v=c.value;
 if(op==="exists")return (c.field in f)&&f[c.field]!=null;
 if(op==="truthy")return !!a;
 if(op==="eq")return a===v;if(op==="ne")return a!==v;
 if(op==="in")return (v||[]).indexOf(a)>=0;
 if(op==="gt"||op==="gte"||op==="lt"||op==="lte"){var x=_num(a),y=_num(v);if(x==null||y==null)return false;return op==="gt"?x>y:op==="gte"?x>=y:op==="lt"?x<y:x<=y;}
 if(op==="between"){var x2=_num(a);if(x2==null)return false;var lo=_num((v||[])[0]),hi=_num((v||[])[1]);if(lo!=null&&x2<lo)return false;if(hi!=null&&x2>=hi)return false;return true;}
 return false;}
function evalCond(c,f){if(!c||!Object.keys(c).length)return true;
 if(c.all)return c.all.every(function(x){return evalCond(x,f);});
 if(c.any)return c.any.some(function(x){return evalCond(x,f);});
 if(c.not)return !evalCond(c.not,f);
 if(c.op)return leaf(c,f);return false;}
function resolveOut(spec,f){if(spec&&typeof spec==="object"){if("const" in spec)return spec.const;if("fact" in spec)return f[spec.fact];}return spec;}
function incoming(edges,node){return edges.filter(function(e){return e.owned_id===node;});}
function effShare(node,pred,useVoting,edges,seen){if(seen[node])return 0;var s=Object.assign({},seen);s[node]=1;var tot=0;
 incoming(edges,node).forEach(function(e){var pct=(useVoting?e.voting_pct:e.ownership_pct)||0;var fr=pct/100;
  if(pred(e))tot+=fr;else tot+=fr*effShare(e.owner_id,pred,useVoting,edges,s);});return Math.min(tot,1);}
function strongest(inds){for(var i=0;i<CONTROL_PRIORITY.length;i++){if(inds.indexOf(CONTROL_PRIORITY[i])>=0)return CONTROL_PRIORITY[i];}return null;}
function uci(node,edges,seen){seen=seen||{};if(seen[node])return null;var inc=incoming(edges,node);if(!inc.length)return null;
 var ult=inc.filter(function(e){return e.is_ultimate==="Y";})[0];
 var dom=ult||inc.reduce(function(a,b){return ((b.voting_pct||b.ownership_pct||0)>(a.voting_pct||a.ownership_pct||0))?b:a;});
 var ns=Object.assign({},seen);ns[node]=1;var p=uci(dom.owner_id,edges,ns);if(p)return p;
 return {uci_name:dom.owner_name||dom.owner_id,is_government:!!dom.owner_is_government,is_resident:dom.owner_is_resident!==false};}
function ownershipFacts(target,edges){
 var govOwn=100*effShare(target,function(e){return e.owner_is_government;},false,edges,{});
 var govVote=100*effShare(target,function(e){return e.owner_is_government;},true,edges,{});
 var forOwn=100*effShare(target,function(e){return e.owner_is_resident===false;},false,edges,{});
 var direct=incoming(edges,target);
 var allInds=direct.map(function(e){return e.control_indicator;}).filter(function(c){return c&&c!=="NONE";});
 var govInds=direct.filter(function(e){return e.owner_is_government;}).map(function(e){return e.control_indicator;}).filter(function(c){return c&&c!=="NONE";});
 var maxVote=direct.length?Math.max.apply(null,direct.map(function(e){return e.voting_pct||e.ownership_pct||0;})):0;
 var u=uci(target,edges,{});var govControl=govVote>50||govInds.length>0;var rep;
 if(govControl){rep=strongest(govInds)||(govVote>50?"MAJ-VOTE":"BO-CHAIN");}
 else if(maxVote>50){rep="MAJ-VOTE";}else if(allInds.length){rep=strongest(allInds)||"NONE";}
 else if(forOwn>50){rep="BO-CHAIN";}else{rep="NONE";}
 return {government_ownership_pct:Math.round(govOwn*100)/100,government_voting_pct:Math.round(govVote*100)/100,
  foreign_ownership_pct:Math.round(forOwn*100)/100,control_indicators:allInds,government_control:govControl,
  representative_control_flag:rep,uci_is_government:!!(u&&u.is_government),uci_is_foreign:!!(u&&u.is_resident===false),
  uci:u,max_direct_voting:maxVote};}
function buildFacts(inp,edges,target){
 var sales=inp.sales||0,costs=inp.production_costs||0,ratio=costs>0?sales/costs:null;
 var f={legal_form_code:inp.legal_form_code,residence:inp.residence,isic_class:inp.isic_class,
  employment:inp.employment||0,turnover_qar:inp.turnover_qar||0,sales:sales,production_costs:costs,
  sales_to_cost_ratio:ratio,sales_cover_pct:ratio!=null?ratio*100:null,is_nonprofit:!!inp.is_nonprofit,
  is_financial:!!inp.is_financial,has_premises:inp.has_premises!==false,has_employees:inp.has_employees!==false,
  has_autonomy:inp.has_autonomy!==false,jurisdiction:inp.jurisdiction};
 f.has_substance=!!(f.has_premises||f.has_employees||f.has_autonomy);
 var of=ownershipFacts(target,edges||[]);for(var k in of)f[k]=of[k];return f;}
var RESULT_FIELDS=["residence","isic_class","sector_code","market_status","control_flag","public_private","size_class","fdi_flag","special_entity_flag"];
function classify(facts){var result={},trace=[],confs=[];
 var tests=DATA.tests.slice().sort(function(a,b){return a.seq-b.seq;});
 tests.forEach(function(t){var rules=DATA.rules.filter(function(r){return r.test_code===t.test_code;}).sort(function(a,b){return a.priority-b.priority;});
  var fired=null;
  for(var i=0;i<rules.length;i++){var r=rules[i];if(evalCond(r.logic,facts)){fired=r;var applied={};
   Object.keys(r.output||{}).forEach(function(k){var val=resolveOut(r.output[k],facts);facts[k]=val;if(RESULT_FIELDS.indexOf(k)>=0)result[k]=val;applied[k]=val;});
   confs.push(r.confidence);trace.push({test_code:t.test_code,test_name:t.name,matched:true,rule_id:r.rule_id,rule_name:r.name,output:applied,standard_ref:r.standard_ref,rationale:r.rationale});break;}}
  if(!fired)trace.push({test_code:t.test_code,test_name:t.name,matched:false});});
 var conf=confs.length?confs.reduce(function(a,b){return a+b;},0)/confs.length:null;
 return {result:result,trace:trace,facts:facts,confidence:conf!=null?Math.round(conf*1000)/1000:null};}
function edgesOf(e){return (e.ownership.chain||[]).map(function(c){return {owner_id:c.owner_id,owner_name:c.owner_name,owned_id:c.owned_id,ownership_pct:c.ownership_pct,voting_pct:c.voting_pct,control_indicator:c.control_indicator,owner_is_government:c.is_government,owner_is_resident:c.is_resident,is_ultimate:"N"};});}
function classifyEnterprise(e){return classify(buildFacts(e.inp,edgesOf(e),e.id));}
function validateInput(inp){var o=[];
 if(!inp.legal_name_en)o.push(["ERROR","required","legal_name_en is required"]);
 if(["RES","NRES","MULTI"].indexOf(inp.residence)<0)o.push(["ERROR","VR-008","residence must be RES, NRES or MULTI"]);
 if(inp.isic_class&&DATA.isic_codes&&!DATA.isic_codes[inp.isic_class])o.push(["WARN","VR-002","ISIC class "+inp.isic_class+" not in codelist"]);
 if(!inp.employment&&!inp.turnover_qar)o.push(["INFO","VR-011","No employment and no turnover — possible dormant unit"]);
 return o;}

/* ===================== HELPERS ===================== */
function esc(s){return (s==null?"":String(s)).replace(/[&<>]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;"}[c];});}
function ent(id){for(var i=0;i<DATA.enterprises.length;i++)if(DATA.enterprises[i].id===id)return DATA.enterprises[i];return null;}
function money(v){if(!v)return "—";if(v>=1e9)return "QAR "+(v/1e9).toFixed(1)+"bn";if(v>=1e6)return "QAR "+(v/1e6).toFixed(1)+"m";if(v>=1e3)return "QAR "+(v/1e3).toFixed(0)+"k";return "QAR "+v.toLocaleString();}
var PP={"PUB-NFC":["b-blue","Public non-financial corporation"],"PUB-FC":["b-blue","Public financial corporation"],"GG":["b-navy","General government"],"PRV-NFC":["b-green","Private non-financial corporation"],"PRV-FC":["b-green","Private financial corporation"],"FCC":["b-gold","Foreign-controlled corporation"],"NPISH":["b-maroon","NPISH"]};
function pp(v){var m=PP[v]||["b-gray",v];return '<span class="bdg '+m[0]+'">'+esc(v)+'</span>';}
function ppName(v){return (PP[v]||["",v])[1];}
function bdg(v,c){return '<span class="bdg '+(c||"b-gray")+'">'+esc(v)+'</span>';}
function qcol(s){return s>=.85?"var(--green)":s>=.7?"#946610":"#bf372a";}
var PAL=["#1B2A41","#8A1538","#2C5F8A","#2E7D6B","#C9A961","#6f1029","#24364f","#5f6675"];
function bars(map){var e=Object.keys(map).map(function(k){return [k,map[k]];}).sort(function(a,b){return b[1]-a[1];});var mx=Math.max.apply(null,e.map(function(x){return x[1];}).concat([1]));
 return e.map(function(p,i){return '<div class="barrow"><div>'+esc(p[0])+'</div><div class="bar"><span style="width:'+(p[1]/mx*100)+'%;background:'+PAL[i%PAL.length]+'"></span></div><div style="text-align:right;font-weight:700">'+p[1]+'</div></div>';}).join("");}
function countBy(arr,k){var m={};arr.forEach(function(x){var v=x[k]||"—";m[v]=(m[v]||0)+1;});return m;}
function tbl(h,rows){return '<div class="tw"><table class="t"><tr>'+h.map(function(x){return "<th>"+esc(x)+"</th>";}).join("")+'</tr>'+rows.map(function(r){return "<tr>"+r.map(function(c){return "<td>"+c+"</td>";}).join("")+"</tr>";}).join("")+'</table></div>';}
function sevb(s){return bdg(s,{ERROR:"b-red",WARN:"b-amber",INFO:"b-blue"}[s]||"b-gray");}
function ownSVG(edges,target,name){
 var ch=edges||[];if(!ch.length)return '<p class="small">No ownership recorded (e.g. household enterprise).</p>';
 var nd={};nd[target]={id:target,label:name,kind:"entity",d:0};var oo={};ch.forEach(function(c){(oo[c.owned_id]=oo[c.owned_id]||[]).push(c);});
 var fr=[target],d=0,sn={};sn[target]=1;
 while(fr.length&&d<5){var nx=[];fr.forEach(function(id){(oo[id]||[]).forEach(function(c){if(!nd[c.owner_id])nd[c.owner_id]={id:c.owner_id,label:c.owner_name||c.owner_id,kind:c.owner_is_government?"gov":(c.owner_is_resident===false?"foreign":"priv"),d:d+1};if(!sn[c.owner_id]){sn[c.owner_id]=1;nx.push(c.owner_id);}});});fr=nx;d++;}
 var mx=Math.max.apply(null,Object.keys(nd).map(function(k){return nd[k].d;}));var ly={};Object.keys(nd).forEach(function(k){(ly[nd[k].d]=ly[nd[k].d]||[]).push(nd[k]);});
 var W=520,rh=88,bw=150,bh=42,H=(mx+1)*rh+16,ps={};
 for(var i=0;i<=mx;i++){var ar=ly[i]||[],g=W/(ar.length+1);ar.forEach(function(n,j){ps[n.id]=[g*(j+1),H-i*rh-rh/2];});}
 var ln="";ch.forEach(function(c){var a=ps[c.owner_id],b=ps[c.owned_id];if(!a||!b)return;var t=c.ownership_pct+"%"+(c.control_indicator?(" · "+c.control_indicator):"");ln+='<line x1="'+a[0]+'" y1="'+(a[1]+bh/2)+'" x2="'+b[0]+'" y2="'+(b[1]-bh/2)+'" stroke="#aab4c0" stroke-width="1.4" marker-end="url(#ar)"/><text x="'+((a[0]+b[0])/2+4)+'" y="'+((a[1]+b[1])/2)+'" font-size="10" fill="#5f6675">'+esc(t)+'</text>';});
 var cl={entity:"#8A1538",gov:"#2C5F8A",foreign:"#C9A961",priv:"#2E7D6B"};var bx="";
 Object.keys(nd).forEach(function(k){var n=nd[k],p=ps[n.id];var lab=n.kind==="entity"?"THIS ENTITY":n.kind.toUpperCase();bx+='<rect x="'+(p[0]-bw/2)+'" y="'+(p[1]-bh/2)+'" width="'+bw+'" height="'+bh+'" rx="7" fill="#fff" stroke="'+cl[n.kind]+'" stroke-width="2"/><text x="'+p[0]+'" y="'+(p[1]-2)+'" font-size="10" text-anchor="middle" fill="#222633">'+esc((n.label||"").slice(0,22))+'</text><text x="'+p[0]+'" y="'+(p[1]+12)+'" font-size="8" text-anchor="middle" fill="'+cl[n.kind]+'">'+lab+'</text>';});
 return '<svg viewBox="0 0 '+W+' '+H+'" width="100%" style="max-height:330px"><defs><marker id="ar" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#aab4c0"/></marker></defs>'+ln+bx+'</svg><div class="legend">■ <span style="color:#8A1538">entity</span> · ■ <span style="color:#2C5F8A">government</span> · ■ <span style="color:#2E7D6B">resident private</span> · ■ <span style="color:#C9A961">non-resident</span></div>';}
function entityType(r,inp){if(r.special_entity_flag==="HOLDING")return "Holding company";if(r.special_entity_flag==="SPV")return "Special-purpose vehicle";if(r.special_entity_flag==="CONSOLIDATE-PARENT")return "Empty-shell entity (consolidated with parent)";if(inp.legal_form_code==="GOV")return "Government body";if(inp.legal_form_code==="SP")return "Household enterprise / sole proprietor";if(inp.legal_form_code==="BR")return "Branch of foreign enterprise";if(inp.legal_form_code==="FND"&&r.public_private==="NPISH")return "Non-profit institution (NPISH)";return "Enterprise (institutional unit)";}
function ownCat(f){if(f.government_control)return "Government-controlled"+(f.government_voting_pct>50?" (majority "+f.government_voting_pct+"%)":" ("+(f.representative_control_flag)+")");if(f.foreign_ownership_pct>50||f.uci_is_foreign)return "Foreign-controlled ("+f.foreign_ownership_pct+"%)";if(f.max_direct_voting>50)return "Privately controlled (majority)";return "Privately controlled / dispersed";}

/* ===================== STATE / NAV ===================== */
var DEF=ent(DATA.demo&&DATA.demo[0]?DATA.demo[0][0]:DATA.enterprises[0].id)||DATA.enterprises[0];
var state={view:"engine",entId:DATA.enterprises[0].id,isicQ:"",regQ:"",eng:engFrom(DEF),sectorPick:null,ruleStd:null,
 animate:false,lastRun:null,
 sim:{base:"QA-ENT-20260000002",gov:51,foreign:0,ctrl:"MAJ-VOTE",sales:22000,costs:12000,employment:5200,isFin:true},
 cmp:["QA-ENT-20260000012","QA-ENT-20260000002","QA-ENT-20260000022"],
 lcId:"QA-ENT-20260000013",lcEvent:"IPO_MINORITY",
 tourStep:-1};
function engFrom(e){var lab=DATA.labels&&DATA.labels[e.id];return {inp:Object.assign({legal_name_en:e.name},e.inp),edges:edgesOf(e),name:e.name,trade:lab?lab.trade_name:e.name,label_note:lab?lab.note:null,license:lab?lab.license_label:null,_id:e.id,_ran:false};}
var NAV=[
 ["Classify",[["engine","Classification Engine"],["register","Enterprise Register"],["dashboard","Intelligence Dashboard"]]],
 ["Advanced interaction",[["simulate","What-if Simulator"],["lifecycle","Reclassification & Events"],["compare","Compare Entities"]]],
 ["Reference",[["isic","ISIC / Activity Master"],["sector","Institutional Sector"],["ownership","Ownership & Control"],["legal","Legal Form & Registration"]]],
 ["Data & Standards",[["integration","Data Integration"],["sources","Source Tiers & Conflicts"],["standards","Standards Catalogue"],["methodology","Methodology"]]],
 ["Governance",[["governance","Governance"],["about","About"]]]
];
var TITLES={engine:"Enterprise Classification Engine",register:"Enterprise Register",dashboard:"Enterprise Intelligence Dashboard",simulate:"What-if Simulator",lifecycle:"Reclassification & Lifecycle Events",compare:"Compare Entities",isic:"ISIC / Activity Master",sector:"Institutional Sector Classification",ownership:"Ownership & Control Module",legal:"Legal Form & Registration Module",integration:"Data Integration",sources:"Source Tiers & Conflict Resolution",standards:"Standards Catalogue",methodology:"Methodology",governance:"Governance",about:"About"};
function go(v,x){state.view=v;if(x)for(var k in x)state[k]=x[k];window.scrollTo(0,0);if(window.innerWidth<=880)document.getElementById('side').classList.remove('open');render();}

/* ===================== VIEW: ENGINE ===================== */
function vEngine(){
 var demos=(DATA.demo||[]).map(function(d){return '<div class="demo" onclick="loadDemo(\''+d[0]+'\')"><div class="dt">'+esc(d[1])+'</div><div class="dd">'+esc(d[2])+'</div><div class="run">▶ Auto-fill &amp; classify</div></div>';}).join("");
 var e=state.eng,inp=e.inp;
 var chooser=DATA.enterprises.map(function(x){return '<option value="'+x.id+'" '+(e._id===x.id?"selected":"")+'>'+esc(x.name)+'  ['+esc(x.sector)+' · '+esc(x.public_private)+']</option>';}).join("");
 var lf=DATA.legal_forms.map(function(x){return x.code;});
 var isicOpts=DATA.isic_list.map(function(x){return '<option value="'+x.code+'" '+(inp.isic_class===x.code?"selected":"")+'>'+x.code+' — '+esc(x.activity)+'</option>';}).join("");
 var fsel=function(id,label,opts,sel){return '<div class="field"><label>'+label+'</label><select onchange="state.eng.inp.'+id+'=this.value">'+opts.map(function(o){return '<option '+(String(sel)===String(o)?"selected":"")+'>'+o+'</option>';}).join("")+'</select></div>';};
 var fin=function(id,label,val,type){return '<div class="field"><label>'+label+'</label><input type="'+(type||"text")+'" value="'+esc(val)+'" oninput="state.eng.inp.'+id+'=this.'+(type==="number"?"valueAsNumber":"value")+'"/></div>';};
 var chk=function(id,label){return '<label class="small" style="display:inline-flex;gap:6px;align-items:center;margin-right:14px"><input type="checkbox" '+(inp[id]?"checked":"")+' onchange="state.eng.inp.'+id+'=this.checked"/> '+label+'</label>';};
 var edrows=e.edges.map(function(x,i){return '<tr><td><input value="'+esc(x.owner_name||"")+'" oninput="state.eng.edges['+i+'].owner_name=this.value;state.eng.edges['+i+'].owner_id=this.value" style="border:1px solid var(--rule);border-radius:6px;padding:5px;width:150px"/></td>'+
  '<td><input type="number" value="'+(x.ownership_pct||0)+'" oninput="state.eng.edges['+i+'].ownership_pct=this.valueAsNumber;state.eng.edges['+i+'].voting_pct=this.valueAsNumber" style="border:1px solid var(--rule);border-radius:6px;padding:5px;width:62px"/></td>'+
  '<td><label class="small"><input type="checkbox" '+(x.owner_is_government?"checked":"")+' onchange="state.eng.edges['+i+'].owner_is_government=this.checked"/> gov</label></td>'+
  '<td><label class="small"><input type="checkbox" '+(x.owner_is_resident!==false?"checked":"")+' onchange="state.eng.edges['+i+'].owner_is_resident=this.checked"/> resident</label></td>'+
  '<td><select onchange="state.eng.edges['+i+'].control_indicator=this.value" style="border:1px solid var(--rule);border-radius:6px;padding:5px">'+["","MAJ-VOTE","GOLDEN","BOARD","CONTRACT","REGULATORY","BO-CHAIN"].map(function(o){return '<option '+(x.control_indicator===o?"selected":"")+'>'+o+'</option>';}).join("")+'</select></td>'+
  '<td><button class="btn sm soft" onclick="state.eng.edges.splice('+i+',1);render()">✕</button></td></tr>';}).join("");
 var labelBox=e.label_note?'<div class="warn"><b>Label vs activity:</b> '+esc(e.label_note)+'</div>':'';
 return '<div class="principle"><b>Classify by reality, not by label.</b> Choose a case below (or edit the inputs), then press <b>Run classification</b> — the engine assembles the full profile from the entity\'s activity, ownership, control, legal form, residency and operations.</div>'+
  '<div class="card"><div class="hd">1 · Choose a case &nbsp;<span class="small" style="font-weight:400">— scroll, pick, and it classifies</span></div><div class="bd">'+
  '<div class="field"><label>Pick any registered enterprise (74) — loads &amp; classifies instantly</label><select onchange="loadDemo(this.value)" style="max-width:520px">'+chooser+'</select></div>'+
  '<div class="small" style="margin:6px 0 8px;font-weight:700;color:var(--navy)">…or pick a featured demonstration case:</div><div class="demos">'+demos+'</div></div></div>'+
  '<div class="card"><div class="hd">2 · Enterprise inputs <span class="small" style="font-weight:400">— edit anything, then run</span></div><div class="bd">'+
  fin("legal_name_en","Legal name (as registered)",inp.legal_name_en)+
  (e.license?'<div class="field"><label>License / trade label (what it is called)</label><input value="'+esc(e.license)+'" disabled style="background:#f6f7f9"/></div>':'')+
  '<div class="frow">'+fsel("legal_form_code","Legal form",lf,inp.legal_form_code)+'<div class="field"><label>Economic activity (ISIC Rev.4 — by value added)</label><select onchange="state.eng.inp.isic_class=this.value">'+isicOpts+'</select></div></div>'+
  '<div class="frow">'+fsel("residence","Residence",["RES","NRES","MULTI"],inp.residence)+fsel("jurisdiction","Jurisdiction",["MAINLAND","QFC","QFZA","QSTP"],inp.jurisdiction)+'</div>'+
  '<div class="frow">'+fin("employment","Employment (FTE)",inp.employment,"number")+fin("turnover_qar","Turnover (QAR)",inp.turnover_qar,"number")+'</div>'+
  '<div class="frow">'+fin("sales","Sales (QAR)",inp.sales,"number")+fin("production_costs","Production costs (QAR)",inp.production_costs,"number")+'</div>'+
  '<div class="field"><label>Operational flags</label>'+chk("is_financial","financial")+chk("is_nonprofit","non-profit")+chk("has_premises","premises")+chk("has_employees","employees")+chk("has_autonomy","autonomy")+'</div>'+
  '<div style="font-weight:700;color:var(--navy);margin:8px 0 6px;font-family:Georgia,serif">Ownership &amp; control</div>'+
  tbl(["Owner","Equity %","Gov?","Resident?","Control",""],[]).replace("</table>",edrows+"</table>")+
  '<button class="btn sm soft" style="margin-top:9px" onclick="state.eng.edges.push({owner_id:\'New owner\',owner_name:\'New owner\',owned_id:\'ENG\',ownership_pct:0,voting_pct:0,control_indicator:\'\',owner_is_government:false,owner_is_resident:true,is_ultimate:\'Y\'});render()">+ Add owner</button>'+
  '<div style="margin-top:16px;display:flex;gap:14px;align-items:center;flex-wrap:wrap"><button class="btn" style="font-size:15px;padding:12px 24px" onclick="runEngine()">▶ Run classification</button>'+
  '<label class="small" style="display:inline-flex;gap:6px;align-items:center"><input type="checkbox" '+(state.animate?"checked":"")+' onchange="state.animate=this.checked"/> Animate the 18 tests</label>'+
  '<span class="small">— result appears below and the page scrolls to it</span></div>'+
  '</div></div>'+
  '<div class="card"><div class="hd">3 · Assembled classification profile</div><div class="bd" id="engresult">'+labelBox+'<div class="note">Choose a case above or press <b>Run classification</b> — the full profile, confidence, source traceability, validation flags, rule trace and audit log appear here.</div></div></div>';
}
function loadDemo(id){var e=ent(id);if(!e)return;state.eng=engFrom(e);state.view="engine";render();setTimeout(function(){runEngine();},30);}
function runEngine(){
 var el=document.getElementById("engresult");
 try{
 var e=state.eng,inp=Object.assign({},e.inp);
 var edges=e.edges.map(function(x){return Object.assign({},x,{owned_id:"ENG",owner_id:x.owner_id||x.owner_name,is_ultimate:"Y"});});
 var f=buildFacts(inp,edges,"ENG");var oc=classify(f);var r=oc.result;
 var v=validateInput(inp);
 state.lastRun={name:inp.legal_name_en,inputs:inp,ownership:edges,result:r,confidence:oc.confidence,classified_at:new Date().toISOString(),methodology_version:"1.0.0"};
 var src={isic_class:"GTA activity / NSO profiling",legal_form_code:"MoCI Commercial Register",residence:"NSO (BPM6 centre of interest)",sector_code:"NSO — SNA 2025",public_private:"NSO — GFS 2014",control_flag:"NSO profiling / QFMA ownership",size_class:"GTA turnover + MoL employment",fdi_flag:"NSO — OECD BD4",special_entity_flag:"NSO substance test"};
 var rows=[["Entity type",esc(entityType(r,inp)),"NSO (Test 1–2)"],
  ["Economic activity (ISIC Rev.4)",esc(r.isic_class)+" — "+esc((DATA.isic_list.filter(function(x){return x.code===r.isic_class;})[0]||{}).activity||""),src.isic_class],
  ["Institutional sector",'<b>'+esc(r.sector_code)+'</b> — '+esc((DATA.sectors.filter(function(s){return s.code===r.sector_code;})[0]||{}).name||""),src.sector_code],
  ["Public / private",pp(r.public_private)+" "+esc(ppName(r.public_private)),src.public_private],
  ["Ownership / control",esc(ownCat(f)),src.control_flag],
  ["Effective control mechanism",bdg(r.control_flag),src.control_flag],
  ["Legal form",esc(inp.legal_form_code)+" — "+esc((DATA.legal_forms.filter(function(x){return x.code===inp.legal_form_code;})[0]||{}).name||""),src.legal_form_code],
  ["Market vs non-market",r.market_status==="MARKET"?bdg("MARKET","b-green"):bdg("NON-MARKET","b-amber"),"NSO — 50% rule"],
  ["Enterprise size",bdg(r.size_class,"b-navy"),src.size_class],
  ["Residency",bdg(r.residence,"b-navy"),src.residence],
  ["FDI relevance",r.fdi_flag==="NONE"?"—":bdg(r.fdi_flag,"b-gold"),src.fdi_flag],
  ["Special entity",r.special_entity_flag==="NONE"?"—":bdg(r.special_entity_flag,"b-maroon"),src.special_entity_flag],
  ["Register status",bdg("Classified — draft (pending peer review)","b-gray"),"CSBR"]];
 var profile='<div class="profile"><div class="top"><div class="nm">'+esc(inp.legal_name_en)+'</div><div class="id">'+(e.license?"License label: "+esc(e.license)+" · ":"")+'classified live · confidence '+oc.confidence+'</div></div>'+
  rows.map(function(p){return '<div class="r"><span class="k">'+p[0]+'</span><span style="text-align:right">'+p[1]+'</span></div>';}).join("")+'</div>';
 var warns=[];
 if(e.label_note)warns.push('<div class="warn"><b>Substance over form:</b> '+esc(e.label_note)+'</div>');
 if(f.government_ownership_pct>=20&&["PRV-NFC","PRV-FC","FCC"].indexOf(r.public_private)>=0)warns.push('<div class="warn">Effective government ownership '+f.government_ownership_pct+'% but classified '+r.public_private+' — flagged for review (hidden government ownership).</div>');
 v.forEach(function(x){warns.push('<div class="warn">'+sevb(x[0])+' <b>'+esc(x[1])+'</b> '+esc(x[2])+'</div>');});
 var sources=tbl(["Dimension","Result","Authoritative source"],rows.map(function(p){return [p[0],p[1],p[2]];}));
 var traceRows=oc.trace.filter(function(t){return t.matched;}).map(function(t){return '<tr><td>'+esc(t.test_code)+'</td><td class="mono">'+esc(t.rule_id)+'</td><td>'+Object.keys(t.output).map(function(k){return bdg(t.output[k],"b-green");}).join(" ")+'</td><td class="small">'+esc(t.standard_ref||"")+'</td></tr>';}).join("");
 var summary='<div class="summary"><b>Final classification:</b> '+esc(inp.legal_name_en)+' is a <b>'+esc(entityType(r,inp))+'</b>, institutional sector <b>'+esc(r.sector_code)+'</b> ('+esc(ppName(r.public_private))+'), '+esc((r.market_status||"").toLowerCase())+' producer, '+esc(ownCat(f).toLowerCase())+', size <b>'+esc(r.size_class)+'</b>, '+esc(r.residence==="RES"?"resident":r.residence)+(r.fdi_flag!=="NONE"?", FDI: "+esc(r.fdi_flag):"")+'. Confidence '+oc.confidence+'.</div>';
 var nowiso=new Date().toISOString().slice(0,16).replace("T"," ");
 var audit=tbl(["When","Action","Detail","By"],[[nowiso,"CAPTURE","Inputs received via classification portal","portal"],[nowiso,"VALIDATE",(v.length?v.length+" finding(s)":"all checks passed"),"engine"],[nowiso,"CLASSIFY","18-test pipeline · confidence "+oc.confidence,"engine"],[nowiso,"PENDING","Awaiting peer review (Layer 2)","workflow"]]);
 var exportbar='<div style="display:flex;gap:8px;justify-content:flex-end;margin-bottom:10px"><button class="btn soft sm" onclick="printProfile()">🖨 Print / Save PDF</button><button class="btn soft sm" onclick="exportJSON()">⬇ Download JSON</button></div>';
 var traceCard=state.animate
  ? '<div class="card"><div class="hd">How the answer was reached — live 18-test pipeline</div><div class="bd"><div class="timeline" id="engtl"></div></div></div>'
  : '<div class="card"><div class="hd">How the answer was reached — rules applied</div><div class="bd">'+tbl(["Test","Rule","Output","Standard"],[]).replace("</table>",traceRows+"</table>")+'</div></div>';
 el.innerHTML=exportbar+profile+summary+
  (warns.length?'<div class="card" style="margin-top:14px"><div class="hd">Validation flags &amp; warnings</div><div class="bd">'+warns.join("")+'</div></div>':'<div class="card" style="margin-top:14px"><div class="bd small" style="color:var(--green)">No validation flags — record passes all checks.</div></div>')+
  '<div class="card"><div class="hd">Ownership network</div><div class="bd"><div class="svgwrap">'+ownSVG(edges,"ENG",inp.legal_name_en)+'</div></div></div>'+
  '<div class="card"><div class="hd">Source traceability</div><div class="bd">'+sources+'</div></div>'+
  traceCard+
  '<div class="card"><div class="hd">Audit log</div><div class="bd">'+audit+'</div></div>';
  if(state.animate){var tl=document.getElementById("engtl");var i=0;(function tick(){if(!tl||i>=oc.trace.length)return;var s=oc.trace[i];var d=document.createElement("div");d.className="tstep"+(s.matched?" fire":"");var out=s.matched?Object.keys(s.output).map(function(k){return bdg(s.output[k],"b-green");}).join(" "):'<span class="small">governance / process step</span>';d.innerHTML='<div class="bt">'+esc(s.test_code)+'</div><div class="nm">'+esc(s.test_name)+'</div><div style="margin-top:3px">'+out+'</div>'+(s.matched?'<div class="small" style="margin-top:2px">'+esc(s.rule_id)+' · '+esc(s.standard_ref||"")+'</div>':'');tl.appendChild(d);d.scrollIntoView({block:"nearest"});i++;setTimeout(tick,160);})();}
  if(el&&el.scrollIntoView)el.scrollIntoView({behavior:"smooth",block:"start"});
 }catch(err){if(el)el.innerHTML='<div class="warn"><b>Could not classify.</b> '+esc(err&&err.message)+'</div>';}
}
function printProfile(){try{window.print();}catch(e){}}
function exportJSON(){try{if(!state.lastRun)return;var blob="data:application/json;charset=utf-8,"+encodeURIComponent(JSON.stringify(state.lastRun,null,2));var a=document.createElement("a");a.href=blob;a.download=(state.lastRun.name||"classification").replace(/[^a-z0-9]+/gi,"_")+"_classification.json";document.body.appendChild(a);a.click();a.remove();}catch(e){}}

/* ===================== VIEW: REGISTER ===================== */
function vRegister(){
 var q=(state.regQ||"").toLowerCase();
 var rows=DATA.enterprises.filter(function(e){return !q||(e.name+e.id+e.sector+e.public_private+e.legal_form).toLowerCase().indexOf(q)>=0;});
 return '<div class="card"><div class="bd"><input placeholder="Search name, ID, sector, legal form…" value="'+esc(state.regQ)+'" oninput="state.regQ=this.value;render()" style="width:100%;max-width:400px;padding:9px 12px;border:1px solid var(--rule);border-radius:7px;margin-bottom:14px"/>'+
  '<p class="small" style="margin:0 0 10px">'+rows.length+' classified records. Click any row to open it in the engine and re-run the live classification.</p>'+
  tbl(["Enterprise","Legal form","Sector","Public/Private","Size","Control","Confidence"],rows.map(function(e){return ['<b>'+esc(e.name)+'</b><div class="small mono">'+esc(e.id)+'</div>',esc(e.legal_form),esc(e.sector),pp(e.public_private),esc(e.size),bdg(e.control),'<span style="color:'+qcol(e.confidence||1)+';font-weight:700">'+(e.confidence||1)+'</span>'];}),true).replace(/<tr>(?!.*<th>)/g,"")+'</div></div>';
}
/* register rows clickable: rebuild with onclick */
function vRegister2(){
 var q=(state.regQ||"").toLowerCase();
 var pps=["all"].concat(Object.keys(PP));
 var secs=["all"].concat(Object.keys(countBy(DATA.enterprises,"sector")).sort());
 var sizes=["all","MICRO","SMALL","MEDIUM","LARGE"];
 var list=DATA.enterprises.filter(function(e){
  if(q&&(e.name+e.id+e.sector+e.public_private+e.legal_form).toLowerCase().indexOf(q)<0)return false;
  if(state.regPP&&state.regPP!=="all"&&e.public_private!==state.regPP)return false;
  if(state.regSec&&state.regSec!=="all"&&e.sector!==state.regSec)return false;
  if(state.regSize&&state.regSize!=="all"&&e.size!==state.regSize)return false;
  return true;});
 var body=list.map(function(e){return '<tr class="row" onclick="loadDemo(\''+e.id+'\')"><td><b>'+esc(e.name)+'</b><div class="small mono">'+esc(e.id)+'</div></td><td>'+esc(e.legal_form)+'</td><td>'+esc(e.sector)+'</td><td>'+pp(e.public_private)+'</td><td>'+esc(e.size)+'</td><td>'+bdg(e.control)+'</td><td><span style="color:'+qcol(e.confidence||1)+';font-weight:700">'+(e.confidence||1)+'</span></td></tr>';}).join("");
 var chips=pps.map(function(p){return '<button class="btn sm '+((state.regPP||"all")===p?"":"soft")+'" onclick="state.regPP=\''+p+'\';render()">'+(p==="all"?"All":esc(p))+'</button>';}).join(" ");
 var ssel=function(id,opts,cur){return '<select onchange="state.'+id+'=this.value;render()" style="padding:8px 10px;border:1px solid var(--rule);border-radius:7px">'+opts.map(function(o){return '<option '+((cur||"all")===o?"selected":"")+'>'+o+'</option>';}).join("")+'</select>';};
 return '<div class="lead">The Central Statistical Business Register. Search and filter, then click any row to open it in the engine and re-run the live classification.</div>'+
  '<div class="card"><div class="bd">'+
  '<div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:12px">'+
  '<input placeholder="Search name, ID, sector, legal form…" value="'+esc(state.regQ)+'" oninput="state.regQ=this.value;render()" style="flex:1;min-width:220px;padding:9px 12px;border:1px solid var(--rule);border-radius:7px"/>'+
  '<label class="small">Sector '+ssel("regSec",secs,state.regSec)+'</label>'+
  '<label class="small">Size '+ssel("regSize",sizes,state.regSize)+'</label></div>'+
  '<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px">'+chips+'</div>'+
  '<p class="small" style="margin:0 0 10px">'+list.length+' of '+DATA.enterprises.length+' records.</p>'+
  '<div class="tw"><table class="t"><tr><th>Enterprise</th><th>Legal form</th><th>Sector</th><th>Public/Private</th><th>Size</th><th>Control</th><th>Confidence</th></tr>'+body+'</table></div></div></div>';
}

/* ===================== VIEW: ISIC MASTER ===================== */
function vIsic(){
 var q=(state.isicQ||"").toLowerCase();
 var secs=["all"].concat(Object.keys(countBy(DATA.isic_list,"section")).sort());
 var list=DATA.isic_list.filter(function(x){return (!q||(x.code+x.activity+x.section).toLowerCase().indexOf(q)>=0)&&(!state.isicSec||state.isicSec==="all"||x.section===state.isicSec);});
 var ssel='<select onchange="state.isicSec=this.value;render()" style="padding:9px 10px;border:1px solid var(--rule);border-radius:7px">'+secs.map(function(o){return '<option '+((state.isicSec||"all")===o?"selected":"")+'>'+o+'</option>';}).join("")+'</select>';
 return '<div class="lead">ISIC Rev.4 is the activity classification. The principal activity is the one generating the largest <b>value added</b> — not revenue, not the license label. Cross-walks to NACE and the GCC-SIC are shown.</div>'+
  '<div class="card"><div class="bd"><div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:14px"><input placeholder="Search ISIC code or activity…" value="'+esc(state.isicQ)+'" oninput="state.isicQ=this.value;render()" style="flex:1;min-width:220px;padding:9px 12px;border:1px solid var(--rule);border-radius:7px"/><label class="small">Section '+ssel+'</label></div>'+
  tbl(["ISIC class","Activity","Section","NACE","GCC-SIC"],list.map(function(x){return ['<span class="mono">'+esc(x.code)+'</span>',esc(x.activity),esc(x.section),esc(x.nace||""),esc(x.gcc||"")];}))+
  '<p class="small" style="margin-top:10px">'+list.length+' classes shown (catalogue covers the 21 ISIC sections and the classes most relevant to Qatar). A national activity classification beyond ISIC + the GCC-SIC cross-walk is not provided in the source files.</p></div></div>';
}

/* ===================== VIEW: SECTOR ===================== */
function vSector(){
 var rows=DATA.sectors.map(function(s){return ['<span class="mono">'+esc(s.code)+'</span>',esc(s.name),esc(s.parent||"—"),esc(s.definition||"")];});
 return '<div class="lead">Every institutional unit is assigned to exactly one resident sector (S.11–S.15) or the Rest of the World (S.2). Financial corporations break down into S.121–S.129; general government into S.1311–S.1314. Sector is independent of ownership — a government-owned bank is still S.12; the public/private split is a separate flag.</div>'+
  '<div class="card"><div class="hd">Institutional sector codelist (SNA 2008 / 2025)</div><div class="bd">'+tbl(["Code","Sector / sub-sector","Parent","Definition"],rows)+'</div></div>'+
  '<div class="card"><div class="hd">Decision flow</div><div class="bd"><div class="flow">'+
  ['Government body (ministry/authority)? → <b>S.13</b>','Financial intermediary/auxiliary? → <b>S.12</b> (S.121–S.129 by activity)','Non-profit, non-market, not government-controlled? → <b>S.15</b> (NPISH)','Government-controlled non-market unit? → <b>S.13</b>','Unincorporated household enterprise? → <b>S.14</b>','Otherwise market producer → <b>S.11</b>'].map(function(t,i){return (i?'<div class="farrow">▼</div>':'')+'<div class="fnode"><div class="ft">'+t+'</div></div>';}).join("")+
  '</div></div></div>';
}

/* ===================== VIEW: OWNERSHIP ===================== */
function vOwnership(){
 var ind=(DATA.codelists.control_indicator||[]).map(function(c){return [bdg(c.code),esc(c.meaning)];});
 var thr=[["< 10%","Portfolio investment — no FDI relationship; no control"],["10 – 50%","Associate / significant influence — FDI relationship; not consolidated"],["> 50% voting","Subsidiary — majority control; consolidated; classified by control test"],["Any % + control indicator","Effective control by substance — e.g. golden share, board rights, dominant financing (can be public with a minority or zero stake)"]];
 var pub=(DATA.codelists.public_private||[]).map(function(c){return [bdg(c.code,(PP[c.code]||["b-gray"])[0]),esc(c.meaning)];});
 return '<div class="principle"><b>Substance over form.</b> Control is not the same as ownership. An entity can be controlled with a minority stake — or none — through a golden share, board-appointment rights, dominant financing, or a beneficial-ownership chain. State stakes spread across several vehicles are <b>aggregated</b>.</div>'+
  '<div class="grid c2"><div class="card"><div class="hd">Nine indicators of effective control (Test 8)</div><div class="bd">'+tbl(["Code","Indicator"],ind)+'</div></div>'+
  '<div class="card"><div class="hd">FDI / ownership thresholds (OECD BD4)</div><div class="bd">'+tbl(["Threshold","Treatment"],thr)+'</div></div></div>'+
  '<div class="card"><div class="hd">Public / private / mixed / foreign categories</div><div class="bd">'+tbl(["Code","Meaning"],pub)+'</div></div>'+
  '<div class="card"><div class="hd">Worked example — government control without majority</div><div class="bd"><div class="svgwrap">'+ownSVG(edgesOf(ent("QA-ENT-20260000024")),"QA-ENT-20260000024","PPP infrastructure SPV")+'</div><p class="small">49% government + golden share → public corporation. <a onclick="loadDemo(\'QA-ENT-20260000024\')">Run this case in the engine →</a></p></div></div>';
}

/* ===================== VIEW: LEGAL FORM ===================== */
function vLegal(){
 var rows=DATA.legal_forms.map(function(x){return ['<span class="mono">'+esc(x.code)+'</span>',esc(x.name),esc(x.notes||"")];});
 return '<div class="lead">Legal form and the registration source are <b>inputs</b> to classification — they never determine the sector by themselves. A commercial-register label, license title or trade name is corroborating evidence only; the assessed activity, ownership and control decide the outcome.</div>'+
  '<div class="card"><div class="hd">Qatar legal forms (codelist 07)</div><div class="bd">'+tbl(["Code","Legal form","Notes / classification implication"],rows)+'</div></div>'+
  '<div class="card"><div class="hd">How registration sources feed classification</div><div class="bd">'+tbl(["Source","Provides","Used for"],[
   ["MoCI Commercial Register","Legal name, legal form, CR number, ownership at incorporation","Legal-unit identity; legal form input"],
   ["Licensing authorities (sector regulators, municipalities)","License title, permitted activities","Corroborating activity evidence (not determinative)"],
   ["QFC / QFZA / QSTP registries","Jurisdiction, foreign-parent status","Residence flag; jurisdiction flag; FDI flag"],
   ["GTA","Declared activity, turnover, employment","Activity (value-added) and size"],
   ["NSO profiling","Ownership chain, control, group","Effective control; sector; group"]])+
   '<div class="warn" style="margin-top:12px"><b>Label-contradiction example:</b> <a onclick="loadDemo(\'QA-ENT-20260000080\')">run the "Foodstuff &amp; General Trading" case →</a> — licensed as trading, but the assessed principal activity is a holding company (ISIC 6420). The engine classifies on the assessed activity.</div></div></div>';
}

/* ===================== VIEW: INTEGRATION ===================== */
function vIntegration(){
 var rows=(DATA.integration||[]).map(function(x){return [esc(x[0]),bdg(x[1],"b-navy"),esc(x[2]),esc(x[3])];});
 return '<div class="lead">The Central Statistical Business Register integrates authoritative feeds from across the Qatari state under secured data-sharing instruments. Each attribute has a designated golden source.</div>'+
  '<div class="card"><div class="hd">Source systems &amp; integration</div><div class="bd">'+tbl(["Source system","Tier","Provides","Integration mode"],rows)+
  '<p class="small" style="margin-top:10px">Source systems and the tiers are drawn from the framework\'s CSBR reference architecture and the Independent Review. Integration <i>modes</i> (API, secure DB read-replica, SFTP, register sync, portal entry) are indicative engineering mechanisms.</p></div></div>'+
  '<div class="card"><div class="hd">Flow into the register</div><div class="bd"><div class="flow">'+
  ['Source systems (left)','Ingestion &amp; entity resolution (LEI lookup, fuzzy + graph matching)','Validation (VR-001..VR-018)','Master Data Hub — golden source by attribute, persistent ID, demographic-event log','Classification engine — 18 tests','Outputs — National Accounts, GFS, FDI, BoP, SBR; SDMX exchange to IMF/OECD/GCC-Stat'].map(function(t,i){return (i?'<div class="farrow">▼</div>':'')+'<div class="fnode"><div class="ft">'+(i+1)+'. '+t+'</div></div>';}).join("")+
  '</div></div></div>';
}

/* ===================== VIEW: SOURCES / CONFLICTS ===================== */
function vSources(){
 var tiers=(DATA.tiers||[]).map(function(x){return [bdg(x[0].split("—")[0].trim(),"b-navy")+" "+esc(x[0].split("—")[1]||""),esc(x[1]),esc(x[2])];});
 var princ=['Documented evidence wins over inferred status.','More recent attestation wins, all else equal.','Substance wins over legal form in control determinations.','Resolution is by data attribute, not by source tier (Review recommendation).','The statistical override is exercised by the Technical Classification Committee — never silently in the database; every override is minuted and reviewable.'];
 return '<div class="lead">When sources disagree, a fixed precedence resolves the conflict — refined by the Review to operate <b>per attribute</b> rather than purely by tier (e.g. GTA may hold more current activity data than the commercial register).</div>'+
  '<div class="card"><div class="hd">Source hierarchy</div><div class="bd">'+tbl(["Tier","Sources","Authoritative for"],tiers)+'</div></div>'+
  '<div class="card"><div class="hd">Conflict-resolution principles</div><div class="bd"><ul class="tight">'+princ.map(function(p){return "<li>"+esc(p)+"</li>";}).join("")+'</ul></div></div>'+
  '<div class="card"><div class="hd">Validation rule library (VR-001..VR-018)</div><div class="bd">'+tbl(["Rule","Name","Scope","Logic","Severity"],(DATA.rules,[]).concat(VR_ROWS()))+'</div></div>'+
  '<div class="card"><div class="hd">Audit trail</div><div class="bd">'+tbl(["When","Record","Action","Field","Old → New","By"],DATA.audit.slice(0,10).map(function(a){return [esc(a.timestamp),'<span class="mono small">'+esc(a.record_id)+'</span>',esc(a.action),esc(a.field||"—"),esc(a.old||"—")+" → "+esc(a.new||"—"),esc(a.by)];}))+'</div></div>';
}
function VR_ROWS(){return [
 ["VR-001","Sector code valid","Enterprise","sector_code must exist in codelist 06","ERROR"],["VR-002","ISIC class valid","Enterprise","isic_class must exist in codelist 08","ERROR"],
 ["VR-004","LEI format","Legal unit","lei null OR 20-char ISO 17442","WARN"],["VR-005","Ownership chain sums","Ownership","Σ ownership_pct into any owned_id ≤ 100","ERROR"],
 ["VR-006","Public-sector control","Enterprise","public-sector entity must carry a control flag","ERROR"],["VR-007","Financial sector match","Enterprise","S.12x ⇒ ISIC Section K","WARN"],
 ["VR-012","Hidden government ownership","Ownership","cross-check owner against state-vehicle list","WARN"],["VR-015","Empty-shell substance","Enterprise","no premises/employees/autonomy ⇒ Test 13","INFO"],
 ["VR-016","Demographic event logged","Audit","sector/control/size change ⇒ audit entry","ERROR"],["VR-018","Quality-flag progression","Enterprise","DRAFT → PEER-REVIEWED → COMMITTEE-RULED","WARN"]
].map(function(r){return [r[0],r[1],r[2],'<span class="mono small">'+esc(r[3])+'</span>',sevb(r[4])];});}

/* ===================== VIEW: STANDARDS ===================== */
function vStandards(){
 return '<div class="lead">Every classification rule is anchored to one or more standards. Below: what each standard is and where it is used in the platform.</div>'+
  DATA.standards.map(function(s){return '<div class="card"><div class="hd">'+esc(s.code)+' — '+esc(s.name)+'</div><div class="bd"><div class="small">'+esc(s.issuer)+' · '+esc(s.edition)+' · used for: '+esc(s.domains)+'</div><p style="margin-bottom:0">'+esc(s.description)+'</p></div></div>';}).join("");
}

/* ===================== VIEW: METHODOLOGY ===================== */
function vMethodology(){
 var stages=[["A","Define &amp; place","Tests 1–5"],["B","Public or private?","Tests 6–9"],["C","Shape &amp; reach","Tests 10–13"],["D","Assure &amp; commit","Tests 14–18"]];
 var sb='<div class="stagebar">'+stages.map(function(s){return '<div class="stage"><div class="sn">'+s[0]+'</div><div style="font-weight:700">'+s[1]+'</div><div class="small">'+s[2]+'</div></div>';}).join("")+'</div>';
 var tests=DATA.tests.slice().sort(function(a,b){return (a.test_code<b.test_code?-1:1);});
 var byNum=DATA.tests.slice().sort(function(a,b){return parseInt(a.test_code.slice(1))-parseInt(b.test_code.slice(1));});
 var rows=byNum.map(function(t){var rs=DATA.rules.filter(function(r){return r.test_code===t.test_code;}).length;return ['<b>'+esc(t.test_code)+'</b>',esc(t.name),esc(t.output_dimension||"—"),esc(t.standard_ref||"—"),rs?rs+" rule(s)":"process"];});
 return '<div class="lead">Every entity passes through the same eighteen sequenced tests, grouped into four stages. The output of each test feeds the next; conflicts within a test are resolved by priority. Classification follows reality, never the label.</div>'+sb+
  '<div class="card"><div class="hd">The eighteen tests</div><div class="bd">'+tbl(["Test","Name","Output","Standard","Rules"],rows)+'</div></div>'+
  '<div class="card"><div class="hd">Live worked example — run the engine on the mixed-ownership bank</div><div class="bd"><div id="methdemo"></div><button class="btn sm" onclick="methRun()">▶ Run the 18-test pipeline</button></div></div>'+
  '<div class="card"><div class="hd">Quality checks &amp; reclassification triggers</div><div class="bd"><ul class="tight"><li>Three-layer QA: analyst self-check → independent peer review → Technical Classification Committee ruling on edge cases.</li><li>Automated validation VR-001..VR-018 on every record.</li><li>Reclassification triggers: IPO, M&amp;A, new licence, material activity change, sovereign-vehicle reorganisation, JV formation, major contract — plus a mandatory three-year deep review.</li></ul></div></div>';
}
function methRun(){var e=ent("QA-ENT-20260000002");var oc=classifyEnterprise(e);var box=document.getElementById("methdemo");if(!box)return;box.innerHTML='<div class="timeline" id="methtl"></div>';var tl=document.getElementById("methtl");var i=0;
 (function tick(){if(i>=oc.trace.length)return;var s=oc.trace[i];var d=document.createElement("div");d.className="tstep"+(s.matched?" fire":"");var out=s.matched?Object.keys(s.output).map(function(k){return bdg(s.output[k],"b-green");}).join(" "):'<span class="small">governance / process step</span>';d.innerHTML='<div class="bt">'+esc(s.test_code)+'</div><div class="nm">'+esc(s.test_name)+'</div><div style="margin-top:3px">'+out+'</div>'+(s.matched?'<div class="small" style="margin-top:2px">'+esc(s.rule_id)+' · '+esc(s.standard_ref||"")+'</div>':'');tl.appendChild(d);d.scrollIntoView({block:"nearest"});i++;setTimeout(tick,170);})();}

/* ===================== VIEW: GOVERNANCE ===================== */
function vGovernance(){
 var g=DATA.governance;
 return '<div class="lead">Classification is a technical, evidence-based act under federated authority: the NSO is the registrar; QCB, MoCI, GTA, QFC, QFZA are co-producers with defined authoritative scopes.</div>'+
  '<div class="card"><div class="hd">Governance bodies</div><div class="bd">'+tbl(["Body","Chair","Mandate"],g.bodies.map(function(b){return [esc(b[0]),esc(b[1]),esc(b[2])];}))+'</div></div>'+
  '<div class="card"><div class="hd">RACI — who does what</div><div class="bd">'+tbl(["Activity","Responsible","Accountable","Consulted","Informed"],g.raci.map(function(r){return r.map(esc);}))+'</div></div>'+
  '<div class="card"><div class="hd">Review &amp; approval workflow</div><div class="bd"><div class="steps">'+g.workflow.map(function(w,i){return bdg((i+1)+". "+w,"b-navy");}).join(" ")+'</div><p class="small" style="margin-top:10px"><b>Cadence:</b> '+esc(g.cadence)+'</p></div></div>'+
  '<div class="card"><div class="hd">Quality KPIs (with SLAs)</div><div class="bd"><ul class="tight">'+g.kpis.map(function(k){return "<li>"+esc(k)+"</li>";}).join("")+'</ul></div></div>';
}

/* ===================== VIEW: DASHBOARD ===================== */
function vDashboard(){
 var E=DATA.enterprises;var conf=E.reduce(function(s,e){return s+(e.confidence||1);},0)/E.length;
 var withLei=E.filter(function(e){return e.lei;}).length;
 var k=function(n,l){return '<div class="kpi"><div class="n">'+n+'</div><div class="l">'+l+'</div></div>';};
 return '<div class="lead">Live distribution of the classified register. <b>Click any bar label to drill into the Enterprise Register</b> filtered to that group.</div>'+
  '<div class="grid auto" style="margin-bottom:18px">'+k(E.length,"Classified enterprises")+k(conf.toFixed(2),"Avg classification confidence")+k(Math.round(withLei/E.length*100)+"%","LEI coverage")+k("100%","Register completeness (demo)")+'</div>'+
  '<div class="grid c2"><div class="card"><div class="hd">By institutional sector</div><div class="bd">'+drillBars(countBy(E,"sector"),"regSec")+'</div></div>'+
  '<div class="card"><div class="hd">By public / private</div><div class="bd">'+drillBars(countBy(E,"public_private"),"regPP")+'</div></div></div>'+
  '<div class="grid c2"><div class="card"><div class="hd">By enterprise size</div><div class="bd">'+drillBars(countBy(E,"size"),"regSize")+'</div></div>'+
  '<div class="card"><div class="hd">By legal form</div><div class="bd">'+bars(countBy(E,"legal_form"))+'</div></div></div>'+
  '<div class="grid c2"><div class="card"><div class="hd">By control mechanism</div><div class="bd">'+bars(countBy(E,"control"))+'</div></div>'+
  '<div class="card"><div class="hd">By residency</div><div class="bd">'+bars(countBy(E,"residence"))+'</div></div></div>';
}

/* ===================== VIEW: ABOUT ===================== */
function vAbout(){
 return '<div class="card"><div class="hd">Purpose</div><div class="bd">A demonstration prototype of the Qatar Enterprise Classification Platform for the National Statistics Center under the National Planning Council. It classifies enterprises and economic entities by their <b>actual economic activity, ownership, control, legal form, institutional role, residency and operational characteristics</b> — never by commercial name, trade name, licence title or registration label alone — using the national framework and international standards (SNA 2025, IMF GFS 2014, BPM6, OECD BD4, ISIC Rev.4, LEI, SDMX, GSIM, GSBPM, DAMA DMBOK).</div></div>'+
  '<div class="card"><div class="hd">Scope</div><div class="bd">The 18-test methodology, institutional-sector and sub-sector classification (S.11–S.15, S.121–S.129, S.1311–S.1314), public/private boundary, ownership &amp; control, legal form, ISIC activity, residency, size, FDI relevance, the integrated register, source hierarchy, standards, governance and a live in-browser classification engine.</div></div>'+
  '<div class="card"><div class="hd">UAT limitations</div><div class="bd"><ul class="tight"><li>Sample records are illustrative stylised composites, not statements about real entities.</li><li>The classification engine runs entirely in your browser for demonstration; the production engine is the FastAPI/PostgreSQL platform.</li><li>Source-system integrations are represented, not live; transport modes are indicative.</li><li>A Qatar national activity classification beyond ISIC Rev.4 + the GCC-SIC cross-walk is not provided in the source files.</li></ul></div></div>'+
  '<div class="card" style="border-color:var(--maroon)"><div class="hd">Disclaimer</div><div class="bd"><b>DEMONSTRATION PROTOTYPE — UAT ENVIRONMENT — not for public deployment.</b> Entity-level records would be confidential under the Statistics Law; this prototype contains only stylised sample data.</div></div>';
}

/* ===================== ADVANCED INTERACTION ===================== */
function classifyAdhoc(inp,edges){var ed=edges.map(function(x){return Object.assign({},x,{owned_id:"ADHOC",owner_id:x.owner_id||x.owner_name,is_ultimate:"Y"});});return classify(buildFacts(inp,ed,"ADHOC"));}
function drillBars(map,stateKey){var e=Object.keys(map).map(function(k){return [k,map[k]];}).sort(function(a,b){return b[1]-a[1];});var mx=Math.max.apply(null,e.map(function(x){return x[1];}).concat([1]));
 return e.map(function(p,i){return '<div class="barrow"><div class="lbl" onclick="go(\'register\',{'+stateKey+':\''+p[0]+'\'})">'+esc(p[0])+'</div><div class="bar"><span style="width:'+(p[1]/mx*100)+'%;background:'+PAL[i%PAL.length]+'"></span></div><div style="text-align:right;font-weight:700">'+p[1]+'</div></div>';}).join("");}

/* ---- global header search ---- */
function gsearch(q){var box=document.getElementById("gsres");if(!box)return;q=(q||"").toLowerCase().trim();if(!q){box.innerHTML="";box.style.display="none";return;}
 var hits=DATA.enterprises.filter(function(e){return (e.name+e.id+e.sector+e.public_private).toLowerCase().indexOf(q)>=0;}).slice(0,8);
 box.style.display=hits.length?"block":"none";
 box.innerHTML=hits.map(function(e){return '<div onclick="gsel(\''+e.id+'\')"><b>'+esc(e.name)+'</b> <span class="small">· '+esc(e.sector)+' · '+esc(e.public_private)+'</span></div>';}).join("");}
function gsel(id){var box=document.getElementById("gsres");if(box){box.innerHTML="";box.style.display="none";}var inp=document.getElementById("gsearch");if(inp)inp.value="";loadDemo(id);}

/* ---- guided tour ---- */
var TOUR=[
 ["engine","Welcome","This is the Qatar Enterprise Classification Platform — a UAT prototype. The engine classifies an entity by its actual activity, ownership, control, legal form, residency and operations — never by its name or licence label. Press Next to begin."],
 ["engine","Classify a case","On the Engine screen, choose any of the 74 enterprises from the dropdown, or click a demonstration card. The 18-test engine runs live in your browser and assembles the full classification profile."],
 ["simulate","What-if simulator","Drag the ownership and market sliders and watch the classification change in real time — see an entity flip across the 50% control line or the market/non-market boundary."],
 ["lifecycle","Lifecycle events","Apply a corporate event — an IPO, a foreign acquisition, an activity change — and see the before/after reclassification with a full event and audit log."],
 ["compare","Compare entities","Place several entities side by side to see how the same methodology resolves different ownership and activity structures."],
 ["dashboard","Intelligence dashboard","Distributions by sector, ownership, size and more. Click any bar to drill into the register."],
 ["methodology","The methodology","The 18 sequenced tests, the standards behind them, and a live worked example. Every result is fully traceable."],
 ["about","You're ready","Explore freely — everything is clickable. This is a demonstration prototype on stylised sample data; not for public deployment."]
];
function tourStart(){state.tourStep=0;tourShow();}
function tourShow(){var t=document.getElementById("tour");if(!t)return;if(state.tourStep<0||state.tourStep>=TOUR.length){t.innerHTML="";return;}
 var s=TOUR[state.tourStep];if(state.view!==s[0]){state.view=s[0];render();}
 t.innerHTML='<div class="modal"><div class="box"><div class="top">★ Guided tour<span class="step">Step '+(state.tourStep+1)+' of '+TOUR.length+'</span></div>'+
  '<div class="bd"><div style="font-family:Georgia,serif;font-weight:700;font-size:16px;color:var(--navy);margin-bottom:6px">'+esc(s[1])+'</div><div>'+esc(s[2])+'</div></div>'+
  '<div class="ft"><button class="btn soft sm" onclick="tourEnd()">Skip</button>'+(state.tourStep>0?'<button class="btn ghost sm" onclick="tourNav(-1)">Back</button>':'')+'<button class="btn sm" onclick="tourNav(1)">'+(state.tourStep===TOUR.length-1?"Finish":"Next")+'</button></div></div></div>';}
function tourNav(d){state.tourStep+=d;if(state.tourStep>=TOUR.length){tourEnd();return;}tourShow();}
function tourEnd(){state.tourStep=-1;var t=document.getElementById("tour");if(t)t.innerHTML="";}

/* ---- What-if simulator ---- */
function simEdges(){var s=state.sim,ed=[];var rem=100;
 if(s.gov>0){ed.push({owner_id:"Government",owner_name:"Government of Qatar",owned_id:"SIM",ownership_pct:s.gov,voting_pct:s.gov,control_indicator:(s.gov>50?"MAJ-VOTE":s.ctrl),owner_is_government:true,owner_is_resident:true,is_ultimate:"Y"});rem-=s.gov;}
 if(s.foreign>0){ed.push({owner_id:"Foreign",owner_name:"Foreign investor",owned_id:"SIM",ownership_pct:s.foreign,voting_pct:s.foreign,control_indicator:(s.foreign>50?"MAJ-VOTE":""),owner_is_government:false,owner_is_resident:false,is_ultimate:"Y"});rem-=s.foreign;}
 if(rem>0.5)ed.push({owner_id:"Private",owner_name:"Resident private investors",owned_id:"SIM",ownership_pct:Math.round(rem*10)/10,voting_pct:Math.round(rem*10)/10,control_indicator:(rem>50?"MAJ-VOTE":""),owner_is_government:false,owner_is_resident:true,is_ultimate:"Y"});
 return ed;}
function simRun(){var s=state.sim,base=ent(s.base)||DATA.enterprises[0];var box=document.getElementById("simout");if(!box)return;
 var inp={legal_name_en:"Simulated entity",legal_form_code:base.inp.legal_form_code,residence:"RES",isic_class:base.inp.isic_class,
  employment:s.employment,turnover_qar:s.sales*1000,sales:s.sales*1000,production_costs:s.costs*1000,is_financial:s.isFin,is_nonprofit:false,
  has_premises:true,has_employees:true,has_autonomy:true,jurisdiction:base.inp.jurisdiction};
 var edges=simEdges();var f=buildFacts(inp,edges,"SIM");var oc=classify(f);var r=oc.result;var cover=f.sales_cover_pct;
 var pass=[["Institutional sector","<b>"+esc(r.sector_code)+"</b>"],["Public / private",pp(r.public_private)],["Control",bdg(r.control_flag)],["Market",r.market_status==="MARKET"?bdg("MARKET","b-green"):bdg("NON-MARKET","b-amber")],["Size",bdg(r.size_class,"b-navy")],["FDI",r.fdi_flag==="NONE"?"—":bdg(r.fdi_flag,"b-gold")]].map(function(p){return '<div class="r"><span class="k">'+p[0]+'</span><span>'+p[1]+'</span></div>';}).join("");
 var flips=[];
 flips.push("Effective government voting <b>"+f.government_voting_pct+"%</b> "+(f.government_voting_pct>50?"→ above the 50% control line (public)":"→ below 50%"));
 if(cover!=null)flips.push("Sales cover <b>"+cover.toFixed(0)+"%</b> of costs "+(cover>50?"→ market producer":"→ non-market producer"));
 if(f.foreign_ownership_pct>=10)flips.push("Foreign ownership <b>"+f.foreign_ownership_pct+"%</b> → FDI: "+r.fdi_flag);
 box.innerHTML='<div class="profile"><div class="top"><div class="nm">Live result · confidence '+oc.confidence+'</div><div class="id">based on '+esc(base.name)+' activity ('+esc(base.inp.isic_class)+')</div></div>'+pass+'</div>'+
  '<div class="flip">'+flips.map(function(x){return '<div>• '+x+'</div>';}).join("")+'</div>'+
  '<div class="svgwrap" style="margin-top:12px">'+ownSVG(edges,"SIM","Simulated entity")+'</div>';}
function vSimulate(){var s=state.sim;
 var bsel='<select onchange="state.sim.base=this.value;simRun()" style="padding:8px 10px;border:1px solid var(--rule);border-radius:7px;max-width:360px">'+DATA.enterprises.map(function(e){return '<option value="'+e.id+'" '+(s.base===e.id?"selected":"")+'>'+esc(e.name)+'</option>';}).join("")+'</select>';
 var rng=function(id,label,min,max,step,val,suf){return '<div class="simrow"><div>'+label+'</div><input class="slider" type="range" min="'+min+'" max="'+max+'" step="'+step+'" value="'+val+'" oninput="state.sim.'+id+'=this.valueAsNumber;document.getElementById(\'sv_'+id+'\').textContent=this.value+\''+(suf||"")+'\';simRun()"/><div class="v" id="sv_'+id+'">'+val+(suf||"")+'</div></div>';};
 var csel='<div class="simrow"><div>Minority control (if gov ≤50%)</div><select onchange="state.sim.ctrl=this.value;simRun()" style="padding:7px;border:1px solid var(--rule);border-radius:6px">'+["MAJ-VOTE","GOLDEN","BOARD","CONTRACT","REGULATORY","NONE"].map(function(o){return '<option '+(s.ctrl===o?"selected":"")+'>'+o+'</option>';}).join("")+'</select><div></div></div>';
 var fin='<div class="simrow"><div>Financial intermediary?</div><label class="small"><input type="checkbox" '+(s.isFin?"checked":"")+' onchange="state.sim.isFin=this.checked;simRun()"/> treat as financial corporation</label><div></div></div>';
 return '<div class="principle"><b>Move the sliders and watch the classification change instantly.</b> This shows exactly how ownership, control and the market test drive the outcome — for example, take government voting across 50%, or push sales below costs.</div>'+
  '<div class="grid c2"><div class="card"><div class="hd">Inputs</div><div class="bd"><div class="field"><label>Base activity / legal form from</label>'+bsel+'</div>'+
  rng("gov","Government ownership",0,100,1,s.gov,"%")+rng("foreign","Foreign ownership",0,100,1,s.foreign,"%")+csel+
  rng("sales","Sales (QAR m)",0,40000,100,s.sales,"m")+rng("costs","Production costs (QAR m)",0,40000,100,s.costs,"m")+rng("employment","Employment (FTE)",0,8000,10,s.employment,"")+fin+
  '</div></div><div class="card"><div class="hd">Live classification</div><div class="bd" id="simout"></div></div></div>';
}

/* ---- Reclassification & lifecycle events ---- */
var EVENTS={
 IPO_MINORITY:["IPO — government sells down to 40%","Government floats a majority of shares, retaining a 40% minority with no special control rights.",function(inp,edges){var e=[{owner_id:"Government",owner_name:"Government of Qatar",owned_id:"LC",ownership_pct:40,voting_pct:40,control_indicator:"",owner_is_government:true,owner_is_resident:true,is_ultimate:"Y"},{owner_id:"Float",owner_name:"Public float (QSE)",owned_id:"LC",ownership_pct:60,voting_pct:60,control_indicator:"",owner_is_government:false,owner_is_resident:true,is_ultimate:"Y"}];return [inp,e];}],
 IPO_GOLDEN:["IPO — sell down to 40% but retain a golden share","Government floats to 40% but keeps a golden share with veto over strategic decisions.",function(inp,edges){var e=[{owner_id:"Government",owner_name:"Government of Qatar",owned_id:"LC",ownership_pct:40,voting_pct:40,control_indicator:"GOLDEN",owner_is_government:true,owner_is_resident:true,is_ultimate:"Y"},{owner_id:"Float",owner_name:"Public float (QSE)",owned_id:"LC",ownership_pct:60,voting_pct:60,control_indicator:"",owner_is_government:false,owner_is_resident:true,is_ultimate:"Y"}];return [inp,e];}],
 FOREIGN_ACQ:["Foreign acquisition — 70% taken by a foreign investor","A foreign multinational acquires a controlling 70% stake.",function(inp,edges){var e=[{owner_id:"ForeignAcq",owner_name:"Foreign acquirer",owned_id:"LC",ownership_pct:70,voting_pct:70,control_indicator:"MAJ-VOTE",owner_is_government:false,owner_is_resident:false,is_ultimate:"Y"},{owner_id:"Residual",owner_name:"Residual holders",owned_id:"LC",ownership_pct:30,voting_pct:30,control_indicator:"",owner_is_government:false,owner_is_resident:true,is_ultimate:"Y"}];return [inp,e];}],
 NATIONALISATION:["Nationalisation — State takes 100%","The State acquires the entity in full.",function(inp,edges){var e=[{owner_id:"Government",owner_name:"Government of Qatar",owned_id:"LC",ownership_pct:100,voting_pct:100,control_indicator:"MAJ-VOTE",owner_is_government:true,owner_is_resident:true,is_ultimate:"Y"}];return [inp,e];}],
 ACTIVITY_CHANGE:["Activity change — pivots to banking","The principal activity by value added shifts to monetary intermediation (a bank).",function(inp,edges){var i=Object.assign({},inp);i.isic_class="6419";i.is_financial=true;return [i,edges];}],
 MARKET_LOSS:["Subsidy shift — sales fall below cost recovery","Tariffs become subsidised; sales now cover less than 50% of costs.",function(inp,edges){var i=Object.assign({},inp);i.sales=Math.round((i.production_costs||100)*0.3);return [i,edges];}],
 DORMANCY:["Dormancy — operations cease","No employment, no turnover, no transactions.",function(inp,edges){var i=Object.assign({},inp);i.employment=0;i.turnover_qar=0;i.sales=0;i.has_employees=false;i.has_premises=false;return [i,edges];}]
};
function vLifecycle(){
 var e=ent(state.lcId)||DATA.enterprises[0];
 var esel='<select onchange="state.lcId=this.value;render()" style="padding:8px 10px;border:1px solid var(--rule);border-radius:7px;max-width:360px">'+DATA.enterprises.map(function(x){return '<option value="'+x.id+'" '+(state.lcId===x.id?"selected":"")+'>'+esc(x.name)+'</option>';}).join("")+'</select>';
 var evsel='<select onchange="state.lcEvent=this.value;render()" style="padding:8px 10px;border:1px solid var(--rule);border-radius:7px;max-width:360px">'+Object.keys(EVENTS).map(function(k){return '<option value="'+k+'" '+(state.lcEvent===k?"selected":"")+'>'+esc(EVENTS[k][0])+'</option>';}).join("")+'</select>';
 var ev=EVENTS[state.lcEvent];
 var before=classifyEnterprise(e).result;
 var mod=ev[2](Object.assign({legal_name_en:e.name},e.inp),edgesOf(e).map(function(x){return Object.assign({},x,{owned_id:"LC"});}));
 var after=classifyAdhoc(mod[0],mod[1]).result;
 var dims=[["Institutional sector","sector_code"],["Public / private","public_private"],["Control","control_flag"],["Market","market_status"],["Size","size_class"],["FDI","fdi_flag"],["Special entity","special_entity_flag"]];
 var col=function(cls,title,r){return '<div class="col '+cls+'"><div class="h">'+title+'</div>'+dims.map(function(d){var chg=before[d[1]]!==after[d[1]];return '<div class="r'+(chg?" chgd":"")+'"><span class="k muted">'+d[0]+'</span><span>'+(d[1]==="public_private"?pp(r[d[1]]):"<b>"+esc(r[d[1]])+"</b>")+'</span></div>';}).join("")+'</div>';};
 var changed=dims.filter(function(d){return before[d[1]]!==after[d[1]];});
 var now=new Date().toISOString().slice(0,16).replace("T"," ");
 var log=tbl(["When","Event","Action","Detail"],[[now,esc(ev[0]),"DEMOGRAPHIC EVENT",esc(ev[1])],[now,"—","RECLASSIFY","18-test pipeline re-run on the new facts"],[now,"—","VERSION","new classification version written; prior retained (valid_from/valid_to)"],[now,"—","AUDIT",changed.length+" dimension(s) changed; logged with rationale"]]);
 return '<div class="principle"><b>Classification is event-driven.</b> Every corporate event — births, deaths, mergers, splits, IPOs, takeovers, activity changes — is recorded and triggers a reclassification. The prior classification is never overwritten; a new version is written so history is reproducible.</div>'+
  '<div class="card"><div class="hd">Choose an entity and apply an event</div><div class="bd"><div class="frow"><div class="field"><label>Entity</label>'+esel+'</div><div class="field"><label>Lifecycle event (trigger)</label>'+evsel+'</div></div><div class="small">'+esc(ev[1])+'</div></div></div>'+
  '<div class="card"><div class="hd">Before → after reclassification'+(changed.length?(' — '+changed.length+' dimension(s) change'):' — no change')+'</div><div class="bd"><div class="ba"><div>'+col("before","BEFORE — current classification",before)+'</div><div class="arrow">→</div><div>'+col("after","AFTER — "+esc(ev[0]),after)+'</div></div></div></div>'+
  '<div class="card"><div class="hd">Event &amp; audit log</div><div class="bd">'+log+'</div></div>';
}

/* ---- Compare entities ---- */
function vCompare(){
 var picks=state.cmp.slice(0,4);
 var opts=function(sel){return DATA.enterprises.map(function(e){return '<option value="'+e.id+'" '+(sel===e.id?"selected":"")+'>'+esc(e.name)+'</option>';}).join("");};
 var sels=picks.map(function(id,i){return '<select onchange="state.cmp['+i+']=this.value;render()" style="width:100%;padding:7px;border:1px solid var(--rule);border-radius:6px">'+opts(id)+'</select>';});
 var dims=[["Legal form","legal_form"],["Institutional sector","sector"],["Public / private","public_private"],["Control","control"],["Market","market"],["Size","size"],["Residency","residence"],["FDI","fdi"],["Special","special"],["Confidence","confidence"]];
 var rows=dims.map(function(d){return '<div style="display:grid;grid-template-columns:160px repeat('+picks.length+',1fr);gap:0"><div style="padding:9px 12px;border-bottom:1px solid var(--rule);color:var(--muted);font-size:12.5px;background:#f0f1f4">'+d[0]+'</div>'+picks.map(function(id){var e=ent(id);var v=e[d[1]];return '<div style="padding:9px 12px;border-bottom:1px solid var(--rule);border-left:1px solid var(--rule);font-size:12.5px">'+(d[1]==="public_private"?pp(v):esc(v))+'</div>';}).join("")+'</div>';}).join("");
 var head='<div style="display:grid;grid-template-columns:160px repeat('+picks.length+',1fr);gap:0"><div style="padding:9px 12px;background:var(--navy);color:#fff"></div>'+picks.map(function(id){var e=ent(id);return '<div style="padding:9px 12px;background:var(--navy);color:#fff;border-left:1px solid #2a3a52;font-size:12.5px;font-weight:700">'+esc(e.name)+'</div>';}).join("")+'</div>';
 return '<div class="lead">Place entities side by side to see how the same 18-test methodology resolves different ownership, activity and control structures into different classifications.</div>'+
  '<div class="card"><div class="hd">Select entities to compare</div><div class="bd"><div class="grid" style="grid-template-columns:repeat('+picks.length+',1fr)">'+sels.join("")+'</div></div></div>'+
  '<div class="card"><div class="bd"><div class="cmpgrid" style="border:0">'+head+rows+'</div><p class="small" style="margin-top:10px">Tip: change any selector to swap an entity. Open the engine for a full profile and explainability of any one of them.</p></div></div>';
}

var VIEWS={engine:vEngine,register:vRegister2,dashboard:vDashboard,simulate:vSimulate,lifecycle:vLifecycle,compare:vCompare,isic:vIsic,sector:vSector,ownership:vOwnership,legal:vLegal,integration:vIntegration,sources:vSources,standards:vStandards,methodology:vMethodology,governance:vGovernance,about:vAbout};
function render(){
 try{
  document.getElementById("nav").innerHTML=NAV.map(function(g){return '<div class="grp">'+g[0]+'</div>'+g[1].map(function(m){var idx=Object.keys(TITLES).indexOf(m[0])+1;return '<a class="'+(state.view===m[0]?"active":"")+'" onclick="go(\''+m[0]+'\')"><span class="ix">'+idx+'</span>'+m[1]+'</a>';}).join("");}).join("");
  var c=document.getElementById("content");
  c.innerHTML='<div class="pt">'+esc(TITLES[state.view])+'</div><div class="ps">Qatar Enterprise Classification Platform · classify by economic reality — activity, ownership, control, residency — not by label.</div>'+(VIEWS[state.view]||vEngine)();
  if(state.view==="engine"&&state.eng&&state.eng._auto){state.eng._auto=false;runEngine();}
  if(state.view==="simulate")simRun();
  document.getElementById("foot").innerHTML='Qatar Enterprise Classification Platform · UAT clickable prototype · data &amp; methodology extracted from the National Framework, Implementation Workbook, Executive Story and Independent Review · generated '+esc(DATA.generated)+'. <b>Not for public deployment.</b>';
 }catch(err){
  document.getElementById("content").innerHTML='<div class="card"><div class="bd"><b>Display notice.</b> <span class="small">'+esc(err&&err.message)+'</span> <button class="btn sm" onclick="state.view=\'engine\';render()">Back to engine</button></div></div>';
 }
}
render();
</script>
</body>
</html>
"""
