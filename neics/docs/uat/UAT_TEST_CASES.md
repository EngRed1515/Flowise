# NEICS — UAT Test Cases

**National Enterprise Intelligence and Classification System (NEICS)** — State of Qatar NSO/NSC
Phase: Staging / UAT (no production deployment) · Version 1.0 · Date 2026-06-18

## How to use this document

- Each case carries a unique **Test ID** (`UAT-<AREA>-NNN`), Description, Preconditions, Steps, Expected Result, and blank **Actual Result** and **Pass/Fail** columns to be completed during execution.
- "Log in as `<user>`" uses the demo credentials (e.g., `classifier/classifier123`). API steps assume a JWT obtained via `POST /api/auth/login` and sent as `Authorization: Bearer <token>`.
- Enterprise identifiers refer to seeded records, e.g. `QA-ENT-20260000002` (workbook samples `…0000001..006, …0000099`) and UAT entities `QA-ENT-2026000000010..030`.
- Expected results are stated against the golden baseline. The engine reproduces 28/28 expected sector and public/private verdicts.

A running cumulative count is shown after each area. A summary table appears at the end (Section 15).

---

## 1. Authentication & RBAC / Security

| Test ID | Description | Preconditions | Steps | Expected Result | Actual | P/F |
|---|---|---|---|---|---|---|
| UAT-SEC-001 | Valid login issues JWT | `admin` user seeded | `POST /api/auth/login` form `username=admin&password=admin123` | HTTP 200; response contains `access_token` and `token_type=bearer` | | |
| UAT-SEC-002 | Invalid password rejected | `admin` seeded | `POST /api/auth/login` with `password=wrong` | HTTP 401; no token issued | | |
| UAT-SEC-003 | Unknown user rejected | — | `POST /api/auth/login` `username=ghost` | HTTP 401 | | |
| UAT-SEC-004 | Current-user identity | Valid token | `GET /api/auth/me` with bearer token | HTTP 200; returns username and role of the token holder | | |
| UAT-SEC-005 | Unauthenticated access blocked | — | `GET /api/enterprises` with no token | HTTP 401 | | |
| UAT-SEC-006 | Expired/invalid token blocked | Tampered token | `GET /api/auth/me` with malformed bearer | HTTP 401 | | |
| UAT-SEC-007 | Administrator full access | `admin` token | `GET /api/admin/users` and `GET /api/admin/roles` | HTTP 200; user and role lists returned | | |
| UAT-SEC-008 | Methodologist may author rules | `methodologist` token | `POST /api/rules/{id}/test` and rule authoring action | Permitted (HTTP 2xx); enterprise write actions denied (403) | | |
| UAT-SEC-009 | Data Steward writes enterprise & classifies | `steward` token | `POST /api/enterprises`, then `POST /api/enterprises/{id}/classify` | Both permitted (HTTP 2xx) | | |
| UAT-SEC-010 | Classifier writes enterprise & classifies | `classifier` token | `POST /api/enterprises`, `POST /api/enterprises/{id}/classify` | Permitted; ownership-authoring restricted per matrix | | |
| UAT-SEC-011 | Reviewer can override | `reviewer` token | `POST /api/enterprises/{id}/override` | Permitted (HTTP 2xx) | | |
| UAT-SEC-012 | Analyst is read-only | `analyst` token | `POST /api/enterprises` | HTTP 403 Forbidden; `GET /api/enterprises` permitted | | |
| UAT-SEC-013 | Auditor reads audit/quality only | `auditor` token | `GET /api/audit`, `GET /api/quality`; then `POST /api/enterprises` | Reads permitted; write denied (403) | | |
| UAT-SEC-014 | Classifier cannot manage users | `classifier` token | `GET /api/admin/users` | HTTP 403 | | |
| UAT-SEC-015 | Reviewer cannot author rules | `reviewer` token | Rule-authoring action | HTTP 403; `POST /api/reviews/{id}/resolve` permitted | | |

**Cumulative: 15**

---

## 2. Enterprise Master Data (CRUD)

