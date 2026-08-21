"""The per-job command nonce store — DECISION F009 D8, ordered by DECISION F009 D15.

The single write door deduplicates by client nonce: a client that retries after a network
timeout must receive the answer the server already gave, not a second effect. This module
owns that store and nothing else — it decides no status code, refuses no request and never
reads a request. `packages/orchestration/ui_server.py` decides; this remembers what was
decided, so that "a replayed nonce is idempotent" is a property of the door rather than a
promise.

One nonce is ONE CREATE-ONLY file, `commands_nonce/<nonce>.json`, inside the job's private
control directory, and the replay window is the job's lifetime (DECISION F009 D8). One file
per nonce rather than one map is what lets two racing publishers converge on a single answer
without a lock: the loser of the `os.link` reads the winner's record and returns it.

PUBLICATION HAS NO DOOR CALL SITE YET, and that hole is deliberate — a reader who greps for
the caller of `publish_nonce_result` finds this paragraph instead of a hole. DECISION F009
D15 rules that a record is published only for an ACCEPTED command, and the door still ends
at its 501 seam, so nothing is accepted yet. Publishing the seam's own 501 would freeze a
transient answer into a permanent one: D8's contract is that a seen nonce returns the
ORIGINAL result, so that 501 would be replayed for the rest of the job's life to the one
client unlucky enough to have retried during the seam. The publish call site therefore lands
with T003's effect table, in the round that retires the seam. Until then the door only ever
LOOKS a nonce up, and this module's own tests are what exercise publication.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from packages.common import secure_fs as _fs
from packages.orchestration import safe_points

__all__ = [
    "NONCE_DIRNAME",
    "NONCE_FILE_MODE",
    "NONCE_FIELD_ORDER",
    "MAX_NONCE_RECORD_BYTES",
    "nonce_is_valid",
    "publish_nonce_result",
    "lookup_nonce_result",
]

#: DECISION F009 D8 fixes the name. It sits beside `commands_audit.jsonl` and `archive`
#: in the job's control directory, so one job's whole write-door state is in one place.
NONCE_DIRNAME = "commands_nonce"

#: The mode the job control directory's other files already use.
NONCE_FILE_MODE = 0o600

#: A record carries the STATUS as well as the body: a body without its status cannot answer
#: a replay truthfully, because the same body means different things under 200 and under 501.
#: The order is fixed and the record is built key by key in it, never sorted.
NONCE_FIELD_ORDER = ("status", "body")

#: A record this large is a bug in the caller, not a response. Matches the door's own
#: request ceiling, so nothing that fits through the door fails to fit in the store.
MAX_NONCE_RECORD_BYTES = 64 * 1024


def nonce_is_valid(nonce: Any) -> bool:
    """True when `nonce` may become a FILENAME in this store.

    A nonce is client-supplied and becomes a path component, so its character class IS the
    guard: `safe_points.is_safe_id`, the same `_ID_RE` that already validates the job
    segment of the very directory this file lands in. `../escape` is not a nonce, an empty
    string is not a nonce, and neither is a 65-character one.
    """
    return safe_points.is_safe_id(nonce)


def _record_name(nonce: str) -> str:
    return f"{nonce}.json"


def _record_bytes(record: dict[str, Any]) -> bytes:
    """Serialise one record with its D15 field order intact.

    `json_bytes` defaults to `sort_keys=True`, which would alphabetise `status` ahead of
    `body` and quietly re-order every record; the order is passed explicitly here for the
    same reason `command_audit` passes it.
    """
    ordered = {key: record[key] for key in NONCE_FIELD_ORDER}
    return _fs.json_bytes(ordered, indent=None, sort_keys=False)


def _parse_record(raw: bytes) -> dict[str, Any] | None:
    """Bytes back into a record. Anything that is not one is a MISS, never an exception.

    A record whose status is missing or is not a whole number cannot answer a replay, so it
    is treated exactly as an absent one: the command runs again, which is the behaviour that
    existed before the nonce did. `True` is an `int` in Python and is refused explicitly.
    """
    try:
        record = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None
    if not isinstance(record, dict):
        return None
    status = record.get("status")
    if not isinstance(status, int) or isinstance(status, bool):
        return None
    return {"status": status, "body": record.get("body")}


def _open_nonce_dir_fd(job_id: str, control_root_path: Path | None, *,
                       create: bool) -> int | None:
    """A verified fd for `<job control>/commands_nonce`. None when it does not exist.

    The subdirectory is created only on the publish path, and never by name: it is made
    THROUGH the held job fd at 0700, which is the idiom `safe_points._open_archive_fd`
    already uses for the archive directory beside it.
    """
    job_fd = safe_points.open_job_control_fd(job_id, control_root_path, create=create)
    if job_fd is None:
        return None
    try:
        try:
            return _fs.open_verified_dir(NONCE_DIRNAME, dir_fd=job_fd,
                                         error_cls=safe_points.StopControlError,
                                         noun="command nonce store")
        except _fs.MissingComponent:
            if not create:
                return None

        _fs.require_writable_dir(job_fd, error_cls=safe_points.StopControlError,
                                 noun="command nonce store", label=NONCE_DIRNAME)
        try:
            os.mkdir(NONCE_DIRNAME, safe_points.CONTROL_DIR_MODE, dir_fd=job_fd)
        except FileExistsError:
            pass                                  # another publisher got there first
        except OSError as exc:
            raise safe_points.StopControlError(
                f"cannot create the command nonce store "
                f"({type(exc).__name__}: {exc.strerror or exc})") from exc
        try:
            return _fs.open_verified_dir(NONCE_DIRNAME, dir_fd=job_fd,
                                         error_cls=safe_points.StopControlError,
                                         noun="command nonce store")
        except _fs.MissingComponent as exc:
            raise safe_points.StopControlError(
                "the command nonce store vanished after creation") from exc
    finally:
        os.close(job_fd)


def _read_record(dir_fd: int, nonce: str) -> dict[str, Any] | None:
    raw = _fs.read_verified_file(_record_name(nonce), dir_fd,
                                 max_bytes=MAX_NONCE_RECORD_BYTES,
                                 error_cls=safe_points.StopControlError,
                                 noun="command nonce record")
    if raw is None:
        return None
    return _parse_record(raw)


def publish_nonce_result(job_id: Any, nonce: Any, body: Any, *, status: int,
                         control_root_path: Path | None = None) -> dict[str, Any] | None:
    """Publish ONE result under `nonce`, CREATE-ONLY. Returns the record in force after it.

    The returned record is `{"status": …, "body": …}` — the body that is in force plus the
    status it was returned with, because a replay has to reproduce both. `None` means
    nothing is in force: an unusable nonce, a job id that is not one, or a control directory
    that could not be reached.

    Publication never overwrites. When `write_file_atomically` reports that the name already
    existed, another caller won the race between our open and our link: THEIR record is the
    answer the client already has and ours never existed, so it is read back and returned.
    `safe_points.request_stop` resolves the identical race the identical way, and that
    convergence is why DECISION F009 D8 chose one file per nonce over a map.
    """
    if not nonce_is_valid(nonce):
        return None
    try:
        jid = safe_points.validate_job_id(str(job_id or ""))
    except safe_points.StopControlError:
        return None

    record = {"status": int(status), "body": body}
    dir_fd = _open_nonce_dir_fd(jid, control_root_path, create=True)
    if dir_fd is None:
        return None
    try:
        published = _fs.write_file_atomically(
            dir_fd, _record_name(nonce), _record_bytes(record),
            create_only=True, file_mode=NONCE_FILE_MODE,
            error_cls=safe_points.StopControlError, noun="command nonce record")
        if published:
            return record
        return _read_record(dir_fd, nonce)
    finally:
        os.close(dir_fd)


def lookup_nonce_result(job_id: Any, nonce: Any, *,
                        control_root_path: Path | None = None) -> dict[str, Any] | None:
    """The record published under `nonce`, or None when there is none to replay.

    This is the one function the door calls while the 501 seam stands, so it NEVER raises.
    An unusable nonce, an absent control directory, an absent record and a record this
    process cannot read are all the same answer — a miss. A miss costs the client one
    re-execution, which is exactly the behaviour that existed before the nonce did, whereas
    an exception here would turn a readable refusal into a 500.
    """
    if not nonce_is_valid(nonce):
        return None
    try:
        jid = safe_points.validate_job_id(str(job_id or ""))
    except safe_points.StopControlError:
        return None
    try:
        dir_fd = _open_nonce_dir_fd(jid, control_root_path, create=False)
        if dir_fd is None:
            return None
        try:
            return _read_record(dir_fd, nonce)
        finally:
            os.close(dir_fd)
    except (OSError, safe_points.StopControlError):
        return None
