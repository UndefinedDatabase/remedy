"""F045 T002/T003 — materialize a loop as work carrying ``loop_ref``.

A loop is declarative configuration (:mod:`packages.orchestration.loop_spec`,
T001). This module turns one into a NORMAL job — the same shape
``remedy job create`` + ``remedy job plan`` produce, and the same shape
``long_run_executor.queued_entry_to_job`` produces for a queue entry. That
similarity is the point: a loop-materialized job must be indistinguishable from
a queue-materialized one except for its provenance.

APPROVAL SEMANTICS, the load-bearing part of T002: the job stops at PLANNED.
Nothing here executes a task, approves a plan, or implies ``--yes``.
``LoopSpec.unattended`` is RECORDED in metadata so it is auditable, and it
changes NOTHING about the job's state — a loop reaches the operator's approval
gate exactly like a typed goal.

DECISION F045 D3 — T002 materializes the JOB action; action dispatch is T003's.
:func:`loop_to_job` requires ``action.kind == "job"``. It makes no claim about
the mission action at all: dispatch across action kinds belongs to ``run_loop``
in T003, together with the CLI, the last-run display and the end-to-end
fixture. See ``.agent/decisions.md``.

F045 T003 — that dispatch lives HERE, in :func:`run_loop`, which routes on
``action.kind``. :func:`loop_to_job` stays exactly the job-kind path it always
was. DECISION F045 D5 governs the mission path's provenance: ``loop_ref`` rides
on the JOB, never on the ``Mission`` record, and the mission stays reachable
from that same job through ``metadata["mission_id"]``.

Remedy deliberately does not schedule, watch or repeat loops here. A loop whose
trigger is inert (``LoopSpec.is_inert``) still materializes on demand;
:func:`run_loop` says so through ``loop_spec.INERT_TRIGGER_NOTICE`` rather than
pretending the trigger fired. Displaying it is the CLI's job in T003.
"""
from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from packages.core.models import Job, JobBudgets, RunState
from packages.orchestration.loop_spec import (
    INERT_TRIGGER_NOTICE,
    LOOP_TEMPLATE_VARS,
    LoopBudgets,
    LoopSpec,
)

#: Metadata key carrying the originating loop's name — the provenance line that
#: makes a loop-materialized job traceable in evidence and reports.
LOOP_REF_METADATA_KEY = "loop_ref"

#: Metadata key recording the loop's ``unattended`` flag for audit. It is a
#: RECORD only: it never approves anything and never changes the job's state.
LOOP_UNATTENDED_METADATA_KEY = "loop_unattended"

#: Matches one ``{placeholder}`` at a time; nested braces are not a template.
#: Mirrors ``loop_spec._TEMPLATE_VAR_RE`` so both ends agree on what a
#: placeholder IS without importing a private name across modules.
_TEMPLATE_VAR_RE = re.compile(r"\{([^{}]*)\}")


class LoopRunError(ValueError):
    """Materializing a loop failed. ``str()`` is the full, user-facing message."""


# WHY: templates are operator-authored text, so rendering must never leak a
# stdlib exception; only the two documented variables are substituted.
def render_goal_template(template: str, *, project: str, date: str) -> str:
    """Substitute ONLY ``{project}`` and ``{date}`` in *template*.

    Any other placeholder is already a VALIDATION failure in
    :mod:`packages.orchestration.loop_spec`, so reaching one here is a
    programming error: this raises :class:`LoopRunError` naming the variable
    rather than emitting a half-rendered prompt.

    ``str.format`` is deliberately not used — a stray brace in an operator's
    template must not raise ``KeyError`` from deep inside the stdlib.
    """
    values = {"project": project, "date": date}
    unknown = [var for var in _TEMPLATE_VAR_RE.findall(template)
               if var not in LOOP_TEMPLATE_VARS]
    if unknown:
        raise LoopRunError(
            f"goal_template references undefined variable '{unknown[0]}'; "
            f"only {sorted(LOOP_TEMPLATE_VARS)} are substituted")
    return _TEMPLATE_VAR_RE.sub(lambda m: values[m.group(1)], template)


