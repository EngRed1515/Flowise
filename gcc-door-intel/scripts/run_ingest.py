"""CLI to ingest an export file or send a digest.

    python -m scripts.run_ingest --file path/to/export.xlsx --profile meed
    python -m scripts.run_ingest --digest
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.alerts import notifier  # noqa: E402
from app.connectors.file_import import FileImportConnector  # noqa: E402
from app.db import init_db, session_scope  # noqa: E402
from app.models import Project  # noqa: E402
from app.pipeline import _project_summary, run_connector  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description="Ingest an export file or send a digest.")
    ap.add_argument("--file", help="Path to a CSV/Excel export to ingest")
    ap.add_argument("--profile", help="Mapping profile name (e.g. meed, protenders, etimad, generic)")
    ap.add_argument("--no-alerts", action="store_true", help="Skip firing alerts")
    ap.add_argument("--digest", action="store_true", help="Send the configured digest and exit")
    args = ap.parse_args()

    init_db()

    if args.digest:
        with session_scope() as session:
            projects = [_project_summary(p) for p in session.query(Project).all()]
        notifier.send_digest(projects)
        return

    if not args.file or not args.profile:
        ap.error("--file and --profile are required (or use --digest)")

    with session_scope() as session:
        connector = FileImportConnector(args.file, args.profile)
        res = run_connector(session, connector, fire_alerts=not args.no_alerts)
    print(
        f"Ingested {res['staged']} rows from {res['source']}: "
        f"created={res['created']} updated={res['updated']} merged_sources={res['merged_sources']}"
    )


if __name__ == "__main__":
    main()
