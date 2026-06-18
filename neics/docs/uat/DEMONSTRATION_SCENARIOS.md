# NEICS — Demonstration Scenarios

**National Enterprise Intelligence and Classification System (NEICS)** — State of Qatar NSO/NSC
Phase: Staging / UAT (no production deployment) · Version 1.0 · Date 2026-06-18

These six end-to-end scenarios are demonstrated live to stakeholders during the UAT demonstration phase. Each script provides both the UI click-path (React frontend) and the equivalent API calls (OpenAPI `/docs`), with concrete expected outputs drawn from the seeded golden dataset.

**Conventions.** Obtain a token first: `POST /api/auth/login` (form `username`, `password`); send `Authorization: Bearer <token>`. Identifiers such as `QA-ENT-2026000000025` are the seeded business keys; resolve to the internal `{id}` via `GET /api/enterprises` if the API requires the numeric id.

---

## Scenario 1 — New enterprise: upload → validation → classification → output

**Goal.** Show the happy path from data entry to a finalised, explainable classification.

**Actor.** Data Steward (`steward/steward123`) or Classifier (`classifier/classifier123`).

**UI click-path**
1. Log in as `steward`.
2. Enterprises → **New Enterprise**. Enter a market non-financial corporation: legal name, legal form (from the legal-form picker), residence = RES, principal activity (ISIC Rev.4), FTE and turnover (e.g., 120 FTE / QAR 80m → MEDIUM).
3. Save → open the new enterprise profile.
4. **Add Ownership** → e.g., 100% domestic private owner.
5. Click **Validate** → review the validation panel (no ERROR findings).
6. Click **Classify** → wait for completion.
7. Review the **Classification** tab and the **Explainability** trace.

**API calls**
```
POST /api/auth/login                         # steward
POST /api/enterprises                         # create -> {id}
POST /api/enterprises/{id}/ownership          # 100% private domestic
POST /api/enterprises/{id}/classify
GET  /api/enterprises/{id}/classification
GET  /api/enterprises/{id}/explain
```

**Expected output.** Validation returns no ERROR findings. Classification yields residence = RES, sector_code = S.11, public_private = PRV-NFC, control_flag = NONE (single owner, privately controlled), market_status = MARKET, size_class = MEDIUM, fdi_flag = NONE, special_entity_flag = NONE. The final record (T18) is persisted; the explainability trace lists tests T1–T18 with outcomes and the rules fired; a confidence indicator is shown; an audit entry and a quality score are created.

---

## Scenario 2 — Incomplete data: validation failures, missing-data detection, quality impact

**Goal.** Show that NEICS detects deficient data, blocks finalisation on ERROR-severity rules, and reflects gaps in the quality score.

**Actor.** Classifier (`classifier/classifier123`).

**UI click-path**
1. Log in as `classifier`.
2. Enterprises → **New Enterprise**. Deliberately omit required fields (e.g., legal name blank or invalid legal form) and provide ownership shares that sum to more than 100%.
3. Click **Validate**.
4. Observe the validation panel listing the triggered rules.
5. Attempt **Classify / Finalise**.
6. Open the **Quality** tab.

**API calls**
```
POST /api/auth/login                          # classifier
POST /api/enterprises                          # deficient payload
POST /api/enterprises/{id}/ownership           # shares summing > 100%
POST /api/enterprises/{id}/classify            # attempt
GET  /api/enterprises/{id}/profile             # quality block
```

**Expected output.** Validation raises the relevant rules — e.g., **VR-001** (mandatory identity completeness), **VR-002** (invalid legal form), **VR-006** (ownership shares exceed tolerance). ERROR-severity findings block finalisation of the final record; the system reports which fields are missing/invalid. The quality score is reduced, with the **Completeness**, **Validity**, and **Consistency** DAMA dimensions specifically lowered, and a validation/quality exception is generated (visible in the Review Center). No finalised classification is produced until the data is corrected.

---

## Scenario 3 — Government-controlled enterprise: ownership analysis, public/private, sector

**Goal.** Show public-sector boundary and control analysis for a state-controlled corporation.

**Actor.** Analyst (`analyst/analyst123`, read-only) or Classifier to (re)run classification.

**Reference entity.** State energy SOE `QA-ENT-20260000001` (and/or listed public corporation 62% state `QA-ENT-2026000000012`).

**UI click-path**
1. Log in; search for `QA-ENT-20260000001`.
2. Open the profile → **Ownership** tab (state ownership structure).
3. Open **Classification** tab; review T6 (Public Sector Boundary), T7 (Market/Non-Market), T8 (Ownership & Effective Control).
4. Open **Explainability** to read the public/private rationale.

**API calls**
```
GET /api/enterprises/{id}/ownership
POST /api/enterprises/{id}/classify            # if re-running (classifier)
GET /api/enterprises/{id}/classification
GET /api/enterprises/{id}/explain
```

**Expected output.** For `QA-ENT-20260000001`: sector_code = S.11, public_private = PUB-NFC, residence = RES, market_status = MARKET, control_flag reflecting majority state ownership. For the listed corporation `QA-ENT-2026000000012`: public_private = PUB-NFC with control_flag = MAJ-VOTE (62% state) and the listed flag set (T9). The explainability trace shows the public-sector boundary test (T6) placing the unit inside the public sector and identifies the controlling government unit.

---

## Scenario 4 — Foreign-owned enterprise: FDI classification, residency, ownership

