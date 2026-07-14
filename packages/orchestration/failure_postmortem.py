"""Automatic failure post-mortems (F010).

Every FINAL failure — a provider call that is abandoned, a task that ends terminally
failed — leaves one machine-readable record explaining what failed and *which signal said
so*. Nothing here guesses, summarizes or calls a model: the classifier is a pure function,
and the record is written atomically to a file.

Three pieces:

* :class:`FailureClass` — one extensible enum for every layer. Later features add members;
  they do not add enums.
* :func:`classify` — pure. No I/O, no clock, no environment, no mutation. It never raises
  for an unknown combination; it returns :attr:`FailureClass.UNKNOWN` and says so.
* :func:`write_postmortem` — atomic, exactly-once, contained.

What is deliberately NOT here: retries (F001 owns the policy — this module imports its
timeout/non-zero predicates rather than re-deriving them), the kill switch (F011), budgets
(F018) and any generated prose. ``stopped`` and ``budget_exhausted`` are reserved classes:
classifiable, wired to nothing.
"""
from __future__ import annotations

import contextlib
import enum
import json
import os
import secrets
import stat
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path, PurePath
from typing import Any

from packages.common import secure_fs as _fs
from packages.orchestration.provider_timeouts import (
    is_nonzero_exit_error,
    is_timeout_error,
)

#: Record version. A reader may refuse a version it does not know.
POSTMORTEM_VERSION = 1

#: The file name of both the call-level record and the task-level rollup. They never
#: collide: one lives in a call directory, the other in ``task_runs/<task_id>/``.
POSTMORTEM_FILENAME = "postmortem.json"

#: A raw reason is a diagnostic, not a payload. Bounded, deterministically.
MAX_RAW_REASON_CHARS = 2000

#: Truncation marker appended when a reason is cut. Part of the contract: a reader can
#: tell a short reason from a truncated one.
TRUNCATION_SUFFIX = "…[truncated]"

#: How many retry reasons a record carries.
MAX_RETRY_REASONS = 20

#: The three scopes a record can have. They are counted separately, never merged: a job
#: that never reached a task, a task that failed, and the calls below it are three
#: different facts about the same afternoon.
SCOPE_CALL = "call"
SCOPE_TASK = "task"
SCOPE_JOB = "job"
SCOPES = (SCOPE_CALL, SCOPE_TASK, SCOPE_JOB)


class PostmortemError(RuntimeError):
    """A post-mortem could not be written. Never swallowed, never guessed around."""


class PostmortemConflictError(PostmortemError):
    """A DIFFERENT post-mortem already exists at this path.

    Exactly-once means exactly once: re-writing the identical logical record is fine
    (idempotent), silently overwriting a different one is not — that would destroy the
    only account of the first failure.
    """


class FailureClass(str, enum.Enum):
    """Why something finally failed. One enum for every layer, extensible by later
    features (F011 uses ``STOPPED``, F018 uses ``BUDGET_EXHAUSTED``)."""

    PROVIDER_TIMEOUT = "provider_timeout"
    PROVIDER_UNAVAILABLE = "provider_unavailable"
    PROVIDER_NONZERO_EXIT = "provider_nonzero_exit"
    PARSE = "parse"
    CONFIG = "config"
    TEST_FAILED = "test_failed"
    REVIEW_FAILED = "review_failed"
    WORKTREE_CONFLICT = "worktree_conflict"
    WORKTREE_LOCK = "worktree_lock"
    RUNTIME_PROBE_FAILED = "runtime_probe_failed"
    #: Reserved for F011's kill switch. Classifiable; nothing in F010 produces it.
    STOPPED = "stopped"
    #: Reserved for F018's budgets. Classifiable; nothing in F010 produces it.
    BUDGET_EXHAUSTED = "budget_exhausted"
    UNKNOWN = "unknown"


#: The precedence chain, most authoritative first. `signal_source` always names the
#: winning link, so a contradictory input set can be explained rather than argued about.
SIGNAL_TYPED_EXCEPTION = "typed_exception"
SIGNAL_TERMINAL_STATUS = "terminal_status"
SIGNAL_ERROR_CLASS = "error_class"
SIGNAL_RETRY_REASONS = "retry_reasons"
SIGNAL_ERROR_TEXT = "error_text"
SIGNAL_NONE = "none"


