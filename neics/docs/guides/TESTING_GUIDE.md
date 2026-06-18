# NEICS — Testing Guide

**National Enterprise Intelligence and Classification System (NEICS)** — State of Qatar NSO/NSC
Phase: Staging / UAT (no production deployment) · Version 1.0 · Date 2026-06-18

This guide explains how to run the automated test suite, exercise the API, execute the UAT cases, interpret the generated verification reports, and use the simulation sandbox for what-if testing.

---

## 1. Test layers

| Layer | What it covers | Where |
|---|---|---|
| Automated unit/integration tests | Engines (rules, ownership, validation, quality, classifier), API endpoints, RBAC | `neics/backend/tests` (pytest) |
| API test scripts / manual API checks | End-to-end request/response against a running backend | OpenAPI `/docs`, `curl`, or an API client |
| UAT cases | Business acceptance, methodology, governance | `docs/uat/UAT_TEST_CASES.md` |
| Verification reports | Methodology traceability, rules verification, classification validation, data quality | `docs/reports/` |

## 2. Running the automated test suite (pytest)

From the backend directory with the virtual environment active:

```
cd neics/backend
source .venv/bin/activate            # if using a venv
pip install -r requirements.txt

# Run the full suite
pytest

# Verbose, with short tracebacks
pytest -v --tb=short

# Run a subset (by path or keyword)
pytest tests/ -k "classif"
pytest tests/test_validation.py

# With coverage (if pytest-cov is installed)
pytest --cov=app --cov-report=term-missing
```

Recommended environment for tests (isolated, fast):

```
export NEICS_DATABASE_URL="sqlite:///./test.db"
export NEICS_JWT_SECRET="test-secret"
export NEICS_AUTO_SEED="true"
```

The suite should exercise: authentication and RBAC, enterprise CRUD, ownership/effective-control resolution, the 18 tests and ~40 rules, validation rules VR-001..VR-018, data-quality scoring, explainability, audit/versioning, ingestion, and the golden-set regression (the engine reproduces 28/28 expected sector and public/private verdicts). A green run is a prerequisite for entering UAT (see UAT entry criteria).

## 3. Exercising the API

With the backend running (`http://localhost:8000`):

1. Open the interactive OpenAPI UI at `http://localhost:8000/docs`.
2. Authenticate: `POST /api/auth/login` with form fields `username`/`password` (e.g., `classifier/classifier123`). Copy the `access_token`.
3. Authorise in `/docs` (the **Authorize** button) or pass `Authorization: Bearer <token>` on each call.

Example smoke check with `curl`:

```
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -d 'username=classifier&password=classifier123' | python -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')

curl -s http://localhost:8000/api/enterprises -H "Authorization: Bearer $TOKEN"
curl -s -X POST http://localhost:8000/api/enterprises/<id>/classify -H "Authorization: Bearer $TOKEN"
curl -s http://localhost:8000/api/enterprises/<id>/explain -H "Authorization: Bearer $TOKEN"
```

A full golden-set check classifies every seeded enterprise and compares each result to the expected baseline (sector and public/private), mirroring UAT case `UAT-CLS-046`.

## 4. Executing the UAT cases

1. Confirm UAT **entry criteria** (Deployment Guide healthy; seed loaded; demo users authenticate; baseline signed off).
2. Open `docs/uat/UAT_TEST_CASES.md`. Execute cases area by area following the test plan phases.
3. For each case: perform the Steps via UI or API, compare against the **Expected Result**, then record the **Actual Result** and **Pass/Fail**.
4. Attach evidence (screenshots or API payloads) and log any defect per the defect-management process in `docs/uat/UAT_TEST_PLAN.md`.
5. Maintain the running tally; confirm the per-area minimums and the total (168 cases planned).
6. Evaluate against `docs/uat/ACCEPTANCE_CRITERIA.md` at closure.

Tip: the six end-to-end scripts in `docs/uat/DEMONSTRATION_SCENARIOS.md` are the fastest way to validate the major flows before running the detailed cases.

## 5. Interpreting the verification reports (`docs/reports/`)

These reports provide automated evidence to cross-check UAT findings. (They are produced by a separate workstream; UAT consumes them read-only.)

| Report | What it shows | How to use it |
|---|---|---|
| Methodology traceability matrix | Each of the 18 tests and ~40 rules mapped to the underlying standard(s) (SNA 2025, GFS 2014, BPM6, BD4, ISIC Rev.4, …) | Confirm AC-03 (100% traceability); reconcile against `GET /api/tests`, `GET /api/rules`, `GET /api/standards` |
| Rules verification | Each rule's expression, severity, effective/expiry dates, and a fired/not-fired evaluation against test fixtures | Confirm rules are data-driven and behave as specified; supports Rules Engine UAT cases |
| Classification validation | The 28 seeded entities with system-determined vs expected sector and public/private (and other dimensions) | Confirm 28/28 accuracy (AC-04/AC-05); reconcile to `UAT-CLS-046` |
| Data quality | Six-dimension DAMA scores per entity and portfolio aggregates; exceptions raised | Confirm quality KPIs (error ≤ 2%, etc.) and exception generation |

When reconciling: dashboard counts (`GET /api/dashboard`) and quality figures (`GET /api/quality`) should agree with the corresponding report. Any discrepancy is logged as a defect with both sources attached.

## 6. Using the simulation sandbox for what-if testing

The sandbox lets you evaluate a hypothetical classification **without persisting** any data or creating audit entries.

UI: open the **Simulation** workspace, enter or adjust a candidate entity (identity, activity, ownership, financials), and run **Simulate** to see the determination and trace.

API:
```
POST /api/simulate            # body = candidate entity facts/payload
```

Recommended what-if checks:
- **FDI threshold sensitivity.** Submit the same entity with 9% vs 11% foreign equity; confirm the FDI determination flips around the 10% threshold.
- **Control sensitivity.** Vary the largest ownership share around 50%; confirm control_flag transitions to MAJ-VOTE.
- **Size sensitivity.** Vary FTE/turnover across Qatar thresholds; confirm size_class changes and the higher criterion governs.
- **No side effects.** After simulating, confirm `GET /api/enterprises` count is unchanged and no new audit entry exists (UAT-SIM-002).

The sandbox is the safe way to explore rule behaviour and prepare expected results before running destructive or persisted tests.

## 7. Regression and defect retest

- After any fix is redeployed to staging, retest the originating UAT case **and** adjacent cases in the same area.
- Re-run the automated suite and the golden-set check before declaring the defect closed.
- Re-confirm the affected acceptance criteria.
