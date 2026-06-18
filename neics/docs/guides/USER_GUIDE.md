# NEICS — User Guide

**National Enterprise Intelligence and Classification System (NEICS)** — State of Qatar NSO/NSC
Phase: Staging / UAT (no production deployment) · Version 1.0 · Date 2026-06-18

This guide is for analysts, classifiers, data stewards, and reviewers using NEICS day to day: logging in, navigating, searching enterprises, reading profiles, running classifications, interpreting explainability and quality, and working through reviews and overrides.

---

## 1. Logging in

1. Open the NEICS frontend in a browser (staging URL provided by your administrator).
2. Enter your username and password and sign in. Your role determines what you can see and do (see the permission summary below).
3. Behind the scenes the platform issues a JWT bearer token; you remain signed in until it expires, after which you log in again.

**What each role can do (summary):** Analyst — read-only; Classifier — create/update enterprises and run classification; Data Steward — also manage ownership; Reviewer — resolve reviews and apply overrides; Auditor — read audit and quality; Methodologist — author rules/standards/metadata; Administrator — everything.

## 2. Navigating the dashboard

After login you land on the **Dashboard**, which summarises the enterprise portfolio:
- Counts by institutional sector (S.11, S.12x, S.13, S.14, S.15, S.2) and by public/private category (PUB-NFC, PUB-FC, GG, PRV-NFC, PRV-FC, FCC, NPISH).
- Data-quality overview and the number of open review items / exceptions.
- Key indicators such as the override rate.

Use the navigation to reach **Enterprises**, the **Review Center**, **Repositories** (Rules, Tests, Standards, Metadata, Reference), the **Simulation** sandbox, **Audit**, and **Quality**.

## 3. Searching for enterprises

1. Open **Enterprises**. The list shows all seeded entities (28 in staging).
2. Filter or search by name, identifier (e.g., `QA-ENT-2026000000025`), sector, or public/private category.
3. Select an enterprise to open its profile.

## 4. Reading an enterprise profile

The profile consolidates everything known about an entity:

- **Identity** — legal name, legal form, residence, identifiers (including LEI where applicable).
- **Ownership structure** — direct owners with shares, and, for groups, the multi-level chain and the ultimate controlling institutional unit (UCI). For the SWF cascade `QA-ENT-2026000000025` the chain resolves through a non-resident QIA subsidiary to UCI = government.
- **Classification** — the nine dimensions: residence, sector_code, public_private, control_flag, market_status, size_class, fdi_flag, special_entity_flag, and the final record.
- **Explainability** — the determination trace (see Section 7).
- **Quality** — the data-quality score and its six DAMA dimensions (see Section 9).
- **History** — every classification version over time, with the ability to view superseded versions.

## 5. Creating or updating an enterprise

(Classifier or Data Steward.)

1. **Enterprises → New Enterprise.** Enter legal name, legal form (from the picker), residence (RES / NRES / MULTI), principal activity (ISIC Rev.4), and financials (FTE and turnover).
2. Save. The platform validates the record and flags any issues.
3. To update, open the profile and edit the fields; saving creates an audited change.
4. (Data Steward) **Add Ownership** to record owners and shares; this drives control and FDI determinations.

Mandatory fields and reference values are enforced — missing or invalid entries raise validation findings (Section 9).

## 6. Running a classification

1. Open the enterprise profile.
2. (Optional) Click **Validate** to check the record first.
3. Click **Classify**. The engine runs the 18 tests and the applicable rules and produces the nine-dimension result.
4. Review the **Classification** tab.

Worked examples (golden dataset):
- Bank `QA-ENT-20260000002` → sector S.122, public_private PUB-FC, control MAJ-VOTE.
- Energy SOE `QA-ENT-20260000001` → S.11, PUB-NFC, MARKET.
- Foreign MNE subsidiary `QA-ENT-2026000000028` → FCC, fdi INWARD-FULL.
- PPP SPV `QA-ENT-2026000000024` → PUB-NFC via GOLDEN (substance over form), special_entity SPV.

