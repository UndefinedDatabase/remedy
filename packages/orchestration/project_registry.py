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
    AmbiguousProjectError                          -- raised on duplicate slug
    InvalidProjectSelectorError                    -- raised on empty selectors
    RepoOwnershipConflictError                     -- raised on repo conflicts
    save_project(project) -> None
    load_project(project_id: UUID) -> RemyProject
    list_projects() -> list[RemyProject]
    attach_repo(project, repo_path) -> bool        # True if added (idempotent)
    attach_job(project, job_id_str) -> bool        # True if added (idempotent)
    summarize_project(project, jobs) -> str
    export_project_json(project, jobs) -> dict
    slugify(name) -> str                            # F146: kebab-case slug
    resolve_project(cwd) -> RemyProject | None      # F146: cwd → project (read-only)
    require_project(cwd) -> RemyProject             # F146: cwd → project or raise
    find_project_by_repo(real_path) -> RemyProject | None  # F146
    select_project(flag, cwd) -> (RemyProject, source)    # F146: precedence
    register_project_repo(name, repo_path) -> RemyProject  # F146: explicit creation
    NotAGitRepoError                           -- raised on non-Git repo
    attach_repo_canonical(project, repo_path)  # F146: canonical attach service
    migrate_legacy_projects() -> int           # F146: deterministic batch migration
