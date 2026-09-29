"""F291 R2 C5 — the round 2 mutation tool (G3 red proofs).

Takes a worktree path as its one argument. For each mutation below it edits the
named production file INSIDE that worktree (asserting its FROM text occurs
exactly once there), runs
``python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_self_use_runner.py``
with the worktree as the working directory and first on ``PYTHONPATH``, restores
the bytes, and prints one line per mutation: its label, the exit code and the
failed count. It runs an unmutated control first and last, reports
``restored byte-identical: True`` after each restore, and ends with
``ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>``.

Never run against the primary checkout — always a disposable worktree.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

TEST_TARGET = "tests/orchestration/test_self_use_runner.py"

MUTATIONS = [
    {
        "label": "r1 (Tier 4 job markdown loses its ## Task 1 heading)",
        "path": "packages/orchestration/self_use_generator.py",
        "from_text": (
            '        "## Task 1\\n"\n'
            '        f"Line {number} of `{path}` excuses a blind exception handler '
            "from ruff's BLE001 rule:\\n\"\n"
        ),
        "to_text": (
            '        f"Line {number} of `{path}` excuses a blind exception handler '
            "from ruff's BLE001 rule:\\n\"\n"
        ),
    },
    {
        "label": "r2 (generate_and_append_if_empty drops source_root)",
        "path": "packages/orchestration/self_use_generator.py",
        "from_text": (
            "        queue_path, ledger_path, order_path=order_path, today=today, "
            "source_root=source_root,\n"
        ),
        "to_text": (
            "        queue_path, ledger_path, order_path=order_path, today=today,\n"
        ),
    },
    {
        "label": "r3 (_MAX_PROVIDER_CALLS reads 1)",
        "path": "packages/orchestration/self_use_runner.py",
        "from_text": "_MAX_PROVIDER_CALLS = 8\n",
        "to_text": "_MAX_PROVIDER_CALLS = 1\n",
    },
]


def _run_pytest(worktree: Path) -> tuple[int, str]:
    env = {**__import__("os").environ}
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
        print("usage: f291-r2-mutations.py <worktree-path>")
        return 2
    worktree = Path(sys.argv[1]).resolve()

    all_ok = True

    # Control run FIRST — unmutated, must pass.
    exit_code, output = _run_pytest(worktree)
    failed = _failed_count(output)
    print(f"control (before) exit={exit_code} failed={failed}")
    if exit_code != 0 or failed != 0:
        all_ok = False

    for mutation in MUTATIONS:
        target = worktree / mutation["path"]
        original = target.read_bytes()
        original_text = original.decode("utf-8")
        occurrences = original_text.count(mutation["from_text"])
        if occurrences != 1:
            print(
                f"{mutation['label']}: FROM text occurs {occurrences} times in "
                f"{mutation['path']}, expected exactly 1 — STOP"
            )
            return 1
        mutated_text = original_text.replace(mutation["from_text"], mutation["to_text"], 1)
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
