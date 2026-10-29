"""amend1027 F4: a red the project already had on the job's base commit is not the job's."""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from packages.orchestration.project_test_baseline import (
    REASON_PREEXISTING_FAILURES,
    failing_test_names,
    judged_against_base,
)

VITEST = """ ❯ tests/a.test.ts (2 tests | 1 failed)
     × adds 6ms
⎯⎯⎯ Failed Tests 1 ⎯⎯⎯
 FAIL  tests/a.test.ts > math > adds
      Tests  1 failed | 1 passed (2)
"""
PYTEST = "F.\nFAILED tests/test_a.py::test_x - assert 1 == 2\n1 failed, 1 passed in 0.1s\n"


@pytest.mark.parametrize(("output", "names"), [
    (VITEST, {"tests/a.test.ts > math > adds"}),
    (PYTEST, {"tests/test_a.py::test_x"}),
    (" × adds\n Tests  1 failed | 1 passed (2)\n", {"adds"}),
    ("FAILED tests/test_a.py::test_x\n2 failed in 0.1s\n", None),       # one name for two failures
    ("1 failed in 0.1s\n", None),
])
def test_the_names_must_be_as_many_as_the_summary_counts(output, names):
    assert failing_test_names(output) == (frozenset(names) if names is not None else None)


def _repo(tmp_path: Path) -> tuple[Path, Path]:
    repo = tmp_path / "repo"
    repo.mkdir()
    for args in (["init", "-q"], ["config", "user.email", "t@e.com"], ["config", "user.name", "T"]):
        subprocess.run(["git", *args], cwd=repo, check=True)
    (repo / "a.txt").write_text("a\n")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=repo, check=True)
    (repo / ".git" / "info" / "exclude").write_text(".remedy-wt/\n")
    wt = repo / ".remedy-wt" / "job-1"
    subprocess.run(["git", "worktree", "add", "-q", "-b", "remedy/job-1", str(wt)], cwd=repo, check=True)
    return repo, wt


def _ev(reason="nonzero_exit", status="failed"):
    import dataclasses

    @dataclasses.dataclass(frozen=True)
    class Ev:
        reason: str
        status: str
        command: str = "npm test"
        output_tail: str = "tail\n"
        preexisting: tuple = ()
        baseline: str = ""
    return Ev(reason, status)


def test_a_failure_the_base_shares_passes_and_one_more_stays_red(tmp_path):
    repo, wt = _repo(tmp_path)
    seen = []

    def rerun(root, ids):                                    # F333: the base runs only the failing tests
        seen.append((root, ids))
        assert root.is_dir() and root != wt and (root / "a.txt").is_file()
        return _ev(), VITEST

    judged = judged_against_base(_ev(), VITEST, wt, rerun)
    assert (judged.status, judged.reason) == ("passed", REASON_PREEXISTING_FAILURES)
    assert judged.output_tail.startswith("Every failing test already failed") and "math > adds" in judged.output_tail
    assert not seen[0][0].exists() and seen[0][1] == ["tests/a.test.ts"]   # the base worktree is gone
    more = VITEST.replace("1 failed | 1 passed", "2 failed").replace(
        " FAIL  tests/a.test.ts > math > adds", " FAIL  tests/a.test.ts > math > adds\n FAIL  tests/b.test.ts > x")
    assert judged_against_base(_ev(), more, wt, rerun).status == "failed"
    assert judged_against_base(_ev(), VITEST, wt, rerun).status == "passed"
    assert len(seen) == 2                                                # the base run of the same ids is kept


def test_nothing_is_compared_outside_a_job_worktree_or_for_a_refusal(tmp_path):
    repo, _wt = _repo(tmp_path)
    never = lambda root, ids: pytest.fail("no base run")  # noqa: E731
    assert judged_against_base(_ev(), VITEST, repo, never).status == "failed"
    assert judged_against_base(_ev(reason="tool_unavailable"), VITEST, repo, never).reason == "tool_unavailable"