def is_provider_unavailable_error(error: str | None) -> bool:
    """Does this error mean "the provider executable is not there"?

    Not a retry predicate — the retry policy has no opinion about a missing binary — so it
    lives here rather than in F001's module.
    """
    if not error:
        return False
    lowered = error.lower()
    return (
        "no such file or directory" in lowered
        or "filenotfounderror" in lowered
        or "not found" in lowered
        or "not installed" in lowered
        or "executable" in lowered and "missing" in lowered
        or "provider_unavailable" in lowered
    )


#: Terminal loop/task statuses that ARE a failure, mapped to their class. A status that is
#: not a failure (``staged_review_passed``) is deliberately absent.
TERMINAL_STATUS_CLASSES: dict[str, FailureClass] = {
    "provider_unavailable": FailureClass.PROVIDER_UNAVAILABLE,
    "test_failed": FailureClass.TEST_FAILED,
    "review_failed": FailureClass.REVIEW_FAILED,
    "worktree_conflict": FailureClass.WORKTREE_CONFLICT,
    "worktree_lock": FailureClass.WORKTREE_LOCK,
    "runtime_probe_failed": FailureClass.RUNTIME_PROBE_FAILED,
    "stopped": FailureClass.STOPPED,
    "budget_exhausted": FailureClass.BUDGET_EXHAUSTED,
}

#: Structured ``error_class`` values produced by the provider layer.
ERROR_CLASS_CLASSES: dict[str, FailureClass] = {
    "parse": FailureClass.PARSE,
    "config": FailureClass.CONFIG,
}


@dataclass(frozen=True)
class FailureSignals:
    """Everything known about ONE failure, as facts rather than as an argument list.

    A typed record instead of eight positional strings: a caller cannot silently pass the
    reviewer's error where the builder's belonged, and a new signal is a new field rather
    than a new parameter in five call sites.
    """

    exception: BaseException | None = None
    #: A terminal loop/task status such as ``test_failed`` (see TERMINAL_STATUS_CLASSES).
    terminal_status: str = ""
    #: The provider layer's structured ``error_class`` ("parse" | "config" | "").
    error_class: str = ""
    #: The raw provider/task error message.
    error_text: str = ""
    #: F001's retry evidence, verbatim.
    retry_reasons: tuple[str, ...] = ()
    #: A runtime-probe failure observed inside an orchestration context (F007 payload).
    runtime_probe_failed: bool = False
    #: A reviewer verdict such as ``needs_repair`` — a normal rejection, NOT a transport
    #: failure. Present so the classifier can refuse to misread it as one.
    reviewer_verdict: str = ""


@dataclass(frozen=True)
class CallRetryEvidence:
    """The retries of ONE logical provider call — not of the whole run.

    ``PingPongResult.retry_reasons`` is a run-global summary: it contains the builder's
    timeout from round 1 as happily as the reviewer's failure in round 3. Handing that to
    the classifier made an unrelated builder timeout classify a reviewer failure as
    ``provider_timeout`` "because the retry evidence said so". This carries only what the
    call being recorded actually did.
    """

    retries_used: int = 0
    retry_reasons: tuple[str, ...] = ()

    @classmethod
    def of(cls, reasons: list[str]) -> CallRetryEvidence:
        return cls(retries_used=len(reasons), retry_reasons=tuple(reasons))


@dataclass(frozen=True)
class Classification:
    """The verdict: the class, and which signal produced it."""

    failure_class: FailureClass
    signal_source: str
    reason: str = ""


def _classify_exception(exc: BaseException) -> Classification | None:
    """Typed exceptions win: they are the least ambiguous thing we ever get."""
    from packages.orchestration.worktrees import (
        WorktreeConflictError,
        WorktreeLockError,
    )

    text = f"{type(exc).__name__}: {exc}"
    if isinstance(exc, WorktreeConflictError):
        return Classification(FailureClass.WORKTREE_CONFLICT, SIGNAL_TYPED_EXCEPTION, text)
    if isinstance(exc, WorktreeLockError):
        return Classification(FailureClass.WORKTREE_LOCK, SIGNAL_TYPED_EXCEPTION, text)
    if isinstance(exc, FileNotFoundError):
        return Classification(
            FailureClass.PROVIDER_UNAVAILABLE, SIGNAL_TYPED_EXCEPTION, text)
    if isinstance(exc, TimeoutError) or type(exc).__name__ == "TimeoutExpired":
        return Classification(FailureClass.PROVIDER_TIMEOUT, SIGNAL_TYPED_EXCEPTION, text)
    if type(exc).__name__ == "CalledProcessError":
        return Classification(
            FailureClass.PROVIDER_NONZERO_EXIT, SIGNAL_TYPED_EXCEPTION, text)
    return None


