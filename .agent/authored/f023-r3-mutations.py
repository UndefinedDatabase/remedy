#!/usr/bin/env python3
"""Mutation tool for F023 T002 prerequisite: the per-round facts route, its client door and their guards.

Given a worktree root, runs an unmutated control first and last, and between them applies
each mutation below (every FROM must occur exactly once in its file), runs the vitest files
of this round and the Python contract guard, restores the file BYTE-IDENTICAL, and reports
each runner's failed count and exit code. A mutation is caught when at least one runner
goes red. vitest runs from the PRIMARY `apps/ui` (a worktree has no node_modules) with a
scratch config under `.remedy-wt/f023-r3-mutscratch/`; pytest runs with `python3 -B` so a
bytecode cache can never serve a previous mutation's module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f023-r3-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

VIEW_REL = "packages/orchestration/run_rounds_view.py"
SERVER_REL = "packages/orchestration/ui_server.py"
DOOR_REL = "apps/ui/src/api/taskRunRounds.ts"
API_REL = "apps/ui/src/api/remedyApi.ts"
VITEST_FILES = [
    "apps/ui/src/api/taskRunRounds.test.ts",
]
GUARD_RELS = [
    "tests/ui_server/test_task_run_rounds.py",
    "tests/ui_contracts/test_task_run_rounds_door.py",
]

MUTATIONS = [
    {"id": "m1", "name": "an uppercase run id is accepted", "file": VIEW_REL,
     "from": '_RUN_ID_RE = re.compile(r"[0-9a-f]{8,32}")\n', "to": '_RUN_ID_RE = re.compile(r"[0-9a-fA-F]{8,32}")\n'},
    {"id": "m2", "name": "any non-empty run id becomes a path segment", "file": VIEW_REL,
     "from": "    if not isinstance(run_id, str) or not _RUN_ID_RE.fullmatch(run_id):\n",
     "to": "    if not isinstance(run_id, str) or not run_id:\n"},
    {"id": "m3", "name": "the builder's summary prose is served", "file": VIEW_REL,
     "from": '            "tokens_used": _count(builder.get("tokens_used")),\n',
     "to": '            "tokens_used": _count(builder.get("tokens_used")),\n            "summary": builder.get("summary"),\n'},
    {"id": "m4", "name": "a finish before the start yields a negative duration", "file": VIEW_REL,
     "from": "    return int(round(delta * 1000)) if delta >= 0 else None\n",
     "to": "    return int(round(delta * 1000))\n"},
    {"id": "m5", "name": "a boolean is counted as a number", "file": VIEW_REL,
     "from": "    if isinstance(value, bool) or not isinstance(value, int) or value < 0:\n",
     "to": "    if not isinstance(value, int) or value < 0:\n"},
    {"id": "m6", "name": "an unknown task falls through to the run lookup", "file": VIEW_REL,
     "from": "        envelope[\"reason\"] = REASON_UNKNOWN_TASK\n        return envelope\n",
     "to": "        envelope[\"reason\"] = REASON_UNKNOWN_TASK\n"},
    {"id": "m7", "name": "a truthy string reads as a parse retry", "file": VIEW_REL,
     "from": '            "parse_retried": reviewer.get("parse_retried") is True,\n',
     "to": '            "parse_retried": bool(reviewer.get("parse_retried")),\n'},
    {"id": "m8", "name": "an unparseable start time is served raw", "file": VIEW_REL,
     "from": '        "started_at": started.isoformat() if started else None,\n',
     "to": '        "started_at": raw.get("started_at"),\n'},
    {"id": "m9", "name": "the server routes the path under another name", "file": SERVER_REL,
     "from": '                and parts[4] == "task-runs" and parts[6] == "rounds"):\n',
     "to": '                and parts[4] == "task-runs" and parts[6] == "round"):\n'},
    {"id": "m10", "name": "the client accepts an envelope of another version", "file": DOOR_REL,
     "from": "  if (!env || env.version !== TASK_RUN_ROUNDS_VERSION || env.task_id !== taskId) return unreadable;\n",
     "to": "  if (!env || env.task_id !== taskId) return unreadable;\n"},
    {"id": "m11", "name": "the client keeps rounds of an unavailable envelope", "file": DOOR_REL,
     "from": "    rounds: env.available === true ? rounds : [],\n", "to": "    rounds,\n"},
    {"id": "m12", "name": "the client reads the builder's tokens from the wrong key", "file": DOOR_REL,
     "from": "tokensUsed: count(builder.tokens_used)", "to": "tokensUsed: count(builder.tokens)"},
    {"id": "m13", "name": "the task id is put in the path unencoded", "file": DOOR_REL,
     "from": "  const task = encodeURIComponent(request.taskId);\n", "to": "  const task = request.taskId;\n"},
    {"id": "m14", "name": "the door throws on a failed fetch", "file": API_REL,
     "from": "    return decodeTaskRunRounds(null, request.taskId);\n",
     "to": '    throw new Error("unreadable");\n'},
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
