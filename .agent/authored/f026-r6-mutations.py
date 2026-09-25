#!/usr/bin/env python3
"""F026 R6 G4 — the round's red proofs (R-1063).

Given a worktree path, runs an unmutated control of the three test files below FIRST
and LAST, and between them applies each mutation, runs the same three files, restores
the mutated file BYTE-IDENTICAL, and reports each mutation's label, exit code, failed
count and failing test names. A mutation is caught when the run goes red.

All three mutations are pure Python (no TypeScript this round), so the tool runs one
runner: `python3 -B -m pytest -q -p no:cacheprovider --tb=no -rfE` over
  tests/ui_server/test_command_channel.py     (m1 — the write door's import guard)
  tests/orchestration/test_task_edit_runtime.py (m3 — dod_resync_pending)
  tests/test_data_paths.py                     (m2 — job_dod_path)
from the WORKTREE ROOT, after purging `__pycache__` before every run so a stale
bytecode cache can never serve a previous mutation's module.

m1 (R-1063 S1) puts `task_edit_runtime.py`'s `dod_gate` import back — one added
   import line — so the door reaches `dod_runners`, `exec_guard` and `subprocess`
   transitively again and `TestCommandDoorImportGuard` reddens.
m2 (R-1063 S1) makes `data_paths.job_dod_path` return the evidence directory itself,
   dropping `/ DOD_FILENAME`, so the new `tests/test_data_paths.py` case reddens.
m3 (R-1063 S2) puts the old field-presence check back — `"acceptance" in fields` — so
   the new unchanged-acceptance-beside-another-field case reddens.

Usage: python3 -B f026-r6-mutations.py <worktree_root>
"""
from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

TASK_EDIT_RUNTIME_REL = "packages/orchestration/task_edit_runtime.py"
DATA_PATHS_REL = "packages/orchestration/data_paths.py"

TEST_FILES = [
    "tests/ui_server/test_command_channel.py",
    "tests/orchestration/test_task_edit_runtime.py",
    "tests/test_data_paths.py",
]

MUTATIONS = [
    # --- S1: the door must not reach dod_gate again (m1, R-1063) -----------
    {"id": "m1",
     "name": "task_edit_runtime.py imports dod_gate again",
     "file": TASK_EDIT_RUNTIME_REL,
     "from": "from packages.orchestration import pause_control, safe_points\n",
     "to": (
         "from packages.orchestration import dod_gate\n"
         "from packages.orchestration import pause_control, safe_points\n"
     )},
    # --- S1: job_dod_path must actually name the file (m2, R-1063) ---------
    {"id": "m2",
     "name": "job_dod_path returns the path without DOD_FILENAME",
     "file": DATA_PATHS_REL,
     "from": "    return job_evidence_dir(job_id, root) / DOD_FILENAME\n",
     "to": "    return job_evidence_dir(job_id, root)\n"},
    # --- S2: the flag must compare values, not field presence (m3, R-1063) -
    {"id": "m3",
     "name": 'dod_resync_pending reads "acceptance" in fields again',
     "file": TASK_EDIT_RUNTIME_REL,
     "from": "        dod_resync_pending = entry.acceptance != acceptance_before and has_stored_dod\n",
     "to": '        dod_resync_pending = "acceptance" in fields and has_stored_dod\n'},
]


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def purge_pycache(worktree: Path) -> None:
    for d in worktree.rglob("__pycache__"):
        shutil.rmtree(d, ignore_errors=True)


def run_pytest(worktree: Path) -> dict:
    purge_pycache(worktree)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "--tb=no", "-rfE"] + TEST_FILES,
        cwd=str(worktree), capture_output=True, text=True, timeout=180)
    out = proc.stdout + proc.stderr
    m_failed = re.search(r"(\d+) failed", out)
    m_error = re.search(r"(\d+) error", out)
    failed = (int(m_failed.group(1)) if m_failed else 0) + \
        (int(m_error.group(1)) if m_error else 0)
    names = re.findall(r"^FAILED (\S+)", out, re.MULTILINE) + \
        re.findall(r"^ERROR (\S+)", out, re.MULTILINE)
    return {"exit": proc.returncode, "failed": failed, "names": names, "raw": out}


def fmt(result: dict) -> str:
    return f"exit={result['exit']} failed={result['failed']}"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f026-r6-mutations.py <worktree_root>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()
    print(f"worktree: {worktree}")

    control_first = run_pytest(worktree)
    print(f"CONTROL FIRST: {fmt(control_first)}")
    first_green = control_first["exit"] == 0 and control_first["failed"] == 0
    if not first_green:
        print("control is not green; aborting")
        print("--- pytest output (tail) ---")
        print(control_first["raw"][-4000:])
        return 1

    all_ok = True
    for mut in MUTATIONS:
        target = worktree / mut["file"]
        original = target.read_bytes()
        digest = sha256_of(target)
        text = original.decode("utf-8")
        count = text.count(mut["from"])
        if count != 1:
            print(f"{mut['id']}: SKIPPED, FROM occurrences {count}")
            all_ok = False
            continue
        text = text.replace(mut["from"], mut["to"], 1)
        target.write_bytes(text.encode("utf-8"))
        try:
            result = run_pytest(worktree)
        finally:
            target.write_bytes(original)
        restored = sha256_of(target) == digest
        caught = result["exit"] != 0 and result["failed"] > 0
        all_ok = all_ok and caught and restored
        names = ", ".join(result["names"]) if result["names"] else "(none parsed)"
        print(f"{mut['id']} ({mut['name']}): {fmt(result)} failing=[{names}] "
              f"| caught={caught} restored byte-identical={restored}")

    control_last = run_pytest(worktree)
    print(f"CONTROL LAST: {fmt(control_last)}")
    last_green = control_last["exit"] == 0 and control_last["failed"] == 0
    all_ok = all_ok and last_green
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