| Test ID | Description | Preconditions | Steps | Expected Result | Actual | P/F |
|---|---|---|---|---|---|---|
| UAT-ENT-001 | List enterprises | Seed loaded | `GET /api/enterprises` as `analyst` | HTTP 200; 28 seeded enterprises returned | | |
| UAT-ENT-002 | Retrieve single enterprise | Seed loaded | `GET /api/enterprises/QA-ENT-20260000001` (resolve to id) | HTTP 200; energy SOE record returned | | |
| UAT-ENT-003 | Create enterprise | `classifier` token | `POST /api/enterprises` with valid legal name, legal form, residence | HTTP 201; new enterprise id returned | | |
| UAT-ENT-004 | Create rejected for read-only role | `analyst` token | `POST /api/enterprises` | HTTP 403 | | |
| UAT-ENT-005 | Update enterprise | `steward` token | `PUT /api/enterprises/{id}` changing legal form | HTTP 200; updated value persisted | | |
| UAT-ENT-006 | Retrieve full profile | Seed loaded | `GET /api/enterprises/QA-ENT-20260000005/profile` (family holding) | HTTP 200; profile includes identity, ownership, latest classification, quality | | |
| UAT-ENT-007 | Profile of unclassified entity | New entity created | `GET /api/enterprises/{id}/profile` before classify | HTTP 200; classification block empty/pending | | |
| UAT-ENT-008 | Not-found handling | — | `GET /api/enterprises/QA-ENT-99999999999` | HTTP 404 | | |
| UAT-ENT-009 | Mandatory-field enforcement on create | `classifier` token | `POST /api/enterprises` omitting legal name | HTTP 422 validation error | | |
| UAT-ENT-010 | Update triggers audit entry | `steward` token | Update an enterprise, then `GET /api/enterprises/{id}/history` | History shows a new versioned change record | | |
| UAT-ENT-011 | Reference integrity on legal form | `classifier` token | Create with legal form from `GET /api/reference/legal-forms` | Accepted; invalid legal form rejected (422) | | |
| UAT-ENT-012 | Search/filter enterprises | Seed loaded | `GET /api/enterprises` with name/sector filter | Returns the matching subset only | | |

**Cumulative: 27**

---

## 3. Ownership & Control logic

| Test ID | Description | Preconditions | Steps | Expected Result | Actual | P/F |
|---|---|---|---|---|---|---|
| UAT-OWN-001 | Add ownership relationship | `steward` token | `POST /api/enterprises/{id}/ownership` with owner + 60% equity | HTTP 201; relationship stored | | |
| UAT-OWN-002 | Retrieve ownership | Ownership present | `GET /api/enterprises/QA-ENT-20260000003/ownership` (free-zone chemicals) | HTTP 200; owner list with shares | | |
| UAT-OWN-003 | Majority-vote control detected | Listed corp 62% state | Classify `QA-ENT-2026000000012`; inspect control | control_flag = MAJ-VOTE | | |
| UAT-OWN-004 | Board control with 0% equity | Dispersed ownership + board-control entity | Classify the dispersed-ownership board-control entity | control_flag = BOARD; public_private = PUB-NFC | | |
| UAT-OWN-005 | Golden-share control (substance over form) | PPP SPV 49% gov + golden share | Classify the PPP SPV | control_flag = GOLDEN; public_private = PUB-NFC | | |
| UAT-OWN-006 | Beneficial-owner chain aggregation | Trading co 45%+15% state (`QA-ENT-20260000099`) | Classify; inspect control | control_flag = BO-CHAIN; public_private = PUB-NFC; sector S.11 | | |
| UAT-OWN-007 | Multi-level ownership chain | SWF cascade `QA-ENT-2026000000025` | `GET /api/enterprises/{id}/ownership` then classify | Chain resolved through non-resident QIA subsidiary; multi-level recognised | | |
| UAT-OWN-008 | Ultimate controlling institutional unit (UCI) | SWF cascade `QA-ENT-2026000000025` | Inspect explainability/UCI in classification | UCI = government | | |
| UAT-OWN-009 | Non-controlling minority stake | Family group 15% non-controlling state stake | Classify the private family group | control_flag = NONE (no control from 15%); public_private = PRV-NFC | | |
| UAT-OWN-010 | Nine effective-control indicators evaluated | Any controlled entity | Inspect T8 trace | All nine ownership/effective-control indicators evaluated and reported | | |
| UAT-OWN-011 | Contractual / financing / dominant control values | Seeded relevant entity | Classify; inspect control | Appropriate value among CONTRACT/FINANCING/DOMINANT/REGULATORY/KEY-PERS applied where indicated | | |
| UAT-OWN-012 | Ownership update re-evaluates control | Existing entity | Change ownership share to majority, reclassify | control_flag transitions to MAJ-VOTE; history records change | | |
| UAT-OWN-013 | 50%/50% JV control resolution | State+foreign 65/35 JV (`QA-ENT-2026000000023`) | Classify | public_private = PUB-NFC (state-controlled JV) | | |

