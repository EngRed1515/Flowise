"""Qualification scorecard — the core of the system.

Scores every project 0-100 from six configurable, weighted factors and maps
the result to a tier (A pursue / B watch / C archive). The full per-factor
breakdown is returned so the team can see *why* a project scored what it did.
All weights and thresholds come from config.yaml — nothing is hardcoded.
"""
from __future__ import annotations

from typing import Any

from ..config import get_config


def _country_factor(country: str | None) -> float:
    weights = get_config()["country_weights"]
    if not country:
        return 0.0
    return float(weights.get(country, 0.5))


def _door_relevance_factor(project: dict[str, Any]) -> float:
    cfg = get_config()["enrichment"]
    demand = project.get("estimated_door_demand")
    if not demand:
        return 0.0
    full = cfg["door_demand_floor"] * cfg["door_demand_full_relevance_multiple"]
    return max(0.0, min(1.0, demand / full)) if full else 0.0


def score_project(
    project: dict[str, Any], stakeholders: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    """Return {'score': float, 'tier': str, 'breakdown': {...}}."""
    cfg = get_config()["scoring"]
    weights = cfg["weights"]
    status = project.get("status")

    # Auto-disqualify (on-hold / cancelled) -> score 0, tier C.
    if status in set(cfg.get("disqualifying_statuses", [])):
        return {
            "score": 0.0,
            "tier": "C",
            "breakdown": {
                "disqualified": True,
                "reason": f"status '{status}' is auto-disqualifying",
                "factors": {},
            },
        }

    status_scores = get_config()["status_scores"]
    spec_scores = get_config()["spec_influence_scores"]

    factors = {
        "funding_status": float(status_scores.get(status, 0.3)),
        "spec_influence": float(spec_scores.get(status, 0.3)),
        "door_relevance": _door_relevance_factor(project),
        "fire_rating": 1.0 if project.get("fire_rating_relevant") else 0.0,
        "reachability": 1.0 if project.get("reachable_before_procurement") else 0.0,
        "country": _country_factor(project.get("country")),
    }

    breakdown_factors = {}
    total = 0.0
    for name, norm in factors.items():
        weight = float(weights.get(name, 0))
        points = round(norm * weight, 2)
        total += points
        breakdown_factors[name] = {
            "normalized": round(norm, 3),
            "weight": weight,
            "points": points,
        }

    score = round(total, 1)
    tiers = cfg["tiers"]
    if score >= tiers["A"]:
        tier = "A"
    elif score >= tiers["B"]:
        tier = "B"
    else:
        tier = "C"

    return {
        "score": score,
        "tier": tier,
        "breakdown": {"disqualified": False, "factors": breakdown_factors},
    }
