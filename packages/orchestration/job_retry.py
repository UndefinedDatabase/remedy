"""R-1331 — a retry puts a blocked job's tasks that ended blocked or failed back to pending.

`remedy job run <job> --retry`, and `POST /api/v1/jobs/{job}/retry`, which starts that command, call
`retry_blocked_job_tasks` with the job's record before the run starts (DECISION F307 D22). Without
it a run stops at such a task and runs nothing, so the job ends blocked again with its old error.

The reset is the one `remedy job edit-task` makes for a failed task: the task's status goes back to
`pending` and its error is cleared, and every `skipped` task after the first such task is restored
with it, but a task a veto makes unreachable is left as it is, as the veto fold leaves it. The job's
error and finish time are cleared, as a subtree rerun clears them. A job that is not blocked, or has
no such task, is left as it is and nothing is written, so the run that follows is a plain run.
"""

from __future__ import annotations

from typing import Any

from packages.orchestration.job_run_ending import job_is_retryable


# WHY: a run never re-attempts a task that ended blocked or failed; the person who retries after a
# provider came back must see that task run again, not the same failure (R-1331).
def retry_blocked_job_tasks(job: Any) -> tuple[str, ...]:
    """Put JOB's tasks that ended blocked or failed, and the skipped tasks after the first of them,
    back to pending, and save JOB; the ids put back, in plan order, or () when nothing was."""
    if not job_is_retryable(job):
        return ()
    from packages.orchestration.pingpong_job import (
        TASK_BLOCKED,
        TASK_FAILED,
        TASK_PENDING,
        TASK_SKIPPED,
        TASK_VETOED,
        save_job_plan,
    )
    from packages.orchestration.task_veto import veto_unreachable

    vetoed = [task.task_id for task in job.tasks if task.status == TASK_VETOED]
    unreachable = set(veto_unreachable(job.tasks, vetoed))
    first = next(i for i, task in enumerate(job.tasks) if task.status in (TASK_BLOCKED, TASK_FAILED))
    reset: list[str] = []
    for task in job.tasks[first:]:
        if task.task_id in unreachable or task.status not in (TASK_BLOCKED, TASK_FAILED, TASK_SKIPPED):
            continue
        task.status = TASK_PENDING
        task.error = ""
        reset.append(task.task_id)
    if not reset:
        return ()
    job.error = ""
    job.finished_at = ""
    save_job_plan(job)
    return tuple(reset)
