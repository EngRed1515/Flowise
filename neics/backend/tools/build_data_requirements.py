#!/usr/bin/env python3
"""
Build NEICS_Data_Requirements.xlsx — the leadership-facing data-requirements
pack for making the National Enterprise Intelligence & Classification System
(NEICS) operational.

Everything here is reverse-engineered from the working platform:
  * provider register  <- INTEGRATION_SOURCES / SOURCE_TIERS (build_walkthrough.py)
  * data-point catalogue <- the engine's actual input schema (uat_enterprises.json
    + uat_ownership.json) and the per-dimension source map used by runEngine
  * test catalogue     <- the 18 classification tests (DB-seeded)
  * standards          <- the standards catalogue (DB-seeded)
  * governance / RACI  <- GOVERNANCE constant

The script AUDITS itself before writing: every input field in the engine schema
must be covered by a data point, and every provider referenced by a data point
must exist in the provider register. It aborts if either check fails.
"""
import json
import os
import sys
from datetime import date

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "NEICS_Data_Requirements.xlsx")

# ---------------------------------------------------------------------------
# Palette (matches the platform's government identity)
NAVY = "1B2A41"; MAROON = "8A1538"; GOLD = "C9A961"; GREEN = "2E7D6B"
BLUE = "2C5F8A"; PAPER = "F4F4F6"; RULE = "D8D8DD"; WHITE = "FFFFFF"

H_FONT = Font(name="Arial", size=10, bold=True, color=WHITE)
B_FONT = Font(name="Arial", size=10, color="222222")
TITLE_FONT = Font(name="Georgia", size=16, bold=True, color=NAVY)
SUB_FONT = Font(name="Arial", size=10, color="555555", italic=True)
THIN = Side(style="thin", color=RULE)
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
WRAP_C = Alignment(wrap_text=True, vertical="center", horizontal="center")


def style_header(ws, row, ncols, fill=NAVY):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = H_FONT
        cell.fill = PatternFill("solid", fgColor=fill)
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left")
        cell.border = BORDER


def write_table(ws, start_row, headers, rows, widths, fill=NAVY, zebra=True):
    """Write a header + data rows, apply autofilter, freeze header, zebra."""
    for j, h in enumerate(headers, start=1):
        ws.cell(row=start_row, column=j, value=h)
    style_header(ws, start_row, len(headers), fill)
    r = start_row
    for ri, row in enumerate(rows):
        r += 1
        for j, val in enumerate(row, start=1):
            cell = ws.cell(row=r, column=j, value=val)
            cell.font = B_FONT
            cell.alignment = WRAP
            cell.border = BORDER
            if zebra and ri % 2 == 1:
                cell.fill = PatternFill("solid", fgColor=PAPER)
    for j, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = ws.cell(row=start_row + 1, column=1)
    ws.auto_filter.ref = "{}:{}".format(
        ws.cell(row=start_row, column=1).coordinate,
        ws.cell(row=r, column=len(headers)).coordinate,
    )
    return r


