"""Standards Repository, Rules Repository, Metadata Repository, the 18 tests,
and reference codelists — the methodological backbone of the platform."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import require
from app.database import get_db
from app.engine.expression import evaluate
from app.models.reference import Codelist, InstitutionalSector, IsicClass, IsicSection, LegalForm, SizeThreshold
from app.models.rules import ClassificationTest, MetadataVariable, Rule, Standard, StandardConcept
from app.schemas import RuleOut

router = APIRouter(prefix="/api", tags=["Repositories"])


# --- Rules Repository ---
@router.get("/rules", response_model=list[RuleOut])
def list_rules(test_code: str | None = None, domain: str | None = None,
               db: Session = Depends(get_db), _=Depends(require("rule:read"))):
    stmt = select(Rule)
    if test_code:
        stmt = stmt.where(Rule.test_code == test_code)
    if domain:
        stmt = stmt.where(Rule.domain == domain)
    return list(db.execute(stmt.order_by(Rule.test_code, Rule.priority)).scalars())


@router.get("/rules/{rule_id}", response_model=RuleOut)
def get_rule(rule_id: str, db: Session = Depends(get_db), _=Depends(require("rule:read"))):
    rule = db.get(Rule, rule_id)
    if not rule:
        raise HTTPException(404, "Rule not found")
    return rule


@router.post("/rules/{rule_id}/test")
def test_rule(rule_id: str, facts: dict, db: Session = Depends(get_db), _=Depends(require("rule:read"))):
    """Evaluate a single rule's logic against a supplied fact set (rule testing)."""
    rule = db.get(Rule, rule_id)
    if not rule:
        raise HTTPException(404, "Rule not found")
    matched = evaluate(rule.logic, facts)
    return {"rule_id": rule_id, "matched": matched,
            "output": rule.output if matched else None,
            "rationale": rule.rationale, "standard_ref": rule.standard_ref}


# --- 18 Classification Tests ---
@router.get("/tests")
def list_tests(db: Session = Depends(get_db), _=Depends(require("metadata:read"))):
    tests = db.execute(select(ClassificationTest).order_by(ClassificationTest.seq)).scalars().all()
    return [{"test_code": t.test_code, "seq": t.seq, "name": t.name, "phase": t.phase,
             "output_dimension": t.output_dimension, "description": t.description,
             "standard_ref": t.standard_ref} for t in tests]


# --- Standards Repository ---
@router.get("/standards")
def list_standards(db: Session = Depends(get_db), _=Depends(require("metadata:read"))):
    out = []
    for s in db.execute(select(Standard)).scalars().all():
        concepts = db.execute(select(StandardConcept).where(StandardConcept.standard_code == s.code)).scalars().all()
        out.append({"code": s.code, "name": s.name, "issuer": s.issuer, "edition": s.edition,
                    "description": s.description, "domains": s.domains,
                    "concepts": [{"concept": c.concept, "definition": c.definition, "reference": c.reference}
                                 for c in concepts]})
    return out


# --- Metadata Repository ---
@router.get("/metadata")
def list_metadata(entity: str | None = None, db: Session = Depends(get_db), _=Depends(require("metadata:read"))):
    stmt = select(MetadataVariable)
    if entity:
        stmt = stmt.where(MetadataVariable.entity == entity)
    return [{"entity": m.entity, "field": m.field, "definition": m.definition, "data_type": m.data_type,
             "allowed_values": m.allowed_values, "mandatory": m.mandatory, "source": m.source,
             "standard_ref": m.standard_ref, "version": m.version, "example": m.example}
            for m in db.execute(stmt.order_by(MetadataVariable.entity, MetadataVariable.field)).scalars()]


# --- Reference codelists ---
@router.get("/reference/sectors")
def sectors(db: Session = Depends(get_db), _=Depends(require("metadata:read"))):
    return [{"code": s.code, "name_en": s.name_en, "name_ar": s.name_ar, "parent_code": s.parent_code,
             "definition": s.definition} for s in db.execute(select(InstitutionalSector)).scalars()]


@router.get("/reference/legal-forms")
def legal_forms(db: Session = Depends(get_db), _=Depends(require("metadata:read"))):
    return [{"code": lf.code, "name_en": lf.name_en, "name_ar": lf.name_ar, "notes": lf.notes}
            for lf in db.execute(select(LegalForm)).scalars()]


@router.get("/reference/isic")
def isic(section: str | None = None, db: Session = Depends(get_db), _=Depends(require("metadata:read"))):
    stmt = select(IsicClass)
    if section:
        stmt = stmt.where(IsicClass.section_code == section)
    return [{"code": c.code, "activity_en": c.activity_en, "section_code": c.section_code,
             "nace": c.nace, "gcc_sic": c.gcc_sic} for c in db.execute(stmt).scalars()]


@router.get("/reference/codelist/{domain}")
def codelist(domain: str, db: Session = Depends(get_db), _=Depends(require("metadata:read"))):
    return [{"code": c.code, "meaning": c.meaning}
            for c in db.execute(select(Codelist).where(Codelist.domain == domain)
                                .order_by(Codelist.sort_order)).scalars()]


@router.get("/reference/size-thresholds")
def size_thresholds(db: Session = Depends(get_db), _=Depends(require("metadata:read"))):
    return [{"size_class": s.size_class, "turnover_min": s.turnover_min, "turnover_max": s.turnover_max,
             "fte_min": s.fte_min, "fte_max": s.fte_max} for s in db.execute(select(SizeThreshold)).scalars()]
