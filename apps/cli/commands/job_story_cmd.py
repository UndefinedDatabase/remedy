"""`remedy job story` — F039 T003, DECISIONS F039 D7 and D8.

Read-only over the job's own records, with ONE side effect: the whole story of a job under
its mission, written as one self-contained HTML page that plays in any browser with no
network and no Remedy. `export_story_html` builds the page from the cockpit's own builders
and the story player's own second `vite build` (DECISION F039 D8); this command's own job is
to resolve the job id, size the budget from `story.export_max_bytes`, and durably write the
bytes it is handed.

Exit codes follow the CLI contract (docs/guides/exit-codes.md): 3 when the job's record
`load_job_plan` cannot read (`job_not_found`) or the built player is missing
(`story_player_missing`, naming the build command); 1 for every other `StoryExportError`
(`story_player_unsafe`, `story_too_large`) and for a write that fails on disk
(`story_write_failed`) — and whatever `resolve_job_id_or_fail` answers for the job id
argument itself, unchanged (the pattern `job_ownership_cmd.py` already uses, F035).
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from apps.cli.job_id_arg import resolve_job_id_or_fail
from apps.cli.json_envelope import emit_ok, fail
from packages.common.secure_fs import durable_write
from packages.orchestration.config import get_config
from packages.orchestration.story_export import StoryExportError, export_story_html

if TYPE_CHECKING:
    import argparse
    from collections.abc import Callable

EXIT_NOT_READY = 3


def _cmd_job_story(job_id_str: str, export_path: str, *, json_output: bool = False) -> None:
    from packages.orchestration.pingpong_job import load_job_plan

    job_id = resolve_job_id_or_fail(job_id_str, json_output=json_output)
    job = load_job_plan(job_id)
    if job is None:
        fail("job_not_found", f"The record of job {job_id} cannot be read.",
             json_output=json_output, exit_code=EXIT_NOT_READY, job_id=job_id)

    budget = get_config().get("story.export_max_bytes")
    try:
        data = export_story_html(job, max_bytes=budget)
    except StoryExportError as exc:
        if exc.error == "story_player_missing":
            fail(exc.error, exc.message, json_output=json_output, exit_code=EXIT_NOT_READY,
                 job_id=job_id)
        fail(exc.error, exc.message, json_output=json_output, job_id=job_id)

    target = Path(export_path)
    try:
        durable_write(target, data, mode=0o644)
    except OSError as exc:
        fail("story_write_failed", f"The story could not be written to {target}: {exc.strerror}",
             json_output=json_output, job_id=job_id)

    if json_output:
        emit_ok(job_id=job_id, path=str(target), bytes=len(data), budget_bytes=budget)
        return

    print(f"Wrote the story of job {job_id} to {target} ({len(data)} bytes). Open it in any "
          f"browser; it needs no network and no Remedy.")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "job.story": lambda args: _cmd_job_story(
        getattr(args, "job_id", "") or "",
        getattr(args, "export", "") or "",
        json_output=bool(getattr(args, "json", False)),
    ),
}
