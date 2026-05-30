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


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "repo.status": lambda args: _cmd_repo_status(
        getattr(args, "job_id", None),
        path=getattr(args, "path", None),
        json_output=getattr(args, "json", False),
    ),
}
