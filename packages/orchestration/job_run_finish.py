"""A job a run leaves blocked keeps the time it ended (R-1332, DECISION F307 D21).

`run_job` blocks a job on more than twenty paths: `_block_job`, the coverage gate of the job's
workspace, the veto and injection folds, the definition-of-done gate, a run that finds its task
already blocked, and others. Only a stop filled `finished_at` (R-0828), so a blocked job's record
kept no finish time and the run story's `ended_at` fell back to its stop time or its newest event.
`stamp_blocked_job_finish` wraps `run_job` once instead of every one of those paths: when the run
returns and the job's record reads blocked with no finish time, the record gets the time the run
ended. A job id with no record is left alone, so a run of a job that does not exist writes nothing.
"""

from __future__ import annotations

import functools
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any


def stamp_blocked_job_finish(run: Callable[..., Any]) -> Callable[..., Any]:
    """Wrap RUN, `run_job`, so a job record it leaves blocked without a finish time is saved with
    the time the run ended; the job RUN returns carries the same time. Nothing else changes."""

    @functools.wraps(run)
    def _wrapped(*args: Any, **kwargs: Any) -> Any:
        job = run(*args, **kwargs)
        from packages.orchestration.pingpong_job import JOB_BLOCKED, load_job_plan_safe, save_job_plan

        job_id = str(getattr(job, "job_id", "") or "")
        record, _damaged = load_job_plan_safe(job_id) if job_id else (None, False)
        if record is not None and record.state == JOB_BLOCKED and not record.finished_at:
            record.finished_at = datetime.now(timezone.utc).isoformat()
            save_job_plan(record)
            job.finished_at = record.finished_at
        return job

    return _wrapped
