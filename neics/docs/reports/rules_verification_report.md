# Rules Engine Validation Report

> **NEICS — Staging / UAT environment.** This report is generated automatically by `tools/generate_reports.py` directly from the live classification engine and seeded test database. Generated: 2026-06-18 10:40 UTC.

**Result: 40/40 rules pass their positive + negative test cases.**

For each rule a fact set is synthesised that should trigger it (positive) and one that should not (negative); the engine evaluates both. A rule passes if the positive case matches and the negative case does not. Default/fallback rules have empty logic (they fire when reached in priority order) and are validated as always-true.

| Rule ID | Name | Test | Domain | Output | Standard | Positive | Negative | Result |
|---|---|---|---|---|---|---|---|---|
| `R-T10-010` | Large enterprise | T10 | size_class | size_class=LARGE | QNCS / EU 2003/361/EC | ✅ `{"turnover_qar": 150000000}` | ✅ `{"turnover_qar": 149999999, "employment": 249}` | PASS |
| `R-T10-020` | Medium enterprise | T10 | size_class | size_class=MEDIUM | QNCS | ✅ `{"turnover_qar": 20000000}` | ✅ `{"turnover_qar": 19999999, "employment": 49}` | PASS |
| `R-T10-030` | Small enterprise | T10 | size_class | size_class=SMALL | QNCS | ✅ `{"turnover_qar": 2000000}` | ✅ `{"turnover_qar": 1999999, "employment": 9}` | PASS |
| `R-T10-100` | Micro enterprise | T10 | size_class | size_class=MICRO | QNCS | ✅ `always-true` | ✅ `—` | PASS |
| `R-T12-010` | Round-tripping (ultimately Qatari-controlled) | T12 | fdi_flag | fdi_flag=ROUND-TRIP | OECD BD4 | ✅ `{"foreign_ownership_pct": 10, "uci_is_government": true}` | ✅ `{"foreign_ownership_pct": 9, "uci_is_government": true}` | PASS |
| `R-T12-020` | Inward FDI — full control (>50%) | T12 | fdi_flag | fdi_flag=INWARD-FULL | OECD BD4 | ✅ `{"foreign_ownership_pct": 51}` | ✅ `{"foreign_ownership_pct": 49}` | PASS |
| `R-T12-030` | Inward FDI — associate (10-50%) | T12 | fdi_flag | fdi_flag=INWARD-ASSOC | OECD BD4 | ✅ `{"foreign_ownership_pct": 10}` | ✅ `{"foreign_ownership_pct": 9}` | PASS |
| `R-T12-100` | No FDI relationship | T12 | fdi_flag | fdi_flag=NONE | OECD BD4 | ✅ `always-true` | ✅ `—` | PASS |
| `R-T13-010` | Empty-shell — consolidate with parent | T13 | special_entity_flag | special_entity_flag=CONSOLIDATE-PARENT | SNA 2025 §4 (empty-shell rule) | ✅ `{"has_substance": false}` | ✅ `{"has_substance": true}` | PASS |
| `R-T13-020` | Holding company | T13 | special_entity_flag | special_entity_flag=HOLDING | ISIC Rev.4 / SNA 2025 | ✅ `{"isic_class": "6420"}` | ✅ `{"isic_class": "__not__6420"}` | PASS |
| `R-T13-030` | Trust/fund/SPV | T13 | special_entity_flag | special_entity_flag=SPV | SNA 2025 | ✅ `{"isic_class": "6430"}` | ✅ `{"isic_class": "__not__6430"}` | PASS |
| `R-T13-100` | Not a special entity | T13 | special_entity_flag | special_entity_flag=NONE | SNA 2025 | ✅ `always-true` | ✅ `—` | PASS |
| `R-T03-001` | Residence from sourced centre of economic interest | T3 | residence | residence=residence | SNA 2025 / BPM6 Ch.4 | ✅ `always-true` | ✅ `—` | PASS |
| `R-T04-001` | Principal activity (ISIC Rev.4) | T4 | isic_class | isic_class=isic_class | ISIC Rev.4 | ✅ `always-true` | ✅ `—` | PASS |
| `R-T05-010` | Government body → S.13 | T5 | sector_code | sector_code=S.13 | SNA 2025 | ✅ `{"legal_form_code": "GOV"}` | ✅ `{"legal_form_code": "__not__GOV"}` | PASS |
| `R-T05-021` | Central banking → S.121 | T5 | sector_code | sector_code=S.121 | SNA 2025 | ✅ `{"is_financial": true, "isic_class": "6411"}` | ✅ `{"is_financial": false, "isic_class": "6411"}` | PASS |
| `R-T05-022` | Deposit-taking corporations → S.122 | T5 | sector_code | sector_code=S.122 | SNA 2025 | ✅ `{"is_financial": true, "isic_class": "6419"}` | ✅ `{"is_financial": false, "isic_class": "6419"}` | PASS |
| `R-T05-023` | Fund management → S.126 | T5 | sector_code | sector_code=S.126 | SNA 2025 | ✅ `{"is_financial": true, "isic_class": "6630"}` | ✅ `{"is_financial": false, "isic_class": "6630"}` | PASS |
| `R-T05-024` | Holding/captive financial → S.127 | T5 | sector_code | sector_code=S.127 | SNA 2025 | ✅ `{"is_financial": true, "isic_class": "6420"}` | ✅ `{"is_financial": false, "isic_class": "6420"}` | PASS |
| `R-T05-025` | Insurance → S.128 | T5 | sector_code | sector_code=S.128 | SNA 2025 | ✅ `{"is_financial": true, "isic_class": "6511"}` | ✅ `{"is_financial": false, "isic_class": "6511"}` | PASS |
| `R-T05-026` | Pension funding → S.129 | T5 | sector_code | sector_code=S.129 | SNA 2025 | ✅ `{"is_financial": true, "isic_class": "6530"}` | ✅ `{"is_financial": false, "isic_class": "6530"}` | PASS |
| `R-T05-029` | Other financial corporation → S.12 | T5 | sector_code | sector_code=S.12 | SNA 2025 | ✅ `{"is_financial": true}` | ✅ `{"is_financial": false}` | PASS |
| `R-T05-030` | Government-controlled non-market unit → S.13 | T5 | sector_code | sector_code=S.13 | GFS 2014 / SNA 2025 | ✅ `{"market_status": "NON-MARKET", "government_control": true}` | ✅ `{"market_status": "__not__NON-MARKET", "government_control": true}` | PASS |
| `R-T05-035` | Non-profit non-market unit → S.15 (NPISH) | T5 | sector_code | sector_code=S.15 | SNA 2025 | ✅ `{"is_nonprofit": true, "market_status": "NON-MARKET"}` | ✅ `{"is_nonprofit": false, "market_status": "NON-MARKET"}` | PASS |
| `R-T05-050` | Sole proprietorship → S.14 | T5 | sector_code | sector_code=S.14 | SNA 2025 | ✅ `{"legal_form_code": "SP"}` | ✅ `{"legal_form_code": "__not__SP"}` | PASS |
| `R-T05-100` | Default → S.11 non-financial corporation | T5 | sector_code | sector_code=S.11 | SNA 2025 | ✅ `always-true` | ✅ `—` | PASS |
| `R-T06-005` | Government body → general government | T6 | public_private | public_private=GG | GFS 2014 | ✅ `{"legal_form_code": "GOV"}` | ✅ `{"legal_form_code": "__not__GOV"}` | PASS |
| `R-T06-010` | Government-controlled financial market producer → PUB-FC | T6 | public_private | public_private=PUB-FC | GFS 2014 | ✅ `{"government_control": true, "is_financial": true, "market_status": "MARKET"}` | ✅ `{"government_control": false, "is_financial": true, "market_status": "MARKET"}` | PASS |
| `R-T06-020` | Government-controlled market producer → PUB-NFC | T6 | public_private | public_private=PUB-NFC | GFS 2014 | ✅ `{"government_control": true, "market_status": "MARKET"}` | ✅ `{"government_control": false, "market_status": "MARKET"}` | PASS |
| `R-T06-030` | Government-controlled non-market producer → GG | T6 | public_private | public_private=GG | GFS 2014 | ✅ `{"government_control": true, "market_status": "NON-MARKET"}` | ✅ `{"government_control": false, "market_status": "NON-MARKET"}` | PASS |
| `R-T06-035` | Non-profit non-market unit → NPISH | T6 | public_private | public_private=NPISH | SNA 2025 | ✅ `{"is_nonprofit": true, "market_status": "NON-MARKET"}` | ✅ `{"is_nonprofit": false, "market_status": "NON-MARKET"}` | PASS |
| `R-T06-040` | Foreign-controlled private corporation → FCC | T6 | public_private | public_private=FCC | OECD BD4 | ✅ `{"government_control": false, "uci_is_foreign": true}` | ✅ `{"government_control": true, "uci_is_foreign": true}` | PASS |
| `R-T06-050` | Private financial corporation → PRV-FC | T6 | public_private | public_private=PRV-FC | SNA 2025 | ✅ `{"is_financial": true}` | ✅ `{"is_financial": false}` | PASS |
| `R-T06-100` | Default → PRV-NFC | T6 | public_private | public_private=PRV-NFC | SNA 2025 | ✅ `always-true` | ✅ `—` | PASS |
| `R-T07-010` | Government bodies are non-market | T7 | market_status | market_status=NON-MARKET | GFS 2014 | ✅ `{"legal_form_code": "GOV"}` | ✅ `{"legal_form_code": "__not__GOV"}` | PASS |
| `R-T07-020` | Non-profit not covering costs is non-market | T7 | market_status | market_status=NON-MARKET | SNA 2025 | ✅ `{"is_nonprofit": true, "sales_cover_pct": 49}` | ✅ `{"is_nonprofit": false, "sales_cover_pct": 49}` | PASS |
| `R-T07-030` | Sales cover >50% of production costs → market | T7 | market_status | market_status=MARKET | SNA 2025 — 50% rule | ✅ `{"sales_cover_pct": 51}` | ✅ `{"sales_cover_pct": 49}` | PASS |
| `R-T07-040` | Sales cover ≤50% of production costs → non-market | T7 | market_status | market_status=NON-MARKET | SNA 2025 — 50% rule | ✅ `{"sales_cover_pct": 1}` | ✅ `{"sales_cover_pct": null}` | PASS |
| `R-T07-100` | Default to market producer | T7 | market_status | market_status=MARKET | SNA 2025 | ✅ `always-true` | ✅ `—` | PASS |
| `R-T08-001` | Effective-control mechanism | T8 | control_flag | control_flag=representative_control_flag | SNA 2025 / OECD BD4 | ✅ `always-true` | ✅ `—` | PASS |

