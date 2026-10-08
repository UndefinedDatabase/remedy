"""The runs the `remedy serve start` supervisor starts (F200, DECISIONs F200 D1 (4) and D4).

The supervisor runs a job the way an operator would: as its own process running
`remedy job run <job>` in direct mode, so the run is the same code path with the
same output, only detached from the terminal that asked for it. Each run has one
record in the `serve` class's `runs/` directory, `<job id>.json`, beside the two
files its output goes to, `<job id>.out` and `<job id>.err`. The record is written
when the run starts and again with its exit code when it ends.

Nothing is kept for later: a job the supervisor is already running is refused, and
a run that cannot start raises. There is no waiting line (DECISION F200 D1 (4)).

A restart reconciles the registry (DECISION F200 D7, `RunLauncher.resume_registered`):
a record whose end was never written is ADOPTED when its process still answers to
that job (the launcher refuses a second `start` of it, a watcher thread records its
end once it is gone), RESTARTED when its job's own record still reads `running`
(or left FAILED, untouched, when that restart could not even launch), or marked
LOST — nothing to resume.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.orchestration.serve_paths import ServePaths

#: The environment variable `apps/cli/serve_client.py` reads: a run the supervisor
#: starts runs direct, and never sends a command back to the supervisor.
DIRECT_ENV = "REMEDY_SERVE_DIRECT"

#: The directory that holds this code's `apps` and `packages`, put first on a run's
#: import path so that `-m apps.cli.main` runs the supervisor's own code wherever
#: the supervisor was started from.
CODE_ROOT = Path(__file__).resolve().parents[2]

#: The longest a command a write route runs may take before it is killed (DECISION F253 D9).
PUBLIC_API_COMMAND_TIMEOUT_SECONDS = 120


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


def child_environment(paths: ServePaths) -> dict[str, str]:
    """The environment of a child the supervisor starts: direct mode, its data root, its code first."""
    return {**os.environ, DIRECT_ENV: "1",
            "REMEDY_DATA_DIR": str(paths.root.parent),
            "PYTHONPATH": os.pathsep.join(
                p for p in (str(CODE_ROOT), os.environ.get("PYTHONPATH", "")) if p)}


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_run_record(paths: ServePaths, job_id: str) -> RunRecord | None:
    """The record of JOB_ID's last run, or None when there is none or it cannot be read."""
    try:
        data = json.loads((paths.runs_dir / f"{job_id}.json").read_text(encoding="utf-8"))
        return RunRecord(**data)
    except (OSError, ValueError, TypeError):
        return None


#: How often an adopted run's watcher checks whether its process has ended.
ADOPT_POLL_SECONDS = 0.2


def _process_is_alive(pid: int) -> bool:
    """True when PID names a live, non-zombie process, by the best check this platform offers.

    A zombie entry (state ``Z``) is treated as gone, not alive: its work is
    already finished and only its exit status is waiting on a parent that will
    never call `wait` on it — the adopted process's real parent died with the
    old supervisor, and this one is not its parent either, so that reap is
    somebody else's job (the kernel's subreaper, usually pid 1) and may lag.
    Waiting on that lag would leave `running()` reporting an adopted job as
    running after its last task already finished.
    """
    proc_dir = Path("/proc") / str(pid)
    if proc_dir.parent.exists():
        try:
            fields = proc_dir.joinpath("stat").read_text().rsplit(") ", 1)[-1].split(" ")
        except OSError:
            return False
        return fields[0] != "Z"
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _process_is_this_job(pid: int, job_id: str) -> bool:
    """True when PID is alive and is the run JOB_ID started (DECISION F200 D7).

    On Linux, ``/proc/<pid>/cmdline`` is argv joined by NUL bytes; JOB_ID must be
    one whole argument, not a substring of one, so a job id that happens to
    prefix another never matches, and a pid the kernel reused for an unrelated
    process is correctly read as "not this run" rather than adopted by mistake.
    Elsewhere `/proc` does not exist and another process's argv cannot be read
    without extra privilege, so aliveness alone stands in; the pid-reuse gap
    that leaves is accepted, the same way SIGKILL detection of foreign
    processes is out of scope for this feature.
    """
    proc_dir = Path("/proc")
    if proc_dir.exists():
        try:
            raw = (proc_dir / str(pid) / "cmdline").read_bytes()
        except OSError:
            return False
        return job_id.encode("utf-8") in [arg for arg in raw.split(b"\0") if arg]
    return _process_is_alive(pid)


