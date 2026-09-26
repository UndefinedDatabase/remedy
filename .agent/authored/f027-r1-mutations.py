#!/usr/bin/env python3
"""F027 R1 G5 — the red proofs for ``packages/orchestration/task_veto.py``.

Takes a worktree path. For each mutation below: edits the named module INSIDE that worktree
(asserting its FROM text occurs exactly once), purges the worktree's ``__pycache__``
directories, runs ``tests/orchestration/test_task_veto.py`` from the worktree's root, restores
the bytes byte-identically, and reports the mutation's label, the run's real exit code, the
failed-test count and the failing node ids. Runs an unmutated control first and last.

Usage:
    python3 -B .agent/authored/f027-r1-mutations.py <worktree-path>
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

MODULE_REL = "packages/orchestration/task_veto.py"
TEST_REL = "tests/orchestration/test_task_veto.py"

# Each mutation names a real behaviour change in task_veto.py: an exact FROM string, replaced
# by an exact TO string. FROM must occur exactly once in the pristine module.
MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "m1 a whitespace-only reason is accepted",
        MODULE_REL,
        "    if not isinstance(reason, str) or not reason.strip():\n",
        "    if not isinstance(reason, str):\n",
    ),
    (
        "m2 a 501-character reason is accepted",
        MODULE_REL,
        "    if len(reason) > MAX_VETO_REASON_CHARS:\n",
        "    if len(reason) > MAX_VETO_REASON_CHARS + 1:\n",
    ),
    (
        "m3 a reason holding a control character is accepted",
        MODULE_REL,
        "    if _CONTROL_CHAR_RE.search(reason) or redact_text(reason) != reason:\n",
        "    if redact_text(reason) != reason:\n",
    ),
    (
        "m4 a secret-shaped reason is accepted",
        MODULE_REL,
        "    if _CONTROL_CHAR_RE.search(reason) or redact_text(reason) != reason:\n",
        "    if _CONTROL_CHAR_RE.search(reason):\n",
    ),
    (
        "m5 an accepted reason is returned stripped",
        MODULE_REL,
        "    return reason\n",
        "    return reason.strip()\n",
    ),
    (
        "m6 the gate admits a completed job",
        MODULE_REL,
        '_JOB_TERMINAL_STATES = frozenset({"completed", "failed", "cancelled"})\n',
        '_JOB_TERMINAL_STATES = frozenset({"failed", "cancelled"})\n',
    ),
    (
        "m7 the gate admits an applied_to_job_workspace task",
        MODULE_REL,
        "VETOABLE_TASK_STATUSES = (TASK_PENDING, TASK_RUNNING, TASK_BLOCKED, TASK_FAILED, "
        "TASK_SKIPPED)\n",
        "VETOABLE_TASK_STATUSES = (TASK_PENDING, TASK_RUNNING, TASK_BLOCKED, TASK_FAILED, "
        'TASK_SKIPPED, "applied_to_job_workspace")\n',
    ),
    (
        "m8 the gate refuses a skipped task",
        MODULE_REL,
        "VETOABLE_TASK_STATUSES = (TASK_PENDING, TASK_RUNNING, TASK_BLOCKED, TASK_FAILED, "
        "TASK_SKIPPED)\n",
        "VETOABLE_TASK_STATUSES = (TASK_PENDING, TASK_RUNNING, TASK_BLOCKED, TASK_FAILED)\n",
    ),
    (
        "m9 the gate ignores already_vetoed",
        MODULE_REL,
        "    if already_vetoed or status == TASK_VETOED:\n",
        "    if status == TASK_VETOED:\n",
    ),
    (
        "m10 the control file is named by the task id itself instead of its digest",
        MODULE_REL,
        "    return f\"{digest}.json\"\n",
        "    return f\"{task_id}.json\"\n",
    ),
    (
        "m11 the unreachable set keeps a task whose work is done",
        MODULE_REL,
        "    return tuple(\n"
        "        task.task_id for task in tasks\n"
        "        if task.task_id in blocked and _state_str(task.status) in "
        "VETOABLE_TASK_STATUSES)\n",
        "    return tuple(\n"
        "        task.task_id for task in tasks\n"
        "        if task.task_id in blocked)\n",
    ),
    (
        "m12 the control file is published without create_only, so a second veto replaces "
        "the first",
        MODULE_REL,
        "        published = _fs.write_file_atomically(\n"
        "            tasks_fd, name, _fs.json_bytes(veto.to_json()), create_only=True,\n",
        "        published = _fs.write_file_atomically(\n"
        "            tasks_fd, name, _fs.json_bytes(veto.to_json()), create_only=False,\n",
    ),
    (
        "m13 the command writes the event without reading the ledger first",
        MODULE_REL,
        "    already = _task_vetoed_event_exists(job.job_id, veto.request_id)\n"
        "    if already is not None and not already:\n"
        "        _write_task_vetoed_event(job, veto, unreachable)\n",
        "    _write_task_vetoed_event(job, veto, unreachable)\n",
    ),
    (
        "m14 the command checks the task before the reason",
        MODULE_REL,
        "    try:\n"
        "        validated_reason = validate_veto_reason(reason)\n"
        "    except TaskVetoRefused as exc:\n"
        '        return {"outcome": "refused", "code": exc.code, "detail": exc.detail,\n'
        '                "task_id": task_id}\n'
        "\n"
        "    task = next((t for t in job.tasks if str(getattr(t, \"task_id\", \"\")) == "
        "task_id), None)\n"
        "    if task is None:\n"
        '        return {"outcome": "refused", "code": "unknown_task",\n'
        '                "detail": f"unknown task {task_id!r}", "task_id": task_id}\n',
        "    task = next((t for t in job.tasks if str(getattr(t, \"task_id\", \"\")) == "
        "task_id), None)\n"
        "    if task is None:\n"
        '        return {"outcome": "refused", "code": "unknown_task",\n'
        '                "detail": f"unknown task {task_id!r}", "task_id": task_id}\n'
        "\n"
        "    try:\n"
        "        validated_reason = validate_veto_reason(reason)\n"
        "    except TaskVetoRefused as exc:\n"
        '        return {"outcome": "refused", "code": exc.code, "detail": exc.detail,\n'
        '                "task_id": task_id}\n',
    ),
    (
        "m15 the command's unreachable set keeps another veto's tasks",
        MODULE_REL,
        "    other_ids = {v.task_id for v in vetoed_tasks(job.job_id, "
        "control_root_path=control_root_path)\n"
        "                if v.task_id != veto.task_id}\n"
        "    return [tid for tid in veto_unreachable(job.tasks, [veto.task_id]) if tid not "
        "in other_ids]\n",
        "    return list(veto_unreachable(job.tasks, [veto.task_id]))\n",
    ),
]

_SUMMARY_RE = re.compile(
    r"(?:(\d+) failed)?(?:.*?(\d+) passed)?.*?in [\d.]+s", re.DOTALL)


def _purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        shutil.rmtree(cache_dir, ignore_errors=True)


def _run_tests(root: Path) -> tuple[int, str]:
    _purge_pycache(root)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST_REL],
        cwd=str(root), capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def _failed_count_and_ids(output: str) -> tuple[int, list[str]]:
    ids = sorted(set(re.findall(r"^FAILED (\S+)", output, re.MULTILINE)))
    match = re.search(r"(\d+) failed", output)
    count = int(match.group(1)) if match else 0
    return count, ids


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f027-r1-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    module_path = root / MODULE_REL

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
            print(f"{label}: exit={code} failed={failed_count} "
                  f"failing_node_ids={failing_ids}")
        finally:
            path.write_bytes(original)
        restored = path.read_bytes() == original
        all_restored = all_restored and restored
        print(f"restored byte-identical: {restored}")

    print("--- control run (unmutated, after) ---")
    code, output = _run_tests(root)
    print(f"control: exit={code}")
    print(output.strip().splitlines()[-1] if output.strip() else "(no output)")
    all_restored = all_restored and (module_path.read_bytes() ==
                                     (root / MODULE_REL).read_bytes())

    result = all_caught and all_restored and code == 0
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {result}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
