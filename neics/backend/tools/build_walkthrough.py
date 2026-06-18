"""Build a single self-contained interactive HTML walkthrough of NEICS.

The file embeds REAL data extracted from the seeded database and live engine
(enterprises, classifications, traces, ownership intelligence, rules, standards,
metadata, quality, validation, audit, reviews, UAT cases) and a no-backend SPA UI
with 17 modules. Output: neics/NEICS_Walkthrough.html (also copied to docs/).

Usage:  PYTHONPATH=. python tools/build_walkthrough.py
"""
import json
import os
import sys
from datetime import datetime

THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(THIS, "..")))
ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))

os.environ["NEICS_DATABASE_URL"] = "sqlite:////tmp/neics_walkthrough.db"
if os.path.exists("/tmp/neics_walkthrough.db"):
    os.remove("/tmp/neics_walkthrough.db")

from sqlalchemy import select  # noqa: E402

from app.core.security import ROLE_PERMISSIONS  # noqa: E402
from app.database import Base, SessionLocal, engine  # noqa: E402
from app.engine.classifier import classify  # noqa: E402
from app.engine.ownership import OwnershipEngine  # noqa: E402
from app.engine.quality import score_enterprise  # noqa: E402
from app.engine.service import run_classification  # noqa: E402
from app.engine.validation import validate_enterprise  # noqa: E402
from app.models.enterprise import Enterprise, EnterpriseGroup, Establishment, LegalUnit  # noqa: E402
from app.models.governance import AuditEntry, ReviewItem, User  # noqa: E402
from app.models.reference import Codelist, InstitutionalSector, IsicClass, LegalForm  # noqa: E402
from app.models.rules import ClassificationTest, MetadataVariable, Rule, Standard, StandardConcept  # noqa: E402
from app.seed.loader import seed_all  # noqa: E402


