"""F288 R3 G5 — mutation (red-proof) tool for the long-run cycle's attempt id
and result (DECISION F288 D3 (1)), the rows' `attemptId`/`planTaskIds`
(D3 (2)) and the reducer's plan-approval, test-run and repair-run births
(D3 (3)).

Takes a worktree path. For each mutation below it edits the named file
INSIDE that worktree (asserting its FROM text occurs exactly once), runs the
named tests, restores the file's exact original bytes, and prints one line:
the label, the exit code, the failed count and the failing test names.

Python mutations (m1-m4, `packages/orchestration/long_run_executor.py` and
`ui_server.py`) run `python3 -B -m pytest -q -p no:cacheprovider` over the
worktree's `tests/orchestration/test_self_healing_cycles.py` and
`tests/ui_server/test_sse_stream.py`, from the worktree's root, after purging
its `__pycache__` directories.

TypeScript mutations (m5-m15, the four vitest files below) run
`apps/ui/node_modules/.bin/vitest run --config <scratch config>` from the
PRIMARY `apps/ui` (a worktree carries no `node_modules`, DECISION F256 D6),
where the scratch config is a PLAIN OBJECT — `root` the primary `apps/ui`,
`cacheDir` under `.remedy-wt/`, and `test.include` the WORKTREE's copies of
`feedRow.test.ts`, `brainReducer.test.ts`, `phaseMapping.test.ts` and
`brainDemoRecording.test.ts`, by absolute path. A config importing
`vitest/config` cannot resolve outside `apps/ui`'s own install, which is why
the config is a bare object instead.

An unmutated CONTROL run happens first and last, for EACH runner. Before the
mutations, one ROUTE PROOF mutation (breaking `feedRow.ts` inside the
worktree so any test importing it throws) proves the vitest route reads the
WORKTREE's sources rather than the primary checkout's — a green run there
would mean every later TypeScript mutation is a false proof.

Usage:
    python3 -B f288-r3-mutations.py <worktree_path>
"""
from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path

PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"
SCRATCH_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f288-r3-worker/mutscratch")

PY_TEST_PATHS = (
    "tests/orchestration/test_self_healing_cycles.py",
    "tests/ui_server/test_sse_stream.py",
)
TS_TEST_FILES = (
    "apps/ui/src/api/feedRow.test.ts",
    "apps/ui/src/components/graph/brainReducer.test.ts",
    "apps/ui/src/components/timeline/phaseMapping.test.ts",
    "apps/ui/src/components/graph/brainDemoRecording.test.ts",
)

_LONG_RUN_EXECUTOR = "packages/orchestration/long_run_executor.py"
_UI_SERVER = "packages/orchestration/ui_server.py"
_FEED_ROW = "apps/ui/src/api/feedRow.ts"
_BRAIN_REDUCER = "apps/ui/src/components/graph/brainReducer.ts"
_BRAIN_ONTOLOGY = "apps/ui/src/components/graph/brainOntology.ts"
_PHASE_MAPPING = "apps/ui/src/components/timeline/phaseMapping.ts"

#: Run once, before m1, never counted in ALL MUTATIONS CAUGHT: proves the
#: vitest route reads the WORKTREE's `feedRow.ts`, not the primary's.
ROUTE_PROOF = {
    "id": "route_proof",
    "name": "the vitest route reads the WORKTREE's feedRow.ts, not the primary's",
    "runner": "ts",
    "file": _FEED_ROW,
    "from": "  const envelope = envelopeOf(frame);\n",
    "to": '  throw new Error("f288-r3 route proof");\n',
}