def _classify_error_text(text: str) -> FailureClass | None:
    """Transport classes read out of a message — through the SHARED predicates.

    ``provider_unavailable`` is checked before the timeout/non-zero predicates: "claude CLI
    not found" is a missing binary, not a non-zero exit, whatever else the sentence says.
    """
    if not text:
        return None
    if is_provider_unavailable_error(text):
        return FailureClass.PROVIDER_UNAVAILABLE
    if is_timeout_error(text):
        return FailureClass.PROVIDER_TIMEOUT
    if is_nonzero_exit_error(text):
        return FailureClass.PROVIDER_NONZERO_EXIT
    return None


def classify(signals: FailureSignals) -> Classification:
    """Pure. Same signals in, same class out — no I/O, no clock, no environment.

    Precedence, and the reason for it:

    1. **typed exception** — a `WorktreeLockError` is not an opinion;
    2. **explicit terminal loop/task signal** — the layer that gave up said why;
    3. **structured ``error_class``** — the provider layer's own verdict (parse/config);
    4. **retry evidence** — what F001 saw while it was still trying;
    5. **unknown** — said out loud, never raised and never guessed.

    A reviewer verdict of ``needs_repair`` is a normal rejection. It is not a provider
    transport failure and never becomes one here.
    """
    if signals.exception is not None:
        verdict = _classify_exception(signals.exception)
        if verdict is not None:
            return verdict
        # An untyped exception is still an exception: fall through to the weaker signals,
        # carrying its text.

    if signals.runtime_probe_failed:
        return Classification(
            FailureClass.RUNTIME_PROBE_FAILED, SIGNAL_TERMINAL_STATUS,
            signals.error_text or "runtime probe failed")

    status = (signals.terminal_status or "").strip()
    if status in TERMINAL_STATUS_CLASSES:
        return Classification(
            TERMINAL_STATUS_CLASSES[status], SIGNAL_TERMINAL_STATUS, status)

    error_class = (signals.error_class or "").strip()
    if error_class in ERROR_CLASS_CLASSES:
        return Classification(
            ERROR_CLASS_CLASSES[error_class], SIGNAL_ERROR_CLASS, error_class)

    from_text = _classify_error_text(signals.error_text or "")
    if from_text is not None:
        return Classification(from_text, SIGNAL_ERROR_TEXT, signals.error_text or "")

    for reason in signals.retry_reasons:
        from_retry = _classify_error_text(reason)
        if from_retry is not None:
            return Classification(from_retry, SIGNAL_RETRY_REASONS, reason)

    if signals.exception is not None:
        return Classification(
            FailureClass.UNKNOWN, SIGNAL_TYPED_EXCEPTION,
            f"{type(signals.exception).__name__}: {signals.exception}")

    return Classification(FailureClass.UNKNOWN, SIGNAL_NONE, signals.error_text or "")


#: What an operational path becomes: a stable, portable reference.
RUNTIME_DATA_PREFIX = "[runtime-data]"
OPAQUE_PATH_PREFIX = "[path]"


def _safe_path_reference(raw: str) -> str:
    """A portable stand-in for one absolute local path.

    A post-mortem is read on another machine. ``/tmp/pytest-of-decodeux/…/pingpong_runs/r1``
    tells that reader nothing and tells everyone else where this box keeps its data. Under
    the Remedy data root the path keeps its meaning as ``[runtime-data]/pingpong_runs/r1/…``;
    anything else keeps only its file name. The words that classify a failure —
    ``postmortem.json``, ``read-only``, ``WorktreeLockError`` — are never touched, because
    they are not paths.
    """
    candidate = raw.rstrip(".,;:)")
    trailer = raw[len(candidate):]
    try:
        from packages.orchestration.data_paths import resolve_data_root
        data_root = resolve_data_root().resolve()
        resolved = Path(candidate).resolve()
        if resolved == data_root or data_root in resolved.parents:
            rel = resolved.relative_to(data_root).as_posix()
            return f"{RUNTIME_DATA_PREFIX}/{rel}{trailer}" if rel else (
                f"{RUNTIME_DATA_PREFIX}{trailer}")
    except (OSError, ValueError):
        pass
    name = PurePath(candidate.replace("\\", "/")).name or "path"
    return f"{OPAQUE_PATH_PREFIX}/{name}{trailer}"


