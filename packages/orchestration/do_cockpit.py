"""F268 — the cockpit a `remedy do` walk opens for the last job that ran, detached, and the
ui step that opens it;
moved out of `packages/orchestration/do_sequence.py` unchanged, as a step of that file's
boundary on `docs/system/structure-ledger-v1.md` (structure rule 2, DECISION F205 D3);
`do_sequence.py` imports every name back by name, so each import path keeps working.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from packages.orchestration.do_context import (
    DO_STEP_DONE,
    DO_STEP_SKIPPED,
    DoContext,
)

# ---------------------------------------------------------------------------
# The cockpit, opened detached (DECISION F268 D9 (1)).
# ---------------------------------------------------------------------------


#: How long the ui step waits for the detached cockpit to write its info file.
DO_COCKPIT_WAIT_SECONDS = 15.0

#: The stop command the ui step reports; it stops every running UI session.
DO_COCKPIT_STOP_COMMAND = "remedy ui stop"


class DoCockpitLaunchError(Exception):
    """The detached cockpit did not come up; the message says why and where its log is."""


def do_cockpit_argv(job_id: str, info_file: Path | str) -> list[str]:
    """The detached cockpit's command line: `remedy ui start` on an automatic port."""
    return [sys.executable, "-m", "apps.cli.grouped", "ui", "start", job_id,
            "--port", "0", "--info-file", str(info_file)]


def do_cockpit_paths(job_id: str) -> tuple[Path, Path]:
    """``(info_file, log_file)`` under the data root, which init keeps out of `git status`.

    The info file sits in the UI session registry `remedy ui start` itself
    writes to, so `remedy ui status` and `remedy ui stop` see the cockpit.
    """
    from packages.orchestration.data_paths import resolve_data_root

    ui_root = Path(resolve_data_root()) / "ui"
    return ui_root / "sessions" / f"do-{job_id}.json", ui_root / "do_logs" / f"{job_id}.log"


def launch_do_cockpit(
    job_id: str,
    *,
    wait_seconds: float = DO_COCKPIT_WAIT_SECONDS,
    spawn: Callable[..., Any] = subprocess.Popen,
    sleep: Callable[[float], None] = time.sleep,
) -> str:
    """Start the cockpit for *job_id* in its own session and return its URL.

    The child outlives `remedy do`: it runs in a new session with its output in
    a log file. Waits at most ``wait_seconds`` for the info file; a child that
    exits first or does not come up in time raises `DoCockpitLaunchError`
    (a child still starting is terminated, so no half-started server is left).
    """
    info_file, log_file = do_cockpit_paths(job_id)
    info_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    info_file.unlink(missing_ok=True)
    with open(log_file, "ab") as log:
        child = spawn(do_cockpit_argv(job_id, info_file), stdin=subprocess.DEVNULL,
                      stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    deadline = time.monotonic() + wait_seconds
    while True:
        try:
            url = json.loads(info_file.read_text(encoding="utf-8")).get("url", "")
        except (OSError, ValueError):
            url = ""
        if url:
            return url
        code = child.poll()
        if code is not None:
            raise DoCockpitLaunchError(
                f"the cockpit exited with code {code} before it came up; its log: {log_file}")
        if time.monotonic() >= deadline:
            child.terminate()
            raise DoCockpitLaunchError(
                f"the cockpit did not come up within {wait_seconds:g}s; its log: {log_file}")
        sleep(0.1)


def _step_ui(ctx: DoContext) -> tuple[str, str]:
    """Open the cockpit for the last job that ran, detached, unless `--no-ui` (DECISIONs F268 D9, D12)."""
    if ctx.no_ui:
        return DO_STEP_SKIPPED, "--no-ui given; the cockpit was not opened"
    job_id = ctx.run_job_ids[-1]
    command = f"remedy ui start {job_id}"
    if ctx.ui_launcher is None:
        ctx.next_lines.append(command)
        return DO_STEP_SKIPPED, f"no cockpit launcher on this walk; open it with: {command}"
    try:
        url = ctx.ui_launcher(job_id)
    except (DoCockpitLaunchError, OSError) as exc:
        ctx.next_lines.append(command)
        return DO_STEP_SKIPPED, f"the cockpit was not opened: {exc}; open it with: {command}"
    ctx.next_lines.append(DO_COCKPIT_STOP_COMMAND)
    return DO_STEP_DONE, (
        f"the cockpit for job {job_id} is open at {url}; "
        f"stop it with: {DO_COCKPIT_STOP_COMMAND}")
