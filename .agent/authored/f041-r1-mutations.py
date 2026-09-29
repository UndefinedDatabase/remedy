#!/usr/bin/env python3
"""F041 R1 — the round's mutation tool (G4 red proofs).

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
    ("m1", "packages/orchestration/artifact_markdown.py",
     '"object", "script", "style", "svg",', '"object", "style", "svg",',
     "tests/orchestration/test_artifact_markdown.py"),
    ("m2", "packages/orchestration/artifact_markdown.py",
     'probe = "".join(ch for ch in value if ch not in _CONTROL_OR_DEL).lower()',
     'probe = value.lower()',
     "tests/orchestration/test_artifact_markdown.py"),
    ("m3", "packages/orchestration/artifact_markdown.py",
     '        if image:\n            return None\n        if probe[:colon] not in LINK_SCHEMES:',
     '        if probe[:colon] not in LINK_SCHEMES:',
     "tests/orchestration/test_artifact_markdown.py"),
    ("m4", "packages/orchestration/artifact_markdown.py",
     '        if tag == "a":\n            kept.append(("rel", LINK_REL))\n'
     '        if tag == "img" and not any(name == "src" for name, _ in kept):',
     '        if tag == "img" and not any(name == "src" for name, _ in kept):',
     "tests/orchestration/test_artifact_markdown.py"),
    ("m5", "packages/orchestration/artifact_markdown.py",
     'out.append(_escape_run("".join(plain)))',
     'out.append("".join(plain))',
     "tests/orchestration/test_artifact_markdown.py"),
    ("m6", "packages/orchestration/artifact_preview.py",
     'if not candidate.is_relative_to(root) or not candidate.is_file():',
     'if not candidate.is_file():',
     "tests/orchestration/test_artifact_preview.py"),
    ("m7", "packages/orchestration/artifact_preview.py",
     'if rel.is_absolute() or ".." in rel.parts:',
     'if rel.is_absolute():',
     "tests/orchestration/test_artifact_preview.py"),
    ("m8", "packages/orchestration/artifact_preview.py",
     "ARTIFACT_ROOTS = (ROOT_WORKSPACE, ROOT_EVIDENCE)",
     "ARTIFACT_ROOTS = (ROOT_EVIDENCE, ROOT_WORKSPACE)",
     "tests/orchestration/test_artifact_preview.py"),
    ("m9", "packages/orchestration/ui_server.py",
     '                "artifacts": _build_artifacts_json,\n',
     '',
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
