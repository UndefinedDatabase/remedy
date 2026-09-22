"""CLI handler for ``remedy ui`` — localhost UI server."""

from __future__ import annotations

import json
import os
import signal
import sys
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any

from apps.cli.json_envelope import emit_ok, fail

if TYPE_CHECKING:
    import argparse


#: The archive keeps at most this many dead sessions (R-0805 Acceptance:
#: "ui status --all shows the last ten dead ones with their end time").
_DEAD_SESSION_LIMIT = 10


# ---------------------------------------------------------------------------
# Session registry
# ---------------------------------------------------------------------------

def _sessions_dir() -> Path:
    """Return (and create) the UI session registry directory."""
    from packages.orchestration.data_paths import resolve_data_root
    d = Path(resolve_data_root()) / "ui" / "sessions"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _dead_sessions_dir() -> Path:
    """Return (and create) the archive of ended UI sessions (R-0805)."""
    from packages.orchestration.data_paths import resolve_data_root
    d = Path(resolve_data_root()) / "ui" / "sessions_dead"
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


def _archive_dead_session(session: dict[str, Any], *, ended_at: str | None = None) -> None:
    """Move one ended session's record into the dead archive (R-0805).

    ``ended_at`` lets a caller that already knows the moment (e.g. ``ui stop``,
    which just sent the signal) record it precisely; a session found dead by
    a PID check alone has no truer moment than "now".
    """
    import datetime

    file_path = session.get("_file")
    record = {k: v for k, v in session.items() if k != "_file"}
    record["ended_at"] = ended_at or datetime.datetime.now(datetime.timezone.utc).isoformat()
    session_id = Path(file_path).stem if file_path else record.get("job_id", "unknown")
    (_dead_sessions_dir() / f"{session_id}.json").write_text(json.dumps(record, indent=2))
    if file_path:
        _remove_session(file_path)
    _prune_dead_archive()


def _prune_dead_archive() -> None:
    """Keep only the `_DEAD_SESSION_LIMIT` most recently ended sessions."""
    d = _dead_sessions_dir()
    entries: list[tuple[str, Path]] = []
    for f in d.glob("*.json"):
        try:
            data = json.loads(f.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        entries.append((data.get("ended_at", ""), f))
    entries.sort(key=lambda t: t[0])
    while len(entries) > _DEAD_SESSION_LIMIT:
        _, oldest = entries.pop(0)
        oldest.unlink(missing_ok=True)


def _read_dead_sessions() -> list[dict[str, Any]]:
    """Archived dead sessions, most-recently-ended first."""
    d = _dead_sessions_dir()
    results = []
    for f in d.glob("*.json"):
        try:
            results.append(json.loads(f.read_text()))
        except (json.JSONDecodeError, OSError):
            continue
    results.sort(key=lambda r: r.get("ended_at", ""), reverse=True)
    return results


def _prune_dead_and_get_live() -> list[dict[str, Any]]:
    """Archive any session in the live registry whose PID is gone; return survivors."""
    alive = []
    for s in _read_sessions():
        if _is_pid_alive(s.get("pid", 0)):
            alive.append(s)
        else:
            _archive_dead_session(s)
    return alive


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
    json_output: bool = False,
) -> None:
    import secrets

    from packages.orchestration.ui_server import start_ui_server

    _prune_dead_and_get_live()

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
        json_output=json_output,
    )


def _cmd_ui_latest(*, json_output: bool = False) -> None:
    """Open the most recently started UI session."""
    alive = _prune_dead_and_get_live()
    if not alive:
        # DECISION F283 D7's shape: the shared `sys.exit(1)` sits AFTER the
        # if/else, so the text branch's print-then-exit pair is unchanged.
        if json_output:
            fail("ui_session_not_found", "No active UI sessions.", json_output=True)
        else:
            print("No active UI sessions.", file=sys.stderr)
        sys.exit(1)

    latest = alive[-1]
    url = latest.get("url", "")
    job_id = latest.get("job_id", "?")
    pid = latest.get("pid", "?")
    if json_output:
        emit_ok(url=url, job_id=job_id, pid=pid)
    else:
        print(f"Latest UI: {url}")
        print(f"Job: {job_id}")
        print(f"PID: {pid}")

    # Try to open browser
    from packages.orchestration.ui_server import _try_open_browser
    _try_open_browser(url)


