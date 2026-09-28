#!/usr/bin/env python3
"""Mutation tool for F039 R7: R-1102's fix (a task's own id kept raw in the
dashboard mapping) and T003's data half (the story payload and its reader).

Given a worktree path, runs an unmutated control first and last, and between
them applies each mutation below (every FROM must occur exactly once in its
file) to the worktree's own copy of the named file, runs the vitest goldens of
`storyExport.test.ts`, `brainView.test.ts` and `remedyApi.test.ts` and the
pytest guard `tests/orchestration/test_story_export.py`, restores the file
BYTE-IDENTICAL, and reports each runner's failed count and exit code. A
mutation is caught when at least one runner goes red. Follows
`.agent/authored/f039-r4-mutations.py`'s route: vitest runs from the PRIMARY
`apps/ui` (a worktree has no node_modules) with a plain-object scratch config
under `.remedy-wt/f039-r7-mutscratch/`; the guard runs with
`python3 -B -m pytest` from the worktree's own root, that root first on
`PYTHONPATH`, so a bytecode cache can never serve a previous mutation's
module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f039-r7-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

REMEDY_API = "apps/ui/src/api/remedyApi.ts"
STORY_EXPORT_TS = "apps/ui/src/components/story/storyExport.ts"
STORY_EXPORT_PY = "packages/orchestration/story_export.py"

VITEST_FILES = [
    "apps/ui/src/components/story/storyExport.test.ts",
    "apps/ui/src/components/graph/brainView.test.ts",
    "apps/ui/src/api/remedyApi.test.ts",
]
GUARD_RELS = [
    "tests/orchestration/test_story_export.py",
]

MUTATIONS = [
    # remedyApi.ts — R-1102's own proof.
    {"id": "m1", "name": "the task's id goes through scrubUiText again", "file": REMEDY_API,
     "from": "      id: t.id ? String(t.id) : `task-${idx}`,",
     "to": "      id: scrubUiText(t.id || `task-${idx}`, `task-${idx}`),"},
    # story_export.py — S2's own rules.
    {"id": "m2", "name": "the frames' seqs are counted from 1", "file": STORY_EXPORT_PY,
     "from": "            for seq, event in enumerate(_load_events(job))\n",
     "to": "            for seq, event in enumerate(_load_events(job), start=1)\n"},
    {"id": "m3", "name": "each frame carries the raw event instead of _safe_event_summary's envelope",
     "file": STORY_EXPORT_PY,
     "from": '            {"seq": seq, "event": _safe_event_summary(seq, event)}\n',
     "to": '            {"seq": seq, "event": event}\n'},
    {"id": "m4", "name": "STORY_DASHBOARD_SECTIONS gains metrics", "file": STORY_EXPORT_PY,
     "from": 'STORY_DASHBOARD_SECTIONS = ("tasks", "live", "story")',
     "to": 'STORY_DASHBOARD_SECTIONS = ("tasks", "live", "story", "metrics")'},
    # storyExport.ts — S3's own rules.
    {"id": "m5", "name": "decodeStoryExport no longer refuses another schema by name",
     "file": STORY_EXPORT_TS,
     "from": ('  const schema = raw["schema"];\n'
              '  if (typeof schema === "string" && schema !== STORY_EXPORT_SCHEMA) {\n'
              '    return { ok: false, message: storyExportVersionLine(schema) };\n'
              '  }\n'),
     "to": '  const schema = raw["schema"];\n'},
    {"id": "m6", "name": "a frame is taken as a row without feedRowOf", "file": STORY_EXPORT_TS,
     "from": "      rows: frames.map((frame) => feedRowOf(frame, 0)),",
     "to": "      rows: frames as unknown as FeedRow[],"},
    {"id": "m7", "name": "the ownership view is taken without decodeOwnershipView", "file": STORY_EXPORT_TS,
     "from": '      ownership: decodeOwnershipView(raw["ownership"]),',
     "to": '      ownership: raw["ownership"] as unknown as OwnershipView | null,'},
    {"id": "m8", "name": "the TypeScript constant reads remedy.story.v2", "file": STORY_EXPORT_TS,
     "from": 'export const STORY_EXPORT_SCHEMA = "remedy.story.v1";',
     "to": 'export const STORY_EXPORT_SCHEMA = "remedy.story.v2";'},
    {"id": "m9", "name": "a frame with no number seq is accepted", "file": STORY_EXPORT_TS,
     "from": ('function isFrame(value: unknown): value is { seq: number; event: unknown } {\n'
              '  return isPlainObject(value) && typeof value["seq"] === "number";\n'
              '}'),
     "to": ('function isFrame(value: unknown): value is { seq: number; event: unknown } {\n'
            '  return isPlainObject(value);\n'
            '}')},
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
