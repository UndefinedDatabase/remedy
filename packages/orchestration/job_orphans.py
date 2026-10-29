"""F331 (operator order beweis): no job stays `running` with nothing running it.

On 2026-10-29 job d1a8b318952f4b04 read `running` („läuft“ in the app) for hours after the order
walk that ran it had ended: a walk runs its jobs in its own process, so such a job has no run record
of its own, and the supervisor's start resumed only runs it had a record of
(`RunLauncher.resume_registered`) and ended only jobs under a cancel request
(`serve_runs.settle_orphaned_job_cancels`).

`settle_orphaned_running_jobs` runs when the supervisor starts, after the first, and settles the
cancels of the second first. Each job that reads
`running`, holds no cancel request and that no process the supervisor started can still run
(`serve_runs.job_runner_alive`) is either

* resumed, when it runs unattended, its order is still live (the supervisor has its order and no
  cancel of that order) and it is within its caps (`budget_stop.job_within_caps`): its run starts
  as `POST /api/v1/jobs/{job}/run` would start it;
* or ended `stopped` with the stop reason `orphaned_after_restart` and one sentence why, so a
  person or a client resumes or drops it. A resume that cannot start ends it the same way.

A job no supervisor process ever ran (no run record and no order) may be held by a run in a
terminal, so it is left alone, as `job_runner_alive` says.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

#: The stop reason of a job whose runner was gone when the supervisor started.
ORPHANED_AFTER_RESTART = "orphaned_after_restart"


def _order_live(paths: Any, job_id: str) -> bool:
    from packages.orchestration.order_cancel import order_cancel_request
    from packages.orchestration.serve_runs import order_record_for_job

    record = order_record_for_job(paths, job_id)
    return record is not None and order_cancel_request(paths.orders_dir / record.order_id) is None


def orphan_stop_text(job: Any, why: str) -> str:
    """The stop sentence of an orphaned job: that nothing ran it after the restart, and WHY it was not resumed."""
    return (f"Remedy found job {job.job_id} running with nothing left to run it after the server started "
            f"again, and stopped it because {why}; `remedy job resume {job.job_id}` continues it.")


def end_orphaned_job(job: Any, why: str, *, now: datetime | None = None) -> None:
    """End JOB `stopped` with the stop reason `orphaned_after_restart` and the sentence WHY, and save it."""
    from packages.orchestration.job_stop_text import JOB_STOP_TEXT_KEY
    from packages.orchestration.pingpong_job import JOB_STOPPED, save_job_plan

    at = (now or datetime.now(timezone.utc)).isoformat()
    job.state, job.stop_reason, job.stop_source, job.stopped_at = JOB_STOPPED, ORPHANED_AFTER_RESTART, "supervisor", at
    job.metadata[JOB_STOP_TEXT_KEY] = orphan_stop_text(job, why)
    save_job_plan(job)


def orphan_resume_refusal(paths: Any, job: Any, *, now: datetime | None = None) -> str:
    """Why the orphaned JOB is not resumed, or "" when it may be: unattended, its order live, within its caps."""
    from packages.orchestration.budget_stop import job_within_caps
    from packages.orchestration.job_unattended import job_runs_unattended

    if job_runs_unattended(job) is not True:
        return "it does not run unattended, so a person decides"
    if not _order_live(paths, str(job.job_id)):
        return "its order is no longer live"
    if not job_within_caps(job, now=now):
        return "it has reached its caps"
    return ""


def settle_orphaned_running_jobs(paths: Any, launcher: Any, *, now: datetime | None = None) -> list[dict[str, str]]:
    """Resume or end each `running` job no process runs; one `{"job_id", "action"}` per job, the action
    `resumed` or `stopped`. One job's failure never stops another's. The jobs under a cancel request
    are settled first (`serve_runs.settle_orphaned_job_cancels`, R-1365), so none of them is resumed."""
    from packages.orchestration.job_cancel import job_cancel_request
    from packages.orchestration.pingpong_job import JOB_RUNNING, list_job_plans_safe
    from packages.orchestration.safe_points import StopControlError
    from packages.orchestration.serve_runs import job_runner_alive, settle_orphaned_job_cancels

    settle_orphaned_job_cancels(paths)
    outcomes: list[dict[str, str]] = []
    plans, _degraded, _skipped = list_job_plans_safe()
    for job in plans:
        job_id = str(job.job_id)
        try:
            if job.state != JOB_RUNNING or job_cancel_request(job_id) is not None or job_runner_alive(paths, job_id):
                continue
            why = orphan_resume_refusal(paths, job, now=now)
            if not why:
                try:
                    launcher.start(job_id)
                except Exception as exc:  # noqa: BLE001 — any refusal of the start ends the job instead
                    why = f"its run could not start again ({type(exc).__name__})"
                else:
                    outcomes.append({"job_id": job_id, "action": "resumed"})
                    continue
            end_orphaned_job(job, why, now=now)
            outcomes.append({"job_id": job_id, "action": "stopped"})
        except (OSError, StopControlError, ValueError):
            continue                    # its record or control area cannot be read or written now
    return outcomes
