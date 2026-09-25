#!/usr/bin/env python3
"""Mutation tool for F023 T002 first half: the zoom render effects, the canvas wiring and their guard.

Given a worktree root, runs an unmutated control first and last, and between them applies
each mutation below (every FROM must occur exactly once in its file), runs the vitest files
of this round and the Python contract guard, restores the file BYTE-IDENTICAL, and reports
each runner's failed count and exit code. A mutation is caught when at least one runner
goes red. vitest runs from the PRIMARY `apps/ui` (a worktree has no node_modules) with a
scratch config under `.remedy-wt/f023-r2-mutscratch/`; pytest runs with `python3 -B` so a
bytecode cache can never serve a previous mutation's module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f023-r2-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

VIEW_REL = "apps/ui/src/components/graph/zoomView.ts"
CANVAS_REL = "apps/ui/src/components/graph/ForceBrainGraph.tsx"
STAGE_REL = "apps/ui/src/components/graph/BrainGraphStage.tsx"
HOOK_REL = "apps/ui/src/components/graph/useSemanticZoom.ts"
VITEST_FILES = [
    "apps/ui/src/components/graph/zoomView.test.ts",
]
GUARD_REL = "tests/ui_contracts/test_semantic_zoom_wiring.py"

MUTATIONS = [
    {"id": "m1", "name": "siblings dim to 40%, not 25%", "file": VIEW_REL,
     "from": "export const ZOOM_DIM_ALPHA = 0.25;\n", "to": "export const ZOOM_DIM_ALPHA = 0.4;\n"},
    {"id": "m2", "name": "the core dims with the siblings", "file": VIEW_REL,
     "from": "  const inBranch = (n: BrainLayoutNode) => n.depth === 0 || n.id === taskId || n.parentId === taskId;\n",
     "to": "  const inBranch = (n: BrainLayoutNode) => n.id === taskId || n.parentId === taskId;\n"},
    {"id": "m3", "name": "every active branch glows at L1 too", "file": VIEW_REL,
     "from": "    if (taskId === null || l.target === taskId || l.source === taskId) glowing.add(l.id);\n",
     "to": "    glowing.add(l.id);\n"},
    {"id": "m4", "name": "the ring stays on the task at L2", "file": VIEW_REL,
     "from": "    ringId: state.level === 0 ? null : state.focusId,\n",
     "to": "    ringId: state.level === 0 ? null : taskId,\n"},
    {"id": "m5", "name": "a click lands L1's camera inside the wheel's dead band", "file": VIEW_REL,
     "from": "export const ZOOM_TASK_CAMERA = 2;\n", "to": "export const ZOOM_TASK_CAMERA = 1.5;\n"},
    {"id": "m6", "name": "a focus hidden by a filter still dims the graph", "file": VIEW_REL,
     "from": "  return taskId !== undefined && layout.nodes.some((n) => n.id === taskId) ? taskId : null;\n",
     "to": "  return taskId ?? null;\n"},
    {"id": "m7", "name": "Escape in a text field walks the zoom back", "file": VIEW_REL,
     "from": '  return tag !== "INPUT" && tag !== "TEXTAREA" && tag !== "SELECT";\n',
     "to": '  return tag !== "TEXTAREA" && tag !== "SELECT";\n'},
    {"id": "m8", "name": "the camera move drifts off --remedy-dur-slow", "file": VIEW_REL,
     "from": "export const ZOOM_CAMERA_MS = 350;\n", "to": "export const ZOOM_CAMERA_MS = 300;\n"},
    {"id": "m9", "name": "the canvas reads its own camera move as a wheel", "file": CANVAS_REL,
     "from": "    if (performance.now() < cameraLockUntilRef.current) return;\n", "to": ""},
    {"id": "m10", "name": "the camera move sets no lock", "file": CANVAS_REL,
     "from": "    cameraLockUntilRef.current = performance.now() + ms + 100;\n", "to": ""},
    {"id": "m11", "name": "a click no longer reaches the machine", "file": CANVAS_REL,
     "from": '    onZoomEvent({ type: "click", nodeId: n.id });\n', "to": ""},
    {"id": "m12", "name": "a dimmed task's label is drawn at full strength", "file": CANVAS_REL,
     "from": "      ctx.globalAlpha = dim;\n", "to": ""},
    {"id": "m13", "name": "the stage checks focus against the view alone", "file": STAGE_REL,
     "from": "  const zoomGraph = useMemo(() => zoomGraphOf(model.nodes, layout.nodes), [model, layout]);\n",
     "to": "  const zoomGraph = useMemo(() => zoomGraphOf(layout.nodes), [layout]);\n"},
    {"id": "m14", "name": "Escape walks back under an open dialog", "file": HOOK_REL,
     "from": "      if (!escapeWalksBack(target, document.querySelector('[role=\"dialog\"]') !== null)) return;\n",
     "to": "      if (!escapeWalksBack(target, false)) return;\n"},
    {"id": "m15", "name": "the focus is no longer reconciled when the graph changes", "file": HOOK_REL,
     "from": "  }, [graph, dispatch]);\n", "to": "  }, [dispatch]);\n"},
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
