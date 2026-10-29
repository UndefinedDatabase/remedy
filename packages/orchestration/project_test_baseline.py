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

F333 (operator order beweis, job de04ce7d2bed47b0): the base run runs only the failing tests, by
their ids (`failing_test_ids`: pytest's node ids, Vitest's file names), in the throwaway worktree.
A failure the base shares is pre-existing ("war schon vorher rot"): the evidence keeps the list
(`preexisting`), and `preexisting_failures_in` names it for the job's worktree, so the reviewer is
told and a finding only about it reads `low` (`review_scope_rules`). When the base run cannot be
made (no ids, a runner that takes no ids, a timeout, no base commit), the red stays red and the
evidence's `baseline` sentence says why.
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
#: (worktree's checkout, base commit, command, ids) → the base run's failing test names and why none, per process.
_BASE_RUNS: dict[tuple[str, str, str, tuple[str, ...]], tuple[frozenset[str] | None, str]] = {}
#: F333: a job worktree → the failing tests of its last red run that all failed on the base too, per process.
_PREEXISTING: dict[str, frozenset[str]] = {}
#: F333: the evidence file of a job that lists the pre-existing failures its rounds met.
PREEXISTING_FAILURES_FILENAME = "preexisting_failures.json"


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


def failing_test_ids(names: frozenset[str]) -> list[str] | None:
    """The ids NAMES' runner takes to run only them: a pytest node id as it stands, a Vitest test's
    file (the part before ` > `); None when a name is no path, so the base run cannot be narrowed."""
    ids: list[str] = []
    for name in sorted(names):
        test_id = name if "::" in name else name.split(" > ")[0].split(" [")[0].strip()
        if "/" not in test_id and "." not in test_id.split("::")[0]:
            return None
        if test_id not in ids:
            ids.append(test_id)
    return ids or None


def preexisting_failures_in(workspace: str | Path | None) -> frozenset[str]:
    """F333: the failing tests WORKSPACE's last red run shared with the job's base commit; empty when none."""
    return _PREEXISTING.get(str(Path(workspace).resolve()), frozenset()) if workspace else frozenset()


def record_preexisting_failures(job_id: str, names: frozenset[str] | tuple[str, ...]) -> None:
    """F333: add NAMES to JOB_ID's `preexisting_failures.json`, which the story counts."""
    from packages.orchestration.builder_test_runs import _append_json
    from packages.orchestration.data_paths import job_evidence_dir

    if job_id and names:
        _append_json(Path(job_evidence_dir(job_id)) / PREEXISTING_FAILURES_FILENAME, [{"tests": sorted(names)}])


def load_preexisting_failures(job_id: str) -> list[str]:
    """F333: every pre-existing failing test JOB_ID's rounds and its DoD gate's checks name, each once, sorted."""
    import json

    from packages.orchestration.data_paths import job_evidence_dir
    from packages.orchestration.dod_gate import load_gate_result

    try:
        rows = json.loads((Path(job_evidence_dir(job_id)) / PREEXISTING_FAILURES_FILENAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        rows = []
    checks = (load_gate_result(job_id) or {}).get("checks") or []
    rows = [*(rows if isinstance(rows, list) else []),
            *({"tests": c.get("preexisting")} for c in checks if isinstance(c, dict))]
    return sorted({str(t) for row in rows if isinstance(row, dict) for t in row.get("tests") or ()})


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


def base_failures(worktree: Path, command: str, ids: list[str],
                  rerun: Callable[[Path, list[str]], tuple[Any, str]]) -> tuple[frozenset[str] | None, str]:
    """The failing tests among IDS on the job's base commit, run by RERUN in a throwaway worktree of
    the checkout, and "" ; (None, why) when there is no checkout apart from WORKTREE or the run
    cannot be made or read (F333)."""
    from packages.orchestration.project_tests import base_lookup_dirs
    from packages.orchestration.worktrees import WORKTREE_DIRNAME, link_installed_packages

    base = job_base_commit(worktree)
    if base is None:
        return None, "the job has no base commit to compare with"
    [checkout] = base_lookup_dirs(worktree)
    key = (str(checkout), base, command, tuple(ids))
    if key in _BASE_RUNS:
        return _BASE_RUNS[key]
    top = Path(_git(checkout, "rev-parse", "--show-toplevel"))
    folder = top / WORKTREE_DIRNAME / f"baseline-{uuid.uuid4().hex[:12]}"
    why = ""
    try:
        _git(top, "worktree", "add", "--detach", str(folder), base)
        link_installed_packages(top, folder)
        evidence, output = rerun(folder / checkout.relative_to(top), ids)
        found = failing_test_names(output) if evidence.reason == "nonzero_exit" else (
            frozenset() if evidence.status == "passed" else None)
        why = "" if found is not None else (
            f"the base run ended {evidence.reason or evidence.status}" if evidence.reason != "nonzero_exit"
            else "the base run's failing tests could not be read completely")
    except (OSError, subprocess.TimeoutExpired, ValueError) as exc:
        found, why = None, f"the base run could not be made: {exc}"
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", str(folder)], cwd=str(top),
                       capture_output=True, timeout=60)
    _BASE_RUNS[key] = (found, why)
    return found, why


def _with_note(evidence: Any, note: str, **changes: Any) -> Any:
    return dataclasses.replace(evidence, output_tail=note + evidence.output_tail[-max(0, 4000 - len(note)):],
                               **changes)


def judged_against_base(evidence: Any, output: str, worktree: Path,
                        rerun: Callable[[Path, list[str]], tuple[Any, str]]) -> Any:
    """EVIDENCE as it stands, or passed with `REASON_PREEXISTING_FAILURES` when every test it failed
    also fails on the job's base commit (see the module text); a red that stays red says why."""
    if evidence.reason != "nonzero_exit":
        return evidence
    key = str(Path(worktree).resolve())
    _PREEXISTING.pop(key, None)
    mine = failing_test_names(output)
    ids = failing_test_ids(mine) if mine else None
    if not mine or ids is None:
        why = "the failing tests could not be read by name and id"
        return _with_note(evidence, f"Not compared with the job's base commit: {why}.\n", baseline=why)
    before, why = base_failures(worktree, evidence.command, ids, rerun)
    if before is None:
        return _with_note(evidence, f"Not compared with the job's base commit: {why}.\n", baseline=why)
    new = sorted(mine - before)
    shared = tuple(sorted(mine & before))
    if new:
        why = f"{len(new)} failing test(s) are new in this job: {', '.join(new)}"
        return _with_note(evidence, f"Compared with the job's base commit: {why}.\n", baseline=why, preexisting=shared)
    _PREEXISTING[key] = frozenset(mine)
    note = ("Every failing test already failed on the job's base commit, so none of them is the "
            "job's (amend1027, F333: already red before the job): " + ", ".join(sorted(mine)) + "\n")
    return _with_note(evidence, note, status="passed", reason=REASON_PREEXISTING_FAILURES,
                      preexisting=tuple(sorted(mine)), baseline="every failing test already failed on the base")