**Cumulative: 40**

---

## 4. Classification methodology (dimensions, rules, 12 case studies)

### 4.1 Per-dimension and per-test coverage

| Test ID | Description | Preconditions | Steps | Expected Result | Actual | P/F |
|---|---|---|---|---|---|---|
| UAT-CLS-001 | T1 Statistical Unit | Seed loaded | Classify any enterprise; inspect T1 | T1 confirms a valid statistical unit | | |
| UAT-CLS-002 | T2 Institutional Unit | Quasi-corporation branch (`QA-ENT-2026000000019`) | Classify; inspect T2 | Recognised as institutional unit / quasi-corporation | | |
| UAT-CLS-003 | T3 Residence — resident | Energy SOE `QA-ENT-20260000001` | Classify; inspect residence | residence = RES | | |
| UAT-CLS-004 | T3 Residence — foreign manufacturer | Free-zone foreign manufacturer (`QA-ENT-2026000000022`) | Classify; inspect residence | Treated as resident producing unit; FCC sector; FDI INWARD where applicable | | |
| UAT-CLS-005 | T3 Residence — MULTI | Multi-territory operating entity | Classify | residence = MULTI where criteria met | | |
| UAT-CLS-006 | T4 ISIC activity | Any entity with activity data | Classify; inspect T4 | ISIC Rev.4 code assigned and reported | | |
| UAT-CLS-007 | T5 Institutional Sector — S.11 | Energy SOE `QA-ENT-20260000001` | Classify | sector_code = S.11 | | |
| UAT-CLS-008 | T5 Sector — S.122 deposit-taking | Bank `QA-ENT-20260000002` | Classify | sector_code = S.122; public_private = PUB-FC; control = MAJ-VOTE | | |
| UAT-CLS-009 | T5 Sector — S.126 financial auxiliary | QFC asset manager `QA-ENT-20260000004` | Classify | sector_code = S.126; public_private = FCC | | |
| UAT-CLS-010 | T5 Sector — S.127 (fund) | Investment fund (`QA-ENT-2026000000017`) | Classify | sector_code = S.127; public_private = PRV-FC | | |
| UAT-CLS-011 | T5 Sector — S.128 insurance | Private insurance (`QA-ENT-2026000000016`) | Classify | sector_code = S.128; public_private = PRV-FC | | |
| UAT-CLS-012 | T5 Sector — S.13 General Government | Government ministry/authority (`QA-ENT-2026000000010`) | Classify | sector_code = S.13; public_private = GG | | |
| UAT-CLS-013 | T5 Sector — S.14 households | Sole proprietor household enterprise (`QA-ENT-2026000000018`) | Classify | sector_code = S.14 | | |
| UAT-CLS-014 | T5 Sector — S.15 NPISH | NPISH sports club (`QA-ENT-2026000000015`) | Classify | sector_code = S.15; public_private = NPISH | | |
| UAT-CLS-015 | T6 Public Sector Boundary | Energy SOE `QA-ENT-20260000001` | Classify; inspect T6 | Inside public-sector boundary; public_private = PUB-NFC | | |
| UAT-CLS-016 | T7 Market / Non-Market (50% rule) | Government authority vs market SOE | Classify each; inspect T7 | Government unit = NON-MARKET; SOE selling at economically significant prices = MARKET | | |
| UAT-CLS-017 | T7 Non-market charitable foundation | Charitable foundation `QA-ENT-20260000006` | Classify | sector_code = S.13; public_private = GG; market_status = NON-MARKET | | |
| UAT-CLS-018 | T8 Ownership & Effective Control | See UAT-OWN-010 | Classify; inspect T8 | Nine indicators evaluated; control_flag set | | |
| UAT-CLS-019 | T9 Listed Company | Listed public corp 62% state (`QA-ENT-2026000000012`) | Classify; inspect T9 | Listed flag set; combined with control → PUB-NFC | | |
| UAT-CLS-020 | T10 Size — MICRO | Micro retailer (`QA-ENT-2026000000029`) | Classify | size_class = MICRO (1–9 FTE / ≤ QAR 3m) | | |
| UAT-CLS-021 | T10 Size — LARGE | Large private industrial (`QA-ENT-2026000000030`) | Classify | size_class = LARGE (250+ FTE / > QAR 200m) | | |
| UAT-CLS-022 | T10 Size — higher criterion governs | Entity with small headcount but large turnover | Classify | Higher of headcount/turnover determines class | | |
| UAT-CLS-023 | T11 Group & Consolidation | Empty-shell holding (`QA-ENT-2026000000026`) | Classify | special_entity_flag = CONSOLIDATE-PARENT | | |
| UAT-CLS-024 | T12 FDI — INWARD-FULL | Foreign MNE subsidiary 80% (`QA-ENT-2026000000028`) | Classify | fdi_flag = INWARD-FULL; public_private = FCC | | |
| UAT-CLS-025 | T12 FDI — ROUND-TRIP | SWF cascade `QA-ENT-2026000000025` | Classify | fdi_flag = ROUND-TRIP; UCI = government; PUB-NFC | | |
| UAT-CLS-026 | T12 FDI — 10% threshold | Entity with 8% vs 12% foreign equity | Classify both | 8% → not FDI (NONE); 12% → FDI relationship recognised | | |
| UAT-CLS-027 | T13 Special Entity — HOLDING/SPV | PPP SPV / holding entities | Classify | special_entity_flag = SPV / HOLDING as appropriate | | |
| UAT-CLS-028 | T14 Data Source Hierarchy | Entity with conflicting source values | Classify; inspect T14 | Higher-priority source value selected per hierarchy | | |
| UAT-CLS-029 | T15 Conflict Resolution | Entity with conflicting indicators | Classify; inspect T15 | Conflict resolved deterministically; rationale recorded | | |
| UAT-CLS-030 | T16 Governance | Any classification | Inspect T16 | Governance checkpoints recorded (authorisation, review status) | | |
| UAT-CLS-031 | T17 QA | Any classification | Inspect T17 | QA checks executed; quality flags reported | | |
| UAT-CLS-032 | T18 Final Record | Any classification | Inspect final record | Consolidated final classification across all nine dimensions persisted | | |
| UAT-CLS-033 | Reclassification on data change | Classified entity | Change ownership, `POST /classify` again | New version supersedes prior; prior retained in history | | |

