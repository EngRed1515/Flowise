# NEICS — User Acceptance Test Plan

**National Enterprise Intelligence and Classification System (NEICS)**
State of Qatar — National Statistics Office (NSO) / National Statistics Centre (NSC)

| Field | Value |
|---|---|
| Document | UAT Test Plan |
| Phase | Staging / UAT (no production deployment) |
| Version | 1.0 |
| Status | Review-ready |
| Date | 2026-06-18 |
| Classification | Internal — Restricted |
| Owner | NEICS Programme — Methodology & Quality Assurance |

---

## 1. Introduction

This document defines the User Acceptance Testing (UAT) plan for the National Enterprise Intelligence and Classification System (NEICS). NEICS is the national platform that implements an 18-test enterprise-classification methodology anchored in the international statistical standards governing the production of the national business register and national accounts (SNA 2025, IMF GFS 2014, IMF BPM6, OECD Benchmark Definition of FDI 4th edition (BD4), ISIC Rev.4, and supporting frameworks CPC, COFOG, ICSE, SEEA, LEI/ISO 17442, SDMX, GSIM, GSBPM, DAMA DMBOK, and the Qatar National Classification Standards).

NEICS classifies enterprises across nine determination dimensions through a database-driven Rules Engine (approximately 40 rules, no hard-coded logic), an Ownership Intelligence Engine, a Validation Engine (rules VR-001 through VR-018), and a Data Quality Engine (six DAMA dimensions). Every determination is fully explainable and temporally versioned for audit.

UAT is conducted in an **isolated staging environment** populated with a controlled seed dataset of 28 enterprises. **No production data, no live data-provider feeds, and no production infrastructure are involved.** This plan governs the formal acceptance activities required before any future decision to promote the platform toward production.

## 2. Objectives

The objectives of UAT are to confirm, to the satisfaction of the business stakeholders, that NEICS:

1. Correctly implements the 18-test classification methodology and reproduces the expected determination for every entity in the golden test set (target: 28/28).
2. Produces classifications across all nine dimensions (residence, institutional sector, public/private, control, market status, size, FDI, special-entity, and the final classification record) consistent with the authoritative standards.
3. Enforces every ERROR-severity validation rule (VR-001..VR-018) and surfaces WARNING/INFO findings without blocking.
4. Provides complete, human-readable explainability for 100% of classifications, traceable to the specific tests and rules applied.
5. Maintains a temporally versioned audit trail capturing 100% of changes to enterprises, ownership, classifications, rules, standards, and overrides.
6. Enforces role-based access control (RBAC) for all seven defined roles.
7. Computes data-quality scores across the six DAMA dimensions and raises validation exceptions and review items appropriately.
8. Supports the operational workflows of statisticians, classifiers, reviewers, auditors, and administrators (ingestion, classification, review, override, simulation, reporting).
9. Meets the agreed non-functional targets for usability, performance, and reliability within the staging environment.

## 3. Scope

### 3.1 In Scope

- **Authentication & RBAC / Security** — login, token issuance, role enforcement, permission boundaries.
- **Enterprise Master Data** — create, read, update, profile retrieval.
- **Ownership & Control** — ownership capture, effective-control analysis (nine indicators), ultimate controlling institutional unit (UCI) determination, multi-level chains.
- **Classification methodology** — all 18 tests, all nine dimensions, the ~40 rules, and the 12 framework case studies.
- **Validation Engine** — VR-001..VR-018 across all severities.
- **Data Quality Engine** — six DAMA dimensions, quality scoring, exception generation.
- **Repositories** — Rules, Tests, Standards, Metadata, Reference codelists, and rule testing.
- **Explainability** — determination traces, confidence, applied tests/rules.
- **Audit & temporal versioning** — change history, point-in-time reconstruction.
- **Simulation sandbox** — what-if classification without persistence.
- **Ingestion** — JSON-array ingest and file upload.
- **Governance** — Dashboard, Review Center, reviews/resolution, override workflow, reporting.
- **APIs** — the documented REST surface (OpenAPI at `/docs`).

### 3.2 Out of Scope

- Production deployment, production data, and production sign-off.
- Integration with live external data providers (commercial registry, tax authority, central bank, LEI issuers, etc.). All such sources are represented by seeded staging data only.
- Performance/load testing at production volumes (only indicative staging performance is assessed).
- Penetration testing and formal security certification (a security review is conducted separately under `docs/architecture` / security workstreams).
- Disaster-recovery and high-availability validation in a clustered Kubernetes environment.
- Localisation/translation acceptance beyond the delivered interface language.
- Migration of legacy register data.

