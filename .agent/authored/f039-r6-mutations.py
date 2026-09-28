#!/usr/bin/env python3
"""Mutation tool for F039 R6: R-1101's own repair — the timer effect of `StoryPanel.tsx` keeps
the pending step through the host's re-renders by reading the latest story view through a ref
(`viewRef`) instead of naming `view` (or `scrub`, which answers a new object every render) as a
dependency.

Given a worktree path, runs an unmutated control first and last, and between them applies each
mutation below (every FROM must occur exactly once in its file) to the worktree's own copy of
`StoryPanel.tsx`, runs `tests/ui_contracts/test_story_panel_contract.py` there (the worktree's
own root first on `PYTHONPATH`, `python3 -B` so no bytecode cache can serve a previous
mutation's module) AND `.agent/authored/f039-r6-render_measure.py` with the WORKTREE as its own
repository root — the harness's relative import then resolves to the worktree's own
`apps/ui/src`, so the page mounts the worktree's own mutated panel — restores the file
BYTE-IDENTICAL, and reports each runner's own reading. A mutation is caught when the contract
fails AND the render reads fewer than 9 of 9 checks passing; m3 is the one case the block itself
names as possibly leaving the contract green (only the ref's own updating EFFECT is deleted, so
`viewRef.current` and the exact dependency line both survive untouched, and only the render's own
churn check, C-i, can tell the pending step now reads a view frozen at its very first render).

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

PRIMARY_ROOT = Path("/home/decodeux/Repos/remedy")
RENDER_MEASURE = PRIMARY_ROOT / ".agent" / "authored" / "f039-r6-render_measure.py"

STORY_PANEL = "apps/ui/src/components/story/StoryPanel.tsx"
GUARD_REL = "tests/ui_contracts/test_story_panel_contract.py"

MUTATIONS = [
    {
        "id": "m1",
        "name": "the timer's dependency list gains `scrub`",
        "file": STORY_PANEL,
        "from": "  }, [playing, position, reducedMotion, scrubTo]);\n",
        "to": "  }, [playing, position, reducedMotion, scrubTo, scrub]);\n",
    },
    {
        "id": "m2",
        "name": "the timer reads `view` itself and its dependency list gains `view`",
        "file": STORY_PANEL,
        "from": (
            "    const currentView = viewRef.current;\n"
            "    const step = autoplayStep(currentView.chapters, currentView.seqs, position, currentView.pacing, reducedMotion);\n"
            "    if (step === null) {\n"
            "      setPlaying(false);\n"
            "      return;\n"
            "    }\n"
            "    const id = window.setTimeout(() => scrubTo(step.position), step.delayMs);\n"
            "    return () => window.clearTimeout(id);\n"
            "  }, [playing, position, reducedMotion, scrubTo]);\n"
        ),
        "to": (
            "    const step = autoplayStep(view.chapters, view.seqs, position, view.pacing, reducedMotion);\n"
            "    if (step === null) {\n"
            "      setPlaying(false);\n"
            "      return;\n"
            "    }\n"
            "    const id = window.setTimeout(() => scrubTo(step.position), step.delayMs);\n"
            "    return () => window.clearTimeout(id);\n"
            "  }, [playing, position, reducedMotion, scrubTo, view]);\n"
        ),
    },
    {
        "id": "m3",
        "name": "the ref's effect is deleted, so the timer reads the first view forever",
        "file": STORY_PANEL,
        "from": (
            "  const viewRef = useRef(view);\n"
            "  useEffect(() => {\n"
            "    viewRef.current = view;\n"
            "  });\n"
        ),
        "to": "  const viewRef = useRef(view);\n",
    },
]


def sha256_of(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def run_render(worktree):
    proc = subprocess.run(
        [sys.executable, str(RENDER_MEASURE), str(worktree)],
        cwd=str(PRIMARY_ROOT), capture_output=True, text=True, timeout=180)
    out = proc.stdout + proc.stderr
    m = re.search(r"RENDER: (\d+) of (\d+) checks pass", out)
    passing, total = (int(m.group(1)), int(m.group(2))) if m else (-1, -1)
    line = m.group(0) if m else "NO RENDER LINE FOUND"
    return {"exit": proc.returncode, "passing": passing, "total": total, "line": line}


def run_both(worktree):
    return run_guard(worktree), run_render(worktree)


def fmt(g, r):
    return f"guard exit={g['exit']} failed={g['failed']} passed={g['passed']} | render exit={r['exit']} {r['line']}"


def main():
    if len(sys.argv) != 2:
        print("usage: mutations.py <worktree_root>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()
    print(f"worktree: {worktree}")
    g, r = run_both(worktree)
    print(f"CONTROL FIRST: {fmt(g, r)}")
    first_green = g["exit"] == 0 and g["failed"] == 0 and r["exit"] == 0 and r["passing"] == r["total"] == 9
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
            g, r = run_both(worktree)
        finally:
            target.write_bytes(original)
        restored = sha256_of(target) == digest
        contract_failed = g["exit"] != 0 and g["failed"] > 0
        render_short = r["exit"] != 0 or r["passing"] < r["total"]
        caught = contract_failed and render_short if mut["id"] != "m3" else render_short
        all_ok &= caught and restored
        print(f"{mut['id']} ({mut['name']}): {fmt(g, r)} | caught={caught} restored byte-identical={restored}")
    g, r = run_both(worktree)
    last_green = g["exit"] == 0 and g["failed"] == 0 and r["exit"] == 0 and r["passing"] == r["total"] == 9
    print(f"CONTROL LAST: {fmt(g, r)}")
    all_ok &= last_green
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
