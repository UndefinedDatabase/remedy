#!/usr/bin/env python3
"""Mutation tool for F024 T001: the phase mapping, its sub-glyph extraction and their guard.

Given a worktree root, runs an unmutated control first and last, and between them applies
each mutation below (every FROM must occur exactly once in its file), runs the vitest files
of this round and the Python contract guard, restores the file BYTE-IDENTICAL, and reports
each runner's failed count and exit code. A mutation is caught when at least one runner
goes red. vitest runs from the PRIMARY `apps/ui` (a worktree has no node_modules) with a
scratch config under `.remedy-wt/f024-r1-mutscratch/`; pytest runs with `python3 -B` so a
bytecode cache can never serve a previous mutation's module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f024-r1-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

MAPPING_REL = "apps/ui/src/components/timeline/phaseMapping.ts"
BAR_REL = "apps/ui/src/components/timeline/PhaseTimeline.tsx"
VITEST_FILES = [
    "apps/ui/src/components/timeline/phaseMapping.test.ts",
]
GUARD_REL = "tests/ui_contracts/test_phase_mapping.py"

MUTATIONS = [
    {"id": "m1", "name": "planning_started marks Build", "file": MAPPING_REL,
     "from": '  planning_started: "planning",\n', "to": '  planning_started: "build",\n'},
    {"id": "m2", "name": "a round with no reviewer marks Review", "file": MAPPING_REL,
     "from": '  if (row.kind === "task_round_completed" && !has(REVIEW_OUTCOME_STATE_TABLE, row.outcome)) return null;\n',
     "to": ""},
    {"id": "m3", "name": "a skipped phase gets no start", "file": MAPPING_REL,
     "from": "    for (let p = reached + 1; p <= index; p += 1) starts[p] = row.seq;\n",
     "to": "    if (index > reached) starts[index] = row.seq;\n"},
    {"id": "m4", "name": "Finalized is sticky", "file": MAPPING_REL,
     "from": "    if (!allPassed) passSince = null;\n    else if (passSince === null) passSince = row.seq;\n",
     "to": "    if (allPassed && passSince === null) passSince = row.seq;\n"},
    {"id": "m5", "name": "the seed keeps today's statuses", "file": MAPPING_REL,
     "from": '  return tasks.map((task) => ({ ...task, status: "pending" }));\n',
     "to": "  return tasks.map((task) => ({ ...task }));\n"},
    {"id": "m6", "name": "Finalized ignores a later marker", "file": MAPPING_REL,
     "from": "    const finalizedAt = Math.max(passSince, starts[reached] as number);\n",
     "to": "    const finalizedAt = passSince;\n"},
    {"id": "m7", "name": "a pass heals another task's failure", "file": MAPPING_REL,
     "from": '    if (row.outcome === "pass" && failedReview.has(row.taskId)) {\n',
     "to": '    if (row.outcome === "pass" && failedReview.size > 0) {\n'},
    {"id": "m8", "name": "one failure heals twice", "file": MAPPING_REL,
     "from": "      failedReview.delete(row.taskId);\n", "to": ""},
    {"id": "m9", "name": "a repeated seq keeps the last row", "file": MAPPING_REL,
     "from": "    if (!bySeq.has(row.seq)) bySeq.set(row.seq, row);\n", "to": "    bySeq.set(row.seq, row);\n"},
    {"id": "m10", "name": "a prototype-named kind resolves as a marker", "file": MAPPING_REL,
     "from": "  if (!has(PHASE_MARKER_TABLE, row.kind)) return null;\n",
     "to": "  if (!(row.kind in PHASE_MARKER_TABLE)) return null;\n"},
    {"id": "m11", "name": "the hover shows the raw kind", "file": MAPPING_REL,
     "from": "      line: humanizeStreamEvent(row.kind).line,\n", "to": "      line: row.kind,\n"},
    {"id": "m12", "name": "the table names a kind nothing writes", "file": MAPPING_REL,
     "from": '  builder_completed: "build",\n', "to": '  builder_completed: "build",\n  builder_finished: "build",\n'},
    {"id": "m13", "name": "a kind marks Job", "file": MAPPING_REL,
     "from": '  planning_started: "planning",\n', "to": '  job_created: "job",\n  planning_started: "planning",\n'},
    {"id": "m14", "name": "the mapping reaches for the wall clock", "file": MAPPING_REL,
     "from": "  let passSince: number | null = null;\n",
     "to": "  let passSince: number | null = null;\n  void Date.now();\n"},
    {"id": "m15", "name": "the bar's phase order drifts from the mapping", "file": BAR_REL,
     "from": '  "build",\n  "test",\n  "review",\n', "to": '  "build",\n  "review",\n  "test",\n'},
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
