"""F258 T002 — carrying a planned self-use job onto the real RUN path.

:mod:`packages.orchestration.self_use_job` plans a curated queue item onto a
:class:`~packages.orchestration.pingpong_job.JobPlan` and deliberately stops
short of running it. This module is the step that runs it: it takes the
planned item through the same builder/reviewer loop, in the same isolated
worktree (or copy, when ``repo_path`` is not a git repository), under the
same budget machinery, every other job already uses —
:func:`packages.orchestration.pingpong_job.run_job` — and stops at the same
normal approval gate every job stops at.

Public API::

    SelfUseRunError: the planned item was already blocked before any task ran
    run_next_self_use_item(dest_dir, repo_path=".", queue_path=None, *,
        max_provider_calls=6, max_cost_usd=0.50, max_tasks=1, **run_job_kwargs)
        -> tuple[SelfUseQueueEntry, Path, JobPlan]

Deliberate absences:
  * REMEDY DELIBERATELY DOES NOT PROMOTE THE RUN'S RESULT. Promotion stays
    behind the ``--approve`` barrier in
    :mod:`packages.orchestration.job_promote`, which never auto-promotes;
    this module calls :func:`~packages.orchestration.pingpong_job.run_job`
    and nothing past it — the same stopping point
    :mod:`packages.orchestration.self_use_job`'s own docstring already names
    for planning, one step further down the same path.
  * REMEDY DELIBERATELY DOES NOT MARK A QUEUE ITEM CONSUMED. Exactly as
    :mod:`packages.orchestration.self_use_job` and
    :mod:`packages.orchestration.self_use_queue` before it: consumption is an
    edit the CLOSURE ROUND makes, which DECISION F257 D2 rules, and a run
    that can check itself off is not a gate.
  * Remedy deliberately does not pick a builder or reviewer PROVIDER here.
    Every ``builder_*``/``reviewer_*`` keyword this module accepts is
    forwarded to :func:`run_job` UNCHANGED, so a real self-use run resolves
    the same product default any other unflagged job resolves, and a test
    can substitute a fake provider the same way every other job test does.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from packages.core.models import JobBudgets
from packages.orchestration.pingpong_job import JOB_BLOCKED, JobPlan, run_job
from packages.orchestration.self_use_job import plan_next_self_use_item
from packages.orchestration.self_use_queue import SelfUseQueueEntry


class SelfUseRunError(RuntimeError):
    """A planned self-use item cannot be run.

    Raised only when planning itself already blocked the item (an
    unparsable job file — ``no_tasks_found`` or worse) before any task ran.
    A job that blocks DURING execution is not this: it still ran, and its
    ``JobPlan`` is the return value, not an exception — blocking mid-run is
    an ordinary, expected outcome of the normal approval gate, exactly as it
    is for any other job.
    """


def run_next_self_use_item(
    dest_dir: Path,
    repo_path: str = ".",
    queue_path: Path | None = None,
    *,
    max_provider_calls: int | None = 6,
    max_cost_usd: float | None = 0.50,
    max_tasks: int | None = 1,
    **run_job_kwargs: Any,
) -> tuple[SelfUseQueueEntry, Path, JobPlan]:
    """Plan the queue's next pending item and RUN it to the approval gate.

    Composes two existing seams and adds no new one:
    :func:`~packages.orchestration.self_use_job.plan_next_self_use_item`
    (which already persists the planned ``JobPlan``), then
    :func:`~packages.orchestration.pingpong_job.run_job` on the id it
    returns, with a SMALL budget attached
    (:class:`~packages.core.models.JobBudgets`, ``max_provider_calls`` and
    ``max_cost_usd`` default to conservative, overridable values) and an
    extra ``max_tasks`` cap alongside it. Every ``run_job_kwargs`` entry is
    forwarded unchanged, so a caller may pass ``builder_provider=``,
    ``reviewer_provider=``, ``repair_rounds=`` or any other keyword
    :func:`run_job` accepts.

    Answers ``(entry, job_file_path, result)`` — the queue entry that was
    run, the job file :func:`plan_next_self_use_item` rendered it to, and
    the ``JobPlan`` :func:`run_job` returns (``JOB_COMPLETED`` or
    ``JOB_BLOCKED``, never promoted).

    Raises:
        SelfUseJobError: the queue holds no pending item (propagated
            unchanged from :func:`plan_next_self_use_item`).
        SelfUseRunError: the planned item was already ``JOB_BLOCKED`` before
            any task ran — a curation defect, not a run outcome.
    """
    entry, job_file_path, plan = plan_next_self_use_item(dest_dir, repo_path, queue_path)
    if plan.status == JOB_BLOCKED:
        raise SelfUseRunError(
            f"{entry.id}: planning already blocked it ({plan.error!r}) — "
            "this item cannot be run"
        )
    budgets = JobBudgets(
        max_provider_calls=max_provider_calls, max_cost_usd=max_cost_usd
    ).model_dump(mode="json")
    result = run_job(plan.job_id, budgets=budgets, max_tasks=max_tasks, **run_job_kwargs)
    return entry, job_file_path, result
