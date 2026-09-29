#!/usr/bin/env python3
"""Mutation tool for F039 R9: the story player's second build following the resolved
`outDir` (S1), and the zero-network live-Chrome test's own reach across the page it drives
(S2) — `render_story_html`'s content security policy, `storyPlayerMain.tsx`'s element id,
`StoryPanel`'s Space toggle and `PhaseTimeline`'s keyboard wiring.

Given a worktree path, symlinks the worktree's `apps/ui/node_modules` to the PRIMARY's own
(a worktree carries no `node_modules` of its own) BEFORE its first control, then runs an
unmutated control first and last, and between them applies each mutation below (every FROM
must occur exactly once in its file) to the worktree's own copy of the named file, runs
`pytest` under `python3 -B` over the worktree's own
`tests/ui_server/test_story_export_file_live.py` and
`tests/ui_contracts/test_story_player_contract.py`, restores the file BYTE-IDENTICAL, and
reports the passed, failed, error and skipped counts alongside the exit code. A mutation is
caught when the run goes red (a failure OR an error — m1 is caught as an ERROR raised by the
live test's own module-scoped fixture, never a FAILED test). `python3 -B` and the worktree's
own root first on `PYTHONPATH` keep a bytecode cache from ever serving a previous mutation's
module, following `.agent/authored/f039-r8-mutations.py`'s route.

Usage: python3 -B mutations.py <worktree_root>
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

PRIMARY_NODE_MODULES = Path("/home/decodeux/Repos/remedy/apps/ui/node_modules")

VITE_CONFIG = "apps/ui/vite.config.ts"
STORY_EXPORT_PY = "packages/orchestration/story_export.py"
STORY_PLAYER_MAIN = "apps/ui/src/storyPlayerMain.tsx"
STORY_PANEL_TSX = "apps/ui/src/components/story/StoryPanel.tsx"
PHASE_TIMELINE_TSX = "apps/ui/src/components/timeline/PhaseTimeline.tsx"

GUARD_RELS = [
    "tests/ui_server/test_story_export_file_live.py",
    "tests/ui_contracts/test_story_player_contract.py",
]

MUTATIONS = [
    {
        "id": "m1",
        "name": "the plugin's configResolved sets nothing, so the player lands in dist/story whatever the outDir",
        "file": VITE_CONFIG,
        "from": "      outDir = path.resolve(config.root, config.build.outDir);\n",
        "to": "",
    },
    {
        "id": "m2",
        "name": "render_story_html drops its content security policy and writes an off-machine image before the root element",
        "file": STORY_EXPORT_PY,
        "from": (
            '        \'<meta http-equiv="Content-Security-Policy" content="default-src \\\'none\\\'; \'\n'
            '        "script-src \'unsafe-inline\'; style-src \'unsafe-inline\'; img-src data:\\">\\n"\n'
            '        f"<title>Remedy story of job {job_id}</title>\\n"\n'
            '        f"<style>{style}</style>\\n"\n'
            '        "</head>\\n"\n'
            '        "<body>\\n"\n'
            '        \'<div id="root" data-ui="remedy-story"></div>\\n\'\n'
        ),
        "to": (
            '        f"<title>Remedy story of job {job_id}</title>\\n"\n'
            '        f"<style>{style}</style>\\n"\n'
            '        "</head>\\n"\n'
            '        "<body>\\n"\n'
            '        \'<img src="http://127.0.0.1:9/pixel.png" alt="">\\n\'\n'
            '        \'<div id="root" data-ui="remedy-story"></div>\\n\'\n'
        ),
    },
    {
        "id": "m3",
        "name": "storyPlayerMain.tsx reads the element remedy-story instead of STORY_DATA_ELEMENT_ID",
        "file": STORY_PLAYER_MAIN,
        "from": "document.getElementById(STORY_DATA_ELEMENT_ID)?.textContent ?? null",
        "to": 'document.getElementById("remedy-story")?.textContent ?? null',
    },
    {
        "id": "m4",
        "name": "StoryPanel's Space branch no longer toggles play",
        "file": STORY_PANEL_TSX,
        "from": "togglePlaying();",
        "to": "/* toggle disabled */;",
    },
    {
        "id": "m5",
        "name": "PhaseTimeline's slider no longer hands its keys to scrub.onKey",
        "file": PHASE_TIMELINE_TSX,
        "from": "if (scrub.onKey(event.key, event.shiftKey)) event.preventDefault();",
        "to": "",
    },
]


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ensure_node_modules_link(worktree: Path) -> None:
    link = worktree / "apps" / "ui" / "node_modules"
    if link.is_symlink() or link.exists():
        return
    os.symlink(PRIMARY_NODE_MODULES, link, target_is_directory=True)


def run_guard(worktree: Path) -> dict:
    env = dict(os.environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(worktree) if not existing else f"{worktree}{os.pathsep}{existing}"
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *GUARD_RELS],
        cwd=str(worktree), capture_output=True, text=True, timeout=180, env=env,
    )
    out = proc.stdout + proc.stderr
    passed = int(m.group(1)) if (m := re.search(r"(\d+) passed", out)) else 0
    failed = int(m.group(1)) if (m := re.search(r"(\d+) failed", out)) else 0
    errors = int(m.group(1)) if (m := re.search(r"(\d+) error", out)) else 0
    skipped = int(m.group(1)) if (m := re.search(r"(\d+) skipped", out)) else 0
    return {"exit": proc.returncode, "passed": passed, "failed": failed, "errors": errors,
            "skipped": skipped, "out": out}


def fmt(g: dict) -> str:
    return (f"exit={g['exit']} passed={g['passed']} failed={g['failed']} "
            f"errors={g['errors']} skipped={g['skipped']}")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: mutations.py <worktree_root>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()
    print(f"worktree: {worktree}")

    ensure_node_modules_link(worktree)
    print(f"node_modules linked: {(worktree / 'apps' / 'ui' / 'node_modules').is_symlink()}")

    g = run_guard(worktree)
    print(f"CONTROL FIRST: {fmt(g)}")
    first_green = g["exit"] == 0 and g["failed"] == 0 and g["errors"] == 0
    if not first_green:
        print("control is not green; aborting")
        print(g["out"])
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
            g = run_guard(worktree)
        finally:
            target.write_bytes(original)
        restored = sha256_of(target) == digest
        caught = g["exit"] != 0 and (g["failed"] > 0 or g["errors"] > 0)
        all_ok &= caught and restored
        print(f"{mut['id']} ({mut['name']}): {fmt(g)} | caught={caught} restored byte-identical={restored}")

    g = run_guard(worktree)
    print(f"CONTROL LAST: {fmt(g)}")
    last_green = g["exit"] == 0 and g["failed"] == 0 and g["errors"] == 0
    all_ok &= last_green
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