### 4.2 Twelve framework case studies

| Test ID | Case study | Enterprise | Steps | Expected Result | Actual | P/F |
|---|---|---|---|---|---|---|
| UAT-CLS-034 | Government ministry & authority | `QA-ENT-2026000000010` / `…011` | Classify | sector S.13; public_private = GG; NON-MARKET | | |
| UAT-CLS-035 | State energy SOE | `QA-ENT-20260000001` | Classify | sector S.11; PUB-NFC; MARKET | | |
| UAT-CLS-036 | Listed public corporation, 62% state | `QA-ENT-2026000000012` | Classify | PUB-NFC; control MAJ-VOTE; listed | | |
| UAT-CLS-037 | Private family group, 15% non-controlling state | `QA-ENT-2026000000013` | Classify | PRV-NFC; control NONE; sector S.11 | | |
| UAT-CLS-038 | Mixed bank, 51% state | `QA-ENT-2026000000014` | Classify | sector S.122; PUB-FC; control MAJ-VOTE | | |
| UAT-CLS-039 | State + foreign 65/35 JV | `QA-ENT-2026000000023` | Classify | PUB-NFC (state-controlled); FDI INWARD-ASSOC where applicable | | |
| UAT-CLS-040 | PPP SPV 49% gov + golden share | `QA-ENT-2026000000024` | Classify | PUB-NFC via GOLDEN (substance over form); SPV | | |
| UAT-CLS-041 | SWF cascade resident developer 70% via non-resident QIA subsidiary | `QA-ENT-2026000000025` | Classify | PUB-NFC; fdi ROUND-TRIP; multi-level chain; UCI = government | | |
| UAT-CLS-042 | Empty-shell holding | `QA-ENT-2026000000026` | Classify | special_entity_flag = CONSOLIDATE-PARENT | | |
| UAT-CLS-043 | Dispersed ownership + board control, 0% equity | `QA-ENT-2026000000027` | Classify | PUB-NFC via BOARD | | |
| UAT-CLS-044 | Foreign MNE subsidiary 80% | `QA-ENT-2026000000028` | Classify | FCC; fdi INWARD-FULL | | |
| UAT-CLS-045 | Free-zone foreign manufacturer | `QA-ENT-2026000000022` | Classify | sector S.11; FCC; resident producing unit | | |
| UAT-CLS-046 | Full golden-set regression | All 28 seeded entities | Classify all; compare to baseline | 28/28 expected sector + public/private verdicts reproduced | | |

