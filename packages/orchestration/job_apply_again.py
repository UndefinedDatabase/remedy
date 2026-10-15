"""A second apply of a job whose result already landed (amend1015 Phase 1.3, DECISION amend1015f D16).

The first apply changed the target, so a second apply of the same job finds the target changed
since the job's start and is blocked. Before this module it was refused as
`target_changed_during_run`, which tells a client that someone else changed the files; a client
that sends its apply again after a lost answer must instead read that its apply already landed.
`already_applied_refusal` names that case `job_already_applied`, the token `remedy job decline`
already answers for a landed result. An apply that the target allows still lands again, so a
result the person reverted by hand can be applied once more.

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
