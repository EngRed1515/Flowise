#!/usr/bin/env python3
"""
Build NEICS_Data_Request.xlsx — the SINGLE, definitive data-request workbook.

Combines the completeness of the master catalogue with the share-ability of the
per-entity pack, and adds plain-language "why it matters" + importance + a
concrete example for every data point, so a non-technical recipient at any
entity knows exactly what to provide, how, and why it matters to the engine.

Tabs:
  1. Start here        — purpose, the data->engine flow, legend, confidentiality
  2. Summary by entity — every entity, what to send, hyperlink to its tab
  3. All data points   — the complete master list (one row per data point)
  4..  one tab per entity — the shareable request

Same audited source of truth as the other generators (PROVIDERS + DP); the
script self-audits before writing.
"""
import os
import sys
from datetime import date

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from build_data_requirements import PROVIDERS, DP, PROV_KEY, NAVY, MAROON, GOLD, GREEN, BLUE, PAPER, RULE, WHITE
from build_entity_requests import EXTRA_CORROB, PID_SHORT  # reuse regime links + tab tokens

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "NEICS_Data_Request.xlsx")

H_FONT = Font(name="Arial", size=10, bold=True, color=WHITE)
B_FONT = Font(name="Arial", size=10, color="222222")
TITLE_FONT = Font(name="Georgia", size=15, bold=True, color=NAVY)
SUB_FONT = Font(name="Arial", size=10, color="555555", italic=True)
LABEL_FONT = Font(name="Arial", size=10, bold=True, color=NAVY)
LINK_FONT = Font(name="Arial", size=10, color="2C5F8A", underline="single")
THIN = Side(style="thin", color=RULE)
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(wrap_text=True, vertical="center", horizontal="center")

PID_ROW = {p[0]: p for p in PROVIDERS}
IMP_COLOR = {"Critical": MAROON, "High": NAVY, "Medium": "777777"}

# What each classification dimension PRODUCES, in plain words (for "Drives")
DIM_RESULT = {
    "Identity": "Register identity & linkage",
    "Legal form": "Legal form / government flag",
    "Economic activity": "Industry (ISIC) classification",
    "Market status": "Market vs non-market producer",
    "Enterprise size": "Size band (micro→large)",
    "Size / sector": "Size & financial-corp check",
    "Institutional sector": "Institutional sector (S.11–S.15 / S.2)",
    "Special entity": "Empty-shell / SPV substance result",
    "Institutional unit": "Is it an institutional unit?",
    "Residence / FDI": "Residence & FDI treatment",
    "Residence": "Residence (in/out of national accounts)",
    "Business demography": "Birth/death & group membership",
    "Enterprise group": "Enterprise-group linkage",
    "Ownership / control": "Ownership & effective control",
    "Public / private": "Public / private boundary",
    "FDI / residence": "Inward-FDI status & residence",
    "FDI": "FDI status & investing country",
    "Control": "Effective control",
    "Effective control": "Effective control (9 indicators)",
    "Control / FDI": "Ultimate controlling unit & FDI chain",
}

