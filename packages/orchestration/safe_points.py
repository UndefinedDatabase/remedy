"""F011 — the kill switch's control protocol and safe points.

A running job is stopped by writing a small file, not by killing a process. `remedy job
stop` writes one JSON control file into a private area of the data root and returns; the
runner reads it at a SAFE POINT — a place where no work is in flight and nothing is half
written — and then stops on purpose: the provider call already running finishes, nothing new
begins, the incomplete task goes back to `pending`, and the job is persisted as `stopped`.

No signal handler, no thread, no daemon, no socket, no database. A stop is a fact on disk.

Three properties this module exists to guarantee:

* **The control area cannot be redirected.** Every read, write, archive and removal happens
  through directory descriptors we opened and identity-verified ourselves, using the shared
  primitives in ``packages/common/secure_fs.py`` — the same ones F010's post-mortem writer
  uses. A symlinked ``control``, ``jobs`` or job directory is refused, not followed; a
  read-only control area raises rather than silently doing nothing (even for root, because
  the check reads the DECLARED mode bits, and ``os.access`` lies to root).
* **The check is cheap.** ``stop_requested()`` opens the job's control directory, stats one
  name and reads one small file. It loads no config, scans no tree and takes no lock,
  because it runs before every provider call.
* **One request is one episode.** Publication is create-only, so two concurrent `job stop`
  callers converge on ONE request id. A consumed request is ARCHIVED under that id, never
  deleted — and the pending file is removed only AFTER the job is durably `stopped`, so a
  crash mid-finalization loses nothing: the next run sees the request again and finishes
  the same episode, without a second event or a second post-mortem.
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import os
import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.common import secure_fs as _fs
from packages.orchestration.failure_postmortem import safe_text

#: The control area is this user's private business: 0700 directories, 0600 files.
CONTROL_DIR_MODE = 0o700
CONTROL_FILE_MODE = 0o600

STOP_SIGNAL_VERSION = 1

STOP_REQUEST_FILENAME = "stop.json"
STOP_ARCHIVE_DIRNAME = "archive"
JOBS_DIRNAME = "jobs"

#: Bounds. A control file is operator input: it is small, or it is not a control file.
MAX_REASON_CHARS = 500
MAX_SOURCE_CHARS = 120
MAX_TIMESTAMP_CHARS = 64
MAX_CONTROL_BYTES = 64 * 1024

UNKNOWN_REASON = "unknown"
UNKNOWN_SOURCE = "unknown"

#: A job id and a request id are PATH COMPONENTS. Anything that is not one is refused before
#: it is ever joined to a path — including an id read back out of a malformed control file,
#: which is attacker-controlled input like any other.
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")


class StopControlError(RuntimeError):
    """The control area could not be used. Loud on purpose: a silent no-op here means an
    operator believes a job is stopping when nothing asked it to."""


class StopArchiveConflictError(StopControlError):
    """An archived request with this id already exists and says something else."""


@dataclass(frozen=True)
class StopSignal:
    """StopSignalV1 — one operator request to stop one job.

    Immutable, bounded, redacted, free of absolute paths, and every field is validated on
    the way IN: it is copied into a ledger event, a post-mortem and an Evidence bundle, all
    of which other people read.
    """

    job_id: str
    request_id: str
    reason: str = UNKNOWN_REASON
    source: str = UNKNOWN_SOURCE
    requested_at: str = ""
    stop_signal_v: int = STOP_SIGNAL_VERSION
    #: True when the on-disk request could not be trusted and this signal was reconstructed.
    degraded: bool = False

    def to_json(self) -> dict[str, Any]:
        return {
            "stop_signal_v": self.stop_signal_v,
            "job_id": self.job_id,
            "request_id": self.request_id,
            "reason": self.reason,
            "source": self.source,
            "requested_at": self.requested_at,
        }


@dataclass(frozen=True)
class StopStatus:
    """What `remedy job stop --status` needs to tell the truth in one shot."""

    job_id: str
    pending: StopSignal | None = None
    archived: tuple[StopSignal, ...] = field(default_factory=tuple)

    @property
    def consumed_count(self) -> int:
        return len(self.archived)

    def to_json(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id,
            "pending": self.pending.to_json() if self.pending else None,
            "consumed_count": self.consumed_count,
            "archived": [s.to_json() for s in self.archived],
        }


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Validation — everything that becomes a path, and everything that becomes evidence
# ---------------------------------------------------------------------------


def validate_job_id(job_id: str) -> str:
    text = str(job_id or "").strip()
    if not _ID_RE.match(text):
        raise StopControlError(
            f"invalid job id {job_id!r}: a job id is 1-64 characters of "
            f"letters, digits, '-' or '_'")
    return text


def is_safe_id(value: Any) -> bool:
    """A request id is a filename. `../../../../escaped` is not one."""
    return isinstance(value, str) and bool(_ID_RE.match(value))


def new_request_id() -> str:
    """Unique per REQUEST, not per job: a job stopped twice has two of these."""
    return uuid.uuid4().hex[:16]


def _degraded_id(raw: bytes) -> str:
    """A deterministic, always-safe id for a control file we cannot trust.

    Deterministic so that re-reading the same corrupt file twice is the SAME episode, and
    safe by construction so that nothing an attacker wrote can ever become a path.
    """
    return "malformed-" + hashlib.sha256(raw).hexdigest()[:12]


def normalize_timestamp(value: Any) -> str:
    """A parsed timestamp is untrusted text until it parses as one.

    The reviewed build copied `requested_at` verbatim out of the control file into the
    ledger event, the post-mortem and the Evidence bundle — so
    ``API_KEY=supersecret /home/alice/private`` travelled all the way into the package.
    Anything that is not a bounded ISO-8601 timestamp is simply not a timestamp, and
    becomes empty.
    """
    if not isinstance(value, str):
        return ""
    text = value.strip()
    if not text or len(text) > MAX_TIMESTAMP_CHARS:
        return ""
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return ""
    return text


def _bounded(text: Any, limit: int, fallback: str) -> str:
    """Bounded, redacted, single-line. Operator text ends up in an Evidence bundle."""
    cleaned = safe_text(str(text or "")).replace("\n", " ").replace("\r", " ").strip()
    if not cleaned:
        return fallback
    return cleaned[:limit]


# ---------------------------------------------------------------------------
# Paths (for reporting) and anchored handles (for doing anything)
# ---------------------------------------------------------------------------


def control_root(root: Path | None = None) -> Path:
    from packages.orchestration.data_paths import control_dir

    return control_dir(root)


def job_control_dir(job_id: str, control_root_path: Path | None = None) -> Path:
    base = control_root_path if control_root_path is not None else control_root()
    return Path(base) / JOBS_DIRNAME / validate_job_id(job_id)


def stop_request_path(job_id: str, control_root_path: Path | None = None) -> Path:
    return job_control_dir(job_id, control_root_path) / STOP_REQUEST_FILENAME


def stop_archive_dir(job_id: str, control_root_path: Path | None = None) -> Path:
    return job_control_dir(job_id, control_root_path) / STOP_ARCHIVE_DIRNAME


def _ensure_control_root(base: Path) -> Path:
    """Verify — and if necessary CREATE — the control root, without ever using a name.

    The previous version called ``base.parent.mkdir(parents=True)`` before any secure
    anchoring ran, so an unverified parent chain could be materialised (and followed) before
    a single check happened. Nothing is created by name here now: ``anchor_root(create=True)``
    walks from the filesystem root, verifies every component it passes, and creates a missing
    one THROUGH the descriptor it holds, at 0700. A validation that fails therefore leaves
    nothing behind — least of all under a symlink.
    """
    base = Path(os.path.normpath(os.path.abspath(str(base))))
    fd = _fs.anchor_root(base, error_cls=StopControlError, noun="stop-control",
                         create=True, dir_mode=CONTROL_DIR_MODE)
    os.close(fd)
    return base


# The one shared way into a job's private control directory: every writer that needs a
# handle under `control/jobs/<job_id>` goes through here rather than opening it by name.
def open_job_control_fd(job_id: str, control_root_path: Path | None, *,
                        create: bool) -> int | None:
    """A verified directory fd for ``control/jobs/<job_id>``. None when it does not exist.

    Every component — the control root, ``jobs``, the job directory — is inspected without
    following symlinks, opened relative to the handle above it, and identity-checked against
    what was inspected. A symlink anywhere on that path is refused; nothing is written
    outside the control root, ever.
    """
    jid = validate_job_id(job_id)
    base = Path(control_root_path) if control_root_path is not None else control_root()
    base = Path(os.path.normpath(str(base)))

    if create:
        _ensure_control_root(base)
    else:
        # Read path: the root must already exist. It is still ANCHORED (walked and verified
        # from the filesystem root) — a missing one simply means "no request pending".
        try:
            os.close(_fs.anchor_root(base, error_cls=StopControlError,
                                     noun="stop-control"))
        except StopControlError as exc:
            if "does not exist" in str(exc):
                return None
            raise

    try:
        return _fs.anchor_destination(
            base / JOBS_DIRNAME / jid, base,
            error_cls=StopControlError, noun="stop-control",
            create=create, dir_mode=CONTROL_DIR_MODE)
    except _fs.MissingComponent:
        return None


def _open_archive_fd(job_fd: int, *, create: bool) -> int | None:
    """The archive directory, through the job control fd we already hold."""
    try:
        return _fs.open_verified_dir(STOP_ARCHIVE_DIRNAME, dir_fd=job_fd,
                                     error_cls=StopControlError, noun="stop-control")
    except _fs.MissingComponent:
        if not create:
            return None
    # Create it through the held fd — never by name, never with a default 0755 mode.
    _fs.require_writable_dir(job_fd, error_cls=StopControlError, noun="stop-control",
                             label=STOP_ARCHIVE_DIRNAME)
    try:
        os.mkdir(STOP_ARCHIVE_DIRNAME, CONTROL_DIR_MODE, dir_fd=job_fd)
    except FileExistsError:
        pass
    except OSError as exc:
        raise StopControlError(
            f"cannot create the stop archive directory "
            f"({type(exc).__name__}: {exc.strerror or exc})") from exc
    try:
        return _fs.open_verified_dir(STOP_ARCHIVE_DIRNAME, dir_fd=job_fd,
                                     error_cls=StopControlError, noun="stop-control")
    except _fs.MissingComponent as exc:
        raise StopControlError("the stop archive directory vanished after creation") from exc


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def _parse_signal(job_id: str, raw: bytes) -> StopSignal:
    """Turn control bytes into a signal. Never raises on CONTENT.

    A corrupt control file is still an operator asking us to stop; refusing to stop because
    we cannot read *why* would be the worst possible reading of the request. But nothing in
    it is trusted: an unknown version or an unsafe request id falls back to the deterministic
    degraded id, so `"request_id": "../../../../escaped"` can never become a path.
    """
    degraded_id = _degraded_id(raw)
    try:
        data = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        data = None
    if not isinstance(data, dict):
        return StopSignal(job_id=job_id, request_id=degraded_id, reason=UNKNOWN_REASON,
                          source=UNKNOWN_SOURCE, requested_at="", degraded=True)

    version = data.get("stop_signal_v")
    request_id = data.get("request_id")
    if version != STOP_SIGNAL_VERSION or not is_safe_id(request_id):
        # Unknown version, or an id we would not dare put in a path: keep the stop, drop
        # every untrusted field, and identify the episode by the bytes themselves.
        return StopSignal(job_id=job_id, request_id=degraded_id, reason=UNKNOWN_REASON,
                          source=UNKNOWN_SOURCE,
                          requested_at=normalize_timestamp(data.get("requested_at")),
                          degraded=True)

    return StopSignal(
        job_id=job_id,
        request_id=request_id,
        reason=_bounded(data.get("reason"), MAX_REASON_CHARS, UNKNOWN_REASON),
        source=_bounded(data.get("source"), MAX_SOURCE_CHARS, UNKNOWN_SOURCE),
        requested_at=normalize_timestamp(data.get("requested_at")),
    )


def _read_request(job_fd: int) -> bytes | None:
    return _fs.read_verified_file(STOP_REQUEST_FILENAME, job_fd,
                                  max_bytes=MAX_CONTROL_BYTES,
                                  error_cls=StopControlError, noun="stop request")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def request_stop(job_id: str, reason: str = "", source: str = "cli",
                 *, control_root_path: Path | None = None) -> StopSignal:
    """Ask a job to stop. Durable, private, atomic — and idempotent even under a race.

    Publication is CREATE-ONLY. Two `remedy job stop` processes that both see no pending
    request no longer each write their own: the loser's ``os.link`` fails, it reads the
    winner's file, and both return the SAME request id. One operator, one episode — and a
    valid pending request is never overwritten.
    """
    jid = validate_job_id(job_id)
    job_fd = open_job_control_fd(jid, control_root_path, create=True)
    assert job_fd is not None                     # create=True either makes it or raises
    try:
        existing = _read_request(job_fd)
        if existing is not None:
            return _parse_signal(jid, existing)   # pending stands — including a degraded one

        signal = StopSignal(
            job_id=jid,
            request_id=new_request_id(),
            reason=_bounded(reason, MAX_REASON_CHARS, UNKNOWN_REASON),
            source=_bounded(source, MAX_SOURCE_CHARS, UNKNOWN_SOURCE),
            requested_at=utc_now_iso(),
        )
        published = _fs.write_file_atomically(
            job_fd, STOP_REQUEST_FILENAME, _fs.json_bytes(signal.to_json()),
            create_only=True, file_mode=CONTROL_FILE_MODE,
            error_cls=StopControlError, noun="stop request")
        if not published:
            # Another caller won the race between our read and our link. Their request is
            # the episode; ours never existed.
            raw = _read_request(job_fd)
            if raw is None:
                raise StopControlError(
                    "the stop request vanished during publication; no stop was requested")
            return _parse_signal(jid, raw)
        return signal
    finally:
        os.close(job_fd)


def stop_requested(job_id: str, *,
                   control_root_path: Path | None = None) -> StopSignal | None:
    """The safe-point check: is a stop pending? One directory open, one stat, one read."""
    jid = validate_job_id(job_id)
    job_fd = open_job_control_fd(jid, control_root_path, create=False)
    if job_fd is None:
        return None
    try:
        raw = _read_request(job_fd)
    finally:
        os.close(job_fd)
    if raw is None:
        return None
    return _parse_signal(jid, raw)


def archive_stop(job_id: str, signal: StopSignal, *,
                 control_root_path: Path | None = None) -> str:
    """Publish the archived copy of a request — WITHOUT removing the pending file.

    This is step one of a two-step consume. The pending request stays exactly where it is
    until the job is durably `stopped` on disk, because a request that is gone while the job
    still says `planned` is a stop that has been thrown away.

    Idempotent: an identical archive already there is a success (a previous attempt got this
    far); a DIFFERENT archive under the same id is a conflict and is never overwritten.
    Returns the control-relative reference.
    """
    jid = validate_job_id(job_id)
    if not is_safe_id(signal.request_id):        # belt and braces at the path boundary
        raise StopControlError(
            f"refusing to archive an unsafe request id {signal.request_id!r}")

    payload = signal.to_json()
    name = f"{signal.request_id}.json"
    job_fd = open_job_control_fd(jid, control_root_path, create=True)
    assert job_fd is not None
    archive_fd = None
    try:
        archive_fd = _open_archive_fd(job_fd, create=True)
        assert archive_fd is not None
        published = _fs.write_file_atomically(
            archive_fd, name, _fs.json_bytes(payload), create_only=True,
            file_mode=CONTROL_FILE_MODE, error_cls=StopControlError,
            noun="stop archive")
        if not published:
            raw = _fs.read_verified_file(name, archive_fd, max_bytes=MAX_CONTROL_BYTES,
                                         error_cls=StopControlError, noun="stop archive")
            existing = json.loads(raw.decode("utf-8")) if raw else None
            if existing != payload:
                raise StopArchiveConflictError(
                    f"an archived stop request {signal.request_id!r} already exists and "
                    f"differs from the pending one; refusing to overwrite stop history")
        return f"{JOBS_DIRNAME}/{jid}/{STOP_ARCHIVE_DIRNAME}/{name}"
    finally:
        if archive_fd is not None:
            os.close(archive_fd)
        os.close(job_fd)


def acknowledge_stop(job_id: str, signal: StopSignal, *,
                     control_root_path: Path | None = None) -> bool:
    """Remove the pending request — the LAST step, once the stop is durably recorded.

    Refuses to remove a pending request that is not the one we archived: if the operator
    requested a *new* stop in the meantime, that request belongs to the next episode.
    """
    jid = validate_job_id(job_id)
    job_fd = open_job_control_fd(jid, control_root_path, create=False)
    if job_fd is None:
        return False
    try:
        raw = _read_request(job_fd)
        if raw is None:
            return False                          # already acknowledged; nothing to do
        pending = _parse_signal(jid, raw)
        if pending.request_id != signal.request_id:
            return False                          # a newer request: not ours to remove
        _fs.require_writable_dir(job_fd, error_cls=StopControlError, noun="stop-control",
                                 label=STOP_REQUEST_FILENAME)
        return _fs.unlink_at(STOP_REQUEST_FILENAME, job_fd,
                             error_cls=StopControlError, noun="stop request")
    finally:
        os.close(job_fd)


def consume_stop(job_id: str, *,
                 control_root_path: Path | None = None) -> StopSignal | None:
    """Archive the pending request and remove it, in one go.

    Kept for callers with nothing durable to checkpoint between the two halves (and for the
    tests). The job runner does NOT use this: it archives, records, persists, and only then
    acknowledges — see ``pingpong_job._stop_job``.
    """
    signal = stop_requested(job_id, control_root_path=control_root_path)
    if signal is None:
        return None
    archive_stop(job_id, signal, control_root_path=control_root_path)
    acknowledge_stop(job_id, signal, control_root_path=control_root_path)
    return signal


def clear_stop(job_id: str, *, control_root_path: Path | None = None) -> bool:
    """Drop a pending request WITHOUT consuming it (no episode, no archive)."""
    jid = validate_job_id(job_id)
    job_fd = open_job_control_fd(jid, control_root_path, create=False)
    if job_fd is None:
        return False
    try:
        if _fs.read_verified_file(STOP_REQUEST_FILENAME, job_fd,
                                  error_cls=StopControlError,
                                  noun="stop request") is None:
            return False
        _fs.require_writable_dir(job_fd, error_cls=StopControlError, noun="stop-control",
                                 label=STOP_REQUEST_FILENAME)
        return _fs.unlink_at(STOP_REQUEST_FILENAME, job_fd,
                             error_cls=StopControlError, noun="stop request")
    finally:
        os.close(job_fd)


def archived_signals(job_id: str, *,
                     control_root_path: Path | None = None) -> list[StopSignal]:
    """Every consumed request, read through held descriptors — no glob, no second walk."""
    jid = validate_job_id(job_id)
    job_fd = open_job_control_fd(jid, control_root_path, create=False)
    if job_fd is None:
        return []
    archive_fd = None
    out: list[StopSignal] = []
    try:
        archive_fd = _open_archive_fd(job_fd, create=False)
        if archive_fd is None:
            return []
        for name in _fs.list_dir_names(archive_fd, error_cls=StopControlError,
                                       noun="stop archive"):
            if not name.endswith(".json"):
                continue
            with contextlib.suppress(StopControlError):
                raw = _fs.read_verified_file(name, archive_fd,
                                             max_bytes=MAX_CONTROL_BYTES,
                                             error_cls=StopControlError,
                                             noun="stop archive")
                if raw is not None:
                    out.append(_parse_signal(jid, raw))
    finally:
        if archive_fd is not None:
            os.close(archive_fd)
        os.close(job_fd)
    out.sort(key=lambda s: (s.requested_at, s.request_id))
    return out


def is_archived(job_id: str, request_id: str, *,
                control_root_path: Path | None = None) -> bool:
    """Has this exact request already been archived? (Used by the finalization retry.)"""
    if not is_safe_id(request_id):
        return False
    return any(s.request_id == request_id
               for s in archived_signals(job_id, control_root_path=control_root_path))


def stop_status(job_id: str, *, control_root_path: Path | None = None) -> StopStatus:
    """Everything on disk about this job's stops: what is pending, what was consumed."""
    jid = validate_job_id(job_id)
    return StopStatus(
        job_id=jid,
        pending=stop_requested(jid, control_root_path=control_root_path),
        archived=tuple(archived_signals(jid, control_root_path=control_root_path)),
    )


