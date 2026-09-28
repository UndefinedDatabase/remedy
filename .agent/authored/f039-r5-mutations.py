#!/usr/bin/env python3
"""Mutation tool for F039 R5: the story's golden rules (storyPlayer.ts), the panel's
one timer and its portal (StoryPanel.tsx), the shell's and the right panel's own
entries, and R-1100's own repair (packages/orchestration/ui_server.py).

Given a worktree path, runs an unmutated control first and last, and between them
applies each mutation below (every FROM must occur exactly once in its file) to the
worktree's own copy of the named file, runs the vitest golden of `storyPlayer.test.ts`
and the two `pytest` guards this round touches, restores the file BYTE-IDENTICAL, and
reports each runner's failed count and exit code. A mutation is caught when at least
one runner goes red. Follows `.agent/authored/f039-r4-mutations.py`'s route: vitest
runs from the PRIMARY `apps/ui` (a worktree has no node_modules) with a plain-object
scratch config under `.remedy-wt/f039-r5-mutscratch/`, pointed at the WORKTREE's own
copy of the test file; the guards run with `python3 -B -m pytest` from the worktree's
own root, that root first on `PYTHONPATH`, so a bytecode cache can never serve a
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

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f039-r5-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

STORY_PLAYER = "apps/ui/src/components/story/storyPlayer.ts"
STORY_PANEL = "apps/ui/src/components/story/StoryPanel.tsx"
REMEDY_SHELL = "apps/ui/src/components/shell/RemedyShell.tsx"
RIGHT_PANEL = "apps/ui/src/components/panels/RightLivePanel.tsx"
UI_SERVER_PY = "packages/orchestration/ui_server.py"

VITEST_FILES = [
    "apps/ui/src/components/story/storyPlayer.test.ts",
]
GUARD_RELS = [
    "tests/ui_contracts/test_story_panel_contract.py",
    "tests/ui_server/test_story_section.py",
]

MUTATIONS = [
    # storyPlayer.ts — S2's own rules, caught by storyPlayer.test.ts's goldens.
    {"id": "m1", "name": "storyBeatsAt answers every beat of the card", "file": STORY_PLAYER,
     "from": "  return card.beats.filter((beat) => beat.seq <= position);\n",
     "to": "  return card.beats;\n"},
    {"id": "m2", "name": "storyPlayStart restarts only when the scrub is LIVE", "file": STORY_PLAYER,
     "from": ('  if (live || view.seqs.length === 0) return -1;\n'
              '  const lastSeq = view.seqs[view.seqs.length - 1];\n'
              '  if (position >= lastSeq) return -1;\n'
              '  return position;\n'),
     "to": ('  if (live) return -1;\n'
            '  if (view.seqs.length === 0) return -1;\n'
            '  return position;\n')},
    {"id": "m3", "name": "storyPlayStart always answers -1", "file": STORY_PLAYER,
     "from": "  return position;\n}\n\n/** A card's beats",
     "to": "  return -1;\n}\n\n/** A card's beats"},
    {"id": "m4", "name": "storyPositionLabel counts chapters from 0", "file": STORY_PLAYER,
     "from": "return `Chapter ${at + 1} of ${view.chapters.length}: ${chapter.title}`;",
     "to": "return `Chapter ${at} of ${view.chapters.length}: ${chapter.title}`;"},
    {"id": "m5", "name": "storyWalk's frames carry a wait of 0", "file": STORY_PLAYER,
     "from": "      delayMs: step.delayMs,\n", "to": "      delayMs: 0,\n"},
    # StoryPanel.tsx — S3's own rules, caught by the contract test's plain reading.
    {"id": "m6", "name": "the panel's timer cleanup no longer clears the timeout", "file": STORY_PANEL,
     "from": "    return () => window.clearTimeout(id);\n",
     "to": "    return () => { /* no cleanup */ };\n"},
    {"id": "m7", "name": "the panel renders in place, without createPortal", "file": STORY_PANEL,
     "from": "  return createPortal(\n", "to": "  return (\n"},
    # RemedyShell.tsx — S4's own entry, caught by the contract test's ordering check.
    {"id": "m8", "name": "the shell mounts the panel inside <main>, after the phase timeline",
     "file": REMEDY_SHELL,
     "from": '          <PhaseTimeline scrub={scrub} />\n',
     "to": ('          <PhaseTimeline scrub={scrub} />\n'
            '          {storyOpen && (<StoryPanel dashboard={dashboard} rows={ledgerRows} '
            'ownership={ownership} scrub={scrub} onClose={() => setStoryOpen(false)} />)}\n')},
    # RightLivePanel.tsx — S4's own entry, caught by the contract test's literal check.
    {"id": "m9", "name": "the Story button is removed from RightLivePanel.tsx", "file": RIGHT_PANEL,
     "from": ('      {onOpenStory && (<button type="button" className={styles.advancedToggle} '
              'onClick={onOpenStory}>Story</button>)}\n'),
     "to": ""},
    # ui_server.py — S1's own repair, R-1100's own proof.
    {"id": "m10", "name": "_build_story_section reads load_config() instead of get_config()",
     "file": UI_SERVER_PY,
     "from": ("    from packages.orchestration.config import get_config\n\n"
              "    config = get_config()\n"),
     "to": ("    from packages.orchestration.config import load_config\n\n"
            "    config = load_config()\n")},
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
