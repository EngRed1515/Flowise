#!/usr/bin/env python3
"""
Build NEICS_Entity_Data_Requests.xlsx — the entity-facing data-request pack.

Same audited source of truth as build_data_requirements.py (PROVIDERS + DP),
but reorganised so each providing entity gets its OWN clean sheet that says, in
plain language: "From you, NEICS requires these specific data points — 1, 2,
3, 4 …". You can send a single tab to a single entity (external ministry /
authority, or the NPC Statistics & Surveys department).

Audited before writing: every data point lands on at least one entity sheet,
and the per-entity counts reconcile to the master catalogue.
"""
import os
import sys
from datetime import date

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Reuse the single source of truth.
from build_data_requirements import (
    PROVIDERS, DP, PROV_KEY, NAVY, MAROON, GOLD, GREEN, BLUE, PAPER, RULE, WHITE,
)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "NEICS_Entity_Data_Requests.xlsx")

H_FONT = Font(name="Arial", size=10, bold=True, color=WHITE)
B_FONT = Font(name="Arial", size=10, color="222222")
TITLE_FONT = Font(name="Georgia", size=15, bold=True, color=NAVY)
SUB_FONT = Font(name="Arial", size=10, color="555555", italic=True)
LABEL_FONT = Font(name="Arial", size=10, bold=True, color=NAVY)
THIN = Side(style="thin", color=RULE)
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")

# pid -> short token (for tab names) and pid -> full provider row
PID_SHORT = {pid: short for short, pid in PROV_KEY.items()}
PID_ROW = {p[0]: p for p in PROVIDERS}

# Friendly dimension phrasing for "why we need it"
DIM_WHY = {
    "Identity": "uniquely identify and link the enterprise in the register",
    "Legal form": "determine legal form and whether the unit is general government",
    "Economic activity": "assign the principal economic activity (ISIC) by value added",
    "Market status": "apply the market vs non-market (50%) test",
    "Enterprise size": "assign the enterprise size band (micro/small/medium/large)",
    "Size / sector": "corroborate size and financial-corporation status",
    "Institutional sector": "assign the institutional sector (S.11–S.15 / S.2)",
    "Special entity": "run the SPV / holding / empty-shell substance test",
    "Institutional unit": "confirm the unit is an institutional unit",
    "Residence / FDI": "determine residence and foreign-direct-investment treatment",
    "Residence": "determine residence (centre of economic interest)",
    "Business demography": "record enterprise birth/death and group membership",
    "Enterprise group": "associate the unit with its enterprise group",
    "Ownership / control": "establish ownership and effective control",
    "Public / private": "place the unit on the public / private boundary",
    "FDI / residence": "determine inward-FDI status and residence of owners",
    "FDI": "determine foreign-direct-investment status and ultimate investing country",
    "Control": "determine effective control (voting / indicators)",
    "Effective control": "determine effective control via the nine control indicators",
    "Control / FDI": "identify the ultimate controlling unit and FDI chain",
}


# Extra corroboration links: an entity that confirms regime/membership for an
# existing data point even though another entity is the primary source. Keyed by
# the data-point 'field' name -> list of PROV_KEY short keys. Grounded in each
# entity's 'domains supplied' in the provider register; does NOT change the set
# of authoritative (required) assignments.
EXTRA_CORROB = {
    "Jurisdiction / licensing regime": ["QFZA", "QSTP"],
    "Principal economic activity (ISIC Rev.4)": ["QSTP"],
    "Ownership %": ["QSE"],
    "Voting %": ["QSE"],
}


def fmt_value(dtype, codelist):
    if codelist and codelist not in ("—",):
        return "{}  ·  {}".format(dtype, codelist)
    return dtype


def collect():
    """Return pid -> list of request rows. Each DP attaches to its primary
    provider (role 'Required from you') and, if set, its secondary provider
    (role 'Corroborating')."""
    by_pid = {p[0]: [] for p in PROVIDERS}
    for d in DP:
        (grp, field, efield, defn, dim, tests, std, prov, prov2, mand, dtype, codel, valid, cadence) = d
        why = "Used to {} (test {}).".format(DIM_WHY.get(dim, "classify the enterprise"), tests)
        val = fmt_value(dtype, codel)
        ppid = PROV_KEY.get(prov)
        if ppid:
            by_pid[ppid].append(["Required from you", grp, field, defn, why, val, mand, cadence])
        if prov2:
            spid = PROV_KEY.get(prov2)
            if spid:
                by_pid[spid].append(["Corroborating (helpful)", grp, field, defn, why, val,
                                     "Optional", cadence])
        for short in EXTRA_CORROB.get(field, []):
            epid = PROV_KEY.get(short)
            if epid:
                by_pid[epid].append(["Corroborating (regime/membership)", grp, field, defn, why, val,
                                     "Optional", cadence])
    # primary first within each entity
    for pid in by_pid:
        by_pid[pid].sort(key=lambda r: (0 if r[0].startswith("Required") else 1))
    return by_pid


