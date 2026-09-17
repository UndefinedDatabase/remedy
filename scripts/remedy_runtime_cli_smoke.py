#!/usr/bin/env python3
"""Standalone runtime CLI smoke test — runs outside pytest.

Executes the propose flow via subprocess, verifies results,
exits 0 on success, nonzero on failure.

Usage:
    python scripts/remedy_runtime_cli_smoke.py --mode propose
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
    # The unified job record: a sixteen-hex id and `jobs/<id>/job.json`.
    jid = uuid4().hex[:16]
    record_dir = root / "jobs" / jid
    record_dir.mkdir(parents=True, exist_ok=True)
    job_data = {
        "job_id": jid,
        "job_title": "runtime-smoke",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "tasks": [],
        "status": "pending",
        "artifacts": [],
        "budget": {"max_steps": 10, "max_tokens": 0, "max_cost_usd": 0.0},
        "metadata": {},
    }
    (record_dir / "job.json").write_text(json.dumps(job_data, indent=2))
    return root, jid


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Standalone runtime CLI smoke test")
    parser.add_argument("--mode", choices=["all"], default="all")
    args = parser.parse_args()

    base = Path(tempfile.mkdtemp(prefix="remedy-smoke-"))
    errors = []

    try:
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
