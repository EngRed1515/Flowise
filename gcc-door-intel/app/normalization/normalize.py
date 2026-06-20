"""Turn a column-mapped source record into a normalized candidate project."""
from __future__ import annotations

from typing import Any

from . import vocab

# Rough city centroids for the map view (no external geocoding dependency).
CITY_COORDS = {
    "riyadh": (24.7136, 46.6753),
    "jeddah": (21.4858, 39.1925),
    "dammam": (26.4207, 50.0888),
    "neom": (28.0, 35.3),
    "mecca": (21.3891, 39.8579),
    "medina": (24.5247, 39.5692),
    "dubai": (25.2048, 55.2708),
    "abu dhabi": (24.4539, 54.3773),
    "sharjah": (25.3463, 55.4209),
    "doha": (25.2854, 51.531),
    "lusail": (25.4306, 51.4912),
    "manama": (26.2285, 50.586),
    "muscat": (23.588, 58.3829),
    "kuwait city": (29.3759, 47.9774),
    "baghdad": (33.3152, 44.3661),
    "basra": (30.5085, 47.7804),
}
COUNTRY_COORDS = {
    "Saudi Arabia": (23.8859, 45.0792),
    "United Arab Emirates": (23.4241, 53.8478),
    "Qatar": (25.3548, 51.1839),
    "Bahrain": (26.0667, 50.5577),
    "Oman": (21.4735, 55.9754),
    "Kuwait": (29.3117, 47.4818),
    "Iraq": (33.2232, 43.6793),
}

# Stakeholder role -> mapped field that holds the organisation name.
STAKEHOLDER_ROLES = [
    "developer",
    "architect",
    "consultant",
    "main_contractor",
    "fitout_contractor",
]


def _coords(city: str | None, country: str | None) -> tuple[float | None, float | None]:
    if city and city.strip().lower() in CITY_COORDS:
        return CITY_COORDS[city.strip().lower()]
    if country and country in COUNTRY_COORDS:
        return COUNTRY_COORDS[country]
    return (None, None)


def normalize_record(mapped: dict[str, Any]) -> dict[str, Any]:
    """Return {'project': {...fields...}, 'stakeholders': [...]}."""
    country = vocab.normalize_country(mapped.get("country"))
    city = (mapped.get("city") or None)
    lat, lon = _coords(city, country)

    project = {
        "project_name": (mapped.get("project_name") or "").strip() or "(unnamed)",
        "country": country,
        "city": city.strip() if city else None,
        "district": (mapped.get("district") or None),
        "project_type": vocab.normalize_project_type(mapped.get("project_type")),
        "status": vocab.normalize_status(mapped.get("status")),
        "stage_date": (mapped.get("stage_date") or None),
        "expected_procurement_date": (mapped.get("expected_procurement_date") or None),
        "value_estimate": vocab.to_float(mapped.get("value_estimate")),
        "value_currency": vocab.normalize_currency(mapped.get("value_currency")),
        "floor_area": vocab.to_float(mapped.get("floor_area")),
        "unit_count": vocab.to_int(mapped.get("unit_count")),
        "latitude": lat,
        "longitude": lon,
    }

    # Build stakeholders. The first available contact_* is attached to the
    # most senior present stakeholder so we know who to actually reach.
    contact = {
        "contact_name": (mapped.get("contact_name") or None),
        "email": (mapped.get("contact_email") or None),
        "phone": (mapped.get("contact_phone") or None),
    }
    stakeholders = []
    contact_used = False
    for role in STAKEHOLDER_ROLES:
        org = mapped.get(role)
        if not org:
            continue
        sh = {
            "role": role,
            "organisation": str(org).strip(),
            "contact_name": None,
            "email": None,
            "phone": None,
        }
        if not contact_used and any(contact.values()):
            sh.update(contact)
            contact_used = True
        stakeholders.append(sh)

    # Contact present but no named org stakeholder -> keep as a generic contact.
    if any(contact.values()) and not contact_used:
        stakeholders.append({"role": "contact", "organisation": None, **contact})

    return {"project": project, "stakeholders": stakeholders}
