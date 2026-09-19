"""Staging Workspace — a filtered copy of the target repo in an isolated directory.

Design:
  - Filtered copy excludes: .git, .env*, node_modules, venv, __pycache__, .data
  - Symlinks resolving outside repo root are excluded (escape detection)
"""
from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# Directories excluded from filtered copy
_EXCLUDE_DIRS: frozenset[str] = frozenset({
    ".git", "node_modules", "venv", ".venv", "__pycache__",
    ".data", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    ".tox", "dist", "build", ".eggs",
})


# ---------------------------------------------------------------------------
# Safety helpers
# ---------------------------------------------------------------------------

def _is_env_file(name: str) -> bool:
    """Return True for .env, .env.*, .env-* files."""
    if name == ".env":
        return True
    if name.startswith(".env.") or name.startswith(".env-"):
        return True
    return False


def _should_exclude_dir(name: str) -> bool:
    """Check if a directory name should be excluded from filtered copy."""
    if name in _EXCLUDE_DIRS:
        return True
    # Skip hidden dot-directories
    if name.startswith(".") and name != ".":
        return True
    return False


def _is_symlink_escape(item: Path, repo_root: Path) -> bool:
    """Return True if item is a symlink resolving outside repo_root."""
    if not item.is_symlink():
        return False
    try:
        resolved = item.resolve()
        root_resolved = repo_root.resolve()
        return not resolved.is_relative_to(root_resolved)
    except (OSError, ValueError):
        return True  # Cannot resolve — treat as escape


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

@dataclass
class StagingWorkspace:
    """An isolated, filtered copy of a target repo."""
    staging_dir: Path
    target_repo: Path
    job_id: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    files_copied: int = 0
    dirs_copied: int = 0
    excluded_dirs: list[str] = field(default_factory=list)
    excluded_symlinks: list[str] = field(default_factory=list)
    excluded_env_files: list[str] = field(default_factory=list)
    active: bool = True


# ---------------------------------------------------------------------------
# Filtered copy
# ---------------------------------------------------------------------------

def create_staging_workspace(
    target_repo: Path,
    staging_parent: Path,
    job_id: str,
) -> StagingWorkspace:
    """Create a filtered copy of target_repo in an isolated staging directory.

    Copies all files except excluded dirs/patterns. Preserves directory structure.
    Excludes symlinks that resolve outside repo root and .env* files.
    staging_parent should be a Remedy workspace-scoped directory.
    """
    staging_dir = staging_parent / f"staging_{job_id[:16]}"
    if staging_dir.exists():
        shutil.rmtree(staging_dir)
    staging_dir.mkdir(parents=True, exist_ok=True)

    files_copied = 0
    dirs_copied = 0
    excluded: list[str] = []
    excluded_symlinks: list[str] = []
    excluded_env_files: list[str] = []

    repo_root_resolved = target_repo.resolve()

    def _copy_tree(src: Path, dst: Path) -> None:
        nonlocal files_copied, dirs_copied
        dst.mkdir(parents=True, exist_ok=True)
        dirs_copied += 1

        for item in sorted(src.iterdir()):
            rel = str(item.relative_to(target_repo))

            # Symlink escape check
            if _is_symlink_escape(item, target_repo):
                excluded_symlinks.append(rel)
                continue

            if item.is_dir():
                if _should_exclude_dir(item.name):
                    excluded.append(rel)
                    continue
                _copy_tree(item, dst / item.name)
            elif item.is_file():
                if _is_env_file(item.name):
                    excluded_env_files.append(rel)
                    continue
                shutil.copy2(str(item), str(dst / item.name))
                files_copied += 1

    _copy_tree(target_repo, staging_dir)

    return StagingWorkspace(
        staging_dir=staging_dir,
        target_repo=target_repo,
        job_id=job_id,
        files_copied=files_copied,
        dirs_copied=dirs_copied,
        excluded_dirs=excluded,
        excluded_symlinks=excluded_symlinks,
        excluded_env_files=excluded_env_files,
    )
