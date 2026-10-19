"""A job ends for good: `remedy job abandon`, and the jobs of a cancelled order (exec-1017c, R-1339).

`remedy job stop` pauses work on purpose: a stopped job keeps its pending tasks and `remedy job run`
resumes it. A person who no longer wants the work had no way to say so: a `blocked` or `stopped`
job stayed in every active view, and only a budget decision's `abandon` wrote the terminal
`cancelled` state. A cancel is that ending for any job that has not finished:

* the request is a durable fact first: `cancel.json` in the job's private control area, written
  create-only through the kill switch's own verified descriptors, so every process that could
  still run the job reads the same request;
* a job no runner holds (never started, stopped, blocked, paused) is `cancelled` at once;
* a running job gets a stop request beside it and ends `cancelled` at its next safe point, where
  `pingpong_job._stop_job` asks `job_stop_end_state`; until then the answer says the cancel is
  pending and never that the job ended;
* a run that starts after the request settles the job `cancelled` before any work
  (`settle_job_cancel`, at the top of `run_job`), so a resumed or restarted run never escapes it;
* a completed job is refused: its result waits for the person's apply or decline, which a cancel
  never makes for them; a failed job has ended already.

Nothing is deleted: the record, evidence, workspace and history stay readable. A cancelled job asks
no decision (`decision_queue.list_decisions`), so it leaves the active digest for its ended list.
"""
from __future__ import annotations

import json
import os
from collections.abc import Callable
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.core.models import RunState

#: The cancel request's file name in the job's control area (beside the kill switch's `stop.json`).
JOB_CANCEL_REQUEST_FILENAME = "cancel.json"

#: The job metadata key a cancelled job keeps its request under: `{reason, source, requested_at}`.
JOB_CANCEL_METADATA_KEY = "cancel"

#: The states a cancel never changes: a result waiting for its apply or decline, or an end.
_NOT_CANCELLABLE = {"completed": "its result waits for an apply or a decline (remedy job decline)",
                    "failed": "it has ended failed already"}


class JobCancelRefused(Exception):
    """A cancel that changes nothing, with its refusal token."""

    def __init__(self, token: str, message: str) -> None:
        super().__init__(message)
        self.token = token


@dataclass(frozen=True)
class JobCancelRequest:
    """One cancel request as `cancel.json` holds it."""

    job_id: str
    reason: str
    source: str
    requested_at: str

    def to_json(self) -> dict[str, str]:
        return asdict(self)


def _state(job: Any) -> str:
    return getattr(job.state, "value", str(job.state))


def request_job_cancel_marker(job_id: str, *, reason: str, source: str,
                              control_root_path: Path | None = None) -> JobCancelRequest:
    """Publish the job's cancel request once; a request already there is returned as it stands."""
    from packages.common import secure_fs as _fs
    from packages.orchestration.safe_points import (
        CONTROL_FILE_MODE,
        MAX_REASON_CHARS,
        MAX_SOURCE_CHARS,
        StopControlError,
        open_job_control_fd,
        utc_now_iso,
        validate_job_id,
    )

    jid = validate_job_id(job_id)
    request = JobCancelRequest(job_id=jid, reason=(reason or "cancelled")[:MAX_REASON_CHARS],
                               source=(source or "cli")[:MAX_SOURCE_CHARS], requested_at=utc_now_iso())
    job_fd = open_job_control_fd(jid, control_root_path, create=True)
    assert job_fd is not None                     # create=True either makes it or raises
    try:
        _fs.write_file_atomically(job_fd, JOB_CANCEL_REQUEST_FILENAME,
                                  _fs.json_bytes(request.to_json()), create_only=True,
                                  file_mode=CONTROL_FILE_MODE, error_cls=StopControlError,
                                  noun="cancel request")
    finally:
        os.close(job_fd)
    return job_cancel_request(jid, control_root_path=control_root_path) or request


def job_cancel_request(job_id: str, *, control_root_path: Path | None = None) -> JobCancelRequest | None:
    """The job's cancel request, or None. Unreadable content still cancels (as a stop does)."""
    from packages.common import secure_fs as _fs
    from packages.orchestration.safe_points import (
        MAX_CONTROL_BYTES,
        StopControlError,
        open_job_control_fd,
        validate_job_id,
    )

    jid = validate_job_id(job_id)
    job_fd = open_job_control_fd(jid, control_root_path, create=False)
    if job_fd is None:
        return None
    try:
        raw = _fs.read_verified_file(JOB_CANCEL_REQUEST_FILENAME, job_fd, max_bytes=MAX_CONTROL_BYTES,
                                     error_cls=StopControlError, noun="cancel request")
    finally:
        os.close(job_fd)
    if raw is None:
        return None
    try:
        data = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        data = {}
    data = data if isinstance(data, dict) else {}
    return JobCancelRequest(job_id=jid, reason=str(data.get("reason") or "unknown")[:500],
                            source=str(data.get("source") or "unknown")[:120],
                            requested_at=str(data.get("requested_at") or "")[:64])


