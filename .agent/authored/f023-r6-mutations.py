#!/usr/bin/env python3
"""Mutation tool for F023 T003 second part: deep links, cluster expansion, the camera and their guards.

Given a worktree root, runs an unmutated control first and last, and between them applies
each mutation below (every FROM must occur exactly once in its file), runs the vitest files
of this round and the Python contract guard, restores the file BYTE-IDENTICAL, and reports
each runner's failed count and exit code. A mutation is caught when at least one runner
goes red. vitest runs from the PRIMARY `apps/ui` (a worktree has no node_modules) with a
scratch config under `.remedy-wt/f023-r6-mutscratch/`; pytest runs with `python3 -B` so a
bytecode cache can never serve a previous mutation's module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f023-r6-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

G = "apps/ui/src/components/graph/"
EXPAND_REL = G + "clusterExpansion.ts"
LINK_REL = G + "zoomDeepLink.ts"
HOOK_REL = G + "useZoomDeepLink.ts"
LAYOUT_REL = G + "buildForceBrainModel.ts"
STAGE_REL = G + "BrainGraphStage.tsx"
CANVAS_REL = G + "ForceBrainGraph.tsx"
VITEST_FILES = [
    G + "clusterExpansion.test.ts",
    G + "zoomDeepLink.test.ts",
]
GUARD_RELS = [
    "tests/ui_contracts/test_zoom_deep_link_wiring.py",
    "tests/ui_contracts/test_semantic_zoom_wiring.py",
]

MUTATIONS = [
    {"id": "m1", "name": "the chip's link survives its expansion", "file": EXPAND_REL,
     "from": "    ...clustered.links.filter((l) => l.target !== chipId),\n", "to": "    ...clustered.links,\n"},
    {"id": "m2", "name": "runs already shown are added a second time", "file": EXPAND_REL,
     "from": '    .filter((n) => n.parentId === taskId && n.kind !== "cluster" && !shown.has(n.id))\n',
     "to": '    .filter((n) => n.parentId === taskId && n.kind !== "cluster")\n'},
    {"id": "m3", "name": "a task with no chip gets a new object", "file": EXPAND_REL,
     "from": "  if (chipIndex < 0) return clustered;\n", "to": "  if (chipIndex < 0) return { ...clustered };\n"},
    {"id": "m4", "name": "the layout never expands", "file": LAYOUT_REL,
     "from": "  const clustered = expandTaskId === null\n", "to": "  const clustered = expandTaskId === null || expandTaskId !== null\n"},
    {"id": "m5", "name": "a link below L3 reads a tab", "file": LINK_REL,
     "from": "  if (level !== \"3\") return { focusId, tab: null };\n", "to": ""},
    {"id": "m6", "name": "an L3 link without a tab opens none", "file": LINK_REL,
     "from": ': "diff" };\n', "to": ": null };\n"},
    {"id": "m7", "name": "the URL records every level as 1", "file": LINK_REL,
     "from": '    params.set("level", String(state.level));\n', "to": '    params.set("level", "1");\n'},
    {"id": "m8", "name": "an L3 link replays no tab", "file": LINK_REL,
     "from": '  if (link.tab !== null) events.push({ type: "open_evidence", tab: link.tab });\n', "to": ""},
    {"id": "m9", "name": "every step adds a history entry", "file": HOOK_REL,
     "from": "    window.history.replaceState(", "to": "    window.history.pushState("},
    {"id": "m10", "name": "a link replays before its node exists", "file": HOOK_REL,
     "from": "    if (!link || !graph.has(link.focusId)) return;\n", "to": "    if (!link) return;\n"},
    {"id": "m11", "name": "a reader moving first does not cancel the link", "file": HOOK_REL,
     "from": "      if (state === ZOOM_HOME) return;\n", "to": "      return;\n"},
    {"id": "m12", "name": "the stage expands the run's level instead of the task's", "file": STAGE_REL,
     "from": "  const expandTaskId = zoomCrumbs.find((c) => c.level === 1)?.nodeId ?? null;\n",
     "to": "  const expandTaskId = zoomCrumbs.find((c) => c.level === 2)?.nodeId ?? null;\n"},
    {"id": "m13", "name": "the stage no longer restores the link", "file": STAGE_REL,
     "from": "  useZoomDeepLink(zoomGraph, zoom.state, zoom.dispatch);\n", "to": ""},
    {"id": "m14", "name": "the camera does not wait for the canvas", "file": CANVAS_REL,
     "from": "  }, [zoom, graphReady]);\n", "to": "  }, [zoom]);\n"},
    {"id": "m15", "name": "the settled fit forces the organism's camera", "file": CANVAS_REL,
     "from": "      const camera = zoomCamera(layoutRef.current, zoomRef.current) ?? { x: 0, y: 0, k: ZOOM_HOME_CAMERA };\n",
     "to": "      const camera = { x: 0, y: 0, k: ZOOM_HOME_CAMERA };\n"},
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
         *[str(worktree / g) for g in GUARD_RELS], f"--rootdir={worktree}"],
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
