"""F042 R7 G3 — the red proofs of R-1107's repair.

Takes a worktree path and, for each mutation below, edits
``tests/ui_server/test_story_export_file_live.py`` INSIDE that worktree (asserting its FROM text
occurs exactly once there), runs
``python3 -B -m pytest -q -p no:cacheprovider
tests/ui_server/test_story_export_file_live.py::test_chrome_timeout_message_names_log``
with the worktree as the working directory and first on ``PYTHONPATH``, restores the bytes, and
reports the mutation's label, exit code and failed count. An unmutated control runs first and
last. Every restore is verified byte-identical to the pre-mutation content.

Usage: python3 f042-r7-mutations.py <worktree-path>
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

TARGET_REL = "tests/ui_server/test_story_export_file_live.py"
NODE_ID = f"{TARGET_REL}::test_chrome_timeout_message_names_log"

# Each mutation's FROM text must occur exactly once in the unmutated file.
MUTATIONS = [
    (
        "r1 (ChromePipe._read_message leaves the log's last lines out of the timeout message)",
        '''                        tail = self._log_path.read_bytes().decode("utf-8", errors="replace").splitlines()[-5:]
                        if tail:
                            msg += "\\n" + "\\n".join(tail)
''',
        "",
    ),
    (
        "r2 (ChromePipe._read_message leaves the log's path out of the message)",
        '''                    msg += f"; Chrome log: {self._log_path}"
''',
        "",
    ),
    (
        "r3 (ChromePipe.__init__ sends Chrome's standard error to subprocess.DEVNULL again)",
        '''            stderr=self._log_file if self._log_file is not None else subprocess.DEVNULL,
''',
        "            stderr=subprocess.DEVNULL,\n",
    ),
]


def run_test(worktree: Path) -> tuple[int, int]:
    """Runs the one test node inside the worktree; returns (exit_code, failed_count)."""
    env = dict(os.environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(worktree) + (os.pathsep + existing if existing else "")
    proc = subprocess.run(
        ["python3", "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", NODE_ID],
        cwd=str(worktree),
        env=env,
        capture_output=True,
        text=True,
    )
    output = proc.stdout + proc.stderr
    failed = 0
    m = re.search(r"(\d+) failed", output)
    if m:
        failed = int(m.group(1))
    print(output)
    return proc.returncode, failed


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: f042-r7-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    worktree = Path(argv[1]).resolve()
    target = worktree / TARGET_REL
    original = target.read_bytes()

    all_clean = True

    # Control run 1: unmutated.
    print("=== control (before mutations) ===")
    exit_code, failed = run_test(worktree)
    print(f"label=control-before exit_code={exit_code} failed_count={failed}")
    if exit_code != 0 or failed != 0:
        all_clean = False

    for label, from_text, to_text in MUTATIONS:
        current = target.read_bytes().decode("utf-8")
        occurrences = current.count(from_text)
        assert occurrences == 1, f"{label}: FROM text occurs {occurrences} times, expected 1"
        mutated = current.replace(from_text, to_text, 1)
        target.write_bytes(mutated.encode("utf-8"))

        print(f"=== {label} ===")
        exit_code, failed = run_test(worktree)
        print(f"label={label} exit_code={exit_code} failed_count={failed}")
        caught = exit_code != 0 and failed >= 1
        if not caught:
            all_clean = False

        target.write_bytes(original)
        restored = target.read_bytes()
        identical = restored == original
        print(f"restored byte-identical: {identical}")
        if not identical:
            all_clean = False

    # Control run 2: unmutated, after all mutations restored.
    print("=== control (after mutations) ===")
    exit_code, failed = run_test(worktree)
    print(f"label=control-after exit_code={exit_code} failed_count={failed}")
    if exit_code != 0 or failed != 0:
        all_clean = False

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_clean}")
    return 0 if all_clean else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
