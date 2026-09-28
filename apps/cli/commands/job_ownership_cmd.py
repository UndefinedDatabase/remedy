"""`remedy job ownership` — F035 T003, DECISION F035 D4.

Read-only: shows who did what in a job under its mission — every recorded action of the
operator on the job or one of its tasks, every default the operator accepted and every choice
Remedy's planner made — one plain sentence each, read through
`ownership_phrases.ownership_view`, the SAME view the browser's `ownership` read route answers
(`packages/orchestration/ui_server.py`), so the CLI and the browser can never say two
different things about who did what. Never writes.

Exit codes follow the CLI contract (docs/guides/exit-codes.md): 3 when the job's record
`load_job_plan` cannot read (`job_not_found`), 1 when the view itself carries an `error`
(`ownership_unreadable`) — and whatever `resolve_job_id_or_fail` answers for the job id
argument itself, unchanged (F035).
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from apps.cli.job_id_arg import resolve_job_id_or_fail
from apps.cli.json_envelope import emit_ok, fail

if TYPE_CHECKING:
    import argparse
    from collections.abc import Callable

EXIT_NOT_READY = 3


def _cmd_job_ownership(job_id_str: str, *, json_output: bool = False) -> None:
    from packages.orchestration.ownership_phrases import ownership_view
    from packages.orchestration.pingpong_job import load_job_plan

    job_id = resolve_job_id_or_fail(job_id_str, json_output=json_output)
    job = load_job_plan(job_id)
    if job is None:
        fail("job_not_found", f"The record of job {job_id} cannot be read.",
             json_output=json_output, exit_code=EXIT_NOT_READY, job_id=job_id)

    view = ownership_view(job)
    if view["error"]:
        fail("ownership_unreadable", view["error"], json_output=json_output, job_id=job_id)

    if json_output:
        emit_ok(job_id=job_id, schema=view["schema"], entries=view["entries"])
        return

    entries = view["entries"]
    if not entries:
        print(f"No action is recorded for job {job_id} yet.")
        return
    print(f"Who did what in job {job_id}:")
    for entry in entries:
        sentence = entry["sentence"].replace("\n", "\n    ")
        print(f"  - {sentence}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "job.ownership": lambda args: _cmd_job_ownership(
        getattr(args, "job_id", "") or "",
        json_output=bool(getattr(args, "json", False)),
    ),
}
