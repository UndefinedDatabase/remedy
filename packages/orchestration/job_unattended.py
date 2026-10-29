"""F324 — a job started unattended stays unattended, through run, resume, retry and continue.

decodeux, 2026-10-29: "das soll absolut autonom laufen und mich nicht wegen jedem scheiss immer
fragen und blockieren in remedy-chat". Before, only the walk of `remedy do run --run-unattended` knew
it ran unattended: the plan's approval audit recorded it, and a later `remedy job run`, a retry
over HTTP or a resume knew nothing of it. Now the choice is stored on the job
(`order_jobs.JOB_UNATTENDED_KEY` in its metadata, written by `do_targets.name_do_job` for an
unattended walk's jobs) and every run reads it there:

- a plan that waits for its approval is approved by the run itself, with the audit naming the
  unattended mode (`approve_unattended_plan`);
- a burn trip of a job with caps records its assumption and the job keeps running within its caps,
  instead of pausing with a question that has no default (`job_burn.record_burn_trip`);
- an order over HTTP runs unattended unless its body says `unattended: false`.

Only a question without a safe default waits, and it says why in one sentence. Remedy
deliberately never lifts a cap for an unattended job: a cap that is reached stops the job with
its reason.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from packages.orchestration.order_jobs import JOB_UNATTENDED_KEY

#: The job metadata key of the assumptions an unattended job made instead of asking.
JOB_ASSUMPTIONS_KEY = "unattended_assumptions"
#: The reason the audit of a plan an unattended run approved carries.
UNATTENDED_RUN_APPROVAL_REASON = "the job runs unattended, so its run approved its plan (F324)"


def job_runs_unattended(job: Any) -> bool | None:
    """True or False when *job* stores its choice, None when it stores none (a job planned before F324)."""
    value = (getattr(job, "metadata", None) or {}).get(JOB_UNATTENDED_KEY)
    return value if isinstance(value, bool) else None


def prepare_unattended_run(job_id: str, unattended: bool | None) -> None:
    """Before `remedy job run` refuses anything: store *unattended* on the job when it is given, and
    approve the plan an unattended job still waits on. A job with no record is left alone."""
    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan

    job = load_job_plan(job_id)
    if job is None:
        return
    if set_job_unattended(job, unattended):
        save_job_plan(job)
    approve_unattended_plan(job)


def set_job_unattended(job: Any, unattended: bool | None) -> bool:
    """Store *unattended* on *job* when it is given; True when the stored choice changed."""
    if unattended is None or job_runs_unattended(job) is unattended:
        return False
    job.metadata[JOB_UNATTENDED_KEY] = bool(unattended)
    return True


def approve_unattended_plan(job: Any) -> bool:
    """Approve and save the plan an unattended *job* still waits on; True when it approved one.

    The approval is the walk's own (`job_plan.auto_approve_task_plan`): every open clarification
    takes its documented default, written to the assumption log, and the audit names the mode.
    A rejected plan stays rejected: a person said no, and no default overrides that.
    """
    from packages.orchestration.data_paths import job_evidence_export_dir
    from packages.orchestration.job_plan import (
        AUTO_APPROVAL_MODE,
        announce_plan_approval,
        auto_approve_task_plan,
        task_plan_blocks_execution,
    )
    from packages.orchestration.pingpong_job import save_job_plan

    if job_runs_unattended(job) is not True or task_plan_blocks_execution(job) != "pending":
        return False
    job.task_plan = auto_approve_task_plan(job.task_plan, job_evidence_export_dir(str(job.job_id)),
                                           reason=UNATTENDED_RUN_APPROVAL_REASON)
    save_job_plan(job)
    announce_plan_approval(job, mode=AUTO_APPROVAL_MODE)
    return True


def job_has_caps(job: Any) -> bool:
    """True when *job* runs under at least one cap that stops it by itself."""
    budgets = getattr(job, "budgets", None)
    if budgets is None:
        return False
    names = ("max_total_tokens", "max_provider_calls", "max_wall_clock_minutes", "max_cost_usd", "deadline")
    values = budgets if isinstance(budgets, dict) else {name: getattr(budgets, name, None) for name in names}
    return any(values.get(name) not in (None, "", 0) for name in names)


def record_unattended_assumption(job: Any, question: str, assumed: str, *, now: datetime | None = None) -> dict[str, str]:
    """Keep on *job* what an unattended run assumed instead of asking; the caller saves the job."""
    entry = {"at": (now or datetime.now(timezone.utc)).isoformat(), "question": question, "assumed": assumed}
    job.metadata[JOB_ASSUMPTIONS_KEY] = [*list(job.metadata.get(JOB_ASSUMPTIONS_KEY) or []), entry]
    return entry
