#!/usr/bin/env python3
"""F029 R7 G5 — the red proofs for T003's end-to-end subtree rerun test.

Takes a worktree path. Runs `python3 -B -m pytest -q -p no:cacheprovider
tests/ui_server/test_subtree_rerun_e2e_live.py` with the worktree as working
directory and an environment of this tool's own plus `PYTHONPATH` set to the
worktree and `PYTHONDONTWRITEBYTECODE=1`, after purging every `__pycache__`
directory under the worktree. Before the first control run it prints, under
that same environment, `__file__` of `packages.orchestration.subtree_rerun`
and of `packages.orchestration.pingpong_job`, so a mismatch against the
worktree is visible before any mutation runs.

Four mutations, each replacing ONE WHOLE line of the named file INSIDE the
worktree (its FROM text asserted to occur exactly once), run and restored in
turn. Unmutated controls run first and last. Prints one line per mutation
(label, exit code, failed count, the failing tests' names) and ends with
`restored byte-identical: <bool>` per touched file, the PRIMARY checkout's own
`git status --porcelain` (must be empty) and
`ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.

Usage:
    python3 -B .agent/authored/f029-r7-mutations.py <worktree-path>
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

PRIMARY_ROOT = Path("/home/decodeux/Repos/remedy")

TEST_ARGS = ["tests/ui_server/test_subtree_rerun_e2e_live.py"]

PINGPONG_JOB = "packages/orchestration/pingpong_job.py"
UI_SERVER = "packages/orchestration/ui_server.py"
RUN_REPORT = "packages/orchestration/run_report.py"
SUBTREE_RERUN = "packages/orchestration/subtree_rerun.py"

# Each entry: (label, relative path, FROM line, TO line). FROM must occur
# exactly once in the pristine file.
MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "m1 a run ignores the model override",
        PINGPONG_JOB,
        "                    builder_model=(task.model_override or builder_model),\n",
        "                    builder_model=builder_model,\n",
    ),
    (
        "m2 the dashboard forgets the attempt",
        UI_SERVER,
        '            "attempt": int(t.attempt),\n',
        '            "attempt": 1,\n',
    ),
    (
        "m3 the report drops the clause for a second attempt",
        RUN_REPORT,
        "    if task.attempt < 2:\n",
        "    if task.attempt < 3:\n",
    ),
    (
        "m4 the fold does not count the attempt",
        SUBTREE_RERUN,
        "            task.attempt += 1\n",
        "            task.attempt += 0\n",
    ),
]


def _purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        shutil.rmtree(cache_dir, ignore_errors=True)


def _run_pytest(worktree: Path) -> tuple[int, str]:
    _purge_pycache(worktree)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(worktree)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TEST_ARGS],
        cwd=str(worktree), env=env, capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def _print_module_files(worktree: Path) -> bool:
    """Prints `__file__` of the two modules under test, resolved under the
    worktree's own PYTHONPATH. Returns whether both lie inside the worktree."""
    env = dict(os.environ)
    env["PYTHONPATH"] = str(worktree)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    code = (
        "import packages.orchestration.subtree_rerun as sr\n"
        "import packages.orchestration.pingpong_job as pj\n"
        "print(sr.__file__)\n"
        "print(pj.__file__)\n"
    )
    proc = subprocess.run(
        [sys.executable, "-B", "-c", code],
        cwd=str(worktree), env=env, capture_output=True, text=True,
    )
    lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    print(f"packages.orchestration.subtree_rerun.__file__ = {lines[0] if lines else '?'}")
    print(f"packages.orchestration.pingpong_job.__file__ = {lines[1] if len(lines) > 1 else '?'}")
    if proc.returncode != 0:
        print(proc.stderr[-2000:])
        return False
    worktree_resolved = str(worktree.resolve())
    return all(Path(line).resolve().is_relative_to(worktree_resolved) for line in lines)


def _failed_count_and_names(output: str) -> tuple[int, list[str]]:
    failing = sorted({
        line.split(" ", 1)[1].split(" - ", 1)[0].strip()
        for line in output.splitlines()
        if line.startswith("FAILED ")
    })
    failed_count = 0
    for line in output.splitlines():
        if " failed" in line and ("passed" in line or "error" in line or line.strip().endswith("failed")):
            for token in line.split(","):
                token = token.strip()
                if token.endswith("failed"):
                    failed_count = int(token.split()[0])
    return failed_count, failing


def _apply_edit(path: Path, from_text: str, to_text: str, label: str) -> bytes | None:
    """Applies one edit, asserting FROM occurs exactly once. Returns the ORIGINAL bytes on
    success (for the caller to restore), or None (with a printed reason) if it refused."""
    original = path.read_bytes()
    text = original.decode("utf-8")
    occurrences = text.count(from_text)
    if occurrences != 1:
        print(f"{label}: FROM text occurs {occurrences} times (expected 1) — aborting")
        return None
    mutated = text.replace(from_text, to_text, 1)
    path.write_bytes(mutated.encode("utf-8"))
    return original


def _git_status_porcelain() -> str:
    proc = subprocess.run(
        ["git", "-C", str(PRIMARY_ROOT), "status", "--porcelain"],
        capture_output=True, text=True)
    return proc.stdout


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f029-r7-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    touched_rels = sorted({rel for _, rel, _, _ in MUTATIONS})
    originals = {rel: (root / rel).read_bytes() for rel in touched_rels}

    print("=" * 78)
    modules_inside_worktree = _print_module_files(root)
    print(f"both modules resolve inside the worktree: {modules_inside_worktree}")
    if not modules_inside_worktree:
        print("A MODULE RESOLVED OUTSIDE THE WORKTREE — aborting the mutation sweep.")
        return 1

    all_ok = True

    # --- unmutated control, before any mutation ------------------------------
    print("--- control run (unmutated, before) ---")
    code, output = _run_pytest(root)
    failed, _names = _failed_count_and_names(output)
    print(f"control: exit={code} failed={failed}")
    if code != 0:
        print("CONTROL RUN IS NOT GREEN — aborting the mutation sweep.")
        print(output[-2000:])
        return 1

    # --- the four mutations ---------------------------------------------------
    for label, rel_path, from_text, to_text in MUTATIONS:
        path = root / rel_path
        original = originals[rel_path]
        applied = _apply_edit(path, from_text, to_text, label)
        if applied is None:
            all_ok = False
            continue
        try:
            code, output = _run_pytest(root)
            failed_count, failing_names = _failed_count_and_names(output)
            caught = code != 0 and failed_count != 0
            all_ok = all_ok and caught
            tag_txt = "" if caught else " — GREEN, NOT CAUGHT"
            print(f"{label}: exit={code} failed={failed_count} "
                  f"failing_tests={failing_names}{tag_txt}")
            if not caught:
                print(output[-2000:])
        finally:
            path.write_bytes(original)

    # --- restore verification --------------------------------------------------
    all_restored = True
    for rel_path in touched_rels:
        restored = (root / rel_path).read_bytes() == originals[rel_path]
        all_restored = all_restored and restored
        print(f"restored byte-identical: {restored} ({rel_path})")

    # --- unmutated control, after the full sweep --------------------------------
    print("--- control run (unmutated, after) ---")
    code, output = _run_pytest(root)
    control_after_ok = code == 0
    print(f"control: exit={code}")

    porcelain = _git_status_porcelain()
    primary_clean = porcelain == ""
    print(f"git status --porcelain (primary checkout): {porcelain!r}")

    result = all_ok and all_restored and control_after_ok and primary_clean
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {result}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
