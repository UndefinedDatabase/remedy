#!/usr/bin/env python3
"""Mutation tool for F039 R8: the story player's second build (DECISION F039 D8),
the page it is inlined into, the export command, and the reader that decodes the
page's own embedded story.

Given a worktree path, runs an unmutated control first and last, and between them
applies each mutation below (every FROM must occur exactly once in its file) to
the worktree's own copy of the named file, runs vitest over the worktree's
`storyExport.test.ts` and pytest over the worktree's
`tests/ui_contracts/test_story_player_contract.py`,
`tests/orchestration/test_story_export.py` and `tests/cli/test_job_story.py`,
restores the file BYTE-IDENTICAL, and reports each runner's failed count and exit
code. A mutation is caught when at least one runner goes red. Follows
`.agent/authored/f039-r7-mutations.py`'s route: vitest runs from the PRIMARY
`apps/ui` (a worktree has no node_modules) with a plain-object scratch config
under `.remedy-wt/f039-r8-mutscratch/`; the guard runs with `python3 -B -m
pytest` from the worktree's own root, that root first on `PYTHONPATH`, so a
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

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f039-r8-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

STORY_EXPORT_PY = "packages/orchestration/story_export.py"
JOB_STORY_CMD = "apps/cli/commands/job_story_cmd.py"
STORY_EXPORT_TS = "apps/ui/src/components/story/storyExport.ts"
STORY_PANEL_TSX = "apps/ui/src/components/story/StoryPanel.tsx"
VITE_CONFIG = "apps/ui/vite.config.ts"

VITEST_FILES = [
    "apps/ui/src/components/story/storyExport.test.ts",
]
GUARD_RELS = [
    "tests/ui_contracts/test_story_player_contract.py",
    "tests/orchestration/test_story_export.py",
    "tests/cli/test_job_story.py",
]

MUTATIONS = [
    {"id": "m1", "name": "render_story_html no longer writes < as \\u003c", "file": STORY_EXPORT_PY,
     "from": '.replace("<", "\\\\u003c")',
     "to": ""},
    {"id": "m2", "name": "the budget refuses at exactly its size (> becomes >=)", "file": STORY_EXPORT_PY,
     "from": "if len(data) > max_bytes:",
     "to": "if len(data) >= max_bytes:"},
    {"id": "m3", "name": "read_story_player no longer refuses a closing script tag", "file": STORY_EXPORT_PY,
     "from": 'if "</script" in script.lower():',
     "to": 'if False and "</script" in script.lower():'},
    {"id": "m4", "name": "the page carries no content security policy", "file": STORY_EXPORT_PY,
     "from": (
         '        \'<meta http-equiv="Content-Security-Policy" content="default-src \\\'none\\\'; \'\n'
         '        "script-src \'unsafe-inline\'; style-src \'unsafe-inline\'; img-src data:\\">\\n"\n'
     ),
     "to": ""},
    {"id": "m5", "name": "the command answers a missing player at exit 1", "file": JOB_STORY_CMD,
     "from": (
         '            fail(exc.error, exc.message, json_output=json_output, exit_code=EXIT_NOT_READY,\n'
         '                 job_id=job_id)'
     ),
     "to": '            fail(exc.error, exc.message, json_output=json_output, job_id=job_id)'},
    {"id": "m6", "name": "the file is written with mode 0o600", "file": JOB_STORY_CMD,
     "from": "durable_write(target, data, mode=0o644)",
     "to": "durable_write(target, data, mode=0o600)"},
    {"id": "m7", "name": "readEmbeddedStory parses with no try", "file": STORY_EXPORT_TS,
     "from": (
         '  try {\n'
         '    return decodeStoryExport(JSON.parse(text));\n'
         '  } catch {\n'
         '    return { ok: false, message: STORY_EXPORT_UNREADABLE_LINE };\n'
         '  }\n'
         '}'
     ),
     "to": '  return decodeStoryExport(JSON.parse(text));\n}'},
    {"id": "m8", "name": "the TypeScript STORY_DATA_ELEMENT_ID reads remedy-story", "file": STORY_EXPORT_TS,
     "from": 'export const STORY_DATA_ELEMENT_ID = "remedy-story-data";',
     "to": 'export const STORY_DATA_ELEMENT_ID = "remedy-story";'},
    {"id": "m9", "name": "StoryPanel shows Close when no onClose is given", "file": STORY_PANEL_TSX,
     "from": '{onClose && <button type="button" onClick={onClose}>Close story</button>}',
     "to": '<button type="button" onClick={onClose}>Close story</button>'},
    {"id": "m10", "name": "the plugin drops inlineDynamicImports", "file": VITE_CONFIG,
     "from": "              inlineDynamicImports: true,\n",
     "to": ""},
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
