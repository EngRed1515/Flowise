"""Internal web UI + JSON API (FastAPI).

INTERNAL TOOL — no public access intended. Run locally / behind the team VPN.
Provides: pipeline board, project detail (with score breakdown + sources),
map view, KPIs, manual add/edit, and a file-upload ingestion endpoint.
"""
from __future__ import annotations

import json
import shutil
import tempfile
import uuid
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session

from .config import MAPPINGS_DIR, get_config
from .connectors.file_import import FileImportConnector
from .db import get_session, init_db, session_scope
from .models import Project
from .normalization import enrich, normalize
from .normalization.vocab import CANONICAL_PROJECT_TYPES, CANONICAL_STATUSES
from .pipeline import _apply_scores, run_connector

BASE = Path(__file__).resolve().parent
app = FastAPI(title="GCC Door Project Intelligence", docs_url="/api/docs")
templates = Jinja2Templates(directory=str(BASE / "web" / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE / "web" / "static")), name="static")

PIPELINE_STATUSES = ["new", "watching", "pursuing", "quoted", "won", "lost", "archived"]


@app.on_event("startup")
def _startup() -> None:
    init_db()


# ---------------------------------------------------------------- helpers ---
def _filtered_projects(session: Session, country, tier, ptype, status, min_score) -> list[Project]:
    q = session.query(Project)
    if country:
        q = q.filter(Project.country == country)
    if tier:
        q = q.filter(Project.tier == tier)
    if ptype:
        q = q.filter(Project.project_type == ptype)
    if status:
        q = q.filter(Project.pipeline_status == status)
    if min_score:
        q = q.filter(Project.score >= float(min_score))
    return q.order_by(Project.score.desc().nullslast()).all()


# ------------------------------------------------------------------ views ---
@app.get("/", response_class=HTMLResponse)
def board(
    request: Request,
    session: Session = Depends(get_session),
    country: Optional[str] = None,
    tier: Optional[str] = None,
    project_type: Optional[str] = None,
    min_score: Optional[str] = None,
):
    projects = _filtered_projects(session, country, tier, project_type, None, min_score)
    columns = {st: [] for st in PIPELINE_STATUSES}
    for p in projects:
        columns.setdefault(p.pipeline_status, []).append(p)
    countries = [c[0] for c in session.query(Project.country).distinct() if c[0]]
    return templates.TemplateResponse(
        "board.html",
        {
            "request": request,
            "columns": columns,
            "statuses": PIPELINE_STATUSES,
            "countries": countries,
            "project_types": CANONICAL_PROJECT_TYPES,
            "filters": {"country": country, "tier": tier, "project_type": project_type, "min_score": min_score},
            "kpis": _kpis(session),
        },
    )


