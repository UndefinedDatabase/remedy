"""
Workspace models and local runtime.

A Workspace represents a bounded working area for a single Job.  The local
runtime backs it with a real directory under .data/workspaces/<job_id>/.

Design constraints:
  - Runtime is injected; orchestration never imports provider code directly.
  - LocalWorkspaceRuntime is the only concrete implementation for Step 6.
  - No patch application, no command execution — only structured file writes.
  - Storage location follows the same resolution order as storage.py:
      1. REMEDY_DATA_DIR env var (workspace dir is a sibling of jobs/ inside it).
      2. Repository-local default: <repo_root>/.data/workspaces/
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from uuid import UUID


# ---------------------------------------------------------------------------
# Domain models
# ---------------------------------------------------------------------------


@dataclass
class MaterializedFile:
    """A file written to the workspace during task execution.

    path:    absolute path of the written file.
    content: the text content that was written.
    size:    number of bytes written.
    """

    path: Path
    content: str
    size: int


@dataclass
class Workspace:
    """Runtime-backed working area for a single Job.

    job_id:             UUID of the owning job.
    root:               root directory of the workspace on disk.
    materialized_files: files written during the current session, in order.
    """

    job_id: UUID
    root: Path
    materialized_files: list[MaterializedFile] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Runtime
# ---------------------------------------------------------------------------


def _resolve_workspace_root() -> Path:
    """Resolve the base directory for all workspaces.

    Checks REMEDY_DATA_DIR env var first; falls back to <repo_root>/.data/workspaces.
    """
    env = os.environ.get("REMEDY_DATA_DIR")
    if env:
        return Path(env) / "workspaces"
    # packages/orchestration/workspace.py → repo root is 3 levels up
    repo_root = Path(__file__).resolve().parent.parent.parent
    return repo_root / ".data" / "workspaces"


class LocalWorkspaceRuntime:
    """Workspace runtime that materializes files on the local filesystem.

    Each job gets its own subdirectory: <workspace_root>/<job_id>/

    This runtime is injected into orchestration functions; it must not be
    imported directly by providers.
    """

    def __init__(self, job_id: UUID) -> None:
        self._job_id = job_id
        root = _resolve_workspace_root() / str(job_id)
        root.mkdir(parents=True, exist_ok=True)
        self._workspace = Workspace(job_id=job_id, root=root)

    @property
    def workspace(self) -> Workspace:
        return self._workspace

    def write(self, relative_path: str, content: str) -> MaterializedFile:
        """Write content to a file inside the workspace.

        relative_path: path relative to the workspace root (e.g. "task_log/type_0.txt").
        content:       text to write (UTF-8).

        Creates parent directories as needed.  Overwrites existing files.

        Returns a MaterializedFile describing what was written.
        """
        target = self._workspace.root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        mf = MaterializedFile(
            path=target,
            content=content,
            size=target.stat().st_size,
        )
        self._workspace.materialized_files.append(mf)
        return mf
