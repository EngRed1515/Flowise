# Explainability Validation Report

> **NEICS — Staging / UAT environment.** This report is generated automatically by `tools/generate_reports.py` directly from the live classification engine and seeded test database. Generated: 2026-06-18 10:40 UTC.

For each sampled enterprise the full classification explanation is shown: the rules applied (with standard references and rationale), the data fields used, the confidence, and reviewer/override status. This demonstrates complete, defensible explainability.

## QA-ENT-20260000002 — Sample National Bank Q.P.S.C.
**Result:** sector `S.122`, public/private `PUB-FC`, control `MAJ-VOTE`, FDI `NONE`, special `NONE`.  **Confidence:** 1.0.

**Applied rules (the 'why'):**

| Test | Rule | Output | Standard reference | Rationale |
|---|---|---|---|---|
| T3 | `R-T03-001` | residence=RES | SNA 2025 / BPM6 Ch.4 | Residence is taken from the assessed centre of predominant economic interest. |
| T4 | `R-T04-001` | isic_class=6419 | ISIC Rev.4 | Principal activity assigned by largest share of value added. |
| T7 | `R-T07-030` | market_status=MARKET | SNA 2025 — 50% rule | Economically significant prices: sales exceed 50% of production costs. |
| T8 | `R-T08-001` | control_flag=MAJ-VOTE | SNA 2025 / OECD BD4 | Control flag reflects the mechanism (majority vote, board rights, golden share, beneficial-ownership chain) by which the controlling unit exercises effective control. |
| T5 | `R-T05-022` | sector_code=S.122 | SNA 2025 | Banks / other depository corporations. |
| T6 | `R-T06-010` | public_private=PUB-FC | GFS 2014 | Public financial corporation. |
| T10 | `R-T10-010` | size_class=LARGE | QNCS / EU 2003/361/EC | ≥250 FTE or > QAR 200m turnover band. |
| T12 | `R-T12-100` | fdi_flag=NONE | OECD BD4 | Foreign ownership below the 10% threshold. |
| T13 | `R-T13-100` | special_entity_flag=NONE | SNA 2025 | Substantive operating unit. |

**Data fields used:** `{"legal_form_code": "JSC", "isic_class": "6419", "residence": "RES", "is_financial": true, "government_ownership_pct": 51.0, "government_voting_pct": 51.0, "foreign_ownership_pct": 0.0, "government_control": true, "market_status": "MARKET", "sales_cover_pct": 183.33333333333331, "employment": 5200, "turnover_qar": 22000000000.0}`
**Data sources:** CSBR golden record; ownership graph; reference codelists.
**Methodology version:** 1.0.0  •  **Reviewer/override:** none (rule-based).

## QA-ENT-20260000099 — Sample Trading Co (sample)
**Result:** sector `S.11`, public/private `PUB-NFC`, control `BO-CHAIN`, FDI `NONE`, special `NONE`.  **Confidence:** 1.0.

**Applied rules (the 'why'):**

| Test | Rule | Output | Standard reference | Rationale |
|---|---|---|---|---|
| T3 | `R-T03-001` | residence=RES | SNA 2025 / BPM6 Ch.4 | Residence is taken from the assessed centre of predominant economic interest. |
| T4 | `R-T04-001` | isic_class=4690 | ISIC Rev.4 | Principal activity assigned by largest share of value added. |
| T7 | `R-T07-030` | market_status=MARKET | SNA 2025 — 50% rule | Economically significant prices: sales exceed 50% of production costs. |
| T8 | `R-T08-001` | control_flag=BO-CHAIN | SNA 2025 / OECD BD4 | Control flag reflects the mechanism (majority vote, board rights, golden share, beneficial-ownership chain) by which the controlling unit exercises effective control. |
| T5 | `R-T05-100` | sector_code=S.11 | SNA 2025 | Market producer of goods/non-financial services. |
| T6 | `R-T06-020` | public_private=PUB-NFC | GFS 2014 | Public non-financial corporation. |
| T10 | `R-T10-020` | size_class=MEDIUM | QNCS | 50-249 FTE or QAR 30-200m turnover band. |
| T12 | `R-T12-100` | fdi_flag=NONE | OECD BD4 | Foreign ownership below the 10% threshold. |
| T13 | `R-T13-100` | special_entity_flag=NONE | SNA 2025 | Substantive operating unit. |

**Data fields used:** `{"legal_form_code": "LLC", "isic_class": "4690", "residence": "RES", "is_financial": false, "government_ownership_pct": 60.0, "government_voting_pct": 60.0, "foreign_ownership_pct": 0.0, "government_control": true, "market_status": "MARKET", "sales_cover_pct": 142.85714285714286, "employment": 85, "turnover_qar": 40000000.0}`
**Data sources:** CSBR golden record; ownership graph; reference codelists.
**Methodology version:** 1.0.0  •  **Reviewer/override:** none (rule-based).