## 4. Assumptions

1. The staging environment is provisioned per the Deployment Guide (`docs/guides/DEPLOYMENT_GUIDE.md`) and is healthy (`GET /health` returns OK) before UAT begins.
2. The seed dataset (28 enterprises, ~40 rules, VR-001..VR-018, reference codelists, standards, and metadata) is loaded via `NEICS_AUTO_SEED` or the seed loader.
3. The seven demo users exist with their documented roles and credentials.
4. Expected classification outcomes for the golden test set are defined and agreed by the Methodology team and treated as the acceptance baseline.
5. Testers have completed an orientation walkthrough using `docs/guides/USER_GUIDE.md`.
6. No data outside the seeded staging dataset is required to execute the cases.
7. The OpenAPI documentation at `/docs` reflects the deployed API surface.

## 5. Dependencies

- Availability of the isolated staging environment (backend on port 8000, frontend, PostgreSQL).
- Availability of the seed/reference data and the agreed golden expected-results set.
- Availability of the supporting verification reports under `docs/reports/` (methodology traceability matrix, rules verification, classification validation, data-quality report) for cross-checking automated evidence.
- Availability of test participants across the required roles.
- A defect-tracking channel for logging, triaging, and resolving findings.

## 6. Test Environment

| Component | Staging configuration |
|---|---|
| Backend | FastAPI (Python) + SQLAlchemy, served on `http://localhost:8000`, OpenAPI at `/docs` |
| Database | PostgreSQL (staging container) — `NEICS_DATABASE_URL`; SQLite available for local zero-infra runs |
| Frontend | React (Vite) single-page application |
| Auth | JWT bearer tokens; `NEICS_JWT_SECRET` configured for staging |
| Deployment | Docker Compose (`backend`, `frontend`, `postgres`); Kubernetes-ready but not clustered for UAT |
| Seeding | `NEICS_AUTO_SEED=true` loads the 28-enterprise dataset, rules, standards, metadata, reference data |
| Data isolation | No live provider connections; no production credentials; outbound integrations disabled |
| CORS | `NEICS_CORS_ORIGINS` restricted to the staging frontend origin |

**Isolation statement.** The UAT environment is fully self-contained. It contains only synthetic/illustrative enterprise records created for testing. It does not connect to, read from, or write to any production system or any live administrative data source. See the Deployment Guide isolation section for the controls applied.

## 7. Roles and Responsibilities

| Role | Responsibility in UAT |
|---|---|
| UAT Lead (NSC) | Owns the UAT schedule, chairs go/no-go, confirms exit criteria |
| Senior Statisticians | Validate methodology correctness, sector and public/private verdicts, case studies |
| Enterprise Architects | Validate API behaviour, deployment, integration boundaries, non-functional aspects |
| Data-Governance Specialists | Validate validation rules, data-quality scoring, audit, RBAC, metadata/standards |
| Methodologists | Confirm rule and test traceability; adjudicate expected-result disputes |
| Data Stewards / Classifiers | Execute ingestion, master-data and classification cases |
| Reviewers | Execute review-resolution and override cases |
| Auditors | Execute audit-trail and temporal-versioning cases |
| NSC Management | Receive results, approve/decline acceptance, own production-go decision (future phase) |
| Development Team (separate workstream) | Triage and resolve defects; redeploy fixes to staging |

## 8. Entry Criteria

UAT may begin only when **all** of the following hold:

1. Staging environment deployed and `GET /health` returns healthy.
2. Seed dataset loaded; `GET /api/enterprises` returns the 28 seeded enterprises.
3. All seven demo users authenticate successfully.
4. The UAT test cases (`UAT_TEST_CASES.md`) and acceptance criteria (`ACCEPTANCE_CRITERIA.md`) are approved.
5. The golden expected-results baseline is signed off by Methodology.
6. No open **Critical** defects from prior test cycles (System/Integration testing).
7. Defect-tracking process and tooling are in place.
8. Testers are assigned, oriented, and have credentials.

## 9. Exit Criteria

UAT is complete and acceptance may be recommended when **all** of the following hold:

