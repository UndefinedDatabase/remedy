"""F069 T001 — the MissionPlan schema.

A mission holds a long prose goal.  A MissionPlan is the structured route
through it: ORDERED MILESTONES, each an outcome the mission reaches, wired into
a DAG, each carrying a compiled Definition-of-Done reference and a handful of
DRAFT job outlines.

Conventions follow F005 structured outputs and the F061 DoD schema: small
models, ``extra="forbid"``, a REQUIRED ``schema_v`` (a bare ``Literal`` with no
default) and the model's own version in a ``SCHEMA_V`` class constant.

Two models, deliberately distinct — the same split the DoD schema makes:

  * :class:`MissionPlanDraft` is the PROVIDER-facing contract.  It cannot
    express ``dod_ref`` and it cannot claim to be compiled: provenance and the
    DoD hand-off are the compiler's to assign.
  * :class:`MissionPlan` is the compiled artifact.  It carries ``compiled`` and
    ``origin``, and a validator makes the dishonest combination
    (``compiled=True`` on a deterministic plan) structurally impossible.

A ``jobs_draft`` entry is an OUTLINE, never a runnable job.  Nothing in this
module or in :mod:`packages.orchestration.mission_compiler` turns one into
work; draft jobs become real jobs only through explicit continuation.  Remedy
deliberately does NOT autostart a compiled milestone — searching here for the
code that does is searching for code that does not exist, by design.

``mission_plan_v1`` is registered in ``schemas.models.SCHEMA_REGISTRY`` — by
that module, importing this one, never as a side effect of importing here.  The
shared bases therefore come from :mod:`packages.orchestration.structured_base`,
which is what keeps the dependency one-directional (the same rule
``dod_schema`` follows).  The draft contract is NOT registered: it never leaves
the compiler's own call and no reader ever resolves that tag.
"""
from __future__ import annotations

from typing import ClassVar, Literal

from pydantic import Field, model_validator

from packages.orchestration.structured_base import _Strict, _Structured

#: Compact schema version tags (F005 convention: short, they travel in prompts).
MISSION_PLAN_SCHEMA_V = "mission_plan_v1"
MISSION_PLAN_DRAFT_SCHEMA_V = "mission_plan_draft_v1"

#: How the plan as a whole was produced.  Mirrors ``dod_schema.DoDOrigin``.
MissionPlanOrigin = Literal["provider", "deterministic"]

#: The token-band vocabulary a draft job outline estimates in.  Spelled out
#: here rather than imported from ``schemas.models``: that module imports THIS
#: one to register the tag, so an import back would close the cycle.  Same
#: vocabulary, same four bands as ``PlannedTask.est_tokens_band``.
MilestoneTokenBand = Literal["S", "M", "L", "XL"]

#: More milestones than a mission plausibly has.  Over the cap is not a big
#: plan — it is hallucinated scope, and it is refused as a parse-class failure
#: exactly as the flight plan refuses more than 25 tasks.
MAX_MISSION_MILESTONES = 12

#: A milestone id becomes part of a rendered filename and of every dependency
#: edge, so it is small, non-empty, and free of whitespace.
MAX_MILESTONE_ID_CHARS = 64

#: How many draft outlines one milestone may sketch (R-0168).  A milestone
#: needing more than eight is not a milestone, it is a project — the same
#: hallucinated-scope reading :data:`MAX_MISSION_MILESTONES` applies one level
#: up.  The cap also keeps the ephemeral ``milestone_flight_plan`` view inside
#: the flight plan's own 25-task limit (one task per outline, plus the outcome
#: task), so an over-eager draft is refused HERE — at parse time, where the
#: single retry and the deterministic fallback still apply — instead of raising
#: out of the DoD hand-off later.
MAX_MILESTONE_DRAFT_JOBS = 8