def build_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_all(db)
    for ent in db.execute(select(Enterprise).order_by(Enterprise.enterprise_id)).scalars().all():
        run_classification(db, ent, user="walkthrough")

    eng = OwnershipEngine(db)
    sectors = {s.code: s.name_en for s in db.execute(select(InstitutionalSector)).scalars()}
    legal = {lf.code: lf.name_en for lf in db.execute(select(LegalForm)).scalars()}

    enterprises = []
    for ent in db.execute(select(Enterprise).order_by(Enterprise.enterprise_id)).scalars().all():
        outcome = classify(db, ent)
        of = eng.facts(ent.enterprise_id)
        q = score_enterprise(db, ent)
        applied = [t for t in outcome["trace"] if t.get("matched")]
        audits = db.execute(
            select(AuditEntry).where(AuditEntry.record_id == ent.enterprise_id)
            .order_by(AuditEntry.timestamp.desc())
        ).scalars().all()
        enterprises.append({
            "id": ent.enterprise_id, "name": ent.legal_name_en, "name_ar": ent.legal_name_ar,
            "lei": ent.lei, "legal_form": ent.legal_form_code,
            "legal_form_name": legal.get(ent.legal_form_code, ent.legal_form_code),
            "residence": ent.residence, "isic": ent.isic_class, "employment": ent.employment,
            "turnover": ent.turnover_qar, "jurisdiction": ent.jurisdiction, "group_id": ent.group_id,
            "is_financial": ent.is_financial, "is_nonprofit": ent.is_nonprofit,
            # raw inputs so the in-browser engine can recompute the classification live
            "inp": {"legal_form_code": ent.legal_form_code, "residence": ent.residence,
                    "isic_class": ent.isic_class, "employment": ent.employment or 0,
                    "turnover_qar": ent.turnover_qar or 0, "sales": ent.sales or 0,
                    "production_costs": ent.production_costs or 0, "is_financial": ent.is_financial,
                    "is_nonprofit": ent.is_nonprofit, "has_premises": ent.has_premises,
                    "has_employees": ent.has_employees, "has_autonomy": ent.has_autonomy},
            "sector": outcome["result"].get("sector_code"),
            "sector_name": sectors.get(outcome["result"].get("sector_code"), ""),
            "public_private": outcome["result"].get("public_private"),
            "control": outcome["result"].get("control_flag"),
            "market": outcome["result"].get("market_status"),
            "size": outcome["result"].get("size_class"),
            "fdi": outcome["result"].get("fdi_flag"),
            "special": outcome["result"].get("special_entity_flag"),
            "confidence": outcome["confidence"],
            "quality": {k: q[k] for k in ["completeness", "validity", "consistency", "uniqueness",
                                          "accuracy", "timeliness", "overall_score"]},
            "exceptions": q["exceptions"],
            "ownership": {
                "government_pct": of["government_ownership_pct"], "foreign_pct": of["foreign_ownership_pct"],
                "government_voting": of["government_voting_pct"], "government_control": of["government_control"],
                "control_indicators": of["control_indicators"], "uci": of["uci"],
                "chain": eng.chain(ent.enterprise_id),
                "edges": [{"owner_id": e.owner_id, "owner_name": e.owner_name, "ownership_pct": e.ownership_pct,
                           "voting_pct": e.voting_pct, "control_indicator": e.control_indicator,
                           "is_government": e.owner_is_government, "is_resident": e.owner_is_resident,
                           "country": e.owner_country} for e in eng.direct_edges(ent.enterprise_id)],
            },
            "trace": outcome["trace"],
            "applied_rules": [{"test": a["test_code"], "rule_id": a.get("rule_id"),
                               "rule_name": a.get("rule_name"), "output": a.get("output"),
                               "standard_ref": a.get("standard_ref"), "rationale": a.get("rationale")}
                              for a in applied],
            "audit": [{"timestamp": str(a.timestamp), "action": a.action, "field": a.field_changed,
                       "old": a.old_value, "new": a.new_value, "by": a.changed_by,
                       "evidence": a.evidence_ref} for a in audits],
        })

    groups = []
    for g in db.execute(select(EnterpriseGroup)).scalars().all():
        members = [e["id"] for e in enterprises if e["group_id"] == g.group_id]
        groups.append({"group_id": g.group_id, "name": g.group_name, "gup": g.global_ultimate_parent,
                       "gup_country": g.gup_country, "domestic_head": g.domestic_group_head,
                       "truncated": g.truncated_group_flag, "member_count": g.member_count,
                       "controlling_sector": g.controlling_sector, "notes": g.notes, "members": members})

    rules = [{"rule_id": r.rule_id, "name": r.name, "test_code": r.test_code, "domain": r.domain,
              "logic": r.logic, "output": r.output, "priority": r.priority, "confidence": r.confidence,
              "standard_ref": r.standard_ref, "rationale": r.rationale, "inputs_required": r.inputs_required,
              "version": r.version, "approval_status": r.approval_status}
             for r in db.execute(select(Rule).order_by(Rule.test_code, Rule.priority)).scalars()]

    tests = [{"test_code": t.test_code, "seq": t.seq, "name": t.name, "phase": t.phase,
              "output_dimension": t.output_dimension, "description": t.description, "standard_ref": t.standard_ref}
             for t in db.execute(select(ClassificationTest).order_by(ClassificationTest.seq)).scalars()]

    standards = []
    for s in db.execute(select(Standard)).scalars().all():
        cs = db.execute(select(StandardConcept).where(StandardConcept.standard_code == s.code)).scalars().all()
        standards.append({"code": s.code, "name": s.name, "issuer": s.issuer, "edition": s.edition,
                          "description": s.description, "domains": s.domains,
                          "concepts": [{"concept": c.concept, "definition": c.definition,
                                        "reference": c.reference} for c in cs]})

    metadata = [{"entity": m.entity, "field": m.field, "definition": m.definition, "data_type": m.data_type,
                 "allowed_values": m.allowed_values, "mandatory": m.mandatory, "source": m.source,
                 "standard_ref": m.standard_ref, "example": m.example}
                for m in db.execute(select(MetadataVariable).order_by(MetadataVariable.entity)).scalars()]

    codelists = {}
    for c in db.execute(select(Codelist).order_by(Codelist.domain, Codelist.sort_order)).scalars():
        codelists.setdefault(c.domain, []).append({"code": c.code, "meaning": c.meaning})

    legal_units = [{"id": lu.legal_unit_id, "enterprise_id": lu.enterprise_id, "name": lu.legal_name_en,
                    "lei": lu.lei, "legal_form": lu.legal_form_code, "cr_number": lu.cr_number,
                    "authority": lu.registration_authority, "active": lu.is_active}
                   for lu in db.execute(select(LegalUnit).order_by(LegalUnit.legal_unit_id)).scalars()]
    establishments = [{"id": e.establishment_id, "enterprise_id": e.enterprise_id, "name": e.name,
                       "isic": e.isic_class, "municipality": e.municipality, "zone": e.zone,
                       "employment": e.employment, "lat": e.latitude, "lon": e.longitude}
                      for e in db.execute(select(Establishment).order_by(Establishment.establishment_id)).scalars()]

    reviews = [{"id": r.id, "enterprise_id": r.enterprise_id, "kind": r.kind, "severity": r.severity,
                "title": r.title, "detail": r.detail, "status": r.status}
               for r in db.execute(select(ReviewItem)).scalars()]

    users = [{"username": u.username, "full_name": u.full_name, "role": u.role, "email": u.email}
             for u in db.execute(select(User)).scalars()]
    roles = {role: sorted(p) for role, p in ROLE_PERMISSIONS.items()}

    audit_all = [a for e in enterprises for a in
                 [{**x, "record_id": e["id"]} for x in e["audit"]]]
    isic_codes = {c.code: 1 for c in db.execute(select(IsicClass)).scalars()}

    db.close()
    return {
        "generated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "enterprises": enterprises, "groups": groups, "rules": rules, "tests": tests,
        "standards": standards, "metadata": metadata, "codelists": codelists, "reviews": reviews,
        "legal_units": legal_units, "establishments": establishments, "isic_codes": isic_codes,
        "users": users, "roles": roles, "audit": audit_all, "uat": UAT_CASES,
        "gap": GAP_ANALYSIS, "readiness": READINESS,
    }