def safe_text(text: str | None) -> str:
    """Deterministic, provider-free redaction of anything a post-mortem carries.

    Three established mechanisms, none of them invented here:

    1. **secrets** — ``stream_evidence.redact_text`` (API keys, tokens, passwords,
       credentials, private-key material, provider key formats);
    2. **local paths hidden behind a label** — ``cwd:/tmp/secret-repo`` → ``cwd:secret-repo``
       (the colon is exactly where the URL-preserving path regex stops looking);
    3. **local paths and `file:` URIs** — F007's accepted scrubber, now shared
       (``packages/common/path_redaction.py``): POSIX, Windows (both slash styles), UNC,
       quoted paths with spaces, percent-encoded `file:` URIs, and the scheme boundary that
       leaves ``profile:``/``myfile:``/``notafile:`` alone.

    An operational path under the Remedy data root keeps its meaning as
    ``[runtime-data]/…`` — that is a reference, not a leak. Everything that makes a failure
    classifiable (``timed out``, ``WorktreeLockError``, ``read-only``, ``postmortem.json``)
    survives.
    """
    if not text:
        return ""
    from packages.common.path_redaction import (
        ABS_PATH_RE,
        FILE_URI_RE,
        QUOTED_PATH_RE,
        basename,
        file_uri_basename,
        scrub_labelled_paths,
    )
    from packages.orchestration.stream_evidence import redact_text

    out = redact_text(str(text))
    out = scrub_labelled_paths(out)                                   # cwd:/tmp/x → cwd:x
    out = FILE_URI_RE.sub(lambda m: file_uri_basename(m.group(0)), out)
    out = QUOTED_PATH_RE.sub(
        lambda m: f"{m.group(1)}{basename(m.group(2))}{m.group(1)}", out)
    # Bare absolute paths last, so a path under the Remedy data root can keep its MEANING
    # as `[runtime-data]/…` instead of collapsing to a bare file name.
    return ABS_PATH_RE.sub(lambda m: _safe_path_reference(m.group(0)), out)


def truncate_reason(text: str | None, limit: int = MAX_RAW_REASON_CHARS) -> str:
    """Bound a raw reason deterministically: the first ``limit`` characters, marked."""
    if not text:
        return ""
    if len(text) <= limit:
        return text
    return text[:limit] + TRUNCATION_SUFFIX


def _validate_evidence_ref(ref: str) -> str:
    """An evidence reference must be relative, normalized, contained and portable.

    An absolute path is somebody's laptop; a ``..`` is an escape. Neither belongs in a
    record that will be read on another machine.
    """
    raw = str(ref or "").strip()
    if not raw:
        raise ValueError("evidence reference is empty")
    if raw.startswith("/") or raw.startswith("\\") or (len(raw) > 1 and raw[1] == ":"):
        raise ValueError(f"evidence reference must be relative: {ref!r}")
    parts = _ref_parts(raw)
    if any(p == ".." for p in parts):
        raise ValueError(f"evidence reference must not traverse upwards: {ref!r}")
    return "/".join(p for p in parts if p not in ("", "."))


def _ref_parts(raw: str) -> list[str]:
    """Split a reference the same way on every platform."""
    return raw.replace("\\", "/").split("/")


