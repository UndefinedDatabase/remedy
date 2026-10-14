"""R-1317 — `remedy job run` refuses, before anything runs or is forwarded to a supervisor, a
job whose task plan still waits for a person's approval or was rejected, with the same token,
sentence and exit code every other `remedy job` command already gives such a job, so the
approval a rehearsal leaves open cannot be bypassed by running the job directly (DECISION F055
D3).
"""

from __future__ import annotations

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