def _mark_cancelled(job: Any, request: JobCancelRequest) -> None:
    job.state = RunState.CANCELLED
    job.metadata[JOB_CANCEL_METADATA_KEY] = request.to_json()
    job.finished_at = job.finished_at or datetime.now(timezone.utc).isoformat()


def job_stop_end_state(job: Any) -> RunState:
    """The state a stop at a safe point ends *job* in: `cancelled` under a cancel request, else `stopped`.

    Read inside the stop's own transaction, so it never raises: a request that cannot be read leaves
    the stop standing, and the next run's `settle_job_cancel` reads it again.
    """
    from packages.orchestration.safe_points import StopControlError

    try:
        request = job_cancel_request(str(job.job_id))
    except StopControlError:
        return RunState.STOPPED
    if request is None:
        return RunState.STOPPED
    _mark_cancelled(job, request)
    return RunState.CANCELLED


def settle_job_cancel(job: Any) -> bool:
    """True when *job* is cancelled; a job that is not, under a request, is settled `cancelled` now.

    Called where a run begins, before anything else: a request written while no runner held the
    job, or one a runner never reached a safe point for, ends the job here. A stop request left
    pending beside it is consumed into the same end, so no stale request outlives the job.
    """
    if job.state == RunState.CANCELLED:
        return True
    if _state(job) in _NOT_CANCELLABLE:
        return False
    from packages.orchestration.safe_points import StopControlError

    try:
        request = job_cancel_request(str(job.job_id))
    except StopControlError:
        return False          # an unreadable control area is the safe points' to report, as a stop's is
    if request is None:
        return False
    _settle_now(job, request)
    return True


def cancel_stop_at_job_end(job: Any, stop_check: Callable[[], Any]) -> Any:
    """The operator stop that ends *job* `cancelled` after its final gate, or None (exec-1018b, R-1357).

    The job's last safe point comes after its last task, but its DoD gate runs after that point and
    may run the project's tests for minutes. A cancel that arrived meanwhile was answered
    `cancel_pending`; the job must end `cancelled` then, never `completed` and applied. Only a
    cancel request is read here: a plain stop, a pause or a budget stop of finished work is not.
    """
    from packages.orchestration.safe_points import StopControlError, StopSignal

    try:
        if job_cancel_request(str(job.job_id)) is None:
            return None
    except StopControlError:
        return None
    signal = stop_check()
    return signal if isinstance(signal, StopSignal) and signal.source != "budget" else None


def _settle_now(job: Any, request: JobCancelRequest) -> None:
    """End *job* `cancelled` on disk and consume a stop request still pending on it."""
    from packages.orchestration.pingpong_job import save_job_plan
    from packages.orchestration.safe_points import (
        StopControlError,
        acknowledge_stop,
        archive_stop,
        stop_requested,
    )

    _mark_cancelled(job, request)
    save_job_plan(job)
    try:
        pending = stop_requested(str(job.job_id))
        if pending is not None:
            job.stop_archive_ref = archive_stop(str(job.job_id), pending)
            acknowledge_stop(str(job.job_id), pending)
            save_job_plan(job)
    except StopControlError:
        pass  # the job is cancelled durably; a request left pending can never resume it


def cancel_job(job: Any, *, reason: str, source: str, runner_alive: bool = True) -> dict[str, Any]:
    """Cancel *job*: `{job_id, job_status, already_cancelled, cancel_pending, cancel}`.

    A job no runner holds ends `cancelled` now. A `running` job gets a stop request beside the
    cancel request and ends `cancelled` at its next safe point (`cancel_pending` true); with
    *runner_alive* False (the caller knows the process that ran it is gone) it ends now. Raises
    `JobCancelRefused` for a completed or failed job. A cancelled job answers its own request.
    """
    from packages.orchestration.safe_points import request_stop

    job_id, state = str(job.job_id), _state(job)
    if job.state == RunState.CANCELLED:
        recorded = dict(job.metadata.get(JOB_CANCEL_METADATA_KEY) or {})
        return {"job_id": job_id, "job_status": state, "already_cancelled": True,
                "cancel_pending": False, "cancel": recorded or None}
    if state in _NOT_CANCELLABLE:
        raise JobCancelRefused("job_not_cancellable",
                               f"job {job_id} is {state}; nothing was cancelled, because {_NOT_CANCELLABLE[state]}")
    request = request_job_cancel_marker(job_id, reason=reason, source=source)
    if state == "running" and runner_alive:
        request_stop(job_id, reason=request.reason, source=request.source)
        return {"job_id": job_id, "job_status": state, "already_cancelled": False,
                "cancel_pending": True, "cancel": request.to_json()}
    _settle_now(job, request)
    return {"job_id": job_id, "job_status": _state(job), "already_cancelled": False,
            "cancel_pending": False, "cancel": request.to_json()}