#: Imperative verbs a task list starts its items with.  Closed and small on
#: purpose: this drives a LINT, and a lint that guesses is worse than no lint.
#: See :func:`looks_like_task_list` for the rule these feed.
_IMPERATIVE_VERBS = frozenset({
    "add", "adjust", "build", "change", "clean", "configure", "create",
    "delete", "deploy", "document", "extract", "fix", "implement", "install",
    "introduce", "merge", "migrate", "move", "refactor", "remove", "rename",
    "run", "set", "split", "test", "update", "wire", "write",
})

#: What separates the items of a task list written as one line.
_LIST_SEPARATORS = (";", ",", " then ", " and then ", " and ")


class MissionPlanError(ValueError):
    """A mission plan is structurally wrong or not outcome-phrased."""


def _leading_verb(text: str) -> str:
    """The first word of ``text``, lowercased and stripped of punctuation."""
    for word in str(text).strip().split():
        return word.strip("*_`\"'()[].,:;").lower()
    return ""


def looks_like_task_list(goal: str) -> bool:
    """Does this milestone goal read as a task list rather than an outcome?

    THE HEURISTIC, stated so a reader never has to infer it from the code:
    a goal is task-list-shaped when it STARTS with an imperative verb from
    :data:`_IMPERATIVE_VERBS` **and** at least one further list item — split on
    ``;``, ``,``, `` then `` or `` and `` — also starts with one.  Two or more
    imperatives in a row is a to-do list; one is merely terse.

    It is deliberately conservative.  A milestone is an OUTCOME ("the payments
    API stays releasable"), and rejecting a real outcome because it happens to
    open with a verb would be worse than letting a terse milestone through, so
    a SINGLE imperative never trips this.
    """
    text = str(goal).strip()
    if not text:
        return False
    if _leading_verb(text) not in _IMPERATIVE_VERBS:
        return False

    remainder = text
    for sep in _LIST_SEPARATORS:
        remainder = remainder.replace(sep, "\x00")
    items = [part for part in remainder.split("\x00") if part.strip()]
    return sum(1 for item in items if _leading_verb(item) in _IMPERATIVE_VERBS) >= 2


class DraftJob(_Strict):
    """One OUTLINE of work a milestone will probably need.

    Not a job.  Not runnable.  It carries no id, no plan and no acceptance
    criteria precisely so that nothing downstream can mistake it for one.
    """

    title: str
    goal: str
    est_band: MilestoneTokenBand

    @model_validator(mode="after")
    def _validate_draft_job(self) -> DraftJob:
        # R-0168: an outline whose goal is blank becomes an empty acceptance
        # line in the milestone flight-plan view, which the FlightPlan
        # validators reject far downstream. Refused here, at parse time.
        for field, value in (("title", self.title), ("goal", self.goal)):
            if not value.strip():
                raise MissionPlanError(
                    f"draft job {field} must not be empty or blank")
        return self


class MilestoneDraft(_Strict):
    """One milestone as the PROVIDER proposes it — no DoD reference yet."""

    id: str
    goal: str
    rationale: str = ""
    depends_on: list[str] = Field(default_factory=list)
    jobs_draft: list[DraftJob] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_milestone(self) -> MilestoneDraft:
        ident = self.id.strip()
        if not ident or ident != self.id or len(self.id) > MAX_MILESTONE_ID_CHARS:
            raise MissionPlanError(
                f"milestone id must be non-empty, unpadded and at most "
                f"{MAX_MILESTONE_ID_CHARS} characters: {self.id!r}")
        if any(ch.isspace() for ch in self.id):
            raise MissionPlanError(
                f"milestone id must not contain whitespace: {self.id!r}")
        if not self.goal.strip():
            raise MissionPlanError(f"milestone {self.id!r} has no goal")
        if looks_like_task_list(self.goal):
            raise MissionPlanError(
                f"milestone {self.id!r} reads as a task list, not an outcome: "
                f"{self.goal!r} — a milestone states what is TRUE when it is "
                f"reached, not the steps taken to get there")
        if len(self.jobs_draft) > MAX_MILESTONE_DRAFT_JOBS:
            raise MissionPlanError(
                f"milestone {self.id!r} exceeds the "
                f"{MAX_MILESTONE_DRAFT_JOBS}-outline cap "
                f"(got {len(self.jobs_draft)}) — that is a project, not a "
                f"milestone; raise the milestone's altitude or split it")
        return self


