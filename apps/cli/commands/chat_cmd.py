"""Handler for ``remedy chat`` — send a steering message to a running job (F264 T001).

`remedy chat <job_id> "<message>"` hands one free-form sentence to the job. Nothing reaches
into a model call in flight: the message is written as a sealed record under the job's
evidence and certified into its run log, and the run reads it at its next safe point (T002).
The command goes through `steering.record_steering_message`, the one place a message is
accepted, which the cockpit's input field will use too. It writes no file in the repository.
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


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "chat.send": lambda args: _cmd_chat_send(
        getattr(args, "job_id", ""), getattr(args, "message", ""),
        json_output=getattr(args, "json", False)),
}
