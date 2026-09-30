#!/usr/bin/env python3
"""F044 R7's red-proof tool (evidence, not product).

One entry, `mutations.py <worktree path>`. For each mutation below it edits the named
production file INSIDE that worktree (asserting its FROM text occurs exactly once there), runs
`pytest tests/orchestration/test_ci_budgets.py`, restores the bytes, and prints one line per
mutation: its label, the check's real exit code, and the failed count. Runs an unmutated control
first and last. Every mutation is a real behaviour change that must turn the suite red; a
mutation that stays green is reported as green, never papered over.

Usage: python3 mutations.py <worktree path>
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


class Mutation:
    def __init__(self, label: str, path: str, frm: str, to: str):
        self.label = label
        self.path = path
        self.frm = frm
        self.to = to


MUTATIONS = [
    Mutation(
        "m1", "packages/orchestration/ci_budgets.py",
        '_CHUNK_HASH_RE = re.compile(r"-(?=[0-9A-Za-z_]*[0-9])[0-9A-Za-z_]{6,10}(?=\\.[^.]+$)")',
        '_CHUNK_HASH_RE = re.compile(r"-[0-9A-Za-z_]{6,10}(?=\\.[^.]+$)")',
    ),
    Mutation(
        "m2", "packages/orchestration/ci_budgets.py",
        "        chunks[name] = chunks.get(name, 0) + size",
        "        chunks[name] = size",
    ),
    Mutation(
        "m3", "packages/orchestration/ci_budgets.py",
        "BUNDLE_SIZE_CAP_FACTOR = 1.10",
        "BUNDLE_SIZE_CAP_FACTOR = 0.5",
    ),
    Mutation(
        "m4", "packages/orchestration/ci_budgets.py",
        "cap = math.ceil(baseline_total * BUNDLE_SIZE_CAP_FACTOR)",
        "cap = baseline_total * BUNDLE_SIZE_CAP_FACTOR",
    ),
    Mutation(
        "m5", "packages/orchestration/ci_budgets.py",
        '    "assets/index.js": 783940,',
        '    "assets/index.js": 83940,',
    ),
]


def run_check(worktree: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/orchestration/test_ci_budgets.py"],
        cwd=str(worktree), capture_output=True, text=True, timeout=120,
    )


def failed_count(output: str) -> int:
    m = re.search(r"(\d+) failed", output)
    return int(m.group(1)) if m else 0


def print_result(label: str, proc: subprocess.CompletedProcess) -> None:
    out = proc.stdout + proc.stderr
    print(f"{label} exit={proc.returncode} failed={failed_count(out)}")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: mutations.py <worktree path>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()

    all_caught = True

    print("-- CONTROL (before), unmutated --")
    proc = run_check(worktree)
    print_result("control-before", proc)
    if proc.returncode != 0:
        all_caught = False

    print("-- MUTATIONS --")
    for mutation in MUTATIONS:
        target = worktree / mutation.path
        original = target.read_bytes()
        text = original.decode("utf-8")
        occurrences = text.count(mutation.frm)
        assert occurrences == 1, f"{mutation.label}: FROM text occurs {occurrences} times in {mutation.path}, expected 1"
        mutated_text = text.replace(mutation.frm, mutation.to, 1)
        target.write_bytes(mutated_text.encode("utf-8"))
        try:
            proc = run_check(worktree)
            print_result(mutation.label, proc)
            if proc.returncode == 0:
                all_caught = False
        finally:
            target.write_bytes(original)
            restored = target.read_bytes() == original
            print(f"restored byte-identical: {restored}")
            if not restored:
                all_caught = False

    print("-- CONTROL (after), unmutated --")
    proc = run_check(worktree)
    print_result("control-after", proc)
    if proc.returncode != 0:
        all_caught = False

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_caught}")
    return 0 if all_caught else 1


if __name__ == "__main__":
    raise SystemExit(main())
