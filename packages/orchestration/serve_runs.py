"""The runs the `remedy serve start` supervisor starts (F200, DECISIONs F200 D1 (4) and D4).

The supervisor runs a job the way an operator would: as its own process running
`remedy job run <job>` in direct mode, so the run is the same code path with the
same output, only detached from the terminal that asked for it. Each run has one
record in the `serve` class's `runs/` directory, `<job id>.json`, beside the two
files its output goes to, `<job id>.out` and `<job id>.err`. The record is written
when the run starts and again with its exit code when it ends.

Nothing is kept for later: a job the supervisor is already running is refused, and
a run that cannot start raises. There is no waiting line (DECISION F200 D1 (4)).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass, replace
from datetime import datetime, timezone

from packages.orchestration.serve_paths import ServePaths

#: The environment variable `apps/cli/serve_client.py` reads: a run the supervisor
#: starts runs direct, and never sends a command back to the supervisor.
DIRECT_ENV = "REMEDY_SERVE_DIRECT"


class RunRefused(Exception):
    """Why a run was not started, with the error token the door reports."""

    def __init__(self, token: str, message: str) -> None:
        super().__init__(message)
        self.token = token


@dataclass(frozen=True)
class RunRecord:
    """One run the supervisor started, as `runs/<job id>.json` holds it."""

    job_id: str
    pid: int
    started_at: str
    out_log: str
    err_log: str
    exit_code: int | None = None
    ended_at: str | None = None

    def to_json(self) -> dict:
        return asdict(self)


def job_run_argv(job_id: str) -> list[str]:
    """The command a run executes: `remedy job run <job>`, through this interpreter."""
    return [sys.executable, "-m", "apps.cli.main", "job", "run", job_id]


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_run_record(paths: ServePaths, job_id: str) -> RunRecord | None:
    """The record of JOB_ID's last run, or None when there is none or it cannot be read."""
    try:
        data = json.loads((paths.runs_dir / f"{job_id}.json").read_text(encoding="utf-8"))
        return RunRecord(**data)
    except (OSError, ValueError, TypeError):
        return None


class RunLauncher:
    """Starts runs as child processes and records each one's start and end."""

    def __init__(self, paths: ServePaths, *,
                 argv_for: Callable[[str], Sequence[str]] = job_run_argv) -> None:
        self._paths = paths
        self._argv_for = argv_for
        self._lock = threading.Lock()
        self._children: dict[str, subprocess.Popen] = {}
        self._reapers: dict[str, threading.Thread] = {}

    def _write(self, record: RunRecord) -> None:
        target = self._paths.runs_dir / f"{record.job_id}.json"
        scratch = target.with_suffix(".json.tmp")
        scratch.write_text(json.dumps(record.to_json(), indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
        os.replace(scratch, target)

    def running(self, job_id: str) -> bool:
        """True while a run this launcher started for JOB_ID has not ended."""
        with self._lock:
            child = self._children.get(job_id)
            return child is not None and child.poll() is None

    def start(self, job_id: str) -> RunRecord:
        """Start JOB_ID's run and return its record; refuse a job whose run has not ended."""
        with self._lock:
            child = self._children.get(job_id)
            if child is not None and child.poll() is None:
                raise RunRefused("job_already_running",
                                 f"the serve supervisor is already running job {job_id} "
                                 f"(process {child.pid})")
            self._paths.runs_dir.mkdir(parents=True, exist_ok=True)
            out_log = self._paths.runs_dir / f"{job_id}.out"
            err_log = self._paths.runs_dir / f"{job_id}.err"
            env = {**os.environ, DIRECT_ENV: "1",
                   "REMEDY_DATA_DIR": str(self._paths.root.parent)}
            with open(out_log, "wb") as out, open(err_log, "wb") as err:
                child = subprocess.Popen(list(self._argv_for(job_id)), stdin=subprocess.DEVNULL,
                                         stdout=out, stderr=err, env=env,
                                         start_new_session=True)
            record = RunRecord(job_id=job_id, pid=child.pid, started_at=_now(),
                               out_log=str(out_log), err_log=str(err_log))
            self._write(record)
            self._children[job_id] = child
            reaper = threading.Thread(target=self._reap, args=(child, record), daemon=True,
                                      name=f"remedy-serve-run-{job_id}")
            self._reapers[job_id] = reaper
            reaper.start()
        return record

    def _reap(self, child: subprocess.Popen, record: RunRecord) -> None:
        code = child.wait()
        with self._lock:
            self._write(replace(record, exit_code=code, ended_at=_now()))

    def wait(self, job_id: str, timeout: float | None = None) -> int | None:
        """Wait until JOB_ID's run has ended and its record says so; its exit code, or
        None when this launcher started no run for it or TIMEOUT passed first."""
        with self._lock:
            reaper = self._reapers.get(job_id)
        if reaper is None:
            return None
        reaper.join(timeout)
        if reaper.is_alive():
            return None
        record = read_run_record(self._paths, job_id)
        return None if record is None else record.exit_code
