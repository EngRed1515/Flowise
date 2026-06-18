"""Automated regression tests for the NEICS engine and API.

Run:  cd backend && PYTHONPATH=. pytest -q
Uses an isolated SQLite database; no external infrastructure required.
"""
import os
import tempfile

import pytest

os.environ["NEICS_DATABASE_URL"] = "sqlite:///" + os.path.join(tempfile.gettempdir(), "neics_pytest.db")
_dbfile = os.path.join(tempfile.gettempdir(), "neics_pytest.db")
if os.path.exists(_dbfile):
    os.remove(_dbfile)

from fastapi.testclient import TestClient  # noqa: E402

from app.core.security import has_permission  # noqa: E402
from app.database import Base, SessionLocal, engine  # noqa: E402
from app.engine.classifier import classify  # noqa: E402
from app.engine.expression import evaluate  # noqa: E402
from app.engine.ownership import OwnershipEngine  # noqa: E402
from app.engine.validation import validate_enterprise  # noqa: E402
from app.main import app  # noqa: E402
from app.models.enterprise import Enterprise  # noqa: E402
from app.seed.loader import seed_all  # noqa: E402

# Expected sector / public-private verdicts for the golden test set.
GOLDEN = {
    "QA-ENT-20260000001": ("S.11", "PUB-NFC"), "QA-ENT-20260000002": ("S.122", "PUB-FC"),
    "QA-ENT-20260000003": ("S.11", "FCC"), "QA-ENT-20260000004": ("S.126", "FCC"),
    "QA-ENT-20260000005": ("S.11", "PRV-NFC"), "QA-ENT-20260000006": ("S.13", "GG"),
    "QA-ENT-20260000099": ("S.11", "PUB-NFC"),
    "QA-ENT-20260000010": ("S.13", "GG"), "QA-ENT-20260000018": ("S.15", "NPISH"),
    "QA-ENT-20260000019": ("S.14", "PRV-NFC"), "QA-ENT-20260000024": ("S.11", "PUB-NFC"),
    "QA-ENT-20260000025": ("S.11", "PUB-NFC"), "QA-ENT-20260000028": ("S.11", "FCC"),
}


@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    seed_all(session)
    yield session
    session.close()


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def _token(client, user):
    r = client.post("/api/auth/login", data={"username": user, "password": f"{user}123"})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


# ----------------------------------------------------------------- engine
@pytest.mark.parametrize("eid,expected", GOLDEN.items())
def test_classification_verdicts(db, eid, expected):
    ent = db.get(Enterprise, eid)
    res = classify(db, ent)["result"]
    assert (res["sector_code"], res["public_private"]) == expected


def test_ownership_aggregation_across_vehicles(db):
    # Trading co: 45% + 15% state vehicles -> 60% effective government control.
    facts = OwnershipEngine(db).facts("QA-ENT-20260000099")
    assert facts["government_ownership_pct"] == 60.0
    assert facts["government_control"] is True


def test_multilevel_swf_cascade_roundtrip(db):
    # Developer owned 70% via a non-resident QIA vehicle, ultimately government.
    ent = db.get(Enterprise, "QA-ENT-20260000025")
    res = classify(db, ent)["result"]
    assert res["public_private"] == "PUB-NFC"
    assert res["fdi_flag"] == "ROUND-TRIP"
    assert OwnershipEngine(db).facts("QA-ENT-20260000025")["uci_is_government"] is True


def test_golden_share_minority_control(db):
    # PPP SPV: 49% government + golden share -> public corporation via GOLDEN.
    res = classify(db, db.get(Enterprise, "QA-ENT-20260000024"))["result"]
    assert res["public_private"] == "PUB-NFC"
    assert res["control_flag"] == "GOLDEN"


def test_empty_shell_consolidation(db):
    res = classify(db, db.get(Enterprise, "QA-ENT-20260000026"))["result"]
    assert res["special_entity_flag"] == "CONSOLIDATE-PARENT"


def test_expression_evaluator():
    assert evaluate({"op": "gt", "field": "x", "value": 50}, {"x": 60}) is True
    assert evaluate({"all": [{"op": "eq", "field": "a", "value": 1},
                             {"op": "truthy", "field": "b"}]}, {"a": 1, "b": True}) is True
    assert evaluate({"any": [{"op": "lt", "field": "x", "value": 0}]}, {"x": 5}) is False


def test_validation_detects_bad_isic(db):
    ent = db.get(Enterprise, "QA-ENT-20260000001")
    original = ent.isic_class
    ent.isic_class = "9999"
    issues = {i["rule_id"] for i in validate_enterprise(db, ent)}
    ent.isic_class = original
    assert "VR-002" in issues


# ----------------------------------------------------------------- API + RBAC
def test_rbac_matrix():
    assert has_permission("Administrator", "anything") is True
    assert has_permission("Analyst", "enterprise:write") is False
    assert has_permission("Classifier", "classify:run") is True


def test_health(client):
    assert client.get("/health").json()["status"] == "ok"


def test_classify_and_explain_endpoint(client):
    tok = _token(client, "classifier")
    h = {"Authorization": f"Bearer {tok}"}
    assert client.post("/api/enterprises/QA-ENT-20260000002/classify", headers=h).status_code == 200
    ex = client.get("/api/enterprises/QA-ENT-20260000002/explain", headers=h).json()
    assert len(ex["applied_rules"]) >= 6
    assert ex["result"]["public_private"] == "PUB-FC"


def test_rbac_denies_analyst_write(client):
    tok = _token(client, "analyst")
    r = client.post("/api/enterprises", headers={"Authorization": f"Bearer {tok}"},
                    json={"legal_name_en": "X"})
    assert r.status_code == 403


def test_simulation_not_persisted(client):
    tok = _token(client, "classifier")
    h = {"Authorization": f"Bearer {tok}"}
    payload = {"legal_name_en": "Sim", "isic_class": "4100", "residence": "RES",
               "sales": 100, "production_costs": 80,
               "ownership": [{"owner_id": "G", "owner_is_government": True, "owned_id": "X",
                              "ownership_pct": 100, "voting_pct": 100, "control_indicator": "MAJ-VOTE"}]}
    r = client.post("/api/simulate", headers=h, json=payload)
    assert r.json()["result"]["public_private"] == "PUB-NFC"
    assert client.get("/api/enterprises/SANDBOX-0001", headers=h).status_code == 404
