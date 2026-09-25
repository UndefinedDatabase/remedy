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

import hashlib
import json
import os
import re
from collections.abc import Iterable, Mapping
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
    "WithheldTasks",
    "request_pause",
    "pause_requested",
    "settle_pause",
    "withdraw_pause",
    "request_task_pause",
    "release_task_pause",
    "paused_tasks",
    "withheld_task_ids",
    "pause_job_command",
    "unpause_job_command",
]

PAUSE_SIGNAL_VERSION = 1

PAUSE_REQUEST_FILENAME = "pause.json"
PAUSE_ARCHIVE_DIRNAME = "pause_archive"
PAUSED_TASKS_DIRNAME = "paused_tasks"
TASK_ARCHIVE_SUBDIR = "tasks"
#: Mirrors ``safe_points.JOBS_DIRNAME`` — used only to compose the control-relative report
#: path ``settle_pause`` returns; no file operation ever opens a path by this name.
JOBS_DIRNAME = "jobs"

#: A task id is operator/planner input that becomes a filename's SOURCE, not the filename
#: itself (the file is named by its digest, never by the id) — so it is bounded and refused if
#: it carries a control character, but never made "safe" by stripping anything out of it.
MAX_TASK_ID_CHARS = 200
_CONTROL_CHAR_RE = re.compile(r"[\x00-\x1f\x7f]")

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


def _validate_task_id(task_id: Any) -> str:
    if (not isinstance(task_id, str) or not task_id or len(task_id) > MAX_TASK_ID_CHARS
            or _CONTROL_CHAR_RE.search(task_id)):
        raise PauseControlError(
            f"invalid task id {task_id!r}: a task id is 1-{MAX_TASK_ID_CHARS} characters "
            f"with no control character")
    return task_id


def _task_pause_filename(task_id: str) -> str:
    """The file is named by a digest of the id, never by the id itself (S4): an id holding
    ``/``, ``..`` or any other path-shaped text can never become — or escape — a path
    component."""
    digest = hashlib.sha256(task_id.encode("utf-8")).hexdigest()[:32]
    return f"{digest}.json"


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