#: (id, name, runner, file, FROM, TO). FROM must occur exactly once in the
#: file at the time of the edit; every mutation starts from the file's own
#: pristine bytes.
MUTATIONS: tuple[dict[str, str], ...] = (
    {
        "id": "m1", "name": "cycle_repair_round carries no attempt_id",
        "runner": "py", "file": _LONG_RUN_EXECUTOR,
        "from": (
            "              stop_reason=repair.stop_reason,\n"
            '              attempt_id=f"cycle-{cycle_index}",\n'
            '              outcome="changed" if repair.changed_files else "unchanged")\n'
        ),
        "to": (
            "              stop_reason=repair.stop_reason,\n"
            '              outcome="changed" if repair.changed_files else "unchanged")\n'
        ),
    },
    {
        "id": "m2", "name": "cycle_repair_round reads changed whatever its changed files",
        "runner": "py", "file": _LONG_RUN_EXECUTOR,
        "from": 'outcome="changed" if repair.changed_files else "unchanged")\n',
        "to": 'outcome="changed")\n',
    },
    {
        "id": "m3", "name": "cycle_completed carries no outcome",
        "runner": "py", "file": _LONG_RUN_EXECUTOR,
        "from": (
            "            _emit(log, LEDGER_EVENT_CYCLE_COMPLETED, **record.to_json(),\n"
            '                  attempt_id=f"cycle-{cycle_index}", outcome=record.verify_result)\n'
        ),
        "to": (
            "            _emit(log, LEDGER_EVENT_CYCLE_COMPLETED, **record.to_json(),\n"
            '                  attempt_id=f"cycle-{cycle_index}")\n'
        ),
    },
    {
        "id": "m4", "name": "ATTEMPT_EVENT_KINDS loses cycle_healed",
        "runner": "py", "file": _UI_SERVER,
        "from": (
            '    "cycle_repair_round",\n'
            '    "cycle_healed",\n'
            '    "cycle_completed",\n'
        ),
        "to": (
            '    "cycle_repair_round",\n'
            '    "cycle_completed",\n'
        ),
    },
    {
        "id": "m5", "name": "feedRowOf reads the envelope key attemptId instead of attempt_id",
        "runner": "ts", "file": _FEED_ROW,
        "from": '    attemptId: stringField(envelope, "attempt_id"),\n',
        "to": '    attemptId: stringField(envelope, "attemptId"),\n',
    },
    {
        "id": "m6", "name": "feedRowOf keeps non-string plan task ids",
        "runner": "ts", "file": _FEED_ROW,
        "from": '  return taskIds.filter((value): value is string => typeof value === "string");\n',
        "to": "  return taskIds;\n",
    },
    {
        "id": "m7", "name": "plan_approved births nothing",
        "runner": "ts", "file": _BRAIN_REDUCER,
        "from": '    case "plan_approved":\n      return onPlanApproved(model, row);\n',
        "to": '    case "plan_approved":\n      return { ...model };\n',
    },
    {
        "id": "m8", "name": "plan_approved sets an existing task back to planned",
        "runner": "ts", "file": _BRAIN_REDUCER,
        "from": (
            "  for (const taskId of taskIds) {\n"
            "    const born = birthTask(nodes, links, taskId, row.seq);\n"
            "    nodes = born.nodes;\n"
            "    links = born.links;\n"
            "  }\n"
        ),
        "to": (
            "  for (const taskId of taskIds) {\n"
            "    const born = birthTask(nodes, links, taskId, row.seq);\n"
            '    nodes = setTaskState(born.nodes, taskId, "planned");\n'
            "    links = born.links;\n"
            "  }\n"
        ),
    },
    {
        "id": "m9", "name": "plan_approved ranks its new tasks in reverse order",
        "runner": "ts", "file": _BRAIN_REDUCER,
        "from": "  for (const taskId of taskIds) {\n",
        "to": "  for (const taskId of [...taskIds].reverse()) {\n",
    },
    {
        "id": "m10", "name": "task_round_tested births a review_run",
        "runner": "ts", "file": _BRAIN_REDUCER,
        "from": (
            '    case "task_round_tested":\n'
            '      return row.taskId === "" ? ignoreRow(model, row) : onTestRun(model, row);\n'
        ),
        "to": (
            '    case "task_round_tested":\n'
            '      return row.taskId === "" ? ignoreRow(model, row) : onTaskRoundCompleted(model, row);\n'
        ),
    },
    {
        "id": "m11", "name": "REPAIR_OUTCOME_STATE_TABLE maps unchanged to pass",
        "runner": "ts", "file": _BRAIN_ONTOLOGY,
        "from": '  unchanged: "blocked",\n',
        "to": '  unchanged: "pass",\n',
    },
    {
        "id": "m12", "name": "task_round_repaired falls to default",
        "runner": "ts", "file": _BRAIN_REDUCER,
        "from": (
            '    case "task_round_repaired":\n'
            '      return row.taskId === "" ? ignoreRow(model, row) : onRepairRun(model, row);\n'
        ),
        "to": "",
    },
    {
        "id": "m13", "name": "test_run_completed without a task id births a task anyway",
        "runner": "ts", "file": _BRAIN_REDUCER,
        "from": (
            '    case "test_run_completed":\n'
            '    case "test_run_timed_out":\n'
            '    case "test_run_blocked":\n'
            '      return row.taskId === "" ? ignoreRow(model, row) : onTestRun(model, row);\n'
        ),
        "to": (
            '    case "test_run_completed":\n'
            '    case "test_run_timed_out":\n'
            '    case "test_run_blocked":\n'
            "      return onTestRun(model, row);\n"
        ),
    },
    {
        "id": "m14", "name": "a run's meta carries attemptId: \"\" when its row has none",
        "runner": "ts", "file": _BRAIN_REDUCER,
        "from": "  return row.attemptId ? { ...meta, attemptId: row.attemptId } : meta;\n",
        "to": '  return { ...meta, attemptId: row.attemptId ?? "" };\n',
    },
    {
        "id": "m15", "name": "PHASE_MARKER_TABLE loses plan_approved",
        "runner": "ts", "file": _PHASE_MAPPING,
        "from": '  plan_approved: "planning",\n',
        "to": "",
    },
)


