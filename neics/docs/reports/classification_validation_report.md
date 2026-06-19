# Classification Validation Report

> **NEICS — Staging / UAT environment.** This report is generated automatically by `tools/generate_reports.py` directly from the live classification engine and seeded test database. Generated: 2026-06-19 07:39 UTC.

Every test enterprise is classified by the live 18-test pipeline. The table shows the result, confidence, and a check against the expected sector / public-private verdict.
**Result: 74/74 enterprises match their expected sector + public-private verdict.**


| Enterprise | Name | Sector | Public/Private | Control | Market | Size | FDI | Special | Conf | Expected | ✓ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| QA-ENT-20260000001 | Qatar National Energy Corp (sample | S.11 | PUB-NFC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PUB-NFC | ✅ |
| QA-ENT-20260000002 | Sample National Bank Q.P.S.C. | S.122 | PUB-FC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.122/PUB-FC | ✅ |
| QA-ENT-20260000003 | Sample Free-Zone Chemicals W.L.L. | S.11 | FCC | MAJ-VOTE | MARKET | MEDIUM | INWARD-FULL | NONE | 1.0 | S.11/FCC | ✅ |
| QA-ENT-20260000004 | Sample QFC Asset Management LLC | S.126 | FCC | MAJ-VOTE | MARKET | SMALL | INWARD-FULL | NONE | 1.0 | S.126/FCC | ✅ |
| QA-ENT-20260000005 | Sample Family Holding Group | S.11 | PRV-NFC | MAJ-VOTE | MARKET | LARGE | NONE | HOLDING | 1.0 | S.11/PRV-NFC | ✅ |
| QA-ENT-20260000006 | Sample Charitable Foundation | S.13 | GG | BOARD | NON-MARKET | LARGE | NONE | NONE | 1.0 | S.13/GG | ✅ |
| QA-ENT-20260000010 | Ministry of Sample Affairs | S.13 | GG | NONE | NON-MARKET | LARGE | NONE | NONE | 1.0 | S.13/GG | ✅ |
| QA-ENT-20260000011 | Sample Regulatory Authority | S.13 | GG | NONE | NON-MARKET | LARGE | NONE | NONE | 1.0 | S.13/GG | ✅ |
| QA-ENT-20260000012 | Sample State Energy Co | S.11 | PUB-NFC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PUB-NFC | ✅ |
| QA-ENT-20260000013 | Sample Industries QPSC | S.11 | PUB-NFC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PUB-NFC | ✅ |
| QA-ENT-20260000014 | Sample Family Trading Group | S.11 | PRV-NFC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PRV-NFC | ✅ |
| QA-ENT-20260000015 | Sample Commercial Bank QPSC | S.122 | PUB-FC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.122/PUB-FC | ✅ |
| QA-ENT-20260000016 | Sample Insurance QPSC | S.128 | PRV-FC | MAJ-VOTE | MARKET | LARGE | INWARD-ASSOC | NONE | 1.0 | S.128/PRV-FC | ✅ |
| QA-ENT-20260000017 | Sample Investment Fund | S.127 | PRV-FC | MAJ-VOTE | MARKET | MEDIUM | NONE | SPV | 1.0 | S.127/PRV-FC | ✅ |
| QA-ENT-20260000018 | Sample Sports Club | S.15 | NPISH | NONE | NON-MARKET | MEDIUM | NONE | NONE | 1.0 | S.15/NPISH | ✅ |
| QA-ENT-20260000019 | Sample Sole Proprietor Workshop | S.14 | PRV-NFC | NONE | MARKET | MICRO | NONE | NONE | 1.0 | S.14/PRV-NFC | ✅ |
| QA-ENT-20260000020 | Sample Quasi-Corporation Branch | S.11 | PRV-NFC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PRV-NFC | ✅ |
| QA-ENT-20260000021 | Sample QFC Advisory LLC | S.126 | FCC | MAJ-VOTE | MARKET | SMALL | INWARD-FULL | NONE | 1.0 | S.126/FCC | ✅ |
| QA-ENT-20260000022 | Sample Free-Zone Plastics WLL | S.11 | FCC | MAJ-VOTE | MARKET | MEDIUM | INWARD-FULL | NONE | 1.0 | S.11/FCC | ✅ |
| QA-ENT-20260000023 | Sample Petrochemicals JV | S.11 | PUB-NFC | MAJ-VOTE | MARKET | LARGE | ROUND-TRIP | NONE | 1.0 | S.11/PUB-NFC | ✅ |
| QA-ENT-20260000024 | Sample Infrastructure SPV | S.11 | PUB-NFC | GOLDEN | MARKET | LARGE | ROUND-TRIP | NONE | 1.0 | S.11/PUB-NFC | ✅ |
| QA-ENT-20260000025 | Sample Property Developer | S.11 | PUB-NFC | MAJ-VOTE | MARKET | LARGE | ROUND-TRIP | NONE | 1.0 | S.11/PUB-NFC | ✅ |
| QA-ENT-20260000026 | Sample Empty-Shell Holding | S.11 | PRV-NFC | MAJ-VOTE | MARKET | MICRO | NONE | CONSOLIDATE-PARENT | 0.956 | S.11/PRV-NFC | ✅ |
| QA-ENT-20260000027 | Sample Dispersed-Ownership Corp | S.11 | PUB-NFC | BOARD | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PUB-NFC | ✅ |
| QA-ENT-20260000028 | Sample MNE Subsidiary WLL | S.11 | FCC | MAJ-VOTE | MARKET | LARGE | INWARD-FULL | NONE | 1.0 | S.11/FCC | ✅ |
| QA-ENT-20260000029 | Sample Micro Retailer | S.11 | PRV-NFC | MAJ-VOTE | MARKET | MICRO | NONE | NONE | 1.0 | S.11/PRV-NFC | ✅ |
| QA-ENT-20260000030 | Sample Large Private Industrial | S.11 | PRV-NFC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PRV-NFC | ✅ |
| QA-ENT-20260000031 | Sample Central Bank of Qatar | S.121 | PUB-FC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.121/PUB-FC | ✅ |
| QA-ENT-20260000032 | Sample State Pension Fund | S.129 | PUB-FC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.129/PUB-FC | ✅ |
| QA-ENT-20260000033 | Sample Reinsurance QPSC | S.128 | PRV-FC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.128/PRV-FC | ✅ |
| QA-ENT-20260000034 | Sample Foreign Bank Branch (QFC) | S.122 | FCC | MAJ-VOTE | MARKET | LARGE | INWARD-FULL | NONE | 1.0 | S.122/FCC | ✅ |
| QA-ENT-20260000035 | Sample Charitable Waqf Endowment | S.15 | NPISH | NONE | NON-MARKET | SMALL | NONE | NONE | 1.0 | S.15/NPISH | ✅ |
| QA-ENT-20260000040 | Sample Electricity & Water Corp | S.11 | PUB-NFC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PUB-NFC | ✅ |
| QA-ENT-20260000041 | Sample Ports Authority Corp | S.11 | PUB-NFC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PUB-NFC | ✅ |
| QA-ENT-20260000042 | Sample Rail Company | S.11 | PUB-NFC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PUB-NFC | ✅ |
| QA-ENT-20260000043 | Sample National Airline | S.11 | PUB-NFC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PUB-NFC | ✅ |
| QA-ENT-20260000044 | Sample Postal Corporation | S.11 | PUB-NFC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PUB-NFC | ✅ |
| QA-ENT-20260000045 | Sample National Telecom QPSC | S.11 | PUB-NFC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PUB-NFC | ✅ |
| QA-ENT-20260000046 | Sample Petrochemical Industries QP | S.11 | PUB-NFC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PUB-NFC | ✅ |
| QA-ENT-20260000047 | Sample Steel Industries QPSC | S.11 | PUB-NFC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PUB-NFC | ✅ |
| QA-ENT-20260000048 | Sample Ministry of Education | S.13 | GG | NONE | NON-MARKET | LARGE | NONE | NONE | 1.0 | S.13/GG | ✅ |
| QA-ENT-20260000049 | Sample Ministry of Public Health | S.13 | GG | NONE | NON-MARKET | LARGE | NONE | NONE | 1.0 | S.13/GG | ✅ |
| QA-ENT-20260000050 | Sample Municipality | S.13 | GG | NONE | NON-MARKET | LARGE | NONE | NONE | 1.0 | S.13/GG | ✅ |
| QA-ENT-20260000051 | Sample Civil Aviation Authority | S.13 | GG | NONE | NON-MARKET | LARGE | NONE | NONE | 1.0 | S.13/GG | ✅ |
| QA-ENT-20260000052 | Sample Public University | S.13 | GG | NONE | NON-MARKET | LARGE | NONE | NONE | 1.0 | S.13/GG | ✅ |
| QA-ENT-20260000053 | Sample Private Commercial Bank QPS | S.122 | PRV-FC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.122/PRV-FC | ✅ |
| QA-ENT-20260000054 | Sample Islamic Bank QPSC | S.122 | PUB-FC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.122/PUB-FC | ✅ |
| QA-ENT-20260000055 | Sample Brokerage House | S.126 | PRV-FC | MAJ-VOTE | MARKET | MEDIUM | NONE | NONE | 1.0 | S.126/PRV-FC | ✅ |
| QA-ENT-20260000056 | Sample Takaful Insurance QPSC | S.128 | PRV-FC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.128/PRV-FC | ✅ |
| QA-ENT-20260000057 | Sample Sovereign Investment Vehicl | S.127 | PUB-FC | MAJ-VOTE | MARKET | LARGE | NONE | HOLDING | 1.0 | S.127/PUB-FC | ✅ |
| QA-ENT-20260000058 | Sample Exchange & Money Transfer | S.126 | PRV-FC | MAJ-VOTE | MARKET | MEDIUM | NONE | NONE | 1.0 | S.126/PRV-FC | ✅ |
| QA-ENT-20260000059 | Sample Real Estate Investment Trus | S.127 | PRV-FC | MAJ-VOTE | MARKET | LARGE | NONE | SPV | 1.0 | S.127/PRV-FC | ✅ |
| QA-ENT-20260000060 | Sample Charitable Society | S.15 | NPISH | NONE | NON-MARKET | MEDIUM | NONE | NONE | 1.0 | S.15/NPISH | ✅ |
| QA-ENT-20260000061 | Sample Professional Association | S.15 | NPISH | NONE | NON-MARKET | SMALL | NONE | NONE | 1.0 | S.15/NPISH | ✅ |
| QA-ENT-20260000062 | Sample Cultural Foundation | S.15 | NPISH | NONE | NON-MARKET | MEDIUM | NONE | NONE | 1.0 | S.15/NPISH | ✅ |
| QA-ENT-20260000063 | Sample Sole Proprietor Garage | S.14 | PRV-NFC | NONE | MARKET | MICRO | NONE | NONE | 1.0 | S.14/PRV-NFC | ✅ |
| QA-ENT-20260000064 | Sample Family Grocery (sole propri | S.14 | PRV-NFC | NONE | MARKET | MICRO | NONE | NONE | 1.0 | S.14/PRV-NFC | ✅ |
| QA-ENT-20260000065 | Sample Foreign Engineering Branch | S.11 | FCC | MAJ-VOTE | MARKET | LARGE | INWARD-FULL | NONE | 1.0 | S.11/FCC | ✅ |
| QA-ENT-20260000066 | Sample QFC Reinsurance Branch | S.128 | FCC | MAJ-VOTE | MARKET | LARGE | INWARD-FULL | NONE | 1.0 | S.128/FCC | ✅ |
| QA-ENT-20260000067 | Sample Free-Zone Logistics WLL | S.11 | FCC | MAJ-VOTE | MARKET | LARGE | INWARD-FULL | NONE | 1.0 | S.11/FCC | ✅ |
| QA-ENT-20260000068 | Sample Foreign Retail Franchise | S.11 | FCC | MAJ-VOTE | MARKET | LARGE | INWARD-FULL | NONE | 1.0 | S.11/FCC | ✅ |
| QA-ENT-20260000069 | Sample MNE Oilfield Services Sub | S.11 | FCC | MAJ-VOTE | MARKET | LARGE | INWARD-FULL | NONE | 1.0 | S.11/FCC | ✅ |
| QA-ENT-20260000070 | Sample Construction Contracting WL | S.11 | PRV-NFC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PRV-NFC | ✅ |
| QA-ENT-20260000071 | Sample IT Services Startup | S.11 | PRV-NFC | MAJ-VOTE | MARKET | SMALL | NONE | NONE | 1.0 | S.11/PRV-NFC | ✅ |
| QA-ENT-20260000072 | Sample Restaurant Group | S.11 | PRV-NFC | MAJ-VOTE | MARKET | MEDIUM | NONE | NONE | 1.0 | S.11/PRV-NFC | ✅ |
| QA-ENT-20260000073 | Sample Real Estate Developer (priv | S.11 | PRV-NFC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PRV-NFC | ✅ |
| QA-ENT-20260000074 | Sample Logistics SME | S.11 | PRV-NFC | MAJ-VOTE | MARKET | MEDIUM | NONE | NONE | 1.0 | S.11/PRV-NFC | ✅ |
| QA-ENT-20260000075 | Sample Private Hospital | S.11 | PRV-NFC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PRV-NFC | ✅ |
| QA-ENT-20260000076 | Sample Private School Operator | S.11 | PRV-NFC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PRV-NFC | ✅ |
| QA-ENT-20260000077 | Sample Micro Bakery | S.11 | PRV-NFC | MAJ-VOTE | MARKET | MICRO | NONE | NONE | 1.0 | S.11/PRV-NFC | ✅ |
| QA-ENT-20260000078 | Sample Large Trading Conglomerate | S.11 | PRV-NFC | MAJ-VOTE | MARKET | LARGE | NONE | NONE | 1.0 | S.11/PRV-NFC | ✅ |
| QA-ENT-20260000079 | Sample Holding Company (private) | S.11 | PRV-NFC | MAJ-VOTE | MARKET | LARGE | NONE | HOLDING | 1.0 | S.11/PRV-NFC | ✅ |
| QA-ENT-20260000080 | Sample Foodstuff & General Trading | S.11 | PRV-NFC | MAJ-VOTE | MARKET | LARGE | NONE | HOLDING | 1.0 | S.11/PRV-NFC | ✅ |
| QA-ENT-20260000099 | Sample Trading Co (sample) | S.11 | PUB-NFC | BO-CHAIN | MARKET | MEDIUM | NONE | NONE | 1.0 | S.11/PUB-NFC | ✅ |

## Per-enterprise classification detail (input → ownership → rules → result)

### QA-ENT-20260000001 — Qatar National Energy Corp (sample)
- **Input:** legal_form=SOE, isic=0610, residence=RES, employment=1800, turnover=48000000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=100.0%, gov_voting=100.0%, foreign_own=0.0%, gov_control=True, UCI=State of Qatar (govt=True)
- **Result:** sector **S.11**, public/private **PUB-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '0610'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-020` → {'public_private': 'PUB-NFC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000002 — Sample National Bank Q.P.S.C.
- **Input:** legal_form=JSC, isic=6419, residence=RES, employment=5200, turnover=22000000000.0, financial=True, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=51.0%, gov_voting=51.0%, foreign_own=0.0%, gov_control=True, UCI=State of Qatar (govt=True)
- **Result:** sector **S.122**, public/private **PUB-FC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6419'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-022` → {'sector_code': 'S.122'}  _(std: SNA 2025)_
    - T6 `R-T06-010` → {'public_private': 'PUB-FC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000003 — Sample Free-Zone Chemicals W.L.L.
- **Input:** legal_form=FZ, isic=2011, residence=RES, employment=240, turnover=50000000.0, financial=False, nonprofit=False, jurisdiction=QFZA
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=100.0%, gov_control=False, UCI=Foreign Industrial Parent (govt=False)
- **Result:** sector **S.11**, public/private **FCC**, control **MAJ-VOTE**, market **MARKET**, size **MEDIUM**, FDI **INWARD-FULL**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '2011'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-040` → {'public_private': 'FCC'}  _(std: OECD BD4)_
    - T10 `R-T10-020` → {'size_class': 'MEDIUM'}  _(std: QNCS)_
    - T12 `R-T12-020` → {'fdi_flag': 'INWARD-FULL'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000004 — Sample QFC Asset Management LLC
- **Input:** legal_form=QFC, isic=6630, residence=RES, employment=30, turnover=15000000.0, financial=True, nonprofit=False, jurisdiction=QFC
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=100.0%, gov_control=False, UCI=Foreign Financial Institution (govt=False)
- **Result:** sector **S.126**, public/private **FCC**, control **MAJ-VOTE**, market **MARKET**, size **SMALL**, FDI **INWARD-FULL**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6630'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-023` → {'sector_code': 'S.126'}  _(std: SNA 2025)_
    - T6 `R-T06-040` → {'public_private': 'FCC'}  _(std: OECD BD4)_
    - T10 `R-T10-030` → {'size_class': 'SMALL'}  _(std: QNCS)_
    - T12 `R-T12-020` → {'fdi_flag': 'INWARD-FULL'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000005 — Sample Family Holding Group
- **Input:** legal_form=LLC, isic=6420, residence=RES, employment=600, turnover=500000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Founding Family (govt=False)
- **Result:** sector **S.11**, public/private **PRV-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **HOLDING**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6420'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-020` → {'special_entity_flag': 'HOLDING'}  _(std: ISIC Rev.4 / SNA 2025)_

### QA-ENT-20260000006 — Sample Charitable Foundation
- **Input:** legal_form=FND, isic=8540, residence=RES, employment=300, turnover=0.0, financial=False, nonprofit=True, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=True, UCI=Supervising Ministry (govt=True)
- **Result:** sector **S.13**, public/private **GG**, control **BOARD**, market **NON-MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '8540'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-020` → {'market_status': 'NON-MARKET'}  _(std: SNA 2025)_
    - T8 `R-T08-001` → {'control_flag': 'BOARD'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-030` → {'sector_code': 'S.13'}  _(std: GFS 2014 / SNA 2025)_
    - T6 `R-T06-030` → {'public_private': 'GG'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000010 — Ministry of Sample Affairs
- **Input:** legal_form=GOV, isic=8412, residence=RES, employment=2000, turnover=0.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=None (govt=False)
- **Result:** sector **S.13**, public/private **GG**, control **NONE**, market **NON-MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '8412'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-010` → {'market_status': 'NON-MARKET'}  _(std: GFS 2014)_
    - T8 `R-T08-001` → {'control_flag': 'NONE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-010` → {'sector_code': 'S.13'}  _(std: SNA 2025)_
    - T6 `R-T06-005` → {'public_private': 'GG'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000011 — Sample Regulatory Authority
- **Input:** legal_form=GOV, isic=8412, residence=RES, employment=400, turnover=2000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=None (govt=False)
- **Result:** sector **S.13**, public/private **GG**, control **NONE**, market **NON-MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '8412'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-010` → {'market_status': 'NON-MARKET'}  _(std: GFS 2014)_
    - T8 `R-T08-001` → {'control_flag': 'NONE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-010` → {'sector_code': 'S.13'}  _(std: SNA 2025)_
    - T6 `R-T06-005` → {'public_private': 'GG'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000012 — Sample State Energy Co
- **Input:** legal_form=SOE, isic=3510, residence=RES, employment=900, turnover=9000000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=100.0%, gov_voting=100.0%, foreign_own=0.0%, gov_control=True, UCI=State of Qatar (govt=True)
- **Result:** sector **S.11**, public/private **PUB-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '3510'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-020` → {'public_private': 'PUB-NFC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000013 — Sample Industries QPSC
- **Input:** legal_form=JSC, isic=2410, residence=RES, employment=1500, turnover=7000000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=62.0%, gov_voting=62.0%, foreign_own=0.0%, gov_control=True, UCI=State of Qatar (govt=True)
- **Result:** sector **S.11**, public/private **PUB-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '2410'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-020` → {'public_private': 'PUB-NFC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000014 — Sample Family Trading Group
- **Input:** legal_form=LLC, isic=4690, residence=RES, employment=800, turnover=600000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=15.0%, gov_voting=15.0%, foreign_own=0.0%, gov_control=False, UCI=Founding Family (govt=False)
- **Result:** sector **S.11**, public/private **PRV-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '4690'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000015 — Sample Commercial Bank QPSC
- **Input:** legal_form=JSC, isic=6419, residence=RES, employment=3000, turnover=15000000000.0, financial=True, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=59.0%, gov_voting=59.0%, foreign_own=0.0%, gov_control=True, UCI=State of Qatar (govt=True)
- **Result:** sector **S.122**, public/private **PUB-FC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6419'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-022` → {'sector_code': 'S.122'}  _(std: SNA 2025)_
    - T6 `R-T06-010` → {'public_private': 'PUB-FC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000016 — Sample Insurance QPSC
- **Input:** legal_form=JSC, isic=6512, residence=RES, employment=300, turnover=800000000.0, financial=True, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=10.0%, gov_control=False, UCI=Private investors (govt=False)
- **Result:** sector **S.128**, public/private **PRV-FC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **INWARD-ASSOC**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6512'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-025` → {'sector_code': 'S.128'}  _(std: SNA 2025)_
    - T6 `R-T06-050` → {'public_private': 'PRV-FC'}  _(std: SNA 2025)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-030` → {'fdi_flag': 'INWARD-ASSOC'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000017 — Sample Investment Fund
- **Input:** legal_form=FND, isic=6430, residence=RES, employment=12, turnover=40000000.0, financial=True, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Asset manager (govt=False)
- **Result:** sector **S.127**, public/private **PRV-FC**, control **MAJ-VOTE**, market **MARKET**, size **MEDIUM**, FDI **NONE**, special **SPV**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6430'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-024` → {'sector_code': 'S.127'}  _(std: SNA 2025)_
    - T6 `R-T06-050` → {'public_private': 'PRV-FC'}  _(std: SNA 2025)_
    - T10 `R-T10-020` → {'size_class': 'MEDIUM'}  _(std: QNCS)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-030` → {'special_entity_flag': 'SPV'}  _(std: SNA 2025)_

### QA-ENT-20260000018 — Sample Sports Club
- **Input:** legal_form=CA, isic=9499, residence=RES, employment=60, turnover=3000000.0, financial=False, nonprofit=True, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=None (govt=False)
- **Result:** sector **S.15**, public/private **NPISH**, control **NONE**, market **NON-MARKET**, size **MEDIUM**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '9499'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-020` → {'market_status': 'NON-MARKET'}  _(std: SNA 2025)_
    - T8 `R-T08-001` → {'control_flag': 'NONE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-035` → {'sector_code': 'S.15'}  _(std: SNA 2025)_
    - T6 `R-T06-035` → {'public_private': 'NPISH'}  _(std: SNA 2025)_
    - T10 `R-T10-020` → {'size_class': 'MEDIUM'}  _(std: QNCS)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000019 — Sample Sole Proprietor Workshop
- **Input:** legal_form=SP, isic=4690, residence=RES, employment=3, turnover=1500000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=None (govt=False)
- **Result:** sector **S.14**, public/private **PRV-NFC**, control **NONE**, market **MARKET**, size **MICRO**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '4690'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'NONE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-050` → {'sector_code': 'S.14'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-100` → {'size_class': 'MICRO'}  _(std: QNCS)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000020 — Sample Quasi-Corporation Branch
- **Input:** legal_form=BR, isic=4100, residence=RES, employment=120, turnover=200000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Resident owner (govt=False)
- **Result:** sector **S.11**, public/private **PRV-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '4100'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000021 — Sample QFC Advisory LLC
- **Input:** legal_form=QFC, isic=6630, residence=RES, employment=25, turnover=12000000.0, financial=True, nonprofit=False, jurisdiction=QFC
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=100.0%, gov_control=False, UCI=Foreign financial parent (govt=False)
- **Result:** sector **S.126**, public/private **FCC**, control **MAJ-VOTE**, market **MARKET**, size **SMALL**, FDI **INWARD-FULL**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6630'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-023` → {'sector_code': 'S.126'}  _(std: SNA 2025)_
    - T6 `R-T06-040` → {'public_private': 'FCC'}  _(std: OECD BD4)_
    - T10 `R-T10-030` → {'size_class': 'SMALL'}  _(std: QNCS)_
    - T12 `R-T12-020` → {'fdi_flag': 'INWARD-FULL'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000022 — Sample Free-Zone Plastics WLL
- **Input:** legal_form=FZ, isic=2013, residence=RES, employment=180, turnover=90000000.0, financial=False, nonprofit=False, jurisdiction=QFZA
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=100.0%, gov_control=False, UCI=Foreign industrial parent (govt=False)
- **Result:** sector **S.11**, public/private **FCC**, control **MAJ-VOTE**, market **MARKET**, size **MEDIUM**, FDI **INWARD-FULL**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '2013'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-040` → {'public_private': 'FCC'}  _(std: OECD BD4)_
    - T10 `R-T10-020` → {'size_class': 'MEDIUM'}  _(std: QNCS)_
    - T12 `R-T12-020` → {'fdi_flag': 'INWARD-FULL'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000023 — Sample Petrochemicals JV
- **Input:** legal_form=JSC, isic=2011, residence=RES, employment=700, turnover=4000000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=65.0%, gov_voting=65.0%, foreign_own=35.0%, gov_control=True, UCI=State petrochemicals corp (govt=True)
- **Result:** sector **S.11**, public/private **PUB-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **ROUND-TRIP**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '2011'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-020` → {'public_private': 'PUB-NFC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-010` → {'fdi_flag': 'ROUND-TRIP'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000024 — Sample Infrastructure SPV
- **Input:** legal_form=LLC, isic=4290, residence=RES, employment=40, turnover=300000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=49.0%, gov_voting=49.0%, foreign_own=51.0%, gov_control=True, UCI=Government (golden share) (govt=True)
- **Result:** sector **S.11**, public/private **PUB-NFC**, control **GOLDEN**, market **MARKET**, size **LARGE**, FDI **ROUND-TRIP**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '4290'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'GOLDEN'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-020` → {'public_private': 'PUB-NFC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-010` → {'fdi_flag': 'ROUND-TRIP'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000025 — Sample Property Developer
- **Input:** legal_form=LLC, isic=6810, residence=RES, employment=350, turnover=800000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=70.0%, gov_voting=70.0%, foreign_own=70.0%, gov_control=True, UCI=Qatar Investment Authority (govt=True)
- **Result:** sector **S.11**, public/private **PUB-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **ROUND-TRIP**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6810'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-020` → {'public_private': 'PUB-NFC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-010` → {'fdi_flag': 'ROUND-TRIP'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000026 — Sample Empty-Shell Holding
- **Input:** legal_form=LLC, isic=6420, residence=RES, employment=0, turnover=0.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Ultimate family unit (govt=False)
- **Result:** sector **S.11**, public/private **PRV-NFC**, control **MAJ-VOTE**, market **MARKET**, size **MICRO**, FDI **NONE**, special **CONSOLIDATE-PARENT**; confidence **0.956**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6420'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-100` → {'market_status': 'MARKET'}  _(std: SNA 2025)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-100` → {'size_class': 'MICRO'}  _(std: QNCS)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-010` → {'special_entity_flag': 'CONSOLIDATE-PARENT'}  _(std: SNA 2025 §4 (empty-shell rule))_

### QA-ENT-20260000027 — Sample Dispersed-Ownership Corp
- **Input:** legal_form=JSC, isic=6810, residence=RES, employment=500, turnover=900000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=True, UCI=State institution (board rights) (govt=True)
- **Result:** sector **S.11**, public/private **PUB-NFC**, control **BOARD**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6810'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'BOARD'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-020` → {'public_private': 'PUB-NFC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000028 — Sample MNE Subsidiary WLL
- **Input:** legal_form=LLC, isic=6201, residence=RES, employment=220, turnover=180000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=80.0%, gov_control=False, UCI=Global technology parent (govt=False)
- **Result:** sector **S.11**, public/private **FCC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **INWARD-FULL**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6201'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-040` → {'public_private': 'FCC'}  _(std: OECD BD4)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-020` → {'fdi_flag': 'INWARD-FULL'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000029 — Sample Micro Retailer
- **Input:** legal_form=LLC, isic=4690, residence=RES, employment=5, turnover=1200000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Local owner (govt=False)
- **Result:** sector **S.11**, public/private **PRV-NFC**, control **MAJ-VOTE**, market **MARKET**, size **MICRO**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '4690'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-100` → {'size_class': 'MICRO'}  _(std: QNCS)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000030 — Sample Large Private Industrial
- **Input:** legal_form=JSC, isic=2310, residence=RES, employment=1200, turnover=2000000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Private holding (govt=False)
- **Result:** sector **S.11**, public/private **PRV-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '2310'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000031 — Sample Central Bank of Qatar
- **Input:** legal_form=SOE, isic=6411, residence=RES, employment=900, turnover=8000000000.0, financial=True, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=100.0%, gov_voting=100.0%, foreign_own=0.0%, gov_control=True, UCI=State of Qatar (govt=True)
- **Result:** sector **S.121**, public/private **PUB-FC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6411'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-021` → {'sector_code': 'S.121'}  _(std: SNA 2025)_
    - T6 `R-T06-010` → {'public_private': 'PUB-FC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000032 — Sample State Pension Fund
- **Input:** legal_form=FND, isic=6530, residence=RES, employment=120, turnover=2000000000.0, financial=True, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=100.0%, gov_voting=100.0%, foreign_own=0.0%, gov_control=True, UCI=State of Qatar (govt=True)
- **Result:** sector **S.129**, public/private **PUB-FC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6530'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-026` → {'sector_code': 'S.129'}  _(std: SNA 2025)_
    - T6 `R-T06-010` → {'public_private': 'PUB-FC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000033 — Sample Reinsurance QPSC
- **Input:** legal_form=JSC, isic=6520, residence=RES, employment=210, turnover=1500000000.0, financial=True, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Private investors (govt=False)
- **Result:** sector **S.128**, public/private **PRV-FC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6520'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-025` → {'sector_code': 'S.128'}  _(std: SNA 2025)_
    - T6 `R-T06-050` → {'public_private': 'PRV-FC'}  _(std: SNA 2025)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000034 — Sample Foreign Bank Branch (QFC)
- **Input:** legal_form=BR, isic=6419, residence=RES, employment=140, turnover=400000000.0, financial=True, nonprofit=False, jurisdiction=QFC
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=100.0%, gov_control=False, UCI=Foreign bank HQ (govt=False)
- **Result:** sector **S.122**, public/private **FCC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **INWARD-FULL**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6419'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-022` → {'sector_code': 'S.122'}  _(std: SNA 2025)_
    - T6 `R-T06-040` → {'public_private': 'FCC'}  _(std: OECD BD4)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-020` → {'fdi_flag': 'INWARD-FULL'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000035 — Sample Charitable Waqf Endowment
- **Input:** legal_form=WQ, isic=9499, residence=RES, employment=40, turnover=1000000.0, financial=False, nonprofit=True, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=None (govt=False)
- **Result:** sector **S.15**, public/private **NPISH**, control **NONE**, market **NON-MARKET**, size **SMALL**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '9499'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-020` → {'market_status': 'NON-MARKET'}  _(std: SNA 2025)_
    - T8 `R-T08-001` → {'control_flag': 'NONE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-035` → {'sector_code': 'S.15'}  _(std: SNA 2025)_
    - T6 `R-T06-035` → {'public_private': 'NPISH'}  _(std: SNA 2025)_
    - T10 `R-T10-030` → {'size_class': 'SMALL'}  _(std: QNCS)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000040 — Sample Electricity & Water Corp
- **Input:** legal_form=SOE, isic=3510, residence=RES, employment=2400, turnover=12000000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=100.0%, gov_voting=100.0%, foreign_own=0.0%, gov_control=True, UCI=State of Qatar (govt=True)
- **Result:** sector **S.11**, public/private **PUB-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '3510'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-020` → {'public_private': 'PUB-NFC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000041 — Sample Ports Authority Corp
- **Input:** legal_form=SOE, isic=5224, residence=RES, employment=1800, turnover=3000000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=100.0%, gov_voting=100.0%, foreign_own=0.0%, gov_control=True, UCI=State of Qatar (govt=True)
- **Result:** sector **S.11**, public/private **PUB-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '5224'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-020` → {'public_private': 'PUB-NFC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000042 — Sample Rail Company
- **Input:** legal_form=SOE, isic=4920, residence=RES, employment=2100, turnover=2500000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=100.0%, gov_voting=100.0%, foreign_own=0.0%, gov_control=True, UCI=State of Qatar (govt=True)
- **Result:** sector **S.11**, public/private **PUB-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '4920'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-020` → {'public_private': 'PUB-NFC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000043 — Sample National Airline
- **Input:** legal_form=SOE, isic=5110, residence=RES, employment=9000, turnover=40000000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=100.0%, gov_voting=100.0%, foreign_own=0.0%, gov_control=True, UCI=State of Qatar (govt=True)
- **Result:** sector **S.11**, public/private **PUB-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '5110'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-020` → {'public_private': 'PUB-NFC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000044 — Sample Postal Corporation
- **Input:** legal_form=SOE, isic=4920, residence=RES, employment=900, turnover=400000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=100.0%, gov_voting=100.0%, foreign_own=0.0%, gov_control=True, UCI=State of Qatar (govt=True)
- **Result:** sector **S.11**, public/private **PUB-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '4920'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-020` → {'public_private': 'PUB-NFC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000045 — Sample National Telecom QPSC
- **Input:** legal_form=JSC, isic=6201, residence=RES, employment=3500, turnover=30000000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=55.0%, gov_voting=55.0%, foreign_own=0.0%, gov_control=True, UCI=State of Qatar (govt=True)
- **Result:** sector **S.11**, public/private **PUB-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6201'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-020` → {'public_private': 'PUB-NFC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000046 — Sample Petrochemical Industries QPSC
- **Input:** legal_form=JSC, isic=2011, residence=RES, employment=2600, turnover=18000000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=62.0%, gov_voting=62.0%, foreign_own=0.0%, gov_control=True, UCI=State of Qatar (govt=True)
- **Result:** sector **S.11**, public/private **PUB-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '2011'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-020` → {'public_private': 'PUB-NFC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000047 — Sample Steel Industries QPSC
- **Input:** legal_form=JSC, isic=2410, residence=RES, employment=1500, turnover=9000000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=51.0%, gov_voting=51.0%, foreign_own=0.0%, gov_control=True, UCI=State of Qatar (govt=True)
- **Result:** sector **S.11**, public/private **PUB-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '2410'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-020` → {'public_private': 'PUB-NFC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000048 — Sample Ministry of Education
- **Input:** legal_form=GOV, isic=8412, residence=RES, employment=5000, turnover=0.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=None (govt=False)
- **Result:** sector **S.13**, public/private **GG**, control **NONE**, market **NON-MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '8412'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-010` → {'market_status': 'NON-MARKET'}  _(std: GFS 2014)_
    - T8 `R-T08-001` → {'control_flag': 'NONE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-010` → {'sector_code': 'S.13'}  _(std: SNA 2025)_
    - T6 `R-T06-005` → {'public_private': 'GG'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000049 — Sample Ministry of Public Health
- **Input:** legal_form=GOV, isic=8412, residence=RES, employment=8000, turnover=0.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=None (govt=False)
- **Result:** sector **S.13**, public/private **GG**, control **NONE**, market **NON-MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '8412'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-010` → {'market_status': 'NON-MARKET'}  _(std: GFS 2014)_
    - T8 `R-T08-001` → {'control_flag': 'NONE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-010` → {'sector_code': 'S.13'}  _(std: SNA 2025)_
    - T6 `R-T06-005` → {'public_private': 'GG'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000050 — Sample Municipality
- **Input:** legal_form=GOV, isic=8412, residence=RES, employment=1200, turnover=0.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=None (govt=False)
- **Result:** sector **S.13**, public/private **GG**, control **NONE**, market **NON-MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '8412'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-010` → {'market_status': 'NON-MARKET'}  _(std: GFS 2014)_
    - T8 `R-T08-001` → {'control_flag': 'NONE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-010` → {'sector_code': 'S.13'}  _(std: SNA 2025)_
    - T6 `R-T06-005` → {'public_private': 'GG'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000051 — Sample Civil Aviation Authority
- **Input:** legal_form=GOV, isic=8412, residence=RES, employment=400, turnover=50000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=None (govt=False)
- **Result:** sector **S.13**, public/private **GG**, control **NONE**, market **NON-MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '8412'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-010` → {'market_status': 'NON-MARKET'}  _(std: GFS 2014)_
    - T8 `R-T08-001` → {'control_flag': 'NONE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-010` → {'sector_code': 'S.13'}  _(std: SNA 2025)_
    - T6 `R-T06-005` → {'public_private': 'GG'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000052 — Sample Public University
- **Input:** legal_form=GOV, isic=8540, residence=RES, employment=2200, turnover=0.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=None (govt=False)
- **Result:** sector **S.13**, public/private **GG**, control **NONE**, market **NON-MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '8540'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-010` → {'market_status': 'NON-MARKET'}  _(std: GFS 2014)_
    - T8 `R-T08-001` → {'control_flag': 'NONE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-010` → {'sector_code': 'S.13'}  _(std: SNA 2025)_
    - T6 `R-T06-005` → {'public_private': 'GG'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000053 — Sample Private Commercial Bank QPSC
- **Input:** legal_form=JSC, isic=6419, residence=RES, employment=1400, turnover=6000000000.0, financial=True, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Private Banking Group (govt=False)
- **Result:** sector **S.122**, public/private **PRV-FC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6419'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-022` → {'sector_code': 'S.122'}  _(std: SNA 2025)_
    - T6 `R-T06-050` → {'public_private': 'PRV-FC'}  _(std: SNA 2025)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000054 — Sample Islamic Bank QPSC
- **Input:** legal_form=JSC, isic=6419, residence=RES, employment=1600, turnover=7000000000.0, financial=True, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=55.0%, gov_voting=55.0%, foreign_own=0.0%, gov_control=True, UCI=State of Qatar (govt=True)
- **Result:** sector **S.122**, public/private **PUB-FC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6419'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-022` → {'sector_code': 'S.122'}  _(std: SNA 2025)_
    - T6 `R-T06-010` → {'public_private': 'PUB-FC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000055 — Sample Brokerage House
- **Input:** legal_form=LLC, isic=6630, residence=RES, employment=80, turnover=80000000.0, financial=True, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Securities Holding (govt=False)
- **Result:** sector **S.126**, public/private **PRV-FC**, control **MAJ-VOTE**, market **MARKET**, size **MEDIUM**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6630'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-023` → {'sector_code': 'S.126'}  _(std: SNA 2025)_
    - T6 `R-T06-050` → {'public_private': 'PRV-FC'}  _(std: SNA 2025)_
    - T10 `R-T10-020` → {'size_class': 'MEDIUM'}  _(std: QNCS)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000056 — Sample Takaful Insurance QPSC
- **Input:** legal_form=JSC, isic=6512, residence=RES, employment=260, turnover=900000000.0, financial=True, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Insurance Investors (govt=False)
- **Result:** sector **S.128**, public/private **PRV-FC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6512'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-025` → {'sector_code': 'S.128'}  _(std: SNA 2025)_
    - T6 `R-T06-050` → {'public_private': 'PRV-FC'}  _(std: SNA 2025)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000057 — Sample Sovereign Investment Vehicle
- **Input:** legal_form=SOE, isic=6420, residence=RES, employment=140, turnover=5000000000.0, financial=True, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=100.0%, gov_voting=100.0%, foreign_own=0.0%, gov_control=True, UCI=State of Qatar (govt=True)
- **Result:** sector **S.127**, public/private **PUB-FC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **HOLDING**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6420'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-024` → {'sector_code': 'S.127'}  _(std: SNA 2025)_
    - T6 `R-T06-010` → {'public_private': 'PUB-FC'}  _(std: GFS 2014)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-020` → {'special_entity_flag': 'HOLDING'}  _(std: ISIC Rev.4 / SNA 2025)_

### QA-ENT-20260000058 — Sample Exchange & Money Transfer
- **Input:** legal_form=LLC, isic=6630, residence=RES, employment=120, turnover=120000000.0, financial=True, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Exchange Holding (govt=False)
- **Result:** sector **S.126**, public/private **PRV-FC**, control **MAJ-VOTE**, market **MARKET**, size **MEDIUM**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6630'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-023` → {'sector_code': 'S.126'}  _(std: SNA 2025)_
    - T6 `R-T06-050` → {'public_private': 'PRV-FC'}  _(std: SNA 2025)_
    - T10 `R-T10-020` → {'size_class': 'MEDIUM'}  _(std: QNCS)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000059 — Sample Real Estate Investment Trust
- **Input:** legal_form=FND, isic=6430, residence=RES, employment=25, turnover=600000000.0, financial=True, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=REIT Manager (govt=False)
- **Result:** sector **S.127**, public/private **PRV-FC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **SPV**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6430'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-024` → {'sector_code': 'S.127'}  _(std: SNA 2025)_
    - T6 `R-T06-050` → {'public_private': 'PRV-FC'}  _(std: SNA 2025)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-030` → {'special_entity_flag': 'SPV'}  _(std: SNA 2025)_

### QA-ENT-20260000060 — Sample Charitable Society
- **Input:** legal_form=CA, isic=9499, residence=RES, employment=90, turnover=2000000.0, financial=False, nonprofit=True, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=None (govt=False)
- **Result:** sector **S.15**, public/private **NPISH**, control **NONE**, market **NON-MARKET**, size **MEDIUM**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '9499'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-020` → {'market_status': 'NON-MARKET'}  _(std: SNA 2025)_
    - T8 `R-T08-001` → {'control_flag': 'NONE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-035` → {'sector_code': 'S.15'}  _(std: SNA 2025)_
    - T6 `R-T06-035` → {'public_private': 'NPISH'}  _(std: SNA 2025)_
    - T10 `R-T10-020` → {'size_class': 'MEDIUM'}  _(std: QNCS)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000061 — Sample Professional Association
- **Input:** legal_form=CA, isic=9499, residence=RES, employment=30, turnover=1000000.0, financial=False, nonprofit=True, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=None (govt=False)
- **Result:** sector **S.15**, public/private **NPISH**, control **NONE**, market **NON-MARKET**, size **SMALL**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '9499'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-020` → {'market_status': 'NON-MARKET'}  _(std: SNA 2025)_
    - T8 `R-T08-001` → {'control_flag': 'NONE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-035` → {'sector_code': 'S.15'}  _(std: SNA 2025)_
    - T6 `R-T06-035` → {'public_private': 'NPISH'}  _(std: SNA 2025)_
    - T10 `R-T10-030` → {'size_class': 'SMALL'}  _(std: QNCS)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000062 — Sample Cultural Foundation
- **Input:** legal_form=FND, isic=9101, residence=RES, employment=70, turnover=3000000.0, financial=False, nonprofit=True, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=None (govt=False)
- **Result:** sector **S.15**, public/private **NPISH**, control **NONE**, market **NON-MARKET**, size **MEDIUM**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '9101'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-020` → {'market_status': 'NON-MARKET'}  _(std: SNA 2025)_
    - T8 `R-T08-001` → {'control_flag': 'NONE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-035` → {'sector_code': 'S.15'}  _(std: SNA 2025)_
    - T6 `R-T06-035` → {'public_private': 'NPISH'}  _(std: SNA 2025)_
    - T10 `R-T10-020` → {'size_class': 'MEDIUM'}  _(std: QNCS)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000063 — Sample Sole Proprietor Garage
- **Input:** legal_form=SP, isic=4690, residence=RES, employment=4, turnover=900000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=None (govt=False)
- **Result:** sector **S.14**, public/private **PRV-NFC**, control **NONE**, market **MARKET**, size **MICRO**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '4690'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'NONE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-050` → {'sector_code': 'S.14'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-100` → {'size_class': 'MICRO'}  _(std: QNCS)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000064 — Sample Family Grocery (sole proprietor)
- **Input:** legal_form=SP, isic=4690, residence=RES, employment=2, turnover=500000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=None (govt=False)
- **Result:** sector **S.14**, public/private **PRV-NFC**, control **NONE**, market **MARKET**, size **MICRO**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '4690'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'NONE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-050` → {'sector_code': 'S.14'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-100` → {'size_class': 'MICRO'}  _(std: QNCS)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000065 — Sample Foreign Engineering Branch
- **Input:** legal_form=BR, isic=4100, residence=RES, employment=300, turnover=400000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=100.0%, gov_control=False, UCI=German Engineering AG (govt=False)
- **Result:** sector **S.11**, public/private **FCC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **INWARD-FULL**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '4100'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-040` → {'public_private': 'FCC'}  _(std: OECD BD4)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-020` → {'fdi_flag': 'INWARD-FULL'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000066 — Sample QFC Reinsurance Branch
- **Input:** legal_form=QFC, isic=6520, residence=RES, employment=60, turnover=500000000.0, financial=True, nonprofit=False, jurisdiction=QFC
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=100.0%, gov_control=False, UCI=Swiss Re Sample (govt=False)
- **Result:** sector **S.128**, public/private **FCC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **INWARD-FULL**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6520'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-025` → {'sector_code': 'S.128'}  _(std: SNA 2025)_
    - T6 `R-T06-040` → {'public_private': 'FCC'}  _(std: OECD BD4)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-020` → {'fdi_flag': 'INWARD-FULL'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000067 — Sample Free-Zone Logistics WLL
- **Input:** legal_form=FZ, isic=5210, residence=RES, employment=240, turnover=200000000.0, financial=False, nonprofit=False, jurisdiction=QFZA
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=100.0%, gov_control=False, UCI=SG Logistics Pte (govt=False)
- **Result:** sector **S.11**, public/private **FCC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **INWARD-FULL**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '5210'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-040` → {'public_private': 'FCC'}  _(std: OECD BD4)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-020` → {'fdi_flag': 'INWARD-FULL'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000068 — Sample Foreign Retail Franchise
- **Input:** legal_form=LLC, isic=4690, residence=RES, employment=180, turnover=300000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=100.0%, gov_control=False, UCI=FR Retail SA (govt=False)
- **Result:** sector **S.11**, public/private **FCC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **INWARD-FULL**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '4690'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-040` → {'public_private': 'FCC'}  _(std: OECD BD4)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-020` → {'fdi_flag': 'INWARD-FULL'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000069 — Sample MNE Oilfield Services Sub
- **Input:** legal_form=LLC, isic=0610, residence=RES, employment=520, turnover=1500000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=100.0%, gov_control=False, UCI=US Oilfield Inc (govt=False)
- **Result:** sector **S.11**, public/private **FCC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **INWARD-FULL**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '0610'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-040` → {'public_private': 'FCC'}  _(std: OECD BD4)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-020` → {'fdi_flag': 'INWARD-FULL'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000070 — Sample Construction Contracting WLL
- **Input:** legal_form=LLC, isic=4100, residence=RES, employment=600, turnover=800000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Contracting Family (govt=False)
- **Result:** sector **S.11**, public/private **PRV-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '4100'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000071 — Sample IT Services Startup
- **Input:** legal_form=LLC, isic=6201, residence=RES, employment=18, turnover=6000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Tech Founders (govt=False)
- **Result:** sector **S.11**, public/private **PRV-NFC**, control **MAJ-VOTE**, market **MARKET**, size **SMALL**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6201'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-030` → {'size_class': 'SMALL'}  _(std: QNCS)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000072 — Sample Restaurant Group
- **Input:** legal_form=LLC, isic=5610, residence=RES, employment=140, turnover=90000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Hospitality Holding (govt=False)
- **Result:** sector **S.11**, public/private **PRV-NFC**, control **MAJ-VOTE**, market **MARKET**, size **MEDIUM**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '5610'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-020` → {'size_class': 'MEDIUM'}  _(std: QNCS)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000073 — Sample Real Estate Developer (private)
- **Input:** legal_form=LLC, isic=6810, residence=RES, employment=220, turnover=700000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Property Family (govt=False)
- **Result:** sector **S.11**, public/private **PRV-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6810'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000074 — Sample Logistics SME
- **Input:** legal_form=LLC, isic=5210, residence=RES, employment=40, turnover=25000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Logistics Owner (govt=False)
- **Result:** sector **S.11**, public/private **PRV-NFC**, control **MAJ-VOTE**, market **MARKET**, size **MEDIUM**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '5210'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-020` → {'size_class': 'MEDIUM'}  _(std: QNCS)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000075 — Sample Private Hospital
- **Input:** legal_form=LLC, isic=8610, residence=RES, employment=480, turnover=600000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Healthcare Holding (govt=False)
- **Result:** sector **S.11**, public/private **PRV-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '8610'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000076 — Sample Private School Operator
- **Input:** legal_form=LLC, isic=8510, residence=RES, employment=260, turnover=120000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Education Holding (govt=False)
- **Result:** sector **S.11**, public/private **PRV-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '8510'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000077 — Sample Micro Bakery
- **Input:** legal_form=LLC, isic=5610, residence=RES, employment=6, turnover=1100000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Local Owner (govt=False)
- **Result:** sector **S.11**, public/private **PRV-NFC**, control **MAJ-VOTE**, market **MARKET**, size **MICRO**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '5610'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-100` → {'size_class': 'MICRO'}  _(std: QNCS)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000078 — Sample Large Trading Conglomerate
- **Input:** legal_form=JSC, isic=4690, residence=RES, employment=2200, turnover=3000000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Founding Family Group (govt=False)
- **Result:** sector **S.11**, public/private **PRV-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '4690'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

### QA-ENT-20260000079 — Sample Holding Company (private)
- **Input:** legal_form=LLC, isic=6420, residence=RES, employment=15, turnover=200000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Ultimate Family Unit (govt=False)
- **Result:** sector **S.11**, public/private **PRV-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **HOLDING**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6420'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-020` → {'special_entity_flag': 'HOLDING'}  _(std: ISIC Rev.4 / SNA 2025)_

### QA-ENT-20260000080 — Sample Foodstuff & General Trading W.L.L.
- **Input:** legal_form=LLC, isic=6420, residence=RES, employment=12, turnover=300000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=0.0%, gov_voting=0.0%, foreign_own=0.0%, gov_control=False, UCI=Founding family (govt=False)
- **Result:** sector **S.11**, public/private **PRV-NFC**, control **MAJ-VOTE**, market **MARKET**, size **LARGE**, FDI **NONE**, special **HOLDING**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '6420'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'MAJ-VOTE'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-100` → {'public_private': 'PRV-NFC'}  _(std: SNA 2025)_
    - T10 `R-T10-010` → {'size_class': 'LARGE'}  _(std: QNCS / EU 2003/361/EC)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-020` → {'special_entity_flag': 'HOLDING'}  _(std: ISIC Rev.4 / SNA 2025)_

### QA-ENT-20260000099 — Sample Trading Co (sample)
- **Input:** legal_form=LLC, isic=4690, residence=RES, employment=85, turnover=40000000.0, financial=False, nonprofit=False, jurisdiction=MAINLAND
- **Ownership intelligence:** gov_own=60.0%, gov_voting=60.0%, foreign_own=0.0%, gov_control=True, UCI=State Holding Company A (govt=True)
- **Result:** sector **S.11**, public/private **PUB-NFC**, control **BO-CHAIN**, market **MARKET**, size **MEDIUM**, FDI **NONE**, special **NONE**; confidence **1.0**
- **Rules applied:**
    - T3 `R-T03-001` → {'residence': 'RES'}  _(std: SNA 2025 / BPM6 Ch.4)_
    - T4 `R-T04-001` → {'isic_class': '4690'}  _(std: ISIC Rev.4)_
    - T7 `R-T07-030` → {'market_status': 'MARKET'}  _(std: SNA 2025 — 50% rule)_
    - T8 `R-T08-001` → {'control_flag': 'BO-CHAIN'}  _(std: SNA 2025 / OECD BD4)_
    - T5 `R-T05-100` → {'sector_code': 'S.11'}  _(std: SNA 2025)_
    - T6 `R-T06-020` → {'public_private': 'PUB-NFC'}  _(std: GFS 2014)_
    - T10 `R-T10-020` → {'size_class': 'MEDIUM'}  _(std: QNCS)_
    - T12 `R-T12-100` → {'fdi_flag': 'NONE'}  _(std: OECD BD4)_
    - T13 `R-T13-100` → {'special_entity_flag': 'NONE'}  _(std: SNA 2025)_

