#!/usr/bin/env python3
"""F026 R5 G4 — the red proofs.

Given a worktree path, runs an unmutated control of BOTH runners first and last, and
between them applies each mutation below (every FROM must occur exactly once in its
file), runs the relevant runner, restores the file BYTE-IDENTICAL, and reports each
mutation's label, runner, exit code, failed count and failing test names. A mutation
is caught when its runner goes red.

m1 (TypeScript, R-1061) runs vitest over the worktree's changed `.test.ts` file by the
SAME route `.agent/authored/f026-r4-mutations.py` uses (itself copying
`f025-r6-mutations.py`'s route): vitest runs from the PRIMARY `apps/ui` (a worktree has
no `node_modules`), against a scratch config naming the WORKTREE's copy of the one
`.test.ts` file this round's diff changed, with its own cacheDir.

m2 and m3 (Python, R-1062) run
`python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_task_edit_runtime.py`
FROM THE WORKTREE ROOT, after purging `__pycache__` — so a stale bytecode cache can
never serve a previous mutation's module.

Usage: python3 -B f026-r5-mutations.py <worktree_root>
"""
from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f026-r5-worker/mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

TASK_EDIT_SEND_REL = "apps/ui/src/api/taskEditSend.ts"
TASK_EDIT_RUNTIME_REL = "packages/orchestration/task_edit_runtime.py"

PY_TEST_FILES = [
    "tests/orchestration/test_task_edit_runtime.py",
]

# The one `.test.ts` file this round's diff changed.
TS_TEST_FILES = [
    "apps/ui/src/api/taskEditSend.test.ts",
]

MUTATIONS = [
    # --- S1: the relaunch sentence (m1, R-1061) -----------------------------
    {"id": "m1", "runner": "ts",
     "name": "the relaunch sentence goes back to the literal <job id>",
     "file": TASK_EDIT_SEND_REL,
     "from": (
         'function relaunchSentence(jobId: string): string {\n'
         '  if (jobId === "") {\n'
         '    return "Relaunch the job to run it.";\n'
         '  }\n'
         '  return `Relaunch the job to run it: remedy job run ${jobId}.`;\n'
         '}\n'
     ),
     "to": (
         'function relaunchSentence(jobId: string): string {\n'
         '  return "Relaunch the job to run it: remedy job run <job id>.";\n'
         '}\n'
     )},
    # --- S2: the pending DoD re-sync note (m2, m3, R-1062) ------------------
    {"id": "m2", "runner": "py",
     "name": "dod_resync_pending is always false",
     "file": TASK_EDIT_RUNTIME_REL,
     "from": '        dod_resync_pending = "acceptance" in fields and has_stored_dod\n',
     "to": '        dod_resync_pending = False\n'},
    {"id": "m3", "runner": "py",
     "name": "dod_resync_pending is true without a stored DoD",
     "file": TASK_EDIT_RUNTIME_REL,
     "from": '        dod_resync_pending = "acceptance" in fields and has_stored_dod\n',
     "to": '        dod_resync_pending = "acceptance" in fields\n'},
]


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def purge_pycache(worktree: Path) -> None:
    for d in worktree.rglob("__pycache__"):
        shutil.rmtree(d, ignore_errors=True)


def run_pytest(worktree: Path) -> dict:
    purge_pycache(worktree)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=no", "-rfE"]
        + PY_TEST_FILES,
        cwd=str(worktree), capture_output=True, text=True, timeout=180)
    out = proc.stdout + proc.stderr
    m_failed = re.search(r"(\d+) failed", out)
    m_error = re.search(r"(\d+) error", out)
    failed = (int(m_failed.group(1)) if m_failed else 0) + (int(m_error.group(1)) if m_error else 0)
    names = re.findall(r"^FAILED (\S+)", out, re.MULTILINE) + re.findall(r"^ERROR (\S+)", out, re.MULTILINE)
    return {"exit": proc.returncode, "failed": failed, "names": names, "raw": out}


def run_vitest(worktree: Path, tag: str) -> dict:
    cache_dir = HELPER_DIR / f"cache-{tag}-{int(time.time() * 1000)}"
    config = HELPER_DIR / f"vitest.config.{tag}.mjs"
    include = ", ".join(f'"{worktree / f}"' for f in TS_TEST_FILES)
    config.write_text(
        "export default {\n"
        f'  root: "{PRIMARY_UI}",\n'
        f'  cacheDir: "{cache_dir}",\n'
        f'  test: {{ environment: "node", include: [{include}] }},\n'
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
    return run_pytest(worktree), run_vitest(worktree, tag)


def fmt_control(py: dict, ts: dict) -> str:
    return (f"pytest exit={py['exit']} failed={py['failed']} | "
            f"vitest exit={ts['exit']} failed={ts['failed']}")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f026-r5-mutations.py <worktree_root>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()
    print(f"worktree: {worktree}")

    py0, ts0 = run_control(worktree, "control-first")
    print(f"CONTROL FIRST: {fmt_control(py0, ts0)}")
    first_green = py0["exit"] == 0 and py0["failed"] == 0 and ts0["exit"] == 0 and ts0["failed"] == 0
    if not first_green:
        print("control is not green; aborting")
        print("--- pytest output ---")
        print(py0["raw"][-4000:])
        print("--- vitest output ---")
        print(ts0["raw"][-4000:])
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
            if mut["runner"] == "py":
                result = run_pytest(worktree)
            else:
                result = run_vitest(worktree, mut["id"])
        finally:
            target.write_bytes(original)
        restored = sha256_of(target) == digest
        caught = result["exit"] != 0 and result["failed"] > 0
        all_ok &= caught and restored
        names = ", ".join(result["names"]) if result["names"] else "(none parsed)"
        print(f"{mut['id']} ({mut['name']}) [{mut['runner']}]: exit={result['exit']} "
              f"failed={result['failed']} failing=[{names}] | caught={caught} "
              f"restored byte-identical={restored}")

    py1, ts1 = run_control(worktree, "control-last")
    print(f"CONTROL LAST: {fmt_control(py1, ts1)}")
    last_green = py1["exit"] == 0 and py1["failed"] == 0 and ts1["exit"] == 0 and ts1["failed"] == 0
    all_ok &= last_green
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
