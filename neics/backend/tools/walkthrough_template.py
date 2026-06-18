"""HTML shell + CSS for the NEICS walkthrough.

This version is STATIC-FIRST: build_walkthrough.py renders every section to HTML in
Python and injects it at {{CONTENT}}. All content is real HTML/CSS (no dependency on
JavaScript to render), so it displays correctly on any browser / device. A tiny,
optional progressive-enhancement script adds single-screen navigation; if it fails,
the page degrades gracefully to a clean, fully-readable long document.
"""

HTML_SHELL = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>NEICS — National Enterprise Intelligence & Classification System</title>
<style>
:root{
 --maroon:#8a1538;--maroon-d:#6b0f2b;--gold:#b08d57;--ink:#202733;--ink2:#3d4757;
 --muted:#697587;--line:#e6e9ee;--line2:#f0f2f5;--bg:#eef1f5;--surface:#fff;--surface2:#f7f9fc;
 --blue:#1d6fb8;--blueb:#e9f2fb;--green:#1a8a4f;--greenb:#e8f5ee;--amber:#946610;--amberb:#fbf1da;
 --red:#bf372a;--redb:#fbe9e7;--purple:#7a3b97;--purpleb:#f4eafa;--teal:#127a6c;--tealb:#e3f3f0;--grayb:#eef1f4;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:64px}
body{margin:0;font-family:"Segoe UI",-apple-system,BlinkMacSystemFont,Roboto,Helvetica,Arial,sans-serif;
 color:var(--ink);background:var(--bg);font-size:15px;line-height:1.6;-webkit-text-size-adjust:100%}
img{max-width:100%}
a{color:var(--maroon);text-decoration:none}
/* Top bar */
.topbar{position:sticky;top:0;z-index:100;background:var(--maroon);color:#fff;display:flex;align-items:center;
 gap:12px;padding:10px 18px}
.topbar .logo{width:32px;height:32px;border-radius:7px;background:#fff;color:var(--maroon);font-weight:800;
 display:flex;align-items:center;justify-content:center}
.topbar b{font-size:15px;letter-spacing:.3px}
.topbar small{opacity:.85;font-size:11px}
.topbar .sp{flex:1}
.topbar .stg{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.32);padding:4px 11px;
 border-radius:20px;font-size:11px;font-weight:600}
/* Nav (sticky tab bar) */
.nav{position:sticky;top:52px;z-index:90;background:var(--surface);border-bottom:1px solid var(--line);
 box-shadow:0 1px 3px rgba(0,0,0,.04);overflow-x:auto;white-space:nowrap;-webkit-overflow-scrolling:touch}
.nav .inner{display:flex;gap:2px;padding:0 10px;max-width:1180px;margin:0 auto}
.nav a{display:inline-block;padding:13px 14px;font-size:13px;color:var(--ink2);font-weight:600;
 border-bottom:3px solid transparent}
.nav a:hover{color:var(--maroon)}
.nav a.active{color:var(--maroon);border-bottom-color:var(--maroon)}
/* Hero */
.hero{background:linear-gradient(135deg,#8a1538,#5c0e25);color:#fff;padding:46px 22px}
.hero .wrap{max-width:1100px;margin:0 auto}
.hero .crest{font-size:12px;letter-spacing:1.5px;text-transform:uppercase;opacity:.8}
.hero h1{font-size:30px;margin:10px 0 6px;font-weight:750;line-height:1.2}
.hero p{font-size:16px;opacity:.92;margin:0;max-width:760px}
.hero .stats{display:flex;gap:14px;flex-wrap:wrap;margin-top:24px}
.hero .stat{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);border-radius:11px;
 padding:13px 18px;min-width:120px}
.hero .stat .n{font-size:24px;font-weight:750}
.hero .stat .l{font-size:11.5px;opacity:.85;margin-top:2px}
/* Sections */
.section{padding:34px 22px;border-bottom:1px solid var(--line)}
.section:nth-of-type(even){background:var(--surface2)}
.section .wrap{max-width:1100px;margin:0 auto}
.shead{display:flex;align-items:center;gap:12px;margin-bottom:6px}
.shead .num{width:30px;height:30px;border-radius:8px;background:var(--maroon);color:#fff;font-weight:700;
 display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0}
.shead h2{font-size:22px;margin:0;font-weight:700}
.sdesc{color:var(--muted);margin:0 0 20px;font-size:14px;max-width:820px}
/* Grid + cards */
.grid{display:grid;gap:16px}
.cols-3{grid-template-columns:repeat(3,1fr)}.cols-2{grid-template-columns:1fr 1fr}
.cols-23{grid-template-columns:3fr 2fr}.auto{grid-template-columns:repeat(auto-fit,minmax(190px,1fr))}
@media(max-width:880px){.cols-3,.cols-2,.cols-23{grid-template-columns:1fr}}
.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;box-shadow:0 1px 2px rgba(17,24,39,.05)}
.card>.hd{padding:14px 18px;border-bottom:1px solid var(--line2);font-weight:650;display:flex;align-items:center;gap:9px}
.card>.hd::before{content:"";width:8px;height:18px;border-radius:3px;background:var(--maroon)}
.card>.bd{padding:18px}
.kpi{background:var(--surface);border:1px solid var(--line);border-top:3px solid var(--maroon);border-radius:12px;
 padding:18px;box-shadow:0 1px 2px rgba(17,24,39,.05)}
