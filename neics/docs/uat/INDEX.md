# NEICS — UAT Documentation Index

**National Enterprise Intelligence and Classification System (NEICS)** — State of Qatar NSO/NSC
Phase: Staging / UAT (no production deployment) · Version 1.0 · Date 2026-06-18

This package contains the User Acceptance Testing (UAT) materials for NEICS. The environment is an **isolated staging** deployment seeded with 28 illustrative enterprises; no production data or live data providers are involved.

## Documents

| Document | Purpose |
|---|---|
| [UAT_TEST_PLAN.md](./UAT_TEST_PLAN.md) | Objectives, scope, assumptions, dependencies, environment, roles, entry/exit criteria, approach, defect management, schedule. |
| [UAT_TEST_CASES.md](./UAT_TEST_CASES.md) | 168 detailed test cases across 14 areas, grouped and numbered, with a per-area count summary (minimum required: 100). |
| [ACCEPTANCE_CRITERIA.md](./ACCEPTANCE_CRITERIA.md) | 28 measurable acceptance criteria, the production-approval rule, and sign-off block. |
| [DEMONSTRATION_SCENARIOS.md](./DEMONSTRATION_SCENARIOS.md) | Six end-to-end demonstration scripts (UI click-paths and API calls) with expected outputs. |

## Suggested reading order

1. **UAT_TEST_PLAN.md** — understand scope, environment, and process.
2. **DEMONSTRATION_SCENARIOS.md** — see the major flows end-to-end.
3. **UAT_TEST_CASES.md** — execute the detailed cases.
4. **ACCEPTANCE_CRITERIA.md** — evaluate acceptance and record sign-off.

## Related guides

See [`../guides/INDEX.md`](../guides/INDEX.md) for the Deployment, Testing, Administrator, and User guides, and `../reports/` for the automated verification reports referenced during UAT.
