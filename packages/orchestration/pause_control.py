"""F025 — pause and resume, the control protocol (DECISION F025 D1).

The pause lives BESIDE the kill switch, in its own files, rather than inside it: D1's
alternative of widening ``should_stop`` to also read a pause was rejected because
``should_stop`` is F011's own safe-point check, and T5_F025.md forbids touching it — a job
scope pause is a create-only ``pause.json`` and a task scope pause is one create-only file per
paused task, both reached through ``safe_points.open_job_control_fd`` and the same
``secure_fs`` primitives F011 uses, so a symlinked control area is refused here exactly as it
is for a stop, and nothing this module writes lands under the stop's own ``archive/``.

A pause is never a waiting process: D1's alternative of a paused process that blocks for its
own resume was rejected by the orchestrator brief, because a process that waits cannot be
killed, restarted or inspected the way one that has already exited and recorded why can. A job
pause therefore parks the run — the state is persisted, the request is archived, and the
process exits with nothing left running — and the resume is simply the next launch of the same
job, reading the same parked state back off disk. This module holds only the control files and
the pure mask arithmetic that decides what a pause withholds; the runners' safe points and
ready sets that read them are a later round's work (D1, clause 9).
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.common import secure_fs as _fs
from packages.orchestration import safe_points as _sp
from packages.orchestration.failure_postmortem import safe_text

__all__ = [
    "PauseControlError",
    "PauseSignal",
    "TaskPause",
    "request_pause",
    "pause_requested",
    "settle_pause",
    "withdraw_pause",
]

PAUSE_SIGNAL_VERSION = 1

PAUSE_REQUEST_FILENAME = "pause.json"
PAUSE_ARCHIVE_DIRNAME = "pause_archive"
#: Mirrors ``safe_points.JOBS_DIRNAME`` — used only to compose the control-relative report
#: path ``settle_pause`` returns; no file operation ever opens a path by this name.
JOBS_DIRNAME = "jobs"

_VALID_SETTLE_OUTCOMES = frozenset({"served", "withdrawn", "superseded_by_stop"})

UNKNOWN_REASON = "unknown"
UNKNOWN_SOURCE = "unknown"


class PauseControlError(RuntimeError):
    """The pause control area could not be used, or an on-disk entry could not be trusted.

    Loud on purpose, same as ``safe_points.StopControlError``: a silently dropped paused-task
    entry would dispatch work the operator asked to withhold.
    """


@dataclass(frozen=True)
class PauseSignal:
    """One operator request to pause one job, at job scope."""

    job_id: str
    request_id: str
    reason: str
    source: str
    requested_at: str
    pause_signal_v: int = PAUSE_SIGNAL_VERSION

    def to_json(self) -> dict[str, Any]:
        return {
            "pause_signal_v": self.pause_signal_v,
            "job_id": self.job_id,
            "request_id": self.request_id,
            "reason": self.reason,
            "source": self.source,
            "requested_at": self.requested_at,
        }


@dataclass(frozen=True)
class TaskPause:
    """One paused task, at task scope."""

    job_id: str
    task_id: str
    request_id: str
    reason: str
    source: str
    requested_at: str

    def to_json(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id,
            "task_id": self.task_id,
            "request_id": self.request_id,
            "reason": self.reason,
            "source": self.source,
            "requested_at": self.requested_at,
        }


# ---------------------------------------------------------------------------
# Bounding — mirrors safe_points._bounded exactly; reason/source are operator text that
# ends up in a ledger event and an Evidence bundle, same as a stop's.
# ---------------------------------------------------------------------------


def _bounded(text: Any, limit: int, fallback: str) -> str:
    cleaned = safe_text(str(text or "")).replace("\n", " ").replace("\r", " ").strip()
    if not cleaned:
        return fallback
    return cleaned[:limit]


# ---------------------------------------------------------------------------
# One verified subdirectory of the job's control directory — pause_archive/, paused_tasks/,
# and pause_archive/tasks/ all go through this. Mirrors safe_points._open_archive_fd.
# ---------------------------------------------------------------------------


def _open_named_dir(parent_fd: int, name: str, *, create: bool) -> int | None:
    try:
        return _fs.open_verified_dir(name, dir_fd=parent_fd, error_cls=PauseControlError,
                                     noun="pause-control")
    except _fs.MissingComponent:
        if not create:
            return None
    _fs.require_writable_dir(parent_fd, error_cls=PauseControlError, noun="pause-control",
                             label=name)
    try:
        os.mkdir(name, _sp.CONTROL_DIR_MODE, dir_fd=parent_fd)
    except FileExistsError:
        pass                                    # a concurrent creator; verify below
    except OSError as exc:
        raise PauseControlError(
            f"cannot create the pause-control directory {name!r} "
            f"({type(exc).__name__}: {exc.strerror or exc})") from exc
    try:
        return _fs.open_verified_dir(name, dir_fd=parent_fd, error_cls=PauseControlError,
                                     noun="pause-control")
    except _fs.MissingComponent as exc:
        raise PauseControlError(
            f"the pause-control directory {name!r} vanished after creation") from exc


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def _parse_pause_signal(job_id: str, raw: bytes) -> PauseSignal:
    try:
        data = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise PauseControlError(f"the pause request is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise PauseControlError("the pause request is not a JSON object")
    request_id = data.get("request_id")
    if not isinstance(request_id, str) or not request_id:
        raise PauseControlError("the pause request carries no request id")
    return PauseSignal(
        job_id=job_id,
        request_id=request_id,
        reason=_bounded(data.get("reason"), _sp.MAX_REASON_CHARS, UNKNOWN_REASON),
        source=_bounded(data.get("source"), _sp.MAX_SOURCE_CHARS, UNKNOWN_SOURCE),
        requested_at=str(data.get("requested_at") or ""),
        pause_signal_v=int(data.get("pause_signal_v") or PAUSE_SIGNAL_VERSION),
    )


# ---------------------------------------------------------------------------
# S3 — job scope
# ---------------------------------------------------------------------------


def request_pause(job_id: str, reason: str = "", source: str = "cli", *,
                  control_root_path: Path | None = None) -> PauseSignal:
    """Ask a job to pause. Create-only, same race rule as ``request_stop``: a pending request
    is returned unchanged, and two concurrent callers converge on one request id."""
    jid = _sp.validate_job_id(job_id)
    job_fd = _sp.open_job_control_fd(jid, control_root_path, create=True)
    assert job_fd is not None
    try:
        existing = _fs.read_verified_file(PAUSE_REQUEST_FILENAME, job_fd,
                                          max_bytes=_sp.MAX_CONTROL_BYTES,
                                          error_cls=PauseControlError, noun="pause request")
        if existing is not None:
            return _parse_pause_signal(jid, existing)

        signal = PauseSignal(
            job_id=jid,
            request_id=_sp.new_request_id(),
            reason=_bounded(reason, _sp.MAX_REASON_CHARS, UNKNOWN_REASON),
            source=_bounded(source, _sp.MAX_SOURCE_CHARS, UNKNOWN_SOURCE),
            requested_at=_sp.utc_now_iso(),
        )
        published = _fs.write_file_atomically(
            job_fd, PAUSE_REQUEST_FILENAME, _fs.json_bytes(signal.to_json()),
            create_only=True, file_mode=_sp.CONTROL_FILE_MODE,
            error_cls=PauseControlError, noun="pause request")
        if not published:
            raw = _fs.read_verified_file(PAUSE_REQUEST_FILENAME, job_fd,
                                         max_bytes=_sp.MAX_CONTROL_BYTES,
                                         error_cls=PauseControlError, noun="pause request")
            if raw is None:
                raise PauseControlError(
                    "the pause request vanished during publication; no pause was requested")
            return _parse_pause_signal(jid, raw)
        return signal
    finally:
        os.close(job_fd)


def pause_requested(job_id: str, *,
                    control_root_path: Path | None = None) -> PauseSignal | None:
    """The cheap check: one directory open, one read. None on a missing root or job."""
    jid = _sp.validate_job_id(job_id)
    job_fd = _sp.open_job_control_fd(jid, control_root_path, create=False)
    if job_fd is None:
        return None
    try:
        raw = _fs.read_verified_file(PAUSE_REQUEST_FILENAME, job_fd,
                                     max_bytes=_sp.MAX_CONTROL_BYTES,
                                     error_cls=PauseControlError, noun="pause request")
    finally:
        os.close(job_fd)
    if raw is None:
        return None
    return _parse_pause_signal(jid, raw)


def settle_pause(job_id: str, signal: PauseSignal, outcome: str, *,
                 control_root_path: Path | None = None) -> str:
    """Archive ``signal`` under ``outcome``, THEN remove the pending file — never the other
    order. Idempotent: an archive already there is not rewritten, and a pending file holding a
    DIFFERENT request id (a newer request) is left exactly as it is. Returns the archived
    copy's control-relative path."""
    if outcome not in _VALID_SETTLE_OUTCOMES:
        raise PauseControlError(
            f"unknown pause outcome {outcome!r}: expected one of "
            f"{sorted(_VALID_SETTLE_OUTCOMES)}")
    jid = _sp.validate_job_id(job_id)
    job_fd = _sp.open_job_control_fd(jid, control_root_path, create=True)
    assert job_fd is not None
    archive_fd = None
    try:
        archive_fd = _open_named_dir(job_fd, PAUSE_ARCHIVE_DIRNAME, create=True)
        assert archive_fd is not None
        name = f"{signal.request_id}.json"
        payload = dict(signal.to_json())
        payload["outcome"] = outcome
        payload["settled_at"] = _sp.utc_now_iso()
        # create_only: a second settle (or a crash after this write and before the removal
        # below) finds the archive already there and simply writes nothing new — the archive
        # publication step above is what must fail loudly, not this one.
        _fs.write_file_atomically(archive_fd, name, _fs.json_bytes(payload), create_only=True,
                                  file_mode=_sp.CONTROL_FILE_MODE, error_cls=PauseControlError,
                                  noun="pause archive")

        pending_raw = _fs.read_verified_file(PAUSE_REQUEST_FILENAME, job_fd,
                                             max_bytes=_sp.MAX_CONTROL_BYTES,
                                             error_cls=PauseControlError, noun="pause request")
        if pending_raw is not None:
            pending_signal = _parse_pause_signal(jid, pending_raw)
            if pending_signal.request_id == signal.request_id:
                _fs.require_writable_dir(job_fd, error_cls=PauseControlError,
                                         noun="pause-control", label=PAUSE_REQUEST_FILENAME)
                _fs.unlink_at(PAUSE_REQUEST_FILENAME, job_fd, error_cls=PauseControlError,
                              noun="pause request")
        return f"{JOBS_DIRNAME}/{jid}/{PAUSE_ARCHIVE_DIRNAME}/{name}"
    finally:
        if archive_fd is not None:
            os.close(archive_fd)
        os.close(job_fd)


def withdraw_pause(job_id: str, *,
                   control_root_path: Path | None = None) -> PauseSignal | None:
    """Settle a pending request as ``withdrawn``. None when nothing is pending."""
    jid = _sp.validate_job_id(job_id)
    pending = pause_requested(jid, control_root_path=control_root_path)
    if pending is None:
        return None
    settle_pause(jid, pending, "withdrawn", control_root_path=control_root_path)
    return pending
