"""Assemble the flat fact set for an enterprise.

The fact set is the single input contract for the rules engine. It is recorded
alongside every classification (data provenance / explainability).
"""
from typing import Any

from sqlalchemy.orm import Session

from app.engine.ownership import OwnershipEngine
from app.models.enterprise import Enterprise


def build_facts(db: Session, ent: Enterprise) -> dict[str, Any]:
    own = OwnershipEngine(db).facts(ent.enterprise_id)

    sales = ent.sales or 0.0
    costs = ent.production_costs or 0.0
    sales_ratio = (sales / costs) if costs > 0 else None

    facts: dict[str, Any] = {
        "enterprise_id": ent.enterprise_id,
        "legal_form_code": ent.legal_form_code,
        "residence": ent.residence,
        "isic_class": ent.isic_class,
        "isic_section": (ent.isic_class or "")[:2],  # placeholder; resolved via codelist elsewhere
        "employment": ent.employment or 0,
        "turnover_qar": ent.turnover_qar or 0.0,
        "total_assets_qar": ent.total_assets_qar or 0.0,
        "sales": sales,
        "production_costs": costs,
        "sales_to_cost_ratio": sales_ratio,
        "sales_cover_pct": (sales_ratio * 100.0) if sales_ratio is not None else None,
        "is_nonprofit": ent.is_nonprofit,
        "is_financial": ent.is_financial,
        "has_premises": ent.has_premises,
        "has_employees": ent.has_employees,
        "has_autonomy": ent.has_autonomy,
        "jurisdiction": ent.jurisdiction,
        "has_substance": bool(ent.has_premises or ent.has_employees or ent.has_autonomy),
    }
    facts.update(own)
    return facts
