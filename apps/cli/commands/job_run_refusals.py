"""The refusals `remedy job run` gives before anything runs or is forwarded to a supervisor.

R-1317: a job whose task plan still waits for a person's approval or was rejected is refused
with the same token, sentence and exit code every other `remedy job` command already gives such
a job, so the approval a rehearsal leaves open cannot be bypassed by running the job directly
(DECISION F055 D3). `refuse_job_run_before_it_starts` is step (1) of `_cmd_job_run`'s boundary on
`docs/system/structure-ledger-v1.md` (DECISION F307 D22): every refusal before the run, in one
function that fails or returns.
"""

from __future__ import annotations

import sys
from typing import Any

from apps.cli.json_envelope import fail
from packages.orchestration.job_plan import task_plan_blocks_execution


# WHY: a rehearsed job's plan is left open for a person to approve or reject; running it
# directly must hit the same gate `remedy job` commands already enforce, never bypass it.
def refuse_unapproved_job_run(job: Any, job_id: str, *, json_output: bool) -> None:
    """Exit 3 when `job`'s task plan is pending approval or was rejected; otherwise return."""
    block_reason = task_plan_blocks_execution(job)
    if block_reason == "pending":
        fail(
            "plan_awaiting_approval",
            f"plan awaiting approval. Run: remedy decision resolve {job_id} plan:approval --reason approve",
            json_output=json_output, exit_code=3,
        )
    elif block_reason == "rejected":
        from apps.cli.commands.job import _plan_rejected_message
        fail("plan_rejected", _plan_rejected_message(job_id), json_output=json_output, exit_code=3)


# WHY: the refusals of `_cmd_job_run` before anything runs, moved verbatim as step (1) of its
# boundary, so that function keeps the flags, the run and the answer (DECISION F307 D22).
def refuse_job_run_before_it_starts(job_id: str, *, json_output: bool) -> Any:
    """The job's record, or None when this data root holds none, once no refusal applies.

    Fails `job_not_resumable` for a job whose recorded worktree cannot be continued and for a
    cancelled job, and `plan_awaiting_approval` or `plan_rejected` for a plan not approved; a
    rehearsal's staleness warning goes to standard error.
    """
    from packages.orchestration.pingpong_job import job_resume_refusal, load_job_plan

    # R-0913: a job whose recorded worktree cannot be continued is refused with
    # resume_job_plan's own words, before anything runs or the record is touched.
    _recorded = load_job_plan(job_id)
    _refusal = job_resume_refusal(_recorded) if _recorded is not None else ""
    if _refusal:
        fail("job_not_resumable", _refusal, json_output=json_output)

    # DECISION F295 D12 (3): a cancelled job never runs again, beside the
    # R-0913 refusal above and before anything runs or is forwarded.
    from packages.core.models import RunState
    if _recorded is not None and _recorded.state == RunState.CANCELLED:
        fail(
            "job_not_resumable",
            f"job {job_id} is cancelled and never runs again.",
            json_output=json_output,
        )
    if _recorded is not None:
        refuse_unapproved_job_run(_recorded, job_id, json_output=json_output)
        from packages.orchestration.do_rehearsal import rehearsal_staleness_warning
        if (warning := rehearsal_staleness_warning(_recorded)):
            print(warning, file=sys.stderr)
    return _recorded
