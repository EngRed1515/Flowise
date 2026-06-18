# NEICS — Data Dictionary

**National Enterprise Intelligence and Classification System**
State of Qatar · National Statistics Office (NSO)

| | |
|---|---|
| **Document** | 07 — Data Dictionary |
| **Status** | STAGING / UAT — pre-pilot review draft |
| **Audience** | Senior statisticians, enterprise architects, data-governance specialists |
| **Classification** | Official — Internal (subject to Qatar Statistics Law) |
| **Owner** | National Statistics Office (NSO), Statistical Methodology & Business Register Programme |
| **Date** | 2026-06-18 |
| **Related** | [`./05_enterprise_data_model.md`](./05_enterprise_data_model.md) · [`./06_erd.md`](./06_erd.md) · [`./08_metadata_model.md`](./08_metadata_model.md) · [`./10_rules_repository_design.md`](./10_rules_repository_design.md) · [`./INDEX.md`](./INDEX.md) |

---

## 1. Purpose and conventions

This is the field-level data dictionary for the core NEICS tables. For each documented table it
gives, per field: the **field** name, the **type** (PostgreSQL physical type), a **definition**,
the **allowed values** (where the field is enumerated or pattern-constrained), whether the field
is **mandatory** (NOT NULL with no usable default), the typical **source** of the value, and the
**standard** the field is anchored to.

The structural model (keys, relationships, versioning) is in
[`./05_enterprise_data_model.md`](./05_enterprise_data_model.md); the ER diagrams are in
[`./06_erd.md`](./06_erd.md). Where this dictionary lists allowed values, those values are the
authoritative controlled vocabulary, also held in the `ref_codelist` and dedicated reference
tables.

**Mandatory column legend:** `Y` = NOT NULL and required at create time; `N` = nullable;
`Y(d)` = NOT NULL but supplied by a default.

**Source legend:** *Admin* = administrative register feed (MOCI / QCB / QFC / QFZA / QSTP /
PSA); *Survey* = statistical survey return; *Engine* = derived by the classification / ownership
engine; *Steward* = entered or curated by an NSO data steward; *System* = set by the platform.

---

## 2. `enterprise` — golden record

Identifiers and names anchored to ISO 17442 (LEI) and Qatar National Classification Standards;
classification outputs anchored to SNA 2025, ISIC Rev.4 and OECD BD4.