def utc_now_iso() -> str:
    """The repository's normal timestamp shape."""
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class PostmortemV1:
    """The record. One per final failure, machine-readable, portable."""

    failure_class: FailureClass
    signal_source: str
    job_id: str = ""
    task_id: str = ""
    run_id: str = ""
    call_id: str = ""
    role: str = ""
    provider: str = ""
    scope: str = SCOPE_CALL                # "call" | "task" | "job"
    raw_reason: str = ""
    terminal_status: str = ""
    retry_reasons: tuple[str, ...] = ()
    retries_used: int = 0
    evidence_refs: tuple[str, ...] = ()
    created_at: str = field(default_factory=utc_now_iso)
    postmortem_v: int = POSTMORTEM_VERSION

    def to_json(self) -> dict[str, Any]:
        """Stable key order; no absolute path anywhere."""
        return {
            "postmortem_v": self.postmortem_v,
            "scope": self.scope,
            "failure_class": self.failure_class.value,
            "signal_source": self.signal_source,
            "job_id": self.job_id,
            "task_id": self.task_id,
            "run_id": self.run_id,
            "call_id": self.call_id,
            "role": self.role,
            "provider": self.provider,
            "terminal_status": self.terminal_status,
            # Redacted BEFORE it is written: a post-mortem that leaks the API key it
            # failed on is a worse artifact than no post-mortem at all.
            "raw_reason": truncate_reason(safe_text(self.raw_reason)),
            "retries_used": self.retries_used,
            "retry_reasons": [
                truncate_reason(safe_text(r), 500)
                for r in list(self.retry_reasons)[:MAX_RETRY_REASONS]
            ],
            "evidence_refs": [_validate_evidence_ref(r) for r in self.evidence_refs],
            "created_at": self.created_at,
        }


def _identity(payload: dict[str, Any]) -> dict[str, Any]:
    """The parts of a record that make it THE record for one logical failure.

    ``created_at`` is deliberately excluded: writing the same failure twice a second apart
    is still the same failure, and a clock tick must not turn idempotence into a conflict.
    """
    return {k: v for k, v in payload.items() if k != "created_at"}


#: The primitives the anchored writer needs. Without them containment cannot be GUARANTEED,
#: only hoped for, and this module fails closed rather than pretending.
#: The primitives the anchored writer needs. Note what is NOT in this list: the mere
#: EXISTENCE of ``O_NOFOLLOW``. The reviewer's Linux 4.4 host has the constant, advertises
#: dir_fd support — and still opened a directory symlink through ``O_NOFOLLOW|O_DIRECTORY``.
#: A flag that the kernel accepts and ignores is not a guarantee, so the guarantee here is
#: made of things we can CHECK ourselves: a no-follow ``stat`` relative to a directory fd,
#: an ``fstat`` on what we actually opened, and the comparison of the two identities.
#: ``O_NOFOLLOW`` stays on every open as defence in depth; it is no longer the argument.
_DIR_FD_SUPPORTED = (
    os.open in getattr(os, "supports_dir_fd", set())
    and os.mkdir in getattr(os, "supports_dir_fd", set())
    and os.link in getattr(os, "supports_dir_fd", set())
    and os.unlink in getattr(os, "supports_dir_fd", set())
    and os.stat in getattr(os, "supports_dir_fd", set())
    and os.stat in getattr(os, "supports_follow_symlinks", set())
)

_OPEN_DIR_FLAGS = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)


def _require_platform() -> None:
    """No semantic guarantee, no write. There is no "best effort" mode here."""
    if not _DIR_FD_SUPPORTED:
        raise PostmortemError(
            "this platform cannot guarantee post-mortem containment (no directory-fd "
            "stat/open/mkdir/link/unlink with follow_symlinks=False); refusing to write")


def _lexical_parts(directory: Path, root: Path) -> list[str]:
    """The requested destination's components below the root — LEXICALLY (see secure_fs)."""
    return _fs.lexical_parts(directory, root, error_cls=PostmortemError, noun="post-mortem")


#: The "component is not there yet" signal, shared with the anchored primitives.
_MissingComponent = _fs.MissingComponent


def _open_verified_dir(name: str, dir_fd: int | None = None) -> int:
    """Open ONE directory component and PROVE it is the thing we inspected (see secure_fs)."""
    return _fs.open_verified_dir(name, dir_fd, error_cls=PostmortemError,
                                 noun="post-mortem")


def _anchor_root(root: Path) -> int:
    """Open the trusted root and verify ITS identity too."""
    _require_platform()
    return _fs.anchor_root(root, error_cls=PostmortemError, noun="post-mortem")


def _anchor_destination(directory: Path, root: Path) -> int:
    """Walk from the trusted root to the destination on VERIFIED directory handles.

    The primitives live in ``packages/common/secure_fs.py`` — ONE implementation of the
    containment rules, shared with F011's stop-control area, so a hardening fix cannot land
    in one of them and miss the other.
    """
    _require_platform()
    return _fs.anchor_destination(directory, root, error_cls=PostmortemError,
                                  noun="post-mortem", dir_mode=0o700)


