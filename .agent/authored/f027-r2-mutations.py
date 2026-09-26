#!/usr/bin/env python3
"""F027 R2 G5 — the red proofs for the linear runner's fold of a veto.

Takes a worktree path. For each mutation below: edits the named module INSIDE that worktree
(asserting its FROM text occurs exactly once), purges the worktree's ``__pycache__``
directories, runs ``tests/orchestration/test_task_veto_runner.py``,
``tests/orchestration/test_task_veto.py`` and ``tests/orchestration/test_worktrees.py`` from
the worktree's root, restores the bytes byte-identically, and reports the mutation's label,
the run's real exit code, the failed-test count and the failing node ids. Runs an unmutated
control first and last.

Usage:
    python3 -B .agent/authored/f027-r2-mutations.py <worktree-path>
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

PINGPONG_JOB = "packages/orchestration/pingpong_job.py"
WORKTREES = "packages/orchestration/worktrees.py"
RUN_MANIFEST = "packages/orchestration/run_manifest.py"
TASK_VETO = "packages/orchestration/task_veto.py"

TEST_RELS = [
    "tests/orchestration/test_task_veto_runner.py",
    "tests/orchestration/test_task_veto.py",
    "tests/orchestration/test_worktrees.py",
]

# Each mutation names one real behaviour this round adds: an exact FROM string, replaced by an
# exact TO string. FROM must occur exactly once in the pristine module.
MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "m1 the pre-task fold is removed, so only the fold before the loop runs",
        PINGPONG_JOB,
        "            # F027 D2 (1): the fold runs again at every pre-task safe point, right after\n"
        "            # the stop and the pause both found nothing — a veto beats neither.\n"
        "            if _fold_task_vetoes(job, job_handle, _control):\n"
        "                return job\n"
        "\n"
        "            if task.status == TASK_VETOED:\n",
        "            if task.status == TASK_VETOED:\n",
    ),
    (
        "m2 the fold never calls restore_tree",
        PINGPONG_JOB,
        "        if (job_handle is not None and task.task_attempt_state == \"active\"\n"
        "                and task.task_start_tree):\n"
        "            try:\n"
        "                _W.restore_tree(job_handle, task.task_start_tree)\n",
        "        if (False and job_handle is not None and task.task_attempt_state == \"active\"\n"
        "                and task.task_start_tree):\n"
        "            try:\n"
        "                _W.restore_tree(job_handle, task.task_start_tree)\n",
    ),
    (
        "m3 the loop dispatches an unreachable task",
        PINGPONG_JOB,
        "            _veto_ids_so_far = [t.task_id for t in job.tasks if t.status == TASK_VETOED]\n"
        "            if _veto_ids_so_far:\n"
        "                from packages.orchestration import task_veto as _tv\n"
        "                if task.task_id in _tv.veto_unreachable(job.tasks, _veto_ids_so_far):\n"
        "                    continue                   # unreachable behind a veto: never dispatched\n",
        "",
    ),
    (
        "m4 the fold never sends a skipped task back to pending",
        PINGPONG_JOB,
        "        if status_at_fold in (TASK_BLOCKED, TASK_FAILED):\n",
        "        if False and status_at_fold in (TASK_BLOCKED, TASK_FAILED):\n",
    ),
    (
        "m5 the fold sends every skipped task after the vetoed one back to pending, "
        "unreachable ones too",
        PINGPONG_JOB,
        "                if later.status == TASK_SKIPPED and later.task_id not in unreachable_now:\n",
        "                if later.status == TASK_SKIPPED:\n",
    ),
    (
        "m6 the terminal branch is removed",
        PINGPONG_JOB,
        "        _veto_terminal_vetoed_ids = [t.task_id for t in job.tasks if t.status == TASK_VETOED]\n"
        "        if _veto_terminal_vetoed_ids:\n"
        "            from packages.orchestration import task_veto as _tv\n"
        "\n"
        "            _veto_terminal_unreachable = list(\n"
        "                _tv.veto_unreachable(job.tasks, _veto_terminal_vetoed_ids))\n"
        "            _veto_terminal_unreachable_set = set(_veto_terminal_unreachable)\n"
        "            _veto_terminal_ready = all(\n"
        "                t.status in (TASK_APPLIED, TASK_PASSED, TASK_SKIPPED, TASK_SPLIT, TASK_VETOED)\n"
        "                or t.task_id in _veto_terminal_unreachable_set\n"
        "                for t in job.tasks\n"
        "            )\n"
        "            if _veto_terminal_ready:\n"
        "                for t in job.tasks:\n"
        "                    if t.status == TASK_PENDING and t.task_id in _veto_terminal_unreachable_set:\n"
        "                        t.status = TASK_SKIPPED\n"
        "                job.state = JOB_BLOCKED\n"
        "                job.error = (\n"
        "                    \"all_remaining_work_vetoed: \"\n"
        "                    f\"vetoed {', '.join(_veto_terminal_vetoed_ids) or 'none'}; \"\n"
        "                    f\"unreachable {', '.join(_veto_terminal_unreachable) or 'none'}\")\n"
        "                job.metadata[\"veto_terminal\"] = {\n"
        "                    \"vetoed\": list(_veto_terminal_vetoed_ids),\n"
        "                    \"unreachable\": list(_veto_terminal_unreachable),\n"
        "                }\n"
        "                _persist_budget_actuals()\n"
        "                _persist_job(job)\n"
        "                return job\n",
        "",
    ),
    (
        "m7 the terminal's error leaves out the unreachable set",
        PINGPONG_JOB,
        "                job.error = (\n"
        "                    \"all_remaining_work_vetoed: \"\n"
        "                    f\"vetoed {', '.join(_veto_terminal_vetoed_ids) or 'none'}; \"\n"
        "                    f\"unreachable {', '.join(_veto_terminal_unreachable) or 'none'}\")\n",
        "                job.error = (\n"
        "                    \"all_remaining_work_vetoed: \"\n"
        "                    f\"vetoed {', '.join(_veto_terminal_vetoed_ids) or 'none'}\")\n",
    ),
    (
        "m8 the fold vetoes a task whose status is outside VETOABLE_TASK_STATUSES",
        PINGPONG_JOB,
        "        if task is None or task.status not in _tv.VETOABLE_TASK_STATUSES:\n",
        "        if task is None:\n",
    ),
    (
        "m9 the fold swallows a TaskVetoError and dispatches on",
        PINGPONG_JOB,
        "    try:\n"
        "        entries = _tv.vetoed_tasks(job.job_id, control_root_path=control_root_path)\n"
        "    except _tv.TaskVetoError as exc:\n"
        "        job.state = JOB_BLOCKED\n"
        "        job.error = f\"task_veto_control_error: {exc}\"\n"
        "        _persist_job(job)\n"
        "        return True\n",
        "    try:\n"
        "        entries = _tv.vetoed_tasks(job.job_id, control_root_path=control_root_path)\n"
        "    except _tv.TaskVetoError:\n"
        "        entries = ()\n",
    ),
    (
        "m10 restore_tree never deletes a path the tree lacks",
        WORKTREES,
        "        if not mode:\n"
        "            # `tree` holds no entry here: delete it, and any directory the deletion\n"
        "            # leaves empty, up to (but never including) the worktree root.\n"
        "            if abs_path.is_symlink() or abs_path.is_file():\n"
        "                abs_path.unlink()\n"
        "            elif abs_path.is_dir():\n"
        "                shutil.rmtree(abs_path)\n",
        "        if not mode:\n"
        "            pass\n",
    ),
    (
        "m11 restore_tree drops the executable bit",
        WORKTREES,
        "            current_mode = os.stat(abs_path).st_mode\n"
        "            if mode == \"100755\":\n"
        "                os.chmod(abs_path, current_mode | 0o111)\n"
        "            else:\n"
        "                os.chmod(abs_path, current_mode & ~0o111)\n",
        "            current_mode = os.stat(abs_path).st_mode\n"
        "            os.chmod(abs_path, current_mode & ~0o111)\n",
    ),
    (
        "m12 \"vetoed\" is left out of VALID_TASK_STATUSES",
        RUN_MANIFEST,
        "VALID_TASK_STATUSES = frozenset({\"pending\", \"running\", \"passed\", "
        "\"applied_to_job_workspace\",\n"
        "                                 \"blocked\", \"failed\", \"skipped\", \"vetoed\"})\n",
        "VALID_TASK_STATUSES = frozenset({\"pending\", \"running\", \"passed\", "
        "\"applied_to_job_workspace\",\n"
        "                                 \"blocked\", \"failed\", \"skipped\"})\n",
    ),
    (
        "m13 the gate's task_already_vetoed route repairs no event (R-1065 as it stood)",
        TASK_VETO,
        "    if refusal is not None:\n"
        "        if refusal.code == \"task_already_vetoed\":\n"
        "            return _already_vetoed_refusal(job, task_id, existing, control_root_path)\n"
        "        return {\"outcome\": \"refused\", \"code\": refusal.code, \"detail\": refusal.detail,\n"
        "                \"task_id\": task_id}\n",
        "    if refusal is not None:\n"
        "        return {\"outcome\": \"refused\", \"code\": refusal.code, \"detail\": refusal.detail,\n"
        "                \"task_id\": task_id}\n",
    ),
    (
        "m14 the lost race answers {\"outcome\": \"task_already_vetoed\"} as before",
        TASK_VETO,
        "    if not created:\n"
        "        # A create-only race was lost: the SAME entry now exists under someone else's\n"
        "        # write. Answer it exactly as the gate's own route does (R-1065).\n"
        "        return _already_vetoed_refusal(job, task_id, veto, control_root_path)\n",
        "    if not created:\n"
        "        return {\"outcome\": \"task_already_vetoed\", \"request_id\": veto.request_id,\n"
        "                \"task_id\": task_id}\n",
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
        print("usage: f027-r2-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    print("--- control run (unmutated, before) ---")
    code, output = _run_tests(root)
    print(f"control: exit={code}")
    print(output.strip().splitlines()[-1] if output.strip() else "(no output)")
    if code != 0:
        print("CONTROL RUN IS NOT GREEN — aborting the mutation sweep.")
        return 1

    all_caught = True
    all_restored = True

    for label, rel_path, from_text, to_text in MUTATIONS:
        path = root / rel_path
        original = path.read_bytes()
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
        restored = path.read_bytes() == original
        all_restored = all_restored and restored
        print(f"restored byte-identical: {restored}")

    print("--- control run (unmutated, after) ---")
    code, output = _run_tests(root)
    print(f"control: exit={code}")
    print(output.strip().splitlines()[-1] if output.strip() else "(no output)")

    result = all_caught and all_restored and code == 0
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {result}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