# WHY: the loop and job budget field names are identical on purpose; this is the
# one place the deadline's string/datetime difference is bridged.
def loop_budgets_to_job_budgets(budgets: LoopBudgets | None) -> JobBudgets | None:
    """Map a ``LoopBudgets`` onto :class:`packages.core.models.JobBudgets`.

    The four numeric field names are IDENTICAL on both sides and are copied
    straight across. The one difference: ``LoopBudgets.deadline`` is a validated
    tz-aware ISO string while ``JobBudgets.deadline`` is a ``datetime``.

    Returns ``None`` when the loop has no budgets, and ``None`` when every field
    is ``None``, so a budget-less loop produces a job whose ``budgets`` is
    ``None`` exactly as ``remedy job create`` does.

    Ranges are NOT re-validated here: ``loop_spec`` already refused
    non-positive values and ``JobBudgets`` has its own validator. A third copy
    would be exactly the drift DECISION F045 D2 avoids.
    """
    if budgets is None:
        return None
    fields = {
        "max_total_tokens": budgets.max_total_tokens,
        "max_provider_calls": budgets.max_provider_calls,
        "max_wall_clock_minutes": budgets.max_wall_clock_minutes,
        "max_cost_usd": budgets.max_cost_usd,
    }
    deadline = budgets.deadline
    if all(value is None for value in fields.values()) and deadline is None:
        return None
    if deadline is not None:
        try:
            parsed_deadline = datetime.fromisoformat(deadline.strip())
        except (AttributeError, TypeError, ValueError) as exc:
            raise LoopRunError(f"budgets.deadline is not an ISO 8601 timestamp: "
                               f"{deadline!r}") from exc
    else:
        parsed_deadline = None
    return JobBudgets(deadline=parsed_deadline, **fields)


# WHY: one place builds a loop's job, so the job and mission paths cannot drift
# apart in what provenance they record.
def _materialize_loop_job(spec: LoopSpec, prompt: str, project_id: str, *,
                          extra_metadata: Mapping[str, object] | None = None,
                          mission: str | None = None,
                          save: Callable[[Job], None] | None = None,
                          root: Path | None = None) -> Job:
    """Build, plan and persist the job a loop firing produces.

    The three metadata keys T002 established are written first; *extra_metadata*
    is merged AFTER them, which is how the mission path adds its own link keys
    without either path re-implementing the provenance record.

    *mission* is set in the ``Job(...)`` constructor, so it is in place before
    ``plan_job`` and before the save and the PERSISTED record carries it — not
    only the in-memory object the caller happens to hold.

    An explicit *save* overrides *root* entirely and is called with the job
    alone, because such a caller has taken responsibility for where the job
    goes; only the DEFAULT save consults *root* (DECISION F045 D6).
    """
    from packages.orchestration.job_runner import plan_job
    from packages.orchestration.storage import save_job as _save_job

    metadata: dict[str, object] = {
        "project_id": project_id,
        LOOP_REF_METADATA_KEY: spec.name,
        LOOP_UNATTENDED_METADATA_KEY: spec.unattended,
    }
    if extra_metadata:
        metadata.update(extra_metadata)
    job = Job(
        name=prompt[:50],
        user_prompt=prompt,
        mission=mission,
        state=RunState.PENDING,
        metadata=metadata,
        project_id=project_id,
        budgets=loop_budgets_to_job_budgets(spec.budgets),
    )
    plan_job(job)
    if save is not None:
        save(job)
    else:
        _save_job(job, root)
    return job


# WHY: the single entry point from a declarative loop to the normal job
# pipeline; every loop_ref in evidence originates here.
def loop_to_job(spec: LoopSpec, *, project_id: str, date: str | None = None,
                save: Callable[[Job], None] | None = None,
                root: Path | None = None) -> Job:
    """Turn a job-action loop into a NORMAL job, planned and persisted.

    Deliberately the same shape as
    ``long_run_executor.queued_entry_to_job``, and deliberately no further: the
    job stops at PLANNED. Nothing here executes a task, approves a plan or
    implies ``--yes``. ``spec.unattended`` is recorded under
    :data:`LOOP_UNATTENDED_METADATA_KEY` so it is auditable, and it changes
    NOTHING about the job's state — a loop reaches the operator's approval gate
    exactly like a typed goal.

    *date* defaults to today's UTC date as ``YYYY-MM-DD``. Callers that must be
    clock-independent (every test here) pass it explicitly.

    *root* isolates the JOB STORE this firing writes to, so the job action path
    isolates exactly as the mission path already does.

    Raises :class:`LoopRunError` for any action kind other than ``job``:
    dispatch across kinds is ``run_loop``'s in T003 (DECISION F045 D3).
    """
    if spec.action.kind != "job":
        raise LoopRunError(
            f"loop '{spec.name}': loop_to_job materializes a job action, got "
            f"action.kind='{spec.action.kind}'; action dispatch is run_loop's "
            f"(DECISION F045 D3)")
    if not spec.action.goal_template:
        raise LoopRunError(
            f"loop '{spec.name}': action.goal_template is required for a job action")

    run_date = date if date is not None else datetime.now(timezone.utc).strftime("%Y-%m-%d")
    prompt = render_goal_template(spec.action.goal_template,
                                  project=project_id, date=run_date)
    return _materialize_loop_job(spec, prompt, project_id, save=save, root=root)


# WHY: one firing produces a job, maybe a mission, and maybe an honest notice;
# returning all three keeps the caller from re-deriving any of them.
@dataclass(frozen=True)
class LoopRunOutcome:
    """What one loop firing produced.

    ``mission_id`` is ``None`` for a job-action loop; ``notice`` is ``None``
    unless the trigger is inert, in which case it is ``INERT_TRIGGER_NOTICE``.
    """

    job: Job
    mission_id: str | None = None
    notice: str | None = None


# WHY: the one dispatch point from a declarative loop to real work; every action
# kind is routed here and nowhere else.
def run_loop(spec: LoopSpec, *, project_id: str, date: str | None = None,
             save: Callable[[Job], None] | None = None,
             root: Path | None = None) -> LoopRunOutcome:
    """Materialize *spec* according to its ``action.kind``.

    APPROVAL SEMANTICS, unchanged from T002 and load-bearing: BOTH paths stop at
    PLANNED. Nothing here executes a task, approves a plan or implies ``--yes``,
    and ``spec.unattended`` is still only RECORDED — a loop reaches the
    operator's approval gate exactly like a typed goal, whichever kind it is.

    The run date is computed ONCE — *date* when given, else today's UTC date as
    ``YYYY-MM-DD``, the same default :func:`loop_to_job` uses — and passed down,
    so the job and the mission goal can never be rendered against two dates.

    *root* isolates the WHOLE run — the job store, the mission record and the
    job-to-mission link all land under it, so no half of a firing escapes it.

    An inert trigger (``LoopSpec.is_inert``) blocks nothing: the loop still
    materializes on demand and the outcome carries ``INERT_TRIGGER_NOTICE``, so
    a caller can say so honestly instead of pretending the trigger fired.

    Raises :class:`LoopRunError` for an action kind this module does not know,
    and for a mission action with no ``action.mission`` template.
    """
    run_date = date if date is not None else datetime.now(timezone.utc).strftime("%Y-%m-%d")
    notice = INERT_TRIGGER_NOTICE if spec.is_inert else None

    if spec.action.kind == "job":
        job = loop_to_job(spec, project_id=project_id, date=run_date, save=save,
                          root=root)
        return LoopRunOutcome(job=job, mission_id=None, notice=notice)

    if spec.action.kind == "mission":
        # DECISION F045 D5: loop_ref rides on the JOB, not on the Mission.
        from packages.orchestration.mission_state import (
            MISSION_ROLE_INITIAL,
            create_mission,
            link_job_to_mission,
        )

        if not spec.action.mission:
            raise LoopRunError(
                f"loop '{spec.name}': action.mission is required for a mission action")
        goal = render_goal_template(spec.action.mission,
                                    project=project_id, date=run_date)
        mission = create_mission(project_id, goal, root=root)
        job = _materialize_loop_job(
            spec, goal, project_id,
            extra_metadata={"mission_id": mission.id,
                            "mission_role": MISSION_ROLE_INITIAL},
            mission=mission.goal,
            save=save, root=root)
        link_job_to_mission(project_id, mission.id, str(job.id),
                            MISSION_ROLE_INITIAL, root=root)
        return LoopRunOutcome(job=job, mission_id=mission.id, notice=notice)

    raise LoopRunError(
        f"loop '{spec.name}': unsupported action.kind='{spec.action.kind}'")


# WHY: the last-run display reads provenance out of the job store, so the scan
# for a loop's own runs lives next to the key that records them.
def last_run_for_loop(name: str, *, root: Path | None = None) -> Job | None:
    """The most recent job carrying ``loop_ref == name``, or ``None``.

    Reads the store through ``storage.list_jobs_safe``, which ALREADY sorts by
    ``created_at`` descending, so the FIRST match is the most recent — no
    ``max()`` and no re-sort. That helper SKIPS unreadable job files, so a loop
    whose only run will not parse reports ``None`` rather than a wrong run.
    """
    from packages.orchestration.storage import list_jobs_safe

    jobs, _degraded, _skipped = list_jobs_safe(root)
    for job in jobs:
        if job.metadata.get(LOOP_REF_METADATA_KEY) == name:
            return job
    return None
