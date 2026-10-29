"""F333: a failing test that was already red on the job's base commit is not the job's and does not block.

The shape is job de04ce7d2bed47b0's (operator order beweis): the builder's full Vitest run had one red
test, `tests/unit/tables-tidy-839.test.ts`, which the base commit already failed, and the reviewer blocked
on it. Real pytest runs in throwaway git repositories; no model call, no real job.
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from packages.orchestration import client_story
from packages.orchestration import project_test_baseline as B
from packages.orchestration import verified_repair as V
from packages.orchestration.changed_test_selection import narrowed_test_argv
from packages.orchestration.client_story_words import story_problems
from packages.orchestration.dod_gate import _evidence_json
from packages.orchestration.dod_runners import STATUS_FAILED, STATUS_PASSED, run_check
from packages.orchestration.dod_schema import DoDCheck
from packages.orchestration.pingpong_provider import ReviewerOutput, ReviewFinding
from packages.orchestration.project_tests import ProjectTestCommand
from packages.orchestration.review_scope_rules import settle_review_findings

_RED = "tests/unit/tables-tidy-839.test.ts > T12_F837: the writing moon moves while she writes"
PYTEST = ProjectTestCommand(argv=("python3", "-m", "pytest", "-p", "no:cacheprovider", "tests", "-q"),
                            source="tests_folder")


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(repo), check=True, capture_output=True, text=True)


def _job_worktree(tmp_path: Path, files: dict[str, str]) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    for args in (("init", "-q", "-b", "main"), ("config", "user.email", "t@e.com"), ("config", "user.name", "T"),
                 ("config", "commit.gpgsign", "false")):
        _git(repo, *args)
    for name, text in {".gitignore": ".remedy-wt/\n", **files}.items():
        (repo / name).parent.mkdir(parents=True, exist_ok=True)
        (repo / name).write_text(text)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "base")
    worktree = repo / ".remedy-wt" / "job"
    _git(repo, "worktree", "add", "-q", str(worktree), "-b", "job")
    return worktree


_PROJECT = {
    "pkg/a.py": "A = 1\n",
    "tests/test_a.py": "from pkg.a import A\n\n\ndef test_a():\n    assert A == 1\n",
    "tests/test_old.py": "def test_old_red():\n    assert False\n\n\ndef test_old_green():\n    assert True\n",
}


def test_the_failing_tests_are_run_by_their_ids() -> None:
    assert B.failing_test_ids(frozenset({_RED, "tests/unit/tables-tidy-839.test.ts > other"})) == \
        ["tests/unit/tables-tidy-839.test.ts"]
    assert B.failing_test_ids(frozenset({"tests/test_a.py::test_x[1]"})) == ["tests/test_a.py::test_x[1]"]
    assert B.failing_test_ids(frozenset({"adds"})) is None                  # a bare test name has no id
    worktree = Path("/nonexistent")
    assert narrowed_test_argv(PYTEST, worktree, only=["tests/test_old.py::test_old_red"])[0] == [
        "python3", "-m", "pytest", "-p", "no:cacheprovider", "tests/test_old.py::test_old_red", "-q"]
    assert narrowed_test_argv(PYTEST, worktree, full=True) == (
        list(PYTEST.argv), "full run: Remedy checks a red run of the builder in full")
    with pytest.raises(ValueError, match="only for pytest and Vitest"):
        narrowed_test_argv(ProjectTestCommand(argv=("make", "test"), source="makefile"), worktree, only=["x"])


def test_a_red_the_base_shares_passes_named_and_recorded_for_the_workspace(tmp_path: Path) -> None:
    worktree = _job_worktree(tmp_path, _PROJECT)
    (worktree / "pkg" / "a.py").write_text("A = 1  # the job's change\n")
    check = DoDCheck(id="c1", kind="project_tests", spec={"full": True}, source="compiled")
    evidence = run_check(check, worktree, timeout_sec=120)
    assert evidence.status == STATUS_PASSED, evidence.output_tail
    assert evidence.preexisting == ("tests/test_old.py::test_old_red",)
    assert "already red before the job" in evidence.output_tail
    assert _evidence_json(evidence)["preexisting"] == ["tests/test_old.py::test_old_red"]
    assert B.preexisting_failures_in(worktree) == frozenset({"tests/test_old.py::test_old_red"})


def test_a_failure_new_in_the_job_blocks_as_before_and_says_so(tmp_path: Path) -> None:
    worktree = _job_worktree(tmp_path, _PROJECT)
    (worktree / "pkg" / "a.py").write_text("A = 2\n")                       # breaks test_a
    evidence = run_check(DoDCheck(id="c1", kind="project_tests", spec={"full": True}, source="compiled"),
                         worktree, timeout_sec=120)
    assert evidence.status == STATUS_FAILED
    assert evidence.baseline == "1 failing test(s) are new in this job: tests/test_a.py::test_a"
    assert evidence.preexisting == ("tests/test_old.py::test_old_red",)
    assert B.preexisting_failures_in(worktree) == frozenset()


def test_a_base_run_that_cannot_be_made_leaves_the_red_and_says_why(tmp_path: Path) -> None:
    worktree = _job_worktree(tmp_path, {"a.txt": "a\n"})
    vitest = f" FAIL  {_RED}\n      Tests  1 failed | 1 passed (2)\n"

    def broken(root: Path, ids: list[str]):
        raise ValueError("timeout")

    import dataclasses

    @dataclasses.dataclass(frozen=True)
    class Ev:
        reason: str = "nonzero_exit"
        status: str = "failed"
        command: str = "npm test"
        output_tail: str = "tail\n"
        preexisting: tuple = ()
        baseline: str = ""

    judged = B.judged_against_base(Ev(), vitest, worktree, broken)
    assert judged.status == "failed" and judged.baseline == "the base run could not be made: timeout"
    assert judged.output_tail.startswith("Not compared with the job's base commit: the base run could not")
    unnamed = B.judged_against_base(Ev(), " × adds\n Tests  1 failed | 1 passed (2)\n", worktree, broken)
    assert unnamed.baseline == "the failing tests could not be read by name and id"


def test_a_finding_only_about_tests_already_red_reads_low(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setitem(B._PREEXISTING, str(tmp_path.resolve()), frozenset({_RED}))
    on_test = ReviewFinding(id="F1", severity="high", file="tests/unit/tables-tidy-839.test.ts",
                            summary="The test command still exits with code 1.")
    exit_one = ReviewFinding(id="F2", severity="high", file="src/screens/Memory.tsx",
                             summary="The project's test command exits with code 1 because 1 test file fails.")
    real = ReviewFinding(id="F3", severity="high", file="src/screens/Memory.tsx",
                         summary="The info button lost its accessible name.")
    out = settle_review_findings(ReviewerOutput(verdict="blocked", findings=[on_test, exit_one, real]),
                                 staged_files=["src/screens/Memory.tsx"], is_fake=False, workspace=str(tmp_path))
    assert [f.severity for f in out.findings] == ["low", "low", "high"]
    clean = settle_review_findings(ReviewerOutput(verdict="blocked", findings=[
        ReviewFinding(id="F1", severity="high", summary="The test command exits with code 1.")]),
        staged_files=["x"], is_fake=False, workspace=str(tmp_path / "other"))
    assert clean.findings[0].severity == "high"                              # nothing proven pre-existing there


def test_the_reviewer_reads_the_preexisting_list_as_a_fact(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    told = "Remedy ran `vitest run` in the worktree: exit=0\n" + V.PREEXISTING_FACT.format(tests=_RED)
    calls: list[dict] = []

    def own(staging, timeout_sec, *, full=False, job_id=""):
        calls.append({"full": full, "job_id": job_id})
        return True, told

    monkeypatch.setattr(V, "remedy_round_test_run", own)
    monkeypatch.setattr("packages.orchestration.builder_test_runs.round_test_reading",
                        lambda **kw: (False, "npx vitest run: 2270 passed, 1 failed", False))
    result = SimpleNamespace(job_id="j1", run_id="r1", task_id="t1", builder_provider="claude-cli")
    rd = SimpleNamespace(round_number=1)
    passed, summary, _ = V.round_tests((True, "passed: ctr-C001", ""), None, rd, tmp_path, result)
    assert passed is True and summary.startswith("passed: ctr-C001\n") and _RED in summary
    assert "no finding against the builder may rest on them" in summary
    assert V.round_tests(None, None, rd, tmp_path, result)[0] is True     # the builder's red is checked in full
    assert calls == [{"full": True, "job_id": "j1"}, {"full": True, "job_id": "j1"}]


def test_the_story_says_the_tests_were_red_before_the_job(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    B.record_preexisting_failures("j1", frozenset({_RED}))
    assert B.load_preexisting_failures("j1") == [_RED]
    monkeypatch.setattr(client_story, "job_verification",
                        lambda plan: {"runs": [{"status": "passed"}], "status": "passed", "reason": ""})
    status, phrase = client_story._checking(SimpleNamespace(job_id="j1"), "done", "done")
    assert (status, phrase) == ("done", {"key": "failed_before_job", "args": {"n": 1}})
    steps = [{"id": i, "status": "done", "phrase": phrase if i == "checking" else None, "tasks": []}
             for i in ("reading", "planning", "building", "checking", "finished")]
    assert story_problems({"state": "done", "next": {"action": "apply"}, "steps": steps}) == []
