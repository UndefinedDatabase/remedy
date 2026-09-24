#!/usr/bin/env python3
"""Mutation-testing tool for F019 T002 first half (buildBrainLayout,
scheduleBrainBirths, the birth-motion tokens).

Given a worktree path, runs an unmutated vitest control first and last, and
between them applies each VITEST mutation (L1-L9 against buildForceBrainModel.ts,
B1-B4 against brainMotion.ts) to exactly one file, runs vitest over the three
graph test files, restores the file BYTE-IDENTICAL, and reports the number of
failed tests and the exit code. It then does the same for the two PYTEST
mutations (P1 against tokens.css, P2 against brainMotion.ts), running pytest
over tests/ui_contracts/test_brain_motion_tokens.py instead.

Usage: python3 mutations.py <worktree_root>
  <worktree_root> is the repo root of the worktree, e.g.
  /home/decodeux/Repos/remedy/.remedy-wt/f019-r2-proto
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f019-r2-helper")
MUTSCRATCH_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f019-r2-mutscratch")
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

LAYOUT_REL = "apps/ui/src/components/graph/buildForceBrainModel.ts"
MOTION_REL = "apps/ui/src/components/graph/brainMotion.ts"
TOKENS_REL = "apps/ui/src/styles/tokens.css"
LAYOUT_TEST_REL = "apps/ui/src/components/graph/buildForceBrainModel.test.ts"
MOTION_TEST_REL = "apps/ui/src/components/graph/brainMotion.test.ts"
REDUCER_TEST_REL = "apps/ui/src/components/graph/brainReducer.test.ts"
TOKEN_PYTEST_REL = "tests/ui_contracts/test_brain_motion_tokens.py"


VITEST_MUTATIONS = [
    {
        "id": "L1",
        "name": "builder skips clusterBrainModel",
        "file": LAYOUT_REL,
        "from": "  const clustered = clusterBrainModel(model);\n",
        "to": "  const clustered = model;\n",
    },
    {
        "id": "L2",
        "name": "task ring radius 150 -> 151",
        "file": LAYOUT_REL,
        "from": "export const BRAIN_TASK_RING_RADIUS = 150;\n",
        "to": "export const BRAIN_TASK_RING_RADIUS = 151;\n",
    },
    {
        "id": "L3",
        "name": "golden angle replaced by a different (even-spacing-style) constant",
        "file": LAYOUT_REL,
        "from": "export const BRAIN_GOLDEN_ANGLE = Math.PI * (3 - Math.sqrt(5));\n",
        "to": "export const BRAIN_GOLDEN_ANGLE = (2 * Math.PI) / 7;\n",
    },
    {
        "id": "L4",
        "name": "child distance measured from the core instead of the task",
        "file": LAYOUT_REL,
        "from": (
            "      childPosition.set(child.id, {\n"
            "        x: anchor.x + Math.cos(angle) * BRAIN_RUN_DISTANCE,\n"
            "        y: anchor.y + Math.sin(angle) * BRAIN_RUN_DISTANCE,\n"
            "      });\n"
        ),
        "to": (
            "      childPosition.set(child.id, {\n"
            "        x: Math.cos(angle) * BRAIN_RUN_DISTANCE,\n"
            "        y: Math.sin(angle) * BRAIN_RUN_DISTANCE,\n"
            "      });\n"
        ),
    },
    {
        "id": "L5",
        "name": "child fan not centred (drop the (n - 1) / 2 term)",
        "file": LAYOUT_REL,
        "from": "      const angle = anchorAngle + (k - (n - 1) / 2) * BRAIN_RUN_FAN_STEP;\n",
        "to": "      const angle = anchorAngle + k * BRAIN_RUN_FAN_STEP;\n",
    },
    {
        "id": "L6",
        "name": "core not pinned (fx/fy removed)",
        "file": LAYOUT_REL,
        "from": (
            "        id: n.id, kind: n.kind, state: n.state, seq: n.seq,\n"
            '        depth: 0, radius: BRAIN_CORE_RADIUS, x: 0, y: 0, fx: 0, fy: 0, label: "",\n'
        ),
        "to": (
            "        id: n.id, kind: n.kind, state: n.state, seq: n.seq,\n"
            '        depth: 0, radius: BRAIN_CORE_RADIUS, x: 0, y: 0, label: "",\n'
        ),
    },
    {
        "id": "L7",
        "name": 'a task label falls back to "" instead of the id',
        "file": LAYOUT_REL,
        "from": (
            "  if (typeof title === \"string\" && title.length > 0) return title;\n"
            '  return task.id.slice("task:".length);\n'
        ),
        "to": (
            "  if (typeof title === \"string\" && title.length > 0) return title;\n"
            '  return "";\n'
        ),
    },
    {
        "id": "L8",
        "name": "active ignores a task whose child is in_progress",
        "file": LAYOUT_REL,
        "from": (
            '  if (target.kind !== "task") return false;\n'
            '  return nodes.some((n) => n.parentId === target.id && n.state === "in_progress");\n'
        ),
        "to": "  return false;\n",
    },
    {
        "id": "L9",
        "name": "link widths swapped",
        "file": LAYOUT_REL,
        "from": "      width: isTaskLink ? BRAIN_CORE_LINK_WIDTH : BRAIN_RUN_LINK_WIDTH,\n",
        "to": "      width: isTaskLink ? BRAIN_RUN_LINK_WIDTH : BRAIN_CORE_LINK_WIDTH,\n",
    },
    {
        "id": "B1",
        "name": "first paint schedules births (the previous === null guard removed)",
        "file": MOTION_REL,
        "from": "  if (previous === null) return [];\n",
        "to": "",
    },
    {
        "id": "B2",
        "name": "no concurrency cap (delay = i * stagger)",
        "file": MOTION_REL,
        "from": (
            "    const concurrencyFloor = i >= BRAIN_BIRTH_MAX_CONCURRENT\n"
            "      ? delays[i - BRAIN_BIRTH_MAX_CONCURRENT] + durationMs\n"
            "      : 0;\n"
            "    delays.push(Math.max(staggerSlot, concurrencyFloor));\n"
        ),
        "to": "    delays.push(staggerSlot);\n",
    },
    {
        "id": "B3",
        "name": "reduced-motion duration left at 420",
        "file": MOTION_REL,
        "from": "  const durationMs = reducedMotion ? BRAIN_BIRTH_REDUCED_MS : BRAIN_BIRTH_MS;\n",
        "to": "  const durationMs = BRAIN_BIRTH_MS;\n",
    },
    {
        "id": "B4",
        "name": "an existing (surviving) node re-born",
        "file": MOTION_REL,
        "from": "  const born = next.nodes.filter((n) => !previousIds.has(n.id));\n",
        "to": "  const born = next.nodes;\n",
    },
]

PYTEST_MUTATIONS = [
    {
        "id": "P1",
        "name": "the app token --remedy-dur-birth changed to 400ms",
        "file": TOKENS_REL,
        "from": "  --remedy-dur-birth: 420ms;\n",
        "to": "  --remedy-dur-birth: 400ms;\n",
    },
    {
        "id": "P2",
        "name": "BRAIN_BIRTH_MS changed to 400",
        "file": MOTION_REL,
        "from": "export const BRAIN_BIRTH_MS = 420;\n",
        "to": "export const BRAIN_BIRTH_MS = 400;\n",
    },
]


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_vitest(worktree: Path, tag: str) -> dict:
    """Run vitest over the three graph test files, with a FRESH cacheDir per
    invocation under MUTSCRATCH_DIR (which this function creates) so no run
    can see a stale transform cache from a previous mutation."""
    MUTSCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    cache_dir = MUTSCRATCH_DIR / f"vitest-cache-{tag}-{int(time.time() * 1000)}"
    config_path = MUTSCRATCH_DIR / f"vitest.config.{tag}.mjs"
    layout_test = worktree / LAYOUT_TEST_REL
    motion_test = worktree / MOTION_TEST_REL
    reducer_test = worktree / REDUCER_TEST_REL
    config_path.write_text(
        "export default {\n"
        f'  root: "{PRIMARY_UI}",\n'
        f'  cacheDir: "{cache_dir}",\n'
        "  test: {\n"
        '    environment: "node",\n'
        f'    include: ["{layout_test}", "{motion_test}", "{reducer_test}"],\n'
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
    """Run pytest over exactly the birth-token contract test."""
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", TOKEN_PYTEST_REL],
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
