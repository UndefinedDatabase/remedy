#!/usr/bin/env python3
"""Mutation tool for F025 R8 G5 — red-proves DECISION F025 D6's fix for R-1056:
a park records the episode it ends under the new manifest status `paused`.

Usage: python3 -B f025-r8-mutations.py <worktree_root>

For each mutation, edits its named production file INSIDE the given worktree
(asserting its FROM text occurs exactly once), prepares the worktree for the
live e2e test by `.agent/authored/f025-r7-mutations.py`'s own route (symlink
`apps/ui/node_modules` in from the primary checkout and COPY `apps/ui/dist`
with mtimes bumped +60s — never running npm), runs `python3 -B -m pytest -q
-p no:cacheprovider` over T1 (`tests/orchestration/test_pause_manifest.py`)
and the e2e file (`tests/ui_server/test_pause_e2e_live.py`) together from the
worktree root, after purging __pycache__ — restores the file BYTE-IDENTICAL,
and prints one line: label, real exit code, failed count and failing test
names. An unmutated control brackets the five mutations, first and last.
Ends with "restored byte-identical: True" per target file and "ALL MUTATIONS
CAUGHT AND RESTORED CLEANLY: <bool>". Undoes the live-test preparation
(unlinking node_modules) as its own last action, before the caller removes
the worktree itself.

Mutations:
  m1 `_park_job` writes no manifest.
  m2 `paused` is removed from `_VALID_STATUS`.
  m3 the worked-phase `paused` row loses `EXPECT_NOT_DISPATCHED` from its
     expectations.
  m4 the task cap's pause writes no manifest.
  m5 `_park_job`'s manifest write passes the pause request id as
     `stop_request_id`.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

PRIMARY_CHECKOUT = Path("/home/decodeux/Repos/remedy")
PRIMARY_UI = PRIMARY_CHECKOUT / "apps" / "ui"

PINGPONG_JOB_REL = "packages/orchestration/pingpong_job.py"
RUN_MANIFEST_REL = "packages/orchestration/run_manifest.py"

T1_TEST_FILE = "tests/orchestration/test_pause_manifest.py"
E2E_TEST_FILE = "tests/ui_server/test_pause_e2e_live.py"
TEST_FILES = [T1_TEST_FILE, E2E_TEST_FILE]

# --- m1: _park_job writes no manifest ---------------------------------------
M1_FROM = (
    "    if not _episode_snapshot_bound_ok(job):\n"
    "        _capture_input_snapshot(job, phase=_PHASE_PRE_WORK_STOP)\n"
    '    _write_run_manifest_record(job, status="paused", episode_id=job.active_episode_id)\n'
    "    return park_job_pause(job, signal, persist=_persist_job,\n"
)
M1_TO = (
    "    if not _episode_snapshot_bound_ok(job):\n"
    "        _capture_input_snapshot(job, phase=_PHASE_PRE_WORK_STOP)\n"
    "    return park_job_pause(job, signal, persist=_persist_job,\n"
)

# --- m2: paused is removed from _VALID_STATUS -------------------------------
M2_FROM = '_VALID_STATUS = frozenset({"completed", "stopped", "paused", "planned"})\n'
M2_TO = '_VALID_STATUS = frozenset({"completed", "stopped", "planned"})\n'

# --- m3: the worked-phase paused row loses EXPECT_NOT_DISPATCHED -----------
M3_FROM = (
    '    ("paused", PHASE_WORKED): {\n'
    "        # DECISION F025 D6 (round 8): equal to the stopped row above except the request id —\n"
    "        # a park is not a stop, so it carries none.\n"
    '        "capture": PHASE_EPISODE_START,\n'
    '        "expectations": {EXPECT_EXECUTED, EXPECT_PRIOR_EPISODE, EXPECT_SKIPPED,\n'
    "                         EXPECT_NOT_DISPATCHED, EXPECT_DISPATCHED_NO_CALLS,\n"
    '                         EXPECT_FAILED_PRE_DISPATCH},\n'
)
M3_TO = (
    '    ("paused", PHASE_WORKED): {\n'
    "        # DECISION F025 D6 (round 8): equal to the stopped row above except the request id —\n"
    "        # a park is not a stop, so it carries none.\n"
    '        "capture": PHASE_EPISODE_START,\n'
    '        "expectations": {EXPECT_EXECUTED, EXPECT_PRIOR_EPISODE, EXPECT_SKIPPED,\n'
    "                         EXPECT_DISPATCHED_NO_CALLS,\n"
    '                         EXPECT_FAILED_PRE_DISPATCH},\n'
)

# --- m4: the task cap's pause writes no manifest ----------------------------
M4_FROM = (
    "        elif job.state == JOB_PAUSED:\n"
    '            _write_run_manifest_record(job, status="paused",\n'
    "                                       episode_id=job.active_episode_id)\n"
)
M4_TO = ""

# --- m5: _park_job's manifest write passes the pause request id as ---------
# stop_request_id.
M5_FROM = '    _write_run_manifest_record(job, status="paused", episode_id=job.active_episode_id)\n'
M5_TO = (
    '    _write_run_manifest_record(job, status="paused", episode_id=job.active_episode_id,\n'
    "                               stop_request_id=signal.request_id)\n"
)

# (id, name, file, from, to)
MUTATIONS = [
    ("m1", "_park_job writes no manifest", PINGPONG_JOB_REL, M1_FROM, M1_TO),
    ("m2", "paused is removed from _VALID_STATUS", RUN_MANIFEST_REL, M2_FROM, M2_TO),
    ("m3", "the worked-phase paused row loses EXPECT_NOT_DISPATCHED",
     RUN_MANIFEST_REL, M3_FROM, M3_TO),
    ("m4", "the task cap's pause writes no manifest", PINGPONG_JOB_REL, M4_FROM, M4_TO),
    ("m5", "_park_job's manifest write passes the pause request id as stop_request_id",
     PINGPONG_JOB_REL, M5_FROM, M5_TO),
]


def sha256_of(path: Path) -> str:
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()


def purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        shutil.rmtree(cache_dir, ignore_errors=True)


def run_pytest(worktree: Path) -> dict:
    purge_pycache(worktree)
    env = dict(os.environ, REMEDY_UI_NO_AUTO_BUILD="1")
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "--tb=no", "-rf", *TEST_FILES],
        cwd=str(worktree), capture_output=True, text=True, env=env, timeout=300)
    out = proc.stdout + proc.stderr
    m_failed = re.search(r"(\d+) failed", out)
    m_error = re.search(r"(\d+) error", out)
    failed = (int(m_failed.group(1)) if m_failed else 0) + (int(m_error.group(1)) if m_error else 0)
    names = (re.findall(r"^FAILED (\S+)", out, re.MULTILINE)
             + re.findall(r"^ERROR (\S+)", out, re.MULTILINE))
    return {"exit": proc.returncode, "failed": failed, "names": names, "raw": out}


def fmt(label: str, result: dict) -> str:
    names = ", ".join(result["names"]) if result["names"] else "(none parsed)"
    return f"{label}: exit={result['exit']} failed={result['failed']} failing=[{names}]"


def prepare_live_worktree(worktree: Path) -> bool:
    """`.agent/authored/f025-r7-mutations.py`'s own route: never run npm."""
    linked = False
    node_modules_src = PRIMARY_UI / "node_modules"
    node_modules_link = worktree / "apps" / "ui" / "node_modules"
    if node_modules_src.is_dir() and not node_modules_link.exists():
        node_modules_link.symlink_to(node_modules_src, target_is_directory=True)
        linked = True
        print(f"{node_modules_link}: symlinked from the primary checkout")

    dist_src = PRIMARY_UI / "dist"
    dist_dst = worktree / "apps" / "ui" / "dist"
    if dist_src.is_dir() and (dist_src / "index.html").is_file() and not dist_dst.exists():
        shutil.copytree(dist_src, dist_dst)
        future = time.time() + 60
        for f in dist_dst.rglob("*"):
            if f.is_file():
                os.utime(f, (future, future))
        print(f"{dist_dst}: copied from the primary checkout, mtimes bumped +60s")
    return linked


