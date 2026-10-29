"""A job a run leaves blocked keeps the time it ended (R-1332, DECISION F307 D21).

`run_job` blocks a job on more than twenty paths: `_block_job`, the coverage gate of the job's
workspace, the veto and injection folds, the definition-of-done gate, a run that finds its task
already blocked, and others. Only a stop filled `finished_at` (R-0828), so a blocked job's record
kept no finish time and the run story's `ended_at` fell back to its stop time or its newest event.
`stamp_blocked_job_finish` wraps `run_job` once instead of every one of those paths: when the run
returns and the job's record reads blocked with no finish time, the record gets the time the run
ended. A job id with no record is left alone, so a run of a job that does not exist writes nothing.

F323 (operator order welt-2): the same wrapper ends every run, also one that raised, by settling
the jobs of its order that wait for it (`order_jobs.settle_waiting_jobs`): a job that ended without
a result that can land ends each job waiting for it `blocked`, with a sentence naming why. Before,
such a job stayed `waiting` forever (job 43e55dbbd5ba4e73 of 2026-10-28). A settle that cannot read
or write a record never fails the run it follows.

F330 (operator order beweis): a blocked, unattended job whose review says its work does not belong
in its repository, with no file changed, ends `failed` with the stop reason `not_in_this_repository`
here (`job_wrong_repository`), so it hands its task back instead of waiting for a person.
"""

from __future__ import annotations

import functools
import logging
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any


def stamp_blocked_job_finish(run: Callable[..., Any]) -> Callable[..., Any]:
    """Wrap RUN, `run_job`, so a job record it leaves blocked without a finish time is saved with
    the time the run ended; the job RUN returns carries the same time. Every run then settles the
    jobs waiting for its job (F323). Nothing else changes."""

    @functools.wraps(run)
    def _wrapped(*args: Any, **kwargs: Any) -> Any:
        try:
            job = run(*args, **kwargs)
            from packages.orchestration.job_wrong_repository import end_job_not_in_this_repository
            from packages.orchestration.pingpong_job import JOB_BLOCKED, load_job_plan_safe, save_job_plan

            job_id = str(getattr(job, "job_id", "") or "")
            record, _damaged = load_job_plan_safe(job_id) if job_id else (None, False)
            if record is not None and end_job_not_in_this_repository(record):    # F330
                save_job_plan(record)
                job.state, job.stop_reason, job.finished_at = record.state, record.stop_reason, record.finished_at
                job.metadata = record.metadata
            elif record is not None and record.state == JOB_BLOCKED and not record.finished_at:
                record.finished_at = datetime.now(timezone.utc).isoformat()
                save_job_plan(record)
                job.finished_at = record.finished_at
            return job
        finally:
            settle_jobs_waiting_for(str(args[0] if args else kwargs.get("job_id", "")))

    return _wrapped


def settle_jobs_waiting_for(job_id: str) -> None:
    """F323: `order_jobs.settle_waiting_jobs` for *job_id* after its run; a failure is only logged."""
    from packages.orchestration.order_jobs import settle_waiting_jobs

    try:
        if job_id:
            settle_waiting_jobs(job_id)
    except (OSError, ValueError, TypeError, AttributeError, KeyError):   # the run's own outcome stands
        logging.getLogger(__name__).warning("settling the jobs waiting for %s failed", job_id, exc_info=True)
