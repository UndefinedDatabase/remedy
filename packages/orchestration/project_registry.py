"""
Project Registry v0 — minimal project metadata store.

Projects represent a named scope containing one or more repos and jobs.
They are the foundation for the future multi-job, multi-repo brain hierarchy:
  Global Brain → Project Brain → Repo Brain → Job Brain.

F146 canonical identity rule: the registry UUID (RemyProject.id) is the
project identity everywhere user-visible and everywhere data is scoped.
The worktree-derived path digest (worktrees.project_id) is a WORKSPACE KEY
for lock namespacing and dev_server runtime only — never a project identity.

This module is read-only at the data layer except for creation, linking,
and legacy migration operations.  No repo scanning. No artifact content.
No approval reasons. No diff previews. No event messages.

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
    slugify(name) -> str                            # F146: kebab-case slug
    resolve_project(cwd) -> RemyProject | None      # F146: cwd → project
    require_project(cwd) -> RemyProject             # F146: cwd → project or raise
    find_project_by_repo(real_path) -> RemyProject | None  # F146
    select_project(flag, cwd) -> (RemyProject, source)    # F146: precedence
"""

from __future__ import annotations

import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from packages.orchestration.data_paths import projects_dir as _projects_dir

_log = logging.getLogger(__name__)


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


class RemyProject(BaseModel):
    """Minimal project metadata — name, attached repos, and linked job IDs.

    F146: ``slug`` and ``canonical_repo_path`` are additive fields. Legacy
    records without them are migrated on first load.
    """

    id: UUID = Field(default_factory=uuid4)
    name: str
    slug: str | None = None
    canonical_repo_path: str | None = None
    description: str | None = None
    created_at: datetime = Field(default_factory=_utcnow)
    repo_paths: list[str] = Field(default_factory=list)
    job_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------


class ProjectNotFoundError(Exception):
    """Raised when a requested project cannot be found or resolved."""

    def __init__(
        self,
        project_id: UUID | None = None,
        *,
        cwd: str | Path | None = None,
    ) -> None:
        if cwd is not None:
            super().__init__(
                "No project registered for this repo. Run: remedy init"
            )
            self.cwd: str | None = str(cwd)
        else:
            super().__init__(f"Project not found: {project_id}")
            self.cwd = None
        self.project_id = project_id


def save_project(project: RemyProject) -> None:
    """Persist a RemyProject to disk as JSON."""
    d = _projects_dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{project.id}.json").write_text(project.model_dump_json(indent=2))


def load_project(project_id: UUID) -> RemyProject:
    """Load a RemyProject from disk by ID.

    Raises ProjectNotFoundError if the project does not exist.
    Legacy records without slug/canonical_repo_path are migrated on load.
    """
    path = _projects_dir() / f"{project_id}.json"
    if not path.exists():
        raise ProjectNotFoundError(project_id)
    project = RemyProject.model_validate_json(path.read_text())
    if _migrate_legacy(project):
        save_project(project)
    return project


def list_projects() -> list[RemyProject]:
    """Return all persisted projects sorted by created_at descending.

    Legacy records without slug/canonical_repo_path are migrated on load.
    """
    d = _projects_dir()
    if not d.exists():
        return []
    projects: list[RemyProject] = []
    for path in d.glob("*.json"):
        try:
            p = RemyProject.model_validate_json(path.read_text())
            if _migrate_legacy(p):
                save_project(p)
            projects.append(p)
        except (ValueError, OSError):
            pass
    return sorted(projects, key=lambda p: p.created_at, reverse=True)


# ---------------------------------------------------------------------------
# F146 — slug, legacy migration, resolution
# ---------------------------------------------------------------------------


def slugify(name: str) -> str:
    """Convert *name* to a stable kebab-case slug.

    Non-alphanumeric runs become a single dash; leading/trailing dashes are
    stripped.  An empty result (e.g. from ``"---"``) falls back to
    ``"project"``.
    """
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s or "project"


def _collect_slugs(exclude_id: UUID | None = None) -> set[str]:
    """Read slug values from all project files without triggering migration."""
    d = _projects_dir()
    if not d.exists():
        return set()
    slugs: set[str] = set()
    for path in d.glob("*.json"):
        try:
            data = json.loads(path.read_text())
            s = data.get("slug")
            eid = data.get("id")
            if s and (exclude_id is None or eid != str(exclude_id)):
                slugs.add(s)
        except (ValueError, OSError):
            pass
    return slugs


