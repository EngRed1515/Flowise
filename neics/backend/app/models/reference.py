"""Reference / master codelist tables.

These mirror the codelists in the implementation workbook (sheets 06, 07, 08, 08b,
10) and form the controlled vocabularies that every classification is traced to.
All are versionable and standard-referenced.
"""
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class InstitutionalSector(Base):
    """SNA 2008/2025 institutional sectors and sub-sectors (workbook sheet 06)."""

    __tablename__ = "ref_institutional_sector"

    code: Mapped[str] = mapped_column(String(10), primary_key=True)  # e.g. S.11, S.122
    name_en: Mapped[str] = mapped_column(String(200))
    name_ar: Mapped[str | None] = mapped_column(String(200))
    parent_code: Mapped[str | None] = mapped_column(String(10))
    definition: Mapped[str | None] = mapped_column(Text)
    standard_ref: Mapped[str] = mapped_column(String(100), default="SNA 2008/2025")


class LegalForm(Base):
    """Qatar legal forms (workbook sheet 07)."""

    __tablename__ = "ref_legal_form"

    code: Mapped[str] = mapped_column(String(10), primary_key=True)
    name_en: Mapped[str] = mapped_column(String(200))
    name_ar: Mapped[str | None] = mapped_column(String(200))
    notes: Mapped[str | None] = mapped_column(Text)


class IsicSection(Base):
    """ISIC Rev.4 sections (A-U) — workbook sheet 08b."""

    __tablename__ = "ref_isic_section"

    code: Mapped[str] = mapped_column(String(1), primary_key=True)
    title_en: Mapped[str] = mapped_column(String(300))
    title_ar: Mapped[str | None] = mapped_column(String(300))


class IsicDivision(Base):
    """ISIC Rev.4 divisions (workbook sheet 08b)."""

    __tablename__ = "ref_isic_division"

    code: Mapped[str] = mapped_column(String(2), primary_key=True)
    section_code: Mapped[str] = mapped_column(ForeignKey("ref_isic_section.code"))
    title_en: Mapped[str] = mapped_column(String(400))
    title_ar: Mapped[str | None] = mapped_column(String(400))


class IsicClass(Base):
    """ISIC Rev.4 classes with cross-walks (workbook sheet 08)."""

    __tablename__ = "ref_isic_class"

    code: Mapped[str] = mapped_column(String(4), primary_key=True)  # 4-digit class
    section_code: Mapped[str] = mapped_column(String(1))
    activity_en: Mapped[str] = mapped_column(String(400))
    activity_ar: Mapped[str | None] = mapped_column(String(400))
    nace: Mapped[str | None] = mapped_column(String(20))
    gcc_sic: Mapped[str | None] = mapped_column(String(20))


class Codelist(Base):
    """Generic auxiliary codelists (workbook sheet 10 reference tables).

    domain examples: residence, public_private, control_indicator, demographic_event,
    fdi_flag, size_class, quality_flag.
    """

    __tablename__ = "ref_codelist"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    domain: Mapped[str] = mapped_column(String(60), index=True)
    code: Mapped[str] = mapped_column(String(40), index=True)
    meaning: Mapped[str] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)


class SizeThreshold(Base):
    """Enterprise size thresholds (workbook sheet 10 / slide 28)."""

    __tablename__ = "ref_size_threshold"

    size_class: Mapped[str] = mapped_column(String(20), primary_key=True)
    turnover_min: Mapped[float | None] = mapped_column(Float)
    turnover_max: Mapped[float | None] = mapped_column(Float)
    fte_min: Mapped[int | None] = mapped_column(Integer)
    fte_max: Mapped[int | None] = mapped_column(Integer)
