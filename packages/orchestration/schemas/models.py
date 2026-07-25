"""Compact structured-output models for enforced provider responses (F005).

Every model is deliberately small (tokens cost money) and forbids unexpected
fields. A top-level structured response carries a compact ``schema_v`` so a reader
and the validator can tell exactly which contract the value claims to satisfy.

Anti-goal (A6): no mega-schemas and no new response taxonomy. The review and
planner models mirror the shapes already parsed by the free-text paths
(`pingpong_provider._parse_reviewer_json`, `planner_models.PlannerOutput`); they
do not invent a second vocabulary.
"""
from __future__ import annotations

from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

#: Compact schema version tags. Keep these short — they travel in every prompt.
REVIEW_VERDICT_SCHEMA_V = "rv1"
PLANNER_PLAN_SCHEMA_V = "pp1"
DESIGN_SPEC_SCHEMA_V = "ds1"
JOB_INTAKE_SCHEMA_V = "ji1"

Verdict = Literal["pass", "fail", "needs_repair", "blocked"]
Severity = Literal["blocker", "high", "medium", "low"]
Confidence = Literal["low", "medium", "high"]


class _Strict(BaseModel):
    """Base that rejects any field the schema did not declare."""

    model_config = ConfigDict(extra="forbid")


class _Structured(_Strict):
    """A top-level structured response.

    ``schema_v`` is a REQUIRED field (a bare ``Literal`` with no default) so a
    response that omits it is a validation failure, not a silently defaulted
    value. The model's version is read from the ``SCHEMA_V`` class constant — the
    validator never depends on a field default to know its own version.
    """

    #: The compact version this model enforces. Set by each concrete subclass.
    SCHEMA_V: ClassVar[str]


class ReviewFinding(_Strict):
    """One reviewer finding. Mirrors the accepted free-text finding shape."""

    id: str
    severity: Severity
    file: str
    summary: str
    required_fix: str = ""


class ReviewVerdict(_Structured):
    """Structured reviewer verdict (schema ``rv1``)."""

    SCHEMA_V: ClassVar[str] = REVIEW_VERDICT_SCHEMA_V
    schema_v: Literal["rv1"]  # required: no default
    verdict: Verdict
    findings: list[ReviewFinding] = Field(default_factory=list)
    confidence: Confidence
    summary: str


class ProposedTask(_Strict):
    """One planner-proposed task. Mirrors ``planner_models.ProposedTask``."""

    task_type: str
    description: str


class PlannerPlan(_Structured):
    """Structured planner output (schema ``pp1``)."""

    SCHEMA_V: ClassVar[str] = PLANNER_PLAN_SCHEMA_V
    schema_v: Literal["pp1"]  # required: no default
    summary: str
    proposed_tasks: list[ProposedTask] = Field(min_length=1)
    acceptance_checks: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class DesignSpec(_Structured):
    """Prepared design-spec placeholder (schema ``ds1``).

    Intentionally minimal: the design document lists design_spec as *prepared*,
    not yet wired. It exists so downstream format work (F013/F014) has a stable
    versioned anchor, and is deliberately not enforced on any provider path yet.
    """

    SCHEMA_V: ClassVar[str] = DESIGN_SPEC_SCHEMA_V
    schema_v: Literal["ds1"]  # required: no default
    summary: str


class IntakeClarification(_Strict):
    """One open clarification the intake identified."""

    question: str
    default_answer: str
    impact: str


class JobIntake(_Structured):
    """Structured job intake (schema ``ji1``).

    Turns a free-text mission into a validated contract the planner
    can consume without re-reading the raw mission text.
    """

    SCHEMA_V: ClassVar[str] = JOB_INTAKE_SCHEMA_V
    schema_v: Literal["ji1"]  # required: no default
    goal: str
    context_refs: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    acceptance_hints: list[str] = Field(default_factory=list)
    truncated_input: bool = False
    clarifications: list[IntakeClarification] = Field(default_factory=list)
    dropped_clarifications: int = 0


#: schema_v -> model. The single source of truth for which contract a tag means.
SCHEMA_REGISTRY: dict[str, type[_Structured]] = {
    REVIEW_VERDICT_SCHEMA_V: ReviewVerdict,
    PLANNER_PLAN_SCHEMA_V: PlannerPlan,
    DESIGN_SPEC_SCHEMA_V: DesignSpec,
    JOB_INTAKE_SCHEMA_V: JobIntake,
}


def schema_v_of(model_cls: type[_Structured]) -> str:
    """Return the compact schema version a structured model declares.

    Reads the ``SCHEMA_V`` class constant — never a field default, so the
    ``schema_v`` response field can stay required.
    """
    version = getattr(model_cls, "SCHEMA_V", None)
    if not version:
        raise ValueError(f"{model_cls.__name__} has no SCHEMA_V constant")
    return str(version)
