#!/usr/bin/env python3
"""Mutation tool for F020 T002's first half: the palette bridge, the node painter and the canvas wiring.

Given a worktree root, runs an unmutated control first and last, and between them applies
each mutation below (every FROM must occur exactly once in its file), runs the vitest files
of this round and the Python token guard, restores the file BYTE-IDENTICAL, and reports
each runner's failed count and exit code. A mutation is caught when at least one runner
goes red. vitest runs from the PRIMARY `apps/ui` (a worktree has no node_modules) with a
scratch config under `.remedy-wt/f020-r2-mutscratch/`; pytest runs with `python3 -B` so a
bytecode cache can never serve a previous mutation's module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f020-r2-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

PAINT_REL = "apps/ui/src/components/graph/renderers/paintNode.ts"
PALETTE_REL = "apps/ui/src/components/graph/renderers/palette.ts"
STATES_REL = "apps/ui/src/components/graph/renderers/nodeStates.ts"
CANVAS_REL = "apps/ui/src/components/graph/ForceBrainGraph.tsx"
VITEST_FILES = [
    "apps/ui/src/components/graph/renderers/glyphPaths.test.ts",
    "apps/ui/src/components/graph/renderers/nodeStates.test.ts",
    "apps/ui/src/components/graph/renderers/paintNode.test.ts",
    "apps/ui/src/components/graph/renderers/palette.test.ts",
]
GUARD_REL = "tests/ui_contracts/test_node_glyph_tokens.py"

MUTATIONS = [
    {"id": "m1", "name": "the halo is drawn at full alpha", "file": PAINT_REL,
     "from": "      ctx.globalAlpha = frame.alpha * treatment.halo.alpha;\n",
     "to": "      ctx.globalAlpha = frame.alpha;\n"},
    {"id": "m2", "name": "the painter ignores the state's size factor", "file": PAINT_REL,
     "from": "  const radius = node.radius * treatment.sizeFactor * frame.scale;\n",
     "to": "  const radius = node.radius * frame.scale;\n"},
    {"id": "m3", "name": "a run's glyph is drawn at every zoom", "file": PAINT_REL,
     "from": "    if (paths.stroke && glyphDrawnAt(node.kind, frame.zoom)) {\n",
     "to": "    if (paths.stroke) {\n"},
    {"id": "m4", "name": "the state marks are never drawn", "file": PAINT_REL,
     "from": "  for (const mark of treatment.marks) drawMark(ctx, mark, node, radius, frame.palette);\n",
     "to": ""},
    {"id": "m5", "name": "a mark's outline is never drawn", "file": PAINT_REL,
     "from": "    if (mark.outlineToken && shape) {\n", "to": "    if (false && mark.outlineToken && shape) {\n"},
    {"id": "m6", "name": "the artifact is drawn as a sphere", "file": PAINT_REL,
     "from": '  "task", "builder_run", "review_run", "repair_run", "test_run",\n',
     "to": '  "task", "builder_run", "review_run", "repair_run", "test_run", "artifact",\n'},
    {"id": "m7", "name": "the sphere's gloss starts from the fill, not the highlight", "file": PAINT_REL,
     "from": "    gradient.addColorStop(0, highlight);\n", "to": "    gradient.addColorStop(0, fill);\n"},
    {"id": "m8", "name": "a token that resolves to nothing is not named", "file": PALETTE_REL,
     "from": "    if (!value) missing.push(token);\n", "to": ""},
    {"id": "m9", "name": "a resolved value keeps the stylesheet's whitespace", "file": PALETTE_REL,
     "from": "    const value = read(token).trim();\n", "to": "    const value = read(token);\n"},
    {"id": "m10", "name": "the canvas paints builder runs with the core's painter", "file": CANVAS_REL,
     "from": "  builder_run: paintGlyphNode,\n", "to": "  builder_run: paintCoreNode,\n"},
    {"id": "m11", "name": "the palette is resolved again on every layout", "file": CANVAS_REL,
     "from": "  const resolvedPalette = useMemo(() => readDocumentPalette(), []);\n",
     "to": "  const resolvedPalette = useMemo(() => readDocumentPalette(), [layout]);\n"},
    {"id": "m12", "name": "the canvas passes a fixed zoom to the painter", "file": CANVAS_REL,
     "from": "  paintBrainNode(ctx, node, { palette, zoom: globalScale, alpha: paint.alpha, scale: paint.scale });\n",
     "to": "  paintBrainNode(ctx, node, { palette, zoom: 1, alpha: paint.alpha, scale: paint.scale });\n"},
    {"id": "m13", "name": "a raw colour literal enters the painter", "file": PAINT_REL,
     "from": "/** How far the soft halo reaches past the node's edge, in world units (the\n",
     "to": "/** How far the soft halo (#4c83ff) reaches past the node's edge, in world units (the\n"},
    {"id": "m14", "name": "the canvas paints a state colour of its own again", "file": CANVAS_REL,
     "from": '  ctx.fillStyle = "#ffffff";\n', "to": '  ctx.fillStyle = "#34c27e";\n'},
    {"id": "m15", "name": "a planned glyph is inked in the planned white", "file": STATES_REL,
     "from": '    inkToken: "--remedy-state-planned-ring",\n', "to": '    inkToken: "--remedy-state-planned",\n'},
    {"id": "m16", "name": "the sphere glyph is stroked in the highlight, not the state's ink", "file": PAINT_REL,
     "from": "      inGlyphBox(ctx, node, radius, () => drawPaths(ctx, paths, null, ink));\n",
     "to": "      inGlyphBox(ctx, node, radius, () => drawPaths(ctx, paths, null, highlight));\n"},
    {"id": "m17", "name": "a shape kind is lined in its fill colour", "file": PAINT_REL,
     "from": "    inGlyphBox(ctx, node, radius, () => drawPaths(ctx, paths, fill, line));\n",
     "to": "    inGlyphBox(ctx, node, radius, () => drawPaths(ctx, paths, fill, fill));\n"},
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