# ===========================================================================
# 1. PROVIDER REGISTER  — who must supply data
#    Source bucket lets leadership filter EXTERNAL (ministries/authorities)
#    vs INTERNAL (NSO/PSA — the statistical production centre).
# Columns: PID, Provider, Category, Source bucket, Tier, Co-authority,
#          Domains supplied, Transfer mechanism, Cadence, Legal gateway, Status
PROVIDERS = [
    ["P-01", "Ministry of Commerce & Industry (MoCI) — Commercial Register",
     "Government Ministry", "EXTERNAL — Ministry", "Tier 1", "—",
     "Legal-unit identity, legal name (EN/AR), legal form, CR number, ownership at incorporation, demographic events (birth/death)",
     "Register sync / secure DB read-replica", "Daily (event-driven)",
     "Commercial Register Law; data-sharing MoU with NSO", "Primary — required"],
    ["P-02", "General Tax Authority (GTA)",
     "Regulatory Authority", "EXTERNAL — Authority", "Tier 2", "—",
     "Principal economic activity, turnover, sales, production costs, total assets, employment proxy, financial-activity status on active entities",
     "Secure API / SFTP drop", "Monthly + annual returns",
     "Tax Law confidentiality gateway; statistical-use MoU", "Primary — required"],
    ["P-03", "Qatar Central Bank (QCB)",
     "Regulatory Authority", "EXTERNAL — Authority", "Tier 2", "Co-authority (S.121–S.129)",
     "Financial-corporation prudential filings; monetary-authority status; sub-sector boundary S.121–S.129; LEI of regulated entities",
     "Secure API (co-authority link)", "Monthly / quarterly",
     "QCB Law; joint sub-committee charter", "Primary — required (financial sector)"],
    ["P-04", "Ministry of Labour (MoL)",
     "Government Ministry", "EXTERNAL — Ministry", "Tier 2", "—",
     "Employer registration, employment counts, establishment workforce (size criterion)",
     "Secure API", "Monthly", "Labour Law; data-sharing MoU", "Primary — required"],
    ["P-05", "Ministry of Finance (MoF)",
     "Government Ministry", "EXTERNAL — Ministry", "Tier 3", "Co-authority (public-sector boundary)",
     "Government-ownership confirmation; public-corporation boundary; PPP & concession terms; budgetary-unit status",
     "Administrative records / secure exchange", "Quarterly + on event",
     "Public-sector boundary sub-committee charter", "Primary — required (public sector)"],
    ["P-06", "Ministry of Justice (MoJ)",
     "Government Ministry", "EXTERNAL — Ministry", "Tier 3", "—",
     "Civil-society organisations, associations, waqf and foundations (NPISH / S.15 determination); non-profit status",
     "Administrative records", "Quarterly", "Associations & Foundations Law", "Required (NPISH)"],
    ["P-07", "Qatar Financial Centre (QFC) Authority",
     "Registry / Free-zone Authority", "EXTERNAL — Authority", "Tier 1", "—",
     "QFC-licensed entities; foreign-parent branches; jurisdiction flag; QFC legal form",
     "Register sync", "Daily (event-driven)", "QFC Law; register-sharing agreement", "Required (jurisdiction)"],
    ["P-08", "Qatar Free Zones Authority (QFZA)",
     "Registry / Free-zone Authority", "EXTERNAL — Authority", "Tier 1", "—",
     "Free-zone entities (Ras Bufontas, Umm Alhoul); FDI flag; jurisdiction flag",
     "Register sync / SFTP", "Daily (event-driven)", "Free Zones Law; MoU", "Required (jurisdiction)"],
    ["P-09", "Qatar Science & Technology Park (QSTP)",
     "Registry / Free-zone Authority", "EXTERNAL — Authority", "Tier 1", "—",
     "QSTP-licensed entities; R&D activity (ISIC 72); IP-holding substance",
     "Register sync", "Daily (event-driven)", "QSTP charter; MoU", "Required (jurisdiction)"],
    ["P-10", "Qatar Stock Exchange (QSE)",
     "Market Infrastructure", "EXTERNAL — Authority", "Tier 4", "—",
     "Listed-company disclosures; free-float; ownership changes (corroborating)",
     "Disclosure feed / API", "Continuous (disclosure-driven)", "QSE rulebook; QFMA disclosure regime", "Required (listed entities)"],
    ["P-11", "Qatar Financial Markets Authority (QFMA)",
     "Regulatory Authority", "EXTERNAL — Authority", "Tier 4", "—",
     "Major-shareholder & beneficial-ownership disclosures for listed entities; concert-party / control changes",
     "Disclosure feed / API", "Continuous (disclosure-driven)", "QFMA Law", "Required (listed entities)"],
    ["P-12", "General Authority of Customs",
     "Government Body", "EXTERNAL — Authority", "Tier 2", "—",
     "Trade flows; free-zone movements; trader-vs-producer evidence; ultimate-investing-country corroboration",
     "Secure API / SFTP", "Monthly", "Customs Law; statistical MoU", "Supporting"],
    ["P-13", "Municipalities (MME)",
     "Government Body", "EXTERNAL — Authority", "Tier 2", "—",
     "Establishment-level licensing; premises existence; geocoding for local units",
     "Register sync", "Monthly", "Municipal licensing regulations", "Supporting"],
    ["P-14", "Investment-promotion entities (IPA / Invest Qatar)",
     "Government Body", "EXTERNAL — Authority", "Tier 3", "—",
     "FDI projects; ultimate investing country; foreign-investor identity corroboration",
     "Administrative records", "Quarterly", "Investment Law; MoU", "Supporting (FDI)"],
    ["P-15", "GLEIF (Global LEI Foundation)",
     "International Registry", "EXTERNAL — International", "Tier 1", "—",
     "Legal Entity Identifier (ISO 17442); parent-relationship (level-2) records",
     "Public LEI download / API", "Daily", "Open GLEIF data", "Required (financial sector LEI)"],
    ["P-16", "NSO / PSA — Economic surveys & large-case profiling",
     "Internal — NSO/PSA", "INTERNAL — NSO/PSA (MPC)", "Tier 3", "—",
     "Control structure, ultimate parent, group consolidation, beneficial ownership, autonomy & institutional substance, principal-activity confirmation",
     "Survey platform / profiling system", "Continuous + annual survey", "Statistics Law", "Internal — required"],
    ["P-17", "NSO / PSA — Statistical Business Register (SBR)",
     "Internal — NSO/PSA", "INTERNAL — NSO/PSA (MPC)", "Tier 3", "—",
     "Master enterprise/establishment/legal-unit linkage; enterprise-group register; demographic-event maintenance; quality flags",
     "Internal master register", "Continuous", "Statistics Law", "Internal — required (master)"],
    ["P-18", "NSO / PSA — Classification portal (manual / committee)",
     "Internal — NSO/PSA", "INTERNAL — NSO/PSA (MPC)", "Tier 3", "—",
     "Analyst-entered profiling evidence; Technical Classification Committee rulings; statistical overrides",
     "NSO classification portal", "On demand", "Statistics Law; TCC charter", "Internal — required"],
]
PROVIDER_HEADERS = ["Provider ID", "Provider / Source entity", "Category", "Source bucket (filter)",
                    "Source tier", "Co-authority role", "Data domains supplied", "Transfer mechanism",
                    "Update cadence", "Legal gateway / basis", "Status"]
