"""Tests for ``remedy init`` (F081 T001)."""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

_CLI = [sys.executable, "-m", "apps.cli.grouped"]


def _make_env(tmp_path):
    """Build subprocess env with REMEDY_DATA_DIR isolated to tmp_path."""
    return {
        **os.environ,
        "PYTHONPATH": os.getcwd(),
        "REMEDY_DATA_DIR": str(tmp_path / "data"),
    }


def _make_git_repo(tmp_path):
    """Create a bare git repo in tmp_path and return the path."""
    subprocess.run(
        ["git", "init", "-q", str(tmp_path)],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(tmp_path), "commit", "--allow-empty", "-m", "init", "-q"],
        check=True,
        capture_output=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
             "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"},
    )
    return tmp_path


def _snapshot_mtimes(projects_dir):
    """Return {filename: mtime} for all files in projects_dir."""
    if not os.path.isdir(projects_dir):
        return {}
    return {f: os.path.getmtime(os.path.join(projects_dir, f))
            for f in os.listdir(projects_dir)}


@pytest.mark.subprocess
class TestInitCmd:

    def test_fresh_repo_creates_project(self, tmp_path):
        repo = _make_git_repo(tmp_path / "repo")
        env = _make_env(tmp_path)
        r = subprocess.run(
            [*_CLI, "init"],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert r.returncode == 0, f"stderr: {r.stderr}"
        assert "[created] project " in r.stdout

    def test_second_run_idempotent(self, tmp_path):
        repo = _make_git_repo(tmp_path / "repo")
        env = _make_env(tmp_path)
        r1 = subprocess.run(
            [*_CLI, "init"],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert r1.returncode == 0

        projects = str(tmp_path / "data" / "projects")
        mtime_before = _snapshot_mtimes(projects)
        assert mtime_before, "first run should have created project files"

        r2 = subprocess.run(
            [*_CLI, "init"],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert r2.returncode == 0, f"stderr: {r2.stderr}"
        assert "[exists] project " in r2.stdout
        for line in r2.stdout.strip().splitlines():
            assert line.strip().startswith("[exists]"), f"unexpected line: {line}"

        mtime_after = _snapshot_mtimes(projects)
        assert mtime_before == mtime_after, (
            f"second run modified project files: before={mtime_before}, after={mtime_after}"
        )

    def test_non_git_exit_4(self, tmp_path):
        plain_dir = tmp_path / "notgit"
        plain_dir.mkdir()
        env = _make_env(tmp_path)
        r = subprocess.run(
            [*_CLI, "init"],
            capture_output=True, text=True, timeout=30,
            cwd=str(plain_dir), env=env, stdin=subprocess.DEVNULL,
        )
        assert r.returncode == 4, f"expected exit 4, got {r.returncode}"
        assert "remedy init requires a git repository" in r.stderr
        contents = os.listdir(str(plain_dir))
        assert contents == [], f"non-git dir should be untouched, found: {contents}"

    def test_project_name_flag(self, tmp_path):
        repo = _make_git_repo(tmp_path / "repo")
        env = _make_env(tmp_path)
        r = subprocess.run(
            [*_CLI, "init", "--project-name", "my-custom-name"],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert r.returncode == 0, f"stderr: {r.stderr}"
        assert "[created] project " in r.stdout

    def test_subdirectory_targets_repo_root(self, tmp_path):
        repo = _make_git_repo(tmp_path / "repo")
        env = _make_env(tmp_path)
        subdir = repo / "deep" / "nested"
        subdir.mkdir(parents=True)
        r = subprocess.run(
            [*_CLI, "init"],
            capture_output=True, text=True, timeout=30,
            cwd=str(subdir), env=env, stdin=subprocess.DEVNULL,
        )
        assert r.returncode == 0, f"stderr: {r.stderr}"
        assert "[created] project " in r.stdout

        r2 = subprocess.run(
            [*_CLI, "init"],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert r2.returncode == 0
        assert "[exists] project " in r2.stdout
