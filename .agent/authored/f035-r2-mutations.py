#!/usr/bin/env python3
"""F035 R2 G5 — the round's red-proof tool. Mutates one FROM text to TO text inside a target
worktree, asserting the FROM text occurs exactly once in its file, runs the two ownership test
files from the worktree root, restores the original bytes, and reports whether each mutation was
caught. `__pycache__` directories are purged before every run so a stale `.pyc` never masks a
live edit. An unmutated control run happens first and last; the tool ends by reporting whether
both mutated files came back byte-identical to what this process first read, and whether every
mutation below was caught.

Usage: `python3 -B .agent/authored/f035-r2-mutations.py <worktree-path>`
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

OWNERSHIP = "packages/orchestration/ownership.py"
PINGPONG = "packages/orchestration/pingpong_job.py"

TEST_ARGS = [
    "tests/orchestration/test_ownership_ledger.py",
    "tests/orchestration/test_pingpong_job_ownership.py",
]

# (label, relative path, FROM text, TO text) — FROM must occur exactly once in the file.
MUTATIONS: list[tuple[str, str, str, str]] = [
    ("m1: a pending hunk row yields an entry", OWNERSHIP,
     '                continue                                          # HUNK_STATE_PENDING: undecided\n',
     '                action = "hunk_pending"                          # MUTATED: pending yields\n'),
    ('m2: a hunk entry\'s text is ""', OWNERSHIP,
     '                "text": row.get("reason", "") if isinstance(row.get("reason"), str) else "",\n',
     '                "text": "",\n'),
    ("m3: a default decision answer is attributed to the operator", OWNERSHIP,
     '            actor = ownership_actor(answer_source, kind="default_policy")\n',
     '            actor = ownership_actor(answer_source, kind="operator")\n'),
    ("m4: an open decision yields an entry", OWNERSHIP,
     '        if not isinstance(record, dict) or record.get("status") != ESCALATION_STATUS_ANSWERED:\n'
     '            continue\n',
     '        if not isinstance(record, dict):\n'
     '            continue\n'),
    ("m5: the planner's clarification is attributed to the operator", OWNERSHIP,
     '_CLARIFICATION_ACTOR_KIND = {"human": "operator", "default": "default_policy", "planner": "remedy"}\n',
     '_CLARIFICATION_ACTOR_KIND = {"human": "operator", "default": "default_policy", "planner": "operator"}\n'),
    ("m6: an unresolved clarification yields an entry", OWNERSHIP,
     '        if source == "unresolved":\n            continue\n',
     '        if source == "MUTATED_NEVER_MATCHES":\n            continue\n'),
    ("m7: an unattended plan approval is not auto_approved", OWNERSHIP,
     '    return ownership_actor(mode, auto_approved=True), text\n',
     '    return ownership_actor(mode, auto_approved=False), text\n'),
    ("m8: the run-log dedupe keys on the request id alone again", OWNERSHIP,
     '        ref = request_id if request_id else raw_ts\n        key = (name, ref)\n',
     '        ref = request_id if request_id else raw_ts\n        key = (name, request_id)\n'),
    ("m9: a rejected plan yields no entry", OWNERSHIP,
     '    if approval == "rejected":\n',
     '    if approval == "MUTATED_NEVER_MATCHES":\n'),
    ("m10: the decorator line is removed from run_job", PINGPONG,
     '@_writes_ownership_ledger\ndef run_job(\n',
     'def run_job(\n'),
    ("m11: an OwnershipError in the write propagates", PINGPONG,
     '    except (OwnershipError, OSError) as exc:\n',
     '    except (KeyError,) as exc:\n'),
    ("m12: the job-directory check is removed", PINGPONG,
     '    if not job_dir(job.job_id).is_dir():\n        return\n',
     '    if False:\n        return\n'),
]


def _purge_pycache(root: Path) -> None:
    for cache in root.rglob("__pycache__"):
        shutil.rmtree(cache, ignore_errors=True)


def _run_pytest(root: Path) -> tuple[int, int, list[str]]:
    _purge_pycache(root)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TEST_ARGS],
        cwd=str(root), capture_output=True, text=True,
    )
    failing_ids = [
        line[len("FAILED "):].split(" - ")[0]
        for line in proc.stdout.splitlines() if line.startswith("FAILED ")
    ]
    return proc.returncode, len(failing_ids), failing_ids


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: f035-r2-mutations.py <worktree-path>", file=sys.stderr)
        raise SystemExit(2)
    root = Path(sys.argv[1]).resolve()

    baseline = {rel: (root / rel).read_bytes() for rel in (OWNERSHIP, PINGPONG)}
    all_caught = True

    exit_code, failed, ids = _run_pytest(root)
    print(f"control (before): exit={exit_code} failed={failed} ids={ids}")
    if exit_code != 0:
        all_caught = False

    for label, rel_path, from_text, to_text in MUTATIONS:
        target = root / rel_path
        original = target.read_bytes()
        original_text = original.decode("utf-8")
        count = original_text.count(from_text)
        assert count == 1, f"{label}: FROM text occurs {count} times in {rel_path}, expected 1"
        mutated_text = original_text.replace(from_text, to_text, 1)
        target.write_text(mutated_text, encoding="utf-8")
        try:
            exit_code, failed, ids = _run_pytest(root)
        finally:
            target.write_bytes(original)
        caught = exit_code != 0 and failed >= 1
        if not caught:
            all_caught = False
        print(f"{label}: exit={exit_code} failed={failed} ids={ids}")

    exit_code, failed, ids = _run_pytest(root)
    print(f"control (after): exit={exit_code} failed={failed} ids={ids}")
    if exit_code != 0:
        all_caught = False

    restored_ok = all(
        (root / rel).read_bytes() == baseline[rel] for rel in (OWNERSHIP, PINGPONG)
    )
    print(f"restored byte-identical: {restored_ok}")
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_caught and restored_ok}")


if __name__ == "__main__":
    main()
