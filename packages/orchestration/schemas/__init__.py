"""Enforced structured-output schemas (F005).

Small Pydantic models with a compact ``schema_v``, a JSON-schema export, and a
single validation primitive that classifies any bad response as a ``parse``
failure carrying a concise retry hint.
"""
from __future__ import annotations

from packages.orchestration.schemas.models import (
    DESIGN_SPEC_SCHEMA_V,
    PLANNER_PLAN_SCHEMA_V,
    REVIEW_VERDICT_SCHEMA_V,
    SCHEMA_REGISTRY,
    Confidence,
    DesignSpec,
    PlannerPlan,
    ProposedTask,
    ReviewFinding,
    ReviewVerdict,
    Severity,
    Verdict,
    schema_v_of,
)
from packages.orchestration.schemas.validation import (
    PARSE_ERROR_CLASS,
    ValidationResult,
    to_json_schema,
    to_json_schema_str,
    validate_response,
)

__all__ = [
    "REVIEW_VERDICT_SCHEMA_V",
    "PLANNER_PLAN_SCHEMA_V",
    "DESIGN_SPEC_SCHEMA_V",
    "SCHEMA_REGISTRY",
    "Confidence",
    "DesignSpec",
    "PlannerPlan",
    "ProposedTask",
    "ReviewFinding",
    "ReviewVerdict",
    "Severity",
    "Verdict",
    "schema_v_of",
    "PARSE_ERROR_CLASS",
    "ValidationResult",
    "to_json_schema",
    "to_json_schema_str",
    "validate_response",
]
