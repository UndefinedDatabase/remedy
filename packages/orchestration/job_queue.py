"""F048 — the per-project job queue (v1, file-based).

Work is queued per project and consumed unattended: an entry is enqueued, a consumer
claims exactly one atomically, and the state survives a killed consumer because it only
ever lives on disk.

**v1 is deliberately FILE-BASED.** In STATUS order this feature lands BEFORE the SQLite
token ledger (F103) introduces that dependency, and the codebase today persists every
entity as an atomic per-entity JSON file (``storage.save_job``, ``project_registry``,
``proposed_tasks``). So the queue matches what exists. If a later scheduler feature
outgrows this, migrating to the then-existing SQLite is THAT feature's decision, not a
debt this module pretends to have paid.

Layout, under the resolved data root::

    <data_root>/queue/<project_id>/<entry_id>.json      the entry record
    <data_root>/queue/<project_id>/<entry_id>.claim     the claim marker

**The claim marker is the mutex, and it is the one the codebase already trusts.** It is
published with ``secure_fs.write_file_atomically(..., create_only=True)`` — the same
create-only ``os.link`` publication F011's stop request uses
(``safe_points.request_stop``): the loser's link fails with ``FileExistsError`` and the
helper returns ``False``, so two consumers can never both hold one entry. Every read and
write goes through identity-verified directory descriptors, so a symlinked ``queue``,
project or entry is refused rather than followed.

Claims are never taken over silently: a consumer that dies leaves its entry visible as
``claimed`` with its owner on it, and re-offering it is an explicit operator command
(T003), not a timeout applied behind the operator's back. Listing stays honest under
corruption — an entry file that will not parse is skipped and COUNTED, exactly as
``storage.list_jobs_safe`` does for jobs.
"""
from __future__ import annotations

import json
import os
import re
import socket
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.common import secure_fs as _fs
from packages.orchestration.data_paths import queue_dir as _queue_dir

#: The queue is this user's private business — same posture as the F011 control area.
QUEUE_DIR_MODE = 0o700
QUEUE_FILE_MODE = 0o600

QUEUE_DIRNAME = "queue"
ENTRY_SUFFIX = ".json"
CLAIM_SUFFIX = ".claim"

QUEUE_ENTRY_VERSION = 1

#: Bounds. A queue record is operator input: it is small, or it is not a queue record.
MAX_GOAL_CHARS = 8_000
MAX_GOAL_PATH_CHARS = 4_096
MAX_CONSUMER_CHARS = 200
MAX_REASON_CHARS = 500
MAX_ENTRY_BYTES = 256 * 1024

STATUS_QUEUED = "queued"
STATUS_CLAIMED = "claimed"
STATUS_DONE = "done"
STATUS_FAILED = "failed"
VALID_STATUSES = (STATUS_QUEUED, STATUS_CLAIMED, STATUS_DONE, STATUS_FAILED)

#: Anything that becomes a path component: the F011 shape, unchanged.
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")


class QueueError(RuntimeError):
    """The queue area could not be used. Loud on purpose: a queue that silently does
    nothing looks exactly like an empty one."""


class QueueEntryNotFoundError(QueueError):
    """The requested entry is not in this project's queue."""


class QueueEntryClaimedError(QueueError):
    """The entry is held by a consumer. Carries the entry so the caller can name the owner
    instead of refusing anonymously."""

    def __init__(self, message: str, *, entry: QueueEntry) -> None:
        super().__init__(message)
        self.entry = entry


# ---------------------------------------------------------------------------
# Validation and small helpers
# ---------------------------------------------------------------------------


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_project_id(project_id: Any) -> str:
    text = str(project_id or "").strip()
    if not _ID_RE.match(text):
        raise QueueError(
            f"invalid project id {project_id!r}: a project id is 1-64 characters of "
            f"letters, digits, '-' or '_'")
    return text


def validate_entry_id(entry_id: Any) -> str:
    text = str(entry_id or "").strip()
    if not _ID_RE.match(text):
        raise QueueError(
            f"invalid queue entry id {entry_id!r}: an entry id is 1-64 characters of "
            f"letters, digits, '-' or '_'")
    return text


