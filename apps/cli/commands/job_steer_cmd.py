"""`remedy job steer` — F030 T002, DECISION F030 D2; `--source`, DECISION F303 D2 (2), D3 (2).

Addresses one steering note to a single task of a running job: the write channel and the
command line share `steering.steer_task_command`, which refuses an unusable text, an ended
job, a task the job does not hold and a task that will not run again, in that order, and
otherwise records the note through `steering.record_steering_message` with the task's id.
The task argument is resolved through `job_plan_cmd._resolve_task_arg` exactly as `job
veto-task` resolves it — the task's own id or its unique id in the job plan, as `remedy job
plan-show` prints them.

`--source` names the door the note came through, kept with the record as its channel
(default `cli`); a value outside `steering.STEERING_CHANNELS` is refused before the job id is
even resolved. `job.steer` is a client operation (DECISION F303 D3 (2)): its answer keys,
answer tree and refusal tokens are `JOB_STEER_ANSWER_KEYS`, `JOB_STEER_ANSWER_TREE` and
`JOB_STEER_REFUSAL_TOKENS`, read by `apps/cli/client_interface.py` as `job.stop`'s are.

Exit codes follow the CLI contract (docs/guides/exit-codes.md): 2 when an argument is wrong —
`invalid_argument` for an unknown `--source`, `invalid_message` for the note, `unknown_task`
for the task — 3 when the job or the task is not in a state that admits a note —
`job_not_steerable`, `task_not_steerable` — or when the job record cannot be read, and 1 —
`fail()`'s own default — for a note that could not be written (`steering_write_failed`).
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from apps.cli.job_id_arg import resolve_job_id_or_fail
from apps.cli.json_envelope import emit_ok, fail

if TYPE_CHECKING:
    import argparse
    from collections.abc import Callable

EXIT_USAGE = 2
EXIT_NOT_READY = 3

#: The refusals that mean the arguments themselves were wrong.
_USAGE_CODES = frozenset({"invalid_message", "unknown_task"})
#: The refusals that mean the job or the task cannot take a note right now.
_NOT_READY_CODES = frozenset({"job_not_steerable", "task_not_steerable"})

#: The refusal tokens and answer keys this command can reach, as the machine client interface
#: declares them (DECISION F303 D3 (2)).
JOB_STEER_REFUSAL_TOKENS = (
    "ambiguous_job_id", "invalid_argument", "invalid_job_id", "invalid_message", "job_not_found",
    "job_not_steerable", "steering_write_failed", "task_not_steerable", "unknown_task",
)
JOB_STEER_ANSWER_KEYS = ("job_id", "matches", "message_id", "received_at", "record_sha256",
                        "request_id", "task_id")
#: No key of the accepted answer holds further keys, unlike `job.stop`'s `stop`/`pending`/`archived`.
JOB_STEER_ANSWER_TREE: dict = {}


def _cmd_job_steer(job_id_str: str, task_arg: str, text: str, *, source: str = "cli",
                   json_output: bool = False) -> None:
    from apps.cli.commands.job_plan_cmd import _resolve_task_arg
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.steering import STEERING_CHANNELS, SteeringWriteError, steer_task_command

    if source not in STEERING_CHANNELS:
        fail("invalid_argument",
             f"The source {source!r} is not one of {', '.join(sorted(STEERING_CHANNELS))}.",
             json_output=json_output, exit_code=EXIT_USAGE)

    job_id = resolve_job_id_or_fail(job_id_str, json_output=json_output)
    job = load_job_plan(job_id)
    if job is None:
        fail("job_not_found", f"The record of job {job_id} cannot be read.",
             json_output=json_output, exit_code=EXIT_NOT_READY, job_id=job_id)

    task_id = _resolve_task_arg(job, task_arg)
    try:
        result = steer_task_command(job, task_id, text, channel=source)
    except SteeringWriteError as exc:
        fail("steering_write_failed", f"The note could not be recorded: {exc}.",
             json_output=json_output, job_id=job_id, task_id=task_id)
        return

    if result["outcome"] == "refused":
        code = result["code"]
        refusal_exit = EXIT_USAGE if code in _USAGE_CODES else (
            EXIT_NOT_READY if code in _NOT_READY_CODES else 1)
        fail(code, f"The note was not sent: {result['detail']}.", json_output=json_output,
             exit_code=refusal_exit, job_id=job_id, task_id=result.get("task_id", task_id))
        return

    if json_output:
        emit_ok(job_id=job_id, **result)
        return
    print(f"Note {result['message_id']} recorded for task {result['task_id']} of job {job_id}.")
    print(f"Task {result['task_id']} reads it at the start of its next round; nothing "
          "interrupts a model call in flight.")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "job.steer": lambda args: _cmd_job_steer(
        getattr(args, "job_id", "") or "",
        getattr(args, "task", "") or "",
        getattr(args, "text", "") or "",
        source=getattr(args, "source", "cli") or "cli",
        json_output=bool(getattr(args, "json", False)),
    ),
}