| Field | Type | Definition | Allowed values | Mand. | Source | Standard |
|---|---|---|---|---|---|---|
| `enterprise_id` | VARCHAR(24) | Persistent national enterprise identifier (golden-record PK). | Pattern `QA-ENT-YYYYNNNNNNN` | Y | System | Qatar Nat. Classification Std |
| `lei` | VARCHAR(20) | Legal Entity Identifier where held. | 20-char ISO 17442 LEI | N | Admin | ISO 17442 |
| `legal_name_en` | VARCHAR(300) | English legal name. | Free text | Y | Admin | UNSD/Eurostat BR |
| `legal_name_ar` | VARCHAR(300) | Arabic legal name. | Free text | N | Admin | Qatar Nat. Classification Std |
| `legal_form_code` | VARCHAR(10) | Legal form code. | FK → `ref_legal_form.code` | N | Admin | Qatar Nat. Classification Std |
| `residence` | VARCHAR(10) | Declared residence status. | `RES`, `NRES`, `MULTI` | N | Admin/Steward | BPM6; SNA 2025 |
| `isic_class` | VARCHAR(4) | Declared principal activity. | FK → `ref_isic_class.code` (4-digit) | N | Admin/Survey | ISIC Rev.4 |
| `employment` | INTEGER | Total employment / FTE feeding the size test. | ≥ 0 | N | Survey/Admin | ICSE; OECD BD4 |
| `turnover_qar` | DOUBLE PRECISION | Annual turnover (QAR). | ≥ 0 | N | Survey/Admin | SNA 2025 |
| `total_assets_qar` | DOUBLE PRECISION | Total assets (QAR). | ≥ 0 | N | Survey/Admin | SNA 2025 |
| `sales` | DOUBLE PRECISION | Sales — numerator of the market test. | ≥ 0 | N | Survey | SNA 2025 (50% rule) |
| `production_costs` | DOUBLE PRECISION | Production costs — denominator of market test. | ≥ 0 | N | Survey | SNA 2025 (50% rule) |
| `is_nonprofit` | BOOLEAN | Non-profit institution flag. | `TRUE`/`FALSE` | Y(d) | Admin/Steward | SNA 2025 (NPISH) |
| `has_premises` | BOOLEAN | Has identifiable premises (establishment criterion). | `TRUE`/`FALSE` | Y(d) | Survey | UNSD/Eurostat BR |
| `has_employees` | BOOLEAN | Has employees (establishment criterion). | `TRUE`/`FALSE` | Y(d) | Survey | UNSD/Eurostat BR |
| `has_autonomy` | BOOLEAN | Has decision-making autonomy (enterprise criterion). | `TRUE`/`FALSE` | Y(d) | Steward | SNA 2025 |
| `is_financial` | BOOLEAN | Is a financial corporation. | `TRUE`/`FALSE` | Y(d) | Admin | SNA 2025 (S.12) |
| `jurisdiction` | VARCHAR(20) | Registration regime. | `MAINLAND`, `QFC`, `QFZA`, `QSTP` | N | Admin | Qatar Nat. Classification Std |
| `sector_code` | VARCHAR(10) | Latest SNA institutional sector (output). | FK → `ref_institutional_sector.code` | N | Engine | SNA 2025; GFS 2014 |
| `public_private` | VARCHAR(15) | Latest public/private status (output). | `PUB-NFC`, `PUB-FC`, `GG`, `PRV-NFC`, `PRV-FC`, `FCC`, `NPISH` | N | Engine | SNA 2025; GFS 2014 |
| `control_flag` | VARCHAR(15) | Latest control determinant (output). | `MAJ-VOTE`, `BOARD`, `GOLDEN`, `CONTRACT`, `FINANCING`, `DOMINANT`, `REGULATORY`, `BO-CHAIN`, `KEY-PERS`, `NONE` | N | Engine | SNA 2025; OECD BD4 |
| `market_status` | VARCHAR(15) | Latest market/non-market status (output). | `MARKET`, `NON-MARKET` | N | Engine | SNA 2025 (50% test) |
| `size_class` | VARCHAR(15) | Latest size class (output). | `MICRO`, `SMALL`, `MEDIUM`, `LARGE` | N | Engine | OECD BD4; EU SME def. |
| `fdi_flag` | VARCHAR(15) | Latest FDI status (output). | `INWARD-FULL`, `INWARD-ASSOC`, `OUTWARD`, `ROUND-TRIP`, `FELLOW`, `NONE` | N | Engine | OECD BD4; BPM6 |
| `special_entity_flag` | VARCHAR(30) | Special-entity flag (output). | `HOLDING`, `SPV`, `CONSOLIDATE-PARENT`, `NONE` | N | Engine | OECD BD4; BPM6 |
| `group_id` | VARCHAR(24) | Owning enterprise group. | FK → `enterprise_group.group_id` | N | Engine | OECD BD4 |
| `birth_date` | DATE | Demographic birth date. | Valid date | N | Admin | UNSD/Eurostat BR |
| `death_date` | DATE | Demographic death date. | Valid date, `>= birth_date` | N | Admin | UNSD/Eurostat BR |
| `last_demographic_event` | VARCHAR(30) | Last demographic event. | `ref_codelist` domain `demographic_event` | N | Engine | UNSD/Eurostat BR |
| `classification_version` | VARCHAR(10) | Methodology version of latest result. | Semantic version | N | Engine | GSBPM |
| `classification_date` | TIMESTAMP | Timestamp of latest result. | ISO 8601 datetime | N | Engine | GSBPM |
| `quality_flag` | VARCHAR(20) | Lifecycle quality flag. | `DRAFT`, `VALIDATED`, `PUBLISHED`, `FLAGGED` | Y(d) | System | DAMA DMBOK |
| `quality_score` | DOUBLE PRECISION | Latest overall DAMA score. | 0.0–1.0 | N | Engine | DAMA DMBOK |
| `created_at` | TIMESTAMP | Row creation timestamp. | ISO 8601 datetime | Y(d) | System | — |
| `updated_at` | TIMESTAMP | Last update timestamp. | ISO 8601 datetime | Y(d) | System | — |

