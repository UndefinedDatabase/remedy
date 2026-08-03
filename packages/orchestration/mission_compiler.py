"""F069 — compile a mission's prose goal into a MissionPlan.

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
stored in ``dod_ref`` (:func:`attach_milestone_dods`).  There is no second DoD
mechanism here (Rule A6); until that hand-off runs, every ``dod_ref`` is empty
and says so.  ``compile_mission_plan`` itself writes NOTHING — persistence,
the DoD files and the rendered ``mission_plan.md`` are separate, explicit calls,
which is what keeps "compiling starts nothing" a property rather than a habit.
"""
from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from packages.orchestration.dod_compiler import DoDCompileResult, compile_dod
from packages.orchestration.mission_plan_schema import (
    MAX_MILESTONE_DRAFT_JOBS,
    MAX_MISSION_MILESTONES,
    MISSION_PLAN_DRAFT_SCHEMA_V,
    MISSION_PLAN_SCHEMA_V,
    Milestone,
    MissionPlan,
    MissionPlanDraft,
)
from packages.orchestration.prompt_facts import repo_facts_block
from packages.orchestration.schemas.models import FLIGHT_PLAN_SCHEMA_V, FlightPlan
from packages.orchestration.storage import _atomic_write_job as _atomic_write
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
  for a human to read, NOT runnable jobs, and nothing starts them. At most
  {max_draft_jobs} per milestone, and every title and goal must be non-empty —
  a milestone needing more outlines than that is a project, not a milestone.
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


@dataclass
class MissionPlanOutcome:
    """What one ``remedy mission plan`` run produced (T003)."""

    mission: Any
    plan: MissionPlan
    #: 1 for the first compilation, 2 for the first recompile, and so on.
    version: int
    source: str
    error_hint: str = ""
    plan_path: Path | None = None
    evidence_dir: Path | None = None


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
        max_draft_jobs=MAX_MILESTONE_DRAFT_JOBS,
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


# ---------------------------------------------------------------------------
# T002 — the per-milestone DoD hand-off
# ---------------------------------------------------------------------------

#: The id the synthetic "milestone reached" task carries inside the per-
#: milestone flight-plan VIEW. It never becomes a real task; see
#: :func:`milestone_flight_plan`.
MILESTONE_OUTCOME_TASK_SUFFIX = "-DONE"

#: Band for that synthetic task. A milestone outcome is never small, and the
#: band is required by the flight-plan schema — it is not an estimate anyone
#: acts on, because nothing runs this view.
_OUTCOME_TASK_BAND = "L"


def milestone_dod_filename(milestone_id: str) -> str:
    """The file one milestone's compiled DoD is written to, inside the evidence area."""
    return f"dod_{milestone_id}.json"


def milestone_flight_plan(milestone: Milestone) -> FlightPlan:
    """A per-milestone flight plan — the VIEW the F061 DoD compiler consumes.

    Rule A6 says the DoD compiler is the only DoD mechanism, and that compiler
    takes ``(intake, FlightPlan)``. A milestone is not a flight plan, so one is
    projected from it: one task per draft job outline, plus a final task whose
    acceptance line IS the milestone's own outcome and which depends on all of
    them.

    This projection is NEVER persisted and never scheduled. It exists for the
    length of one ``compile_dod`` call, so that the milestone's DoD is compiled
    by the existing mechanism instead of by a second one written here.
    """
    tasks: list[dict[str, Any]] = []
    for index, draft in enumerate(milestone.jobs_draft, start=1):
        tasks.append({
            "id": f"{milestone.id}-J{index:03d}",
            "title": draft.title,
            "goal": draft.goal,
            "acceptance": [draft.goal],
            "depends_on": [],
            "est_tokens_band": draft.est_band,
            "files_hint": [],
        })
    tasks.append({
        "id": f"{milestone.id}{MILESTONE_OUTCOME_TASK_SUFFIX}",
        "title": f"Milestone {milestone.id} reached",
        "goal": milestone.goal,
        "acceptance": [milestone.goal],
        "depends_on": [t["id"] for t in tasks],
        "est_tokens_band": _OUTCOME_TASK_BAND,
        "files_hint": [],
    })
    return FlightPlan.model_validate({
        "schema_v": FLIGHT_PLAN_SCHEMA_V,
        "tasks": tasks,
    })