**Cumulative: 86**

---

## 5. Validation rules VR-001..VR-018

Each rule is exercised with at least one record that triggers it. ERROR-severity findings must block finalisation; WARNING/INFO must surface without blocking.

| Test ID | Rule | Description | Steps | Expected Result | Actual | P/F |
|---|---|---|---|---|---|---|
| UAT-VAL-001 | VR-001 | Mandatory identity completeness | Submit entity missing legal name | VR-001 raised; finalisation blocked if ERROR | | |
| UAT-VAL-002 | VR-002 | Valid legal form against reference | Submit invalid legal form | VR-002 raised | | |
| UAT-VAL-003 | VR-003 | Residence value valid (RES/NRES/MULTI) | Submit invalid residence | VR-003 raised | | |
| UAT-VAL-004 | VR-004 | ISIC code validity (Rev.4) | Submit non-existent ISIC code | VR-004 raised | | |
| UAT-VAL-005 | VR-005 | Sector code in allowed set | Submit out-of-range sector | VR-005 raised | | |
| UAT-VAL-006 | VR-006 | Ownership shares sum within tolerance | Owners sum to 130% | VR-006 raised | | |
| UAT-VAL-007 | VR-007 | Owner reference exists | Owner id not in register | VR-007 raised | | |
| UAT-VAL-008 | VR-008 | No self-ownership cycle | Entity owns itself / circular chain | VR-008 raised | | |
| UAT-VAL-009 | VR-009 | Control flag consistent with ownership | Control MAJ-VOTE but max share 5% | VR-009 raised | | |
| UAT-VAL-010 | VR-010 | Public/private consistent with control | PUB-NFC with no public control evidence | VR-010 raised | | |
| UAT-VAL-011 | VR-011 | Market status consistent with sector | S.13 unit flagged MARKET without basis | VR-011 raised | | |
| UAT-VAL-012 | VR-012 | Size class consistent with FTE/turnover | size LARGE with 3 FTE / QAR 1m | VR-012 raised | | |
| UAT-VAL-013 | VR-013 | FDI flag consistent with foreign equity | INWARD-FULL with 0% foreign equity | VR-013 raised | | |
| UAT-VAL-014 | VR-014 | FDI 10% threshold respected | FDI flag set below 10% without basis | VR-014 raised | | |
| UAT-VAL-015 | VR-015 | Special-entity flag consistency | SPV without qualifying attributes | VR-015 raised | | |
| UAT-VAL-016 | VR-016 | LEI present/valid for financial entities | S.12x entity missing LEI | VR-016 raised | | |
| UAT-VAL-017 | VR-017 | Temporal validity of values (effective dates) | Effective date after expiry date | VR-017 raised | | |
| UAT-VAL-018 | VR-018 | Final record completeness before publish | Finalise with a missing dimension | VR-018 raised; finalisation blocked | | |
| UAT-VAL-019 | All | Clean record passes all rules | Submit a fully valid seeded entity | No ERROR findings; classification finalises | | |
| UAT-VAL-020 | Severity | WARNING does not block | Record triggering only a WARNING rule | Classification proceeds; warning recorded | | |