def _writable_by_mode_fd(dir_fd: int) -> bool:
    """Does the destination DECLARE itself writable to its owner? (``os.access`` lies to
    root; the declared mode bits do not.)"""
    return _fs.writable_by_mode_fd(dir_fd)


def _read_record_fd(dir_fd: int) -> dict[str, Any] | None:
    """Read an existing record THROUGH the destination fd — and prove what we opened.

    Same discipline as the directory walk, for the same reason: ``O_NOFOLLOW`` on the final
    name is not a guarantee on every host. The entry is stat'ed without following symlinks,
    must be a REGULAR file, is opened, and the opened descriptor's identity must match what
    was inspected. A symlinked ``postmortem.json`` is refused here, in our code — the record
    outside the evidence directory is never even read.
    """
    try:
        pre = os.stat(POSTMORTEM_FILENAME, dir_fd=dir_fd, follow_symlinks=False)
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise PostmortemConflictError(
            f"an existing post-mortem could not be inspected: "
            f"{type(exc).__name__}: {exc}") from exc

    if stat.S_ISLNK(pre.st_mode):
        raise PostmortemError(
            "refusing to read a symlinked post-mortem: the record must live in the "
            "evidence directory, not point out of it")
    if not stat.S_ISREG(pre.st_mode):
        raise PostmortemError("the existing post-mortem is not a regular file")

    try:
        fd = os.open(POSTMORTEM_FILENAME,
                     os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=dir_fd)
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise PostmortemConflictError(
            f"an existing post-mortem could not be read safely: "
            f"{type(exc).__name__}: {exc}") from exc

    try:
        post = os.fstat(fd)
        if (not stat.S_ISREG(post.st_mode)
                or (post.st_dev, post.st_ino) != (pre.st_dev, pre.st_ino)):
            raise PostmortemError(
                "the existing post-mortem is not the file it claimed to be "
                "(a symlink was followed, or it changed between the check and the open)")
        with os.fdopen(os.dup(fd), "r", encoding="utf-8") as fh:
            data = json.loads(fh.read())
    except ValueError as exc:
        raise PostmortemConflictError(
            f"an unreadable post-mortem already exists: {exc}") from exc
    finally:
        os.close(fd)
    return data if isinstance(data, dict) else {}


def write_postmortem(
    directory: str | Path,
    record: PostmortemV1,
    *,
    root: str | Path,
) -> Path:
    """Write one post-mortem into ``directory``. Contained, atomic, exactly once.

    ``root`` is the trusted containment root and is **mandatory**. It used to be optional,
    and the optional path did ``mkdir(parents=True)`` on an untrusted destination — so
    ``parent/link -> outside`` had ``outside/newdir/postmortem.json`` created in it before
    anything was checked. There is no safe way to infer a trusted root from the very path
    you are trying to validate, so the caller must name one. Every production call site
    already did.

    Containment is anchored to identity-verified directory handles
    (:func:`_open_verified_dir`): names are resolved once, against descriptors we hold, and
    what we opened must be the same inode we inspected. Publication is create-only
    (``os.link``), not ``os.replace`` — a concurrent DIFFERENT record conflicts instead of
    silently overwriting the only account of the first failure.
    """
    if root is None or str(root) == "":
        raise PostmortemError(
            "a post-mortem needs an explicit trusted evidence root; refusing to guess one "
            "from the destination path")

    payload = record.to_json()
    text = (json.dumps(payload, indent=2) + "\n").encode("utf-8")

    target_dir = Path(directory)
    dir_fd = _anchor_destination(target_dir, Path(root))
    tmp_name = f".{POSTMORTEM_FILENAME}.{os.getpid()}.{secrets.token_hex(8)}.tmp"
    tmp_created = False
    try:
        if not _writable_by_mode_fd(dir_fd):
            raise PostmortemError(
                f"post-mortem evidence directory is read-only "
                f"({oct(os.fstat(dir_fd).st_mode & 0o777)}): {target_dir.name}")

        existing = _read_record_fd(dir_fd)
        if existing is not None:
            return _settle(target_dir / POSTMORTEM_FILENAME, existing, payload)

        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        try:
            fd = os.open(tmp_name, flags, 0o600, dir_fd=dir_fd)
        except OSError as exc:
            raise PostmortemError(
                f"post-mortem could not be written in {target_dir.name}: "
                f"{type(exc).__name__}: {exc}") from exc
        tmp_created = True
        try:
            written = 0
            while written < len(text):
                try:
                    chunk = os.write(fd, text[written:])
                except OSError as exc:
                    raise PostmortemError(
                        f"post-mortem could not be written in {target_dir.name}: "
                        f"{type(exc).__name__}: {exc}") from exc
                if chunk <= 0:
                    # A write that writes nothing will never finish. Fail, do not spin.
                    raise PostmortemError(
                        f"post-mortem write made no progress at byte {written}")
                written += chunk
            os.fsync(fd)
        finally:
            os.close(fd)

        try:
            os.link(tmp_name, POSTMORTEM_FILENAME,
                    src_dir_fd=dir_fd, dst_dir_fd=dir_fd)   # create-only publication
        except FileExistsError:
            concurrent = _read_record_fd(dir_fd)
            if concurrent is None:
                raise PostmortemError(
                    "an unreadable post-mortem appeared during publication") from None
            return _settle(target_dir / POSTMORTEM_FILENAME, concurrent, payload)
        except OSError as exc:
            raise PostmortemError(
                f"post-mortem could not be published in {target_dir.name}: "
                f"{type(exc).__name__}: {exc}") from exc
    finally:
        if tmp_created:
            with contextlib.suppress(OSError):
                os.unlink(tmp_name, dir_fd=dir_fd)
        os.close(dir_fd)

    return target_dir / POSTMORTEM_FILENAME