def new_entry_id() -> str:
    """Unique per ENTRY. Duplicate goal text is allowed, so identity cannot be the goal."""
    return uuid.uuid4().hex


def consumer_id() -> str:
    """This consumer, as the feature spells it: host + pid."""
    try:
        host = socket.gethostname() or "unknown-host"
    except OSError:
        host = "unknown-host"
    return _bounded(f"{host}#{os.getpid()}", MAX_CONSUMER_CHARS, "unknown-consumer")


def _bounded(text: Any, limit: int, fallback: str) -> str:
    """Bounded, single-line. Goal text is NOT redacted — it is the work item itself, and a
    redacted goal is a different goal. Only its size and line shape are ours to bound."""
    cleaned = str(text if text is not None else "").replace("\r", " ").strip()
    if not cleaned:
        return fallback
    return cleaned[:limit]


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------


@dataclass
class QueueEntry:
    """One queued unit of work. The file on disk is the truth; this is a read of it."""

    id: str
    project_id: str
    goal: str = ""
    goal_path: str = ""
    priority: int = 0
    created_at: str = ""
    status: str = STATUS_QUEUED
    claimed_by: str = ""
    claimed_at: str = ""
    result_job_id: str = ""
    failure_reason: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "queue_entry_v": QUEUE_ENTRY_VERSION,
            "id": self.id,
            "project_id": self.project_id,
            "goal": self.goal,
            "goal_path": self.goal_path,
            "priority": self.priority,
            "created_at": self.created_at,
            "status": self.status,
            "claimed_by": self.claimed_by,
            "claimed_at": self.claimed_at,
            "result_job_id": self.result_job_id,
            "failure_reason": self.failure_reason,
        }

    @property
    def sort_key(self) -> tuple[int, str, str]:
        """Higher priority first, FIFO within a priority (A9). ``created_at`` is an
        ISO-8601 UTC string, which sorts lexicographically iff it sorts chronologically;
        ``id`` is the tie-break for two entries enqueued in the same microsecond."""
        return (-self.priority, self.created_at, self.id)


def _parse_entry(raw: bytes) -> QueueEntry | None:
    """Bytes to entry, or None for anything this version cannot trust — an id that would
    not survive being a path component, an unknown record version, a non-integer
    priority. Unreadable rather than dangerous; the caller counts it as skipped."""
    try:
        data = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None
    if not isinstance(data, dict) or data.get("queue_entry_v") != QUEUE_ENTRY_VERSION:
        return None

    entry_id = data.get("id")
    project_id = data.get("project_id")
    if not _is_safe_id(entry_id) or not _is_safe_id(project_id):
        return None

    priority = data.get("priority", 0)
    if isinstance(priority, bool) or not isinstance(priority, int):
        return None

    status = data.get("status")
    if status not in VALID_STATUSES:
        return None

    return QueueEntry(
        id=entry_id,
        project_id=project_id,
        goal=_bounded(data.get("goal"), MAX_GOAL_CHARS, ""),
        goal_path=_bounded(data.get("goal_path"), MAX_GOAL_PATH_CHARS, ""),
        priority=priority,
        created_at=_bounded(data.get("created_at"), 64, ""),
        status=status,
        claimed_by=_bounded(data.get("claimed_by"), MAX_CONSUMER_CHARS, ""),
        claimed_at=_bounded(data.get("claimed_at"), 64, ""),
        result_job_id=_bounded(data.get("result_job_id"), 64, ""),
        failure_reason=_bounded(data.get("failure_reason"), MAX_REASON_CHARS, ""),
    )


def _is_safe_id(value: Any) -> bool:
    """An id is a filename. ``../../../../escaped`` is not one."""
    return isinstance(value, str) and bool(_ID_RE.match(value))


# ---------------------------------------------------------------------------
# The queue area
# ---------------------------------------------------------------------------


def queue_root(root: Path | None = None) -> Path:
    """The queue area (``<data_root>/queue``), resolved by ``data_paths`` like every other
    storage area — promoted there in T003 now that the CLI resolves it too."""
    # Coerced to Path here: the public API accepts a str root (a CLI flag, a test tmpdir),
    # while data_paths' helpers, like every other storage area, do Path arithmetic.
    return Path(os.path.normpath(str(_queue_dir(Path(root) if root is not None else None))))


