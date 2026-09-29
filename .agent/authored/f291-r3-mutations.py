"""F291 R3 C6 — the round 3 mutation tool (G3 red proofs).

Takes a worktree path as its one argument. For each mutation below it edits
``apps/cli/commands/brain.py`` INSIDE that worktree (asserting its FROM text,
the line ``        except OSError:``, occurs exactly once there), runs
``python3 -B -m pytest -q -p no:cacheprovider tests/test_brain_viewer.py``
with the worktree as the working directory and first on ``PYTHONPATH``, restores
the bytes, and prints one line per mutation: its label, the exit code and the
failed count. It runs an unmutated control first and last, reports
``restored byte-identical: True`` after each restore, and ends with
``ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>``.

Never run against the primary checkout — always a disposable worktree.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

TEST_TARGET = "tests/test_brain_viewer.py"
TARGET_PATH = "apps/cli/commands/brain.py"
FROM_TEXT = "        except OSError:\n"

MUTATIONS = [
    {
        "label": "m1 (the handler goes back to catching Exception)",
        "to_text": "        except Exception:\n",
    },
    {
        "label": "m2 (the handler catches ValueError in place of OSError)",
        "to_text": "        except ValueError:\n",
    },
]


def _run_pytest(worktree: Path) -> tuple[int, str]:
    env = {**os.environ}
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(worktree) + (f":{existing}" if existing else "")
    result = subprocess.run(
        ["python3", "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST_TARGET],
        cwd=str(worktree),
        env=env,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout + result.stderr


def _failed_count(output: str) -> int:
    match = re.search(r"(\d+) failed", output)
    return int(match.group(1)) if match else 0


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f291-r3-mutations.py <worktree-path>")
        return 2
    worktree = Path(sys.argv[1]).resolve()
    target = worktree / TARGET_PATH

    all_ok = True

    # Control run FIRST — unmutated, must pass.
    exit_code, output = _run_pytest(worktree)
    failed = _failed_count(output)
    print(f"control (before) exit={exit_code} failed={failed}")
    if exit_code != 0 or failed != 0:
        all_ok = False

    for mutation in MUTATIONS:
        original = target.read_bytes()
        original_text = original.decode("utf-8")
        occurrences = original_text.count(FROM_TEXT)
        if occurrences != 1:
            print(
                f"{mutation['label']}: FROM text occurs {occurrences} times in "
                f"{TARGET_PATH}, expected exactly 1 — STOP"
            )
            return 1
        mutated_text = original_text.replace(FROM_TEXT, mutation["to_text"], 1)
        target.write_bytes(mutated_text.encode("utf-8"))
        try:
            exit_code, output = _run_pytest(worktree)
            failed = _failed_count(output)
            print(f"{mutation['label']}: exit={exit_code} failed={failed}")
            if exit_code == 0:
                all_ok = False
        finally:
            target.write_bytes(original)
            restored = target.read_bytes()
            identical = restored == original
            print(f"restored byte-identical: {identical}")
            if not identical:
                all_ok = False

    # Control run LAST — unmutated again, must pass.
    exit_code, output = _run_pytest(worktree)
    failed = _failed_count(output)
    print(f"control (after) exit={exit_code} failed={failed}")
    if exit_code != 0 or failed != 0:
        all_ok = False

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
