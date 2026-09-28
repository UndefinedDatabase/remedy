#!/usr/bin/env python3
"""Mutation tool for F039 R2: the story's narration cards and R-1098's repair.

Given a worktree path, runs an unmutated control first and last, and between them applies
each mutation below (every FROM must occur exactly once in its file, or the mutation
prepends a line) to the worktree's own copy of the named file, runs the vitest goldens of
both `apps/ui/src/components/story/` test files and the six `tests/ui_contracts/` guards
this round touches or adds, restores the file BYTE-IDENTICAL, and reports each runner's
failed count and exit code. A mutation is caught when at least one runner goes red. Follows
`.agent/authored/f039-r1-mutations.py`'s route: vitest runs from the PRIMARY `apps/ui` (a
worktree has no node_modules) with a plain-object scratch config under
`.remedy-wt/f039-r2-mutscratch/`; the guards run with `python3 -B -m pytest` from the
worktree's own root, that root first on `PYTHONPATH`, so a bytecode cache can never serve a
previous mutation's module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f039-r2-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

STORY_NARRATION = "apps/ui/src/components/story/storyNarration.ts"
TEST_PHASE_MAPPING = "tests/ui_contracts/test_phase_mapping.py"

VITEST_FILES = [
    "apps/ui/src/components/story/storyChapters.test.ts",
    "apps/ui/src/components/story/storyNarration.test.ts",
]
GUARD_RELS = [
    "tests/ui_contracts/test_phase_mapping.py",
    "tests/ui_contracts/test_timeline_scrub_contract.py",
    "tests/ui_contracts/test_scrub_snapshots.py",
    "tests/ui_contracts/test_semantic_zoom_contract.py",
    "tests/ui_contracts/test_story_chapters.py",
    "tests/ui_contracts/test_story_narration.py",
]

BARE_IMPORT = 'import "../../api/unguarded";\n'

MUTATIONS = [
    # storyNarration.ts — DECISION F039 D3's own rules.
    {"id": "m1", "name": "the cost line reads the earliest tick at or before the seq instead of the latest",
     "file": STORY_NARRATION,
     "from": "tick.seq > latest.seq", "to": "tick.seq < latest.seq"},
    {"id": "m2", "name": "the cost line reads a tick one seq past the cluster", "file": STORY_NARRATION,
     "from": "storyCostLine(ticks, cluster.lastSeq)", "to": "storyCostLine(ticks, cluster.lastSeq + 1)"},
    {"id": "m3", "name": "an estimated figure loses its ~", "file": STORY_NARRATION,
     "from": '? "~" : ""', "to": '? "" : ""'},
    {"id": "m4", "name": "a token figure loses ' tokens'", "file": STORY_NARRATION,
     "from": '? " tokens" : ""', "to": '? "" : ""'},
    {"id": "m5", "name": "a tick with no figure gives a cost line", "file": STORY_NARRATION,
     "from": "  if (metric.display === NO_COST_DISPLAY) return null;\n", "to": ""},
    {"id": "m6", "name": "every row's outcome is read as a verdict, not only a review round's",
     "file": STORY_NARRATION,
     "from": 'if (source === undefined || source.kind !== "task_round_completed") return null;\n',
     "to": "if (source === undefined) return null;\n"},
    {"id": "m7", "name": "an actor is named when two ownership entries match", "file": STORY_NARRATION,
     "from": "if (matchingEntries.length !== 1) return null;\n",
     "to": "if (matchingEntries.length < 1) return null;\n"},
    {"id": "m8", "name": "an unreadable ownership view still names an actor", "file": STORY_NARRATION,
     "from": 'if (ownership === null || ownership.error !== "") return null;\n',
     "to": "if (ownership === null) return null;\n"},
    {"id": "m9", "name": "a decision's actor ignores its task", "file": STORY_NARRATION,
     "from": 'const scoped = action === "decision_answered";\n', "to": "const scoped = false;\n"},
    {"id": "m10", "name": "cardAt shows a card of another chapter", "file": STORY_NARRATION,
     "from": "if (card.chapter === chapter && card.firstSeq <= position) found = card;\n",
     "to": "if (card.firstSeq <= position) found = card;\n"},
    {"id": "m11", "name": "cardAt shows a card before its first key event", "file": STORY_NARRATION,
     "from": "if (card.chapter === chapter && card.firstSeq <= position) found = card;\n",
     "to": "if (card.chapter === chapter) found = card;\n"},
    {"id": "m12", "name": "chapterAt counts a chapter's endSeq as inside it", "file": STORY_NARRATION,
     "from": "chapter.startSeq <= position && position < chapter.endSeq",
     "to": "chapter.startSeq <= position && position <= chapter.endSeq"},
    {"id": "m13", "name": "STORY_VERDICT_LINES gains a skipped line after its blocked line",
     "file": STORY_NARRATION,
     "from": '  blocked: "Verdict: blocked",\n',
     "to": '  blocked: "Verdict: blocked",\n  skipped: "Verdict: skipped",\n'},
    {"id": "m14", "name": "a statement void \"no cost here\"; is added inside storyCostLine",
     "file": STORY_NARRATION,
     "from": "export function storyCostLine(ticks: readonly StoryTick[], seq: number): string | null {\n",
     "to": ("export function storyCostLine(ticks: readonly StoryTick[], seq: number): string | null {\n"
            '  void "no cost here";\n')},
    # R-1098 — a bare import of an unguarded specifier, prepended to each module a guard reads.
    {"id": "m15", "name": "phaseMapping.ts gains an unguarded bare import",
     "file": "apps/ui/src/components/timeline/phaseMapping.ts", "prepend": BARE_IMPORT},
    {"id": "m16", "name": "scrubState.ts gains an unguarded bare import",
     "file": "apps/ui/src/components/timeline/scrubState.ts", "prepend": BARE_IMPORT},
    {"id": "m17", "name": "timelineIndex.ts gains an unguarded bare import",
     "file": "apps/ui/src/components/timeline/timelineIndex.ts", "prepend": BARE_IMPORT},
    {"id": "m18", "name": "timelineView.ts gains an unguarded bare import",
     "file": "apps/ui/src/components/timeline/timelineView.ts", "prepend": BARE_IMPORT},
    {"id": "m19", "name": "scrubSnapshots.ts gains an unguarded bare import",
     "file": "apps/ui/src/components/timeline/scrubSnapshots.ts", "prepend": BARE_IMPORT},
    {"id": "m20", "name": "semanticZoom.ts gains an unguarded bare import",
     "file": "apps/ui/src/components/graph/semanticZoom.ts", "prepend": BARE_IMPORT},
    {"id": "m21", "name": "zoomWheel.ts gains an unguarded bare import",
     "file": "apps/ui/src/components/graph/zoomWheel.ts", "prepend": BARE_IMPORT},
    {"id": "m22", "name": "storyChapters.ts gains an unguarded bare import",
     "file": "apps/ui/src/components/story/storyChapters.ts", "prepend": BARE_IMPORT},
    {"id": "m23", "name": "TS_IMPORT_RE reverts to the blind from-only pattern", "file": TEST_PHASE_MAPPING,
     "from": 'TS_IMPORT_RE = re.compile(r\'^(?:import|export)\\s+(?:[^;]*?\\s+from\\s+)?"([^"]+)";$\', re.MULTILINE)\n',
     "to": 'TS_IMPORT_RE = re.compile(r\'^import [^;]*from "([^"]+)";$\', re.MULTILINE)\n'},
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
        if "prepend" in mut:
            mutated = mut["prepend"] + text
        else:
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
