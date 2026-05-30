"""Repo group command handlers."""

from __future__ import annotations

import hashlib
import json as _json
import sys
from typing import TYPE_CHECKING, Callable
from uuid import UUID

if TYPE_CHECKING:
    import argparse


def _cmd_repo_status(
    job_id_str: str | None = None,
    *,
    path: str | None = None,
    json_output: bool = False,
) -> None:
    from packages.orchestration.git_status import (
        export_git_status_json,
        read_git_status,
        summarize_git_status,
    )

    repo_path: str | None = path

    # Job-aware: load target_repo from job metadata
    job = None
    if job_id_str:
        from packages.orchestration.storage import JobNotFoundError, load_job
        try:
            job_id = UUID(job_id_str)
        except ValueError:
            print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
            sys.exit(1)
        try:
            job = load_job(job_id)
        except JobNotFoundError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
        if not repo_path:
            repo_path = (job.metadata or {}).get("target_repo", "")
            if not repo_path:
                print("Error: job has no target_repo attached", file=sys.stderr)
                sys.exit(1)

    if not repo_path:
        repo_path = "."

    status = read_git_status(repo_path)

    # Emit run-log event when job-aware
    if job is not None:
        from packages.orchestration.run_log import RunLogWriter
        changed = len(status.modified_files) + len(status.untracked_files) + len(status.staged_files)
        raw = f"{status.current_branch}:{status.head_sha}:{status.is_clean}:{changed}"
        status_hash = hashlib.sha256(raw.encode()).hexdigest()[:16]
        log = RunLogWriter(job_id=job.id)
        log.log(
            "git_status_read",
            outcome="clean" if status.is_clean else "dirty",
            is_git_repo=status.is_git_repo,
            git_available=status.is_git_repo,
            branch=status.current_branch,
            head_sha=status.head_sha,
            dirty=not status.is_clean,
            changed_file_count=changed,
            status_hash=status_hash,
        )

    if json_output:
        print(_json.dumps(export_git_status_json(status), sort_keys=True))
    else:
        print(summarize_git_status(status))


def _cmd_commit_readiness(
    job_id_str: str,
    *,
    json_output: bool = False,
) -> None:
    """Preview commit readiness — read-only, no git writes."""
    from packages.orchestration.storage import load_job
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.timeline import load_run_events
    from packages.orchestration.git_status import read_git_status

    try:
        job = load_job(UUID(job_id_str))
    except Exception:
        print(f"Error: job not found: {job_id_str}", file=sys.stderr)
        sys.exit(1)

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job.id)
    repo_path = (job.metadata or {}).get("repo_path", ".")
    git = read_git_status(repo_path)

    # Tests passed?
    tests_passed = False
    for e in reversed(events):
        if e.get("event") == "test_run_completed":
            tests_passed = e.get("metadata", {}).get("exit_code") == 0
            break

    # Proof present?
    proof_present = any(e.get("event") == "proof_collected" for e in events)

    # Revert available?
    revert_available = any(e.get("event") == "source_patch_applied" for e in events)

    # Changed files (from git)
    changed_files = sorted(set(
        git.modified_files + git.staged_files + git.untracked_files
    ))

    # Reasons for not ready
    reasons = []
    if not git.is_git_repo:
        reasons.append("not a git repository")
    if not changed_files:
        reasons.append("no changed files detected")
    if not tests_passed:
        reasons.append("tests not passed after apply")
    if not proof_present:
        reasons.append("no proof collected")
    if not revert_available:
        reasons.append("no revert snapshot available")

    ready = len(reasons) == 0

    # Suggested commit message
    short_id = str(job.id)[:8]
    task_summary = ""
    if job.tasks:
        types = [t.task_type for t in job.tasks[:3]]
        task_summary = ", ".join(types)
    suggested = f"remedy/{short_id}: {task_summary or job.name}"

    result = {
        "version": 1,
        "job_id": str(job.id),
        "repo_path": str(repo_path),
        "ready": ready,
        "reasons": reasons,
        "changed_files": changed_files[:50],
        "tests_passed": tests_passed,
        "proof_present": proof_present,
        "revert_available": revert_available,
        "suggested_commit_message": suggested,
    }

    if json_output:
        print(_json.dumps(result, indent=2))
    else:
        mark = "READY" if ready else "NOT READY"
        print(f"Commit readiness: {mark}")
        print(f"  Job: {str(job.id)[:8]} ({job.name})")
        print(f"  Repo: {repo_path}")
        print(f"  Tests passed: {tests_passed}")
        print(f"  Proof present: {proof_present}")
        print(f"  Revert available: {revert_available}")
        print(f"  Changed files: {len(changed_files)}")
        if reasons:
            print("  Issues:")
            for r in reasons:
                print(f"    - {r}")
        if ready:
            print(f"  Suggested: {suggested}")
        print()
        print("Note: This is read-only. No git add/commit/push.")


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "repo.status": lambda args: _cmd_repo_status(
        getattr(args, "job_id", None),
        path=getattr(args, "path", None),
        json_output=getattr(args, "json", False),
    ),
    "repo.commit-readiness": lambda args: _cmd_commit_readiness(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),
}
