"""Pydantic request/response models for the API."""
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# --- auth ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str


class UserOut(ORM):
    id: int
    username: str
    full_name: str | None = None
    email: str | None = None
    role: str
    is_active: bool


# --- enterprise ---
class EnterpriseIn(BaseModel):
    enterprise_id: str | None = None
    lei: str | None = None
    legal_name_en: str
    legal_name_ar: str | None = None
    legal_form_code: str | None = None
    residence: str | None = "RES"
    isic_class: str | None = None
    employment: int | None = None
    turnover_qar: float | None = None
    total_assets_qar: float | None = None
    sales: float | None = None
    production_costs: float | None = None
    is_nonprofit: bool = False
    is_financial: bool = False
    has_premises: bool = True
    has_employees: bool = True
    has_autonomy: bool = True
    jurisdiction: str | None = "MAINLAND"
    group_id: str | None = None
    birth_date: date | None = None


class EnterpriseOut(ORM):
    enterprise_id: str
    lei: str | None = None
    legal_name_en: str
    legal_name_ar: str | None = None
    legal_form_code: str | None = None
    residence: str | None = None
    isic_class: str | None = None
    sector_code: str | None = None
    public_private: str | None = None
    control_flag: str | None = None
    market_status: str | None = None
    size_class: str | None = None
    fdi_flag: str | None = None
    special_entity_flag: str | None = None
    group_id: str | None = None
    employment: int | None = None
    turnover_qar: float | None = None
    jurisdiction: str | None = None
    is_financial: bool = False
    is_nonprofit: bool = False
    quality_flag: str
    quality_score: float | None = None
    classification_version: str | None = None
    classification_date: datetime | None = None
    birth_date: date | None = None


class OwnershipIn(BaseModel):
    edge_id: str | None = None
    owner_id: str
    owner_name: str | None = None
    owner_is_government: bool = False
    owner_is_resident: bool = True
    owner_country: str | None = None
    owned_id: str
    owned_name: str | None = None
    ownership_pct: float = 0.0
    voting_pct: float = 0.0
    control_indicator: str | None = None
    is_ultimate: str = "N"


class OwnershipOut(ORM):
    edge_id: str
    owner_id: str
    owner_name: str | None = None
    owner_is_government: bool
    owner_is_resident: bool
    owner_country: str | None = None
    owned_id: str
    owned_name: str | None = None
    ownership_pct: float
    voting_pct: float
    control_indicator: str | None = None
    is_ultimate: str


class OverrideIn(BaseModel):
    field: str
    value: str
    reason: str


class ClassificationOut(ORM):
    id: int
    enterprise_id: str
    version: int
    methodology_version: str
    residence: str | None = None
    isic_class: str | None = None
    sector_code: str | None = None
    public_private: str | None = None
    control_flag: str | None = None
    market_status: str | None = None
    size_class: str | None = None
    fdi_flag: str | None = None
    special_entity_flag: str | None = None
    confidence: float | None = None
    is_current: bool
    is_override: bool
    override_reason: str | None = None
    reviewer: str | None = None
    quality_flag: str
    trace: list[Any] | None = None
    facts: dict[str, Any] | None = None
    created_at: datetime
    valid_from: datetime
    valid_to: datetime | None = None


class RuleOut(ORM):
    rule_id: str
    name: str
    description: str | None = None
    test_code: str
    domain: str
    inputs_required: list[Any] | None = None
    logic: dict[str, Any] | None = None
    output: dict[str, Any] | None = None
    priority: int
    confidence: float
    standard_ref: str | None = None
    rationale: str | None = None
    version: str
    author: str | None = None
    approval_status: str
    is_active: bool


class SimulateIn(EnterpriseIn):
    """Sandbox classification — same shape as enterprise input; never persisted."""
    ownership: list[OwnershipIn] = []
