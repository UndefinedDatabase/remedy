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

import codecs
import os
import secrets
import sys
import time
from typing import Any

from apps.cli.json_envelope import fail
from packages.orchestration.serve_runs import DIRECT_ENV

__all__ = ["DIRECT_ENV", "follow_run", "forward_effect", "supervisor_answers"]

#: How long a run whose process is gone may take to have its end recorded before
#: following it gives up and says so.
END_GRACE_SECONDS = 5.0


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


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def follow_run(body: dict[str, Any], *, poll: float = 0.1) -> int:
    """Print the output of the run BODY names as it is written, until its end is recorded.

    BODY is the door's answer to `job.run`: the run's record. Its standard output goes
    to this process's standard output and its standard error to this one's, decoded
    as they arrive, and the run's exit code is returned. Every other ending returns 1,
    the CLI's `failed`, because its exit-code table has no narrower code for them
    (DECISION F283 D12): Ctrl-C, which stops following and leaves the run going; a
    run a signal ended; and a run whose process is gone and whose end was not
    recorded within `END_GRACE_SECONDS`.
    """
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import read_run_record

    paths = serve_paths()
    job_id, pid = str(body["job_id"]), int(body["pid"])
    sources = [(open(body["out_log"], "rb"), sys.stdout), (open(body["err_log"], "rb"), sys.stderr)]
    decoders = [codecs.getincrementaldecoder("utf-8")("replace") for _ in sources]
    gone_since: float | None = None

    def drain(final: bool = False) -> None:
        for (source, stream), decoder in zip(sources, decoders):
            text = decoder.decode(source.read(), final=final)
            if text:
                stream.write(text)
                stream.flush()

    try:
        while True:
            record = read_run_record(paths, job_id)
            ended = record is not None and record.pid == pid and record.exit_code is not None
            drain(final=ended)
            if ended and record.exit_code < 0:
                print(f"The run of job {job_id} was ended by signal {-record.exit_code}.",
                      file=sys.stderr)
                return 1
            if ended:
                return int(record.exit_code)
            if _pid_alive(pid):
                gone_since = None
            elif gone_since is None:
                gone_since = time.monotonic()
            elif time.monotonic() - gone_since > END_GRACE_SECONDS:
                drain(final=True)
                print(f"The run of job {job_id} (process {pid}) ended, but the serve supervisor "
                      f"did not record how; see `remedy serve status` and `remedy job show "
                      f"{job_id}`.", file=sys.stderr)
                return 1
            time.sleep(poll)
    except KeyboardInterrupt:
        print(f"\nStopped following. The run of job {job_id} goes on in the serve supervisor; "
              f"stop it with `remedy job stop {job_id}`.", file=sys.stderr)
        return 1
    finally:
        for source, _stream in sources:
            source.close()
