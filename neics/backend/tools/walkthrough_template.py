"""Interactive NEICS walkthrough template — a working, clickable demonstration.

Embeds the data (enterprises with raw inputs + ownership, rules, the 18 tests,
standards, etc.) and a faithful in-browser port of the classification engine, so
the walkthrough actually CLASSIFIES live (existing enterprises and user-uploaded
ones), shows the data-flow architecture, the ingestion/upload path, and a working
API console. `/*__DATA__*/` is replaced by build_walkthrough.py.

Clean corporate design; robust (render wrapped in try/catch with visible fallback).
"""

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>NEICS — National Enterprise Intelligence & Classification System</title>
<style>
:root{
 --maroon:#8a1538;--maroon-d:#6b0f2b;--gold:#b08d57;--ink:#202733;--ink2:#3d4757;--muted:#697587;
 --line:#e6e9ee;--line2:#f0f2f5;--bg:#eef1f5;--surface:#fff;--surface2:#f7f9fc;
 --blue:#1d6fb8;--blueb:#e9f2fb;--green:#1a8a4f;--greenb:#e8f5ee;--amber:#946610;--amberb:#fbf1da;
 --red:#bf372a;--redb:#fbe9e7;--purple:#7a3b97;--purpleb:#f4eafa;--teal:#127a6c;--tealb:#e3f3f0;--grayb:#eef1f4;
}
*{box-sizing:border-box}
body{margin:0;font-family:"Segoe UI",-apple-system,BlinkMacSystemFont,Roboto,Helvetica,Arial,sans-serif;
 color:var(--ink);background:var(--bg);font-size:14.5px;line-height:1.6;-webkit-text-size-adjust:100%}
