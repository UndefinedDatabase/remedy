#!/usr/bin/env python3
"""F035 R4 G5 — the round's red-proof tool (DECISION F035 D4).

Usage: ``python3 -B .agent/authored/f035-r4-mutations.py <worktree-path>``.

Takes the path of a disposable worktree, and for each mutation below: reads the named
file INSIDE that worktree, asserts its FROM text occurs exactly once, writes the TO
text in its place, purges every ``__pycache__`` directory under the worktree, runs the
round's test selection from the worktree's own root, restores the file's ORIGINAL bytes
(never a reversed edit — the saved original is written back verbatim), and prints one
line naming the mutation, its exit code, its failed-test count and its failing node ids.
An unmutated control run brackets the eight mutations, first and last, and the tool ends
by stating whether every mutated file came back byte-identical to what it read before
editing, and whether every mutation was caught.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

TEST_SELECTION = (
    "tests/orchestration/test_ownership_phrases.py",
    "tests/cli/test_job_ownership.py",
    "tests/ui_server/test_ownership_route.py",
)

OWNERSHIP_PHRASES = "packages/orchestration/ownership_phrases.py"
JOB_OWNERSHIP_CMD = "apps/cli/commands/job_ownership_cmd.py"
UI_SERVER = "packages/orchestration/ui_server.py"

MUTATIONS = [
    ("m1", OWNERSHIP_PHRASES,
     "plan_delete_task reads with the unknown-command fallback",
     '        if command == "plan_delete_task":',
     '        if command == "plan_delete_task_mutated":'),
    ("m2", OWNERSHIP_PHRASES,
     "the version keeps its leading v",
     '    n = ref[1:] if ref.startswith("v") else ref',
     '    n = ref'),
    ("m3", OWNERSHIP_PHRASES,
     "ownership_view leaves out each entry's sentence",
     '        entries = [\n'
     '            {**entry, "sentence": ownership_sentence(entry, titles=titles)}\n'
     '            for entry in ledger.get("entries", [])\n'
     '        ]',
     '        entries = [dict(entry) for entry in ledger.get("entries", [])]'),
    ("m4", OWNERSHIP_PHRASES,
     "ownership_view answers an empty error when the ledger raises",
     '            "error": f"The ownership ledger could not be read: {exc}",',
     '            "error": "",'),
    ("m5", JOB_OWNERSHIP_CMD,
     "an unknown job exits 1 instead of 3",
     "EXIT_NOT_READY = 3",
     "EXIT_NOT_READY = 1"),
    ("m6", JOB_OWNERSHIP_CMD,
     "a ledger error exits 0 and prints nothing",
     '    view = ownership_view(job)\n'
     '    if view["error"]:\n'
     '        fail("ownership_unreadable", view["error"], json_output=json_output, job_id=job_id)',
     '    view = ownership_view(job)\n'
     '    if view["error"]:\n'
     '        return'),
    ("m7", JOB_OWNERSHIP_CMD,
     "a job with no entry prints nothing",
     '    entries = view["entries"]\n'
     '    if not entries:\n'
     '        print(f"No action is recorded for job {job_id} yet.")\n'
     '        return',
     '    entries = view["entries"]\n'
     '    if not entries:\n'
     '        return'),
    ("m8", UI_SERVER,
     "the ownership key is left out of the handlers table",
     '                "ownership": _build_ownership_json,\n',
     ''),
]

FAILED_RE = re.compile(r"(\d+) failed")
FAILED_NODE_RE = re.compile(r"^FAILED (\S+)", re.MULTILINE)


def _purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        if cache_dir.is_dir():
            for child in cache_dir.rglob("*"):
                if child.is_file():
                    child.unlink()
            for child in sorted(cache_dir.rglob("*"), reverse=True):
                if child.is_dir():
                    child.rmdir()
            cache_dir.rmdir()


def _run_selection(root: Path) -> tuple[int, str]:
    _purge_pycache(root)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         *TEST_SELECTION],
        cwd=str(root), capture_output=True, text=True, timeout=600,
    )
    return proc.returncode, proc.stdout + proc.stderr


def _report(label: str, exit_code: int, output: str) -> None:
    m = FAILED_RE.search(output)
    failed_count = int(m.group(1)) if m else 0
    node_ids = FAILED_NODE_RE.findall(output)
    print(f"{label}: exit={exit_code} failed={failed_count} nodes={node_ids}")


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    all_ok = True
    restored_identical = True

    exit_code, output = _run_selection(root)
    _report("control (before)", exit_code, output)
    if exit_code != 0:
        all_ok = False

    for label, rel_path, description, from_text, to_text in MUTATIONS:
        target = root / rel_path
        original = target.read_text(encoding="utf-8")
        assert original.count(from_text) == 1, (
            f"{label}: FROM text does not occur exactly once in {rel_path}")
        mutated = original.replace(from_text, to_text, 1)
        target.write_text(mutated, encoding="utf-8")
        try:
            exit_code, output = _run_selection(root)
        finally:
            target.write_text(original, encoding="utf-8")
        restored = target.read_text(encoding="utf-8")
        if restored != original:
            restored_identical = False
        m = FAILED_RE.search(output)
        failed_count = int(m.group(1)) if m else 0
        node_ids = FAILED_NODE_RE.findall(output)
        print(f"{label} ({description}): exit={exit_code} failed={failed_count} "
              f"nodes={node_ids}")
        if exit_code == 0 or failed_count < 1:
            all_ok = False

    exit_code, output = _run_selection(root)
    _report("control (after)", exit_code, output)
    if exit_code != 0:
        all_ok = False

    print(f"restored byte-identical: {restored_identical}")
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: "
          f"{bool(all_ok and restored_identical)}")
    return 0 if (all_ok and restored_identical) else 1


if __name__ == "__main__":
    raise SystemExit(main())