# Per-data-point enrichment: importance, a concrete example, and a plain-English
# sentence on why it matters / what breaks without it. Keyed by data-point name.
ENRICH = {
 "Enterprise ID": ("Critical", "QA-ENT-20260000123",
   "The key everything links to — without it your data cannot be matched to the right enterprise."),
 "Legal Entity Identifier (LEI)": ("High", "5493001KJTIIGC8Y1R12",
   "Matches the entity across global financial datasets; mandatory for banks, insurers and funds."),
 "Legal name (EN / AR)": ("High", "Doha Steel W.L.L. / شركة الدوحة للصلب",
   "Confirms identity. The name is NEVER used to decide what the company actually does."),
 "Legal form code": ("Critical", "WLL · QPSC · GOV",
   "Tells us the legal type and flags government bodies — drives the public/government test."),
 "CR number": ("High", "CR-100245",
   "The Commercial-Register key that ties the unit to its registration record."),
 "Principal economic activity (ISIC Rev.4)": ("Critical", "4711 — retail sale in non-specialised stores",
   "The single most important activity field. Must be the REAL activity by value added, not the licence wording."),
 "Secondary / ancillary activities": ("Medium", "5210 — warehousing",
   "Lets us split mixed-activity units into the right industries."),
 "Turnover": ("Critical", "QAR 85,000,000",
   "Decides the size band. Without turnover we cannot size the enterprise."),
 "Sales / market output": ("Critical", "QAR 40,000,000",
   "Core of the market test: do the unit's sales cover the cost of what it produces?"),
 "Production costs": ("Critical", "QAR 70,000,000",
   "Paired with sales to apply the 50% rule that separates market producers from government/non-profit."),
 "Total assets": ("Medium", "QAR 320,000,000",
   "Confirms size and helps identify financial corporations."),
 "Employment": ("Critical", "5,200",
   "The other half of the size test — the higher of employment/turnover governs the size band."),
 "Non-profit status": ("High", "true",
   "Routes associations, charities, waqf and foundations into the non-profit sector (S.15)."),
 "Financial-activity status": ("Critical", "true — QCB-licensed bank",
   "Routes banks, insurers and funds into the financial sector (S.12) and its sub-sectors."),
 "Has premises": ("High", "true",
   "Substance test that catches empty-shell and letter-box companies."),
 "Has employees": ("High", "true",
   "A unit with no premises and no staff may be merged with its parent rather than counted separately."),
 "Has autonomy": ("High", "true",
   "Confirms the unit genuinely makes its own decisions — a real institutional unit."),
 "Jurisdiction / licensing regime": ("Critical", "QFZA — free zone",
   "Mainland / QFC / free-zone / QSTP changes the legal-form, FDI and residence treatment."),
 "Residence": ("Critical", "RES — resident in Qatar",
   "Only resident units enter Qatar's national accounts; this decides in- or out-of-scope."),
 "Birth date": ("High", "2015-01-01",
   "Marks economic birth; feeds business-demography statistics and the birth-lag target."),
 "Death / cessation date": ("Medium", "2024-06-30",
   "Marks cessation so the register stays accurate and live."),
 "Last demographic event": ("High", "MERGER",
   "Triggers re-classification when a unit is born, dies, merges, splits or restructures."),
 "Enterprise group ID": ("High", "GRP-014",
   "Links the unit to its group so we can find the ultimate parent and avoid double-counting."),
 "Owner identity": ("Critical", "Qatar Holding LLC — 70%",
   "Each owner is a node in the ownership graph used to work out who really controls the unit."),
 "Owner is government": ("Critical", "true",
   "Drives the public/private boundary; government stakes are added up across every vehicle."),
 "Owner is resident": ("Critical", "false — foreign owner",
   "A foreign owner holding 10% or more makes the unit inward foreign direct investment."),
 "Owner country": ("High", "AE — United Arab Emirates",
   "Identifies the ultimate investing country for FDI statistics."),
 "Ownership %": ("Critical", "70",
   "The equity stake, propagated through the chain to compute effective ownership."),
 "Voting %": ("Critical", "51",
   "Voting power can differ from equity; more than 50% voting means control."),
 "Control indicator": ("Critical", "GOLDEN — golden share",
   "Captures control that exists even below 50% — golden share, board seats, key contracts, financing."),
 "Ultimate controlling unit (UCI) flag": ("High", "Y — ultimate parent",
   "Marks the top of the ownership chain: the ultimate controlling unit."),
}


def prov_label(short):
    pid = PROV_KEY.get(short)
    if not pid:
        return "—"
    p = PID_ROW[pid]
    return "{} ({})".format(p[1].split(" —")[0].split(":")[0].split(" (")[0].strip(), pid)


def fmt_value(dtype, codel):
    return "{}  ·  {}".format(dtype, codel) if codel and codel != "—" else dtype


def tab_name(pid):
    return "{} {}".format(pid, PID_SHORT.get(pid, ""))[:31]


def style_header(ws, row, ncols, fill):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = H_FONT
        cell.fill = PatternFill("solid", fgColor=fill)
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = BORDER


