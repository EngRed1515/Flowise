"""Enterprise master-data, ownership, classification, history, quality and audit."""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import require
from app.database import get_db
from app.engine.ownership import OwnershipEngine
from app.engine.quality import score_enterprise
from app.engine.service import apply_override, run_classification
from app.engine.validation import validate_enterprise
from app.models.enterprise import Enterprise, Establishment, LegalUnit, OwnershipEdge
from app.models.governance import AuditEntry, Classification
from app.schemas import (
    ClassificationOut,
    EnterpriseIn,
    EnterpriseOut,
    OverrideIn,
    OwnershipIn,
    OwnershipOut,
)

router = APIRouter(prefix="/api/enterprises", tags=["Enterprises"])


def _next_enterprise_id(db: Session) -> str:
    year = datetime.now().year
    n = db.execute(select(func.count()).select_from(Enterprise)).scalar_one() + 1
    return f"QA-ENT-{year}{n:07d}"


def _get(db: Session, eid: str) -> Enterprise:
    ent = db.get(Enterprise, eid)
    if not ent:
        raise HTTPException(404, f"Enterprise {eid} not found")
    return ent


@router.get("", response_model=list[EnterpriseOut])
def list_enterprises(
    sector: str | None = None, public_private: str | None = None, size: str | None = None,
    q: str | None = None, limit: int = 200, offset: int = 0,
    db: Session = Depends(get_db), _=Depends(require("enterprise:read")),
):
    stmt = select(Enterprise)
    if sector:
        stmt = stmt.where(Enterprise.sector_code == sector)
    if public_private:
        stmt = stmt.where(Enterprise.public_private == public_private)
    if size:
        stmt = stmt.where(Enterprise.size_class == size)
    if q:
        stmt = stmt.where(Enterprise.legal_name_en.ilike(f"%{q}%"))
    stmt = stmt.order_by(Enterprise.enterprise_id).limit(limit).offset(offset)
    return list(db.execute(stmt).scalars())


@router.post("", response_model=EnterpriseOut, status_code=201)
def create_enterprise(body: EnterpriseIn, db: Session = Depends(get_db), user=Depends(require("enterprise:write"))):
    data = body.model_dump()
    data["enterprise_id"] = data.get("enterprise_id") or _next_enterprise_id(db)
    if db.get(Enterprise, data["enterprise_id"]):
        raise HTTPException(409, "Enterprise ID already exists")
    ent = Enterprise(**data, last_demographic_event="BIRTH", quality_flag="DRAFT")
    db.add(ent)
    db.add(AuditEntry(record_type="enterprise", record_id=ent.enterprise_id, action="CREATE",
                      new_value=ent.legal_name_en, changed_by=user.username))
    db.commit()
    db.refresh(ent)
    return ent


@router.get("/{eid}", response_model=EnterpriseOut)
def get_enterprise(eid: str, db: Session = Depends(get_db), _=Depends(require("enterprise:read"))):
    return _get(db, eid)


@router.put("/{eid}", response_model=EnterpriseOut)
def update_enterprise(eid: str, body: EnterpriseIn, db: Session = Depends(get_db), user=Depends(require("enterprise:write"))):
    ent = _get(db, eid)
    for k, v in body.model_dump(exclude_unset=True, exclude={"enterprise_id"}).items():
        old = getattr(ent, k)
        if old != v:
            setattr(ent, k, v)
            db.add(AuditEntry(record_type="enterprise", record_id=eid, action="UPDATE",
                              field_changed=k, old_value=str(old), new_value=str(v), changed_by=user.username))
    db.commit()
    db.refresh(ent)
    return ent


@router.get("/{eid}/profile")
def enterprise_profile(eid: str, db: Session = Depends(get_db), _=Depends(require("enterprise:read"))):
    """Full enterprise profile: master data, legal units, establishments, ownership,
    current classification, ownership intelligence, quality, and audit history."""
    ent = _get(db, eid)
    eng = OwnershipEngine(db)
    current = db.execute(
        select(Classification).where(Classification.enterprise_id == eid, Classification.is_current.is_(True))
    ).scalars().first()
    audits = db.execute(
        select(AuditEntry).where(AuditEntry.record_id == eid).order_by(AuditEntry.timestamp.desc()).limit(50)
    ).scalars().all()
    return {
        "enterprise": EnterpriseOut.model_validate(ent),
        "legal_units": [
            {"legal_unit_id": lu.legal_unit_id, "legal_name_en": lu.legal_name_en, "lei": lu.lei,
             "legal_form_code": lu.legal_form_code, "cr_number": lu.cr_number,
             "registration_authority": lu.registration_authority, "is_active": lu.is_active}
            for lu in ent.legal_units
        ],
        "establishments": [
            {"establishment_id": e.establishment_id, "name": e.name, "isic_class": e.isic_class,
             "municipality": e.municipality, "zone": e.zone, "employment": e.employment,
             "latitude": e.latitude, "longitude": e.longitude}
            for e in ent.establishments
        ],
        "ownership": {
            "facts": eng.facts(eid),
            "chain": eng.chain(eid),
            "uci": eng.ultimate_controlling_unit(eid),
            "edges": [OwnershipOut.model_validate(x) for x in eng.direct_edges(eid)],
        },
        "current_classification": ClassificationOut.model_validate(current) if current else None,
        "quality": score_enterprise(db, ent),
        "validation": validate_enterprise(db, ent),
        "audit": [
            {"timestamp": a.timestamp, "action": a.action, "field": a.field_changed,
             "old": a.old_value, "new": a.new_value, "by": a.changed_by, "evidence": a.evidence_ref}
            for a in audits
        ],
    }


