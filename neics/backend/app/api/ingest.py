"""Data Integration Framework — file upload (JSON/CSV) and bulk ingestion with
validation, error detection, and missing-data reporting."""
import csv
import io
import json

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import require
from app.database import get_db
from app.engine.service import run_classification
from app.engine.validation import validate_enterprise
from app.models.enterprise import Enterprise
from app.models.governance import AuditEntry
from app.schemas import EnterpriseIn

router = APIRouter(prefix="/api/ingest", tags=["Data Integration"])

REQUIRED = ["legal_name_en"]
RECOMMENDED = ["legal_form_code", "isic_class", "residence", "employment", "turnover_qar"]


def _next_id(db: Session, offset: int) -> str:
    from datetime import datetime
    n = db.execute(select(func.count()).select_from(Enterprise)).scalar_one() + 1 + offset
    return f"QA-ENT-{datetime.now().year}{n:07d}"


def _ingest_records(db: Session, records: list[dict], user: str, classify_now: bool) -> dict:
    report = {"received": len(records), "created": 0, "rejected": 0, "results": []}
    for i, raw in enumerate(records):
        missing_required = [f for f in REQUIRED if not raw.get(f)]
        missing_recommended = [f for f in RECOMMENDED if not raw.get(f)]
        row = {"index": i, "legal_name_en": raw.get("legal_name_en"),
               "missing_required": missing_required, "missing_recommended": missing_recommended}
        if missing_required:
            report["rejected"] += 1
            row["status"] = "REJECTED"
            report["results"].append(row)
            continue
        try:
            payload = EnterpriseIn(**{k: v for k, v in raw.items() if k in EnterpriseIn.model_fields})
        except Exception as exc:  # noqa: BLE001
            report["rejected"] += 1
            row["status"] = "REJECTED"
            row["error"] = str(exc)
            report["results"].append(row)
            continue
        data = payload.model_dump()
        data["enterprise_id"] = data.get("enterprise_id") or _next_id(db, i)
        ent = Enterprise(**data, last_demographic_event="BIRTH", quality_flag="DRAFT")
        db.add(ent)
        db.add(AuditEntry(record_type="enterprise", record_id=ent.enterprise_id, action="CREATE",
                          new_value=ent.legal_name_en, changed_by=user, evidence_ref="bulk-ingest"))
        db.flush()
        row["enterprise_id"] = ent.enterprise_id
        row["validation"] = validate_enterprise(db, ent)
        if classify_now:
            cls = run_classification(db, ent, user=user, commit=False)
            row["classification"] = {f: getattr(cls, f) for f in
                                     ["sector_code", "public_private", "control_flag", "size_class",
                                      "fdi_flag", "market_status", "special_entity_flag"]}
            row["confidence"] = cls.confidence
        row["status"] = "CREATED"
        report["created"] += 1
        report["results"].append(row)
    db.commit()
    return report


@router.post("/enterprises")
def ingest_json(records: list[dict], classify_now: bool = True,
                db: Session = Depends(get_db), user=Depends(require("enterprise:write"))):
    """Bulk-ingest a JSON array of enterprise records."""
    return _ingest_records(db, records, user.username, classify_now)


@router.post("/upload")
async def ingest_file(file: UploadFile = File(...), classify_now: bool = True,
                      db: Session = Depends(get_db), user=Depends(require("enterprise:write"))):
    """Upload a JSON or CSV file of enterprise records, validate and ingest."""
    content = (await file.read()).decode("utf-8-sig")
    name = (file.filename or "").lower()
    if name.endswith(".json") or content.lstrip().startswith(("[", "{")):
        parsed = json.loads(content)
        records = parsed if isinstance(parsed, list) else [parsed]
    else:  # CSV
        reader = csv.DictReader(io.StringIO(content))
        records = []
        for r in reader:
            rec = {k: (v if v != "" else None) for k, v in r.items()}
            for numf in ("employment",):
                if rec.get(numf) is not None:
                    rec[numf] = int(float(rec[numf]))
            for numf in ("turnover_qar", "total_assets_qar", "sales", "production_costs"):
                if rec.get(numf) is not None:
                    rec[numf] = float(rec[numf])
            for boolf in ("is_financial", "is_nonprofit", "has_premises", "has_employees", "has_autonomy"):
                if rec.get(boolf) is not None:
                    rec[boolf] = str(rec[boolf]).strip().lower() in ("1", "true", "yes", "y")
            records.append(rec)
    return _ingest_records(db, records, user.username, classify_now)
