"""Shared helper for runtime subprocess CLI tests.

Every subprocess gets: timeout, REMEDY_DATA_DIR, captured output, no shell=True.
"""

from __future__ import annotations

import json
import os
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

    Always captures output, always has timeout, never uses shell=True.
    On TimeoutExpired, kills process and re-raises with safe info.
    """
    full_env = {**os.environ, "REMEDY_DATA_DIR": str(root)}
    try:
        return subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped"] + args,
            capture_output=True, text=True, timeout=timeout, env=full_env,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = (exc.stdout or b"").decode("utf-8", errors="replace")[:200] if isinstance(exc.stdout, bytes) else (exc.stdout or "")[:200]
        stderr = (exc.stderr or b"").decode("utf-8", errors="replace")[:200] if isinstance(exc.stderr, bytes) else (exc.stderr or "")[:200]
        raise AssertionError(
            f"CLI subprocess timed out after {timeout}s: {args}\n"
            f"stdout: {stdout}\nstderr: {stderr}"
        ) from exc


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