def _parse_task_pause(job_id: str, raw: bytes) -> TaskPause:
    try:
        data = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise PauseControlError(f"the task pause entry is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise PauseControlError("the task pause entry is not a JSON object")
    task_id = data.get("task_id")
    request_id = data.get("request_id")
    if not isinstance(task_id, str) or not task_id:
        raise PauseControlError("the task pause entry carries no task id")
    if not isinstance(request_id, str) or not request_id:
        raise PauseControlError("the task pause entry carries no request id")
    return TaskPause(
        job_id=job_id,
        task_id=task_id,
        request_id=request_id,
        reason=_bounded(data.get("reason"), _sp.MAX_REASON_CHARS, UNKNOWN_REASON),
        source=_bounded(data.get("source"), _sp.MAX_SOURCE_CHARS, UNKNOWN_SOURCE),
        requested_at=str(data.get("requested_at") or ""),
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


# ---------------------------------------------------------------------------
# S4 — task scope
# ---------------------------------------------------------------------------


def request_task_pause(job_id: str, task_id: str, reason: str = "", source: str = "cli", *,
                       control_root_path: Path | None = None) -> TaskPause:
    """Pause one task. Create-only per task, named by digest. Pausing a paused task returns
    its existing entry unchanged."""
    jid = _sp.validate_job_id(job_id)
    tid = _validate_task_id(task_id)
    job_fd = _sp.open_job_control_fd(jid, control_root_path, create=True)
    assert job_fd is not None
    tasks_fd = None
    try:
        tasks_fd = _open_named_dir(job_fd, PAUSED_TASKS_DIRNAME, create=True)
        assert tasks_fd is not None
        name = _task_pause_filename(tid)
        existing = _fs.read_verified_file(name, tasks_fd, max_bytes=_sp.MAX_CONTROL_BYTES,
                                          error_cls=PauseControlError, noun="task pause")
        if existing is not None:
            return _parse_task_pause(jid, existing)

        pause = TaskPause(
            job_id=jid,
            task_id=tid,
            request_id=_sp.new_request_id(),
            reason=_bounded(reason, _sp.MAX_REASON_CHARS, UNKNOWN_REASON),
            source=_bounded(source, _sp.MAX_SOURCE_CHARS, UNKNOWN_SOURCE),
            requested_at=_sp.utc_now_iso(),
        )
        published = _fs.write_file_atomically(
            tasks_fd, name, _fs.json_bytes(pause.to_json()), create_only=True,
            file_mode=_sp.CONTROL_FILE_MODE, error_cls=PauseControlError, noun="task pause")
        if not published:
            raw = _fs.read_verified_file(name, tasks_fd, max_bytes=_sp.MAX_CONTROL_BYTES,
                                         error_cls=PauseControlError, noun="task pause")
            if raw is None:
                raise PauseControlError(
                    "the task pause vanished during publication; no pause was requested")
            return _parse_task_pause(jid, raw)
        return pause
    finally:
        if tasks_fd is not None:
            os.close(tasks_fd)
        os.close(job_fd)


def release_task_pause(job_id: str, task_id: str, *,
                       control_root_path: Path | None = None) -> TaskPause | None:
    """Archive the entry under ``pause_archive/tasks/`` as ``released``, then remove it.
    None, and nothing written, when the task is not paused."""
    jid = _sp.validate_job_id(job_id)
    tid = _validate_task_id(task_id)
    job_fd = _sp.open_job_control_fd(jid, control_root_path, create=False)
    if job_fd is None:
        return None
    tasks_fd = None
    archive_fd = None
    archive_tasks_fd = None
    try:
        tasks_fd = _open_named_dir(job_fd, PAUSED_TASKS_DIRNAME, create=False)
        if tasks_fd is None:
            return None
        name = _task_pause_filename(tid)
        raw = _fs.read_verified_file(name, tasks_fd, max_bytes=_sp.MAX_CONTROL_BYTES,
                                     error_cls=PauseControlError, noun="task pause")
        if raw is None:
            return None
        pause = _parse_task_pause(jid, raw)

        archive_fd = _open_named_dir(job_fd, PAUSE_ARCHIVE_DIRNAME, create=True)
        assert archive_fd is not None
        archive_tasks_fd = _open_named_dir(archive_fd, TASK_ARCHIVE_SUBDIR, create=True)
        assert archive_tasks_fd is not None
        payload = dict(pause.to_json())
        payload["outcome"] = "released"
        payload["settled_at"] = _sp.utc_now_iso()
        _fs.write_file_atomically(archive_tasks_fd, name, _fs.json_bytes(payload),
                                  create_only=True, file_mode=_sp.CONTROL_FILE_MODE,
                                  error_cls=PauseControlError, noun="task pause archive")

        _fs.require_writable_dir(tasks_fd, error_cls=PauseControlError, noun="pause-control",
                                 label=name)
        _fs.unlink_at(name, tasks_fd, error_cls=PauseControlError, noun="task pause")
        return pause
    finally:
        if archive_tasks_fd is not None:
            os.close(archive_tasks_fd)
        if archive_fd is not None:
            os.close(archive_fd)
        if tasks_fd is not None:
            os.close(tasks_fd)
        os.close(job_fd)


def paused_tasks(job_id: str, *,
                 control_root_path: Path | None = None) -> tuple[TaskPause, ...]:
    """Every paused task, ordered by ``requested_at`` then ``task_id``. An entry that cannot
    be read or parsed RAISES — dropping it would dispatch a task the operator paused."""
    jid = _sp.validate_job_id(job_id)
    job_fd = _sp.open_job_control_fd(jid, control_root_path, create=False)
    if job_fd is None:
        return ()
    tasks_fd = None
    try:
        tasks_fd = _open_named_dir(job_fd, PAUSED_TASKS_DIRNAME, create=False)
        if tasks_fd is None:
            return ()
        names = _fs.list_dir_names(tasks_fd, error_cls=PauseControlError,
                                   noun="paused tasks")
        out: list[TaskPause] = []
        for name in names:
            raw = _fs.read_verified_file(name, tasks_fd, max_bytes=_sp.MAX_CONTROL_BYTES,
                                         error_cls=PauseControlError, noun="task pause")
            if raw is None:
                continue
            out.append(_parse_task_pause(jid, raw))
        out.sort(key=lambda p: (p.requested_at, p.task_id))
        return tuple(out)
    finally:
        if tasks_fd is not None:
            os.close(tasks_fd)
        os.close(job_fd)


# ---------------------------------------------------------------------------
# S5 — the mask, pure
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WithheldTasks:
    """The pure mask's answer, all four tuples ordered per the module docstring's rules."""

    withheld: tuple[str, ...]
    paused: tuple[str, ...]
    downstream: tuple[str, ...]
    inert: tuple[str, ...]


def withheld_task_ids(order: Iterable[str], pending: Iterable[str], paused: Iterable[str],
                      *, depends_on: Mapping[str, Iterable[str]] | None = None
                      ) -> WithheldTasks:
    """Which of ``order``'s ids a pause withholds. Pure: no I/O, no clock.

    LINEAR (``depends_on`` None): the first paused PENDING task in plan order and every
    pending task after it are withheld; tasks before it are not. GRAPH: the paused pending
    tasks and every pending task that transitively depends on one of them are withheld. A
    task that is not pending is never withheld and never propagates, in either scope.
    """
    order_list = list(order)
    pending_set = set(pending)

    seen: set[str] = set()
    paused_given_order: list[str] = []
    for pid in paused:
        if pid not in seen:
            seen.add(pid)
            paused_given_order.append(pid)
    paused_set = set(paused_given_order)
    paused_pending = {pid for pid in paused_set if pid in pending_set}

    if depends_on is None:
        withheld_set: set[str] = set()
        idx_start = next(
            (i for i, pid in enumerate(order_list) if pid in paused_pending), None)
        if idx_start is not None:
            for pid in order_list[idx_start:]:
                if pid in pending_set:
                    withheld_set.add(pid)
    else:
        dependents: dict[str, list[str]] = {}
        for tid, deps in depends_on.items():
            for dep in deps:
                dependents.setdefault(dep, []).append(tid)
        withheld_set = set(paused_pending)
        queue: list[str] = list(paused_pending)
        while queue:
            current = queue.pop(0)
            for dependent in dependents.get(current, ()):
                if dependent in withheld_set:
                    continue
                if dependent not in pending_set:
                    continue                       # not pending: never withheld, never spreads
                withheld_set.add(dependent)
                queue.append(dependent)

    withheld_field = tuple(pid for pid in order_list if pid in withheld_set)
    paused_field = tuple(pid for pid in order_list if pid in paused_pending)
    downstream_field = tuple(pid for pid in withheld_field if pid not in paused_pending)
    inert_field = tuple(pid for pid in paused_given_order if pid not in pending_set)

    return WithheldTasks(withheld=withheld_field, paused=paused_field,
                         downstream=downstream_field, inert=inert_field)


# ---------------------------------------------------------------------------
# S6 — the shared effects (DECISION F025 D2): the CLI and the door call these
# two functions, and nothing else, to pause or unpause a job or one of its
# tasks. Each takes a loaded ``JobPlan`` and never raises for a refusal —
# a job whose state is terminal or a task id the plan does not hold answers
# outcome ``refused`` instead, naming the state or the task.
# ---------------------------------------------------------------------------

#: The states D2 refuses a pause or an unpause over. Mirrors
#: ``job_stop_cmd._FINISHED_STATES``, widened to the three names D2 rules —
#: that set answers a different question ("can a stop still be requested")
#: and is untouched by this feature.
_TERMINAL_STATES = frozenset({"completed", "failed", "cancelled"})

#: The state a job carries while parked by an operator pause — ``RunState.PAUSED``'s
#: own value, read as a bare string so this module need not import the enum
#: (it already avoids importing ``pingpong_job``; see the module docstring).
_PARKED_STATE = "paused"


def _job_state_str(job: Any) -> str:
    """``job.state`` as a bare string, whether it is a ``RunState`` or already one."""
    state = getattr(job, "state", "")
    return state.value if hasattr(state, "value") else str(state)


def _job_task_ids(job: Any) -> frozenset[str]:
    """Every task id ``job``'s own plan holds."""
    return frozenset(str(getattr(t, "task_id", "")) for t in getattr(job, "tasks", ()))


def _refuse_unknown_task(task_id: str, job: Any) -> dict[str, Any] | None:
    """None when ``task_id`` is one of ``job``'s own; D2's ``refused`` body otherwise."""
    if task_id in _job_task_ids(job):
        return None
    return {"outcome": "refused", "reason": f"unknown task {task_id!r}",
           "scope": "task", "task_id": task_id}


def _task_pause_event_exists(job_id: str, event: str, request_id: str) -> bool | None:
    """Has this exact request already produced a ``task_paused`` or ``task_resumed``
    ledger event? Mirrors ``pingpong_job._job_paused_event_exists`` exactly — True/False,
    or None when the ledger could not be read at all, which must never be mistaken for
    "no event": writing a second one would break exactly-once (R-1052)."""
    try:
        from packages.orchestration.data_paths import run_log_dir

        job_runs = run_log_dir(job_id)
        if not job_runs.is_dir():
            return False
        for jsonl in sorted(job_runs.glob("*.jsonl")):
            for line in jsonl.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    raw = json.loads(line)
                except ValueError:
                    continue                      # a torn line is not our event
                if (raw.get("event") == event
                        and str(raw.get("job_id")) == job_id
                        and str((raw.get("metadata") or {}).get("request_id")) == request_id):
                    return True
        return False
    except OSError:
        return None


def _write_task_paused_event(job: Any, pause: TaskPause) -> None:
    """One ``task_paused`` ledger event, an inline literal through ``RunLogWriter``
    (DECISION F025 D2 clause 3) — the caller writes this only when the LEDGER holds
    none for this request id yet (R-1052), never a second time for the same request."""
    from packages.orchestration.run_log import RunLogWriter

    writer = RunLogWriter(job.job_id)
    writer.log(
        "task_paused",
        outcome="paused",
        scope="task",
        task_id=pause.task_id,
        request_id=pause.request_id,
        reason=pause.reason,
        source=pause.source,
        requested_at=pause.requested_at,
    )


def _write_task_resumed_event(job: Any, pause: TaskPause) -> None:
    """One ``task_resumed`` ledger event, an inline literal through ``RunLogWriter``
    (DECISION F025 D2 clause 3) — the caller writes this only when the LEDGER holds
    none for this request id yet (R-1052), and BEFORE the entry is released, so a
    failed write leaves the task paused rather than silently losing the event."""
    from packages.orchestration.run_log import RunLogWriter

    writer = RunLogWriter(job.job_id)
    writer.log(
        "task_resumed",
        outcome="resumed",
        scope="task",
        task_id=pause.task_id,
        request_id=pause.request_id,
        reason=pause.reason,
        source=pause.source,
        requested_at=pause.requested_at,
    )


def pause_job_command(job: Any, *, task_id: str | None = None, reason: str = "",
                      source: str, control_root_path: Path | None = None
                      ) -> dict[str, Any]:
    """Pause ``job`` as a whole, or one of its tasks — the effect the CLI and
    the door share (DECISION F025 D2 clause 2). ``job`` is a loaded ``JobPlan``.

    Never raises for a refusal: a job whose state is completed, failed or
    cancelled, or a task id the plan does not hold, answers outcome
    ``refused`` with a ``reason`` naming the state or the task. Otherwise
    answers ``requested`` (job scope) or ``paused`` (task scope), each with
    the request id.
    """
    state = _job_state_str(job)
    if state in _TERMINAL_STATES:
        body: dict[str, Any] = {"outcome": "refused", "reason": state,
                                "scope": "task" if task_id else "job"}
        if task_id:
            body["task_id"] = task_id
        return body

    if task_id:
        refusal = _refuse_unknown_task(task_id, job)
        if refusal is not None:
            return refusal
        pause = request_task_pause(job.job_id, task_id, reason, source,
                                   control_root_path=control_root_path)
        # R-1052: exactly once per request id BY THE LEDGER, as `job_paused` is — not
        # by whether this call is the one that created the control-file entry, which
        # a retry after a failed write can never be.
        already = _task_pause_event_exists(job.job_id, "task_paused", pause.request_id)
        if already is not None and not already:
            _write_task_paused_event(job, pause)
        return {"outcome": "paused", "request_id": pause.request_id, "scope": "task",
                "task_id": task_id}

    signal = request_pause(job.job_id, reason, source, control_root_path=control_root_path)
    return {"outcome": "requested", "request_id": signal.request_id, "scope": "job"}


def unpause_job_command(job: Any, *, task_id: str | None = None, source: str,
                        control_root_path: Path | None = None) -> dict[str, Any]:
    """Release a pause on ``job``, or on one of its tasks — ``pause_job_command``'s
    reverse (DECISION F025 D2 clause 2). ``job`` is a loaded ``JobPlan``.

    Never raises for a refusal: the same terminal-state and unknown-task
    checks ``pause_job_command`` applies. With a task, answers ``released``
    or ``not_paused``. Without one (R-1051): a pending request is withdrawn
    first — ``withdrawn`` — whatever the job's state; only once nothing is
    pending does a job the last park left in state ``paused`` WITH a
    non-empty pause record answer ``parked`` with the relaunch command; a
    job the task cap parked, whose pause record is empty, falls through to
    ``not_paused`` like any other job with nothing pending.
    """
    state = _job_state_str(job)
    if state in _TERMINAL_STATES:
        body: dict[str, Any] = {"outcome": "refused", "reason": state,
                                "scope": "task" if task_id else "job"}
        if task_id:
            body["task_id"] = task_id
        return body

    if task_id:
        refusal = _refuse_unknown_task(task_id, job)
        if refusal is not None:
            return refusal
        pause = next(
            (p for p in paused_tasks(job.job_id, control_root_path=control_root_path)
             if p.task_id == task_id), None)
        if pause is None:
            return {"outcome": "not_paused", "scope": "task", "task_id": task_id}
        # R-1052: the event is written BEFORE the entry is released, so a failed
        # write raises with the task still paused — the retry finds the same
        # entry, the same request id, and writes the missing event exactly once.
        already = _task_pause_event_exists(job.job_id, "task_resumed", pause.request_id)
        if already is not None and not already:
            _write_task_resumed_event(job, pause)
        release_task_pause(job.job_id, task_id, control_root_path=control_root_path)
        return {"outcome": "released", "request_id": pause.request_id, "scope": "task",
                "task_id": task_id}

    # R-1051: a pending job pause is withdrawn first, whatever the job's state — a
    # pause requested again on an already-parked job must be answered `withdrawn`,
    # not `parked` (which would send the operator to relaunch straight back into
    # the same park). Only once nothing is pending does a job the last park left
    # in `paused` WITH a non-empty pause record answer `parked`; a job the task
    # cap parked (state `paused`, `job.pause` empty) falls through to `not_paused`.
    pending = withdraw_pause(job.job_id, control_root_path=control_root_path)
    if pending is not None:
        return {"outcome": "withdrawn", "request_id": pending.request_id, "scope": "job"}

    if state == _PARKED_STATE and job.pause:
        return {"outcome": "parked", "scope": "job",
                "next": f"remedy job run {job.job_id}"}

    return {"outcome": "not_paused", "scope": "job"}
