# NEICS — Complete Project Bundle (Manifest)

**National Enterprise Intelligence & Classification System (NEICS) — State of Qatar**
Prepared for: independent audit / external review tooling.
Status: **UAT prototype — NOT for public deployment.** Entity-level records are
confidential under the Statistics Law; all sample identifiers are stylised
composites, not real entities.

This bundle contains the full project: the data-request deliverables, the
clickable platform prototype, the backend classification engine, the React
frontend, the reference/test data, the architecture & governance documentation,
the UAT pack, and the original source material the system was reverse-engineered
from.

---

## 1. Headline deliverables (root)

| File | What it is |
|------|------------|
| `NEICS_Data_Request.xlsx` | The single, definitive data-request workbook (use this one). Start-here guide, summary-by-entity index (hyperlinked), the complete master list of every data point, and one ready-to-send request tab per entity. Each data point carries: plain meaning, why it matters to the engine, a concrete example, format, must-have flag, colour-coded importance, the authoritative entity, standard and test. |
| `NEICS_Data_Requirements.xlsx` | Earlier master catalogue (superseded by NEICS_Data_Request.xlsx; kept for traceability). |
| `NEICS_Entity_Data_Requests.xlsx` | Earlier entity-facing pack (superseded; kept for traceability). |
| `Qatar_Enterprise_Classification_Platform.html` | Self-contained clickable platform prototype — open by double-click, no server/internet. 23 screens: classification engine, register, dashboard, simulators, scenarios, rules, governance, workflow, RBAC. |
| `NEICS_Walkthrough.html` | Same prototype (alternate filename). |
| `README.md` | Project overview and run instructions. |

## 2. Data-request generators (audited source of truth)

Located in `backend/tools/` — these build the Excel deliverables and self-audit before writing.

| File | Purpose |
|------|---------|
| `build_data_request.py` | Builds the unified NEICS_Data_Request.xlsx. |
| `build_data_requirements.py` | Defines the provider register (18 entities) and the data-point catalogue (31 points) — the single source of truth imported by the others. |
| `build_entity_requests.py` | Builds the per-entity pack; defines regime/membership corroboration links. |
| `build_walkthrough.py` + `walkthrough_template.py` | Build the clickable HTML platform from the seeded database. |
| `audit_walkthrough.js` | Headless audit: engine vs backend (67/67), all views render, interactions and RBAC verified. |
| `generate_reports.py`, `fact_synth.py` | Verification-report and fact-synthesis helpers. |

## 3. Backend — classification engine (`backend/app/`)

FastAPI + SQLAlchemy + Pydantic. Database-driven rules (not hard-coded).

- `engine/` — classifier.py, facts.py, ownership.py, expression.py (rule condition evaluator), validation.py, quality.py, service.py.
- `models/` — enterprise, ownership, rules, reference, governance ORM models.
- `api/` — auth, enterprises, catalog, governance, ingest endpoints.
- `core/security.py` — JWT + RBAC (7 roles).
- `seed/` — definitions.py (the 18 tests, rules, standards, codelists) and loader.py.
- `tests/test_neics.py` — pytest suite (engine reproduces 74/74 expected verdicts).
- `requirements.txt`, `Dockerfile`.

## 4. Frontend — React platform (`frontend/`)

Vite + React SPA (src/pages/, src/components/), nginx config, Dockerfile. `dist/` holds a prebuilt bundle.

## 5. Reference & test data (`data/`)

- `ref_*.json` — ISIC sections/divisions/classes, institutional sectors, legal forms, size thresholds, codelists, metadata variables.
- `sample_*.json` — illustrative enterprises, establishments, legal units, groups, ownership.
- `uat_*.json` — UAT dataset: 74 enterprises, ownership chains, and uat_expected.json golden verdicts the engine is audited against.

## 6. Documentation (`docs/`)

- `architecture/00–17` — executive, business, information, application and technical architecture; enterprise data model; ERD; data dictionary; metadata model; standards & rules repository design; classification logic maps; security; data quality; audit & lineage; AI review; simulation; roadmap.
- `guides/` — Administrator, Deployment, Testing, User guides.
- `reports/` — classification, data-quality, explainability, methodology and rules verification reports + methodology traceability matrix.
- `uat/` — UAT test plan, 100+ test cases, acceptance criteria, demonstration scenarios.

## 7. Original source material (`source_material/`)

The framework and narrative the entire system was reverse-engineered from (extracted to text). Use these to audit fidelity of the implementation against the intended methodology.

- `framework.txt` — the national framework (standards, 18 tests, sectors, control indicators, governance).
- `executive_story.txt` — the executive narrative / implementation story.

## 8. Infrastructure

- `docker-compose.yml` — Postgres + backend + frontend stack.
- `.env.example` — configuration template.

---

## Audit anchors (claims you can verify)

- Engine correctness: `backend/tests/test_neics.py` and `audit_walkthrough.js` — the engine reproduces the golden verdicts in `data/uat_expected.json` (74/74 backend; 67/67 in the headless HTML audit for entries with expected values).
- Data-request completeness: `build_data_request.py` aborts unless all 31 data points are enriched and assigned to an authoritative entity, and counts reconcile to the catalogue. The 31 points equal every input field the engine consumes (reconciled against `data/uat_enterprises.json` + `uat_ownership.json`).
- No invented entities: every record is a stylised composite; provider list, tests, sectors, standards and thresholds trace to `source_material/`.
