#!/usr/bin/env python3
"""Mutation tool for F023 T001: the semantic-zoom machine, its wheel adapter and their guard.

Given a worktree root, runs an unmutated control first and last, and between them applies
each mutation below (every FROM must occur exactly once in its file), runs the vitest files
of this round and the Python contract guard, restores the file BYTE-IDENTICAL, and reports
each runner's failed count and exit code. A mutation is caught when at least one runner
goes red. vitest runs from the PRIMARY `apps/ui` (a worktree has no node_modules) with a
scratch config under `.remedy-wt/f023-r1-mutscratch/`; pytest runs with `python3 -B` so a
bytecode cache can never serve a previous mutation's module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f023-r1-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

MACHINE_REL = "apps/ui/src/components/graph/semanticZoom.ts"
WHEEL_REL = "apps/ui/src/components/graph/zoomWheel.ts"
VITEST_FILES = [
    "apps/ui/src/components/graph/semanticZoom.test.ts",
    "apps/ui/src/components/graph/zoomWheel.test.ts",
]
GUARD_REL = "tests/ui_contracts/test_semantic_zoom_contract.py"

MUTATIONS = [
    {"id": "m1", "name": "Escape at L3 skips run detail", "file": MACHINE_REL,
     "from": "  if (state.level === 3) return moveTo(state, { level: 2, focusId: state.focusId, tab: null });\n",
     "to": "  if (state.level === 3) return moveTo(state, { level: 1, focusId: state.focusId, tab: null });\n"},
    {"id": "m2", "name": "an empty transition returns a new object", "file": MACHINE_REL,
     "from": "  return step(same ? state : next);\n", "to": "  return step(next);\n"},
    {"id": "m3", "name": "the wheel leaves run detail", "file": MACHINE_REL,
     "from": '  if (state.level >= 2) return step(state, "the wheel does not leave run detail; Escape walks back");\n',
     "to": ""},
    {"id": "m4", "name": "a run click opens its task, not the run", "file": MACHINE_REL,
     "from": "    return moveTo(state, { level: 2, focusId: nodeId, tab: null });\n",
     "to": "    return moveTo(state, taskFocus(owningTaskId(graph, nodeId) as string));\n"},
    {"id": "m5", "name": "a deeper breadcrumb is not refused with its note", "file": MACHINE_REL,
     "from": '  if (level >= state.level) return step(state, level > state.level ? "a breadcrumb only walks back" : null);\n',
     "to": "  if (level === state.level) return step(state);\n"},
    {"id": "m6", "name": "evidence opens from task focus", "file": MACHINE_REL,
     "from": '  if (state.level < 2) return step(state, "evidence opens from a run\'s detail");\n',
     "to": '  if (state.level < 1) return step(state, "evidence opens from a run\'s detail");\n'},
    {"id": "m7", "name": "reconcile leaves a dangling focus", "file": MACHINE_REL,
     "from": "  if (state.focusId === null || graph.has(state.focusId)) return step(state);\n",
     "to": "  return step(state);\n"},
    {"id": "m8", "name": "a later node list overwrites an earlier one", "file": MACHINE_REL,
     "from": "      if (!graph.has(n.id)) graph.set(n.id, { kind: n.kind, parentId: n.parentId });\n",
     "to": "      graph.set(n.id, { kind: n.kind, parentId: n.parentId });\n"},
    {"id": "m9", "name": "the run crumb is current at L3", "file": MACHINE_REL,
     "from": "  if (state.level >= 2) crumbs.push({ level: 2, nodeId: state.focusId, current: state.level === 2 });\n",
     "to": "  if (state.level >= 2) crumbs.push({ level: 2, nodeId: state.focusId, current: state.level >= 2 });\n"},
    {"id": "m10", "name": "a wheel crossing out walks back one level only", "file": MACHINE_REL,
     "from": '    case "zoom_out":\n      return moveTo(state, ZOOM_HOME);\n',
     "to": '    case "zoom_out":\n      return onEscape(graph, state);\n'},
    {"id": "m11", "name": "the machine imports React state", "file": MACHINE_REL,
     "from": 'import type { BrainNode, NodeKind } from "./brainOntology";\n',
     "to": 'import type { BrainNode, NodeKind } from "./brainOntology";\nimport { useState } from "react";\nexport const HOOK = useState;\n'},
    {"id": "m12", "name": "reaching 1.6 already zooms in", "file": WHEEL_REL,
     "from": '  if (previous <= ZOOM_IN_ABOVE && next > ZOOM_IN_ABOVE) return "in";\n',
     "to": '  if (previous < ZOOM_IN_ABOVE && next >= ZOOM_IN_ABOVE) return "in";\n'},
    {"id": "m13", "name": "the dead band collapses: out at the in threshold", "file": WHEEL_REL,
     "from": "export const ZOOM_OUT_BELOW = 0.8;\n", "to": "export const ZOOM_OUT_BELOW = 1.6;\n"},
    {"id": "m14", "name": "the in threshold drifts from graph_spec", "file": WHEEL_REL,
     "from": "export const ZOOM_IN_ABOVE = 1.6;\n", "to": "export const ZOOM_IN_ABOVE = 1.5;\n"},
    {"id": "m15", "name": "a wheel-in over empty space still zooms in", "file": WHEEL_REL,
     "from": '  if (crossing === "in" && nodeIdUnderPointer !== null) return { type: "zoom_in", nodeId: nodeIdUnderPointer };\n',
     "to": '  if (crossing === "in") return { type: "zoom_in", nodeId: nodeIdUnderPointer ?? "" };\n'},
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
