"""
Data path resolution for Remedy.

This is the single authoritative location in production Python that reads
REMEDY_DATA_DIR.  All other production modules (storage.py, run_log.py,
project_registry.py, workspace.py, apps/cli/main.py) must import helpers
from this module instead of reading the environment variable directly.

Resolution order (same as the historical per-module convention):
  1. REMEDY_DATA_DIR environment variable, if set: use Path(REMEDY_DATA_DIR).
  2. Repository-local default: <repo_root>/.data, where repo_root is derived
     from this file's own location (packages/orchestration/data_paths.py →
     repo root is 3 levels up).

Public API::

    resolve_data_root() -> Path
    jobs_dir(root: Path | None = None) -> Path
    runs_dir(root: Path | None = None) -> Path
    projects_dir(root: Path | None = None) -> Path
    workspaces_dir(root: Path | None = None) -> Path
    viewers_dir(root: Path | None = None) -> Path
"""

from __future__ import annotations

import os
from pathlib import Path


def resolve_data_root() -> Path:
    """Return the Remedy data root directory.

    Checks REMEDY_DATA_DIR env var first; falls back to <repo_root>/.data.
    The returned path is NOT guaranteed to exist — callers must mkdir as needed.
    """
    env = os.environ.get("REMEDY_DATA_DIR")
    if env:
        return Path(env)
    # packages/orchestration/data_paths.py → repo root is 3 levels up
    repo_root = Path(__file__).resolve().parents[2]
    return repo_root / ".data"


def jobs_dir(root: Path | None = None) -> Path:
    """Return the jobs storage directory (<root>/jobs)."""
    return (root if root is not None else resolve_data_root()) / "jobs"


def runs_dir(root: Path | None = None) -> Path:
    """Return the run-log base directory (<root>/runs)."""
    return (root if root is not None else resolve_data_root()) / "runs"


def projects_dir(root: Path | None = None) -> Path:
    """Return the projects storage directory (<root>/projects)."""
    return (root if root is not None else resolve_data_root()) / "projects"


def workspaces_dir(root: Path | None = None) -> Path:
    """Return the workspaces base directory (<root>/workspaces)."""
    return (root if root is not None else resolve_data_root()) / "workspaces"


def viewers_dir(root: Path | None = None) -> Path:
    """Return the brain viewer output directory (<root>/viewers)."""
    return (root if root is not None else resolve_data_root()) / "viewers"


def proposed_tasks_dir(root: Path | None = None) -> Path:
    """Return the proposed tasks storage directory (<root>/proposed_tasks)."""
    return (root if root is not None else resolve_data_root()) / "proposed_tasks"