def compile_milestone_dod(
    goal: str,
    milestone: Milestone,
    call_fn: Callable[[str, int], str] | None = None,
    *,
    on_call: Callable[[int, str, bool, str], None] | None = None,
) -> DoDCompileResult:
    """Compile ONE milestone's Definition of Done through the F061 compiler.

    There is no second DoD mechanism here (Rule A6): this builds the intake and
    the flight-plan view and hands both to ``compile_dod``, which owns the
    provider call, the fallback and the traceability rule.
    """
    intake = {
        "goal": milestone.goal,
        "mission_goal": goal,
        "context_refs": [],
        "constraints": [],
        "acceptance_hints": [d.goal for d in milestone.jobs_draft],
    }
    return compile_dod(intake, milestone_flight_plan(milestone), call_fn,
                       on_call=on_call)


def attach_milestone_dods(
    plan: MissionPlan,
    *,
    goal: str,
    evidence_dir: Path,
    call_fn: Callable[[str, int], str] | None = None,
) -> MissionPlan:
    """Compile a DoD for every milestone, write it, and fill in ``dod_ref``.

    Each DoD lands in ``evidence_dir`` as ``dod_<milestone id>.json`` and the
    milestone's ``dod_ref`` records that filename — RELATIVE, so a mission
    whose data root moves keeps a reference that still resolves.

    Writing evidence is not execution: no job is created and nothing starts.
    """
    evidence_dir.mkdir(parents=True, exist_ok=True)
    milestones: list[Milestone] = []
    for ms in plan.milestones:
        result = compile_milestone_dod(goal, ms, call_fn)
        filename = milestone_dod_filename(ms.id)
        _atomic_write(
            evidence_dir / filename,
            json.dumps(result.dod.model_dump(), indent=2, sort_keys=True))
        milestones.append(ms.model_copy(update={"dod_ref": filename}))
    return plan.model_copy(update={"milestones": milestones})


# ---------------------------------------------------------------------------
# T002 — rendering
# ---------------------------------------------------------------------------

MISSION_PLAN_FILENAME = "mission_plan.md"


def render_mission_plan_md(plan: MissionPlan, goal: str = "") -> str:
    """Render a MissionPlan to deterministic, stably ordered markdown.

    Same shape as ``flight_plan.render_plan_md``: no clock, no randomness, no
    disk — the same plan renders to the same bytes every time.
    """
    lines: list[str] = ["# Mission Plan", ""]
    lines.append(f"Schema: {plan.schema_v}")
    lines.append(f"Milestones: {len(plan.milestones)}")
    lines.append(f"Origin: {plan.origin}"
                 f"{'' if plan.compiled else ' (no provider — degraded route)'}")
    lines.append("")

    if goal:
        lines.append("## Goal")
        lines.append("")
        lines.append(" ".join(str(goal).split()))
        lines.append("")

    lines.append("## Milestones")
    lines.append("")
    for index, ms in enumerate(plan.milestones, 1):
        deps = ", ".join(ms.depends_on) if ms.depends_on else "none"
        lines.append(f"### {index}. {ms.id}")
        lines.append("")
        lines.append(f"**Outcome:** {ms.goal}")
        lines.append(f"**Depends on:** {deps}")
        lines.append(f"**DoD:** {ms.dod_ref or 'not compiled yet'}")
        if ms.rationale:
            lines.append(f"**Why:** {ms.rationale}")
        lines.append("")
        if ms.jobs_draft:
            lines.append("**Draft jobs** — outlines only; nothing here is "
                         "runnable and nothing starts on its own:")
            for draft in ms.jobs_draft:
                lines.append(f"- [{draft.est_band}] {draft.title} — {draft.goal}")
            lines.append("")

    lines.append("## Risks")
    lines.append("")
    if plan.risks:
        for risk in plan.risks:
            lines.append(f"- {risk}")
    else:
        lines.append("None recorded.")
    lines.append("")

    lines.append("## Assumptions")
    lines.append("")
    if plan.assumptions:
        for assumption in plan.assumptions:
            lines.append(f"- {assumption}")
    else:
        lines.append("None recorded.")
    lines.append("")
    return "\n".join(lines)