def collect():
    """pid -> list of rows for its tab. Returns also the master rows."""
    by_pid = {p[0]: [] for p in PROVIDERS}
    master = []
    for n, d in enumerate(DP, start=1):
        (grp, field, efield, defn, dim, tests, std, prov, prov2, mand, dtype, codel, valid, cadence) = d
        imp, example, matters = ENRICH.get(field, ("High", "", ""))
        val = fmt_value(dtype, codel)
        drives = DIM_RESULT.get(dim, dim)
        # master row
        master.append([n, grp, field, defn, matters, drives, example, val, mand, imp,
                       prov_label(prov), prov_label(prov2) if prov2 else "—",
                       PID_ROW[PROV_KEY[prov]][3] if PROV_KEY.get(prov) else "", cadence, std, tests])
        # entity rows
        base = (grp, field, defn, matters, example, val, mand, imp, cadence)
        if PROV_KEY.get(prov):
            by_pid[PROV_KEY[prov]].append(("Required from you",) + base)
        if prov2 and PROV_KEY.get(prov2):
            by_pid[PROV_KEY[prov2]].append(("Corroborating (helpful)",) + base[:6] + ("Optional", imp, cadence))
        for short in EXTRA_CORROB.get(field, []):
            if PROV_KEY.get(short):
                by_pid[PROV_KEY[short]].append(("Corroborating (regime/membership)",) + base[:6] + ("Optional", imp, cadence))
    for pid in by_pid:
        by_pid[pid].sort(key=lambda r: (0 if r[0].startswith("Required") else 1))
    return by_pid, master