# --- ownership ---
@router.get("/{eid}/ownership", response_model=list[OwnershipOut])
def get_ownership(eid: str, db: Session = Depends(get_db), _=Depends(require("enterprise:read"))):
    return OwnershipEngine(db).direct_edges(eid)


@router.post("/{eid}/ownership", response_model=OwnershipOut, status_code=201)
def add_ownership(eid: str, body: OwnershipIn, db: Session = Depends(get_db), user=Depends(require("ownership:write"))):
    _get(db, eid)
    data = body.model_dump()
    data["owned_id"] = eid
    if not data.get("edge_id"):
        n = db.execute(select(func.count()).select_from(OwnershipEdge)).scalar_one() + 1
        data["edge_id"] = f"E{n:05d}"
    edge = OwnershipEdge(**data)
    db.add(edge)
    db.add(AuditEntry(record_type="ownership", record_id=eid, action="UPDATE",
                      field_changed="ownership_edge", new_value=f"{data['owner_id']}->{eid}", changed_by=user.username))
    db.commit()
    db.refresh(edge)
    return edge


# --- classification ---
@router.post("/{eid}/classify", response_model=ClassificationOut)
def classify_enterprise(eid: str, db: Session = Depends(get_db), user=Depends(require("classify:run"))):
    ent = _get(db, eid)
    return run_classification(db, ent, user=user.username)


@router.get("/{eid}/classification", response_model=ClassificationOut)
def current_classification(eid: str, db: Session = Depends(get_db), _=Depends(require("classify:read"))):
    cls = db.execute(
        select(Classification).where(Classification.enterprise_id == eid, Classification.is_current.is_(True))
    ).scalars().first()
    if not cls:
        raise HTTPException(404, "No classification yet — run /classify")
    return cls


@router.get("/{eid}/history", response_model=list[ClassificationOut])
def classification_history(eid: str, db: Session = Depends(get_db), _=Depends(require("classify:read"))):
    return list(db.execute(
        select(Classification).where(Classification.enterprise_id == eid).order_by(Classification.version.desc())
    ).scalars())


@router.get("/{eid}/explain")
def explain(eid: str, db: Session = Depends(get_db), _=Depends(require("classify:read"))):
    """Full explainability payload for the current classification."""
    cls = db.execute(
        select(Classification).where(Classification.enterprise_id == eid, Classification.is_current.is_(True))
    ).scalars().first()
    if not cls:
        raise HTTPException(404, "No classification yet — run /classify")
    applied = [t for t in (cls.trace or []) if t.get("matched")]
    return {
        "enterprise_id": eid,
        "result": {f: getattr(cls, f) for f in
                   ["residence", "isic_class", "sector_code", "public_private", "control_flag",
                    "market_status", "size_class", "fdi_flag", "special_entity_flag"]},
        "confidence": cls.confidence,
        "applied_rules": [{"test": t["test_code"], "rule_id": t.get("rule_id"), "rule_name": t.get("rule_name"),
                           "output": t.get("output"), "standard_ref": t.get("standard_ref"),
                           "rationale": t.get("rationale")} for t in applied],
        "data_fields_used": cls.facts,
        "data_sources": ["CSBR golden record", "Ownership graph", "Reference codelists"],
        "reviewer": cls.reviewer, "is_override": cls.is_override, "override_reason": cls.override_reason,
        "classification_timestamp": cls.created_at, "methodology_version": cls.methodology_version,
        "full_trace": cls.trace,
    }


@router.post("/{eid}/override", response_model=ClassificationOut)
def override(eid: str, body: OverrideIn, db: Session = Depends(get_db), user=Depends(require("override:write"))):
    ent = _get(db, eid)
    return apply_override(db, ent, body.field, body.value, body.reason, user.username)
