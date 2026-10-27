"""Operator amendment amend1027-green-builds C2: which provider calls a job repeated after a time-out.

Jobs d3cdac567bb843cb and bfd0a45cc3ca4124 (2026-10-26) ended `provider_unavailable`: every
claude-cli call had 120 seconds. A call now gets thirty minutes and, when it runs into them, is
repeated once (`pingpong_provider_call._call_with_retry`). This module reads those repeats back
from each task's run record (`retry_reasons`, `<role>:attempt<n>:<error>`), so the story says a
call was repeated and why.
"""
from __future__ import annotations

import json
from typing import Any


def job_timeout_retries(plan: Any) -> list[dict[str, Any]]:
    """Each repeat after a time-out in PLAN's task runs, as `{task_id, role, attempt, reason}`, in
    task order; [] when no run record can be read or none timed out."""
    from packages.orchestration.data_paths import run_dir
    from packages.orchestration.provider_timeouts import is_timeout_error

    found: list[dict[str, Any]] = []
    for task in getattr(plan, "tasks", None) or ():
        run_id = str(getattr(task, "run_id", "") or "")
        if not run_id:
            continue
        try:
            record = json.loads((run_dir(run_id) / "result.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for reason in record.get("retry_reasons") or () if isinstance(record, dict) else ():
            role, _, rest = str(reason).partition(":attempt")
            attempt, _, error = rest.partition(":")
            if is_timeout_error(error) and attempt.isdigit():
                found.append({"task_id": str(task.task_id), "role": role, "attempt": int(attempt),
                              "reason": "timeout"})
    return found
