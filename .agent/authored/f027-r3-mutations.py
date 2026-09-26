#!/usr/bin/env python3
"""F027 R3 G5 — the red proofs for the in-flight veto and the cycle executor's veto.

Takes a worktree path. For each mutation below: edits the named module INSIDE that worktree
(asserting its FROM text occurs exactly once), purges the worktree's ``__pycache__``
directories, runs ``tests/orchestration/test_task_veto_runner.py``,
``tests/orchestration/test_task_veto_cycles.py`` and ``tests/orchestration/test_worktrees.py``
from the worktree's root, restores the bytes byte-identically, and reports the mutation's
label, the run's real exit code, the failed-test count and the failing node ids. Runs an
unmutated control first and last.

Usage:
    python3 -B .agent/authored/f027-r3-mutations.py <worktree-path>
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

PINGPONG_JOB = "packages/orchestration/pingpong_job.py"
LONG_RUN_EXECUTOR = "packages/orchestration/long_run_executor.py"
WORKTREES = "packages/orchestration/worktrees.py"

TEST_RELS = [
    "tests/orchestration/test_task_veto_runner.py",
    "tests/orchestration/test_task_veto_cycles.py",
    "tests/orchestration/test_worktrees.py",
]

# Each mutation names one real behaviour this round adds: an exact FROM string, replaced by an
# exact TO string. FROM must occur exactly once in the pristine module.
MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "m1 _run_stop_check never reads a veto",
        PINGPONG_JOB,
        "            _pause_sig = _pause_park_signal(in_flight_task=task)\n"
        "            if _pause_sig is not None:\n"
        "                return _pause_sig\n"
        "            # DECISION F027 D3 (1) THE IN-TASK READING: the stop and the pause\n"
        "            # both found nothing, so a veto of THIS in-flight task is read\n"
        "            # LAST — the call already running finishes and the loop halts at\n"
        "            # its own next safe point, never mid-call.\n"
        "            from packages.orchestration import task_veto as _tv\n"
        "            try:\n"
        "                _veto_entry = next(\n"
        "                    (e for e in _tv.vetoed_tasks(job.job_id, control_root_path=_control)\n"
        "                     if e.task_id == task.task_id), None)\n"
        "            except _tv.TaskVetoError as exc:\n"
        "                return _StopSignal(\n"
        "                    job_id=job.job_id, request_id=\"\",\n"
        "                    reason=f\"{_VETO_ERROR_REASON_PREFIX}{exc}\", source=\"veto\")\n"
        "            if _veto_entry is not None:\n"
        "                return _StopSignal(\n"
        "                    job_id=job.job_id, request_id=_veto_entry.request_id,\n"
        "                    reason=f\"{_VETO_REASON_PREFIX}{_veto_entry.request_id}\",\n"
        "                    source=\"veto\")\n"
        "            return None\n",
        "            _pause_sig = _pause_park_signal(in_flight_task=task)\n"
        "            if _pause_sig is not None:\n"
        "                return _pause_sig\n"
        "            return None\n",
    ),
    (
        "m2 the stopped branch lets a veto halt fall through to the stop path",
        PINGPONG_JOB,
        "                if _reason_is_veto(_halt_reason):\n",
        "                if False and _reason_is_veto(_halt_reason):\n",
    ),
    (
        "m3 the halt sets TASK_VETOED itself instead of calling the fold, so nothing is restored",
        PINGPONG_JOB,
        "                    if _fold_task_vetoes(job, job_handle, _control):\n"
        "                        return job\n"
        "                    if task.status == TASK_VETOED:\n",
        "                    task.status = TASK_VETOED\n"
        "                    if task.status == TASK_VETOED:\n",
    ),
    (
        "m4 the halt returns the job instead of continuing the loop",
        PINGPONG_JOB,
        "                    if task.status == TASK_VETOED:\n"
        "                        _log_task_ended(task_log, task, \"vetoed\")\n"
        "                        _persist_budget_actuals()\n"
        "                        _persist_job(job)\n"
        "                        continue\n",
        "                    if task.status == TASK_VETOED:\n"
        "                        _log_task_ended(task_log, task, \"vetoed\")\n"
        "                        _persist_budget_actuals()\n"
        "                        _persist_job(job)\n"
        "                        return job\n",
    ),
    (
        "m5 ready_tasks ignores vetoed_ids",
        LONG_RUN_EXECUTOR,
        "    vetoed_live = _veto_seeds(job, vetoed_ids)\n",
        "    vetoed_live = set()\n",
    ),
    (
        "m6 ready_tasks withholds the vetoed seeds but not their dependents",
        LONG_RUN_EXECUTOR,
        "    withheld_seeds = set(blocked_ids) | set(awaiting_ids) | paused_pending | vetoed_live\n"
        "    if withheld_seeds:\n"
        "        withheld = withheld_seeds | blocked_downstream(job.tasks, withheld_seeds)\n"
        "        ready = [task_id for task_id in ready if task_id not in withheld]\n"
        "    return ready[:batch_size]\n",
        "    withheld_seeds = set(blocked_ids) | set(awaiting_ids) | paused_pending\n"
        "    if withheld_seeds:\n"
        "        withheld = withheld_seeds | blocked_downstream(job.tasks, withheld_seeds)\n"
        "        ready = [task_id for task_id in ready if task_id not in withheld]\n"
        "    ready = [task_id for task_id in ready if task_id not in vetoed_live]\n"
        "    return ready[:batch_size]\n",
    ),
    (
        "m7 the cycle executor's veto terminal branch is removed",
        LONG_RUN_EXECUTOR,
        "                elif vetoed_ids and _veto_withholds_pending_work(job, vetoed_ids):\n"
        "                    # DECISION F027 D3 (3): the vetoed seeds withhold at least\n"
        "                    # one PENDING task (a seed itself or one of its transitive\n"
        "                    # dependents) and nothing else explains the empty batch —\n"
        "                    # the run ends here naming both sets, in plan order.\n"
        "                    terminal = TERMINAL_BLOCKED\n"
        "                    stop_reason = (\n"
        "                        \"all_remaining_work_vetoed; vetoed=\"\n"
        "                        + _plan_ordered_ids(job, _veto_seeds(job, vetoed_ids))\n"
        "                        + \"; unreachable=\"\n"
        "                        + _plan_ordered_ids(\n"
        "                            job, _veto_unreachable_ids(job, vetoed_ids))\n"
        "                    )\n",
        "",
    ),
    (
        "m8 the cycle executor swallows a TaskVetoError and picks on",
        LONG_RUN_EXECUTOR,
        "    try:\n"
        "        return _tv.vetoed_tasks(str(job.job_id), control_root_path=control_root_path)\n"
        "    except _tv.TaskVetoError as exc:\n"
        "        raise _TaskVetoErrorObserved(str(exc)) from exc\n",
        "    try:\n"
        "        return _tv.vetoed_tasks(str(job.job_id), control_root_path=control_root_path)\n"
        "    except _tv.TaskVetoError:\n"
        "        return ()\n",
    ),
    (
        "m9 ready_tasks seeds a vetoed task that is completed",
        LONG_RUN_EXECUTOR,
        "    return {\n"
        "        task_id for task_id in vetoed_ids\n"
        "        if (task := tasks_by_id.get(task_id)) is not None\n"
        "        and _task_status_str(task.status) != RunState.COMPLETED.value\n"
        "    }\n",
        "    return {\n"
        "        task_id for task_id in vetoed_ids\n"
        "        if (task := tasks_by_id.get(task_id)) is not None\n"
        "    }\n",
    ),
    (
        "m10 restore_tree removes nothing standing where the tree holds a file",
        WORKTREES,
        "            if abs_path.is_dir() and not abs_path.is_symlink():\n"
        "                # R-1066: a vetoed attempt replaced this file (or symlink) with a\n"
        "                # directory. Whatever stands here that is not the file `tree` holds\n"
        "                # is removed before the write, so the restore converges instead of\n"
        "                # raising `IsADirectoryError` out of `write_bytes`/`symlink_to`.\n"
        "                shutil.rmtree(abs_path)\n",
        "",
    ),
    (
        "m11 restore_tree lets an OSError escape unconverted",
        WORKTREES,
        "        except OSError as exc:\n"
        "            raise WorktreeError(f\"restore_tree failed at {rel_path!r}: {exc}\") from exc\n",
        "        except WorktreeError:\n"
        "            raise\n",
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
        print("usage: f027-r3-mutations.py <worktree-path>", file=sys.stderr)
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
