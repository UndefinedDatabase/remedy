"""F041 T002 — the preview record and its state machine (DECISION F041 D3).

This module holds the preview record and runs nothing: it never launches a process,
never imports ``subprocess``, ``packages.runtimes`` or ``preview_runner``. The one
runtime verb that ever runs lives in :mod:`packages.orchestration.preview_runner`, and
is handed to :func:`run_pending` as a plain callable so this module can be read, and
tested, without a child process anywhere in it.

One record per job, ``preview.json`` under the job's own directory, schema
``remedy.preview.v1``. Its ``state`` is one of ``PREVIEW_STATES``; while it is one of
``ACTIVE_STATES`` (``starting``, ``probing``, ``live``) a fresh start request changes
nothing (DECISION F041 D3 (3)) — a preview already under way, or already live, is not
restarted underneath itself.

The two functions that touch the record split cleanly along "recording a request" and
"acting on one": :func:`request_preview` records a start or a stop and runs no verb;
:func:`run_pending` reads the record's own pending ``requested`` action and, if one is
set, runs it with the verb callable it is handed. A start serves, records ``probing``,
then probes: only a passed probe records ``live`` with the probe's own link — never the
serve's, because the serve answers only that a process began, not that it is healthy
(DECISION F041 D3 (3)). A failed probe stops the runtime again and records ``failed``
with a message naming the health check; a serve the harness cannot configure records
``not_applicable``; any other serve failure records ``failed`` with the harness's own
message. The link (``url``, ``port``) is cleared on every ending but a passed probe, and
``viewed_at`` is set only when a preview goes ``live`` — the one moment a person is
handed a link to open.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from packages.common.secure_fs import durable_write_json
from packages.orchestration.data_paths import job_dir

#: The record's schema tag. Any other value on disk makes the record unusable.
PREVIEW_SCHEMA = "remedy.preview.v1"

#: The record's filename, under the job's own directory.
PREVIEW_FILENAME = "preview.json"

STATE_STOPPED = "stopped"
STATE_STARTING = "starting"
STATE_PROBING = "probing"
STATE_LIVE = "live"
STATE_FAILED = "failed"
STATE_NOT_APPLICABLE = "not_applicable"

#: Every state a preview record may hold, in the order the tests pin.
PREVIEW_STATES = (
    STATE_STOPPED,
    STATE_STARTING,
    STATE_PROBING,
    STATE_LIVE,
    STATE_FAILED,
    STATE_NOT_APPLICABLE,
)

#: The states a fresh start request finds already under way, and so changes nothing.
ACTIVE_STATES = (STATE_STARTING, STATE_PROBING, STATE_LIVE)

ACTION_START = "start"
ACTION_STOP = "stop"
PREVIEW_ACTIONS = (ACTION_START, ACTION_STOP)

#: The one error token that turns a failed serve into ``not_applicable`` rather than
#: ``failed``: the harness itself found no runtime to configure, which is not a defect
#: in the job's project, only a project this feature has nothing to show for.
CONFIG_ERROR_TOKEN = "runtime_config_error"


@dataclass(frozen=True)
class VerbResult:
    """What one runtime verb answered: whether it was ok, and its whole envelope."""

    ok: bool
    payload: dict[str, Any]


#: One runtime verb, run against a project root, answering a `VerbResult`. The shape
#: both `preview_runner.run_runtime_verb` and every test's scripted stand-in share.
RuntimeVerb = Callable[[str, Path], VerbResult]


def preview_path(job_id: str, data_root: Path | None = None) -> Path:
    """Where job ``job_id``'s preview record lives."""
    return job_dir(job_id, data_root) / PREVIEW_FILENAME


def _default_record(job_id: str) -> dict[str, Any]:
    return {
        "schema": PREVIEW_SCHEMA,
        "job_id": job_id,
        "state": STATE_STOPPED,
        "requested": "",
        "url": "",
        "port": 0,
        "reason": "",
        "updated_at": "",
        "viewed_at": "",
    }


def load_preview(job_id: str, data_root: Path | None = None) -> dict[str, Any]:
    """The job's preview record, or the stopped default when none can be trusted.

    A stored record is used only when its ``schema`` is `PREVIEW_SCHEMA` and its
    ``state`` is in `PREVIEW_STATES` — anything else (unreadable, foreign, or naming a
    state this module has never written) is not merged at all, and the default is
    returned whole. Once that gate passes, each key of the default is taken from the
    stored record only when the stored value's type matches the default's, so a
    corrupted single field cannot poison the rest of the record.
    """
    record = _default_record(job_id)
    path = preview_path(job_id, data_root)
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return record
    try:
        stored = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        return record
    if (not isinstance(stored, dict)
            or stored.get("schema") != PREVIEW_SCHEMA
            or stored.get("state") not in PREVIEW_STATES):
        return record
    for key, default_value in record.items():
        if key in stored and isinstance(stored[key], type(default_value)):
            record[key] = stored[key]
    return record


def preview_view(job_id: str, data_root: Path | None = None) -> dict[str, Any]:
    """The cockpit-facing slice of the record: state, link, reason, and when."""
    record = load_preview(job_id, data_root)
    return {
        "state": record["state"],
        "url": record["url"],
        "port": record["port"],
        "reason": record["reason"],
        "updated_at": record["updated_at"],
    }