def _unique_slug(base: str, exclude_id: UUID | None = None) -> str:
    """Return *base* if unique among persisted slugs, else *base-2*, *base-3*, …"""
    existing = _collect_slugs(exclude_id)
    if base not in existing:
        return base
    for i in range(2, 1000):
        candidate = f"{base}-{i}"
        if candidate not in existing:
            return candidate
    raise ValueError(f"Cannot derive unique slug for {base!r}")


def _migrate_legacy(project: RemyProject) -> bool:
    """Derive missing ``slug`` and ``canonical_repo_path`` on a legacy record.

    Returns True if any field was populated (caller should persist).
    """
    changed = False
    if project.slug is None:
        base = slugify(project.name)
        project.slug = _unique_slug(base, exclude_id=project.id)
        changed = True
    if project.canonical_repo_path is None and project.repo_paths:
        project.canonical_repo_path = str(Path(project.repo_paths[0]).resolve())
        changed = True
    return changed


def _managed_worktree_parent(root: Path) -> Path | None:
    """If *root* is inside a ``.remedy-wt/`` directory, return the parent repo."""
    from packages.orchestration.worktrees import WORKTREE_DIRNAME

    parts = root.parts
    for i, part in enumerate(parts):
        if part == WORKTREE_DIRNAME:
            return Path(*parts[:i]) if i > 0 else None
    return None


def find_project_by_repo(real_path: str) -> RemyProject | None:
    """Return the registered project owning *real_path*, or ``None``.

    When multiple projects claim the same path (legacy duplicate),
    the newest valid record wins and a bounded warning is logged.
    """
    matches: list[RemyProject] = []
    for p in list_projects():
        if p.canonical_repo_path == real_path:
            matches.append(p)
        elif real_path in p.repo_paths:
            matches.append(p)
    if not matches:
        return None
    if len(matches) > 1:
        ids = ", ".join(str(m.id) for m in matches[:5])
        _log.warning(
            "Multiple projects claim %s — using newest: %s", real_path, ids
        )
    return matches[0]


def resolve_project(cwd: str | Path) -> RemyProject | None:
    """Resolve the registered project for a working directory.

    Never writes.  Git root → symlink resolve → real-path match against
    registry.  Inside a managed worktree (``.remedy-wt/``), maps back to the
    parent repo.  Returns ``None`` when *cwd* is not in a git repo or no
    project is registered.
    """
    from packages.orchestration.worktrees import is_git_repo, repo_root

    cwd_path = Path(cwd).resolve()
    if not is_git_repo(cwd_path):
        return None
    try:
        root = repo_root(cwd_path)
    except Exception:
        return None

    real = str(root.resolve())

    parent = _managed_worktree_parent(root)
    if parent is not None:
        real = str(parent.resolve())

    return find_project_by_repo(real)


def require_project(cwd: str | Path) -> RemyProject:
    """Like :func:`resolve_project` but raises on failure.

    Raises :class:`ProjectNotFoundError` with an exact fix-it message when
    no project matches.
    """
    project = resolve_project(cwd)
    if project is None:
        raise ProjectNotFoundError(cwd=cwd)
    return project


def _lookup_by_slug_or_uuid(value: str) -> RemyProject:
    """Resolve *value* as UUID first, then as slug. Raises on failure."""
    try:
        uid = UUID(value)
        return load_project(uid)
    except (ValueError, ProjectNotFoundError):
        pass
    for p in list_projects():
        if p.slug == value:
            return p
    raise ProjectNotFoundError()


def select_project(
    flag: str | None,
    cwd: str | Path,
) -> tuple[RemyProject, str]:
    """Shared project-selection precedence.

    Resolution order:
      1. ``flag`` (``--project`` CLI flag) — UUID or slug
      2. ``REMEDY_PROJECT`` environment variable — UUID or slug
      3. cwd autodetection via :func:`resolve_project`
      4. :class:`ProjectNotFoundError` with fix-it

    Returns ``(project, source)`` where *source* is one of
    ``"flag"``, ``"env"``, ``"cwd"``.  Empty or whitespace-only
    *flag* / env values are treated as absent.
    """
    import os

    if flag and flag.strip():
        return _lookup_by_slug_or_uuid(flag.strip()), "flag"

    env_val = os.environ.get("REMEDY_PROJECT", "").strip()
    if env_val:
        return _lookup_by_slug_or_uuid(env_val), "env"

    project = resolve_project(cwd)
    if project is not None:
        return project, "cwd"

    raise ProjectNotFoundError(cwd=cwd)


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
