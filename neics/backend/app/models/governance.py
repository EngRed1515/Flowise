"""Classification results & explainability, temporal history, audit, data quality,
review workflow, and security (RBAC)."""
from datetime import date, datetime

from sqlalchemy import JSON, Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Classification(Base):
    """A committed classification result for an enterprise at a point in time.

    Full temporal versioning: a new row is written on every (re)classification.
    `is_current` marks the active record; history is never overwritten.
    """

    __tablename__ = "classification"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    enterprise_id: Mapped[str] = mapped_column(ForeignKey("enterprise.enterprise_id"), index=True)
    version: Mapped[int] = mapped_column(Integer, default=1)  # incrementing per enterprise
    methodology_version: Mapped[str] = mapped_column(String(10))

    # Multi-dimensional classification key (framework Test 18 — final record)
    residence: Mapped[str | None] = mapped_column(String(10))
    isic_class: Mapped[str | None] = mapped_column(String(4))
    sector_code: Mapped[str | None] = mapped_column(String(10))
    public_private: Mapped[str | None] = mapped_column(String(15))
    control_flag: Mapped[str | None] = mapped_column(String(15))
    market_status: Mapped[str | None] = mapped_column(String(15))
    size_class: Mapped[str | None] = mapped_column(String(15))
    fdi_flag: Mapped[str | None] = mapped_column(String(15))
    special_entity_flag: Mapped[str | None] = mapped_column(String(30))
    group_id: Mapped[str | None] = mapped_column(String(24))

    confidence: Mapped[float | None] = mapped_column(Float)
    trace: Mapped[list | None] = mapped_column(JSON)  # ordered list of test/rule decisions
    facts: Mapped[dict | None] = mapped_column(JSON)  # the fact set used (data provenance)
    is_current: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    is_override: Mapped[bool] = mapped_column(Boolean, default=False)
    override_reason: Mapped[str | None] = mapped_column(Text)
    reviewer: Mapped[str | None] = mapped_column(String(120))
    quality_flag: Mapped[str] = mapped_column(String(20), default="DRAFT")
    created_by: Mapped[str | None] = mapped_column(String(120))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    valid_from: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    valid_to: Mapped[datetime | None] = mapped_column(DateTime)


class AuditEntry(Base):
    """Per-record change log (workbook sheet 12) — who changed what, when, why."""

    __tablename__ = "audit_entry"

    audit_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    record_type: Mapped[str] = mapped_column(String(40))
    record_id: Mapped[str] = mapped_column(String(40), index=True)
    field_changed: Mapped[str | None] = mapped_column(String(60))
    old_value: Mapped[str | None] = mapped_column(String(400))
    new_value: Mapped[str | None] = mapped_column(String(400))
    action: Mapped[str] = mapped_column(String(40))  # CREATE/UPDATE/CLASSIFY/OVERRIDE/DELETE
    changed_by: Mapped[str | None] = mapped_column(String(120))
    evidence_ref: Mapped[str | None] = mapped_column(String(120))


class QualityResult(Base):
    """Data quality measurement for an enterprise across DAMA dimensions."""

    __tablename__ = "quality_result"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    enterprise_id: Mapped[str] = mapped_column(index=True)
    completeness: Mapped[float] = mapped_column(Float, default=0.0)
    validity: Mapped[float] = mapped_column(Float, default=0.0)
    consistency: Mapped[float] = mapped_column(Float, default=0.0)
    uniqueness: Mapped[float] = mapped_column(Float, default=0.0)
    accuracy: Mapped[float] = mapped_column(Float, default=0.0)
    timeliness: Mapped[float] = mapped_column(Float, default=0.0)
    overall_score: Mapped[float] = mapped_column(Float, default=0.0)
    exceptions: Mapped[list | None] = mapped_column(JSON)
    computed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class ReviewItem(Base):
    """Manual review queue — exceptions, anomalies, reclassification triggers."""

    __tablename__ = "review_item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    enterprise_id: Mapped[str] = mapped_column(index=True)
    kind: Mapped[str] = mapped_column(String(40))  # ANOMALY / VALIDATION / TRIGGER / OVERRIDE
    severity: Mapped[str] = mapped_column(String(20), default="INFO")
    title: Mapped[str] = mapped_column(String(300))
    detail: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="OPEN")  # OPEN / RESOLVED / DISMISSED
    assigned_to: Mapped[str | None] = mapped_column(String(120))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime)


class User(Base):
    """Platform user with a single role (RBAC)."""

    __tablename__ = "app_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    full_name: Mapped[str | None] = mapped_column(String(200))
    email: Mapped[str | None] = mapped_column(String(200))
    hashed_password: Mapped[str] = mapped_column(String(200))
    role: Mapped[str] = mapped_column(String(40), default="Analyst")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