If the case is ambiguous, the system may flag it for review (Section 8).

## 7. Understanding the explainability trace and confidence

Open **Explainability** for a classified entity (or call `GET /api/enterprises/{id}/explain`). The trace shows:
- Each of the 18 tests (T1–T18) that ran and its outcome.
- The specific rules that fired, referenced by identifier.
- A per-dimension rationale (why this residence, sector, public/private, control, etc.).
- A **confidence** indicator for the determination.

Read the trace top-down: residence and unit tests (T1–T3), activity (T4), sector and boundary (T5–T7), ownership/control (T8–T9), size (T10), group/FDI/special-entity (T11–T13), source/conflict/governance/QA (T14–T17), and the final record (T18). The trace is the authoritative justification for the verdict and is suitable for review and audit.

## 8. Submitting and resolving reviews; applying an override

### Reviews
- Ambiguous classifications, substance-over-form cases, and low-quality records generate review items/exceptions.
- **Reviewers** open the **Review Center** (`GET /api/reviews`), select an item, examine the explainability and ownership evidence, and **Resolve** it (`POST /api/reviews/{id}/resolve`).

### Overrides (Reviewer)
- When the methodology requires a manual determination, a Reviewer applies an **Override** (`POST /api/enterprises/{id}/override`) and must provide a written justification.
- The override is recorded as a new version; the prior automated version is retained in history; the action is captured in the audit trail; and the dashboard override-rate KPI updates.
- Overrides should remain the exception — the framework target is an override rate of ≤ 5%.

## 9. Interpreting quality scores and validation exceptions

### Quality score
The **Quality** tab shows an overall data-quality score and the six DAMA dimensions: **Completeness**, **Accuracy**, **Consistency**, **Validity**, **Timeliness**, and **Uniqueness**. A low sub-score points to the kind of issue: e.g., missing fields lower Completeness; codelist failures lower Validity; conflicting cross-field values lower Consistency.

### Validation exceptions
Records are checked against validation rules **VR-001..VR-018**. Findings carry a severity:
- **ERROR** — blocks finalisation of the classification; the record must be corrected (e.g., VR-001 missing identity, VR-006 ownership shares not summing within tolerance, VR-016 missing LEI for a financial entity).
- **WARNING / INFO** — surfaced for attention but do not block classification.

Exceptions appear on the profile and, where appropriate, generate a review item. Correct the underlying data and re-validate / re-classify to clear them.

## 10. Using the simulation sandbox

The **Simulation** workspace lets you test "what-if" scenarios **without saving anything**:
1. Open **Simulation** and enter or adjust a candidate entity (identity, activity, ownership, financials).
2. Click **Simulate** (`POST /api/simulate`).
3. Review the simulated classification and its trace.

Nothing is persisted and no audit entry is created. Use it to explore thresholds — for example, set foreign equity to 9% then 11% to see the FDI determination change around the 10% threshold, or vary the largest ownership share around 50% to see control move to MAJ-VOTE.

## 11. Quick reference — classification dimensions

| Dimension | Values |
|---|---|
| residence | RES, NRES, MULTI |
| sector_code | S.11; S.12 (S.121–S.129); S.13 (S.1311–S.1314); S.14; S.15; S.2 |
| public_private | PUB-NFC, PUB-FC, GG, PRV-NFC, PRV-FC, FCC, NPISH |
| control_flag | MAJ-VOTE, BOARD, GOLDEN, CONTRACT, FINANCING, DOMINANT, REGULATORY, BO-CHAIN, KEY-PERS, NONE |
| market_status | MARKET, NON-MARKET (50% rule) |
| size_class | MICRO, SMALL, MEDIUM, LARGE (higher of FTE/turnover governs) |
| fdi_flag | INWARD-FULL, INWARD-ASSOC, OUTWARD, ROUND-TRIP, FELLOW, NONE (10% threshold) |
| special_entity_flag | HOLDING, SPV, CONSOLIDATE-PARENT, NONE |