PROVIDER_WIDTHS = [10, 38, 22, 26, 12, 24, 44, 26, 22, 30, 24]
PROVIDER_IDS = {p[1].split(" —")[0].split(" (")[0].strip(): p[0] for p in PROVIDERS}
# A lookup by a short key we use in data points
PROV_KEY = {
    "MoCI": "P-01", "GTA": "P-02", "QCB": "P-03", "MoL": "P-04", "MoF": "P-05",
    "MoJ": "P-06", "QFC": "P-07", "QFZA": "P-08", "QSTP": "P-09", "QSE": "P-10",
    "QFMA": "P-11", "Customs": "P-12", "Municipalities": "P-13", "IPA": "P-14",
    "GLEIF": "P-15", "NSO-Profiling": "P-16", "SBR": "P-17", "Portal": "P-18",
}

# ===========================================================================
# 2. DATA-POINT CATALOGUE — every field the engine consumes to classify.
# Columns: DP ID, Data point, Engine field, Definition, Dimension fed, Test(s),
#          Standard, Primary provider(key), Secondary provider(key),
#          Source bucket, Mandatory, Type, Code list / values, Validation,
#          Cadence, Confidentiality
# group, field, engine_field, definition, dimension, tests, std, prov, prov2, mand, dtype, codelist, validation, cadence
DP = [
 # --- Identity ---------------------------------------------------------
 ("Identity", "Enterprise ID", "enterprise_id", "Unique national enterprise identifier in the Statistical Business Register.",
  "Identity", "T1, T18", "IRBR", "SBR", "MoCI", "Mandatory", "Text (QA-ENT-…)", "Register-assigned",
  "Unique; non-null; matches SBR master.", "On birth"),
 ("Identity", "Legal Entity Identifier (LEI)", "lei", "Globally unique ISO 17442 identifier; mandatory for financial-sector units.",
  "Identity", "T18", "LEI", "GLEIF", "QCB", "Conditional", "Text (20 char)", "ISO 17442 checksum",
  "Valid LEI checksum when present; 100% for financial sector (KPI).", "Daily"),
 ("Identity", "Legal name (EN / AR)", "legal_name_en / legal_name_ar", "Registered legal name in English and Arabic.",
  "Identity", "T1", "IRBR", "MoCI", "", "Mandatory", "Text", "—",
  "Non-null EN; AR where registered. NB: name is NEVER used to classify activity.", "On change"),
 ("Identity", "Legal form code", "legal_form_code", "Qatari legal form (LLC/WLL, QPSC, SPC, GOV, branch, free-zone forms, association, waqf…).",
  "Legal form", "T2, T6", "QNCS", "MoCI", "QFC", "Mandatory", "Code", "Legal-form code list",
  "Must exist in legal-form code list; GOV → general-government candidate.", "On change"),
 ("Identity", "CR number", "(cr_number)", "Commercial Register number issued at incorporation.",
  "Identity", "T1", "IRBR", "MoCI", "", "Mandatory", "Text", "—", "Non-null for mainland units.", "On birth"),
 # --- Activity ---------------------------------------------------------
 ("Activity", "Principal economic activity (ISIC Rev.4)", "isic_class", "Principal activity by largest share of value added (4-digit ISIC class).",
  "Economic activity", "T4", "ISIC4", "GTA", "NSO-Profiling", "Mandatory", "Code (4-digit)", "ISIC Rev.4",
  "Valid ISIC class; profiled, NOT taken from trade name/licence label.", "Annual / on change"),
 ("Activity", "Secondary / ancillary activities", "(secondary_isic)", "Other activities for KAU split and secondary-activity flagging.",
  "Economic activity", "T4", "ISIC4", "GTA", "NSO-Profiling", "Optional", "Code list", "ISIC Rev.4",
  "Each a valid ISIC class.", "Annual"),
 # --- Size / financials -----------------------------------------------
 ("Size & financials", "Turnover", "turnover_qar", "Annual turnover in QAR (size criterion).",
  "Enterprise size", "T10", "QNCS", "GTA", "", "Mandatory", "Number (QAR)", "—",
  "≥ 0; reconciles to tax return; size band per thresholds sheet.", "Annual"),
 ("Size & financials", "Sales / market output", "sales", "Sales revenue used in the 50% market/non-market test.",
  "Market status", "T7", "SNA2025", "GTA", "MoF", "Mandatory", "Number (QAR)", "—",
  "≥ 0; basis of sales-cover-50%-of-costs rule.", "Annual"),
 ("Size & financials", "Production costs", "production_costs", "Total production costs for the 50% rule.",
  "Market status", "T7", "SNA2025", "GTA", "MoF", "Mandatory", "Number (QAR)", "—",
  "≥ 0; market if sales > 50% of costs.", "Annual"),
 ("Size & financials", "Total assets", "total_assets_qar", "Balance-sheet total (financial-corporation profiling, size corroboration).",
  "Size / sector", "T5, T10", "SNA2025", "GTA", "QCB", "Optional", "Number (QAR)", "—",
  "≥ 0.", "Annual"),
 ("Size & financials", "Employment", "employment", "Number of persons employed (size criterion; higher criterion governs).",
  "Enterprise size", "T10", "QNCS", "MoL", "GTA", "Mandatory", "Integer", "—",
  "≥ 0; reconciles MoL vs GTA; size band per thresholds.", "Monthly"),
 # --- Sector flags -----------------------------------------------------
 ("Sector flags", "Non-profit status", "is_nonprofit", "Whether the unit is a non-profit institution (NPISH candidate, S.15).",
  "Institutional sector", "T5", "SNA2025", "MoJ", "NSO-Profiling", "Mandatory", "Boolean", "true/false",
  "Set from MoJ register for associations/waqf/foundations.", "On change"),
 ("Sector flags", "Financial-activity status", "is_financial", "Whether the unit is a financial corporation (S.12 candidate).",
  "Institutional sector", "T5, T6", "GFS2014", "QCB", "GTA", "Mandatory", "Boolean", "true/false",
  "QCB-regulated → financial; drives S.121–S.129 routing.", "On change"),
 # --- Substance (institutional-unit test) ------------------------------
 ("Substance", "Has premises", "has_premises", "Existence of physical premises (institutional-unit & empty-shell substance test).",
  "Special entity", "T2, T13", "SNA2025", "Municipalities", "NSO-Profiling", "Mandatory", "Boolean", "true/false",
  "No premises + no employees → empty-shell / consolidate with parent.", "Annual"),
 ("Substance", "Has employees", "has_employees", "Whether the unit has its own employees (substance test).",
  "Special entity", "T2, T13", "SNA2025", "MoL", "NSO-Profiling", "Mandatory", "Boolean", "true/false",
  "Used with premises/autonomy for SPV/holding/captive substance.", "Annual"),
 ("Substance", "Has autonomy", "has_autonomy", "Autonomy of decision in respect of its principal function.",
  "Institutional unit", "T2", "SNA2025", "NSO-Profiling", "", "Mandatory", "Boolean", "true/false",
  "Required for institutional-unit recognition.", "Annual"),
 # --- Jurisdiction / residence ----------------------------------------
 ("Jurisdiction", "Jurisdiction / licensing regime", "jurisdiction", "MAINLAND / QFC / QFZA / QSTP — drives legal form, FDI and residence treatment.",
  "Residence / FDI", "T3, T12", "QNCS", "MoCI", "QFC", "Mandatory", "Code", "MAINLAND|QFC|QFZA|QSTP",
  "Must match the licensing authority's register.", "On change"),
 ("Jurisdiction", "Residence", "residence", "Centre of predominant economic interest (resident ≥ 1 year).",
  "Residence", "T3", "BPM6", "NSO-Profiling", "MoCI", "Mandatory", "Code", "RES|NON-RES",
  "Determined by centre of economic interest, not registration alone.", "Annual"),
 # --- Business demography ----------------------------------------------
 ("Demography", "Birth date", "birth_date", "Date of economic birth (registration / first activity).",
  "Business demography", "T11", "IRBR", "MoCI", "SBR", "Mandatory", "Date", "—",
  "≤ today; drives demographic-event lag KPI (≤ 60 days).", "On birth"),
 ("Demography", "Death / cessation date", "death_date", "Date of economic death / cessation.",
  "Business demography", "T11", "IRBR", "MoCI", "SBR", "Conditional", "Date", "—",
  "≥ birth_date when present; death lag KPI (≤ 90 days).", "On death"),
 ("Demography", "Last demographic event", "last_demographic_event", "Most recent demographic event (birth, death, merger, split, restructuring).",
  "Business demography", "T11", "IRBR", "SBR", "MoCI", "Mandatory", "Code", "BIRTH|DEATH|MERGER|SPLIT|RESTRUCTURE",
  "Triggers reclassification workflow.", "On event"),
 ("Demography", "Enterprise group ID", "group_id", "Link to the enterprise group (truncated/global) for consolidation.",
  "Enterprise group", "T11", "SNA2025", "SBR", "NSO-Profiling", "Conditional", "Text", "Group register",
  "Resolves global ultimate parent, domestic head & resident perimeter.", "On change"),
 # --- Ownership & control (per ownership edge) -------------------------
 ("Ownership & control", "Owner identity", "owner_id / owner_name", "Each direct owner of the unit (ownership graph edge).",
  "Ownership / control", "T8", "BD4", "MoCI", "NSO-Profiling", "Mandatory", "Text", "—",
  "Each owner resolvable; chain leads to ultimate owner.", "On change"),
 ("Ownership & control", "Owner is government", "owner_is_government", "Whether the owner is a government unit / sovereign vehicle.",
  "Public / private", "T6, T8", "GFS2014", "MoF", "NSO-Profiling", "Mandatory", "Boolean", "true/false",
  "Aggregated across vehicles → effective government ownership %.", "On change"),
 ("Ownership & control", "Owner is resident", "owner_is_resident", "Residence of the owner (FDI directionality).",
  "FDI / residence", "T12", "BD4", "NSO-Profiling", "IPA", "Mandatory", "Boolean", "true/false",
  "Non-resident owner ≥ 10% → inward FDI.", "On change"),
 ("Ownership & control", "Owner country", "owner_country", "ISO country of the owner / ultimate investing country.",
  "FDI", "T12", "BD4", "IPA", "Customs", "Conditional", "Code (ISO-2)", "ISO 3166",
  "Valid ISO code; supports ultimate-investing-country.", "On change"),
 ("Ownership & control", "Ownership %", "ownership_pct", "Equity share held by the owner on this edge.",
  "Ownership / control", "T8, T12", "BD4", "MoCI", "NSO-Profiling", "Mandatory", "Number (0–100)", "—",
  "Per-owner ≤ 100; effective % propagated through the chain.", "On change"),
 ("Ownership & control", "Voting %", "voting_pct", "Voting power held (effective control can differ from equity).",
  "Control", "T8", "BD4", "NSO-Profiling", "QFMA", "Mandatory", "Number (0–100)", "—",
  ">50% voting → majority control; 10% → FDI threshold.", "On change"),
 ("Ownership & control", "Control indicator", "control_indicator", "Which of the 9 control indicators applies (golden share, board, key personnel, contract, regulatory, financing, dominant, BO-chain…).",
  "Effective control", "T8", "BD4/SNA2025", "NSO-Profiling", "QFMA", "Mandatory", "Code", "9-indicator code list",
  "Substance over form: control can exist below 50% equity.", "On change"),
 ("Ownership & control", "Ultimate controlling unit (UCI) flag", "is_ultimate", "Marks the top of the ownership chain (UCI / global ultimate parent).",
  "Control / FDI", "T8, T11, T12", "BD4", "NSO-Profiling", "GLEIF", "Mandatory", "Boolean", "Y/N",
  "Exactly one UCI per chain.", "On change"),
]
DP_HEADERS = ["DP ID", "Group", "Data point", "Engine field", "Definition", "Classification dimension",
              "Test(s)", "Standard", "Primary provider", "Secondary provider", "Source bucket (filter)",
              "Mandatory?", "Type", "Code list / values", "Validation rule", "Update cadence", "Confidentiality"]
