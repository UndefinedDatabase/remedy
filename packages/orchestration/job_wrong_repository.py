"""F330 (operator order beweis): an unattended job whose work is not in its repository ends at once.

On 2026-10-29 job 44f5ec598488464c ran unattended in Remedy's own repository for an app error of
the Orb Remedy; its reviewer blocked the task with "this repository has no diff view" (finding
tzbwja-wrong-repo, high), no file changed, and the job then waited for a person who was not
there ("wartet auf dich"). The reviewer's finding now carries a `kind`, and a finding of kind
`not_in_this_repository` says the work does not belong in this repository.

`end_job_not_in_this_repository` reads a blocked job after its run: when it runs unattended, no
task of it changed a file, and the last review of a blocked task holds such a finding, the job
ends `failed`, a state that does not wait, with the stop reason `not_in_this_repository` and one
sentence naming the repository and why, so a client hands the task back. An attended job, and a
job that changed a file, keep the plain review path: they stay blocked for a person to judge.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

#: The finding kind and the stop reason: the work does not belong in this repository.
NOT_IN_THIS_REPOSITORY = "not_in_this_repository"
#: How much of the finding's summary the stop sentence quotes.
_WHY_CHARS = 240


def not_in_this_repository_finding(job: Any) -> tuple[Any, dict[str, Any]] | None:
    """The first blocked task of JOB whose last review holds a finding of kind
    `not_in_this_repository`, with that finding; None when there is none or no run can be read."""
    from packages.orchestration.pingpong_loop import load_run

    for task in getattr(job, "tasks", ()) or ():
        if str(getattr(task, "status", "")) != "blocked" or not getattr(task, "run_id", ""):
            continue
        try:
            run = load_run(task.run_id)
        except (OSError, ValueError):
            continue
        rounds = run.get("rounds") if isinstance(run, dict) else None
        last = rounds[-1] if isinstance(rounds, list) and rounds and isinstance(rounds[-1], dict) else {}
        reviewer = last.get("reviewer")
        for finding in (reviewer.get("findings") if isinstance(reviewer, dict) else None) or ():
            if isinstance(finding, dict) and finding.get("kind") == NOT_IN_THIS_REPOSITORY:
                return task, finding
    return None


def not_in_this_repository_text(job: Any, task: Any, finding: dict[str, Any]) -> str:
    """The stop sentence: the repository by name and path, the task, and the review's reason."""
    repo = str(getattr(job, "repo_path", "") or "")
    name = Path(repo).name or "this repository"
    why = " ".join(str(finding.get("summary") or "").split())[:_WHY_CHARS] or "the review gave no reason"
    return (f"Remedy ended the job without a change, because the review says the work of task "
            f"\"{getattr(task, 'title', '') or getattr(task, 'id', '')}\" does not belong in the repository "
            f"{name} ({repo}): {why}")


def end_job_not_in_this_repository(job: Any, *, now: datetime | None = None) -> bool:
    """End the blocked, unattended JOB `failed` with the stop reason `not_in_this_repository` when
    no task changed a file and a blocked task's last review says the work is not in this
    repository; True when it did. The caller saves the job."""
    from packages.orchestration.job_stop_text import JOB_STOP_TEXT_KEY
    from packages.orchestration.job_unattended import job_runs_unattended

    if str(getattr(job.state, "value", job.state)) != "blocked" or job_runs_unattended(job) is not True:
        return False
    if any(getattr(task, "safe_diff_files", None) for task in job.tasks):
        return False
    found = not_in_this_repository_finding(job)
    if found is None:
        return False
    from packages.core.models import RunState

    job.state = RunState.FAILED
    job.stop_reason = NOT_IN_THIS_REPOSITORY
    job.metadata[JOB_STOP_TEXT_KEY] = not_in_this_repository_text(job, *found)
    job.finished_at = job.finished_at or (now or datetime.now(timezone.utc)).isoformat()
    return True
