#!/usr/bin/env python3
"""Mutation-testing tool for F019 R6: the performance fixture's arithmetic
(brainPerfFixture.ts, vitest) and the demo recording's own truth, checked
from BOTH sides — the hand-derived golden in brainDemoRecording.test.ts
(vitest) and the live-fake-job-vs-recording pytest this round adds
(tests/ui_server/test_brain_demo_recording_live.py).

Given a worktree path, runs unmutated control runs first and last (vitest
over every graph test file plus brainStreamDeps.test.ts and
brainPerfFixture.test.ts; pytest over the new live-recording test alone),
and between them applies each mutation to exactly one file, runs the
runner(s) that mutation names, restores the file BYTE-IDENTICAL, and reports
the number of failed tests and the exit code for EVERY runner it ran.

F1-F3 mutate the fixture (brainPerfFixture.ts) and are checked by vitest
alone. P1-P2 mutate the COMMITTED RECORDING (brainDemoRecording.ts, never the
test) and are checked by BOTH vitest (the hand-derived golden) AND the new
pytest (the live comparison) — reported as two separate counts.

Usage: python3 -B mutations.py <worktree_root>
  <worktree_root> is the repo root of the worktree, e.g.
  /home/decodeux/Repos/remedy/.remedy-wt/f019-r6-proto
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f019-r6-helper")
MUTSCRATCH_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f019-r6-mutscratch")
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

FIXTURE_REL = "apps/ui/src/components/graph/brainPerfFixture.ts"
RECORDING_REL = "apps/ui/src/components/graph/brainDemoRecording.ts"

BRAIN_VIEW_TEST_REL = "apps/ui/src/components/graph/brainView.test.ts"
LAYOUT_TEST_REL = "apps/ui/src/components/graph/buildForceBrainModel.test.ts"
MOTION_TEST_REL = "apps/ui/src/components/graph/brainMotion.test.ts"
REDUCER_TEST_REL = "apps/ui/src/components/graph/brainReducer.test.ts"
DEMO_TEST_REL = "apps/ui/src/components/graph/brainDemoRecording.test.ts"
LEDGER_TEST_REL = "apps/ui/src/components/graph/brainLedger.test.ts"
PERF_TEST_REL = "apps/ui/src/components/graph/brainPerfFixture.test.ts"
DEPS_TEST_REL = "apps/ui/src/api/brainStreamDeps.test.ts"

PYTEST_NODE_IDS = ["tests/ui_server/test_brain_demo_recording_live.py"]

VITEST = "vitest"
PYTEST = "pytest"

MUTATIONS = [
    {
        "id": "F1",
        "name": "the fixture's stage-1 constant becomes 199",
        "file": FIXTURE_REL,
        "runners": [VITEST],
        "from": "export const BRAIN_PERF_STAGE1_NODES = 200;",
        "to": "export const BRAIN_PERF_STAGE1_NODES = 199;",
    },
    {
        "id": "F2",
        "name": "the generator leaves no builder run in progress (no active link)",
        "file": FIXTURE_REL,
        "runners": [VITEST],
        "from": "    const leaveOpen = t % 5 === 0;\n",
        "to": "    const leaveOpen = false;\n",
    },
    {
        "id": "F3",
        "name": "the generator skips task_run_completed for every task (lastSeq changes)",
        "file": FIXTURE_REL,
        "runners": [VITEST],
        "from": (
            '      rows.push(row(seq++, "verification_passed", taskId, "pass"));\n'
            '      rows.push(row(seq++, "task_run_completed", taskId, "pass"));\n'
        ),
        "to": '      rows.push(row(seq++, "verification_passed", taskId, "pass"));\n',
    },
    {
        "id": "P1",
        "name": 'one outcome in brainDemoRecording.ts changed from "pass" to "fail" (seq 3)',
        "file": RECORDING_REL,
        "runners": [VITEST, PYTEST],
        "from": (
            '{ seq: 3, event: { seq: 3, event: "task_run_completed", '
            'timestamp: "2026-09-24T16:57:03.293776+00:00", outcome: "pass", '
            'task_id: "a7a8f67f1b9a4814" } },'
        ),
        "to": (
            '{ seq: 3, event: { seq: 3, event: "task_run_completed", '
            'timestamp: "2026-09-24T16:57:03.293776+00:00", outcome: "fail", '
            'task_id: "a7a8f67f1b9a4814" } },'
        ),
    },
    {
        "id": "P2",
        "name": "one recorded task label changed",
        "file": RECORDING_REL,
        "runners": [VITEST, PYTEST],
        "from": 'label: "Deliver src/main.py",',
        "to": 'label: "Deliver src/main-changed.py",',
    },
]


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_vitest(worktree: Path, tag: str) -> dict:
    """Run vitest over every graph test file plus brainStreamDeps.test.ts and
    brainPerfFixture.test.ts, with a FRESH cacheDir per invocation under
    MUTSCRATCH_DIR (which this function creates) so no run can see a stale
    transform cache from a previous mutation."""
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
        worktree / PERF_TEST_REL,
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
    """Run pytest over the new live-recording test alone, verbosely, so a
    survived mutation can be reported by NAME."""
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


RUNNERS = {VITEST: run_vitest, PYTEST: run_pytest}


def run_all(worktree: Path, tag: str) -> dict:
    """Run BOTH runners (used for the control runs, which must be green on
    both sides before any mutation is trusted)."""
    return {name: fn(worktree, f"{tag}-{name}") for name, fn in RUNNERS.items()}


def apply_and_run(worktree: Path, mut: dict, tag_prefix: str) -> dict:
    target = worktree / mut["file"]
    original_bytes = target.read_bytes()
    original_hash = sha256_of(target)
    text = original_bytes.decode("utf-8")
    occurrences = text.count(mut["from"])
    print("-" * 78)
    print(f"{mut['id']}: {mut['name']}  [{mut['file']}]  runners={mut['runners']}")
    if occurrences != 1:
        print(f"  !! FROM string occurs {occurrences} times (expected exactly 1); skipping mutation.")
        return {**mut, "skipped": True, "occurrences": occurrences}

    mutated = text.replace(mut["from"], mut["to"], 1)
    target.write_bytes(mutated.encode("utf-8"))
    per_runner: dict[str, dict] = {}
    try:
        for runner_name in mut["runners"]:
            result = RUNNERS[runner_name](worktree, f"{tag_prefix}-{mut['id'].lower()}-{runner_name}")
            per_runner[runner_name] = result
    finally:
        target.write_bytes(original_bytes)
    restored_ok = sha256_of(target) == original_hash

    turned_red = True
    for runner_name, result in per_runner.items():
        red = result["exit_code"] != 0 and result["failed"] != 0
        turned_red = turned_red and red
        print(f"  [{runner_name}] exit_code={result['exit_code']} failed={result['failed']} passed={result['passed']}")
        if result.get("failed_names"):
            print(f"  [{runner_name}] failed node(s): {result['failed_names']}")
        print(f"  [{runner_name}] turned red: {red}")
        if not red:
            print(f"  !! [{runner_name}] MUTATION SURVIVED GREEN")
            print(result["raw_tail"])
    print(f"  restored byte-identical: {restored_ok}")
    print(f"  turned red on EVERY runner it names: {turned_red}")
    return {
        **mut, "skipped": False, "restored_ok": restored_ok,
        "turned_red": turned_red, "per_runner": per_runner,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: mutations.py <worktree_root>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()

    print(f"worktree: {worktree}")
    print("=" * 78)
    print("CONTROL RUN #1 (unmutated, before any mutation) — both runners")
    control_first = run_all(worktree, "control-first")
    for name, result in control_first.items():
        print(f"  [{name}] exit_code={result['exit_code']} failed={result['failed']} passed={result['passed']}")
    control_first_green = all(r["exit_code"] == 0 and r["failed"] == 0 for r in control_first.values())
    if not control_first_green:
        print("  !! control run #1 is not green on every runner; aborting mutation sweep.")
        for name, result in control_first.items():
            print(f"  [{name}] tail:\n{result['raw_tail']}")
        return 1

    results = []
    for mut in MUTATIONS:
        results.append(apply_and_run(worktree, mut, "mut"))

    print("=" * 78)
    print("CONTROL RUN #2 (unmutated, after the full sweep) — both runners")
    control_last = run_all(worktree, "control-last")
    for name, result in control_last.items():
        print(f"  [{name}] exit_code={result['exit_code']} failed={result['failed']} passed={result['passed']}")
    control_last_green = all(r["exit_code"] == 0 and r["failed"] == 0 for r in control_last.values())

    print("=" * 78)
    print("SUMMARY")
    all_ok = control_first_green and control_last_green
    for r in results:
        if r.get("skipped"):
            print(f"  {r['id']}: SKIPPED (from-string occurrences={r['occurrences']})")
            all_ok = False
            continue
        status = "RED (caught)" if r["turned_red"] else "GREEN (SURVIVED — needs a stronger test)"
        restored = "restored OK" if r["restored_ok"] else "RESTORE MISMATCH"
        counts = ", ".join(
            f"{name}: failed={res['failed']}/passed={res['passed']}/exit={res['exit_code']}"
            for name, res in r["per_runner"].items()
        )
        print(f"  {r['id']}: {status}, {restored} | {counts}")
        if not r["turned_red"] or not r["restored_ok"]:
            all_ok = False

    print("=" * 78)
    print(f"control #1 green (all runners): {control_first_green}")
    print(f"control #2 green (all runners): {control_last_green}")
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
