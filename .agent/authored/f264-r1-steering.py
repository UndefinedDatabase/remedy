"""F264 T001 — the steering message: accepted, persisted and certified, not yet consumed.

A steering message is one free-form sentence an operator sends to a job while it runs
(`remedy chat <job_id> "<message>"`, and later the cockpit's input field over F009's write
channel). This module is the one place such a message is accepted. It writes the message as a
SEALED record under the job's evidence, create-once, and only then certifies it into the run
log as a `steering_message_received` event (declared in `event_names.py`) carrying the
record's seal, so a later reader can
prove which text the run was given and when (DECISION F264 D1).

Remedy deliberately does not consume a message here. Folding it into the next prompt at the
run's next safe point is T002, and the acknowledgement is T003; a sealed record never changes
after it is written, so the round a message is consumed in is recorded by T002 as its own
fact rather than by rewriting this one.

Remedy deliberately does not accept a message for a job that has ended: no run will ever
read it, and a steering message the run silently ignores is worse than no channel at all
(T5_F264.md, "Why this exists").
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.common.secure_fs import SecureFsError, json_bytes, write_file_atomically

SCHEMA = "remedy.steering_message.v1"
RECORD_DIRNAME = "steering"
#: A correction is usually one sentence; the bound keeps a message inside one prompt segment.
STEERING_MAX_CHARS = 2000
#: Where the message came from: the CLI today, the cockpit's input field once T003 wires it.
STEERING_CHANNELS = frozenset({"cli", "cockpit"})
#: Record ids are numbered per job; this many attempts cover every concurrent sender.
_MAX_ID_ATTEMPTS = 64


class SteeringError(ValueError):
    """A message was refused before anything was written."""


class SteeringWriteError(SteeringError):
    """A message was acceptable but its record could not be written."""


def _seal(body: dict[str, Any]) -> str:
    unsealed = {k: v for k, v in body.items() if k != "record_sha256"}
    return hashlib.sha256(json.dumps(unsealed, sort_keys=True).encode("utf-8")).hexdigest()


def steering_dir(job_id: str, root: Path | None = None) -> Path:
    """The folder holding the job's steering records, beside its other evidence."""
    from packages.orchestration.data_paths import job_evidence_dir

    return job_evidence_dir(job_id, root) / RECORD_DIRNAME


def normalize_steering_text(text: object) -> str:
    """The message as it will be recorded, or `SteeringError` naming why it is refused."""
    if not isinstance(text, str):
        raise SteeringError("the message must be text")
    cleaned = text.strip()
    if not cleaned:
        raise SteeringError("the message is empty")
    if "\x00" in cleaned:
        raise SteeringError("the message contains a NUL character")
    if len(cleaned) > STEERING_MAX_CHARS:
        raise SteeringError(
            f"the message is {len(cleaned)} characters long; the limit is {STEERING_MAX_CHARS}")
    return cleaned


def _numbered_records(folder: Path) -> list[tuple[int, Path]]:
    found = [(int(p.stem[3:]), p) for p in folder.glob("sm-*.json") if p.stem[3:].isdigit()]
    return sorted(found)


def _next_number(folder: Path) -> int:
    return max((n for n, _ in _numbered_records(folder)), default=0) + 1


def record_steering_message(
    job_id: str, text: object, *, job_state: str, channel: str,
    root: Path | None = None, now: datetime | None = None,
) -> dict[str, Any]:
    """Accept ``text`` for ``job_id``, write its sealed record, certify it, and return the record.

    ``job_state`` is the job's stored state, read by the caller; an ended job refuses. The
    record is published create-once under the next free id, so two senders at once get two
    records and neither overwrites the other. The run-log event is written only after the
    record is on disk, so an event never names a record that does not exist.
    """
    from packages.orchestration.pingpong_job import job_is_terminal

    if channel not in STEERING_CHANNELS:
        raise SteeringError(f"unknown channel {channel!r}")
    if job_is_terminal(job_state):
        raise SteeringError(f"job {job_id} has ended ({job_state}); no run will read a message")
    message = normalize_steering_text(text)

    folder = steering_dir(job_id, root)
    received_at = (now or datetime.now(timezone.utc)).isoformat()
    try:
        folder.mkdir(parents=True, exist_ok=True)
        dir_fd = os.open(folder, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    except OSError as exc:
        raise SteeringWriteError(f"the steering folder cannot be opened: {exc}") from exc
    try:
        number = _next_number(folder)
        for _ in range(_MAX_ID_ATTEMPTS):
            body: dict[str, Any] = {
                "schema": SCHEMA,
                "message_id": f"sm-{number:04d}",
                "job_id": str(job_id),
                "text": message,
                "channel": channel,
                "received_at": received_at,
            }
            body["record_sha256"] = _seal(body)
            try:
                published = write_file_atomically(
                    dir_fd, f"{body['message_id']}.json", json_bytes(body), create_only=True,
                    noun="steering record")
            except SecureFsError as exc:
                raise SteeringWriteError(str(exc)) from exc
            if published:
                with contextlib.suppress(OSError):
                    os.fsync(dir_fd)
                break
            number += 1
        else:
            raise SteeringWriteError(
                f"no free steering record id after {_MAX_ID_ATTEMPTS} attempts")
    finally:
        os.close(dir_fd)

    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.timeline import append_run_event

    append_run_event(
        root if root is not None else resolve_data_root(), job_id,
        event="steering_message_received",
        metadata={"message_id": body["message_id"], "channel": channel, "text": message,
                  "record_sha256": body["record_sha256"]},
    )
    return body


def verify_steering_record(path: Path) -> list[str]:
    """Every reason the record at ``path`` is not intact; empty when it is."""
    try:
        body = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"unreadable: {exc}"]
    if not isinstance(body, dict):
        return ["not a JSON object"]
    problems: list[str] = []
    if body.get("schema") != SCHEMA:
        problems.append(f"schema is {body.get('schema')!r}, not {SCHEMA!r}")
    if body.get("record_sha256") != _seal(body):
        problems.append("record_sha256 does not match the record")
    if body.get("message_id") != Path(path).stem:
        problems.append(f"message_id {body.get('message_id')!r} does not match the file name")
    return problems


def list_steering_messages(job_id: str, root: Path | None = None) -> list[dict[str, Any]]:
    """The job's steering records in the order they were accepted.

    A record that fails verification raises `SteeringError`: a tampered message must be loud,
    never silently skipped or silently trusted.
    """
    folder = steering_dir(job_id, root)
    if not folder.is_dir():
        return []
    records = []
    for _, path in _numbered_records(folder):
        problems = verify_steering_record(path)
        if problems:
            raise SteeringError(f"steering record {path.name} is not intact: {'; '.join(problems)}")
        records.append(json.loads(path.read_text(encoding="utf-8")))
    return records