"""

from __future__ import annotations

import json
import logging
import os
import re
import subprocess
import tempfile
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
# Errors
# ---------------------------------------------------------------------------


class ProjectNotFoundError(Exception):
    """Raised when a requested project cannot be found or resolved."""

    def __init__(
        self,
        project_id: UUID | None = None,
        *,
        cwd: str | Path | None = None,
        selector_value: str | None = None,
        selector_source: str | None = None,
    ) -> None:
        if cwd is not None:
            super().__init__(
                "No project registered for this repo. Run: remedy init"
            )
            self.cwd: str | None = str(cwd)
        elif selector_value is not None:
            source_label = f" (from {selector_source})" if selector_source else ""
            super().__init__(
                f"Project not found: {selector_value!r}{source_label}"
            )
            self.cwd = None
        else:
            super().__init__(f"Project not found: {project_id}")
            self.cwd = None
        self.project_id = project_id
        self.selector_value = selector_value
        self.selector_source = selector_source


class AmbiguousProjectError(Exception):
    """Raised when a slug matches more than one project."""

    def __init__(self, slug: str, project_ids: list[UUID]) -> None:
        ids = ", ".join(str(p) for p in project_ids[:5])
        super().__init__(
            f"Ambiguous slug {slug!r}: matches projects {ids}. "
            f"Use the full UUID to disambiguate."
        )
        self.slug = slug
        self.project_ids = project_ids


class InvalidProjectSelectorError(Exception):
    """Raised when a project selector (flag or env) is empty/whitespace."""

    def __init__(self, source: str, value: str) -> None:
        super().__init__(
            f"Invalid project selector from {source}: {value!r} "
            f"(empty or whitespace-only)"
        )
        self.source = source
        self.value = value


class RepoOwnershipConflictError(Exception):
    """Raised when a repo path is already owned by another project."""

    def __init__(self, repo_path: str, owner_project: RemyProject) -> None:
        super().__init__(
            f"Repo {repo_path!r} is already owned by project "
            f"{owner_project.slug} ({str(owner_project.id)[:8]})"
        )
        self.repo_path = repo_path
        self.owner_project = owner_project


# ---------------------------------------------------------------------------
# Storage — atomic save
# ---------------------------------------------------------------------------


_SLUG_RE = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")


def _validate_slug(slug: str | None, project_id: UUID) -> None:
    """Enforce the closed persisted slug contract before save."""
    if slug is None:
        raise ValueError("slug must not be None when saving a project")
    if not slug:
        raise ValueError("slug must not be empty")
    if not _SLUG_RE.match(slug):
        raise ValueError(f"slug {slug!r} is not valid kebab-case")
    existing = _collect_slugs(exclude_id=project_id)
    if slug in existing:
        raise ValueError(
            f"slug {slug!r} is already used by another project"
        )


def save_project(project: RemyProject) -> None:
    """Persist a RemyProject to disk as JSON (atomic: temp file + os.replace).

    When slug is None, auto-derives one from: canonical_repo_path dir name,
    then repo_paths[0] dir name, then project.name. Validates slug contract:
    non-null, kebab-case, unique among persisted records.
    """
    if project.slug is None:
        if project.canonical_repo_path:
            base = slugify(Path(project.canonical_repo_path).name)
        elif project.repo_paths:
            base = slugify(Path(project.repo_paths[0]).name)
        else:
            base = slugify(project.name)
        project.slug = _unique_slug(base, exclude_id=project.id)
    _validate_slug(project.slug, project.id)
    d = _projects_dir()
    d.mkdir(parents=True, exist_ok=True)
    target = d / f"{project.id}.json"
    fd, tmp_path = tempfile.mkstemp(dir=str(d), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(project.model_dump_json(indent=2))
        os.replace(tmp_path, str(target))
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def _project_set_readonly() -> list[RemyProject]:
    """Deterministic read-only projection of the full project set.

    Loads all valid raw records without writing, reserves every persisted
    slug, orders legacy missing-slug records by (created_at asc, UUID asc),
    allocates unique effective slugs across the full set, and derives
    canonical_repo_path in memory. Produces the same slug for a project
    regardless of which API accesses it first.
    """
    d = _projects_dir()
    if not d.exists():
        return []

    raw: list[tuple[Path, RemyProject]] = []
    for path in d.glob("*.json"):
        try:
            raw.append((path, RemyProject.model_validate_json(path.read_text())))
        except (ValueError, OSError):
            pass

    reserved: set[str] = set()
    needs_slug: list[RemyProject] = []
    for _path, p in raw:
        if p.slug is not None:
            reserved.add(p.slug)
        else:
            needs_slug.append(p)

    needs_slug.sort(key=lambda p: (p.created_at, str(p.id)))

    for p in needs_slug:
        base = slugify(p.name)
        candidate = base
        idx = 2
        while candidate in reserved:
            candidate = f"{base}-{idx}"
            idx += 1
        p.slug = candidate
        reserved.add(candidate)

    for _path, p in raw:
        if p.canonical_repo_path is None and p.repo_paths:
            p.canonical_repo_path = str(Path(p.repo_paths[0]).resolve())

    return [p for _path, p in raw]


def _load_project_readonly(path: Path) -> RemyProject:
    """Load one project from the deterministic read-only projection.

    Uses the full-set projection to guarantee slug uniqueness even for
    legacy records. Never writes.
    """
    target_id = None
    try:
        stem = path.stem
        target_id = UUID(stem)
    except ValueError:
        pass

    for p in _project_set_readonly():
        if target_id is not None and p.id == target_id:
            return p

    project = RemyProject.model_validate_json(path.read_text())
    if project.slug is None:
        base = slugify(project.name)
        project.slug = _unique_slug(base, exclude_id=project.id)
    if project.canonical_repo_path is None and project.repo_paths:
        project.canonical_repo_path = str(Path(project.repo_paths[0]).resolve())
    return project


def load_project(project_id: UUID) -> RemyProject:
    """Load a RemyProject from disk by ID.

    Raises ProjectNotFoundError if the project does not exist.
    Legacy records without slug/canonical_repo_path are migrated via
    deterministic batch migration (not per-record) so slug allocation
    is independent of access order.
    """
    path = _projects_dir() / f"{project_id}.json"
    if not path.exists():
        raise ProjectNotFoundError(project_id)
    migrate_legacy_projects()
    project = RemyProject.model_validate_json(path.read_text())
    return project


def list_projects() -> list[RemyProject]:
    """Return all persisted projects sorted by created_at descending.

    Legacy records without slug/canonical_repo_path are migrated via
    deterministic batch migration (sorted by created_at ascending, then
    UUID as tie-breaker) before returning.
    """
    d = _projects_dir()
    if not d.exists():
        return []
    migrate_legacy_projects()
    projects: list[RemyProject] = []
    for path in d.glob("*.json"):
        try:
            projects.append(RemyProject.model_validate_json(path.read_text()))
        except (ValueError, OSError):
            pass
    return sorted(projects, key=lambda p: p.created_at, reverse=True)


def _list_projects_readonly() -> list[RemyProject]:
    """Load all projects read-only via deterministic projection, never write."""
    return sorted(_project_set_readonly(), key=lambda p: p.created_at, reverse=True)


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


def migrate_legacy_projects() -> int:
    """Deterministic batch migration of legacy records without slug.

    Reads all raw project files, sorts by (created_at ascending, UUID
    ascending) for deterministic slug allocation, derives missing slugs
    from that ordered set, and persists atomically. Returns the count
    of migrated records.
    """
    d = _projects_dir()
    if not d.exists():
        return 0

    raw: list[tuple[Path, RemyProject]] = []
    for path in d.glob("*.json"):
        try:
            p = RemyProject.model_validate_json(path.read_text())
            if p.slug is None or (p.canonical_repo_path is None and p.repo_paths):
                raw.append((path, p))
        except (ValueError, OSError):
            pass

    if not raw:
        return 0

    raw.sort(key=lambda t: (t[1].created_at, str(t[1].id)))

    allocated_slugs = _collect_slugs()
    count = 0
    for _path, project in raw:
        changed = False
        if project.slug is None:
            base = slugify(project.name)
            candidate = base
            idx = 2
            while candidate in allocated_slugs:
                candidate = f"{base}-{idx}"
                idx += 1
            project.slug = candidate
            allocated_slugs.add(candidate)
            changed = True
        if project.canonical_repo_path is None and project.repo_paths:
            project.canonical_repo_path = str(Path(project.repo_paths[0]).resolve())
            changed = True
        if changed:
            save_project(project)
            count += 1

    return count


def attach_repo_canonical(
    project: RemyProject,
    repo_path: str | Path,
) -> tuple[bool, str]:
    """Canonical repository attachment service.

    Validates Git, resolves root, checks ownership, rebinds canonical,
    deduplicates repo_paths, and persists atomically.

    Returns (changed, repo_real). Raises RepoOwnershipConflictError or
    NotAGitRepoError.
    """
    from packages.orchestration.worktrees import is_git_repo, repo_root

    if not is_git_repo(repo_path):
        raise NotAGitRepoError(str(Path(repo_path).resolve()))

    repo_real = str(repo_root(repo_path).resolve())

    existing = _find_project_by_repo_readonly(repo_real)
    if existing is not None and existing.id != project.id:
        raise RepoOwnershipConflictError(repo_real, existing)

    needs_dedup = len(project.repo_paths) != len(set(project.repo_paths))

    if (
        project.canonical_repo_path == repo_real
        and repo_real in project.repo_paths
        and not needs_dedup
    ):
        return False, repo_real

    old_canonical = project.canonical_repo_path
    project.canonical_repo_path = repo_real

    new_paths: list[str] = []
    seen: set[str] = set()
    for rp in project.repo_paths:
        effective = repo_real if rp == old_canonical else rp
        if effective not in seen:
            new_paths.append(effective)
            seen.add(effective)
    if repo_real not in seen:
        new_paths.append(repo_real)
    project.repo_paths = new_paths

    save_project(project)
    return True, repo_real


def _managed_worktree_parent(root: Path) -> Path | None:
    """If *root* is inside a managed Remedy worktree, return the parent repo.

    Validates via git common-dir: a real managed worktree has its git
    common directory pointing back to the parent repo's .git. Falls back
    to path component detection only when git is unavailable.
    """
    import subprocess

    from packages.orchestration.worktrees import WORKTREE_DIRNAME

    parts = root.parts
    wt_index = None
    for i, part in enumerate(parts):
        if part == WORKTREE_DIRNAME:
            wt_index = i
            break
    if wt_index is None:
        return None

    candidate_parent = Path(*parts[:wt_index]) if wt_index > 0 else None
    if candidate_parent is None:
        return None

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-common-dir"],
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            common_dir = Path(result.stdout.strip())
            if not common_dir.is_absolute():
                common_dir = (root / common_dir).resolve()
            else:
                common_dir = common_dir.resolve()
            parent_git = candidate_parent.resolve() / ".git"
            if common_dir == parent_git or common_dir == parent_git.resolve():
                return candidate_parent
            return None
    except (OSError, subprocess.TimeoutExpired):
        pass

    return None


def _find_project_by_repo_readonly(real_path: str) -> RemyProject | None:
    """Read-only repo lookup — never triggers migration writes."""
    matches: list[RemyProject] = []
    for p in _list_projects_readonly():
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

    NEVER WRITES.  Git root → symlink resolve → real-path match against
    registry using read-only loading.  Inside a managed worktree
    (``.remedy-wt/``), maps back to the parent repo via git common-dir
    validation.  Returns ``None`` when *cwd* is not in a git repo or no
    project is registered.
    """
    from packages.orchestration.worktrees import WorktreeError, is_git_repo, repo_root

    cwd_path = Path(cwd).resolve()
    if not is_git_repo(cwd_path):
        return None
    try:
        root = repo_root(cwd_path)
    except (WorktreeError, OSError, subprocess.SubprocessError):
        # The named failures of `git rev-parse`: a non-repository or an
        # unusable checkout (WorktreeError), a missing/unreadable path (OSError)
        # and a git that never returned (SubprocessError, incl. TimeoutExpired).
        # Anything else is a defect and must not be swallowed here.
        return None

    real = str(root.resolve())

    parent = _managed_worktree_parent(root)
    if parent is not None:
        real = str(parent.resolve())

    return _find_project_by_repo_readonly(real)


