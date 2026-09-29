#!/usr/bin/env python3
"""Mutation tool for F039 R10: R-1103's repair — the zero-network test's own idle drain after its
last check.

Given a worktree path, symlinks the worktree's `apps/ui/node_modules` to the PRIMARY's own (a
worktree carries no `node_modules` of its own) BEFORE its first control, then runs an unmutated
control first and last, and between them applies each mutation below (every FROM must occur
exactly once in its file) to the worktree's own copy of `storyPlayerMain.tsx`, runs `pytest`
under `python3 -B` over the worktree's own
`tests/ui_server/test_story_export_file_live.py`, restores the file BYTE-IDENTICAL, and reports
the passed, failed, error and skipped counts alongside the exit code. A mutation is caught when
the run goes red (a failure OR an error).

After the two mutations, ONE REVERT PROBE applies m1's own mutation together with the test
file's `IDLE_DRAIN_SECONDS` set to `0.0` instead of `2.0` — a drain window of zero seconds never
reads the late request, so this shows the drain, not something else, is what catches m1. Its
expected reading is GREEN; it is reported as the probe it is, never folded into the mutation
count. `python3 -B` and the worktree's own root first on `PYTHONPATH` keep a bytecode cache from
ever serving a previous mutation's module, following `.agent/authored/f039-r9-mutations.py`'s
route.

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

STORY_PLAYER_MAIN = "apps/ui/src/storyPlayerMain.tsx"
TEST_FILE = "tests/ui_server/test_story_export_file_live.py"

GUARD_RELS = [TEST_FILE]

RENDER_TAIL = "  </React.StrictMode>,\n);\n"

MUTATIONS = [
    {
        "id": "m1",
        "name": "storyPlayerMain.tsx fetches an off-machine address 500 ms after load",
        "file": STORY_PLAYER_MAIN,
        "from": RENDER_TAIL,
        "to": RENDER_TAIL + '\nsetTimeout(() => {\n  fetch("http://127.0.0.1:9/late");\n}, 500);\n',
    },
    {
        "id": "m2",
        "name": (
            "storyPlayerMain.tsx sends an XMLHttpRequest to an off-machine address 1500 ms "
            "after load"
        ),
        "file": STORY_PLAYER_MAIN,
        "from": RENDER_TAIL,
        "to": (
            RENDER_TAIL
            + "\nsetTimeout(() => {\n"
            + '  const xhr = new XMLHttpRequest();\n'
            + '  xhr.open("GET", "http://127.0.0.1:9/late-xhr");\n'
            + "  xhr.send();\n"
            + "}, 1500);\n"
        ),
    },
]

REVERT_PROBE = {
    "id": "revert-probe",
    "name": (
        "m1 together with IDLE_DRAIN_SECONDS = 0.0 — shows the drain is what catches m1"
    ),
    "steps": [
        {"file": STORY_PLAYER_MAIN, "from": RENDER_TAIL, "to": MUTATIONS[0]["to"]},
        {"file": TEST_FILE, "from": "IDLE_DRAIN_SECONDS = 2.0\n", "to": "IDLE_DRAIN_SECONDS = 0.0\n"},
    ],
}


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


def apply_one(worktree: Path, file_rel: str, from_text: str, to_text: str) -> tuple[Path, bytes, str]:
    target = worktree / file_rel
    original = target.read_bytes()
    digest = sha256_of(target)
    text = original.decode("utf-8")
    count = text.count(from_text)
    if count != 1:
        raise ValueError(f"{file_rel}: FROM occurrences {count}")
    mutated = text.replace(from_text, to_text, 1)
    target.write_bytes(mutated.encode("utf-8"))
    return target, original, digest


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
        try:
            target, original, digest = apply_one(worktree, mut["file"], mut["from"], mut["to"])
        except ValueError as exc:
            print(f"{mut['id']}: SKIPPED, {exc}")
            all_ok = False
            continue
        try:
            g = run_guard(worktree)
        finally:
            target.write_bytes(original)
        restored = sha256_of(target) == digest
        caught = g["exit"] != 0 and (g["failed"] > 0 or g["errors"] > 0)
        all_ok &= caught and restored
        print(f"{mut['id']} ({mut['name']}): {fmt(g)} | caught={caught} restored byte-identical={restored}")

    # ONE REVERT PROBE — reported as the probe it is, never folded into all_ok or the mutation count.
    applied = [
        apply_one(worktree, step["file"], step["from"], step["to"])
        for step in REVERT_PROBE["steps"]
    ]
    try:
        g = run_guard(worktree)
    finally:
        for target, original, _ in applied:
            target.write_bytes(original)
    probe_restored = all(sha256_of(target) == digest for target, _, digest in applied)
    probe_green = g["exit"] == 0 and g["failed"] == 0 and g["errors"] == 0
    print(
        f"REVERT PROBE ({REVERT_PROBE['name']}): {fmt(g)} | green={probe_green} "
        f"restored byte-identical={probe_restored}"
    )

    g = run_guard(worktree)
    print(f"CONTROL LAST: {fmt(g)}")
    last_green = g["exit"] == 0 and g["failed"] == 0 and g["errors"] == 0
    all_ok &= last_green
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
