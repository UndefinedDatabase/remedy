"""Shared helper for runtime subprocess CLI tests.

IMPORTANT: This module must NOT import modules that use fcntl.flock,
because flock fds in the test process can prevent pytest exit on some
platforms. All orchestration state is created via direct JSON writes.

Process isolation strategy:
- Popen with start_new_session=True (new process group)
- stdout/stderr redirected to temp files (no pipe inheritance)
- proc.wait(timeout=...) for bounded wait
- os.killpg(SIGTERM) then os.killpg(SIGKILL) on timeout
- Proven process group cleanup after normal exit
- Diagnostic trace log for debugging order-dependent hangs
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

# Module-level trace log path, set per test root via enable_trace()
_trace_path: Path | None = None


def enable_trace(root: Path) -> Path:
    """Enable diagnostic tracing under root. Returns trace file path."""
    global _trace_path
    _trace_path = root / ".runtime_trace.log"
    return _trace_path


def _trace(msg: str) -> None:
    """Append bounded trace line if tracing is enabled."""
    if _trace_path is None:
        return
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S.%f")[:-3]
    line = f"{ts} {msg}\n"
    try:
        with open(_trace_path, "a") as f:
            # Cap file at 64KB
            if f.tell() > 64 * 1024:
                return
            f.write(line)
    except OSError:
        pass


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
    # Always enable trace for runtime tests
    enable_trace(root)
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


def _process_group_exists(pgid: int) -> bool:
    """Check if a process group still has live processes."""
    try:
        os.killpg(pgid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def _kill_process_group(pgid: int, sig: int) -> None:
    """Best-effort kill a process group."""
    try:
        os.killpg(pgid, sig)
    except (ProcessLookupError, PermissionError):
        pass


def _ensure_process_group_dead(pgid: int) -> None:
    """Prove process group is gone after normal exit. SIGTERM → wait → SIGKILL."""
    if not _process_group_exists(pgid):
        return
    _kill_process_group(pgid, signal.SIGTERM)
    # Brief bounded wait for SIGTERM
    for _ in range(10):
        time.sleep(0.05)
        if not _process_group_exists(pgid):
            return
    # Escalate to SIGKILL
    _kill_process_group(pgid, signal.SIGKILL)
    for _ in range(10):
        time.sleep(0.05)
        if not _process_group_exists(pgid):
            return
    _trace(f"WARN pgid={pgid} still alive after SIGKILL")


def run_grouped_cli(
    args: list[str],
    root: Path,
    *,
    timeout: int = 10,
    cwd: Path | str | None = None,
) -> subprocess.CompletedProcess:
    """Run python -m apps.cli.grouped with REMEDY_DATA_DIR set.

    Uses Popen with temp files for stdout/stderr (no pipe inheritance),
    start_new_session=True for process group isolation, and killpg for
    cleanup on timeout or after normal exit.

    `cwd` runs the child somewhere other than this repository. Several guards
    read repository state RELATIVE to the working directory — the branch guard in
    `self_dogfood_execution.py::_git_head_file` opens `Path(".git")` — so a test
    about such a guard is otherwise asserting against whatever checkout the suite
    happens to run in, and a detached HEAD (what `actions/checkout` produces for
    a pull_request) changes the answer. PYTHONPATH is pinned to the repository
    root whenever `cwd` is set, so `python -m apps.cli.grouped` still resolves
    from the repository and not from the temporary one. The root comes from this
    file's own location rather than from `os.getcwd()`, which a test that chdir'd
    would otherwise decide.
    """
    full_env = {**os.environ, "REMEDY_DATA_DIR": str(root)}
    if cwd is not None:
        full_env["PYTHONPATH"] = str(Path(__file__).resolve().parents[2])
    cmd = [sys.executable, "-m", "apps.cli.grouped"] + args
    args_str = " ".join(args)

    _trace(f"START {args_str}")

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
            cwd=str(cwd) if cwd is not None else None,
        )
        pgid = os.getpgid(proc.pid)

        timed_out = False
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            _trace(f"TIMEOUT {args_str}")
            _kill_process_group(pgid, signal.SIGTERM)
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                _kill_process_group(pgid, signal.SIGKILL)
                proc.wait(timeout=3)

        # Proven cleanup: ensure process group is fully dead
        _ensure_process_group_dead(pgid)

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
        trace_info = ""
        if _trace_path and _trace_path.exists():
            trace_info = f"\ntrace: {_trace_path}"
        raise AssertionError(
            f"CLI subprocess timed out after {timeout}s: {args}\n"
            f"stdout: {stdout_text[:200]}\nstderr: {stderr_text[:200]}"
            f"{trace_info}"
        )

    _trace(f"END rc={proc.returncode} {args_str}")

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
    """Read bounded event content from job_logs/<job_id>/*.jsonl only.

    - Only reads from job_logs/<job_id>/ (no broad directory scans)
    - Caps file count to max_files
    - Caps bytes per file to max_bytes
    - Ignores unreadable files
    """
    runs_dir = root / "job_logs" / job_id
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