**Cumulative: 106**

---

## 6. Data Quality (six DAMA dimensions)

| Test ID | Description | Steps | Expected Result | Actual | P/F |
|---|---|---|---|---|---|
| UAT-DQ-001 | Quality score retrievable | `GET /api/enterprises/{id}/profile` or `GET /api/quality` | Quality score and six dimension sub-scores returned | | |
| UAT-DQ-002 | Completeness dimension | Entity with missing fields | Completeness score reduced; gap listed | | |
| UAT-DQ-003 | Accuracy dimension | Entity with implausible value | Accuracy score reflects the issue | | |
| UAT-DQ-004 | Consistency dimension | Conflicting cross-field values | Consistency score reduced | | |
| UAT-DQ-005 | Validity dimension | Value failing a codelist | Validity score reflects VR finding | | |
| UAT-DQ-006 | Timeliness dimension | Stale reference date | Timeliness score reflects staleness | | |
| UAT-DQ-007 | Uniqueness dimension | Duplicate identity attributes | Uniqueness score reduced; duplicate flagged | | |
| UAT-DQ-008 | Quality exception → review item | Entity below quality threshold | Validation/quality exception generated and visible in Review Center | | |
| UAT-DQ-009 | Quality dashboard aggregation | `GET /api/quality` | Portfolio-level quality KPIs aggregated across the 28 entities | | |

**Cumulative: 115**

---

## 7. Metadata & Standards repositories

| Test ID | Description | Steps | Expected Result | Actual | P/F |
|---|---|---|---|---|---|
| UAT-MET-001 | List standards | `GET /api/standards` | SNA 2025, GFS 2014, BPM6, BD4, ISIC Rev.4, etc. listed | | |
| UAT-MET-002 | Metadata catalogue | `GET /api/metadata` | Variable/metadata definitions returned (GSIM/SDMX-aligned) | | |
| UAT-MET-003 | Sector reference | `GET /api/reference/sectors` | S.11..S.2 with sub-sectors S.121–S.129, S.1311–S.1314 | | |
| UAT-MET-004 | Legal forms reference | `GET /api/reference/legal-forms` | Qatar legal-form codelist returned | | |
| UAT-MET-005 | ISIC reference | `GET /api/reference/isic` | ISIC Rev.4 hierarchy returned | | |
| UAT-MET-006 | Size thresholds reference | `GET /api/reference/size-thresholds` | Qatar thresholds (MICRO/SMALL/MEDIUM/LARGE) returned | | |
| UAT-MET-007 | Generic codelist | `GET /api/reference/codelist/{domain}` for a known domain | Codelist values returned | | |
| UAT-MET-008 | Tests catalogue | `GET /api/tests` | All 18 tests (T1–T18) listed with descriptions | | |

**Cumulative: 123**

---

## 8. Rules Engine & rule testing

