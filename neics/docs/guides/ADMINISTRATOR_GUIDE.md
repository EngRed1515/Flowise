# NEICS — Administrator Guide

**National Enterprise Intelligence and Classification System (NEICS)** — State of Qatar NSO/NSC
Phase: Staging / UAT (no production deployment) · Version 1.0 · Date 2026-06-18

This guide is for administrators and methodology owners managing the NEICS staging environment: users and roles, configuration, seeding, the Rules Repository, standards and metadata, audit review, backup/restore, methodology version control, and reclassification triggers.

---

## 1. User and role management

Administer users and roles via the API (`GET /api/admin/users`, `GET /api/admin/roles`) or the Administration area of the UI. Only the **Administrator** role may manage users and roles.

### 1.1 Demo users (staging)

| Username | Password | Role |
|---|---|---|
| `admin` | `admin123` | Administrator |
| `methodologist` | `methodologist123` | Methodologist |
| `steward` | `steward123` | Data Steward |
| `classifier` | `classifier123` | Classifier |
| `reviewer` | `reviewer123` | Reviewer |
| `auditor` | `auditor123` | Auditor |
| `analyst` | `analyst123` | Analyst |

These accounts exist only in staging. Replace credentials and rotate `NEICS_JWT_SECRET` before any environment that is not throwaway.

### 1.2 RBAC permission matrix

| Capability | Administrator | Methodologist | Data Steward | Classifier | Reviewer | Auditor | Analyst |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Read enterprises / classifications / explain | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Create/update enterprises | ✅ | — | ✅ | ✅ | — | — | — |
| Manage ownership | ✅ | — | ✅ | — | — | — | — |
| Run classification (`/classify`) | ✅ | — | ✅ | ✅ | — | — | — |
| Author rules / standards / metadata | ✅ | ✅ | — | — | — | — | — |
| Test rules (`/rules/{id}/test`) | ✅ | ✅ | — | — | — | — | — |
| Review & resolve (`/reviews/{id}/resolve`) | ✅ | — | — | — | ✅ | — | — |
| Override classification (`/override`) | ✅ | — | — | — | ✅ | — | — |
| Read audit / quality | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅(read) |
| Manage users / roles (`/admin/*`) | ✅ | — | — | — | — | — | — |
| Ingest data (`/ingest/*`) | ✅ | — | ✅ | ✅ | — | — | — |

Summary of role intent: Administrator — all capabilities; Methodologist — authors rules/standards/metadata; Data Steward — writes enterprises and ownership plus classify; Classifier — writes enterprises plus classify; Reviewer — reviews and overrides; Auditor — reads audit/quality; Analyst — read-only. The Auditor's primary remit is audit and quality reads.

### 1.3 Administering accounts

1. Log in as `admin`.
2. `GET /api/admin/users` to list accounts; `GET /api/admin/roles` to list roles and their permissions.
3. Create/disable users and assign a single role per the matrix above (use the UI Administration area or the admin API).
4. Enforce least privilege: assign the narrowest role that supports the user's duties.

## 2. Configuration and environment variables

| Variable | Purpose | Notes |
|---|---|---|
| `NEICS_DATABASE_URL` | Datastore connection | PostgreSQL in staging; SQLite for local dev |
| `NEICS_JWT_SECRET` | JWT signing secret | Unique per environment; rotate on suspected exposure |
| `NEICS_AUTO_SEED` | Seed on startup | `true` for fresh UAT; `false` to persist data |
| `NEICS_CORS_ORIGINS` | Allowed browser origins | Exact staging frontend origin; avoid `*` |

Changing configuration requires a backend restart (`docker compose up -d` or restart the uvicorn process). See the Deployment Guide for full details.

## 3. Seeding and reseeding

- On startup with `NEICS_AUTO_SEED=true`, the seed loader populates the 28 enterprises, ~40 rules, validation rules VR-001..VR-018, the standards catalogue, metadata, reference codelists, and the demo users.
- **Reseed (fresh):** tear down and remove the database volume, then start again:
  ```
  docker compose down -v
  docker compose up -d --build      # with NEICS_AUTO_SEED=true
  ```
- **Local dev reseed (SQLite):** delete the SQLite file and restart with `NEICS_AUTO_SEED=true`.
- Verify after reseed: `GET /api/enterprises` returns 28 entities; demo users authenticate; `GET /api/rules` returns ~40 rules; `GET /api/tests` returns T1–T18.

## 4. Managing the Rules Repository

