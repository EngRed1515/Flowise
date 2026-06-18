# NEICS — Deployment Guide (Isolated Staging / UAT)

**National Enterprise Intelligence and Classification System (NEICS)** — State of Qatar NSO/NSC
Phase: Staging / UAT (no production deployment) · Version 1.0 · Date 2026-06-18

This guide describes how to stand up the **isolated staging** environment used for UAT. It does **not** describe a production deployment. The environment is self-contained and connects to no live data providers.

---

## 1. Architecture overview

| Service | Technology | Port (staging) | Purpose |
|---|---|---|---|
| `backend` | FastAPI (Python) + SQLAlchemy | 8000 | REST API, Rules/Ownership/Validation/Quality engines, OpenAPI at `/docs` |
| `frontend` | React (Vite) | 80 / mapped host port | Web UI |
| `postgres` | PostgreSQL | 5432 (internal) | Primary datastore for staging |

Deployment is via **Docker Compose** for staging; the images are **Kubernetes-ready** for a future phase. For local zero-infrastructure work, the backend can run directly with SQLite + uvicorn.

Assumed repository layout:

```
neics/
├── docker-compose.yml          # services: backend, frontend, postgres
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/                    # FastAPI application (app.main:app)
├── frontend/
│   └── Dockerfile
└── docs/
```

## 2. Prerequisites

- Docker Engine 24+ and the Docker Compose plugin (`docker compose`).
- ~2 vCPU / 4 GB RAM available to Docker for the staging stack.
- Host ports free for the frontend (e.g., 5173 or 8080) and backend (8000).
- For local zero-infra runs only: Python 3.11+ and `pip`.
- No external network access to administrative data sources is required or used.

## 3. Configuration (environment variables)

The backend reads the following variables (set them in `docker-compose.yml`, an `.env` file at `neics/`, or the shell for local runs):

| Variable | Purpose | Staging value (example) |
|---|---|---|
| `NEICS_DATABASE_URL` | SQLAlchemy connection string | `postgresql+psycopg://neics:neics@postgres:5432/neics` |
| `NEICS_JWT_SECRET` | Secret used to sign JWT access tokens | a long random string unique to staging |
| `NEICS_AUTO_SEED` | If true, seed the 28-enterprise dataset, ~40 rules, VR-001..VR-018, standards, metadata, reference data on startup | `true` |
| `NEICS_CORS_ORIGINS` | Allowed browser origins for CORS | the staging frontend origin, e.g. `http://localhost:8080` |

Notes:
- Use a dedicated, non-production `NEICS_JWT_SECRET` for staging. Never reuse a production secret.
- Set `NEICS_CORS_ORIGINS` to the exact staging frontend origin; avoid `*` even in staging.
- Set `NEICS_AUTO_SEED=true` for a fresh UAT environment so the golden dataset and demo users are present. Set it to `false` once you want data to persist across restarts without reseeding.

## 4. Deploying with Docker Compose (recommended for UAT)

From the `neics/` directory:

```
# 1. Build and start the stack (backend, frontend, postgres)
docker compose up -d --build

# 2. Watch backend startup and seeding
docker compose logs -f backend

# 3. Verify health
curl http://localhost:8000/health
```

Expected: `GET /health` returns an OK/healthy status, and the backend log reports the seed completing (28 enterprises, rules, standards, metadata, reference data, demo users).

Access points:
- Backend API and OpenAPI UI: `http://localhost:8000/docs`
- Frontend: `http://localhost:<mapped-frontend-port>` (per `docker-compose.yml`)

Log in with any demo user (see Administrator Guide), e.g. `admin/admin123`.

## 5. Local zero-infrastructure option (SQLite + uvicorn)

For a developer or a quick reviewer run without Docker/PostgreSQL:

```
cd neics/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export NEICS_DATABASE_URL="sqlite:///./neics.db"
export NEICS_JWT_SECRET="dev-only-secret"
export NEICS_AUTO_SEED="true"
export NEICS_CORS_ORIGINS="http://localhost:5173"

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

This starts the API at `http://localhost:8000` backed by a local SQLite file. Run the frontend separately with the Vite dev server (`npm install && npm run dev` in `neics/frontend`), pointing it at `http://localhost:8000`.

