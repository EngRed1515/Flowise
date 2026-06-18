"""Validation Engine — implements the business-rule library from workbook sheet 09
(VR-001..VR-018) plus cross-field / cross-source / ownership checks."""
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.enterprise import Enterprise, EnterpriseGroup, LegalUnit, OwnershipEdge
from app.models.reference import IsicClass, InstitutionalSector, LegalForm

FINANCIAL_SUBSECTORS = {f"S.12{n}" for n in range(1, 10)} | {"S.12"}


def validate_enterprise(db: Session, ent: Enterprise) -> list[dict[str, Any]]:
    """Return a list of validation findings for one enterprise."""
    issues: list[dict[str, Any]] = []

    def add(rule_id, severity, message, action):
        issues.append({"rule_id": rule_id, "severity": severity, "message": message, "action": action})

    # VR-001 sector code valid
    if ent.sector_code and not db.get(InstitutionalSector, ent.sector_code):
        add("VR-001", "ERROR", f"Sector code {ent.sector_code} not in codelist", "Reject record")
    # VR-002 ISIC class valid
    if ent.isic_class and not db.get(IsicClass, ent.isic_class):
        add("VR-002", "ERROR", f"ISIC class {ent.isic_class} not in codelist", "Reject record")
    # VR-003 legal form valid
    if ent.legal_form_code and not db.get(LegalForm, ent.legal_form_code):
        add("VR-003", "ERROR", f"Legal form {ent.legal_form_code} not in codelist", "Reject record")
    # VR-004 LEI format
    if ent.lei and len(ent.lei) != 20:
        add("VR-004", "WARN", "LEI is not a 20-char ISO 17442 identifier", "Flag for review")
    # VR-005 ownership chain sums <= 100
    rows = db.execute(
        select(OwnershipEdge.owned_id, func.sum(OwnershipEdge.ownership_pct))
        .where(OwnershipEdge.owned_id == ent.enterprise_id)
        .group_by(OwnershipEdge.owned_id)
    ).all()
    for _, total in rows:
        if total and total > 100.01:
            add("VR-005", "ERROR", f"Ownership percentages sum to {total} (>100)", "Flag conflict")
    # VR-006 public-sector entities must carry a control flag.
    # Exemption: a core government body (legal_form GOV) is intrinsically government —
    # the control test applies to public corporations and reclassified controlled units.
    if (
        ent.public_private in ("PUB-NFC", "PUB-FC", "GG")
        and ent.legal_form_code != "GOV"
        and (not ent.control_flag or ent.control_flag == "NONE")
    ):
        add("VR-006", "ERROR", "Public-sector entity has no effective-control flag", "Flag for review")
    # VR-007 financial sector should map to ISIC section K
    if ent.sector_code in FINANCIAL_SUBSECTORS and ent.isic_class:
        isic = db.get(IsicClass, ent.isic_class)
        if isic and isic.section_code != "K":
            add("VR-007", "WARN", "Financial-sector entity with non-section-K ISIC", "Flag for review")
    # VR-008 residence required
    if ent.residence not in ("RES", "NRES", "MULTI"):
        add("VR-008", "ERROR", "Residence must be RES, NRES or MULTI", "Reject record")
    # VR-009 death after birth
    if ent.death_date and ent.birth_date and ent.death_date < ent.birth_date:
        add("VR-009", "ERROR", "death_date precedes birth_date", "Reject record")
    # VR-010 group reference exists
    if ent.group_id and not db.get(EnterpriseGroup, ent.group_id):
        add("VR-010", "ERROR", f"group_id {ent.group_id} not found", "Flag conflict")
    # VR-011 dormant detection
    if (ent.employment or 0) == 0 and (ent.turnover_qar or 0) == 0:
        add("VR-011", "INFO", "No employment and no turnover — possible dormant unit", "Schedule review")
    # VR-013 size-revenue consistency (light check)
    if ent.size_class == "LARGE" and (ent.employment or 0) < 50 and (ent.turnover_qar or 0) < 20_000_000:
        add("VR-013", "WARN", "Size class LARGE inconsistent with employment/turnover", "Flag for review")
    # VR-014 duplicate detection (name + cr_number across legal units)
    if ent.legal_units:
        for lu in ent.legal_units:
            dupes = db.execute(
                select(func.count())
                .select_from(LegalUnit)
                .where(LegalUnit.legal_name_en == lu.legal_name_en, LegalUnit.cr_number == lu.cr_number)
            ).scalar_one()
            if dupes > 1:
                add("VR-014", "WARN", f"Duplicate legal unit (name+CR): {lu.legal_name_en}", "Flag for merge")
                break
    # VR-015 empty-shell substance
    if not (ent.has_premises or ent.has_employees or ent.has_autonomy):
        add("VR-015", "INFO", "No premises/employees/autonomy — apply Test 13 substance rule", "Consolidate with parent")
    # VR-012 hidden government ownership — material effective state stake vs private status
    from app.engine.ownership import OwnershipEngine

    gov_own = OwnershipEngine(db).government_ownership(ent.enterprise_id)
    if gov_own > 0 and ent.public_private in ("PRV-NFC", "PRV-FC", "FCC"):
        add("VR-012", "WARN", f"Effective government ownership {gov_own}% but classified "
            f"{ent.public_private} — cross-check against state-vehicle list", "Flag for review")

    # VR-016 demographic / classification change must have an audit-trail entry
    if ent.classification_date is not None:
        from app.models.governance import AuditEntry

        has_audit = db.execute(
            select(func.count()).select_from(AuditEntry)
            .where(AuditEntry.record_id == ent.enterprise_id,
                   AuditEntry.action.in_(["CLASSIFY", "OVERRIDE", "UPDATE", "CREATE"]))
        ).scalar_one()
        if not has_audit:
            add("VR-016", "ERROR", "Classified record has no audit-trail entry", "Reject change")

    # VR-017 classification version set on commit
    if ent.quality_flag != "DRAFT" and not ent.classification_version:
        add("VR-017", "ERROR", "Committed record missing classification_version", "Reject record")

    # VR-018 quality-flag must be a valid progression state
    if ent.quality_flag not in ("DRAFT", "PEER-REVIEWED", "COMMITTEE-RULED"):
        add("VR-018", "WARN", f"Invalid quality flag '{ent.quality_flag}' "
            "(allowed progression DRAFT → PEER-REVIEWED → COMMITTEE-RULED)", "Flag for review")

    return issues
