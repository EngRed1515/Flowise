"""Render a single self-contained HTML snapshot of the dashboard.

Bakes the real (seeded) database into one standalone .html file with CSS
inlined and no server needed — so the dashboard can be reviewed on any device.
This is a static PREVIEW for sign-off, not the live app.

    python -m scripts.make_preview        # writes docs/dashboard_preview.html
"""
from __future__ import annotations

import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db import SessionLocal, init_db  # noqa: E402
from app.main import PIPELINE_STATUSES, _kpis  # noqa: E402
from app.models import Project  # noqa: E402

BASE = Path(__file__).resolve().parent.parent
CSS = (BASE / "app" / "web" / "static" / "style.css").read_text()
OUT = BASE / "docs" / "dashboard_preview.html"


def esc(v) -> str:
    return html.escape(str(v if v is not None else ""))


def card(p: Project) -> str:
    fire = " · 🔥" if p.fire_rating_relevant else ""
    return f"""
      <div class="card tier-{p.tier}">
        <div class="card-top"><span class="tier-badge tier-{p.tier}">{p.tier}</span><span class="score">{p.score}</span></div>
        <div class="card-name">{esc(p.project_name)}</div>
        <div class="card-meta">{esc(p.country) or '?'} · {esc(p.project_type)}</div>
        <div class="card-meta">{esc(p.status)} · doors~{p.estimated_door_demand or '?'}{fire}</div>
      </div>"""


def breakdown_rows(p: Project) -> str:
    bd = p.score_breakdown
    if bd.get("disqualified"):
        return f'<tr><td colspan="3" class="disq">Auto-disqualified — {esc(bd.get("reason"))}</td></tr>'
    rows = ""
    for name, f in bd.get("factors", {}).items():
        rows += f"<tr><td>{name}</td><td>{f['normalized']}</td><td>{f['points']} / {f['weight']}</td></tr>"
    return rows


def detail(p: Project) -> str:
    sh = "".join(
        f"<tr><td>{esc(s.role)}</td><td>{esc(s.organisation) or '—'}</td>"
        f"<td>{esc(s.contact_name)} {esc(s.email)} {esc(s.phone)}</td></tr>"
        for s in p.stakeholders
    ) or '<tr><td colspan="3">No stakeholders recorded.</td></tr>'
    srcs = "".join(f"<li><b>{esc(s.source)}</b> · {esc(s.source_record_id)}</li>" for s in p.source_refs)
    val = f"{esc(p.value_currency)} {p.value_estimate:,.0f}" if p.value_estimate else "—"
    return f"""
    <div class="detail">
      <div class="detail-main">
        <h1>{esc(p.project_name)} <span class="tier-badge tier-{p.tier}">Tier {p.tier} · {p.score}</span></h1>
        <p class="sub">{esc(p.country)} · {esc(p.city)} · {esc(p.project_type)} · {esc(p.status)}</p>
        <h3>Project</h3>
        <table class="kv">
          <tr><th>Value estimate</th><td>{val}</td></tr>
          <tr><th>Units / Floor area</th><td>{p.unit_count or '—'} units · {p.floor_area or '—'} sqm</td></tr>
          <tr><th>Estimated door demand</th><td>{p.estimated_door_demand or '—'}</td></tr>
          <tr><th>Fire-rating relevant</th><td>{'✓ yes' if p.fire_rating_relevant else 'no'}</td></tr>
          <tr><th>Reachable before procurement</th><td>{'✓ yes' if p.reachable_before_procurement else 'no'}</td></tr>
        </table>
        <h3>Stakeholders</h3>
        <table class="kv"><tr><th>Role</th><th>Organisation</th><th>Contact</th></tr>{sh}</table>
        <h3>Source references</h3><ul class="sources">{srcs}</ul>
      </div>
      <aside class="detail-side">
        <h3>Why this score?</h3>
        <table class="kv small"><tr><th>Factor</th><th>norm</th><th>pts</th></tr>{breakdown_rows(p)}</table>
      </aside>
    </div>"""


def main() -> None:
    init_db()
    session = SessionLocal()
    try:
        projects = session.query(Project).order_by(Project.score.desc()).all()
        if not projects:
            print("No data. Run `python -m scripts.seed` first.")
            return
        kpis = _kpis(session)
        columns = {st: [p for p in projects if p.pipeline_status == st] for st in PIPELINE_STATUSES}
        board_cols = "".join(
            f'<div class="col"><h3>{st} <span class="count">{len(columns[st])}</span></h3>'
            + "".join(card(p) for p in columns[st]) + "</div>"
            for st in PIPELINE_STATUSES
        )
        # Feature the top-scoring merged project for the detail preview.
        featured = max(projects, key=lambda p: (len(p.source_refs), p.score or 0))
        page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GCC Door Intel — Dashboard Preview</title><style>{CSS}
.banner{{background:#fff7e6;border:1px solid #f0d9a8;color:#7a5b12;padding:10px 14px;
  border-radius:8px;margin:14px 0;font-size:14px;}}
hr.sep{{border:0;border-top:2px dashed var(--line);margin:30px 0;}}</style></head>
<body>
<header class="topbar"><div class="brand">SBK · GCC Door Intelligence <span class="internal">INTERNAL · PREVIEW</span></div>
<nav><a>Pipeline</a><a>Map</a><a>+ Add lead</a><a>Import file</a><a>API</a></nav></header>
<main>
  <div class="banner"><b>Static preview</b> — real seeded data baked into one file. This is what the
  live dashboard looks like. To click, filter and edit, run the app locally (see the UAT walkthrough).</div>

  <h2 style="margin:6px 0">Pipeline board</h2>
  <section class="kpis">
    <div class="kpi"><span class="num">{kpis['total']}</span><span class="lbl">Projects</span></div>
    <div class="kpi"><span class="num tierA">{kpis['by_tier'].get('A',0)}</span><span class="lbl">Tier A</span></div>
    <div class="kpi"><span class="num tierB">{kpis['by_tier'].get('B',0)}</span><span class="lbl">Tier B</span></div>
    <div class="kpi"><span class="num">{kpis['pipeline_value']:,.0f}</span><span class="lbl">Pipeline value</span></div>
    <div class="kpi"><span class="num">{kpis['pre_tender']}/{kpis['post_tender']}</span><span class="lbl">Pre / post tender</span></div>
  </section>
  <div class="board">{board_cols}</div>

  <hr class="sep">
  <h2 style="margin:6px 0">Project detail — example (the merged, cross-source project)</h2>
  {detail(featured)}
</main></body></html>"""
        OUT.write_text(page)
        print(f"Wrote {OUT} ({len(page):,} bytes, {len(projects)} projects).")
    finally:
        session.close()


if __name__ == "__main__":
    main()
