"""F328 (operator order beweis): an unattended job raises its call or token cap once by itself.

decodeux's order beweis: a job that runs unattended and reaches its cap of provider calls or tokens
extends once by itself to the next size, the doubled value the budget answer `extend` gives
(`budget_stop.doubled_limit_answers`), keeps that as an assumption in its story ("Remedy hat das
Budget einmal selbst erhöht, weil niemand da war"), and stops only at the second touch, with the
budget question extend or cancel. The time cap and the deadline always stop the job: they are
never raised here. A job whose metadata says `auto_extend: false` (the order's body
`auto_extend: false`, `remedy do --no-auto-extend`) stops at its first cap as before.

`should_stop_or_extend` is `safe_points.should_stop` with that one extension, and `run_job`'s
safe-point check calls it in place of `should_stop`.
"""
from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.orchestration import safe_points
from packages.orchestration.job_unattended import job_runs_unattended, record_unattended_assumption
from packages.orchestration.safe_points import ShouldStopResult

#: The job metadata key that switches the one extension off when it is False.
JOB_AUTO_EXTEND_KEY = "auto_extend"
#: The job metadata key recording the one extension: when, and each limit with its new value.
JOB_AUTO_EXTENDED_KEY = "budget_auto_extended"
#: The limits the extension raises; time and money are never raised by it.
AUTO_EXTENDED_LIMITS = ("max_provider_calls", "max_total_tokens")
#: The assumption the story shows, in his words.
AUTO_EXTEND_ASSUMPTION = "Remedy hat das Budget einmal selbst erhöht, weil niemand da war"


def auto_extend_allowed(job: Any) -> bool:
    """True when *job* runs unattended, does not switch the extension off and has not used it yet."""
    metadata = getattr(job, "metadata", None) or {}
    return (job_runs_unattended(job) is True and metadata.get(JOB_AUTO_EXTEND_KEY) is not False
            and not metadata.get(JOB_AUTO_EXTENDED_KEY))


def should_stop_or_extend(job_id: str, *, job: Any = None, budgets: Any | None = None,
                          counters: Any | None = None, now: datetime | None = None,
                          control_root_path: Path | None = None,
                          persist: Callable[[Any], Any] | None = None) -> ShouldStopResult:
    """`should_stop`, except that the first budget stop of an unattended JOB on its call or token cap
    doubles each such cap that is reached, in BUDGETS and in the job's own budgets, records the
    assumption and the extension on the job, saves the job with PERSIST (the job record writer by
    default, so a restart keeps the raised cap and never extends twice) and reads the safe point again."""
    def check() -> ShouldStopResult:
        return safe_points.should_stop(job_id, budgets=budgets, counters=counters, now=now,
                                       control_root_path=control_root_path)

    result = check()
    if job is None or budgets is None or not auto_extend_allowed(job):
        return result
    raised: dict[str, int] = {}
    while (result.should_stop and result.source == "budget" and result.budget_evaluation is not None
           and (limit := result.budget_evaluation.first_exhausted_limit) in AUTO_EXTENDED_LIMITS
           and limit not in raised and getattr(budgets, limit, None) is not None):
        raised[limit] = 2 * getattr(budgets, limit)
        setattr(budgets, limit, raised[limit])
        result = check()
    if raised:
        at = (now or datetime.now(timezone.utc)).isoformat()
        job.budgets = {**(job.budgets or {}), **raised}
        job.metadata[JOB_AUTO_EXTENDED_KEY] = {"at": at, **raised}
        record_unattended_assumption(
            job, "The job reached its " + " and ".join(name.removeprefix("max_").replace("_", " ")
                                                        for name in raised) + " cap. Raise it?",
            AUTO_EXTEND_ASSUMPTION, now=now)
        from packages.orchestration.pingpong_job import _persist_job

        (persist or _persist_job)(job)
    return result
