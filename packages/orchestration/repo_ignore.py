"""The `.git/info/exclude` entries Remedy adds to a repository it works in.

Shared by ``remedy init`` (``apps/cli/commands/init_cmd.py``) and the init step
of ``remedy do`` (``packages/orchestration/do_sequence.py``), so both keep the
worktree directory and an in-repository data directory out of ``git status``
the same way (DECISION F268 D2).
"""

from __future__ import annotations

from pathlib import Path


def ensure_ignore_entry(root: Path, entry: str) -> str:
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


def ignore_entries(root: Path) -> list[str]:
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
