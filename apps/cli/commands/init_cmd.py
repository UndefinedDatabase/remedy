"""Handler for ``remedy init`` — register a git repo as a Remedy project."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse

_CONFIG_FILENAME = "remedy.toml"

_CORE_TEMPLATE = """\
# Remedy project configuration
# Run `remedy config list` to see all available keys.

[remedy]
# data_dir = ".data"
"""

_RUNTIME_ACTIVE = """\

[runtime]
cmd = {cmd}
cwd = {cwd}
port = {port}
"""

_RUNTIME_SKIP = """\

# [runtime]
# No known framework marker detected. Add a [runtime] section
# manually or re-run after adding a supported framework.
# cmd = ["npm", "run", "dev", "--"]
# port = 5173
"""


def _format_toml_list(items: list[str]) -> str:
    return "[" + ", ".join(f'"{i}"' for i in items) + "]"


def _build_config(root: Path) -> tuple[str, str | None]:
    """Return (config_text, skip_message_or_None)."""
    from packages.runtimes.runtime_config import detect_runtimes

    found = detect_runtimes(root)
    if len(found) == 1:
        rt = found[0]
        runtime_section = _RUNTIME_ACTIVE.format(
            cmd=_format_toml_list(rt.spec.cmd),
            cwd=f'"{Path(rt.spec.cwd).relative_to(root)}"'
            if Path(rt.spec.cwd) != root
            else '"."',
            port=rt.spec.port,
        )
        return _CORE_TEMPLATE + runtime_section, None
    return _CORE_TEMPLATE + _RUNTIME_SKIP, "skipped runtime autodetect (no known framework marker)"


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

    config_file = root / _CONFIG_FILENAME
    if config_file.is_file():
        print(f"[exists] config {_CONFIG_FILENAME}")
    else:
        content, skip_msg = _build_config(root)
        config_file.write_text(content, encoding="utf-8")
        print(f"[created] config {_CONFIG_FILENAME}")
        if skip_msg:
            print(f"[skipped] {skip_msg}")

    existing = resolve_project(cwd)
    if existing is not None:
        print(f"[exists] project {existing.slug}")
    else:
        project = register_project_repo(project_name, root)
        print(f"[created] project {project.slug}")


COMMAND_HANDLERS = {
    "init.run": _handle_init,
}
