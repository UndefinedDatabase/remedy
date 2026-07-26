"""Checkpoint writer and loader for kill-proof runs (F047 T001).

A hard-killed run should lose nothing but the in-flight task.  After every
cycle the conductor writes ``checkpoint_<n>.json`` under the job's OWN
evidence area — the same area F046's cycle records live in, one directory
over::

    <data root>/jobs/<job id>/evidence/cycles/cycle_0001.json      (F046)
    <data root>/jobs/<job id>/evidence/checkpoints/checkpoint_0001.json

What a checkpoint is, and what it deliberately is not:

* It is a POINTER, not a copy.  The persisted job already IS checkpoint v1
  (the kill switch established that); a checkpoint references that snapshot
  by path and digest and adds what the job file alone cannot answer — which
  worktree head the run stood on, what it had spent, what it verified, and
  which task/cycle would have run next.
* It is self-verifying.  ``content_hash`` is a SHA-256 over the canonical
  encoding of the record body, so a torn or edited file is detectable
  without a second source of truth.
* It is never load-bearing for the run itself.  A checkpoint write that
  fails is logged loudly and the run continues (feature-file A9 default);
  the next cycle simply writes the next one.

Reuse (A6): the atomic write is ``storage._atomic_write_job`` — temp file,
fsync, ``os.replace`` — the same helper behind ``save_job``.  This module
introduces NO second atomic writer.  (F046's ``write_cycle_record`` uses a
plain ``write_text``; checkpoints deliberately do not copy that, because a
half-written checkpoint is exactly the failure mode this feature exists to
survive.)

Corruption policy:

* ``load_latest_valid`` walks checkpoints newest-first and returns the first
  whose hash verifies.  Every skipped file is logged as a warning and LEFT
  ON DISK for forensics — a corrupted checkpoint is evidence, not litter.
* No checkpoints at all -> ``None``.  The caller degrades honestly to plain
  continuation from the persisted job state.
* Checkpoints exist but none verifies -> ``AllCheckpointsCorruptError``.
  That is a different, louder situation than "never checkpointed", and the
  resume path must not blur the two.
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.orchestration.storage import _atomic_write_job as _atomic_write

_log = logging.getLogger("remedy.checkpoints")

#: Bumped whenever the record body changes shape.  A reader that meets a
#: version it does not know refuses that record rather than guessing.
SCHEMA_VERSION = 1

#: Where checkpoints live inside the job's evidence area, and how they are named.
CHECKPOINT_DIRNAME = "checkpoints"
CHECKPOINT_FILENAME = "checkpoint_{index:04d}.json"
_CHECKPOINT_GLOB = "checkpoint_*.json"

#: Config key owned by this feature, and its small default.
CONFIG_KEY_RETENTION = "cycles.checkpoint_retention"
DEFAULT_RETENTION = 5

#: The two intent kinds a checkpoint can express about what comes next.
INTENT_CYCLE = "cycle"          # another cycle would run
INTENT_NONE = "none"            # nothing left to run


class CheckpointError(Exception):
    """A checkpoint operation failed in a way the caller must handle."""


class AllCheckpointsCorruptError(CheckpointError):
    """Checkpoints exist for this job, but not one of them verifies."""

    def __init__(self, job_id: str, paths: list[str]) -> None:
        super().__init__(
            f"all {len(paths)} checkpoint(s) for job {job_id} failed hash "
            f"verification: {', '.join(paths)}"
        )
        self.job_id = job_id
        self.paths = paths


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Checkpoint:
    """One cycle boundary, captured.

    ``job_snapshot_path`` is data-root-relative on purpose: an absolute
    private path must never end up in a record that can be shared.
    ``job_snapshot_sha256`` is empty when the snapshot could not be read —
    an unmeasured digest is reported as unmeasured, never as a match.
    """

    cycle_index: int
    job_id: str
    job_snapshot_path: str = ""
    job_snapshot_sha256: str = ""
    worktree_head: str = ""
    budget_spent_tokens: int = 0
    verify_result: str = ""
    verify_digest: str = ""
    next_intent: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    schema_version: int = SCHEMA_VERSION

    def to_body(self) -> dict[str, Any]:
        """The hashed part of the file — everything except the hash itself."""
        return {
            "schema_version": self.schema_version,
            "job_id": self.job_id,
            "cycle_index": self.cycle_index,
            "job_snapshot_path": self.job_snapshot_path,
            "job_snapshot_sha256": self.job_snapshot_sha256,
            "worktree_head": self.worktree_head,
            "budget_spent_tokens": self.budget_spent_tokens,
            "verify_result": self.verify_result,
            "verify_digest": self.verify_digest,
            "next_intent": dict(self.next_intent),
            "created_at": self.created_at,
        }

    @property
    def content_hash(self) -> str:
        return compute_content_hash(self.to_body())

    def to_json(self) -> dict[str, Any]:
        body = self.to_body()
        return {"record": body, "content_hash": compute_content_hash(body)}

    @classmethod
    def from_body(cls, body: dict[str, Any]) -> Checkpoint:
        return cls(
            cycle_index=int(body["cycle_index"]),
            job_id=str(body["job_id"]),
            job_snapshot_path=str(body.get("job_snapshot_path", "")),
            job_snapshot_sha256=str(body.get("job_snapshot_sha256", "")),
            worktree_head=str(body.get("worktree_head", "")),
            budget_spent_tokens=int(body.get("budget_spent_tokens", 0)),
            verify_result=str(body.get("verify_result", "")),
            verify_digest=str(body.get("verify_digest", "")),
            next_intent=dict(body.get("next_intent") or {}),
            created_at=str(body.get("created_at", "")),
            schema_version=int(body.get("schema_version", 0)),
        )


def _canonical(body: dict[str, Any]) -> bytes:
    """The exact bytes the hash covers.  Sorted keys, no incidental spacing."""
    return json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")


def compute_content_hash(body: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(_canonical(body)).hexdigest()


def verify_digest_for(verify_result: str, verify_command: str | None) -> str:
    """A stable digest of what the cycle verified, and with what.

    Two cycles that ran the same command to the same outcome produce the same
    digest; a cycle that ran no verification produces the digest of exactly
    that fact.  The digest never claims a verification that did not run.
    """
    return "sha256:" + hashlib.sha256(
        f"{verify_result}|{verify_command or ''}".encode()
    ).hexdigest()


# ---------------------------------------------------------------------------
# Locations
# ---------------------------------------------------------------------------


def checkpoint_dir(job_id: str) -> Path:
    """The job's evidence area, ``checkpoints/`` subdirectory.

    Built on ``pingpong_job.job_evidence_dir`` so checkpoints land exactly
    where every other job-level record lives — no second evidence convention.
    """
    from packages.orchestration.pingpong_job import job_evidence_dir
    from packages.orchestration.safe_points import validate_job_id

    return Path(job_evidence_dir(validate_job_id(str(job_id)))) / CHECKPOINT_DIRNAME


def checkpoint_paths(job_id: str) -> list[Path]:
    """Every checkpoint file for a job, oldest first, ordered by index."""
    directory = checkpoint_dir(job_id)
    if not directory.is_dir():
        return []
    return sorted(directory.glob(_CHECKPOINT_GLOB), key=_index_of_path)


def _index_of_path(path: Path) -> int:
    """The cycle index encoded in the filename; -1 when it is unreadable.

    Ordering never depends on the record body — a corrupted file still sorts
    into its right place, which is what lets the loader walk backwards past it.
    """
    try:
        return int(path.stem.split("_", 1)[1])
    except (IndexError, ValueError):
        return -1


def _job_snapshot_reference(job_id: str) -> tuple[str, str]:
    """(data-root-relative path, sha256) of the persisted job snapshot.

    Returns ("", "") when the snapshot cannot be read.  A checkpoint that
    could not measure the snapshot says so rather than inventing a digest.
    """
    try:
        from packages.orchestration.data_paths import jobs_dir

        path = jobs_dir() / f"{job_id}.json"
        data = path.read_bytes()
    except (OSError, ValueError):
        return ("", "")
    return (f"jobs/{job_id}.json", "sha256:" + hashlib.sha256(data).hexdigest())


def resolve_worktree_head(job_id: str) -> str:
    """The worktree head recorded on the persisted job plan, or "" when unknown.

    ``packages.core.models.Job`` carries no worktree field — the F006 job plan
    does, and that is the only durable source.  A job that never ran in a
    worktree honestly reports no head.
    """
    try:
        from packages.orchestration.pingpong_job import load_job_plan

        plan = load_job_plan(str(job_id))
    except Exception:  # noqa: BLE001 — a missing/corrupt plan must not break a write
        return ""
    return str(getattr(plan, "worktree_head", "") or "") if plan is not None else ""


# ---------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------


def build_checkpoint(
    job_id: str,
    cycle_index: int,
    *,
    budget_spent_tokens: int = 0,
    verify_result: str = "",
    verify_command: str | None = None,
    next_intent: dict[str, Any] | None = None,
    worktree_head: str | None = None,
    now: datetime | None = None,
) -> Checkpoint:
    """Assemble the record for one cycle boundary.

    Everything that has to be looked up on disk (job snapshot, worktree head)
    is looked up HERE, so the writer below stays a pure serializer.
    """
    jid = str(job_id)
    snapshot_path, snapshot_sha = _job_snapshot_reference(jid)
    head = resolve_worktree_head(jid) if worktree_head is None else worktree_head
    stamp = (now or datetime.now(timezone.utc)).isoformat()
    return Checkpoint(
        cycle_index=cycle_index,
        job_id=jid,
        job_snapshot_path=snapshot_path,
        job_snapshot_sha256=snapshot_sha,
        worktree_head=head,
        budget_spent_tokens=budget_spent_tokens,
        verify_result=verify_result,
        verify_digest=verify_digest_for(verify_result, verify_command),
        next_intent=dict(next_intent or {"kind": INTENT_NONE}),
        created_at=stamp,
    )


def write_checkpoint(job_id: str, checkpoint: Checkpoint,
                     *, retention: int | None = None) -> Path:
    """Persist one checkpoint atomically, then prune superseded ones.

    Raises on failure — the caller decides whether a failed checkpoint may
    stop anything.  Inside the cycle loop it never may; see
    ``record_cycle_checkpoint``.
    """
    directory = checkpoint_dir(job_id)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / CHECKPOINT_FILENAME.format(index=checkpoint.cycle_index)
    _atomic_write(path, json.dumps(checkpoint.to_json(), indent=2, sort_keys=True))
    apply_retention(job_id, retention)
    return path


def record_cycle_checkpoint(
    job_id: str,
    cycle_index: int,
    *,
    budget_spent_tokens: int = 0,
    verify_result: str = "",
    verify_command: str | None = None,
    next_intent: dict[str, Any] | None = None,
    retention: int | None = None,
) -> tuple[Path | None, str]:
    """Write a cycle's checkpoint and NEVER raise out of the cycle.

    Returns ``(path, "")`` on success and ``(None, reason)`` on failure.  A
    run must not die because bookkeeping hiccuped (feature-file A9): the
    caller logs the reason, keeps going, and the next cycle retries.
    """
    try:
        checkpoint = build_checkpoint(
            job_id, cycle_index,
            budget_spent_tokens=budget_spent_tokens,
            verify_result=verify_result,
            verify_command=verify_command,
            next_intent=next_intent,
        )
        return (write_checkpoint(job_id, checkpoint, retention=retention), "")
    except Exception as exc:  # noqa: BLE001 — bookkeeping never kills the run
        reason = f"{type(exc).__name__}: {exc}"
        _log.warning(
            "checkpoint write FAILED for job %s cycle %s: %s — the run continues "
            "and the next cycle retries", job_id, cycle_index, reason,
        )
        return (None, reason)


# ---------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------


def read_checkpoint(path: Path) -> Checkpoint | None:
    """Parse and VERIFY one checkpoint file.  ``None`` when it does not verify.

    "Does not verify" covers every way a file can lie: unreadable, not JSON,
    wrong shape, unknown schema version, or a body whose hash does not match
    the stored one.  The caller cannot tell those apart on purpose — none of
    them may be trusted.
    """
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(raw, dict):
        return None
    body = raw.get("record")
    stored_hash = raw.get("content_hash")
    if not isinstance(body, dict) or not isinstance(stored_hash, str):
        return None
    try:
        if compute_content_hash(body) != stored_hash:
            return None
        checkpoint = Checkpoint.from_body(body)
    except (KeyError, TypeError, ValueError):
        return None
    if checkpoint.schema_version != SCHEMA_VERSION:
        return None
    return checkpoint


def load_latest_valid(job_id: str) -> Checkpoint | None:
    """The newest checkpoint whose hash verifies.

    Walks newest-first.  Every file it has to skip is logged as a warning and
    left on disk for forensics.  Returns ``None`` when the job was never
    checkpointed; raises ``AllCheckpointsCorruptError`` when checkpoints exist
    but not one of them verifies — the caller must be able to tell those two
    apart.
    """
    paths = checkpoint_paths(job_id)
    if not paths:
        return None
    skipped: list[str] = []
    for path in reversed(paths):
        checkpoint = read_checkpoint(path)
        if checkpoint is not None:
            if skipped:
                _log.warning(
                    "job %s: resumed from %s after skipping %d unverifiable "
                    "checkpoint(s) (kept on disk for forensics): %s",
                    job_id, path.name, len(skipped), ", ".join(skipped),
                )
            return checkpoint
        skipped.append(path.name)
        _log.warning("job %s: checkpoint %s does not verify — skipped, kept on disk",
                     job_id, path.name)
    raise AllCheckpointsCorruptError(str(job_id), skipped)


# ---------------------------------------------------------------------------
# Retention
# ---------------------------------------------------------------------------


def resolve_retention(config: Any = None) -> int:
    """How many checkpoints to keep.  Config beats the small default."""
    if config is None:
        try:
            from packages.orchestration.config import get_config

            config = get_config()
        except Exception:  # noqa: BLE001 — retention must never break a write
            return DEFAULT_RETENTION
    try:
        value = config.get(CONFIG_KEY_RETENTION)
    except Exception:  # noqa: BLE001
        return DEFAULT_RETENTION
    if value is None:
        return DEFAULT_RETENTION
    try:
        return max(1, int(value))
    except (TypeError, ValueError):
        return DEFAULT_RETENTION


def apply_retention(job_id: str, keep: int | None = None) -> list[str]:
    """Prune superseded checkpoints; return the names actually deleted.

    Kept, always: the FIRST checkpoint (where the run began) and the LATEST
    (where it stands), plus the last ``keep`` overall.  Also kept, always: any
    file that does not verify — a corrupted checkpoint is forensic evidence,
    and retention is not the mechanism that discards evidence.
    """
    limit = resolve_retention() if keep is None else max(1, int(keep))
    paths = checkpoint_paths(job_id)
    if len(paths) <= limit:
        return []
    survivors = {paths[0], *paths[-limit:]}
    deleted: list[str] = []
    for path in paths:
        if path in survivors:
            continue
        if read_checkpoint(path) is None:
            continue                       # unverifiable: kept for forensics
        try:
            path.unlink()
        except OSError as exc:
            _log.warning("job %s: could not prune checkpoint %s: %s",
                         job_id, path.name, exc)
            continue
        deleted.append(path.name)
    return deleted