def _cmd_ui_status(*, show_all: bool = False, json_output: bool = False) -> None:
    """Show status of UI sessions: live ones always, the last ten dead with --all."""
    alive = _prune_dead_and_get_live()
    dead = _read_dead_sessions() if show_all else []

    if json_output:
        emit_ok(
            sessions=[
                {"job_id": s.get("job_id", "?"), "port": s.get("port", "?"),
                 "pid": s.get("pid", "?"), "url": s.get("url", "?")}
                for s in alive
            ],
            dead=[
                {"job_id": s.get("job_id", "?"), "port": s.get("port", "?"),
                 "pid": s.get("pid", "?"), "ended_at": s.get("ended_at", "?")}
                for s in dead
            ],
        )
        return

    if not alive and not dead:
        print("No UI sessions.")
        return

    for s in alive:
        print(f"  [RUNNING] job={s.get('job_id', '?')} port={s.get('port', '?')} pid={s.get('pid', '?')}")
        print(f"          {s.get('url', '?')}")

    if show_all and dead:
        print("Last dead sessions:")
        for s in dead:
            print(f"  [DEAD] job={s.get('job_id', '?')} port={s.get('port', '?')} "
                  f"pid={s.get('pid', '?')} ended={s.get('ended_at', '?')}")


def _cmd_ui_stop(*, json_output: bool = False) -> None:
    """Stop all running UI sessions, archiving every session this call sees."""
    import datetime

    sessions = _read_sessions()
    stopped = 0
    stopped_entries: list[dict[str, Any]] = []
    failed_entries: list[dict[str, Any]] = []
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    for s in sessions:
        pid = s.get("pid", 0)
        if _is_pid_alive(pid):
            try:
                os.kill(pid, signal.SIGTERM)
                stopped += 1
                stopped_entries.append({"pid": pid, "job_id": s.get("job_id", "?")})
                if not json_output:
                    print(f"  Stopped PID {pid} (job={s.get('job_id', '?')})")
            except OSError as e:
                failed_entries.append({"pid": pid, "job_id": s.get("job_id", "?"), "error": str(e)})
                if not json_output:
                    print(f"  Failed to stop PID {pid}: {e}", file=sys.stderr)
        _archive_dead_session(s, ended_at=now)

    if json_output:
        emit_ok(stopped=stopped_entries, failed=failed_entries)
        return

    if stopped == 0:
        print("No active UI sessions to stop.")
    else:
        print(f"Stopped {stopped} session(s).")


def _cmd_ui_open(job_id_str: str, *, json_output: bool = False) -> None:
    """Open browser for a specific job's UI session."""
    alive = _prune_dead_and_get_live()

    for s in alive:
        if s.get("job_id") == job_id_str:
            url = s.get("url", "")
            if json_output:
                emit_ok(url=url, job_id=job_id_str)
            else:
                print(f"Opening: {url}")
            from packages.orchestration.ui_server import _try_open_browser
            _try_open_browser(url)
            return

    # DECISION F283 D7's shape: the shared `sys.exit(1)` sits AFTER the
    # if/else, so the text branch's two-line stderr refusal is unchanged.
    _message = (
        f"No active UI session for job {job_id_str}.\n"
        "Start one with: remedy ui <job_id>"
    )
    if json_output:
        fail("ui_session_not_found", _message, json_output=True)
    else:
        print(f"No active UI session for job {job_id_str}.", file=sys.stderr)
        print("Start one with: remedy ui <job_id>", file=sys.stderr)
    sys.exit(1)


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "ui.start": lambda args: _cmd_ui_start(
        args.job_id,
        port=int(getattr(args, "port", None) or 8787),
        host=getattr(args, "host", None) or "127.0.0.1",
        open_browser=not getattr(args, "no_open", False),
        info_file=getattr(args, "info_file", None) or None,
        json_output=getattr(args, "json", False),
    ),
    "ui.latest": lambda args: _cmd_ui_latest(json_output=getattr(args, "json", False)),
    "ui.status": lambda args: _cmd_ui_status(
        show_all=getattr(args, "all", False),
        json_output=getattr(args, "json", False),
    ),
    "ui.stop": lambda args: _cmd_ui_stop(json_output=getattr(args, "json", False)),
    "ui.open": lambda args: _cmd_ui_open(args.job_id, json_output=getattr(args, "json", False)),
}
