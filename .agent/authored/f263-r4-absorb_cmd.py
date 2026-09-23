"""Handler for ``remedy absorb`` — absorb a hand edit into this repository's jobs (F263 T002).

After a human has worked on the repository by hand, the command captures its actual state,
certifies the deviation from each job's last known state as a human change record, and re-bases
the job onto it (DECISION F259 D1 names the command; DECISION D-E of T2_F263.md makes the
human's edit the authority). It goes through `human_change.absorb_job`, the one implementation
the run's own safe points use too. It writes no file in the repository.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from apps.cli.json_envelope import emit_ok, fail

if TYPE_CHECKING:
    import argparse
    from collections.abc import Callable

#: Jobs that will never run or apply again; their last known state is left where it is.
_ENDED = frozenset({"failed", "cancelled"})


def _repository_jobs(repo: Path, job_filter: str | None) -> list:
    from packages.orchestration.data_paths import job_record_paths
    from packages.orchestration.pingpong_job import load_job_plan

    jobs = []
    for record in job_record_paths():
        job = load_job_plan(record.parent.name)
        if job is None or not job.repo_path:
            continue
        if job_filter is not None and job.job_id != job_filter:
            continue
        try:
            same_repo = Path(job.repo_path).resolve() == repo
        except OSError:
            continue
        state = job.state.value if hasattr(job.state, "value") else str(job.state)
        if same_repo and state not in _ENDED:
            jobs.append(job)
    return jobs


def _cmd_absorb(*, repo: str = ".", job_filter: str | None = None,
                json_output: bool = False) -> None:
    """Absorb the repository's current state into each of its jobs. Exits 0 unless it cannot run."""
    from packages.orchestration import human_change as HC
    from packages.orchestration import worktrees as W
    from packages.orchestration.pingpong_job import job_worktree_id

    try:
        root = W.repo_root(repo)
    except (W.WorktreeError, OSError):
        fail("not_a_git_repository", f"{repo} is not inside a git repository.",
             json_output=json_output)
    jobs = _repository_jobs(root, job_filter)
    if job_filter is not None and not jobs:
        fail("job_not_found",
             f"No job {job_filter!r} of this repository can absorb a change. Try: remedy job list.",
             json_output=json_output)

    outcomes = []
    for job in jobs:
        if W.lock_is_held(root, job_worktree_id(job.job_id)):
            outcomes.append(HC.JobAbsorbOutcome(job_id=job.job_id, status="skipped_running"))
            continue
        try:
            outcomes.append(HC.absorb_job(job, detected_by="absorb"))
        except (HC.HumanChangeError, W.WorktreeError, OSError) as exc:
            fail("absorb_failed", f"job {job.job_id}: {exc}", json_output=json_output)

    rows = [{"job_id": o.job_id, "status": o.status,
             "record": o.record_path.name if o.record_path else None,
             "files": [{"path": f.path, "status": f.status} for f in o.files]}
            for o in outcomes]
    if json_output:
        emit_ok(repo=str(root), jobs=rows)
        return
    if not rows:
        print("No job of this repository holds a state to absorb into.")
        return
    words = {"absorbed": "absorbed", "unchanged": "nothing changed since its last known state",
             "skipped_running": "running now; not touched",
             "skipped_no_state": "holds no last known state; not touched"}
    for row in rows:
        line = f"job {row['job_id']}: {words[row['status']]}"
        if row["status"] == "absorbed":
            line += f" — {len(row['files'])} file(s), human change record {row['record']}"
        print(line)


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "absorb.run": lambda args: _cmd_absorb(
        repo=getattr(args, "repo", None) or ".",
        job_filter=getattr(args, "job", None),
        json_output=getattr(args, "json", False)),
}