---

## 3. `legal_unit`

Legal / administrative units mapped to enterprises (N:1). Anchored to ISO 17442 and the Qatar
commercial-registration regime.

| Field | Type | Definition | Allowed values | Mand. | Source | Standard |
|---|---|---|---|---|---|---|
| `legal_unit_id` | VARCHAR(24) | Persistent legal-unit identifier (PK). | Pattern `QA-LU-YYYYNNNNNNN` | Y | System | Qatar Nat. Classification Std |
| `enterprise_id` | VARCHAR(24) | Owning enterprise. | FK → `enterprise.enterprise_id` | Y | Engine/Steward | UNSD/Eurostat BR |
| `lei` | VARCHAR(20) | Legal Entity Identifier where held. | 20-char ISO 17442 LEI | N | Admin | ISO 17442 |
| `legal_name_en` | VARCHAR(300) | English legal name. | Free text | Y | Admin | UNSD/Eurostat BR |
| `legal_name_ar` | VARCHAR(300) | Arabic legal name. | Free text | N | Admin | Qatar Nat. Classification Std |
| `legal_form_code` | VARCHAR(10) | Legal form code. | FK → `ref_legal_form.code` | N | Admin | Qatar Nat. Classification Std |
| `cr_number` | VARCHAR(40) | Commercial Registration number. | Free text / CR format | N | Admin | Qatar commercial law |
| `registration_authority` | VARCHAR(60) | Registering authority. | e.g. `MOCI`, `QFC`, `QFZA`, `QSTP` | N | Admin | Qatar Nat. Classification Std |
| `registration_date` | DATE | Date of registration (birth). | Valid date | N | Admin | UNSD/Eurostat BR |
| `ceased_date` | DATE | Date ceased. | Valid date, `>= registration_date` | N | Admin | UNSD/Eurostat BR |
| `is_active` | BOOLEAN | Active flag. | `TRUE`/`FALSE` | Y(d) | Admin | UNSD/Eurostat BR |
| `notes` | TEXT | Free-text notes. | Free text | N | Steward | — |

---

## 4. `establishment`

Establishments / local units, geo-coded and activity-coded. Anchored to ISIC Rev.4.

| Field | Type | Definition | Allowed values | Mand. | Source | Standard |
|---|---|---|---|---|---|---|
| `establishment_id` | VARCHAR(24) | Persistent establishment identifier (PK). | Pattern `QA-EST-YYYYNNNNNNN` | Y | System | Qatar Nat. Classification Std |
| `enterprise_id` | VARCHAR(24) | Owning enterprise. | FK → `enterprise.enterprise_id` | Y | Engine/Steward | UNSD/Eurostat BR |
| `kau_id` | VARCHAR(24) | Kind-of-activity-unit grouping key. | Free text id | N | Engine | SNA 2025 (KAU) |
| `name` | VARCHAR(300) | English establishment name. | Free text | Y | Admin/Survey | UNSD/Eurostat BR |
| `name_ar` | VARCHAR(300) | Arabic name. | Free text | N | Admin/Survey | Qatar Nat. Classification Std |
| `isic_class` | VARCHAR(4) | Activity of the establishment. | FK → `ref_isic_class.code` | N | Survey | ISIC Rev.4 |
| `municipality` | VARCHAR(100) | Municipality. | Free text / gazetteer | N | Admin | Qatar geo standards |
| `zone` | VARCHAR(100) | Zone. | Free text / gazetteer | N | Admin | Qatar geo standards |
| `latitude` | DOUBLE PRECISION | WGS84 latitude. | −90.0 … 90.0 | N | Survey | WGS84 |
| `longitude` | DOUBLE PRECISION | WGS84 longitude. | −180.0 … 180.0 | N | Survey | WGS84 |
| `employment` | INTEGER | Establishment headcount. | ≥ 0 | N | Survey | ICSE |
| `is_active` | BOOLEAN | Active flag. | `TRUE`/`FALSE` | Y(d) | Admin | UNSD/Eurostat BR |

---

