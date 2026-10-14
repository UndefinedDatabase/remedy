"""Reusable side-effect counters for a `remedy do` run (F055, DECISION F055 D1).

The feature file's Orchestrator brief asks for these as test utilities any round or
feature can reuse: a rehearsal's whole claim is that none of these seams fire, and a
real run's whole claim is that some of them do. Each counting function monkeypatches
the seam IN PLACE — the module attribute a caller looks up at call time — with a
wrapper that records the call and then calls the original, so behaviour is unchanged
and only the count is new.
"""

from __future__ import annotations

import collections
import hashlib
import subprocess
from pathlib import Path


def count_role_provider_builds(monkeypatch) -> collections.Counter:
    """Count every provider a run builds, keyed by its `role`, at the seam a run calls:
    `_create_provider_with_cwd`, the shim that always calls `create_role_provider`."""
    from packages.orchestration import pingpong_loop

    counts: collections.Counter = collections.Counter()
    original = pingpong_loop._create_provider_with_cwd

    def counting(*args, **kwargs):
        counts[kwargs.get("role", "")] += 1
        return original(*args, **kwargs)

    monkeypatch.setattr(pingpong_loop, "_create_provider_with_cwd", counting)
    return counts


def count_applicator_calls(monkeypatch) -> collections.Counter:
    """Count `apply_job`, `apply_patch_intent` and `_strict_apply_to_workspace`, by name."""
    from packages.orchestration import job_apply, patch_apply, pingpong_job

    counts: collections.Counter = collections.Counter()

    def _wrap(module: object, name: str) -> None:
        original = getattr(module, name)

        def counting(*args, **kwargs):
            counts[name] += 1
            return original(*args, **kwargs)

        monkeypatch.setattr(module, name, counting)

    _wrap(job_apply, "apply_job")
    _wrap(patch_apply, "apply_patch_intent")
    _wrap(pingpong_job, "_strict_apply_to_workspace")
    return counts


def count_worktree_creations(monkeypatch) -> list[str]:
    """Record each `worktrees.create`'s job id, in call order."""
    from packages.orchestration import worktrees

    created: list[str] = []
    original = worktrees.create

    def counting(job_id, *args, **kwargs):
        created.append(job_id)
        return original(job_id, *args, **kwargs)

    monkeypatch.setattr(worktrees, "create", counting)
    return created


def snapshot_repository_state(repo: Path) -> dict[str, object]:
    """A repository's state: its HEAD, refs, status, worktrees, stash, and every tracked-or-not
    file's sha256 outside `.git`, keyed by its path relative to `repo`."""

    def git(*args: str) -> str:
        return subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                              text=True, check=True).stdout

    files: dict[str, str] = {}
    for path in sorted(repo.rglob("*")):
        if not path.is_file():
            continue
        if ".git" in path.relative_to(repo).parts:
            continue
        files[str(path.relative_to(repo))] = hashlib.sha256(path.read_bytes()).hexdigest()

    return {
        "head": git("rev-parse", "HEAD"),
        "refs": git("for-each-ref"),
        "status": git("status", "--porcelain=v1", "--untracked-files=all", "--ignored"),
        "worktrees": git("worktree", "list", "--porcelain"),
        "stash": git("stash", "list"),
        "files": files,
    }