def tab_name(pid):
    return "{} {}".format(pid, PID_SHORT.get(pid, ""))[:31]


def build():
    by_pid = collect()
    wb = Workbook()

    # ---- Cover ----------------------------------------------------------
    ws = wb.active
    ws.title = "Start here"
    ws.sheet_view.showGridLines = False
    ws["A1"] = "NEICS — Data Request Pack for Contributing Entities"
    ws["A1"].font = TITLE_FONT
    ws["A2"] = "National Enterprise Classification System · NPC · {} · NOT for public deployment".format(date.today().isoformat())
    ws["A2"].font = SUB_FONT
    intro = [
        "",
        ("What this pack is", True),
        ("This workbook tells every contributing entity EXACTLY which data points the National Enterprise Classification engine needs from them. There is one tab per entity. Open your tab to see your numbered list of required data points.", False),
        "",
        ("How to use it", True),
        ("1. Find your entity in the index below (or open your tab directly at the bottom of the screen).", False),
        ("2. Each row is one data point we require from you: what it means, why it is needed, the format, whether it is mandatory, and how often.", False),
        ("3. 'Required from you' = you are the authoritative source. 'Corroborating (helpful)' = another entity is primary but your data helps confirm it.", False),
        ("4. Send the data through the channel shown on your tab. Entity-level data is confidential under the Statistics Law and is used for statistical classification only.", False),
        "",
        ("One principle behind every request", True),
        ("Enterprises are classified by economic REALITY — activity, ownership, control, residency and operations — never by their commercial name or licence label. Some data points exist specifically to detect where a name and the real activity disagree.", False),
        "",
        ("Index of entities", True),
    ]
    r = 3
    for item in intro:
        r += 1
        if isinstance(item, tuple):
            ws.cell(row=r, column=1, value=item[0]).font = Font(name="Arial", size=11, bold=item[1], color=NAVY if item[1] else "333333")
        else:
            ws.cell(row=r, column=1, value=item).font = B_FONT
        ws.cell(row=r, column=1).alignment = WRAP

    # index table
    idx_head_row = r + 2
    headers = ["Tab", "Entity", "Bucket", "Required data points", "Corroborating", "Delivery channel"]
    for j, h in enumerate(headers, start=1):
        c = ws.cell(row=idx_head_row, column=j, value=h)
        c.font = H_FONT
        c.fill = PatternFill("solid", fgColor=NAVY)
        c.border = BORDER
        c.alignment = Alignment(wrap_text=True, vertical="center")
    rr = idx_head_row
    for p in PROVIDERS:
        pid = p[0]
        rows = by_pid[pid]
        req = sum(1 for x in rows if x[0].startswith("Required"))
        cor = sum(1 for x in rows if not x[0].startswith("Required"))
        rr += 1
        vals = [tab_name(pid), p[1], p[3], req, cor, p[7]]
        for j, v in enumerate(vals, start=1):
            c = ws.cell(row=rr, column=j, value=v)
            c.font = B_FONT
            c.border = BORDER
            c.alignment = WRAP
            if (rr - idx_head_row) % 2 == 1:
                c.fill = PatternFill("solid", fgColor=PAPER)
    ws.auto_filter.ref = "A{}:F{}".format(idx_head_row, rr)
    for j, w in enumerate([12, 46, 30, 14, 14, 28], start=1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.column_dimensions["A"].width = 14

    # ---- One sheet per entity ------------------------------------------
    REQ_HEADERS = ["No.", "Role", "Data domain", "Data point", "What it means",
                   "Why NEICS needs it", "Format / values", "Mandatory?", "How often"]
    REQ_WIDTHS = [5, 22, 18, 30, 50, 52, 28, 13, 18]
    for p in PROVIDERS:
        pid = p[0]
        ws = wb.create_sheet(tab_name(pid))
        ws.sheet_view.showGridLines = False
        ws["A1"] = "DATA REQUEST — {}".format(p[1])
        ws["A1"].font = TITLE_FONT
        ws.merge_cells("A1:I1")
        ws["A2"] = "From: National Enterprise Classification System (NEICS) · NPC"
        ws["A2"].font = SUB_FONT
        ws.merge_cells("A2:I2")
        # meta block
        meta = [
            ("Entity category", p[2]),
            ("Source bucket", p[3]),
            ("Source tier", p[4]),
            ("Co-authority role", p[5]),
            ("Delivery channel", p[7]),
            ("Update cadence", p[8]),
            ("Legal basis / gateway", p[9]),
        ]
        r = 3
        for k, v in meta:
            r += 1
            ws.cell(row=r, column=1, value=k).font = LABEL_FONT
            ws.cell(row=r, column=1).alignment = WRAP
            ws.cell(row=r, column=3, value=v).font = B_FONT
            ws.cell(row=r, column=3).alignment = WRAP
            ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=9)
        rows = by_pid[pid]
        req_n = sum(1 for x in rows if x[0].startswith("Required"))
        r += 2
        ws.cell(row=r, column=1,
                value="What we need from you: {} data point(s) you are the authoritative source for{}.".format(
                    req_n, "" if req_n == len(rows) else " (plus {} where your data corroborates another source)".format(len(rows) - req_n))
                ).font = Font(name="Arial", size=11, bold=True, color=MAROON)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=9)
        # table
        hr = r + 2
        for j, h in enumerate(REQ_HEADERS, start=1):
            c = ws.cell(row=hr, column=j, value=h)
            c.font = H_FONT
            c.fill = PatternFill("solid", fgColor=MAROON)
            c.border = BORDER
            c.alignment = Alignment(wrap_text=True, vertical="center")
        rr = hr
        if not rows:
            rr += 1
            note = ("This is the NPC's internal classification workspace, not an external data request — "
                    "analysts and the Technical Classification Committee enter rulings here."
                    if pid == "P-18" else
                    "No specific data column is requested from this entity today; it remains a corroborating "
                    "register. Notify the NEICS team of any change to entities under your regime.")
            ws.cell(row=rr, column=2, value=note).font = B_FONT
            ws.cell(row=rr, column=2).alignment = WRAP
            ws.merge_cells(start_row=rr, start_column=2, end_row=rr, end_column=9)
        for i, x in enumerate(rows, start=1):
            rr += 1
            role, grp, field, defn, why, val, mand, cadence = x
            vals = [i, role, grp, field, defn, why, val, mand, cadence]
            for j, v in enumerate(vals, start=1):
                c = ws.cell(row=rr, column=j, value=v)
                c.font = B_FONT
                c.border = BORDER
                c.alignment = WRAP
                if i % 2 == 0:
                    c.fill = PatternFill("solid", fgColor=PAPER)
        for j, w in enumerate(REQ_WIDTHS, start=1):
            ws.column_dimensions[get_column_letter(j)].width = w
        ws.freeze_panes = ws.cell(row=hr + 1, column=1)
        ws.auto_filter.ref = "A{}:I{}".format(hr, rr)
        # footer
        rr += 2
        ws.cell(row=rr, column=1,
                value="Confidentiality: entity-level data is confidential under the Statistics Law and used solely for statistical classification. Questions: NPC — National Statistics Office (NEICS classification team)."
                ).font = Font(name="Arial", size=9, italic=True, color="666666")
        ws.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=9)

    wb.save(OUT)
    return by_pid


