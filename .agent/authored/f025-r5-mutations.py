#!/usr/bin/env python3
"""Mutation tool for F025 R5: R-1051's FIX, R-1052's FIX, U1 (the dashboard's
pause object) and U2-U6 (the paused node state, its treatment, mark, reducer
cases and seed).

Given a worktree path, runs an unmutated control of BOTH runners first and
last, and between them applies each mutation below (every FROM must occur
exactly once in its file), runs the relevant runner(s), restores the file
BYTE-IDENTICAL, and reports each mutation's label, runner, exit code, failed
count and failing test names. A mutation is caught when its runner goes red.

Python mutations (m1-m6) run `python3 -B -m pytest -q -p no:cacheprovider`
over T1 (tests/cli/test_job_pause.py) and T2 (tests/ui_server/test_dashboard_pause.py)
FROM THE WORKTREE ROOT, after purging __pycache__ — so a stale bytecode cache
can never serve a previous mutation's module.

TypeScript mutations (m7-m11) run vitest over the worktree's changed
`.test.ts` files by the SAME route `.agent/authored/f024-r1-mutations.py`
uses: vitest runs from the PRIMARY `apps/ui` (a worktree has no
node_modules), against a scratch config naming the WORKTREE's copies of the
changed test files, with its own cacheDir.

Usage: python3 -B f025-r5-mutations.py <worktree_root>
"""
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f025-r5-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

PAUSE_CONTROL_REL = "packages/orchestration/pause_control.py"
UI_SERVER_REL = "packages/orchestration/ui_server.py"
BRAIN_REDUCER_REL = "apps/ui/src/components/graph/brainReducer.ts"
NODE_STATES_REL = "apps/ui/src/components/graph/renderers/nodeStates.ts"
BRAIN_VIEW_REL = "apps/ui/src/components/graph/brainView.ts"

PY_TEST_FILES = [
    "tests/cli/test_job_pause.py",
    "tests/ui_server/test_dashboard_pause.py",
]

# Every `.test.ts` file this round's diff changed (db496696..HEAD) — the same
# fixed set is run for every TypeScript mutation, exactly as
# f024-r1-mutations.py runs its own fixed VITEST_FILES for every mutation.
TS_TEST_FILES = [
    "apps/ui/src/components/graph/brainReducer.test.ts",
    "apps/ui/src/components/graph/brainView.test.ts",
    "apps/ui/src/components/graph/renderers/nodeStates.test.ts",
    "apps/ui/src/components/graph/renderers/glyphConformance.test.ts",
    "apps/ui/src/components/graph/renderers/paintNode.test.ts",
    "apps/ui/src/api/remedyApi.test.ts",
]

