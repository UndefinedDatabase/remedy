#!/usr/bin/env python3
"""F026 R1 G5 — the red proofs.

For each mutation below: edit the named module INSIDE the given worktree (asserting its FROM
text occurs exactly once), run the worktree's ``tests/orchestration/test_task_edit_runtime.py``
after purging ``__pycache__``, restore the bytes, and report the label, the exit code, the
failed count and the failing node ids. An unmutated control runs first and last. Every mutation
is a real behaviour change to the runtime task edit (DECISION F026 D1) or to the ``spec_version``
field it depends on, and every one of them must turn the test file red.

Usage: python3 -B .agent/authored/f026-r1-mutations.py <worktree-path>
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TER = "packages/orchestration/task_edit_runtime.py"
PPJ = "packages/orchestration/pingpong_job.py"
TEST = "tests/orchestration/test_task_edit_runtime.py"

MUTATIONS: list[tuple[str, str, str, str]] = [
    ("m1 the gate admits a `running` job", TER,
     '    if job_value == RunState.RUNNING.value:',
     '    if job_value == "never-matches-running":'),

    ("m2 the gate admits a `completed` job", TER,
     '    if job_value in (RunState.COMPLETED.value, RunState.FAILED.value, '
     'RunState.CANCELLED.value):',
     '    if job_value in (RunState.FAILED.value, RunState.CANCELLED.value):'),

    ("m3 the gate admits a `pending` approval", TER,
     '    if approval_value in ("pending", "rejected"):',
     '    if approval_value in ("rejected",):'),

    ("m4 the gate admits a `running` task", TER,
     '    if status_value in (TASK_FAILED, TASK_BLOCKED):\n        return "failed"',
     '    if status_value in (TASK_FAILED, TASK_BLOCKED, "running"):\n        return "failed"'),

    ("m5 the gate admits an `applied_to_job_workspace` task", TER,
     '    if status_value in (TASK_FAILED, TASK_BLOCKED):\n        return "failed"',
     '    if status_value in (TASK_FAILED, TASK_BLOCKED, "applied_to_job_workspace"):\n'
     '        return "failed"'),

    ("m6 the gate refuses a `blocked` task", TER,
     '    if status_value in (TASK_FAILED, TASK_BLOCKED):\n        return "failed"',
     '    if status_value in (TASK_FAILED,):\n        return "failed"'),

    ("m7 a pending task with a task pause file reads `waiting`", TER,
     '            task_paused = task_paused or task_id in paused_ids',
     '            task_paused = task_paused'),

    ("m8 a stale `expected_spec_version` is accepted", TER,
     '        if expected_spec_version != spec_version_before:',
     '        if False:'),

    ("m9 the entry is replaced by the freshly mapped one instead of updated in place", TER,
     '        entry.title = fresh.title\n'
     '        entry.acceptance = fresh.acceptance\n'
     '        entry.inputs["plan"] = fresh.inputs["plan"]',
     '        job.tasks[idx] = fresh\n'
     '        entry = fresh'),

    ("m10 `spec_version` is not raised", TER,
     '        entry.spec_version = spec_version_before + 1',
     '        entry.spec_version = spec_version_before'),

    ("m11 the archive is written before the edit validates, so a refused edit leaves one", TER,
     '        args = {"task_id": planned_id, "fields": fields}\n'
     '        try:\n'
     '            new_plan = apply_edit(plan, "plan_edit_task", args)\n'
     '        except PlanEditRefused as exc:\n'
     '            exc.current_version = spec_version_before\n'
     '            raise\n'
     '\n'
     '        # S5: the archive is written after the edit validated and before the record is\n'
     '        # written — a refused edit above never reaches here, and nothing below this point\n'
     '        # runs unless the archive itself succeeds or finds an equal prior write.\n'
     '        plan_task = next(t for t in plan.tasks if t.id == planned_id)\n'
     '        archive_path = _archive_prior_spec(\n'
     '            job_id, root, planned_id, plan_task, entry, state, spec_version_before)',
     '        plan_task = next(t for t in plan.tasks if t.id == planned_id)\n'
     '        archive_path = _archive_prior_spec(\n'
     '            job_id, root, planned_id, plan_task, entry, state, spec_version_before)\n'
     '\n'
     '        args = {"task_id": planned_id, "fields": fields}\n'
     '        try:\n'
     '            new_plan = apply_edit(plan, "plan_edit_task", args)\n'
     '        except PlanEditRefused as exc:\n'
     '            exc.current_version = spec_version_before\n'
     '            raise'),

    ("m12 an existing archive with other content is overwritten", TER,
     '    if existing_cmp != new_cmp:\n'
     '        raise PlanEditRefused(\n'
     '            "spec_archive_conflict",\n'
     '            f"an archived spec already exists at {path} with different content")\n'
     '    return path',
     '    if existing_cmp != new_cmp:\n'
     '        path.write_bytes(data)\n'
     '    return path'),

    ("m13 the approval hash is not re-stamped", TER,
     '        if body.get("_approval") == "approved" and approved_before:',
     '        if False:'),

    ("m14 a failed task keeps its status", TER,
     '        if state == "failed":\n'
     '            entry.status = TASK_PENDING\n'
     '            entry.error = ""\n'
     '            for later in job.tasks[idx + 1:]:',
     '        if state == "failed":\n'
     '            for later in job.tasks[idx + 1:]:'),

    ("m15 the skipped tasks after the reset task stay skipped", TER,
     '                if _value(later.status) == TASK_SKIPPED:\n'
     '                    later.status = TASK_PENDING\n'
     '                    restored.append(later.task_id)',
     '                if False:\n'
     '                    later.status = TASK_PENDING\n'
     '                    restored.append(later.task_id)'),

    ("m16 every skipped task is restored, including one before the reset task", TER,
     '            for later in job.tasks[idx + 1:]:',
     '            for later in job.tasks:'),

    ("m17 the log entry's `command` is not `plan_edit_task`", TER,
     '            "command": "plan_edit_task",',
     '            "command": "plan_edit_task_mutated",'),

    ("m18 `_export_job` drops `spec_version` (in `pingpong_job.py`)", PPJ,
     '                # DECISION F026 D1.\n'
     '                "spec_version": t.spec_version,\n'
     '            }',
     '            }'),

    ("m19 `_import_job` ignores a stored `spec_version` and reads 1 (in `pingpong_job.py`)", PPJ,
     '            spec_version=int(t.get("spec_version", 1) or 1),',
     '            spec_version=1,'),
]


def _purge_pycache(root: Path) -> None:
    for p in root.rglob("__pycache__"):
        for f in sorted(p.rglob("*"), reverse=True):
            try:
                if f.is_dir():
                    f.rmdir()
                else:
                    f.unlink()
            except OSError:
                pass
        try:
            p.rmdir()
        except OSError:
            pass


def _run_tests(root: Path) -> tuple[int, int, list[str]]:
    _purge_pycache(root)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=no", "-rf",
         TEST],
        cwd=root, capture_output=True, text=True, check=False)
    failed_ids = [
        line[len("FAILED "):].split(" - ", 1)[0].strip()
        for line in proc.stdout.splitlines() if line.startswith("FAILED ")
    ]
    return proc.returncode, len(failed_ids), failed_ids


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f026-r1-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    originals: dict[str, bytes] = {}
    for relpath in (TER, PPJ):
        originals[relpath] = (root / relpath).read_bytes()

    all_ok = True

    exit_code, failed, ids = _run_tests(root)
    print(f"control (before): exit={exit_code} failed={failed} ids={ids}")
    if exit_code != 0 or failed != 0:
        all_ok = False

    for label, relpath, from_text, to_text in MUTATIONS:
        path = root / relpath
        original = originals[relpath]
        text = original.decode("utf-8")
        count = text.count(from_text)
        assert count == 1, f"{label}: FROM text occurs {count} times in {relpath}, not once"
        mutated = text.replace(from_text, to_text, 1)
        path.write_text(mutated, encoding="utf-8")
        try:
            exit_code, failed, ids = _run_tests(root)
        finally:
            path.write_bytes(original)
        restored = path.read_bytes() == original
        caught = exit_code != 0 and failed > 0
        if not caught or not restored:
            all_ok = False
        print(f"{label}: exit={exit_code} failed={failed} ids={ids} restored={restored}")

    for relpath in (TER, PPJ):
        identical = (root / relpath).read_bytes() == originals[relpath]
        if not identical:
            all_ok = False
        print(f"{relpath} restored byte-identical: {identical}")

    exit_code, failed, ids = _run_tests(root)
    print(f"control (after): exit={exit_code} failed={failed} ids={ids}")
    if exit_code != 0 or failed != 0:
        all_ok = False

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
