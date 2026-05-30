"""CLI handler for ``remedy ui`` — localhost UI server."""

from __future__ import annotations

import json
import os
import signal
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    import argparse


# ---------------------------------------------------------------------------
# Session registry
# ---------------------------------------------------------------------------

def _sessions_dir() -> Path:
    """Return (and create) the UI session registry directory."""
    from packages.orchestration.data_paths import resolve_data_root
    d = Path(resolve_data_root()) / "ui" / "sessions"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _write_session(session_id: str, info: dict[str, Any]) -> Path:
    """Write a session file. Returns path."""
    p = _sessions_dir() / f"{session_id}.json"
    p.write_text(json.dumps(info, indent=2))
    return p


def _read_sessions() -> list[dict[str, Any]]:
    """Read all session files, filter to those with live PIDs."""
    results = []
    d = _sessions_dir()
    for f in sorted(d.glob("*.json")):
        try:
            data = json.loads(f.read_text())
            data["_file"] = str(f)
            results.append(data)
        except (json.JSONDecodeError, OSError):
            continue
    return results


def _is_pid_alive(pid: int) -> bool:
    """Check if a PID is still running."""
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def _remove_session(path: str) -> None:
    """Remove a session file."""
    try:
        Path(path).unlink(missing_ok=True)
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def _cmd_ui_start(
    job_id_str: str,
    *,
    port: int = 8787,
    host: str = "127.0.0.1",
    open_browser: bool = False,
    info_file: str | None = None,
) -> None:
    import secrets
    from packages.orchestration.ui_server import start_ui_server

    # Generate session ID for registry
    session_id = secrets.token_hex(8)
    session_file = str(_sessions_dir() / f"{session_id}.json")

    # Use info_file if provided, otherwise register in session dir
    actual_info_file = info_file or session_file

    start_ui_server(
        job_id_str,
        host=host,
        port=port,
        open_browser=open_browser,
        info_file=actual_info_file,
    )


def _cmd_ui_latest() -> None:
    """Open the most recently started UI session."""
    sessions = _read_sessions()
    alive = [s for s in sessions if _is_pid_alive(s.get("pid", 0))]
    if not alive:
        # Clean up dead sessions
        for s in sessions:
            _remove_session(s["_file"])
        print("No active UI sessions.", file=sys.stderr)
        sys.exit(1)

    latest = alive[-1]
    url = latest.get("url", "")
    print(f"Latest UI: {url}")
    print(f"Job: {latest.get('job_id', '?')}")
    print(f"PID: {latest.get('pid', '?')}")

    # Try to open browser
    from packages.orchestration.ui_server import _try_open_browser
    _try_open_browser(url)


def _cmd_ui_status() -> None:
    """Show status of all UI sessions."""
    sessions = _read_sessions()
    if not sessions:
        print("No UI sessions.")
        return

    for s in sessions:
        pid = s.get("pid", 0)
        alive = _is_pid_alive(pid)
        status = "RUNNING" if alive else "DEAD"
        job_id = s.get("job_id", "?")
        url = s.get("url", "?")
        port = s.get("port", "?")
        print(f"  [{status}] job={job_id} port={port} pid={pid}")
        if not alive:
            _remove_session(s["_file"])
        else:
            print(f"          {url}")


def _cmd_ui_stop() -> None:
    """Stop all running UI sessions."""
    sessions = _read_sessions()
    stopped = 0
    for s in sessions:
        pid = s.get("pid", 0)
        if _is_pid_alive(pid):
            try:
                os.kill(pid, signal.SIGTERM)
                stopped += 1
                print(f"  Stopped PID {pid} (job={s.get('job_id', '?')})")
            except OSError as e:
                print(f"  Failed to stop PID {pid}: {e}", file=sys.stderr)
        _remove_session(s["_file"])

    if stopped == 0:
        print("No active UI sessions to stop.")
    else:
        print(f"Stopped {stopped} session(s).")


def _cmd_ui_open(job_id_str: str) -> None:
    """Open browser for a specific job's UI session."""
    sessions = _read_sessions()
    alive = [s for s in sessions if _is_pid_alive(s.get("pid", 0))]

    for s in alive:
        if s.get("job_id") == job_id_str:
            url = s.get("url", "")
            print(f"Opening: {url}")
            from packages.orchestration.ui_server import _try_open_browser
            _try_open_browser(url)
            return

    print(f"No active UI session for job {job_id_str}.", file=sys.stderr)
    print("Start one with: remedy ui start <job_id>", file=sys.stderr)
    sys.exit(1)


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "ui.start": lambda args: _cmd_ui_start(
        args.job_id,
        port=int(getattr(args, "port", None) or 8787),
        host=getattr(args, "host", None) or "127.0.0.1",
        open_browser=str(getattr(args, "open", "false")).lower() == "true",
        info_file=getattr(args, "info_file", None) or None,
    ),
    "ui.latest": lambda _args: _cmd_ui_latest(),
    "ui.status": lambda _args: _cmd_ui_status(),
    "ui.stop": lambda _args: _cmd_ui_stop(),
    "ui.open": lambda args: _cmd_ui_open(args.job_id),
}
