"""Shared helper for runtime subprocess CLI tests.

IMPORTANT: This module must NOT import modules that use fcntl.flock,
because flock fds in the test process can prevent pytest exit on some
platforms. All orchestration state is created via direct JSON writes.

Process isolation strategy:
- Popen with start_new_session=True (new process group)
- stdout/stderr redirected to temp files (no pipe inheritance)
- proc.wait(timeout=...) for bounded wait
- os.killpg(SIGTERM) then os.killpg(SIGKILL) on timeout
- Best-effort kill remaining group children after normal exit
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


def create_test_env(tmp_path: Path) -> tuple[Path, str]:
    """Create isolated data root with unique Job via direct JSON write."""
    root = tmp_path / "data"
    jid = str(uuid4())
    jobs_dir = root / "jobs"
    jobs_dir.mkdir(parents=True, exist_ok=True)
    job_data = {
        "id": jid,
        "name": "runtime-test",
        "user_prompt": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "tasks": [],
        "state": "pending",
        "artifacts": [],
        "budget": {"max_steps": 10, "max_tokens": 0, "max_cost_usd": 0.0},
        "metadata": {},
    }
    (jobs_dir / f"{jid}.json").write_text(json.dumps(job_data, indent=2))
    return root, jid


def create_proposed_task(
    root: Path,
    job_id: str,
    *,
    title: str = "Test task",
    risk: str = "medium",
    status: str = "proposed",
) -> str:
    """Create a ProposedTask via direct JSON write (no flock)."""
    task_id = uuid4().hex[:12]
    pt_dir = root / "proposed_tasks"
    pt_dir.mkdir(parents=True, exist_ok=True)
    pt_file = pt_dir / f"{job_id}.json"

    existing = []
    if pt_file.exists():
        existing = json.loads(pt_file.read_text())

    task = {
        "id": task_id,
        "title": title,
        "reason": "",
        "description": "",
        "source": "reviewer",
        "risk": risk,
        "priority": "medium",
        "status": status,
        "approval_required": True,
        "job_id": job_id,
        "origin_task_id": "",
        "origin_recommendation_id": "",
        "task_type": "unknown",
        "evaluation_notes": "",
        "evaluated_by": "",
        "evaluated_at": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "resolved_at": None,
        "materialized_task_id": "",
        "materialized_at": None,
    }
    existing.append(task)
    pt_file.write_text(json.dumps(existing, indent=2))
    return task_id


def _kill_process_group(pgid: int, sig: int) -> None:
    """Best-effort kill a process group."""
    try:
        os.killpg(pgid, sig)
    except (ProcessLookupError, PermissionError):
        pass


def run_grouped_cli(
    args: list[str],
    root: Path,
    *,
    timeout: int = 10,
) -> subprocess.CompletedProcess:
    """Run python -m apps.cli.grouped with REMEDY_DATA_DIR set.

    Uses Popen with temp files for stdout/stderr (no pipe inheritance),
    start_new_session=True for process group isolation, and killpg for
    cleanup on timeout or after normal exit.
    """
    full_env = {**os.environ, "REMEDY_DATA_DIR": str(root)}
    cmd = [sys.executable, "-m", "apps.cli.grouped"] + args

    stdout_file = tempfile.NamedTemporaryFile(
        mode="w+", suffix=".stdout", delete=False
    )
    stderr_file = tempfile.NamedTemporaryFile(
        mode="w+", suffix=".stderr", delete=False
    )
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=stdout_file,
            stderr=stderr_file,
            stdin=subprocess.DEVNULL,
            close_fds=True,
            start_new_session=True,
            env=full_env,
        )
        pgid = os.getpgid(proc.pid)

        timed_out = False
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            # SIGTERM the process group
            _kill_process_group(pgid, signal.SIGTERM)
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                # SIGKILL if SIGTERM didn't work
                _kill_process_group(pgid, signal.SIGKILL)
                proc.wait(timeout=3)

        # Best-effort kill remaining children in the process group
        _kill_process_group(pgid, signal.SIGTERM)

        # Read bounded output from temp files
        stdout_file.seek(0)
        stderr_file.seek(0)
        stdout_text = stdout_file.read(64 * 1024)  # 64KB cap
        stderr_text = stderr_file.read(64 * 1024)  # 64KB cap
    finally:
        stdout_file.close()
        stderr_file.close()
        try:
            os.unlink(stdout_file.name)
        except OSError:
            pass
        try:
            os.unlink(stderr_file.name)
        except OSError:
            pass

    if timed_out:
        raise AssertionError(
            f"CLI subprocess timed out after {timeout}s: {args}\n"
            f"stdout: {stdout_text[:200]}\nstderr: {stderr_text[:200]}"
        )

    return subprocess.CompletedProcess(
        args=cmd,
        returncode=proc.returncode,
        stdout=stdout_text,
        stderr=stderr_text,
    )


def run_json(args: list[str], root: Path, *, timeout: int = 10) -> dict:
    """Run CLI, parse JSON stdout, fail on non-zero or parse error."""
    r = run_grouped_cli(args, root, timeout=timeout)
    assert r.returncode == 0, f"CLI failed (rc={r.returncode}): {r.stderr[:200]}"
    return json.loads(r.stdout)


def read_events(root: Path, job_id: str, *, max_files: int = 5, max_bytes: int = 10000) -> str:
    """Read bounded event content from runs/<job_id>/*.jsonl only.

    - Only reads from runs/<job_id>/ (no broad directory scans)
    - Caps file count to max_files
    - Caps bytes per file to max_bytes
    - Ignores unreadable files
    """
    runs_dir = root / "runs" / job_id
    if not runs_dir.is_dir():
        return ""
    files = sorted(runs_dir.glob("*.jsonl"))[:max_files]
    parts = []
    for f in files:
        try:
            parts.append(f.read_text()[:max_bytes])
        except (OSError, UnicodeDecodeError):
            continue
    return "".join(parts)


def assert_no_leftover_locks(root: Path) -> None:
    """Fail if any *.lock files remain under root.

    Uses Path.rglob — no flock imports needed.
    Reports relative filenames for clarity.
    """
    lock_files = list(root.rglob("*.lock"))
    if lock_files:
        rel = [str(lf.relative_to(root)) for lf in lock_files]
        raise AssertionError(f"Leftover lock files found: {rel}")
