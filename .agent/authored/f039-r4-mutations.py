#!/usr/bin/env python3
"""Mutation tool for F039 R4: the story's data path — a budget tick's figures on
its own feed row, the dashboard's `story` section (both language halves) and the
pure view that assembles a job's story.

Given a worktree path, runs an unmutated control first and last, and between them
applies each mutation below (every FROM must occur exactly once in its file) to the
worktree's own copy of the named file, runs the vitest goldens of `storyView.test.ts`,
`storyNarration.test.ts`, `feedRow.test.ts` and `remedyApi.test.ts` and the three
`pytest` guards this round touches, restores the file BYTE-IDENTICAL, and reports
each runner's failed count and exit code. A mutation is caught when at least one
runner goes red. Follows `.agent/authored/f039-r3-mutations.py`'s route: vitest runs
from the PRIMARY `apps/ui` (a worktree has no node_modules) with a plain-object
scratch config under `.remedy-wt/f039-r4-mutscratch/`; the guards run with
`python3 -B -m pytest` from the worktree's own root, that root first on `PYTHONPATH`,
so a bytecode cache can never serve a previous mutation's module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f039-r4-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

FEED_ROW = "apps/ui/src/api/feedRow.ts"
REMEDY_API = "apps/ui/src/api/remedyApi.ts"
STORY_VIEW = "apps/ui/src/components/story/storyView.ts"
CONFIG_PY = "packages/orchestration/config.py"
UI_SERVER_PY = "packages/orchestration/ui_server.py"

VITEST_FILES = [
    "apps/ui/src/components/story/storyView.test.ts",
    "apps/ui/src/components/story/storyNarration.test.ts",
    "apps/ui/src/api/feedRow.test.ts",
    "apps/ui/src/api/remedyApi.test.ts",
]
GUARD_RELS = [
    "tests/ui_server/test_story_section.py",
    "tests/ui_contracts/test_story_view.py",
    "tests/docs/test_environment_guide.py",
]

MUTATIONS = [
    # feedRow.ts — S1's own rule.
    {"id": "m1", "name": "feedRowOf never sets budget", "file": FEED_ROW,
     "from": "    ...(budget !== null ? { budget } : {}),\n", "to": ""},
    {"id": "m2", "name": "feedRowOf sets budget on every row, undefined where there is no tick",
     "file": FEED_ROW,
     "from": "    ...(budget !== null ? { budget } : {}),", "to": "    budget,"},
    # storyView.ts — S4's own rules.
    {"id": "m3", "name": "storyTicksOf reads the rows in the order given, not orderedLedger's",
     "file": STORY_VIEW,
     "from": "  for (const row of orderedLedger(rows)) {", "to": "  for (const row of rows) {"},
    {"id": "m4", "name": "storyTicksOf accepts an array budget", "file": STORY_VIEW,
     "from": 'if (typeof budget === "object" && budget !== null && !Array.isArray(budget)) {',
     "to": 'if (typeof budget === "object" && budget !== null) {'},
    {"id": "m5", "name": "buildStoryView hands the cards no tick", "file": STORY_VIEW,
     "from": "cards: buildNarrationCards(chapters, rows, storyTicksOf(rows), ownership),",
     "to": "cards: buildNarrationCards(chapters, rows, [], ownership),"},
    {"id": "m6", "name": "buildStoryView decodes null instead of its pacing argument", "file": STORY_VIEW,
     "from": "pacing: storyPacingOf(pacing),", "to": "pacing: storyPacingOf(null),"},
    {"id": "m7", "name": "the view's seqs are the rows' seqs in the order given", "file": STORY_VIEW,
     "from": "seqs: orderedLedger(rows).map((row) => row.seq),",
     "to": "seqs: rows.map((row) => row.seq),"},
    {"id": "m12", "name": "storyView.ts gains an unguarded import after its imports", "file": STORY_VIEW,
     "from": 'import { buildNarrationCards, type NarrationCard, type StoryTick } from "./storyNarration";',
     "to": ('import { buildNarrationCards, type NarrationCard, type StoryTick } from "./storyNarration";\n'
            'import "../../api/unguarded";')},
    # remedyApi.ts — S3's browser half.
    {"id": "m8", "name": "normalizeDashboardPayload carries story: null always", "file": REMEDY_API,
     "from": "    story: dashboard.story ?? null,", "to": "    story: null,"},
    # ui_server.py — S3's Python half.
    {"id": "m9", "name": "_build_story_section's step_ms reads story.chapter_pause_ms",
     "file": UI_SERVER_PY,
     "from": '"step_ms": config.get("story.step_ms"),',
     "to": '"step_ms": config.get("story.chapter_pause_ms"),'},
    {"id": "m11", "name": "_build_dashboard omits the story entry", "file": UI_SERVER_PY,
     "from": '        "story": _build_story_section(),\n', "to": ""},
    # config.py — S2's own registration.
    {"id": "m10", "name": "story.step_ms's default is 400", "file": CONFIG_PY,
     "from": "        default=420,", "to": "        default=400,"},
]


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
    env = dict(os.environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(worktree) if not existing else f"{worktree}{os.pathsep}{existing}"
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *GUARD_RELS],
        cwd=str(worktree), capture_output=True, text=True, timeout=180, env=env)
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
        count = text.count(mut["from"])
        if count != 1:
            print(f"{mut['id']}: SKIPPED, FROM occurrences {count}")
            all_ok = False
            continue
        mutated = text.replace(mut["from"], mut["to"], 1)
        target.write_bytes(mutated.encode("utf-8"))
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
