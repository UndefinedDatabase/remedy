#!/usr/bin/env python3
"""Mutation-testing tool for F019 R5: the live ledger's merge/prefix/cursor
rules (brainLedger.ts, vitest) and the wiring pytest source guards catch that
vitest cannot see (BrainGraphStage.tsx, RemedyShell.tsx, useBrainLedger.ts).

Given a worktree path, runs an unmutated vitest control first and last, and
between them applies each VITEST mutation (L1-L8, all against
brainLedger.ts) to exactly one file, runs vitest over the graph test files
plus brainStreamDeps.test.ts, restores the file BYTE-IDENTICAL, and reports
the number of failed tests and the exit code. It then does the same for the
three PYTEST mutations (W1 against BrainGraphStage.tsx, W2 against
RemedyShell.tsx, W3 against useBrainLedger.ts), running pytest over
tests/ui_contracts/test_brain_live_wiring.py and
tests/ui_contracts/test_brain_stage_mount.py together instead.

Usage: python3 -B mutations.py <worktree_root>
  <worktree_root> is the repo root of the worktree, e.g.
  /home/decodeux/Repos/remedy/.remedy-wt/f019-r5-proto
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f019-r5-helper")
MUTSCRATCH_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f019-r5-mutscratch")
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

LEDGER_REL = "apps/ui/src/components/graph/brainLedger.ts"
STAGE_REL = "apps/ui/src/components/graph/BrainGraphStage.tsx"
SHELL_REL = "apps/ui/src/components/shell/RemedyShell.tsx"
HOOK_REL = "apps/ui/src/components/graph/useBrainLedger.ts"

BRAIN_VIEW_TEST_REL = "apps/ui/src/components/graph/brainView.test.ts"
LAYOUT_TEST_REL = "apps/ui/src/components/graph/buildForceBrainModel.test.ts"
MOTION_TEST_REL = "apps/ui/src/components/graph/brainMotion.test.ts"
REDUCER_TEST_REL = "apps/ui/src/components/graph/brainReducer.test.ts"
DEMO_TEST_REL = "apps/ui/src/components/graph/brainDemoRecording.test.ts"
LEDGER_TEST_REL = "apps/ui/src/components/graph/brainLedger.test.ts"
DEPS_TEST_REL = "apps/ui/src/api/brainStreamDeps.test.ts"

PYTEST_NODE_IDS = [
    "tests/ui_contracts/test_brain_live_wiring.py",
    "tests/ui_contracts/test_brain_stage_mount.py",
]


VITEST_MUTATIONS = [
    {
        "id": "L1",
        "name": "merge lets the incoming duplicate win instead of the already-held row",
        "file": LEDGER_REL,
        "from": (
            "  for (const row of rows) {\n"
            "    if (bySeq.has(row.seq)) continue;\n"
            "    bySeq.set(row.seq, row);\n"
            "    added = true;\n"
            "  }\n"
        ),
        "to": (
            "  for (const row of rows) {\n"
            "    bySeq.set(row.seq, row);\n"
            "    added = true;\n"
            "  }\n"
        ),
    },
    {
        "id": "L2",
        "name": "prefix returns every held row, ignoring a hole",
        "file": LEDGER_REL,
        "from": (
            "export function brainLedgerPrefix(ledger: BrainLedger): BrainEventRow[] {\n"
            "  const prefix: BrainEventRow[] = [];\n"
            "  let next = 0;\n"
            "  for (const row of ledger.rows) {\n"
            "    if (row.seq !== next) break;\n"
            "    prefix.push(row);\n"
            "    next += 1;\n"
            "  }\n"
            "  return prefix;\n"
            "}\n"
        ),
        "to": (
            "export function brainLedgerPrefix(ledger: BrainLedger): BrainEventRow[] {\n"
            "  return [...ledger.rows];\n"
            "}\n"
        ),
    },
    {
        "id": "L3",
        "name": "next cursor returns null before any read instead of 0",
        "file": LEDGER_REL,
        "from": "  if (ledger.known === null) return 0;\n",
        "to": "  if (ledger.known === null) return null;\n",
    },
    {
        "id": "L4",
        "name": "next cursor returns known instead of the first hole",
        "file": LEDGER_REL,
        "from": (
            "  const held = new Set(ledger.rows.map((row) => row.seq));\n"
            "  for (let seq = 0; seq < ledger.known; seq += 1) {\n"
            "    if (!held.has(seq)) return seq;\n"
            "  }\n"
            "  return null;\n"
        ),
        "to": "  return ledger.known;\n",
    },
    {
        "id": "L5",
        "name": "an unchanged read does not stall",
        "file": LEDGER_REL,
        "from": "  const stalled = ledger === load.ledger ? cursor : null;\n",
        "to": "  const stalled = null;\n",
    },
    {
        "id": "L6",
        "name": "a live change does not clear the stall",
        "file": LEDGER_REL,
        "from": "  return { ledger, stalled: null };\n",
        "to": "  return { ledger, stalled: load.stalled };\n",
    },
    {
        "id": "L7",
        "name": "brainLedgerPage ignores the payload's cursor",
        "file": LEDGER_REL,
        "from": "  return { rows, known: knownLengthOf(payload) };\n",
        "to": "  return { rows, known: null };\n",
    },
    {
        "id": "L8",
        "name": "known is not raised by held rows past the declared length",
        "file": LEDGER_REL,
        "from": "  const known = maxKnown(ledger.known, knownLength, fromHeld);\n",
        "to": "  const known = maxKnown(ledger.known, knownLength, null);\n",
    },
]

PYTEST_MUTATIONS = [
    {
        "id": "W1",
        "name": "the stage builds from seedBrainModel again instead of rebuildBrainModel",
        "file": STAGE_REL,
        "from": "rebuildBrainModel(dashboard.jobId, seeds, rows)",
        "to": "seedBrainModel(dashboard.jobId, seeds)",
    },
    {
        "id": "W2",
        "name": "the shell's stage line loses recent=",
        "file": SHELL_REL,
        "from": "recent={stream.recent} readEventsPage={readEventsPage}",
        "to": "readEventsPage={readEventsPage}",
    },
    {
        "id": "W3",
        "name": "useBrainLedger.ts stops holding the in-flight cursor in a useRef",
        "file": HOOK_REL,
        "from": "const inFlightCursorRef = useRef<number | null>(null);",
        "to": "let inFlightCursorRef = { current: null as number | null };",
    },
]


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_vitest(worktree: Path, tag: str) -> dict:
    """Run vitest over every graph test file plus brainStreamDeps.test.ts,
    with a FRESH cacheDir per invocation under MUTSCRATCH_DIR (which this
    function creates) so no run can see a stale transform cache from a
    previous mutation."""
    MUTSCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    cache_dir = MUTSCRATCH_DIR / f"vitest-cache-{tag}-{int(time.time() * 1000)}"
    config_path = MUTSCRATCH_DIR / f"vitest.config.{tag}.mjs"
    test_files = [
        worktree / BRAIN_VIEW_TEST_REL,
        worktree / LAYOUT_TEST_REL,
        worktree / MOTION_TEST_REL,
        worktree / REDUCER_TEST_REL,
        worktree / DEMO_TEST_REL,
        worktree / LEDGER_TEST_REL,
        worktree / DEPS_TEST_REL,
    ]
    config_path.write_text(
        "export default {\n"
        f'  root: "{PRIMARY_UI}",\n'
        f'  cacheDir: "{cache_dir}",\n'
        "  test: {\n"
        '    environment: "node",\n'
        "    include: [\""
        + '", "'.join(str(p) for p in test_files)
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
    """Run pytest over the two guard modules together, verbosely, so a
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
