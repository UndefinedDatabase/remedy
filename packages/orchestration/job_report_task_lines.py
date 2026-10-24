"""The job report's per-task detail lines: a structural step under rule 4 of "The structure
rule" (`docs/agents/self_drive_protocol.md`), moving `format_job_report_text`'s per-task body out
of that function so the function can gain a capability-degradations line without growing past its
structure-ledger row (DECISION F157 D5 (4)).

Public API:
    task_report_detail_lines(job, task, steering_map) -> list[str]
"""

from __future__ import annotations

from typing import Any

from packages.contracts.capability_matrix import format_capability_degradations
from packages.orchestration.capability_evidence import task_capability_degradations
from packages.orchestration.pingpong_job import JobPlan, TaskEntry


# WHY: the lines `format_job_report_text` prints under one task, beyond its status line — moved
# here unchanged (DECISION F157 D5 (4)) so a later call can add to them without growing that row;
# the degradations line is the later call, added here under the same roof (DECISION F157 D5 (2)).
def task_report_detail_lines(
    job: JobPlan, task: TaskEntry, steering_map: dict[str, list[dict[str, Any]]],
) -> list[str]:
    lines: list[str] = []
    for note in steering_map.get(task.task_id, []):
        lines.append(
            "      Steering not consumed: “" + note["text"].replace("\n", "\n        ") + "”"
        )
    degradations = task_capability_degradations(job.job_id, task.task_id, task.run_id)
    if degradations:
        lines.append(f"      Degradations: {format_capability_degradations(degradations)}")
    return lines
