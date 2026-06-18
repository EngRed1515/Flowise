# NEICS — Acceptance Criteria

**National Enterprise Intelligence and Classification System (NEICS)** — State of Qatar NSO/NSC
Phase: Staging / UAT (no production deployment) · Version 1.0 · Date 2026-06-18

This document defines the measurable criteria that NEICS must satisfy during UAT for the system to be recommended for production approval (a future-phase decision). Each criterion has a measurement method, a target, and a blank result/verdict to be completed during acceptance evaluation. All criteria are evaluated against the isolated staging environment and the seeded golden dataset (28 enterprises).

## 1. Acceptance categories and weighting

| Category | Intent |
|---|---|
| Functional coverage | All in-scope functions tested and passing |
| Methodology correctness & traceability | Standards-compliant determinations, fully traceable |
| Classification accuracy | Golden test set reproduced exactly |
| Validation enforcement | All ERROR rules enforced |
| Security & RBAC | Access control enforced for every role |
| Explainability | Every classification explainable |
| Auditability | Every change audited and temporally versioned |
| Data quality | Quality KPIs within framework thresholds |
| Performance & reliability | Staging non-functional targets met |
| Defects | No critical/unresolved blocking defects |

## 2. Measurable acceptance criteria

| ID | Criterion | Target | Measurement method | Result | Verdict |
|---|---|---|---|---|---|
| AC-01 | Functional coverage — UAT execution | 100% of planned cases executed | UAT_TEST_CASES execution log (168 cases) | | |
| AC-02 | Functional coverage — pass rate | ≥ 98% pass overall; 100% of Critical cases pass | UAT pass/fail tally | | |
| AC-03 | Methodology traceability | 100% of the 18 tests and ~40 rules traceable to standards | Methodology traceability matrix (`docs/reports/`) reconciled to `GET /api/tests`, `GET /api/rules`, `GET /api/standards` | | |
| AC-04 | Classification accuracy (golden set) | 28/28 expected sector verdicts | Classify all 28; compare to baseline (UAT-CLS-046) | | |
| AC-05 | Classification accuracy — public/private | 28/28 expected public/private verdicts | Classify all 28; compare to baseline | | |
| AC-06 | Control determination correctness | 100% of seeded control cases (MAJ-VOTE, BOARD, GOLDEN, BO-CHAIN, NONE, etc.) match baseline | Inspect control_flag per entity vs baseline | | |
| AC-07 | FDI determination correctness | 100% of FDI cases (INWARD-FULL, INWARD-ASSOC, ROUND-TRIP, NONE) match baseline; 10% threshold honoured | UAT-CLS-024..026, UAT-SIM-004 | | |
| AC-08 | ERROR-severity validation enforcement | 100% of ERROR-severity rules among VR-001..VR-018 block finalisation | Trigger each ERROR rule; confirm block (Section 5 cases) | | |
| AC-09 | WARNING/INFO non-blocking | 100% of WARNING/INFO findings surface without blocking | UAT-VAL-020 | | |
| AC-10 | RBAC enforcement | 100% of role permissions enforced for all 7 roles (Administrator, Methodologist, Data Steward, Classifier, Reviewer, Auditor, Analyst) | Section 1 RBAC cases vs permission matrix | | |
| AC-11 | Explainability coverage | Explainability present for 100% of classifications | `GET /api/enterprises/{id}/explain` for all classified entities (UAT-EXP-006) | | |
| AC-12 | Audit coverage | Audit entry present for 100% of changes (enterprise, ownership, classification, rule, override) | Audit-trail cases (Section 10); spot-check after each write | | |
| AC-13 | Temporal versioning | 100% of superseded classifications retained and reconstructable | `GET /api/enterprises/{id}/history` (UAT-AUD-003/004) | | |
| AC-14 | Quality scoring coverage | Quality score with six DAMA dimensions for 100% of enterprises | `GET /api/quality` / profile (Section 6) | | |
| AC-15 | Data-quality KPI — error rate | Classification error rate ≤ 2% on the golden set | (Incorrect verdicts / total determinations) | | |
| AC-16 | Data-quality KPI — time-to-classify | Median time-to-classify ≤ 10 working days (operational KPI; staging classification latency recorded for reference) | Operational metric definition confirmed; staging per-call latency recorded | | |
| AC-17 | Data-quality KPI — override rate | Override rate ≤ 5% | Overrides / total classifications (dashboard) | | |
| AC-18 | LEI coverage of financial entities | 100% of financial-sector (S.12x) entities carry a valid LEI (ISO 17442) | VR-016 evaluation across S.12x entities | | |
| AC-19 | Performance — single classification | `POST /classify` returns within 3 s (staging, single entity) | Timed API calls | | |
| AC-20 | Performance — profile/read | Read endpoints (`/profile`, `/explain`, `/classification`) return within 2 s | Timed API calls | | |
| AC-21 | Performance — batch classify | Classifying all 28 entities completes within 60 s | Timed batch run | | |
| AC-22 | Reliability — health | `GET /health` healthy throughout UAT; no unhandled 5xx during scripted runs | Health checks + error-log review | | |
| AC-23 | Critical defects | Zero open Critical defects at exit | Defect log | | |
| AC-24 | High defects | Zero open High defects without an agreed, time-bound remediation plan | Defect log | | |
| AC-25 | Standards anchoring | Standards repository lists SNA 2025, GFS 2014, BPM6, BD4, ISIC Rev.4 and supporting frameworks | `GET /api/standards` (UAT-MET-001) | | |
| AC-26 | Reference completeness | Reference codelists (sectors, legal-forms, ISIC, size-thresholds, domain codelists) present and used by validation | Section 7 cases | | |
| AC-27 | Isolation integrity | No live-provider/production connectivity during UAT | Configuration & network review (Deployment Guide isolation section) | | |
| AC-28 | Demonstration scenarios | All 6 end-to-end demonstration scenarios executed with expected outputs | `DEMONSTRATION_SCENARIOS.md` results | | |

## 3. Production-approval rule

Production approval may be **recommended** only if **all** of the following hold:

1. AC-01, AC-02, AC-03, AC-04, AC-05 are met in full (functional coverage, traceability, and 28/28 golden accuracy on both sector and public/private).
2. AC-08, AC-10, AC-11, AC-12, AC-13 are met in full (ERROR-rule enforcement, RBAC, explainability, audit, temporal versioning).
3. AC-15, AC-17, AC-18 meet the framework KPI thresholds (error ≤ 2%, override ≤ 5%, LEI coverage 100%).
4. AC-23 holds (zero open Critical defects) and AC-24 has an accepted plan for any High defects.
5. All 28 acceptance criteria have a recorded result and verdict.

Note: AC-16 (median time-to-classify ≤ 10 working days) is an operational throughput KPI realised in production operations; for UAT it is confirmed by definition and supported by staging latency evidence, not by elapsed-day measurement on synthetic data.

## 4. Sign-off

| Role | Name | Decision (Accept / Accept with conditions / Reject) | Date | Signature |
|---|---|---|---|---|
| UAT Lead (NSC) | | | | |
| Lead Methodologist | | | | |
| Enterprise Architecture | | | | |
| Data Governance Lead | | | | |
| NSC Management Sponsor | | | | |
