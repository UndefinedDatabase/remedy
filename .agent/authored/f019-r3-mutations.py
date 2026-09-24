#!/usr/bin/env python3
"""Mutation-testing tool for F019 T002 part one (brainView.ts's pure glue
functions, plus three source-guard tripwires in BrainGraphStage.tsx and
ForceBrainGraph.tsx).

Given a worktree path, runs an unmutated vitest control first and last, and
between them applies each VITEST mutation (V1-V11, all against brainView.ts)
to exactly one file, runs vitest over the four graph test files, restores the
file BYTE-IDENTICAL, and reports the number of failed tests and the exit
code. It then does the same for the three PYTEST mutations (S1 and S3
against BrainGraphStage.tsx, S2 against ForceBrainGraph.tsx), running pytest
over tests/ui_contracts/test_brain_stage_mount.py instead.

Usage: python3 mutations.py <worktree_root>
  <worktree_root> is the repo root of the worktree, e.g.
  /home/decodeux/Repos/remedy/.remedy-wt/f019-r3-proto
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f019-r3-helper")
MUTSCRATCH_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f019-r3-mutscratch")
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

BRAIN_VIEW_REL = "apps/ui/src/components/graph/brainView.ts"
STAGE_REL = "apps/ui/src/components/graph/BrainGraphStage.tsx"
RENDERER_REL = "apps/ui/src/components/graph/ForceBrainGraph.tsx"
BRAIN_VIEW_TEST_REL = "apps/ui/src/components/graph/brainView.test.ts"
LAYOUT_TEST_REL = "apps/ui/src/components/graph/buildForceBrainModel.test.ts"
MOTION_TEST_REL = "apps/ui/src/components/graph/brainMotion.test.ts"
REDUCER_TEST_REL = "apps/ui/src/components/graph/brainReducer.test.ts"
STAGE_MOUNT_PYTEST_REL = "tests/ui_contracts/test_brain_stage_mount.py"


VITEST_MUTATIONS = [
    {
        "id": "V1",
        "name": "the table maps done to running",
        "file": BRAIN_VIEW_REL,
        "from": '  done: "completed",\n',
        "to": '  done: "running",\n',
    },
    {
        "id": "V2",
        "name": "rank is not the index (index + 1)",
        "file": BRAIN_VIEW_REL,
        "from": "    rank: index,\n",
        "to": "    rank: index + 1,\n",
    },
    {
        "id": "V3",
        "name": "filterBrainLayout keeps planned tasks under open",
        "file": BRAIN_VIEW_REL,
        "from": '  open: ["in_progress", "blocked", "fail"],\n',
        "to": '  open: ["in_progress", "blocked", "fail", "planned"],\n',
    },
    {
        "id": "V4",
        "name": "a depth-2 node kept regardless of its parent",
        "file": BRAIN_VIEW_REL,
        "from": "    else keep = n.parentId !== undefined && keptTaskIds.has(n.parentId);\n",
        "to": "    else keep = true;\n",
    },
    {
        "id": "V5",
        "name": "a link kept when only its source is kept",
        "file": BRAIN_VIEW_REL,
        "from": "  const links = layout.links.filter((l) => keptIds.has(l.source) && keptIds.has(l.target));\n",
        "to": "  const links = layout.links.filter((l) => keptIds.has(l.source));\n",
    },
    {
        "id": "V6",
        "name": '"all" returns a copy instead of the same object',
        "file": BRAIN_VIEW_REL,
        "from": '  if (filter === "all") return layout;\n',
        "to": '  if (filter === "all") return { nodes: [...layout.nodes], links: [...layout.links] };\n',
    },
    {
        "id": "V7",
        "name": "selectedBrainNodeId ignores nodeId",
        "file": BRAIN_VIEW_REL,
        "from": "  const task = tasks.find((t) => t.id === selectedNodeId || t.nodeId === selectedNodeId);\n",
        "to": "  const task = tasks.find((t) => t.id === selectedNodeId);\n",
    },
    {
        "id": "V8",
        "name": "selectionTaskIdOf returns the run's own id for a run",
        "file": BRAIN_VIEW_REL,
        "from": '  return node.parentId ? node.parentId.slice("task:".length) : null;\n',
        "to": "  return node.id;\n",
    },
    {
        "id": "V9",
        "name": "carryBrainPositions copies fx/fy from previous",
        "file": BRAIN_VIEW_REL,
        "from": (
            "      return { ...n, x: prior.x as number, y: prior.y as number };\n"
        ),
        "to": (
            "      return { ...n, x: prior.x as number, y: prior.y as number,"
            " fx: (prior as { fx?: number }).fx, fy: (prior as { fy?: number }).fy };\n"
        ),
    },
    {
        "id": "V10",
        "name": "carryBrainPositions ignores previous x/y",
        "file": BRAIN_VIEW_REL,
        "from": "    if (prior && Number.isFinite(prior.x) && Number.isFinite(prior.y)) {\n",
        "to": "    if (false) {\n",
    },
    {
        "id": "V11",
        "name": "shellSelectionIdOf returns the bare task id",
        "file": BRAIN_VIEW_REL,
        "from": "  return task ? task.nodeId : taskId;\n",
        "to": "  return taskId;\n",
    },
]

PYTEST_MUTATIONS = [
    {
        "id": "S1",
        "name": "the stage mounts BrainGraphCanvas only (ForceBrainGraph element deleted)",
        "file": STAGE_REL,
        "from": (
            "      {showLiveGraph ? (\n"
            "        <ForceBrainGraph\n"
            "          layout={visible}\n"
            "          selectedId={selectedId}\n"
            "          onSelectNode={(taskId) => onSelectNode(shellSelectionIdOf(dashboard.tasks, taskId))}\n"
            "        />\n"
            "      ) : (\n"
            "        // No tasks, an empty filter, or the operator pressed \"Simple view\":\n"
            "        // BrainGraphCanvas owns its own empty and filter-empty messages.\n"
            "        <BrainGraphCanvas dashboard={dashboard} filter={filter} selectedNodeId={selectedNodeId} onSelectNode={onSelectNode} />\n"
            "      )}\n"
        ),
        "to": (
            "      <BrainGraphCanvas dashboard={dashboard} filter={filter} selectedNodeId={selectedNodeId} onSelectNode={onSelectNode} />\n"
        ),
    },
    {
        "id": "S2",
        "name": "the particle expression drops reducedMotion",
        "file": RENDERER_REL,
        "from": "          linkDirectionalParticles={(l) => ((l as BrainLayoutLink).active && !reducedMotion ? 1 : 0)}\n",
        "to": "          linkDirectionalParticles={(l) => ((l as BrainLayoutLink).active ? 1 : 0)}\n",
    },
    {
        "id": "S3",
        "name": "the stage stops calling shellSelectionIdOf (mapped callback replaced by the raw onSelectNode)",
        "file": STAGE_REL,
        "from": "          onSelectNode={(taskId) => onSelectNode(shellSelectionIdOf(dashboard.tasks, taskId))}\n",
        "to": "          onSelectNode={onSelectNode}\n",
    },
]


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_vitest(worktree: Path, tag: str) -> dict:
    """Run vitest over the four graph test files, with a FRESH cacheDir per
    invocation under MUTSCRATCH_DIR (which this function creates) so no run
    can see a stale transform cache from a previous mutation."""
    MUTSCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    cache_dir = MUTSCRATCH_DIR / f"vitest-cache-{tag}-{int(time.time() * 1000)}"
    config_path = MUTSCRATCH_DIR / f"vitest.config.{tag}.mjs"
    brain_view_test = worktree / BRAIN_VIEW_TEST_REL
    layout_test = worktree / LAYOUT_TEST_REL
    motion_test = worktree / MOTION_TEST_REL
    reducer_test = worktree / REDUCER_TEST_REL
    config_path.write_text(
        "export default {\n"
        f'  root: "{PRIMARY_UI}",\n'
        f'  cacheDir: "{cache_dir}",\n'
        "  test: {\n"
        '    environment: "node",\n'
        f'    include: ["{brain_view_test}", "{layout_test}", "{motion_test}", "{reducer_test}"],\n'
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
    return {"exit_code": proc.returncode, "failed": failed, "passed": passed, "raw_tail": out[-1500:]}


def run_pytest(worktree: Path, tag: str) -> dict:
    """Run pytest over exactly the stage-mount source guard."""
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", STAGE_MOUNT_PYTEST_REL],
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
    return {"exit_code": proc.returncode, "failed": failed, "passed": passed, "raw_tail": out[-1500:]}


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
    print(f"  restored byte-identical: {restored_ok}")
    turned_red = result["exit_code"] != 0 and result["failed"] != 0
    print(f"  turned at least one test red: {turned_red}")
    if not turned_red:
        print("  !! MUTATION SURVIVED GREEN — needs a strengthened test.")
        print(result["raw_tail"])
    return {
        **mut, "skipped": False, "restored_ok": restored_ok,
        "exit_code": result["exit_code"], "failed": result["failed"],
        "passed": result["passed"], "turned_red": turned_red,
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
        print(f"  {r['id']}: {status}, failed={r['failed']}, exit={r['exit_code']}, {restored}")
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
