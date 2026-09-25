#!/usr/bin/env python3
"""Mutation tool for F020 T002's second half: the legend, the cluster's count and the matrix fixture.

Given a worktree root, runs an unmutated control first and last, and between them applies
each mutation below (every FROM must occur exactly once in its file), runs the vitest files
of this round and the Python contract tests, restores the file BYTE-IDENTICAL, and reports
each runner's failed count and exit code. A mutation is caught when at least one runner
goes red. vitest runs from the PRIMARY `apps/ui` (a worktree has no node_modules) with a
scratch config under `.remedy-wt/f020-r3-mutscratch/`; pytest runs with `python3 -B` so a
bytecode cache can never serve a previous mutation's module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f020-r3-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

LEGEND_MODEL_REL = "apps/ui/src/components/graph/renderers/legendModel.ts"
MATRIX_REL = "apps/ui/src/components/graph/renderers/glyphMatrix.ts"
PAINT_REL = "apps/ui/src/components/graph/renderers/paintNode.ts"
PALETTE_REL = "apps/ui/src/components/graph/renderers/palette.ts"
LAYOUT_REL = "apps/ui/src/components/graph/buildForceBrainModel.ts"
LEGEND_REL = "apps/ui/src/components/graph/GraphLegend.tsx"
STAGE_REL = "apps/ui/src/components/graph/BrainGraphStage.tsx"
VITEST_FILES = [
    "apps/ui/src/components/graph/renderers/legendModel.test.ts",
    "apps/ui/src/components/graph/renderers/glyphMatrix.test.ts",
    "apps/ui/src/components/graph/renderers/paintNode.test.ts",
    "apps/ui/src/components/graph/renderers/palette.test.ts",
    "apps/ui/src/components/graph/buildForceBrainModel.test.ts",
]
GUARD_FILES = [
    "tests/ui_contracts/test_graph_legend_contract.py",
    "tests/ui_contracts/test_node_glyph_tokens.py",
]

MUTATIONS = [
    {"id": "m1", "name": "the kind rows ignore the module they are given", "file": LEGEND_MODEL_REL,
     "from": "  return Object.entries(glyphs).map(([kind, g]) => ({\n",
     "to": "  return Object.entries(GLYPHS).map(([kind, g]) => ({\n"},
    {"id": "m2", "name": "a kind row carries its fill path as its stroke", "file": LEGEND_MODEL_REL,
     "from": "    kind: kind as NodeKind, name: g.name, strokePath: g.strokePath, fillPath: g.fillPath,\n",
     "to": "    kind: kind as NodeKind, name: g.name, strokePath: g.fillPath, fillPath: g.fillPath,\n"},
    {"id": "m3", "name": "a state row's mark takes another mark's path", "file": LEGEND_MODEL_REL,
     "from": "      strokePath: STATE_MARK_PATHS[m.mark].strokePath,\n",
     "to": "      strokePath: STATE_MARK_PATHS.strike.strokePath,\n"},
    {"id": "m4", "name": "tokenVar writes the bare token", "file": LEGEND_MODEL_REL,
     "from": "  return `var(${token})`;\n", "to": "  return token;\n"},
    {"id": "m5", "name": "the matrix columns run in reverse state order", "file": MATRIX_REL,
     "from": "  const states: NodeState[] = nodeStateOrder();\n",
     "to": "  const states: NodeState[] = nodeStateOrder().reverse();\n"},
    {"id": "m6", "name": "the matrix grows a core row", "file": MATRIX_REL,
     "from": '  const kinds = glyphKinds().filter((k) => k !== "job_core");\n',
     "to": "  const kinds = glyphKinds();\n"},
    {"id": "m7", "name": "the matrix paints at a zoom that hides run glyphs", "file": MATRIX_REL,
     "from": "export const MATRIX_ZOOM = GLYPH_MIN_ZOOM_RUN;\n", "to": "export const MATRIX_ZOOM = 1;\n"},
    {"id": "m8", "name": "a cluster cell carries no count", "file": MATRIX_REL,
     "from": '      label: kind === "cluster" ? MATRIX_CLUSTER_LABEL : "",\n', "to": '      label: "",\n'},
    {"id": "m9", "name": "the painter writes any kind's label", "file": PAINT_REL,
     "from": '  if (node.kind === "cluster" && node.label) {\n', "to": "  if (node.label) {\n"},
    {"id": "m10", "name": "the count is written in the fill colour", "file": PAINT_REL,
     "from": "    ctx.fillStyle = line;\n", "to": "    ctx.fillStyle = fill;\n"},
    {"id": "m11", "name": "the count's font names no resolved family", "file": PAINT_REL,
     "from": "    ctx.font = `600 ${radius * CLUSTER_COUNT_SIZE}px ${tokenValue(frame.palette, BRAIN_LABEL_FONT_TOKEN)}`;\n",
     "to": "    ctx.font = `600 ${radius * CLUSTER_COUNT_SIZE}px sans-serif`;\n"},
    {"id": "m12", "name": "the count's font leaves the palette", "file": PALETTE_REL,
     "from": "  return [...new Set<RemedyToken>([...nodeStateTokens(), BRAIN_HIGHLIGHT_TOKEN, BRAIN_LABEL_FONT_TOKEN])];\n",
     "to": "  return [...new Set<RemedyToken>([...nodeStateTokens(), BRAIN_HIGHLIGHT_TOKEN])];\n"},
    {"id": "m13", "name": "the layout gives a cluster no label", "file": LAYOUT_REL,
     "from": '      depth: 2, radius, x: p.x, y: p.y, label: n.kind === "cluster" ? clusterLabelOf(n) : "",\n',
     "to": '      depth: 2, radius, x: p.x, y: p.y, label: "",\n'},
    {"id": "m14", "name": "the cluster label drops its plus sign", "file": LAYOUT_REL,
     "from": '  return typeof count === "number" && count > 0 ? `+${count}` : "";\n',
     "to": '  return typeof count === "number" && count > 0 ? `${count}` : "";\n'},
    {"id": "m15", "name": "the legend draws a path literal of its own", "file": LEGEND_REL,
     "from": "                  {row.strokePath && <path d={row.strokePath} className={styles.kindLine} />}\n",
     "to": '                  {row.strokePath && <path d="M3 21L21 3" className={styles.kindLine} />}\n'},
    {"id": "m16", "name": "the legend paints a colour that is not a token", "file": LEGEND_REL,
     "from": "          {m.fillPath && <path d={m.fillPath} style={{ fill: tokenVar(m.token) }} />}\n",
     "to": '          {m.fillPath && <path d={m.fillPath} style={{ fill: "red" }} />}\n'},
    {"id": "m17", "name": "the legend writes a kind's name by hand", "file": LEGEND_REL,
     "from": "                {row.name}\n              </li>\n            ))}\n          </ul>\n          <p className={styles.heading}>States</p>\n",
     "to": '                {"Builder run"}\n              </li>\n            ))}\n          </ul>\n          <p className={styles.heading}>States</p>\n'},
    {"id": "m18", "name": "the legend no longer closes on Escape", "file": LEGEND_REL,
     "from": '    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") setOpen(false); };\n',
     "to": "    const onKey = (_e: KeyboardEvent) => {};\n"},
    {"id": "m19", "name": "the stage no longer mounts the legend", "file": STAGE_REL,
     "from": "        <GraphLegend />\n", "to": ""},
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