class RunLauncher:
    """Starts runs as child processes and records each one's start and end."""

    def __init__(self, paths: ServePaths, *,
                 argv_for: Callable[[str], Sequence[str]] = job_run_argv) -> None:
        self._paths = paths
        self._argv_for = argv_for
        self._lock = threading.Lock()
        self._children: dict[str, subprocess.Popen] = {}
        self._reapers: dict[str, threading.Thread] = {}
        #: Job ids adopted from a previous supervisor (DECISION F200 D7): this
        #: launcher started no child for them, but a `start` is refused and
        #: `running` reports True until a watcher thread records their end.
        self._adopted: set[str] = set()

    def _write(self, record: RunRecord) -> None:
        target = self._paths.runs_dir / f"{record.job_id}.json"
        scratch = target.with_suffix(".json.tmp")
        scratch.write_text(json.dumps(record.to_json(), indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
        os.replace(scratch, target)

    def running(self, job_id: str) -> bool:
        """True while a run this launcher started or adopted for JOB_ID has not ended."""
        with self._lock:
            if job_id in self._adopted:
                return True
            child = self._children.get(job_id)
            return child is not None and child.poll() is None

    def start(self, job_id: str, *, json_output: bool = False) -> RunRecord:
        """Start JOB_ID's run and return its record; refuse a job whose run has not ended.

        JSON_OUTPUT adds `--json` to the run's command, the one option a run started
        through the supervisor takes (DECISION F200 D5). A job adopted after a
        restart (DECISION F200 D7) is refused exactly as a child this launcher
        started itself is.
        """
        with self._lock:
            if job_id in self._adopted:
                raise RunRefused("job_already_running",
                                 f"the serve supervisor is already running job {job_id} "
                                 f"(adopted from before a restart)")
            child = self._children.get(job_id)
            if child is not None and child.poll() is None:
                raise RunRefused("job_already_running",
                                 f"the serve supervisor is already running job {job_id} "
                                 f"(process {child.pid})")
            self._paths.runs_dir.mkdir(parents=True, exist_ok=True)
            out_log = self._paths.runs_dir / f"{job_id}.out"
            err_log = self._paths.runs_dir / f"{job_id}.err"
            env = child_environment(self._paths)
            argv = [*self._argv_for(job_id), *(["--json"] if json_output else [])]
            with open(out_log, "wb") as out, open(err_log, "wb") as err:
                child = subprocess.Popen(argv, stdin=subprocess.DEVNULL,
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

    def resume_registered(self, *, job_is_running: Callable[[str], bool] | None = None
                          ) -> list[dict[str, str]]:
        """Reconcile every run this data root's registry still names as open.

        DECISION F200 D7. Called once, when the supervisor starts, before it
        answers its socket. Every ``runs/<job id>.json`` whose ``exit_code`` is
        None — its end was never recorded — is one of these:

        * its process is still running THAT job (:func:`_process_is_this_job`) —
          ADOPTED: a second `start` of it is refused exactly as for a child this
          launcher started itself, and a thread polls until it is gone and then
          writes its end, `exit_code` staying None because this supervisor is
          not its parent and the kernel never tells it one;
        * else the job's own record (read through JOB_IS_RUNNING) still reads
          `running` — RESTARTED: a fresh `start`, same as any other run; if
          that raises OSError (the run could not even be launched), the
          outcome is FAILED instead and the stale record is left exactly as it
          was, so the next restart attempt tries it again;
        * else — LOST: its end is written with `exit_code` None, nothing to
          resume.

        A record that cannot be read is skipped, and one job's FAILED start
        never stops another record in the same registry from being reconciled.
        JOB_IS_RUNNING answers whether one job's own plan reads `running`;
        tests replace it the way they replace `argv_for`. Returns one
        `{"job_id", "action"}` dict per reconciled job, ACTION one of
        `"adopted"`, `"restarted"`, `"failed"`, `"lost"`, so a caller or a test
        can assert what happened.
        """
        if job_is_running is None:
            job_is_running = self._job_is_running
        if not self._paths.runs_dir.is_dir():
            return []
        outcomes: list[dict[str, str]] = []
        for job_id in sorted(p.stem for p in self._paths.runs_dir.glob("*.json")):
            record = read_run_record(self._paths, job_id)
            if record is None or record.exit_code is not None:
                continue
            if _process_is_this_job(record.pid, job_id):
                self._adopt(record)
                outcomes.append({"job_id": job_id, "action": "adopted"})
            elif job_is_running(job_id):
                try:
                    self.start(job_id)
                except OSError:
                    outcomes.append({"job_id": job_id, "action": "failed"})
                else:
                    outcomes.append({"job_id": job_id, "action": "restarted"})
            else:
                with self._lock:
                    self._write(replace(record, ended_at=_now()))
                outcomes.append({"job_id": job_id, "action": "lost"})
        return outcomes

    def _job_is_running(self, job_id: str) -> bool:
        """True when JOB_ID's own job record — not this launcher's run record — reads `running`.

        Reads through :func:`load_job_plan_safe`, which never raises: a record
        of the wrong shape reads as not running, the same as a missing one, so
        one rotten job record cannot stop the supervisor from starting.
        """
        from packages.orchestration.pingpong_job import JOB_RUNNING, load_job_plan_safe

        plan, _degraded = load_job_plan_safe(job_id, self._paths.root.parent)
        return plan is not None and plan.state == JOB_RUNNING

    def _adopt(self, record: RunRecord) -> None:
        """Start a thread that watches an inherited run's process until it ends."""
        with self._lock:
            self._adopted.add(record.job_id)
            watcher = threading.Thread(target=self._watch_adopted, args=(record,), daemon=True,
                                       name=f"remedy-serve-adopt-{record.job_id}")
            self._reapers[record.job_id] = watcher
            watcher.start()

    def _watch_adopted(self, record: RunRecord) -> None:
        """Poll until RECORD's process is gone, then write its end.

        `exit_code` stays None: this supervisor did not start this process and
        is not its parent, so the kernel never reports an exit code to it.
        """
        while _process_is_alive(record.pid):
            time.sleep(ADOPT_POLL_SECONDS)
        with self._lock:
            self._adopted.discard(record.job_id)
            self._write(replace(record, ended_at=_now()))

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


class CommandRunner:
    """Runs one command line command as a child of the supervisor and returns its envelope.

    DECISION F253 D9. A write route under `/api/v1` answers what the command
    answers, so it runs the command rather than copying its logic: the child
    gets the environment of a run (:func:`child_environment`), and at most one
    command runs for a job at a time, while commands for two jobs may overlap.
    """

    def __init__(self, paths: ServePaths, *,
                 timeout: float = PUBLIC_API_COMMAND_TIMEOUT_SECONDS,
                 argv_prefix: Sequence[str] | None = None) -> None:
        self._paths = paths
        self.timeout = timeout
        self._prefix = (list(argv_prefix) if argv_prefix is not None
                        else [sys.executable, "-m", "apps.cli.main"])
        self._guard = threading.Lock()
        self._job_locks: dict[str, threading.Lock] = {}

    def _lock_for(self, job_id: str) -> threading.Lock:
        with self._guard:
            return self._job_locks.setdefault(job_id, threading.Lock())

    def run(self, job_id: str, argv: Sequence[str]) -> dict[str, Any] | None:
        """The envelope the command prints, or None when it prints none or outlives the timeout.

        The envelope is the last non-empty line of standard output, parsed as
        JSON, when that is an object holding the key `ok`.
        """
        with self._lock_for(job_id):
            try:
                done = subprocess.run([*self._prefix, *argv], stdin=subprocess.DEVNULL,
                                      capture_output=True, text=True, errors="replace",
                                      env=child_environment(self._paths),
                                      timeout=self.timeout)
            except (subprocess.TimeoutExpired, OSError):
                return None
        lines = [line for line in done.stdout.splitlines() if line.strip()]
        if not lines:
            return None
        try:
            envelope = json.loads(lines[-1])
        except ValueError:
            return None
        return envelope if isinstance(envelope, dict) and "ok" in envelope else None
