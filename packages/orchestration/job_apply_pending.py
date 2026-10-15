"""amend1015 Part 1.3: whether a finished job's result still waits to be applied, and the one command.

``remedy do`` stops before apply unless ``--apply``: its task ends ``applied_to_job_workspace``,
which means the result sits in the job's own workspace and the target repository is untouched.
The run report's ``apply-pending`` rule names the command that moves it there, spelled by
``job_apply_command`` — the same function ``do_apply.py`` prints its ``Next:`` line with, so the
cockpit and the terminal can never spell it two ways.

Public API::

    job_apply_command(job_id, repo_path) -> str
    job_apply_pending_fields(job) -> dict
"""

from __future__ import annotations

import shlex
from typing import Any

#: The task status that means "the result is in the job workspace, not yet in the target".
TASK_STATUS_IN_JOB_WORKSPACE = "applied_to_job_workspace"


# The one spelling of the command that applies a job's reviewed result to its target repository.
def job_apply_command(job_id: str, repo_path: str) -> str:
    """``remedy job apply <job_id> --repo <repo_path> --approve``, the repository shell-quoted."""
    return f"remedy job apply {job_id} --repo {shlex.quote(repo_path)} --approve"


def job_apply_pending_fields(job: Any) -> dict[str, Any]:
    """``{"repo_path", "result_applied"}`` for the run report's sources.

    ``result_applied`` is None (not recorded) unless a task of *job* left its result in the job
    workspace; then it is whether an apply record reads ``applied``
    (``job_apply.job_apply_landed``, the client digest's own reader). A result the operator
    declined is not pending either, so it reads None. Never raises: an unreadable record store
    leaves both fields at their absent values.
    """
    repo_path = str(getattr(job, "repo_path", "") or "")
    statuses = {str(getattr(t, "status", "") or "") for t in getattr(job, "tasks", ()) or ()}
    if TASK_STATUS_IN_JOB_WORKSPACE not in statuses:
        return {"repo_path": repo_path, "result_applied": None}
    try:
        from packages.orchestration.job_apply import job_apply_landed, job_result_decline

        if job_result_decline(job) is not None:
            return {"repo_path": repo_path, "result_applied": None}
        applied = job_apply_landed(str(getattr(job, "job_id", "") or ""))
    except (ImportError, OSError, ValueError):
        return {"repo_path": repo_path, "result_applied": None}
    return {"repo_path": repo_path, "result_applied": applied}
