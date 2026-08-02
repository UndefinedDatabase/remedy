"""F069 T001 — compile a mission's prose goal into a MissionPlan.

A mission holds a long goal and nothing else.  :func:`compile_mission_plan` —
the feature file's ``compile(mission)`` — turns that prose into the structured
route the orchestrator loop follows: ordered milestones wired into a DAG, each
an OUTCOME rather than a step, each carrying draft job outlines.

The shape mirrors intake, the flight planner and the DoD compiler, because it
is the same problem one level up: one provider call through
``run_structured_call`` (schema-enforced, at most one parse retry), and an
honest deterministic fallback when there is no provider or the provider fails.
The prompt's repo facts come from the SHARED ``prompt_facts.repo_facts_block``
that the flight planner uses — not a second copy of it.

Two guarantees this module holds to, both pinned by tests:

* **Zero execution side effects.**  Compiling creates no jobs, starts no
  process and touches no worktree.  Remedy deliberately does NOT autostart a
  compiled milestone: a ``jobs_draft`` entry is an outline, and it becomes real
  work only through explicit continuation.  There is no code here that starts
  anything — that absence is the feature, not an oversight.
* **A fallback is never dressed up as a compiled plan.**  Without a provider
  the result is ONE milestone wrapping the whole goal, labeled
  ``compiled=False`` / ``origin="deterministic"``.  The schema refuses the
  dishonest combination, so the label cannot drift from the truth.

The per-milestone Definition of Done is compiled by the F061 compiler and
stored in ``dod_ref`` (T002).  There is no second DoD mechanism here (Rule A6);
until that hand-off runs, every ``dod_ref`` is empty and says so.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from packages.orchestration.mission_plan_schema import (
    MAX_MISSION_MILESTONES,
    MISSION_PLAN_DRAFT_SCHEMA_V,
    MISSION_PLAN_SCHEMA_V,
    Milestone,
    MissionPlan,
    MissionPlanDraft,
)
from packages.orchestration.prompt_facts import repo_facts_block
from packages.orchestration.structured_outputs import StructuredOutcome, run_structured_call

#: The id the deterministic fallback's single milestone carries.
DETERMINISTIC_MILESTONE_ID = "M001"

#: Recorded as the fallback milestone's rationale, so a reader of a persisted
#: plan sees WHY it has exactly one milestone without consulting this module.
DETERMINISTIC_RATIONALE = (
    "No provider produced a plan, so the whole mission goal is carried as one "
    "milestone. This is a degraded route, not a considered decomposition.")

#: How the fallback phrases its milestone. The mission goal is user prose and
#: may well read as a task list ("add X, fix Y") — which the outcome lint
#: rightly refuses. Wrapping it in an outcome sentence keeps the fallback
#: constructible for ANY goal, without editing what the user actually asked for.
_FALLBACK_GOAL_TEMPLATE = "The mission goal is met in full: {goal}"

#: How much of the goal a draft outline's title carries.
_MAX_TITLE_CHARS = 80

_MISSION_PROMPT_TEMPLATE = """\
You are compiling a mission plan. A MISSION is a long-lived goal that outlives
any single job. Break the goal below into the ordered milestones that reach it.

## Mission Goal
{goal}

## Repo Facts
{repo_facts}

## Rules
- A milestone is an OUTCOME, not a step: state what is TRUE once it is
  reached ("the payments API stays releasable"), never the actions taken to
  get there ("add tests, refactor the client"). A milestone phrased as a task
  list is rejected.
- Each milestone needs a unique id (e.g. "M001", "M002") with no whitespace.
- depends_on lists the milestone ids that must be reached first. No cycles.
- Maximum {max_milestones} milestones. If the goal seems to need more, the
  milestones are too small — raise their altitude instead.
- rationale says in one line why this milestone exists.
- jobs_draft is an OUTLINE of the work the milestone will probably need:
  {{"title": "...", "goal": "...", "est_band": "S|M|L|XL"}}. These are sketches
  for a human to read, NOT runnable jobs, and nothing starts them.
- risks lists what could make this mission fail.
- assumptions lists what you decided on your own because the goal did not say.
  Prefer conservative choices: an assumption keeps existing behavior or does
  nothing; it never deletes, overwrites or migrates.

