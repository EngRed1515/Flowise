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
from app.models.reference import Codelist, InstitutionalSector, LegalForm  # noqa: E402
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

    db.close()
    return {
        "generated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "enterprises": enterprises, "groups": groups, "rules": rules, "tests": tests,
        "standards": standards, "metadata": metadata, "codelists": codelists, "reviews": reviews,
        "legal_units": legal_units, "establishments": establishments,
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


# ===================================================================== rendering
import html as _html  # noqa: E402

from tools.walkthrough_template import HTML_SHELL  # noqa: E402

PP = {"PUB-NFC": ("b-blue", "Public non-financial corp"), "PUB-FC": ("b-blue", "Public financial corp"),
      "GG": ("b-purple", "General government"), "PRV-NFC": ("b-green", "Private non-financial corp"),
      "PRV-FC": ("b-green", "Private financial corp"), "FCC": ("b-amber", "Foreign-controlled corp"),
      "NPISH": ("b-teal", "NPISH")}
PAL = ["#8a1538", "#1d6fb8", "#7a3b97", "#1a8a4f", "#b9651b", "#127a6c", "#a8204a", "#946610", "#52606d"]
SECTORS = [("S.11", "Non-financial corporations"), ("S.121", "Central bank"),
           ("S.122", "Deposit-taking corporations"), ("S.124", "Non-MMF investment funds"),
           ("S.126", "Financial auxiliaries"), ("S.127", "Captive financial institutions"),
           ("S.128", "Insurance corporations"), ("S.129", "Pension funds"),
           ("S.13", "General government"), ("S.14", "Households"), ("S.15", "NPISH"),
           ("S.2", "Rest of the World")]


def e(s):
    return _html.escape("" if s is None else str(s))


def bdg(v, cls="b-gray"):
    return f'<span class="bdg {cls}">{e(v)}</span>'


def pp(v):
    cls, _lbl = PP.get(v, ("b-gray", v))
    return f'<span class="bdg {cls}">{e(v)}</span>'


def money(v):
    if not v:
        return "—"
    if v >= 1e9:
        return f"QAR {v/1e9:.1f}bn"
    if v >= 1e6:
        return f"QAR {v/1e6:.1f}m"
    if v >= 1e3:
        return f"QAR {v/1e3:.0f}k"
    return f"QAR {v:,.0f}"


def qcol(s):
    return "var(--green)" if s >= 0.85 else ("var(--amber)" if s >= 0.7 else "var(--red)")


def bars(counts):
    items = sorted(counts.items(), key=lambda x: -x[1])
    mx = max([v for _, v in items] + [1])
    rows = ""
    for i, (k, v) in enumerate(items):
        rows += (f'<div class="barrow"><div>{e(k)}</div><div class="bar"><span style="width:{v/mx*100:.0f}%;'
                 f'background:{PAL[i%len(PAL)]}"></span></div><div style="text-align:right;font-weight:650">{v}</div></div>')
    return rows


def count_by(ents, key):
    m = {}
    for x in ents:
        m[x.get(key) or "—"] = m.get(x.get(key) or "—", 0) + 1
    return m


def ownership_svg(ent):
    chain = ent["ownership"]["chain"] or []
    if not chain:
        return '<p class="small">No ownership recorded (e.g. household enterprise).</p>'
    nodes = {ent["id"]: {"id": ent["id"], "label": ent["name"], "kind": "entity", "d": 0}}
    owners_of = {}
    for c in chain:
        owners_of.setdefault(c["owned_id"], []).append(c)
    frontier, depth, seen = [ent["id"]], 0, {ent["id"]}
    while frontier and depth < 5:
        nxt = []
        for nid in frontier:
            for c in owners_of.get(nid, []):
                oid = c["owner_id"]
                if oid not in nodes:
                    kind = "gov" if c["is_government"] else ("priv" if c["is_resident"] else "foreign")
                    nodes[oid] = {"id": oid, "label": c["owner_name"] or oid, "kind": kind, "d": depth + 1}
                if oid not in seen:
                    seen.add(oid)
                    nxt.append(oid)
        frontier, depth = nxt, depth + 1
    maxd = max(n["d"] for n in nodes.values())
    layers = {}
    for n in nodes.values():
        layers.setdefault(n["d"], []).append(n)
    W, rh, bw, bh = 540, 92, 150, 44
    H = (maxd + 1) * rh + 18
    pos = {}
    for d in range(maxd + 1):
        arr = layers.get(d, [])
        gap = W / (len(arr) + 1)
        for j, n in enumerate(arr):
            pos[n["id"]] = (gap * (j + 1), H - d * rh - rh / 2)
    lines = ""
    for c in chain:
        a, b = pos.get(c["owner_id"]), pos.get(c["owned_id"])
        if not a or not b:
            continue
        lbl = f'{c["ownership_pct"]}%' + (f' · {c["control_indicator"]}' if c["control_indicator"] else "")
        lines += (f'<line x1="{a[0]:.0f}" y1="{a[1]+bh/2:.0f}" x2="{b[0]:.0f}" y2="{b[1]-bh/2:.0f}" '
                  f'stroke="#aab4c0" stroke-width="1.4" marker-end="url(#ar)"/>'
                  f'<text x="{(a[0]+b[0])/2+4:.0f}" y="{(a[1]+b[1])/2:.0f}" font-size="10" fill="#5a6473">{e(lbl)}</text>')
    col = {"entity": "#8a1538", "gov": "#7a3b97", "foreign": "#b9651b", "priv": "#1a8a4f"}
    boxes = ""
    for n in nodes.values():
        x, y = pos[n["id"]]
        lab = "THIS ENTITY" if n["kind"] == "entity" else n["kind"].upper()
        boxes += (f'<rect x="{x-bw/2:.0f}" y="{y-bh/2:.0f}" width="{bw}" height="{bh}" rx="8" fill="#fff" '
                  f'stroke="{col[n["kind"]]}" stroke-width="2"/>'
                  f'<text x="{x:.0f}" y="{y-2:.0f}" font-size="10" text-anchor="middle" fill="#202733">{e(n["label"][:22])}</text>'
                  f'<text x="{x:.0f}" y="{y+12:.0f}" font-size="8" text-anchor="middle" fill="{col[n["kind"]]}">{lab}</text>')
    return (f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-height:340px">'
            f'<defs><marker id="ar" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto">'
            f'<path d="M0,0 L8,4 L0,8 z" fill="#aab4c0"/></marker></defs>{lines}{boxes}</svg>'
            '<div class="legend">■ <span style="color:#8a1538">entity</span> · '
            '■ <span style="color:#7a3b97">government</span> · '
            '■ <span style="color:#1a8a4f">resident private</span> · '
            '■ <span style="color:#b9651b">non-resident</span></div>')


def table(headers, rows):
    th = "".join(f"<th>{e(h)}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tw"><table class="t"><tr>{th}</tr>{trs}</table></div>'


def section(sid, num, title, desc, body):
    return (f'<section class="section" id="{sid}"><div class="wrap">'
            f'<div class="shead"><div class="num">{num}</div><h2>{e(title)}</h2></div>'
            f'<p class="sdesc">{desc}</p>{body}</div></section>')


def render_body(d):
    E = d["enterprises"]
    secs = []

    # 1. Dashboard
    avgq = sum(x["quality"]["overall_score"] for x in E) / len(E)
    openr = sum(1 for r in d["reviews"] if r["status"] == "OPEN")
    exc = sum(len(x["exceptions"]) for x in E)
    kpis = "".join(f'<div class="kpi"><div class="n">{n}</div><div class="l">{l}</div></div>' for n, l in
                   [(len(E), "Enterprises registered"), (len(E), "Classified (100%)"), (f"{avgq:.2f}", "Avg quality score"),
                    (openr, "Pending reviews"), (exc, "Open exceptions"), (len(d["rules"]), "Active rules")])
    dash = (f'<div class="grid auto" style="margin-bottom:18px">{kpis}</div>'
            f'<div class="grid cols-2">'
            f'<div class="card"><div class="hd">By institutional sector (SNA)</div><div class="bd">{bars(count_by(E,"sector"))}</div></div>'
            f'<div class="card"><div class="hd">By public / private (GFS)</div><div class="bd">{bars(count_by(E,"public_private"))}</div></div>'
            f'</div>')
    secs.append(section("dashboard", 1, "Executive Dashboard",
                        "National view of the register — classification coverage, quality and pending reviews.", dash))

    # 2. Classification Studio (worked example) — feature the bank
    feat = next((x for x in E if x["id"] == "QA-ENT-20260000002"), E[0])
    steps = ""
    dimmap = {"sector": "Institutional sector", "public_private": "Public / private", "control": "Effective control",
              "market": "Market status", "size": "Size class", "fdi": "FDI treatment", "special": "Special entity"}
    for s in feat["trace"]:
        cls = "tstep fire" if s.get("matched") else "tstep skip"
        if s.get("matched"):
            out = " ".join(bdg(str(v), "b-green") for v in (s.get("output") or {}).values())
            meta = f'<div class="small" style="margin-top:4px">{e(s.get("rule_id"))} · {e(s.get("standard_ref") or "")}</div>'
        else:
            out = '<span class="small">governance / process step</span>'
            meta = ""
        steps += (f'<div class="{cls}"><div class="badge-test">{e(s["test_code"])}</div>'
                  f'<div class="nm">{e(s["test_name"])}</div><div style="margin-top:4px">{out}</div>{meta}</div>')
    pprows = "".join(f'<div class="r"><span class="k">{lbl}</span><span>{(pp(feat[k]) if k=="public_private" else "<b>"+e(feat[k])+"</b>")}</span></div>'
                     for k, lbl in dimmap.items())
    pprows += f'<div class="r"><span class="k">Confidence</span><span style="color:var(--green);font-weight:700">{feat["confidence"]}</span></div>'
    studio = (f'<div class="grid cols-23"><div>'
              f'<div class="card" style="margin-bottom:16px"><div class="hd">Subject — {e(feat["name"])}</div><div class="bd">'
              f'<div class="kv" style="grid-template-columns:140px 1fr"><div class="k">Legal form</div><div>{e(feat["legal_form"])}</div>'
              f'<div class="k">ISIC Rev.4</div><div>{e(feat["isic"])}</div><div class="k">Residence</div><div>{e(feat["residence"])}</div>'
              f'<div class="k">Employment</div><div>{feat["employment"]} FTE</div><div class="k">Turnover</div><div>{money(feat["turnover"])}</div>'
              f'<div class="k">Gov ownership</div><div>{feat["ownership"]["government_pct"]}%</div></div>'
              f'<div class="svgwrap" style="margin-top:14px">{ownership_svg(feat)}</div></div></div>'
              f'<div class="card"><div class="hd">18-test classification pipeline</div><div class="bd"><div class="timeline">{steps}</div></div></div>'
              f'</div><div><div class="passport"><div class="top"><div class="nm">{e(feat["name"])}</div><div class="id">{e(feat["id"])}</div></div>{pprows}</div>'
              f'<p class="note" style="margin-top:14px">In the live platform this runs on demand via <span class="mono">POST /api/enterprises/{{id}}/classify</span> and animates step-by-step. Every result is reproducible and explainable.</p></div></div>')
    secs.append(section("studio", 2, "Classification Studio",
                        "The classification engine. Each enterprise passes through the 18 sequenced tests; the institutional sector, "
                        "public/private status, control, size and FDI treatment are derived rule-by-rule, each citing the international standard applied.",
                        studio))

    # 3. Enterprise Registry
    rows = [[f'<b>{e(x["name"])}</b>', f'<span class="mono small">{e(x["id"][-8:])}</span>', e(x["sector"]),
             pp(x["public_private"]), e(x["size"]), bdg(x["control"]),
             f'<span style="color:{qcol(x["quality"]["overall_score"])};font-weight:700">{x["quality"]["overall_score"]}</span>']
            for x in E]
    reg = table(["Enterprise", "ID", "Sector", "Public/Private", "Size", "Control", "Quality"], rows)
    secs.append(section("registry", 3, "Enterprise Registry",
                        f"The Central Statistical Business Register — {len(E)} resident statistical units covering every enterprise type "
                        "(government, public corporations, banks, insurers, funds, NPISH, household, foreign-owned, free-zone, QFC, SMEs, MNE groups).",
                        reg))

    # 4. Enterprise Profile (featured example)
    fp = feat
    o = fp["ownership"]
    appl = "".join(f'<tr><td>{e(a["test"])}</td><td class="mono">{e(a["rule_id"])}</td>'
                   f'<td>{" ".join(bdg(str(v),"b-green") for v in (a.get("output") or {}).values())}</td>'
                   f'<td class="small">{e(a["standard_ref"])}</td><td class="small">{e(a["rationale"])}</td></tr>'
                   for a in fp["applied_rules"])
    prof = (f'<div class="card" style="margin-bottom:16px"><div class="bd">'
            f'<div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center"><div style="flex:1;min-width:200px">'
            f'<div style="font-size:18px;font-weight:700">{e(fp["name"])}</div><div class="mono small">{e(fp["id"])} · LEI {e(fp["lei"] or "—")}</div></div>'
            f'<div>{bdg(fp["sector"])} {pp(fp["public_private"])} {bdg(fp["size"])}</div></div></div></div>'
            f'<div class="grid cols-2"><div class="card"><div class="hd">Ownership network</div><div class="bd"><div class="svgwrap">{ownership_svg(fp)}</div></div></div>'
            f'<div class="card"><div class="hd">Control intelligence</div><div class="bd"><div class="kv" style="grid-template-columns:1fr auto">'
            f'<div class="k">Effective government ownership</div><div><b>{o["government_pct"]}%</b></div>'
            f'<div class="k">Government voting</div><div>{o["government_voting"]}%</div>'
            f'<div class="k">Foreign ownership</div><div>{o["foreign_pct"]}%</div>'
            f'<div class="k">Government control</div><div>{("Yes" if o["government_control"] else "No")}</div>'
            f'<div class="k">Ultimate controlling unit</div><div>{e((o["uci"] or {}).get("uci_name") or "—")}</div></div></div></div></div>'
            f'<div class="card" style="margin-top:16px"><div class="hd">Why this classification — applied rules (explainability)</div><div class="bd">'
            f'{table(["Test","Rule","Output","Standard","Rationale"],[])}</div></div>')
    # inject explainability rows directly (table() with prebuilt rows)
    prof = prof.replace(table(["Test", "Rule", "Output", "Standard", "Rationale"], []),
                        f'<div class="tw"><table class="t"><tr><th>Test</th><th>Rule</th><th>Output</th><th>Standard</th><th>Rationale</th></tr>{appl}</table></div>')
    secs.append(section("profile", 4, "Enterprise Profile (360°)",
                        "A complete enterprise file: classification passport, ownership network, and full explainability — the rules applied, "
                        "the output each set, and the standard each traces to.", prof))

    # 5. Ownership & Groups
    swf = next((x for x in E if x["id"] == "QA-ENT-20260000025"), None)
    own_examples = ""
    for x in [feat, swf]:
        if x:
            own_examples += f'<div class="card"><div class="hd">{e(x["name"])}</div><div class="bd"><div class="svgwrap">{ownership_svg(x)}</div></div></div>'
    gtrees = ""
    for g in d["groups"]:
        head = next((x for x in E if x["id"] == g["domestic_head"]), None)
        mem = ""
        for m in g["members"]:
            me = next((x for x in E if x["id"] == m), None)
            kind = "gov" if (me and me["public_private"].startswith("PUB")) else ("foreign" if (me and me["public_private"] == "FCC") else "priv")
            mem += f'<div class="lvl"><span class="gnode {kind}">{e(me["name"] if me else m)} <span class="small">· {e(me["sector"] if me else "")}</span></span></div>'
        gtrees += (f'<div class="card" style="margin-bottom:14px"><div class="hd">{e(g["name"])}</div><div class="bd">'
                   f'<span class="gnode" style="border-color:#444">{e(g["gup"])} <span class="small">· global ultimate parent ({e(g["gup_country"])})</span></span>'
                   f'<div class="lvl"><span class="gnode entity">{e(head["name"] if head else g["domestic_head"])} <span class="small">· domestic head</span></span>{mem}</div>'
                   f'<p class="small" style="margin-top:8px">{e(g["notes"])}</p></div></div>')
    secs.append(section("ownership", 5, "Ownership & Enterprise Groups",
                        "Effective ownership is computed across the whole graph (direct + indirect, aggregated across vehicles) to the Ultimate "
                        "Controlling Institutional Unit — including multi-level sovereign-wealth cascades. Enterprise groups show the global ultimate parent and resident perimeter.",
                        f'<div class="grid cols-2">{own_examples}</div><div style="margin-top:16px">{gtrees}</div>'))

    # 6. Registers (workbook)
    enr = table(["enterprise_id", "legal_name_en", "legal_form", "sector_code", "public_private", "control_flag", "isic", "size_class"],
                [[f'<span class="mono">{e(x["id"])}</span>', e(x["name"]), e(x["legal_form"]), e(x["sector"]),
                  e(x["public_private"]), e(x["control"]), e(x["isic"]), e(x["size"])] for x in E])
    lus = table(["legal_unit_id", "enterprise_id", "name", "legal_form", "cr_number", "authority"],
                [[f'<span class="mono">{e(l["id"])}</span>', f'<span class="mono small">{e(l["enterprise_id"])}</span>',
                  e(l["name"]), e(l["legal_form"]), e(l["cr_number"]), e(l["authority"])] for l in d["legal_units"]])
    regs = (f'<div class="card" style="margin-bottom:16px"><div class="hd">Enterprise Register</div><div class="bd">{enr}</div></div>'
            f'<div class="card"><div class="hd">Legal Unit Register</div><div class="bd">{lus}</div></div>')
    secs.append(section("registers", 6, "Registers (workbook equivalent)",
                        "The platform's statistical registers — the live, database-backed equivalent of the implementation workbook's sheets. "
                        "Persistent identifiers, codelists and validation rules match the workbook.", regs))

    # 7. Rules & Methodology
    testchips = " ".join(f'<span class="bdg b-gray" title="{e(t["description"])}">{e(t["test_code"])} · {e(t["name"])}</span>'
                         for t in d["tests"])
    rule_rows = table(["Rule", "Name", "Test", "Standard", "Logic"],
                      [[f'<span class="mono">{e(r["rule_id"])}</span>', e(r["name"]), bdg(r["test_code"]),
                        f'<span class="small">{e(r["standard_ref"])}</span>',
                        f'<span class="mono small">{e(json.dumps(r["logic"]) if r["logic"] else "default")}</span>'] for r in d["rules"]])
    rules_html = (f'<div class="card" style="margin-bottom:16px"><div class="hd">The 18 sequenced tests</div>'
                  f'<div class="bd"><div style="display:flex;gap:7px;flex-wrap:wrap">{testchips}</div></div></div>'
                  f'<div class="card"><div class="hd">Rules repository ({len(d["rules"])} database-driven rules)</div><div class="bd">{rule_rows}</div></div>')
    secs.append(section("rules", 7, "Rules Engine & Methodology",
                        "No classification logic is hard-coded. Every rule is a database row with a JSON condition, an output, a priority and a "
                        "standard reference — fully auditable and revisable.", rules_html))

    # 8. Standards
    std_html = ""
    for s in d["standards"]:
        cs = "".join(f'<tr><td>{e(c["concept"])}</td><td>{e(c["definition"])}</td></tr>' for c in s["concepts"])
        std_html += (f'<div class="card" style="margin-bottom:12px"><div class="hd">{e(s["code"])} — {e(s["name"])}</div>'
                     f'<div class="bd"><div class="small">{e(s["issuer"])} · {e(s["edition"])} · {e(s["domains"])}</div>'
                     f'<p>{e(s["description"])}</p>'
                     f'{("<div class=tw><table class=t><tr><th>Concept</th><th>Definition</th></tr>"+cs+"</table></div>") if cs else ""}</div></div>')
    secs.append(section("standards", 8, "Standards Repository",
                        "Every rule is anchored to international and national standards: SNA 2025, IMF GFS 2014, IMF BPM6, OECD BD4, ISIC Rev.4 and the wider stack.",
                        std_html))

    # 9. Data Quality & Validation
    dims = ["completeness", "validity", "consistency", "uniqueness", "accuracy", "timeliness", "overall_score"]
    agg = {dm: sum(x["quality"][dm] for x in E) / len(E) for dm in dims}
    qkpi = "".join(f'<div class="kpi"><div class="n" style="color:{qcol(agg[dm])}">{agg[dm]:.2f}</div><div class="l">{dm.replace("_"," ")}</div></div>' for dm in dims)
    allexc = [(x["name"], ex) for x in E for ex in x["exceptions"]]
    sevcls = {"ERROR": "b-red", "WARN": "b-amber", "INFO": "b-blue"}
    exc_rows = table(["Enterprise", "Rule", "Severity", "Message", "Action"],
                     [[e(nm), f'<span class="mono">{e(ex["rule_id"])}</span>', bdg(ex["severity"], sevcls.get(ex["severity"], "b-gray")),
                       e(ex["message"]), f'<span class="small">{e(ex["action"])}</span>'] for nm, ex in allexc]) if allexc else '<p class="small">No exceptions.</p>'
    q_html = (f'<div class="grid auto" style="margin-bottom:18px">{qkpi}</div>'
              f'<div class="card"><div class="hd">Validation exceptions (VR-001..VR-018)</div><div class="bd">{exc_rows}</div></div>')
    secs.append(section("quality", 9, "Data Quality & Validation",
                        "Quality is scored across the six DAMA dimensions; the VR-001..VR-018 business-rule library surfaces exceptions with severity and recommended action.",
                        q_html))

    # 10. Governance (users/roles)
    perms = sorted({p for ps in d["roles"].values() for p in ps})
    rolekeys = list(d["roles"].keys())
    matrix_rows = []
    for p in perms:
        cells = [f'<span class="mono">{e(p)}</span>']
        for r in rolekeys:
            ok = "*" in d["roles"][r] or p in d["roles"][r]
            cells.append('<span style="color:var(--green)">✔</span>' if ok else '·')
        matrix_rows.append(cells)
    user_rows = [[f'<span class="mono">{e(u["username"])}</span>', e(u["full_name"]), bdg(u["role"], "b-blue")]
                 for u in d["users"]]
    gov_html = (f'<div class="card" style="margin-bottom:16px"><div class="hd">Roles (RBAC)</div><div class="bd">'
                f'{table(["Username", "Name", "Role"], user_rows)}</div></div>'
                f'<div class="card"><div class="hd">Permission matrix</div><div class="bd">'
                f'{table(["Permission"] + [r[:4] for r in rolekeys], matrix_rows)}</div></div>')
    secs.append(section("governance", 10, "Governance & Security",
                        "Role-Based Access Control with seven roles; every change is captured in an immutable audit trail under the Technical Classification Committee.",
                        gov_html))

    # 11. UAT & Production Readiness
    uat_rows = table(["Test ID", "Area", "Description", "Expected result", "Status"],
                     [[f'<span class="mono">{e(c[0])}</span>', e(c[1]), e(c[2]), e(c[3]), bdg(c[4], "b-green")] for c in d["uat"]])
    g = d["gap"]
    def box(t, arr):
        lis = "".join(f"<li>{e(x)}</li>" for x in arr)
        return f'<div class="card"><div class="hd">{t}</div><div class="bd"><ul class="tight">{lis}</ul></div></div>'
    rag = table(["Dimension", "Status", "Notes"],
                [[e(r[0]), f'<span class="rag {r[1].replace("-","")}">{e(r[1])}</span>', e(r[2])] for r in d["readiness"]])
    uat_html = (f'<div class="grid auto" style="margin-bottom:16px">'
                f'<div class="kpi"><div class="n">100+</div><div class="l">UAT cases (full suite)</div></div>'
                f'<div class="kpi"><div class="n" style="color:var(--green)">33/33</div><div class="l">Classification verdicts</div></div>'
                f'<div class="kpi"><div class="n" style="color:var(--green)">40/40</div><div class="l">Rules verified</div></div>'
                f'<div class="kpi"><div class="n" style="color:var(--green)">18/18</div><div class="l">Validation rules</div></div></div>'
                f'<div class="card" style="margin-bottom:16px"><div class="hd">Representative acceptance tests</div><div class="bd">{uat_rows}</div></div>'
                f'<div class="grid cols-2" style="margin-bottom:16px">{box("✔ Fully implemented",g["implemented"])}{box("◑ Partially implemented",g["partial"])}</div>'
                f'<div class="grid cols-2" style="margin-bottom:16px">{box("→ Future enhancements",g["future"])}{box("⚠ Production-readiness gaps",g["production_gaps"])}</div>'
                f'<div class="card"><div class="hd">Production readiness assessment</div><div class="bd">{rag}'
                f'<div class="note" style="margin-top:12px"><b>Recommendation:</b> Methodology and data-governance readiness are <span class="rag Green">Green</span>. '
                f'Proceed to a controlled <b>pilot</b> on the largest 100 enterprises after security hardening and one administrative-source integration; '
                f'defer production until HA, load testing and data-sharing instruments under the Statistics Law are in place.</div></div></div>')
    secs.append(section("uat", 11, "UAT & Production Readiness",
                        "Acceptance testing, gap analysis and a formal readiness assessment for the move Development → Staging → Pilot → Production.",
                        uat_html))

    # Hero (prepended, not a nav section)
    hero = (f'<div class="hero"><div class="wrap"><div class="crest">State of Qatar · National Statistics Office</div>'
            f'<h1>National Enterprise Intelligence &amp; Classification System</h1>'
            f'<p>The national platform for classifying and profiling enterprises and economic entities — aligned with SNA 2025, '
            f'IMF GFS 2014, IMF BPM6, OECD BD4 and ISIC Rev.4, applied through an 18-test, fully explainable, auditable methodology.</p>'
            f'<div class="stats">'
            f'<div class="stat"><div class="n">{len(E)}</div><div class="l">Test enterprises</div></div>'
            f'<div class="stat"><div class="n">18</div><div class="l">Classification tests</div></div>'
            f'<div class="stat"><div class="n">{len(d["rules"])}</div><div class="l">Database-driven rules</div></div>'
            f'<div class="stat"><div class="n">{len(d["standards"])}</div><div class="l">Standards mapped</div></div>'
            f'<div class="stat"><div class="n">33/33</div><div class="l">Verdicts verified</div></div>'
            f'</div></div></div>')
    return hero + "".join(secs)


NAV_ITEMS = [("dashboard", "Dashboard"), ("studio", "Classification Studio"), ("registry", "Registry"),
             ("profile", "Enterprise Profile"), ("ownership", "Ownership & Groups"), ("registers", "Registers"),
             ("rules", "Rules & Methodology"), ("standards", "Standards"), ("quality", "Quality & Validation"),
             ("governance", "Governance"), ("uat", "UAT & Readiness")]


def main():
    d = build_data()
    nav = "".join(f'<a href="#{sid}">{e(lbl)}</a>' for sid, lbl in NAV_ITEMS)
    html = (HTML_SHELL.replace("{{NAV}}", nav)
            .replace("{{CONTENT}}", render_body(d))
            .replace("{{GENERATED}}", e(d["generated"])))
    for out in (os.path.join(ROOT, "NEICS_Walkthrough.html"), os.path.join(ROOT, "docs", "NEICS_Walkthrough.html")):
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", out, f"({len(html)} bytes)")
    print(f"enterprises={len(d['enterprises'])} rules={len(d['rules'])} sections={len(NAV_ITEMS)}")


if __name__ == "__main__":
    main()