def audit(by_pid):
    issues = []
    # every DP must appear at least once as 'Required from you'
    required_fields = set()
    for pid, rows in by_pid.items():
        for x in rows:
            if x[0].startswith("Required"):
                required_fields.add(x[2])
    catalogue_fields = {d[1] for d in DP}
    missing = sorted(catalogue_fields - required_fields)
    if missing:
        issues.append("Data points with no authoritative entity: " + ", ".join(missing))
    # counts reconcile: total 'Required' rows == number of DP entries
    total_req = sum(1 for rows in by_pid.values() for x in rows if x[0].startswith("Required"))
    if total_req != len(DP):
        issues.append("Required-row count {} != catalogue size {}".format(total_req, len(DP)))
    return missing, issues, total_req


if __name__ == "__main__":
    by_pid = build()
    missing, issues, total_req = audit(by_pid)
    entities_with_req = sum(1 for rows in by_pid.values() if any(x[0].startswith("Required") for x in rows))
    print("Entities:", len(PROVIDERS), "| with required data points:", entities_with_req)
    print("Required data-point assignments:", total_req, "(catalogue:", len(DP), ")")
    if issues:
        print("AUDIT ISSUES:")
        for i in issues:
            print("  -", i)
        sys.exit(1)
    print("AUDIT PASSED — wrote", OUT)
