"""Capability evidence, read back for a run and for a job's task (DECISION F157 D5 (2)):
`routed_claude_cli_build` (`packages/orchestration/capability_routes.py`) writes a build's
decisions beside the run `create_role_provider` was given — the run's own directory unless a job
task streams, when it is the task's directory under the job's evidence root. These readers find
every directory one run's build may have written to, so `remedy run show` and the job report see a
degradation wherever its build wrote it, whichever directory that was.

Public API:
    task_capability_degradations(job_id, task_id, run_id) -> list[dict]
    run_capability_degradations(run_id, record) -> list[dict]
    capability_report_line(record) -> str | None
"""

from __future__ import annotations

from typing import Any

from packages.contracts.capability_matrix import (
    CAPABILITY_DEGRADATIONS_FIELD,
    format_capability_degradations,
)
from packages.orchestration import data_paths
from packages.orchestration.capability_routes import read_capability_degradations


# WHY: a job task's build may have written its evidence beside the run OR beside the task — both
# are read together, so a caller never has to know which one a given build chose (DECISION F157 D5 (2)).
def task_capability_degradations(job_id: str, task_id: str, run_id: str) -> list[dict]:
    run_directory = str(data_paths.run_dir(run_id)) if run_id else None
    task_directory = str(data_paths.job_evidence_dir(job_id) / "task_runs" / task_id)
    return read_capability_degradations(run_directory, task_directory)


# WHY: `remedy run show` reads a run's degradations without being told whether the run was a job's
# task; a readable plan naming this run's task adds that task's own directory too (DECISION F157 D5 (2)).
def run_capability_degradations(run_id: str, record: dict[str, Any]) -> list[dict]:
    from packages.orchestration.pingpong_job import load_job_plan_safe

    directories: list[str | None] = [str(data_paths.run_dir(run_id))]
    job_id = record.get("job_id") if isinstance(record, dict) else None
    if job_id:
        plan, degraded = load_job_plan_safe(job_id)
        if plan is not None and not degraded:
            task = next((t for t in plan.tasks if t.run_id == run_id), None)
            if task is not None:
                directories.append(
                    str(data_paths.job_evidence_dir(job_id) / "task_runs" / task.task_id)
                )
    return read_capability_degradations(*directories)


# WHY: `None` when there is nothing to show, so a report omits the line rather than printing an
# empty one — the same honesty rule `failover_report_line` follows (DECISION F157 D5 (3)).
def capability_report_line(record: dict[str, Any]) -> str | None:
    entries = record.get(CAPABILITY_DEGRADATIONS_FIELD) if isinstance(record, dict) else None
    if not entries:
        return None
    return "Degradations: " + format_capability_degradations(entries)
