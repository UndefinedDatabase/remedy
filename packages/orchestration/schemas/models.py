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

from pydantic import Field, model_validator

# The shared bases live in `structured_base` — a leaf module outside this
# package — so a contract defined elsewhere (the DoD) can use them without
# importing THIS module, which is what lets this module import that contract to
# register its tag. Both names are re-exported, so every existing
# `from ...schemas.models import _Strict` keeps working unchanged.
from packages.orchestration.dod_schema import DOD_SCHEMA_V, DoD
from packages.orchestration.mission_plan_schema import (
    MISSION_PLAN_SCHEMA_V,
    MissionPlan,
)
from packages.orchestration.structured_base import _Strict, _Structured

#: Compact schema version tags. Keep these short — they travel in every prompt.
REVIEW_VERDICT_SCHEMA_V = "rv1"
PLANNER_PLAN_SCHEMA_V = "pp1"
DESIGN_SPEC_SCHEMA_V = "ds1"
JOB_INTAKE_SCHEMA_V = "ji1"
FLIGHT_PLAN_SCHEMA_V = "flight_plan_v1"

Verdict = Literal["pass", "fail", "needs_repair", "blocked"]
Severity = Literal["blocker", "high", "medium", "low"]
Confidence = Literal["low", "medium", "high"]


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


# Deprecated by F014: superseded by FlightPlan. Retained for --no-llm/fallback.
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
    #: F056: this goal smells like it outlives one job.  A HINT ONLY — it
    #: surfaces the "run as mission?" offer in the plan approval, which
    #: defaults to NO.  Nothing is created because this is true (P2).
    #: Additive: payloads written before F056 load unchanged as False.
    mission_candidate: bool = False


TokenBand = Literal["S", "M", "L", "XL"]

_MAX_FLIGHT_PLAN_TASKS = 25
_LARGE_PLAN_THRESHOLD = 12


class PlannedTask(_Strict):
    """One task in a FlightPlan DAG."""

    id: str
    title: str
    goal: str
    acceptance: list[str] = Field(min_length=1)
    depends_on: list[str] = Field(default_factory=list)
    est_tokens_band: TokenBand
    files_hint: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_acceptance_entries(self) -> PlannedTask:
        for i, entry in enumerate(self.acceptance):
            if not entry.strip():
                raise ValueError(
                    f"PlannedTask.acceptance[{i}] must not be empty")
        return self


#: Who supplied a clarification's answer. Empty until the approval gate
#: resolves it — an unresolved question is neither human- nor default-answered.
AnsweredBy = Literal["human", "default", ""]


class FlightPlanClarification(_Strict):
    """A resolved clarification carried in the flight plan.

    ``id`` and ``answered_by`` are additive (F034): plans written before
    bundled clarification existed load unchanged and carry the empty
    defaults. The id is assigned by intake order (``q1``, ``q2``, …) so it
    stays stable across plan regeneration for the same intake.
    """

    question: str
    default_answer: str
    impact: str
    answer: str
    id: str = ""
    answered_by: AnsweredBy = ""


class FlightPlan(_Structured):
    """LLM-generated flight plan (schema ``fp1``).

    A DAG of PlannedTasks with goals, acceptance criteria, dependency
    edges, and token-band estimates. Validated on construction: no
    duplicate ids, no unknown dependencies, no cycles, hard task cap.
    """

    SCHEMA_V: ClassVar[str] = FLIGHT_PLAN_SCHEMA_V
    schema_v: Literal["flight_plan_v1"]  # required: no default
    tasks: list[PlannedTask] = Field(min_length=1)
    risks: list[str] = Field(default_factory=list)
    clarifications_resolved: list[FlightPlanClarification] = Field(
        default_factory=list)
    budgets: dict[str, int | str | None] | None = None
    fences: dict[str, list[str]] | None = None

    large_plan: bool = False

    @model_validator(mode="after")
    def _validate_dag(self) -> FlightPlan:
        if len(self.tasks) > _MAX_FLIGHT_PLAN_TASKS:
            raise ValueError(
                f"FlightPlan exceeds {_MAX_FLIGHT_PLAN_TASKS}-task cap "
                f"(got {len(self.tasks)})")

        ids: set[str] = set()
        for t in self.tasks:
            if t.id in ids:
                raise ValueError(f"duplicate task id: {t.id!r}")
            ids.add(t.id)

        for t in self.tasks:
            for dep in t.depends_on:
                if dep not in ids:
                    raise ValueError(
                        f"task {t.id!r} depends on unknown id {dep!r}")

        visited: set[str] = set()
        path: set[str] = set()

        def _visit(tid: str) -> None:
            if tid in path:
                raise ValueError(
                    f"dependency cycle detected involving {tid!r}")
            if tid in visited:
                return
            path.add(tid)
            task_map = {t.id: t for t in self.tasks}
            for dep in task_map[tid].depends_on:
                _visit(dep)
            path.discard(tid)
            visited.add(tid)

        for t in self.tasks:
            _visit(t.id)

        object.__setattr__(
            self, "large_plan", len(self.tasks) > _LARGE_PLAN_THRESHOLD)

        return self


#: schema_v -> model. The single source of truth for which contract a tag means.
SCHEMA_REGISTRY: dict[str, type[_Structured]] = {
    REVIEW_VERDICT_SCHEMA_V: ReviewVerdict,
    PLANNER_PLAN_SCHEMA_V: PlannerPlan,
    DESIGN_SPEC_SCHEMA_V: DesignSpec,
    JOB_INTAKE_SCHEMA_V: JobIntake,
    FLIGHT_PLAN_SCHEMA_V: FlightPlan,
    # F061: the compiled Definition of Done. Registered because a dod_v1
    # payload is PERSISTED (a job's evidence area) and therefore has to be
    # resolvable from its tag alone. Its provider-facing draft contract
    # (dod_draft_v1) is not registered: it never leaves the compiler's own
    # call and no reader ever resolves that tag.
    DOD_SCHEMA_V: DoD,
    # F069: the compiled mission plan. Registered for the same reason the DoD
    # is — a mission_plan_v1 payload is PERSISTED (on the mission record) and
    # therefore has to be resolvable from its tag alone. Its provider-facing
    # draft contract (mission_plan_draft_v1) is not registered: it never leaves
    # the compiler's own call and no reader ever resolves that tag.
    MISSION_PLAN_SCHEMA_V: MissionPlan,
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
