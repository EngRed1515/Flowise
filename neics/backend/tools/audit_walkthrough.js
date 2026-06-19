/* Headless audit of the self-contained platform HTML.
   Stubs a minimal DOM, loads the embedded <script>, then exercises the
   classification engine (vs backend expected verdicts) and every view. */
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const HTML = fs.readFileSync(process.argv[2] || path.join(__dirname, '../../Qatar_Enterprise_Classification_Platform.html'), 'utf8');
const expected = JSON.parse(fs.readFileSync(path.join(__dirname, '../../data/uat_expected.json'), 'utf8'));

// Pull the big inline <script> that contains DATA + engine + views (the last one).
const scripts = [...HTML.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
const code = scripts.sort((a, b) => b.length - a.length)[0];

function makeEl() {
  const el = {
    _html: '', children: [],
    set innerHTML(v) { this._html = String(v); },
    get innerHTML() { return this._html; },
    style: {}, classList: { add(){}, remove(){}, contains(){return false;} },
    appendChild(c){ this.children.push(c); }, scrollIntoView(){},
    setAttribute(){}, addEventListener(){}, value: '', focus(){},
    querySelector(){ return makeEl(); }, querySelectorAll(){ return []; },
  };
  return el;
}
const registry = {};
const document = {
  getElementById(id){ return registry[id] || (registry[id] = makeEl()); },
  createElement(){ return makeEl(); },
  querySelector(){ return makeEl(); }, querySelectorAll(){ return []; },
  addEventListener(){},
};
const window = { innerWidth: 1400, scrollTo(){}, addEventListener(){}, matchMedia(){return{matches:false,addListener(){}};} };
const ctx = {
  document, window, console,
  setTimeout: () => 0, clearTimeout(){}, alert(){}, navigator:{}, location:{},
  Date, Math, JSON, Object, Array, String, Number, Boolean, RegExp, parseInt, parseFloat, isNaN,
};
ctx.globalThis = ctx; ctx.self = ctx;
vm.createContext(ctx);
vm.runInContext(code, ctx, { timeout: 10000 });

let fail = 0;
function ok(c, m){ if(!c){ console.log('  ✗ ' + m); fail++; } }

// ---- Engine vs backend ----
const DATA = ctx.DATA;
console.log('Loaded DATA: enterprises=' + DATA.enterprises.length + ' rules=' + DATA.rules.length + ' roles=' + Object.keys(DATA.roles).length + ' groups=' + DATA.groups.length);

let match = 0, tot = 0;
DATA.enterprises.forEach(e => {
  const exp = expected[e.id];
  if (!exp) return;
  tot++;
  const inp = Object.assign({ legal_name_en: e.name }, e.inp);
  const edges = ctx.edgesOf(e).map(x => Object.assign({}, x, { owned_id: e.id, owner_id: x.owner_id || x.owner_name, is_ultimate: 'Y' }));
  const f = ctx.buildFacts(inp, edges, e.id);
  const r = ctx.classify(f).result;
  const dims = ['sector_code', 'public_private'];
  const good = dims.every(d => !exp[d] || String(r[d]) === String(exp[d]));
  if (good) match++;
  else console.log('  ✗ ' + e.id + ' got ' + r.sector_code + '/' + r.public_private + ' exp ' + exp.sector_code + '/' + exp.public_private);
});
console.log('Engine vs backend: ' + match + '/' + tot + (match === tot ? '  ✓' : '  ✗'));
ok(match === tot, 'engine mismatch');

// ---- Every view renders non-trivially ----
const views = Object.keys(ctx.VIEWS);
console.log('Views: ' + views.length);
views.forEach(v => {
  try {
    ctx.state.view = v;
    const html = ctx.VIEWS[v]();
    ok(typeof html === 'string' && html.length > 80, 'view ' + v + ' too small (' + (html||'').length + ')');
  } catch (err) { ok(false, 'view ' + v + ' threw: ' + err.message); }
});

// ---- Interactions ----
function tryRun(label, fn){ try { fn(); console.log('  ✓ ' + label); } catch(err){ ok(false, label + ' threw: ' + err.message); } }

tryRun('loadDemo + runEngine', () => {
  ctx.loadDemo(DATA.enterprises[0].id);
  ctx.runEngine();
  ok(registry.engresult._html.length > 2000, 'engresult small');
});
tryRun('submitReview (Classifier can)', () => {
  ctx.state.role = 'Classifier';
  const before = ctx.state.queue.length;
  ctx.submitReview();
  ok(ctx.state.queue.length === before + 1, 'queue did not grow');
});
tryRun('reviewAct approve (Reviewer)', () => {
  ctx.state.role = ctx.DATA.roles['Reviewer'] ? 'Reviewer' : Object.keys(ctx.DATA.roles).find(r=>ctx.DATA.roles[r].includes('review:write'))||'Administrator';
  ctx.reviewAct(0, 'approve');
  ok(ctx.state.queue[0].status.indexOf('APPROVED') >= 0, 'not approved (role=' + ctx.state.role + ')');
});
tryRun('batchDemo + exportCSV', () => { ctx.batchDemo && ctx.batchDemo(); ctx.exportCSV && ctx.exportCSV(); });
tryRun('scenarioPlay', () => { ctx.scenarioPlay && ctx.scenarioPlay(0); });
tryRun('simRun', () => { ctx.state.view='simulate'; ctx.simRun(); });
tryRun('ruleTest', () => { if(ctx.ruleTest){ ctx.state.ruleId=(DATA.rules[0]||{}).rule_id; ctx.ruleTest(); } });
tryRun('role gating: Viewer cannot submit', () => {
  const viewer = Object.keys(DATA.roles).find(r => !DATA.roles[r].includes('*') && !DATA.roles[r].includes('classify:run'));
  if (viewer) { ctx.state.role = viewer; const before = ctx.state.queue.length; ctx.submitReview(); ok(ctx.state.queue.length === before, viewer + ' should not submit'); }
});

console.log(fail === 0 ? '\nAUDIT PASSED' : '\nAUDIT FAILED (' + fail + ' issues)');
process.exit(fail === 0 ? 0 : 1);