class Milestone(MilestoneDraft):
    """One milestone of a compiled plan, with its Definition-of-Done reference.

    ``dod_ref`` is empty until the compiler hands the milestone to the F061 DoD
    compiler and stores what came back.  Empty means "no DoD compiled yet",
    which is the truth for a milestone the compiler has only just parsed.
    """

    dod_ref: str = ""


class MissionPlanDraft(_Structured):
    """The provider-facing mission plan (schema ``mission_plan_draft_v1``)."""

    SCHEMA_V: ClassVar[str] = MISSION_PLAN_DRAFT_SCHEMA_V
    schema_v: Literal["mission_plan_draft_v1"]  # required: no default
    milestones: list[MilestoneDraft] = Field(min_length=1)
    risks: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_dag(self) -> MissionPlanDraft:
        validate_milestone_dag(self.milestones)
        return self


class MissionPlan(_Structured):
    """A compiled mission plan (schema ``mission_plan_v1``).

    A DAG of milestones with goals, rationales, dependency edges, DoD
    references and draft job outlines.  Validated on construction with the same
    discipline as ``FlightPlan._validate_dag``: no duplicate ids, no unknown
    dependencies, no cycles, hard milestone cap.
    """

    SCHEMA_V: ClassVar[str] = MISSION_PLAN_SCHEMA_V
    schema_v: Literal["mission_plan_v1"]  # required: no default
    milestones: list[Milestone] = Field(min_length=1)
    risks: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    #: True only when a provider produced the milestones.
    compiled: bool = False
    origin: MissionPlanOrigin = "deterministic"

    @model_validator(mode="after")
    def _validate_plan(self) -> MissionPlan:
        if self.compiled != (self.origin == "provider"):
            raise MissionPlanError(
                f"compiled={self.compiled} contradicts origin={self.origin!r} — "
                f"a deterministic plan may not be presented as compiled")
        validate_milestone_dag(self.milestones)
        return self

    @property
    def milestones_without_dod(self) -> tuple[str, ...]:
        """Ids of milestones that carry no Definition-of-Done reference yet."""
        return tuple(m.id for m in self.milestones if not m.dod_ref.strip())


def validate_milestone_dag(milestones: list[MilestoneDraft]) -> None:
    """Refuse a milestone list that is not a well-formed DAG.

    The same four rules ``FlightPlan._validate_dag`` enforces for task DAGs,
    applied to milestones: hard cap first (an over-cap plan is hallucinated
    scope and there is no point validating its edges), then duplicate ids,
    unknown dependencies, and cycles by depth-first search.
    """
    if len(milestones) > MAX_MISSION_MILESTONES:
        raise MissionPlanError(
            f"MissionPlan exceeds {MAX_MISSION_MILESTONES}-milestone cap "
            f"(got {len(milestones)}) — that is hallucinated scope, not a plan")

    ids: set[str] = set()
    for m in milestones:
        if m.id in ids:
            raise MissionPlanError(f"duplicate milestone id: {m.id!r}")
        ids.add(m.id)

    for m in milestones:
        for dep in m.depends_on:
            if dep not in ids:
                raise MissionPlanError(
                    f"milestone {m.id!r} depends on unknown id {dep!r}")
            if dep == m.id:
                raise MissionPlanError(
                    f"milestone {m.id!r} depends on itself")

    by_id = {m.id: m for m in milestones}
    visited: set[str] = set()
    path: set[str] = set()

    def _visit(mid: str) -> None:
        if mid in path:
            raise MissionPlanError(
                f"dependency cycle detected involving {mid!r}")
        if mid in visited:
            return
        path.add(mid)
        for dep in by_id[mid].depends_on:
            _visit(dep)
        path.discard(mid)
        visited.add(mid)

    for m in milestones:
        _visit(m.id)
