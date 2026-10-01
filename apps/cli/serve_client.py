"""The command line's client mode (F200, DECISIONs F200 D1 (3) and D3).

When a `remedy serve start` supervisor answers on the resolved data root's
socket, a command the cockpit's door carries does not write its effect itself:
it sends the effect as one F009 command envelope to the supervisor and prints the
answer exactly as it prints its own. Everything before the effect — resolving the
job id, the refusals a read can decide — still runs here, so both modes print the
same lines and exit with the same codes. With no supervisor answering, nothing
in this module is used and the command runs direct, as it always has.

`REMEDY_SERVE_DIRECT` set to a non-empty value forces direct mode; the supervisor
sets it for the runs it starts, so a run it started never sends a command back to
the supervisor that is waiting on it.
"""
from __future__ import annotations

import os
import secrets
from typing import Any

from apps.cli.json_envelope import fail

#: The environment variable that forces direct mode.
DIRECT_ENV = "REMEDY_SERVE_DIRECT"


def supervisor_answers() -> bool:
    """True when this process should send door commands to a supervisor."""
    if os.environ.get(DIRECT_ENV):
        return False
    from packages.orchestration.serve_daemon import socket_answers
    from packages.orchestration.serve_paths import serve_paths

    return socket_answers(serve_paths().socket)


def forward_effect(job_id: str, command: str, args: dict[str, Any], *,
                   json_output: bool, error: str, subject: str) -> dict[str, Any]:
    """Send COMMAND's effect for JOB_ID to the supervisor; the door's body without `command`.

    A refusal the door returns is reported with ERROR and SUBJECT as the command's
    own refusals are; a supervisor that stops answering mid-request is reported as
    `serve_unreachable`, and the command never falls back to writing direct,
    because the supervisor may already have applied it.
    """
    from packages.orchestration.serve_daemon import post_command

    envelope = {"command": command, "client_nonce": secrets.token_hex(8), "args": args}
    try:
        status, body = post_command(None, job_id, envelope)
    except (OSError, ValueError) as exc:
        fail("serve_unreachable",
             f"the serve supervisor did not answer {command} for job {job_id} — {exc}; "
             f"check `remedy serve status`",
             json_output=json_output, job_id=job_id)
    if status != 200:
        detail = body.get("error", "") if isinstance(body, dict) else ""
        fail(error, f"{subject} — the serve supervisor refused it: {detail or status}",
             json_output=json_output, job_id=job_id, status=status)
    return {k: v for k, v in body.items() if k != "command"}
