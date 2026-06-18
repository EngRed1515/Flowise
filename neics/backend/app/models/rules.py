"""Standards Repository, Statistical Metadata Repository, and the database-driven
Rules Repository. Rules are data, never hard-coded (per framework requirement)."""
from datetime import date, datetime

from sqlalchemy import JSON, Boolean, Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Standard(Base):
    """International / national statistical standards the framework is anchored to."""

    __tablename__ = "std_standard"

    code: Mapped[str] = mapped_column(String(40), primary_key=True)  # e.g. SNA2025, GFS2014, BD4
    name: Mapped[str] = mapped_column(String(300))
    issuer: Mapped[str | None] = mapped_column(String(200))
    edition: Mapped[str | None] = mapped_column(String(40))
    description: Mapped[str | None] = mapped_column(Text)
    url: Mapped[str | None] = mapped_column(String(400))
    domains: Mapped[str | None] = mapped_column(String(300))  # comma-separated statistical domains


class StandardConcept(Base):
    """Concepts / definitions belonging to a standard (Standards Repository)."""

    __tablename__ = "std_concept"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    standard_code: Mapped[str] = mapped_column(ForeignKey("std_standard.code"))
    concept: Mapped[str] = mapped_column(String(200))
    definition: Mapped[str] = mapped_column(Text)
    reference: Mapped[str | None] = mapped_column(String(200))  # paragraph / chapter reference


class MetadataVariable(Base):
    """Statistical Metadata Repository — variable catalog (GSIM/SDMX aligned).

    Mirrors workbook sheet 11 plus full GSIM-style metadata.
    """

    __tablename__ = "meta_variable"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    entity: Mapped[str] = mapped_column(String(60))  # table / dataset
    field: Mapped[str] = mapped_column(String(60))
    definition: Mapped[str] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    methodology: Mapped[str | None] = mapped_column(Text)
    data_type: Mapped[str | None] = mapped_column(String(40))
    allowed_values: Mapped[str | None] = mapped_column(String(200))
    mandatory: Mapped[bool] = mapped_column(Boolean, default=False)
    source: Mapped[str | None] = mapped_column(String(120))
    standard_ref: Mapped[str | None] = mapped_column(String(120))
    related_domains: Mapped[str | None] = mapped_column(String(300))
    effective_date: Mapped[date | None] = mapped_column(Date)
    version: Mapped[str] = mapped_column(String(10), default="1.0.0")
    example: Mapped[str | None] = mapped_column(String(200))


class Rule(Base):
    """A single configurable classification rule (Rules Repository).

    The `logic` column holds a JSON condition tree evaluated by the rules engine
    against the fact set of an enterprise. The `output` column declares the
    attribute/value assigned when the rule fires. Rules belong to a `test_code`
    (one of the 18 tests) and a `domain` (output dimension).
    """

    __tablename__ = "rule"

    rule_id: Mapped[str] = mapped_column(String(40), primary_key=True)  # e.g. R-T07-001
    name: Mapped[str] = mapped_column(String(300))
    description: Mapped[str | None] = mapped_column(Text)
    test_code: Mapped[str] = mapped_column(String(10), index=True)  # T1..T18
    domain: Mapped[str] = mapped_column(String(40), index=True)  # output dimension
    inputs_required: Mapped[list | None] = mapped_column(JSON)  # list of fact keys
    logic: Mapped[dict | None] = mapped_column(JSON)  # condition tree
    output: Mapped[dict | None] = mapped_column(JSON)  # {field: value}
    priority: Mapped[int] = mapped_column(Integer, default=100)  # lower = evaluated first
    confidence: Mapped[float] = mapped_column(default=1.0)
    standard_ref: Mapped[str | None] = mapped_column(String(200))
    rationale: Mapped[str | None] = mapped_column(Text)  # human-readable "why"
    effective_date: Mapped[date | None] = mapped_column(Date)
    expiry_date: Mapped[date | None] = mapped_column(Date)
    version: Mapped[str] = mapped_column(String(10), default="1.0.0")
    author: Mapped[str | None] = mapped_column(String(120))
    approval_status: Mapped[str] = mapped_column(String(20), default="APPROVED")  # DRAFT/APPROVED/RETIRED
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class ClassificationTest(Base):
    """Catalogue of the 18 sequenced classification tests (framework Part III)."""

    __tablename__ = "classification_test"

    test_code: Mapped[str] = mapped_column(String(10), primary_key=True)  # T1..T18
    seq: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(200))
    phase: Mapped[str | None] = mapped_column(String(60))  # A.UNIT&RESIDENCE etc.
    output_dimension: Mapped[str | None] = mapped_column(String(60))
    description: Mapped[str | None] = mapped_column(Text)
    standard_ref: Mapped[str | None] = mapped_column(String(200))