def undo_live_worktree_prep(worktree: Path, linked: bool) -> None:
    node_modules_link = worktree / "apps" / "ui" / "node_modules"
    if linked:
        if node_modules_link.is_symlink():
            node_modules_link.unlink()
        elif node_modules_link.is_dir():
            shutil.rmtree(node_modules_link)
        print(f"{node_modules_link}: removed")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f025-r8-mutations.py <worktree_root>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()
    print(f"worktree: {worktree}")

    linked = prepare_live_worktree(worktree)

    all_ok = True
    control0 = run_pytest(worktree)
    print(f"CONTROL FIRST: {fmt('control', control0)}")
    if not (control0["exit"] == 0 and control0["failed"] == 0):
        print("control is not green; aborting")
        print("--- pytest output ---")
        print(control0["raw"][-4000:])
        undo_live_worktree_prep(worktree, linked)
        return 1

    originals: dict[str, bytes] = {}
    restores_ok = True
    for mid, name, file_rel, from_text, to_text in MUTATIONS:
        target = worktree / file_rel
        if file_rel not in originals:
            originals[file_rel] = target.read_bytes()
        original = target.read_bytes()
        digest = sha256_of(target)
        text = original.decode("utf-8")
        count = text.count(from_text)
        if count != 1:
            print(f"{mid} ({name}): SKIPPED, FROM occurrences {count} in {file_rel}")
            all_ok = False
            continue
        target.write_bytes(text.replace(from_text, to_text, 1).encode("utf-8"))
        try:
            result = run_pytest(worktree)
        finally:
            target.write_bytes(original)
        restored = sha256_of(target) == digest
        caught = result["exit"] != 0 and result["failed"] > 0
        all_ok = all_ok and caught and restored
        print(f"{mid} ({name}): {fmt(mid, result)} | caught={caught} "
              f"restored byte-identical={restored}")
        restores_ok = restores_ok and restored

    control1 = run_pytest(worktree)
    print(f"CONTROL LAST: {fmt('control', control1)}")
    last_green = control1["exit"] == 0 and control1["failed"] == 0
    all_ok = all_ok and last_green

    for file_rel, original in originals.items():
        target = worktree / file_rel
        final_restored = target.read_bytes() == original
        print(f"{file_rel}: restored byte-identical: {final_restored}")
        restores_ok = restores_ok and final_restored

    undo_live_worktree_prep(worktree, linked)

    overall = all_ok and restores_ok
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {overall}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
