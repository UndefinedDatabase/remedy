"""F028 R5 G5 — mutation (red-proof) tool for the write door's three injection commands,
R-1078's repair, the door's own `after` resolver, and the run-log event a folded injection
writes.

Takes a worktree path and, for each mutation below, edits the named file INSIDE that
worktree (asserting its FROM text occurs exactly once in the file at the time of the edit —
every mutation starts from the file's own pristine bytes, restored after the previous
mutation to THAT file), runs the fixed test selection from the worktree's root under pytest
— after purging every `__pycache__` directory under it, so a stale bytecode file cannot hide
or fake a result — then restores the file's exact original bytes. An unmutated CONTROL run
happens first and last. Every mutation is a real behaviour change S1 to S5 forbid, and every
one of them must turn at least one node red.

Usage:
    python3 -B mutations.py <worktree_path>
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_TEST_PATHS = (
    "tests/cli/test_job_inject.py",
    "tests/orchestration/test_task_injection.py",
    "tests/orchestration/test_task_injection_runner.py",
    "tests/ui_server/test_command_dispatch.py",
    "tests/ui_server/test_command_channel.py",
)

_JOB_INJECT_CMD = "apps/cli/commands/job_inject_cmd.py"
_TASK_INJECTION = "packages/orchestration/task_injection.py"
_UI_SERVER = "packages/orchestration/ui_server.py"
_PINGPONG_JOB = "packages/orchestration/pingpong_job.py"

#: (label, file, FROM text, TO text). FROM must occur exactly once in the file at the time of
#: the edit; every mutation starts from the file's own pristine bytes, restored after the
#: previous mutation to THAT file.
MUTATIONS: tuple[tuple[str, str, str, str], ...] = (
    (
        "m1_yes_json_over_a_shortfall_emits_ok_before_fail_again",
        _JOB_INJECT_CMD,
        '        if yes:\n'
        '            # R-1078\'s repair: `--yes` over a shortfall never emits `emit_ok`\'s '
        'envelope\n'
        '            # first — under `--json` a caller must be able to parse stdout as '
        'exactly one\n'
        '            # JSON document, so this fails straight into `draft_needs_decision`\'s '
        'own\n'
        '            # envelope, carrying what the seed carries.\n'
        '            if not json_output:\n'
        '                _print_shortfall(job_id, answer)\n'
        '            fail("draft_needs_decision",\n',
        '        if yes:\n'
        '            if json_output:\n'
        '                emit_ok(**answer)\n'
        '            else:\n'
        '                _print_shortfall(job_id, answer)\n'
        '            fail("draft_needs_decision",\n',
    ),
    (
        "m2_resolve_after_ref_never_maps_an_entry_id_to_its_planned_id",
        _TASK_INJECTION,
        '    entry = next((t for t in getattr(job, "tasks", None) or [] if t.task_id == ref), '
        'None)\n'
        '    if entry is None:\n'
        '        return ref\n'
        '    planned_id = (entry.inputs.get("plan") or {}).get("planned_id")\n'
        '    return planned_id if planned_id else ref\n',
        '    entry = next((t for t in getattr(job, "tasks", None) or [] if t.task_id == ref), '
        'None)\n'
        '    if entry is None:\n'
        '        return ref\n'
        '    return ref\n',
    ),
    (
        "m3_the_doors_job_inject_check_never_calls_validate_injection_text",
        _UI_SERVER,
        '        if command == JOB_INJECT_COMMAND_ID:\n'
        '            from packages.orchestration.task_injection import (\n'
        '                TaskInjectionRefused,\n'
        '                validate_injection_text,\n'
        '            )\n'
        '\n'
        '            try:\n'
        '                validate_injection_text(args.get("text"))\n'
        '            except TaskInjectionRefused as exc:\n'
        '                return None, _command_field_error("text", exc.detail)\n'
        '            after = args.get("after")\n',
        '        if command == JOB_INJECT_COMMAND_ID:\n'
        '            after = args.get("after")\n',
    ),
    (
        "m4_the_doors_option_check_admits_any_string",
        _UI_SERVER,
        '            if args.get("option") not in SHORTFALL_OPTIONS:\n'
        '                return None, _command_field_error(\n'
        '                    "option", f"option must be one of '
        '{\', \'.join(SHORTFALL_OPTIONS)}")\n',
        '            if False:\n'
        '                return None, _command_field_error(\n'
        '                    "option", f"option must be one of '
        '{\', \'.join(SHORTFALL_OPTIONS)}")\n',
    ),
    (
        "m5_dispatch_injection_passes_after_unresolved",
        _UI_SERVER,
        '        if command == JOB_INJECT_COMMAND_ID:\n'
        '            result = draft_task_injection(\n'
        '                job, args["text"], call_fn=injection_call_fn(), budgets=budgets,\n'
        '                counters=counters, config=config, actor=actor,\n'
        '                after=resolve_after_ref(job, args.get("after")))\n',
        '        if command == JOB_INJECT_COMMAND_ID:\n'
        '            result = draft_task_injection(\n'
        '                job, args["text"], call_fn=injection_call_fn(), budgets=budgets,\n'
        '                counters=counters, config=config, actor=actor,\n'
        '                after=args.get("after"))\n',
    ),
    (
        "m6_dispatch_injection_names_the_actor_cli",
        _UI_SERVER,
        '        args = payload["args"]\n'
        '        command = payload["command"]\n'
        '        actor = token_fingerprint(self._supplied_bearer_token())\n',
        '        args = payload["args"]\n'
        '        command = payload["command"]\n'
        '        actor = "cli"\n',
    ),
    (
        "m7_the_injection_branch_answers_a_refusal_with_200",
        _UI_SERVER,
        '            if accepted_body.get("outcome") == "refused":\n'
        '                self._audit_attempt(str(job.job_id), "rejected_state", create=True,\n'
        '                                    payload=payload)\n'
        '                self._send_json(*_safe_error(\n'
        '                    409, f"{accepted_body[\'code\']}: {accepted_body[\'detail\']}"))\n'
        '                return\n'
        '            # D18, clause three: both writes below fail SOFT. The injection is '
        'already\n',
        '            if False:\n'
        '                self._audit_attempt(str(job.job_id), "rejected_state", create=True,\n'
        '                                    payload=payload)\n'
        '                self._send_json(*_safe_error(\n'
        '                    409, f"{accepted_body[\'code\']}: {accepted_body[\'detail\']}"))\n'
        '                return\n'
        '            # D18, clause three: both writes below fail SOFT. The injection is '
        'already\n',
    ),
    (
        "m8_the_fold_writes_no_event_for_an_applied_record",
        _PINGPONG_JOB,
        '        task_injections[draft_id] = applied\n'
        '        changed = True\n'
        '        folded_events.append({\n'
        '            "outcome": "applied", "task_id": applied["task_id"], "draft_id": '
        'draft_id,\n'
        '            "planned_id": planned_id, "basis": basis, "actor": actor,\n'
        '            "confirmed_unseen": confirmed_unseen,\n'
        '        })\n',
        '        task_injections[draft_id] = applied\n'
        '        changed = True\n',
    ),
    (
        "m9_the_fold_writes_the_event_for_an_inert_record_with_outcome_applied",
        _PINGPONG_JOB,
        '            folded_events.append({\n'
        '                "outcome": "inert", "task_id": "", "draft_id": draft_id,\n'
        '                "planned_id": planned_id, "basis": basis, "actor": actor,\n'
        '                "confirmed_unseen": confirmed_unseen, "reason": exc.detail,\n'
        '            })\n',
        '            folded_events.append({\n'
        '                "outcome": "applied", "task_id": "", "draft_id": draft_id,\n'
        '                "planned_id": planned_id, "basis": basis, "actor": actor,\n'
        '                "confirmed_unseen": confirmed_unseen, "reason": exc.detail,\n'
        '            })\n',
    ),
)


def _purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        if cache_dir.is_dir():
            for child in sorted(cache_dir.rglob("*"), reverse=True):
                if child.is_file():
                    child.unlink()
                else:
                    child.rmdir()
            cache_dir.rmdir()


def _run_tests(root: Path) -> tuple[int, int, list[str]]:
    """Run the fixed test selection from `root`. Returns (exit_code, failed_count, node_ids)."""
    _purge_pycache(root)
    result = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "--tb=no", *_TEST_PATHS],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    failed_ids = [
        line[len("FAILED "):].split(" ", 1)[0]
        for line in result.stdout.splitlines()
        if line.startswith("FAILED ")
    ]
    return result.returncode, len(failed_ids), failed_ids


def main(worktree: str) -> bool:
    root = Path(worktree).resolve()
    all_ok = True

    exit_code, failed_count, node_ids = _run_tests(root)
    control_ok = exit_code == 0 and failed_count == 0
    all_ok = all_ok and control_ok
    print(f"control (before): exit={exit_code} failed={failed_count} nodes={node_ids}")

    originals: dict[str, bytes] = {}
    for _, rel_path, _, _ in MUTATIONS:
        if rel_path not in originals:
            originals[rel_path] = (root / rel_path).read_bytes()

    for label, rel_path, from_text, to_text in MUTATIONS:
        target = root / rel_path
        pristine = originals[rel_path]
        text = pristine.decode("utf-8")
        occurrences = text.count(from_text)
        if occurrences != 1:
            raise AssertionError(
                f"{label}: FROM text occurs {occurrences} times in {rel_path}, expected 1")
        mutated_text = text.replace(from_text, to_text, 1)
        target.write_bytes(mutated_text.encode("utf-8"))

        exit_code, failed_count, node_ids = _run_tests(root)
        caught = exit_code != 0 and failed_count >= 1
        all_ok = all_ok and caught
        print(f"{label} ({rel_path}): exit={exit_code} failed={failed_count} nodes={node_ids}")
        if not caught:
            print(f"  {label}: STAYED GREEN — not caught by the test selection")

        target.write_bytes(pristine)

    for rel_path, pristine in originals.items():
        restored = (root / rel_path).read_bytes() == pristine
        all_ok = all_ok and restored
        print(f"restored byte-identical: {restored} ({rel_path})")

    exit_code, failed_count, node_ids = _run_tests(root)
    control_ok_after = exit_code == 0 and failed_count == 0
    all_ok = all_ok and control_ok_after
    print(f"control (after): exit={exit_code} failed={failed_count} nodes={node_ids}")

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return all_ok


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: mutations.py <worktree_path>")
    ok = main(sys.argv[1])
    raise SystemExit(0 if ok else 1)