def _persist(record: dict[str, Any], job_id: str, data_root: Path | None) -> None:
    path = preview_path(job_id, data_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    durable_write_json(path, record)


def request_preview(
    job_id: str, action: str, *, now: datetime, data_root: Path | None = None,
) -> dict[str, Any]:
    """Record a start or a stop. Runs no verb; :func:`run_pending` acts on it.

    A start request while the record is already `ACTIVE_STATES` changes nothing —
    nothing is written, and the unchanged record is returned. A stop request always
    records, whatever the current state, because stopping an idle preview is never a
    conflict the way restarting a live one would be.
    """
    if action not in PREVIEW_ACTIONS:
        raise ValueError(f"unknown preview action: {action!r}")

    record = load_preview(job_id, data_root)
    if action == ACTION_START and record["state"] in ACTIVE_STATES:
        return record

    record = dict(record)
    record["requested"] = action
    record["updated_at"] = now.isoformat()
    if action == ACTION_START:
        record["state"] = STATE_STARTING
        record["url"] = ""
        record["port"] = 0
        record["reason"] = ""
    _persist(record, job_id, data_root)
    return record


def _verb_message(result: VerbResult) -> str:
    """The message of a failed verb: its envelope's ``message``, else ``error``."""
    message = result.payload.get("message")
    if isinstance(message, str):
        return message
    error = result.payload.get("error")
    if isinstance(error, str):
        return error
    return "unknown error"


def _settle(
    record: dict[str, Any], *, state: str, reason: str, url: str, port: int,
    now: datetime,
) -> dict[str, Any]:
    settled = dict(record)
    settled["state"] = state
    settled["requested"] = ""
    settled["url"] = url
    settled["port"] = port
    settled["reason"] = reason
    settled["updated_at"] = now.isoformat()
    return settled


def _no_project_folder(
    record: dict[str, Any], requested: str, job_id: str, data_root: Path | None,
    now: datetime,
) -> dict[str, Any]:
    state = STATE_FAILED if requested == ACTION_START else STATE_STOPPED
    settled = _settle(
        record, state=state, reason="the job has no project folder to run",
        url="", port=0, now=now,
    )
    _persist(settled, job_id, data_root)
    return settled


def _run_start(
    record: dict[str, Any], job_id: str, root: Path, runner: RuntimeVerb,
    now: datetime, data_root: Path | None,
) -> dict[str, Any]:
    served = runner("serve", root)
    if not served.ok:
        message = _verb_message(served)
        state = (STATE_NOT_APPLICABLE
                 if served.payload.get("error") == CONFIG_ERROR_TOKEN else STATE_FAILED)
        settled = _settle(record, state=state, reason=message, url="", port=0, now=now)
        _persist(settled, job_id, data_root)
        return settled

    probing = dict(record)
    probing["state"] = STATE_PROBING
    probing["updated_at"] = now.isoformat()
    _persist(probing, job_id, data_root)

    probed = runner("probe", root)
    if not probed.ok:
        message = _verb_message(probed)
        runner("stop", root)
        settled = _settle(
            probing, state=STATE_FAILED,
            reason=f"started but health check failed: {message}", url="", port=0,
            now=now,
        )
        _persist(settled, job_id, data_root)
        return settled

    url = probed.payload.get("url", "")
    port = probed.payload.get("port", 0)
    settled = _settle(probing, state=STATE_LIVE, reason="", url=url, port=port, now=now)
    settled["viewed_at"] = now.isoformat()
    _persist(settled, job_id, data_root)
    return settled


def _run_stop(
    record: dict[str, Any], job_id: str, root: Path, runner: RuntimeVerb,
    now: datetime, data_root: Path | None,
) -> dict[str, Any]:
    stopped = runner("stop", root)
    if not stopped.ok:
        message = _verb_message(stopped)
        settled = _settle(
            record, state=STATE_FAILED, reason=f"could not stop: {message}",
            url="", port=0, now=now,
        )
    else:
        settled = _settle(
            record, state=STATE_STOPPED, reason="stopped on request",
            url="", port=0, now=now,
        )
    _persist(settled, job_id, data_root)
    return settled


def run_pending(
    job: Any, runner: RuntimeVerb, *, now: datetime, data_root: Path | None = None,
) -> dict[str, Any]:
    """Act on the job's pending preview request with ``runner``, and persist the end.

    Dispatch reads the record's own ``requested`` field, not its ``state`` — a fresh
    start request is recorded with ``state`` already set to ``starting`` (so a second
    start request finds it in `ACTIVE_STATES` and changes nothing), and this is exactly
    the request this call must still process. Nothing is pending when ``requested`` is
    empty, and the record is returned unchanged.
    """
    job_id = job.job_id
    record = load_preview(job_id, data_root)
    requested = record["requested"]
    if requested == "":
        return record

    repo_path = getattr(job, "repo_path", "") or ""
    if not repo_path or not Path(repo_path).is_dir():
        return _no_project_folder(record, requested, job_id, data_root, now)

    root = Path(repo_path)
    if requested == ACTION_START:
        return _run_start(record, job_id, root, runner, now, data_root)
    return _run_stop(record, job_id, root, runner, now, data_root)
