"""Ingestion pipeline: connector -> staging(raw) -> normalize -> dedupe/merge
-> enrich -> score -> persist -> alerts.

Keeps a raw copy of every record (StagingRecord) for traceability, merges
duplicates across sources into one Project, and returns a summary plus the
new / window-opened projects so the caller can fire alerts.
"""
from __future__ import annotations

import json
import uuid
from typing import Any, Iterable

from sqlalchemy.orm import Session

from .alerts import notifier
from .config import get_config
from .connectors.base import BaseConnector, IngestRecord
from .models import Project, SourceRef, Stakeholder, StagingRecord
from .normalization import dedupe, enrich, normalize
from .scoring import scorecard


def _spec_score(status: str | None) -> float:
    return float(get_config()["spec_influence_scores"].get(status, 0.0))


def _window_opened(old_status: str | None, new_status: str | None) -> bool:
    """A spec window 'opens' when influence increases into design/pre-tender."""
    if new_status not in ("design", "pre-tender", "concept"):
        return False
    return _spec_score(new_status) > _spec_score(old_status)


def _apply_scores(project: Project) -> None:
    pdata = {
        "status": project.status,
        "country": project.country,
        "project_type": project.project_type,
        "estimated_door_demand": project.estimated_door_demand,
        "fire_rating_relevant": project.fire_rating_relevant,
        "reachable_before_procurement": project.reachable_before_procurement,
    }
    result = scorecard.score_project(pdata)
    project.score = result["score"]
    project.tier = result["tier"]
    project.score_breakdown_json = json.dumps(result["breakdown"])


def _project_summary(p: Project) -> dict[str, Any]:
    return {
        "project_id": p.project_id,
        "project_name": p.project_name,
        "country": p.country,
        "project_type": p.project_type,
        "status": p.status,
        "score": p.score,
        "tier": p.tier,
        "estimated_door_demand": p.estimated_door_demand,
        "value_estimate": p.value_estimate,
        "value_currency": p.value_currency,
        "reachable_before_procurement": p.reachable_before_procurement,
    }


def _merge_stakeholders(project: Project, stakeholders: list[dict], session: Session) -> None:
    existing = {(s.role, (s.organisation or "").lower()) for s in project.stakeholders}
    for s in stakeholders:
        key = (s["role"], (s.get("organisation") or "").lower())
        if key in existing:
            continue
        session.add(Stakeholder(project_id=project.project_id, **s))
        existing.add(key)


def stage_records(session: Session, records: Iterable[IngestRecord]) -> int:
    """Write raw + mapped copies to the staging table. Returns count staged."""
    count = 0
    for rec in records:
        session.add(
            StagingRecord(
                source=rec.source,
                source_record_id=rec.source_record_id,
                raw_json=json.dumps(rec.raw, default=str),
                mapped_json=json.dumps(rec.mapped, default=str),
                processed=False,
            )
        )
        count += 1
    session.flush()
    return count


def process_staging(session: Session) -> dict[str, Any]:
    """Normalize, dedupe/merge, enrich and score all unprocessed staging rows."""
    new_projects: list[dict] = []
    window_opened: list[dict] = []
    created = updated = merged = 0

    pending = (
        session.query(StagingRecord)
        .filter(StagingRecord.processed.is_(False))
        .order_by(StagingRecord.id)
        .all()
    )

    for staging in pending:
        norm = normalize.normalize_record(staging.mapped)
        proj_data = enrich.enrich(norm["project"], norm["stakeholders"])
        stakeholders = norm["stakeholders"]

        match = dedupe.find_duplicate(session, proj_data, stakeholders)

        if match is None:
            project = Project(project_id=uuid.uuid4().hex[:12], source=staging.source, **proj_data)
            session.add(project)
            session.flush()
            _merge_stakeholders(project, stakeholders, session)
            _apply_scores(project)
            session.add(
                SourceRef(
                    project_id=project.project_id,
                    source=staging.source,
                    source_record_id=staging.source_record_id,
                )
            )
            created += 1
            new_projects.append(_project_summary(project))
        else:
            old_status = match.status
            # Fill blanks + take the more-advanced status / better data.
            for field, value in proj_data.items():
                if value in (None, "", 0) and field not in ("status",):
                    continue
                setattr(match, field, value)
            _merge_stakeholders(match, stakeholders, session)
            opened = _window_opened(old_status, match.status)
            # add source ref if this source/record not already linked
            exists = (
                session.query(SourceRef)
                .filter_by(
                    project_id=match.project_id,
                    source=staging.source,
                    source_record_id=staging.source_record_id,
                )
                .first()
            )
            if not exists:
                session.add(
                    SourceRef(
                        project_id=match.project_id,
                        source=staging.source,
                        source_record_id=staging.source_record_id,
                    )
                )
                merged += 1
            _apply_scores(match)
            if opened:
                window_opened.append(_project_summary(match))
            updated += 1
            project = match

        staging.processed = True
        staging.project_id = project.project_id

    session.flush()
    return {
        "created": created,
        "updated": updated,
        "merged_sources": merged,
        "new_projects": new_projects,
        "window_opened": window_opened,
    }


def run_connector(session: Session, connector: BaseConnector, fire_alerts: bool = True) -> dict[str, Any]:
    """Full run for one connector: stage -> process -> alert."""
    staged = stage_records(session, connector.fetch())
    result = process_staging(session)
    result["staged"] = staged
    result["source"] = connector.source
    if fire_alerts:
        notifier.dispatch_new_and_changed(result["new_projects"], result["window_opened"])
    return result