def build():
    by_pid, master = collect()
    wb = Workbook()

    # ---------- 1. Start here ----------
    ws = wb.active
    ws.title = "Start here"
    ws.sheet_view.showGridLines = False
    ws["A1"] = "NEICS — Data Request to Build the Classification Engine"
    ws["A1"].font = TITLE_FONT
    ws["A2"] = "National Enterprise Classification System · NPC · {} · NOT for public deployment".format(date.today().isoformat())
    ws["A2"].font = SUB_FONT
    blocks = [
        "",
        ("Why you have received this", True),
        ("To classify every enterprise in Qatar by its economic reality, NEICS needs a small set of facts about each enterprise from the entities that hold them. This workbook says, in plain language, exactly what each entity should provide and why it matters.", False),
        "",
        ("How the data is used (the flow)", True),
        ("Your data  →  Statistical Business Register  →  18-test classification engine  →  Each enterprise gets: industry · institutional sector · public/private · size · ownership & control · residency · FDI.", False),
        "",
        ("How to read your tab", True),
        ("• Open 'Summary by entity' and click your entity, or open your tab directly (tabs are named by entity).", False),
        ("• Each row is one data point. Columns tell you: what it means · why it matters to the engine · an example · the format · whether it is a must-have · its importance · how often to send it.", False),
        ("• 'Required from you' = you are the authoritative source. 'Corroborating' = another entity is primary, your data confirms it.", False),
        "",
        ("Legend", True),
        ("Importance — Critical: the engine cannot classify without it.   High: needed for an accurate result.   Medium: improves quality / corroborates.", False),
        ("Must-have? — Mandatory: always required.   Conditional: required when it applies (e.g. LEI for financial entities).   Optional: provide if available.", False),
        "",
        ("The one principle behind every request", True),
        ("Enterprises are classified by economic REALITY — activity, ownership, control, residency, operations — never by their commercial name or licence label. A few data points exist specifically to catch where the name and the real activity disagree.", False),
        "",
        ("Confidentiality", True),
        ("Entity-level data is confidential under the Statistics Law and is used solely for statistical classification. This workbook contains requirements only — no live entity records.", False),
        "",
        ("At a glance", True),
        ("Contributing entities: {}   |   Data points to build the engine: {}   |   Critical: {}   |   Mandatory: {}".format(
            len(PROVIDERS), len(DP),
            sum(1 for d in DP if ENRICH.get(d[1], ("High",))[0] == "Critical"),
            sum(1 for d in DP if d[9] == "Mandatory")), False),
    ]
    r = 3
    for item in blocks:
        r += 1
        if isinstance(item, tuple):
            ws.cell(row=r, column=1, value=item[0]).font = Font(name="Arial", size=11, bold=item[1], color=NAVY if item[1] else "333333")
        else:
            ws.cell(row=r, column=1, value=item).font = B_FONT
        ws.cell(row=r, column=1).alignment = WRAP
    ws.column_dimensions["A"].width = 145

    # ---------- 2. Summary by entity ----------
    ws = wb.create_sheet("Summary by entity")
    ws.sheet_view.showGridLines = False
    ws["A1"] = "Summary by entity — what each entity provides (click the tab link)"
    ws["A1"].font = TITLE_FONT
    ws.merge_cells("A1:G1")
    headers = ["Go to tab", "Entity", "Type", "Source bucket (filter)", "Required points", "Corroborating", "How to send"]
    hr = 3
    for j, h in enumerate(headers, start=1):
        ws.cell(row=hr, column=j, value=h)
    style_header(ws, hr, len(headers), NAVY)
    rr = hr
    for p in PROVIDERS:
        pid = p[0]
        rows = by_pid[pid]
        req = sum(1 for x in rows if x[0].startswith("Required"))
        cor = len(rows) - req
        rr += 1
        link = ws.cell(row=rr, column=1, value=tab_name(pid))
        link.hyperlink = "#'{}'!A1".format(tab_name(pid))
        link.font = LINK_FONT
        for j, v in enumerate([None, p[1], p[2], p[3], req, cor, p[7]], start=1):
            if j == 1:
                continue
            c = ws.cell(row=rr, column=j, value=v)
            c.font = B_FONT
            c.alignment = WRAP
            c.border = BORDER
        ws.cell(row=rr, column=1).border = BORDER
        if (rr - hr) % 2 == 1:
            for j in range(1, len(headers) + 1):
                if ws.cell(row=rr, column=j).fill.fgColor.rgb in (None, "00000000"):
                    ws.cell(row=rr, column=j).fill = PatternFill("solid", fgColor=PAPER)
    ws.freeze_panes = "A{}".format(hr + 1)
    ws.auto_filter.ref = "A{}:G{}".format(hr, rr)
    for j, w in enumerate([14, 46, 22, 30, 14, 14, 28], start=1):
        ws.column_dimensions[get_column_letter(j)].width = w

    # ---------- 3. All data points (master) ----------
    ws = wb.create_sheet("All data points")
    ws.sheet_view.showGridLines = False
    ws["A1"] = "All data points needed to build the engine (complete list)"
    ws["A1"].font = TITLE_FONT
    ws.merge_cells("A1:P1")
    m_head = ["No.", "Data domain", "Data point", "What it means", "Why it matters to the engine",
              "Drives (result)", "Example", "Format / values", "Must-have?", "Importance",
              "Primary entity", "Also from", "Source bucket (filter)", "How often", "Standard", "Test(s)"]
    hr = 3
    for j, h in enumerate(m_head, start=1):
        ws.cell(row=hr, column=j, value=h)
    style_header(ws, hr, len(m_head), MAROON)
    rr = hr
    for row in master:
        rr += 1
        for j, v in enumerate(row, start=1):
            c = ws.cell(row=rr, column=j, value=v)
            c.font = B_FONT
            c.alignment = WRAP
            c.border = BORDER
            if (rr - hr) % 2 == 1:
                c.fill = PatternFill("solid", fgColor=PAPER)
        ic = ws.cell(row=rr, column=10)  # Importance
        ic.font = Font(name="Arial", size=10, bold=True, color=IMP_COLOR.get(row[9], NAVY))
    ws.freeze_panes = "C{}".format(hr + 1)
    ws.auto_filter.ref = "A{}:P{}".format(hr, rr)
    for j, w in enumerate([5, 17, 28, 40, 50, 26, 26, 22, 13, 12, 30, 26, 26, 16, 12, 24], start=1):
        ws.column_dimensions[get_column_letter(j)].width = w

    # ---------- 4. One tab per entity ----------
    e_head = ["No.", "Role", "Data domain", "Data point", "What it means",
              "Why it matters to the engine", "Example", "Format / values", "Must-have?", "Importance", "How often"]
    e_w = [5, 22, 17, 28, 44, 50, 26, 22, 13, 12, 16]
    for p in PROVIDERS:
        pid = p[0]
        ws = wb.create_sheet(tab_name(pid))
        ws.sheet_view.showGridLines = False
        ws["A1"] = "DATA REQUEST — {}".format(p[1])
        ws["A1"].font = TITLE_FONT
        ws.merge_cells("A1:K1")
        ws["A2"] = "From: National Enterprise Classification System (NEICS) · NPC      ·      ← back to 'Summary by entity'"
        ws["A2"].font = SUB_FONT
        ws.merge_cells("A2:K2")
        meta = [("Entity type", p[2]), ("Source bucket", p[3]), ("Source tier", p[4]),
                ("How to send", p[7]), ("How often", p[8]), ("Legal basis / gateway", p[9])]
        r = 3
        for k, v in meta:
            r += 1
            ws.cell(row=r, column=1, value=k).font = LABEL_FONT
            ws.cell(row=r, column=1).alignment = WRAP
            cc = ws.cell(row=r, column=3, value=v)
            cc.font = B_FONT
            cc.alignment = WRAP
            ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=11)
        rows = by_pid[pid]
        req_n = sum(1 for x in rows if x[0].startswith("Required"))
        r += 2
        msg = ("What we need from you: {} data point(s) you are the authoritative source for{}.".format(
            req_n, "" if req_n == len(rows) else " plus {} where your data corroborates another source".format(len(rows) - req_n)))
        ws.cell(row=r, column=1, value=msg).font = Font(name="Arial", size=11, bold=True, color=MAROON)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=11)
        hr = r + 2
        for j, h in enumerate(e_head, start=1):
            ws.cell(row=hr, column=j, value=h)
        style_header(ws, hr, len(e_head), MAROON)
        rr = hr
        if not rows:
            rr += 1
            note = ("This is the NPC's internal classification workspace, not an external data request — "
                    "analysts and the Technical Classification Committee enter rulings here."
                    if pid == "P-18" else
                    "No specific data column is requested from you today; you remain a corroborating register. "
                    "Please notify the NEICS team of any change to entities under your regime.")
            c = ws.cell(row=rr, column=2, value=note)
            c.font = B_FONT
            c.alignment = WRAP
            ws.merge_cells(start_row=rr, start_column=2, end_row=rr, end_column=11)
        for i, x in enumerate(rows, start=1):
            rr += 1
            role, grp, field, defn, matters, example, val, mand, imp, cadence = x
            vals = [i, role, grp, field, defn, matters, example, val, mand, imp, cadence]
            for j, v in enumerate(vals, start=1):
                c = ws.cell(row=rr, column=j, value=v)
                c.font = B_FONT
                c.alignment = WRAP
                c.border = BORDER
                if i % 2 == 0:
                    c.fill = PatternFill("solid", fgColor=PAPER)
            ws.cell(row=rr, column=10).font = Font(name="Arial", size=10, bold=True, color=IMP_COLOR.get(imp, NAVY))
        for j, w in enumerate(e_w, start=1):
            ws.column_dimensions[get_column_letter(j)].width = w
        ws.freeze_panes = ws.cell(row=hr + 1, column=1)
        ws.auto_filter.ref = "A{}:K{}".format(hr, max(rr, hr))
        rr += 2
        ws.cell(row=rr, column=1,
                value="Confidentiality: entity-level data is confidential under the Statistics Law and used solely for statistical classification. Questions: NPC — National Statistics Office (NEICS classification team)."
                ).font = Font(name="Arial", size=9, italic=True, color="666666")
        ws.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=11)

    wb.save(OUT)
    return by_pid, master