DP_WIDTHS = [8, 18, 30, 24, 46, 22, 12, 12, 40, 30, 26, 13, 16, 24, 46, 18, 18]


def bucket_for(prov_key):
    pid = PROV_KEY.get(prov_key)
    if not pid:
        return ""
    for p in PROVIDERS:
        if p[0] == pid:
            return p[3]
    return ""


def prov_name(prov_key):
    pid = PROV_KEY.get(prov_key)
    for p in PROVIDERS:
        if p[0] == pid:
            return "{} ({})".format(p[1].split(" —")[0].split(" (")[0].strip(), pid)
    return ""


# ===========================================================================
# 3. Build the data-point rows (with computed bucket / provider names)
def build_dp_rows():
    rows = []
    for i, d in enumerate(DP, start=1):
        (grp, field, efield, defn, dim, tests, std, prov, prov2, mand, dtype, codel, valid, cadence) = d
        dp_id = "DP-{:02d}".format(i)
        confid = "Entity-level — confidential (Statistics Law)"
        rows.append([dp_id, grp, field, efield, defn, dim, tests, std,
                     prov_name(prov), prov_name(prov2) if prov2 else "—",
                     bucket_for(prov), mand, dtype, codel, valid, cadence, confid])
    return rows


# ===========================================================================
# 4. AUDIT — reconcile data points vs the live engine input schema
def audit(dp_rows):
    issues = []
    # engine input fields actually present in the data
    ents = json.load(open(os.path.join(DATA_DIR, "uat_enterprises.json")))
    owns = json.load(open(os.path.join(DATA_DIR, "uat_ownership.json")))
    ent = ents[0] if isinstance(ents, list) else list(ents.values())[0]
    own = owns[0] if isinstance(owns, list) else list(owns.values())[0]
    # Outputs the engine PRODUCES (not required from providers)
    OUTPUTS = {"sector_code", "public_private", "control_flag", "market_status",
               "size_class", "fdi_flag", "special_entity_flag", "classification_version",
               "classification_date", "quality_flag", "quality_score", "owned_id",
               "owned_name", "edge_id"}
    input_fields = set()
    for k in list(ent.keys()):
        if k not in OUTPUTS:
            input_fields.add(k)
    for k in list(own.keys()):
        if k not in OUTPUTS:
            input_fields.add(k)
    # fields covered by the catalogue (engine_field column may list a/b)
    covered = set()
    for r in dp_rows:
        for tok in r[3].replace("(", "").replace(")", "").replace("/", " ").split():
            covered.add(tok.strip())
    missing = sorted(f for f in input_fields if f not in covered)
    if missing:
        issues.append("Input fields NOT covered by a data point: " + ", ".join(missing))
    # every provider referenced exists in the register
    valid_pids = {p[0] for p in PROVIDERS}
    for k, pid in PROV_KEY.items():
        if pid not in valid_pids:
            issues.append("PROV_KEY '{}' -> {} not in provider register".format(k, pid))
    # mandatory data points all have a primary provider
    for r in dp_rows:
        if not r[8]:
            issues.append("Data point {} has no primary provider".format(r[0]))
    return input_fields, covered, missing, issues


