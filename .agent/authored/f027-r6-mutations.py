#!/usr/bin/env python3
"""F027 R6 G5 — the red proofs for the write door's veto, its answer of a replan
proposal, and the guard walker's `if TYPE_CHECKING:` skip (DECISION F027 D6).

Takes a worktree path. For each mutation below: edits the named file INSIDE that
worktree (asserting its FROM text occurs exactly once), purges the worktree's
``__pycache__`` directories, runs ``tests/ui_server/test_command_dispatch.py``,
``tests/ui_server/test_command_channel.py`` and
``tests/orchestration/test_decision_inbox.py`` from the worktree's root, restores the
bytes byte-identically, and reports the mutation's label, the run's real exit code, the
failed-test count and the failing node ids. Runs an unmutated control first and last,
and checks every touched file is restored byte-identical at the end.

Usage:
    python3 -B .agent/authored/f027-r6-mutations.py <worktree-path>
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

UI_SERVER = "packages/orchestration/ui_server.py"
DECISION_INBOX = "packages/orchestration/decision_inbox.py"
TEST_COMMAND_CHANNEL = "tests/ui_server/test_command_channel.py"

TEST_RELS = [
    "tests/ui_server/test_command_dispatch.py",
    "tests/ui_server/test_command_channel.py",
    "tests/orchestration/test_decision_inbox.py",
]

# Each mutation names one real behaviour this round adds: an exact FROM string, replaced
# by an exact TO string. FROM must occur exactly once in the pristine file.
MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "m1 the door's payload check lets a blank reason through to the job",
        UI_SERVER,
        '            try:\n'
        '                validate_veto_reason(args.get("reason"))\n'
        '            except TaskVetoRefused as exc:\n'
        '                return None, _command_field_error("reason", exc.detail)\n',
        '            try:\n'
        '                pass  # MUTATED (m1): reason no longer validated\n'
        '            except TaskVetoRefused as exc:\n'
        '                return None, _command_field_error("reason", exc.detail)\n',
    ),
    (
        "m2 the door's payload check is removed for task_id",
        UI_SERVER,
        '            task_id = args.get("task_id")\n'
        '            if not isinstance(task_id, str) or not task_id:\n'
        '                return None, _command_field_error(\n'
        '                    "task_id", "task_id must be a non-empty string")\n',
        '            task_id = args.get("task_id")\n'
        '            if False:  # MUTATED (m2): task_id shape check disabled\n'
        '                return None, _command_field_error(\n'
        '                    "task_id", "task_id must be a non-empty string")\n',
    ),
    (
        "m3 the door's clause answers a refused veto with a 200",
        UI_SERVER,
        '            if accepted_body.get("outcome") == "refused":\n'
        '                self._audit_attempt(str(job.job_id), "rejected_state", create=True,\n'
        '                                    payload=payload)\n'
        '                self._send_json(*_safe_error(\n'
        "                    409, f\"{accepted_body['code']}: {accepted_body['detail']}\"))\n"
        '                return\n',
        '            if False:  # MUTATED (m3): refused veto never answered 409\n'
        '                self._audit_attempt(str(job.job_id), "rejected_state", create=True,\n'
        '                                    payload=payload)\n'
        '                self._send_json(*_safe_error(\n'
        "                    409, f\"{accepted_body['code']}: {accepted_body['detail']}\"))\n"
        '                return\n',
    ),
    (
        "m4 the door's clause passes a fixed actor instead of the token fingerprint",
        UI_SERVER,
        '        result = veto_task_command(\n'
        '            job, task_id=args["task_id"], reason=args["reason"],\n'
        '            actor=token_fingerprint(self._supplied_bearer_token()))\n',
        '        result = veto_task_command(\n'
        '            job, task_id=args["task_id"], reason=args["reason"],\n'
        '            actor="fixed-actor")  # MUTATED (m4)\n',
    ),
    (
        "m5 the door's veto: branch is removed, so the answer falls to the escalation route",
        UI_SERVER,
        '        if isinstance(decision_id, str) and decision_id.startswith("veto:"):\n',
        '        if False and isinstance(decision_id, str) and decision_id.startswith("veto:"):'
        '  # MUTATED (m5)\n',
    ),
    (
        "m6 the inbox's veto: branch reads true for an answered proposal",
        DECISION_INBOX,
        '        return (any(e.request_id == request_id for e in entries)\n'
        '                and request_id not in answers)\n',
        '        return (any(e.request_id == request_id for e in entries)\n'
        '                and True)  # MUTATED (m6): answered check dropped\n',
    ),
    (
        "m7 the walker follows the body of an if TYPE_CHECKING: block again",
        TEST_COMMAND_CHANNEL,
        '                if isinstance(node, ast.If) and is_type_checking_test(node.test):\n'
        '                    pending.extend(node.orelse)\n'
        '                else:\n'
        '                    pending.extend(ast.iter_child_nodes(node))\n',
        '                if False and isinstance(node, ast.If) and is_type_checking_test('
        'node.test):  # MUTATED (m7)\n'
        '                    pending.extend(node.orelse)\n'
        '                else:\n'
        '                    pending.extend(ast.iter_child_nodes(node))\n',
    ),
    (
        "m8 the walker skips every if body, not only a type-only one",
        TEST_COMMAND_CHANNEL,
        '                if isinstance(node, ast.If) and is_type_checking_test(node.test):\n'
        '                    pending.extend(node.orelse)\n'
        '                else:\n'
        '                    pending.extend(ast.iter_child_nodes(node))\n',
        '                if isinstance(node, ast.If):  # MUTATED (m8): every if body skipped\n'
        '                    pending.extend(node.orelse)\n'
        '                else:\n'
        '                    pending.extend(ast.iter_child_nodes(node))\n',
    ),
]


def _purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        shutil.rmtree(cache_dir, ignore_errors=True)


def _run_tests(root: Path) -> tuple[int, str]:
    _purge_pycache(root)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TEST_RELS],
        cwd=str(root), capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def _failed_count_and_ids(output: str) -> tuple[int, list[str]]:
    ids = sorted(set(re.findall(r"^FAILED (\S+)", output, re.MULTILINE)))
    match = re.search(r"(\d+) failed", output)
    count = int(match.group(1)) if match else 0
    return count, ids


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f027-r6-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    touched_rels = sorted({rel for _, rel, _, _ in MUTATIONS})
    originals = {rel: (root / rel).read_bytes() for rel in touched_rels}

    print("--- control run (unmutated, before) ---")
    code, output = _run_tests(root)
    print(f"control: exit={code}")
    print(output.strip().splitlines()[-1] if output.strip() else "(no output)")
    if code != 0:
        print("CONTROL RUN IS NOT GREEN — aborting the mutation sweep.")
        return 1

    all_caught = True

    for label, rel_path, from_text, to_text in MUTATIONS:
        path = root / rel_path
        original = originals[rel_path]
        text = original.decode("utf-8")
        occurrences = text.count(from_text)
        if occurrences != 1:
            print(f"{label}: FROM text occurs {occurrences} times (expected 1) — aborting")
            return 1
        mutated = text.replace(from_text, to_text, 1)
        path.write_bytes(mutated.encode("utf-8"))
        try:
            code, output = _run_tests(root)
            failed_count, failing_ids = _failed_count_and_ids(output)
            caught = code != 0 and failed_count > 0
            all_caught = all_caught and caught
            tag = "" if caught else " — GREEN, NOT CAUGHT"
            print(f"{label}: exit={code} failed={failed_count} "
                  f"failing_node_ids={failing_ids}{tag}")
        finally:
            path.write_bytes(original)

    all_restored = True
    for rel_path in touched_rels:
        restored = (root / rel_path).read_bytes() == originals[rel_path]
        all_restored = all_restored and restored
        print(f"restored byte-identical: {restored} ({rel_path})")

    print("--- control run (unmutated, after) ---")
    code, output = _run_tests(root)
    print(f"control: exit={code}")
    print(output.strip().splitlines()[-1] if output.strip() else "(no output)")

    result = all_caught and all_restored and code == 0
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {result}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
