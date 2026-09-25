#!/usr/bin/env python3
"""Mutation tool for F024 T003, pure half: the index, the scrubber machine, the bar's view model and their guard.

Given a worktree root, runs an unmutated control first and last, and between them applies
each mutation below (every FROM must occur exactly once in its file), runs the vitest files
of this round and the Python contract guard, restores the file BYTE-IDENTICAL, and reports
each runner's failed count and exit code. A mutation is caught when at least one runner
goes red. vitest runs from the PRIMARY `apps/ui` (a worktree has no node_modules) with a
scratch config under `.remedy-wt/f024-r3-mutscratch/`; pytest runs with `python3 -B` so a
bytecode cache can never serve a previous mutation's module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f024-r3-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

INDEX_REL = "apps/ui/src/components/timeline/timelineIndex.ts"
STATE_REL = "apps/ui/src/components/timeline/scrubState.ts"
VIEW_REL = "apps/ui/src/components/timeline/timelineView.ts"
VITEST_FILES = [
    "apps/ui/src/components/timeline/timelineIndex.test.ts",
    "apps/ui/src/components/timeline/scrubState.test.ts",
    "apps/ui/src/components/timeline/timelineView.test.ts",
]
GUARD_REL = "tests/ui_contracts/test_timeline_scrub_contract.py"

MUTATIONS = [
    {"id": "m1", "name": "a skipped phase gets no start in the index", "file": INDEX_REL,
     "from": "    for (let p = high + 1; p <= index; p += 1) starts[p] = row.seq;\n",
     "to": "    if (index > high) starts[index] = row.seq;\n"},
    {"id": "m2", "name": "the index never withdraws a pass", "file": INDEX_REL,
     "from": '    if (model.nodes[0].state !== "pass") since = null;\n    else if (since === null) since = row.seq;\n',
     "to": '    if (model.nodes[0].state === "pass" && since === null) since = row.seq;\n'},
    {"id": "m3", "name": "a position reads the row after it", "file": INDEX_REL,
     "from": "    if (index.seqs[mid] <= seq) lo = mid + 1;\n", "to": "    if (index.seqs[mid] < seq) lo = mid + 1;\n"},
    {"id": "m4", "name": "Finalized ignores a later marker in the index", "file": INDEX_REL,
     "from": "    const finalizedAt = Math.max(since, starts[reached] as number);\n",
     "to": "    const finalizedAt = since;\n"},
    {"id": "m5", "name": "the phase stops repeat a shared start", "file": INDEX_REL,
     "from": "  return [...new Set(phasesAt(index, head).spans.map((s) => s.startSeq))].sort((a, b) => a - b);\n",
     "to": "  return phasesAt(index, head).spans.map((s) => s.startSeq).sort((a, b) => a - b);\n"},
    {"id": "m6", "name": "a scrubbed view follows the head", "file": STATE_REL,
     "from": "      return { ...state, head: event.head, queued: state.queued + (event.head - state.head) };\n",
     "to": "      return { ...state, position: event.head, head: event.head, queued: state.queued + (event.head - state.head) };\n"},
    {"id": "m7", "name": "rows behind the view are not counted", "file": STATE_REL,
     "from": "      return { ...state, head: event.head, queued: state.queued + (event.head - state.head) };\n",
     "to": "      return { ...state, head: event.head };\n"},
    {"id": "m8", "name": "the handle goes below before-the-first-event", "file": STATE_REL,
     "from": "  const position = Math.max(-1, Math.min(state.head, seq));\n",
     "to": "  const position = Math.min(state.head, seq);\n"},
    {"id": "m9", "name": "a step forward from LIVE leaves LIVE", "file": STATE_REL,
     "from": '      if (state.mode === "live" && event.delta > 0) return state;\n', "to": ""},
    {"id": "m10", "name": "the queue overflows at the cap itself", "file": STATE_REL,
     "from": "  return state.queued > SCRUB_QUEUE_CAP;\n", "to": "  return state.queued >= SCRUB_QUEUE_CAP;\n"},
    {"id": "m11", "name": "Shift is ignored on the arrows", "file": STATE_REL,
     "from": '    return shiftKey ? { type: "step_phase", delta, stops } : { type: "step", delta };\n',
     "to": '    return { type: "step", delta };\n'},
    {"id": "m12", "name": "the catch-up replays every queued event", "file": STATE_REL,
     "from": "  const steps = Math.min(to - from, CATCH_UP_MAX_STEPS);\n", "to": "  const steps = to - from;\n"},
    {"id": "m13", "name": "reduced motion still fast-forwards", "file": STATE_REL,
     "from": "  if (reducedMotion) return [{ atMs: 0, seq: to }];\n", "to": ""},
    {"id": "m14", "name": "the frame length drifts from the motion token", "file": STATE_REL,
     "from": "export const CATCH_UP_STEP_MS = 120;\n", "to": "export const CATCH_UP_STEP_MS = 150;\n"},
    {"id": "m15", "name": "segment states come from the whole ledger", "file": VIEW_REL,
     "from": "  const current = at.lastSeq === null ? -1 : TIMELINE_PHASES.indexOf(at.current);\n",
     "to": "  const current = whole.lastSeq === null ? -1 : TIMELINE_PHASES.indexOf(whole.current);\n"},
    {"id": "m16", "name": "a one-event phase is drawn compact", "file": VIEW_REL,
     "from": "    const compact = range !== null && range[0] === range[1];\n",
     "to": "    const compact = range !== null && range[1] - range[0] <= 1;\n"},
    {"id": "m17", "name": "a glyph at the handle is not reached", "file": VIEW_REL,
     "from": "      reached: g.seq <= position,\n", "to": "      reached: g.seq < position,\n"},
    {"id": "m18", "name": "the readout shows elapsed time before the first event", "file": VIEW_REL,
     "from": "    if (position >= 0 && args.elapsed !== null) readout += ` · ${args.elapsed}`;\n",
     "to": "    if (args.elapsed !== null) readout += ` · ${args.elapsed}`;\n"},
    {"id": "m19", "name": "the view reads the wall clock", "file": VIEW_REL,
     "from": "  const ranges = rangesOf(whole);\n", "to": "  const ranges = rangesOf(whole);\n  void Date.now();\n"},
    {"id": "m20", "name": "a label drifts from the dashboard's title", "file": VIEW_REL,
     "from": '  test: "Test",\n', "to": '  test: "Tests",\n'},
]


def edits_of(mut):
    return mut.get("edits") or [{"from": mut["from"], "to": mut["to"]}]


def sha256_of(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_vitest(worktree, tag):
    cache_dir = HELPER_DIR / f"cache-{tag}-{int(time.time() * 1000)}"
    config = HELPER_DIR / f"vitest.config.{tag}.mjs"
    include = ", ".join(f'"{worktree / f}"' for f in VITEST_FILES)
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
    if m:
        failed, passed = int(m.group(1)), int(m.group(2))
    else:
        m2 = re.search(r"Tests\s+(\d+)\s+passed", out)
        failed, passed = (0, int(m2.group(1))) if m2 else (-1, -1)
    return {"exit": proc.returncode, "failed": failed, "passed": passed}


def run_guard(worktree):
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         str(worktree / GUARD_REL), f"--rootdir={worktree}"],
        cwd=str(worktree), capture_output=True, text=True, timeout=180)
    out = proc.stdout + proc.stderr
    failed = int(m.group(1)) if (m := re.search(r"(\d+) failed", out)) else 0
    passed = int(m.group(1)) if (m := re.search(r"(\d+) passed", out)) else 0
    return {"exit": proc.returncode, "failed": failed, "passed": passed}


def run_both(worktree, tag):
    return run_vitest(worktree, tag), run_guard(worktree)


def fmt(v, g):
    return (f"vitest exit={v['exit']} failed={v['failed']} passed={v['passed']} | "
            f"guard exit={g['exit']} failed={g['failed']} passed={g['passed']}")


def main():
    if len(sys.argv) != 2:
        print("usage: mutations.py <worktree_root>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()
    print(f"worktree: {worktree}")
    v, g = run_both(worktree, "control-first")
    print(f"CONTROL FIRST: {fmt(v, g)}")
    first_green = v["exit"] == 0 and v["failed"] == 0 and g["exit"] == 0 and g["failed"] == 0
    if not first_green:
        print("control is not green; aborting")
        return 1
    all_ok = True
    for mut in MUTATIONS:
        target = worktree / mut["file"]
        original = target.read_bytes()
        digest = sha256_of(target)
        text = original.decode("utf-8")
        counts = []
        for edit in edits_of(mut):
            counts.append(text.count(edit["from"]))
            text = text.replace(edit["from"], edit["to"], 1)
        if counts != [1] * len(counts):
            print(f"{mut['id']}: SKIPPED, FROM occurrences {counts}")
            all_ok = False
            continue
        target.write_bytes(text.encode("utf-8"))
        try:
            v, g = run_both(worktree, mut["id"])
        finally:
            target.write_bytes(original)
        restored = sha256_of(target) == digest
        caught = (v["exit"] != 0 and v["failed"] > 0) or (g["exit"] != 0 and g["failed"] > 0)
        all_ok &= caught and restored
        print(f"{mut['id']} ({mut['name']}): {fmt(v, g)} | caught={caught} restored byte-identical={restored}")
    v, g = run_both(worktree, "control-last")
    last_green = v["exit"] == 0 and v["failed"] == 0 and g["exit"] == 0 and g["failed"] == 0
    print(f"CONTROL LAST: {fmt(v, g)}")
    all_ok &= last_green
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