def project_queue_dir(project_id: str, root: Path | None = None) -> Path:
    """This project's queue area. Cross-project queues are out of scope by construction:
    a consumer only ever holds a descriptor to one project's directory."""
    return queue_root(root) / validate_project_id(project_id)


def _open_project_fd(project_id: str, root: Path | None, *, create: bool) -> int | None:
    """A verified directory fd for ``queue/<project_id>``; None when it does not exist.
    Every component — data root, ``queue``, the project directory — is inspected without
    following symlinks, opened relative to the handle above it, and identity-checked."""
    pid = validate_project_id(project_id)
    base = queue_root(root)

    if create:
        os.close(_fs.anchor_root(base, error_cls=QueueError, noun="queue",
                                 create=True, dir_mode=QUEUE_DIR_MODE))
    else:
        try:
            os.close(_fs.anchor_root(base, error_cls=QueueError, noun="queue"))
        except QueueError as exc:
            if "does not exist" in str(exc):
                return None
            raise

    try:
        return _fs.anchor_destination(
            base / pid, base, error_cls=QueueError, noun="queue",
            create=create, dir_mode=QUEUE_DIR_MODE)
    except _fs.MissingComponent:
        return None


def _write_entry(project_fd: int, entry: QueueEntry, *, create_only: bool) -> bool:
    return _fs.write_file_atomically(
        project_fd, f"{entry.id}{ENTRY_SUFFIX}", _fs.json_bytes(entry.to_json()),
        create_only=create_only, file_mode=QUEUE_FILE_MODE,
        error_cls=QueueError, noun="queue entry")


def _read_entry(project_fd: int, entry_id: str) -> QueueEntry | None:
    raw = _fs.read_verified_file(
        f"{entry_id}{ENTRY_SUFFIX}", project_fd, max_bytes=MAX_ENTRY_BYTES,
        error_cls=QueueError, noun="queue entry")
    if raw is None:
        return None
    return _parse_entry(raw)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def enqueue(project: str, goal: str = "", prio: int = 0, *,
            goal_path: str = "", root: Path | None = None) -> QueueEntry:
    """Add one entry to *project*'s queue and return it. Exactly one of *goal* (the text)
    or *goal_path* (a reference to a goal file) is required. Duplicate goal text is
    allowed and makes a SECOND entry: dedup is a human judgment, not the queue's (A9)."""
    pid = validate_project_id(project)
    goal_text = _bounded(goal, MAX_GOAL_CHARS, "")
    path_text = _bounded(goal_path, MAX_GOAL_PATH_CHARS, "")
    if bool(goal_text) == bool(path_text):
        raise QueueError(
            "a queue entry carries either goal text or a goal-file path — "
            "exactly one, never both and never neither")
    if isinstance(prio, bool) or not isinstance(prio, int):
        raise QueueError(f"invalid priority {prio!r}: a priority is an integer")

    entry = QueueEntry(
        id=new_entry_id(),
        project_id=pid,
        goal=goal_text,
        goal_path=path_text,
        priority=prio,
        created_at=utc_now_iso(),
        status=STATUS_QUEUED,
    )
    project_fd = _open_project_fd(pid, root, create=True)
    assert project_fd is not None            # create=True either makes it or raises
    try:
        if not _write_entry(project_fd, entry, create_only=True):
            raise QueueError(f"queue entry id collision: {entry.id}")
    finally:
        os.close(project_fd)
    return entry


