#!/usr/bin/env python3
"""F041 R2 — the round's mutation tool (G4 red proofs).

Takes ONE argument, a worktree path. For each mutation below it edits the named
production file INSIDE that worktree (asserting its FROM text occurs exactly once
there), runs the named test file with the worktree as the working directory and the
worktree's root first on PYTHONPATH, restores the bytes, and prints one line per
mutation: its label, the exit code and the failed count. It runs an unmutated control
of every distinct test file the mutations name first and last, and ends with
``ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>``.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

# (label, production file relative to worktree root, FROM text, TO text, test file)
MUTATIONS = [
    ("n1", "packages/orchestration/ui_server.py",
     "            if not target.is_relative_to(dist.resolve()):",
     "            if not str(target).startswith(str(dist.resolve())):",
     "tests/ui_server/test_artifacts_route.py"),
    ("n2", "packages/orchestration/ui_server.py",
     '        ("X-Content-Type-Options", "nosniff"),\n',
     "",
     "tests/ui_server/test_artifacts_route.py"),
    ("n3", "packages/orchestration/ui_server.py",
     '        ("Content-Security-Policy", "default-src \'none\'; sandbox"),',
     '        ("Content-Security-Policy", "default-src \'none\'"),',
     "tests/ui_server/test_artifacts_route.py"),
    ("n4", "packages/orchestration/artifact_preview.py",
     '                and relative == f"{CAPTURES_DIRNAME}/{name}"',
     "                and True",
     "tests/orchestration/test_artifact_preview.py"),
    ("n5", "packages/orchestration/artifact_preview.py",
     "        if path.stat().st_size > FILE_MAX_BYTES:",
     "        if False:",
     "tests/orchestration/test_artifact_preview.py"),
    ("n6", "packages/orchestration/artifact_preview.py",
     "        if (root == ROOT_EVIDENCE",
     "        if (True",
     "tests/orchestration/test_artifact_preview.py"),
    ("n7", "packages/orchestration/artifact_preview.py",
     'README_CONTENT_TYPE = "text/plain; charset=utf-8"',
     'README_CONTENT_TYPE = "text/html; charset=utf-8"',
     "tests/ui_server/test_artifacts_route.py"),
]


def _run_pytest(worktree: Path, test_file: str) -> tuple[int, int]:
    """(exit code, failed count) of `test_file`, run inside `worktree`."""
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(worktree) + (os.pathsep + existing if existing else "")
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", test_file],
        cwd=str(worktree), env=env, capture_output=True, text=True,
    )
    failed = 0
    match = re.search(r"(\d+) failed", proc.stdout)
    if match:
        failed = int(match.group(1))
    return proc.returncode, failed


def main() -> int:
    worktree = Path(sys.argv[1]).resolve()
    distinct_test_files = list(dict.fromkeys(m[4] for m in MUTATIONS))

    print("CONTROL (unmutated, first):")
    for test_file in distinct_test_files:
        code, failed = _run_pytest(worktree, test_file)
        print(f"  {test_file}: exit={code} failed={failed}")

    all_caught = True
    for label, prod_rel, from_text, to_text, test_file in MUTATIONS:
        prod_path = worktree / prod_rel
        original = prod_path.read_text()
        count = original.count(from_text)
        assert count == 1, f"{label}: FROM text occurs {count} times in {prod_rel}, expected 1"
        mutated = original.replace(from_text, to_text)
        prod_path.write_text(mutated)
        code, failed = _run_pytest(worktree, test_file)
        caught = code != 0
        all_caught = all_caught and caught
        print(f"{label}: exit={code} failed={failed} caught={caught}")
        prod_path.write_text(original)
        restored = prod_path.read_text() == original
        print(f"restored byte-identical: {restored}")
        if not restored:
            all_caught = False

    print("CONTROL (unmutated, last):")
    for test_file in distinct_test_files:
        code, failed = _run_pytest(worktree, test_file)
        print(f"  {test_file}: exit={code} failed={failed}")

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_caught}")
    return 0 if all_caught else 1


if __name__ == "__main__":
    raise SystemExit(main())
