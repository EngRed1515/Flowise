"""API connector (LATER PHASE — scaffold).

Config-driven connector for sources that offer OFFICIAL API / integration
access (e.g. an enterprise MEED feed) using credentials the user supplies in
.env. Base URL, auth header, polling interval and field mapping are all config.

This is intentionally a stub: it documents the contract and fails loudly until
a real endpoint + credentials are wired up in a later phase. We never use it to
circumvent a platform's terms — only official, authorized API access.
"""
from __future__ import annotations

from typing import Any, Iterator

from .base import BaseConnector, IngestRecord, stable_record_id


class ApiConnector(BaseConnector):
    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.source = config["source"]
        self.base_url = config.get("base_url")
        self.mapping = config.get("mapping", {})
        self.id_columns = config.get("id_columns", [])

    def fetch(self) -> Iterator[IngestRecord]:  # pragma: no cover - scaffold
        raise NotImplementedError(
            "ApiConnector is a later-phase scaffold. Provide official API "
            "credentials (.env) and implement the authorized request/paging "
            "logic before enabling. Do not use to bypass platform terms."
        )

    def _map_row(self, row: dict[str, Any]) -> IngestRecord:
        mapped = {uf: row.get(sc) for uf, sc in self.mapping.items()}
        return IngestRecord(
            source=self.source,
            source_record_id=stable_record_id(self.source, row, self.id_columns),
            raw=row,
            mapped=mapped,
        )
