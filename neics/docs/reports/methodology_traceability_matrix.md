# Methodology Traceability Matrix

> **NEICS — Staging / UAT environment.** This report is generated automatically by `tools/generate_reports.py` directly from the live classification engine and seeded test database. Generated: 2026-06-18 10:46 UTC.

Framework requirement → System component → Rule → Output. Every classification rule is traceable to one or more international/national standards.

## 1. The 18 classification tests → rules → outputs

| Test | Name | Exec seq | Output dimension | Standard | Rules implementing |
|------|------|----------|------------------|----------|--------------------|
| T1 | Statistical Unit Test | 10 | — | SNA2025 | _(governance/process test — no data rule)_ |
| T2 | Institutional Unit Test | 20 | — | SNA2025 | _(governance/process test — no data rule)_ |
| T3 | Residence Test | 30 | residence | SNA2025/BPM6 | R-T03-001 |
| T4 | Economic Activity (ISIC) Classification | 40 | isic_class | ISIC4 | R-T04-001 |
| T7 | Market vs Non-Market Producer | 50 | market_status | SNA2025 | R-T07-010, R-T07-020, R-T07-030, R-T07-040, R-T07-100 |
| T8 | Ownership & Effective Control | 60 | control_flag | BD4/SNA2025 | R-T08-001 |
| T5 | Institutional Sector Classification | 70 | sector_code | SNA2025 | R-T05-010, R-T05-021, R-T05-022, R-T05-023, R-T05-024, R-T05-025, R-T05-026, R-T05-029, R-T05-030, R-T05-035, R-T05-050, R-T05-100 |
| T6 | Public Sector Boundary Test | 80 | public_private | GFS2014 | R-T06-005, R-T06-010, R-T06-020, R-T06-030, R-T06-035, R-T06-040, R-T06-050, R-T06-100 |
| T9 | Listed Company Classification | 90 | — | QNCS | _(governance/process test — no data rule)_ |
| T10 | Enterprise Size Classification | 100 | size_class | QNCS | R-T10-010, R-T10-020, R-T10-030, R-T10-100 |
| T11 | Enterprise Group & Consolidation | 110 | — | SNA2025 | _(governance/process test — no data rule)_ |
| T12 | Foreign Ownership & FDI | 120 | fdi_flag | BD4 | R-T12-010, R-T12-020, R-T12-030, R-T12-100 |
| T13 | Special Entity Treatment | 130 | special_entity_flag | SNA2025 | R-T13-010, R-T13-020, R-T13-030, R-T13-100 |
| T14 | Data Source Hierarchy | 140 | — | QNCS | _(governance/process test — no data rule)_ |
| T15 | Conflict Resolution | 150 | — | QNCS | _(governance/process test — no data rule)_ |
| T16 | Classification Governance | 160 | — | QNCS | _(governance/process test — no data rule)_ |
| T17 | Quality Assurance | 170 | — | QNCS | _(governance/process test — no data rule)_ |
| T18 | Final Classification Record | 180 | — | SNA2025 | _(governance/process test — no data rule)_ |

## 2. Framework requirement → component coverage

| Framework requirement (deck/workbook) | System component | Evidence |
|---|---|---|
| 18-test classification methodology | Rules Engine + ClassificationTest catalogue | 18 tests seeded; 40 rules |
| Institutional sector (SNA) | ref_institutional_sector + T5 rules | 20 sectors/sub-sectors |
| Public sector boundary (GFS) | T6 rules | PUB-NFC/PUB-FC/GG/PRV-*/FCC/NPISH |
| Market/non-market 50% rule | T7 rules | R-T07-030 sales_cover_pct>50 → MARKET |
| Ownership & effective control (9 indicators) | OwnershipEngine + T8 | control_flag derivation |
| FDI 10% threshold (BD4) | T12 rules | INWARD-FULL/ASSOC/ROUND-TRIP |
| Enterprise size thresholds | ref_size_threshold + T10 rules | MICRO/SMALL/MEDIUM/LARGE |
| Special-entity substance (SPV/holding/empty shell) | T13 rules | HOLDING/SPV/CONSOLIDATE-PARENT |
| ISIC Rev.4 activity coding | ref_isic_section/division/class | 21 sections / 88 divisions / 35 classes |
| Validation rule library (VR-001..018) | Validation Engine | see Rules/Validation report |
| Standards repository | std_standard + std_concept | 16 standards |
| Statistical metadata (GSIM/SDMX) | meta_variable | 31 variables |
| Explainability & audit | classification.trace + audit_entry | per-classification trace stored |
| Temporal versioning / lineage | classification (is_current, version, valid_from/to) | history retained |
| Data quality (DAMA) | quality_result | 6 dimensions scored |
| RBAC & governance | app_user + ROLE_PERMISSIONS | 7 roles |
| Simulation sandbox | /api/simulate | non-persistent what-if |
