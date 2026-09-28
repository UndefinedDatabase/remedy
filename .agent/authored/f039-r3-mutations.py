#!/usr/bin/env python3
"""Mutation tool for F039 R3: the story's autoplay pacing and R-1099's repair.

Given a worktree path, runs an unmutated control first and last, and between them applies
each mutation below (every FROM must occur exactly once in its file) to the worktree's own
copy of the named file, runs the vitest goldens of the three `apps/ui/src/components/story/`
test files and the two `tests/ui_contracts/` guards this round touches, restores the file
BYTE-IDENTICAL, and reports each runner's failed count and exit code. A mutation is caught
when at least one runner goes red. Follows `.agent/authored/f039-r2-mutations.py`'s route:
vitest runs from the PRIMARY `apps/ui` (a worktree has no node_modules) with a plain-object
scratch config under `.remedy-wt/f039-r3-mutscratch/`; the guards run with
`python3 -B -m pytest` from the worktree's own root, that root first on `PYTHONPATH`, so a
bytecode cache can never serve a previous mutation's module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f039-r3-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

STORY_AUTOPLAY = "apps/ui/src/components/story/storyAutoplay.ts"
STORY_NARRATION = "apps/ui/src/components/story/storyNarration.ts"

VITEST_FILES = [
    "apps/ui/src/components/story/storyChapters.test.ts",
    "apps/ui/src/components/story/storyNarration.test.ts",
    "apps/ui/src/components/story/storyAutoplay.test.ts",
]
GUARD_RELS = [
    "tests/ui_contracts/test_story_autoplay.py",
    "tests/ui_contracts/test_story_narration.py",
]

MUTATIONS = [
    # storyAutoplay.ts — DECISION F039 D4's own rules.
    {"id": "m1", "name": "no chapter pause is ever added", "file": STORY_AUTOPLAY,
     "from": "delayMs: pacing.stepMs + (entersNewChapter ? pacing.chapterPauseMs : 0),",
     "to": "delayMs: pacing.stepMs,"},
    {"id": "m2", "name": "every step adds a chapter pause", "file": STORY_AUTOPLAY,
     "from": "const entersNewChapter = chapterAt(chapters, next) !== here;",
     "to": "const entersNewChapter = true;"},
    {"id": "m3", "name": "entering the first chapter from -1 adds no pause", "file": STORY_AUTOPLAY,
     "from": "const entersNewChapter = chapterAt(chapters, next) !== here;",
     "to": "const entersNewChapter = position === -1 ? false : chapterAt(chapters, next) !== here;"},
    {"id": "m4", "name": "reduced motion is ignored", "file": STORY_AUTOPLAY,
     "from": "if (reducedMotion) {", "to": "if (false) {"},
    {"id": "m5", "name": "reduced motion never steps to the last seq", "file": STORY_AUTOPLAY,
     "from": "if (lastSeq !== undefined && lastSeq > position) {", "to": "if (false) {"},
    {"id": "m6", "name": "a wait of exactly 50 is refused", "file": STORY_AUTOPLAY,
     "from": "value >= STORY_PACING_MIN_MS &&", "to": "value > STORY_PACING_MIN_MS &&"},
    {"id": "m7", "name": "a fractional wait is accepted", "file": STORY_AUTOPLAY,
     "from": "Number.isInteger(value) &&\n", "to": ""},
    {"id": "m8", "name": "the payload is read by stepMs rather than step_ms", "file": STORY_AUTOPLAY,
     "from": 'clampedField(raw, "step_ms", STORY_STEP_MS),',
     "to": 'clampedField(raw, "stepMs", STORY_STEP_MS),'},
    {"id": "m9", "name": "STORY_STEP_MS is 400", "file": STORY_AUTOPLAY,
     "from": "export const STORY_STEP_MS = 420;", "to": "export const STORY_STEP_MS = 400;"},
    {"id": "m10", "name": "a setTimeout statement is added inside autoplayTotalMs", "file": STORY_AUTOPLAY,
     "from": "  let total = 0;\n  let position = -1;\n",
     "to": "  let total = 0;\n  let position = -1;\n  setTimeout(() => undefined, 0);\n"},
    # storyNarration.ts — R-1099's own proof.
    {"id": "m11", "name": "the actor check of the count of matching events is deleted (R-1099)",
     "file": STORY_NARRATION,
     "from": "  if (matchingEvents.length !== 1) return null;\n", "to": ""},
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
