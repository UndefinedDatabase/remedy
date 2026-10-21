"""`build_builder_context`: the structural move (C2) answers exactly what `build_repo_context`
always did, and the `read` seam (C3) refuses before a worktree is ever touched (F141 round 2,
DECISION F141 D2).
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from packages.orchestration import pingpong_loop as PL
from packages.orchestration import worktrees as W
from packages.orchestration.builder_context import build_builder_context
from packages.orchestration.data_paths import job_dir, jobs_dir
from packages.orchestration.permission_matrix import (
    JOB_LEVEL_FILENAME,
    PERMISSION_DENY,
    PERMISSION_MATRIX,
    PermissionRefusedError,
)
from packages.orchestration.pingpong_loop import build_repo_context, load_run, run_pingpong


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True).stdout


@pytest.fixture
def repo(tmp_path) -> Path:
    """A plain folder with one file: enough for `build_repo_context`'s own tree walk."""
    r = tmp_path / "repo"
    r.mkdir()
    (r / "a.txt").write_text("hello\n")
    return r


@pytest.fixture
def git_repo(tmp_path) -> Path:
    """A real git repository, for the `run_pingpong` path, which needs a worktree."""
    r = tmp_path / "git_repo"
    r.mkdir()
    _git(r, "init", "-q")
    _git(r, "config", "user.email", "t@e.com")
    _git(r, "config", "user.name", "T")
    _git(r, "config", "commit.gpgsign", "false")
    (r / "a.txt").write_text("v1\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "init")
    return r


def _capture_worktree(monkeypatch) -> dict:
    """Record the handle the loop creates, so a test can read the run id back (mirrors
    tests/orchestration/test_worktree_cleanup_paths.py)."""
    seen: dict = {}
    real_create = W.create

    def spy(job_id, r):
        h = real_create(job_id, r)
        seen["handle"] = h
        return h

    monkeypatch.setattr(W, "create", spy)
    return seen


def test_default_path_matches_build_repo_context_and_pins_l2(repo):
    folder = job_dir("job-1")
    folder.mkdir(parents=True)

    expected = build_repo_context(str(repo), "goal", mentioned_files=None)
    got = build_builder_context(
        repo_path=str(repo), goal="goal", mentioned_files=None,
        compiled_context_paths=None, compiled_context_candidates=None,
        compiled_context_token_budget=None, context_record_dir=None, job_id="job-1",
    )

    assert got == expected
    record = json.loads((folder / JOB_LEVEL_FILENAME).read_text(encoding="utf-8"))
    assert record["level"] == "L2"


def test_a_denied_read_refuses_before_build_repo_context_is_ever_called(repo, monkeypatch):
    calls: list = []

    def spy(*a, **kw):
        calls.append((a, kw))
        raise AssertionError("build_repo_context must not be called")

    monkeypatch.setattr(PL, "build_repo_context", spy)
    monkeypatch.setitem(PERMISSION_MATRIX, ("read", "L2"), PERMISSION_DENY)

    with pytest.raises(PermissionRefusedError) as excinfo:
        build_builder_context(
            repo_path=str(repo), goal="goal", mentioned_files=None,
            compiled_context_paths=None, compiled_context_candidates=None,
            compiled_context_token_budget=None, context_record_dir=None,
        )

    assert "(read, L2) = deny" in str(excinfo.value)
    assert calls == []


def test_run_pingpong_with_a_denied_read_ends_context_error(git_repo, monkeypatch):
    seen = _capture_worktree(monkeypatch)
    monkeypatch.setitem(PERMISSION_MATRIX, ("read", "L2"), PERMISSION_DENY)

    with pytest.raises(PermissionRefusedError) as excinfo:
        run_pingpong("goal", str(git_repo), max_rounds=1)

    run_id = seen["handle"].job_id
    record = load_run(run_id)
    assert record["final_status"] == "context_error"
    assert str(excinfo.value) in record["error"]


def test_without_a_job_id_nothing_is_written_and_the_context_is_answered(repo):
    context, categories = build_builder_context(
        repo_path=str(repo), goal="goal", mentioned_files=None,
        compiled_context_paths=None, compiled_context_candidates=None,
        compiled_context_token_budget=None, context_record_dir=None,
    )

    assert context
    assert categories
    assert not jobs_dir().exists()
