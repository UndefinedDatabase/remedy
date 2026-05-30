"""
Project Registry v0 — minimal project metadata store.

Projects represent a named scope containing one or more repos and jobs.
They are the foundation for the future multi-job, multi-repo brain hierarchy:
  Global Brain → Project Brain → Repo Brain → Job Brain.

This module is read-only at the data layer except for creation and linking
operations.  No repo scanning. No artifact content. No approval reasons.
No diff previews. No event messages.

Public API::

    RemyProject                                    -- Pydantic model
    ProjectNotFoundError                           -- raised on missing project
    save_project(project) -> None
    load_project(project_id: UUID) -> RemyProject
    list_projects() -> list[RemyProject]
    attach_repo(project, repo_path) -> bool        # True if added (idempotent)
    attach_job(project, job_id_str) -> bool        # True if added (idempotent)
    summarize_project(project, jobs) -> str
    export_project_json(project, jobs) -> dict
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from packages.orchestration.data_paths import projects_dir as _projects_dir


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


class RemyProject(BaseModel):
    """Minimal project metadata — name, attached repos, and linked job IDs."""

    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str | None = None
    created_at: datetime = Field(default_factory=_utcnow)
    repo_paths: list[str] = Field(default_factory=list)
    job_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------


class ProjectNotFoundError(Exception):
    """Raised when a requested project cannot be found in storage."""

    def __init__(self, project_id: UUID) -> None:
        super().__init__(f"Project not found: {project_id}")
        self.project_id = project_id


def save_project(project: RemyProject) -> None:
    """Persist a RemyProject to disk as JSON."""
    d = _projects_dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{project.id}.json").write_text(project.model_dump_json(indent=2))


def load_project(project_id: UUID) -> RemyProject:
    """Load a RemyProject from disk by ID.

    Raises ProjectNotFoundError if the project does not exist.
    """
    path = _projects_dir() / f"{project_id}.json"
    if not path.exists():
        raise ProjectNotFoundError(project_id)
    return RemyProject.model_validate_json(path.read_text())


def list_projects() -> list[RemyProject]:
    """Return all persisted projects sorted by created_at descending."""
    d = _projects_dir()
    if not d.exists():
        return []
    projects: list[RemyProject] = []
    for path in d.glob("*.json"):
        try:
            projects.append(RemyProject.model_validate_json(path.read_text()))
        except (ValueError, OSError):
            pass
    return sorted(projects, key=lambda p: p.created_at, reverse=True)


# ---------------------------------------------------------------------------
# Linking helpers
# ---------------------------------------------------------------------------


def attach_repo(project: RemyProject, repo_path: str) -> bool:
    """Add the resolved repo_path to project.repo_paths if not already present.

    Returns True if the path was added; False if already present (idempotent).
    Does not scan or access the repository.
    """
    resolved = str(Path(repo_path).resolve())
    if resolved in project.repo_paths:
        return False
    project.repo_paths.append(resolved)
    return True


def attach_job(project: RemyProject, job_id_str: str) -> bool:
    """Add job_id_str to project.job_ids if not already present.

    Returns True if added; False if already present (idempotent).
    """
    if job_id_str in project.job_ids:
        return False
    project.job_ids.append(job_id_str)
    return True


# ---------------------------------------------------------------------------
# Summarize / export
# ---------------------------------------------------------------------------


def summarize_project(
    project: RemyProject,
    jobs: list[Any],  # list[Job] — Any to avoid cross-package circular imports
) -> str:
    """Return a human-readable text summary for a project.

    Redaction: no artifact content, no approval reasons, no event messages,
    no diff previews, no command output, no raw exception text.
    """
    job_map = {str(j.id): j for j in jobs}
    lines: list[str] = []
    lines.append("Remedy Project Registry v0")
    lines.append(f"Project : {project.name}")
    lines.append(f"ID      : {project.id}")
    if project.description:
        lines.append(f"Desc    : {project.description}")
    lines.append(f"Created : {project.created_at.strftime('%Y-%m-%dT%H:%M:%SZ')}")
    lines.append("")
    lines.append(f"Repos ({len(project.repo_paths)}):")
    if project.repo_paths:
        for rp in project.repo_paths:
            lines.append(f"  {rp}")
    else:
        lines.append("  (none)")
    lines.append("")
    lines.append(f"Jobs ({len(project.job_ids)}):")
    if project.job_ids:
        for jid in project.job_ids:
            j = job_map.get(jid)
            if j is not None:
                lines.append(f"  {jid[:8]}  {j.state.value:<12}  {j.name[:40]}")
            else:
                lines.append(f"  {jid[:8]}  (not loaded)")
    else:
        lines.append("  (none)")
    lines.append("")
    lines.append("Context coverage aggregate : placeholder (not implemented)")
    lines.append("Project Brain UI           : not implemented")
    lines.append("Note: Project Brain visual aggregation deferred to a future step.")
    return "\n".join(lines)


def export_project_json(
    project: RemyProject,
    jobs: list[Any],  # list[Job]
) -> dict[str, Any]:
    """Return JSON-serialisable project summary dict.

    Schema::

        {
            "version": 1,
            "project": {id, name, description, created_at},
            "repo_paths": [...],
            "jobs": [{id, state, task_count, artifact_count}, ...],
            "counts": {repo_count, job_count, task_count, artifact_count},
            "context_coverage": {score, scope, present_signal_count,
                                 missing_signal_count, v0_max_score},
            "future_layers": {
                "repo_brain": "not_implemented",
                "project_brain": "not_implemented",
                "global_brain": "not_implemented",
                "mempalace": "not_implemented",
                "mcp_skill_registry": "not_implemented"
            }
        }

    context_coverage is a compact summary only — full signal detail is
    available via `remedy project context <project_id> --json`.

    Redaction: no artifact content, no approval reasons, no diff previews,
    no event messages, no command output, no raw exception text.
    """
    from packages.orchestration.project_context_coverage import (
        derive_project_context_coverage,
    )

    job_map = {str(j.id): j for j in jobs}
    jobs_out: list[dict[str, Any]] = []
    total_tasks = 0
    total_artifacts = 0
    for jid in project.job_ids:
        j = job_map.get(jid)
        if j is not None:
            tc = len(j.tasks)
            ac = len(j.artifacts)
            total_tasks += tc
            total_artifacts += ac
            jobs_out.append({
                "id": str(j.id),
                "state": j.state.value,
                "task_count": tc,
                "artifact_count": ac,
            })
        else:
            jobs_out.append({
                "id": jid,
                "state": "unknown",
                "task_count": 0,
                "artifact_count": 0,
            })

    loaded_jobs = [j for j in jobs if j is not None]
    ctx_snap = derive_project_context_coverage(project, loaded_jobs)

    return {
        "version": 1,
        "project": {
            "id": str(project.id),
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at.isoformat(),
        },
        "repo_paths": list(project.repo_paths),
        "jobs": jobs_out,
        "counts": {
            "repo_count": len(project.repo_paths),
            "job_count": len(project.job_ids),
            "task_count": total_tasks,
            "artifact_count": total_artifacts,
        },
        "context_coverage": {
            "score": ctx_snap.score,
            "scope": ctx_snap.scope,
            "present_signal_count": ctx_snap.present_signal_count,
            "missing_signal_count": ctx_snap.missing_signal_count,
            "v0_max_score": 95,
        },
        "future_layers": {
            "repo_brain": "not_implemented",
            "project_brain": "not_implemented",
            "global_brain": "not_implemented",
            "mempalace": "not_implemented",
            "mcp_skill_registry": "not_implemented",
        },
    }