## Detailed rule cards

### `R-T10-010` — Large enterprise
- **Test:** T10  •  **Domain:** size_class  •  **Priority:** 10  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** ≥250 FTE or > QAR 200m turnover band.
- **Standard reference:** QNCS / EU 2003/361/EC
- **Inputs required:** —
- **Logic:** `{"any": [{"op": "gte", "field": "turnover_qar", "value": 150000000}, {"op": "gte", "field": "employment", "value": 250}]}`
- **Output:** `{"size_class": {"const": "LARGE"}}`
- **Test case (positive):** `{"turnover_qar": 150000000}` → matched = **True**
- **Test case (negative):** `{"turnover_qar": 149999999, "employment": 249}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T10-020` — Medium enterprise
- **Test:** T10  •  **Domain:** size_class  •  **Priority:** 20  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** 50-249 FTE or QAR 30-200m turnover band.
- **Standard reference:** QNCS
- **Inputs required:** —
- **Logic:** `{"any": [{"op": "gte", "field": "turnover_qar", "value": 20000000}, {"op": "gte", "field": "employment", "value": 50}]}`
- **Output:** `{"size_class": {"const": "MEDIUM"}}`
- **Test case (positive):** `{"turnover_qar": 20000000}` → matched = **True**
- **Test case (negative):** `{"turnover_qar": 19999999, "employment": 49}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T10-030` — Small enterprise
- **Test:** T10  •  **Domain:** size_class  •  **Priority:** 30  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** 10-49 FTE or QAR 3-30m turnover band.
- **Standard reference:** QNCS
- **Inputs required:** —
- **Logic:** `{"any": [{"op": "gte", "field": "turnover_qar", "value": 2000000}, {"op": "gte", "field": "employment", "value": 10}]}`
- **Output:** `{"size_class": {"const": "SMALL"}}`
- **Test case (positive):** `{"turnover_qar": 2000000}` → matched = **True**
- **Test case (negative):** `{"turnover_qar": 1999999, "employment": 9}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T10-100` — Micro enterprise
- **Test:** T10  •  **Domain:** size_class  •  **Priority:** 100  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** 1-9 FTE; up to QAR 3m turnover.
- **Standard reference:** QNCS
- **Inputs required:** —
- **Logic:** `null`
- **Output:** `{"size_class": {"const": "MICRO"}}`
- **Test case (positive):** `{}` → matched = **True**
- **Type:** default/fallback rule
- **Result:** PASS

