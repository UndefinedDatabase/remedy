"""`remedy job rerun-subtree` — F029 T002, DECISION F029 D3.

Estimates what re-running a subtree will cost, shows that estimate through the
shared cost preview before anything is touched, and — once confirmed — prepares
the rerun with `subtree_rerun.prepare_subtree_rerun` (F029 T002, DECISION F029
D2). Modelled on `job_veto_cmd.py`: the same job-id resolution, the task
argument resolved through `job_plan_cmd._resolve_task_arg` exactly as `job
veto-task` resolves it, and the same usage/not-ready/other exit-code split
built from `SubtreeRerunRefused.code`. This command names no run and starts no
task itself — `remedy job run <job_id>` is what re-executes the pending subtree
this prepares.

Exit codes follow the CLI contract (docs/guides/exit-codes.md): 2 when the task
argument or the model override is wrong — `unknown_task`, `model_invalid` — 1
for a job that does not exist — `job_not_found` — and 3 for every other refusal
of the job's or the worktree's state — `job_running`, `job_not_rerunnable`,
`not_worktree_mode`, `task_not_committed`, `job_branch_missing`,
`checkpoint_object_missing`, `stream_archive_occupied`, `worktree_conflict`,
`worktree_drift`, `worktree_dirty`, `commit_not_on_branch`, `subtree_order` and
`interleaved`. A declined cost-preview confirmation exits 0 having changed
nothing; a non-interactive decline is `confirmation_required` at exit 2, raised
by the shared `confirm_cost_preview` helper itself.
"""
from __future__ import annotations

import sys
from typing import Any

from apps.cli.cost_preview_confirm import confirm_cost_preview
from apps.cli.job_id_arg import resolve_job_id_or_fail
from apps.cli.json_envelope import emit_ok, fail

EXIT_USAGE = 2
EXIT_NOT_READY = 3

#: The refusals that mean the arguments themselves were wrong.
_USAGE_CODES = frozenset({"unknown_task", "model_invalid"})

#: Who the rerun's audit line names for a request made here.
CLI_ACTOR = "cli"


def _refuse(exc: Any, *, job_id: str, task_id: str, json_output: bool) -> None:
    """Map one `SubtreeRerunRefused` onto the CLI contract's exit codes and envelope."""
    code = exc.code
    refusal_exit = (
        EXIT_USAGE if code in _USAGE_CODES else
        1 if code == "job_not_found" else
        EXIT_NOT_READY
    )
    fail(code, exc.detail, json_output=json_output, exit_code=refusal_exit,
         job_id=job_id, task_id=task_id, facts=exc.facts)


def _print_prepared(job_id: str, record: dict, run_command: str) -> None:
    n = len(record["subtree"]) - 1
    print(
        f"Rerun {record['rerun_id']} prepared for job {job_id}: task "
        f"{record['root_task_id']} and {n} dependent task{'' if n == 1 else 's'} reset."
    )
    print(f"  reset commit: {record['reset_commit'][:12]}")
    paths = record["paths"]
    print(f"  files put back: {', '.join(paths) if paths else 'no file changed'}")
    print(f"  tasks returned to pending: {', '.join(record['subtree'])}")
    model = record["model"]
    if model["override"]:
        print(f"  model: {model['override']} (configured: {model['configured'] or 'none'})")
    print(f"Run it with: {run_command}")


def _cmd_rerun_subtree(job_id_str: str, task_arg: str, *, model: str = "",
                       yes: bool = False, json_output: bool = False) -> None:
    from apps.cli.commands.job_plan_cmd import _resolve_task_arg
    from packages.orchestration import subtree_rerun as SR
    from packages.orchestration.budget_resolution import resolve_predictive_budget_config
    from packages.orchestration.cost_preview import resolve_confirm_above_usd
    from packages.orchestration.pingpong_job import JobNotFoundError, require_job_plan

    job_id = resolve_job_id_or_fail(job_id_str, json_output=json_output)
    try:
        job = require_job_plan(job_id)
    except JobNotFoundError as exc:
        fail("job_not_found", str(exc), json_output=json_output)

    task_id = _resolve_task_arg(job, task_arg)

    try:
        subtree_ids = SR.rerun_subtree_ids(job.tasks, task_id)
    except SR.SubtreeRerunRefused as exc:
        _refuse(exc, job_id=job_id, task_id=task_id, json_output=json_output)
        return

    config = resolve_predictive_budget_config(project_root=job.repo_path or None)
    estimate = SR.subtree_rerun_cost_estimate(job, subtree_ids, config=config)

    proceed = confirm_cost_preview(
        estimate, confirm_above_usd=resolve_confirm_above_usd(), yes=yes,
        command_name="job.rerun-subtree", json_output=json_output)
    if not proceed:
        print("Cancelled. Nothing was changed.", file=sys.stderr if json_output else sys.stdout)
        if json_output:
            emit_ok(job_id=job_id, cancelled=True)
        return

    try:
        record = SR.prepare_subtree_rerun(
            job_id, task_id, model_override=model, actor=CLI_ACTOR)
    except SR.SubtreeRerunRefused as exc:
        _refuse(exc, job_id=job_id, task_id=task_id, json_output=json_output)
        return

    run_command = f"remedy job run {job_id}"
    if json_output:
        emit_ok(**record, estimate={
            "band_usd_low": estimate.band_usd_low,
            "band_usd_high": estimate.band_usd_high,
            "basis": estimate.basis,
        }, run_command=run_command)
        return
    _print_prepared(job_id, record, run_command)


COMMAND_HANDLERS = {
    "job.rerun-subtree": lambda args: _cmd_rerun_subtree(
        getattr(args, "job_id", "") or "",
        getattr(args, "task", "") or "",
        model=getattr(args, "model", None) or "",
        yes=bool(getattr(args, "yes", False)),
        json_output=bool(getattr(args, "json", False)),
    ),
}
