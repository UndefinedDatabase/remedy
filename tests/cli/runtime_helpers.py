"""Shared helper for runtime subprocess CLI tests.

Every subprocess gets: timeout, REMEDY_DATA_DIR, captured output, no shell=True.
Subprocesses run in a new session to prevent fd/lock inheritance hangs.
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
from pathlib import Path
from uuid import UUID, uuid4

from packages.core.models import Job
from packages.orchestration.storage import save_job


def create_test_env(tmp_path: Path) -> tuple[Path, str]:
    """Create isolated data root with unique Job. Returns (root, job_id)."""
    root = tmp_path / "data"
    jid = str(uuid4())
    job = Job(id=UUID(jid), name="runtime-test")
    save_job(job, root)
    return root, jid


def run_grouped_cli(
    args: list[str],
    root: Path,
    *,
    timeout: int = 10,
) -> subprocess.CompletedProcess:
    """Run python -m apps.cli.grouped with REMEDY_DATA_DIR set.

    Uses start_new_session=True to isolate subprocess from parent fds/locks.
    Always captures output, always has timeout, never uses shell=True.
    """
    full_env = {**os.environ, "REMEDY_DATA_DIR": str(root)}
    proc = subprocess.Popen(
        [sys.executable, "-m", "apps.cli.grouped"] + args,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env=full_env, start_new_session=True,
    )
    try:
        stdout_bytes, stderr_bytes = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        stdout_bytes, stderr_bytes = proc.communicate(timeout=5)
        stdout = stdout_bytes.decode("utf-8", errors="replace")[:200]
        stderr = stderr_bytes.decode("utf-8", errors="replace")[:200]
        raise AssertionError(
            f"CLI subprocess timed out after {timeout}s: {args}\n"
            f"stdout: {stdout}\nstderr: {stderr}"
        )
    return subprocess.CompletedProcess(
        args=proc.args,
        returncode=proc.returncode,
        stdout=stdout_bytes.decode("utf-8", errors="replace"),
        stderr=stderr_bytes.decode("utf-8", errors="replace"),
    )


def run_json(args: list[str], root: Path, *, timeout: int = 10) -> dict:
    """Run CLI, parse JSON stdout, fail on non-zero or parse error."""
    r = run_grouped_cli(args, root, timeout=timeout)
    assert r.returncode == 0, f"CLI failed (rc={r.returncode}): {r.stderr[:200]}"
    return json.loads(r.stdout)


def read_events(root: Path, job_id: str, max_files: int = 5) -> str:
    """Read bounded event content from runs/<job_id>/*.jsonl."""
    runs_dir = root / "runs" / job_id
    if not runs_dir.exists():
        return ""
    files = sorted(runs_dir.glob("*.jsonl"))[:max_files]
    return "".join(f.read_text()[:10000] for f in files)


def assert_no_leftover_locks(root: Path) -> None:
    """Assert no .lock files remain in proposal store under root."""
    pt_dir = root / "proposed_tasks"
    if not pt_dir.exists():
        return
    locks = list(pt_dir.glob("*.lock"))
    assert not locks, f"Leftover lock files: {[l.name for l in locks]}"