MUTATIONS = [
    # --- R-1051's FIX (m1, m2) ------------------------------------------------
    {"id": "m1", "runner": "py",
     "name": "unpause_job_command answers parked before it looks for a pending pause",
     "file": PAUSE_CONTROL_REL,
     "from": (
         "    pending = withdraw_pause(job.job_id, control_root_path=control_root_path)\n"
         "    if pending is not None:\n"
         "        return {\"outcome\": \"withdrawn\", \"request_id\": pending.request_id, \"scope\": \"job\"}\n"
         "\n"
         "    if state == _PARKED_STATE and job.pause:\n"
         "        return {\"outcome\": \"parked\", \"scope\": \"job\",\n"
         "                \"next\": f\"remedy job run {job.job_id}\"}\n"
         "\n"
         "    return {\"outcome\": \"not_paused\", \"scope\": \"job\"}\n"
     ),
     "to": (
         "    if state == _PARKED_STATE:\n"
         "        return {\"outcome\": \"parked\", \"scope\": \"job\",\n"
         "                \"next\": f\"remedy job run {job.job_id}\"}\n"
         "\n"
         "    pending = withdraw_pause(job.job_id, control_root_path=control_root_path)\n"
         "    if pending is None:\n"
         "        return {\"outcome\": \"not_paused\", \"scope\": \"job\"}\n"
         "    return {\"outcome\": \"withdrawn\", \"request_id\": pending.request_id, \"scope\": \"job\"}\n"
     )},
    {"id": "m2", "runner": "py",
     "name": "a job in state paused with an EMPTY pause record answers parked",
     "file": PAUSE_CONTROL_REL,
     "from": (
         "    if state == _PARKED_STATE and job.pause:\n"
         "        return {\"outcome\": \"parked\", \"scope\": \"job\",\n"
         "                \"next\": f\"remedy job run {job.job_id}\"}\n"
     ),
     "to": (
         "    if state == _PARKED_STATE:\n"
         "        return {\"outcome\": \"parked\", \"scope\": \"job\",\n"
         "                \"next\": f\"remedy job run {job.job_id}\"}\n"
     )},
    # --- R-1052's FIX (m3, m4) -------------------------------------------------
    {"id": "m3", "runner": "py",
     "name": "task_paused is written only when the call created the entry",
     "file": PAUSE_CONTROL_REL,
     "from": (
         "        pause = request_task_pause(job.job_id, task_id, reason, source,\n"
         "                                   control_root_path=control_root_path)\n"
         "        # R-1052: exactly once per request id BY THE LEDGER, as `job_paused` is — not\n"
         "        # by whether this call is the one that created the control-file entry, which\n"
         "        # a retry after a failed write can never be.\n"
         "        already = _task_pause_event_exists(job.job_id, \"task_paused\", pause.request_id)\n"
         "        if already is not None and not already:\n"
         "            _write_task_paused_event(job, pause)\n"
     ),
     "to": (
         "        already = any(\n"
         "            p.task_id == task_id\n"
         "            for p in paused_tasks(job.job_id, control_root_path=control_root_path))\n"
         "        pause = request_task_pause(job.job_id, task_id, reason, source,\n"
         "                                   control_root_path=control_root_path)\n"
         "        if not already:\n"
         "            _write_task_paused_event(job, pause)\n"
     )},
    {"id": "m4", "runner": "py",
     "name": "a release removes the entry before it writes task_resumed",
     "file": PAUSE_CONTROL_REL,
     "from": (
         "        pause = next(\n"
         "            (p for p in paused_tasks(job.job_id, control_root_path=control_root_path)\n"
         "             if p.task_id == task_id), None)\n"
         "        if pause is None:\n"
         "            return {\"outcome\": \"not_paused\", \"scope\": \"task\", \"task_id\": task_id}\n"
         "        # R-1052: the event is written BEFORE the entry is released, so a failed\n"
         "        # write raises with the task still paused — the retry finds the same\n"
         "        # entry, the same request id, and writes the missing event exactly once.\n"
         "        already = _task_pause_event_exists(job.job_id, \"task_resumed\", pause.request_id)\n"
         "        if already is not None and not already:\n"
         "            _write_task_resumed_event(job, pause)\n"
         "        release_task_pause(job.job_id, task_id, control_root_path=control_root_path)\n"
     ),
     "to": (
         "        pause = release_task_pause(job.job_id, task_id, control_root_path=control_root_path)\n"
         "        if pause is None:\n"
         "            return {\"outcome\": \"not_paused\", \"scope\": \"task\", \"task_id\": task_id}\n"
         "        _write_task_resumed_event(job, pause)\n"
     )},
    # --- U1: the dashboard's pause object (m5, m6) ------------------------------
    {"id": "m5", "runner": "py",
     "name": "the dashboard's paused_task_ids keeps a paused task that is done",
     "file": UI_SERVER_REL,
     "from": '        paused_task_ids = [tid for tid in order if tid in paused_ids and tid in pending_ids]\n',
     "to": '        paused_task_ids = [tid for tid in order if tid in paused_ids]\n'},
    {"id": "m6", "runner": "py",
     "name": "the dashboard raises on a PauseControlError instead of reporting error",
     "file": UI_SERVER_REL,
     "from": "    except (PauseControlError, StopControlError) as exc:\n",
     "to": "    except () as exc:\n"},
    # --- U6: the reducer's four cases (m7, m8, m9) ------------------------------
    {"id": "m7", "runner": "ts",
     "name": "the reducer ignores task_paused",
     "file": BRAIN_REDUCER_REL,
     "from": (
         "    case \"task_paused\":\n"
         "      return row.taskId === \"\" ? ignoreRow(model, row) : onTaskPaused(model, row);\n"
     ),
     "to": "    case \"task_paused\":\n      return ignoreRow(model, row);\n"},
    {"id": "m8", "runner": "ts",
     "name": "task_resumed leaves the node paused",
     "file": BRAIN_REDUCER_REL,
     "from": '  const nodes = setTaskState(model.nodes, row.taskId, "planned");\n  return { ...model, nodes };\n}\n\n/** `job_paused`',
     "to": '  const nodes = setTaskState(model.nodes, row.taskId, "paused");\n  return { ...model, nodes };\n}\n\n/** `job_paused`'},
    {"id": "m9", "runner": "ts",
     "name": "job_paused leaves in-progress run nodes in_progress",
     "file": BRAIN_REDUCER_REL,
     "from": '    if (isRunKind(n.kind) && n.state === "in_progress") return { ...n, state: "paused" as NodeState };\n',
     "to": ""},
    # --- U4/U5: the treatment and the mark (m10) --------------------------------
    {"id": "m10", "runner": "ts",
     "name": "the paused treatment drops the pause mark",
     "file": NODE_STATES_REL,
     "from": (
         "    marks: [\n"
         "      { mark: \"ring\", token: \"--remedy-state-planned-ring\", outlineToken: null },\n"
         "      { mark: \"pause\", token: \"--remedy-orange-400\", outlineToken: \"--remedy-graph-node-ring\" },\n"
         "    ],\n"
     ),
     "to": (
         "    marks: [\n"
         "      { mark: \"ring\", token: \"--remedy-state-planned-ring\", outlineToken: null },\n"
         "    ],\n"
     )},
    # --- U6: the seed (m11) -----------------------------------------------------
    {"id": "m11", "runner": "ts",
     "name": "the seed ignores pausedTaskIds",
     "file": BRAIN_VIEW_REL,
     "from": "  const paused = new Set(pausedTaskIds);\n",
     "to": "  const paused = new Set<string>();\n"},
]


