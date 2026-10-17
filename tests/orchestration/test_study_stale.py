"""Audit P1-5: a recorded study is reused only while the repository still looks like it did."""
from __future__ import annotations

import subprocess
from pathlib import Path

from packages.orchestration.study import STUDY_STALE_CHANGED_PATHS, study_stale_reason


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-c", "user.email=t@example.com", "-c", "user.name=t",
                           "-c", "commit.gpgsign=false", *args], cwd=repo, check=True,
                          capture_output=True, text=True).stdout.strip()


def _repo(tmp_path: Path) -> Path:
    repo = tmp_path / "r"
    repo.mkdir()
    _git(repo, "init", "-q")
    (repo / "README.md").write_text("# r\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "init")
    return repo


def _commit(repo: Path, **files: str) -> str:
    for name, text in files.items():
        (repo / name.replace("__", "/")).parent.mkdir(parents=True, exist_ok=True)
        (repo / name.replace("__", "/")).write_text(text)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "change")
    return _git(repo, "rev-parse", "HEAD")


def test_the_same_head_is_never_stale(tmp_path):
    repo = _repo(tmp_path)
    assert study_stale_reason(str(repo), _git(repo, "rev-parse", "HEAD")) == ""


def test_a_small_source_change_keeps_the_study(tmp_path):
    repo = _repo(tmp_path)
    studied = _git(repo, "rev-parse", "HEAD")
    _commit(repo, README_extra="more\n")
    assert study_stale_reason(str(repo), studied) == ""


def test_a_changed_dependency_file_makes_the_study_stale(tmp_path):
    repo = _repo(tmp_path)
    studied = _git(repo, "rev-parse", "HEAD")
    _commit(repo, sub__notes_txt="not a manifest\n")
    assert study_stale_reason(str(repo), studied) == ""
    _commit(repo, **{"package.json": "{}\n"})
    assert "package.json changed" in study_stale_reason(str(repo), studied)


def test_many_changed_paths_make_the_study_stale(tmp_path):
    repo = _repo(tmp_path)
    studied = _git(repo, "rev-parse", "HEAD")
    _commit(repo, **{f"mod{n}.py": "x = 1\n" for n in range(STUDY_STALE_CHANGED_PATHS)})
    assert "paths changed" in study_stale_reason(str(repo), studied)


def test_an_unknown_or_missing_studied_head_is_stale_and_an_empty_repository_is_not(tmp_path):
    repo = _repo(tmp_path)
    assert "no head" in study_stale_reason(str(repo), "")
    assert "not in the repository" in study_stale_reason(str(repo), "0" * 40)
    empty = tmp_path / "empty"
    empty.mkdir()
    _git(empty, "init", "-q")
    assert study_stale_reason(str(empty), "") == ""