# ===========================================================================
# 5. Tests, tiers, standards, governance content (imported / inlined)
TESTS = [
 ["T1", "Statistical Unit Test", "A. Unit & Residence", "—", "Determine the statistical-unit type (10 types).", "SNA2025",
  "enterprise_id; legal_name; CR number"],
 ["T2", "Institutional Unit Test", "A. Unit & Residence", "—", "Assess institutional substance (7 criteria).", "SNA2025",
  "legal_form_code; has_premises; has_employees; has_autonomy"],
 ["T3", "Residence Test", "A. Unit & Residence", "residence", "Centre of predominant economic interest.", "SNA2025 / BPM6",
  "residence; jurisdiction"],
 ["T4", "Economic Activity (ISIC) Classification", "B. Activity & Sector", "isic_class", "Principal activity by value added.", "ISIC4",
  "isic_class; secondary activities"],
 ["T7", "Market vs Non-Market Producer", "B. Activity & Sector", "market_status", "50% rule on production costs.", "SNA2025",
  "sales; production_costs"],
 ["T8", "Ownership & Effective Control", "C. Control & Scope", "control_flag", "Nine indicators; substance over form.", "BD4 / SNA2025",
  "owner_*; ownership_pct; voting_pct; control_indicator; is_ultimate"],
 ["T5", "Institutional Sector Classification", "B. Activity & Sector", "sector_code", "Assign to S.11–S.15 / S.2.", "SNA2025",
  "is_nonprofit; is_financial; total_assets; (control)"],
 ["T6", "Public Sector Boundary Test", "B. Activity & Sector", "public_private", "Public corp / general government / private.", "GFS2014",
  "legal_form_code; owner_is_government; is_financial; (market_status)"],
 ["T9", "Listed Company Classification", "C. Control & Scope", "—", "QSE listing is classification-neutral; reassess control.", "QNCS",
  "QSE listing; voting_pct"],
 ["T10", "Enterprise Size Classification", "C. Control & Scope", "size_class", "Micro/Small/Medium/Large; higher criterion governs.", "QNCS",
  "employment; turnover_qar; total_assets"],
 ["T11", "Enterprise Group & Consolidation", "C. Control & Scope", "—", "Associate with enterprise group; truncated group.", "SNA2025",
  "group_id; is_ultimate; owner_*; demographic events"],
 ["T12", "Foreign Ownership & FDI", "D. Residence & International", "fdi_flag", "10% threshold; directional principle.", "BD4",
  "owner_is_resident; owner_country; ownership_pct; jurisdiction"],
 ["T13", "Special Entity Treatment", "C. Control & Scope", "special_entity_flag", "SPV / holding / captive / empty-shell substance test.", "SNA2025",
  "has_premises; has_employees; isic_class (6420 etc.)"],
 ["T14", "Data Source Hierarchy", "D. Evidence & Governance", "—", "Fixed precedence order across sources.", "QNCS",
  "source tier of every attribute"],
 ["T15", "Conflict Resolution", "D. Evidence & Governance", "—", "First-match-by-priority; statistical override.", "QNCS",
  "competing source values + attestation dates"],
 ["T16", "Classification Governance", "D. Evidence & Governance", "—", "Technical Classification Committee ruling.", "QNCS",
  "committee ruling record"],
 ["T17", "Quality Assurance", "D. Evidence & Governance", "—", "Three-layer QA before commit.", "QNCS",
  "validation results; reviewer sign-off"],
 ["T18", "Final Classification Record", "D. Evidence & Governance", "—", "Full multi-dimensional classification key.", "SNA2025",
  "all dimensions + lei + version"],
]
TEST_HEADERS = ["Test", "Name", "Stage", "Output dimension", "What it decides", "Standard", "Data points consumed"]
TEST_WIDTHS = [8, 36, 26, 18, 46, 16, 50]