## 5. `enterprise_group`

Enterprise group — the widest delineation of control. Anchored to OECD BD4.

| Field | Type | Definition | Allowed values | Mand. | Source | Standard |
|---|---|---|---|---|---|---|
| `group_id` | VARCHAR(24) | Persistent group identifier (PK). | Pattern `QA-GRP-YYYYNNNNNNN` | Y | System | Qatar Nat. Classification Std |
| `group_name` | VARCHAR(300) | English group name. | Free text | Y | Engine/Steward | OECD BD4 |
| `group_name_ar` | VARCHAR(300) | Arabic group name. | Free text | N | Steward | Qatar Nat. Classification Std |
| `global_ultimate_parent` | VARCHAR(300) | Name of the global ultimate parent. | Free text | N | Engine | OECD BD4 |
| `gup_country` | VARCHAR(2) | Country of the global ultimate parent. | ISO 3166-1 alpha-2 | N | Engine | ISO 3166 |
| `domestic_group_head` | VARCHAR(24) | Domestic group head enterprise id. | `QA-ENT-…` | N | Engine | OECD BD4 |
| `truncated_group_flag` | VARCHAR(1) | Group truncated at national border. | `Y`, `N` | Y(d) | Engine | OECD BD4 |
| `member_count` | INTEGER | Count of member enterprises. | ≥ 0 | Y(d) | Engine | OECD BD4 |
| `controlling_sector` | VARCHAR(10) | SNA sector of the controlling unit. | FK → `ref_institutional_sector.code` | N | Engine | SNA 2025 |
| `notes` | TEXT | Free-text notes. | Free text | N | Steward | — |
| `created_at` | TIMESTAMP | Row creation timestamp. | ISO 8601 datetime | Y(d) | System | — |

---

## 6. `ownership_edge`

Directed share-by-share ownership edge. Anchored to OECD BD4, BPM6 and SNA 2025 control
concepts.

| Field | Type | Definition | Allowed values | Mand. | Source | Standard |
|---|---|---|---|---|---|---|
| `edge_id` | VARCHAR(24) | Ownership-edge identifier (PK). | Free text id | Y | System | — |
| `owner_id` | VARCHAR(40) | Owner endpoint (register id or external token). | `QA-ENT-…` or external token (`STATE-QA`, `FOREIGN-PARENT-01`, …) | Y | Admin/Steward | OECD BD4 |
| `owner_name` | VARCHAR(300) | Owner display name. | Free text | N | Admin | — |
| `owner_is_government` | BOOLEAN | Owner is a government unit. | `TRUE`/`FALSE` | Y(d) | Steward/Engine | SNA 2025 (S.13); GFS 2014 |
| `owner_is_resident` | BOOLEAN | Owner is resident in Qatar. | `TRUE`/`FALSE` | Y(d) | Steward/Engine | BPM6 |
| `owner_country` | VARCHAR(2) | Country of the owner. | ISO 3166-1 alpha-2 | N | Admin | ISO 3166 |
| `owned_id` | VARCHAR(40) | Owned endpoint. | `QA-ENT-…` (typically) | Y | Admin/Steward | OECD BD4 |
| `owned_name` | VARCHAR(300) | Owned display name. | Free text | N | Admin | — |
| `ownership_pct` | DOUBLE PRECISION | Equity / ownership percentage. | 0.0 … 100.0 | Y(d) | Admin | OECD BD4 (10% FDI threshold) |
| `voting_pct` | DOUBLE PRECISION | Voting-rights percentage. | 0.0 … 100.0 | Y(d) | Admin | SNA 2025 (control) |
| `control_indicator` | VARCHAR(15) | Control basis on this edge. | `MAJ-VOTE`, `BOARD`, `GOLDEN`, `CONTRACT`, `FINANCING`, `DOMINANT`, `REGULATORY`, `BO-CHAIN`, `KEY-PERS`, `NONE` | N | Engine | SNA 2025; OECD BD4 |
| `is_ultimate` | VARCHAR(1) | Edge represents ultimate control. | `Y`, `N` | Y(d) | Engine | OECD BD4 (UCI) |
| `created_at` | TIMESTAMP | Row creation timestamp. | ISO 8601 datetime | Y(d) | System | — |