def audit(by_pid, master):
    issues = []
    if len(master) != len(DP):
        issues.append("Master rows {} != catalogue {}".format(len(master), len(DP)))
    required = {x[2] for rows in by_pid.values() for x in rows if x[0].startswith("Required")}
    missing = sorted({d[1] for d in DP} - required)
    if missing:
        issues.append("Data points with no authoritative entity: " + ", ".join(missing))
    no_imp = sorted(d[1] for d in DP if d[1] not in ENRICH)
    if no_imp:
        issues.append("Data points missing enrichment (importance/example/why): " + ", ".join(no_imp))
    total_req = sum(1 for rows in by_pid.values() for x in rows if x[0].startswith("Required"))
    if total_req != len(DP):
        issues.append("Required-row count {} != catalogue {}".format(total_req, len(DP)))
    return missing, no_imp, issues, total_req


if __name__ == "__main__":
    by_pid, master = build()
    missing, no_imp, issues, total_req = audit(by_pid, master)
    print("Entities:", len(PROVIDERS), "| Data points:", len(DP), "| Master rows:", len(master))
    print("Required assignments:", total_req, "| Enriched:", len(DP) - len(no_imp), "/", len(DP))
    if issues:
        print("AUDIT ISSUES:")
        for i in issues:
            print("  -", i)
        sys.exit(1)
    print("AUDIT PASSED — wrote", OUT)