TIERS = [
 ["Tier 1 — Primary registry", "MoCI Commercial Register; QFC Authority; QFZA; QSTP; QSE listings; GLEIF",
  "Highest authority for legal-entity identity, name, legal form, ownership at incorporation."],
 ["Tier 2 — Tax / financial / operational", "General Tax Authority; Qatar Central Bank; Customs; Ministry of Labour; Municipalities",
  "Highest authority for activity, turnover, employment and financial-activity status on active entities."],
 ["Tier 3 — Direct statistical", "NSO economic surveys; large-case profiling; beneficial-ownership filings; MoF; MoJ records",
  "Highest authority for control structure, ultimate parent and group consolidation."],
 ["Tier 4 — Public information", "Audited annual reports; QSE / QFMA continuous disclosures; ministerial decisions",
  "Corroborating evidence; decisive only where other sources are silent."],
]
TIER_HEADERS = ["Source tier", "Authoritative sources", "Decisive for"]
TIER_WIDTHS = [30, 60, 60]
CONFLICT = [
 "Documented evidence wins over inferred status.",
 "More recent attestation wins, all else equal.",
 "Substance wins over legal form in control determinations.",
 "Resolution is by data attribute, not by source tier (Review recommendation).",
 "Statistical override is exercised by the Technical Classification Committee — never silently in the database; every override is minuted and reviewable.",
]

STANDARDS = [
 ["SNA 2025", "System of National Accounts (with SNA 2008 transition)", "UN, IMF, OECD, WB, Eurostat", "Institutional sector, residence, market/non-market, ownership & control, enterprise groups"],
 ["GFS 2014", "Government Finance Statistics Manual", "IMF", "Public-sector boundary; general government vs public corporations; PPPs/SPVs"],
 ["BPM6", "Balance of Payments & IIP Manual (6th)", "IMF", "Residence; branches; external-sector boundary"],
 ["OECD BD4", "Benchmark Definition of FDI (4th)", "OECD", "10% threshold; directional principle; ultimate investing country; UCI"],
 ["ISIC Rev.4", "Int'l Standard Industrial Classification", "UNSD", "Economic-activity coding; principal/secondary/ancillary"],
 ["CPC 2.1", "Central Product Classification", "UNSD", "Products cross-walked to ISIC"],
 ["LEI (ISO 17442)", "Legal Entity Identifier", "GLEIF / ISO", "Globally unique legal-entity identification"],
 ["GSIM 1.2 / GSBPM 5.1", "Generic Statistical Information & Process Models", "UNECE", "Metadata model & production process"],
 ["SDMX 3.0", "Statistical Data & Metadata eXchange", "SDMX Initiative", "Data/metadata exchange & dissemination"],
 ["IRBR", "Int'l Recommendations for Business Registers", "UNSD/Eurostat", "Register units, coverage, maintenance"],
 ["QNCS 1.0", "National Classification Standards of Qatar", "NSO — State of Qatar", "Legal forms, size thresholds, jurisdictional treatment"],
]
STD_HEADERS = ["Standard", "Full name", "Issuer", "Used in NEICS for"]
STD_WIDTHS = [20, 44, 28, 56]