def list_entries_safe(project: str, root: Path | None = None,
                      ) -> tuple[list[QueueEntry], bool, list[str]]:
    """List a project's queue with corruption visible: ``(entries, degraded,
    skipped_files)`` — the same honesty shape ``storage.list_jobs_safe`` uses for jobs. A
    file that will not parse is skipped and COUNTED; the queue stays listable always."""
    project_fd = _open_project_fd(project, root, create=False)
    if project_fd is None:
        return ([], False, [])
    entries: list[QueueEntry] = []
    skipped: list[str] = []
    try:
        for name in _fs.list_dir_names(project_fd, error_cls=QueueError, noun="queue"):
            if not name.endswith(ENTRY_SUFFIX):
                continue
            try:
                raw = _fs.read_verified_file(name, project_fd, max_bytes=MAX_ENTRY_BYTES,
                                             error_cls=QueueError, noun="queue entry")
            except QueueError:
                skipped.append(name)
                continue
            if raw is None:
                continue                     # removed between listing and reading
            entry = _parse_entry(raw)
            if entry is None or f"{entry.id}{ENTRY_SUFFIX}" != name:
                skipped.append(name)
                continue
            entries.append(entry)
    finally:
        os.close(project_fd)
    entries.sort(key=lambda e: e.sort_key)
    return (entries, len(skipped) > 0, skipped)


def list_entries(project: str, root: Path | None = None) -> list[QueueEntry]:
    """The project's entries in claim order. Corrupt files are skipped silently — use
    :func:`list_entries_safe` to see how many."""
    entries, _, _ = list_entries_safe(project, root)
    return entries


def load_entry(project: str, entry_id: str, root: Path | None = None) -> QueueEntry:
    """Re-read one entry FROM DISK. This is what makes a claim survive a restart: no
    consumer state is held in memory across calls."""
    eid = validate_entry_id(entry_id)
    project_fd = _open_project_fd(project, root, create=False)
    if project_fd is None:
        raise QueueEntryNotFoundError(f"no queue for project {project!r}")
    try:
        entry = _read_entry(project_fd, eid)
    finally:
        os.close(project_fd)
    if entry is None:
        raise QueueEntryNotFoundError(f"queue entry not found or unreadable: {eid}")
    return entry


def claim_next(project: str, consumer: str | None = None,
               root: Path | None = None) -> QueueEntry | None:
    """Claim the next entry for *consumer*, or None when nothing is claimable. Order:
    higher priority value first, FIFO by ``created_at`` within equal priority (A9).

    The claim is one create-only publication of ``<entry-id>.claim``. Losing that race is
    not an error and not a retry: someone else owns the entry, so we move on. Because the
    marker is created BEFORE the record is rewritten, an entry whose file still reads
    ``queued`` but whose marker exists is already spoken for."""
    who = consumer if consumer is not None else consumer_id()
    who = _bounded(who, MAX_CONSUMER_CHARS, "unknown-consumer")

    project_fd = _open_project_fd(project, root, create=False)
    if project_fd is None:
        return None
    try:
        candidates, _, _ = list_entries_safe(project, root)
        for candidate in candidates:
            if candidate.status != STATUS_QUEUED:
                continue
            claim_name = f"{candidate.id}{CLAIM_SUFFIX}"
            claim_body = _fs.json_bytes({
                "queue_entry_v": QUEUE_ENTRY_VERSION,
                "entry_id": candidate.id,
                "claimed_by": who,
                "claimed_at": utc_now_iso(),
            })
            won = _fs.write_file_atomically(
                project_fd, claim_name, claim_body, create_only=True,
                file_mode=QUEUE_FILE_MODE, error_cls=QueueError, noun="queue claim")
            if not won:
                continue                     # another consumer got there first

            # We hold the marker. Re-read from disk before writing: the file is the truth,
            # and it may have moved on since the listing that suggested it.
            fresh = _read_entry(project_fd, candidate.id)
            if fresh is None or fresh.status != STATUS_QUEUED:
                _fs.unlink_at(claim_name, project_fd, error_cls=QueueError,
                              noun="queue claim")
                continue

            fresh.status = STATUS_CLAIMED
            fresh.claimed_by = who
            fresh.claimed_at = utc_now_iso()
            _write_entry(project_fd, fresh, create_only=False)
            return fresh
        return None
    finally:
        os.close(project_fd)


def release(entry: QueueEntry, root: Path | None = None) -> QueueEntry:
    """Give a claimed entry back to the queue: status ``queued``, owner cleared, marker
    removed. The entry becomes claimable again by anyone, including us."""
    return _transition(entry, root, status=STATUS_QUEUED, drop_claim=True,
                       claimed_by="", claimed_at="")


