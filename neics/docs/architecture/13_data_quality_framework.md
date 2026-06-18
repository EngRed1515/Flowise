# Data Quality Framework

> NEICS — Staging / UAT. See sibling docs in [`INDEX.md`](./INDEX.md).

## 1. Purpose

Data quality is a first-class, measured property of every record in NEICS. The
Data Quality Engine (`app/engine/quality.py`) scores each enterprise across the six
**DAMA DMBOK** dimensions, surfaces validation exceptions, and feeds anomalies to the
manual review queue. Quality scores are stored (`quality_result`) and exposed through
`/api/quality` and the dashboard.

## 2. The six dimensions

| Dimension | What it measures | How it is scored in NEICS |
|---|---|---|
| **Completeness** | Presence of expected attributes | Proportion of a defined set of key fields that are populated (LEI, legal form, residence, ISIC, sector, public/private, control, size, employment, turnover, birth date, …). |
| **Validity** | Conformance to rules/codelists | `1 − 0.25 × (number of ERROR-severity validation findings)`, floored at 0. |
| **Consistency** | Internal/cross-field coherence | `1 − 0.10 × (number of WARN-severity findings)`, floored at 0. |
| **Uniqueness** | Absence of duplication | Penalised when duplicate legal-unit names are detected within an enterprise. |
| **Accuracy** | Confidence in correctness | Proxied by QA state: COMMITTEE-RULED = 1.0, PEER-REVIEWED = 0.85, DRAFT = 0.6. |
| **Timeliness** | Currency of classification | 1.0 if the record has been classified, else 0.5. |

**Overall score** = mean of the six dimensions, recorded per enterprise and aggregated
to dataset level.

## 3. Exceptions

Every quality computation runs the full **Validation Engine** (VR-001..VR-018) and
attaches the findings as `exceptions`, each with `rule_id`, `severity`
(ERROR/WARN/INFO), `message` and recommended `action`. Errors materially reduce the
validity score; warnings reduce consistency.

## 4. Anomaly detection (AI-assisted review input)

Rule-based anomaly detectors flag patterns the framework calls out — and never decide a
classification themselves:

- **Hidden government ownership** — material effective state stake but a private status.
- **ISIC ↔ sector mismatch** — financial activity (ISIC section K) with a non-financial sector.
- **Empty-shell producer** — no premises/employees but not flagged as SPV/holding.
- **Missing FDI flag** — foreign ownership ≥ 10 % with no FDI relationship recorded.

Each anomaly becomes a `review_item` in the manual review queue.

## 5. Quality KPIs (framework targets)

The framework sets operational quality targets that NEICS is designed to report against:

- Classification **error rate ≤ 2 %**
- **Median time-to-classify ≤ 10 working days**
- **LEI coverage of financial-sector entities = 100 %**
- **Override rate ≤ 5 %**

## 6. Dashboards & reporting

- `/api/dashboard` — average quality score, counts by sector/size/control/quality flag.
- `/api/quality` — dataset-level scores, per-enterprise scores, and the full exception list.
- `docs/reports/data_quality_validation_report.md` — system-generated quality report.
- The HTML walkthrough's **Data Quality Dashboard** and **Validation & Exception Center**
  render these live from the seeded dataset.