SQLite is for local development and demonstration only; UAT acceptance runs on PostgreSQL via Docker Compose.

## 6. Data seeding behaviour

- When `NEICS_AUTO_SEED=true`, the backend loads on startup: the 28 seeded enterprises (workbook samples `QA-ENT-20260000001..006` + `…099`, and UAT entities `QA-ENT-2026000000010..030`), approximately 40 classification rules, validation rules VR-001..VR-018, the standards catalogue, metadata, and reference codelists (sectors, legal-forms, ISIC, size-thresholds, domain codelists), plus the seven demo users.
- Seeding is idempotent for a clean database. To force a fresh reseed, tear down and recreate the database volume (Section 8) and start with `NEICS_AUTO_SEED=true`.
- See the Administrator Guide for reseeding and the seed loader details.

## 7. Health checks

| Check | Command | Expected |
|---|---|---|
| Liveness | `curl http://localhost:8000/health` | Healthy status |
| Service identity | `curl http://localhost:8000/` | Service name/version |
| Data present | `GET /api/enterprises` (with token) | 28 enterprises |
| Auth | `POST /api/auth/login` (`admin/admin123`) | `access_token` returned |
| Database | `docker compose exec postgres pg_isready` | accepting connections |

A Docker healthcheck on the backend service should target `/health`; Compose will mark the service healthy once it passes.

## 8. Teardown

```
# Stop and remove containers and network (keep the database volume)
docker compose down

# Stop and ALSO remove the database volume (full reset before a fresh reseed)
docker compose down -v
```

After `down -v`, the next `docker compose up -d` with `NEICS_AUTO_SEED=true` recreates a pristine seeded environment.

## 9. Cloud / Kubernetes readiness (future phase — not part of UAT)

The images are container-native and Kubernetes-ready. For a future deployment:
- Deploy `backend` and `frontend` as Deployments with Services; expose via an Ingress with TLS.
- Provide `NEICS_*` configuration via ConfigMaps (non-secret) and Secrets (`NEICS_JWT_SECRET`).
- Use a managed PostgreSQL instance rather than the in-cluster container; set `NEICS_DATABASE_URL` accordingly.
- Configure a liveness/readiness probe on `/health`.
- Set `NEICS_AUTO_SEED=false` for any environment holding real data.

These notes are informational; Kubernetes deployment is out of scope for the UAT phase.

## 10. Isolation from production and live providers

The staging/UAT environment is deliberately isolated:

1. **No live data providers.** NEICS does not connect to the commercial registry, tax authority, central bank, LEI issuers, or any other administrative source in staging. All such data is represented by the seeded synthetic dataset only.
2. **Synthetic data only.** The 28 seeded enterprises are illustrative records created for testing. No real enterprise records are present.
3. **No production credentials or secrets.** Staging uses a dedicated `NEICS_JWT_SECRET` and demo accounts that exist only in staging.
4. **Restricted CORS.** `NEICS_CORS_ORIGINS` is limited to the staging frontend origin.
5. **Self-contained network.** The Compose network is internal; only the intended frontend/backend ports are published to the host. No outbound integrations are configured or enabled.
6. **Disposable state.** The environment can be reset at any time (`docker compose down -v`) without affecting any other system.

This isolation guarantees that UAT activities cannot read from or write to any production or live system.

## 11. Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| Backend unhealthy on startup | Postgres not ready | Confirm `postgres` healthy; check `NEICS_DATABASE_URL`; restart `backend` |
| `GET /api/enterprises` empty | Seeding skipped | Confirm `NEICS_AUTO_SEED=true`; reset volume and restart |
| Login 401 for demo users | Database not seeded / wrong DB | Verify seed log; confirm DB URL points to the seeded database |
| Frontend cannot call API (CORS error) | Origin not allowed | Set `NEICS_CORS_ORIGINS` to the exact frontend origin |
| Port already in use | Host port conflict | Change the published port mapping in `docker-compose.yml` |
