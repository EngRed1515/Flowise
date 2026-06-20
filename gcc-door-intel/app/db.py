"""Database engine / session setup (SQLite by default, Postgres-ready)."""
from __future__ import annotations

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import DATA_DIR, database_url

DATA_DIR.mkdir(parents=True, exist_ok=True)

_url = database_url()
# check_same_thread only matters for SQLite + the dev web server.
_connect_args = {"check_same_thread": False} if _url.startswith("sqlite") else {}
engine = create_engine(_url, connect_args=_connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)


def init_db() -> None:
    from .models import Base  # imported here to avoid circular import

    Base.metadata.create_all(engine)


@contextmanager
def session_scope() -> Session:
    """Transactional session scope for scripts and the pipeline."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session() -> Session:
    """FastAPI dependency."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
