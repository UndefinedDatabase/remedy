#!/usr/bin/env python3
"""Mutation tool for F025 R7 G5 — red-proves R-1053's fix (m1), R-1054's fix
(m2) and DECISION F025 D5's end-to-end (m3-m5).

Usage: python3 -B f025-r7-mutations.py <worktree_root>

For each mutation, edits its named production/source file INSIDE the given
worktree (asserting its FROM text occurs exactly once), runs the mutation's
own runner — vitest over `pauseView.test.ts`, by `.agent/authored/
f025-r6-mutations.py`'s route (a scratch config, from the PRIMARY `apps/ui`,
naming the worktree's own copy of the test file), or `python3 -B -m pytest
-q -p no:cacheprovider` over the mutation's named test file(s) from the
worktree root, after purging __pycache__ — restores the file BYTE-IDENTICAL,
and prints one line: label, runner, real exit code, failed count and failing
test names. An unmutated control of BOTH runners brackets the five
mutations, first and last. Ends with "restored byte-identical: True" per
target file and "ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>".

m3-m5 exercise `tests/ui_server/test_pause_e2e_live.py`, which starts a real
`start_ui_server` the same way `test_pause_door_live.py` does — so this tool
prepares the worktree for the live tests by `.agent/authored/
f025-r4-mutations.py`'s own route FIRST (symlinking apps/ui/node_modules in
and COPYING apps/ui/dist with mtimes bumped +60s, never running npm), and
undoes that preparation (unlinking node_modules) as its own last action,
before the caller removes the worktree itself.
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
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"
HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f025-r7-mutscratch")

PAUSE_VIEW_REL = "apps/ui/src/api/pauseView.ts"
POPOVER_REL = "apps/ui/src/components/detail/DetailPopover.tsx"
PINGPONG_JOB_REL = "packages/orchestration/pingpong_job.py"
PAUSE_CONTROL_REL = "packages/orchestration/pause_control.py"

VITEST_TEST_FILE = "apps/ui/src/api/pauseView.test.ts"
CONTRACT_TEST_FILE = "tests/ui_contracts/test_pause_controls_contract.py"
E2E_TEST_FILE = "tests/ui_server/test_pause_e2e_live.py"

CONTROL_PY_FILES = [CONTRACT_TEST_FILE, E2E_TEST_FILE]

# --- m1: taskPauseAction answers "pause" for a task in state `current` -----
M1_FROM = (
    '  if (taskState === "pending") {\n'
    '    return "pause";\n'
    "  }\n"
)
M1_TO = (
    '  if (taskState === "pending" || taskState === "current") {\n'
    '    return "pause";\n'
    "  }\n"
)

# --- m2: the popover's PauseControl loses its key={task.id} ----------------
M2_FROM = "          key={task.id}\n"
M2_TO = ""

# --- m3: lift_job_pause's body raises instead of lifting the pause ---------
M3_FROM = (
    "    if not job.pause:\n"
    "        return\n"
    "    resumed_at = datetime.now(timezone.utc).isoformat()\n"
    "    _append_job_resumed_event(job, job.pause, resumed_at)\n"
    "    job.pause = {}\n"
)
M3_TO = '    raise RuntimeError("m3 probe")\n'

# --- m4: unpause_job_command answers not_paused where it answers parked ----
M4_FROM = (
    "    if state == _PARKED_STATE and job.pause:\n"
    '        return {"outcome": "parked", "scope": "job",\n'
    '                "next": f"remedy job run {job.job_id}"}\n'
)
M4_TO = (
    "    if state == _PARKED_STATE and job.pause:\n"
    '        return {"outcome": "not_paused", "scope": "job"}\n'
)

# --- m5: park_job_pause leaves job.pause empty ------------------------------
M5_FROM = (
    "    job.state = JOB_PAUSED\n"
    "    job.pause = {\n"
    '        "scope": signal.scope,\n'
    '        "request_id": signal.request_id,\n'
    '        "reason": reason,\n'
    '        "source": signal.source,\n'
    '        "requested_at": signal.requested_at,\n'
    '        "paused_at": datetime.now(timezone.utc).isoformat(),\n'
    '        "paused_task_ids": list(signal.paused_task_ids),\n'
    '        "withheld_task_ids": list(signal.withheld_task_ids),\n'
    "    }\n"
)
M5_TO = (
    "    job.state = JOB_PAUSED\n"
    "    job.pause = {}\n"
)

# (id, name, runner, file, from, to, pytest target files)
MUTATIONS = [
    ("m1", "taskPauseAction answers pause for a task in state current",
     "vitest", PAUSE_VIEW_REL, M1_FROM, M1_TO, None),
    ("m2", "the popover's key={task.id} is deleted",
     "pytest", POPOVER_REL, M2_FROM, M2_TO, [CONTRACT_TEST_FILE]),
    ("m3", 'lift_job_pause\'s body is replaced by raise RuntimeError("m3 probe")',
     "pytest", PINGPONG_JOB_REL, M3_FROM, M3_TO, [E2E_TEST_FILE]),
    ("m4", "unpause_job_command answers not_paused where it answers parked",
     "pytest", PAUSE_CONTROL_REL, M4_FROM, M4_TO, [E2E_TEST_FILE]),
    ("m5", "the park leaves job.pause empty (park_job_pause assigns {})",
     "pytest", PINGPONG_JOB_REL, M5_FROM, M5_TO, [E2E_TEST_FILE]),
]


def sha256_of(path: Path) -> str:
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()


def purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        shutil.rmtree(cache_dir, ignore_errors=True)


def run_pytest(worktree: Path, files: list[str]) -> dict:
    purge_pycache(worktree)
    env = dict(os.environ, REMEDY_UI_NO_AUTO_BUILD="1")
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "--tb=no", "-rf", *files],
        cwd=str(worktree), capture_output=True, text=True, env=env, timeout=300)
    out = proc.stdout + proc.stderr
    m_failed = re.search(r"(\d+) failed", out)
    m_error = re.search(r"(\d+) error", out)
    failed = (int(m_failed.group(1)) if m_failed else 0) + (int(m_error.group(1)) if m_error else 0)
    names = re.findall(r"^FAILED (\S+)", out, re.MULTILINE) + re.findall(r"^ERROR (\S+)", out, re.MULTILINE)
    return {"exit": proc.returncode, "failed": failed, "names": names, "raw": out}


def run_vitest(worktree: Path, tag: str) -> dict:
    HELPER_DIR.mkdir(parents=True, exist_ok=True)
    cache_dir = HELPER_DIR / f"cache-{tag}-{int(time.time() * 1000)}"
    config = HELPER_DIR / f"vitest.config.{tag}.mjs"
    target = worktree / VITEST_TEST_FILE
    config.write_text(
        "export default {\n"
        f'  root: "{PRIMARY_UI}",\n'
        f'  cacheDir: "{cache_dir}",\n'
        f'  test: {{ environment: "node", include: ["{target}"] }},\n'
        "};\n"
    )
    proc = subprocess.run([str(VITEST_BIN), "run", "--config", str(config)],
                          cwd=str(PRIMARY_UI), capture_output=True, text=True, timeout=180)
    out = proc.stdout + proc.stderr
    m = re.search(r"Tests\s+(\d+)\s+failed\s*\|\s*(\d+)\s+passed", out)
    failed = int(m.group(1)) if m else 0
    names = re.findall(r"^\s*[×✗]\s+(.+?)\s*(?:\d+ms)?$", out, re.MULTILINE)
    return {"exit": proc.returncode, "failed": failed, "names": names, "raw": out}


def run_control(worktree: Path, tag: str) -> tuple[dict, dict]:
    return run_pytest(worktree, CONTROL_PY_FILES), run_vitest(worktree, tag)


def fmt(label: str, runner: str, result: dict) -> str:
    names = ", ".join(result["names"]) if result["names"] else "(none parsed)"
    return (f"{label} [{runner}]: exit={result['exit']} failed={result['failed']} "
            f"failing=[{names}]")


def prepare_live_worktree(worktree: Path) -> bool:
    """`.agent/authored/f025-r4-mutations.py`'s own route: never run npm."""
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
        print("usage: f025-r7-mutations.py <worktree_root>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()
    print(f"worktree: {worktree}")

    linked = prepare_live_worktree(worktree)

    all_ok = True
    py0, ts0 = run_control(worktree, "control-first")
    print(f"CONTROL FIRST: {fmt('pytest', 'pytest', py0)} | {fmt('vitest', 'vitest', ts0)}")
    if not (py0["exit"] == 0 and py0["failed"] == 0 and ts0["exit"] == 0 and ts0["failed"] == 0):
        print("control is not green; aborting")
        print("--- pytest output ---")
        print(py0["raw"][-4000:])
        print("--- vitest output ---")
        print(ts0["raw"][-4000:])
        undo_live_worktree_prep(worktree, linked)
        return 1

    originals: dict[str, bytes] = {}
    restores_ok = True
    for mid, name, runner, file_rel, from_text, to_text, py_files in MUTATIONS:
        target = worktree / file_rel
        if file_rel not in originals:
            originals[file_rel] = target.read_bytes()
        original = target.read_bytes()
        digest = sha256_of(target)
        text = original.decode("utf-8")
        count = text.count(from_text)
        if count != 1:
            print(f"{mid} ({name}) [{runner}]: SKIPPED, FROM occurrences {count} in {file_rel}")
            all_ok = False
            continue
        target.write_bytes(text.replace(from_text, to_text, 1).encode("utf-8"))
        try:
            if runner == "vitest":
                result = run_vitest(worktree, mid)
            else:
                result = run_pytest(worktree, py_files)
        finally:
            target.write_bytes(original)
        restored = sha256_of(target) == digest
        caught = result["exit"] != 0 and result["failed"] > 0
        all_ok = all_ok and caught and restored
        print(f"{mid} ({name}) [{runner}]: {fmt(mid, runner, result)} | "
              f"caught={caught} restored byte-identical={restored}")
        restores_ok = restores_ok and restored

    py1, ts1 = run_control(worktree, "control-last")
    print(f"CONTROL LAST: {fmt('pytest', 'pytest', py1)} | {fmt('vitest', 'vitest', ts1)}")
    last_green = py1["exit"] == 0 and py1["failed"] == 0 and ts1["exit"] == 0 and ts1["failed"] == 0
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
