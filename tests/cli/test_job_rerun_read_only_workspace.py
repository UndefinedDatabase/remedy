"""F11 (round 11) — a persisted workspace path is resolved CONTAINED under the canonical root.

The `--check-manifest` inspection these tests were written for is gone (F261 round 24 deleted
the command, F273 the candidate builder for finding R-0931). What stays is the containment rule
itself: a persisted path resolves through the canonical worktree root with anchored no-follow
traversal, and a path outside it is refused rather than believed.
"""
from __future__ import annotations

import subprocess

import pytest

from packages.orchestration.run_manifest import (
    contained_workspace_path,
)


def _git_repo(path, content="# demo"):
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(f"git init -q && git config user.email t@t && git config user.name t "
                   f"&& echo '{content}' > README.md && git add -A && git commit -qm init",
                   shell=True, cwd=path, check=True)
    return path


@pytest.fixture
def repo(tmp_path):
    return _git_repo(tmp_path / "repo")


def _live_workspace(repo, name="job-live"):
    """A real workspace under the canonical `.remedy-wt/` root."""
    ws = repo / ".remedy-wt" / name
    ws.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "worktree", "add", "-q", "--detach", str(ws)], cwd=repo,
                   check=True, capture_output=True)
    return ws


# --------------------------------------------------------------------------- containment


class TestContainment:
    def test_a_contained_workspace_resolves(self, repo):
        ws = _live_workspace(repo)
        path, state = contained_workspace_path(ws, repo)
        assert state == "ok" and path is not None

    def test_the_persisted_path_is_not_its_own_trust_root(self, repo, tmp_path):
        """The path is a claim. It is checked against the canonical root, not believed."""
        outside = _git_repo(tmp_path / "outside3")
        path, state = contained_workspace_path(outside, repo)
        assert path is None and state == "escapes"
