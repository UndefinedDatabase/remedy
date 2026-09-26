"""`remedy job veto-task` — F027 T003, DECISION F027 D5.

Vetoes one task of a job so it, and every task that depends on it, will not run.
Modelled on `job_plan_cmd.py`: the task argument is resolved through
`job_plan_cmd._resolve_task_arg` exactly as `job edit-task` resolves it — the
task's own id or its unique id in the job plan, as `remedy job plan-show` prints
them. The write channel shares `task_veto.veto_task_command` with the write door
(`packages/orchestration/ui_server.py`), so the CLI and the browser answer
identically for the same request.

Exit codes follow the CLI contract (docs/guides/exit-codes.md): 2 when the
reason or the task argument is wrong — `reason_required`, `reason_too_long`,
`reason_invalid`, `unknown_task` — 3 when the job or the task is not in a state
that admits a veto — `job_not_vetoable`, `task_not_vetoable`,
`task_already_vetoed` — and 1, `fail()`'s own default, for a job that does not
exist.
"""
from __future__ import annotations

from apps.cli.job_id_arg import resolve_job_id_or_fail
from apps.cli.json_envelope import emit_ok, fail

EXIT_USAGE = 2
EXIT_NOT_READY = 3

#: The refusals that mean the arguments themselves were wrong.
_USAGE_CODES = frozenset({"reason_required", "reason_too_long", "reason_invalid", "unknown_task"})
#: The refusals that mean the job or the task cannot take a veto right now.
_NOT_READY_CODES = frozenset({"job_not_vetoable", "task_not_vetoable", "task_already_vetoed"})

#: Who the veto's audit line names for a veto made here; the write door names a
#: token fingerprint instead (DECISION F027 D5 (2)).
CLI_ACTOR = "cli"


def _cmd_veto_task(job_id_str: str, task_arg: str, *, reason: str = "",
                   json_output: bool = False) -> None:
    from apps.cli.commands.job_plan_cmd import _resolve_task_arg
    from packages.orchestration.pingpong_job import JobNotFoundError, require_job_plan
    from packages.orchestration.task_veto import veto_task_command

    job_id = resolve_job_id_or_fail(job_id_str, json_output=json_output)
    try:
        job = require_job_plan(job_id)
    except JobNotFoundError as exc:
        fail("job_not_found", str(exc), json_output=json_output)

    task_id = _resolve_task_arg(job, task_arg)
    result = veto_task_command(job, task_id=task_id, reason=reason, actor=CLI_ACTOR)

    if result["outcome"] == "refused":
        code = result["code"]
        refusal_exit = EXIT_USAGE if code in _USAGE_CODES else (
            EXIT_NOT_READY if code in _NOT_READY_CODES else 1)
        fail(code, result["detail"], json_output=json_output, exit_code=refusal_exit,
             job_id=job_id, task_id=result.get("task_id", task_id))
        return

    if json_output:
        emit_ok(job_id=job_id, **result)
        return

    unreachable = result.get("unreachable") or ()
    print(f"Task {result['task_id']} vetoed for job {job_id}.")
    print(f"  request: {result['request_id']}")
    if unreachable:
        print(f"  no longer reachable: {', '.join(unreachable)}")
    else:
        print("  no other task is lost.")


COMMAND_HANDLERS = {
    "job.veto-task": lambda args: _cmd_veto_task(
        getattr(args, "job_id", "") or "",
        getattr(args, "task", "") or "",
        reason=getattr(args, "reason", None) or "",
        json_output=bool(getattr(args, "json", False)),
    ),
}
