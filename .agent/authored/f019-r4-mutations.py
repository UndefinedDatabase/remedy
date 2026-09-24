#!/usr/bin/env python3
"""Mutation-testing tool for F019 R4: the old decorative builder's removal
(pytest source guards) and the demo recording (vitest goldens).

Given a worktree path, runs an unmutated vitest control first and last, and
between them applies each VITEST mutation (D1-D4, against brainOntology.ts /
brainDemoRecording.ts) to exactly one file, runs vitest over the five graph
test files, restores the file BYTE-IDENTICAL, and reports the number of
failed tests and the exit code. It then does the same for the three PYTEST
mutations (P1 against forceBrainTypes.ts, P2 and P3 against
buildForceBrainModel.ts), running pytest over
tests/ui_server/test_dashboard_contract.py::TestRealGraphTruthContract and
tests/ui_contracts/test_graph_architecture.py::TestForceGraphComponentIntegrity
together instead.

Usage: python3 -B mutations.py <worktree_root>
  <worktree_root> is the repo root of the worktree, e.g.
  /home/decodeux/Repos/remedy/.remedy-wt/f019-r4-proto
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f019-r4-helper")
MUTSCRATCH_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f019-r4-mutscratch")
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

ONTOLOGY_REL = "apps/ui/src/components/graph/brainOntology.ts"
DEMO_REL = "apps/ui/src/components/graph/brainDemoRecording.ts"
LAYOUT_TYPES_REL = "apps/ui/src/components/graph/forceBrainTypes.ts"
BUILD_MODEL_REL = "apps/ui/src/components/graph/buildForceBrainModel.ts"

BRAIN_VIEW_TEST_REL = "apps/ui/src/components/graph/brainView.test.ts"
LAYOUT_TEST_REL = "apps/ui/src/components/graph/buildForceBrainModel.test.ts"
MOTION_TEST_REL = "apps/ui/src/components/graph/brainMotion.test.ts"
REDUCER_TEST_REL = "apps/ui/src/components/graph/brainReducer.test.ts"
DEMO_TEST_REL = "apps/ui/src/components/graph/brainDemoRecording.test.ts"

PYTEST_NODE_IDS = [
    "tests/ui_server/test_dashboard_contract.py::TestRealGraphTruthContract",
    "tests/ui_contracts/test_graph_architecture.py::TestForceGraphComponentIntegrity",
]


VITEST_MUTATIONS = [
    {
        "id": "D1",
        "name": "REVIEW_OUTCOME_STATE_TABLE maps needs_repair to pass",
        "file": ONTOLOGY_REL,
        "from": '  needs_repair: "fail",\n',
        "to": '  needs_repair: "pass",\n',
    },
    {
        "id": "D2",
        "name": "one frame (seq 5) dropped from BRAIN_DEMO_FRAMES",
        "file": DEMO_REL,
        "from": (
            '  { seq: 5, event: { seq: 5, event: "task_round_completed", '
            'timestamp: "2026-09-24T16:57:03.807739+00:00", outcome: "needs_repair", '
            'task_id: "1965fb3f26b64fe7" } },\n'
        ),
        "to": "",
    },
    {
        "id": "D3",
        "name": "task A's nodeId set to empty string",
        "file": DEMO_REL,
        "from": '    nodeId: "a7a8f67f1b9a4814",\n',
        "to": '    nodeId: "",\n',
    },
    {
        "id": "D4",
        "name": "brainDemoRows hand-builds rows and drops outcome instead of using feedRowOf",
        "file": DEMO_REL,
        "from": (
            "export function brainDemoRows(): BrainEventRow[] {\n"
            "  return BRAIN_DEMO_FRAMES.map((frame) => feedRowOf(frame, 0));\n"
            "}\n"
        ),
        "to": (
            "export function brainDemoRows(): BrainEventRow[] {\n"
            "  return BRAIN_DEMO_FRAMES.map((frame) => {\n"
            "    const envelope = frame.event as Record<string, unknown>;\n"
            "    return {\n"
            "      seq: frame.seq,\n"
            '      kind: String(envelope.event ?? ""),\n'
            '      outcome: "",\n'
            "      taskId: String(envelope.task_id ?? \"\"),\n"
            "    };\n"
            "  });\n"
            "}\n"
        ),
    },
]

PYTEST_MUTATIONS = [
    {
        "id": "P1",
        "name": "re-add sourceKind? to interface BrainLayoutNode",
        "file": LAYOUT_TYPES_REL,
        "from": "  label: string;\n",
        "to": "  label: string;\n  sourceKind?: string;\n",
    },
    {
        "id": "P2",
        "name": 'a comment naming "layout_only" added to buildForceBrainModel.ts',
        "file": BUILD_MODEL_REL,
        "from": 'import { clusterBrainModel } from "./brainReducer";\n',
        "to": (
            'import { clusterBrainModel } from "./brainReducer";\n'
            "// a layout_only decorative node used to live here.\n"
        ),
    },
    {
        "id": "P3",
        "name": "buildBrainLayout renamed to buildBrainLayoutX in its declaration line only",
        "file": BUILD_MODEL_REL,
        "from": "export function buildBrainLayout(model: BrainModel): BrainLayoutData {\n",
        "to": "export function buildBrainLayoutX(model: BrainModel): BrainLayoutData {\n",
    },
]


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_vitest(worktree: Path, tag: str) -> dict:
    """Run vitest over the five graph test files, with a FRESH cacheDir per
    invocation under MUTSCRATCH_DIR (which this function creates) so no run
    can see a stale transform cache from a previous mutation."""
    MUTSCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    cache_dir = MUTSCRATCH_DIR / f"vitest-cache-{tag}-{int(time.time() * 1000)}"
    config_path = MUTSCRATCH_DIR / f"vitest.config.{tag}.mjs"
    brain_view_test = worktree / BRAIN_VIEW_TEST_REL
    layout_test = worktree / LAYOUT_TEST_REL
    motion_test = worktree / MOTION_TEST_REL
    reducer_test = worktree / REDUCER_TEST_REL
    demo_test = worktree / DEMO_TEST_REL
    config_path.write_text(
        "export default {\n"
        f'  root: "{PRIMARY_UI}",\n'
        f'  cacheDir: "{cache_dir}",\n'
        "  test: {\n"
        '    environment: "node",\n'
        "    include: [\""
        + '", "'.join(str(p) for p in [brain_view_test, layout_test, motion_test, reducer_test, demo_test])
        + "\"],\n"
        "  },\n"
        "};\n"
    )
    proc = subprocess.run(
        [str(VITEST_BIN), "run", "--config", str(config_path)],
        cwd=str(PRIMARY_UI),
        capture_output=True,
        text=True,
        timeout=120,
    )
    out = proc.stdout + proc.stderr
    m = re.search(r"Tests\s+(\d+)\s+failed\s*\|\s*(\d+)\s+passed", out)
    if m:
        failed, passed = int(m.group(1)), int(m.group(2))
    else:
        m2 = re.search(r"Tests\s+(\d+)\s+passed", out)
        if m2:
            failed, passed = 0, int(m2.group(1))
        else:
            failed, passed = -1, -1
    return {"exit_code": proc.returncode, "failed": failed, "passed": passed, "raw_tail": out[-2000:]}


def run_pytest(worktree: Path, tag: str) -> dict:
    """Run pytest over the two guard classes together, verbosely, so a
    survived mutation can be reported by NAME (which test, if any, went red)."""
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", "-p", "no:cacheprovider", *PYTEST_NODE_IDS],
        cwd=str(worktree),
        capture_output=True,
        text=True,
        timeout=120,
    )
    out = proc.stdout + proc.stderr
    m = re.search(r"(\d+)\s+failed(?:,\s*(\d+)\s+passed)?", out)
    if m:
        failed = int(m.group(1))
        passed = int(m.group(2)) if m.group(2) else 0
    else:
        m2 = re.search(r"(\d+)\s+passed", out)
        passed = int(m2.group(1)) if m2 else -1
        failed = 0 if m2 else -1
    failed_names = re.findall(r"^FAILED (\S+)", out, flags=re.MULTILINE)
    return {
        "exit_code": proc.returncode, "failed": failed, "passed": passed,
        "raw_tail": out[-2500:], "failed_names": failed_names,
    }


def apply_and_run(worktree: Path, mut: dict, runner, tag_prefix: str) -> dict:
    target = worktree / mut["file"]
    original_bytes = target.read_bytes()
    original_hash = sha256_of(target)
    text = original_bytes.decode("utf-8")
    occurrences = text.count(mut["from"])
    print("-" * 78)
    print(f"{mut['id']}: {mut['name']}  [{mut['file']}]")
    if occurrences != 1:
        print(f"  !! FROM string occurs {occurrences} times (expected exactly 1); skipping mutation.")
        return {**mut, "skipped": True, "occurrences": occurrences}

    mutated = text.replace(mut["from"], mut["to"], 1)
    target.write_bytes(mutated.encode("utf-8"))
    try:
        result = runner(worktree, f"{tag_prefix}-{mut['id'].lower()}")
    finally:
        target.write_bytes(original_bytes)
    restored_ok = sha256_of(target) == original_hash
    print(f"  exit_code={result['exit_code']} failed={result['failed']} passed={result['passed']}")
    if result.get("failed_names"):
        print(f"  failed node(s): {result['failed_names']}")
    print(f"  restored byte-identical: {restored_ok}")
    turned_red = result["exit_code"] != 0 and result["failed"] != 0
    print(f"  turned at least one test red: {turned_red}")
    if not turned_red:
        print("  !! MUTATION SURVIVED GREEN — needs a stronger test (or is a known-weak check).")
        print(result["raw_tail"])
    return {
        **mut, "skipped": False, "restored_ok": restored_ok,
        "exit_code": result["exit_code"], "failed": result["failed"],
        "passed": result["passed"], "turned_red": turned_red,
        "failed_names": result.get("failed_names", []),
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: mutations.py <worktree_root>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()

    print(f"worktree: {worktree}")
    print("=" * 78)
    print("VITEST CONTROL RUN #1 (unmutated, before any mutation)")
    vitest_before = run_vitest(worktree, "control-first")
    print(f"  exit_code={vitest_before['exit_code']} failed={vitest_before['failed']} passed={vitest_before['passed']}")
    if vitest_before["exit_code"] != 0 or vitest_before["failed"] != 0:
        print("  !! vitest control run #1 is not green; aborting mutation sweep.")
        print(vitest_before["raw_tail"])
        return 1

    print("=" * 78)
    print("PYTEST CONTROL RUN #1 (unmutated, before any mutation)")
    pytest_before = run_pytest(worktree, "control-first")
    print(f"  exit_code={pytest_before['exit_code']} failed={pytest_before['failed']} passed={pytest_before['passed']}")
    if pytest_before["exit_code"] != 0 or pytest_before["failed"] != 0:
        print("  !! pytest control run #1 is not green; aborting mutation sweep.")
        print(pytest_before["raw_tail"])
        return 1

    results = []
    for mut in VITEST_MUTATIONS:
        results.append(apply_and_run(worktree, mut, run_vitest, "vitest"))
    for mut in PYTEST_MUTATIONS:
        results.append(apply_and_run(worktree, mut, run_pytest, "pytest"))

    print("=" * 78)
    print("VITEST CONTROL RUN #2 (unmutated, after the full sweep)")
    vitest_after = run_vitest(worktree, "control-last")
    print(f"  exit_code={vitest_after['exit_code']} failed={vitest_after['failed']} passed={vitest_after['passed']}")

    print("=" * 78)
    print("PYTEST CONTROL RUN #2 (unmutated, after the full sweep)")
    pytest_after = run_pytest(worktree, "control-last")
    print(f"  exit_code={pytest_after['exit_code']} failed={pytest_after['failed']} passed={pytest_after['passed']}")

    print("=" * 78)
    print("SUMMARY")
    all_ok = (
        vitest_before["exit_code"] == 0 and vitest_after["exit_code"] == 0
        and pytest_before["exit_code"] == 0 and pytest_after["exit_code"] == 0
    )
    for r in results:
        if r.get("skipped"):
            print(f"  {r['id']}: SKIPPED (from-string occurrences={r['occurrences']})")
            all_ok = False
            continue
        status = "RED (caught)" if r["turned_red"] else "GREEN (SURVIVED — needs a stronger test)"
        restored = "restored OK" if r["restored_ok"] else "RESTORE MISMATCH"
        names = f", failed_names={r['failed_names']}" if r.get("failed_names") else ""
        print(f"  {r['id']}: {status}, failed={r['failed']}, exit={r['exit_code']}, {restored}{names}")
        if not r["turned_red"] or not r["restored_ok"]:
            all_ok = False

    print("=" * 78)
    print(f"vitest control #1 green: {vitest_before['exit_code'] == 0 and vitest_before['failed'] == 0}")
    print(f"vitest control #2 green: {vitest_after['exit_code'] == 0 and vitest_after['failed'] == 0}")
    print(f"pytest control #1 green: {pytest_before['exit_code'] == 0 and pytest_before['failed'] == 0}")
    print(f"pytest control #2 green: {pytest_after['exit_code'] == 0 and pytest_after['failed'] == 0}")
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