def complete(entry: QueueEntry, job_id: str, root: Path | None = None) -> QueueEntry:
    """Mark a claimed entry ``done`` and record the job it became."""
    return _transition(entry, root, status=STATUS_DONE, drop_claim=True,
                       result_job_id=_bounded(job_id, 64, ""))


def fail(entry: QueueEntry, reason: str, root: Path | None = None) -> QueueEntry:
    """Mark a claimed entry ``failed`` and record why."""
    return _transition(entry, root, status=STATUS_FAILED, drop_claim=True,
                       failure_reason=_bounded(reason, MAX_REASON_CHARS, "unknown"))


def _transition(entry: QueueEntry, root: Path | None, *, status: str,
                drop_claim: bool, **fields: Any) -> QueueEntry:
    """Re-read, transition, write, and only then drop the marker. The re-read is the
    point: the caller's ``QueueEntry`` is a snapshot that may be older than the file, and
    a transition written from a stale one would silently undo what happened in between."""
    eid = validate_entry_id(entry.id)
    project_fd = _open_project_fd(entry.project_id, root, create=False)
    if project_fd is None:
        raise QueueEntryNotFoundError(f"no queue for project {entry.project_id!r}")
    try:
        fresh = _read_entry(project_fd, eid)
        if fresh is None:
            raise QueueEntryNotFoundError(
                f"queue entry not found or unreadable: {eid}")
        if fresh.status != STATUS_CLAIMED:
            raise QueueError(
                f"queue entry {eid} is {fresh.status}, not {STATUS_CLAIMED}: "
                f"only a claimed entry can be released, completed or failed")
        fresh.status = status
        for name, value in fields.items():
            setattr(fresh, name, value)
        _write_entry(project_fd, fresh, create_only=False)
        if drop_claim:
            _fs.unlink_at(f"{eid}{CLAIM_SUFFIX}", project_fd, error_cls=QueueError,
                          noun="queue claim")
    finally:
        os.close(project_fd)
    return fresh


def remove_entry(project: str, entry_id: str, root: Path | None = None) -> QueueEntry:
    """Remove an entry from the queue and return what was removed.

    A CLAIMED entry is never removed: a consumer is holding it, and deleting the record
    under a running consumer would turn its completion into a write to nothing. The caller
    gets the owner in the error so it can say who.
    """
    eid = validate_entry_id(entry_id)
    project_fd = _open_project_fd(project, root, create=False)
    if project_fd is None:
        raise QueueEntryNotFoundError(f"no queue for project {project!r}")
    try:
        entry = _read_entry(project_fd, eid)
        if entry is None:
            raise QueueEntryNotFoundError(f"queue entry not found or unreadable: {eid}")
        if entry.status == STATUS_CLAIMED:
            raise QueueEntryClaimedError(
                f"queue entry {eid} is claimed by {entry.claimed_by or 'an unknown consumer'}",
                entry=entry)
        _fs.unlink_at(f"{eid}{ENTRY_SUFFIX}", project_fd, error_cls=QueueError,
                      noun="queue entry")
        _fs.unlink_at(f"{eid}{CLAIM_SUFFIX}", project_fd, error_cls=QueueError,
                      noun="queue claim")
    finally:
        os.close(project_fd)
    return entry


def claim_holder(project: str, entry_id: str, root: Path | None = None) -> str:
    """Who holds the claim marker for this entry, as read from disk. Empty when there is
    no marker. Stale claims stay VISIBLE — nothing here takes one over."""
    eid = validate_entry_id(entry_id)
    project_fd = _open_project_fd(project, root, create=False)
    if project_fd is None:
        return ""
    try:
        raw = _fs.read_verified_file(f"{eid}{CLAIM_SUFFIX}", project_fd,
                                     max_bytes=MAX_ENTRY_BYTES,
                                     error_cls=QueueError, noun="queue claim")
    finally:
        os.close(project_fd)
    if raw is None:
        return ""
    try:
        data = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return ""
    if not isinstance(data, dict):
        return ""
    return _bounded(data.get("claimed_by"), MAX_CONSUMER_CHARS, "")
