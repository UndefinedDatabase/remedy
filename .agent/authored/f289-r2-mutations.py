"""F289 R2 G5 — the mutation tool: seventeen red-proofs against the round's own tests.

Usage: python3 -B .agent/authored/f289-r2-mutations.py <worktree-path>

For each mutation: read the named module inside the worktree, assert its FROM
text occurs EXACTLY ONCE, write the mutated text, run the round's two test
files from the worktree's root (after purging `__pycache__`), restore the
original bytes, and report the label, the real exit code, the failed-test
count and the failing node ids. An unmutated control run brackets the sweep
(first and last). Ends with a byte-identical restore check per touched file
and a single boolean verdict.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

DOC_STALENESS = "packages/orchestration/doc_staleness.py"
SELF_USE_GENERATOR = "packages/orchestration/self_use_generator.py"

TEST_FILES = (
    "tests/orchestration/test_doc_staleness.py",
    "tests/orchestration/test_self_use_generator.py",
)

MUTATIONS: list[dict[str, str]] = [
    dict(
        label="m1 C01 reads only the Guides section",
        module=DOC_STALENESS,
        find='quick_find_bounds = _section_bounds(text, "## Quick-Find Table", exact=True)',
        replace="quick_find_bounds = None",
    ),
    dict(
        label="m2 C02 ignores a subcommand that ships and is not documented",
        module=DOC_STALENESS,
        find="for order, sub in enumerate(sorted(shipped - documented)):",
        replace="for order, sub in enumerate(sorted(set())):",
    ),
    dict(
        label="m3 C03 accepts a second word that is not a group",
        module=DOC_STALENESS,
        find="            if group_id is None:\n                items.append((0, line_no, StaleClaim(",
        replace="            if False:\n                items.append((0, line_no, StaleClaim(",
    ),
    dict(
        label="m4 C04 resolves a link against the root instead of the guide's folder",
        module=DOC_STALENESS,
        find="resolved = (guide_dir / path_part).resolve()",
        replace="resolved = (root / path_part).resolve()",
    ),
    dict(
        label="m5 C05 keeps punctuation in a heading's slug",
        module=DOC_STALENESS,
        find='kept = re.sub(r"[^\\w\\s-]", "", lowered)',
        replace="kept = lowered",
    ),
    dict(
        label="m6 C06 no longer skips a match followed by *",
        module=DOC_STALENESS,
        find='if tail[:1] == "*":\n                    continue',
        replace='if False:\n                    continue',
    ),
    dict(
        label="m7 C07 reads a span whose first segment is not a key prefix",
        module=DOC_STALENESS,
        find="                if first not in prefixes:\n                    continue\n                if span in truth.command_ids:",
        replace="                if False:\n                    continue\n                if span in truth.command_ids:",
    ),
    dict(
        label="m8 C08 drops the table prefix and checks the bare name",
        module=DOC_STALENESS,
        find='full_key = f"{prefix}.{name}" if prefix else name',
        replace="full_key = name",
    ),
    dict(
        label="m9 C09 writes the folder guides as guides",
        module=DOC_STALENESS,
        find='expected = "guide" if folder == "guides" else folder',
        replace="expected = folder",
    ),
    dict(
        label="m10 C10 accepts a path without checking that it exists",
        module=DOC_STALENESS,
        find="if not (root / candidate).is_file():",
        replace="if False:",
    ),
    dict(
        label="m11 C11 reads a span whose first segment is a key prefix",
        module=DOC_STALENESS,
        find="if group_id is None or first in prefixes:",
        replace="if group_id is None:",
    ),
    dict(
        label="m12 C12 reads only the catalog's descriptions and no ArgDef.help",
        module=DOC_STALENESS,
        find="for arg in c.args:",
        replace="for arg in ():",
    ),
    dict(
        label="m13 fences are no longer skipped by C04",
        module=DOC_STALENESS,
        find=(
            "        guide_dir = (root / document).parent\n"
            "        for line_no, line in _iter_lines_outside_fences(text):"
        ),
        replace=(
            "        guide_dir = (root / document).parent\n"
            "        for line_no, line in enumerate(text.splitlines(), start=1):"
        ),
    ),
    dict(
        label="m14 Tier 2 ignores the keys the queue already targets",
        module=SELF_USE_GENERATOR,
        find="claim = next((c for c in claims if c.key not in targeted), None)",
        replace="claim = next((c for c in claims), None)",
    ),
    dict(
        label="m15 generate_self_use_item tries Tier 3 before Tier 2",
        module=SELF_USE_GENERATOR,
        find=(
            "    doc_result = _doc_staleness_tier(queue_path)\n"
            "    if doc_result is not None:\n"
            "        return doc_result\n"
            "\n"
            "    return _doctor_warning_tier(queue_path)"
        ),
        replace=(
            "    doctor_result = _doctor_warning_tier(queue_path)\n"
            "    if doctor_result is not None:\n"
            "        return doctor_result\n"
            "\n"
            "    return _doc_staleness_tier(queue_path)"
        ),
    ),
    dict(
        label="m16 Tier 2 accepts a claim holding a line break",
        module=SELF_USE_GENERATOR,
        find='if "\\n" in claim.claim or "\\n" in claim.truth:',
        replace="if False:",
    ),
    dict(
        label="m17 Tier 2 writes the truth on the Claim line and the claim on the Shipped truth line",
        module=SELF_USE_GENERATOR,
        find=(
            'f"Claim: {claim.claim}\\n"\n'
            '        f"Shipped truth: {claim.truth}\\n"'
        ),
        replace=(
            'f"Claim: {claim.truth}\\n"\n'
            '        f"Shipped truth: {claim.claim}\\n"'
        ),
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
