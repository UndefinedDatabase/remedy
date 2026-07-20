"""F4 (round 29) — git porcelain paths are parsed NUL-safely, so the leading status column is never
mistaken for part of the path. ``_dirty_files`` reconstructs ``XY PATH`` records from
``git status --porcelain=v1 -z`` and ``_dirty_line_path`` returns the EXACT repository-relative path
for staged/unstaged/deleted/untracked/renamed/copied entries, including paths with spaces and unicode.
"""
from __future__ import annotations

import contextlib
import importlib.util
import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_git", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git required")


def _git(repo, *args):
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


@contextlib.contextmanager
def _in(repo):
    prev = os.getcwd()
    os.chdir(repo)
    try:
        yield
    finally:
        os.chdir(prev)


def _repo(tmp_path):
    repo = tmp_path / "r"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    return repo


def _paths(repo):
    with _in(repo):
        return sorted(_brm._dirty_line_path(x) for x in _brm._dirty_files())


class TestPorcelainPaths:
    def test_parser_preserves_status_and_full_path(self):
        recs = _brm._parse_status_z(" M scripts/app.py\0?? new.py\0")
        assert recs == [(" M", "scripts/app.py"), ("??", "new.py")]
        # the classic regression: the first path character is intact.
        assert _brm._dirty_line_path(" M scripts/app.py") == "scripts/app.py"

    def test_unstaged_modify(self, tmp_path):
        repo = _repo(tmp_path)
        (repo / "app.py").write_text("x\n")
        _git(repo, "add", "-A"); _git(repo, "commit", "-qm", "c")
        (repo / "app.py").write_text("y\n")
        assert _paths(repo) == ["app.py"]

    def test_staged_modify_and_delete(self, tmp_path):
        repo = _repo(tmp_path)
        (repo / "a.py").write_text("1\n"); (repo / "b.py").write_text("2\n")
        _git(repo, "add", "-A"); _git(repo, "commit", "-qm", "c")
        (repo / "a.py").write_text("9\n"); _git(repo, "add", "a.py")   # M  a.py (staged)
        _git(repo, "rm", "-q", "b.py")                                  # D  b.py (staged)
        assert _paths(repo) == ["a.py", "b.py"]

    def test_untracked(self, tmp_path):
        repo = _repo(tmp_path)
        (repo / "seed").write_text("x\n"); _git(repo, "add", "-A"); _git(repo, "commit", "-qm", "c")
        (repo / "fresh.py").write_text("z\n")
        assert _paths(repo) == ["fresh.py"]
        with _in(repo):
            assert _brm._has_untracked_files() is True

    def test_renamed_uses_new_path(self, tmp_path):
        repo = _repo(tmp_path)
        (repo / "old_name.py").write_text("stable content used for rename detection\n" * 3)
        _git(repo, "add", "-A"); _git(repo, "commit", "-qm", "c")
        _git(repo, "mv", "old_name.py", "new_name.py")
        assert _paths(repo) == ["new_name.py"]

    def test_copied_uses_new_path(self, tmp_path):
        repo = _repo(tmp_path)
        body = "a copied body long enough for copy detection\n" * 5
        (repo / "orig.py").write_text(body)
        _git(repo, "add", "-A"); _git(repo, "commit", "-qm", "c")
        (repo / "dup.py").write_text(body)
        _git(repo, "add", "-A")
        with _in(repo):
            # -z status with copy detection; whatever git reports, the NEW path is recovered whole.
            recs = _brm._git_status_records()
            paths = {p for _, p in recs}
        assert "dup.py" in paths and all(not p.startswith("up.py") for p in paths)

    def test_path_with_spaces(self, tmp_path):
        repo = _repo(tmp_path)
        (repo / "a file.py").write_text("x\n")
        _git(repo, "add", "-A"); _git(repo, "commit", "-qm", "c")
        (repo / "a file.py").write_text("y\n")
        assert _paths(repo) == ["a file.py"]

    def test_unicode_path(self, tmp_path):
        repo = _repo(tmp_path)
        name = "café_ω.py"
        (repo / name).write_text("x\n")
        assert _paths(repo) == [name]
