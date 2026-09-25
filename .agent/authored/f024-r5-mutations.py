#!/usr/bin/env python3
"""Mutation tool for F024 T003 end-to-end: the fixture's ledger and the live scrub of a real fake job.

Given a worktree root, runs an unmutated control first and last, and between them applies
each mutation below (every FROM must occur exactly once in its file), runs the vitest files
of this round and the Python contract guard, restores the file BYTE-IDENTICAL, and reports
each runner's failed count and exit code. A mutation is caught when at least one runner
goes red. vitest runs from the PRIMARY `apps/ui` (a worktree has no node_modules) with a
scratch config under `.remedy-wt/f024-r5-mutscratch/`; pytest runs with `python3 -B` so a
bytecode cache can never serve a previous mutation's module.

The live end-to-end needs the UI toolchain inside the worktree, so the tool links the primary's
`apps/ui/node_modules` into it first and removes that link last.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f024-r5-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

MEMO_REL = "apps/ui/src/components/timeline/scrubSnapshots.ts"
INDEX_REL = "apps/ui/src/components/timeline/timelineIndex.ts"
VIEW_REL = "apps/ui/src/components/timeline/timelineView.ts"
STATE_REL = "apps/ui/src/components/timeline/scrubState.ts"
FIXTURE_REL = "apps/ui/src/components/graph/brainPerfFixture.ts"
VITEST_FILES = [
    "apps/ui/src/components/graph/brainPerfFixture.test.ts",
]
# The live end-to-end: it runs a fake job and scrubs its ledger with the worktree's modules.
GUARD_REL = "tests/ui_server/test_timeline_scrub_live.py"

MUTATIONS = [
    {"id": "m1", "name": "a snapshot also holds the row at its boundary", "file": MEMO_REL,
     "from": "    for (let i = lowerBound(from); i < rows.length && rows[i].seq < to; i += 1) {\n",
     "to": "    for (let i = lowerBound(from); i < rows.length && rows[i].seq <= to; i += 1) {\n"},
    {"id": "m2", "name": "the index reads a position without its own row", "file": INDEX_REL,
     "from": "    if (index.seqs[mid] <= seq) lo = mid + 1;\n", "to": "    if (index.seqs[mid] < seq) lo = mid + 1;\n"},
    {"id": "m3", "name": "the handle sits at the start of its event's slot", "file": VIEW_REL,
     "from": "  return (p + (at + 1 - from) / (to - from)) / TIMELINE_PHASES.length;\n",
     "to": "  return (p + (at - from) / (to - from)) / TIMELINE_PHASES.length;\n"},
    {"id": "m4", "name": "End scrubs to the head instead of returning to LIVE", "file": STATE_REL,
     "from": '  if (key === "End") return { type: "go_live" };\n', "to": '  if (key === "End") return { type: "scrub_to", seq: 1e9 };\n'},
    {"id": "m5", "name": "the fixture's ledger loses its first row", "file": FIXTURE_REL,
     "from": "  return buildRowsAndSeeds(config.normalCount, config.bareCount, ROUNDS_PER_TASK);\n",
     "to": "  const built = buildRowsAndSeeds(config.normalCount, config.bareCount, ROUNDS_PER_TASK);\n"
           "  return { seeds: built.seeds, rows: built.rows.slice(1) };\n"},
]

LINK = "apps/ui/node_modules"


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
    link = worktree / LINK
    linked = not link.exists()
    if linked:
        link.symlink_to(PRIMARY_UI / "node_modules", target_is_directory=True)
    print(f"node_modules linked by this tool: {linked}")
    try:
        return run_all(worktree)
    finally:
        if linked:
            link.unlink()
        print(f"node_modules link removed: {linked and not link.exists()}")


def run_all(worktree):
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