## QA-ENT-20260000024 — Sample Infrastructure SPV
**Result:** sector `S.11`, public/private `PUB-NFC`, control `GOLDEN`, FDI `ROUND-TRIP`, special `NONE`.  **Confidence:** 1.0.

**Applied rules (the 'why'):**

| Test | Rule | Output | Standard reference | Rationale |
|---|---|---|---|---|
| T3 | `R-T03-001` | residence=RES | SNA 2025 / BPM6 Ch.4 | Residence is taken from the assessed centre of predominant economic interest. |
| T4 | `R-T04-001` | isic_class=4290 | ISIC Rev.4 | Principal activity assigned by largest share of value added. |
| T7 | `R-T07-030` | market_status=MARKET | SNA 2025 — 50% rule | Economically significant prices: sales exceed 50% of production costs. |
| T8 | `R-T08-001` | control_flag=GOLDEN | SNA 2025 / OECD BD4 | Control flag reflects the mechanism (majority vote, board rights, golden share, beneficial-ownership chain) by which the controlling unit exercises effective control. |
| T5 | `R-T05-100` | sector_code=S.11 | SNA 2025 | Market producer of goods/non-financial services. |
| T6 | `R-T06-020` | public_private=PUB-NFC | GFS 2014 | Public non-financial corporation. |
| T10 | `R-T10-010` | size_class=LARGE | QNCS / EU 2003/361/EC | ≥250 FTE or > QAR 200m turnover band. |
| T12 | `R-T12-010` | fdi_flag=ROUND-TRIP | OECD BD4 | Apparent inward FDI through a non-resident vehicle, ultimately Qatari-controlled. |
| T13 | `R-T13-100` | special_entity_flag=NONE | SNA 2025 | Substantive operating unit. |

**Data fields used:** `{"legal_form_code": "LLC", "isic_class": "4290", "residence": "RES", "is_financial": false, "government_ownership_pct": 49.0, "government_voting_pct": 49.0, "foreign_ownership_pct": 51.0, "government_control": true, "market_status": "MARKET", "sales_cover_pct": 120.0, "employment": 40, "turnover_qar": 300000000.0}`
**Data sources:** CSBR golden record; ownership graph; reference codelists.
**Methodology version:** 1.0.0  •  **Reviewer/override:** none (rule-based).

## QA-ENT-20260000025 — Sample Property Developer
**Result:** sector `S.11`, public/private `PUB-NFC`, control `MAJ-VOTE`, FDI `ROUND-TRIP`, special `NONE`.  **Confidence:** 1.0.

**Applied rules (the 'why'):**

| Test | Rule | Output | Standard reference | Rationale |
|---|---|---|---|---|
| T3 | `R-T03-001` | residence=RES | SNA 2025 / BPM6 Ch.4 | Residence is taken from the assessed centre of predominant economic interest. |
| T4 | `R-T04-001` | isic_class=6810 | ISIC Rev.4 | Principal activity assigned by largest share of value added. |
| T7 | `R-T07-030` | market_status=MARKET | SNA 2025 — 50% rule | Economically significant prices: sales exceed 50% of production costs. |
| T8 | `R-T08-001` | control_flag=MAJ-VOTE | SNA 2025 / OECD BD4 | Control flag reflects the mechanism (majority vote, board rights, golden share, beneficial-ownership chain) by which the controlling unit exercises effective control. |
| T5 | `R-T05-100` | sector_code=S.11 | SNA 2025 | Market producer of goods/non-financial services. |
| T6 | `R-T06-020` | public_private=PUB-NFC | GFS 2014 | Public non-financial corporation. |
| T10 | `R-T10-010` | size_class=LARGE | QNCS / EU 2003/361/EC | ≥250 FTE or > QAR 200m turnover band. |
| T12 | `R-T12-010` | fdi_flag=ROUND-TRIP | OECD BD4 | Apparent inward FDI through a non-resident vehicle, ultimately Qatari-controlled. |
| T13 | `R-T13-100` | special_entity_flag=NONE | SNA 2025 | Substantive operating unit. |

**Data fields used:** `{"legal_form_code": "LLC", "isic_class": "6810", "residence": "RES", "is_financial": false, "government_ownership_pct": 70.0, "government_voting_pct": 70.0, "foreign_ownership_pct": 70.0, "government_control": true, "market_status": "MARKET", "sales_cover_pct": 160.0, "employment": 350, "turnover_qar": 800000000.0}`
**Data sources:** CSBR golden record; ownership graph; reference codelists.
**Methodology version:** 1.0.0  •  **Reviewer/override:** none (rule-based).

