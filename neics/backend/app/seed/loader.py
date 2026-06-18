"""Idempotent seed loader. Populates reference data, standards, the 18 tests, the
rules repository, sample/test enterprises, ownership graph, and RBAC users.

Reference + sample data is read from the JSON files under neics/data (extracted
faithfully from the implementation workbook). Platform definitions come from
app.seed.definitions.
"""
import json
import os
from datetime import date, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.enterprise import Enterprise, EnterpriseGroup, Establishment, LegalUnit, OwnershipEdge
from app.models.governance import User
from app.models.reference import (
    Codelist,
    InstitutionalSector,
    IsicClass,
    IsicDivision,
    IsicSection,
    LegalForm,
    SizeThreshold,
)
from app.models.rules import ClassificationTest, MetadataVariable, Rule, Standard, StandardConcept
from app.seed import definitions as D

# neics/data directory (three levels up from this file: app/seed -> app -> backend -> neics)
DATA_DIR = os.environ.get(
    "NEICS_DATA_DIR",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data")),
)


def _load(name: str):
    with open(os.path.join(DATA_DIR, f"{name}.json"), encoding="utf-8") as f:
        return json.load(f)


def _date(v):
    if not v:
        return None
    try:
        return date.fromisoformat(str(v)[:10])
    except ValueError:
        return None


def _dt(v):
    if not v:
        return None
    try:
        return datetime.fromisoformat(str(v)[:19].replace(" ", "T"))
    except ValueError:
        return None


def seed_reference(db: Session) -> None:
    if db.execute(select(func.count()).select_from(InstitutionalSector)).scalar_one() == 0:
        db.add_all(InstitutionalSector(**r) for r in _load("ref_sectors"))
    if db.execute(select(func.count()).select_from(LegalForm)).scalar_one() == 0:
        db.add_all(LegalForm(**r) for r in _load("ref_legal_forms"))
    if db.execute(select(func.count()).select_from(IsicSection)).scalar_one() == 0:
        db.add_all(IsicSection(**r) for r in _load("ref_isic_sections"))
    if db.execute(select(func.count()).select_from(IsicDivision)).scalar_one() == 0:
        db.add_all(IsicDivision(**r) for r in _load("ref_isic_divisions"))
    if db.execute(select(func.count()).select_from(IsicClass)).scalar_one() == 0:
        db.add_all(IsicClass(**r) for r in _load("ref_isic_classes"))
    if db.execute(select(func.count()).select_from(Codelist)).scalar_one() == 0:
        db.add_all(Codelist(**r) for r in _load("ref_codelists"))
    if db.execute(select(func.count()).select_from(SizeThreshold)).scalar_one() == 0:
        db.add_all(SizeThreshold(**r) for r in _load("ref_size_thresholds"))
    db.commit()


def seed_standards_and_tests(db: Session) -> None:
    if db.execute(select(func.count()).select_from(Standard)).scalar_one() == 0:
        db.add_all(Standard(**s) for s in D.STANDARDS)
        db.add_all(StandardConcept(**c) for c in D.CONCEPTS)
    if db.execute(select(func.count()).select_from(ClassificationTest)).scalar_one() == 0:
        for code, seq, name, phase, dim, desc, std in D.TESTS:
            db.add(ClassificationTest(test_code=code, seq=seq, name=name, phase=phase,
                                      output_dimension=dim, description=desc, standard_ref=std))
    db.commit()


def seed_rules(db: Session) -> None:
    if db.execute(select(func.count()).select_from(Rule)).scalar_one() == 0:
        for r in D.RULES:
            db.add(Rule(**r))
    db.commit()


def seed_metadata(db: Session) -> None:
    if db.execute(select(func.count()).select_from(MetadataVariable)).scalar_one() == 0:
        for m in _load("metadata_variables"):
            db.add(MetadataVariable(
                entity=m["entity"], field=m["field"], definition=m["definition"],
                data_type=m.get("data_type"), allowed_values=m.get("allowed_values"),
                mandatory=bool(m.get("mandatory")), source=m.get("source"),
                example=m.get("example"), standard_ref="GSIM/SDMX", version="1.0.0",
                effective_date=date(2026, 1, 1),
            ))
    db.commit()


def seed_users(db: Session) -> None:
    if db.execute(select(func.count()).select_from(User)).scalar_one() == 0:
        for username, full_name, role in D.USERS:
            db.add(User(username=username, full_name=full_name, role=role,
                        email=f"{username}@nso.gov.qa",
                        hashed_password=hash_password(f"{username}123")))
    db.commit()


def seed_enterprises(db: Session) -> None:
    if db.execute(select(func.count()).select_from(Enterprise)).scalar_one() > 0:
        return
    # Workbook sample groups + the expanded UAT dataset groups.
    for g in _load("sample_groups") + _load("uat_groups"):
        db.add(EnterpriseGroup(**g))
    db.commit()

    for e in _load("sample_enterprises") + _load("uat_enterprises"):
        rec = dict(e)
        rec["birth_date"] = _date(rec.get("birth_date"))
        rec["death_date"] = _date(rec.get("death_date"))
        rec["classification_date"] = _dt(rec.get("classification_date"))
        db.add(Enterprise(**rec))
    db.commit()

    for lu in _load("sample_legal_units"):
        rec = dict(lu)
        rec["registration_date"] = _date(rec.get("registration_date"))
        rec["ceased_date"] = _date(rec.get("ceased_date"))
        db.add(LegalUnit(**rec))
    for est in _load("sample_establishments"):
        db.add(Establishment(**est))
    for edge in _load("sample_ownership") + _load("uat_ownership"):
        db.add(OwnershipEdge(**edge))
    db.commit()


def seed_all(db: Session) -> None:
    seed_reference(db)
    seed_standards_and_tests(db)
    seed_rules(db)
    seed_metadata(db)
    seed_users(db)
    seed_enterprises(db)