NEICS classification logic is **database-driven** (no hard-coding). Rules live in the Rules Repository and are authored by Methodologists (or Administrators).

### 4.1 Inspecting rules

- `GET /api/rules` — list all rules with metadata.
- `GET /api/rules/{id}` — full definition: expression, severity, applicable test/dimension, effective and expiry dates, version.
- `GET /api/tests` — the 18 tests (T1–T18) the rules support.

### 4.2 Authoring / versioning / approval workflow

1. **Author** a new rule or a new version of an existing rule as `methodologist`.
2. **Test** it in isolation via `POST /api/rules/{id}/test` with representative facts, and/or in the simulation sandbox (`POST /api/simulate`), before activation.
3. **Set effective/expiry dates.** A rule applies only within its effective window: it is not applied before its effective date and not applied after its expiry date.
4. **Approve/activate.** Follow the methodology governance approval before a rule becomes effective. Superseding an existing rule should set the prior version's expiry to the new version's effective date so there is no gap or overlap.
5. **Audit.** Every rule creation/change is recorded in the audit trail (actor, timestamp, before/after, version).

### 4.3 Good practice

- Never embed classification thresholds in code; express them as rule data so they are versioned and auditable.
- Validate the golden set after any rule change (re-run the classification validation report and `UAT-CLS-046`) to confirm 28/28 still holds or that any intended change is reflected in an updated baseline.

## 5. Managing standards and metadata

- **Standards** (`GET /api/standards`): the catalogue anchoring the methodology — SNA 2025, IMF GFS 2014, IMF BPM6, OECD BD4, ISIC Rev.4, plus CPC, COFOG, ICSE, SEEA, LEI/ISO 17442, SDMX, GSIM, GSBPM, DAMA DMBOK, and the Qatar National Classification Standards. Methodologists maintain references and version notes here.
- **Metadata** (`GET /api/metadata`): variable and concept definitions (GSIM/SDMX-aligned) used across the platform.
- **Reference codelists**: `GET /api/reference/{sectors|legal-forms|isic|size-thresholds}` and `GET /api/reference/codelist/{domain}`. Keep codelists aligned with the standards; validation rules reference them (e.g., VR-002 legal form, VR-004 ISIC, VR-005 sector).

Changes to standards, metadata, and codelists are versioned and audited.

## 6. Audit review

- `GET /api/audit` (Administrator/Auditor) — chronological change records with actor, timestamp, entity, and before/after values, covering enterprises, ownership, classifications, rules, standards/metadata, reviews, and overrides.
- `GET /api/enterprises/{id}/history` — the temporally versioned classification history for an entity; superseded versions are retained and reconstructable.
- Review the audit trail regularly to confirm 100% change coverage (acceptance criterion AC-12) and to investigate overrides (each override carries a justification).

## 7. Backup and restore (staging)

NEICS state lives in PostgreSQL. For staging:

```
# Backup
docker compose exec -T postgres pg_dump -U neics neics > neics_staging_backup.sql

# Restore (into a fresh, empty database)
cat neics_staging_backup.sql | docker compose exec -T postgres psql -U neics -d neics
```

Notes:
- Because the environment is seedable, the simplest "restore to known good" is `docker compose down -v` followed by a reseeded startup.
- For local SQLite dev, back up by copying the database file.
- Production-grade backup/restore (PITR, managed backups) is a future-phase concern and out of scope for UAT.

## 8. Methodology version control

- The methodology is realised as versioned rules, tests, standards references, and reference data — all stored in the database and audited.
- Treat the rule set as a versioned artefact: record the methodology version associated with each release, and keep the agreed golden expected-results baseline in step with it.
- After any methodology change, re-run the verification reports under `docs/reports/` and confirm the classification-validation outcome against the (possibly updated) baseline.

## 9. Reclassification triggers

Re-run classification (`POST /api/enterprises/{id}/classify`) when any of the following occurs:

1. **Source data changes** — updated identity, activity (ISIC), financials (FTE/turnover affecting size), or residence.
2. **Ownership changes** — new/updated ownership relationships affecting control or FDI (e.g., crossing the 50% control or 10% FDI thresholds).
3. **Rule or standard changes** — a new effective rule version or codelist change that affects the entity's dimensions.
4. **Methodology version uplift** — a new methodology release.
5. **Override or review resolution** — when a review concludes the prior determination should be revisited.

Each reclassification creates a new version that supersedes the prior one; the prior version is retained in history and the change is audited.
