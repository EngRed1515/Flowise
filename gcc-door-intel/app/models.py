"""ORM models for the unified project schema, stakeholders, source references
and the raw ingestion staging table."""
from __future__ import annotations

import datetime as dt
import json
from typing import Any

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


def _now() -> dt.datetime:
    return dt.datetime.utcnow()


class StagingRecord(Base):
    """Raw copy of every ingested record, kept for traceability."""

    __tablename__ = "staging_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(64), index=True)
    source_record_id: Mapped[str] = mapped_column(String(255), index=True)
    ingested_at: Mapped[dt.datetime] = mapped_column(DateTime, default=_now)
    raw_json: Mapped[str] = mapped_column(Text)  # original row, verbatim
    mapped_json: Mapped[str] = mapped_column(Text)  # after column mapping
    processed: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    project_id: Mapped[str | None] = mapped_column(String(64), nullable=True)

    @property
    def raw(self) -> dict[str, Any]:
        return json.loads(self.raw_json)

    @property
    def mapped(self) -> dict[str, Any]:
        return json.loads(self.mapped_json)


class Project(Base):
    """Unified, normalized project record (deduped across sources)."""

    __tablename__ = "projects"

    project_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    source: Mapped[str] = mapped_column(String(64))  # origin source
    ingested_at: Mapped[dt.datetime] = mapped_column(DateTime, default=_now)
    last_updated: Mapped[dt.datetime] = mapped_column(DateTime, default=_now, onupdate=_now)

    project_name: Mapped[str] = mapped_column(String(512), index=True)
    country: Mapped[str | None] = mapped_column(String(64), index=True)
    city: Mapped[str | None] = mapped_column(String(128))
    district: Mapped[str | None] = mapped_column(String(128))

    project_type: Mapped[str | None] = mapped_column(String(64), index=True)
    status: Mapped[str | None] = mapped_column(String(32), index=True)
    stage_date: Mapped[str | None] = mapped_column(String(32))
    expected_procurement_date: Mapped[str | None] = mapped_column(String(32))

    value_estimate: Mapped[float | None] = mapped_column(Float)
    value_currency: Mapped[str | None] = mapped_column(String(8))
    floor_area: Mapped[float | None] = mapped_column(Float)
    unit_count: Mapped[int | None] = mapped_column(Integer)

    fire_rating_relevant: Mapped[bool] = mapped_column(Boolean, default=False)
    estimated_door_demand: Mapped[int | None] = mapped_column(Integer)
    reachable_before_procurement: Mapped[bool] = mapped_column(Boolean, default=False)

    # Geo (best-effort, for the map view)
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)

    score: Mapped[float | None] = mapped_column(Float, index=True)
    tier: Mapped[str | None] = mapped_column(String(2), index=True)
    score_breakdown_json: Mapped[str | None] = mapped_column(Text)

    notes: Mapped[str | None] = mapped_column(Text)
    assigned_to: Mapped[str | None] = mapped_column(String(128))
    pipeline_status: Mapped[str] = mapped_column(String(32), default="new", index=True)

    stakeholders: Mapped[list["Stakeholder"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    source_refs: Mapped[list["SourceRef"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )

    @property
    def score_breakdown(self) -> dict[str, Any]:
        return json.loads(self.score_breakdown_json) if self.score_breakdown_json else {}


class Stakeholder(Base):
    __tablename__ = "stakeholders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.project_id"))
    role: Mapped[str] = mapped_column(String(32))  # developer/architect/consultant/...
    contact_name: Mapped[str | None] = mapped_column(String(255))
    organisation: Mapped[str | None] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(64))

    project: Mapped[Project] = relationship(back_populates="stakeholders")


class SourceRef(Base):
    """Every source a merged project was seen in (full traceability)."""

    __tablename__ = "source_refs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.project_id"))
    source: Mapped[str] = mapped_column(String(64))
    source_record_id: Mapped[str] = mapped_column(String(255))
    ingested_at: Mapped[dt.datetime] = mapped_column(DateTime, default=_now)

    project: Mapped[Project] = relationship(back_populates="source_refs")
