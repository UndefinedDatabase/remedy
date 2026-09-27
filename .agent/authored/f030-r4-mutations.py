#!/usr/bin/env python3
"""F030 R4 C4 — the round 4 mutation tool (G5).

Takes ONE argument: a worktree path. For each of the four mutations m1-m4 it replaces the
quoted FROM text with the TO text inside that worktree's copy of the named production file
(asserting the FROM text occurs exactly once in that file), purges the worktree's
`__pycache__` directories, runs `tests/ui_server/test_steering_note_e2e_live.py` from the
worktree's root, and restores the file's original bytes. An unmutated control run goes first
and last. Prints one line per mutation (label, exit code, failed count, failing node ids),
then `restored byte-identical: True` (or `False`) per file, then
`ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

TEST_PATH = "tests/ui_server/test_steering_note_e2e_live.py"

#: (label, relative path, FROM text, TO text)
MUTATIONS = [
    ("m1", "packages/orchestration/steering.py",
     "if addressed_to and addressed_to != str(task_id):",
     "if addressed_to:"),
    ("m2", "packages/orchestration/pingpong_loop.py",
     "operator_notes_text = _operator_notes_text_for_round(job_id, task_id)",
     'operator_notes_text = ""'),
    ("m3", "packages/orchestration/ui_server.py",
     'summary["note"] = note',
     'summary.pop("note", None)'),
    ("m4", "packages/orchestration/pingpong_job.py",
     "if task.status in (TASK_PENDING, TASK_RUNNING):",
     "if True:"),
]


def _purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        for f in cache_dir.glob("*"):
            f.unlink()
        cache_dir.rmdir()


def _run_tests(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST_PATH],
        cwd=str(root), capture_output=True, text=True, timeout=300,
    )


def _failing_node_ids(stdout: str) -> list[str]:
    return [line.split(" ", 1)[0] for line in stdout.splitlines() if line.startswith("FAILED ")]


def _failed_count(stdout: str) -> int:
    m = re.search(r"(\d+) failed", stdout)
    return int(m.group(1)) if m else 0


def _report(label: str, proc: subprocess.CompletedProcess) -> bool:
    """Print the line, return True when this run is RED (caught)."""
    failed = _failed_count(proc.stdout)
    nodes = _failing_node_ids(proc.stdout)
    print(f"{label}: exit={proc.returncode} failed={failed} nodes={nodes}")
    return proc.returncode != 0


def main() -> None:
    root = Path(sys.argv[1]).resolve()
    all_ok = True

    _purge_pycache(root)
    control_first = _run_tests(root)
    is_red = _report("control (first)", control_first)
    if is_red:
        all_ok = False  # the unmutated control must be GREEN

    restored: dict[str, bool] = {}
    for label, rel_path, from_text, to_text in MUTATIONS:
        path = root / rel_path
        original = path.read_bytes()
        text = original.decode("utf-8")
        occurrences = text.count(from_text)
        assert occurrences == 1, (
            f"{label}: FROM text occurs {occurrences} times in {rel_path}, expected exactly 1")
        mutated = text.replace(from_text, to_text, 1)
        try:
            path.write_bytes(mutated.encode("utf-8"))
            _purge_pycache(root)
            proc = _run_tests(root)
            is_red = _report(label, proc)
            if not is_red:
                all_ok = False  # a mutation that stayed green is reported as green
        finally:
            path.write_bytes(original)
            restored[rel_path] = path.read_bytes() == original

    _purge_pycache(root)
    control_last = _run_tests(root)
    is_red = _report("control (last)", control_last)
    if is_red:
        all_ok = False  # the unmutated control must be GREEN

    for rel_path, ok in restored.items():
        print(f"restored byte-identical: {ok} ({rel_path})")
        if not ok:
            all_ok = False

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")


if __name__ == "__main__":
    main()
