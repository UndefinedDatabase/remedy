"""F291 R1 C5 — the round's mutation tool (G4).

Takes a worktree path. For each mutation, edits
`packages/orchestration/self_use_generator.py` INSIDE that worktree (asserting its
FROM text occurs exactly once there), runs
`python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_self_use_generator.py`
with the worktree as the working directory and the worktree's root first on
PYTHONPATH, restores the bytes, and prints one line per mutation: its label, the
exit code and the failed count. Runs an unmutated control first and last, reports
"restored byte-identical: True" after each restore, and ends with a final line
"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>".
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

TARGET_RELATIVE_PATH = "packages/orchestration/self_use_generator.py"
TEST_RELATIVE_PATH = "tests/orchestration/test_self_use_generator.py"

_FAILED_RE = re.compile(r"(\d+) failed")


# Each mutation: (label, FROM text, TO text). Applied one at a time to a freshly
# restored copy of the target file — never cumulative.
MUTATIONS: tuple[tuple[str, str, str], ...] = (
    (
        "m1 Tier 4's marks are sorted in reverse",
        "    marks.sort(key=lambda mark: (mark[0], mark[1]))",
        "    marks.sort(key=lambda mark: (mark[0], mark[1]), reverse=True)",
    ),
    (
        "m2 Tier 4 ignores the keys queue entries target",
        "        if key in targeted or RETIRED_WORD.search(text):",
        "        if RETIRED_WORD.search(text):",
    ),
    (
        "m3 Tier 4's key drops the ordinal (always 1)",
        '                key = f"{relpath}:{seen[stripped]}:{stripped}"',
        '                key = f"{relpath}:1:{stripped}"',
    ),
    (
        "m4 Tier 4's key carries the line number in place of the ordinal",
        '                key = f"{relpath}:{seen[stripped]}:{stripped}"',
        '                key = f"{relpath}:{number}:{stripped}"',
    ),
    (
        "m5 EXCUSED_HANDLER_ROOTS also holds \"tests\"",
        'EXCUSED_HANDLER_ROOTS = ("packages", "apps", "scripts")',
        'EXCUSED_HANDLER_ROOTS = ("packages", "apps", "scripts", "tests")',
    ),
    (
        "m6 Tier 5 is tried before Tier 4",
        "    root = source_root or default_source_root()\n"
        "\n"
        "    excused_result = _excused_handler_tier(queue_path, root)\n"
        "    if excused_result is not None:\n"
        "        return excused_result\n"
        "\n"
        "    return _untested_module_tier(queue_path, root)",
        "    root = source_root or default_source_root()\n"
        "\n"
        "    untested_result = _untested_module_tier(queue_path, root)\n"
        "    if untested_result is not None:\n"
        "        return untested_result\n"
        "\n"
        "    return _excused_handler_tier(queue_path, root)",
    ),
    (
        "m7 Tier 4 is tried before Tier 3",
        "    doctor_result = _doctor_warning_tier(queue_path)\n"
        "    if doctor_result is not None:\n"
        "        return doctor_result\n"
        "\n"
        "    root = source_root or default_source_root()\n"
        "\n"
        "    excused_result = _excused_handler_tier(queue_path, root)\n"
        "    if excused_result is not None:\n"
        "        return excused_result\n"
        "\n"
        "    return _untested_module_tier(queue_path, root)",
        "    root = source_root or default_source_root()\n"
        "\n"
        "    excused_result = _excused_handler_tier(queue_path, root)\n"
        "    if excused_result is not None:\n"
        "        return excused_result\n"
        "\n"
        "    doctor_result = _doctor_warning_tier(queue_path)\n"
        "    if doctor_result is not None:\n"
        "        return doctor_result\n"
        "\n"
        "    return _untested_module_tier(queue_path, root)",
    ),
    (
        "m8 a `from a.b import c` statement binds `a.b` only",
        "            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:\n"
        "                names.add(node.module)\n"
        "                for alias in node.names:\n"
        '                    names.add(f"{node.module}.{alias.name}")',
        "            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:\n"
        "                names.add(node.module)",
    ),
    (
        "m9 a package's __init__.py is no longer skipped",
        '            if path.name == "__init__.py":\n'
        "                continue\n",
        "",
    ),
    (
        "m10 a module with no public name offers nothing (no fallback to its private names)",
        "    return public or names",
        "    return public",
    ),
    (
        "m11 Tier 4 no longer screens with RETIRED_WORD",
        "        if key in targeted or RETIRED_WORD.search(text):",
        "        if key in targeted:",
    ),
    (
        "m12 the Tier 4 task no longer names MAX_EXCUSED",
        '        f"delete its `{mark}` mark. In the same change lower `MAX_EXCUSED` in `{ratchet}` by "',
        '        f"delete its `{mark}` mark. In the same change adjust the ratchet count in `{ratchet}` by "',
    ),
    (
        "m13 Tier 5 ignores the paths queue entries target",
        "            if relpath in targeted or RETIRED_WORD.search(relpath):",
        "            if RETIRED_WORD.search(relpath):",
    ),
    (
        "m14 Tier 5's names leave out classes",
        "        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))",
        "        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))",
    ),
)


def _run_tests(worktree: Path) -> tuple[int, int]:
    """Run the generator's tests inside `worktree`; return (exit code, failed count)."""
    env = {**os.environ, "PYTHONPATH": str(worktree)}
    result = subprocess.run(
        ["python3", "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST_RELATIVE_PATH],
        cwd=str(worktree),
        env=env,
        capture_output=True,
        text=True,
    )
    output = result.stdout + result.stderr
    match = _FAILED_RE.search(output)
    failed = int(match.group(1)) if match else 0
    return result.returncode, failed


def main(worktree_arg: str) -> None:
    worktree = Path(worktree_arg).resolve()
    target = worktree / TARGET_RELATIVE_PATH
    original = target.read_bytes()

    all_clean = True

    exit_code, failed = _run_tests(worktree)
    print(f"control (start): exit={exit_code} failed={failed}")
    if exit_code != 0 or failed != 0:
        all_clean = False

    for label, from_text, to_text in MUTATIONS:
        current = target.read_text(encoding="utf-8")
        occurrences = current.count(from_text)
        if occurrences != 1:
            raise AssertionError(
                f"{label}: FROM text occurs {occurrences} times in {target}, expected exactly 1"
            )
        mutated = current.replace(from_text, to_text)
        target.write_text(mutated, encoding="utf-8")

        exit_code, failed = _run_tests(worktree)
        print(f"{label}: exit={exit_code} failed={failed}")
        if exit_code == 0 and failed == 0:
            all_clean = False

        target.write_bytes(original)
        restored = target.read_bytes()
        identical = restored == original
        print(f"restored byte-identical: {identical}")
        if not identical:
            all_clean = False

    exit_code, failed = _run_tests(worktree)
    print(f"control (end): exit={exit_code} failed={failed}")
    if exit_code != 0 or failed != 0:
        all_clean = False

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_clean}")


if __name__ == "__main__":
    main(sys.argv[1])
