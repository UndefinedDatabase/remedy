"""Handler for ``remedy chat`` — send a steering message to a running job (F264 T001).

`remedy chat <job_id> "<message>"` hands one free-form sentence to the job. Nothing reaches
into a model call in flight: the message is written as a sealed record under the job's
evidence and certified into its run log, and the run reads it at its next safe point (T002).
The command goes through `steering.record_steering_message`, the one place a message is
accepted, which the cockpit's input field uses too. It writes no file in the repository.

`remedy chat show <job_id>` (T003) lists the job's messages with each acknowledgement — the task
round that took it in and what was understood — read from the same run-log events the cockpit's
stream carries, and says plainly when a message is still waiting or was never taken in.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from apps.cli.json_envelope import emit_ok, fail

if TYPE_CHECKING:
    import argparse
    from collections.abc import Callable

#: The contract's exit code for a job whose record is unreadable or which has ended
#: (DECISION F283 D12): the invocation is well formed, the job cannot take a message.
EXIT_NOT_READY = 3


def _cmd_chat_send(job_id: str, message: str, *, json_output: bool = False) -> None:
    """Record ``message`` for the job. Exits 2 on an unusable message, 3 on an ended job."""
    from apps.cli.job_id_arg import resolve_job_id_or_fail
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.steering import (
        SteeringError,
        SteeringWriteError,
        normalize_steering_text,
        record_steering_message,
    )

    try:
        normalize_steering_text(message)
    except SteeringError as exc:
        fail("invalid_message", f"The message was not sent: {exc}.", json_output=json_output,
             exit_code=2)
    full_id = resolve_job_id_or_fail((job_id or "").strip(), json_output=json_output,
                                     job_id=job_id)
    job = load_job_plan(full_id)
    if job is None:
        fail("job_not_found", f"The record of job {full_id} cannot be read.",
             json_output=json_output, exit_code=EXIT_NOT_READY, job_id=full_id)
    state = job.state.value if hasattr(job.state, "value") else str(job.state)
    try:
        record = record_steering_message(job.job_id, message, job_state=state, channel="cli")
    except SteeringWriteError as exc:
        fail("steering_write_failed", f"The message could not be recorded: {exc}.",
             json_output=json_output, job_id=job.job_id)
    except SteeringError as exc:
        fail("job_not_steerable", f"The message was not sent: {exc}.",
             json_output=json_output, exit_code=EXIT_NOT_READY, job_id=job.job_id)

    if json_output:
        emit_ok(job_id=job.job_id, message_id=record["message_id"],
                received_at=record["received_at"], record_sha256=record["record_sha256"])
        return
    print(f"Message {record['message_id']} recorded for job {job.job_id}.")
    print("The job reads it at its next safe point; nothing interrupts a model call in flight.")


#: What each status says to the operator, in plain words (T003, DECISION F264 D6).
_STATUS_WORDS = {
    "waiting": "waiting — the job has not reached a safe point since it arrived",
    "not_taken_in": "not taken in — the job ended before it reached another round",
}


def _cmd_chat_show(job_id: str, *, json_output: bool = False) -> None:
    """List the job's steering messages with each acknowledgement. Exits 3 on an unreadable job."""
    from apps.cli.job_id_arg import resolve_job_id_or_fail
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.steering import SteeringError, steering_overview

    full_id = resolve_job_id_or_fail((job_id or "").strip(), json_output=json_output,
                                     job_id=job_id)
    job = load_job_plan(full_id)
    if job is None:
        fail("job_not_found", f"The record of job {full_id} cannot be read.",
             json_output=json_output, exit_code=EXIT_NOT_READY, job_id=full_id)
    state = job.state.value if hasattr(job.state, "value") else str(job.state)
    try:
        rows = steering_overview(job.job_id, state)
    except SteeringError as exc:
        fail("steering_record_damaged", f"The job's steering records cannot be trusted: {exc}.",
             json_output=json_output, job_id=job.job_id)

    if json_output:
        emit_ok(job_id=job.job_id, job_status=state, messages=rows)
        return
    if not rows:
        print(f"Job {job.job_id} has no steering messages.")
        return
    print(f"Job {job.job_id} — {state}")
    for row in rows:
        print(f"{row['message_id']}  {row['received_at']}  via {row['channel']}: {row['text']}")
        if row["status"] == "acknowledged":
            print(f"  taken in at round {row['round_number']} of task {row['task_id']}: "
                  f"{row['understood']}")
        else:
            print(f"  {_STATUS_WORDS[row['status']]}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "chat.send": lambda args: _cmd_chat_send(
        getattr(args, "job_id", ""), getattr(args, "message", ""),
        json_output=getattr(args, "json", False)),
    "chat.show": lambda args: _cmd_chat_show(
        getattr(args, "job_id", ""), json_output=getattr(args, "json", False)),
}
