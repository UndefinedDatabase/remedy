#!/usr/bin/env python3
"""F041 R3 C5 — the round's red-proof tool (G4).

Takes ONE argument, a worktree path. For each mutation below it edits the named
production file INSIDE that worktree (asserting its FROM text occurs exactly once
there), runs `python3 -B -m pytest -q -p no:cacheprovider <the named test file>` with
the worktree as the working directory and its root first on PYTHONPATH, restores the
file's original bytes, and reports one line per mutation: its label, the exit code and
the failed count. It runs an unmutated control of each test file the mutations name
first and last, reports "restored byte-identical: True" after each restore, and ends
with "ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>".

Every mutation here is a real behaviour change in the preview state machine, the
runtime-verb runner or the preview commands — never a cosmetic edit a test cannot see.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Mutation:
    label: str
    file: str
    test: str
    frm: str
    to: str


MUTATIONS: list[Mutation] = [
    Mutation(
        "p1", "packages/orchestration/preview_control.py",
        "tests/orchestration/test_preview_control.py",
        '    probed = runner("probe", root)\n',
        "    probed = served  # MUTATED p1: the serve's answer stands in for the probe's\n",
    ),
    Mutation(
        "p2", "packages/orchestration/preview_control.py",
        "tests/orchestration/test_preview_control.py",
        '        runner("stop", root)\n',
        "        pass  # MUTATED p2: a failed probe no longer stops the runtime\n",
    ),
    Mutation(
        "p3", "packages/orchestration/preview_control.py",
        "tests/orchestration/test_preview_control.py",
        'served.payload.get("error") == CONFIG_ERROR_TOKEN',
        "False",
    ),
    Mutation(
        "p4", "packages/orchestration/preview_control.py",
        "tests/orchestration/test_preview_control.py",
        '    if action == ACTION_START and record["state"] in ACTIVE_STATES:\n',
        "    if False:  # MUTATED p4: a start while live restarts it\n",
    ),
    Mutation(
        "p5", "packages/orchestration/preview_control.py",
        "tests/orchestration/test_preview_control.py",
        'stored.get("schema") != PREVIEW_SCHEMA',
        "False  # MUTATED p5: schema is never checked",
    ),
    Mutation(
        "p6", "packages/orchestration/preview_runner.py",
        "tests/orchestration/test_preview_runner.py",
        '    ok = bool(envelope.get("ok")) and result.returncode == 0\n',
        '    ok = bool(envelope.get("ok"))  # MUTATED p6: exit code ignored\n',
    ),
    Mutation(
        "p7", "packages/orchestration/preview_runner.py",
        "tests/orchestration/test_preview_runner.py",
        "            timeout=VERB_TIMEOUT_SECONDS, check=False,\n",
        "            check=False,  # MUTATED p7: no timeout passed\n",
    ),
    Mutation(
        "p8", "apps/cli/commands/job_preview_cmd.py",
        "tests/cli/test_job_preview.py",
        "    if state != _EXPECTED_STATE[action]:\n",
        "    if False:  # MUTATED p8: the command never fails\n",
    ),
]


def _test_files_in_order() -> list[str]:
    seen: list[str] = []
    for mutation in MUTATIONS:
        if mutation.test not in seen:
            seen.append(mutation.test)
    return seen


def _run_pytest(worktree: Path, test_path: str) -> tuple[int, int, str]:
    env = dict(os.environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(worktree) + (os.pathsep + existing if existing else "")
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", test_path],
        cwd=str(worktree), env=env, capture_output=True, text=True,
    )
    output = proc.stdout + proc.stderr
    match = re.search(r"(\d+) failed", output)
    failed = int(match.group(1)) if match else 0
    return proc.returncode, failed, output


def _run_control(worktree: Path, label: str, all_ok: bool) -> bool:
    print(f"{label}:")
    for test_path in _test_files_in_order():
        code, failed, _ = _run_pytest(worktree, test_path)
        ok = code == 0 and failed == 0
        all_ok = all_ok and ok
        print(f"  control {test_path}: exit_code={code} failed_count={failed} ok={ok}")
    return all_ok


def main() -> int:
    worktree = Path(sys.argv[1]).resolve()
    all_ok = True

    all_ok = _run_control(worktree, "CONTROL (first)", all_ok)

    for mutation in MUTATIONS:
        target = worktree / mutation.file
        original = target.read_bytes()
        original_text = original.decode("utf-8")
        occurrences = original_text.count(mutation.frm)
        if occurrences != 1:
            raise RuntimeError(
                f"{mutation.label}: FROM text occurs {occurrences} times in "
                f"{mutation.file}, expected exactly 1"
            )
        mutated_text = original_text.replace(mutation.frm, mutation.to, 1)
        target.write_text(mutated_text, encoding="utf-8")
        try:
            code, failed, _ = _run_pytest(worktree, mutation.test)
        finally:
            target.write_bytes(original)
        restored = target.read_bytes()
        identical = restored == original
        caught = code != 0
        all_ok = all_ok and caught and identical
        print(f"{mutation.label}: exit_code={code} failed_count={failed}")
        print(f"  restored byte-identical: {identical}")

    all_ok = _run_control(worktree, "CONTROL (last)", all_ok)

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
