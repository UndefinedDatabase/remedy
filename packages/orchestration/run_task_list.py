"""F308 — what a run manifest says about the task list a job ran: the ids the episode's embedded
definition declares, their agreement across a job's episodes, what a task that owns no run is
expected to have done, and the split of a task whose context exceeds its class cap. It imports
neither `run_manifest` nor `pingpong_job` at its top, so that `run_manifest.py` can import it at
its own top without a cycle; each function below imports what it needs from those two modules
inside its own body.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from packages.orchestration.context_compiler import ClassBudgetFit
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry


# F308, step (2) of `_collect_calls`'s boundary: the task without a run gets its own function.
def expect_task_without_run(
    task_id: str, status: str, must_have_calls: bool, problems: list[str], expectations: list,
) -> None:
    """Record what a task that owns no run is expected to have done, by F6's three cases."""
    from packages.orchestration.pingpong_job import (
        TASK_BLOCKED,
        TASK_FAILED,
        TASK_SKIPPED,
        TASK_VETOED,
    )
    from packages.orchestration.run_manifest import (
        DISPATCH_NEVER,
        DISPATCH_THIS_EPISODE,
        EXPECT_EXECUTED,
        EXPECT_FAILED_PRE_DISPATCH,
        EXPECT_NOT_DISPATCHED,
        EXPECT_SKIPPED,
        TaskCallExpectationV1,
    )
    # F6: a task whose status says it ran, but which carries no run to point at, is
    # MISSING evidence — not a zero-call task. Publishing it as "complete" would be the
    # manifest certifying its own blind spot.
    if must_have_calls:
        problems.append(
            f"task {task_id} is {status!r} but has no run id, so its calls cannot be "
            f"accounted for")
        expectations.append(TaskCallExpectationV1(
            task_id=task_id, expectation=EXPECT_EXECUTED, run_id="",
            expected_call_count=1, task_status_at_finalization=status,
            dispatch_state=DISPATCH_THIS_EPISODE))
    elif status in (TASK_FAILED, TASK_BLOCKED):
        # F4 (round 12): failed/blocked with NO run is its own truth — the task never
        # reached dispatch. Calling it "not dispatched" would lose the failure; calling
        # it "dispatched_no_calls" would invent a run that never existed.
        expectations.append(TaskCallExpectationV1(
            task_id=task_id, expectation=EXPECT_FAILED_PRE_DISPATCH, run_id="",
            task_status_at_finalization=status, dispatch_state=DISPATCH_NEVER))
    else:
        # F027 D2 (6): a vetoed task with no run is EXPECT_SKIPPED exactly as a
        # skipped one is — the veto struck before dispatch, same as a skip.
        expectations.append(TaskCallExpectationV1(
            task_id=task_id,
            expectation=(EXPECT_SKIPPED if status in (TASK_SKIPPED, TASK_VETOED)
                         else EXPECT_NOT_DISPATCHED),
            run_id="", task_status_at_finalization=status,
            dispatch_state=DISPATCH_NEVER))


# F308, outside `run_job`'s named steps: the split of a task over its class cap gets its own
# function.
def split_task_over_class_cap(
    job: JobPlan, task: TaskEntry, idx: int, fit_result: ClassBudgetFit,
) -> bool:
    """Answer True when it replaced the task with its parts."""
    from packages.orchestration.escalation import (
        auto_apply_safe_default,
        enqueue_task_decision,
    )
    from packages.orchestration.pingpong_job import (
        TASK_SPLIT,
        planned_task_to_task_entry,
        save_job_plan,
        task_entry_to_planned_task,
    )
    from packages.orchestration.task_granularity import (
        split_one_task,
    )
    decision = enqueue_task_decision(
        job,
        task_id=task.task_id,
        question="task context exceeds its class cap",
        options=["split task"],
        safe_default="split task",
        impact=(
            f"tier1_tokens={fit_result.tier1_tokens} "
            f"cap_tokens={fit_result.cap_tokens} "
            f"task_class={fit_result.task_class}"
        ),
        now=datetime.now(timezone.utc),
    )
    answered = auto_apply_safe_default(
        job, decision, now=datetime.now(timezone.utc))
    split_entries: list[TaskEntry] = []
    if answered is not None and answered["answer"] == "split task":
        planned = task_entry_to_planned_task(task)
        if planned is not None:
            used_ids = {t.task_id for t in job.tasks}
            children = split_one_task(planned, used_ids=used_ids)
            if children:
                split_entries = [
                    planned_task_to_task_entry(
                        child,
                        task_class=task.task_class,
                        source_heading_number=task.source_heading_number,
                    )
                    for child in children
                ]
    if split_entries:
        job.tasks[idx + 1:idx + 1] = split_entries
        task.status = TASK_SPLIT
        save_job_plan(job)
        return True
    return False