---

## 7. `classification`

Temporally-versioned committed classification result. Anchored to SNA 2025, GFS 2014, BPM6,
OECD BD4 and GSBPM (process metadata).

| Field | Type | Definition | Allowed values | Mand. | Source | Standard |
|---|---|---|---|---|---|---|
| `id` | INTEGER | Surrogate PK. | Autoincrement | Y(d) | System | — |
| `enterprise_id` | VARCHAR(24) | Subject enterprise. | FK → `enterprise.enterprise_id` | Y | Engine | — |
| `version` | INTEGER | Per-enterprise incrementing version. | ≥ 1 | Y(d) | Engine | GSBPM |
| `methodology_version` | VARCHAR(10) | Methodology / rule-base version. | Semantic version | Y | Engine | GSBPM |
| `residence` | VARCHAR(10) | Residence dimension. | `RES`, `NRES`, `MULTI` | N | Engine | BPM6 |
| `isic_class` | VARCHAR(4) | Activity dimension. | FK → `ref_isic_class.code` | N | Engine | ISIC Rev.4 |
| `sector_code` | VARCHAR(10) | SNA institutional sector. | FK → `ref_institutional_sector.code` | N | Engine | SNA 2025 |
| `public_private` | VARCHAR(15) | Public/private dimension. | `PUB-NFC`, `PUB-FC`, `GG`, `PRV-NFC`, `PRV-FC`, `FCC`, `NPISH` | N | Engine | SNA 2025; GFS 2014 |
| `control_flag` | VARCHAR(15) | Control determinant. | `MAJ-VOTE`, `BOARD`, `GOLDEN`, `CONTRACT`, `FINANCING`, `DOMINANT`, `REGULATORY`, `BO-CHAIN`, `KEY-PERS`, `NONE` | N | Engine | SNA 2025 |
| `market_status` | VARCHAR(15) | Market/non-market dimension. | `MARKET`, `NON-MARKET` | N | Engine | SNA 2025 |
| `size_class` | VARCHAR(15) | Size dimension. | `MICRO`, `SMALL`, `MEDIUM`, `LARGE` | N | Engine | OECD BD4 |
| `fdi_flag` | VARCHAR(15) | FDI dimension. | `INWARD-FULL`, `INWARD-ASSOC`, `OUTWARD`, `ROUND-TRIP`, `FELLOW`, `NONE` | N | Engine | OECD BD4; BPM6 |
| `special_entity_flag` | VARCHAR(30) | Special-entity dimension. | `HOLDING`, `SPV`, `CONSOLIDATE-PARENT`, `NONE` | N | Engine | OECD BD4 |
| `group_id` | VARCHAR(24) | Group at time of classification. | `QA-GRP-…` | N | Engine | OECD BD4 |
| `confidence` | DOUBLE PRECISION | Overall confidence of the result. | 0.0–1.0 | N | Engine | — |
| `trace` | JSONB | Ordered list of test/rule decisions. | JSON array | N | Engine | GSBPM (explainability) |
| `facts` | JSONB | Fact set used (provenance). | JSON object | N | Engine | GSBPM |
| `is_current` | BOOLEAN | Marks the active row. | `TRUE`/`FALSE` | Y(d) | Engine | — |
| `is_override` | BOOLEAN | Result is a manual override. | `TRUE`/`FALSE` | Y(d) | Engine/Steward | — |
| `override_reason` | TEXT | Justification when overridden. | Free text | N | Reviewer | — |
| `reviewer` | VARCHAR(120) | Reviewing officer. | `app_user.username` | N | Reviewer | — |
| `quality_flag` | VARCHAR(20) | Quality flag. | `DRAFT`, `VALIDATED`, `PUBLISHED`, `FLAGGED` | Y(d) | System | DAMA DMBOK |
| `created_by` | VARCHAR(120) | Creating actor. | `app_user.username` / `SYSTEM` | N | System | — |
| `created_at` | TIMESTAMP | Creation timestamp. | ISO 8601 datetime | Y(d) | System | — |
| `valid_from` | TIMESTAMP | Start of validity period. | ISO 8601 datetime | Y(d) | System | — |
| `valid_to` | TIMESTAMP | End of validity period (NULL while current). | ISO 8601 datetime | N | System | — |

