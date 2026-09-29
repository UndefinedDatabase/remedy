#!/usr/bin/env python3
"""Mutation tool for F039 T001: the story's chapters, their clusters and their guard.

Given a worktree path, runs an unmutated control first and last, and between them applies each
mutation below (every FROM must occur exactly once in its file) to the worktree's own copy of
`storyChapters.ts`, runs the vitest goldens of this round and the Python contract guard, restores
the file BYTE-IDENTICAL, and reports each runner's failed count and exit code. A mutation is
caught when at least one runner goes red. Follows `.agent/authored/f024-r1-mutations.py`'s route:
vitest runs from the PRIMARY `apps/ui` (a worktree has no node_modules) with a plain-object
scratch config under `.remedy-wt/f039-r1-mutscratch/`; the guard runs with `python3 -B -m pytest`
from the worktree's own root, that root first on `PYTHONPATH`, so a bytecode cache can never serve
a previous mutation's module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f039-r1-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

MODULE_REL = "apps/ui/src/components/story/storyChapters.ts"
VITEST_FILES = [
    "apps/ui/src/components/story/storyChapters.test.ts",
]
GUARD_REL = "tests/ui_contracts/test_story_chapters.py"

MUTATIONS = [
    {"id": "m1", "name": "two key events exactly two seqs apart fall into separate clusters", "file": MODULE_REL,
     "from": "event.seq - previous.seq > STORY_CLUSTER_SEQ_GAP) {\n",
     "to": "event.seq - previous.seq >= STORY_CLUSTER_SEQ_GAP) {\n"},
    {"id": "m2", "name": "a phase of exactly six key events splits", "file": MODULE_REL,
     "from": "const parts = Math.max(1, Math.ceil(phaseEvents.length / STORY_CHAPTER_KEY_EVENT_LIMIT));\n",
     "to": "const parts = Math.max(1, Math.ceil((phaseEvents.length + 1) / STORY_CHAPTER_KEY_EVENT_LIMIT));\n"},
    {"id": "m3", "name": "a phase with a zero span gives a chapter", "file": MODULE_REL,
     "from": "if (start >= end) continue;\n", "to": "if (start > end) continue;\n"},
    {"id": "m4", "name": "a later part begins at its phase's start", "file": MODULE_REL,
     "from": "const startSeq = part === 1 ? start : partEvents[0].seq;\n",
     "to": "const startSeq = start;\n"},
    {"id": "m5", "name": "an earlier part ends at its phase's end", "file": MODULE_REL,
     "from": "const endSeq = part === parts ? end : phaseEvents[partStartIndex + STORY_CHAPTER_KEY_EVENT_LIMIT].seq;\n",
     "to": "const endSeq = end;\n"},
    {"id": "m6", "name": "the last chapter ends at the ledger's last seq instead of one past it", "file": MODULE_REL,
     "from": "const end = span.endSeq === null ? lastSeq + 1 : span.endSeq;\n",
     "to": "const end = span.endSeq === null ? lastSeq : span.endSeq;\n"},
    {"id": "m7", "name": "a split phase's titles lose their part numbers", "file": MODULE_REL,
     "from": "title: storyChapterTitle(phase, part, parts),\n",
     "to": "title: storyChapterTitle(phase, part, 1),\n"},
    {"id": "m8", "name": "heals are dropped from the key events", "file": MODULE_REL,
     "from": "const keyEvents = extractSubGlyphs(rows);\n",
     "to": 'const keyEvents = extractSubGlyphs(rows).filter((event) => event.glyph !== "heal");\n'},
    {"id": "m9", "name": "clusters are read over the whole phase instead of inside a part", "file": MODULE_REL,
     "from": "clusters: clusterKeyEvents(partEvents),\n",
     "to": "clusters: clusterKeyEvents(phaseEvents),\n"},
    {"id": "m10", "name": "Finalized's title reads `The review`", "file": MODULE_REL,
     "from": '  finalized: "The finish",\n', "to": '  finalized: "The review",\n'},
    {"id": "m11", "name": "the module reads the clock", "file": MODULE_REL,
     "from": "  const reading = readPhases(jobId, tasks, rows);\n",
     "to": "  const reading = readPhases(jobId, tasks, rows);\n  void Date.now();\n"},
    {"id": "m12", "name": "the title table's test and review lines swap places", "file": MODULE_REL,
     "from": '  test: "The tests",\n  review: "The review",\n',
     "to": '  review: "The review",\n  test: "The tests",\n'},
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
    env = dict(os.environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(worktree) if not existing else f"{worktree}{os.pathsep}{existing}"
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", GUARD_REL],
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