# ---------------------------------------------------------------------------
# Unified should_stop — ONE evaluation per safe point
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ShouldStopResult:
    """Result of the unified safe-point check."""

    should_stop: bool
    reason: str = ""
    source: str = ""
    operator_signal: StopSignal | None = None
    budget_evaluation: Any = None

    def to_json(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "should_stop": self.should_stop,
            "reason": self.reason,
            "source": self.source,
        }
        if self.operator_signal is not None:
            d["operator_signal"] = self.operator_signal.to_json()
        if self.budget_evaluation is not None:
            d["budget_evaluation"] = self.budget_evaluation.to_json()
        return d


#: Every budget tick of ONE job shares ONE run-log file. `RunLogWriter` mints a
#: fresh run id per instance and the emitter below is constructed per safe-point
#: evaluation, so the default would leave one `.jsonl` file per safe point for the
#: length of a long job (DECISION F022 D2, clause three). Nothing in Remedy parses
#: a run-log file NAME — `timeline.load_run_events` globs `*.jsonl` and sorts by
#: timestamp — so a stable name costs nothing.
BUDGET_TICK_RUN_ID = "budget-ticks"


def _budget_tick_payload(evaluation: Any) -> dict[str, Any]:
    """The absolute figures one budget tick carries, and the basis of each.

    DECISION F022 D1 fixes this field set. A key exists only when its value does:
    an unconfigured limit is an ABSENT KEY, never a null and never a zero, which
    is what stops a limitless job from rendering a fabricated denominator. No
    display sentence is transported; the basis strings are composed in the client.

    `basis.cost` reads `absent` before it reads anything else, because an unpriced
    run has no cost figure to call a lower bound — `evaluate_budget` sets
    `cost_lower_bound` in that case too, and it means "the limit cannot be decided",
    not "the figure is a floor".

    No key here collides with a NAMED parameter of `RunLogWriter.log` (`task_id`,
    `artifact_id`, `provider`, `role`, `model`, `outcome`, `message`); a colliding
    key would be hijacked out of `metadata` into the event envelope.
    `TestPayloadKeysNeverCollide` pins that against the live signature.
    """
    counters = evaluation.counters
    limits = evaluation.configured_limits
    payload: dict[str, Any] = {
        "spent_tokens": counters.measured_token_total,
        "unmeasured_calls": counters.unmeasured_call_count,
    }
    if counters.measured_cost_usd is not None:
        payload["spent_usd"] = counters.measured_cost_usd
    if limits is not None:
        if limits.max_total_tokens is not None:
            payload["limit_tokens"] = limits.max_total_tokens
        if limits.max_cost_usd is not None:
            payload["limit_usd"] = limits.max_cost_usd
    if counters.measured_cost_usd is None:
        cost_basis = "absent"
    elif evaluation.cost_lower_bound:
        cost_basis = "lower_bound"
    else:
        cost_basis = "actual"
    payload["basis"] = {
        "tokens": "lower_bound" if evaluation.token_lower_bound else "actual",
        "cost": cost_basis,
    }
    return payload