a{color:var(--maroon);text-decoration:none}
button{font-family:inherit;cursor:pointer}
input,select,textarea{font-family:inherit;font-size:13.5px}
.topbar{position:sticky;top:0;z-index:100;background:var(--maroon);color:#fff;display:flex;align-items:center;gap:12px;padding:10px 16px}
.topbar .logo{width:32px;height:32px;border-radius:7px;background:#fff;color:var(--maroon);font-weight:800;display:flex;align-items:center;justify-content:center}
.topbar b{font-size:15px}.topbar small{opacity:.85;font-size:11px}
.topbar .sp{flex:1}
.topbar .stg{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.32);padding:4px 11px;border-radius:20px;font-size:11px;font-weight:600;white-space:nowrap}
.nav{position:sticky;top:52px;z-index:90;background:var(--surface);border-bottom:1px solid var(--line);overflow-x:auto;white-space:nowrap;-webkit-overflow-scrolling:touch;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.nav .inner{display:flex;gap:1px;padding:0 8px;max-width:1180px;margin:0 auto}
.nav button{border:0;background:none;padding:12px 13px;font-size:13px;color:var(--ink2);font-weight:600;border-bottom:3px solid transparent}
.nav button:hover{color:var(--maroon)} .nav button.active{color:var(--maroon);border-bottom-color:var(--maroon)}
.content{max-width:1180px;margin:0 auto;padding:24px 20px}
.h-page{font-size:23px;font-weight:750;margin:0 0 3px}
.h-sub{color:var(--muted);font-size:13.5px;margin:0 0 20px;max-width:840px}
.help{background:var(--blueb);border:1px solid #cfe0f1;border-left:4px solid var(--blue);border-radius:8px;padding:11px 14px;margin-bottom:18px;font-size:13.5px;color:#27496b}
.grid{display:grid;gap:16px}.auto{grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}
.c2{grid-template-columns:1fr 1fr}.c23{grid-template-columns:3fr 2fr}.c32{grid-template-columns:2fr 1fr}
@media(max-width:900px){.c2,.c23,.c32{grid-template-columns:1fr}}
.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;box-shadow:0 1px 2px rgba(17,24,39,.05);margin-bottom:16px}
.card>.hd{padding:14px 18px;border-bottom:1px solid var(--line2);font-weight:650;display:flex;align-items:center;gap:9px}
.card>.hd::before{content:"";width:8px;height:18px;border-radius:3px;background:var(--maroon)}
.card>.bd{padding:18px}
.kpi{background:var(--surface);border:1px solid var(--line);border-top:3px solid var(--maroon);border-radius:12px;padding:17px;box-shadow:0 1px 2px rgba(17,24,39,.05)}
.kpi .n{font-size:29px;font-weight:780;line-height:1}.kpi .l{color:var(--muted);font-size:12.5px;margin-top:6px}
.bdg{display:inline-block;padding:3px 10px;border-radius:14px;font-size:11.5px;font-weight:650;white-space:nowrap}
.b-blue{background:var(--blueb);color:var(--blue)}.b-green{background:var(--greenb);color:var(--green)}
.b-purple{background:var(--purpleb);color:var(--purple)}.b-amber{background:var(--amberb);color:var(--amber)}
.b-red{background:var(--redb);color:var(--red)}.b-teal{background:var(--tealb);color:var(--teal)}.b-gray{background:var(--grayb);color:#4b5563}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--line);border-radius:10px}
table.t{width:100%;border-collapse:collapse;font-size:13.5px;background:var(--surface)}
table.t th,table.t td{text-align:left;padding:10px 13px;border-bottom:1px solid var(--line2)}
table.t th{background:var(--surface2);color:var(--muted);font-size:10.5px;text-transform:uppercase;letter-spacing:.6px;font-weight:700}
table.t tr:last-child td{border-bottom:0} table.t tr.row:hover{background:var(--surface2);cursor:pointer}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px}.small{font-size:12.5px;color:var(--muted)}
.kv{display:grid;grid-template-columns:190px 1fr;gap:8px 16px;font-size:14px}.kv .k{color:var(--muted)}
@media(max-width:620px){.kv{grid-template-columns:1fr;gap:2px}.kv .k{margin-top:7px;font-weight:600}}
.btn{display:inline-block;background:var(--maroon);color:#fff;border:0;padding:10px 17px;border-radius:8px;font-size:13.5px;font-weight:600}
.btn:hover{background:var(--maroon-d)} .btn.ghost{background:#fff;color:var(--maroon);border:1px solid var(--maroon)}
.btn.soft{background:var(--surface2);color:var(--ink2);border:1px solid var(--line)} .btn.sm{padding:6px 11px;font-size:12px}
.bar{height:10px;background:var(--line2);border-radius:6px;overflow:hidden}.bar>span{display:block;height:100%}
.barrow{display:grid;grid-template-columns:180px 1fr 44px;gap:11px;align-items:center;margin:9px 0;font-size:13px}
@media(max-width:620px){.barrow{grid-template-columns:120px 1fr 36px}}
.note{background:#fbfaf6;border:1px solid #ece4d2;border-radius:10px;padding:12px 15px;font-size:13.5px}
ul.tight{margin:6px 0;padding-left:20px}ul.tight li{margin:6px 0}
.field{margin-bottom:11px}.field label{display:block;font-size:12px;color:var(--muted);font-weight:600;margin-bottom:4px}
.field input,.field select{width:100%;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:#fff}
.frow{display:grid;grid-template-columns:1fr 1fr;gap:11px}
.svgwrap{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:10px;overflow:auto}
.legend{font-size:11.5px;color:var(--muted);margin-top:8px}
/* Flow diagram */
.flow{display:flex;flex-direction:column;gap:14px}
.flowrow{display:flex;gap:12px;flex-wrap:wrap;align-items:stretch;justify-content:center}
.fnode{flex:1;min-width:150px;max-width:230px;border:1.5px solid var(--line);border-radius:11px;background:#fff;padding:13px;cursor:pointer;box-shadow:0 1px 2px rgba(17,24,39,.05);transition:.15s}
.fnode:hover{border-color:var(--maroon);transform:translateY(-2px)}
.fnode .ft{font-weight:700;font-size:13.5px;margin-bottom:4px}.fnode .fd{font-size:11.5px;color:var(--muted)}
.fnode.stage{border-top:4px solid var(--maroon)}
.farrow{text-align:center;color:var(--maroon);font-size:20px;line-height:1}
/* Stepper */
.timeline{border-left:3px solid var(--line);margin-left:13px;padding-left:20px}
.tstep{position:relative;margin-bottom:11px;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 14px;opacity:.5;transition:.2s}
.tstep.on{opacity:1;box-shadow:0 1px 3px rgba(17,24,39,.06)} .tstep.fire{border-color:var(--maroon)}
.tstep .bt{position:absolute;left:-33px;top:12px;width:26px;height:26px;border-radius:50%;background:#c4ccd6;color:#fff;font-size:10px;font-weight:700;display:flex;align-items:center;justify-content:center;border:3px solid var(--surface2)}
.tstep.fire .bt{background:var(--maroon)}.tstep .nm{font-weight:650;font-size:13.5px}
.passport{border:1px solid var(--line);border-radius:13px;overflow:hidden;box-shadow:0 2px 8px rgba(17,24,39,.08)}
.passport .top{background:linear-gradient(135deg,#8a1538,#5c0e25);color:#fff;padding:15px 17px}
.passport .top .nm{font-weight:700} .passport .top .id{font-size:11px;opacity:.85}
.passport .r{display:flex;justify-content:space-between;align-items:center;padding:10px 17px;border-bottom:1px solid var(--line2);font-size:13.5px}
.passport .r:last-child{border-bottom:0}.passport .r .k{color:var(--muted)}
.gnode{display:inline-block;border:1.5px solid var(--line);border-radius:9px;padding:7px 13px;margin:5px;background:#fff}
.lvl{padding-left:22px;border-left:2px dashed #d6dde4;margin-left:18px}
.gnode.gov{border-color:var(--purple)}.gnode.foreign{border-color:#b9651b}.gnode.entity{border-color:var(--maroon)}.gnode.priv{border-color:var(--green)}
.rag{font-weight:700}.rag.Green{color:var(--green)}.rag.Amber{color:var(--amber)}.rag.Red,.rag.RedAmber{color:var(--red)}.rag.AmberGreen{color:#6e861b}
pre.code{background:#101826;color:#d6e2ee;padding:12px;border-radius:9px;overflow:auto;font-size:12px;white-space:pre-wrap;word-break:break-word}
.foot{padding:24px;text-align:center;color:var(--muted);font-size:12px}
</style>
</head>
<body>
<div class="topbar"><div class="logo">N</div><div><b>NEICS</b> <small>· State of Qatar · NSO</small></div><span class="sp"></span><span class="stg">● STAGING / UAT — engine running in-browser</span></div>
<div class="nav"><div class="inner" id="nav"></div></div>
<div class="content" id="content"></div>
<div class="foot">NEICS — National Enterprise Intelligence &amp; Classification System · Staging / UAT walkthrough · the classification engine in this page runs entirely in your browser</div>
<script>
"use strict";
var DATA = /*__DATA__*/;

/* ============================== ENGINE (faithful port of the backend) ============================== */
var CONTROL_PRIORITY=["MAJ-VOTE","GOLDEN","BOARD","KEY-PERS","CONTRACT","REGULATORY","FINANCING","DOMINANT","BO-CHAIN"];
function _num(v){var n=parseFloat(v);return isNaN(n)?null:n;}
function leaf(c,f){var op=c.op,a=f[c.field],v=c.value;
 if(op==="exists")return (c.field in f)&&f[c.field]!=null;
 if(op==="truthy")return !!a;
 if(op==="eq")return a===v; if(op==="ne")return a!==v;
 if(op==="in")return (v||[]).indexOf(a)>=0;
 if(op==="gt"||op==="gte"||op==="lt"||op==="lte"){var x=_num(a),y=_num(v);if(x==null||y==null)return false;return op==="gt"?x>y:op==="gte"?x>=y:op==="lt"?x<y:x<=y;}
 if(op==="between"){var x2=_num(a);if(x2==null)return false;var lo=_num((v||[])[0]),hi=_num((v||[])[1]);if(lo!=null&&x2<lo)return false;if(hi!=null&&x2>=hi)return false;return true;}
 return false;}
function evalCond(c,f){if(!c||!Object.keys(c).length)return true;
 if(c.all)return c.all.every(function(x){return evalCond(x,f);});
 if(c.any)return c.any.some(function(x){return evalCond(x,f);});
 if(c.not)return !evalCond(c.not,f);
 if(c.op)return leaf(c,f); return false;}
function resolveOut(spec,f){if(spec&&typeof spec==="object"){if("const" in spec)return spec.const;if("fact" in spec)return f[spec.fact];}return spec;}

/* ownership over an edge list [{owner_id,owned_id,ownership_pct,voting_pct,control_indicator,owner_is_government,owner_is_resident}] */
function incoming(edges,node){return edges.filter(function(e){return e.owned_id===node;});}
function effShare(node,pred,useVoting,edges,seen){if(seen[node])return 0;var s=Object.assign({},seen);s[node]=1;var tot=0;
 incoming(edges,node).forEach(function(e){var pct=(useVoting?e.voting_pct:e.ownership_pct)||0;var fr=pct/100;
  if(pred(e))tot+=fr; else tot+=fr*effShare(e.owner_id,pred,useVoting,edges,s);});
 return Math.min(tot,1);}
function strongest(inds){for(var i=0;i<CONTROL_PRIORITY.length;i++){if(inds.indexOf(CONTROL_PRIORITY[i])>=0)return CONTROL_PRIORITY[i];}return null;}
function uci(node,edges,seen){seen=seen||{};if(seen[node])return null;var inc=incoming(edges,node);if(!inc.length)return null;
 var ult=inc.filter(function(e){return e.is_ultimate==="Y";})[0];
 var dom=ult||inc.reduce(function(a,b){return ((b.voting_pct||b.ownership_pct||0)>(a.voting_pct||a.ownership_pct||0))?b:a;});
 var ns=Object.assign({},seen);ns[node]=1;var parent=uci(dom.owner_id,edges,ns);
 if(parent)return parent;
 return {uci_name:dom.owner_name||dom.owner_id,is_government:!!dom.owner_is_government,is_resident:dom.owner_is_resident!==false};}
function ownershipFacts(target,edges){
 var govOwn=Math.round(100*effShare(target,function(e){return e.owner_is_government;},false,edges,{}))/1;
 var govVote=Math.round(100*effShare(target,function(e){return e.owner_is_government;},true,edges,{}));
 var forOwn=Math.round(100*effShare(target,function(e){return e.owner_is_resident===false;},false,edges,{}));
 var direct=incoming(edges,target);
 var allInds=direct.map(function(e){return e.control_indicator;}).filter(function(c){return c&&c!=="NONE";});
 var govInds=direct.filter(function(e){return e.owner_is_government;}).map(function(e){return e.control_indicator;}).filter(function(c){return c&&c!=="NONE";});
 var maxVote=direct.length?Math.max.apply(null,direct.map(function(e){return e.voting_pct||e.ownership_pct||0;})):0;
 var u=uci(target,edges,{});
 var govControl=govVote>50||govInds.length>0;
 var rep;
 if(govControl){rep=strongest(govInds)||(govVote>50?"MAJ-VOTE":"BO-CHAIN");}
 else if(maxVote>50){rep="MAJ-VOTE";}
 else if(allInds.length){rep=strongest(allInds)||"NONE";}
 else if(forOwn>50){rep="BO-CHAIN";}
 else{rep="NONE";}
 return {government_ownership_pct:Math.round(govOwn*100)/100,government_voting_pct:govVote,foreign_ownership_pct:Math.round(forOwn*100)/100,
  control_indicators:allInds,government_control:govControl,representative_control_flag:rep,has_substance:undefined,
  uci_is_government:!!(u&&u.is_government),uci_is_foreign:!!(u&&u.is_resident===false),uci:u,max_direct_voting:maxVote};}
function buildFacts(inp,edges,target){
 var sales=inp.sales||0,costs=inp.production_costs||0;
 var ratio=costs>0?sales/costs:null;
 var f={legal_form_code:inp.legal_form_code,residence:inp.residence,isic_class:inp.isic_class,
  employment:inp.employment||0,turnover_qar:inp.turnover_qar||0,sales:sales,production_costs:costs,
  sales_to_cost_ratio:ratio,sales_cover_pct:ratio!=null?ratio*100:null,
  is_nonprofit:!!inp.is_nonprofit,is_financial:!!inp.is_financial,has_premises:inp.has_premises!==false,
  has_employees:inp.has_employees!==false,has_autonomy:inp.has_autonomy!==false,jurisdiction:inp.jurisdiction};
 f.has_substance=!!(f.has_premises||f.has_employees||f.has_autonomy);
 var of=ownershipFacts(target,edges||[]);for(var k in of)f[k]=of[k];
 return f;}
var RESULT_FIELDS=["residence","isic_class","sector_code","market_status","control_flag","public_private","size_class","fdi_flag","special_entity_flag"];
function classify(facts){
 var result={},trace=[],confs=[];
 var tests=DATA.tests.slice().sort(function(a,b){return a.seq-b.seq;});
 tests.forEach(function(t){
  var rules=DATA.rules.filter(function(r){return r.test_code===t.test_code;}).sort(function(a,b){return a.priority-b.priority;});
  var fired=null;
  for(var i=0;i<rules.length;i++){var r=rules[i];
   if(evalCond(r.logic,facts)){fired=r;var applied={};
    Object.keys(r.output||{}).forEach(function(k){var val=resolveOut(r.output[k],facts);facts[k]=val;if(RESULT_FIELDS.indexOf(k)>=0)result[k]=val;applied[k]=val;});
    confs.push(r.confidence);
    trace.push({test_code:t.test_code,test_name:t.name,matched:true,rule_id:r.rule_id,rule_name:r.name,output:applied,confidence:r.confidence,standard_ref:r.standard_ref,rationale:r.rationale});
    break;}}
  if(!fired)trace.push({test_code:t.test_code,test_name:t.name,matched:false});});
 var conf=confs.length?confs.reduce(function(a,b){return a+b;},0)/confs.length:null;
 return {result:result,trace:trace,facts:facts,confidence:conf!=null?Math.round(conf*1000)/1000:null};}
function edgesOf(ent){ // existing enterprise: use its embedded chain as the edge set
 return (ent.ownership.chain||[]).map(function(c){return {owner_id:c.owner_id,owner_name:c.owner_name,owned_id:c.owned_id,
  ownership_pct:c.ownership_pct,voting_pct:c.voting_pct,control_indicator:c.control_indicator,
  owner_is_government:c.is_government,owner_is_resident:c.is_resident,is_ultimate:"N"};});}
function classifyEnterprise(ent){return classify(buildFacts(ent.inp,edgesOf(ent),ent.id));}

/* lightweight validation (subset of VR-001..018) for the ingestion demo */
function validateInput(inp){var out=[];
 if(!inp.legal_name_en)out.push({rule:"required",sev:"ERROR",msg:"legal_name_en is required"});
 if(["RES","NRES","MULTI"].indexOf(inp.residence)<0)out.push({rule:"VR-008",sev:"ERROR",msg:"residence must be RES, NRES or MULTI"});
 if(inp.isic_class&&DATA.isic_codes&&!DATA.isic_codes[inp.isic_class])out.push({rule:"VR-002",sev:"WARN",msg:"ISIC class "+inp.isic_class+" not in codelist"});
 if(!inp.employment&&!inp.turnover_qar)out.push({rule:"VR-011",sev:"INFO",msg:"No employment and no turnover — possible dormant unit"});
 return out;}

/* ============================== HELPERS ============================== */
function esc(s){return (s==null?"":String(s)).replace(/[&<>]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;"}[c];});}
function ent(id){for(var i=0;i<DATA.enterprises.length;i++)if(DATA.enterprises[i].id===id)return DATA.enterprises[i];return null;}
function money(v){if(!v)return "—";if(v>=1e9)return "QAR "+(v/1e9).toFixed(1)+"bn";if(v>=1e6)return "QAR "+(v/1e6).toFixed(1)+"m";if(v>=1e3)return "QAR "+(v/1e3).toFixed(0)+"k";return "QAR "+v.toLocaleString();}
var PP={"PUB-NFC":["b-blue","Public non-financial corp"],"PUB-FC":["b-blue","Public financial corp"],"GG":["b-purple","General government"],"PRV-NFC":["b-green","Private non-financial corp"],"PRV-FC":["b-green","Private financial corp"],"FCC":["b-amber","Foreign-controlled corp"],"NPISH":["b-teal","NPISH"]};
function pp(v){var m=PP[v]||["b-gray",v];return '<span class="bdg '+m[0]+'">'+esc(v)+'</span>';}
function bdg(v,c){return '<span class="bdg '+(c||"b-gray")+'">'+esc(v)+'</span>';}
function qcol(s){return s>=.85?"var(--green)":s>=.7?"var(--amber)":"var(--red)";}
var PAL=["#8a1538","#1d6fb8","#7a3b97","#1a8a4f","#b9651b","#127a6c","#a8204a","#946610","#52606d"];
function bars(map){var e=Object.keys(map).map(function(k){return [k,map[k]];}).sort(function(a,b){return b[1]-a[1];});var mx=Math.max.apply(null,e.map(function(x){return x[1];}).concat([1]));
 return e.map(function(p,i){return '<div class="barrow"><div>'+esc(p[0])+'</div><div class="bar"><span style="width:'+(p[1]/mx*100)+'%;background:'+PAL[i%PAL.length]+'"></span></div><div style="text-align:right;font-weight:650">'+p[1]+'</div></div>';}).join("");}
function countBy(arr,k){var m={};arr.forEach(function(x){var v=x[k]||"—";m[v]=(m[v]||0)+1;});return m;}
function tbl(h,rows){return '<div class="tw"><table class="t"><tr>'+h.map(function(x){return "<th>"+esc(x)+"</th>";}).join("")+'</tr>'+rows.map(function(r){return "<tr>"+r.map(function(c){return "<td>"+c+"</td>";}).join("")+"</tr>";}).join("")+'</table></div>';}
function sevb(s){return bdg(s,{ERROR:"b-red",WARN:"b-amber",INFO:"b-blue"}[s]||"b-gray");}

function ownSVG(edgesAll,target,name){
 var ch=edgesAll||[];if(!ch.length)return '<p class="small">No ownership recorded (e.g. household enterprise).</p>';
 var nd={};nd[target]={id:target,label:name,kind:"entity",d:0};var oo={};ch.forEach(function(c){(oo[c.owned_id]=oo[c.owned_id]||[]).push(c);});
 var fr=[target],d=0,sn={};sn[target]=1;
 while(fr.length&&d<5){var nx=[];fr.forEach(function(id){(oo[id]||[]).forEach(function(c){if(!nd[c.owner_id])nd[c.owner_id]={id:c.owner_id,label:c.owner_name||c.owner_id,kind:c.owner_is_government?"gov":(c.owner_is_resident===false?"foreign":"priv"),d:d+1};if(!sn[c.owner_id]){sn[c.owner_id]=1;nx.push(c.owner_id);}});});fr=nx;d++;}
 var mx=Math.max.apply(null,Object.keys(nd).map(function(k){return nd[k].d;}));var ly={};Object.keys(nd).forEach(function(k){(ly[nd[k].d]=ly[nd[k].d]||[]).push(nd[k]);});
 var W=520,rh=90,bw=150,bh=44,H=(mx+1)*rh+18,ps={};
 for(var i=0;i<=mx;i++){var ar=ly[i]||[],g=W/(ar.length+1);ar.forEach(function(n,j){ps[n.id]=[g*(j+1),H-i*rh-rh/2];});}
 var ln="";ch.forEach(function(c){var a=ps[c.owner_id],b=ps[c.owned_id];if(!a||!b)return;var t=c.ownership_pct+"%"+(c.control_indicator?(" · "+c.control_indicator):"");ln+='<line x1="'+a[0]+'" y1="'+(a[1]+bh/2)+'" x2="'+b[0]+'" y2="'+(b[1]-bh/2)+'" stroke="#aab4c0" stroke-width="1.4" marker-end="url(#ar)"/><text x="'+((a[0]+b[0])/2+4)+'" y="'+((a[1]+b[1])/2)+'" font-size="10" fill="#5a6473">'+esc(t)+'</text>';});
 var cl={entity:"#8a1538",gov:"#7a3b97",foreign:"#b9651b",priv:"#1a8a4f"};var bx="";
 Object.keys(nd).forEach(function(k){var n=nd[k],p=ps[n.id];var lab=n.kind==="entity"?"THIS ENTITY":n.kind.toUpperCase();bx+='<rect x="'+(p[0]-bw/2)+'" y="'+(p[1]-bh/2)+'" width="'+bw+'" height="'+bh+'" rx="8" fill="#fff" stroke="'+cl[n.kind]+'" stroke-width="2"/><text x="'+p[0]+'" y="'+(p[1]-2)+'" font-size="10" text-anchor="middle" fill="#202733">'+esc((n.label||"").slice(0,22))+'</text><text x="'+p[0]+'" y="'+(p[1]+12)+'" font-size="8" text-anchor="middle" fill="'+cl[n.kind]+'">'+lab+'</text>';});
 return '<svg viewBox="0 0 '+W+' '+H+'" width="100%" style="max-height:340px"><defs><marker id="ar" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#aab4c0"/></marker></defs>'+ln+bx+'</svg><div class="legend">■ <span style="color:#8a1538">entity</span> · ■ <span style="color:#7a3b97">government</span> · ■ <span style="color:#1a8a4f">resident private</span> · ■ <span style="color:#b9651b">non-resident</span></div>';}

/* ============================== STATE & NAV ============================== */
var state={view:"home",entId:DATA.enterprises[0].id,studioId:DATA.enterprises[1].id,ruleId:null,filter:"",sheet:0,flowStage:null,apiEp:0,
 upload:{legal_name_en:"New Sample Enterprise",legal_form_code:"JSC",residence:"RES",isic_class:"6419",employment:1200,turnover_qar:8000000000,sales:8000000000,production_costs:5000000000,is_financial:true,is_nonprofit:false,has_premises:true,has_employees:true,has_autonomy:true,jurisdiction:"MAINLAND"},
 uploadEdges:[{owner_name:"State of Qatar",owner_is_government:true,owner_is_resident:true,ownership_pct:55,voting_pct:55,control_indicator:"MAJ-VOTE"},{owner_name:"Public float (QSE)",owner_is_government:false,owner_is_resident:true,ownership_pct:45,voting_pct:45,control_indicator:""}]};
var NAV=[["home","Overview"],["howitworks","How It Works"],["ingest","Data Ingestion"],["studio","Classification Engine"],["registry","Registry"],["profile","Enterprise Profile"],["ownership","Ownership & Groups"],["rules","Rules Engine"],["api","API Integration"],["standards","Standards"],["quality","Quality & Validation"],["uat","UAT & Roadmap"]];
var TITLES={};NAV.forEach(function(n){TITLES[n[0]]=n[1];});
var HELP={
 home:"A working demonstration of NEICS. The classification engine in this page runs entirely in your browser — every result you see is computed live from the rules, not pre-baked.",
 howitworks:"How the platform operates end to end. Click any stage to see what happens there and which standards apply.",
 ingest:"Where data enters the system. Enter or edit an enterprise and its ownership, then run the live engine — exactly what happens when a record is uploaded via the API or a file.",
 studio:"Pick an enterprise and run the engine. The 18 tests evaluate the real rules live and build the classification result step by step.",
 registry:"The Central Statistical Business Register — every resident statistical unit.",
 profile:"A complete enterprise file: ownership network, the live classification, and the explainability trace.",
 ownership:"Effective ownership computed across the whole graph to the Ultimate Controlling Institutional Unit, plus enterprise-group structures.",
 rules:"The database-driven rules. Pick a rule, read its logic, and test it against your own facts — the same evaluator the engine uses.",
 api:"How systems integrate with NEICS. Choose an endpoint and send a request; the response is generated live by the in-browser engine.",
 standards:"The international and national standards every rule is anchored to.",
 quality:"Data quality across the six DAMA dimensions and the VR-001..VR-018 validation library.",
 uat:"Acceptance testing, gap analysis, and the roadmap from staging to production."};

function go(v,x){state.view=v;if(x)for(var k in x)state[k]=x[k];window.scrollTo(0,0);render();}

/* ============================== VIEWS ============================== */
function vHome(){
 var E=DATA.enterprises;var avgq=E.reduce(function(s,e){return s+e.quality.overall_score;},0)/E.length;
 var k=function(n,l){return '<div class="kpi"><div class="n">'+n+'</div><div class="l">'+l+'</div></div>';};
 return '<div class="grid auto" style="margin-bottom:18px">'+k(E.length,"Test enterprises")+k("18","Classification tests")+k(DATA.rules.length,"Database-driven rules")+k(DATA.standards.length,"Standards mapped")+k(avgq.toFixed(2),"Avg quality")+k("33/33","Verdicts verified")+'</div>'+
  '<div class="grid c2"><div class="card"><div class="hd">By institutional sector (SNA)</div><div class="bd">'+bars(countBy(E,"sector"))+'</div></div>'+
  '<div class="card"><div class="hd">Start here</div><div class="bd"><p class="small" style="margin-top:0">This walkthrough shows the engine actually working. Suggested path:</p><ol class="tight">'+
  '<li><a onclick="go(\'howitworks\')">How It Works</a> — the architecture & data flow.</li>'+
  '<li><a onclick="go(\'ingest\')">Data Ingestion</a> — upload/enter an enterprise and classify it live.</li>'+
  '<li><a onclick="go(\'studio\')">Classification Engine</a> — run the 18 tests on any unit.</li>'+
  '<li><a onclick="go(\'api\')">API Integration</a> — see real request/response.</li></ol>'+
  '<button class="btn" onclick="go(\'howitworks\')">Begin walkthrough →</button></div></div></div>';
}

var STAGES={
 src:["Administrative data sources","MoCI commercial register · General Tax Authority · Qatar Central Bank · QFC · QFZA · Qatar Stock Exchange · Ministry of Labour. Each provides authoritative attributes under the Tier 1–4 source hierarchy.","Source hierarchy (QNCS)"],
 ing:["Ingestion & validation","Records arrive by API or file upload (JSON/CSV/XML/SDMX). Entity resolution matches the same unit across sources; the VR-001..VR-018 rules validate every field; missing-data is reported.","UNSD/Eurostat SBR; DAMA DMBOK"],
 reg:["Master register (CSBR)","The golden record — Enterprise > KAU > Establishment, with Legal Units mapped and a persistent statistical identifier (QA-ENT-…). One classification per unit, used by all programmes.","SNA 2025; IR-BR"],
 eng:["Rules engine — 18 tests","Each unit passes through 18 sequenced, database-driven tests. Conflict resolution is first-match-by-priority. No logic is hard-coded; every rule cites a standard.","SNA · GFS · BPM6 · BD4 · ISIC"],
 cls:["Classification & explainability","Outputs: institutional sector, public/private, control, market, size, FDI, special-entity — with a full rule trace, confidence and temporal version.","SNA 2025; OECD BD4"],
 rep:["Repositories & governance","Standards, Metadata (GSIM/SDMX) and Rules repositories; data-quality scoring; immutable audit trail; manual review queue; RBAC.","GSIM · GSBPM · DAMA"],
 out:["Outputs & dissemination","Feeds National Accounts, GFS, FDI, Balance of Payments, Business Demography and SBR — disseminated via API and SDMX.","SNA · GFS · BPM6 · SDMX"]};
function vHow(){
 var node=function(id,stage){var s=STAGES[id];return '<div class="fnode'+(stage?" stage":"")+'" onclick="state.flowStage=\''+id+'\';render()"><div class="ft">'+esc(s[0])+'</div><div class="fd">'+esc(s[1].slice(0,70))+'…</div></div>';};
 var ar='<div class="farrow">▼</div>';
 var flow='<div class="flow">'+
  '<div class="flowrow">'+node("src",1)+'</div>'+ar+
  '<div class="flowrow">'+node("ing",1)+'</div>'+ar+
  '<div class="flowrow">'+node("reg",1)+'</div>'+ar+
  '<div class="flowrow">'+node("eng",1)+'</div>'+ar+
  '<div class="flowrow">'+node("cls",1)+'</div>'+ar+
  '<div class="flowrow">'+node("rep",1)+node("out",1)+'</div></div>';
 var det="";var sid=state.flowStage;
 if(sid&&STAGES[sid]){var s=STAGES[sid];det='<div class="card"><div class="hd">'+esc(s[0])+'</div><div class="bd"><p style="margin-top:0">'+esc(s[1])+'</p><div class="small">Standards: '+esc(s[2])+'</div></div></div>';}
 else{det='<div class="note">Click any stage in the flow to see what happens there.</div>';}
 return '<div class="grid c23"><div class="card"><div class="hd">End-to-end data flow</div><div class="bd">'+flow+'</div></div><div>'+det+
  '<div class="card"><div class="hd">Operating model</div><div class="bd"><div class="kv" style="grid-template-columns:1fr"><div><b>Owned by</b> the National Statistics Office; governed by the Technical Classification Committee (MoCI, GTA, QCB, QFC, QFZA, MoF).</div><div><b>Cadence</b> — quarterly review plus trigger-based reclassification (IPO, M&A, new licence, restructuring).</div><div><b>Confidentiality</b> — entity records protected under the Statistics Law; methodology public.</div></div></div></div></div></div>';
}

function vIngest(){
 var u=state.upload;
 var lf=["JSC","LLC","SOE","GOV","FND","CA","WQ","SP","BR","QFC","FZ","PT","COOP"];
 var fopt=function(id,label,val,opts){return '<div class="field"><label>'+label+'</label><select onchange="state.upload.'+id+'=this.value;render()">'+opts.map(function(o){return '<option '+(String(val)===String(o)?"selected":"")+'>'+o+'</option>';}).join("")+'</select></div>';};
 var fin=function(id,label,val,type){return '<div class="field"><label>'+label+'</label><input type="'+(type||"text")+'" value="'+esc(val)+'" oninput="state.upload.'+id+'=this.'+(type==="number"?"valueAsNumber":"value")+'"/></div>';};
 var chk=function(id,label){return '<label class="small" style="display:inline-flex;gap:6px;align-items:center;margin-right:14px"><input type="checkbox" '+(u[id]?"checked":"")+' onchange="state.upload.'+id+'=this.checked"/> '+label+'</label>';};
 var edrows=state.uploadEdges.map(function(e,i){return '<tr><td><input value="'+esc(e.owner_name)+'" oninput="state.uploadEdges['+i+'].owner_name=this.value" style="border:1px solid var(--line);border-radius:6px;padding:5px;width:150px"/></td>'+
  '<td><input type="number" value="'+e.ownership_pct+'" oninput="state.uploadEdges['+i+'].ownership_pct=this.valueAsNumber;state.uploadEdges['+i+'].voting_pct=this.valueAsNumber" style="border:1px solid var(--line);border-radius:6px;padding:5px;width:64px"/></td>'+
  '<td><label class="small"><input type="checkbox" '+(e.owner_is_government?"checked":"")+' onchange="state.uploadEdges['+i+'].owner_is_government=this.checked"/> gov</label></td>'+
  '<td><label class="small"><input type="checkbox" '+(e.owner_is_resident?"checked":"")+' onchange="state.uploadEdges['+i+'].owner_is_resident=this.checked"/> resident</label></td>'+
  '<td><select onchange="state.uploadEdges['+i+'].control_indicator=this.value" style="border:1px solid var(--line);border-radius:6px;padding:5px">'+["","MAJ-VOTE","GOLDEN","BOARD","CONTRACT","BO-CHAIN"].map(function(o){return '<option '+(e.control_indicator===o?"selected":"")+'>'+o+'</option>';}).join("")+'</select></td>'+
  '<td><button class="btn sm soft" onclick="state.uploadEdges.splice('+i+',1);render()">✕</button></td></tr>';}).join("");
 var form='<div class="card"><div class="hd">1 · Enterprise record (as uploaded via API / file)</div><div class="bd">'+
  fin("legal_name_en","Legal name",u.legal_name_en)+
  '<div class="frow">'+fopt("legal_form_code","Legal form",u.legal_form_code,lf)+fin("isic_class","ISIC Rev.4 class",u.isic_class)+'</div>'+
  '<div class="frow">'+fopt("residence","Residence",u.residence,["RES","NRES","MULTI"])+fopt("jurisdiction","Jurisdiction",u.jurisdiction,["MAINLAND","QFC","QFZA","QSTP"])+'</div>'+
  '<div class="frow">'+fin("employment","Employment (FTE)",u.employment,"number")+fin("turnover_qar","Turnover (QAR)",u.turnover_qar,"number")+'</div>'+
  '<div class="frow">'+fin("sales","Sales (QAR)",u.sales,"number")+fin("production_costs","Production costs (QAR)",u.production_costs,"number")+'</div>'+
  '<div class="field"><label>Flags</label>'+chk("is_financial","financial")+chk("is_nonprofit","non-profit")+chk("has_premises","premises")+chk("has_employees","employees")+chk("has_autonomy","autonomy")+'</div>'+
  '</div></div>'+
  '<div class="card"><div class="hd">2 · Ownership &amp; control</div><div class="bd">'+tbl(["Owner","Equity %","Gov?","Resident?","Control","" ],[]).replace("</table>",edrows+"</table>")+
  '<button class="btn sm soft" style="margin-top:10px" onclick="state.uploadEdges.push({owner_name:\'New owner\',owner_is_government:false,owner_is_resident:true,ownership_pct:0,voting_pct:0,control_indicator:\'\'});render()">+ Add owner</button></div></div>'+
  '<button class="btn" onclick="state.view=\'ingest\';window._runIngest=1;render()">▶ Validate &amp; classify (run engine)</button>';
 var res="";
 if(window._runIngest){
  var inp=Object.assign({},u);
  var edges=state.uploadEdges.map(function(e){return {owner_id:e.owner_name,owner_name:e.owner_name,owned_id:"NEW",ownership_pct:e.ownership_pct||0,voting_pct:e.voting_pct||e.ownership_pct||0,control_indicator:e.control_indicator,owner_is_government:e.owner_is_government,owner_is_resident:e.owner_is_resident,is_ultimate:"Y"};});
  var v=validateInput(inp);
  var oc=classify(buildFacts(inp,edges,"NEW"));
  var vhtml=v.length?v.map(function(x){return '<div style="margin:3px 0">'+sevb(x.sev)+' <span class="small">'+esc(x.rule)+'</span> '+esc(x.msg)+'</div>';}).join(""):'<div class="small" style="color:var(--green)">All checks passed.</div>';
  var trace=oc.trace.filter(function(t){return t.matched;}).map(function(t){return '<tr><td>'+esc(t.test_code)+'</td><td class="mono">'+esc(t.rule_id)+'</td><td>'+Object.keys(t.output).map(function(k){return bdg(t.output[k],"b-green");}).join(" ")+'</td><td class="small">'+esc(t.standard_ref||"")+'</td></tr>';}).join("");
  var r=oc.result;
  res='<div class="card" style="border-color:var(--maroon)"><div class="hd">3 · Live engine output</div><div class="bd">'+
   '<div class="grid c2"><div><div style="font-weight:650;margin-bottom:6px">Validation</div>'+vhtml+
   '<div style="font-weight:650;margin:14px 0 6px">Ownership network</div><div class="svgwrap">'+ownSVG(edges,"NEW",inp.legal_name_en)+'</div></div>'+
   '<div><div class="passport"><div class="top"><div class="nm">'+esc(inp.legal_name_en)+'</div><div class="id">computed live · confidence '+oc.confidence+'</div></div>'+
   [["Institutional sector",r.sector_code],["Public / private",r.public_private],["Control",r.control_flag],["Market",r.market_status],["Size",r.size_class],["FDI",r.fdi_flag],["Special entity",r.special_entity_flag]].map(function(p){return '<div class="r"><span class="k">'+p[0]+'</span><span>'+(p[0]==="Public / private"?pp(p[1]):"<b>"+esc(p[1])+"</b>")+'</span></div>';}).join("")+'</div></div></div>'+
   '<div style="font-weight:650;margin:16px 0 6px">Rules applied (explainability)</div>'+tbl(["Test","Rule","Output","Standard"],[]).replace("</table>",trace+"</table>")+
   '</div></div>';
  window._runIngest=0;
 }
 return form+res;
}

function studioSteps(ent){return ent.trace_cache;}
function vStudio(){
 var e=ent(state.studioId);
 var opts=DATA.enterprises.map(function(x){return '<option value="'+x.id+'" '+(x.id===e.id?"selected":"")+'>'+esc(x.name)+'</option>';}).join("");
 var dims=[["Institutional sector","sector_code"],["Public / private","public_private"],["Effective control","control_flag"],["Market status","market_status"],["Size class","size_class"],["FDI treatment","fdi_flag"],["Special entity","special_entity_flag"]];
 return '<div class="grid c23"><div><div class="card"><div class="hd">Subject enterprise</div><div class="bd">'+
  '<select onchange="state.studioId=this.value;render()" style="width:100%;padding:9px;border:1px solid var(--line);border-radius:8px">'+opts+'</select>'+
  '<div class="kv" style="grid-template-columns:130px 1fr;margin-top:14px"><div class="k">Legal form</div><div>'+esc(e.legal_form)+'</div><div class="k">ISIC</div><div>'+esc(e.isic)+'</div><div class="k">Employment</div><div>'+e.employment+' FTE</div><div class="k">Turnover</div><div>'+money(e.turnover)+'</div><div class="k">Gov ownership</div><div>'+e.ownership.government_pct+'%</div></div>'+
  '<button class="btn" style="margin-top:14px" onclick="runStudio()">▶ Run classification engine</button>'+
  '<div class="svgwrap" style="margin-top:14px">'+ownSVG(edgesOf(e),e.id,e.name)+'</div></div></div>'+
  '<div class="card"><div class="hd">18-test pipeline (live)</div><div class="bd"><div class="timeline" id="stepper"><div class="small">Press <b>Run classification engine</b> to evaluate the rules live.</div></div></div></div></div>'+
  '<div><div class="passport" id="passport"><div class="top"><div class="nm">'+esc(e.name)+'</div><div class="id">'+esc(e.id)+'</div></div>'+
  dims.map(function(p){return '<div class="r"><span class="k">'+p[0]+'</span><span id="pp-'+p[1]+'" class="small">—</span></div>';}).join("")+
  '<div class="r"><span class="k">Confidence</span><span id="pp-conf" class="small">—</span></div></div></div></div>';
}
function runStudio(){
 var e=ent(state.studioId);var oc=classifyEnterprise(e);var stp=document.getElementById("stepper");if(!stp)return;stp.innerHTML="";
 var i=0;
 (function tick(){if(i>=oc.trace.length){var c=document.getElementById("pp-conf");if(c){c.innerHTML='<b style="color:var(--green)">'+oc.confidence+'</b>';}return;}
  var s=oc.trace[i];var d=document.createElement("div");d.className="tstep on"+(s.matched?" fire":"");
  var out=s.matched?Object.keys(s.output).map(function(k){return bdg(s.output[k],"b-green");}).join(" "):'<span class="small">governance / process step</span>';
  d.innerHTML='<div class="bt">'+esc(s.test_code)+'</div><div class="nm">'+esc(s.test_name)+'</div><div style="margin-top:4px">'+out+'</div>'+(s.matched?'<div class="small" style="margin-top:3px">'+esc(s.rule_id)+' · '+esc(s.standard_ref||"")+'</div>':'');
  stp.appendChild(d);d.scrollIntoView({block:"nearest"});
  if(s.matched)Object.keys(s.output).forEach(function(k){var el=document.getElementById("pp-"+k);if(el)el.innerHTML=(k==="public_private")?pp(s.output[k]):"<b>"+esc(s.output[k])+"</b>";});
  i++;setTimeout(tick,Math.max(150,430-i*9));})();
}

function vRegistry(){
 var f=(state.filter||"").toLowerCase();
 var r=DATA.enterprises.filter(function(e){return !f||(e.name+e.id+e.sector+e.public_private).toLowerCase().indexOf(f)>=0;});
 return '<div class="card"><div class="bd"><input placeholder="Search name, ID, sector…" value="'+esc(state.filter)+'" oninput="state.filter=this.value;render()" style="width:100%;max-width:380px;padding:9px 12px;border:1px solid var(--line);border-radius:8px;margin-bottom:14px"/>'+
  tbl(["Enterprise","Sector","Public/Private","Size","Control","Quality"],r.map(function(e){return ['<b style="cursor:pointer" onclick="go(\'profile\',{entId:\''+e.id+'\'})">'+esc(e.name)+'</b>',esc(e.sector),pp(e.public_private),esc(e.size),bdg(e.control),'<span style="color:'+qcol(e.quality.overall_score)+';font-weight:700">'+e.quality.overall_score+'</span>'];}))+
  '<div class="small" style="margin-top:10px">'+r.length+' of '+DATA.enterprises.length+' enterprises</div></div></div>';
}
function vProfile(){
 var e=ent(state.entId),o=e.ownership,oc=classifyEnterprise(e);
 var appl=oc.trace.filter(function(t){return t.matched;}).map(function(a){return '<tr><td>'+esc(a.test_code)+'</td><td class="mono">'+esc(a.rule_id)+'</td><td>'+Object.keys(a.output).map(function(k){return bdg(a.output[k],"b-green");}).join(" ")+'</td><td class="small">'+esc(a.standard_ref||"")+'</td><td class="small">'+esc(a.rationale||"")+'</td></tr>';}).join("");
 return '<select onchange="state.entId=this.value;render()" style="margin-bottom:14px;padding:9px;border:1px solid var(--line);border-radius:8px">'+DATA.enterprises.map(function(x){return '<option value="'+x.id+'" '+(x.id===e.id?"selected":"")+'>'+esc(x.name)+'</option>';}).join("")+'</select>'+
  '<div class="card"><div class="bd"><div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center"><div style="flex:1;min-width:200px"><div style="font-size:18px;font-weight:700">'+esc(e.name)+'</div><div class="mono small">'+esc(e.id)+' · LEI '+esc(e.lei||"—")+'</div></div><div>'+bdg(e.sector)+" "+pp(e.public_private)+" "+bdg(e.size)+'</div></div></div></div>'+
  '<div class="grid c2"><div class="card"><div class="hd">Ownership network</div><div class="bd"><div class="svgwrap">'+ownSVG(edgesOf(e),e.id,e.name)+'</div></div></div>'+
  '<div class="card"><div class="hd">Control intelligence</div><div class="bd"><div class="kv" style="grid-template-columns:1fr auto"><div class="k">Effective government ownership</div><div><b>'+o.government_pct+'%</b></div><div class="k">Government voting</div><div>'+o.government_voting+'%</div><div class="k">Foreign ownership</div><div>'+o.foreign_pct+'%</div><div class="k">Government control</div><div>'+(o.government_control?"Yes":"No")+'</div><div class="k">Ultimate controlling unit</div><div>'+esc((o.uci||{}).uci_name||"—")+'</div></div></div></div></div>'+
  '<div class="card"><div class="hd">Live classification &amp; explainability (confidence '+oc.confidence+')</div><div class="bd">'+tbl(["Test","Rule","Output","Standard","Rationale"],[]).replace("</table>",appl+"</table>")+'</div></div>';
}

function vOwnership(){
 var swf=ent("QA-ENT-20260000025"),bank=ent("QA-ENT-20260000002");
 var ex="";[bank,swf].forEach(function(x){if(x)ex+='<div class="card"><div class="hd">'+esc(x.name)+'</div><div class="bd"><div class="svgwrap">'+ownSVG(edgesOf(x),x.id,x.name)+'</div></div></div>';});
 var gt="";DATA.groups.forEach(function(g){var head=ent(g.domestic_head);var mem=g.members.map(function(m){var me=ent(m);var kind=me&&me.public_private.indexOf("PUB")===0?"gov":(me&&me.public_private==="FCC"?"foreign":"priv");return '<div class="lvl"><span class="gnode '+kind+'">'+esc(me?me.name:m)+' <span class="small">· '+esc(me?me.sector:"")+'</span></span></div>';}).join("");
  gt+='<div class="card"><div class="hd">'+esc(g.name)+'</div><div class="bd"><span class="gnode" style="border-color:#444">'+esc(g.gup)+' <span class="small">· global ultimate parent</span></span><div class="lvl"><span class="gnode entity">'+esc(head?head.name:g.domestic_head)+' <span class="small">· domestic head</span></span>'+mem+'</div><p class="small" style="margin-top:8px">'+esc(g.notes)+'</p></div></div>';});
 return '<div class="grid c2">'+ex+'</div>'+gt;
}

function vRules(){
 var cur=state.ruleId?DATA.rules.filter(function(r){return r.rule_id===state.ruleId;})[0]:DATA.rules[0];
 var list=DATA.rules.map(function(r){return '<tr class="row" onclick="state.ruleId=\''+r.rule_id+'\';render()"><td class="mono">'+esc(r.rule_id)+'</td><td>'+esc(r.name)+'</td><td>'+bdg(r.test_code)+'</td></tr>';}).join("");
 var facts=sugg(cur);
 return '<div class="grid c23"><div class="card"><div class="hd">Rules repository ('+DATA.rules.length+')</div><div class="bd" style="max-height:520px;overflow:auto">'+tbl(["ID","Name","Test"],[]).replace("</table>",list+"</table>")+'</div></div>'+
  '<div><div class="card"><div class="hd">'+esc(cur.rule_id)+' — '+esc(cur.name)+'</div><div class="bd"><div class="kv" style="grid-template-columns:110px 1fr"><div class="k">Test</div><div>'+esc(cur.test_code)+'</div><div class="k">Standard</div><div>'+esc(cur.standard_ref)+'</div><div class="k">Rationale</div><div>'+esc(cur.rationale)+'</div></div>'+
  '<div class="small" style="margin:10px 0 4px">Logic</div><pre class="code">'+esc(JSON.stringify(cur.logic,null,1))+'</pre><div class="small">Output: <span class="mono">'+esc(JSON.stringify(cur.output))+'</span></div></div></div>'+
  '<div class="card"><div class="hd">Rule tester (live)</div><div class="bd"><div class="small" style="margin-bottom:6px">Edit the facts and evaluate — same engine.</div><textarea id="rtf" style="width:100%;min-height:120px;border:1px solid var(--line);border-radius:8px;padding:9px" class="mono">'+esc(JSON.stringify(facts,null,1))+'</textarea><div style="margin-top:8px"><button class="btn sm" onclick="testRule(\''+cur.rule_id+'\')">▶ Evaluate</button> <span id="rtres"></span></div></div></div></div></div>';
}
function sugg(r){var f={};(function w(c){if(!c)return;if(c.all)c.all.forEach(w);else if(c.any)c.any.forEach(w);else if(c.not)w(c.not);else if(c.op){if(c.op==="eq"||c.op==="in")f[c.field]=Array.isArray(c.value)?c.value[0]:c.value;else if(["gt","gte","lt","lte"].indexOf(c.op)>=0)f[c.field]=c.value;else if(c.op==="truthy")f[c.field]=true;else if(c.op==="exists")f[c.field]="…";}})(r.logic);return f;}
function testRule(id){var r=DATA.rules.filter(function(x){return x.rule_id===id;})[0];var f;try{f=JSON.parse(document.getElementById("rtf").value);}catch(e){document.getElementById("rtres").innerHTML='<span style="color:var(--red)">Invalid JSON</span>';return;}var m=evalCond(r.logic,f);document.getElementById("rtres").innerHTML=m?'<span style="color:var(--green)">✔ MATCH → '+esc(JSON.stringify(r.output))+'</span>':'<span style="color:var(--red)">✘ no match</span>';}

var ENDPOINTS=[
 ["POST","/api/enterprises/{id}/classify","Run the 18-test classification for an enterprise"],
 ["GET","/api/enterprises/{id}/explain","Full explainability for the current classification"],
 ["GET","/api/dashboard","Register KPIs and breakdowns"],
 ["GET","/api/enterprises/{id}/profile","Master data + ownership + quality"],
 ["POST","/api/rules/{id}/test","Evaluate a rule against a fact set"]];
function vApi(){
 var ep=ENDPOINTS[state.apiEp];var e=ent(state.studioId);
 var list=ENDPOINTS.map(function(x,i){return '<tr class="row" onclick="state.apiEp='+i+';render()"><td>'+bdg(x[0],x[0]==="GET"?"b-blue":"b-green")+'</td><td class="mono">'+esc(x[1])+'</td></tr>';}).join("");
 // build a real response from the engine
 var resp;
 var oc=classifyEnterprise(e);
 if(ep[1].indexOf("classify")>=0){resp={enterprise_id:e.id,methodology_version:"1.0.0",confidence:oc.confidence,result:oc.result};}
 else if(ep[1].indexOf("explain")>=0){resp={enterprise_id:e.id,confidence:oc.confidence,applied_rules:oc.trace.filter(function(t){return t.matched;}).map(function(t){return {test:t.test_code,rule_id:t.rule_id,output:t.output,standard_ref:t.standard_ref};})};}
 else if(ep[1].indexOf("dashboard")>=0){resp={total_enterprises:DATA.enterprises.length,by_sector:countBy(DATA.enterprises,"sector"),by_public_private:countBy(DATA.enterprises,"public_private")};}
 else if(ep[1].indexOf("profile")>=0){resp={enterprise:{id:e.id,name:e.name,sector_code:e.sector,public_private:e.public_private},ownership:{government_pct:e.ownership.government_pct,uci:(e.ownership.uci||{}).uci_name},quality:e.quality.overall_score};}
 else{resp={rule_id:"R-T07-030",matched:true,output:{market_status:"MARKET"}};}
 var path=ep[1].replace("{id}",e.id);
 return '<div class="help">Choose an endpoint and an enterprise. The response below is generated live by the in-browser engine — the same payload the FastAPI backend returns.</div>'+
  '<div class="grid c23"><div class="card"><div class="hd">Endpoints</div><div class="bd">'+tbl(["Method","Path"],[]).replace("</table>",list+"</table>")+'</div></div>'+
  '<div><div class="card"><div class="hd">Request</div><div class="bd"><select onchange="state.studioId=this.value;render()" style="padding:8px;border:1px solid var(--line);border-radius:8px;margin-bottom:10px;width:100%">'+DATA.enterprises.map(function(x){return '<option value="'+x.id+'" '+(x.id===e.id?"selected":"")+'>'+esc(x.name)+'</option>';}).join("")+'</select>'+
  '<pre class="code">'+esc(ep[0]+" "+path)+'\nAuthorization: Bearer &lt;jwt&gt;</pre></div></div>'+
  '<div class="card"><div class="hd">Response (live)</div><div class="bd"><pre class="code">HTTP 200 OK\n'+esc(JSON.stringify(resp,null,2))+'</pre></div></div></div></div>';
}

function vStandards(){return DATA.standards.map(function(s){var cs=s.concepts.map(function(c){return '<tr><td>'+esc(c.concept)+'</td><td>'+esc(c.definition)+'</td></tr>';}).join("");return '<div class="card"><div class="hd">'+esc(s.code)+' — '+esc(s.name)+'</div><div class="bd"><div class="small">'+esc(s.issuer)+' · '+esc(s.edition)+' · '+esc(s.domains)+'</div><p>'+esc(s.description)+'</p>'+(cs?tbl(["Concept","Definition"],[]).replace("</table>",cs+"</table>"):"")+'</div></div>';}).join("");}

function vQuality(){var E=DATA.enterprises,ds=["completeness","validity","consistency","uniqueness","accuracy","timeliness","overall_score"],ag={};ds.forEach(function(d){ag[d]=E.reduce(function(s,e){return s+e.quality[d];},0)/E.length;});
 var all=[];E.forEach(function(e){e.exceptions.forEach(function(x){all.push([e.name,x]);});});
 return '<div class="grid auto" style="margin-bottom:16px">'+ds.map(function(d){return '<div class="kpi"><div class="n" style="color:'+qcol(ag[d])+'">'+ag[d].toFixed(2)+'</div><div class="l">'+d.replace("_"," ")+'</div></div>';}).join("")+'</div>'+
  '<div class="card"><div class="hd">Validation exceptions (VR-001..VR-018)</div><div class="bd">'+tbl(["Enterprise","Rule","Severity","Message"],all.map(function(p){return [esc(p[0]),'<span class="mono">'+esc(p[1].rule_id)+'</span>',sevb(p[1].severity),esc(p[1].message)];}))+'</div></div>';
}

function vUat(){var c=DATA.uat,g=DATA.gap;
 var box=function(t,a){return '<div class="card"><div class="hd">'+t+'</div><div class="bd"><ul class="tight">'+a.map(function(x){return "<li>"+esc(x)+"</li>";}).join("")+'</ul></div></div>';};
 var rag=tbl(["Dimension","Status","Notes"],DATA.readiness.map(function(r){return [esc(r[0]),'<span class="rag '+r[1].replace(/[^A-Za-z]/g,"")+'">'+esc(r[1])+'</span>',esc(r[2])];}));
 return '<div class="grid auto" style="margin-bottom:16px"><div class="kpi"><div class="n">100+</div><div class="l">UAT cases</div></div><div class="kpi"><div class="n" style="color:var(--green)">33/33</div><div class="l">Verdicts</div></div><div class="kpi"><div class="n" style="color:var(--green)">40/40</div><div class="l">Rules verified</div></div><div class="kpi"><div class="n" style="color:var(--green)">18/18</div><div class="l">Validation rules</div></div></div>'+
  '<div class="card"><div class="hd">Representative acceptance tests</div><div class="bd">'+tbl(["Test ID","Area","Description","Expected","Status"],c.map(function(r){return ['<span class="mono">'+esc(r[0])+'</span>',esc(r[1]),esc(r[2]),esc(r[3]),bdg(r[4],"b-green")];}))+'</div></div>'+
  '<div class="grid c2">'+box("✔ Fully implemented",g.implemented)+box("◑ Partially implemented",g.partial)+'</div>'+
  '<div class="grid c2">'+box("→ Future enhancements",g.future)+box("⚠ Production-readiness gaps",g.production_gaps)+'</div>'+
  '<div class="card"><div class="hd">Production readiness — Development → Staging → Pilot → Production</div><div class="bd">'+rag+'<div class="note" style="margin-top:12px"><b>Recommendation:</b> methodology and data-governance readiness are <span class="rag Green">Green</span>. Proceed to a controlled <b>pilot</b> on the largest 100 enterprises after security hardening and one administrative-source integration.</div></div></div>';
}

var VIEWS={home:vHome,howitworks:vHow,ingest:vIngest,studio:vStudio,registry:vRegistry,profile:vProfile,ownership:vOwnership,rules:vRules,api:vApi,standards:vStandards,quality:vQuality,uat:vUat};
function render(){
 try{
  document.getElementById("nav").innerHTML=NAV.map(function(n){return '<button class="'+(state.view===n[0]?"active":"")+'" onclick="go(\''+n[0]+'\')">'+esc(n[1])+'</button>';}).join("");
  var help=HELP[state.view]?'<div class="help">'+HELP[state.view]+'</div>':"";
  document.getElementById("content").innerHTML='<div class="h-page">'+esc(TITLES[state.view]||"")+'</div><div class="h-sub">National Enterprise Intelligence &amp; Classification System · State of Qatar · National Statistics Office</div>'+help+(VIEWS[state.view]||vHome)();
 }catch(err){
  document.getElementById("content").innerHTML='<div class="card"><div class="bd"><b>Display error.</b> <span class="small">'+esc(err&&err.message)+'</span><div style="margin-top:8px"><button class="btn sm" onclick="state.view=\'home\';render()">Back to overview</button></div></div></div>';
 }
}
render();
</script>
</body>
</html>
"""
