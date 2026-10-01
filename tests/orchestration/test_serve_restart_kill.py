"""F200 D7 — the restart kill test (acceptance, F200 feature file).

The scenario, verbatim from the amended acceptance: "Killing the supervisor and
its runs with SIGKILL and starting it again runs every registered job that
still reads `running` again, to the end F047's kill test proves: each task
executed once and every task green." This module is that proof for the
supervisor, the way ``test_resume_kill.py`` is it for a direct run.

Two real processes die here: the supervisor (``run_supervisor``, in its own
subprocess) and the run it started (a child of THAT subprocess, in its own
session — ``RunLauncher.start`` sets ``start_new_session=True``). Both are
SIGKILLed with nothing given a chance to clean up, and a second supervisor is
started on the same data root afterward. Synchronisation is by marker file and
registry polling, never by sleeping: the fixture run writes a marker at the
instant it begins the task that must die in flight, then blocks; a resumed run
checks the marker, finds it already there, and never blocks again.

Exactly-once is proven from the CYCLE EVIDENCE RECORDS on disk
(``evidence/cycles/cycle_*.json``, field ``executed_task_ids``), which span
both the killed process and the resumed one — the same evidence
``test_resume_kill.py`` reads, because nothing about what counts as "once" is
specific to how a run was launched.
"""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

from packages.orchestration.serve_daemon import socket_answers
from packages.orchestration.serve_paths import serve_paths
from packages.orchestration.serve_runs import read_run_record

REPO_ROOT = Path(__file__).resolve().parents[2]

#: Tasks in the fixture job, and the cycle whose task is killed in flight.
TOTAL_TASKS = 5
KILL_ON_CYCLE = 3

#: Deadlines for the polling loops below; none of them ever bare-sleeps.
READY_TIMEOUT_SECONDS = 15.0
MARKER_TIMEOUT_SECONDS = 25.0
END_TIMEOUT_SECONDS = 30.0
POLL_SECONDS = 0.02

#: The fixture run: a stand-in for `remedy job run` that executes real cycles
#: through `run_cycles`, sets the job's own state to `running` the way the real
#: `run_job` does (DECISION F200 D7's restart reads exactly this field), and —
#: on its FIRST execution only, told apart by the marker not existing yet —
#: parks itself mid-task so the test can SIGKILL it in flight.
FIXTURE_RUN_SOURCE = '''
import json
import sys
import time
from pathlib import Path

from packages.core.models import RunState
from packages.orchestration.long_run_executor import CycleLimits, TaskAttempt, run_cycles
from packages.orchestration.pingpong_job import require_job_plan, save_job_plan

JOB_ID = sys.argv[1]
MARKER = Path(sys.argv[2])
KILL_ON_CYCLE = int(sys.argv[3])
TOTAL_TASKS = int(sys.argv[4])

job = require_job_plan(JOB_ID)
first_execution = not MARKER.exists()
if job.state != RunState.RUNNING:
    job.state = RunState.RUNNING
    save_job_plan(job)

_cycle = {"n": 0}


def step(j, _provider):
    pending = [t for t in j.tasks if t.status == RunState.PENDING]
    if not pending:
        return TaskAttempt()
    task = pending[0]
    _cycle["n"] += 1
    if first_execution and _cycle["n"] == KILL_ON_CYCLE:
        MARKER.write_text(json.dumps({"task_id": task.task_id}), encoding="utf-8")
        while True:
            time.sleep(0.05)            # the test kills us here
    task.status = RunState.COMPLETED
    return TaskAttempt(task_id=task.task_id, executed=True, verified=True)


result = run_cycles(job, CycleLimits(max_cycles=TOTAL_TASKS + 2), lambda _ctx: None,
                    task_step=step)
print(json.dumps({"terminal_status": result.terminal_status, "job_id": JOB_ID}))
'''

#: Starts one supervisor on an explicit data root, with RUN_ARGV built from
#: argv rather than a closure — a real subprocess cannot be handed a Python
#: callable, so this script is the whole of what runs in it.
SUPERVISOR_SOURCE = '''
import sys
from pathlib import Path

from packages.orchestration.serve_daemon import run_supervisor

root = Path(sys.argv[1])
fixture_run = sys.argv[2]
marker = sys.argv[3]
kill_on_cycle = sys.argv[4]
total_tasks = sys.argv[5]


def run_argv(job_id):
    return [sys.executable, fixture_run, job_id, marker, kill_on_cycle, total_tasks]


run_supervisor(root, run_argv=run_argv)
'''


def _env(data_root: Path) -> dict[str, str]:
    env = dict(os.environ)
    env["REMEDY_DATA_DIR"] = str(data_root)
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONUNBUFFERED"] = "1"
    return env


