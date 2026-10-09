"""Tests for `packages/orchestration/structure_measure.py` and `remedy integrity structure`
(F300 T001, DECISION F300 D1)."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from packages.orchestration.structure_measure import (
    NotAGitRepository,
    count_lines,
    function_sizes,
    measure_repository,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(cwd), check=True, timeout=60, capture_output=True)


def _init_repo(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@e.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")


def _commit_all(root: Path, message: str = "commit") -> None:
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", message)


def _fn(name: str, lines: int, indent: str = "", head: str = "def") -> str:
    """A function literal of exactly `lines` lines (the `def`/decorator line counted)."""
    return f"{indent}{head} {name}():\n" + "".join(f"{indent}    x = {i}\n" for i in range(lines - 1))


def _digest_tree(root: Path) -> str:
    """sha256 over every file's path and bytes outside `.git`, for the unchanged-tree proof."""
    hasher = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts):
        hasher.update(str(path.relative_to(root)).encode("utf-8"))
        hasher.update(path.read_bytes())
    return hasher.hexdigest()


def _status(root: Path) -> str:
    return subprocess.run(["git", "status", "--porcelain"], cwd=str(root), capture_output=True,
                           text=True, timeout=60, check=True).stdout


class TestAcceptance:
    def test_measures_and_names_both_entries_leaving_the_tree_unchanged(self, tmp_path):
        root = tmp_path / "repo"
        _init_repo(root)
        (root / "big.py").write_text(_fn("big", 101), encoding="utf-8")
        (root / "notes.txt").write_text("n\n" * 1001, encoding="utf-8")
        _commit_all(root)

        before_digest = _digest_tree(root)
        before_status = _status(root)

        measure = measure_repository(root)

        assert measure.files_measured == 2
        assert measure.functions_measured == 1
        assert [f.name for f in measure.large_functions] == ["big"]
        assert measure.large_functions[0].lines == 101
        assert [f.path for f in measure.large_files] == ["notes.txt"]
        assert measure.large_files[0].lines == 1001

        assert _digest_tree(root) == before_digest
        assert _status(root) == before_status


class TestStrictlyAbove:
    def test_exactly_at_the_limit_is_not_named_one_below_is(self, tmp_path):
        root = tmp_path / "repo"
        _init_repo(root)
        (root / "edge.py").write_text(_fn("edge", 100), encoding="utf-8")
        (root / "edge.txt").write_text("e\n" * 1000, encoding="utf-8")
        _commit_all(root)

        measure = measure_repository(root)
        assert measure.large_functions == ()
        assert measure.large_files == ()

        lowered = measure_repository(root, function_limit=99, file_limit=999)
        assert [f.name for f in lowered.large_functions] == ["edge"]
        assert [f.path for f in lowered.large_files] == ["edge.txt"]

    def test_a_limit_of_zero_raises_value_error(self, tmp_path):
        root = tmp_path / "repo"
        _init_repo(root)
        (root / "a.txt").write_text("x\n", encoding="utf-8")
        _commit_all(root)

        with pytest.raises(ValueError):
            measure_repository(root, function_limit=0)
        with pytest.raises(ValueError):
            measure_repository(root, file_limit=0)


class TestNames:
    def test_method_nested_function_and_a_repeated_name(self):
        source = (
            "class K:\n"
            "    def method():\n"
            "        pass\n"
            "def outer():\n"
            "    def inner():\n"
            "        pass\n"
            "def again():\n"
            "    pass\n"
            "def again():\n"
            "    pass\n"
        )
        names = {f.name for f in function_sizes(source, "m.py")}
        assert names == {"K.method", "outer", "outer.inner", "again", "again#2"}

    def test_a_decorated_functions_line_is_its_def_line_and_async_def_is_measured(self):
        source = (
            "@deco\n"
            "def plain():\n"
            "    pass\n"
            "async def waiter():\n"
            "    pass\n"
        )
        by_name = {f.name: f for f in function_sizes(source, "m.py")}
        assert by_name["plain"].line == 2
        assert by_name["waiter"].lines == 2


class TestCountLines:
    @pytest.mark.parametrize("text, expected", [
        ("", 0),
        ("a", 1),
        ("a\n", 1),
        ("a\nb", 2),
        ("a\x0cb\n", 1),
    ])
    def test_count_lines(self, text, expected):
        assert count_lines(text) == expected


