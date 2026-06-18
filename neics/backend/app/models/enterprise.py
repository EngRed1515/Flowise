"""Core Master Data Management entities.

Implements the statistical-unit model from the framework:
    Enterprise Group > Enterprise > KAU > Establishment / Local Unit,
with Legal Units mapped to Enterprises, plus the share-by-share ownership graph.
Mirrors workbook sheets 01-05.
"""
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class EnterpriseGroup(Base):
    """Enterprise group — global ultimate parent, domestic head, truncated group."""

    __tablename__ = "enterprise_group"

    group_id: Mapped[str] = mapped_column(String(24), primary_key=True)  # QA-GRP-YYYYNNNNNNN
    group_name: Mapped[str] = mapped_column(String(300))
    group_name_ar: Mapped[str | None] = mapped_column(String(300))
    global_ultimate_parent: Mapped[str | None] = mapped_column(String(300))
    gup_country: Mapped[str | None] = mapped_column(String(2))  # ISO country
    domestic_group_head: Mapped[str | None] = mapped_column(String(24))
    truncated_group_flag: Mapped[str] = mapped_column(String(1), default="N")
    member_count: Mapped[int] = mapped_column(Integer, default=0)
    controlling_sector: Mapped[str | None] = mapped_column(String(10))
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Enterprise(Base):
    """Core enterprise register — the golden record. One row per enterprise."""

    __tablename__ = "enterprise"

    enterprise_id: Mapped[str] = mapped_column(String(24), primary_key=True)  # QA-ENT-YYYYNNNNNNN
    lei: Mapped[str | None] = mapped_column(String(20))
    legal_name_en: Mapped[str] = mapped_column(String(300))
    legal_name_ar: Mapped[str | None] = mapped_column(String(300))
    legal_form_code: Mapped[str | None] = mapped_column(String(10))

    # --- Inputs that feed classification (declared / sourced facts) ---
    residence: Mapped[str | None] = mapped_column(String(10))  # RES / NRES / MULTI
    isic_class: Mapped[str | None] = mapped_column(String(4))
    employment: Mapped[int | None] = mapped_column(Integer)
    turnover_qar: Mapped[float | None] = mapped_column(Float)
    total_assets_qar: Mapped[float | None] = mapped_column(Float)
    sales: Mapped[float | None] = mapped_column(Float)  # market-test numerator
    production_costs: Mapped[float | None] = mapped_column(Float)  # market-test denominator
    is_nonprofit: Mapped[bool] = mapped_column(Boolean, default=False)
    has_premises: Mapped[bool] = mapped_column(Boolean, default=True)
    has_employees: Mapped[bool] = mapped_column(Boolean, default=True)
    has_autonomy: Mapped[bool] = mapped_column(Boolean, default=True)
    is_financial: Mapped[bool] = mapped_column(Boolean, default=False)
    jurisdiction: Mapped[str | None] = mapped_column(String(20))  # MAINLAND / QFC / QFZA / QSTP

    # --- Classification outputs (latest committed result; full history in classification_*) ---
    sector_code: Mapped[str | None] = mapped_column(String(10))
    public_private: Mapped[str | None] = mapped_column(String(15))
    control_flag: Mapped[str | None] = mapped_column(String(15))
    market_status: Mapped[str | None] = mapped_column(String(15))  # MARKET / NON-MARKET
    size_class: Mapped[str | None] = mapped_column(String(15))
    fdi_flag: Mapped[str | None] = mapped_column(String(15))
    special_entity_flag: Mapped[str | None] = mapped_column(String(30))

    group_id: Mapped[str | None] = mapped_column(ForeignKey("enterprise_group.group_id"))

    # --- Demography & governance ---
    birth_date: Mapped[date | None] = mapped_column(Date)
    death_date: Mapped[date | None] = mapped_column(Date)
    last_demographic_event: Mapped[str | None] = mapped_column(String(30))
    classification_version: Mapped[str | None] = mapped_column(String(10))
    classification_date: Mapped[datetime | None] = mapped_column(DateTime)
    quality_flag: Mapped[str] = mapped_column(String(20), default="DRAFT")
    quality_score: Mapped[float | None] = mapped_column(Float)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    legal_units: Mapped[list["LegalUnit"]] = relationship(back_populates="enterprise", cascade="all, delete-orphan")
    establishments: Mapped[list["Establishment"]] = relationship(back_populates="enterprise", cascade="all, delete-orphan")


class LegalUnit(Base):
    """Legal units mapped to enterprises (workbook sheet 02)."""

    __tablename__ = "legal_unit"

    legal_unit_id: Mapped[str] = mapped_column(String(24), primary_key=True)  # QA-LU-YYYYNNNNNNN
    enterprise_id: Mapped[str] = mapped_column(ForeignKey("enterprise.enterprise_id"))
    lei: Mapped[str | None] = mapped_column(String(20))
    legal_name_en: Mapped[str] = mapped_column(String(300))
    legal_name_ar: Mapped[str | None] = mapped_column(String(300))
    legal_form_code: Mapped[str | None] = mapped_column(String(10))
    cr_number: Mapped[str | None] = mapped_column(String(40))
    registration_authority: Mapped[str | None] = mapped_column(String(60))
    registration_date: Mapped[date | None] = mapped_column(Date)
    ceased_date: Mapped[date | None] = mapped_column(Date)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[str | None] = mapped_column(Text)

    enterprise: Mapped["Enterprise"] = relationship(back_populates="legal_units")


class Establishment(Base):
    """Establishments / local units, geo-coded and activity-coded (workbook sheet 03)."""

    __tablename__ = "establishment"

    establishment_id: Mapped[str] = mapped_column(String(24), primary_key=True)  # QA-EST-YYYYNNNNNNN
    enterprise_id: Mapped[str] = mapped_column(ForeignKey("enterprise.enterprise_id"))
    kau_id: Mapped[str | None] = mapped_column(String(24))
    name: Mapped[str] = mapped_column(String(300))
    name_ar: Mapped[str | None] = mapped_column(String(300))
    isic_class: Mapped[str | None] = mapped_column(String(4))
    municipality: Mapped[str | None] = mapped_column(String(100))
    zone: Mapped[str | None] = mapped_column(String(100))
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    employment: Mapped[int | None] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    enterprise: Mapped["Enterprise"] = relationship(back_populates="establishments")


class OwnershipEdge(Base):
    """Directed share-by-share ownership edge (workbook sheet 05).

    Owners may be registered enterprises (QA-ENT-...) or external parties
    (e.g. STATE-QA, FOREIGN-PARENT-01). This forms the ownership graph used by
    the Enterprise Group & Ownership Intelligence Engine.
    """

    __tablename__ = "ownership_edge"

    edge_id: Mapped[str] = mapped_column(String(24), primary_key=True)
    owner_id: Mapped[str] = mapped_column(String(40), index=True)
    owner_name: Mapped[str | None] = mapped_column(String(300))
    owner_is_government: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_is_resident: Mapped[bool] = mapped_column(Boolean, default=True)
    owner_country: Mapped[str | None] = mapped_column(String(2))
    owned_id: Mapped[str] = mapped_column(String(40), index=True)
    owned_name: Mapped[str | None] = mapped_column(String(300))
    ownership_pct: Mapped[float] = mapped_column(Float, default=0.0)
    voting_pct: Mapped[float] = mapped_column(Float, default=0.0)
    control_indicator: Mapped[str | None] = mapped_column(String(15))  # MAJ-VOTE, BOARD, GOLDEN...
    is_ultimate: Mapped[str] = mapped_column(String(1), default="N")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