---

## 8. `rule`

A single configurable classification rule. Anchored via `standard_ref` to the relevant standard.
Full design in [`./10_rules_repository_design.md`](./10_rules_repository_design.md).

| Field | Type | Definition | Allowed values | Mand. | Source | Standard |
|---|---|---|---|---|---|---|
| `rule_id` | VARCHAR(40) | Rule identifier (PK). | Pattern `R-Txx-nnn` | Y | Methodologist | — |
| `name` | VARCHAR(300) | Rule name. | Free text | Y | Methodologist | — |
| `description` | TEXT | Rule description. | Free text | N | Methodologist | — |
| `test_code` | VARCHAR(10) | Owning test. | FK → `classification_test.test_code` (`T1`–`T18`) | Y | Methodologist | Framework Part III |
| `domain` | VARCHAR(40) | Output dimension the rule contributes to. | e.g. `residence`, `sector_code`, `public_private`, `control_flag`, `market_status`, `size_class`, `fdi_flag`, `special_entity_flag`, `isic_class` | Y | Methodologist | — |
| `inputs_required` | JSONB | Fact keys the rule consumes. | JSON array of strings | N | Methodologist | — |
| `logic` | JSONB | Condition tree evaluated against facts. | JSON condition tree | N | Methodologist | — |
| `output` | JSONB | `{field: value}` assignment when the rule fires. | JSON object | N | Methodologist | — |
| `priority` | INTEGER | Evaluation order within a test (lower = first). | ≥ 0; default 100 | Y(d) | Methodologist | — |
| `confidence` | DOUBLE PRECISION | Confidence weight contributed. | 0.0–1.0; default 1.0 | Y(d) | Methodologist | — |
| `standard_ref` | VARCHAR(200) | Anchoring standard reference. | Free text / `std_standard.code` + para | N | Methodologist | (varies) |
| `rationale` | TEXT | Human-readable "why". | Free text | N | Methodologist | — |
| `effective_date` | DATE | Date from which the rule is in force. | Valid date | N | Methodologist | GSBPM |
| `expiry_date` | DATE | Date the rule expires (NULL = open). | Valid date `>= effective_date` | N | Methodologist | GSBPM |
| `version` | VARCHAR(10) | Semantic version. | e.g. `1.0.0` | Y(d) | Methodologist | — |
| `author` | VARCHAR(120) | Author. | `app_user.username` | N | Methodologist | — |
| `approval_status` | VARCHAR(20) | Approval lifecycle. | `DRAFT`, `APPROVED`, `RETIRED` | Y(d) | Methodologist | — |
| `is_active` | BOOLEAN | Active flag. | `TRUE`/`FALSE` | Y(d) | Methodologist | — |
| `created_at` | TIMESTAMP | Row creation timestamp. | ISO 8601 datetime | Y(d) | System | — |

---

## 9. `classification` dimension vocabularies (reference)

The complete controlled vocabularies for the multi-dimensional classification key, with the
standard that governs each dimension. These values populate the corresponding columns on both
`enterprise` (latest) and `classification` (history).

### 9.1 `residence` — SNA 2025 / BPM6

| Code | Meaning |
|---|---|
| `RES` | Resident in the economic territory of Qatar. |
| `NRES` | Non-resident. |
| `MULTI` | Multi-territory / split residence. |

### 9.2 `sector_code` — SNA 2025 institutional sectors

| Code | Meaning |
|---|---|
| `S.11` | Non-financial corporations. |
| `S.12` | Financial corporations. |
| `S.121` | Central bank. |
| `S.122` | Deposit-taking corporations except the central bank. |
| `S.123` | Money market funds. |
| `S.124` | Non-MMF investment funds. |
| `S.125` | Other financial intermediaries except ICPF. |
| `S.126` | Financial auxiliaries. |
| `S.127` | Captive financial institutions and money lenders. |
| `S.128` | Insurance corporations. |
| `S.129` | Pension funds. |
| `S.13` | General government. |
| `S.1311` | Central government. |
| `S.1312` | State government. |
| `S.1313` | Local government. |
| `S.1314` | Social security funds. |
| `S.14` | Households. |
| `S.15` | Non-profit institutions serving households (NPISH). |
| `S.2` | Rest of the world. |

