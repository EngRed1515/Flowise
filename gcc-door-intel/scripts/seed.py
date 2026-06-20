"""Load the bundled sample exports through the full pipeline.

Demonstrates the whole Phase-1 flow with NO live credentials:
file import -> staging(raw) -> normalize -> dedupe/merge -> enrich -> score
-> alerts. The Lusail Marina Twin Towers project appears in both the MEED and
ProTenders samples and should collapse into a single record with two sources.

    python -m scripts.seed
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import DATA_DIR  # noqa: E402
from app.connectors.file_import import FileImportConnector  # noqa: E402
from app.db import init_db, session_scope  # noqa: E402
from app.models import Base, Project  # noqa: E402
from app.db import engine  # noqa: E402
from app.pipeline import run_connector  # noqa: E402

SAMPLES = [
    ("sample_meed.csv", "meed"),
    ("sample_protenders.csv", "protenders"),
    ("sample_etimad.csv", "etimad"),
]


def main(reset: bool = True) -> None:
    if reset:
        Base.metadata.drop_all(engine)
    init_db()
    samples_dir = DATA_DIR / "samples"
    with session_scope() as session:
        for filename, profile in SAMPLES:
            path = samples_dir / filename
            connector = FileImportConnector(path, profile)
            res = run_connector(session, connector, fire_alerts=True)
            print(
                f"[seed] {profile}: staged={res['staged']} created={res['created']} "
                f"updated={res['updated']} merged_sources={res['merged_sources']}"
            )
        total = session.query(Project).count()
        print(f"\n[seed] done. {total} unique projects in the database.")
        for p in session.query(Project).order_by(Project.score.desc()).all():
            srcs = ",".join(sorted({s.source for s in p.source_refs}))
            print(f"  {p.tier} {p.score:>5} | {p.project_name[:40]:40} | {p.country} | [{srcs}]")


if __name__ == "__main__":
    main(reset="--no-reset" not in sys.argv)
