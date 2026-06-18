"""Central configuration for the NEICS backend.

Settings are environment-driven so the same image runs against SQLite (zero-infra
local/dev) and PostgreSQL (production via docker-compose / Kubernetes).
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NEICS_", env_file=".env", extra="ignore")

    app_name: str = "National Enterprise Intelligence and Classification System (NEICS)"
    app_version: str = "1.0.0"
    methodology_version: str = "1.0.0"  # version of the 18-test framework currently in force

    # Default to a file-based SQLite DB so the MVP runs with no external infra.
    # docker-compose overrides this with the PostgreSQL DSN.
    database_url: str = "sqlite:///./neics.db"

    # JWT / auth
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 480

    # Behaviour
    auto_seed: bool = True  # seed reference data + samples on startup if empty
    cors_origins: str = "*"


@lru_cache
def get_settings() -> Settings:
    return Settings()