Return ONLY a JSON object matching the {schema_v} schema.
"""


@dataclass
class MissionCompileResult:
    """Outcome of one mission compilation, provider path or fallback."""

    plan: MissionPlan
    #: ``"llm"`` when the provider produced the milestones, else
    #: ``"deterministic"``. Mirrors ``plan.origin``; kept for symmetry with
    #: IntakeResult / FlightPlanResult / DoDCompileResult.
    source: str
    #: Why the provider path was not used, when it was not.
    error_hint: str = ""
    calls: int = 0
    call_log: list[dict[str, Any]] = field(default_factory=list)


def mission_goal(mission: Any) -> str:
    """The goal text of a mission, however the caller happens to hold it.

    Three shapes reach this compiler and all three must read the same way: the
    :class:`~packages.orchestration.mission_state.Mission` record (a ``goal``
    attribute), the record as loaded JSON (a ``"goal"`` key), and the bare goal
    text. Reading only the attribute would silently stringify a dict INTO the
    prompt — a plan compiled from ``{'goal': ...}`` rather than from the goal.
    """
    goal = getattr(mission, "goal", None)
    if goal is None and isinstance(mission, dict):
        goal = mission.get("goal")
    if goal is None:
        goal = mission
    return str(goal or "").strip()


def build_mission_prompt(goal: str, *, project_facts: str = "") -> str:
    """The provider prompt for one mission goal.

    ``project_facts`` defaults to the SHARED repo-facts block — the same one
    the flight planner puts in front of its provider. A caller that already
    knows the project's shape passes it instead of paying for a second listing.
    """
    return _MISSION_PROMPT_TEMPLATE.format(
        goal=str(goal).strip(),
        repo_facts=project_facts or repo_facts_block(),
        max_milestones=MAX_MISSION_MILESTONES,
        schema_v=MISSION_PLAN_DRAFT_SCHEMA_V,
    )


def deterministic_mission_plan(goal: str) -> MissionPlan:
    """The honest no-provider plan: ONE milestone wrapping the whole goal.

    Coarser than a compiled plan — it decomposes nothing — but it is real, it
    validates, and it is labeled for what it is: ``compiled=False`` /
    ``origin="deterministic"``. The loop can still function on it, degraded.
    """
    text = " ".join(str(goal).split())
    title = text[:_MAX_TITLE_CHARS] or "the mission goal"
    return MissionPlan(
        schema_v=MISSION_PLAN_SCHEMA_V,
        milestones=[Milestone(
            id=DETERMINISTIC_MILESTONE_ID,
            goal=_FALLBACK_GOAL_TEMPLATE.format(goal=text),
            rationale=DETERMINISTIC_RATIONALE,
            depends_on=[],
            # One outline, restating the goal. Not a decomposition and not a
            # job — an XL sketch of "all of it", which is the honest estimate
            # when nothing has reasoned about the goal yet.
            jobs_draft=[{"title": title, "goal": text, "est_band": "XL"}],
        )],
        compiled=False,
        origin="deterministic",
    )


def compile_mission_plan(
    mission: Any,
    call_fn: Callable[[str, int], str] | None = None,
    *,
    on_call: Callable[[int, str, bool, str], None] | None = None,
    project_facts: str = "",
) -> MissionCompileResult:
    """Compile a mission's goal into a MissionPlan.  Starts nothing.

    ``mission`` is a :class:`~packages.orchestration.mission_state.Mission`, a
    loaded mission record, or the goal text itself — see :func:`mission_goal`.
    ``call_fn is None`` — or any provider failure, or an unparseable answer —
    yields the deterministic fallback rather than an exception or an empty
    plan: a mission without a provider still gets a real route.

    Compiling has NO side effects: nothing is persisted here, no job is
    created, no process starts. Persistence and the per-milestone DoD hand-off
    are the caller's step (T002).
    """
    goal = mission_goal(mission)
    if not goal:
        raise ValueError("a mission plan needs a goal to compile")

    if call_fn is None:
        return _fallback(goal, hint="no provider")

    try:
        outcome: StructuredOutcome = run_structured_call(
            MissionPlanDraft,
            build_mission_prompt(goal, project_facts=project_facts),
            call_fn,
            on_call=on_call,
            allow_parse_retry=True,
        )
    except Exception as exc:
        return _fallback(goal, hint=f"provider error: {exc}")

    if not outcome.ok:
        result = _fallback(goal, hint=outcome.hint)
        result.calls = outcome.calls
        result.call_log = outcome.call_log
        return result

    assert isinstance(outcome.value, MissionPlanDraft)

    try:
        plan = MissionPlan(
            schema_v=MISSION_PLAN_SCHEMA_V,
            # dod_ref stays empty here: the DoD hand-off is a separate step,
            # and a plan that claimed a reference it does not have would be a
            # lie the persistence layer would then carry forever.
            milestones=[Milestone(**draft.model_dump())
                        for draft in outcome.value.milestones],
            risks=list(outcome.value.risks),
            assumptions=list(outcome.value.assumptions),
            compiled=True,
            origin="provider",
        )
    except ValueError as exc:
        # The draft validated but the compiled artifact did not — treat it as
        # the parse-class failure it is rather than raising into the caller.
        result = _fallback(goal, hint=f"invalid compiled plan: {exc}")
        result.calls = outcome.calls
        result.call_log = outcome.call_log
        return result

    return MissionCompileResult(
        plan=plan,
        source="llm",
        calls=outcome.calls,
        call_log=outcome.call_log,
    )


def _fallback(goal: str, *, hint: str) -> MissionCompileResult:
    return MissionCompileResult(
        plan=deterministic_mission_plan(goal),
        source="deterministic",
        error_hint=hint,
    )
