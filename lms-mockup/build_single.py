#!/usr/bin/env python3
import re, pathlib

base = pathlib.Path("/home/user/Flowise/lms-mockup")
css = (base/"assets/styles.css").read_text()
appjs = (base/"assets/app.js").read_text()

pages = ["index","login","dashboard","catalog","course","instructor","admin","ai"]

def body_inner(html):
    m = re.search(r"<body[^>]*>(.*)</body>", html, re.S)
    s = m.group(1)
    # drop the external script include + stylesheet (we inline globally)
    s = s.replace('<script src="assets/app.js"></script>', "")
    return s

def fix_links(s):
    # X.html or X.html#anchor  ->  router call
    def repl(m):
        name = m.group(1)
        return f'href="#" onclick="go(\'{name}\');return false"'
    s = re.sub(r'href="(\w+)\.html(?:#[\w-]+)?"', repl, s)
    return s

views = []
for p in pages:
    html = (base/f"{p}.html").read_text()
    inner = fix_links(body_inner(html))
    show = "active" if p == "index" else ""
    views.append(f'<div class="view {show}" id="view-{p}">\n{inner}\n</div>')

views_html = "\n".join(views)

router = """
function go(name){
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
  var el=document.getElementById('view-'+name);
  if(el){el.classList.add('active'); if(window.activateScope){window.activateScope(el);} }
  // close any open mobile sidebar
  document.querySelectorAll('.sidebar.open').forEach(function(s){s.classList.remove('open');});
  var sc=document.querySelector('.scrim'); if(sc){sc.style.display='none';}
  window.scrollTo(0,0);
  if(location.hash!=='#'+name){history.replaceState(null,'','#'+name);}
}
window.addEventListener('DOMContentLoaded',function(){
  var h=(location.hash||'#index').slice(1);
  if(document.getElementById('view-'+h)){go(h);}
});
"""

out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NPC Qatar LMS — Visual Mockup</title>
<style>
{css}
/* single-file view switching */
.view{{display:none}}
.view.active{{display:block}}
</style>
</head>
<body>
{views_html}
<script>
{appjs}
{router}
</script>
</body>
</html>
"""

target = base/"NPC-LMS-Mockup.html"
target.write_text(out)
print("wrote", target, len(out), "bytes,", len(pages), "screens")
