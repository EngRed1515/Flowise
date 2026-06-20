"""Configuration loader.

All tunable behaviour (scoring weights, thresholds, country weights,
enrichment heuristics, alert settings) is read from config/config.yaml.
Secrets are read from environment variables (.env), never from config.yaml.
"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = Path(os.environ.get("GCC_CONFIG", BASE_DIR / "config" / "config.yaml"))
MAPPINGS_DIR = BASE_DIR / "config" / "mappings"
DATA_DIR = BASE_DIR / "data"

# Load .env once at import time (no error if missing).
load_dotenv(BASE_DIR / ".env")


@lru_cache(maxsize=1)
def get_config() -> dict[str, Any]:
    """Load and lightly validate the central config file."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)

    weights = cfg.get("scoring", {}).get("weights", {})
    total = sum(weights.values())
    if round(total, 6) != 100:
        # Non-fatal: scores are normalized, but warn so the user can fix intent.
        print(f"[config] WARNING: scoring weights sum to {total}, expected 100.")
    return cfg


def reload_config() -> dict[str, Any]:
    get_config.cache_clear()
    return get_config()


def get_mapping(profile: str) -> dict[str, Any]:
    """Load a connector column-mapping profile by name (e.g. 'meed')."""
    path = MAPPINGS_DIR / f"{profile}.yaml"
    if not path.exists():
        raise FileNotFoundError(
            f"Mapping profile '{profile}' not found at {path}. "
            f"Available: {[p.stem for p in MAPPINGS_DIR.glob('*.yaml')]}"
        )
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def env(key: str, default: str | None = None) -> str | None:
    """Read a secret/setting from the environment."""
    return os.environ.get(key, default)


def database_url() -> str:
    """SQLite by default; set DATABASE_URL in .env for Postgres."""
    default = f"sqlite:///{(DATA_DIR / 'gcc_door_intel.db').as_posix()}"
    return os.environ.get("DATABASE_URL", default)