| Test ID | Description | Steps | Expected Result | Actual | P/F |
|---|---|---|---|---|---|
| UAT-RUL-001 | List rules | `GET /api/rules` | ~40 rules returned with metadata | | |
| UAT-RUL-002 | Retrieve a rule | `GET /api/rules/{id}` | Rule definition incl. expression, severity, effective/expiry dates | | |
| UAT-RUL-003 | Rule test harness | `POST /api/rules/{id}/test` with sample facts | Returns evaluation result (fired / not fired) and trace | | |
| UAT-RUL-004 | No hard-coding (data-driven) | Inspect rule store vs behaviour | Classification logic sourced from rule records, not code constants | | |
| UAT-RUL-005 | Rule effective-dating | Rule with future effective date | Rule not applied before its effective date | | |
| UAT-RUL-006 | Rule expiry | Rule past expiry date | Expired rule not applied | | |
| UAT-RUL-007 | Methodologist authors a rule | `methodologist` token; create/version a rule | Permitted; version recorded | | |
| UAT-RUL-008 | Non-methodologist cannot author | `classifier` token; attempt rule authoring | HTTP 403 | | |

**Cumulative: 131**

---

## 9. Explainability

| Test ID | Description | Steps | Expected Result | Actual | P/F |
|---|---|---|---|---|---|
| UAT-EXP-001 | Explain endpoint returns trace | `GET /api/enterprises/QA-ENT-20260000002/explain` | Full determination trace returned | | |
| UAT-EXP-002 | Tests cited | Inspect trace | Each applied test (T1–T18) listed with outcome | | |
| UAT-EXP-003 | Rules cited | Inspect trace | Each fired rule referenced by id | | |
| UAT-EXP-004 | Per-dimension rationale | Inspect trace | Rationale present for each of the nine dimensions | | |
| UAT-EXP-005 | Confidence reported | Inspect trace | Confidence indicator present for the classification | | |
| UAT-EXP-006 | Explainability for 100% | Classify all 28, request explain for each | Every classification has a non-empty trace | | |

**Cumulative: 137**

---

## 10. Audit & temporal versioning

| Test ID | Description | Steps | Expected Result | Actual | P/F |
|---|---|---|---|---|---|
| UAT-AUD-001 | Audit log accessible | `GET /api/audit` as `auditor` | HTTP 200; chronological change records | | |
| UAT-AUD-002 | Change creates audit entry | Update entity then `GET /api/audit` | New entry with actor, timestamp, before/after | | |
| UAT-AUD-003 | Classification history | `GET /api/enterprises/{id}/history` | All classification versions listed | | |
| UAT-AUD-004 | Temporal point-in-time | Inspect history for superseded version | Prior version retained and reconstructable | | |
| UAT-AUD-005 | Override audited | Reviewer override then `GET /api/audit` | Override captured with actor and justification | | |
| UAT-AUD-006 | Rule change audited | Methodologist edits a rule | Rule-version change recorded in audit | | |

**Cumulative: 143**

---

## 11. Simulation sandbox

| Test ID | Description | Steps | Expected Result | Actual | P/F |
|---|---|---|---|---|---|
| UAT-SIM-001 | What-if classification | `POST /api/simulate` with a candidate entity payload | Returns simulated classification without persisting | | |
| UAT-SIM-002 | No persistence side-effects | Simulate, then `GET /api/enterprises` count | Enterprise count unchanged; no audit entry created | | |
| UAT-SIM-003 | Rule-change simulation | Simulate with an altered ownership share | Outcome reflects the hypothetical input | | |
| UAT-SIM-004 | Threshold sensitivity | Simulate foreign equity at 9% vs 11% | FDI determination flips across the 10% threshold | | |

**Cumulative: 147**

---

## 12. Ingestion / file upload

| Test ID | Description | Steps | Expected Result | Actual | P/F |
|---|---|---|---|---|---|
| UAT-ING-001 | JSON-array ingest | `POST /api/ingest/enterprises` with a valid array | HTTP 2xx; entities created; count reported | | |
| UAT-ING-002 | File upload ingest | `POST /api/ingest/upload` with a supported file | HTTP 2xx; rows parsed and ingested | | |
| UAT-ING-003 | Ingest validation | Ingest with invalid rows | Invalid rows rejected/flagged; valid rows accepted; summary returned | | |
| UAT-ING-004 | Ingest then classify | Ingest new entity, then `POST /classify` | Entity classified successfully | | |
| UAT-ING-005 | Ingest permission | `analyst` token attempts ingest | HTTP 403 | | |

