"""The orchestrator loop's dispatch path: one ``dispatch_job`` move made into a job that runs.

F301's structural step (DECISION F301 D1): ``execute_move`` in
``packages/orchestration/orchestrator_loop.py`` hands its ``dispatch_job`` branch to
:func:`dispatch_milestone_job` unchanged, along the boundary
``docs/system/structure-ledger-v1.md`` writes for it. The loop's own helpers are read from
the loop's module at call time, so a name a test replaces there is the name this path calls.
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
    milestone's contract criteria. Answers the loop's ``MoveOutcome``.
    """
    from packages.orchestration import orchestrator_loop as loop
    from packages.orchestration.mission_state import continue_mission

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
