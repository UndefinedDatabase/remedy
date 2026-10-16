"""A stop of a job that never started ends it at once (DECISION amend1016s D1).

`safe_points.request_stop` only writes a request, and a RUNNING job consumes it at its next
safe point. A job that never started has no runner that will ever reach one: the second job of
a mission whose order process already ended stays `planned` with its request pending, and its
story reads `planning`, so a client shows it as running. `request_job_stop` is the one place
both `remedy job stop` without a supervisor and the supervisor's forwarded `job.stop` go
through: it writes (or reads back) the request exactly as before and then, for a job that never
started, finalizes it on the spot as a first-class stop.

A job never started when its state is `planned` and it carries no first run time and no run
episode: `run_job` leaves `planned` only past its safe point zero, where it stamps both. A
running, blocked, paused or otherwise started job is never touched here; its request waits for
its safe point exactly as before.

The finalization reuses the kill switch's own steps in its own order (`pingpong_job._stop_job`):
archive the request, write the stop fields and the `stopped` state through the job store, and
only then acknowledge the request. It writes no `job_stopped` run-log event, no F010 post-mortem
and no F012 manifest, because a job that never ran has no run ledger, no failure to explain and
no execution episode. A `stopped` job that never ran is resumed by `remedy job run` like any
stopped job; `remedy do`'s run step does not run a job of its walk that is already stopped.

Known window: a `run_job` that has already passed safe point zero but not yet persisted
`running` still reads the job as `planned` on disk. A stop in that instant ends the record as
`stopped`, and the runner's next write overwrites it. That window is the runner's workspace
acquisition only, and closing it needs a lock `run_job` does not have.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.orchestration.safe_points import (
    StopControlError,
    StopSignal,
    acknowledge_stop,
    archive_stop,
    request_stop,
)

#: The job states that mean "no run ever started" in Remedy's job model.
JOB_NEVER_STARTED_STATES = frozenset({"planned"})


def job_never_started(job: Any) -> bool:
    """True when JOB is `planned` and no run of it ever passed safe point zero."""
    state = getattr(job.state, "value", str(job.state))
    return (state in JOB_NEVER_STARTED_STATES
            and not getattr(job, "first_running_at", "")
            and not getattr(job, "active_episode_id", ""))


def stop_unstarted_job(job: Any, signal: StopSignal, *,
                       control_root_path: Path | None = None) -> bool:
    """End JOB, which never started, as stopped by SIGNAL. True when it is stopped now.

    A request that cannot be archived stays pending and the job stays `planned` (False): the
    stop is still requested, and a run of the job honours it at safe point zero. An
    acknowledge that fails after the stopped record is saved is kept on the job as
    `stop_error`, as the runner keeps it, and the next `run_job` acknowledges the request.
    """
    from packages.orchestration.failure_postmortem import safe_text
    from packages.orchestration.pingpong_job import JOB_STOPPED, save_job_plan

    try:
        archive_ref = archive_stop(job.job_id, signal, control_root_path=control_root_path)
    except StopControlError:
        return False
    now = datetime.now(timezone.utc).isoformat()
    job.stop_archive_ref = archive_ref
    job.stop_request_id = signal.request_id
    job.stop_reason = signal.reason
    job.stop_source = signal.source
    job.stopped_at = now
    job.finished_at = now
    job.stop_error = ""
    job.error = ""
    job.state = JOB_STOPPED
    save_job_plan(job)
    try:
        acknowledge_stop(job.job_id, signal, control_root_path=control_root_path)
    except StopControlError as exc:
        job.stop_error = safe_text(
            f"stop_acknowledge_failed: {type(exc).__name__}: {exc}")[:500]
        save_job_plan(job)
    return True


def request_job_stop(job_id: str, reason: str = "", source: str = "cli", *,
                     control_root_path: Path | None = None) -> tuple[StopSignal, bool]:
    """Ask JOB_ID to stop: (the request, whether the job is stopped already).

    The request is `request_stop`'s, so a request already pending is the same episode and
    is returned again. A job that never started is then stopped at once, which also
    finalizes a request that was left pending on it before this rule existed.
    """
    from packages.orchestration.pingpong_job import load_job_plan

    signal = request_stop(job_id, reason=reason, source=source,
                          control_root_path=control_root_path)
    job = load_job_plan(signal.job_id)
    if job is None or not job_never_started(job):
        return signal, False
    return signal, stop_unstarted_job(job, signal, control_root_path=control_root_path)