### `R-T12-010` — Round-tripping (ultimately Qatari-controlled)
- **Test:** T12  •  **Domain:** fdi_flag  •  **Priority:** 10  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Apparent inward FDI through a non-resident vehicle, ultimately Qatari-controlled.
- **Standard reference:** OECD BD4
- **Inputs required:** —
- **Logic:** `{"all": [{"op": "gte", "field": "foreign_ownership_pct", "value": 10}, {"op": "truthy", "field": "uci_is_government"}]}`
- **Output:** `{"fdi_flag": {"const": "ROUND-TRIP"}}`
- **Test case (positive):** `{"foreign_ownership_pct": 10, "uci_is_government": true}` → matched = **True**
- **Test case (negative):** `{"foreign_ownership_pct": 9, "uci_is_government": true}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T12-020` — Inward FDI — full control (>50%)
- **Test:** T12  •  **Domain:** fdi_flag  •  **Priority:** 20  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Foreign majority direct investment — subsidiary.
- **Standard reference:** OECD BD4
- **Inputs required:** —
- **Logic:** `{"op": "gt", "field": "foreign_ownership_pct", "value": 50}`
- **Output:** `{"fdi_flag": {"const": "INWARD-FULL"}}`
- **Test case (positive):** `{"foreign_ownership_pct": 51}` → matched = **True**
- **Test case (negative):** `{"foreign_ownership_pct": 49}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T12-030` — Inward FDI — associate (10-50%)
- **Test:** T12  •  **Domain:** fdi_flag  •  **Priority:** 30  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Direct investment relationship at the 10% threshold; treated as influence.
- **Standard reference:** OECD BD4
- **Inputs required:** —
- **Logic:** `{"op": "gte", "field": "foreign_ownership_pct", "value": 10}`
- **Output:** `{"fdi_flag": {"const": "INWARD-ASSOC"}}`
- **Test case (positive):** `{"foreign_ownership_pct": 10}` → matched = **True**
- **Test case (negative):** `{"foreign_ownership_pct": 9}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T12-100` — No FDI relationship
- **Test:** T12  •  **Domain:** fdi_flag  •  **Priority:** 100  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Foreign ownership below the 10% threshold.
- **Standard reference:** OECD BD4
- **Inputs required:** —
- **Logic:** `null`
- **Output:** `{"fdi_flag": {"const": "NONE"}}`
- **Test case (positive):** `{}` → matched = **True**
- **Type:** default/fallback rule
- **Result:** PASS

