# NEICS — Operational Guides Index

**National Enterprise Intelligence and Classification System (NEICS)** — State of Qatar NSO/NSC
Phase: Staging / UAT (no production deployment) · Version 1.0 · Date 2026-06-18

Operational documentation for deploying, testing, administering, and using NEICS in the isolated staging environment.

## Guides

| Guide | Audience | Purpose |
|---|---|---|
| [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) | Enterprise architects, DevOps | Stand up the isolated staging stack (Docker Compose: backend, frontend, postgres), configuration, local SQLite option, health checks, teardown, K8s readiness, and production isolation. |
| [TESTING_GUIDE.md](./TESTING_GUIDE.md) | Testers, QA, methodologists | Run the pytest suite, exercise the API, execute UAT cases, interpret the verification reports, and use the simulation sandbox. |
| [ADMINISTRATOR_GUIDE.md](./ADMINISTRATOR_GUIDE.md) | Administrators, methodology owners | Users/roles and the RBAC matrix, configuration, seeding/reseeding, Rules Repository, standards & metadata, audit, backup/restore, methodology versioning, reclassification triggers. |
| [USER_GUIDE.md](./USER_GUIDE.md) | Analysts, classifiers, stewards, reviewers | Logging in, navigating, searching, reading profiles, classifying, explainability, quality, reviews, overrides, and the simulation sandbox. |

## Suggested reading order

1. **DEPLOYMENT_GUIDE.md** — get the staging environment running.
2. **ADMINISTRATOR_GUIDE.md** — set up users, seed data, and configuration.
3. **USER_GUIDE.md** — perform day-to-day tasks.
4. **TESTING_GUIDE.md** — run automated tests and the UAT cases.

## Related UAT package

See [`../uat/INDEX.md`](../uat/INDEX.md) for the UAT Test Plan, Test Cases, Acceptance Criteria, and Demonstration Scenarios.