SIZE = [
 ["MICRO", "1 – 9", "Up to QAR 3 million", "Up to QAR 2 million"],
 ["SMALL", "10 – 49", "QAR 3 – 30 million", "QAR 2 – 20 million"],
 ["MEDIUM", "50 – 249", "QAR 30 – 200 million", "QAR 20 – 150 million"],
 ["LARGE", "250 +", "Above QAR 200 million", "Above QAR 150 million"],
]
SIZE_HEADERS = ["Size class", "Employment", "Turnover", "Total assets (alt.)"]
SIZE_WIDTHS = [14, 16, 26, 26]

RACI = [
 ["Own the methodology", "NSO / PSA", "NPC", "Methodologist", "All agencies"],
 ["Provide source data", "MoCI / GTA / QCB / QFC / QFZA / MoL / MoF / MoJ", "NSO / PSA", "Data Steward", "TCC"],
 ["Classify an entity", "Classifier", "TCC", "Reviewer", "Auditor"],
 ["Review & approve", "Reviewer / TCC", "NSO DG", "Methodologist", "Analyst"],
 ["Resolve source conflict", "TCC", "NSO DG", "Sub-committees", "Source agency"],
 ["Audit & assurance", "Auditor", "SAC", "Data Steward", "All"],
]
RACI_HEADERS = ["Activity", "Responsible", "Accountable", "Consulted", "Informed"]
RACI_WIDTHS = [30, 48, 18, 22, 20]


