"""`remedy job preview-start` and `remedy job preview-stop` — F041 T002, DECISION F041 D3.

Each command records the request and acts on it in the same call: `request_preview`
writes the pending action, `run_pending` runs it — through `run_runtime_verb`, imported
by name into this module so a test can replace it — and the resulting view is read back
with `preview_view`. A preview that ends anywhere but where the command asked (a start
that is not `live`, a stop that is not `stopped`) is reported honestly and the command
exits 1; an unknown job answers `job_not_found` at exit 3, the same contract every other
job command in this CLI already answers (docs/guides/exit-codes.md).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from apps.cli.job_id_arg import resolve_job_id_or_fail
from apps.cli.json_envelope import emit_ok, fail
from packages.orchestration.preview_control import (
    preview_view,
    request_preview,
    run_pending,
)
from packages.orchestration.preview_runner import run_runtime_verb

if TYPE_CHECKING:
    import argparse
    from collections.abc import Callable

EXIT_NOT_READY = 3

#: The state a preview must end in for each action to count as a success.
_EXPECTED_STATE = {"start": "live", "stop": "stopped"}


def _cmd_job_preview(job_id_str: str, action: str, *, json_output: bool = False) -> None:
    from packages.orchestration.pingpong_job import load_job_plan

    job_id = resolve_job_id_or_fail(job_id_str, json_output=json_output)
    job = load_job_plan(job_id)
    if job is None:
        fail("job_not_found", f"The record of job {job_id} cannot be read.",
             json_output=json_output, exit_code=EXIT_NOT_READY, job_id=job_id)

    now = datetime.now(timezone.utc)
    request_preview(job_id, action, now=now, data_root=None)
    run_pending(job, run_runtime_verb, now=now, data_root=None)
    view = preview_view(job_id, data_root=None)
    state = view["state"]

    if state != _EXPECTED_STATE[action]:
        reason = view["reason"] or f"the preview is {state}"
        fail(f"preview_{state}", reason, json_output=json_output, exit_code=1,
             job_id=job_id, **view)

    if json_output:
        emit_ok(job_id=job_id, **view)
        return

    if state == "live":
        print(f"The preview of job {job_id} is live at {view['url']}.")
    else:
        print(f"The preview of job {job_id} is {state}.")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "job.preview-start": lambda args: _cmd_job_preview(
        getattr(args, "job_id", "") or "", "start",
        json_output=bool(getattr(args, "json", False)),
    ),
    "job.preview-stop": lambda args: _cmd_job_preview(
        getattr(args, "job_id", "") or "", "stop",
        json_output=bool(getattr(args, "json", False)),
    ),
}
