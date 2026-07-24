"""
Project-scoped job listing (F148).

Provides a scope selector (project + flags), a predicate (job_in_scope),
and the single listing helper (scoped_jobs) every command uses.

Legacy rule: jobs with project_id=None are in scope only under
--all-projects OR when exactly one project exists on the machine.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from packages.core.models import Job


@dataclass(frozen=True)
class ProjectScope:
    """Resolved scope for job listing."""

    project_id: str | None
    all_projects: bool
    source: str


def resolve_scope(
    *,
    project_flag: str | None = None,
    all_projects: bool = False,
    cwd: str = ".",
) -> ProjectScope:
    """Build a scope from CLI flags and environment.

    Precedence (matches select_project from F146):
      1. --all-projects → show everything
      2. --project flag → that specific project
      3. REMEDY_PROJECT env → that specific project
      4. cwd autodetection
      5. fallback: all_projects (no project resolvable)
    """
    if all_projects:
        return ProjectScope(project_id=None, all_projects=True, source="flag")

    from packages.orchestration.project_registry import (
        ProjectNotFoundError,
        select_project,
    )

    try:
        project, source = select_project(project_flag, cwd)
        return ProjectScope(
            project_id=str(project.id),
            all_projects=False,
            source=source,
        )
    except ProjectNotFoundError:
        return ProjectScope(project_id=None, all_projects=True, source="fallback")


def _project_count() -> int:
    """Return number of registered projects (read-only)."""
    from packages.orchestration.project_registry import _list_projects_readonly

    return len(_list_projects_readonly())


def job_in_scope(
    job: Job,
    scope: ProjectScope,
    *,
    _legacy_visible: bool | None = None,
) -> bool:
    """Return True if *job* is visible under *scope*.

    Legacy rule: jobs with project_id=None are in scope only under
    --all-projects OR when exactly one project exists on the machine.

    ``_legacy_visible`` is a precomputed override for the legacy check,
    used by :func:`scoped_jobs` to avoid per-job registry reads.
    """
    if scope.all_projects:
        return True

    if job.project_id is None:
        if _legacy_visible is not None:
            return _legacy_visible
        return _project_count() <= 1

    if scope.project_id is None:
        return True

    return job.project_id == scope.project_id


def scoped_jobs(
    scope: ProjectScope,
    *,
    root: Path | None = None,
) -> tuple[list[Job], bool, list[str]]:
    """Return jobs visible under *scope*.

    Returns ``(jobs, degraded, skipped_files)`` — same shape as
    ``storage.list_jobs_safe`` with the unreadable-files honesty count
    passed through.
    """
    from packages.orchestration.storage import list_jobs_safe

    all_jobs, degraded, skipped = list_jobs_safe(root)
    legacy_visible = scope.all_projects or _project_count() <= 1
    filtered = [
        j for j in all_jobs
        if job_in_scope(j, scope, _legacy_visible=legacy_visible)
    ]
    return filtered, degraded, skipped
