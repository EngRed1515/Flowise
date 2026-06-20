"""End-to-end Phase-1 tests: vocab, scoring, enrichment, dedupe, full pipeline.

Runs against a throwaway in-memory SQLite DB so no credentials/files needed
beyond the bundled samples. Run with:  python -m pytest -q
"""
from __future__ import annotations

import os
import tempfile

# Point the DB at a temp file BEFORE importing app.db.
_tmp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp_db.name}"

from app.config import DATA_DIR  # noqa: E402
from app.connectors.file_import import FileImportConnector  # noqa: E402
from app.db import engine, session_scope  # noqa: E402
from app.models import Base, Project, SourceRef  # noqa: E402
from app.normalization import enrich, vocab  # noqa: E402
from app.pipeline import run_connector  # noqa: E402
from app.scoring.scorecard import score_project  # noqa: E402


def _fresh():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def test_vocab_normalization():
    assert vocab.normalize_country("KSA") == "Saudi Arabia"
    assert vocab.normalize_country("u.a.e") == "United Arab Emirates"
    assert vocab.normalize_status("Out to Tender") == "tender"
    assert vocab.normalize_status("on hold") == "on-hold"
    assert vocab.normalize_project_type("Residential High-Rise") == "residential tower"
    assert vocab.to_float("QAR 1,530,000,000") == 1530000000.0


def test_disqualification():
    res = score_project({"status": "on-hold", "country": "Qatar"})
    assert res["tier"] == "C" and res["score"] == 0.0
    assert res["breakdown"]["disqualified"] is True


def test_high_value_project_scores_tier_a():
    p = {"status": "pre-tender", "country": "Saudi Arabia", "project_type": "hospital"}
    p = enrich.enrich({**p, "unit_count": 800, "floor_area": 200000}, [{"email": "x@y.z"}])
    res = score_project(p)
    assert res["tier"] == "A"
    assert res["breakdown"]["factors"]["fire_rating"]["points"] > 0


def test_enrichment_door_demand_and_fire_flag():
    p = enrich.enrich({"project_type": "hotel", "unit_count": 100, "floor_area": None}, [])
    assert p["estimated_door_demand"] == 600  # 100 units * 6 doors
    assert p["fire_rating_relevant"] is True


def test_full_pipeline_dedupes_across_sources():
    _fresh()
    samples = DATA_DIR / "samples"
    with session_scope() as session:
        run_connector(session, FileImportConnector(samples / "sample_meed.csv", "meed"), fire_alerts=False)
        run_connector(session, FileImportConnector(samples / "sample_protenders.csv", "protenders"), fire_alerts=False)
        run_connector(session, FileImportConnector(samples / "sample_etimad.csv", "etimad"), fire_alerts=False)

        # Lusail Marina Twin Towers is in MEED + ProTenders -> one project, two sources.
        lusail = session.query(Project).filter(Project.project_name.ilike("%Lusail Marina%")).all()
        assert len(lusail) == 1
        srcs = {s.source for s in session.query(SourceRef).filter_by(project_id=lusail[0].project_id)}
        assert {"meed", "protenders"} <= srcs

        # On-hold / cancelled rows are auto-disqualified to Tier C.
        onhold = session.query(Project).filter(Project.status.in_(["on-hold", "cancelled"])).all()
        assert all(p.tier == "C" and p.score == 0 for p in onhold)

        # Every project got scored and tiered.
        assert all(p.score is not None and p.tier in ("A", "B", "C") for p in session.query(Project).all())