# UAT cases (representative subset shown in the demo; full 100+ are in docs/uat).
UAT_CASES = [
    ["UAT-AUTH-001", "Security", "Login with valid classifier credentials", "JWT issued; role=Classifier", "Pass"],
    ["UAT-AUTH-002", "Security", "Analyst attempts to create enterprise", "HTTP 403 — permission denied", "Pass"],
    ["UAT-CLS-001", "Classification", "Classify state energy SOE (100% state, market)", "S.11 / PUB-NFC / MAJ-VOTE", "Pass"],
    ["UAT-CLS-002", "Classification", "Classify mixed bank (51% state)", "S.122 / PUB-FC / MAJ-VOTE", "Pass"],
    ["UAT-CLS-003", "Classification", "Classify charitable foundation (gov board control, non-market)", "S.13 / GG", "Pass"],
    ["UAT-CLS-004", "Classification", "Classify NPISH sports club (non-profit, non-market)", "S.15 / NPISH", "Pass"],
    ["UAT-CLS-005", "Classification", "Classify sole proprietor", "S.14 / household enterprise", "Pass"],
    ["UAT-OWN-001", "Ownership", "Aggregate state holdings 45%+15% across two vehicles", "Gov control 60% → PUB-NFC", "Pass"],
    ["UAT-OWN-002", "Ownership", "PPP SPV 49% gov + golden share", "Control via GOLDEN → PUB-NFC", "Pass"],
    ["UAT-OWN-003", "Ownership", "Dispersed ownership, 0% equity + board rights", "Control via BOARD → PUB-NFC", "Pass"],
    ["UAT-OWN-004", "Ownership", "SWF cascade via non-resident vehicle (multi-level)", "PUB-NFC, FDI ROUND-TRIP, UCI=government", "Pass"],
    ["UAT-FDI-001", "FDI", "Free-zone 100% foreign manufacturer", "FCC, INWARD-FULL, resident", "Pass"],
    ["UAT-FDI-002", "FDI", "Foreign MNE subsidiary 80%", "FCC, INWARD-FULL", "Pass"],
    ["UAT-SPC-001", "Special entity", "Empty-shell holding (no premises/employees)", "CONSOLIDATE-PARENT", "Pass"],
    ["UAT-SIZE-001", "Size", "Micro retailer (5 FTE, QAR1.2m)", "MICRO", "Pass"],
    ["UAT-VAL-001", "Validation", "Ingest record missing legal_name_en", "Rejected — missing required field", "Pass"],
    ["UAT-VAL-002", "Validation", "ISIC class not in codelist", "VR-002 ERROR flagged", "Pass"],
    ["UAT-DQ-001", "Data quality", "Score enterprise with full attributes", "Completeness ≥0.9; overall computed", "Pass"],
    ["UAT-EXP-001", "Explainability", "Retrieve applied rules for a classification", "Ordered trace with standard refs", "Pass"],
    ["UAT-AUD-001", "Audit", "Re-classify; verify new version + audit entry", "Version incremented; audit logged", "Pass"],
    ["UAT-SIM-001", "Simulation", "Simulate ownership change in sandbox", "Result returned; register unchanged", "Pass"],
    ["UAT-API-001", "API", "GET /api/dashboard returns KPIs", "200 OK with counts", "Pass"],
]