@app.get("/project/{project_id}", response_class=HTMLResponse)
def project_detail(project_id: str, request: Request, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        return HTMLResponse("Not found", status_code=404)
    return templates.TemplateResponse(
        "project.html",
        {
            "request": request,
            "p": project,
            "breakdown": project.score_breakdown,
            "pipeline_statuses": PIPELINE_STATUSES,
            "statuses": CANONICAL_STATUSES,
        },
    )


@app.post("/project/{project_id}/edit")
def project_edit(
    project_id: str,
    session: Session = Depends(get_session),
    pipeline_status: str = Form(...),
    assigned_to: str = Form(""),
    notes: str = Form(""),
    status: str = Form(""),
):
    project = session.get(Project, project_id)
    if project:
        project.pipeline_status = pipeline_status
        project.assigned_to = assigned_to or None
        project.notes = notes or None
        if status and status != project.status:
            project.status = status
            _apply_scores(project)
        session.commit()
    return RedirectResponse(f"/project/{project_id}", status_code=303)


@app.get("/add", response_class=HTMLResponse)
def add_form(request: Request):
    return templates.TemplateResponse(
        "add.html",
        {"request": request, "statuses": CANONICAL_STATUSES, "project_types": CANONICAL_PROJECT_TYPES},
    )


@app.post("/add")
def add_project(
    session: Session = Depends(get_session),
    project_name: str = Form(...),
    country: str = Form(""),
    city: str = Form(""),
    project_type: str = Form("other"),
    status: str = Form("design"),
    unit_count: str = Form(""),
    floor_area: str = Form(""),
    developer: str = Form(""),
    contact_name: str = Form(""),
    contact_email: str = Form(""),
    contact_phone: str = Form(""),
):
    """Manual add for word-of-mouth / network leads — runs the same enrich+score."""
    mapped = {
        "project_name": project_name, "country": country, "city": city,
        "project_type": project_type, "status": status, "unit_count": unit_count,
        "floor_area": floor_area, "developer": developer, "contact_name": contact_name,
        "contact_email": contact_email, "contact_phone": contact_phone,
    }
    norm = normalize.normalize_record(mapped)
    pdata = enrich.enrich(norm["project"], norm["stakeholders"])
    project = Project(project_id=uuid.uuid4().hex[:12], source="manual", **pdata)
    session.add(project)
    session.flush()
    from .models import Stakeholder
    for s in norm["stakeholders"]:
        session.add(Stakeholder(project_id=project.project_id, **s))
    _apply_scores(project)
    session.commit()
    return RedirectResponse(f"/project/{project.project_id}", status_code=303)


@app.get("/map", response_class=HTMLResponse)
def map_view(request: Request, session: Session = Depends(get_session)):
    rows = session.query(Project).filter(Project.latitude.isnot(None)).all()
    points = [
        {
            "id": p.project_id, "name": p.project_name, "lat": p.latitude, "lon": p.longitude,
            "tier": p.tier, "score": p.score, "country": p.country, "type": p.project_type,
        }
        for p in rows
    ]
    return templates.TemplateResponse("map.html", {"request": request, "points": json.dumps(points)})


@app.get("/upload", response_class=HTMLResponse)
def upload_form(request: Request):
    profiles = sorted(p.stem for p in MAPPINGS_DIR.glob("*.yaml"))
    return templates.TemplateResponse("upload.html", {"request": request, "profiles": profiles})


@app.post("/upload")
async def upload_file(file: UploadFile, profile: str = Form(...)):
    """Ingest a user-provided export file through the file-import connector."""
    suffix = Path(file.filename or "upload.csv").suffix or ".csv"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    with session_scope() as session:
        connector = FileImportConnector(tmp_path, profile)
        result = run_connector(session, connector, fire_alerts=True)
    Path(tmp_path).unlink(missing_ok=True)
    return RedirectResponse("/", status_code=303)


# -------------------------------------------------------------------- KPIs ---
def _kpis(session: Session) -> dict:
    total = session.query(func.count(Project.project_id)).scalar() or 0
    by_tier = dict(session.query(Project.tier, func.count()).group_by(Project.tier).all())
    by_country = dict(session.query(Project.country, func.count()).group_by(Project.country).all())
    pipeline_value = session.query(func.coalesce(func.sum(Project.value_estimate), 0)).scalar() or 0
    won = session.query(func.count()).filter(Project.pipeline_status == "won").scalar() or 0
    lost = session.query(func.count()).filter(Project.pipeline_status == "lost").scalar() or 0
    win_rate = round(100 * won / (won + lost), 1) if (won + lost) else None
    # entered pre-tender vs post-tender (proxy: current status when first scored)
    pre = session.query(func.count()).filter(Project.status.in_(["concept", "design", "pre-tender"])).scalar() or 0
    post = session.query(func.count()).filter(Project.status.in_(["tender", "awarded", "under-construction"])).scalar() or 0
    return {
        "total": total, "by_tier": by_tier, "by_country": by_country,
        "pipeline_value": pipeline_value, "win_rate": win_rate,
        "pre_tender": pre, "post_tender": post,
    }


# ------------------------------------------------------------- JSON API -----
@app.get("/api/projects")
def api_projects(
    session: Session = Depends(get_session),
    country: Optional[str] = None,
    tier: Optional[str] = None,
    project_type: Optional[str] = None,
    pipeline_status: Optional[str] = None,
    min_score: Optional[str] = None,
):
    projects = _filtered_projects(session, country, tier, project_type, pipeline_status, min_score)
    return JSONResponse(
        [
            {
                "project_id": p.project_id, "project_name": p.project_name, "country": p.country,
                "city": p.city, "project_type": p.project_type, "status": p.status,
                "score": p.score, "tier": p.tier, "pipeline_status": p.pipeline_status,
                "estimated_door_demand": p.estimated_door_demand, "value_estimate": p.value_estimate,
                "value_currency": p.value_currency, "fire_rating_relevant": p.fire_rating_relevant,
                "reachable_before_procurement": p.reachable_before_procurement,
                "sources": [{"source": s.source, "id": s.source_record_id} for s in p.source_refs],
            }
            for p in projects
        ]
    )


@app.get("/api/kpis")
def api_kpis(session: Session = Depends(get_session)):
    return _kpis(session)
