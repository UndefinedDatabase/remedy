"""F028 R2 G5 — mutation (red-proof) tool for the confirmation, the apply, the plan_add_task
edit and the runner's fold of a confirmed injection (DECISION F028 D2): S1's expiry checks,
S3's confirmation refusal ladder, S4's provenance/version/hash/DoD bookkeeping, S2's
duplicate-id guard, and S5's four fold points and its already-folded/control-error handling.

Takes a worktree path and, for each mutation below, edits the named file INSIDE that
worktree (asserting its FROM text occurs exactly once in the file at the time of the edit
— every mutation starts from the file's own pristine bytes, restored after the previous
mutation), runs `tests/orchestration/test_task_injection.py`,
`tests/orchestration/test_task_injection_runner.py` and
`tests/orchestration/test_plan_editing.py` from the worktree's root under pytest — after
purging every `__pycache__` directory under it, so a stale bytecode file cannot hide or
fake a result — then restores the file's exact original bytes. An unmutated CONTROL run
happens first and last. Every mutation is a real behaviour change the specification (S1 to
S6) forbids, and every one of them must turn at least one node red.

Usage:
    python3 -B mutations.py <worktree_path>
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_TEST_PATHS = (
    "tests/orchestration/test_task_injection.py",
    "tests/orchestration/test_task_injection_runner.py",
    "tests/orchestration/test_plan_editing.py",
)

_TASK_INJECTION = "packages/orchestration/task_injection.py"
_PLAN_EDITING = "packages/orchestration/plan_editing.py"
_PINGPONG_JOB = "packages/orchestration/pingpong_job.py"

#: (label, file, FROM text, TO text). FROM must occur exactly once in the file at the time
#: of the edit; every mutation starts from the file's own pristine bytes, restored after the
#: previous mutation to THAT file.
MUTATIONS: tuple[tuple[str, str, str, str], ...] = (
    (
        "m1_read_injection_draft_treats_a_missing_expiry_as_live",
        _TASK_INJECTION,
        '    if not isinstance(expires_at, str) or not expires_at:\n'
        '        raise TaskInjectionError(\n'
        '            f"the injection draft entry for {draft_id!r} carries no readable expiry")\n',
        '    if not isinstance(expires_at, str) or not expires_at:\n'
        '        expires_at = "9999-01-01T00:00:00+00:00"\n',
    ),
    (
        "m2_confirm_task_injection_skips_the_status_check",
        _TASK_INJECTION,
        '    if record.get("status") != "confirmable":\n',
        '    if False and record.get("status") != "confirmable":\n',
    ),
    (
        "m3_confirm_task_injection_skips_the_task_id_half_of_the_stale_check",
        _TASK_INJECTION,
        '    if task["id"] in known_ids:\n',
        '    if False and task["id"] in known_ids:\n',
    ),
    (
        "m4_apply_injection_to_job_omits_origin",
        _TASK_INJECTION,
        '    fresh.inputs["plan"]["origin"] = ORIGIN_HUMAN_INJECTED\n',
        '',
    ),
    (
        "m5_apply_injection_to_job_never_reseals_the_approval_hash",
        _TASK_INJECTION,
        '    if body.get("_approval") == "approved" and body.get(APPROVED_PLAN_HASH_KEY):\n',
        '    if False and body.get("_approval") == "approved" '
        'and body.get(APPROVED_PLAN_HASH_KEY):\n',
    ),
    (
        "m6_apply_injection_to_job_leaves_the_plan_version_unchanged",
        _TASK_INJECTION,
        '    new_body[PLAN_VERSION_KEY] = version + 1\n',
        '    new_body[PLAN_VERSION_KEY] = version\n',
    ),
    (
        "m7_apply_injection_to_job_writes_dod_resync_pending_false_always",
        _TASK_INJECTION,
        '    dod_resync_pending = job_dod_path(job.job_id).is_file()\n',
        '    dod_resync_pending = False\n',
    ),
    (
        "m8_add_task_admits_a_duplicate_id",
        _PLAN_EDITING,
        '    if any(t.id == task.id for t in tasks):\n',
        '    if False and any(t.id == task.id for t in tasks):\n',
    ),
    (
        "m9_fold_point_a_is_removed",
        _PINGPONG_JOB,
        '        # F028 D2 (3): the injection fold runs at the same point, right after the veto\n'
        '        # fold — a confirmed injection waiting before this episode started joins task 1.\n'
        '        if _fold_task_injections(job, _control):\n'
        '            return job\n'
        '\n'
        '        tasks_run = 0\n',
        '        tasks_run = 0\n',
    ),
    (
        "m10_fold_point_c_is_removed",
        _PINGPONG_JOB,
        '            # F028 D2 (3): the injection fold\'s third point — the last statement of the\n'
        '            # loop body — so a task confirmed while an earlier one ran is folded before the\n'
        '            # NEXT iteration checks it (never later than one task late).\n'
        '            if _fold_task_injections(job, _control):\n'
        '                return job\n'
        '\n'
        '        # F028 D2 (3): the injection fold\'s fourth and last point, once the loop has ended.\n',
        '        # F028 D2 (3): the injection fold\'s fourth and last point, once the loop has ended.\n',
    ),
    (
        "m11_fold_point_d_no_longer_sets_job_paused",
        _PINGPONG_JOB,
        '        if len(job.tasks) > _tasks_before_injection_terminal_fold:\n'
        '            job.state = JOB_PAUSED\n',
        '        if False and len(job.tasks) > _tasks_before_injection_terminal_fold:\n'
        '            job.state = JOB_PAUSED\n',
    ),
    (
        "m12_the_fold_ignores_task_injections_and_folds_every_record",
        _PINGPONG_JOB,
        '        if draft_id in task_injections:\n'
        '            continue                                          # already folded\n',
        '        if False and draft_id in task_injections:\n'
        '            continue                                          # already folded\n',
    ),
    (
        "m13_the_folds_taskinjectionerror_branch_answers_false_without_blocking",
        _PINGPONG_JOB,
        '    except _ti.TaskInjectionError as exc:\n'
        '        job.state = JOB_BLOCKED\n'
        '        job.error = f"task_injection_control_error: {exc}"\n'
        '        _persist_job(job)\n'
        '        return True\n',
        '    except _ti.TaskInjectionError as exc:\n'
        '        return False\n',
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
