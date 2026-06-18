"""NEICS FastAPI application entrypoint.

National Enterprise Intelligence and Classification System — Staging / UAT build.
"""
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, catalog, enterprises, governance, ingest
from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.seed.loader import seed_all

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("neics")
settings = get_settings()

DESCRIPTION = """
**National Enterprise Intelligence and Classification System (NEICS)** — the national
platform for enterprise classification, profiling, ownership analysis and statistical
sectorisation for the State of Qatar.

Anchored in **SNA 2025, IMF GFS 2014, IMF BPM6, OECD BD4, ISIC Rev.4** and the modern
statistical-standards stack (LEI, SDMX, GSIM, GSBPM). Implements the 18-test
classification methodology with a database-driven Rules Engine, full explainability,
temporal versioning, and complete auditability.

> **Environment: STAGING / UAT.** Isolated from production and live data providers.
"""

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=DESCRIPTION,
    contact={"name": "NSO — State of Qatar (NEICS Programme)"},
    license_info={"name": "Government of Qatar — National Statistics Office"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origins] if settings.cors_origins != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(enterprises.router)
app.include_router(catalog.router)
app.include_router(governance.router)
app.include_router(ingest.router)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    if settings.auto_seed:
        db = SessionLocal()
        try:
            seed_all(db)
            log.info("Seed complete.")
        finally:
            db.close()


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok", "environment": "staging-uat", "version": settings.app_version,
            "methodology_version": settings.methodology_version}


@app.get("/", tags=["System"])
def root():
    return {
        "system": settings.app_name,
        "environment": "STAGING / UAT — not for production use",
        "docs": "/docs",
        "openapi": "/openapi.json",
        "health": "/health",
    }
