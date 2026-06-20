"""Derive estimated_door_demand, the fire-rating flag and reachability."""
from __future__ import annotations

from typing import Any

from ..config import get_config


def estimate_door_demand(project: dict[str, Any]) -> int | None:
    """Heuristic door demand from unit count and/or floor area (configurable)."""
    cfg = get_config()["enrichment"]
    candidates = []
    if project.get("unit_count"):
        candidates.append(project["unit_count"] * cfg["doors_per_unit"])
    if project.get("floor_area"):
        candidates.append(project["floor_area"] * cfg["doors_per_sqm"])
    if not candidates:
        return None
    return int(round(max(candidates)))


def is_fire_rating_relevant(project: dict[str, Any]) -> bool:
    cfg = get_config()["enrichment"]
    return project.get("project_type") in set(cfg["fire_rated_project_types"])


def is_reachable(stakeholders: list[dict[str, Any]]) -> bool:
    """Reachable if we have at least one named contact with email or phone."""
    return any(s.get("email") or s.get("phone") for s in stakeholders)


def enrich(project: dict[str, Any], stakeholders: list[dict[str, Any]]) -> dict[str, Any]:
    project["estimated_door_demand"] = estimate_door_demand(project)
    project["fire_rating_relevant"] = is_fire_rating_relevant(project)
    project["reachable_before_procurement"] = is_reachable(stakeholders)
    return project