def _emit_budget_tick(job_id: str, evaluation: Any) -> None:
    """Write ONE budget tick beside the safe-point decision, never into it.

    The tick is a NOTIFICATION: `should_stop`'s result, its reason and its source
    are the same whether this writes or raises. DECISION F022 D1 puts the emission
    ABOVE the exhaustion test so the evaluation that stops a job still reports the
    money it spent.

    The writer is `RunLogWriter` and NOT `timeline.append_run_event` (DECISION F022
    D2, clause one): `append_run_event` resolves its id with `UUID(str(job_id))`,
    while a JobPlan's `job_id` is `uuid4().hex[:16]` — sixteen hex characters, which
    `UUID()` rejects. The short route would raise on every ping-pong safe point and
    the soft failure below would swallow it, leaving the ticker silently dead on the
    one job shape that runs long enough to need it.

    The event name is an INLINE string literal (DECISION F022 D2, clause two):
    `tests/ui_contracts/test_humanize_catalog.py` derives the Python stream
    vocabulary with an AST walk that keeps a name only when it is an `ast.Constant`,
    so a module constant would be invisible to it and the catalog key would sit
    unpaired.

    It FAILS SOFT for `_emit_command_accepted_event`'s reason: a notification that
    breaks the run it reports on is worse than a missing frame. The caught set is
    spelled out rather than written as `except Exception` — `OSError` from the
    filesystem, `RuntimeError`, and `ValueError` / `TypeError` from serialising the
    payload.
    """
    from packages.orchestration.run_log import RunLogWriter

    try:
        writer = RunLogWriter(job_id, run_id=BUDGET_TICK_RUN_ID)
        writer.log("budget.tick", **_budget_tick_payload(evaluation))
    except (OSError, RuntimeError, ValueError, TypeError):   # D2, clause four
        return


def should_stop(
    job_id: str,
    *,
    budgets: Any | None = None,
    counters: Any | None = None,
    now: datetime | None = None,
    control_root_path: Path | None = None,
) -> ShouldStopResult:
    """Unified safe-point check: operator stop first, then budget, then continue.

    This is the SINGLE entry point for safe-point evaluation.
    Call it once per safe point; never call stop_requested and budget check separately.
    """
    signal = stop_requested(job_id, control_root_path=control_root_path)
    if signal is not None:
        return ShouldStopResult(
            should_stop=True,
            reason=f"operator_stop: {signal.reason}",
            source="operator",
            operator_signal=signal,
        )

    if budgets is not None and counters is not None:
        from packages.orchestration.budget_guard import evaluate_budget

        evaluation = evaluate_budget(budgets, counters, now=now)
        _emit_budget_tick(job_id, evaluation)
        if evaluation.exhausted:
            limit = evaluation.first_exhausted_limit or "unknown"
            return ShouldStopResult(
                should_stop=True,
                reason=f"budget_exhausted:{limit}",
                source="budget",
                budget_evaluation=evaluation,
            )

    return ShouldStopResult(should_stop=False)
