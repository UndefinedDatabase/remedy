"""Shared helper for runtime subprocess CLI tests.

IMPORTANT: This module must NOT import modules that use fcntl.flock,
because flock fds in the test process can prevent pytest exit on some
platforms. All orchestration state is created via direct JSON writes.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
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


def run_grouped_cli(
    args: list[str],
    root: Path,
    *,
    timeout: int = 10,
) -> subprocess.CompletedProcess:
    """Run python -m apps.cli.grouped with REMEDY_DATA_DIR set."""
    full_env = {**os.environ, "REMEDY_DATA_DIR": str(root)}
    try:
        return subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped"] + args,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=full_env,
            stdin=subprocess.DEVNULL,
            close_fds=True,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = (exc.stdout or "")[:200] if isinstance(exc.stdout, str) else ""
        stderr = (exc.stderr or "")[:200] if isinstance(exc.stderr, str) else ""
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
