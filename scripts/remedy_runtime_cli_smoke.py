#!/usr/bin/env python3
"""Standalone runtime CLI smoke test — runs outside pytest.

Executes propose and/or worker flows via subprocess, verifies results,
exits 0 on success, nonzero on failure.

Usage:
    python scripts/remedy_runtime_cli_smoke.py --mode propose
    python scripts/remedy_runtime_cli_smoke.py --mode worker
    python scripts/remedy_runtime_cli_smoke.py --mode all

Process isolation:
- Popen with start_new_session=True
- stdout/stderr to temp files (no pipe inheritance)
- killpg on timeout
- No shell=True
- No orchestration imports that use flock
- Direct JSON setup only
"""

from __future__ import annotations

import argparse
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

TIMEOUT = 10


def _kill_pg(pgid: int, sig: int) -> None:
    try:
        os.killpg(pgid, sig)
    except (ProcessLookupError, PermissionError):
        pass


def _pg_exists(pgid: int) -> bool:
    try:
        os.killpg(pgid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def _ensure_pg_dead(pgid: int) -> None:
    if not _pg_exists(pgid):
        return
    _kill_pg(pgid, signal.SIGTERM)
    for _ in range(10):
        time.sleep(0.05)
        if not _pg_exists(pgid):
            return
    _kill_pg(pgid, signal.SIGKILL)
    for _ in range(10):
        time.sleep(0.05)
        if not _pg_exists(pgid):
            return


def run_cli(args: list[str], root: Path, timeout: int = TIMEOUT) -> subprocess.CompletedProcess:
    """Run python -m apps.cli.grouped with full process isolation."""
    env = {**os.environ, "REMEDY_DATA_DIR": str(root)}
    cmd = [sys.executable, "-m", "apps.cli.grouped"] + args

    out_f = tempfile.NamedTemporaryFile(mode="w+", suffix=".out", delete=False)
    err_f = tempfile.NamedTemporaryFile(mode="w+", suffix=".err", delete=False)
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=out_f,
            stderr=err_f,
            stdin=subprocess.DEVNULL,
            close_fds=True,
            start_new_session=True,
            env=env,
        )
        pgid = os.getpgid(proc.pid)
        timed_out = False
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            _kill_pg(pgid, signal.SIGTERM)
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                _kill_pg(pgid, signal.SIGKILL)
                proc.wait(timeout=3)
        _ensure_pg_dead(pgid)
        out_f.seek(0)
        err_f.seek(0)
        stdout = out_f.read(64 * 1024)
        stderr = err_f.read(64 * 1024)
    finally:
        out_f.close()
        err_f.close()
        try:
            os.unlink(out_f.name)
        except OSError:
            pass
        try:
            os.unlink(err_f.name)
        except OSError:
            pass

    if timed_out:
        return subprocess.CompletedProcess(cmd, 124, stdout, stderr)

    return subprocess.CompletedProcess(cmd, proc.returncode, stdout, stderr)


def run_json(args: list[str], root: Path) -> dict:
    r = run_cli(args, root)
    if r.returncode != 0:
        raise RuntimeError(f"CLI failed (rc={r.returncode}): {r.stderr[:200]}")
    return json.loads(r.stdout)


