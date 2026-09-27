#!/usr/bin/env python3
"""F028 R9 G5 — the reach of the injection end-to-end test.

Takes a worktree path. For each of the three probes below: edits the named
file INSIDE the worktree (asserting its FROM text occurs exactly once), runs
`tests/ui_server/test_task_injection_e2e_live.py` from the worktree's root
after purging its `__pycache__` directories, restores the bytes
BYTE-IDENTICAL, and prints the probe's label, the run's real exit code, the
failed count and the failing node ids. An unmutated control runs first and
last. Ends with `restored byte-identical: <bool>` per touched file, `git
status --porcelain` of the PRIMARY checkout, and
`ALL PROBES CAUGHT AND RESTORED CLEANLY: <bool>`.

Usage:
    python3 -B .agent/authored/f028-r9-probes.py <worktree-path>
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

PRIMARY_ROOT = Path("/home/decodeux/Repos/remedy")

RUN_REPORT = "packages/orchestration/run_report.py"
UI_SERVER = "packages/orchestration/ui_server.py"
PINGPONG_JOB = "packages/orchestration/pingpong_job.py"

PYTEST_TEST_RELS = [
    "tests/ui_server/test_task_injection_e2e_live.py",
]

# Each probe: an exact FROM string, replaced by an exact TO string. FROM must
# occur exactly once in the pristine file. All three are caught by the pytest
# route above, over the one file PYTEST_TEST_RELS names.
PROBES: list[tuple[str, str, str, str]] = [
    (
        "p1 _origin_clause answers \"\"",
        RUN_REPORT,
        '    return " — added by you while the job ran"\n',
        '    return ""  # PROBED (p1): the clause never renders\n',
    ),
    (
        "p2 the dashboard's _task_origin answers \"\"",
        UI_SERVER,
        '    return origin if isinstance(origin, str) and origin else ""\n',
        '    return ""  # PROBED (p2): the dashboard never names an origin\n',
    ),
    (
        "p3 _fold_task_injections answers False before it reads any confirmation",
        PINGPONG_JOB,
        "    from packages.orchestration import task_injection as _ti\n",
        "    return False  # PROBED (p3): never folds, never reads a confirmation\n\n"
        "    from packages.orchestration import task_injection as _ti\n",
    ),
]


def _purge_pycache(root: Path) -> None:
    for path in root.rglob("__pycache__"):
        shutil.rmtree(path, ignore_errors=True)


def _run_pytest(worktree: Path) -> tuple[int, str]:
    _purge_pycache(worktree)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         *PYTEST_TEST_RELS],
        cwd=str(worktree), capture_output=True, text=True, timeout=300)
    return proc.returncode, proc.stdout + proc.stderr


def _failed_count_and_node_ids(output: str) -> tuple[int, list[str]]:
    node_ids = re.findall(r"^FAILED (\S+)", output, re.MULTILINE)
    match = re.search(r"(\d+) failed", output)
    count = int(match.group(1)) if match else len(node_ids)
    return count, node_ids


def _apply_edit(path: Path, from_text: str, to_text: str, label: str) -> bytes | None:
    """Applies one edit, asserting FROM occurs exactly once. Returns the
    ORIGINAL bytes on success (for the caller to restore), or None (with a
    printed reason) if it refused."""
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
        print("usage: f028-r9-probes.py <worktree-path>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    touched_rels = sorted({rel for _, rel, _, _ in PROBES})
    originals = {rel: (root / rel).read_bytes() for rel in touched_rels}

    all_ok = True

    # --- control run, before any of the three probes -----------------------
    print("=" * 78)
    print("--- pytest control run (unmutated, before) ---")
    code, output = _run_pytest(root)
    failed, _ = _failed_count_and_node_ids(output)
    print(f"control: exit={code} failed={failed}")
    if code != 0:
        print("PYTEST CONTROL RUN IS NOT GREEN — aborting the probe sweep.")
        print(output[-2000:])
        return 1

    # --- the three probes ----------------------------------------------------
    for label, rel_path, from_text, to_text in PROBES:
        path = root / rel_path
        original = originals[rel_path]
        applied = _apply_edit(path, from_text, to_text, label)
        if applied is None:
            all_ok = False
            continue
        try:
            code, output = _run_pytest(root)
            failed_count, failing_ids = _failed_count_and_node_ids(output)
            caught = code != 0 and failed_count != 0
            all_ok = all_ok and caught
            tag_txt = "" if caught else " — GREEN, NOT CAUGHT"
            print(f"{label}: exit={code} failed={failed_count} "
                  f"failing_node_ids={failing_ids}{tag_txt}")
            if not caught:
                print(output[-2000:])
        finally:
            path.write_bytes(original)

    # --- restore verification -------------------------------------------------
    all_restored = True
    for rel_path in touched_rels:
        restored = (root / rel_path).read_bytes() == originals[rel_path]
        all_restored = all_restored and restored
        print(f"restored byte-identical: {restored} ({rel_path})")

    # --- control run, after the full sweep -------------------------------------
    print("--- pytest control run (unmutated, after) ---")
    code, output = _run_pytest(root)
    pytest_after_ok = code == 0
    print(f"control: exit={code}")

    porcelain = _git_status_porcelain()
    primary_clean = porcelain == ""
    print(f"git status --porcelain (primary checkout): {porcelain!r}")

    result = all_ok and all_restored and pytest_after_ok and primary_clean
    print(f"ALL PROBES CAUGHT AND RESTORED CLEANLY: {result}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
