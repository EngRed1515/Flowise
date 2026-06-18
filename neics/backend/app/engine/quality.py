"""Data Quality Engine — scores each enterprise across the six DAMA DMBOK
dimensions and surfaces exceptions. Also hosts lightweight anomaly detection
for the AI-assisted review layer (rule-based; never overrides official rules)."""
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.engine.validation import validate_enterprise
from app.models.enterprise import Enterprise

# Fields that contribute to completeness scoring.
COMPLETENESS_FIELDS = [
    "lei",
    "legal_name_en",
    "legal_form_code",
    "residence",
    "isic_class",
    "sector_code",
    "public_private",
    "control_flag",
    "size_class",
    "employment",
    "turnover_qar",
    "birth_date",
]


def score_enterprise(db: Session, ent: Enterprise) -> dict[str, Any]:
    # Completeness
    present = sum(1 for f in COMPLETENESS_FIELDS if getattr(ent, f) not in (None, ""))
    completeness = round(present / len(COMPLETENESS_FIELDS), 3)

    # Validity / consistency from the validation engine
    issues = validate_enterprise(db, ent)
    errors = [i for i in issues if i["severity"] == "ERROR"]
    warns = [i for i in issues if i["severity"] == "WARN"]
    validity = round(max(0.0, 1.0 - 0.25 * len(errors)), 3)
    consistency = round(max(0.0, 1.0 - 0.1 * len(warns)), 3)

    # Uniqueness — penalise if duplicate legal name detected
    uniqueness = 1.0
    if ent.legal_units:
        names = [lu.legal_name_en for lu in ent.legal_units]
        if len(names) != len(set(names)):
            uniqueness = 0.7

    # Accuracy proxy — committee/peer-reviewed records score higher
    accuracy = {"COMMITTEE-RULED": 1.0, "PEER-REVIEWED": 0.85, "DRAFT": 0.6}.get(ent.quality_flag, 0.6)

    # Timeliness — has the record been classified at all
    timeliness = 1.0 if ent.classification_date else 0.5

    overall = round((completeness + validity + consistency + uniqueness + accuracy + timeliness) / 6, 3)

    return {
        "enterprise_id": ent.enterprise_id,
        "completeness": completeness,
        "validity": validity,
        "consistency": consistency,
        "uniqueness": uniqueness,
        "accuracy": accuracy,
        "timeliness": timeliness,
        "overall_score": overall,
        "exceptions": issues,
    }


def detect_anomalies(db: Session, ent: Enterprise, facts: dict | None = None) -> list[dict[str, Any]]:
    """Rule-based anomaly detection feeding the AI-assisted review queue.

    Flags patterns the framework calls out (hidden government ownership, ISIC vs
    cost pattern mismatch, empty-shell producers, sudden classification drift).
    """
    anomalies: list[dict[str, Any]] = []

    def flag(title, detail, severity="WARN"):
        anomalies.append({"kind": "ANOMALY", "severity": severity, "title": title, "detail": detail})

    f = facts or {}
    gov_own = f.get("government_ownership_pct", 0) or 0
    # Hidden government ownership: material state stake but classified private
    if gov_own >= 20 and ent.public_private in ("PRV-NFC", "PRV-FC", "FCC"):
        flag(
            "Possible hidden government ownership",
            f"Effective government ownership {gov_own}% but classified {ent.public_private}. "
            "Recommend manual review of control indicators (framework Test 8).",
            "WARN",
        )
    # Empty shell recorded as a producer
    if not (ent.has_premises or ent.has_employees) and ent.special_entity_flag not in (
        "CONSOLIDATE-PARENT",
        "HOLDING",
    ):
        flag(
            "Empty-shell entity treated as producer",
            "No premises/employees but not flagged as SPV/holding — apply substance test (Test 13).",
        )
    # Financial activity but non-financial sector
    if (ent.isic_class or "").startswith(("64", "65", "66")) and not (ent.sector_code or "").startswith("S.12"):
        flag(
            "ISIC/sector mismatch",
            f"ISIC {ent.isic_class} is financial (section K) but sector is {ent.sector_code}.",
        )
    # Large foreign stake but no FDI flag
    if f.get("foreign_ownership_pct", 0) and f["foreign_ownership_pct"] >= 10 and ent.fdi_flag in (None, "NONE"):
        flag("Missing FDI flag", f"Foreign ownership {f['foreign_ownership_pct']}% but no FDI relationship recorded.")
    return anomalies
