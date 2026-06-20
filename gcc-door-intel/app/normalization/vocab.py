"""Controlled vocabularies and value normalizers.

Maps the many ways sources spell countries / statuses / project types into a
single canonical set used everywhere downstream (scoring, filtering, dedupe).
"""
from __future__ import annotations

import re

# --- Countries -------------------------------------------------------------
CANONICAL_COUNTRIES = {
    "Saudi Arabia",
    "United Arab Emirates",
    "Qatar",
    "Bahrain",
    "Oman",
    "Kuwait",
    "Iraq",
}

_COUNTRY_ALIASES = {
    "ksa": "Saudi Arabia",
    "saudi": "Saudi Arabia",
    "saudi arabia": "Saudi Arabia",
    "kingdom of saudi arabia": "Saudi Arabia",
    "uae": "United Arab Emirates",
    "u.a.e": "United Arab Emirates",
    "united arab emirates": "United Arab Emirates",
    "emirates": "United Arab Emirates",
    "dubai": "United Arab Emirates",
    "abu dhabi": "United Arab Emirates",
    "qatar": "Qatar",
    "state of qatar": "Qatar",
    "bahrain": "Bahrain",
    "kingdom of bahrain": "Bahrain",
    "oman": "Oman",
    "sultanate of oman": "Oman",
    "kuwait": "Kuwait",
    "state of kuwait": "Kuwait",
    "iraq": "Iraq",
    "republic of iraq": "Iraq",
}

# --- Statuses --------------------------------------------------------------
CANONICAL_STATUSES = [
    "concept",
    "design",
    "pre-tender",
    "tender",
    "awarded",
    "under-construction",
    "on-hold",
    "cancelled",
]

_STATUS_ALIASES = {
    "concept": "concept",
    "conceptual": "concept",
    "feasibility": "concept",
    "planning": "concept",
    "design": "design",
    "design development": "design",
    "detailed design": "design",
    "schematic": "design",
    "pre-tender": "pre-tender",
    "pre tender": "pre-tender",
    "pretender": "pre-tender",
    "prequalification": "pre-tender",
    "tender": "tender",
    "tendering": "tender",
    "out to tender": "tender",
    "bidding": "tender",
    "open": "tender",
    "awarded": "awarded",
    "award": "awarded",
    "contract awarded": "awarded",
    "execution": "under-construction",
    "under construction": "under-construction",
    "under-construction": "under-construction",
    "construction": "under-construction",
    "ongoing": "under-construction",
    "on hold": "on-hold",
    "on-hold": "on-hold",
    "suspended": "on-hold",
    "postponed": "on-hold",
    "stalled": "on-hold",
    "cancelled": "cancelled",
    "canceled": "cancelled",
    "abandoned": "cancelled",
    "terminated": "cancelled",
}

# --- Project types ---------------------------------------------------------
CANONICAL_PROJECT_TYPES = [
    "residential tower",
    "compound",
    "hospital",
    "hotel",
    "school",
    "commercial",
    "commercial fit-out",
    "mixed-use",
    "infrastructure",
    "industrial",
    "other",
]

_PROJECT_TYPE_PATTERNS = [
    (r"hospital|clinic|health|medical", "hospital"),
    (r"hotel|resort|hospitality", "hotel"),
    (r"school|university|college|educat|campus", "school"),
    (r"residential tower|apartment|high[- ]?rise|tower", "residential tower"),
    (r"villa|compound|housing|community", "compound"),
    (r"fit[- ]?out|interior", "commercial fit-out"),
    (r"mixed[- ]?use", "mixed-use"),
    (r"mall|retail|office|commercial", "commercial"),
    (r"road|bridge|metro|airport|port|utilit|infrastructure", "infrastructure"),
    (r"factory|plant|warehouse|industrial", "industrial"),
]


def _clean(value) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip()).lower()


def normalize_country(value) -> str | None:
    key = _clean(value)
    if not key:
        return None
    if key in _COUNTRY_ALIASES:
        return _COUNTRY_ALIASES[key]
    for alias, canonical in _COUNTRY_ALIASES.items():
        if alias in key:
            return canonical
    # already canonical?
    for c in CANONICAL_COUNTRIES:
        if key == c.lower():
            return c
    return str(value).strip().title()


def normalize_status(value) -> str | None:
    key = _clean(value)
    if not key:
        return None
    if key in _STATUS_ALIASES:
        return _STATUS_ALIASES[key]
    for alias, canonical in _STATUS_ALIASES.items():
        if alias in key:
            return canonical
    return "concept"  # safest default: earliest stage


def normalize_project_type(value) -> str:
    key = _clean(value)
    if not key:
        return "other"
    for pattern, canonical in _PROJECT_TYPE_PATTERNS:
        if re.search(pattern, key):
            return canonical
    return "other"


# --- Currency / numbers ----------------------------------------------------
_CURRENCY_ALIASES = {
    "$": "USD",
    "usd": "USD",
    "us$": "USD",
    "sar": "SAR",
    "sr": "SAR",
    "aed": "AED",
    "dhs": "AED",
    "qar": "QAR",
    "bhd": "BHD",
    "omr": "OMR",
    "kwd": "KWD",
    "iqd": "IQD",
}


def normalize_currency(value) -> str | None:
    key = _clean(value)
    if not key:
        return None
    return _CURRENCY_ALIASES.get(key, str(value).strip().upper()[:3])


def to_float(value) -> float | None:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    cleaned = re.sub(r"[^\d.\-]", "", str(value))
    try:
        return float(cleaned) if cleaned not in ("", "-", ".") else None
    except ValueError:
        return None


def to_int(value) -> int | None:
    f = to_float(value)
    return int(f) if f is not None else None