.kpi .n{font-size:30px;font-weight:780;line-height:1}.kpi .l{color:var(--muted);font-size:12.5px;margin-top:6px}
/* Badges */
.bdg{display:inline-block;padding:3px 10px;border-radius:14px;font-size:11.5px;font-weight:650;white-space:nowrap}
.b-blue{background:var(--blueb);color:var(--blue)}.b-green{background:var(--greenb);color:var(--green)}
.b-purple{background:var(--purpleb);color:var(--purple)}.b-amber{background:var(--amberb);color:var(--amber)}
.b-red{background:var(--redb);color:var(--red)}.b-teal{background:var(--tealb);color:var(--teal)}.b-gray{background:var(--grayb);color:#4b5563}
/* Tables */
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--line);border-radius:10px}
table.t{width:100%;border-collapse:collapse;font-size:13.5px;background:var(--surface)}
table.t th,table.t td{text-align:left;padding:11px 13px;border-bottom:1px solid var(--line2)}
table.t th{background:var(--surface2);color:var(--muted);font-size:10.5px;text-transform:uppercase;letter-spacing:.6px;font-weight:700}
table.t tr:last-child td{border-bottom:0}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px}
.muted{color:var(--muted)}.small{font-size:12.5px;color:var(--muted)}
.kv{display:grid;grid-template-columns:200px 1fr;gap:9px 18px;font-size:14px}
.kv .k{color:var(--muted)}
@media(max-width:620px){.kv{grid-template-columns:1fr;gap:2px}.kv .k{margin-top:8px;font-weight:600}}
.bar{height:10px;background:var(--line2);border-radius:6px;overflow:hidden}.bar>span{display:block;height:100%}
.barrow{display:grid;grid-template-columns:190px 1fr 46px;gap:12px;align-items:center;margin:9px 0;font-size:13px}
@media(max-width:620px){.barrow{grid-template-columns:120px 1fr 38px}}
/* Timeline (classification studio) */
.timeline{border-left:3px solid var(--line);margin-left:14px;padding-left:22px}
.tstep{position:relative;margin-bottom:14px;background:var(--surface);border:1px solid var(--line);
 border-radius:10px;padding:13px 15px;box-shadow:0 1px 2px rgba(17,24,39,.04)}
.tstep.fire{border-color:var(--maroon)}
.tstep::before,.tstep::after{}
.tstep .badge-test{position:absolute;left:-34px;top:14px;width:26px;height:26px;border-radius:50%;
 background:var(--maroon);color:#fff;font-size:10px;font-weight:700;display:flex;align-items:center;justify-content:center;border:3px solid var(--surface2)}
.tstep.skip .badge-test{background:#c4ccd6}
.tstep .nm{font-weight:650;font-size:13.5px}
/* Passport */
.passport{border:1px solid var(--line);border-radius:13px;overflow:hidden;box-shadow:0 2px 8px rgba(17,24,39,.08)}
.passport .top{background:linear-gradient(135deg,#8a1538,#5c0e25);color:#fff;padding:16px 18px}
.passport .top .nm{font-weight:700;font-size:15px}.passport .top .id{font-size:11px;opacity:.85}
.passport .r{display:flex;justify-content:space-between;align-items:center;padding:11px 18px;border-bottom:1px solid var(--line2);font-size:13.5px}
.passport .r:last-child{border-bottom:0}.passport .r .k{color:var(--muted)}
/* Ownership svg */
.svgwrap{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:10px;overflow:auto}
.legend{font-size:11.5px;color:var(--muted);margin-top:8px}
/* Group tree */
.gnode{display:inline-block;border:1.5px solid var(--line);border-radius:9px;padding:7px 13px;margin:5px;background:#fff}
.lvl{padding-left:22px;border-left:2px dashed #d6dde4;margin-left:18px}
.gnode.gov{border-color:var(--purple)}.gnode.foreign{border-color:#b9651b}.gnode.entity{border-color:var(--maroon)}.gnode.priv{border-color:var(--green)}
.note{background:#fbfaf6;border:1px solid #ece4d2;border-radius:10px;padding:13px 15px;font-size:13.5px}
ul.tight{margin:6px 0;padding-left:20px}ul.tight li{margin:6px 0}
.rag{font-weight:700}.rag.Green{color:var(--green)}.rag.Amber{color:var(--amber)}.rag.Red,.rag.RedAmber{color:var(--red)}.rag.AmberGreen{color:#6e861b}
.foot{padding:26px 22px;text-align:center;color:var(--muted);font-size:12.5px;background:var(--surface)}
/* progressive single-screen mode */
body.app .section{display:none}
body.app .section.shown{display:block}
</style>
</head>
<body>
<div class="topbar"><div class="logo">N</div><div><b>NEICS</b> <small>· State of Qatar · NSO</small></div><span class="sp"></span><span class="stg">STAGING / UAT</span></div>
<div class="nav"><div class="inner" id="navinner">{{NAV}}</div></div>
{{CONTENT}}
<div class="foot">NEICS — National Enterprise Intelligence &amp; Classification System · Staging / UAT walkthrough · State of Qatar, National Statistics Office · Generated {{GENERATED}}</div>
<script>
/* Progressive enhancement only: show one section at a time with the top nav.
   If anything here fails, the page remains a fully-readable long document. */
try{
 var secs=[].slice.call(document.querySelectorAll('.section'));
 var links=[].slice.call(document.querySelectorAll('.nav a'));
 if(secs.length&&links.length){
  document.body.classList.add('app');
  function show(id){secs.forEach(function(s){s.classList.toggle('shown',s.id===id);});
   links.forEach(function(l){l.classList.toggle('active',l.getAttribute('href')==='#'+id);});
   window.scrollTo(0,0);}
  links.forEach(function(l){l.addEventListener('click',function(e){e.preventDefault();show(l.getAttribute('href').slice(1));});});
  show(secs[0].id);
 }
}catch(err){/* graceful: long-document fallback */}
</script>
</body>
</html>
"""