### 9.3 `public_private` — SNA 2025 / GFS 2014

| Code | Meaning |
|---|---|
| `PUB-NFC` | Public non-financial corporation. |
| `PUB-FC` | Public financial corporation. |
| `GG` | General government. |
| `PRV-NFC` | Private non-financial corporation. |
| `PRV-FC` | Private financial corporation. |
| `FCC` | Foreign-controlled corporation. |
| `NPISH` | Non-profit institution serving households. |

### 9.4 `control_flag` — SNA 2025 / OECD BD4 control indicators

| Code | Meaning |
|---|---|
| `MAJ-VOTE` | Majority of voting rights. |
| `BOARD` | Control of the board / appointment rights. |
| `GOLDEN` | Golden share / special statutory powers. |
| `CONTRACT` | Control via contractual arrangement. |
| `FINANCING` | Control via dominant financing. |
| `DOMINANT` | Dominant minority influence. |
| `REGULATORY` | Control via regulation. |
| `BO-CHAIN` | Control via beneficial-ownership chain. |
| `KEY-PERS` | Control via key personnel / interlocking directorates. |
| `NONE` | No controlling relationship identified. |

### 9.5 `market_status` — SNA 2025 (50% test)

| Code | Meaning |
|---|---|
| `MARKET` | Market producer (sales cover ≥ 50% of production costs). |
| `NON-MARKET` | Non-market producer. |

### 9.6 `size_class` — OECD BD4 / `ref_size_threshold`

| Code | FTE band | Turnover band (QAR) |
|---|---|---|
| `MICRO` | 1–9 | ≤ 3,000,000 |
| `SMALL` | 10–49 | 3,000,000 – 30,000,000 |
| `MEDIUM` | 50–249 | 30,000,000 – 200,000,000 |
| `LARGE` | 250+ | > 200,000,000 |

The **higher criterion governs**: an entity that meets the headcount band for one class but the
turnover band for a larger class is assigned the larger class.

### 9.7 `fdi_flag` — OECD BD4 / BPM6

| Code | Meaning |
|---|---|
| `INWARD-FULL` | Inward FDI, full control (≥ 50% by a non-resident). |
| `INWARD-ASSOC` | Inward FDI, associate (10–50% by a non-resident). |
| `OUTWARD` | Outward FDI (resident direct investor abroad). |
| `ROUND-TRIP` | Round-tripping investment. |
| `FELLOW` | Fellow-enterprise relationship. |
| `NONE` | No FDI relationship. |

### 9.8 `special_entity_flag` — OECD BD4 / BPM6

| Code | Meaning |
|---|---|
| `HOLDING` | Holding company. |
| `SPV` | Special-purpose vehicle / entity. |
| `CONSOLIDATE-PARENT` | Parent requiring consolidation. |
| `NONE` | Not a special entity. |

---

## 10. Key codelist tables

### 10.1 `ref_institutional_sector`

| Field | Type | Definition | Allowed values | Mand. | Source | Standard |
|---|---|---|---|---|---|---|
| `code` | VARCHAR(10) | SNA sector code (PK). | `S.11`, `S.12`, `S.121`–`S.129`, `S.13`, `S.1311`–`S.1314`, `S.14`, `S.15`, `S.2` | Y | Steward | SNA 2008/2025 |
| `name_en` | VARCHAR(200) | English sector name. | Free text | Y | Steward | SNA 2025 |
| `name_ar` | VARCHAR(200) | Arabic sector name. | Free text | N | Steward | Qatar Nat. Classification Std |
| `parent_code` | VARCHAR(10) | Parent sector (self-FK). | `ref_institutional_sector.code` | N | Steward | SNA 2025 |
| `definition` | TEXT | SNA definition. | Free text | N | Steward | SNA 2025 |
| `standard_ref` | VARCHAR(100) | Anchoring standard. | default `SNA 2008/2025` | Y(d) | Steward | SNA 2025 |

### 10.2 `ref_isic_class`

