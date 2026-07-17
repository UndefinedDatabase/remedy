"""Missing tests gate — deterministic, read-only verification scaffolding.

Inspects a task's staged diff and recorded test output to decide whether tests
*should* have run but didn't. Pure orchestration logic: no provider calls, no
target-repo mutation, no job state mutation. Same inputs always yield the same
gate, so the result is reproducible across runs.

Public API:
    build_missing_tests_gate(task, evidence_dir) -> dict
    write_missing_tests_gate(task, evidence_dir, written) -> None
"""
from __future__ import annotations

import fnmatch
import json
import re
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0.0"

_SAFE_TASK_ID_RE = re.compile(r"^T\d{3,}$")

# Diff header lines that name the changed file, e.g. ``+++ b/pkg/mod.py``.
_DIFF_PATH_RE = re.compile(r"^[+-]{3}\s+[ab]/(.+)$")

# Markers in tests.txt that mean tests were NOT executed.
_NOT_RUN_MARKERS = ("not run", "not_run", "tests_not_run", "no tests")
# Markers that mean tests actually ran and produced a result.
_RAN_MARKERS = ("passed", "failed", "error", "collected")
# Markers that mean the environment blocked execution.
_BLOCKED_MARKERS = ("blocked", "sandbox")


#: F8 (round 16): the regression suites a changed SOURCE file is known to be covered by, when
#: that suite does not live at a path any convention would derive.
#:
#: A reviewable constant on purpose (the F017 builtin-deny-list precedent): additions show up in
#: diffs. It is a floor, not a map of everything — every suite whose path follows the usual
#: convention is already reached by the changed-set rule.
_RELEVANT_SUITES_FOR_SOURCE: dict[str, tuple[str, ...]] = {
    # `do job-flow`'s end-to-end regressions do NOT live under tests/cli/, so a change to the do
    # command was invisible to the authoritative CLI matrix. That is exactly how round 15 shipped
    # `NameError: timeout_sec is not defined` in a public command with every gate green.
    "apps/cli/commands/do_cmd.py": ("tests/test_do_job_flow.py",),
}


def _relevant_suites_for_source(path: str) -> tuple[str, ...]:
    """The regression suites that must run green for a changed source file."""
    return _RELEVANT_SUITES_FOR_SOURCE.get(path, ())


def _task_attr(task: Any, key: str, default: Any = None) -> Any:
    if isinstance(task, dict):
        return task.get(key, default)
    return getattr(task, key, default)


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except (OSError, ValueError):
        return ""


def _changed_files(diff_text: str) -> list[str]:
    """Return the de-duplicated, sorted list of file paths named in a diff."""
    files: set[str] = set()
    for line in diff_text.splitlines():
        m = _DIFF_PATH_RE.match(line)
        if not m:
            continue
        path = m.group(1).strip()
        if not path or path == "/dev/null":
            continue
        files.add(path)
    return sorted(files)


def _is_under_tests(path: str) -> bool:
    return path == "tests" or path.startswith("tests/") or "/tests/" in path


def _is_test_file(path: str) -> bool:
    base = path.rsplit("/", 1)[-1]
    return fnmatch.fnmatch(base, "test_*.py") or _is_under_tests(path)


_SOURCE_EXTENSIONS = frozenset((
    ".py", ".ts", ".tsx", ".js", ".jsx",
    ".sh", ".css", ".scss",
))


def _is_source_file(path: str) -> bool:
    if _is_under_tests(path):
        return False
    for ext in _SOURCE_EXTENSIONS:
        if path.endswith(ext):
            return True
    return False


def _tests_executed(tests_text: str) -> bool:
    """True only when tests.txt records an actual test result (not 'not run').

    Blocked/sandbox markers take precedence — environment-blocked output
    must never count as executed even if it also contains 'error'.
    """
    text = tests_text.strip()
    if not text:
        return False
    lower = text.lower()
    if any(marker in lower for marker in _NOT_RUN_MARKERS):
        return False
    if any(marker in lower for marker in _BLOCKED_MARKERS):
        return False
    return any(marker in lower for marker in _RAN_MARKERS)


def _tests_blocked(tests_text: str) -> bool:
    lower = tests_text.lower()
    return any(marker in lower for marker in _BLOCKED_MARKERS)


def build_missing_tests_gate(task: Any, evidence_dir: str) -> dict[str, Any]:
    """Check whether tests should have run but didn't.

    Reads ``task_runs/<task_id>/safe.diff`` and ``task_runs/<task_id>/tests.txt``
    from ``evidence_dir`` and classifies the gate. Never mutates either file.
    """
    task_id = str(_task_attr(task, "task_id", "") or "")

    base = Path(evidence_dir) / "task_runs" / task_id
    diff_text = _read_text(base / "safe.diff")
    tests_text = _read_text(base / "tests.txt")

    changed = _changed_files(diff_text)
    test_files = [f for f in changed if _is_test_file(f)]
    source_files_changed = any(_is_source_file(f) for f in changed)
    test_files_changed = bool(test_files)

    tests_executed = _tests_executed(tests_text)
    tests_blocked = _tests_blocked(tests_text)

    code_changed = source_files_changed or test_files_changed

    if code_changed and not tests_executed:
        gate_status = "NEEDS_TESTS"
        suggested = [f"python3 -m pytest {f} -q" for f in test_files]
        if tests_blocked:
            reason = "Tests were blocked by the execution environment"
        elif source_files_changed and test_files_changed:
            reason = "Source and test files changed but no tests were executed"
        elif source_files_changed:
            reason = "Source files changed but no tests were executed"
        else:
            reason = "Test files changed but no tests were executed"
        test_result_summary = ""
    elif tests_executed:
        gate_status = "PASS"
        suggested = []
        reason = "Tests were executed and results are recorded"
        test_result_summary = tests_text.strip()
    else:
        gate_status = "PASS"
        suggested = []
        reason = "No source or test files changed; tests not required"
        test_result_summary = ""

    return {
        "schema_version": SCHEMA_VERSION,
        "task_id": task_id,
        "gate_status": gate_status,
        "source_files_changed": source_files_changed,
        "test_files_changed": test_files_changed,
        "tests_executed": tests_executed,
        "tests_blocked_by_environment": tests_blocked,
        "suggested_test_commands": suggested,
        "reason": reason,
        "test_result_summary": test_result_summary,
    }


def write_missing_tests_gate(
    task: Any,
    evidence_dir: str,
    written: dict[str, str],
) -> None:
    """Build and write ``missing_tests_gate.json`` to task evidence.

    Writes ``task_runs/<task_id>/missing_tests_gate.json`` into the job evidence
    dir and registers it in ``written``. No-op when the task has no safe
    ``task_id`` or no evidence dir.
    """
    task_id = str(_task_attr(task, "task_id", "") or "")
    if not task_id or not _SAFE_TASK_ID_RE.fullmatch(task_id) or not evidence_dir:
        return

    gate = build_missing_tests_gate(task, evidence_dir)

    rel_run = f"task_runs/{task_id}"
    run_dir = Path(evidence_dir) / "task_runs" / task_id
    run_dir.mkdir(parents=True, exist_ok=True)

    json_path = run_dir / "missing_tests_gate.json"
    json_path.write_text(json.dumps(gate, indent=2) + "\n", encoding="utf-8")
    written[f"{rel_run}/missing_tests_gate.json"] = str(json_path)
