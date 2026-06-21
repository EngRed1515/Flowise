/* NPC Qatar LMS — premium mockup interactions (no backend) */

/* ---------- Language (EN / AR + RTL) ---------- */
function setLang(lang){
  const html = document.documentElement;
  html.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
  html.setAttribute('lang', lang);
  document.querySelectorAll('.lang button').forEach(b => b.classList.toggle('active', b.dataset.lang === lang));
  localStorage.setItem('lms_lang', lang);
}
document.addEventListener('click', e => {
  const b = e.target.closest('.lang button');
  if (b) setLang(b.dataset.lang);
});

/* ---------- Theme (light / dark) ---------- */
function setTheme(t){
  document.documentElement.setAttribute('data-theme', t);
  localStorage.setItem('lms_theme', t);
  const fab = document.querySelector('.fab.theme');
  if (fab) fab.textContent = t === 'dark' ? '☀️' : '🌙';
}
function toggleTheme(){ setTheme(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'); }

/* ---------- Floating controls + mobile menu ---------- */
function injectControls(){
  // theme FAB (once)
  if (!document.querySelector('.fab-stack')){
    const stack = document.createElement('div');
    stack.className = 'fab-stack';
    const theme = document.createElement('button');
    theme.className = 'fab theme'; theme.title = 'Toggle theme';
    theme.onclick = toggleTheme;
    stack.appendChild(theme);
    document.body.appendChild(stack);
  }
  // scrim (once)
  if (!document.querySelector('.scrim')){
    const s = document.createElement('div'); s.className = 'scrim';
    s.onclick = () => { document.querySelectorAll('.sidebar.open').forEach(sb => sb.classList.remove('open')); s.style.display='none'; };
    document.body.appendChild(s);
  }
  // menu buttons in app topbars
  document.querySelectorAll('.topbar').forEach(tb => {
    if (tb.querySelector('.menu-btn')) return;
    const app = tb.closest('.app'); if (!app) return;
    const btn = document.createElement('button');
    btn.className = 'menu-btn'; btn.innerHTML = '☰';
    btn.onclick = () => {
      const sb = app.querySelector('.sidebar');
      sb.classList.toggle('open');
      document.querySelector('.scrim').style.display = sb.classList.contains('open') ? 'block' : 'none';
    };
    tb.insertBefore(btn, tb.firstChild);
  });
}

/* ---------- Scroll reveal + animated stats ---------- */
function tagReveals(scope){
  scope.querySelectorAll('.card, .feature, .course, .stat-strip > div').forEach((el, i) => {
    if (el.closest('.sidebar, .topbar, .chat')) return;
    if (el.hasAttribute('data-reveal')) return;
    el.setAttribute('data-reveal', '');
    el.style.transitionDelay = ((i % 6) * 60) + 'ms';
  });
}
function prepStats(scope){
  scope.querySelectorAll('.kpi .n, .stat-strip .n').forEach(el => {
    if (el.dataset.count) return;
    el.dataset.count = el.textContent.trim();
    el.textContent = el.textContent.replace(/[\d]/g, '0');
  });
  scope.querySelectorAll('.bar > i').forEach(i => {
    if (i.dataset.w) return;
    i.dataset.w = i.style.width || getComputedStyle(i).width;
    i.style.width = '0';
  });
  scope.querySelectorAll('.ring').forEach(r => {
    if (r.dataset.p) return;
    r.dataset.p = r.style.getPropertyValue('--p').trim() || '0';
    r.style.setProperty('--p', '0');
  });
}
function animateCount(el){
  const raw = el.dataset.count; const m = raw.match(/^([^\d]*)([\d.,]+)(.*)$/);
  if (!m){ el.textContent = raw; return; }
  const [, pre, numStr, suf] = m;
  const dec = (numStr.split('.')[1] || '').length;
  const target = parseFloat(numStr.replace(/,/g, ''));
  const grouped = numStr.includes(',');
  const t0 = performance.now(), dur = 1100;
  (function step(now){
    const p = Math.min(1, (now - t0) / dur);
    const v = target * (1 - Math.pow(1 - p, 3));
    let s = dec ? v.toFixed(dec) : Math.round(v).toString();
    if (grouped) s = (+s).toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
    el.textContent = pre + s + suf;
    if (p < 1) requestAnimationFrame(step);
  })(t0);
}
function animateRing(r){
  const target = parseFloat(r.dataset.p) || 0, t0 = performance.now(), dur = 1100;
  (function step(now){
    const p = Math.min(1, (now - t0) / dur);
    r.style.setProperty('--p', (target * (1 - Math.pow(1 - p, 3))).toFixed(1));
    if (p < 1) requestAnimationFrame(step);
  })(t0);
}
let _io;
function observeAnim(scope){
  if (!_io){
    _io = new IntersectionObserver((ents) => {
      ents.forEach(e => {
        if (!e.isIntersecting) return;
        const el = e.target;
        if (el.hasAttribute('data-reveal')) el.classList.add('in');
        if (el.dataset.count) animateCount(el);
        if (el.classList.contains('bar')) { const i = el.querySelector('i'); if (i && i.dataset.w) i.style.width = i.dataset.w; }
        if (el.classList.contains('ring')) animateRing(el);
        _io.unobserve(el);
      });
    }, { threshold: .18 });
  }
  scope.querySelectorAll('[data-reveal], .kpi .n, .stat-strip .n, .bar, .ring').forEach(el => _io.observe(el));
}
function activateScope(scope){
  scope = scope || document.body;
  tagReveals(scope); prepStats(scope); observeAnim(scope);
}
window.activateScope = activateScope;

/* ---------- Demo chatbot with typing indicator ---------- */
const BOT_REPLIES = [
  "You have <b>2 deadlines</b> this week: the “Statistical Analysis II” quiz (Tue) and the “Data Ethics” assignment (Thu). Want me to set reminders?",
  "Based on your role (Statistician) and recent activity, I recommend <b>“Advanced Survey Sampling”</b> and <b>“Power BI for Analysts.”</b> Shall I enroll you?",
  "Your learning path is <b>62% complete</b>. Finish the “Regression Modelling” module to unlock your certificate 🎓.",
  "I found 3 courses on analytics tools. Want me to filter to ones approved for external entities?",
  "Here’s a quick summary of Module 3: it covers multiple regression, multicollinearity (VIF), and reading model fit with adjusted R²."
];
function botReply(text){
  const r = text.toLowerCase();
  if (/(deadline|due|reminder)/.test(r)) return BOT_REPLIES[0];
  if (/(recommend|suggest|course|enroll)/.test(r)) return BOT_REPLIES[1];
  if (/(progress|certificate|how am i)/.test(r)) return BOT_REPLIES[2];
  if (/(summary|summarize|explain|module)/.test(r)) return BOT_REPLIES[4];
  return BOT_REPLIES[Math.floor(Math.random() * BOT_REPLIES.length)];
}
function sendChat(form){
  const input = form.querySelector('input');
  const stream = form.closest('.chat').querySelector('.stream');
  const text = input.value.trim(); if (!text) return false;
  const me = document.createElement('div'); me.className = 'bubble me'; me.textContent = text;
  stream.appendChild(me); input.value = ''; stream.scrollTop = stream.scrollHeight;
  const typing = document.createElement('div');
  typing.className = 'bubble ai typing'; typing.innerHTML = '<span></span><span></span><span></span>';
  stream.appendChild(typing); stream.scrollTop = stream.scrollHeight;
  setTimeout(() => {
    typing.remove();
    const ai = document.createElement('div'); ai.className = 'bubble ai'; ai.innerHTML = botReply(text);
    stream.appendChild(ai); stream.scrollTop = stream.scrollHeight;
  }, 900);
  return false;
}

/* ---------- Init ---------- */
document.addEventListener('DOMContentLoaded', () => {
  setLang(localStorage.getItem('lms_lang') || 'en');
  setTheme(localStorage.getItem('lms_theme') || 'light');
  injectControls();
  activateScope(document.body);
});
