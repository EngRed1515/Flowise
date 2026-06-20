"""Build and dispatch alerts to the configured channels."""
from __future__ import annotations

from typing import Any

from ..config import get_config
from .channels import CHANNELS


def _active_channels():
    names = get_config()["alerts"].get("channels", ["console"])
    channels = []
    for name in names:
        cls = CHANNELS.get(name)
        if cls:
            channels.append(cls())
        else:
            print(f"[alerts] unknown channel '{name}' (have: {list(CHANNELS)})")
    return channels


def _tier_rank(tier: str) -> int:
    return {"A": 3, "B": 2, "C": 1}.get(tier, 0)


def _format_project(p: dict[str, Any]) -> str:
    val = f"{p['value_currency']} {p['value_estimate']:,.0f}" if p.get("value_estimate") else "n/a"
    return (
        f"- [{p['tier']}] {p['project_name']} ({p.get('country') or '?'})\n"
        f"    type={p.get('project_type')} status={p.get('status')} "
        f"score={p.get('score')} doors~{p.get('estimated_door_demand')}\n"
        f"    value={val} reachable={p.get('reachable_before_procurement')}"
    )


def dispatch_new_and_changed(new: list[dict], window_opened: list[dict]) -> None:
    """Push Tier-A (or configured floor) new projects + window-open changes."""
    cfg = get_config()["alerts"]
    floor = _tier_rank(cfg.get("alert_on_new_tier", "A"))
    channels = _active_channels()
    if not channels:
        return

    qualifying_new = [p for p in new if _tier_rank(p.get("tier", "C")) >= floor]
    sections = []
    if qualifying_new:
        sections.append(
            f"{len(qualifying_new)} new Tier-{cfg.get('alert_on_new_tier','A')}+ project(s):\n"
            + "\n".join(_format_project(p) for p in qualifying_new)
        )
    if cfg.get("alert_on_window_open") and window_opened:
        sections.append(
            f"{len(window_opened)} project(s) opened a spec window:\n"
            + "\n".join(_format_project(p) for p in window_opened)
        )
    if not sections:
        return

    subject = f"GCC Door Intel: {len(qualifying_new)} new Tier-A+ / {len(window_opened)} window changes"
    body = "\n\n".join(sections)
    payload = {"new": qualifying_new, "window_opened": window_opened}
    for ch in channels:
        ch.send(subject, body, payload)


def send_digest(projects: list[dict]) -> None:
    """Daily/weekly digest of new Tier A + B projects."""
    cfg = get_config()["alerts"]
    tiers = set(cfg.get("digest", {}).get("include_tiers", ["A", "B"]))
    freq = cfg.get("digest", {}).get("frequency", "daily")
    selected = [p for p in projects if p.get("tier") in tiers]
    channels = _active_channels()
    if not channels:
        return
    subject = f"GCC Door Intel — {freq} digest ({len(selected)} projects)"
    body = "\n".join(_format_project(p) for p in selected) or "No qualifying projects."
    for ch in channels:
        ch.send(subject, body, {"projects": selected})
