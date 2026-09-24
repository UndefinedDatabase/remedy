"""F264 T001 — the steering message: accepted, persisted and certified, not yet consumed.

A steering message is one free-form sentence an operator sends to a job while it runs
(`remedy chat <job_id> "<message>"`, and later the cockpit's input field over F009's write
channel). This module is the one place such a message is accepted. It writes the message as a
SEALED record under the job's evidence, create-once, and only then certifies it into the run
log as a `steering_message_received` event (declared in `event_names.py`) carrying the
record's seal, so a later reader can
prove which text the run was given and when (DECISION F264 D1).

A message is CONSUMED at the run's next safe point (T002, DECISION F264 D4): the ping-pong
loop calls `consume_pending_steering` at the top of every round, before anything of that round
is composed or sent, and folds every consumed message into the builder prompt. A sealed record
never changes after it is written, so the round a message took effect in is its own sealed
consumption marker rather than an edit to the record. The acknowledgement is T003.

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


# --- T002: consumption at the run's safe point (DECISION F264 D4) -----------------------------

CONSUMPTION_SCHEMA = "remedy.steering_consumption.v1"
CONSUMED_DIRNAME = "consumed"


def consumption_dir(job_id: str, root: Path | None = None) -> Path:
    """The folder holding one create-once consumption marker per consumed message."""
    return steering_dir(job_id, root) / CONSUMED_DIRNAME


def consume_pending_steering(
    job_id: str, *, task_id: str, round_number: int,
    root: Path | None = None, now: datetime | None = None,
) -> list[dict[str, Any]]:
    """At a run's safe point: consume every pending message, and return every consumed one.

    A message is consumed EXACTLY ONCE, by publishing a sealed marker under
    `consumed/<message_id>.json` create-once, naming the task and round it took effect in;
    only the call that publishes the marker writes the `steering_message_consumed` event. The
    return value is EVERY message of the job, oldest first, because every message is consumed
    once this call returns and a correction holds for the rest of the job, not for one round.
    A tampered record raises `SteeringError` from `list_steering_messages`, so a run never
    folds in text it cannot prove the operator sent. A job with no message writes nothing.

    For a job that belongs to a mission, consuming a message also AMENDS the mission's
    contract with it (DECISION F264 D5, DECISION amend0905-vocab D9), before the marker is
    published, and the marker names the amendment. The job's own lock keeps one runner per
    job, which is what makes checking for the marker and then amending safe.
    """
    records = list_steering_messages(job_id, root)
    if not records:
        return []
    folder = consumption_dir(job_id, root)
    try:
        folder.mkdir(parents=True, exist_ok=True)
        dir_fd = os.open(folder, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    except OSError as exc:
        raise SteeringWriteError(f"the consumption folder cannot be opened: {exc}") from exc
    consumed_now: list[dict[str, Any]] = []
    mission: Any = _UNRESOLVED
    try:
        for record in records:
            if (folder / f"{record['message_id']}.json").exists():
                continue
            if mission is _UNRESOLVED:
                mission = _mission_of(job_id, root)
            amendment_id = _amend_mission(mission, record["text"], root, now) if mission else ""
            marker: dict[str, Any] = {
                "schema": CONSUMPTION_SCHEMA,
                "message_id": record["message_id"],
                "message_sha256": record["record_sha256"],
                "job_id": str(job_id),
                "task_id": str(task_id),
                "round_number": int(round_number),
                "consumed_at": (now or datetime.now(timezone.utc)).isoformat(),
                "mission_id": mission.id if mission else "",
                "amendment_id": amendment_id,
            }
            marker["record_sha256"] = _seal(marker)
            try:
                published = write_file_atomically(
                    dir_fd, f"{record['message_id']}.json", json_bytes(marker), create_only=True,
                    noun="steering consumption marker")
            except SecureFsError as exc:
                raise SteeringWriteError(str(exc)) from exc
            if published:
                consumed_now.append(marker)
        if consumed_now:
            with contextlib.suppress(OSError):
                os.fsync(dir_fd)
    finally:
        os.close(dir_fd)

    if consumed_now:
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.timeline import append_run_event

        for marker in consumed_now:
            append_run_event(
                root if root is not None else resolve_data_root(), job_id,
                event="steering_message_consumed",
                metadata={"message_id": marker["message_id"], "task_id": marker["task_id"],
                          "round_number": marker["round_number"],
                          "record_sha256": marker["message_sha256"],
                          "amendment_id": marker["amendment_id"]},
            )
    return records


#: "Not looked up yet", as distinct from a job that belongs to no mission.
_UNRESOLVED = object()


def _mission_of(job_id: str, root: Path | None) -> Any:
    """The mission the job belongs to, or None; looked up only when a message is pending."""
    from packages.orchestration.mission_state import mission_for_job

    return mission_for_job(str(job_id), root)


def _amend_mission(mission: Any, text: str, root: Path | None, now: datetime | None) -> str:
    """Amend ``mission``'s contract with one steering message and return the amendment's id.

    F269's `amend_mission_contract` adds one blocking criterion compiled from the message and
    an entry that applies from the mission's next loop round, where the loop acknowledges it
    (DECISION F269 D8). A failure raises: a message the mission silently lost is the ignored
    steering this feature exists to prevent.
    """
    from packages.orchestration.mission_contract import amend_mission_contract

    contract = amend_mission_contract(mission.project_id, mission.id, text, root=root, now=now)
    return str(contract.amendments[-1]["id"])


def list_steering_consumptions(job_id: str, root: Path | None = None) -> dict[str, dict[str, Any]]:
    """The job's consumption markers by message id; a marker that fails its seal raises."""
    folder = consumption_dir(job_id, root)
    if not folder.is_dir():
        return {}
    markers: dict[str, dict[str, Any]] = {}
    for path in sorted(folder.glob("sm-*.json")):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise SteeringError(f"consumption marker {path.name} is unreadable: {exc}") from exc
        if (not isinstance(body, dict) or body.get("schema") != CONSUMPTION_SCHEMA
                or body.get("record_sha256") != _seal(body)
                or body.get("message_id") != path.stem):
            raise SteeringError(f"consumption marker {path.name} is not intact")
        markers[path.stem] = body
    return markers


def render_steering_segment(records: list[dict[str, Any]]) -> str:
    """The builder prompt's steering segment for ``records``, or "" when there are none.

    Each message is carried VERBATIM, one bullet each, oldest first; a message's own line
    breaks are kept and indented under its bullet, never joined or cut, for the reason F033
    gives for an operator's rejection reason: text that is half-quoted has been rewritten.
    """
    if not records:
        return ""
    lines = [
        "OPERATOR STEERING — messages the operator sent to this job while it ran, oldest first.",
        "Follow them. Where one conflicts with an earlier instruction, the later message wins.",
    ]
    for record in records:
        lines.append("- " + str(record["text"]).replace("\n", "\n  "))
    return "\n".join(lines) + "\n"
