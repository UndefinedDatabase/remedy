"""F047 T003 — the kill test: SIGKILL mid-cycle, then resume (acceptance).

The scenario, verbatim from the feature file: start a fixture multi-cycle
run, kill -9 mid-cycle, resume, and assert completion with EACH TASK
EXECUTED EXACTLY ONCE.

Two things make the proof real rather than decorative:

* the kill is a genuine ``SIGKILL`` to a genuine child process — no
  exception is raised inside the run, no cleanup handler gets to tidy up,
  and nothing in the run's own code path can know it is about to die;
* exactly-once is proven from the CYCLE EVIDENCE RECORDS on disk
  (``evidence/cycles/cycle_*.json``, field ``executed_task_ids``), which
  span BOTH processes.  A counter in the test process could not see what
  the killed process did, and would be exactly the kind of evidence this
  feature exists to distrust.

Synchronisation is by marker file, never by sleeping: the child writes a
marker at the instant it begins the task that must die in flight, then
blocks; the parent polls for that marker and sends the signal.  A test that
slept would be racy on a loaded machine and slow on an idle one.

What is deliberately NOT here (feature-file "Do not touch"): daemonisation,
schedulers, cross-machine resume, and SIGKILL detection of foreign
processes.  The child is our own subprocess and we know its pid.
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

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

#: Cycles the fixture job is allowed, and the cycle whose task is killed.
TOTAL_TASKS = 5
KILL_ON_CYCLE = 3

#: How long the parent waits for a marker before declaring the child stuck.
MARKER_TIMEOUT_SECONDS = 25.0
POLL_SECONDS = 0.02


# ---------------------------------------------------------------------------
# The child: a real multi-cycle run that parks itself mid-cycle
# ---------------------------------------------------------------------------

CHILD_SOURCE = '''
"""Fixture multi-cycle run. Executes one task per cycle and, on the cycle
named by KILL_ON_CYCLE, writes a marker and blocks forever so the parent can
SIGKILL it with a task genuinely in flight."""
import json
import sys
import time
from pathlib import Path

from packages.core.models import Job, RunState, Task
from packages.orchestration.long_run_executor import (
    CycleLimits,
    TaskAttempt,
    run_cycles,
)
from packages.orchestration.storage import load_job, save_job

MARKER = Path(sys.argv[1])
JOB_FILE = Path(sys.argv[2])
KILL_ON_CYCLE = int(sys.argv[3])
TOTAL_TASKS = int(sys.argv[4])
MODE = sys.argv[5]                     # "first" | "resume"

if MODE == "first":
    job = Job(name="kill-fixture",
              tasks=[Task(title=f"t{i}", description="d") for i in range(TOTAL_TASKS)])
    save_job(job)
    JOB_FILE.write_text(str(job.id), encoding="utf-8")
else:
    job = load_job(__import__("uuid").UUID(JOB_FILE.read_text(encoding="utf-8")))

_cycle = {"n": 0}


def step(j, _provider):
    """Complete exactly one pending task — or park forever, in flight."""
    pending = [t for t in j.tasks if t.status == RunState.PENDING]
    if not pending:
        return TaskAttempt()
    task = pending[0]
    _cycle["n"] += 1
    if MODE == "first" and _cycle["n"] == KILL_ON_CYCLE:
        # In flight: the task is picked but NOT completed and NOT recorded.
        MARKER.write_text(json.dumps({"cycle": _cycle["n"], "task_id": str(task.id)}),
                          encoding="utf-8")
        while True:
            time.sleep(0.05)            # the parent kills us here
    task.status = RunState.COMPLETED
    return TaskAttempt(task_id=task.id, executed=True, verified=True)


result = run_cycles(
    job,
    CycleLimits(max_cycles=TOTAL_TASKS + 2),
    lambda _ctx: None,
    task_step=step,
)
print(json.dumps({"terminal_status": result.terminal_status,
                  "cycles_run": result.cycles_run,
                  "job_id": str(job.id)}))
'''


def _child_env(data_dir: Path) -> dict[str, str]:
    env = dict(os.environ)
    env["REMEDY_DATA_DIR"] = str(data_dir)
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONUNBUFFERED"] = "1"
    return env


def _wait_for(path: Path, proc: subprocess.Popen) -> dict:
    """Poll for the child's marker. Never sleeps as a synchronisation device."""
    deadline = time.monotonic() + MARKER_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except ValueError:
                pass                      # marker still being written; poll again
        if proc.poll() is not None:
            out, err = proc.communicate()
            pytest.fail(f"child exited early ({proc.returncode})\n"
                        f"stdout: {out}\nstderr: {err}")
        time.sleep(POLL_SECONDS)
    proc.kill()
    pytest.fail(f"child never wrote {path.name} within {MARKER_TIMEOUT_SECONDS}s")


