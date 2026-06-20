"""Pluggable connector framework.

Three connector types feed the same staging table:
  - FileImportConnector  (Phase 1): user-provided CSV/Excel exports
  - ApiConnector         (later):   official API/integration feeds
  - PortalMonitorConnector (later): public government portals (robots-aware)

A connector's only job is to yield IngestRecords (a stable per-source id, the
verbatim raw row, and a column-mapped dict). Normalization/dedupe/scoring all
happen downstream in the pipeline, so every connector type behaves identically
once data is staged.
"""
from __future__ import annotations

import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Iterator


@dataclass
class IngestRecord:
    source: str
    source_record_id: str
    raw: dict[str, Any]
    mapped: dict[str, Any]


def stable_record_id(source: str, row: dict[str, Any], id_columns: list[str]) -> str:
    """Use the first present id column; otherwise hash the row for stability."""
    for col in id_columns or []:
        val = row.get(col)
        if val not in (None, "", "nan"):
            return f"{source}:{val}"
    digest = hashlib.sha1(
        json.dumps(row, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()[:16]
    return f"{source}:{digest}"


class BaseConnector(ABC):
    """All connectors yield IngestRecords for the pipeline to stage."""

    source: str

    @abstractmethod
    def fetch(self) -> Iterator[IngestRecord]:
        raise NotImplementedError
