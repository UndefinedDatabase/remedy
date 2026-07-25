"""
Data path resolution for Remedy.

This is the single authoritative location in production Python that reads
REMEDY_DATA_DIR.  All other production modules (storage.py, run_log.py,
project_registry.py, workspace.py, apps/cli/main.py) must import helpers
from this module instead of reading the environment variable directly.

Resolution order (via config system):
  1. REMEDY_DATA_DIR environment variable
  2. Project remedy.toml [remedy] data_dir
  3. User ~/.config/remedy/remedy.toml [remedy] data_dir
  4. Repository-local default: <repo_root>/.data

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
import re
import sys
from pathlib import Path
from uuid import UUID


def resolve_data_root() -> Path:
    """Return the Remedy data root directory.

    Env var checked directly (always fresh) for backward compatibility with
    tests that set REMEDY_DATA_DIR at runtime. TOML config checked via cached
    config system for file-based overrides.
    The returned path is NOT guaranteed to exist — callers must mkdir as needed.
    """
    env = os.environ.get("REMEDY_DATA_DIR")
    if env:
        return Path(env)
    from packages.orchestration.config import get_config

    configured = get_config().get("data_dir")
    if configured:
        return Path(configured)
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


def evidence_exports_dir(root: Path | None = None) -> Path:
    """Return the hidden evidence-export base directory (<root>/evidence_exports).

    Evidence bundles default here instead of the repository root, so a working
    tree is never littered with ``remedy-job-evidence-*`` directories.
    """
    return (root if root is not None else resolve_data_root()) / "evidence_exports"


def job_evidence_export_dir(job_id: str, root: Path | None = None) -> Path:
    """Return the default export directory for one job's evidence bundle."""
    return evidence_exports_dir(root) / job_id


def job_evidence_index_dir(root: Path | None = None) -> Path:
    """Return the existing job evidence index directory (<root>/job_evidence_index)."""
    return (root if root is not None else resolve_data_root()) / "job_evidence_index"


def control_dir(root: Path | None = None) -> Path:
    """Return the control area (<root>/control).

    F011: operator control data — a stop request and its archive — lives here, kept apart
    from the evidence a job produces about itself. It is private (0700/0600); see
    ``packages/orchestration/safe_points.py``.
    """
    return (root if root is not None else resolve_data_root()) / "control"


_SHORT_HEX_RE = re.compile(r"[0-9a-fA-F]{4,32}")


def resolve_job_id(raw: str) -> UUID:
    """Parse a full UUID or resolve a short hex prefix to a unique job UUID.

    Exits with code 1 on invalid input, code 2 on ambiguous prefix.
    """
    try:
        return UUID(raw)
    except ValueError:
        pass

    if not _SHORT_HEX_RE.fullmatch(raw):
        print(f"Error: invalid job ID: {raw!r}", file=sys.stderr)
        sys.exit(1)

    jdir = jobs_dir()
    if not jdir.exists():
        print(f"Error: no job matches prefix {raw!r}", file=sys.stderr)
        sys.exit(1)

    lower = raw.lower()
    matches = [
        p.stem for p in jdir.glob("*.json")
        if p.stem.lower().startswith(lower)
    ]
    if len(matches) == 1:
        return UUID(matches[0])
    if len(matches) > 1:
        print(f"Error: ambiguous job id prefix '{raw}' matches "
              f"{len(matches)} jobs:", file=sys.stderr)
        for m in sorted(matches):
            print(f"  {m[:8]}", file=sys.stderr)
        sys.exit(2)

    print(f"Error: no job matches prefix {raw!r}", file=sys.stderr)
    sys.exit(1)
