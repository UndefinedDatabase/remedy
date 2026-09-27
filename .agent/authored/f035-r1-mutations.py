#!/usr/bin/env python3
"""F035 R1 G5 — the ownership ledger's mutation tool (red proofs).

Takes one argument, a disposable worktree's path. For each mutation below it edits
``packages/orchestration/ownership.py`` INSIDE that worktree — asserting its FROM text occurs
exactly once — runs ``tests/orchestration/test_ownership_ledger.py`` from the worktree's root
after purging its ``__pycache__`` directories, restores the original bytes, and prints one line
per mutation: its label, the exit code, the failed count and the failing node ids. It runs an
UNMUTATED control first and last, and ends with ``restored byte-identical: True`` and
``ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>``.

Every mutation is a real behaviour change over the reader logic ``packages/orchestration/
ownership.py`` implements — never a comment or a docstring — so a mutation that leaves every
test green means the test suite has a hole, not that the mutation was cosmetic.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

TARGET_REL = "packages/orchestration/ownership.py"
TEST_REL = "tests/orchestration/test_ownership_ledger.py"

# Each (label, FROM, TO): FROM must occur exactly once in the unmutated file; TO replaces it.
MUTATIONS: list[tuple[str, str, str]] = [
    (
        "m1 ownership_actor maps cli to the door \"\"",
        'elif recorded == "cli":\n        door = "cli"',
        'elif recorded == "cli":\n        door = ""',
    ),
    (
        "m2 fingerprints numbered in sorted order of their text, not by first appearance",
        '    fingerprint_numbers: dict[str, int] = {}\n'
        '    next_number = 1\n'
        '    for entry in entries:\n'
        '        recorded_as = entry["actor"].get("recorded_as", "")',
        '    fingerprint_numbers: dict[str, int] = {}\n'
        '    next_number = 1\n'
        '    for entry in sorted(entries, key=lambda e: e["actor"].get("recorded_as", "")):\n'
        '        recorded_as = entry["actor"].get("recorded_as", "")',
    ),
    (
        "m3 an injection's auto_approved is always false",
        'auto_approved=bool(record.get("confirmed_unseen")))',
        'auto_approved=False)',
    ),
    (
        "m4 a folded veto's consequence drops its unreachable ids",
        '"task_ids": [str(t) for t in (value.get("unreachable_task_ids") or [])],\n'
        '                "ref": "",',
        '"task_ids": [],\n'
        '                "ref": "",',
    ),
    (
        "m5 a veto only in the control files is skipped",
        '    all_control_ids = {entry.task_id for entry in control_entries}\n'
        '    for entry in control_entries:\n'
        '        if entry.task_id in metadata:\n'
        '            continue                                          # already folded, read above',
        '    all_control_ids = {entry.task_id for entry in control_entries}\n'
        '    for entry in control_entries:\n'
        '        continue                                          # m5: skip every control-only veto',
    ),
    (
        "m6 an injection's own _edits entry is read as a plan_edited entry",
        '        if "injection" in entry:\n'
        '            continue                                          # (c)\'s own entry, not (e)\'s\n',
        '',
    ),
    (
        "m7 a steering record's consequence ignores its marker",
        'marker = consumptions.get(record["message_id"])\n        if marker is not None:',
        'marker = consumptions.get(record["message_id"])\n        marker = None\n        if marker is not None:',
    ),
    (
        "m8 a resume's actor is read from the event's source",
        '            actor = ownership_actor("")',
        '            actor = ownership_actor(md.get("source"))',
    ),
    (
        "m9 a second pause event for one request id yields a second entry",
        '        key = (name, request_id)\n        if key in seen:\n            continue\n        seen.add(key)',
        '        key = (name, request_id)\n        seen.add(key)',
    ),
    (
        "m10 entries with an empty ts sort first",
        'entries.sort(key=lambda e: (e["ts"] == "", e["ts"], e["record_ref"]))',
        'entries.sort(key=lambda e: (e["ts"] != "", e["ts"], e["record_ref"]))',
    ),
    (
        "m11 a veto reader error is swallowed and yields no veto entries",
        '    try:\n        control_entries = _tv.vetoed_tasks(job.job_id)\n'
        '    except _tv.TaskVetoError as exc:\n'
        '        raise OwnershipError(f"TaskVetoError: {exc}") from exc',
        '    try:\n        control_entries = _tv.vetoed_tasks(job.job_id)\n'
        '    except _tv.TaskVetoError:\n        return out',
    ),
    (
        "m12 ownership_entry_problems accepts an actor kind outside ACTOR_KINDS",
        '        if actor.get("kind") not in ACTOR_KINDS:\n'
        '            problems.append(f"actor kind {actor.get(\'kind\')!r} is outside {ACTOR_KINDS}")\n',
        '',
    ),
]


def _purge_pycache(root: Path) -> None:
    for cache in root.rglob("__pycache__"):
        shutil.rmtree(cache, ignore_errors=True)


def _run_tests(root: Path) -> tuple[int, int, list[str]]:
    """Runs the ownership test file from *root*. Answers (exit_code, failed_count, failing_ids)."""
    _purge_pycache(root)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rf",
         "--tb=no", TEST_REL],
        cwd=root, capture_output=True, text=True,
    )
    failing_ids = [
        line[len("FAILED "):].split(" - ")[0].strip()
        for line in proc.stdout.splitlines()
        if line.startswith("FAILED ")
    ]
    failed_count = len(failing_ids)
    return proc.returncode, failed_count, failing_ids


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f035-r1-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    target = root / TARGET_REL
    original = target.read_bytes()

    all_caught = True
    restored_byte_identical = True

    exit_code, failed_count, failing_ids = _run_tests(root)
    print(f"control (before any mutation): exit={exit_code} failed={failed_count} "
          f"failing={failing_ids}")
    if exit_code != 0 or failed_count != 0:
        all_caught = False

    for label, from_text, to_text in MUTATIONS:
        text = target.read_text(encoding="utf-8")
        occurrences = text.count(from_text)
        assert occurrences == 1, (
            f"{label}: FROM text occurs {occurrences} times, expected exactly 1")
        mutated = text.replace(from_text, to_text, 1)
        target.write_text(mutated, encoding="utf-8")

        exit_code, failed_count, failing_ids = _run_tests(root)
        print(f"{label}: exit={exit_code} failed={failed_count} failing={failing_ids}")
        if exit_code == 0 or failed_count == 0:
            all_caught = False

        target.write_bytes(original)
        if target.read_bytes() != original:
            restored_byte_identical = False

    exit_code, failed_count, failing_ids = _run_tests(root)
    print(f"control (after every mutation restored): exit={exit_code} failed={failed_count} "
          f"failing={failing_ids}")
    if exit_code != 0 or failed_count != 0:
        all_caught = False

    print(f"restored byte-identical: {restored_byte_identical}")
    overall = all_caught and restored_byte_identical
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {overall}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
