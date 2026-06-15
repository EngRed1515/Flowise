/* NPC Qatar LMS — mockup interactions (no backend) */

// --- Language toggle (EN / AR direction demo) ---
function setLang(lang){
  const html = document.documentElement;
  if(lang === 'ar'){ html.setAttribute('dir','rtl'); html.setAttribute('lang','ar'); }
  else { html.setAttribute('dir','ltr'); html.setAttribute('lang','en'); }
  document.querySelectorAll('.lang button').forEach(b=>{
    b.classList.toggle('active', b.dataset.lang === lang);
  });
  localStorage.setItem('lms_lang', lang);
}
document.addEventListener('click', e=>{
  const b = e.target.closest('.lang button');
  if(b) setLang(b.dataset.lang);
});

// --- Demo chatbot ---
const BOT_REPLIES = [
  "You have <b>2 deadlines</b> this week: “Statistical Analysis II” quiz (Tue) and the “Data Ethics” assignment (Thu).",
  "Based on your role (Statistician) and recent activity, I recommend <b>“Advanced Survey Sampling”</b> and <b>“Power BI for Analysts.”</b>",
  "Your current learning path is <b>62% complete</b>. Finish the “Regression Modelling” module to unlock your certificate.",
  "I’ve found 3 courses on analytics tools. Want me to filter to ones approved for external entities?",
  "Sure — I drafted a short summary of Module 3. It covers descriptive statistics, dispersion, and visual encoding."
];
function botReply(text){
  const r = text.toLowerCase();
  if(r.includes('deadline')||r.includes('due')) return BOT_REPLIES[0];
  if(r.includes('recommend')||r.includes('suggest')||r.includes('course')) return BOT_REPLIES[1];
  if(r.includes('progress')||r.includes('certificate')) return BOT_REPLIES[2];
  if(r.includes('summary')||r.includes('summarize')||r.includes('explain')) return BOT_REPLIES[4];
  return BOT_REPLIES[Math.floor(Math.random()*BOT_REPLIES.length)];
}
function sendChat(form){
  const input = form.querySelector('input');
  const stream = form.closest('.chat').querySelector('.stream');
  const text = input.value.trim();
  if(!text) return false;
  const me = document.createElement('div');
  me.className = 'bubble me'; me.textContent = text; stream.appendChild(me);
  input.value = '';
  stream.scrollTop = stream.scrollHeight;
  setTimeout(()=>{
    const ai = document.createElement('div');
    ai.className = 'bubble ai'; ai.innerHTML = botReply(text); stream.appendChild(ai);
    stream.scrollTop = stream.scrollHeight;
  }, 450);
  return false;
}

// restore language preference
document.addEventListener('DOMContentLoaded', ()=>{
  setLang(localStorage.getItem('lms_lang') || 'en');
});