def sha256_of(path: Path) -> str:
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()


def purge_pycache(worktree: Path) -> None:
    for d in worktree.rglob("__pycache__"):
        shutil.rmtree(d, ignore_errors=True)


def run_pytest(worktree: Path) -> dict:
    purge_pycache(worktree)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=no", "-rf"]
        + PY_TEST_FILES,
        cwd=str(worktree), capture_output=True, text=True, timeout=180)
    out = proc.stdout + proc.stderr
    m = re.search(r"(\d+) failed", out)
    failed = int(m.group(1)) if m else 0
    names = re.findall(r"^FAILED (\S+)", out, re.MULTILINE)
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
    if failed == 0 and "failed" not in out.lower():
        failed = 0
    names = re.findall(r"^\s*[×✗]\s+(.+?)\s*(?:\d+ms)?$", out, re.MULTILINE)
    return {"exit": proc.returncode, "failed": failed, "names": names, "raw": out}


def run_control(worktree: Path, tag: str) -> tuple[dict, dict]:
    return run_pytest(worktree), run_vitest(worktree, tag)


def fmt_control(py: dict, ts: dict) -> str:
    return (f"pytest exit={py['exit']} failed={py['failed']} | "
            f"vitest exit={ts['exit']} failed={ts['failed']}")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f025-r5-mutations.py <worktree_root>", file=sys.stderr)
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
