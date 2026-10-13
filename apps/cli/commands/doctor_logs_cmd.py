"""CLI handler for `remedy doctor logs` (F203 T002, DECISION F203 D4)."""

from __future__ import annotations

from typing import Any

from apps.cli.json_envelope import emit_ok


def _cmd_doctor_logs(ns: Any) -> None:
    """Print the operations-log lines of one job, oldest first; never exits non-zero."""
    from packages.orchestration.structured_log import read_log_entries

    job_id = ns.job_id
    run_id = getattr(ns, "run", None)
    result = read_log_entries(job_id=job_id, run_id=run_id)
    if getattr(ns, "json", False):
        emit_ok(
            job_id=job_id,
            run_id=run_id,
            entries=list(result.entries),
            unreadable=result.unreadable,
            files=list(result.files),
        )
        return
    if not result.entries:
        if run_id is None:
            print(f"No operations-log lines for job {job_id}.")
        else:
            print(f"No operations-log lines for job {job_id} and run {run_id}.")
    for entry in result.entries:
        print(
            f"{entry.get('ts') or ''} {entry.get('level') or ''} {entry.get('logger') or ''} "
            f"task={entry.get('task_id') or '-'} run={entry.get('run_id') or '-'} "
            f"{entry.get('message') or ''}"
        )
        exception = entry.get("exception")
        if exception:
            for line in str(exception).splitlines():
                print(f"    {line}")
    if result.unreadable > 0:
        print(f"{result.unreadable} lines of the log are not JSON and were skipped.")


COMMAND_HANDLERS = {"doctor.logs": _cmd_doctor_logs}