def _purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        if cache_dir.is_dir():
            for child in sorted(cache_dir.rglob("*"), reverse=True):
                if child.is_file():
                    child.unlink()
                else:
                    child.rmdir()
            cache_dir.rmdir()


def _run_py(root: Path) -> dict[str, object]:
    _purge_pycache(root)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *PY_TEST_PATHS],
        cwd=str(root), capture_output=True, text=True, timeout=180,
    )
    failed_names = [
        line[len("FAILED "):].split(" ", 1)[0]
        for line in proc.stdout.splitlines()
        if line.startswith("FAILED ")
    ]
    return {"exit": proc.returncode, "failed": len(failed_names), "names": failed_names}


def _run_ts(root: Path, tag: str) -> dict[str, object]:
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    cache_dir = SCRATCH_DIR / f"cache-{tag}-{int(time.time() * 1000)}"
    config = SCRATCH_DIR / f"vitest.config.{tag}.mjs"
    include = ", ".join(f'"{root / f}"' for f in TS_TEST_FILES)
    config.write_text(
        "export default {\n"
        f'  root: "{PRIMARY_UI}",\n'
        f'  cacheDir: "{cache_dir}",\n'
        f'  test: {{ environment: "node", include: [{include}] }},\n'
        "};\n"
    )
    proc = subprocess.run(
        [str(VITEST_BIN), "run", "--config", str(config)],
        cwd=str(PRIMARY_UI), capture_output=True, text=True, timeout=180,
    )
    out = proc.stdout + proc.stderr
    m = re.search(r"Tests\s+(\d+)\s+failed\s*\|\s*(\d+)\s+passed", out)
    if m:
        failed = int(m.group(1))
    elif re.search(r"Tests\s+(\d+)\s+passed", out):
        failed = 0
    else:
        failed = -1
    names = re.findall(r"^\s*(?:×|✗)\s+(.+)$", out, re.MULTILINE)
    return {"exit": proc.returncode, "failed": failed, "names": names}


