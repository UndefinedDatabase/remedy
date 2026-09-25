#!/usr/bin/env python3
"""Mutation tool for F024 T002: the scrubber's snapshot memo and its guard.

Given a worktree root, runs an unmutated control first and last, and between them applies
each mutation below (every FROM must occur exactly once in its file), runs the vitest files
of this round and the Python contract guard, restores the file BYTE-IDENTICAL, and reports
each runner's failed count and exit code. A mutation is caught when at least one runner
goes red. vitest runs from the PRIMARY `apps/ui` (a worktree has no node_modules) with a
scratch config under `.remedy-wt/f024-r2-mutscratch/`; pytest runs with `python3 -B` so a
bytecode cache can never serve a previous mutation's module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f024-r2-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

MEMO_REL = "apps/ui/src/components/timeline/scrubSnapshots.ts"
VITEST_FILES = [
    "apps/ui/src/components/timeline/scrubSnapshots.test.ts",
]
GUARD_REL = "tests/ui_contracts/test_scrub_snapshots.py"

MUTATIONS = [
    {"id": "m1", "name": "the boundary rounds down one seq early", "file": MEMO_REL,
     "from": "      const boundary = Math.floor((seq + 1) / every) * every;\n",
     "to": "      const boundary = Math.floor(seq / every) * every;\n"},
    {"id": "m2", "name": "a snapshot also holds the row at its boundary", "file": MEMO_REL,
     "from": "    for (let i = lowerBound(from); i < rows.length && rows[i].seq < to; i += 1) {\n",
     "to": "    for (let i = lowerBound(from); i < rows.length && rows[i].seq <= to; i += 1) {\n"},
    {"id": "m3", "name": "the ledger is kept in arrival order", "file": MEMO_REL,
     "from": "    rows = [...rows, ...fresh].sort((a, b) => a.seq - b.seq);\n", "to": "    rows = [...rows, ...fresh];\n"},
    {"id": "m4", "name": "a gap-filling row leaves the snapshots above it", "file": MEMO_REL,
     "from": "      if (boundary > lowest) snapshots.delete(boundary);\n", "to": ""},
    {"id": "m5", "name": "a row at the head drops every snapshot", "file": MEMO_REL,
     "from": "      if (boundary > lowest) snapshots.delete(boundary);\n",
     "to": "      if (boundary > 0) snapshots.delete(boundary);\n"},
    {"id": "m6", "name": "a reset keeps the old snapshots", "file": MEMO_REL,
     "from": "      snapshots.clear();\n", "to": ""},
    {"id": "m7", "name": "the cap drops the nearest snapshot", "file": MEMO_REL,
     "from": "        if (d > distance) {\n", "to": "        if (distance < 0 || d < distance) {\n"},
    {"id": "m8", "name": "a tie drops the higher snapshot", "file": MEMO_REL,
     "from": "        if (d > distance) {\n", "to": "        if (d >= distance) {\n"},
    {"id": "m9", "name": "the cap is never enforced", "file": MEMO_REL,
     "from": "    while (snapshots.size > cap) {\n", "to": "    while (snapshots.size > cap * 100) {\n"},
    {"id": "m10", "name": "a missing snapshot is always rebuilt from the seed", "file": MEMO_REL,
     "from": "    while (base > 0 && !snapshots.has(base)) base -= every;\n", "to": "    base = 0;\n"},
    {"id": "m11", "name": "the memo seeds with today's statuses", "file": MEMO_REL,
     "from": "  const seed = seedBrainModel(jobId, timelineSeedOf(tasks));\n",
     "to": "  const seed = seedBrainModel(jobId, tasks);\n  void timelineSeedOf;\n"},
    {"id": "m12", "name": "the spacing drifts from the spec", "file": MEMO_REL,
     "from": "export const SNAPSHOT_EVERY = 200;\n", "to": "export const SNAPSHOT_EVERY = 100;\n"},
    {"id": "m13", "name": "the memo reaches for the wall clock", "file": MEMO_REL,
     "from": "  let reductions = 0;\n", "to": "  let reductions = 0;\n  void Date.now();\n"},
    {"id": "m14", "name": "every position folds from the seed", "file": MEMO_REL,
     "from": "      return fold(snapshotAt(boundary, seq), boundary, seq + 1);\n",
     "to": "      return fold(seed, -1, seq + 1);\n"},
    {"id": "m15", "name": "a position also folds the row after it", "file": MEMO_REL,
     "from": "      return fold(snapshotAt(boundary, seq), boundary, seq + 1);\n",
     "to": "      return fold(snapshotAt(boundary, seq), boundary, seq + 2);\n"},
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
