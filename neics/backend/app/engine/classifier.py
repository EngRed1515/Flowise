"""Classification orchestrator — runs the 18-test pipeline using database-driven
rules and produces a fully explainable, traceable result.

Conflict resolution (framework Test 15) is implemented as first-match-by-priority
within each test (lower `priority` value evaluated first). Outputs of earlier
tests are folded back into the fact set so later tests can chain on them.
"""
from datetime import date
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.engine.expression import evaluate
from app.engine.facts import build_facts
from app.models.enterprise import Enterprise
from app.models.rules import ClassificationTest, Rule

# Dimensions that constitute the final classification key.
RESULT_FIELDS = [
    "residence",
    "isic_class",
    "sector_code",
    "market_status",
    "control_flag",
    "public_private",
    "size_class",
    "fdi_flag",
    "special_entity_flag",
]


def _resolve_output(spec: Any, facts: dict) -> Any:
    """Resolve an output spec: {"const": X} or {"fact": "name"} (or a bare value)."""
    if isinstance(spec, dict):
        if "const" in spec:
            return spec["const"]
        if "fact" in spec:
            return facts.get(spec["fact"])
    return spec


def classify(db: Session, ent: Enterprise) -> dict[str, Any]:
    facts = build_facts(db, ent)
    result: dict[str, Any] = {}
    trace: list[dict] = []
    confidences: list[float] = []

    tests = db.execute(select(ClassificationTest).order_by(ClassificationTest.seq)).scalars().all()
    today = date.today()

    for test in tests:
        rules = (
            db.execute(
                select(Rule)
                .where(Rule.test_code == test.test_code, Rule.is_active.is_(True))
                .order_by(Rule.priority)
            )
            .scalars()
            .all()
        )
        rules = [
            r
            for r in rules
            if (r.effective_date is None or r.effective_date <= today)
            and (r.expiry_date is None or r.expiry_date >= today)
            and r.approval_status == "APPROVED"
        ]

        fired = None
        for rule in rules:
            if evaluate(rule.logic, facts):
                fired = rule
                applied = {}
                for field, spec in (rule.output or {}).items():
                    val = _resolve_output(spec, facts)
                    facts[field] = val
                    if field in RESULT_FIELDS:
                        result[field] = val
                    applied[field] = val
                confidences.append(rule.confidence)
                trace.append(
                    {
                        "test_code": test.test_code,
                        "test_name": test.name,
                        "matched": True,
                        "rule_id": rule.rule_id,
                        "rule_name": rule.name,
                        "output": applied,
                        "confidence": rule.confidence,
                        "standard_ref": rule.standard_ref,
                        "rationale": rule.rationale,
                    }
                )
                break

        if fired is None:
            trace.append(
                {
                    "test_code": test.test_code,
                    "test_name": test.name,
                    "matched": False,
                    "note": "No active rule fired; dimension left unchanged.",
                }
            )

    overall_conf = round(sum(confidences) / len(confidences), 3) if confidences else None
    return {
        "result": result,
        "trace": trace,
        "facts": facts,
        "confidence": overall_conf,
    }
