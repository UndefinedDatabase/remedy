"""F268 T005 — the quick start `remedy --help` prints runs, line by line (DECISION F268 D15).

The numbered lines are read from the rendered help, not from a copy of them, and run in
order in-process through `apps.cli.grouped.main` on a temporary git repository holding
one committed file, with the data root under `tmp_path`. Each `remedy do` line gets
exactly the fake builder and reviewer, `--no-llm` and `--no-ui` appended; no other line
gets anything. A tripwire fails the test if any model-call factory is reached, and
another if any line reads the terminal.
"""
from __future__ import annotations

import re
import shlex
import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest

from apps.cli.grouped import main

DO_LINE_SUFFIX = ["--builder-provider", "fake", "--reviewer-provider", "fake", "--no-llm", "--no-ui"]


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True).stdout


@pytest.fixture
def repo(tmp_path, monkeypatch) -> Path:
    """An UNREGISTERED git repository with one committed file, as the working directory."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    target = tmp_path / "target"
    target.mkdir()
    _git(target, "init", "-q")
    _git(target, "config", "user.email", "t@e.com")
    _git(target, "config", "user.name", "T")
    _git(target, "config", "commit.gpgsign", "false")
    (target / "README.md").write_text("# target\n")
    _git(target, "add", "-A")
    _git(target, "commit", "-qm", "init")
    monkeypatch.chdir(target)
    return target.resolve()


@pytest.fixture(autouse=True)
def no_model_call(monkeypatch):
    """Every factory that could reach a model fails the test when called."""
    def tripwire(*args, **kwargs):
        raise AssertionError("a quick-start line reached a model-call factory")

    monkeypatch.setattr("packages.orchestration.intake.make_provider_call_fn", tripwire)
    monkeypatch.setattr("packages.orchestration.intake.make_structured_call_fn", tripwire)
    monkeypatch.setattr("packages.orchestration.study.study_call_fn", tripwire)


@pytest.fixture(autouse=True)
def no_terminal_read(monkeypatch):
    """No quick-start line may wait on the terminal."""
    def tripwire(*args, **kwargs):
        raise AssertionError("a quick-start line read the terminal")

    monkeypatch.setattr("builtins.input", tripwire)


def _printed_quick_start_lines(capsys) -> list[str]:
    """The numbered lines of `remedy --help` as printed, each starting with `remedy`."""
    capsys.readouterr()
    main([])
    out = capsys.readouterr().out
    return re.findall(r"^  \d+\. (remedy .*)$", out, re.MULTILINE)


def _quick_start_argv(line: str) -> list[str]:
    """The argv a printed line runs with: its words after `remedy`, plus the suffix on a `do` line."""
    words = shlex.split(line)[1:]
    return words + DO_LINE_SUFFIX if words[0] == "do" else words


def _exit_code_of(argv: list[str]) -> int:
    try:
        main(argv)
    except SystemExit as exc:
        return 0 if exc.code is None else exc.code
    return 0


def _run_quick_start(lines: list[str], execute: Callable[[list[str]], int],
                     after_each: Callable[[int], None] = lambda _n: None) -> list[int]:
    codes = []
    for number, line in enumerate(lines, start=1):
        codes.append(execute(_quick_start_argv(line)))
        after_each(number)
    return codes


def test_every_quick_start_line_exits_0_and_leaves_the_target_as_line_one_left_it(repo, capsys):
    lines = _printed_quick_start_lines(capsys)
    assert len(lines) == 5
    status_after: dict[int, str] = {}

    def read_status(number: int) -> None:
        capsys.readouterr()
        status_after[number] = _git(repo, "status", "--porcelain")

    codes = _run_quick_start(lines, _exit_code_of, read_status)

    assert codes == [0, 0, 0, 0, 0], list(zip(lines, codes))
    assert status_after[5] == status_after[1]


def test_each_line_runs_with_its_printed_words_and_only_a_do_line_gets_the_suffix(capsys):
    lines = _printed_quick_start_lines(capsys)
    executed: list[list[str]] = []

    def record(argv: list[str]) -> int:
        executed.append(list(argv))
        return 0

    _run_quick_start(lines, record)

    suffix = ["--builder-provider", "fake", "--reviewer-provider", "fake", "--no-llm", "--no-ui"]
    assert len(executed) == len(lines) == 5
    do_lines = 0
    for line, argv in zip(lines, executed):
        words = shlex.split(line)[1:]
        assert argv[:len(words)] == words, line
        if words[0] == "do":
            do_lines += 1
            assert argv[len(words):] == suffix, line
        else:
            assert argv == words, line
    assert do_lines == 2