## QA-ENT-20260000026 — Sample Empty-Shell Holding
**Result:** sector `S.11`, public/private `PRV-NFC`, control `MAJ-VOTE`, FDI `NONE`, special `CONSOLIDATE-PARENT`.  **Confidence:** 0.956.

**Applied rules (the 'why'):**

| Test | Rule | Output | Standard reference | Rationale |
|---|---|---|---|---|
| T3 | `R-T03-001` | residence=RES | SNA 2025 / BPM6 Ch.4 | Residence is taken from the assessed centre of predominant economic interest. |
| T4 | `R-T04-001` | isic_class=6420 | ISIC Rev.4 | Principal activity assigned by largest share of value added. |
| T7 | `R-T07-100` | market_status=MARKET | SNA 2025 | Absent cost data, a commercial entity is presumed a market producer pending profiling. |
| T8 | `R-T08-001` | control_flag=MAJ-VOTE | SNA 2025 / OECD BD4 | Control flag reflects the mechanism (majority vote, board rights, golden share, beneficial-ownership chain) by which the controlling unit exercises effective control. |
| T5 | `R-T05-100` | sector_code=S.11 | SNA 2025 | Market producer of goods/non-financial services. |
| T6 | `R-T06-100` | public_private=PRV-NFC | SNA 2025 | Private non-financial corporation. |
| T10 | `R-T10-100` | size_class=MICRO | QNCS | 1-9 FTE; up to QAR 3m turnover. |
| T12 | `R-T12-100` | fdi_flag=NONE | OECD BD4 | Foreign ownership below the 10% threshold. |
| T13 | `R-T13-010` | special_entity_flag=CONSOLIDATE-PARENT | SNA 2025 §4 (empty-shell rule) | No premises, employees or autonomy — consolidated with controlling parent. |

**Data fields used:** `{"legal_form_code": "LLC", "isic_class": "6420", "residence": "RES", "is_financial": false, "government_ownership_pct": 0.0, "government_voting_pct": 0.0, "foreign_ownership_pct": 0.0, "government_control": false, "market_status": "MARKET", "sales_cover_pct": null, "employment": 0, "turnover_qar": 0.0}`
**Data sources:** CSBR golden record; ownership graph; reference codelists.
**Methodology version:** 1.0.0  •  **Reviewer/override:** none (rule-based).

## QA-ENT-20260000018 — Sample Sports Club
**Result:** sector `S.15`, public/private `NPISH`, control `NONE`, FDI `NONE`, special `NONE`.  **Confidence:** 1.0.

**Applied rules (the 'why'):**

| Test | Rule | Output | Standard reference | Rationale |
|---|---|---|---|---|
| T3 | `R-T03-001` | residence=RES | SNA 2025 / BPM6 Ch.4 | Residence is taken from the assessed centre of predominant economic interest. |
| T4 | `R-T04-001` | isic_class=9499 | ISIC Rev.4 | Principal activity assigned by largest share of value added. |
| T7 | `R-T07-020` | market_status=NON-MARKET | SNA 2025 | Non-profit whose sales cover ≤50% of costs is a non-market producer. |
| T8 | `R-T08-001` | control_flag=NONE | SNA 2025 / OECD BD4 | Control flag reflects the mechanism (majority vote, board rights, golden share, beneficial-ownership chain) by which the controlling unit exercises effective control. |
| T5 | `R-T05-035` | sector_code=S.15 | SNA 2025 | Non-market non-profit serving households, not government-controlled. |
| T6 | `R-T06-035` | public_private=NPISH | SNA 2025 | Serving households; outside the public sector. |
| T10 | `R-T10-020` | size_class=MEDIUM | QNCS | 50-249 FTE or QAR 30-200m turnover band. |
| T12 | `R-T12-100` | fdi_flag=NONE | OECD BD4 | Foreign ownership below the 10% threshold. |
| T13 | `R-T13-100` | special_entity_flag=NONE | SNA 2025 | Substantive operating unit. |

**Data fields used:** `{"legal_form_code": "CA", "isic_class": "9499", "residence": "RES", "is_financial": false, "government_ownership_pct": 0.0, "government_voting_pct": 0.0, "foreign_ownership_pct": 0.0, "government_control": false, "market_status": "NON-MARKET", "sales_cover_pct": 15.0, "employment": 60, "turnover_qar": 3000000.0}`
**Data sources:** CSBR golden record; ownership graph; reference codelists.
**Methodology version:** 1.0.0  •  **Reviewer/override:** none (rule-based).