### `R-T13-010` — Empty-shell — consolidate with parent
- **Test:** T13  •  **Domain:** special_entity_flag  •  **Priority:** 10  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** No premises, employees or autonomy — consolidated with controlling parent.
- **Standard reference:** SNA 2025 §4 (empty-shell rule)
- **Inputs required:** —
- **Logic:** `{"not": {"op": "truthy", "field": "has_substance"}}`
- **Output:** `{"special_entity_flag": {"const": "CONSOLIDATE-PARENT"}}`
- **Test case (positive):** `{"has_substance": false}` → matched = **True**
- **Test case (negative):** `{"has_substance": true}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T13-020` — Holding company
- **Test:** T13  •  **Domain:** special_entity_flag  •  **Priority:** 20  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Activities of holding companies (owns equity in subsidiaries).
- **Standard reference:** ISIC Rev.4 / SNA 2025
- **Inputs required:** —
- **Logic:** `{"op": "eq", "field": "isic_class", "value": "6420"}`
- **Output:** `{"special_entity_flag": {"const": "HOLDING"}}`
- **Test case (positive):** `{"isic_class": "6420"}` → matched = **True**
- **Test case (negative):** `{"isic_class": "__not__6420"}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T13-030` — Trust/fund/SPV
- **Test:** T13  •  **Domain:** special_entity_flag  •  **Priority:** 30  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Trusts, funds and similar financial entities.
- **Standard reference:** SNA 2025
- **Inputs required:** —
- **Logic:** `{"op": "eq", "field": "isic_class", "value": "6430"}`
- **Output:** `{"special_entity_flag": {"const": "SPV"}}`
- **Test case (positive):** `{"isic_class": "6430"}` → matched = **True**
- **Test case (negative):** `{"isic_class": "__not__6430"}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T13-100` — Not a special entity
- **Test:** T13  •  **Domain:** special_entity_flag  •  **Priority:** 100  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Substantive operating unit.
- **Standard reference:** SNA 2025
- **Inputs required:** —
- **Logic:** `null`
- **Output:** `{"special_entity_flag": {"const": "NONE"}}`
- **Test case (positive):** `{}` → matched = **True**
- **Type:** default/fallback rule
- **Result:** PASS