class TestSkippedAndListed:
    def test_nul_non_utf8_symlink_and_untracked_are_skipped_broken_py_is_unparsed_but_counted(
        self, tmp_path,
    ):
        root = tmp_path / "repo"
        _init_repo(root)
        (root / "nul.txt").write_bytes(b"a\0b\n")
        (root / "latin.txt").write_bytes("caf\xe9\n".encode("latin-1"))
        (root / "edge.txt").write_text("e\n", encoding="utf-8")
        (root / "broken.py").write_text("def broken(:\n    z = 1\n", encoding="utf-8")
        os.symlink("edge.txt", root / "link.txt")
        _commit_all(root)
        (root / "untracked.py").write_text(_fn("loose", 5), encoding="utf-8")

        measure = measure_repository(root)
        assert measure.files_measured == 2  # edge.txt, broken.py
        assert measure.unparsed == ("broken.py",)


class TestSubfolderScoping:
    def test_a_subfolder_as_folder_or_as_pathspec_measures_only_its_files(self, tmp_path):
        root = tmp_path / "repo"
        _init_repo(root)
        (root / "top.py").write_text(_fn("top_fn", 150), encoding="utf-8")
        pkg = root / "pkg"
        pkg.mkdir()
        (pkg / "inner.py").write_text(_fn("inner_fn", 150), encoding="utf-8")
        _commit_all(root)

        by_folder = measure_repository(pkg)
        by_pathspec = measure_repository(root, paths=("pkg",))

        for measure in (by_folder, by_pathspec):
            assert measure.files_measured == 1
            assert [f.path for f in measure.large_functions] == ["pkg/inner.py"]
            assert measure.root == str(root.resolve())


class TestNotAGitRepository:
    def test_a_folder_outside_any_repository_raises(self, tmp_path, monkeypatch):
        outside = tmp_path / "lonely"
        outside.mkdir()
        monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
        with pytest.raises(NotAGitRepository):
            measure_repository(outside)


class TestTheHandler:
    def _run(self, capsys, **kwargs):
        from apps.cli.commands.integrity_cmd import _cmd_integrity_structure

        namespace = argparse.Namespace(path=None, function_limit="100", file_limit="1000", json=True)
        for key, value in kwargs.items():
            setattr(namespace, key, value)
        code = 0
        try:
            _cmd_integrity_structure(namespace)
        except SystemExit as exc:
            code = exc.code
        return code, capsys.readouterr().out

    def test_json_envelope_has_the_measure_as_dict_keys(self, tmp_path, capsys):
        root = tmp_path / "repo"
        _init_repo(root)
        (root / "big.py").write_text(_fn("big", 101), encoding="utf-8")
        (root / "notes.txt").write_text("n\n" * 1001, encoding="utf-8")
        _commit_all(root)

        code, out = self._run(capsys, path=str(root))
        assert code == 0
        document = json.loads(out)
        assert document["ok"] is True
        assert set(document) >= {"root", "limits", "files_measured", "functions_measured",
                                  "large_functions", "large_files", "unparsed"}

    def test_text_mode_prints_the_rendered_lines(self, tmp_path, capsys):
        root = tmp_path / "repo"
        _init_repo(root)
        (root / "big.py").write_text(_fn("big", 101), encoding="utf-8")
        (root / "notes.txt").write_text("n\n" * 1001, encoding="utf-8")
        _commit_all(root)

        code, out = self._run(capsys, path=str(root), json=False)
        assert code == 0
        assert "Functions above 100 lines: 1" in out
        assert "Files above 1000 lines: 1" in out
        assert "big.py:1  big" in out
        assert "notes.txt" in out

    @pytest.mark.parametrize("value", ["0", "x", "-3", "1.5", "\u00b2"])
    def test_invalid_limits_exit_2(self, tmp_path, capsys, value):
        code, out = self._run(capsys, path=str(tmp_path), function_limit=value)
        assert code == 2
        assert json.loads(out)["error"] == "invalid_limit"

    def test_a_missing_folder_exits_2(self, tmp_path, capsys):
        code, out = self._run(capsys, path=str(tmp_path / "absent"))
        assert code == 2
        assert json.loads(out)["error"] == "path_not_found"

    def test_a_folder_in_no_repository_exits_4(self, tmp_path, capsys, monkeypatch):
        outside = tmp_path / "lonely"
        outside.mkdir()
        monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
        code, out = self._run(capsys, path=str(outside))
        assert code == 4
        assert json.loads(out)["error"] == "not_a_git_repo"


class TestReachedAsAUser:
    def test_the_grouped_cli_runs_the_command_and_prints_expected_entries_only(self, tmp_path):
        root = tmp_path / "repo"
        _init_repo(root)
        (root / "big.py").write_text(_fn("big", 150), encoding="utf-8")
        (root / "small.py").write_text(_fn("small", 10), encoding="utf-8")
        _commit_all(root)

        proc = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "integrity", "structure", "--path", str(root),
             "--function-limit", "100"],
            cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=120,
        )
        assert proc.returncode == 0
        assert "big" in proc.stdout
        assert "small" not in proc.stdout
