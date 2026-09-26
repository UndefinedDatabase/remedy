"""F289 R3 G5 — the mutation tool: six red-proofs against the round's own tests.

Usage: python3 -B .agent/authored/f289-r3-mutations.py <worktree-path>

For each mutation: read the named module inside the worktree, assert its FROM
text occurs EXACTLY ONCE, write the mutated text, run
`tests/orchestration/test_doc_staleness.py` and
`tests/orchestration/test_self_use_runner.py` from the worktree's root (after
purging `__pycache__`), restore the original bytes, and report the label, the
real exit code, the failed-test count and the failing node ids. An unmutated
control run brackets the sweep (first and last). Ends with a byte-identical
restore check per touched file and a single boolean verdict.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

DOC_STALENESS = "packages/orchestration/doc_staleness.py"
SELF_USE_GENERATOR = "packages/orchestration/self_use_generator.py"
SELF_USE_RUNNER = "packages/orchestration/self_use_runner.py"

TEST_FILES = (
    "tests/orchestration/test_doc_staleness.py",
    "tests/orchestration/test_self_use_runner.py",
)

MUTATIONS: list[dict[str, str]] = [
    dict(
        label="m1 R-1074: _run_c04 goes back to requiring a file",
        module=DOC_STALENESS,
        find="if not resolved.exists():",
        replace="if not resolved.is_file():",
    ),
    dict(
        label="m2 R-1074: _run_c04 accepts every link whose target's parent folder exists",
        module=DOC_STALENESS,
        find="if not resolved.exists():",
        replace="if not resolved.parent.exists():",
    ),
    dict(
        label="m3 _doc_staleness_tier ignores the keys the queue already targets",
        module=SELF_USE_GENERATOR,
        find="claim = next((c for c in claims if c.key not in targeted), None)",
        replace="claim = next((c for c in claims), None)",
    ),
    dict(
        label="m4 _doctor_warning_tier answers None",
        module=SELF_USE_GENERATOR,
        find=(
            "    from apps.cli.commands import worker_facade_cmd\n"
            "\n"
            "    report = worker_facade_cmd.doctor_core_report()"
        ),
        replace=(
            "    return None\n"
            "\n"
            "    from apps.cli.commands import worker_facade_cmd\n"
            "\n"
            "    report = worker_facade_cmd.doctor_core_report()"
        ),
    ),
    dict(
        label="m5 _run_c01 reads only the Guides section",
        module=DOC_STALENESS,
        find='quick_find_bounds = _section_bounds(text, "## Quick-Find Table", exact=True)',
        replace="quick_find_bounds = None",
    ),
    dict(
        label="m6 run_next_self_use_item resolves its default max_cost_usd to 1.00",
        module=SELF_USE_RUNNER,
        find='max_cost_usd = _resolve("max_cost_usd", max_cost_usd, _MAX_COST_USD)',
        replace='max_cost_usd = _resolve("max_cost_usd", max_cost_usd, 1.00)',
    ),
]


def _purge_pycache(root: Path) -> None:
    for path in root.rglob("__pycache__"):
        shutil.rmtree(path, ignore_errors=True)


def _run_tests(root: Path) -> tuple[int, int, list[str]]:
    _purge_pycache(root)
    cmd = [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TEST_FILES]
    proc = subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=300)
    output = proc.stdout + proc.stderr
    failed_nodes = [
        line[len("FAILED "):].split(" ")[0]
        for line in output.splitlines()
        if line.startswith("FAILED ")
    ]
    return proc.returncode, len(failed_nodes), failed_nodes


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: mutations.py <worktree-path>", file=sys.stderr)
        return 2
    worktree = Path(argv[1]).resolve()

    exit_code, failed_count, nodes = _run_tests(worktree)
    print(f"control (before) | exit={exit_code} failed={failed_count} nodes={nodes}")
    if exit_code != 0:
        print("CONTROL RUN IS NOT GREEN — aborting the sweep.")
        return 1

    all_caught = True
    originals: dict[str, str] = {}
    for mutation in MUTATIONS:
        module_path = worktree / mutation["module"]
        original = module_path.read_text(encoding="utf-8")
        originals.setdefault(mutation["module"], original)
        occurrences = original.count(mutation["find"])
        assert occurrences == 1, (
            f'{mutation["label"]}: FROM text occurs {occurrences} times in '
            f'{mutation["module"]}, expected exactly 1'
        )
        mutated = original.replace(mutation["find"], mutation["replace"], 1)
        module_path.write_text(mutated, encoding="utf-8")
        try:
            exit_code, failed_count, nodes = _run_tests(worktree)
        finally:
            module_path.write_text(original, encoding="utf-8")
        caught = exit_code != 0 and failed_count > 0
        if not caught:
            all_caught = False
        print(f'{mutation["label"]} | exit={exit_code} failed={failed_count} nodes={nodes}')

    for relpath, original in originals.items():
        restored = (worktree / relpath).read_text(encoding="utf-8")
        print(f"restored byte-identical: {restored == original} ({relpath})")

    exit_code, failed_count, nodes = _run_tests(worktree)
    print(f"control (after) | exit={exit_code} failed={failed_count} nodes={nodes}")
    if exit_code != 0:
        all_caught = False

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_caught}")
    return 0 if all_caught else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