**Cumulative: 152**

---

## 13. Dashboard, Review Center & Reporting

| Test ID | Description | Steps | Expected Result | Actual | P/F |
|---|---|---|---|---|---|
| UAT-GOV-001 | Dashboard loads | `GET /api/dashboard` | Portfolio KPIs (counts by sector, public/private, quality) returned | | |
| UAT-GOV-002 | Review list | `GET /api/reviews` as `reviewer` | Pending review items listed | | |
| UAT-GOV-003 | Resolve review | `POST /api/reviews/{id}/resolve` | Review marked resolved; audit entry created | | |
| UAT-GOV-004 | Override workflow | `POST /api/enterprises/{id}/override` with justification | Manual classification recorded; original retained | | |
| UAT-GOV-005 | Override requires justification | Override without justification | Rejected (422) or flagged per policy | | |
| UAT-GOV-006 | Review generated from exception | Low-quality/ambiguous entity | Review item auto-created and visible | | |
| UAT-GOV-007 | Dashboard reflects overrides | After an override | Override rate KPI updates | | |
| UAT-GOV-008 | Reporting cross-check | Compare dashboard counts to `docs/reports/` outputs | Figures reconcile with verification reports | | |

**Cumulative: 160**

---

## 14. APIs

| Test ID | Description | Steps | Expected Result | Actual | P/F |
|---|---|---|---|---|---|
| UAT-API-001 | Health endpoint | `GET /health` | HTTP 200; healthy status | | |
| UAT-API-002 | Root endpoint | `GET /` | HTTP 200; service identity/version | | |
| UAT-API-003 | OpenAPI docs | Open `/docs` | Interactive OpenAPI UI lists all documented endpoints | | |
| UAT-API-004 | Classify endpoint contract | `POST /api/enterprises/{id}/classify` | Response matches documented schema | | |
| UAT-API-005 | Classification retrieval | `GET /api/enterprises/{id}/classification` | Latest classification returned | | |
| UAT-API-006 | Error contract | Call protected endpoint without token | Consistent 401 error body | | |
| UAT-API-007 | Validation error contract | `POST /api/enterprises` with bad payload | HTTP 422 with field-level details | | |
| UAT-API-008 | Pagination/listing contract | `GET /api/enterprises` | Stable, documented list response shape | | |

**Cumulative: 168**

---

## 15. Summary — test-case counts per area

| # | Area | Cases | Minimum required |
|---|---|---|---|
| 1 | Authentication & RBAC / Security | 15 | ≥ 12 |
| 2 | Enterprise Master Data (CRUD) | 12 | ≥ 10 |
| 3 | Ownership & Control logic | 13 | ≥ 12 |
| 4 | Classification methodology (dimensions, rules, 12 case studies) | 46 | ≥ 30 |
| 5 | Validation rules VR-001..VR-018 | 20 | ≥ 18 |
| 6 | Data Quality | 9 | ≥ 8 |
| 7 | Metadata & Standards repositories | 8 | ≥ 6 |
| 8 | Rules Engine & rule testing | 8 | ≥ 8 |
| 9 | Explainability | 6 | ≥ 6 |
| 10 | Audit & temporal versioning | 6 | ≥ 6 |
| 11 | Simulation sandbox | 4 | ≥ 4 |
| 12 | Ingestion / file upload | 5 | ≥ 5 |
| 13 | Dashboard, Review Center & Reporting | 8 | ≥ 8 |
| 14 | APIs | 8 | ≥ 8 |
| | **Total** | **168** | **≥ 100** |

**Total UAT test cases: 168** (exceeds the required minimum of 100, and meets every per-area minimum).