def _existing_record(target: Path) -> dict[str, Any] | None:
    """The record already at ``target`` — or None when there is none."""
    if not target.exists():
        return None
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise PostmortemConflictError(
            f"an unreadable post-mortem already exists at {target}: {exc}") from exc
    return data if isinstance(data, dict) else {}


def _settle(target: Path, existing: dict[str, Any], payload: dict[str, Any]) -> Path:
    """Idempotent when it is the same failure; a conflict when it is a different one."""
    if _identity(existing) == _identity(payload):
        return target
    raise PostmortemConflictError(
        f"a different post-mortem already exists at {target} "
        f"({existing.get('failure_class')!r} vs {payload['failure_class']!r}); "
        f"refusing to overwrite the only record of that failure")


def call_evidence_dir(
    run_dir: str | Path,
    role: str,
    round_no: int,
    kind: str,
    provider_call_dir: str | Path = "",
) -> Path:
    """Where ONE logical provider call's post-mortem belongs.

    The provider's own per-call stream directory when it has one — that is the existing
    per-call evidence directory and F010 does not build a parallel hierarchy beside it.
    When the provider streams nothing (fake/manual providers, or stream evidence off) the
    normal supported call path still needs a stable directory, so it gets one under the
    run: ``calls/<role>/round-NN/<kind>``. Deterministic, so the same logical call always
    resolves to the same place — which is what makes exactly-once possible at all.
    """
    if provider_call_dir and Path(provider_call_dir).is_dir():
        return Path(provider_call_dir)
    return (Path(run_dir) / "calls" / (role or "unknown")
            / f"round-{max(1, int(round_no or 1)):02d}" / (kind or "attempt"))


def existing_evidence_refs(directory: str | Path, names: list[str] | None = None) -> tuple[str, ...]:
    """References to the artifacts that REALLY exist beside a post-mortem.

    A reference to a file that was never written is worse than no reference: it sends a
    reader looking for evidence that does not exist. So the directory is asked.
    """
    target = Path(directory)
    if not target.is_dir():
        return ()
    candidates = names or ["raw_stream.jsonl", "run_events.jsonl", "stderr.txt",
                           "result.json"]
    return tuple(sorted(n for n in candidates if (target / n).is_file()))


#: Where a task's call-level post-mortems are collected inside the evidence bundle, so the
#: rollup can reference them by a relative path that survives the trip to another machine.
CALL_POSTMORTEM_SUBDIR = "call_postmortems"


def collect_call_postmortems(run_dir: str | Path) -> list[Path]:
    """Every call-level post-mortem under ONE source directory, deterministically ordered.

    Kept for the run-directory layout; :func:`collect_task_call_postmortems` is the
    canonical collector that knows about BOTH source layouts.
    """
    root = Path(run_dir)
    if not root.is_dir():
        return []
    return sorted(root.rglob(POSTMORTEM_FILENAME))