def _start_supervisor(root: Path, fixture_run: Path, marker: Path, script: Path) -> subprocess.Popen:
    return subprocess.Popen(
        [sys.executable, str(script), str(root), str(fixture_run), str(marker),
         str(KILL_ON_CYCLE), str(TOTAL_TASKS)],
        cwd=str(REPO_ROOT), env=_env(root),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def _wait_until(deadline_seconds: float, what: str, check) -> None:
    deadline = time.monotonic() + deadline_seconds
    while time.monotonic() < deadline:
        if check():
            return
        time.sleep(POLL_SECONDS)
    raise AssertionError(f"timed out waiting for {what}")


def _post_run(root: Path, job_id: str) -> None:
    from packages.orchestration.serve_daemon import post_command

    status, body = post_command(root, job_id, {"command": "job.run", "client_nonce": "restart-kill"})
    assert status == 200, body


def executed_task_ids(data_root: Path, job_id: str) -> list[str]:
    """Every task id recorded as EXECUTED, read from disk, across both processes."""
    directory = data_root / "jobs" / job_id / "evidence" / "cycles"
    ids: list[str] = []
    for path in sorted(directory.glob("cycle_*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        ids.extend(record.get("executed_task_ids", []))
    return ids


def test_restart_after_sigkill_resumes_the_job_with_each_task_executed_exactly_once(tmp_path):
    from packages.orchestration.data_paths import normalize_job_id
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry, load_job_plan, save_job_plan

    root = tmp_path / "data"
    root.mkdir()
    marker = tmp_path / "marker.json"
    fixture_run = tmp_path / "fixture_run.py"
    fixture_run.write_text(FIXTURE_RUN_SOURCE, encoding="utf-8")
    supervisor_script = tmp_path / "run_supervisor_cmd.py"
    supervisor_script.write_text(SUPERVISOR_SOURCE, encoding="utf-8")

    job = JobPlan(job_title="restart-kill-fixture",
                 tasks=[TaskEntry(title=f"t{i}", body="d") for i in range(TOTAL_TASKS)])
    save_job_plan(job, root)
    job_id = str(job.job_id)
    paths = serve_paths(root)

    supervisor_one: subprocess.Popen | None = None
    supervisor_two: subprocess.Popen | None = None
    run_pid: int | None = None
    try:
        supervisor_one = _start_supervisor(root, fixture_run, marker, supervisor_script)
        _wait_until(READY_TIMEOUT_SECONDS, "the first supervisor's socket to answer",
                   lambda: socket_answers(paths.socket) or supervisor_one.poll() is not None)
        assert supervisor_one.poll() is None, (
            f"the first supervisor exited early:\n{supervisor_one.stderr.read()}")

        _post_run(root, job_id)
        _wait_until(MARKER_TIMEOUT_SECONDS, "the doomed task's marker", marker.exists)

        record = read_run_record(paths, job_id)
        assert record is not None and record.exit_code is None
        run_pid = record.pid

        # SIGKILL both: the supervisor, and the run it started (its own session).
        os.kill(supervisor_one.pid, signal.SIGKILL)
        try:
            os.killpg(run_pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        supervisor_one.wait(timeout=10)

        _wait_until(READY_TIMEOUT_SECONDS, "the killed socket to stop answering",
                   lambda: not socket_answers(paths.socket))

        supervisor_two = _start_supervisor(root, fixture_run, marker, supervisor_script)
        _wait_until(READY_TIMEOUT_SECONDS, "the second supervisor's socket to answer",
                   lambda: socket_answers(paths.socket) or supervisor_two.poll() is not None)
        assert supervisor_two.poll() is None, (
            f"the second supervisor exited early:\n{supervisor_two.stderr.read()}")

        def resumed_and_ended() -> bool:
            current = read_run_record(paths, job_id)
            return (current is not None and current.pid != run_pid
                   and current.exit_code is not None)

        _wait_until(END_TIMEOUT_SECONDS, "the resumed run to record its end", resumed_and_ended)

        ended = read_run_record(paths, job_id)
        assert ended.exit_code == 0, Path(ended.err_log).read_text(encoding="utf-8")

        after = executed_task_ids(root, job_id)
        counts = Counter(after)
        duplicated = {tid: n for tid, n in counts.items() if n > 1}
        assert not duplicated, f"tasks executed more than once: {duplicated}"
        assert len(after) == TOTAL_TASKS

        finished = load_job_plan(normalize_job_id(job_id), root)
        assert all(t.status == "completed" for t in finished.tasks)
        assert finished.state == "completed"
    finally:
        for proc in (supervisor_one, supervisor_two):
            if proc is not None and proc.poll() is None:
                proc.kill()
                proc.wait(timeout=10)
        if run_pid is not None:
            try:
                os.killpg(run_pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass
