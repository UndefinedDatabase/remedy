"""The orchestrator loop's dispatch path: one ``dispatch_job`` move made into a job that runs.

F301's structural step (DECISION F301 D1): ``execute_move`` in
``packages/orchestration/orchestrator_loop.py`` hands its ``dispatch_job`` branch to
:func:`dispatch_milestone_job` unchanged, along the boundary
``docs/system/structure-ledger-v1.md`` writes for it. The loop's own helpers are read from
the loop's module at call time, so a name a test replaces there is the name this path calls.
F301 T003 adds the mission's upkeep: when an upkeep job is due, :func:`run_upkeep_job` runs it
in place of the dispatch.
"""
from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any


def dispatch_milestone_job(project_id: str, mission_id: str, payload: dict[str, Any], *,
                           root: Path | None = None,
                           dispatch: Callable[..., Any] | None = None,
                           execute: Callable[[Any], Any] | None = None,
                           now: datetime | None = None) -> Any:
    """Create, approve, bind and RUN the job one ``dispatch_job`` move asks for.

    The job comes from ``dispatch`` or ``mission_state.continue_mission``; its milestone's
    DoD, contract slice, repository grant and milestone key are attached before it runs
    through ``execute`` or ``execute_dispatched_job``, and its gate result then decides the
    milestone's contract criteria. Answers the loop's ``MoveOutcome``. When the mission's upkeep
    job is due, that job runs instead, through :func:`run_upkeep_job`.
    """
    from packages.orchestration import orchestrator_loop as loop
    from packages.orchestration.mission_state import continue_mission
    from packages.orchestration.mission_upkeep import make_upkeep_job_if_due

    # DECISION F301 D1 (9): when upkeep is due, its job runs in place of this dispatch. The loop
    # never skips one; the model is asked again at its next iteration.
    upkeep = make_upkeep_job_if_due(project_id, mission_id, root, now=now)
    if upkeep.job is not None:
        return run_upkeep_job(upkeep, payload["milestone_id"], execute=execute)
    create = dispatch or continue_mission
    job = create(project_id, mission_id, payload["step"], root=root,
                 now=now)
    approved = loop._auto_approve_if_gated(job)
    detail = f"job {job.job_id} dispatched for {payload['milestone_id']}"
    if approved:
        detail += " (plan auto-approved, audited)"
    from packages.orchestration.mission_contract import (
        JOB_MILESTONE_KEY,
        grant_contract_job_repository,
        merge_contract_slice_into_dod,
        record_contract_results,
        record_job_milestone,
    )
    from packages.orchestration.mission_state import load_mission as _load

    # R-0188: give the job its milestone's DoD before it runs, or the gate
    # has nothing to evaluate when it finishes.
    current = _load(project_id, mission_id, root)
    if loop.attach_milestone_dod(project_id, mission_id, current,
                                 payload["milestone_id"], str(job.job_id), root):
        detail += "; DoD attached"
    # DECISION F269 D4 (3): the job's DoD carries its contract slice, so
    # the job's own gate decides the criteria it serves.
    merge_contract_slice_into_dod(current, payload["milestone_id"],
                                  str(job.job_id))
    # DECISION F269 D7: the contract binds the job to its repository and
    # grants it; the in-memory job carries the same values, as below.
    granted = grant_contract_job_repository(current, str(job.job_id), root)
    if granted and isinstance(getattr(job, "metadata", None), dict):
        job.metadata.update(granted)
    # DECISION F269 D3 (1): the job records the milestone it serves, so its
    # contract slice can be derived. The in-memory job is the one the
    # executor saves next, so it carries the same key.
    if record_job_milestone(str(job.job_id), payload["milestone_id"], root):
        metadata = getattr(job, "metadata", None)
        if isinstance(metadata, dict):
            metadata[JOB_MILESTONE_KEY] = payload["milestone_id"]
    run = (execute or loop.execute_dispatched_job)(job)
    # DECISION F269 D4 (4): the job's gate result decides its slice criteria.
    record_contract_results(project_id, mission_id, str(job.job_id),
                            payload["milestone_id"], root)
    return loop.MoveOutcome(status="dispatched",
                            detail=detail + loop.execution_detail(run),
                            job_id=str(job.job_id))


def run_upkeep_job(upkeep: Any, milestone_id: str, *,
                   execute: Callable[[Any], Any] | None = None) -> Any:
    """Approve and RUN the upkeep job made in place of a dispatch for ``milestone_id``.

    It serves no milestone, so no DoD, contract slice, repository grant or milestone key is
    attached and no contract result is recorded; and its detail names no gate, so the loop never
    reads it as the milestone's blocked completion. Answers the outcome ``upkeep_dispatched``.
    """
    from packages.orchestration import orchestrator_loop as loop

    job = upkeep.job
    approved = loop._auto_approve_if_gated(job)
    count = upkeep.cadence.completed
    detail = (f"upkeep job {job.job_id} dispatched in place of {milestone_id}'s step after {count} "
              f"completed job{'' if count == 1 else 's'} (DECISION F301 D1)")
    if approved:
        detail += " (plan auto-approved, audited)"
    run = (execute or loop.execute_dispatched_job)(job)
    detail += (f"; executed: terminal={getattr(run, 'terminal_status', '')}"
               f" job_status={getattr(run, 'job_status', '')}")
    return loop.MoveOutcome(status="upkeep_dispatched", detail=detail, job_id=str(job.job_id))