**Goal.** Show residency treatment of a resident producing unit under foreign control and the FDI determination.

**Actor.** Classifier (`classifier/classifier123`).

**Reference entity.** Foreign MNE subsidiary 80% `QA-ENT-2026000000028` (and free-zone foreign manufacturer `QA-ENT-2026000000022`).

**UI click-path**
1. Log in; open `QA-ENT-2026000000028`.
2. **Ownership** tab → 80% non-resident parent.
3. **Classify** → review **Classification** and **Explainability** (T3 Residence, T12 Foreign Ownership & FDI).

**API calls**
```
GET  /api/enterprises/{id}/ownership
POST /api/enterprises/{id}/classify
GET  /api/enterprises/{id}/classification
GET  /api/enterprises/{id}/explain
```

**Expected output.** For `QA-ENT-2026000000028`: residence = RES (resident producing unit), public_private = FCC (foreign-controlled corporation), fdi_flag = INWARD-FULL (≥ 50% non-resident control, above the 10% FDI threshold), control_flag = MAJ-VOTE. For the free-zone manufacturer `QA-ENT-2026000000022`: sector_code = S.11, public_private = FCC, treated as a resident producing unit. The trace explains the 10% FDI threshold and the inward direct-investment relationship.

---

## Scenario 5 — Enterprise group: parent identification, subsidiary mapping, ultimate ownership

**Goal.** Show multi-level ownership-chain resolution and identification of the ultimate controlling institutional unit (UCI), including a round-trip cascade.

**Actor.** Data Steward or Analyst.

**Reference entity.** SWF cascade resident developer `QA-ENT-2026000000025` — 70% held via a non-resident QIA subsidiary; UCI = government.

**UI click-path**
1. Log in; open `QA-ENT-2026000000025`.
2. **Ownership** tab → view the chain: resident developer ← non-resident QIA subsidiary ← government (SWF/QIA).
3. Open the **Group / Consolidation** view to see parent and subsidiary mapping.
4. **Classify** → **Explainability**: review T11 (Group & Consolidation), T8 (Effective Control), T12 (FDI).

**API calls**
```
GET  /api/enterprises/{id}/ownership           # multi-level chain
POST /api/enterprises/{id}/classify
GET  /api/enterprises/{id}/classification
GET  /api/enterprises/{id}/explain             # UCI = government
```

**Expected output.** The ownership chain is resolved through the non-resident QIA subsidiary to the ultimate controlling institutional unit = **government**. Classification: public_private = PUB-NFC, fdi_flag = ROUND-TRIP (resident funds routed via a non-resident entity back into the resident economy), residence = RES, with the multi-level chain represented. The empty-shell holding `QA-ENT-2026000000026` may be shown alongside as special_entity_flag = CONSOLIDATE-PARENT to illustrate group consolidation handling.

---

## Scenario 6 — Manual review: ambiguous classification, exception, review workflow + override

**Goal.** Show how ambiguous or substance-over-form cases generate exceptions, flow through the Review Center, and can be overridden by a Reviewer with full audit.

**Actors.** Classifier (creates/raises), Reviewer (`reviewer/reviewer123`, resolves/overrides).

**Reference entity.** PPP SPV 49% gov + golden share `QA-ENT-2026000000024` (substance-over-form), or the dispersed-ownership board-control entity `QA-ENT-2026000000027`.

**UI click-path**
1. Log in as `classifier`; open `QA-ENT-2026000000024`; **Classify**.
2. Observe that the case is flagged for review (ambiguity: 49% equity but golden-share control) and an exception/review item is created.
3. Log in as `reviewer`; open the **Review Center**; select the item.
4. Review the explainability and ownership evidence.
5. Resolve the review, and where required apply an **Override** with a written justification.
6. Confirm the audit entry and history.

**API calls**
```
POST /api/auth/login                           # classifier
POST /api/enterprises/{id}/classify            # raises review/exception
GET  /api/reviews                              # reviewer: pending items
POST /api/reviews/{id}/resolve                 # resolve
POST /api/enterprises/{id}/override            # override with justification
GET  /api/enterprises/{id}/history             # versioned trail
GET  /api/audit                                # actor, timestamp, justification
```

**Expected output.** The PPP SPV is determined public_private = PUB-NFC via control_flag = GOLDEN (substance over form, despite 49% equity) and special_entity_flag = SPV; the case appears in the Review Center. The Reviewer can resolve it or apply an override; any override is recorded with actor, timestamp, and justification, the prior version is retained in history, and the override is captured in the audit log. The dashboard override-rate KPI updates accordingly.

---

## Demonstration checklist

| Scenario | Entities | Key endpoints | Demonstrated outcome | P/F |
|---|---|---|---|---|
| 1 New enterprise end-to-end | new entity | create/ownership/classify/explain | S.11 / PRV-NFC / MARKET, full trace | |
| 2 Incomplete data | deficient entity | validate/classify | VR-001/002/006, quality drop, exception | |
| 3 Government-controlled | `…0000001`, `…000012` | classify/explain | S.11 PUB-NFC; MAJ-VOTE; T6/T7 | |
| 4 Foreign-owned | `…000028`, `…000022` | classify/explain | FCC; INWARD-FULL; RES | |
| 5 Enterprise group | `…000025` (`…000026`) | ownership/classify/explain | UCI = government; ROUND-TRIP; chain | |
| 6 Manual review & override | `…000024` (`…000027`) | reviews/resolve/override/audit | GOLDEN; review→override; audited | |
