"""Dashboard, review centre, audit reports, quality reports, simulation sandbox,
and administration (users / roles)."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import ROLE_PERMISSIONS, require
from app.database import get_db
from app.engine.classifier import classify
from app.engine.ownership import OwnershipEngine
from app.models.enterprise import Enterprise, OwnershipEdge
from app.models.governance import AuditEntry, Classification, QualityResult, ReviewItem, User
from app.models.rules import Rule
from app.schemas import SimulateIn, UserOut

router = APIRouter(prefix="/api", tags=["Governance"])


# --- Dashboard ---
@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), _=Depends(require("enterprise:read"))):
    total = db.execute(select(func.count()).select_from(Enterprise)).scalar_one()

    def group_count(col):
        rows = db.execute(select(col, func.count()).group_by(col)).all()
        return {(k or "UNCLASSIFIED"): v for k, v in rows}

    open_reviews = db.execute(
        select(func.count()).select_from(ReviewItem).where(ReviewItem.status == "OPEN")
    ).scalar_one()
    avg_quality = db.execute(select(func.avg(Enterprise.quality_score))).scalar_one()
    classified = db.execute(
        select(func.count()).select_from(Enterprise).where(Enterprise.classification_date.is_not(None))
    ).scalar_one()
    return {
        "total_enterprises": total,
        "classified": classified,
        "pending_reviews": open_reviews,
        "avg_quality_score": round(avg_quality, 3) if avg_quality else None,
        "by_sector": group_count(Enterprise.sector_code),
        "by_public_private": group_count(Enterprise.public_private),
        "by_size": group_count(Enterprise.size_class),
        "by_control": group_count(Enterprise.control_flag),
        "by_quality_flag": group_count(Enterprise.quality_flag),
        "rules_active": db.execute(select(func.count()).select_from(Rule).where(Rule.is_active.is_(True))).scalar_one(),
    }


# --- Review Centre ---
@router.get("/reviews")
def list_reviews(status: str = "OPEN", db: Session = Depends(get_db), _=Depends(require("review:read"))):
    stmt = select(ReviewItem)
    if status != "ALL":
        stmt = stmt.where(ReviewItem.status == status)
    items = db.execute(stmt.order_by(ReviewItem.created_at.desc())).scalars().all()
    return [{"id": r.id, "enterprise_id": r.enterprise_id, "kind": r.kind, "severity": r.severity,
             "title": r.title, "detail": r.detail, "status": r.status, "created_at": r.created_at}
            for r in items]


@router.post("/reviews/{review_id}/resolve")
def resolve_review(review_id: int, resolution: str = "RESOLVED",
                   db: Session = Depends(get_db), user=Depends(require("review:write"))):
    item = db.get(ReviewItem, review_id)
    if not item:
        raise HTTPException(404, "Review item not found")
    item.status = resolution
    item.assigned_to = user.username
    db.commit()
    return {"id": review_id, "status": resolution}


# --- Audit report ---
@router.get("/audit")
def audit_report(record_id: str | None = None, limit: int = 200,
                 db: Session = Depends(get_db), _=Depends(require("audit:read"))):
    stmt = select(AuditEntry)
    if record_id:
        stmt = stmt.where(AuditEntry.record_id == record_id)
    rows = db.execute(stmt.order_by(AuditEntry.timestamp.desc()).limit(limit)).scalars().all()
    return [{"audit_id": a.audit_id, "timestamp": a.timestamp, "record_type": a.record_type,
             "record_id": a.record_id, "action": a.action, "field": a.field_changed,
             "old_value": a.old_value, "new_value": a.new_value, "changed_by": a.changed_by,
             "evidence_ref": a.evidence_ref} for a in rows]


# --- Quality report ---
@router.get("/quality")
def quality_report(db: Session = Depends(get_db), _=Depends(require("quality:read"))):
    latest = {}
    for q in db.execute(select(QualityResult).order_by(QualityResult.computed_at)).scalars():
        latest[q.enterprise_id] = q
    rows = list(latest.values())
    dims = ["completeness", "validity", "consistency", "uniqueness", "accuracy", "timeliness", "overall_score"]
    agg = {d: round(sum(getattr(r, d) for r in rows) / len(rows), 3) for d in dims} if rows else {}
    exceptions = []
    for r in rows:
        for e in (r.exceptions or []):
            exceptions.append({"enterprise_id": r.enterprise_id, **e})
    return {
        "dataset_scores": agg,
        "enterprise_scores": [{"enterprise_id": r.enterprise_id,
                               **{d: getattr(r, d) for d in dims}} for r in rows],
        "exceptions": exceptions,
        "exception_count": len(exceptions),
    }


# --- Simulation sandbox (never persisted) ---
@router.post("/simulate", tags=["Simulation"])
def simulate(body: SimulateIn, db: Session = Depends(get_db), _=Depends(require("classify:run"))):
    """Classify a hypothetical enterprise + ownership in-memory without touching the
    register. Supports what-if analysis (ownership / legal-status / restructuring)."""
    sandbox_id = body.enterprise_id or "SANDBOX-0001"

    # Build a transient enterprise (not added to the session).
    ent_fields = {k: v for k, v in body.model_dump().items() if k != "ownership"}
    ent_fields["enterprise_id"] = sandbox_id
    ent = Enterprise(**ent_fields)

    # Temporarily insert ownership edges in a nested transaction, classify, then roll back.
    with db.begin_nested() as nested:
        db.add(ent)
        for i, o in enumerate(body.ownership):
            data = o.model_dump()
            data["owned_id"] = sandbox_id
            data["edge_id"] = data.get("edge_id") or f"SIM-{i+1:04d}"
            db.add(OwnershipEdge(**data))
        db.flush()
        outcome = classify(db, ent)
        nested.rollback()
    return {"sandbox": True, "enterprise_id": sandbox_id, **outcome}


# --- Administration: users / roles ---
@router.get("/admin/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _=Depends(require("*"))):
    return list(db.execute(select(User)).scalars())


@router.get("/admin/roles")
def list_roles(_=Depends(require("*"))):
    return {role: sorted(perms) for role, perms in ROLE_PERMISSIONS.items()}
