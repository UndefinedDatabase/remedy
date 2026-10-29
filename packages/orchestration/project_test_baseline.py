"""Operator amendment amend1027-green-builds, F4: a red the project already had is not the job's.

Since B2 every order's final check runs the project's own test command, blocking. On 2026-10-27
universe-chat's `main` itself failed three Vitest tests (a golden record of texts and an animation
list, from merges that had nothing to do with Remedy), so every job of that project would have
ended red, and the last task's repair rounds would have chased failures the job never caused.

`judged_against_base` closes that gap with one comparison, never a guess:

* only a run that ran and failed (`nonzero_exit`) is compared;
* the names of its failing tests are read from the runner's full output (`failing_test_names`:
  Vitest's and Jest's `FAIL` lines, else their `×` or `✕` lines, pytest's `FAILED` and `ERROR`
  lines), and they must be exactly
  as many as the runner's own summary counts (`builder_test_runs.read_test_result`), else nothing is
  compared and the run stays red;
* the same command then runs once more, in a throwaway worktree of the job's base commit (the
  merge base of the job's branch and the checkout's `HEAD`), under the same sandbox; the result is
  kept for the process, so a repair round does not pay for it twice;
* when every failing test of the job also fails on the base, the check passes with the reason
  `preexisting_failures`, and its output names them; one failure more, and it stays red.

Remedy deliberately does not skip, deselect or retry a failing test here, and never compares when
the names cannot be read completely: an unreadable red stays red.
"""
from __future__ import annotations

import dataclasses
import re
import subprocess
import uuid
from collections.abc import Callable
from pathlib import Path
from typing import Any

#: The reason of a check whose only failures were already failing on the job's base commit.
REASON_PREEXISTING_FAILURES = "preexisting_failures"

_ANSI = re.compile(r"\x1b\[[0-9;]*m")
_JS_FAIL = re.compile(r"^\s*FAIL\s+(\S.*?)\s*$")
_JS_CROSS = re.compile(r"^\s*(?:✕|×)\s+(\S.*?)\s*$")
_PY_FAIL = re.compile(r"^(?:FAILED|ERROR)\s+(\S+)")
#: (worktree's checkout, base commit, command) → the base run's failing test names, per process.
_BASE_RUNS: dict[tuple[str, str, str], frozenset[str] | None] = {}


def failing_test_names(output: str) -> frozenset[str] | None:
    """The failing tests OUTPUT names, or None when they cannot be read completely: their number
    must equal the failures the runner's summary line counts."""
    from packages.orchestration.builder_test_runs import read_test_result

    text = _ANSI.sub("", output)
    lines = text.splitlines()

    def named(pattern: re.Pattern[str]) -> set[str]:
        return {m.group(1).split(" - ")[0].strip() for line in lines if (m := pattern.match(line))}

    # Vitest prints each failure twice, as `×` while it runs and as `FAIL` in its summary.
    names = (named(_JS_FAIL) or named(_JS_CROSS)) | named(_PY_FAIL)
    _passed, summary = read_test_result(text, True)
    counted = int(summary.split(" passed, ")[1].split(" failed")[0])
    return frozenset(names) if names and len(names) == counted else None


def _git(cwd: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True, timeout=60)
    if done.returncode != 0:
        raise OSError(done.stderr.strip()[:300] or f"git {args[0]} failed")
    return done.stdout.strip()


def job_base_commit(worktree: Path) -> str | None:
    """The job's base commit: the merge base of WORKTREE's `HEAD` and its checkout's `HEAD`; None when
    WORKTREE has no checkout apart from itself or git cannot say (F329 reads its diff against it)."""
    from packages.orchestration.project_tests import base_lookup_dirs

    [checkout] = base_lookup_dirs(worktree)
    if checkout == worktree:
        return None
    try:
        return _git(worktree, "merge-base", "HEAD", _git(checkout, "rev-parse", "HEAD"))
    except (OSError, subprocess.TimeoutExpired):
        return None


def base_failures(worktree: Path, command: str,
                  rerun: Callable[[Path], tuple[Any, str]]) -> frozenset[str] | None:
    """The failing tests of COMMAND on the job's base commit, run by RERUN in a throwaway worktree
    of the checkout; None when there is no checkout apart from WORKTREE or the run cannot be read."""
    from packages.orchestration.project_tests import base_lookup_dirs
    from packages.orchestration.worktrees import WORKTREE_DIRNAME, link_installed_packages

    base = job_base_commit(worktree)
    if base is None:
        return None
    [checkout] = base_lookup_dirs(worktree)
    key = (str(checkout), base, command)
    if key in _BASE_RUNS:
        return _BASE_RUNS[key]
    top = Path(_git(checkout, "rev-parse", "--show-toplevel"))
    folder = top / WORKTREE_DIRNAME / f"baseline-{uuid.uuid4().hex[:12]}"
    try:
        _git(top, "worktree", "add", "--detach", str(folder), base)
        link_installed_packages(top, folder)
        evidence, output = rerun(folder / checkout.relative_to(top))
        found = failing_test_names(output) if evidence.reason == "nonzero_exit" else (
            frozenset() if evidence.status == "passed" else None)
    except (OSError, subprocess.TimeoutExpired, ValueError):
        found = None
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", str(folder)], cwd=str(top),
                       capture_output=True, timeout=60)
    _BASE_RUNS[key] = found
    return found


def judged_against_base(evidence: Any, output: str, worktree: Path,
                        rerun: Callable[[Path], tuple[Any, str]]) -> Any:
    """EVIDENCE as it stands, or passed with `REASON_PREEXISTING_FAILURES` when every test it failed
    also fails on the job's base commit (see the module text)."""
    if evidence.reason != "nonzero_exit":
        return evidence
    mine = failing_test_names(output)
    if not mine:
        return evidence
    before = base_failures(worktree, evidence.command, rerun)
    if before is None or not mine <= before:
        return evidence
    note = ("Every failing test already failed on the job's base commit, so none of them is the "
            "job's (amend1027): " + ", ".join(sorted(mine)) + "\n")
    return dataclasses.replace(evidence, status="passed", reason=REASON_PREEXISTING_FAILURES,
                               output_tail=note + evidence.output_tail[-max(0, 4000 - len(note)):])