### `R-T03-001` — Residence from sourced centre of economic interest
- **Test:** T3  •  **Domain:** residence  •  **Priority:** 100  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Residence is taken from the assessed centre of predominant economic interest.
- **Standard reference:** SNA 2025 / BPM6 Ch.4
- **Inputs required:** —
- **Logic:** `null`
- **Output:** `{"residence": {"fact": "residence"}}`
- **Test case (positive):** `{}` → matched = **True**
- **Type:** default/fallback rule
- **Result:** PASS

### `R-T04-001` — Principal activity (ISIC Rev.4)
- **Test:** T4  •  **Domain:** isic_class  •  **Priority:** 100  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Principal activity assigned by largest share of value added.
- **Standard reference:** ISIC Rev.4
- **Inputs required:** —
- **Logic:** `null`
- **Output:** `{"isic_class": {"fact": "isic_class"}}`
- **Test case (positive):** `{}` → matched = **True**
- **Type:** default/fallback rule
- **Result:** PASS

### `R-T05-010` — Government body → S.13
- **Test:** T5  •  **Domain:** sector_code  •  **Priority:** 10  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Ministries, authorities and councils are general government.
- **Standard reference:** SNA 2025
- **Inputs required:** —
- **Logic:** `{"op": "eq", "field": "legal_form_code", "value": "GOV"}`
- **Output:** `{"sector_code": {"const": "S.13"}}`
- **Test case (positive):** `{"legal_form_code": "GOV"}` → matched = **True**
- **Test case (negative):** `{"legal_form_code": "__not__GOV"}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T05-021` — Central banking → S.121
- **Test:** T5  •  **Domain:** sector_code  •  **Priority:** 21  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Central bank sub-sector.
- **Standard reference:** SNA 2025
- **Inputs required:** —
- **Logic:** `{"all": [{"op": "truthy", "field": "is_financial"}, {"op": "eq", "field": "isic_class", "value": "6411"}]}`
- **Output:** `{"sector_code": {"const": "S.121"}}`
- **Test case (positive):** `{"is_financial": true, "isic_class": "6411"}` → matched = **True**
- **Test case (negative):** `{"is_financial": false, "isic_class": "6411"}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T05-022` — Deposit-taking corporations → S.122
- **Test:** T5  •  **Domain:** sector_code  •  **Priority:** 22  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Banks / other depository corporations.
- **Standard reference:** SNA 2025
- **Inputs required:** —
- **Logic:** `{"all": [{"op": "truthy", "field": "is_financial"}, {"op": "in", "field": "isic_class", "value": ["6419"]}]}`
- **Output:** `{"sector_code": {"const": "S.122"}}`
- **Test case (positive):** `{"is_financial": true, "isic_class": "6419"}` → matched = **True**
- **Test case (negative):** `{"is_financial": false, "isic_class": "6419"}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T05-023` — Fund management → S.126
- **Test:** T5  •  **Domain:** sector_code  •  **Priority:** 23  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Financial auxiliaries (fund managers, brokers).
- **Standard reference:** SNA 2025
- **Inputs required:** —
- **Logic:** `{"all": [{"op": "truthy", "field": "is_financial"}, {"op": "eq", "field": "isic_class", "value": "6630"}]}`
- **Output:** `{"sector_code": {"const": "S.126"}}`
- **Test case (positive):** `{"is_financial": true, "isic_class": "6630"}` → matched = **True**
- **Test case (negative):** `{"is_financial": false, "isic_class": "6630"}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T05-024` — Holding/captive financial → S.127
- **Test:** T5  •  **Domain:** sector_code  •  **Priority:** 24  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Captive financial institutions / SPEs.
- **Standard reference:** SNA 2025
- **Inputs required:** —
- **Logic:** `{"all": [{"op": "truthy", "field": "is_financial"}, {"op": "in", "field": "isic_class", "value": ["6420", "6430"]}]}`
- **Output:** `{"sector_code": {"const": "S.127"}}`
- **Test case (positive):** `{"is_financial": true, "isic_class": "6420"}` → matched = **True**
- **Test case (negative):** `{"is_financial": false, "isic_class": "6420"}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T05-025` — Insurance → S.128
- **Test:** T5  •  **Domain:** sector_code  •  **Priority:** 25  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Insurance corporations.
- **Standard reference:** SNA 2025
- **Inputs required:** —
- **Logic:** `{"all": [{"op": "truthy", "field": "is_financial"}, {"op": "in", "field": "isic_class", "value": ["6511", "6512", "6520"]}]}`
- **Output:** `{"sector_code": {"const": "S.128"}}`
- **Test case (positive):** `{"is_financial": true, "isic_class": "6511"}` → matched = **True**
- **Test case (negative):** `{"is_financial": false, "isic_class": "6511"}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T05-026` — Pension funding → S.129
- **Test:** T5  •  **Domain:** sector_code  •  **Priority:** 26  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Autonomous pension funds.
- **Standard reference:** SNA 2025
- **Inputs required:** —
- **Logic:** `{"all": [{"op": "truthy", "field": "is_financial"}, {"op": "eq", "field": "isic_class", "value": "6530"}]}`
- **Output:** `{"sector_code": {"const": "S.129"}}`
- **Test case (positive):** `{"is_financial": true, "isic_class": "6530"}` → matched = **True**
- **Test case (negative):** `{"is_financial": false, "isic_class": "6530"}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T05-029` — Other financial corporation → S.12
- **Test:** T5  •  **Domain:** sector_code  •  **Priority:** 29  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Financial corporation, sub-sector to be refined.
- **Standard reference:** SNA 2025
- **Inputs required:** —
- **Logic:** `{"op": "truthy", "field": "is_financial"}`
- **Output:** `{"sector_code": {"const": "S.12"}}`
- **Test case (positive):** `{"is_financial": true}` → matched = **True**
- **Test case (negative):** `{"is_financial": false}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T05-030` — Government-controlled non-market unit → S.13
- **Test:** T5  •  **Domain:** sector_code  •  **Priority:** 30  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** A government-controlled non-market producer (incl. controlled NPI) is general government.
- **Standard reference:** GFS 2014 / SNA 2025
- **Inputs required:** —
- **Logic:** `{"all": [{"op": "eq", "field": "market_status", "value": "NON-MARKET"}, {"op": "truthy", "field": "government_control"}]}`
- **Output:** `{"sector_code": {"const": "S.13"}}`
- **Test case (positive):** `{"market_status": "NON-MARKET", "government_control": true}` → matched = **True**
- **Test case (negative):** `{"market_status": "__not__NON-MARKET", "government_control": true}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T05-035` — Non-profit non-market unit → S.15 (NPISH)
- **Test:** T5  •  **Domain:** sector_code  •  **Priority:** 35  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Non-market non-profit serving households, not government-controlled.
- **Standard reference:** SNA 2025
- **Inputs required:** —
- **Logic:** `{"all": [{"op": "truthy", "field": "is_nonprofit"}, {"op": "eq", "field": "market_status", "value": "NON-MARKET"}]}`
- **Output:** `{"sector_code": {"const": "S.15"}}`
- **Test case (positive):** `{"is_nonprofit": true, "market_status": "NON-MARKET"}` → matched = **True**
- **Test case (negative):** `{"is_nonprofit": false, "market_status": "NON-MARKET"}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T05-050` — Sole proprietorship → S.14
- **Test:** T5  •  **Domain:** sector_code  •  **Priority:** 50  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Unincorporated household enterprise.
- **Standard reference:** SNA 2025
- **Inputs required:** —
- **Logic:** `{"op": "eq", "field": "legal_form_code", "value": "SP"}`
- **Output:** `{"sector_code": {"const": "S.14"}}`
- **Test case (positive):** `{"legal_form_code": "SP"}` → matched = **True**
- **Test case (negative):** `{"legal_form_code": "__not__SP"}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T05-100` — Default → S.11 non-financial corporation
- **Test:** T5  •  **Domain:** sector_code  •  **Priority:** 100  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Market producer of goods/non-financial services.
- **Standard reference:** SNA 2025
- **Inputs required:** —
- **Logic:** `null`
- **Output:** `{"sector_code": {"const": "S.11"}}`
- **Test case (positive):** `{}` → matched = **True**
- **Type:** default/fallback rule
- **Result:** PASS

