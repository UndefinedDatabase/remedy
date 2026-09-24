#!/usr/bin/env python3
"""Mutation tool for F020 T003's second half: the conformance probes, the binding spec and the pixel judge.

Given a worktree root, runs an unmutated control first and last, and between them applies
each mutation below (every FROM must occur exactly once in its file), runs the vitest files
of this round and the Python contract tests, restores the file BYTE-IDENTICAL, and reports
each runner's failed count and exit code. A mutation is caught when at least one runner
goes red. vitest runs from the PRIMARY `apps/ui` (a worktree has no node_modules) with a
scratch config under `.remedy-wt/f020-r5-mutscratch/`; pytest runs with `python3 -B` so a
bytecode cache can never serve a previous mutation's module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f020-r5-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

CONF_REL = "apps/ui/src/components/graph/renderers/glyphConformance.ts"
VITEST_FILES = [
    "apps/ui/src/components/graph/renderers/glyphConformance.test.ts",
]
GUARD_FILES = [
    "tests/ui_contracts/test_node_glyph_tokens.py",
]

MUTATIONS = [
    {"id": "m1", "name": "the spec drops the failed state's dot", "file": CONF_REL,
     "from": '  fail: ["status_dot"],\n', "to": "  fail: [],\n"},
    {"id": "m2", "name": "the dot is probed off its centre", "file": CONF_REL,
     "from": "  status_dot: { mark: [20, 4.5], outline: [20, 8.25] },\n",
     "to": "  status_dot: { mark: [18, 4.5], outline: [20, 8.25] },\n"},
    {"id": "m3", "name": "the strike's outline is probed on the strike itself", "file": CONF_REL,
     "from": "  strike: { mark: [6, 18], outline: [6.8, 18.8] },\n",
     "to": "  strike: { mark: [6, 18], outline: [6.5, 17.5] },\n"},
    {"id": "m4", "name": "a missing ring is probed too", "file": CONF_REL,
     "from": '      } else if (mark !== "ring") {\n', "to": "      } else {\n"},
    {"id": "m5", "name": "the probes ignore the state's size factor", "file": CONF_REL,
     "from": "    const t = glyphTransform(cell.node.x, cell.node.y, cell.node.radius * NODE_STATE_TREATMENTS[state].sizeFactor);\n",
     "to": "    const t = glyphTransform(cell.node.x, cell.node.y, cell.node.radius);\n"},
    {"id": "m6", "name": "a function colour's alpha is read unscaled", "file": CONF_REL,
     "from": "    return { r: Number(fn[1]), g: Number(fn[2]), b: Number(fn[3]), a: Math.round(alpha * 255) };\n",
     "to": "    return { r: Number(fn[1]), g: Number(fn[2]), b: Number(fn[3]), a: alpha };\n"},
    {"id": "m7", "name": "the tolerance excludes its own bound", "file": CONF_REL,
     "from": "  return d <= CONFORMANCE_TOLERANCE;\n", "to": "  return d < CONFORMANCE_TOLERANCE;\n"},
    {"id": "m8", "name": "an unpainted pixel counts as a colour", "file": CONF_REL,
     "from": "  if (pixel.a < CONFORMANCE_MIN_ALPHA) return false;\n", "to": ""},
    {"id": "m9", "name": "an absent probe passes when the colour shows", "file": CONF_REL,
     "from": '  const ok = probe.expect === "present" ? shows : !shows;\n', "to": "  const ok = shows;\n"},
    {"id": "m10", "name": "an unresolved token passes", "file": CONF_REL,
     "from": "  if (colour === null) return { ok: false, why: `${probe.token} does not resolve to a colour` };\n",
     "to": "  if (colour === null) return { ok: true, why: `${probe.token} does not resolve to a colour` };\n"},
    {"id": "m11", "name": "the strike is judged in the failure red", "file": CONF_REL,
     "from": '  strike: { mark: "--remedy-state-vetoed", outline: "--remedy-graph-node-ring" },\n',
     "to": '  strike: { mark: "--remedy-state-blocked", outline: "--remedy-graph-node-ring" },\n'},
    {"id": "m12", "name": "a raw colour literal enters the conformance module", "file": CONF_REL,
     "from": "/** An 8-bit RGBA colour. */\n", "to": "/** An 8-bit RGBA colour, like #ef6363. */\n"},
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