def collect_task_call_postmortems(
    *, run_dir: str | Path | None = None, task_stream_dir: str | Path | None = None,
) -> list[tuple[str, Path]]:
    """THE collector: every call-level record belonging to one task, from both layouts.

    A provider call writes its post-mortem next to its own artifacts, and there are two
    legitimate places for those:

    * ``pingpong_runs/<run_id>/calls/...`` — the fallback per-call directory (no streaming);
    * ``jobs/<job>/evidence/task_runs/<task>/streams/<role>/round-NN/<kind>-II/`` — the
      streamed call directory, which is where a real streamed job actually puts them.

    The reviewed build only looked at the first, so a streamed failure's post-mortem never
    reached the bundle and the rollup pointed at nothing. Both are collected here, ONCE
    each, keyed by a stable relative layout that becomes the canonical exported path.

    Returns ``[(relative_layout, source_path)]``, sorted, with no duplicate key.
    """
    found: dict[str, Path] = {}

    for label, base in (("runs", run_dir), ("streams", task_stream_dir)):
        if not base:
            continue
        root = Path(base)
        if not root.is_dir():
            continue
        for src in sorted(root.rglob(POSTMORTEM_FILENAME)):
            if src.is_symlink():
                continue
            rel_dir = src.parent.relative_to(root).as_posix()
            key = f"{label}/{rel_dir}" if rel_dir and rel_dir != "." else label
            if key in found and found[key] != src:
                raise PostmortemConflictError(
                    f"two different call post-mortems claim the same layout {key!r}")
            found[key] = src

    return sorted(found.items())


def build_job_rollup(
    *,
    job_id: str,
    signals: FailureSignals,
    task_refs: tuple[str, ...] = (),
) -> PostmortemV1:
    """A JOB-level record: the job failed before any task could own the failure.

    A worktree lock that stops `_acquire_job_workspace()` is not a task failure — no task
    ever ran — and blaming a pending task for it would be a lie in the histogram. It gets
    its own scope, and the typed exception reaches the classifier intact.
    """
    verdict = classify(signals)
    return PostmortemV1(
        failure_class=verdict.failure_class,
        signal_source=verdict.signal_source,
        scope=SCOPE_JOB,
        job_id=job_id,
        terminal_status=signals.terminal_status,
        raw_reason=signals.error_text or verdict.reason,
        evidence_refs=task_refs,
    )


def task_failure_signals(task: Any) -> FailureSignals:
    """Read the terminal signals off a finished task, without interpreting them.

    Interpretation is :func:`classify`'s job — this only says what the task layer actually
    recorded. A task that ran no provider at all still produces usable signals.
    """
    final_status = str(getattr(task, "final_status", "") or "")
    error = str(getattr(task, "error", "") or "")
    test_passed = getattr(task, "test_passed", None)

    terminal = final_status
    if not terminal and test_passed is False:
        terminal = "test_failed"

    return FailureSignals(
        terminal_status=terminal,
        error_text=error,
        reviewer_verdict=str(getattr(task, "reviewer_verdict", "") or ""),
    )


def build_task_rollup(
    task: Any,
    *,
    job_id: str,
    call_refs: tuple[str, ...] = (),
    signals: FailureSignals | None = None,
) -> PostmortemV1:
    """The task-level rollup: ONE record for a task that ended terminally failed.

    It does not re-litigate the call-level records — it points at them. Aggregation later
    counts a call and a task as different scopes precisely so that one failure is not
    counted twice under two names.
    """
    resolved = signals if signals is not None else task_failure_signals(task)
    verdict = classify(resolved)
    return PostmortemV1(
        failure_class=verdict.failure_class,
        signal_source=verdict.signal_source,
        scope="task",
        job_id=job_id,
        task_id=str(getattr(task, "task_id", "") or ""),
        run_id=str(getattr(task, "run_id", "") or ""),
        terminal_status=resolved.terminal_status,
        raw_reason=resolved.error_text or verdict.reason,
        evidence_refs=call_refs,
    )


def read_postmortem(path: str | Path) -> dict[str, Any]:
    """Read one record. Raises ``ValueError`` on malformed JSON or an unknown version."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("post-mortem is not a JSON object")
    version = data.get("postmortem_v")
    if version != POSTMORTEM_VERSION:
        raise ValueError(f"unsupported postmortem_v {version!r}")
    return data