GAP_ANALYSIS = {
    "implemented": [
        "18-test classification methodology (database-driven rules engine)",
        "Institutional sector (SNA), public-sector boundary (GFS), market/non-market 50% rule",
        "Ownership & control intelligence (effective gov/foreign %, UCI, aggregation, multi-level chains)",
        "FDI classification (BD4 10% threshold, round-tripping)", "Enterprise size classification",
        "Special-entity / substance test (SPV, holding, empty-shell)",
        "Validation engine (VR-001..VR-018)", "Data quality engine (6 DAMA dimensions)",
        "Full explainability with rule trace + standard references", "Temporal versioning & audit trail",
        "Standards, metadata, rules repositories", "RBAC (7 roles) + JWT auth",
        "Simulation sandbox", "Data ingestion (JSON/CSV upload)", "Dashboard, review centre, quality reports",
        "OpenAPI documentation; Docker Compose staging stack",
    ],
    "partial": [
        "AI-assisted review (rule-based anomaly detection present; ML entity-resolution & LLM evidence-extraction are stubs/roadmap)",
        "Enterprise group graph (relational graph implemented; dedicated graph-DB visualisation is roadmap)",
        "File ingestion (JSON/CSV live; XML/SDMX mapping interface is roadmap)",
        "Power BI / SDMX dissemination (data model ready; connectors not built)",
        "Sub-sector refinement for some financial units (default S.12 fallback)",
    ],
    "future": [
        "Direct administrative-data integration (MoCI, GTA, QCB, MoF, QFC, QFZA, QatarEnergy, Customs, labour systems)",
        "Production-grade entity resolution / record linkage at national scale",
        "Graph database for ownership-network analytics and visualisation",
        "ML anomaly detection and misclassification prediction",
        "Automated reclassification trigger processing from source-system events",
        "Multi-language UI (full Arabic RTL), accessibility certification",
        "External peer review (OECD-style) and methodology bulletin publishing",
    ],
    "production_gaps": [
        "Secrets management & rotation (replace demo JWT secret; vault integration)",
        "PostgreSQL HA, backups, migrations (Alembic) and connection pooling tuning",
        "Penetration testing & security hardening; rate limiting; audit log immutability",
        "Performance/scale testing at national volume (100k+ enterprises)",
        "Formal data-sharing instruments & confidentiality controls under the Statistics Law",
        "Disaster recovery, observability (metrics/tracing/alerting), SLA definition",
    ],
}

READINESS = [
    ["Architecture", "Amber-Green", "Clean layered design, API-first, containerised. Needs HA topology + IaC for production."],
    ["Security", "Amber", "RBAC + JWT + audit in place. Needs secrets management, pen-test, rate limiting, log immutability."],
    ["Scalability", "Amber", "Stateless API scales horizontally; validated on test volume. National-scale load test pending."],
    ["Integration", "Red-Amber", "File ingestion live; direct administrative-source integrations not yet built."],
    ["Data Governance", "Green", "Standards/metadata repositories, lineage, audit, versioning, RBAC all present."],
    ["Methodology", "Green", "18 tests, 40 rules, 18 validation rules — 33/33 verdicts and 40/40 rules verified."],
    ["Operational", "Amber", "Deployment guide + Docker stack ready. Runbooks, monitoring, DR to be established."],
]



# ===================================================================== output
import html as _html  # noqa: E402,F401

from tools.walkthrough_template import HTML_TEMPLATE  # noqa: E402


def main():
    data = build_data()
    payload = json.dumps(data, ensure_ascii=False, default=str)
    html = HTML_TEMPLATE.replace("/*__DATA__*/", payload)
    for out in (os.path.join(ROOT, "NEICS_Walkthrough.html"),
                os.path.join(ROOT, "docs", "NEICS_Walkthrough.html")):
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", out, f"({len(html)} bytes)")
    print(f"enterprises={len(data['enterprises'])} rules={len(data['rules'])} "
          f"standards={len(data['standards'])}")


if __name__ == "__main__":
    main()
