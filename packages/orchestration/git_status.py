"""
Git Safety Readiness v1 — safe read-only git status reader.

Uses subprocess with list argv (no shell=True, no shell injection).
READ-ONLY only — no commit, no push, no PR, no checkout.

Public API::

    read_git_status(repo_path) -> GitRepoStatus
    export_git_status_json(status) -> dict
    summarize_git_status(status) -> str
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class GitRepoStatus:
    """Immutable snapshot of git repo state."""

    repo_path: str
    is_git_repo: bool
    current_branch: str
    head_sha: str
    is_clean: bool
    modified_files: tuple[str, ...]
    untracked_files: tuple[str, ...]
    staged_files: tuple[str, ...]
    has_upstream: bool
    upstream_branch: str
    ahead_count: int
    behind_count: int
    error: str


def _run_git(repo_path: str, *args: str, timeout: int = 10) -> tuple[str, str, int]:
    """Run a git command safely. Returns (stdout, stderr, returncode)."""
    cmd = ["git", "-C", repo_path] + list(args)
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "timeout", 1
    except FileNotFoundError:
        return "", "git not found", 127


def read_git_status(repo_path: str) -> GitRepoStatus:
    """Read git repository status. Safe, read-only, no shell=True."""
    repo = Path(repo_path)
    if not repo.is_dir():
        return GitRepoStatus(
            repo_path=repo_path, is_git_repo=False, current_branch="",
            head_sha="", is_clean=False, modified_files=(), untracked_files=(),
            staged_files=(), has_upstream=False, upstream_branch="",
            ahead_count=0, behind_count=0, error=f"not a directory: {repo_path}",
        )

    # Check if git repo
    out, err, rc = _run_git(repo_path, "rev-parse", "--is-inside-work-tree")
    if rc != 0:
        return GitRepoStatus(
            repo_path=repo_path, is_git_repo=False, current_branch="",
            head_sha="", is_clean=False, modified_files=(), untracked_files=(),
            staged_files=(), has_upstream=False, upstream_branch="",
            ahead_count=0, behind_count=0, error=err or "not a git repo",
        )

    # Current branch
    branch_out, _, _ = _run_git(repo_path, "rev-parse", "--abbrev-ref", "HEAD")
    current_branch = branch_out or "HEAD"

    # HEAD sha
    sha_out, _, _ = _run_git(repo_path, "rev-parse", "--short", "HEAD")
    head_sha = sha_out or ""

    # Porcelain status
    status_out, _, _ = _run_git(repo_path, "status", "--porcelain")
    modified = []
    untracked = []
    staged = []
    for line in status_out.splitlines():
        if len(line) < 3:
            continue
        x, y = line[0], line[1]
        fname = line[3:]
        if x == "?":
            untracked.append(fname)
        elif x in ("M", "A", "D", "R", "C"):
            staged.append(fname)
        if y in ("M", "D"):
            modified.append(fname)

    is_clean = len(modified) == 0 and len(untracked) == 0 and len(staged) == 0

    # Upstream info
    upstream_out, _, up_rc = _run_git(
        repo_path, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}",
    )
    has_upstream = up_rc == 0
    upstream_branch = upstream_out if has_upstream else ""

    ahead = 0
    behind = 0
    if has_upstream:
        ab_out, _, _ = _run_git(repo_path, "rev-list", "--left-right", "--count", "HEAD...@{u}")
        parts = ab_out.split()
        if len(parts) == 2:
            try:
                ahead = int(parts[0])
                behind = int(parts[1])
            except ValueError:
                pass

    return GitRepoStatus(
        repo_path=repo_path,
        is_git_repo=True,
        current_branch=current_branch,
        head_sha=head_sha,
        is_clean=is_clean,
        modified_files=tuple(modified),
        untracked_files=tuple(untracked),
        staged_files=tuple(staged),
        has_upstream=has_upstream,
        upstream_branch=upstream_branch,
        ahead_count=ahead,
        behind_count=behind,
        error="",
    )


def export_git_status_json(status: GitRepoStatus) -> dict[str, Any]:
    """Export as safe JSON dict."""
    return {
        "version": 1,
        "repo_path": status.repo_path,
        "is_git_repo": status.is_git_repo,
        "current_branch": status.current_branch,
        "head_sha": status.head_sha,
        "is_clean": status.is_clean,
        "modified_files": list(status.modified_files),
        "untracked_files": list(status.untracked_files),
        "staged_files": list(status.staged_files),
        "has_upstream": status.has_upstream,
        "upstream_branch": status.upstream_branch,
        "ahead_count": status.ahead_count,
        "behind_count": status.behind_count,
        "error": status.error,
    }


def summarize_git_status(status: GitRepoStatus) -> str:
    """Human-readable summary."""
    if not status.is_git_repo:
        return f"Not a git repo: {status.repo_path} ({status.error})"
    lines = [
        f"Git Status: {status.repo_path}",
        f"  Branch: {status.current_branch} ({status.head_sha})",
        f"  Clean: {status.is_clean}",
    ]
    if status.modified_files:
        lines.append(f"  Modified: {len(status.modified_files)} files")
    if status.untracked_files:
        lines.append(f"  Untracked: {len(status.untracked_files)} files")
    if status.staged_files:
        lines.append(f"  Staged: {len(status.staged_files)} files")
    if status.has_upstream:
        lines.append(f"  Upstream: {status.upstream_branch} (ahead={status.ahead_count}, behind={status.behind_count})")
    return "\n".join(lines)