def require_project(cwd: str | Path) -> RemyProject:
    """Like :func:`resolve_project` but raises on failure.

    Raises :class:`ProjectNotFoundError` with an exact fix-it message when
    no project matches.
    """
    project = resolve_project(cwd)
    if project is None:
        raise ProjectNotFoundError(cwd=cwd)
    return project


def _lookup_by_slug_or_uuid_readonly(value: str) -> RemyProject:
    """Resolve *value* as UUID first, then as slug — read-only, never writes.

    Raises AmbiguousProjectError when multiple projects share the slug.
    Raises ProjectNotFoundError (with the value) when nothing matches.
    """
    try:
        uid = UUID(value)
        path = _projects_dir() / f"{uid}.json"
        if path.exists():
            return _load_project_readonly(path)
    except ValueError:
        pass
    matches: list[RemyProject] = []
    for p in _list_projects_readonly():
        if p.slug == value:
            matches.append(p)
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise AmbiguousProjectError(value, [m.id for m in matches])
    raise ProjectNotFoundError(project_id=None, selector_value=value)


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
    ``"flag"``, ``"environment"``, ``"cwd"``.

    Empty or whitespace-only *flag* / env values raise
    :class:`InvalidProjectSelectorError`.
    """
    if flag is not None:
        if not flag.strip():
            raise InvalidProjectSelectorError("flag", flag)
        try:
            return _lookup_by_slug_or_uuid_readonly(flag.strip()), "flag"
        except ProjectNotFoundError:
            raise ProjectNotFoundError(
                selector_value=flag.strip(), selector_source="flag"
            ) from None

    env_val = os.environ.get("REMEDY_PROJECT")
    if env_val is not None:
        if not env_val.strip():
            raise InvalidProjectSelectorError("environment", env_val)
        try:
            return _lookup_by_slug_or_uuid_readonly(env_val.strip()), "environment"
        except ProjectNotFoundError:
            raise ProjectNotFoundError(
                selector_value=env_val.strip(), selector_source="environment"
            ) from None

    project = resolve_project(cwd)
    if project is not None:
        return project, "cwd"

    raise ProjectNotFoundError(cwd=cwd)


# ---------------------------------------------------------------------------
# Registration primitive
# ---------------------------------------------------------------------------


class NotAGitRepoError(Exception):
    """Raised when a path is not a Git repository but one is required."""

    def __init__(self, path: str) -> None:
        super().__init__(f"Not a git repository: {path!r}")
        self.path = path


def register_project_repo(
    name: str,
    repo_path: str | Path,
    *,
    description: str | None = None,
) -> RemyProject:
    """Create or return a project for the given repository path.

    Requires a real Git repository — raises NotAGitRepoError for plain dirs.
    Resolves the Git root and derives slug from the repository directory name
    (not the display name). If a project already owns this canonical path,
    returns that project (same-repo idempotency).
    """
    from packages.orchestration.worktrees import is_git_repo, repo_root

    if not is_git_repo(repo_path):
        raise NotAGitRepoError(str(Path(repo_path).resolve()))

    real = str(repo_root(repo_path).resolve())

    existing = _find_project_by_repo_readonly(real)
    if existing is not None:
        return existing

    slug = _unique_slug(slugify(Path(real).name))
    project = RemyProject(
        name=name,
        slug=slug,
        canonical_repo_path=real,
        description=description,
        repo_paths=[real],
    )
    save_project(project)
    return project


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