def _run(root: Path, runner: str, tag: str) -> dict[str, object]:
    return _run_py(root) if runner == "py" else _run_ts(root, tag)


def _fmt(label: str, result: dict[str, object]) -> str:
    return f"{label}: exit={result['exit']} failed={result['failed']} names={result['names']}"


def main(worktree: str) -> bool:
    root = Path(worktree).resolve()
    all_ok = True

    py_control_first = _run(root, "py", "control-first")
    print(_fmt("control py (before)", py_control_first))
    ts_control_first = _run(root, "ts", "control-first")
    print(_fmt("control ts (before)", ts_control_first))
    all_ok = all_ok and py_control_first["exit"] == 0 and py_control_first["failed"] == 0
    all_ok = all_ok and ts_control_first["exit"] == 0 and ts_control_first["failed"] == 0

    # --- the route proof, before m1 -----------------------------------------
    proof_target = root / ROUTE_PROOF["file"]
    proof_original = proof_target.read_bytes()
    proof_text = proof_original.decode("utf-8")
    proof_occurrences = proof_text.count(ROUTE_PROOF["from"])
    if proof_occurrences != 1:
        raise AssertionError(
            f"route_proof: FROM text occurs {proof_occurrences} times in "
            f"{ROUTE_PROOF['file']}, expected 1"
        )
    proof_target.write_bytes(
        proof_text.replace(ROUTE_PROOF["from"], ROUTE_PROOF["to"], 1).encode("utf-8")
    )
    proof_result = _run(root, ROUTE_PROOF["runner"], ROUTE_PROOF["id"])
    proof_target.write_bytes(proof_original)
    proof_caught = proof_result["exit"] != 0 and proof_result["failed"] != 0
    proof_restored = proof_target.read_bytes() == proof_original
    all_ok = all_ok and proof_caught and proof_restored
    print(_fmt(f"{ROUTE_PROOF['id']} ({ROUTE_PROOF['name']})", proof_result))
    print(f"  route_proof caught={proof_caught} restored byte-identical={proof_restored}")

    # --- the ordered mutations -----------------------------------------------
    originals: dict[str, bytes] = {}
    for mut in MUTATIONS:
        rel_path = mut["file"]
        if rel_path not in originals:
            originals[rel_path] = (root / rel_path).read_bytes()

    for mut in MUTATIONS:
        label = f"{mut['id']} ({mut['name']})"
        target = root / mut["file"]
        original_bytes = originals[mut["file"]]
        text = original_bytes.decode("utf-8")
        occurrences = text.count(mut["from"])
        if occurrences != 1:
            raise AssertionError(
                f"{label}: FROM text occurs {occurrences} times in {mut['file']}, expected 1"
            )
        mutated_text = text.replace(mut["from"], mut["to"], 1)
        target.write_bytes(mutated_text.encode("utf-8"))

        result = _run(root, mut["runner"], mut["id"])
        caught = result["exit"] != 0 and result["failed"] not in (0,)
        all_ok = all_ok and caught
        print(_fmt(label, result))
        if not caught:
            print(f"  {label}: STAYED GREEN — not caught by the test selection")

        target.write_bytes(original_bytes)

    for rel_path, original_bytes in originals.items():
        restored = (root / rel_path).read_bytes() == original_bytes
        all_ok = all_ok and restored
        print(f"restored byte-identical: {restored} ({rel_path})")

    py_control_last = _run(root, "py", "control-last")
    print(_fmt("control py (after)", py_control_last))
    ts_control_last = _run(root, "ts", "control-last")
    print(_fmt("control ts (after)", ts_control_last))
    all_ok = all_ok and py_control_last["exit"] == 0 and py_control_last["failed"] == 0
    all_ok = all_ok and ts_control_last["exit"] == 0 and ts_control_last["failed"] == 0

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return all_ok


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: f288-r3-mutations.py <worktree_path>")
    ok = main(sys.argv[1])
    raise SystemExit(0 if ok else 1)