### `R-T06-005` — Government body → general government
- **Test:** T6  •  **Domain:** public_private  •  **Priority:** 5  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** A ministry, authority or council is part of general government by definition.
- **Standard reference:** GFS 2014
- **Inputs required:** —
- **Logic:** `{"op": "eq", "field": "legal_form_code", "value": "GOV"}`
- **Output:** `{"public_private": {"const": "GG"}}`
- **Test case (positive):** `{"legal_form_code": "GOV"}` → matched = **True**
- **Test case (negative):** `{"legal_form_code": "__not__GOV"}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T06-010` — Government-controlled financial market producer → PUB-FC
- **Test:** T6  •  **Domain:** public_private  •  **Priority:** 10  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Public financial corporation.
- **Standard reference:** GFS 2014
- **Inputs required:** —
- **Logic:** `{"all": [{"op": "truthy", "field": "government_control"}, {"op": "truthy", "field": "is_financial"}, {"op": "eq", "field": "market_status", "value": "MARKET"}]}`
- **Output:** `{"public_private": {"const": "PUB-FC"}}`
- **Test case (positive):** `{"government_control": true, "is_financial": true, "market_status": "MARKET"}` → matched = **True**
- **Test case (negative):** `{"government_control": false, "is_financial": true, "market_status": "MARKET"}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T06-020` — Government-controlled market producer → PUB-NFC
- **Test:** T6  •  **Domain:** public_private  •  **Priority:** 20  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Public non-financial corporation.
- **Standard reference:** GFS 2014
- **Inputs required:** —
- **Logic:** `{"all": [{"op": "truthy", "field": "government_control"}, {"op": "eq", "field": "market_status", "value": "MARKET"}]}`
- **Output:** `{"public_private": {"const": "PUB-NFC"}}`
- **Test case (positive):** `{"government_control": true, "market_status": "MARKET"}` → matched = **True**
- **Test case (negative):** `{"government_control": false, "market_status": "MARKET"}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T06-030` — Government-controlled non-market producer → GG
- **Test:** T6  •  **Domain:** public_private  •  **Priority:** 30  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Inside general government.
- **Standard reference:** GFS 2014
- **Inputs required:** —
- **Logic:** `{"all": [{"op": "truthy", "field": "government_control"}, {"op": "eq", "field": "market_status", "value": "NON-MARKET"}]}`
- **Output:** `{"public_private": {"const": "GG"}}`
- **Test case (positive):** `{"government_control": true, "market_status": "NON-MARKET"}` → matched = **True**
- **Test case (negative):** `{"government_control": false, "market_status": "NON-MARKET"}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T06-035` — Non-profit non-market unit → NPISH
- **Test:** T6  •  **Domain:** public_private  •  **Priority:** 35  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Serving households; outside the public sector.
- **Standard reference:** SNA 2025
- **Inputs required:** —
- **Logic:** `{"all": [{"op": "truthy", "field": "is_nonprofit"}, {"op": "eq", "field": "market_status", "value": "NON-MARKET"}]}`
- **Output:** `{"public_private": {"const": "NPISH"}}`
- **Test case (positive):** `{"is_nonprofit": true, "market_status": "NON-MARKET"}` → matched = **True**
- **Test case (negative):** `{"is_nonprofit": false, "market_status": "NON-MARKET"}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T06-040` — Foreign-controlled private corporation → FCC
- **Test:** T6  •  **Domain:** public_private  •  **Priority:** 40  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Foreign-controlled corporation (FDI sub-flag applies).
- **Standard reference:** OECD BD4
- **Inputs required:** —
- **Logic:** `{"all": [{"not": {"op": "truthy", "field": "government_control"}}, {"any": [{"op": "truthy", "field": "uci_is_foreign"}, {"op": "gt", "field": "foreign_ownership_pct", "value": 50}]}]}`
- **Output:** `{"public_private": {"const": "FCC"}}`
- **Test case (positive):** `{"government_control": false, "uci_is_foreign": true}` → matched = **True**
- **Test case (negative):** `{"government_control": true, "uci_is_foreign": true}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T06-050` — Private financial corporation → PRV-FC
- **Test:** T6  •  **Domain:** public_private  •  **Priority:** 50  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Privately controlled financial corporation.
- **Standard reference:** SNA 2025
- **Inputs required:** —
- **Logic:** `{"op": "truthy", "field": "is_financial"}`
- **Output:** `{"public_private": {"const": "PRV-FC"}}`
- **Test case (positive):** `{"is_financial": true}` → matched = **True**
- **Test case (negative):** `{"is_financial": false}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T06-100` — Default → PRV-NFC
- **Test:** T6  •  **Domain:** public_private  •  **Priority:** 100  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Private non-financial corporation.
- **Standard reference:** SNA 2025
- **Inputs required:** —
- **Logic:** `null`
- **Output:** `{"public_private": {"const": "PRV-NFC"}}`
- **Test case (positive):** `{}` → matched = **True**
- **Type:** default/fallback rule
- **Result:** PASS