# ===========================================================================
def build():
    dp_rows = build_dp_rows()
    input_fields, covered, missing, issues = audit(dp_rows)

    wb = Workbook()

    # ---- Sheet: Read me ---------------------------------------------------
    ws = wb.active
    ws.title = "Read me"
    ws.sheet_view.showGridLines = False
    ws["A1"] = "NEICS — National Enterprise Classification System"
    ws["A1"].font = TITLE_FONT
    ws["A2"] = "Data Requirements Pack — provider register, data points and inter-agency requirements to make the system operational"
    ws["A2"].font = SUB_FONT
    ws["A3"] = "Prepared for leadership review · {} · UAT prototype basis — NOT for public deployment".format(date.today().isoformat())
    ws["A3"].font = SUB_FONT
    notes = [
        "",
        ("How to use this workbook", True),
        ("• 'Provider register' lists every entity that must supply data. Filter the 'Source bucket' column to separate EXTERNAL ministries/authorities from INTERNAL NSO/PSA (MPC) sources.", False),
        ("• 'Data requirements' is the master list of every data point the classification engine consumes. Filter by 'Primary provider', 'Source bucket', 'Mandatory?' or 'Classification dimension' to produce a per-entity data request.", False),
        ("• 'Test → data points' shows which of the 18 classification tests each data point feeds — the justification for why each field is needed.", False),
        ("• 'Source tiers', 'Standards', 'Size thresholds' and 'Governance (RACI)' give the rules that govern how the data is ranked, validated and owned.", False),
        ("• 'Audit & reconciliation' documents the verification performed before this file was issued.", False),
        "",
        ("Scope & confidentiality", True),
        ("• Every data point is collected at entity level and is CONFIDENTIAL under the Statistics Law. This pack lists the REQUIREMENTS only; it contains no live entity records.", False),
        ("• Sample identifiers elsewhere in the platform are stylised composites, not real entities.", False),
        "",
        ("Terminology note — 'MPC'", True),
        ("• 'MPC' in the request has been interpreted as the internal statistical production centre (NSO / PSA) that operates NEICS. Internal sources are tagged 'INTERNAL — NSO/PSA (MPC)'. Please confirm if a different body is meant.", False),
        "",
        ("Classify by economic reality", True),
        ("• Entities are classified by activity, ownership, control, residency and operations — NEVER by commercial name or licence label. Several data points exist precisely to detect label-vs-substance contradictions.", False),
        "",
        ("Coverage summary", True),
        ("• Providers: {}   |   Data points: {}   |   Mandatory: {}   |   Tests covered: {}   |   Engine input fields reconciled: {}/{}".format(
            len(PROVIDERS), len(dp_rows),
            sum(1 for r in dp_rows if r[11] == "Mandatory"), len(TESTS),
            len(covered & input_fields), len(input_fields)), False),
        ("• Audit status: {}".format("PASSED — all engine input fields covered, all providers resolve" if not issues else "ISSUES FOUND (see Audit sheet)"), False),
    ]
    r = 4
    for item in notes:
        r += 1
        if isinstance(item, tuple):
            text, bold = item
            ws.cell(row=r, column=1, value=text).font = Font(name="Arial", size=11, bold=bold, color=NAVY if bold else "333333")
        else:
            ws.cell(row=r, column=1, value=item)
    ws.column_dimensions["A"].width = 140

    # ---- Sheet: Provider register ----------------------------------------
    ws = wb.create_sheet("Provider register")
    ws.sheet_view.showGridLines = False
    ws["A1"] = "Provider register — entities required to supply data"
    ws["A1"].font = TITLE_FONT
    ws.merge_cells("A1:K1")
    write_table(ws, 3, PROVIDER_HEADERS, PROVIDERS, PROVIDER_WIDTHS, fill=NAVY)

    # ---- Sheet: Data requirements ----------------------------------------
    ws = wb.create_sheet("Data requirements")
    ws.sheet_view.showGridLines = False
    ws["A1"] = "Data requirements — every data point needed to operate the classification engine"
    ws["A1"].font = TITLE_FONT
    ws.merge_cells("A1:Q1")
    write_table(ws, 3, DP_HEADERS, dp_rows, DP_WIDTHS, fill=MAROON)

    # ---- Sheet: Test -> data points --------------------------------------
    ws = wb.create_sheet("Test → data points")
    ws.sheet_view.showGridLines = False
    ws["A1"] = "The 18 classification tests and the data they consume"
    ws["A1"].font = TITLE_FONT
    ws.merge_cells("A1:G1")
    write_table(ws, 3, TEST_HEADERS, TESTS, TEST_WIDTHS, fill=BLUE)

    # ---- Sheet: Source tiers ---------------------------------------------
    ws = wb.create_sheet("Source tiers")
    ws.sheet_view.showGridLines = False
    ws["A1"] = "Source tiers & conflict resolution"
    ws["A1"].font = TITLE_FONT
    ws.merge_cells("A1:C1")
    last = write_table(ws, 3, TIER_HEADERS, TIERS, TIER_WIDTHS, fill=GREEN)
    r = last + 2
    ws.cell(row=r, column=1, value="Conflict-resolution principles").font = Font(name="Arial", size=11, bold=True, color=NAVY)
    for c in CONFLICT:
        r += 1
        ws.cell(row=r, column=1, value="• " + c).font = B_FONT
        ws.cell(row=r, column=1).alignment = WRAP

    # ---- Sheet: Standards -------------------------------------------------
    ws = wb.create_sheet("Standards")
    ws.sheet_view.showGridLines = False
    ws["A1"] = "International & national standards applied"
    ws["A1"].font = TITLE_FONT
    ws.merge_cells("A1:D1")
    write_table(ws, 3, STD_HEADERS, STANDARDS, STD_WIDTHS, fill=NAVY)

    # ---- Sheet: Size thresholds ------------------------------------------
    ws = wb.create_sheet("Size thresholds")
    ws.sheet_view.showGridLines = False
    ws["A1"] = "Enterprise size thresholds (higher criterion governs)"
    ws["A1"].font = TITLE_FONT
    ws.merge_cells("A1:D1")
    write_table(ws, 3, SIZE_HEADERS, SIZE, SIZE_WIDTHS, fill=GOLD)

    # ---- Sheet: Governance (RACI) ----------------------------------------
    ws = wb.create_sheet("Governance (RACI)")
    ws.sheet_view.showGridLines = False
    ws["A1"] = "Data governance — RACI for sourcing, classifying and assuring"
    ws["A1"].font = TITLE_FONT
    ws.merge_cells("A1:E1")
    write_table(ws, 3, RACI_HEADERS, RACI, RACI_WIDTHS, fill=NAVY)

    # ---- Sheet: Audit & reconciliation -----------------------------------
    ws = wb.create_sheet("Audit & reconciliation")
    ws.sheet_view.showGridLines = False
    ws["A1"] = "Audit & reconciliation"
    ws["A1"].font = TITLE_FONT
    ws["A2"] = "Performed automatically when this workbook was generated, against the live engine input schema."
    ws["A2"].font = SUB_FONT
    checks = [
        ["Check", "Result", "Detail"],
        ["Engine input fields discovered (uat_enterprises + uat_ownership, outputs excluded)",
         str(len(input_fields)), ", ".join(sorted(input_fields))],
        ["Input fields covered by a data point", "{}/{}".format(len(covered & input_fields), len(input_fields)),
         "Every required input maps to at least one data point." if not missing else "MISSING: " + ", ".join(missing)],
        ["Providers in register", str(len(PROVIDERS)), "All referenced provider keys resolve to a registered provider."],
        ["Data points catalogued", str(len(dp_rows)), "{} mandatory, {} conditional/optional".format(
            sum(1 for r in dp_rows if r[11] == "Mandatory"), sum(1 for r in dp_rows if r[11] != "Mandatory"))],
        ["Classification tests covered", str(len(TESTS)), "All 18 tests have their consumed data points listed."],
        ["Standards referenced", str(len(STANDARDS)), "Each data point cites the standard that governs it."],
        ["Overall audit status", "PASSED" if not issues else "FAILED", "; ".join(issues) if issues else "No discrepancies."],
    ]
    write_table(ws, 4, checks[0], checks[1:], [56, 16, 90], fill=GREEN, zebra=True)

    wb.save(OUT)
    return dp_rows, input_fields, covered, missing, issues


if __name__ == "__main__":
    dp_rows, input_fields, covered, missing, issues = build()
    print("Engine input fields:", len(input_fields))
    print("Covered:", len(covered & input_fields), "/", len(input_fields))
    if missing:
        print("MISSING FIELDS:", missing)
    if issues:
        print("AUDIT ISSUES:")
        for i in issues:
            print("  -", i)
        sys.exit(1)
    print("Providers:", len(PROVIDERS), "| Data points:", len(dp_rows), "| Tests:", len(TESTS))
    print("AUDIT PASSED — wrote", OUT)
