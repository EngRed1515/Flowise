# NEICS Frontend

React (Vite) frontend for the **National Enterprise Intelligence and Classification System (NEICS)** — a Qatar national-statistics enterprise-classification platform.

> **STAGING / UAT ENVIRONMENT — Not for production.**

## Tech stack

- Vite + React 18 + React Router 6
- Plain CSS (no UI library) — Qatar maroon `#8A1538` accent, neutral grays, white cards
- A small `fetch`-based API client (`src/api/client.js`) — no axios
- JWT bearer auth (OAuth2 password flow), token stored in `localStorage`

## Running locally (dev)

```bash
cd neics/frontend
npm install
npm run dev
```

The dev server runs on http://localhost:5173 and proxies `/api` and `/health` to the
backend. The proxy target defaults to `http://localhost:8000` and is configurable:

```bash
VITE_API_BASE=http://localhost:8000 npm run dev
```

Copy `.env.example` to `.env` to set it permanently.

### Demo users (UAT)

The Login page exposes quick-login buttons for every demo role:

| Username       | Password           | Role          |
| -------------- | ------------------ | ------------- |
| admin          | admin123           | Administrator |
| methodologist  | methodologist123   | Methodologist |
| steward        | steward123         | Data Steward  |
| classifier     | classifier123      | Classifier    |
| reviewer       | reviewer123        | Reviewer      |
| auditor        | auditor123         | Auditor       |
| analyst        | analyst123         | Analyst       |

## Build (static)

```bash
npm run build      # outputs to dist/
npm run preview    # preview the production build locally
```

## Docker

Multi-stage build (Node build → nginx serve). The nginx config proxies `/api` and
`/health` to `http://backend:8000`, so run it on the same network as the backend
container (named `backend`).

```bash
# from neics/frontend
docker build -t neics-frontend .
docker run --rm -p 8080:80 --network <backend-network> neics-frontend
```

With a `backend` service on the same Docker network, the frontend is served at
http://localhost:8080 and API calls are transparently proxied.

### Example docker-compose snippet

```yaml
services:
  backend:
    # ... FastAPI service exposing :8000 ...
    expose: ["8000"]
  frontend:
    build: ./neics/frontend
    ports: ["8080:80"]
    depends_on: ["backend"]
```

## Pages

| Route             | Page                 | Notes                                                       |
| ----------------- | -------------------- | ----------------------------------------------------------- |
| `/login`          | Login                | Demo quick-login buttons                                    |
| `/`               | Dashboard            | KPI cards + CSS bar breakdowns                              |
| `/enterprises`    | Enterprises          | Filterable table, New Enterprise, file upload ingestion     |
| `/enterprises/new`| New Enterprise       | Registration form                                           |
| `/enterprises/:id`| Enterprise Profile   | Tabs: Master / Ownership / Classification / **Explainability** / History / Quality / Audit; Re-classify + Override |
| `/rules`          | Rules Repository     | Grouped by test code + interactive Rule Tester              |
| `/methodology`    | Methodology          | The 18 tests + standards repository                         |
| `/reviews`        | Review Center        | Open review queue + resolve                                 |
| `/quality`        | Quality              | Dataset scores, per-enterprise scores, exceptions           |
| `/simulate`       | Simulation Sandbox   | Hypothetical enterprise + ownership edges; never persisted  |
| `/admin`          | Administration       | Users + roles→permissions matrix (admin only)               |

## Architecture notes

- `src/api/client.js` — single fetch wrapper; attaches the bearer token, handles
  form-encoded login, JSON bodies, multipart upload, and 401 → redirect to login.
- `src/auth.jsx` — React context for auth state (`useAuth`, `hasRole`).
- `src/hooks.js` — `useAsync` data-fetching hook (loading / error / reload).
- `src/components/` — `Layout` (sidebar + UAT banner) and shared `ui.jsx` primitives
  (Card, Badge, Gauge, BarBreakdown, Loading, ErrorBox, KpiCard, etc.).
- Role-gating: admin-only nav/pages are hidden; other role restrictions are enforced
  by the backend and surfaced as graceful HTTP 403 messages.
