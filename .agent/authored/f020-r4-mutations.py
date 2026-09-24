#!/usr/bin/env python3
"""Mutation tool for F020 T003's first half: state motion, the pulse, the frame rule and the canvas wiring.

Given a worktree root, runs an unmutated control first and last, and between them applies
each mutation below (every FROM must occur exactly once in its file), runs the vitest files
of this round and the Python contract tests, restores the file BYTE-IDENTICAL, and reports
each runner's failed count and exit code. A mutation is caught when at least one runner
goes red. vitest runs from the PRIMARY `apps/ui` (a worktree has no node_modules) with a
scratch config under `.remedy-wt/f020-r4-mutscratch/`; pytest runs with `python3 -B` so a
bytecode cache can never serve a previous mutation's module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f020-r4-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

MOTION_REL = "apps/ui/src/components/graph/renderers/stateMotion.ts"
STATES_REL = "apps/ui/src/components/graph/renderers/nodeStates.ts"
PAINT_REL = "apps/ui/src/components/graph/renderers/paintNode.ts"
CANVAS_REL = "apps/ui/src/components/graph/ForceBrainGraph.tsx"
VISIBLE_REL = "apps/ui/src/components/graph/usePageVisible.ts"
VITEST_FILES = [
    "apps/ui/src/components/graph/renderers/stateMotion.test.ts",
    "apps/ui/src/components/graph/renderers/paintNode.test.ts",
    "apps/ui/src/components/graph/renderers/nodeStates.test.ts",
]
GUARD_FILES = [
    "tests/ui_contracts/test_brain_motion_wiring.py",
    "tests/ui_contracts/test_node_glyph_tokens.py",
]

MUTATIONS = [
    {"id": "m1", "name": "reduced motion still schedules state changes", "file": MOTION_REL,
     "from": "  if (previous === null || reducedMotion) return [];\n", "to": "  if (previous === null) return [];\n"},
    {"id": "m2", "name": "the job core's state change is scheduled", "file": MOTION_REL,
     "from": '    .filter((n) => n.kind !== "job_core" && before.has(n.id) && before.get(n.id) !== n.state)\n',
     "to": "    .filter((n) => before.has(n.id) && before.get(n.id) !== n.state)\n"},
    {"id": "m3", "name": "every state change ripples", "file": MOTION_REL,
     "from": '      ripple: n.state === "pass",\n', "to": "      ripple: true,\n"},
    {"id": "m4", "name": "a node just born is scheduled as a change", "file": MOTION_REL,
     "from": '    .filter((n) => n.kind !== "job_core" && before.has(n.id) && before.get(n.id) !== n.state)\n',
     "to": '    .filter((n) => n.kind !== "job_core" && before.get(n.id) !== n.state)\n'},
    {"id": "m5", "name": "the crossfade runs backwards", "file": MOTION_REL,
     "from": "  return { fromAlpha: 1 - p, toAlpha: p, ripple, done: p >= 1 };\n",
     "to": "  return { fromAlpha: p, toAlpha: 1 - p, ripple, done: p >= 1 };\n"},
    {"id": "m6", "name": "the ripple travels linearly", "file": MOTION_REL,
     "from": "    ? { spread: COMPLETION_RIPPLE_SPREAD * easeOut(p), alpha: 1 - p }\n",
     "to": "    ? { spread: COMPLETION_RIPPLE_SPREAD * p, alpha: 1 - p }\n"},
    {"id": "m7", "name": "a hidden page still asks for frames", "file": MOTION_REL,
     "from": "  if (!needs.pageVisible) return false;\n", "to": ""},
    {"id": "m8", "name": "the pulse draws frames under reduced motion", "file": MOTION_REL,
     "from": "  return needs.pulsing && !needs.reducedMotion;\n", "to": "  return needs.pulsing;\n"},
    {"id": "m9", "name": "the core counts as a pulsing node", "file": MOTION_REL,
     "from": '  return layout.nodes.some((n) => n.kind !== "job_core" && NODE_STATE_TREATMENTS[n.state].pulse);\n',
     "to": "  return layout.nodes.some((n) => NODE_STATE_TREATMENTS[n.state].pulse);\n"},
    {"id": "m10", "name": "the pulse multiplier ignores reduced motion", "file": STATES_REL,
     "from": "  if (!NODE_STATE_TREATMENTS[state].pulse || reducedMotion) return 1;\n",
     "to": "  if (!NODE_STATE_TREATMENTS[state].pulse) return 1;\n"},
    {"id": "m11", "name": "the old state is painted at full alpha during a change", "file": PAINT_REL,
     "from": "  if (t.fromAlpha > 0) paintBrainNode(ctx, { ...node, state: motion.fromState }, { ...pulsed, alpha: frame.alpha * t.fromAlpha });\n",
     "to": "  if (t.fromAlpha > 0) paintBrainNode(ctx, { ...node, state: motion.fromState }, { ...pulsed });\n"},
    {"id": "m12", "name": "the ripple is never painted", "file": PAINT_REL,
     "from": "  if (t.ripple) paintCompletionRipple(ctx, node, pulsed, t.ripple);\n", "to": ""},
    {"id": "m13", "name": "the painter ignores the pulse multiplier", "file": PAINT_REL,
     "from": "  const pulsed: NodePaintFrame = { ...frame, scale: frame.scale * motion.pulseScale };\n",
     "to": "  const pulsed: NodePaintFrame = { ...frame };\n"},
    {"id": "m14", "name": "the canvas redraws only for births again", "file": CANVAS_REL,
     "from": "          autoPauseRedraw={!animating}\n", "to": "          autoPauseRedraw={!birthsInFlight}\n"},
    {"id": "m15", "name": "particles flow on a hidden page", "file": CANVAS_REL,
     "from": "(l as BrainLayoutLink).active && !reducedMotion && pageVisible ? 1 : 0",
     "to": "(l as BrainLayoutLink).active && !reducedMotion ? 1 : 0"},
    {"id": "m16", "name": "the frame rule is told the page is always visible", "file": CANVAS_REL,
     "from": "  const animating = brainNeedsAnimationFrames({ pageVisible, reducedMotion, birthsInFlight, transitionsInFlight, pulsing });\n",
     "to": "  const animating = brainNeedsAnimationFrames({ pageVisible: true, reducedMotion, birthsInFlight, transitionsInFlight, pulsing });\n"},
    {"id": "m17", "name": "the canvas paints every node without its motion", "file": CANVAS_REL,
     "from": "    NODE_PAINTERS[n.kind](n, ctx, globalScale, paint, resolvedPalette.palette, motionOf(n));\n",
     "to": "    NODE_PAINTERS[n.kind](n, ctx, globalScale, paint, resolvedPalette.palette, { fromState: null, transition: null, pulseScale: 1 });\n"},
    {"id": "m18", "name": "the visibility hook never listens", "file": VISIBLE_REL,
     "from": '    document.addEventListener("visibilitychange", onChange);\n', "to": ""},
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
         *[str(worktree / g) for g in GUARD_FILES], f"--rootdir={worktree}"],
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
