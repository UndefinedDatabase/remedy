"""Handler for ``remedy init`` — register a git repo as a Remedy project."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


def _handle_init(args: argparse.Namespace) -> None:
    from packages.orchestration.project_registry import (
        register_project_repo,
        resolve_project,
    )
    from packages.orchestration.worktrees import is_git_repo, repo_root

    cwd = Path.cwd()

    if not is_git_repo(cwd):
        print(
            "remedy init requires a git repository — run `git init` first.",
            file=sys.stderr,
        )
        sys.exit(4)

    root = repo_root(cwd)
    project_name = getattr(args, "project_name", None) or root.name

    existing = resolve_project(cwd)
    if existing is not None:
        print(f"[exists] project {existing.slug}")
        return

    project = register_project_repo(project_name, root)
    print(f"[created] project {project.slug}")


COMMAND_HANDLERS = {
    "init.run": _handle_init,
}
