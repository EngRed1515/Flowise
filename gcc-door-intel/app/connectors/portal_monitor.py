"""Public-portal monitor (LATER PHASE — scaffold).

Scheduled checks of PUBLIC government tender/permit portals (e.g. Saudi Etimad,
Qatar Ashghal, UAE/Bahrain/Oman/Kuwait/Iraq public tender portals) — ONLY where
their terms permit. It must:
  - prefer official RSS / API / open-data endpoints when available,
  - obey robots.txt,
  - respect a configurable rate limit / polling interval,
  - store both the raw and parsed record.

This stub enforces the robots.txt check up front so the contract is explicit.
Parsing logic is implemented per-portal in a later phase.
"""
from __future__ import annotations

import urllib.robotparser
from typing import Any, Iterator
from urllib.parse import urljoin, urlparse

from .base import BaseConnector, IngestRecord


class PortalMonitorConnector(BaseConnector):
    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.source = config["source"]
        self.base_url = config["base_url"]
        self.user_agent = config.get("user_agent", "SBK-DoorIntel/1.0")
        self.rate_limit_seconds = config.get("rate_limit_seconds", 5)

    def is_allowed(self, path: str = "/") -> bool:
        """Check robots.txt before any request. Default-deny on error."""
        robots_url = urljoin(self.base_url, "/robots.txt")
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        try:
            rp.read()
        except Exception:
            return False
        target = urljoin(self.base_url, path)
        return rp.can_fetch(self.user_agent, target)

    def fetch(self) -> Iterator[IngestRecord]:  # pragma: no cover - scaffold
        if not self.is_allowed():
            raise PermissionError(
                f"robots.txt disallows monitoring {urlparse(self.base_url).netloc} "
                f"for agent {self.user_agent}. Aborting (never bypass robots.txt)."
            )
        raise NotImplementedError(
            "PortalMonitorConnector parsing is implemented per-portal in a later "
            "phase. Prefer official RSS/API/open-data endpoints; honor rate limits."
        )
