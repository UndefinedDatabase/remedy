"""A second apply of a job whose result already landed (amend1015 Phase 1.3, DECISION amend1015f D16).

The first apply changed the target, so a second apply of the same job finds the target changed
since the job's start and is blocked. Before this module it was refused as
`target_changed_during_run`, which tells a client that someone else changed the files; a client
that sends its apply again after a lost answer must instead read that its apply already landed.
`already_applied_refusal` names that case `job_already_applied`, the token `remedy job decline`
already answers for a landed result. An apply that the target allows still lands again, so a
result the person reverted by hand can be applied once more.

`job_not_ready_reason` (DECISION amend1015c D9) is the apply's first readiness gate: a job that
is not completed, or whose result was declined, is not ready, because a decline is final.

This module reads apply records only; it never applies, saves or changes anything.
"""

from __future__ import annotations

from typing import Any

JOB_ALREADY_APPLIED = "job_already_applied"


def already_applied_refusal(result: Any) -> tuple[str, str] | None:
    """`(job_already_applied, sentence)` when RESULT, an apply blocked because the target changed,
    is of a job an earlier apply record of which reads `applied`; else None."""
    from packages.orchestration.job_apply import job_apply_landed

    job_id = str(getattr(result, "job_id", "") or "")
    if not job_id or not job_apply_landed(job_id):
        return None
    return JOB_ALREADY_APPLIED, (
        f"Job {job_id}'s result is already applied; the target holds that apply's change, so "
        "nothing was applied again.")


def job_not_ready_reason(job: Any, completed: str) -> str | None:
    """The blocked reason of a JOB that may not be applied yet or ever: `job_not_completed` while
    its state is not COMPLETED, `job_declined` once its result was declined; else None."""
    from packages.orchestration.job_apply import job_result_decline

    if job.state != completed:
        return f"job_not_completed: status={job.state}"
    declined = job_result_decline(job)
    if declined is not None:
        return f"job_declined: at={declined.get('declined_at', '')}"
    return None
