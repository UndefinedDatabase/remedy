"""How a run of a job ends once its task loop is over (amend1015 Phase 1.2, DECISION amend1015f D11).

`run_job` asks here whether every task is finished and whether one still waits to run. A run whose
loop stopped at a task that had already ended blocked or failed ran nothing more; before this module
such a run left the job's record reading `running` with no run alive, and the run story said
"working" for ever after a retry. `blocked_rerun_reason` names that case, so the job ends blocked
again with the blocked tasks as its reason.

This module reads task records only; it never runs, saves or changes anything.
"""

from __future__ import annotations

from typing import Any

#: Task statuses after which the job has nothing left to do for the task.
_FINISHED = ("applied_to_job_workspace", "skipped", "split", "vetoed")
#: Task statuses that stop the task loop without running the task again.
_STUCK = ("blocked", "failed")


def job_task_ending(tasks: list[Any]) -> tuple[bool, bool]:
    """(every task is finished, some task still waits to run) for TASKS."""
    statuses = [str(getattr(task, "status", "") or "") for task in tasks]
    return all(s in _FINISHED for s in statuses), any(s == "pending" for s in statuses)


def blocked_rerun_reason(job: Any, prior_error: str = "") -> str:
    """The error a job that still reads `running` ends blocked with, because a task of it ended
    blocked or failed and the run did not run it again; "" when the job is not in that state.

    PRIOR_ERROR is the error the job carried before this run cleared it (R-1059); the job keeps it,
    because nothing ran that could have changed it. Without one, the blocked tasks are named."""
    if str(getattr(getattr(job, "state", None), "value", getattr(job, "state", ""))) != "running":
        return ""
    stuck = [task for task in getattr(job, "tasks", ()) or ()
             if str(getattr(task, "status", "") or "") in _STUCK]
    if not stuck:
        return ""
    return prior_error or "; ".join(
        f"task_{task.task_id}_blocked: {task.error or task.final_status or task.status}" for task in stuck)


def job_is_retryable(job: Any) -> bool:
    """True when JOB reads blocked and a task of it ended blocked or failed: a retry puts such a
    task back to pending before the run (R-1331, DECISION F307 D22), a plain run never runs it."""
    if str(getattr(getattr(job, "state", None), "value", getattr(job, "state", ""))) != "blocked":
        return False
    return any(str(getattr(task, "status", "") or "") in _STUCK for task in getattr(job, "tasks", ()) or ())
