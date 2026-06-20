"""File-import connector (Phase 1).

Parses a user-provided CSV/Excel export and maps its columns to the unified
schema using a mapping profile from config/mappings/. We NEVER scrape paid
platforms (MEED, ProTenders, Ventures ONSITE, BNC, GlobalData); their data
enters only through these official export files.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterator

import pandas as pd

from ..config import get_mapping
from .base import BaseConnector, IngestRecord, stable_record_id


class FileImportConnector(BaseConnector):
    def __init__(self, path: str | Path, profile: str):
        self.path = Path(path)
        self.profile_name = profile
        self.profile = get_mapping(profile)
        self.source = self.profile.get("source", profile)

    def _read(self) -> pd.DataFrame:
        suffix = self.path.suffix.lower()
        if suffix in (".xlsx", ".xls"):
            df = pd.read_excel(self.path, dtype=str)
        elif suffix in (".csv", ".txt"):
            df = pd.read_csv(self.path, dtype=str)
        else:
            raise ValueError(f"Unsupported file type: {suffix} ({self.path})")
        return df.where(pd.notnull(df), None)

    def fetch(self) -> Iterator[IngestRecord]:
        df = self._read()
        mapping: dict[str, str] = self.profile.get("mapping", {})
        defaults: dict[str, Any] = self.profile.get("defaults", {})
        id_columns: list[str] = self.profile.get("id_columns", [])

        for _, row in df.iterrows():
            raw = {k: (None if v is None else str(v)) for k, v in row.to_dict().items()}

            # Apply column mapping: unified_field <- source_column value.
            mapped: dict[str, Any] = dict(defaults)
            for unified_field, source_col in mapping.items():
                if source_col in raw and raw[source_col] not in (None, ""):
                    mapped[unified_field] = raw[source_col]
                elif unified_field not in mapped:
                    mapped[unified_field] = None

            yield IngestRecord(
                source=self.source,
                source_record_id=stable_record_id(self.source, raw, id_columns),
                raw=raw,
                mapped=mapped,
            )
