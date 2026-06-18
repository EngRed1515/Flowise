"""Application services that tie the engine to persistence: run classification,
write the versioned classification history, update the golden record, and emit
audit, quality and review-queue records."""
from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.config import get_settings
from app.engine.classifier import RESULT_FIELDS, classify
from app.engine.quality import detect_anomalies, score_enterprise
from app.engine.validation import validate_enterprise
from app.models.enterprise import Enterprise
from app.models.governance import AuditEntry, Classification, QualityResult, ReviewItem

settings = get_settings()


def _audit(db, record_id, action, field=None, old=None, new=None, by=None, evidence=None):
    db.add(AuditEntry(record_type="enterprise", record_id=record_id, action=action,
                      field_changed=field, old_value=str(old) if old is not None else None,
                      new_value=str(new) if new is not None else None, changed_by=by,
                      evidence_ref=evidence))


def run_classification(db: Session, ent: Enterprise, user: str | None = None, commit: bool = True) -> Classification:
    """Execute the 18-test pipeline and persist a new classification version."""
    outcome = classify(db, ent)
    result, trace, facts, conf = outcome["result"], outcome["trace"], outcome["facts"], outcome["confidence"]

    # Determine next version number for this enterprise.
    last = db.execute(
        select(Classification).where(Classification.enterprise_id == ent.enterprise_id)
        .order_by(Classification.version.desc())
    ).scalars().first()
    next_version = (last.version + 1) if last else 1

    # Close the previous current record (temporal versioning).
    db.execute(
        update(Classification)
        .where(Classification.enterprise_id == ent.enterprise_id, Classification.is_current.is_(True))
        .values(is_current=False, valid_to=datetime.now(timezone.utc))
    )

    cls = Classification(
        enterprise_id=ent.enterprise_id, version=next_version,
        methodology_version=settings.methodology_version,
        residence=result.get("residence"), isic_class=result.get("isic_class"),
        sector_code=result.get("sector_code"), public_private=result.get("public_private"),
        control_flag=result.get("control_flag"), market_status=result.get("market_status"),
        size_class=result.get("size_class"), fdi_flag=result.get("fdi_flag"),
        special_entity_flag=result.get("special_entity_flag"), group_id=ent.group_id,
        confidence=conf, trace=trace, facts={k: v for k, v in facts.items() if k != "uci"} | {"uci": facts.get("uci")},
        is_current=True, quality_flag=ent.quality_flag, created_by=user,
    )
    db.add(cls)

    # Update the golden record (latest committed classification).
    for f in RESULT_FIELDS:
        if f in result:
            setattr(ent, f, result[f])
    ent.classification_version = settings.methodology_version
    ent.classification_date = datetime.now(timezone.utc)
    _audit(db, ent.enterprise_id, "CLASSIFY", new=f"v{next_version}", by=user,
           evidence=f"confidence={conf}")

    # Quality scoring
    q = score_enterprise(db, ent)
    ent.quality_score = q["overall_score"]
    db.add(QualityResult(
        enterprise_id=ent.enterprise_id, completeness=q["completeness"], validity=q["validity"],
        consistency=q["consistency"], uniqueness=q["uniqueness"], accuracy=q["accuracy"],
        timeliness=q["timeliness"], overall_score=q["overall_score"], exceptions=q["exceptions"],
    ))

    # Anomaly detection -> review queue
    for a in detect_anomalies(db, ent, facts):
        existing = db.execute(
            select(ReviewItem).where(ReviewItem.enterprise_id == ent.enterprise_id,
                                     ReviewItem.title == a["title"], ReviewItem.status == "OPEN")
        ).scalars().first()
        if not existing:
            db.add(ReviewItem(enterprise_id=ent.enterprise_id, kind=a["kind"], severity=a["severity"],
                              title=a["title"], detail=a["detail"]))

    if commit:
        db.commit()
        db.refresh(cls)
    return cls


def apply_override(db: Session, ent: Enterprise, field: str, value: str, reason: str, reviewer: str) -> Classification:
    """Committee / reviewer manual override — recorded as a new classification version."""
    current = db.execute(
        select(Classification).where(Classification.enterprise_id == ent.enterprise_id,
                                     Classification.is_current.is_(True))
    ).scalars().first()
    old_value = getattr(current, field, None) if current else getattr(ent, field, None)

    if current:
        current.is_current = False
        current.valid_to = datetime.now(timezone.utc)

    next_version = (current.version + 1) if current else 1
    data = {}
    for f in RESULT_FIELDS + ["group_id"]:
        data[f] = getattr(current, f, None) if current else getattr(ent, f, None)
    data[field] = value

    cls = Classification(
        enterprise_id=ent.enterprise_id, version=next_version,
        methodology_version=settings.methodology_version, is_current=True, is_override=True,
        override_reason=reason, reviewer=reviewer, quality_flag="COMMITTEE-RULED",
        confidence=current.confidence if current else None,
        trace=(current.trace if current else []) + [{
            "test_code": "OVERRIDE", "matched": True, "rule_id": "MANUAL-OVERRIDE",
            "rule_name": "Technical Classification Committee override",
            "output": {field: value}, "rationale": reason, "reviewer": reviewer,
        }],
        facts=current.facts if current else None, created_by=reviewer, **data,
    )
    db.add(cls)
    setattr(ent, field, value)
    ent.quality_flag = "COMMITTEE-RULED"
    _audit(db, ent.enterprise_id, "OVERRIDE", field=field, old=old_value, new=value, by=reviewer, evidence=reason)
    db.commit()
    db.refresh(cls)
    return cls