| Field | Type | Definition | Allowed values | Mand. | Source | Standard |
|---|---|---|---|---|---|---|
| `code` | VARCHAR(4) | 4-digit ISIC Rev.4 class (PK). | 4-digit numeric, e.g. `6419` | Y | Steward | ISIC Rev.4 |
| `section_code` | VARCHAR(1) | Owning section letter. | `A`–`U` | Y | Steward | ISIC Rev.4 |
| `activity_en` | VARCHAR(400) | English activity description. | Free text | Y | Steward | ISIC Rev.4 |
| `activity_ar` | VARCHAR(400) | Arabic activity description. | Free text | N | Steward | Qatar Nat. Classification Std |
| `nace` | VARCHAR(20) | NACE cross-walk. | NACE code | N | Steward | NACE Rev.2 |
| `gcc_sic` | VARCHAR(20) | GCC-SIC cross-walk. | GCC-SIC code | N | Steward | GCC-SIC |

### 10.3 `ref_legal_form`

| Field | Type | Definition | Allowed values | Mand. | Source | Standard |
|---|---|---|---|---|---|---|
| `code` | VARCHAR(10) | Legal-form code (PK). | e.g. `WLL`, `QPSC`, `SP`, `GOV`, `BRANCH` | Y | Steward | Qatar commercial law |
| `name_en` | VARCHAR(200) | English name. | Free text | Y | Steward | Qatar Nat. Classification Std |
| `name_ar` | VARCHAR(200) | Arabic name. | Free text | N | Steward | Qatar Nat. Classification Std |
| `notes` | TEXT | Usage notes / scope. | Free text | N | Steward | — |

### 10.4 `ref_size_threshold`

| Field | Type | Definition | Allowed values | Mand. | Source | Standard |
|---|---|---|---|---|---|---|
| `size_class` | VARCHAR(20) | Size class (PK). | `MICRO`, `SMALL`, `MEDIUM`, `LARGE` | Y | Steward | OECD BD4 |
| `turnover_min` | DOUBLE PRECISION | Lower turnover bound (QAR). | ≥ 0 (NULL = unbounded) | N | Steward | OECD BD4 |
| `turnover_max` | DOUBLE PRECISION | Upper turnover bound (QAR). | ≥ 0 (NULL = unbounded) | N | Steward | OECD BD4 |
| `fte_min` | INTEGER | Lower FTE bound. | ≥ 0 (NULL = unbounded) | N | Steward | OECD BD4 |
| `fte_max` | INTEGER | Upper FTE bound. | ≥ 0 (NULL = unbounded) | N | Steward | OECD BD4 |

---

## 11. Quality dimensions (`quality_result`) — DAMA DMBOK

| Field | Type | Definition | Range | Standard |
|---|---|---|---|---|
| `completeness` | DOUBLE PRECISION | Proportion of required attributes populated. | 0.0–1.0 | DAMA DMBOK |
| `validity` | DOUBLE PRECISION | Proportion of values conforming to codelists / domains. | 0.0–1.0 | DAMA DMBOK |
| `consistency` | DOUBLE PRECISION | Cross-field / cross-record consistency. | 0.0–1.0 | DAMA DMBOK |
| `uniqueness` | DOUBLE PRECISION | Absence of duplication. | 0.0–1.0 | DAMA DMBOK |
| `accuracy` | DOUBLE PRECISION | Agreement with authoritative source. | 0.0–1.0 | DAMA DMBOK |
| `timeliness` | DOUBLE PRECISION | Currency of the data relative to reference period. | 0.0–1.0 | DAMA DMBOK |
| `overall_score` | DOUBLE PRECISION | Composite of the six dimensions. | 0.0–1.0 | DAMA DMBOK |

---

## 12. Cross-references

- Logical & physical model: [`./05_enterprise_data_model.md`](./05_enterprise_data_model.md)
- Entity-relationship diagrams: [`./06_erd.md`](./06_erd.md)
- Metadata model (GSIM/SDMX): [`./08_metadata_model.md`](./08_metadata_model.md)
- Rules repository design: [`./10_rules_repository_design.md`](./10_rules_repository_design.md)
- Document index: [`./INDEX.md`](./INDEX.md)

*End of document 07 — Data Dictionary.*
