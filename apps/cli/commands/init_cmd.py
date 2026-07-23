"""Handler for ``remedy init`` — register a git repo as a Remedy project."""

from __future__ import annotations

import json as _json
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


def _build_runtime_config(root: Path) -> tuple[str, str | None]:
    """Return (runtime_config_text, skip_message_or_None)."""
    from packages.runtimes.runtime_config import detect_runtimes

    found = detect_runtimes(root)
    if len(found) == 1:
        rt = found[0]
        text = _RUNTIME_ACTIVE.format(
            cmd=_format_toml_list(rt.spec.cmd),
            cwd=f'"{Path(rt.spec.cwd).relative_to(root)}"'
            if Path(rt.spec.cwd) != root
            else '"."',
            port=rt.spec.port,
        )
        return text, None
    return _RUNTIME_SKIP, "skipped runtime autodetect (no known framework marker)"


def _ensure_ignore_entry(root: Path, entry: str) -> str:
    """Add *entry* to .git/info/exclude if missing. Return status word."""
    import subprocess

    proc = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        cwd=str(root), capture_output=True, text=True, timeout=10,
    )
    if proc.returncode != 0:
        return "skipped"
    git_dir_raw = proc.stdout.strip()
    git_dir = Path(git_dir_raw) if Path(git_dir_raw).is_absolute() else root / git_dir_raw
    exclude = git_dir / "info" / "exclude"
    try:
        existing = exclude.read_text(encoding="utf-8") if exclude.is_file() else ""
        if entry not in existing.split():
            exclude.parent.mkdir(parents=True, exist_ok=True)
            with exclude.open("a", encoding="utf-8") as fh:
                if existing and not existing.endswith("\n"):
                    fh.write("\n")
                fh.write(f"{entry}\n")
            return "created"
        return "exists"
    except OSError:
        return "skipped"


def _ignore_entries(root: Path) -> list[str]:
    """Return ignore patterns for data-dir and workspaces if inside repo."""
    from packages.orchestration.data_paths import resolve_data_root, workspaces_dir
    from packages.orchestration.worktrees import WORKTREE_DIRNAME

    entries = [f"{WORKTREE_DIRNAME}/"]
    data_root = resolve_data_root()
    try:
        rel = data_root.resolve().relative_to(root.resolve())
        entries.append(f"{rel}/")
        ws = workspaces_dir(data_root)
        ws_rel = ws.resolve().relative_to(root.resolve())
        if str(ws_rel) != str(rel):
            entries.append(f"{ws_rel}/")
    except ValueError:
        pass
    return entries


def _handle_init(args: argparse.Namespace) -> None:
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.project_registry import (
        register_project_repo,
        resolve_project,
    )
    from packages.orchestration.worktrees import is_git_repo, repo_root
    from packages.runtimes.runtime_config import CONFIG_RELPATH

    print_only = getattr(args, "print_only", False)
    json_mode = getattr(args, "json", False)

    cwd = Path.cwd()

    if not is_git_repo(cwd):
        if json_mode:
            _json.dump({"error": "not a git repository"}, sys.stdout)
            print()
        else:
            print(
                "remedy init requires a git repository — run `git init` first.",
                file=sys.stderr,
            )
        sys.exit(4)

    root = repo_root(cwd)
    project_name = getattr(args, "project_name", None) or root.name
    steps: list[dict[str, str]] = []

    config_file = root / _CONFIG_FILENAME
    if config_file.is_file():
        steps.append({"status": "exists", "target": f"config {_CONFIG_FILENAME}"})
    else:
        if not print_only:
            config_file.write_text(_CORE_TEMPLATE, encoding="utf-8")
        steps.append({"status": "created", "target": f"config {_CONFIG_FILENAME}",
                       "content": _CORE_TEMPLATE})

    runtime_file = root / CONFIG_RELPATH
    if runtime_file.is_file():
        steps.append({"status": "exists", "target": f"runtime {CONFIG_RELPATH}"})
    else:
        content, skip_msg = _build_runtime_config(root)
        if not print_only:
            runtime_file.parent.mkdir(parents=True, exist_ok=True)
            runtime_file.write_text(content, encoding="utf-8")
        steps.append({"status": "created", "target": f"runtime {CONFIG_RELPATH}",
                       "content": content})
        if skip_msg:
            steps.append({"status": "skipped", "target": skip_msg})

    for entry in _ignore_entries(root):
        if print_only:
            steps.append({"status": "created", "target": f"ignore {entry}"})
        else:
            status = _ensure_ignore_entry(root, entry)
            steps.append({"status": status, "target": f"ignore {entry}"})

    if print_only:
        slug = project_name
        project_id = "(dry-run)"
    else:
        existing = resolve_project(cwd)
        if existing is not None:
            steps.append({"status": "exists", "target": f"project {existing.slug}"})
            slug = existing.slug
            project_id = str(existing.id)
        else:
            project = register_project_repo(project_name, root)
            steps.append({"status": "created", "target": f"project {project.slug}"})
            slug = project.slug
            project_id = str(project.id)

    data_root = resolve_data_root()
    summary = {
        "slug": slug,
        "uuid": project_id,
        "config": str(config_file),
        "runtime_config": str(runtime_file),
        "data_root": str(data_root),
        "repo_root": str(root),
        "next": 'remedy do "<your first mission>"',
    }

    if json_mode:
        _json.dump({"steps": steps, "summary": summary}, sys.stdout, indent=2)
        print()
    else:
        for step in steps:
            line = f"[{step['status']}] {step['target']}"
            print(line)
            if "content" in step and print_only:
                for cl in step["content"].splitlines():
                    print(f"  | {cl}")

        print()
        print(f"  slug:           {slug}")
        print(f"  uuid:           {project_id}")
        print(f"  config:         {config_file}")
        print(f"  runtime_config: {runtime_file}")
        print(f"  data_root:      {data_root}")
        if root != cwd:
            print(f"  repo_root:      {root}")
        print()
        print('  Next: remedy do "<your first mission>"')


COMMAND_HANDLERS = {
    "init.run": _handle_init,
}
