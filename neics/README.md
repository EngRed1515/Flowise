# NEICS — National Enterprise Intelligence & Classification System

**State of Qatar · National Statistics Office — Staging / UAT build (v1.0.0)**

> ⚠️ **This is an isolated STAGING / UAT environment.** It is not connected to
> production systems, live databases, or external administrative-data providers.
> No production deployment is authorised in this phase.

NEICS is the national platform for enterprise classification, profiling, ownership
analysis and statistical sectorisation. It operationalises the *National Framework
for Classifying Enterprises & Economic Entities in Qatar* — an 18‑test methodology
anchored in **SNA 2025, IMF GFS 2014, IMF BPM6, OECD BD4 and ISIC Rev.4** (plus CPC,
COFOG, ICSE, SEEA, LEI/ISO 17442, SDMX, GSIM, GSBPM, DAMA DMBOK and the Qatar National
Classification Standards) — as a database‑driven, fully explainable, auditable system.

---

## 🚀 The fastest way to review it

Open **[`NEICS_Walkthrough.html`](./NEICS_Walkthrough.html)** in any browser.
It is a single, self‑contained interactive demo (no backend, no install) covering all
17 modules with the real, verified sample data. Use the left nav to move between
modules and the *Acting as* selector to switch roles.

---

## Run the full stack (Docker — isolated staging)

```bash
cd neics
docker compose up --build
# Frontend  → http://localhost:8080
# API + docs→ http://localhost:8000/docs   (OpenAPI)
# PostgreSQL→ internal only (isolated)
```

The database auto‑seeds reference data + the 28‑enterprise test dataset on first start.

### Run the backend with zero infrastructure (SQLite)

```bash
cd neics/backend
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload          # API on http://localhost:8000
```

### Demo users (username / password — role)

| User | Password | Role |
|---|---|---|
| `admin` | `admin123` | Administrator |
| `methodologist` | `methodologist123` | Methodologist |
| `steward` | `steward123` | Data Steward |
| `classifier` | `classifier123` | Classifier |
| `reviewer` | `reviewer123` | Reviewer |
| `auditor` | `auditor123` | Auditor |
| `analyst` | `analyst123` | Analyst |

---

## What's inside

```
neics/
├── NEICS_Walkthrough.html      ← single-file interactive demo (start here)
├── docker-compose.yml          ← isolated staging stack
├── .env.example
├── backend/                    ← FastAPI + SQLAlchemy + rules/ownership/quality engines
│   ├── app/                    ← models, engine, api, seed, core (security/RBAC)
│   ├── tests/                  ← pytest regression suite (24 tests)
│   └── tools/                  ← report + walkthrough generators
├── frontend/                   ← React (Vite) SPA
├── data/                       ← reference codelists + test dataset (faithful to workbook)
└── docs/
    ├── architecture/           ← executive, business, info, app, technical, data model,
    │                             ERD, data dictionary, metadata, standards/rules design,
    │                             logic maps, security, AI-review, simulation
    ├── reports/                ← SYSTEM-GENERATED verification reports (see below)
    ├── uat/                    ← UAT test plan, 168 test cases, acceptance criteria, demos
    └── guides/                 ← deployment, testing, administrator, user guides
```

## Verification at a glance (auto‑generated from the live engine)

These reports under [`docs/reports/`](./docs/reports/) are produced by
`backend/tools/generate_reports.py` directly from the running classifier — nothing is
hand‑written:

| Report | Headline result |
|---|---|
| Methodology verification | 18 tests · all workbook codelists migrated · 16 standards · **all checks PASS** |
| Methodology traceability matrix | Framework requirement → component → rule → output |
| Rules verification | **40/40 rules** pass positive + negative test cases |
| Classification validation | **28/28 enterprises** match expected sector + public/private verdict |
| Data quality validation | 6 DAMA dimensions scored; validation exceptions surfaced |
| Explainability validation | Full rule trace + standard references per classification |

```bash
cd neics/backend && PYTHONPATH=. pytest -q          # 24 passed
PYTHONPATH=. python tools/generate_reports.py        # regenerate verification reports
PYTHONPATH=. python tools/build_walkthrough.py       # regenerate the HTML walkthrough
```

## Key capabilities

- **18‑test classification pipeline** — database‑driven rules engine (no hard‑coded logic);
  conflict resolution by priority; outputs sector, public/private, control, market,
  size, FDI and special‑entity dimensions.
- **Ownership & Control Intelligence** — effective government/foreign ownership across
  multi‑level chains, aggregation across vehicles, Ultimate Controlling Institutional
  Unit, substance‑over‑form control (golden share, board rights, beneficial‑ownership chain).
- **Explainability** — every classification stores the ordered rule trace, the facts used
  and the standards referenced.
- **Temporal versioning & audit** — immutable history; reproduce any past classification.
- **Validation engine** (VR‑001..VR‑018), **Data Quality engine** (6 DAMA dimensions),
  **anomaly detection** feeding a manual review queue.
- **Standards / Metadata / Rules repositories**; **RBAC** (7 roles); **simulation sandbox**;
  **data ingestion** (JSON/CSV); **API‑first** with OpenAPI docs.

See [`docs/`](./docs/) for the full architecture, UAT package and guides.
