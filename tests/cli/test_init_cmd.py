"""Tests for ``remedy init`` (F081 T001)."""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

_CLI = [sys.executable, "-m", "apps.cli.grouped"]
_ENV = {**os.environ, "PYTHONPATH": os.getcwd()}


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


@pytest.mark.subprocess
class TestInitCmd:

    def test_fresh_repo_creates_project(self, tmp_path):
        repo = _make_git_repo(tmp_path)
        r = subprocess.run(
            [*_CLI, "init"],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=_ENV, stdin=subprocess.DEVNULL,
        )
        assert r.returncode == 0, f"stderr: {r.stderr}"
        assert "[created] project " in r.stdout

    def test_second_run_idempotent(self, tmp_path):
        repo = _make_git_repo(tmp_path)
        r1 = subprocess.run(
            [*_CLI, "init"],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=_ENV, stdin=subprocess.DEVNULL,
        )
        assert r1.returncode == 0

        mtime_before = {}
        data_dir = os.path.join(os.environ.get("REMEDY_DATA_DIR", ""), "projects")
        if os.path.isdir(data_dir):
            for f in os.listdir(data_dir):
                fp = os.path.join(data_dir, f)
                mtime_before[f] = os.path.getmtime(fp)

        r2 = subprocess.run(
            [*_CLI, "init"],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=_ENV, stdin=subprocess.DEVNULL,
        )
        assert r2.returncode == 0, f"stderr: {r2.stderr}"
        assert "[exists] project " in r2.stdout
        for line in r2.stdout.strip().splitlines():
            assert line.strip().startswith("[exists]"), f"unexpected line: {line}"

    def test_non_git_exit_4(self, tmp_path):
        plain_dir = tmp_path / "notgit"
        plain_dir.mkdir()
        r = subprocess.run(
            [*_CLI, "init"],
            capture_output=True, text=True, timeout=30,
            cwd=str(plain_dir), env=_ENV, stdin=subprocess.DEVNULL,
        )
        assert r.returncode == 4, f"expected exit 4, got {r.returncode}"
        assert "remedy init requires a git repository" in r.stderr
        contents = os.listdir(str(plain_dir))
        assert contents == [], f"non-git dir should be untouched, found: {contents}"

    def test_project_name_flag(self, tmp_path):
        repo = _make_git_repo(tmp_path)
        r = subprocess.run(
            [*_CLI, "init", "--project-name", "my-custom-name"],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=_ENV, stdin=subprocess.DEVNULL,
        )
        assert r.returncode == 0, f"stderr: {r.stderr}"
        assert "[created] project " in r.stdout

    def test_subdirectory_targets_repo_root(self, tmp_path):
        repo = _make_git_repo(tmp_path)
        subdir = repo / "deep" / "nested"
        subdir.mkdir(parents=True)
        r = subprocess.run(
            [*_CLI, "init"],
            capture_output=True, text=True, timeout=30,
            cwd=str(subdir), env=_ENV, stdin=subprocess.DEVNULL,
        )
        assert r.returncode == 0, f"stderr: {r.stderr}"
        assert "[created] project " in r.stdout

        r2 = subprocess.run(
            [*_CLI, "init"],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=_ENV, stdin=subprocess.DEVNULL,
        )
        assert r2.returncode == 0
        assert "[exists] project " in r2.stdout