def create_env(base: Path) -> tuple[Path, str]:
    root = base / "data"
    jid = str(uuid4())
    jobs_dir = root / "jobs"
    jobs_dir.mkdir(parents=True, exist_ok=True)
    job_data = {
        "id": jid,
        "name": "runtime-smoke",
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


def create_task(root: Path, jid: str, *, title: str = "Smoke", status: str = "proposed") -> str:
    tid = uuid4().hex[:12]
    pt_dir = root / "proposed_tasks"
    pt_dir.mkdir(parents=True, exist_ok=True)
    pt_file = pt_dir / f"{jid}.json"
    existing = json.loads(pt_file.read_text()) if pt_file.exists() else []
    existing.append({
        "id": tid, "title": title, "reason": "", "description": "",
        "source": "reviewer", "risk": "medium", "priority": "medium",
        "status": status, "approval_required": True, "job_id": jid,
        "origin_task_id": "", "origin_recommendation_id": "",
        "task_type": "unknown", "evaluation_notes": "",
        "evaluated_by": "", "evaluated_at": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "resolved_at": None, "materialized_task_id": "", "materialized_at": None,
    })
    pt_file.write_text(json.dumps(existing, indent=2))
    return tid


def read_events(root: Path, jid: str) -> str:
    runs_dir = root / "job_logs" / jid
    if not runs_dir.is_dir():
        return ""
    files = sorted(runs_dir.glob("*.jsonl"))[:5]
    parts = []
    for f in files:
        try:
            parts.append(f.read_text()[:10000])
        except OSError:
            continue
    return "".join(parts)


def check_no_locks(root: Path) -> None:
    locks = list(root.rglob("*.lock"))
    if locks:
        rel = [str(lf.relative_to(root)) for lf in locks]
        raise RuntimeError(f"Leftover lock files: {rel}")


def smoke_propose(base: Path) -> None:
    root, jid = create_env(base)
    tid = create_task(root, jid, title="E2E propose")

    # list
    data = run_json(["propose", "list", jid, "--json"], root)
    assert data["count"] == 1, f"list count: {data['count']}"

    # evaluate
    data = run_json(["propose", "evaluate", jid, "--json"], root)
    assert data["evaluated_count"] == 1

    # approve
    data = run_json(["propose", "approve", jid, tid, "--json"], root)
    assert data["approved"] is True

    # materialize
    data = run_json(["propose", "materialize", jid, "--task-id", tid, "--json"], root)
    assert data["materialized_count"] == 1

    # verify job
    job = json.loads((root / "jobs" / f"{jid}.json").read_text())
    assert len(job["tasks"]) == 1

    # verify events
    events = read_events(root, jid)
    assert "proposed_task_evaluated" in events
    assert "proposed_task_approved" in events
    assert "proposed_task_materialized" in events

    # verify no locks
    check_no_locks(root)

    print(f"  propose: PASS (job={jid[:8]})")


def smoke_worker(base: Path) -> None:
    root, jid = create_env(base)
    tid = create_task(root, jid, title="E2E worker")

    # propose flow
    run_json(["propose", "evaluate", jid, "--json"], root)
    run_json(["propose", "approve", jid, tid, "--json"], root)
    run_json(["propose", "materialize", jid, "--task-id", tid, "--json"], root)

    # enqueue + worker
    run_cli(["job", "enqueue", jid], root)
    data = run_json(["worker", "run", "--once", "--provider", "fixture", "--job", jid, "--json"], root)
    assert data["action_taken"] == "task_completed"
    assert data["work_performed"] is True

    # verify job
    job = json.loads((root / "jobs" / f"{jid}.json").read_text())
    assert len(job["tasks"]) == 1
    assert job["tasks"][0]["status"] == "completed"

    # verify events
    events = read_events(root, jid)
    assert "proposed_task_evaluated" in events
    assert "proposed_task_approved" in events
    assert "proposed_task_materialized" in events
    assert "task_execution_started" in events
    assert "task_execution_completed" in events

    # verify no locks
    check_no_locks(root)

    print(f"  worker: PASS (job={jid[:8]})")


def main() -> int:
    parser = argparse.ArgumentParser(description="Standalone runtime CLI smoke test")
    parser.add_argument("--mode", choices=["propose", "worker", "all"], default="all")
    args = parser.parse_args()

    base = Path(tempfile.mkdtemp(prefix="remedy-smoke-"))
    errors = []

    try:
        if args.mode in ("propose", "all"):
            try:
                smoke_propose(base / "propose")
            except Exception as e:
                errors.append(f"propose: {e}")
                print(f"  propose: FAIL — {e}")

        if args.mode in ("worker", "all"):
            try:
                smoke_worker(base / "worker")
            except Exception as e:
                errors.append(f"worker: {e}")
                print(f"  worker: FAIL — {e}")
    finally:
        # Cleanup temp dir best-effort
        import shutil
        shutil.rmtree(base, ignore_errors=True)

    if errors:
        print(f"FAIL: {len(errors)} error(s)")
        for e in errors:
            print(f"  {e}")
        return 1

    print("runtime smoke: ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