### `R-T07-010` — Government bodies are non-market
- **Test:** T7  •  **Domain:** market_status  •  **Priority:** 10  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Government bodies produce non-market output financed by levies.
- **Standard reference:** GFS 2014
- **Inputs required:** —
- **Logic:** `{"op": "eq", "field": "legal_form_code", "value": "GOV"}`
- **Output:** `{"market_status": {"const": "NON-MARKET"}}`
- **Test case (positive):** `{"legal_form_code": "GOV"}` → matched = **True**
- **Test case (negative):** `{"legal_form_code": "__not__GOV"}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T07-020` — Non-profit not covering costs is non-market
- **Test:** T7  •  **Domain:** market_status  •  **Priority:** 20  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Non-profit whose sales cover ≤50% of costs is a non-market producer.
- **Standard reference:** SNA 2025
- **Inputs required:** —
- **Logic:** `{"all": [{"op": "truthy", "field": "is_nonprofit"}, {"any": [{"op": "lt", "field": "sales_cover_pct", "value": 50}, {"not": {"op": "exists", "field": "sales_cover_pct"}}]}]}`
- **Output:** `{"market_status": {"const": "NON-MARKET"}}`
- **Test case (positive):** `{"is_nonprofit": true, "sales_cover_pct": 49}` → matched = **True**
- **Test case (negative):** `{"is_nonprofit": false, "sales_cover_pct": 49}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T07-030` — Sales cover >50% of production costs → market
- **Test:** T7  •  **Domain:** market_status  •  **Priority:** 30  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Economically significant prices: sales exceed 50% of production costs.
- **Standard reference:** SNA 2025 — 50% rule
- **Inputs required:** —
- **Logic:** `{"op": "gt", "field": "sales_cover_pct", "value": 50}`
- **Output:** `{"market_status": {"const": "MARKET"}}`
- **Test case (positive):** `{"sales_cover_pct": 51}` → matched = **True**
- **Test case (negative):** `{"sales_cover_pct": 49}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T07-040` — Sales cover ≤50% of production costs → non-market
- **Test:** T7  •  **Domain:** market_status  •  **Priority:** 40  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Sales fail to cover 50% of production costs.
- **Standard reference:** SNA 2025 — 50% rule
- **Inputs required:** —
- **Logic:** `{"op": "exists", "field": "sales_cover_pct"}`
- **Output:** `{"market_status": {"const": "NON-MARKET"}}`
- **Test case (positive):** `{"sales_cover_pct": 1}` → matched = **True**
- **Test case (negative):** `{"sales_cover_pct": null}` → matched = **False** (expected not-matched)
- **Result:** PASS

### `R-T07-100` — Default to market producer
- **Test:** T7  •  **Domain:** market_status  •  **Priority:** 100  •  **Confidence:** 0.6  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Absent cost data, a commercial entity is presumed a market producer pending profiling.
- **Standard reference:** SNA 2025
- **Inputs required:** —
- **Logic:** `null`
- **Output:** `{"market_status": {"const": "MARKET"}}`
- **Test case (positive):** `{}` → matched = **True**
- **Type:** default/fallback rule
- **Result:** PASS

### `R-T08-001` — Effective-control mechanism
- **Test:** T8  •  **Domain:** control_flag  •  **Priority:** 100  •  **Confidence:** 1.0  •  **Approval:** APPROVED (v1.0.0)
- **Description / rationale:** Control flag reflects the mechanism (majority vote, board rights, golden share, beneficial-ownership chain) by which the controlling unit exercises effective control.
- **Standard reference:** SNA 2025 / OECD BD4
- **Inputs required:** —
- **Logic:** `null`
- **Output:** `{"control_flag": {"fact": "representative_control_flag"}}`
- **Test case (positive):** `{}` → matched = **True**
- **Type:** default/fallback rule
- **Result:** PASS

