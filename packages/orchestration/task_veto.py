"""F027 T001 — the veto control protocol (DECISION F027 D1).

A veto is a CONTROL FACT, never a write of ``job.json``: ``run_job`` in
``pingpong_job.py`` walks a job's tasks in memory and saves the whole record at
its own points (DECISION F026 D1), so a command that wrote ``job.json`` while a
job runs would simply be overwritten at the runner's next save. A veto is
instead one create-only file per vetoed task under the job's control
directory, reached through ``safe_points.open_job_control_fd`` and the same
``secure_fs`` primitives F011's kill switch and F025's pause use — a runner
folds the fact into the record at its own safe points, and a reader that needs
a veto no runner has folded yet reads the control files directly.

The reason is mandatory and kept VERBATIM: an operator's own words travel
into the event, the record, the report and the page unchanged, so a reason
that cannot be trusted as given — empty, oversized, or holding a control
character or secret-shaped text — is REFUSED outright rather than stored in
some altered form that would silently misrepresent what the operator wrote.

There is no un-veto in v1: reversibility would blur the human red line this
feature exists to draw, and the intended recovery from a mistaken veto is the
replan proposal (T002), not a second command undoing the first.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.common import secure_fs as _fs
from packages.orchestration import safe_points as _sp
from packages.orchestration.dag_schedule import blocked_downstream
from packages.orchestration.failure_postmortem import safe_text
from packages.orchestration.pingpong_job import (
    TASK_BLOCKED,
    TASK_FAILED,
    TASK_PENDING,
    TASK_RUNNING,
    TASK_SKIPPED,
    TASK_VETOED,
)
from packages.orchestration.stream_evidence import redact_text

__all__ = [
    "TaskVetoRefused",
    "TaskVetoError",
    "TaskVeto",
    "MAX_VETO_REASON_CHARS",
    "VETOABLE_TASK_STATUSES",
    "VETOED_TASKS_DIRNAME",
    "validate_veto_reason",
    "veto_refusal",
    "veto_unreachable",
    "record_task_veto",
    "vetoed_tasks",
    "veto_task_command",
]

VETOED_TASKS_DIRNAME = "vetoed_tasks"

#: A task id is operator/planner input that becomes a filename's SOURCE, never the filename
#: itself (the file is named by its digest — see ``_veto_filename``); it is bounded and
#: refused if it carries a control character, but never made "safe" by stripping anything.
#: Mirrors ``pause_control.MAX_TASK_ID_CHARS`` exactly, kept as this module's own constant
#: because ``pause_control`` is not imported here.
MAX_TASK_ID_CHARS = 200
_CONTROL_CHAR_RE = re.compile(r"[\x00-\x1f\x7f]")

TASK_VETO_VERSION = 1

MAX_VETO_REASON_CHARS = 500

#: S4 — the task statuses a veto may still act on. Every other status, `passed`,
#: `applied_to_job_workspace`, `split`, `vetoed` and `completed` among them, is refused.
VETOABLE_TASK_STATUSES = (TASK_PENDING, TASK_RUNNING, TASK_BLOCKED, TASK_FAILED, TASK_SKIPPED)

#: The job states a veto is refused over — mirrors ``pause_control._TERMINAL_STATES``.
_JOB_TERMINAL_STATES = frozenset({"completed", "failed", "cancelled"})


class TaskVetoRefused(Exception):
    """A refusal an operator can act on: a bad reason, or the gate. Carries ``code`` and
    ``detail`` rather than a bare message, so a caller can render either without parsing text.
    """

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


class TaskVetoError(RuntimeError):
    """The veto control area could not be used, or an on-disk entry could not be trusted.

    Loud on purpose, same as ``safe_points.StopControlError`` and
    ``pause_control.PauseControlError``: a silently dropped veto entry would dispatch work the
    operator vetoed.
    """


@dataclass(frozen=True)
class TaskVeto:
    """One vetoed task, the control fact itself."""

    job_id: str
    task_id: str
    request_id: str
    reason: str
    actor: str
    requested_at: str
    status_at_veto: str

    def to_json(self) -> dict[str, Any]:
        return {
            "task_veto_v": TASK_VETO_VERSION,
            "job_id": self.job_id,
            "task_id": self.task_id,
            "request_id": self.request_id,
            "reason": self.reason,
            "actor": self.actor,
            "requested_at": self.requested_at,
            "status_at_veto": self.status_at_veto,
        }


def _state_str(value: Any) -> str:
    """A ``RunState`` or a plain string, read as its bare string value either way."""
    return value.value if hasattr(value, "value") else str(value)


# ---------------------------------------------------------------------------
# S3 — the reason, mandatory and kept verbatim
# ---------------------------------------------------------------------------


def validate_veto_reason(reason: Any) -> str:
    """Refuse, or return ``reason`` UNCHANGED — never stripped, bounded or redacted.

    In order: not a string, or empty after ``.strip()``, is ``reason_required``; longer than
    ``MAX_VETO_REASON_CHARS`` is ``reason_too_long``; holding any character of
    ``[\\x00-\\x1f\\x7f]`` (newline and tab included), or differing from ``redact_text``'s
    reading of it, is ``reason_invalid``.
    """
    if not isinstance(reason, str) or not reason.strip():
        raise TaskVetoRefused(
            "reason_required", "a veto reason is required and must not be empty or blank")
    if len(reason) > MAX_VETO_REASON_CHARS:
        raise TaskVetoRefused(
            "reason_too_long",
            f"a veto reason is at most {MAX_VETO_REASON_CHARS} characters")
    if _CONTROL_CHAR_RE.search(reason) or redact_text(reason) != reason:
        raise TaskVetoRefused(
            "reason_invalid",
            "a veto reason holding a control character or secret-shaped text is refused "
            "rather than stored altered")
    return reason


# ---------------------------------------------------------------------------
# S4 — the gate, pure
# ---------------------------------------------------------------------------


def veto_refusal(job_state: Any, task_status: Any, *, already_vetoed: bool
                 ) -> TaskVetoRefused | None:
    """Pure, no I/O. None when ``job_state``/``task_status`` admit a veto.

    R-1065's repair: the ``task_already_vetoed`` detail says the task is already vetoed —
    never the status it happened to carry — because the command answers this refusal from
    an entry's own request id, not from the gate's read of the task's current status.
    """
    state = _state_str(job_state)
    status = _state_str(task_status)
    if state in _JOB_TERMINAL_STATES:
        return TaskVetoRefused("job_not_vetoable", f"the job is {state!r}")
    if already_vetoed or status == TASK_VETOED:
        return TaskVetoRefused("task_already_vetoed", "the task is already vetoed")
    if status not in VETOABLE_TASK_STATUSES:
        return TaskVetoRefused("task_not_vetoable", f"the task is {status!r}")
    return None


# ---------------------------------------------------------------------------
# S5 — the unreachable set, pure
# ---------------------------------------------------------------------------


def veto_unreachable(tasks: Any, vetoed_ids: Any) -> tuple[str, ...]:
    """``blocked_downstream`` over ``vetoed_ids``, minus the vetoed ids themselves, keeping
    only tasks a veto could still act on — in the order of ``tasks``."""
    vetoed_set = set(vetoed_ids)
    blocked = blocked_downstream(tasks, vetoed_set) - vetoed_set
    return tuple(
        task.task_id for task in tasks
        if task.task_id in blocked and _state_str(task.status) in VETOABLE_TASK_STATUSES)


# ---------------------------------------------------------------------------
# S6 — the control files
# ---------------------------------------------------------------------------


def _validate_job_id(job_id: str) -> str:
    try:
        return _sp.validate_job_id(job_id)
    except _sp.StopControlError as exc:
        raise TaskVetoError(str(exc)) from exc


def _validate_task_id(task_id: Any) -> str:
    """Mirrors ``pause_control._validate_task_id`` exactly, raising ``TaskVetoError``."""
    if (not isinstance(task_id, str) or not task_id or len(task_id) > MAX_TASK_ID_CHARS
            or _CONTROL_CHAR_RE.search(task_id)):
        raise TaskVetoError(
            f"invalid task id {task_id!r}: a task id is 1-{MAX_TASK_ID_CHARS} characters "
            f"with no control character")
    return task_id


def _bounded_actor(actor: Any) -> str:
    cleaned = safe_text(str(actor or "")).replace("\n", " ").replace("\r", " ").strip()
    if not cleaned:
        return "unknown"
    return cleaned[:_sp.MAX_SOURCE_CHARS]


def _veto_filename(task_id: str) -> str:
    """Named by a digest of the id, never by the id itself: an id holding ``/``, ``..`` or
    any other path-shaped text can never become — or escape — a path component."""
    digest = hashlib.sha256(task_id.encode("utf-8")).hexdigest()[:32]
    return f"{digest}.json"


def _open_named_dir(parent_fd: int, name: str, *, create: bool) -> int | None:
    """One verified subdirectory of the job's control directory. Mirrors
    ``pause_control._open_named_dir``, written fresh so this module need not import that one."""
    try:
        return _fs.open_verified_dir(name, dir_fd=parent_fd, error_cls=TaskVetoError,
                                     noun="task-veto-control")
    except _fs.MissingComponent:
        if not create:
            return None
    _fs.require_writable_dir(parent_fd, error_cls=TaskVetoError, noun="task-veto-control",
                             label=name)
    try:
        os.mkdir(name, _sp.CONTROL_DIR_MODE, dir_fd=parent_fd)
    except FileExistsError:
        pass                                        # a concurrent creator; verify below
    except OSError as exc:
        raise TaskVetoError(
            f"cannot create the task-veto control directory {name!r} "
            f"({type(exc).__name__}: {exc.strerror or exc})") from exc
    try:
        return _fs.open_verified_dir(name, dir_fd=parent_fd, error_cls=TaskVetoError,
                                     noun="task-veto-control")
    except _fs.MissingComponent as exc:
        raise TaskVetoError(
            f"the task-veto control directory {name!r} vanished after creation") from exc


def _parse_task_veto(job_id: str, raw: bytes) -> TaskVeto:
    try:
        data = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise TaskVetoError(f"the task veto entry is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise TaskVetoError("the task veto entry is not a JSON object")
    task_id = data.get("task_id")
    request_id = data.get("request_id")
    if not isinstance(task_id, str) or not task_id:
        raise TaskVetoError("the task veto entry carries no task id")
    if not isinstance(request_id, str) or not request_id:
        raise TaskVetoError("the task veto entry carries no request id")
    try:
        reason = validate_veto_reason(data.get("reason"))
    except TaskVetoRefused as exc:
        # Dropping this entry would dispatch a task the operator vetoed — a tampered or
        # corrupted reason is loud, never silently discarded.
        raise TaskVetoError(
            f"the stored veto reason for {task_id!r} fails validation: {exc.detail}") from exc
    return TaskVeto(
        job_id=job_id,
        task_id=task_id,
        request_id=request_id,
        reason=reason,
        actor=str(data.get("actor") or "unknown"),
        requested_at=str(data.get("requested_at") or ""),
        status_at_veto=str(data.get("status_at_veto") or ""),
    )


def record_task_veto(job_id: str, task_id: str, reason: str, actor: str, status_at_veto: Any, *,
                     control_root_path: Path | None = None) -> tuple[TaskVeto, bool]:
    """Publish one create-only veto file for ``task_id``. Answers the new veto and ``True``,
    or — an entry already existed, before this write or after losing the publication race —
    that entry read back unchanged and ``False``."""
    validated_reason = validate_veto_reason(reason)
    tid = _validate_task_id(task_id)
    jid = _validate_job_id(job_id)
    bounded_actor = _bounded_actor(actor)
    status_str = _state_str(status_at_veto)

    try:
        job_fd = _sp.open_job_control_fd(jid, control_root_path, create=True)
    except _sp.StopControlError as exc:
        raise TaskVetoError(str(exc)) from exc
    assert job_fd is not None
    tasks_fd = None
    try:
        tasks_fd = _open_named_dir(job_fd, VETOED_TASKS_DIRNAME, create=True)
        assert tasks_fd is not None
        name = _veto_filename(tid)
        existing = _fs.read_verified_file(name, tasks_fd, max_bytes=_sp.MAX_CONTROL_BYTES,
                                          error_cls=TaskVetoError, noun="task veto")
        if existing is not None:
            return _parse_task_veto(jid, existing), False

        veto = TaskVeto(
            job_id=jid,
            task_id=tid,
            request_id=_sp.new_request_id(),
            reason=validated_reason,
            actor=bounded_actor,
            requested_at=_sp.utc_now_iso(),
            status_at_veto=status_str,
        )
        published = _fs.write_file_atomically(
            tasks_fd, name, _fs.json_bytes(veto.to_json()), create_only=True,
            file_mode=_sp.CONTROL_FILE_MODE, error_cls=TaskVetoError, noun="task veto")
        if not published:
            raw = _fs.read_verified_file(name, tasks_fd, max_bytes=_sp.MAX_CONTROL_BYTES,
                                         error_cls=TaskVetoError, noun="task veto")
            if raw is None:
                raise TaskVetoError(
                    "the task veto vanished during publication; no veto was recorded")
            return _parse_task_veto(jid, raw), False
        return veto, True
    finally:
        if tasks_fd is not None:
            os.close(tasks_fd)
        os.close(job_fd)


def vetoed_tasks(job_id: str, *,
                 control_root_path: Path | None = None) -> tuple[TaskVeto, ...]:
    """Every vetoed task, ordered by ``requested_at`` then ``task_id``. ``()`` when the
    control root, the job's directory or ``vetoed_tasks/`` does not exist. An entry that
    cannot be read, is not a JSON object, lacks a task id or a request id, or whose stored
    reason fails S3 RAISES — dropping it would dispatch a task the operator vetoed."""
    jid = _validate_job_id(job_id)
    try:
        job_fd = _sp.open_job_control_fd(jid, control_root_path, create=False)
    except _sp.StopControlError as exc:
        raise TaskVetoError(str(exc)) from exc
    if job_fd is None:
        return ()
    tasks_fd = None
    try:
        tasks_fd = _open_named_dir(job_fd, VETOED_TASKS_DIRNAME, create=False)
        if tasks_fd is None:
            return ()
        names = _fs.list_dir_names(tasks_fd, error_cls=TaskVetoError, noun="vetoed tasks")
        out: list[TaskVeto] = []
        for name in names:
            raw = _fs.read_verified_file(name, tasks_fd, max_bytes=_sp.MAX_CONTROL_BYTES,
                                         error_cls=TaskVetoError, noun="task veto")
            if raw is None:
                continue
            out.append(_parse_task_veto(jid, raw))
        out.sort(key=lambda v: (v.requested_at, v.task_id))
        return tuple(out)
    finally:
        if tasks_fd is not None:
            os.close(tasks_fd)
        os.close(job_fd)


# ---------------------------------------------------------------------------
# S8 — the event, an inline literal through RunLogWriter (mirrors
# pause_control._task_pause_event_exists / _write_task_paused_event exactly).
# ---------------------------------------------------------------------------


def _task_vetoed_event_exists(job_id: str, request_id: str) -> bool | None:
    """Has this exact request already produced a ``task_vetoed`` ledger event? True/False,
    or None when the ledger could not be read at all — never mistaken for "no event": writing
    a second one would break exactly-once."""
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
                    continue                        # a torn line is not our event
                if (raw.get("event") == "task_vetoed"
                        and str(raw.get("job_id")) == job_id
                        and str((raw.get("metadata") or {}).get("request_id")) == request_id):
                    return True
        return False
    except OSError:
        return None


def _write_task_vetoed_event(job: Any, veto: TaskVeto, unreachable: list[str]) -> None:
    from packages.orchestration.run_log import RunLogWriter

    writer = RunLogWriter(job.job_id)
    writer.log(
        "task_vetoed",
        outcome="vetoed",
        scope="task",
        task_id=veto.task_id,
        request_id=veto.request_id,
        reason=veto.reason,
        actor=veto.actor,
        status_at_veto=veto.status_at_veto,
        requested_at=veto.requested_at,
        unreachable_task_ids=list(unreachable),
    )


def _event_unreachable(job: Any, veto: TaskVeto, control_root_path: Path | None) -> list[str]:
    """``veto_unreachable`` over this veto alone, without every task another entry of
    ``vetoed_tasks`` already holds."""
    other_ids = {v.task_id for v in vetoed_tasks(job.job_id, control_root_path=control_root_path)
                if v.task_id != veto.task_id}
    return [tid for tid in veto_unreachable(job.tasks, [veto.task_id]) if tid not in other_ids]


def _maybe_repair_task_vetoed_event(job: Any, veto: TaskVeto, unreachable: list[str]) -> None:
    """Write the audit event only when the ledger could be read and holds none for this
    request id yet — so a retry after a failed event write repairs the line exactly once."""
    already = _task_vetoed_event_exists(job.job_id, veto.request_id)
    if already is not None and not already:
        _write_task_vetoed_event(job, veto, unreachable)


def _already_vetoed_refusal(job: Any, task_id: str, veto: TaskVeto | None,
                            control_root_path: Path | None) -> dict[str, Any]:
    """R-1065's repair: the ONE shape ``task_already_vetoed`` answers with, whether the gate
    read an existing entry or ``record_task_veto`` just lost a create-only race for one.

    When an entry exists, its audit event is repaired first — the one write a refusal may
    make — and its ``request_id`` travels with the refusal. A task whose status merely
    READS ``vetoed`` with no entry to point at (``veto`` is None) repairs nothing and
    answers ``request_id`` "": there is nothing recorded to repair or to name.
    """
    if veto is None:
        return {"outcome": "refused", "code": "task_already_vetoed",
                "detail": "the task is already vetoed", "task_id": task_id, "request_id": ""}
    unreachable = _event_unreachable(job, veto, control_root_path)
    _maybe_repair_task_vetoed_event(job, veto, unreachable)
    return {"outcome": "refused", "code": "task_already_vetoed",
            "detail": "the task is already vetoed", "task_id": task_id,
            "request_id": veto.request_id}


# ---------------------------------------------------------------------------
# S7 — the command effect, shared by the CLI and the door
# ---------------------------------------------------------------------------


def veto_task_command(job: Any, *, task_id: str, reason: str, actor: str,
                      control_root_path: Path | None = None) -> dict[str, Any]:
    """Veto one task of ``job``, a loaded ``JobPlan``. Never raises for a refusal, and never
    writes ``job.json``: it answers ``{"outcome": "refused", "code", "detail", "task_id"}``,
    checking in order the reason, an unknown task id, and the gate. An already-vetoed task —
    whether the gate's own read found the entry, or ``record_task_veto`` lost a create-only
    race against another veto of the same task — answers the SAME refused shape (R-1065):
    ``code`` ``task_already_vetoed``, a ``request_id`` naming the entry that won, and its
    missing audit event repaired first. Otherwise it records the veto and answers ``vetoed``
    with the unreachable set.
    """
    try:
        validated_reason = validate_veto_reason(reason)
    except TaskVetoRefused as exc:
        return {"outcome": "refused", "code": exc.code, "detail": exc.detail,
                "task_id": task_id}

    task = next((t for t in job.tasks if str(getattr(t, "task_id", "")) == task_id), None)
    if task is None:
        return {"outcome": "refused", "code": "unknown_task",
                "detail": f"unknown task {task_id!r}", "task_id": task_id}

    existing = next(
        (v for v in vetoed_tasks(job.job_id, control_root_path=control_root_path)
         if v.task_id == task_id), None)
    refusal = veto_refusal(getattr(job, "state", ""), task.status,
                           already_vetoed=existing is not None)
    if refusal is not None:
        if refusal.code == "task_already_vetoed":
            return _already_vetoed_refusal(job, task_id, existing, control_root_path)
        return {"outcome": "refused", "code": refusal.code, "detail": refusal.detail,
                "task_id": task_id}

    veto, created = record_task_veto(job.job_id, task_id, validated_reason, actor,
                                     task.status, control_root_path=control_root_path)
    if not created:
        # A create-only race was lost: the SAME entry now exists under someone else's
        # write. Answer it exactly as the gate's own route does (R-1065).
        return _already_vetoed_refusal(job, task_id, veto, control_root_path)

    # We won the race: this is the FIRST time this entry exists, so its audit event is
    # written here (never merely "repaired" — there is nothing yet to repair).
    unreachable = _event_unreachable(job, veto, control_root_path)
    _maybe_repair_task_vetoed_event(job, veto, unreachable)

    return {"outcome": "vetoed", "request_id": veto.request_id, "task_id": task_id,
            "reason": veto.reason, "actor": veto.actor, "status_at_veto": veto.status_at_veto,
            "unreachable": unreachable}
