"""F288 R2 G5 — mutation (red-proof) tool for the run-next path's attempt id, the
test service's attempt id/task id/outcome, the plan-approved event and their
readers (DECISION F288 D2).

Takes a worktree path and, for each mutation below, edits the named file INSIDE
that worktree (asserting its FROM text occurs exactly once in the file at the
time of the edit — every mutation starts from the file's own pristine bytes,
restored after the previous mutation), runs the worktree's own
`tests/ui_server/test_sse_stream.py`, `tests/orchestration/test_teacher_narration.py`,
`tests/test_timeline.py`, `tests/orchestration/test_mint_call_sites.py`,
`tests/ui_contracts/test_humanize_catalog.py`, `tests/test_run_log_cli.py`,
`tests/orchestration/test_test_execution_service.py` and the node ids of the
classes this round added to `tests/orchestration/test_plan_editing.py`,
`tests/orchestration/test_orchestrator_loop.py` and
`tests/orchestration/test_do_run.py`, under pytest from the worktree's root —
after purging every `__pycache__` directory under it, so a stale bytecode file
cannot hide or fake a result — then restores the file's exact original bytes. An
unmutated CONTROL run happens first and last. Every mutation is a real behaviour
change the specification (S1 to S5) forbids, and every one of them must turn at
least one node red.

Usage:
    python3 -B f288-r2-mutations.py <worktree_path>
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

#: Run together for the control and for every mutation, from the worktree's root.
_TEST_PATHS = (
    "tests/ui_server/test_sse_stream.py",
    "tests/orchestration/test_teacher_narration.py",
    "tests/test_timeline.py",
    "tests/orchestration/test_mint_call_sites.py",
    "tests/ui_contracts/test_humanize_catalog.py",
    "tests/test_run_log_cli.py",
    "tests/orchestration/test_test_execution_service.py",
    "tests/orchestration/test_plan_editing.py::TestTheApprovalAnnouncesPlanApproved",
    "tests/orchestration/test_orchestrator_loop.py::TestAutoApproveIfGated",
    "tests/orchestration/test_do_run.py::TestYesPathAnnouncesPlanApproved",
)

_JOB_CMD = "apps/cli/commands/job.py"
_TEST_EXECUTION_SERVICE = "packages/orchestration/test_execution_service.py"
_JOB_PLAN = "packages/orchestration/job_plan.py"
_ORCHESTRATOR_LOOP = "packages/orchestration/orchestrator_loop.py"
_DO_SEQUENCE = "packages/orchestration/do_sequence.py"
_UI_SERVER = "packages/orchestration/ui_server.py"
_HUMANIZE_CATALOG = "apps/ui/src/api/humanizeCatalog.ts"

#: (label, relative file path, FROM text, TO text). FROM must occur exactly once
#: in the file at the time of the edit; every mutation starts from the file's own
#: pristine bytes, restored after the previous mutation.
MUTATIONS: tuple[tuple[str, str, str, str], ...] = (
    (
        "m1_run_next_task_run_started_carries_no_attempt_id",
        _JOB_CMD,
        '    log.log("task_run_started", task_id=str(pending_task.task_id) if pending_task else None,\n'
        "            task_type=pending_task_type, attempt_id=attempt_id)\n",
        '    log.log("task_run_started", task_id=str(pending_task.task_id) if pending_task else None,\n'
        "            task_type=pending_task_type)\n",
    ),
    (
        "m2_fails_task_run_failed_carries_no_attempt_id",
        _JOB_CMD,
        "    def _fail(outcome: str, **meta: object) -> None:\n"
        "        log.log(\n"
        '            "task_run_failed",\n'
        "            task_id=str(pending_task.task_id) if pending_task else None,\n"
        "            outcome=outcome, task_type=pending_task_type, attempt_id=attempt_id, **meta,\n"
        "        )\n",
        "    def _fail(outcome: str, **meta: object) -> None:\n"
        "        log.log(\n"
        '            "task_run_failed",\n'
        "            task_id=str(pending_task.task_id) if pending_task else None,\n"
        "            outcome=outcome, task_type=pending_task_type, **meta,\n"
        "        )\n",
    ),
    (
        "m3_task_run_completed_carries_a_second_freshly_minted_id",
        _JOB_CMD,
        '        log.log("task_run_completed", task_id=str(result.task_id), outcome="pass", attempt_id=attempt_id)\n',
        '        log.log("task_run_completed", task_id=str(result.task_id), outcome="pass", attempt_id=mint_run_id())\n',
    ),
    (
        "m4_test_service_omits_attempt_id_from_test_run_started",
        _TEST_EXECUTION_SERVICE,
        '    meta = dict(metadata)\n'
        '    meta["attempt_id"] = result.test_run_id\n'
        "    if result.linked_task_id:\n",
        '    meta = dict(metadata)\n'
        '    if event != "test_run_started":\n'
        '        meta["attempt_id"] = result.test_run_id\n'
        "    if result.linked_task_id:\n",
    ),
    (
        "m5_test_run_completed_carries_no_top_level_outcome",
        _TEST_EXECUTION_SERVICE,
        '    if event == "test_run_completed":\n'
        '        meta["outcome"] = result.status\n',
        '    if event == "test_run_completed_never":\n'
        '        meta["outcome"] = result.status\n',
    ),
    (
        "m6_test_run_blocked_carries_outcome_failed",
        _TEST_EXECUTION_SERVICE,
        '    elif event == "test_run_blocked":\n'
        '        meta["outcome"] = "blocked"\n',
        '    elif event == "test_run_blocked":\n'
        '        meta["outcome"] = "failed"\n',
    ),
    (
        "m7_the_requests_task_id_is_not_lifted_onto_test_run_requested",
        _TEST_EXECUTION_SERVICE,
        '    meta = dict(metadata)\n'
        '    meta["attempt_id"] = result.test_run_id\n'
        "    if result.linked_task_id:\n"
        '        meta["task_id"] = result.linked_task_id\n',
        '    meta = dict(metadata)\n'
        '    meta["attempt_id"] = result.test_run_id\n'
        '    if result.linked_task_id and event != "test_run_requested":\n'
        '        meta["task_id"] = result.linked_task_id\n',
    ),
    (
        "m8_resolve_task_plan_approval_announces_on_its_reject_branch_too",
        _JOB_PLAN,
        '    if reason != "approve":\n'
        '        fp["_approval"] = "rejected"\n'
        "        job.task_plan = fp\n"
        "        save_job_plan(job)\n"
        "        return None\n",
        '    if reason != "approve":\n'
        '        fp["_approval"] = "rejected"\n'
        "        job.task_plan = fp\n"
        "        save_job_plan(job)\n"
        '        announce_plan_approval(job, mode="human")\n'
        "        return None\n",
    ),
    (
        "m9_announce_plan_approval_lists_the_task_ids_in_reverse_order",
        _JOB_PLAN,
        '                "task_ids": [str(t.task_id) for t in job.tasks],\n',
        '                "task_ids": [str(t.task_id) for t in job.tasks][::-1],\n',
    ),
    (
        "m10_announce_plan_approval_lets_an_oserror_propagate",
        _JOB_PLAN,
        "    except (OSError, ValueError, TypeError):\n"
        "        logging.getLogger(__name__).warning(\n"
        '            "plan_approved event write failed for job %s", job.job_id)\n',
        "    except (ValueError, TypeError):\n"
        "        logging.getLogger(__name__).warning(\n"
        '            "plan_approved event write failed for job %s", job.job_id)\n',
    ),
    (
        "m11_auto_approve_if_gated_does_not_announce",
        _ORCHESTRATOR_LOOP,
        "    save_job_plan(job)\n"
        "    announce_plan_approval(job, mode=AUTO_APPROVAL_MODE)\n"
        "    return True\n",
        "    save_job_plan(job)\n"
        "    return True\n",
    ),
    (
        "m12_the_yes_branch_of_do_sequence_does_not_announce",
        _DO_SEQUENCE,
        "                save_job_plan(job)\n"
        "                announce_plan_approval(job, mode=AUTO_APPROVAL_MODE)\n"
        "                plan_label = (\n",
        "                save_job_plan(job)\n"
        "                plan_label = (\n",
    ),
    (
        "m13_the_envelopes_plan_block_keeps_non_string_entries",
        _UI_SERVER,
        '    task_ids = [t for t in raw if isinstance(t, str)] if isinstance(raw, list) else []\n',
        "    task_ids = list(raw) if isinstance(raw, list) else []\n",
    ),
    (
        "m14_attempt_event_kinds_loses_test_run_blocked",
        _UI_SERVER,
        '    "test_run_timed_out",\n'
        '    "test_run_blocked",\n'
        "})\n",
        '    "test_run_timed_out",\n'
        "})\n",
    ),
    (
        "m15_humanize_catalog_loses_its_plan_approved_line",
        _HUMANIZE_CATALOG,
        '  "plan_approved": "The plan was approved and its tasks were released.",\n',
        "",
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
    for _label, rel_path, _from_text, _to_text in MUTATIONS:
        if rel_path not in originals:
            originals[rel_path] = (root / rel_path).read_bytes()

    for label, rel_path, from_text, to_text in MUTATIONS:
        target = root / rel_path
        original_bytes = originals[rel_path]
        text = original_bytes.decode("utf-8")
        occurrences = text.count(from_text)
        if occurrences != 1:
            raise AssertionError(
                f"{label}: FROM text occurs {occurrences} times in {rel_path}, expected 1"
            )
        mutated_text = text.replace(from_text, to_text, 1)
        target.write_bytes(mutated_text.encode("utf-8"))

        exit_code, failed_count, node_ids = _run_tests(root)
        caught = exit_code != 0 and failed_count >= 1
        all_ok = all_ok and caught
        print(f"{label}: exit={exit_code} failed={failed_count} nodes={node_ids}")
        if not caught:
            print(f"  {label}: STAYED GREEN — not caught by the test selection")

        target.write_bytes(original_bytes)

    for rel_path, original_bytes in originals.items():
        restored = (root / rel_path).read_bytes() == original_bytes
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
        raise SystemExit("usage: f288-r2-mutations.py <worktree_path>")
    ok = main(sys.argv[1])
    raise SystemExit(0 if ok else 1)
