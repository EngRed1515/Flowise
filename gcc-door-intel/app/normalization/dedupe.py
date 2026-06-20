"""Cross-source deduplication.

A project arriving from MEED, ProTenders and Etimad should collapse into one
record. We fuzzy-match on project name (+ same country, + developer name) and
return the existing Project to merge into, or None for a fresh insert.
"""
from __future__ import annotations

from typing import Any

from rapidfuzz import fuzz
from sqlalchemy.orm import Session

from ..config import get_config
from ..models import Project, Stakeholder


def _developer_name(stakeholders: list[dict[str, Any]]) -> str | None:
    for s in stakeholders:
        if s.get("role") == "developer" and s.get("organisation"):
            return s["organisation"]
    return None


def _existing_developer(session: Session, project_id: str) -> str | None:
    row = (
        session.query(Stakeholder)
        .filter(Stakeholder.project_id == project_id, Stakeholder.role == "developer")
        .first()
    )
    return row.organisation if row else None


def find_duplicate(
    session: Session, candidate: dict[str, Any], stakeholders: list[dict[str, Any]]
) -> Project | None:
    cfg = get_config()["dedupe"]
    name = candidate.get("project_name") or ""
    country = candidate.get("country")
    dev = _developer_name(stakeholders)

    query = session.query(Project)
    if cfg.get("require_same_country") and country:
        query = query.filter(Project.country == country)

    best: tuple[float, Project | None] = (0.0, None)
    for proj in query.all():
        name_score = fuzz.token_sort_ratio(name.lower(), (proj.project_name or "").lower())
        if name_score < cfg["name_similarity_threshold"]:
            continue
        # If both sides name a developer, it must also be similar enough.
        if dev:
            existing_dev = _existing_developer(session, proj.project_id)
            if existing_dev:
                # token_set_ratio so "Qatari Diar" ~ "Qatari Diar Real Estate".
                dev_score = fuzz.token_set_ratio(dev.lower(), existing_dev.lower())
                if dev_score < cfg["developer_similarity_threshold"]:
                    continue
        if name_score > best[0]:
            best = (name_score, proj)

    return best[1]
