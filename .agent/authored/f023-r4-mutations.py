#!/usr/bin/env python3
"""Mutation tool for F023 T002 second half: the L2 run detail's words, its popover and their wiring guard.

Given a worktree root, runs an unmutated control first and last, and between them applies
each mutation below (every FROM must occur exactly once in its file), runs the vitest files
of this round and the Python contract guard, restores the file BYTE-IDENTICAL, and reports
each runner's failed count and exit code. A mutation is caught when at least one runner
goes red. vitest runs from the PRIMARY `apps/ui` (a worktree has no node_modules) with a
scratch config under `.remedy-wt/f023-r4-mutscratch/`; pytest runs with `python3 -B` so a
bytecode cache can never serve a previous mutation's module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f023-r4-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

MODEL_REL = "apps/ui/src/components/graph/runDetailModel.ts"
POPOVER_REL = "apps/ui/src/components/graph/RunDetailPopover.tsx"
STAGE_REL = "apps/ui/src/components/graph/BrainGraphStage.tsx"
CANVAS_REL = "apps/ui/src/components/graph/ForceBrainGraph.tsx"
SHELL_REL = "apps/ui/src/components/shell/RemedyShell.tsx"
VITEST_FILES = [
    "apps/ui/src/components/graph/runDetailModel.test.ts",
]
GUARD_RELS = [
    "tests/ui_contracts/test_run_detail_wiring.py",
]

MUTATIONS = [
    {"id": "m1", "name": "a round the ledger logged without a review is not counted", "file": MODEL_REL,
     "from": '  const round = own.filter((r) => r.kind === "task_round_completed" && r.seq > startSeq && r.seq <= node.seq).length;\n',
     "to": '  const round = own.filter((r) => r.kind === "task_round_completed" && r.outcome !== "no_review" && r.seq > startSeq && r.seq <= node.seq).length;\n'},
    {"id": "m2", "name": "an earlier run is taken for the latest", "file": MODEL_REL,
     "from": "  const latest = startSeq !== null && startSeq === starts[starts.length - 1];\n",
     "to": "  const latest = startSeq !== null;\n"},
    {"id": "m3", "name": "the reviewer's tokens are filled from the builder's", "file": MODEL_REL,
     "from": "    tokens: { missing: RUN_FACT_REVIEWER_TOKENS },\n",
     "to": "    tokens: { value: formatTokens(round.builder?.tokensUsed ?? 0) },\n"},
    {"id": "m4", "name": "a running run is described from the report", "file": MODEL_REL,
     "from": "  const why = node.state === \"in_progress\" ? RUN_FACT_RUNNING\n    : !place.latest ? RUN_FACT_EARLIER\n",
     "to": "  const why = !place.latest ? RUN_FACT_EARLIER\n"},
    {"id": "m5", "name": "needs repair reads as failed", "file": MODEL_REL,
     "from": '  needs_repair: "Needs repair",\n', "to": '  needs_repair: "Failed",\n'},
    {"id": "m6", "name": "a test run claims a timing", "file": MODEL_REL,
     "from": "    return { ...base, tokens: { value: RUN_FACT_TEST_TOKENS }, duration: { missing: RUN_FACT_TEST_TIMING }, retries: { value: \"None\" } };\n",
     "to": "    return { ...base, tokens: { value: RUN_FACT_TEST_TOKENS }, duration: { value: \"0 ms\" }, retries: { value: \"None\" } };\n"},
    {"id": "m7", "name": "Why opens a reviewer prompt of another round", "file": MODEL_REL,
     "from": '    return own.find((p) => p.role === "reviewer" && p.round === round)?.id ?? null;\n',
     "to": '    return own.find((p) => p.role === "reviewer")?.id ?? null;\n'},
    {"id": "m8", "name": "a long duration is written in seconds only", "file": MODEL_REL,
     "from": "  return `${Math.floor(whole / 60)} min ${whole % 60} s`;\n", "to": "  return `${whole} s`;\n"},
    {"id": "m9", "name": "a task with no run reads as an unreadable report", "file": MODEL_REL,
     "from": '  if (rounds.reason === "no_run_recorded") return RUN_FACT_NO_RUN;\n', "to": ""},
    {"id": "m10", "name": "the detail shows a report read for another task", "file": POPOVER_REL,
     "from": "  const rounds = loaded !== null && loaded.taskId === taskId ? loaded : null;\n",
     "to": "  const rounds = loaded;\n"},
    {"id": "m11", "name": "Rerun is enabled", "file": POPOVER_REL,
     "from": "className={styles.action} disabled title={RERUN_NOT_YET}",
     "to": "className={styles.action} title={RERUN_NOT_YET}"},
    {"id": "m12", "name": "the detail becomes a dialog Escape skips", "file": POPOVER_REL,
     "from": '<aside className={styles.popover} aria-label="Run detail" data-ui="run-detail">',
     "to": '<aside className={styles.popover} role="dialog" aria-label="Run detail" data-ui="run-detail">'},
    {"id": "m13", "name": "the stage looks the run up in the filtered view", "file": STAGE_REL,
     "from": "  const focusedRun = zoom.state.level >= 2 ? model.nodes.find(",
     "to": "  const focusedRun = zoom.state.level >= 2 ? visible.nodes.find("},
    {"id": "m14", "name": "a run click opens its task's popover too", "file": CANVAS_REL,
     "from": "    if (isZoomRunKind(n.kind)) return;\n", "to": ""},
    {"id": "m15", "name": "the shell hands the stage no token", "file": SHELL_REL,
     "from": "serverToken={serverToken} onOpenDiff={setOpenDiffTaskId}",
     "to": 'serverToken="" onOpenDiff={setOpenDiffTaskId}'},
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
