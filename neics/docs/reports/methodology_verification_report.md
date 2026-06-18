# Methodology Verification Report

> **NEICS — Staging / UAT environment.** This report is generated automatically by `tools/generate_reports.py` directly from the live classification engine and seeded test database. Generated: 2026-06-18 10:40 UTC.

Confirms that every classification, rule, lookup table, decision dimension, methodology reference and standard from the source framework and implementation workbook is represented in the system.

## Coverage checks

| Item | Expected (source) | In system | Status |
|---|---|---|---|
| Classification tests (framework Part III) | 18 | 18 | PASS |
| Institutional sectors migrated (workbook sheet 06) | 20 | 20 | PASS |
| Legal forms migrated (sheet 07) | 15 | 15 | PASS |
| ISIC classes migrated (sheet 08) | 35 | 35 | PASS |
| ISIC sections migrated (sheet 08b) | 21 | 21 | PASS |
| ISIC divisions migrated (sheet 08b) | 88 | 88 | PASS |
| Reference codelist entries migrated (sheet 10) | 42 | 42 | PASS |
| Metadata variables migrated (sheet 11) | 31 | 31 | PASS |
| Standards represented | 16 | 16 | PASS |
| Validation rules VR-001..VR-018 implemented | 18 | 18 | PASS |

## Validation rule library

Implemented validation rules: VR-001, VR-002, VR-003, VR-004, VR-005, VR-006, VR-007, VR-008, VR-009, VR-010, VR-011, VR-012, VR-013, VR-014, VR-015, VR-016, VR-017, VR-018.

## Public/private decision dimensions present

PUB-NFC, PUB-FC, GG, PRV-NFC, PRV-FC, FCC, NPISH — all produced by T6 rules.

## Control indicators present (Test 8 — 9 indicators)

MAJ-VOTE, BOARD, GOLDEN, CONTRACT, FINANCING, DOMINANT, REGULATORY, BO-CHAIN, KEY-PERS.

## FDI treatments present (Test 12)

INWARD-FULL, INWARD-ASSOC, ROUND-TRIP, (OUTWARD/FELLOW reserved), NONE.

