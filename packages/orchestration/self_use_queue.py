"""F257 — the self-use queue: the curated maintenance jobs Remedy runs on itself.

"Remedy is used on Remedy" rots the moment it depends on someone remembering to
do it.  This module is the read side of the mechanism that stops that: a
shipped, operator-curated data file (``scripts/self_use_queue.json``) holding
small maintenance jobs, exactly one of which is consumed per feature close.

Each item carries the LITERAL text of a job file in the format
:func:`packages.orchestration.pingpong_job.parse_job_file` already accepts, so
the queue never grows a second task format that has to be kept in step with the
first (DECISION F257 D2).  The file lives in ``scripts/`` beside the other
shipped campaign data, resolved the same way
:func:`packages.orchestration.gauntlet_orders.default_orders_dir` resolves its
directory: it is shipped INPUT an operator is meant to edit, not test data.

Public API::

    SELF_USE_QUEUE_SCHEMA_VERSION: the schema_version this loader accepts
    SELF_USE_QUEUE_FILENAME: the file name shipped under scripts/
    SelfUseQueueError: the queue is missing or malformed
    SelfUseQueueEntry: one curated item and the feature that consumed it
    default_self_use_queue_path(repo_root=None) -> Path
    load_self_use_queue(path=None) -> tuple[SelfUseQueueEntry, ...]
    pending_self_use_items(path=None) -> tuple[SelfUseQueueEntry, ...]
    next_self_use_item(path=None) -> SelfUseQueueEntry | None

Deliberate absences:
  * REMEDY DELIBERATELY DOES NOT LET A JOB MARK ITS OWN QUEUE ITEM CONSUMED.
    This module is read-only and owns no writer: it opens the queue file for
    reading and exports no function that sets ``consumed_by``.  The reason is
    the one that puts ``docs/roadmap/STATUS.md`` in
    ``packages.orchestration.scope_fences.BUILTIN_DENY`` — a run that can check
    itself off is not a gate, and this queue is a ledger of the same kind.
    Consumption is an edit the CLOSURE ROUND makes, which DECISION F257 D2
    rules.
  * Remedy deliberately does not fall back to an empty tuple when the queue
    cannot be read.  "The queue is empty" and "I could not read the queue" are
    opposite answers and must never look alike: the first means the track is
    exhausted and a human must curate more, the second means something is
    broken.  Every failure raises :class:`SelfUseQueueError`; only
    :func:`next_self_use_item` answers ``None``, and only for exhaustion.
  * Remedy deliberately does not discover, generate or infer queue items.  The
    list is operator-curated DATA — curation is where this feature's risk sits,
    not in code — so the queue is exactly as useful as the human who wrote it.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

#: The one schema version this loader accepts.  A file from the future is
#: refused rather than half-read: a field this code does not understand is
#: exactly the field that would have said "this item is already consumed".
SELF_USE_QUEUE_SCHEMA_VERSION = 2

#: The file name shipped under ``scripts/``.  One spelling, so nothing loads a
#: copy of the queue.
SELF_USE_QUEUE_FILENAME = "self_use_queue.json"

#: The shape of a queue item id.  Pinned so ids sort in curation order and a
#: typo is refused at load time rather than silently becoming a new item.
_ITEM_ID_RE = re.compile(r"^SU-\d{3}$")

#: The six keys an item carries — no more, no fewer.  An unexpected key is a
#: curation mistake or a format drift, and either way it is refused.  Schema v2
#: (F258) added ``provenance``; every v1 item was migrated to carry one.
_ITEM_KEYS: tuple[str, ...] = ("id", "title", "why", "job_markdown", "consumed_by", "provenance")


class SelfUseQueueError(RuntimeError):
    """The self-use queue is missing, unreadable, or malformed.

    Raised rather than degraded to an empty queue: a track that silently
    reports "nothing left to do" because it could not open its data file would
    retire itself through an I/O failure, which is the exact failure the queue
    exists to prevent.
    """


@dataclass(frozen=True)
class SelfUseQueueEntry:
    """One curated self-use item, as written in the shipped file."""

    id: str
    title: str
    why: str
    job_markdown: str
    consumed_by: str
    provenance: str

    @property
    def is_pending(self) -> bool:
        """True while no feature has consumed this item."""
        return not self.consumed_by.strip()


def default_self_use_queue_path(repo_root: Path | None = None) -> Path:
    """Where the shipped queue lives — resolved like the gauntlet order set."""
    root = repo_root or Path(__file__).resolve().parents[2]
    return root / "scripts" / SELF_USE_QUEUE_FILENAME


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SelfUseQueueError(message)


def load_self_use_queue(path: Path | None = None) -> tuple[SelfUseQueueEntry, ...]:
    """Read and validate the self-use queue. Never half-loads, never guesses.

    Every failure message names the path, because the first question a reader
    has when this raises is "which file did it try to read?" — and the answer
    is not obvious once an operator has pointed the loader elsewhere.

    Raises:
        SelfUseQueueError: the file is missing or unreadable, is not a JSON
            object, carries an unsupported ``schema_version``, holds an
            ``items`` value that is not a list, holds an item that is not an
            object or whose keys are not exactly the six this module names,
            holds a non-string or blank field where a string is required,
            holds an ``id`` that does not match ``^SU-\\d{3}$``, or holds a
            duplicate ``id``.
    """
    queue_path = path or default_self_use_queue_path()
    try:
        body = json.loads(queue_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SelfUseQueueError(f"{queue_path}: unreadable ({exc})") from exc

    _require(isinstance(body, dict), f"{queue_path}: not a JSON object")

    version = body.get("schema_version")
    _require(version == SELF_USE_QUEUE_SCHEMA_VERSION,
             f"{queue_path}: unsupported schema_version {version!r} "
             f"(this Remedy reads {SELF_USE_QUEUE_SCHEMA_VERSION})")

    _require(isinstance(body.get("description"), str),
             f"{queue_path}: description must be a string")

    raw_items = body.get("items")
    _require(isinstance(raw_items, list), f"{queue_path}: items must be a list")

    entries: list[SelfUseQueueEntry] = []
    for position, raw in enumerate(raw_items, 1):
        _require(isinstance(raw, dict),
                 f"{queue_path}: items[{position}] is not an object")
        _require(tuple(sorted(raw)) == tuple(sorted(_ITEM_KEYS)),
                 f"{queue_path}: items[{position}] must carry exactly the keys "
                 f"{sorted(_ITEM_KEYS)}, found {sorted(raw)}")
        for field_name in ("id", "title", "why", "job_markdown", "provenance"):
            value = raw.get(field_name)
            _require(isinstance(value, str) and value.strip(),
                     f"{queue_path}: items[{position}] has a missing or blank "
                     f"{field_name}")
        consumed_by = raw.get("consumed_by")
        _require(isinstance(consumed_by, str),
                 f"{queue_path}: items[{position}].consumed_by must be a string "
                 f"(empty while the item is pending)")
        item_id = raw["id"]
        _require(bool(_ITEM_ID_RE.match(item_id)),
                 f"{queue_path}: items[{position}] id {item_id!r} does not match "
                 f"{_ITEM_ID_RE.pattern}")
        entries.append(SelfUseQueueEntry(
            id=item_id,
            title=raw["title"],
            why=raw["why"],
            job_markdown=raw["job_markdown"],
            consumed_by=consumed_by,
            provenance=raw["provenance"],
        ))

    ids = [entry.id for entry in entries]
    _require(len(set(ids)) == len(ids),
             f"{queue_path}: duplicate self-use item ids: {sorted(ids)}")
    return tuple(entries)


def pending_self_use_items(path: Path | None = None) -> tuple[SelfUseQueueEntry, ...]:
    """The items no feature has consumed yet, in file order — the curation order."""
    return tuple(entry for entry in load_self_use_queue(path) if entry.is_pending)


def next_self_use_item(path: Path | None = None) -> SelfUseQueueEntry | None:
    """The FIRST pending item in file order, or ``None`` when all are consumed.

    ``None`` means one thing only: the track is exhausted and a human must
    curate more items.  It never stands for an error, because every failure
    :func:`load_self_use_queue` can meet raises instead.
    """
    pending = pending_self_use_items(path)
    return pending[0] if pending else None
