"""F030 R2 G5 — the red-proof tool for the task-addressed steering command (DECISION F030 D2).

Takes a worktree path (argv[1]). For each mutation below: edits the named file inside that
worktree (asserting its FROM text occurs exactly once), purges the worktree's __pycache__
directories, runs the pinned steer selection from the worktree's root, records the exit code and
every failing node id, restores the file's original bytes, and verifies the restoration is
byte-identical. Runs an unmutated control first and last. Prints one line per mutation plus a
final verdict line.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

TEST_ARGS = [
    "tests/orchestration/test_steer_task.py",
    "tests/cli/test_job_steer.py",
    "tests/ui_server/test_steer_task_door.py",
    "tests/orchestration/test_steering.py",
    "tests/cli/test_chat_cmd.py",
]

# label, path (relative to worktree root), FROM (must occur exactly once), TO
MUTATIONS: list[tuple[str, str, str, str]] = [
    ("m1 STEERABLE_TASK_STATUSES also holds passed",
     "packages/orchestration/steering.py",
     'STEERABLE_TASK_STATUSES = frozenset({"pending", "running", "blocked", "failed", '
     '"skipped"})',
     'STEERABLE_TASK_STATUSES = frozenset({"pending", "running", "blocked", "failed", '
     '"skipped", "passed"})'),

    ("m2 STEERABLE_TASK_STATUSES loses failed",
     "packages/orchestration/steering.py",
     'STEERABLE_TASK_STATUSES = frozenset({"pending", "running", "blocked", "failed", '
     '"skipped"})',
     'STEERABLE_TASK_STATUSES = frozenset({"pending", "running", "blocked", "skipped"})'),

    ("m3 steer_task_command records the note without its task id",
     "packages/orchestration/steering.py",
     "    record = record_steering_message(job.job_id, text, job_state=state, channel=channel,\n"
     "                                     task_id=task_id, root=root, now=now)\n",
     "    record = record_steering_message(job.job_id, text, job_state=state, channel=channel,\n"
     "                                     root=root, now=now)\n"),

    ("m4 step c (the unknown-task check) is skipped",
     "packages/orchestration/steering.py",
     "    task = next((t for t in job.tasks if str(getattr(t, \"task_id\", \"\")) == task_id), "
     "None)\n"
     "    if task is None:\n",
     "    task = next((t for t in job.tasks if str(getattr(t, \"task_id\", \"\")) == task_id), "
     "None)\n"
     "    if False:\n"),

    ("m5 step b (the ended-job check) is skipped",
     "packages/orchestration/steering.py",
     "    state = job.state.value if hasattr(job.state, \"value\") else str(job.state)\n"
     "    if job_is_terminal(state):\n",
     "    state = job.state.value if hasattr(job.state, \"value\") else str(job.state)\n"
     "    if False:\n"),

    ("m6 steering_overview ignores task_statuses",
     "packages/orchestration/steering.py",
     "    statuses = task_statuses or {}\n",
     "    statuses = {}\n"),

    ("m7 task_not_steerable exits 1",
     "apps/cli/commands/job_steer_cmd.py",
     '_NOT_READY_CODES = frozenset({"job_not_steerable", "task_not_steerable"})',
     '_NOT_READY_CODES = frozenset({"job_not_steerable"})'),

    ("m8 the task argument is passed on without _resolve_task_arg",
     "apps/cli/commands/job_steer_cmd.py",
     "    task_id = _resolve_task_arg(job, task_arg)\n",
     "    task_id = task_arg\n"),

    ("m9 _dispatch_steer_task records with channel cli",
     "packages/orchestration/ui_server.py",
     "        result = steer_task_command(\n"
     '            job, args["task_id"], args["message"], channel="cockpit")\n',
     "        result = steer_task_command(\n"
     '            job, args["task_id"], args["message"], channel="cli")\n'),

    ("m10 _read_command_payload's job.steer check on task_id is skipped",
     "packages/orchestration/ui_server.py",
     '            task_id = args.get("task_id")\n'
     "            if not isinstance(task_id, str) or not task_id:\n"
     "                return None, _command_field_error(\n"
     '                    "task_id", "task_id must be a non-empty string")\n'
     "            try:\n"
     '                normalize_steering_text(args.get("message"))\n',
     '            task_id = args.get("task_id")\n'
     "            if False:\n"
     "                return None, _command_field_error(\n"
     '                    "task_id", "task_id must be a non-empty string")\n'
     "            try:\n"
     '                normalize_steering_text(args.get("message"))\n'),

    ("m11 the new branch answers a refusal 200",
     "packages/orchestration/ui_server.py",
     '        if payload["command"] == JOB_STEER_COMMAND_ID:\n'
     "            try:\n"
     "                accepted_body = self._dispatch_steer_task(job, payload)\n"
     "            except (OSError, RuntimeError, ValueError, TypeError):\n"
     "                # D18, clause four: an effect that RAISED is neither `accepted`,\n"
     "                # which would be false, nor unaudited, which would break D6.\n"
     '                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,\n'
     "                                    payload=payload)\n"
     "                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))\n"
     "                return\n"
     '            if accepted_body.get("outcome") == "refused":\n'
     '                self._audit_attempt(str(job.job_id), "rejected_state", create=True,\n'
     "                                    payload=payload)\n"
     "                self._send_json(*_safe_error(\n"
     "                    409, f\"{accepted_body['code']}: {accepted_body['detail']}\"))\n"
     "                return\n",
     '        if payload["command"] == JOB_STEER_COMMAND_ID:\n'
     "            try:\n"
     "                accepted_body = self._dispatch_steer_task(job, payload)\n"
     "            except (OSError, RuntimeError, ValueError, TypeError):\n"
     "                # D18, clause four: an effect that RAISED is neither `accepted`,\n"
     "                # which would be false, nor unaudited, which would break D6.\n"
     '                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,\n'
     "                                    payload=payload)\n"
     "                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))\n"
     "                return\n"
     "            if False:\n"
     '                self._audit_attempt(str(job.job_id), "rejected_state", create=True,\n'
     "                                    payload=payload)\n"
     "                self._send_json(*_safe_error(\n"
     "                    409, f\"{accepted_body['code']}: {accepted_body['detail']}\"))\n"
     "                return\n"),

    ("m12 _cmd_chat_show passes no task_statuses",
     "apps/cli/commands/chat_cmd.py",
     "    try:\n"
     "        rows = steering_overview(job.job_id, state, task_statuses=task_statuses)\n",
     "    try:\n"
     "        rows = steering_overview(job.job_id, state)\n"),
]


def _purge_pycache(root: Path) -> None:
    for path in root.rglob("__pycache__"):
        if path.is_dir():
            for child in path.rglob("*"):
                if child.is_file():
                    child.unlink()
            for child in sorted(path.rglob("*"), key=lambda p: len(p.parts), reverse=True):
                if child.is_dir():
                    child.rmdir()
            path.rmdir()


def _run_suite(root: Path) -> tuple[int, int, list[str]]:
    _purge_pycache(root)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TEST_ARGS],
        cwd=root, capture_output=True, text=True,
    )
    out = proc.stdout + proc.stderr
    failing = re.findall(r"^FAILED\s+(\S+)", out, flags=re.MULTILINE)
    match = re.search(r"(\d+) failed", out)
    failed_count = int(match.group(1)) if match else len(failing)
    return proc.returncode, failed_count, failing


def main() -> int:
    worktree = Path(sys.argv[1]).resolve()
    all_caught = True

    label, exit_code, failed_count, failing = (
        "control (start)", *_run_suite(worktree))
    print(f"{label}: exit={exit_code} failed={failed_count} nodes={failing}")
    if exit_code != 0:
        print("CONTROL RUN IS NOT GREEN — aborting.")
        return 1

    restored_all = True
    for label, rel_path, from_text, to_text in MUTATIONS:
        target = worktree / rel_path
        original = target.read_bytes()
        original_text = original.decode("utf-8")
        occurrences = original_text.count(from_text)
        if occurrences != 1:
            print(f"{label}: FROM text occurs {occurrences} times in {rel_path} "
                  f"(expected 1) — SKIPPED")
            all_caught = False
            continue
        mutated_text = original_text.replace(from_text, to_text, 1)
        target.write_text(mutated_text, encoding="utf-8")
        try:
            exit_code, failed_count, failing = _run_suite(worktree)
        finally:
            target.write_bytes(original)
        restored = target.read_bytes() == original
        restored_all = restored_all and restored
        caught = exit_code != 0 and failed_count > 0 and bool(failing)
        all_caught = all_caught and caught
        print(f"{label}: exit={exit_code} failed={failed_count} nodes={failing} "
              f"caught={caught} restored={restored}")

    label, exit_code, failed_count, failing = (
        "control (end)", *_run_suite(worktree))
    print(f"{label}: exit={exit_code} failed={failed_count} nodes={failing}")
    if exit_code != 0:
        all_caught = False

    print(f"restored byte-identical: {restored_all}")
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_caught and restored_all}")
    return 0 if (all_caught and restored_all) else 1


if __name__ == "__main__":
    raise SystemExit(main())