def write_mission_plan_md(plan: MissionPlan, evidence_dir: Path,
                          goal: str = "", version: int = 1) -> Path:
    """Write the rendered plan into the mission's evidence area.

    Prior versions are KEPT, exactly as ``flight_plan.write_plan_md`` keeps
    ``plan.md`` / ``plan_v2.md``: a recompile must never destroy the plan a
    human already read and acted on.
    """
    evidence_dir.mkdir(parents=True, exist_ok=True)
    filename = (MISSION_PLAN_FILENAME if version == 1
                else f"mission_plan_v{version}.md")
    path = evidence_dir / filename
    path.write_text(render_mission_plan_md(plan, goal), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# T003 — planning a persisted mission: versioning and the in-progress refusal
# ---------------------------------------------------------------------------

#: Keys the PERSISTED plan body carries beyond the model's own fields. The
#: flight-plan replan precedent (``flight_plan.replan``) established this
#: spelling, and reusing it means one versioning convention in the codebase
#: rather than two.
PLAN_VERSIONS_KEY = "_versions"
PLAN_VERSION_KEY = "_version"


class MissionPlanInProgressError(Exception):
    """A recompile was refused because work on the current plan has begun."""


def mission_plan_of(mission: Any) -> MissionPlan | None:
    """The MissionPlan persisted on a mission record, or None.

    The persisted body carries the versioning keys alongside the model's own
    fields, and the model forbids unknown fields — so they are stripped here,
    in the one place that knows they exist.
    """
    body = getattr(mission, "mission_plan", None)
    if not isinstance(body, dict) or not body:
        return None
    return MissionPlan.model_validate(
        {k: v for k, v in body.items() if not k.startswith("_")})


def plan_version_of(mission: Any) -> int:
    """Which version the persisted plan is, or 0 when there is none."""
    body = getattr(mission, "mission_plan", None)
    if not isinstance(body, dict) or not body:
        return 0
    return int(body.get(PLAN_VERSION_KEY, 1))


def milestones_in_progress(mission: Any) -> tuple[str, ...]:
    """Which milestones of the persisted plan count as already in progress.

    THE RULE, stated where it lives: a milestone counts as in progress as soon
    as any real job attributable to it exists on the mission record.

    A mission record attributes a job to the MISSION, not to a milestone —
    ``MissionJobLink`` carries a job id, a role and a timestamp, and nothing
    else.  With no per-milestone attribution available, the conservative
    reading is the only honest one: once ANY job is linked to the mission,
    every milestone of its current plan is treated as in progress.  Adding a
    milestone id to the link would mean changing job creation, which this
    feature must not touch.

    Erring this way costs a refused recompile; erring the other way would
    silently rewrite the plan under work already running.  A mission with no
    plan yet has no milestones, so nothing is in progress and the FIRST
    compilation is always allowed.
    """
    plan = mission_plan_of(mission)
    if plan is None or not getattr(mission, "job_links", ()):
        return ()
    return tuple(m.id for m in plan.milestones)


def plan_mission(
    project_id: str,
    mission_id: str,
    call_fn: Callable[[str, int], str] | None = None,
    *,
    root: Path | None = None,
    on_call: Callable[[int, str, bool, str], None] | None = None,
) -> MissionPlanOutcome:
    """Compile (or recompile) a mission's plan, persist it, render it.

    A recompile KEEPS every prior version — the old body moves into
    ``_versions`` and the previous ``mission_plan.md`` stays on disk beside the
    new ``mission_plan_v<n>.md``, exactly as a flight-plan replan keeps
    ``plan.md``.  A plan a human already read and acted on is never destroyed.

    Recompiling is REFUSED once any milestone is in progress
    (:func:`milestones_in_progress`): rewriting the route under running work
    would leave that work serving a plan that no longer exists.

    Nothing here starts anything.  It compiles, it writes evidence, and it
    updates one record.
    """
    from packages.orchestration.mission_state import (
        load_mission,
        mission_evidence_dir,
        set_mission_plan,
    )

    mission = load_mission(project_id, mission_id, root)

    in_progress = milestones_in_progress(mission)
    if in_progress:
        raise MissionPlanInProgressError(
            f"mission {mission.id} cannot be replanned: "
            f"{len(in_progress)} milestone(s) are already in progress "
            f"({', '.join(in_progress)}) because "
            f"{len(mission.job_links)} job(s) are linked to this mission. "
            f"Start a new mission for a different route, or achieve/abandon "
            f"this one (remedy mission achieve|abandon {mission.id[:12]}).")

    result = compile_mission_plan(mission, call_fn, on_call=on_call)
    evidence_dir = mission_evidence_dir(project_id, mission.id, root)
    plan = attach_milestone_dods(
        result.plan, goal=mission.goal, evidence_dir=evidence_dir,
        call_fn=call_fn)

    previous = mission.mission_plan if isinstance(mission.mission_plan, dict) else None
    versions = list((previous or {}).get(PLAN_VERSIONS_KEY, []))
    if previous:
        versions.append(previous)
    version = len(versions) + 1

    body = plan.model_dump()
    body[PLAN_VERSIONS_KEY] = versions
    body[PLAN_VERSION_KEY] = version

    path = write_mission_plan_md(plan, evidence_dir, mission.goal, version=version)
    updated = set_mission_plan(project_id, mission.id, body, root)

    return MissionPlanOutcome(
        mission=updated,
        plan=plan,
        version=version,
        source=result.source,
        error_hint=result.error_hint,
        plan_path=path,
        evidence_dir=evidence_dir,
    )
