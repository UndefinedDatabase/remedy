#!/usr/bin/env python3
"""F027 R11 G4 — the red proofs for the R-1071 repair.

Takes a worktree path. Runs an unmutated PYTEST control over the worktree's
`tests/orchestration/test_task_expectation_episode_context.py`, from the worktree's root,
first and last. For each of the two ordered mutations below: edits the named file INSIDE
the worktree (asserting its FROM text occurs exactly once), purges the worktree's
`__pycache__` directories, runs the same file again, restores the bytes BYTE-IDENTICAL,
and prints the mutation's label, the run's real exit code, the failed count and the
failing test node ids. Ends with `restored byte-identical: <bool>` per touched file and
`ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.

Usage:
    python3 -B .agent/authored/f027-r11-mutations.py <worktree-path>
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

RUN_MANIFEST = "packages/orchestration/run_manifest.py"

PYTEST_NODE_IDS = [
    "tests/orchestration/test_task_expectation_episode_context.py",
]

# The two ordered mutations: an exact FROM string, replaced by an exact TO string. FROM
# must occur exactly once in the pristine file.
MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "m1 vetoed leaves the completed worked EXPECT_EXECUTED tight set",
        RUN_MANIFEST,
        '    EXPECT_EXECUTED: frozenset({"passed", "applied_to_job_workspace", "vetoed"}),\n',
        '    EXPECT_EXECUTED: frozenset({"passed", "applied_to_job_workspace"}),'
        '  # MUTATED (m1): vetoed dropped\n',
    ),
    (
        "m2 vetoed leaves the completed worked EXPECT_PRIOR_EPISODE tight set",
        RUN_MANIFEST,
        '    EXPECT_PRIOR_EPISODE: frozenset({"passed", "applied_to_job_workspace", "vetoed"}),\n',
        '    EXPECT_PRIOR_EPISODE: frozenset({"passed", "applied_to_job_workspace"}),'
        '  # MUTATED (m2): vetoed dropped\n',
    ),
]


def _purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        shutil.rmtree(cache_dir, ignore_errors=True)


def _run_pytest(worktree: Path) -> tuple[int, str]:
    _purge_pycache(worktree)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *PYTEST_NODE_IDS],
        cwd=str(worktree), capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def _failed_count_and_ids(output: str) -> tuple[int, list[str]]:
    ids = sorted(set(re.findall(r"^FAILED (\S+)", output, re.MULTILINE)))
    match = re.search(r"(\d+) failed", output)
    count = int(match.group(1)) if match else 0
    return count, ids


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


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f027-r11-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    touched_rels = sorted({rel for _, rel, _, _ in MUTATIONS})
    originals = {rel: (root / rel).read_bytes() for rel in touched_rels}

    all_ok = True

    print("=" * 78)
    print("--- pytest control run (unmutated, before) ---")
    code, output = _run_pytest(root)
    print(f"control: exit={code}")
    print(output.strip().splitlines()[-1] if output.strip() else "(no output)")
    if code != 0:
        print("PYTEST CONTROL RUN IS NOT GREEN — aborting the mutation sweep.")
        return 1

    for label, rel_path, from_text, to_text in MUTATIONS:
        path = root / rel_path
        original = originals[rel_path]
        applied = _apply_edit(path, from_text, to_text, label)
        if applied is None:
            all_ok = False
            continue
        try:
            code, output = _run_pytest(root)
            failed_count, failing_ids = _failed_count_and_ids(output)
            caught = code != 0 and failed_count > 0
            all_ok = all_ok and caught
            tag = "" if caught else " — GREEN, NOT CAUGHT"
            print(f"{label}: exit={code} failed={failed_count} "
                  f"failing_node_ids={failing_ids}{tag}")
            if not caught:
                print(output[-2000:])
        finally:
            path.write_bytes(original)

    all_restored = True
    for rel_path in touched_rels:
        restored = (root / rel_path).read_bytes() == originals[rel_path]
        all_restored = all_restored and restored
        print(f"restored byte-identical: {restored} ({rel_path})")

    print("--- pytest control run (unmutated, after) ---")
    code, output = _run_pytest(root)
    control_after_ok = code == 0
    print(f"control: exit={code}")
    print(output.strip().splitlines()[-1] if output.strip() else "(no output)")

    result = all_ok and all_restored and control_after_ok
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {result}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
