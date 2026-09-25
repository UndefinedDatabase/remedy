#!/usr/bin/env python3
"""F026 R2 G5 — the red proofs.

For each mutation below: edit the named module INSIDE the given worktree (asserting its FROM
text occurs exactly once), purge `__pycache__`, run the worktree's
`tests/orchestration/test_task_edit_runtime.py`, `tests/cli/test_job_plan_cmd.py` and
`tests/ui_server/test_command_dispatch.py` from the worktree's root, restore the bytes, and
report the label, the exit code, the failed/errored count and the failing node ids. An
unmutated control runs first and last. Every mutation is a real behaviour change to T002's
own code — `job.edit-task` in the catalog and CLI, the write door, or the reset/update
`task_edit_runtime.py` already carries — and every one of them must turn the suite red.

Usage: python3 -B .agent/authored/f026-r2-mutations.py <worktree-path>
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PPJ = "packages/orchestration/pingpong_job.py"
TER = "packages/orchestration/task_edit_runtime.py"
UI = "packages/orchestration/ui_server.py"
CLI = "apps/cli/commands/job_plan_cmd.py"

TEST_FILES = (
    "tests/orchestration/test_task_edit_runtime.py",
    "tests/cli/test_job_plan_cmd.py",
    "tests/ui_server/test_command_dispatch.py",
)

MUTATIONS: list[tuple[str, str, str, str]] = [
    ("m1 run_job leaves `error` as it was when the job starts running", PPJ,
     '        job.state = JOB_RUNNING\n'
     '        job.error = ""  # R-1059: a relaunch clears a prior run\'s stale error.\n'
     '        _persist_job(job)',
     '        job.state = JOB_RUNNING\n'
     '        _persist_job(job)'),

    ("m2 the edit no longer updates the entry's title (the v1 remnant)", TER,
     '        entry.title = fresh.title\n'
     '        entry.acceptance = fresh.acceptance',
     '        entry.acceptance = fresh.acceptance'),

    ("m3 the reset no longer restores the skipped tasks after the reset task", TER,
     '                if _value(later.status) == TASK_SKIPPED:\n'
     '                    later.status = TASK_PENDING\n'
     '                    restored.append(later.task_id)',
     '                if False:\n'
     '                    later.status = TASK_PENDING\n'
     '                    restored.append(later.task_id)'),

    ("m4 the door admits job.edit-task without expected_version", UI,
     '        if command == JOB_EDIT_TASK_COMMAND_ID and (\n'
     '                not isinstance(version, int) or isinstance(version, bool) or version < 1):\n'
     '            return None, _command_field_error("expected_version", COMMAND_TASK_VERSION_MESSAGE)',
     '        if False and command == JOB_EDIT_TASK_COMMAND_ID:\n'
     '            return None, _command_field_error("expected_version", COMMAND_TASK_VERSION_MESSAGE)'),

    ("m5 task_edit_refusal answers task_not_editable with 500", UI,
     '    if code in _TASK_RUNTIME_REFUSAL_CODES:\n'
     '        return 409, "rejected_state", {"error": COMMAND_TASK_STATE_MESSAGE, "detail": detail}\n'
     '    return plan_edit_refusal(code, detail, current_version)',
     '    if code == "task_not_editable":\n'
     '        return 500, "rejected_effect", {"error": COMMAND_EFFECT_FAILED_MESSAGE}\n'
     '    if code in _TASK_RUNTIME_REFUSAL_CODES:\n'
     '        return 409, "rejected_state", {"error": COMMAND_TASK_STATE_MESSAGE, "detail": detail}\n'
     '    return plan_edit_refusal(code, detail, current_version)'),

    ("m6 the door's dispatcher names the actor \"door\" instead of the token fingerprint", UI,
     '        result = edit_task_at_runtime(\n'
     '            str(job.job_id), args.get("task_id"), args.get("fields"),\n'
     '            expected_spec_version=args["expected_version"],\n'
     '            actor=token_fingerprint(self._supplied_bearer_token()))',
     '        result = edit_task_at_runtime(\n'
     '            str(job.job_id), args.get("task_id"), args.get("fields"),\n'
     '            expected_spec_version=args["expected_version"],\n'
     '            actor="door")'),

    ("m7 the CLI exits 1 for task_not_editable", CLI,
     '_RUNTIME_NOT_READY_REFUSALS = frozenset({\n'
     '    "job_not_found", "no_task_plan", "plan_not_editable", "version_conflict",\n'
     '    "lock_timeout", "job_not_editable", "task_not_editable", "spec_archive_conflict",\n'
     '})',
     '_RUNTIME_NOT_READY_REFUSALS = frozenset({\n'
     '    "job_not_found", "no_task_plan", "plan_not_editable", "version_conflict",\n'
     '    "lock_timeout", "job_not_editable", "spec_archive_conflict",\n'
     '})'),

    ("m8 the CLI does not resolve a planned id to its task entry", CLI,
     '    matches = [t.task_id for t in job.tasks\n'
     '              if (t.inputs.get("plan") or {}).get("planned_id") == task_arg]\n'
     '    if len(matches) == 1:\n'
     '        return matches[0]\n'
     '    return task_arg',
     '    return task_arg'),

    ("m9 the CLI reads a missing --spec-version as 1", CLI,
     '    if raw is None:\n'
     '        fail("missing_spec_version", "Name the spec version the edit was made against with "\n'
     '             "--spec-version, as `remedy job plan-show` prints it.", json_output=json_output,\n'
     '             exit_code=EXIT_USAGE)',
     '    if raw is None:\n'
     '        return 1'),

    ("m10 `job plan-show` omits `spec_version`", CLI,
     '        task["status"] = entry.status if entry is not None else ""\n'
     '        task["spec_version"] = entry.spec_version if entry is not None else 1\n'
     '        tasks.append(task)',
     '        task["status"] = entry.status if entry is not None else ""\n'
     '        tasks.append(task)'),
]

MUTATED_FILES = (PPJ, TER, UI, CLI)


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
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=no", "-rfE",
         *TEST_FILES],
        cwd=root, capture_output=True, text=True, check=False)
    bad_ids = [
        line.split(" ", 1)[1].split(" - ", 1)[0].strip()
        for line in proc.stdout.splitlines()
        if line.startswith("FAILED ") or line.startswith("ERROR ")
    ]
    return proc.returncode, len(bad_ids), bad_ids


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f026-r2-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    originals: dict[str, bytes] = {}
    for relpath in MUTATED_FILES:
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

    for relpath in MUTATED_FILES:
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