def executed_task_ids(data_dir: Path, job_id: str) -> list[str]:
    """Every task id recorded as EXECUTED, read from disk, across all processes."""
    directory = data_dir / "jobs" / job_id / "evidence" / "cycles"
    ids: list[str] = []
    for path in sorted(directory.glob("cycle_*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        ids.extend(record.get("executed_task_ids", []))
    return ids


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def data_dir(tmp_path: Path, monkeypatch) -> Path:
    """One throwaway data root shared by the child and this process."""
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def child_script(tmp_path: Path) -> Path:
    script = tmp_path / "kill_fixture_run.py"
    script.write_text(CHILD_SOURCE, encoding="utf-8")
    return script


@pytest.fixture
def killed_run(data_dir: Path, child_script: Path, tmp_path: Path) -> dict:
    """Run the fixture until it parks mid-cycle, SIGKILL it, return the facts."""
    marker = tmp_path / "in_flight.json"
    job_file = tmp_path / "job_id.txt"

    proc = subprocess.Popen(
        [sys.executable, str(child_script), str(marker), str(job_file),
         str(KILL_ON_CYCLE), str(TOTAL_TASKS), "first"],
        cwd=str(REPO_ROOT), env=_child_env(data_dir),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    in_flight = _wait_for(marker, proc)

    os.kill(proc.pid, signal.SIGKILL)
    proc.wait(timeout=10)

    assert proc.returncode == -signal.SIGKILL, (
        f"child was not killed by SIGKILL (returncode {proc.returncode})")

    return {
        "job_id": job_file.read_text(encoding="utf-8").strip(),
        "in_flight": in_flight,
        "returncode": proc.returncode,
    }


# ---------------------------------------------------------------------------
# The acceptance centerpiece
# ---------------------------------------------------------------------------


class TestKillAndResume:
    def test_the_kill_leaves_checkpoints_for_the_committed_cycles(
            self, killed_run, data_dir):
        from packages.orchestration.checkpoints import load_latest_valid

        job_id = killed_run["job_id"]
        checkpoint = load_latest_valid(job_id)

        assert checkpoint is not None, "no checkpoint survived the kill"
        # Cycles 1..KILL_ON_CYCLE-1 committed; the killed one never did.
        assert checkpoint.cycle_index == KILL_ON_CYCLE - 1
        assert checkpoint.job_snapshot_path == f"jobs/{job_id}.json"

    def test_the_in_flight_task_was_never_recorded_as_executed(
            self, killed_run, data_dir):
        """Only the in-flight task is lost — and it is lost cleanly."""
        job_id = killed_run["job_id"]
        recorded = executed_task_ids(data_dir, job_id)

        assert len(recorded) == KILL_ON_CYCLE - 1
        assert killed_run["in_flight"]["task_id"] not in recorded

    def test_resume_completes_the_job_with_each_task_executed_exactly_once(
            self, killed_run, data_dir, child_script, tmp_path):
        """THE acceptance test: kill -9, resume, no duplicated work."""
        job_id = killed_run["job_id"]
        before = executed_task_ids(data_dir, job_id)

        proc = subprocess.run(
            [sys.executable, str(child_script), str(tmp_path / "unused.json"),
             str(tmp_path / "job_id.txt"), str(KILL_ON_CYCLE), str(TOTAL_TASKS),
             "resume"],
            cwd=str(REPO_ROOT), env=_child_env(data_dir),
            capture_output=True, text=True, timeout=60,
        )
        assert proc.returncode == 0, f"resume failed:\n{proc.stderr}"
        summary = json.loads(proc.stdout.strip().splitlines()[-1])
        assert summary["terminal_status"] == "all_green"

        after = executed_task_ids(data_dir, job_id)

        # Exactly-once, proven from evidence written by TWO processes.
        counts = Counter(after)
        duplicated = {tid: n for tid, n in counts.items() if n > 1}
        assert not duplicated, f"tasks executed more than once: {duplicated}"
        assert len(after) == TOTAL_TASKS
        assert set(before).issubset(set(after))     # pre-kill work was not redone

        # And the job really is finished.
        from uuid import UUID

        from packages.orchestration.storage import load_job

        job = load_job(UUID(job_id))
        assert all(t.status.value == "completed" for t in job.tasks)

    def test_the_f047_resume_path_accepts_the_killed_job(
            self, killed_run, data_dir, monkeypatch, capsys):
        """The real ``remedy job resume`` decision path, executor stubbed.

        Every F047 check runs for real here — checkpoint load, stop request,
        head comparison, plan gate. Only the hand-off is stubbed, because the
        production executor binds a live provider.
        """
        import apps.cli.commands.job as job_cmd

        job_id = killed_run["job_id"]
        handed_off: list[tuple] = []
        monkeypatch.setattr(job_cmd, "_cmd_job_run_cycles",
                            lambda jid, **kw: handed_off.append((jid, kw)))

        job_cmd._cmd_job_resume(job_id)

        assert len(handed_off) == 1
        out = capsys.readouterr().out
        assert f"resuming from checkpoint {KILL_ON_CYCLE - 1}" in out

    def test_the_dry_run_preview_of_a_killed_job_runs_nothing(
            self, killed_run, data_dir, monkeypatch, capsys):
        import apps.cli.commands.job as job_cmd

        handed_off: list[tuple] = []
        monkeypatch.setattr(job_cmd, "_cmd_job_run_cycles",
                            lambda jid, **kw: handed_off.append((jid, kw)))

        job_cmd._cmd_job_resume(killed_run["job_id"], dry_run=True)

        assert handed_off == []
        out = capsys.readouterr().out
        assert "resume preview (--dry-run)" in out
        assert f"would resume from checkpoint {KILL_ON_CYCLE - 1}" in out


# ---------------------------------------------------------------------------
# A torn checkpoint is what a kill during a write would leave behind
# ---------------------------------------------------------------------------


class TestTornCheckpoint:
    """The atomic write makes a torn file impossible to produce on demand.

    ``storage._atomic_write_job`` writes a temp file, fsyncs it and renames
    it, so a kill leaves either the old file or the new one — never a half
    one. Forcing a real mid-write kill is therefore not deterministic, and a
    test that tried would be a flake generator. The torn file is written
    explicitly instead: the property under test is that the LOADER survives
    one, which is the same property either way.
    """

    def test_resume_falls_back_to_the_previous_valid_checkpoint(
            self, killed_run, data_dir, monkeypatch, capsys):
        import apps.cli.commands.job as job_cmd
        from packages.orchestration.checkpoints import checkpoint_paths

        job_id = killed_run["job_id"]
        paths = checkpoint_paths(job_id)
        assert len(paths) >= 2, "need at least two checkpoints for a fallback"

        newest = paths[-1]
        newest.write_text('{"record": {"cycle_index": 9, "job_id": "x"',
                          encoding="utf-8")          # truncated mid-write

        handed_off: list[tuple] = []
        monkeypatch.setattr(job_cmd, "_cmd_job_run_cycles",
                            lambda jid, **kw: handed_off.append((jid, kw)))

        job_cmd._cmd_job_resume(job_id)

        assert len(handed_off) == 1
        out = capsys.readouterr().out
        assert f"resuming from checkpoint {KILL_ON_CYCLE - 2}" in out
        assert newest.exists(), "the torn checkpoint must be kept for forensics"

    def test_a_torn_newest_still_completes_the_job_exactly_once(
            self, killed_run, data_dir, child_script, tmp_path):
        from packages.orchestration.checkpoints import checkpoint_paths

        job_id = killed_run["job_id"]
        checkpoint_paths(job_id)[-1].write_text('{"record": {', encoding="utf-8")

        proc = subprocess.run(
            [sys.executable, str(child_script), str(tmp_path / "unused.json"),
             str(tmp_path / "job_id.txt"), str(KILL_ON_CYCLE), str(TOTAL_TASKS),
             "resume"],
            cwd=str(REPO_ROOT), env=_child_env(data_dir),
            capture_output=True, text=True, timeout=60,
        )
        assert proc.returncode == 0, f"resume failed:\n{proc.stderr}"

        after = executed_task_ids(data_dir, job_id)
        assert not [t for t, n in Counter(after).items() if n > 1]
        assert len(after) == TOTAL_TASKS
