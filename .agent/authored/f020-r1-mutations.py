#!/usr/bin/env python3
"""Mutation tool for F020 T001: the glyph geometry, the state language and the token guard.

Given a worktree root, runs an unmutated control first and last, and between them applies
each mutation below (every FROM must occur exactly once in its file), runs the vitest files
of this round and the Python token guard, restores the file BYTE-IDENTICAL, and reports
each runner's failed count and exit code. A mutation is caught when at least one runner
goes red. vitest runs from the PRIMARY `apps/ui` (a worktree has no node_modules) with a
scratch config under `.remedy-wt/f020-r1-mutscratch/`; pytest runs with `python3 -B` so a
bytecode cache can never serve a previous mutation's module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f020-r1-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

GLYPHS_REL = "apps/ui/src/components/graph/renderers/glyphPaths.ts"
STATES_REL = "apps/ui/src/components/graph/renderers/nodeStates.ts"
TOKENS_REL = "apps/ui/src/styles/tokens.css"
VITEST_FILES = [
    "apps/ui/src/components/graph/renderers/glyphPaths.test.ts",
    "apps/ui/src/components/graph/renderers/nodeStates.test.ts",
]
GUARD_REL = "tests/ui_contracts/test_node_glyph_tokens.py"

MUTATIONS = [
    {"id": "m1", "name": "the builder glyph's geometry drifts", "file": GLYPHS_REL,
     "from": '    strokePath: "M8 7L4 12L8 17M16 7L20 12L16 17M13.5 5L10.5 19",\n',
     "to": '    strokePath: "M8 7L4 12L8 17M16 7L20 12L16 17M13 5L11 19",\n'},
    {"id": "m2", "name": "the flask's declared bounds stop short of its base", "file": GLYPHS_REL,
     "from": "    bounds: { minX: 4.5, minY: 3, maxX: 19.5, maxY: 21 },\n",
     "to": "    bounds: { minX: 4.5, minY: 3, maxX: 19.5, maxY: 20 },\n"},
    {"id": "m3", "name": "glyphPath2D rebuilds its paths on every call", "file": GLYPHS_REL,
     "from": "  if (cached) return cached;\n", "to": ""},
    {"id": "m4", "name": "the canvas stroke is built from the fill string", "file": GLYPHS_REL,
     "from": "    stroke: geometry.strokePath ? new Path2D(geometry.strokePath) : null,\n",
     "to": "    stroke: geometry.strokePath ? new Path2D(geometry.fillPath) : null,\n"},
    {"id": "m5", "name": "run glyphs show from a lower zoom than L1", "file": GLYPHS_REL,
     "from": "export const GLYPH_MIN_ZOOM_RUN = 1.6;\n", "to": "export const GLYPH_MIN_ZOOM_RUN = 1.5;\n"},
    {"id": "m6", "name": "glyphTransform scales the box to the radius, not the diameter", "file": GLYPHS_REL,
     "from": "  const scale = (2 * radius) / GLYPH_BOX;\n", "to": "  const scale = radius / GLYPH_BOX;\n"},
    {"id": "m7", "name": "a failed node loses its status dot (colour alone)", "file": STATES_REL,
     "edits": [{"from": (
         '    name: "Failed",\n'
         '    fillToken: "--remedy-state-blocked",\n'
         '    halo: { token: "--remedy-state-blocked", alpha: 0.4 },\n'
         '    sizeFactor: 1,\n'
         '    marks: [{ mark: "status_dot", token: "--remedy-state-blocked", outlineToken: "--remedy-graph-node-ring" }],\n'),
         "to": (
         '    name: "Failed",\n'
         '    fillToken: "--remedy-state-blocked",\n'
         '    halo: { token: "--remedy-state-blocked", alpha: 0.4 },\n'
         '    sizeFactor: 1,\n'
         '    marks: [],\n')}]},
    {"id": "m8", "name": "a veto no longer dims what hangs below it", "file": STATES_REL,
     "from": "    downstreamAlpha: 0.4,\n", "to": "    downstreamAlpha: 1,\n"},
    {"id": "m9", "name": "a planned node is drawn full size", "file": STATES_REL,
     "from": "    sizeFactor: 0.9,\n", "to": "    sizeFactor: 1,\n"},
    {"id": "m10", "name": "reduced motion still pulses", "file": STATES_REL,
     "from": "  if (!treatment.pulse || reducedMotion) return treatment.sizeFactor;\n",
     "to": "  if (!treatment.pulse) return treatment.sizeFactor;\n"},
    {"id": "m11", "name": "the in-progress state is painted with the open token", "file": STATES_REL,
     "from": '    fillToken: "--remedy-state-current",\n', "to": '    fillToken: "--remedy-state-open",\n'},
    {"id": "m12", "name": "the vetoed state names a token the sheet never declares", "file": STATES_REL,
     "from": '    fillToken: "--remedy-state-vetoed",\n', "to": '    fillToken: "--remedy-state-veto",\n'},
    {"id": "m13", "name": "the pulse constant drifts from --remedy-dur-pulse", "file": STATES_REL,
     "from": "export const NODE_PULSE_MS = 1600;\n", "to": "export const NODE_PULSE_MS = 1500;\n"},
    {"id": "m14", "name": "a raw colour literal enters the state module", "file": STATES_REL,
     "from": "/** In-progress pulse depth: ±8% scale (graph_spec §12 \"Active pulse\"). */\n",
     "to": "/** In-progress pulse depth: ±8% scale (graph_spec §12 \"Active pulse\"), #4c83ff. */\n"},
    {"id": "m15", "name": "the app sheet's vetoed grey drifts from the reference", "file": TOKENS_REL,
     "from": "  --remedy-state-vetoed: #9aa9c5;\n", "to": "  --remedy-state-vetoed: #9aa9c6;\n"},
    {"id": "m16", "name": "the glyph module's header misquotes the precedence rule", "file": GLYPHS_REL,
     "from": '// + this table win over any feature-file prose."\n', "to": '// + this table wins over any feature-file prose."\n'},
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
