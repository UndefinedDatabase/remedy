"""F286 R1 C4 — the mutation tool for R-1104's repair (`_run_c07` in
`packages/orchestration/doc_staleness.py`).

Usage: `python3 -B .agent/authored/f286-r1-mutations.py <worktree-path>`

For each mutation below, edits the target file INSIDE the given worktree
(asserting its FROM text occurs exactly once there first), runs the
doc_staleness test file with the worktree as the working directory and the
worktree's own root first on PYTHONPATH, restores the original bytes, and
reports one line per mutation: its label, the real exit code and the
"failed" count parsed from pytest's summary line. Runs an unmutated control
first and last. Ends with a single boolean verdict line.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

TARGET_RELPATH = "packages/orchestration/doc_staleness.py"
TEST_RELPATH = "tests/orchestration/test_doc_staleness.py"

MUTATIONS = [
    (
        "m1 the skip of S2 is deleted",
        (
            "                last = span.rsplit(\".\", 1)[-1]\n"
            "                if last in _FILE_EXTENSIONS:\n"
            "                    continue\n"
        ),
        "",
    ),
    (
        "m2 html is removed from _FILE_EXTENSIONS",
        '    "css", "html", "js", "json", "md", "py", "sh", "toml", "ts", "tsx", "txt", "yaml", "yml",\n',
        '    "css", "js", "json", "md", "py", "sh", "toml", "ts", "tsx", "txt", "yaml", "yml",\n',
    ),
    (
        "m3 the skip reads the span's FIRST segment instead of its last",
        '                last = span.rsplit(".", 1)[-1]\n',
        '                last = span.split(".", 1)[0]\n',
    ),
    (
        "m4 host is added to _FILE_EXTENSIONS, which hides the registered key ollama.host",
        '    "css", "html", "js", "json", "md", "py", "sh", "toml", "ts", "tsx", "txt", "yaml", "yml",\n',
        '    "css", "html", "host", "js", "json", "md", "py", "sh", "toml", "ts", "tsx", "txt", "yaml", "yml",\n',
    ),
]


def _run_tests(worktree: Path) -> tuple[int, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(worktree) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        ["python3", "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST_RELPATH],
        cwd=str(worktree),
        env=env,
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def _failed_count(output: str) -> int:
    m = re.search(r"(\d+) failed", output)
    return int(m.group(1)) if m else 0


def _run_control(worktree: Path, label: str) -> bool:
    """Run the unmutated suite; return True iff it is clean (exit 0, 0 failed)."""
    exit_code, output = _run_tests(worktree)
    failed = _failed_count(output)
    print(f"{label}: exit={exit_code} failed={failed}")
    return exit_code == 0 and failed == 0


def main() -> None:
    worktree = Path(sys.argv[1]).resolve()
    target = worktree / TARGET_RELPATH
    original_bytes = target.read_bytes()
    original_text = original_bytes.decode("utf-8")

    ok = True

    ok = _run_control(worktree, "control (before, unmutated)") and ok

    for label, from_text, to_text in MUTATIONS:
        occurrences = original_text.count(from_text)
        assert occurrences == 1, f"{label}: FROM text occurs {occurrences} times, expected 1"
        mutated_text = original_text.replace(from_text, to_text, 1)
        target.write_text(mutated_text, encoding="utf-8")
        try:
            exit_code, output = _run_tests(worktree)
            failed = _failed_count(output)
            print(f"{label}: exit={exit_code} failed={failed}")
            if exit_code == 0:
                ok = False
        finally:
            target.write_bytes(original_bytes)
            restored = target.read_bytes()
            identical = restored == original_bytes
            print(f"restored byte-identical: {identical}")
            if not identical:
                ok = False

    ok = _run_control(worktree, "control (after, unmutated)") and ok

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {ok}")


if __name__ == "__main__":
    main()