1. 100% of planned UAT test cases executed.
2. ≥ 98% of test cases pass; 100% of cases designated **Critical** pass.
3. The golden test set reproduces 28/28 expected sector and public/private verdicts.
4. Zero open **Critical** defects; zero open **High** defects without an agreed, time-bound remediation plan accepted by NSC management.
5. All acceptance criteria in `ACCEPTANCE_CRITERIA.md` are evaluated, with results recorded.
6. UAT summary report produced and signed off by the UAT Lead and NSC management.

## 10. Test Approach

1. **Preparation.** Confirm environment, seed data, users, and baseline. Conduct tester orientation.
2. **Execution by area.** Execute the grouped test cases (Authentication/RBAC, Master Data, Ownership/Control, Classification, Validation, Data Quality, Repositories, Rules Engine, Explainability, Audit, Simulation, Ingestion, Governance/Reporting, APIs).
3. **Methodology focus.** For each classification case, compare the system determination against the golden expected result for every relevant dimension and confirm the explainability trace cites the correct tests and rules.
4. **Evidence capture.** Record Actual Result and Pass/Fail for each case; attach screenshots or API response payloads as evidence.
5. **Cross-verification.** Reconcile classification outcomes against the automated verification reports under `docs/reports/`.
6. **Defect handling.** Log, triage, fix (separate workstream), redeploy, and retest.
7. **Acceptance evaluation.** Assess exit criteria and acceptance criteria; produce the summary report.

Testing combines UI-driven execution (React frontend), API-driven execution (OpenAPI `/docs`, scripts, or an API client), and review of generated reports.

## 11. Defect Management

### 11.1 Severity Classification

| Severity | Definition |
|---|---|
| **Critical** | Incorrect classification verdict on a golden-set entity; data loss; failed RBAC enforcement; system unavailable; missing/incorrect audit entry for a change. |
| **High** | Major function unusable or producing materially misleading output (e.g., explainability missing for a classification; ERROR-rule not enforced) with no acceptable workaround. |
| **Medium** | Function works incorrectly but a workaround exists; non-blocking validation or quality-scoring discrepancy. |
| **Low** | Cosmetic, wording, or minor usability issues; documentation gaps. |

### 11.2 Lifecycle

`New → Triaged → In Progress → Fixed → Ready for Retest → Closed` (or `Rejected` / `Deferred` with rationale).

### 11.3 Process

1. Tester logs the defect with Test ID, steps, expected vs actual, evidence, and severity.
2. UAT Lead and Methodology/Development triage and confirm severity within one business day.
3. Development resolves in a separate workstream and redeploys to staging.
4. Tester retests the originating case and any regression-adjacent cases.
5. Defect closed only after a passing retest is recorded.

## 12. Schedule and Phases

| Phase | Activities | Indicative duration |
|---|---|---|
| Phase 0 — Mobilisation | Environment readiness, seed verification, tester orientation, baseline sign-off | 2–3 days |
| Phase 1 — Foundation | Authentication/RBAC, Master Data, APIs, Repositories | 3 days |
| Phase 2 — Methodology Core | Ownership/Control, Classification (all dimensions + case studies), Validation | 5 days |
| Phase 3 — Quality & Governance | Data Quality, Explainability, Audit, Simulation, Ingestion, Dashboard/Reviews/Reporting | 4 days |
| Phase 4 — Demonstration | Execute the six end-to-end demonstration scenarios with stakeholders | 1–2 days |
| Phase 5 — Closure | Defect burndown, regression retest, acceptance evaluation, summary report & sign-off | 2–3 days |

The schedule is indicative; the UAT Lead confirms calendar dates at mobilisation.

## 13. Deliverables

- Executed `UAT_TEST_CASES.md` with Actual Results and Pass/Fail recorded.
- Defect log with final dispositions.
- Acceptance-criteria evaluation against `ACCEPTANCE_CRITERIA.md`.
- Demonstration-scenario outcomes (`DEMONSTRATION_SCENARIOS.md`).
- UAT Summary Report and formal sign-off.

## 14. References

- `UAT_TEST_CASES.md` — detailed test cases.
- `ACCEPTANCE_CRITERIA.md` — measurable acceptance criteria.
- `DEMONSTRATION_SCENARIOS.md` — end-to-end demo scripts.
- `../guides/DEPLOYMENT_GUIDE.md`, `../guides/TESTING_GUIDE.md`, `../guides/ADMINISTRATOR_GUIDE.md`, `../guides/USER_GUIDE.md`.
- Verification reports under `../reports/` (methodology traceability, rules verification, classification validation, data quality).
