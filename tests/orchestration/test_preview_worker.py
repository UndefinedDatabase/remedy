"""F041 T002 — the UI server's preview worker (DECISION F041 D4).

`step` is driven by hand with a scripted runner, a fixed clock and jobs held in memory, so
each test states exactly which verbs ran; one test runs the real thread and waits for it.
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from packages.orchestration import preview_runner
from packages.orchestration.preview_control import (
    VerbResult,
    load_preview,
    preview_path,
    request_preview,
)
from packages.orchestration.preview_worker import PREVIEW_TICK_SECONDS, PreviewWorker

JOB_A = "0123456789abcdef0123456789abcdef"
JOB_B = "fedcba9876543210fedcba9876543210"
T0 = datetime(2026, 9, 29, 12, 0, 0, tzinfo=timezone.utc)

SERVED = VerbResult(True, {"ok": True, "url": "http://127.0.0.1:5173/", "port": 5173})
PROBED = VerbResult(True, {"ok": True, "url": "http://127.0.0.1:5173/", "port": 5173})
STOPPED = VerbResult(True, {"ok": True})
BAD_PROBE = VerbResult(False, {"ok": False, "error": "runtime_not_ready",
                               "message": "health status 500"})


class Runner:
    def __init__(self, **answers: VerbResult) -> None:
        self.answers = answers
        self.calls: list[tuple[str, str]] = []

    def __call__(self, verb: str, root: Path) -> VerbResult:
        self.calls.append((verb, Path(root).name))
        return self.answers[verb]


class Clock:
    def __init__(self) -> None:
        self.now = T0

    def __call__(self) -> datetime:
        return self.now

    def advance(self, seconds: int) -> None:
        self.now = datetime.fromtimestamp(self.now.timestamp() + seconds, tz=timezone.utc)


@pytest.fixture
def data_root(tmp_path: Path) -> Path:
    return tmp_path / "data"


@pytest.fixture
def jobs(tmp_path: Path) -> dict:
    found = {}
    for job_id, name in ((JOB_A, "project-a"), (JOB_B, "project-b")):
        (tmp_path / name).mkdir()
        found[job_id] = SimpleNamespace(job_id=job_id, repo_path=str(tmp_path / name))
    return found


def _worker(jobs, data_root, runner, clock, ttl=900):
    return PreviewWorker(ttl_seconds=ttl, runner=runner, load_job=jobs.get, clock=clock,
                         data_root=data_root)


def test_the_tick_is_fifteen_seconds():
    assert PREVIEW_TICK_SECONDS == 15


def test_a_submitted_start_is_run_on_the_next_step_and_then_looked_after(jobs, data_root):
    runner, clock = Runner(serve=SERVED, probe=PROBED), Clock()
    worker = _worker(jobs, data_root, runner, clock)
    request_preview(JOB_A, "start", now=T0, data_root=data_root)
    worker.submit(JOB_A)
    worker.submit(JOB_A)
    assert runner.calls == []
    worker.step()
    assert runner.calls == [("serve", "project-a"), ("probe", "project-a")]
    assert load_preview(JOB_A, data_root)["state"] == "live"
    assert worker.live_jobs == frozenset({JOB_A})
    runner.calls.clear()
    worker.step()
    assert runner.calls == [("probe", "project-a")]


def test_a_preview_that_stops_answering_leaves_the_worker(jobs, data_root):
    runner, clock = Runner(serve=SERVED, probe=PROBED, stop=STOPPED), Clock()
    worker = _worker(jobs, data_root, runner, clock)
    request_preview(JOB_A, "start", now=T0, data_root=data_root)
    worker.submit(JOB_A)
    worker.step()
    runner.answers["probe"] = BAD_PROBE
    runner.calls.clear()
    worker.step()
    assert runner.calls == [("probe", "project-a"), ("stop", "project-a")]
    assert load_preview(JOB_A, data_root)["state"] == "failed"
    assert worker.live_jobs == frozenset()


def test_an_unviewed_preview_is_stopped_at_the_idle_limit(jobs, data_root):
    runner, clock = Runner(serve=SERVED, probe=PROBED, stop=STOPPED), Clock()
    worker = _worker(jobs, data_root, runner, clock, ttl=900)
    request_preview(JOB_A, "start", now=T0, data_root=data_root)
    worker.submit(JOB_A)
    worker.step()
    clock.advance(899)
    worker.step()
    assert load_preview(JOB_A, data_root)["state"] == "live"
    clock.advance(1)
    runner.calls.clear()
    worker.step()
    assert runner.calls == [("stop", "project-a")]
    record = load_preview(JOB_A, data_root)
    assert (record["state"], record["reason"]) == (
        "stopped", "stopped after 900 seconds without a viewer")
    assert worker.live_jobs == frozenset()


def test_a_submitted_stop_stops(jobs, data_root):
    runner, clock = Runner(serve=SERVED, probe=PROBED, stop=STOPPED), Clock()
    worker = _worker(jobs, data_root, runner, clock)
    request_preview(JOB_A, "start", now=T0, data_root=data_root)
    worker.submit(JOB_A)
    worker.step()
    request_preview(JOB_A, "stop", now=T0, data_root=data_root)
    worker.submit(JOB_A)
    runner.calls.clear()
    worker.step()
    assert runner.calls == [("stop", "project-a")]
    assert load_preview(JOB_A, data_root)["state"] == "stopped"
    assert worker.live_jobs == frozenset()


def test_a_submitted_job_that_cannot_be_loaded_runs_nothing(jobs, data_root):
    runner = Runner()
    worker = _worker(jobs, data_root, runner, Clock())
    worker.submit("00000000000000000000000000000000")
    worker.step()
    assert runner.calls == []


def test_closing_stops_every_preview_the_worker_keeps_live(jobs, data_root):
    runner, clock = Runner(serve=SERVED, probe=PROBED, stop=STOPPED), Clock()
    worker = _worker(jobs, data_root, runner, clock)
    for job_id in (JOB_B, JOB_A):
        request_preview(job_id, "start", now=T0, data_root=data_root)
        worker.submit(job_id)
    worker.step()
    runner.calls.clear()
    worker.close()
    assert runner.calls == [("stop", "project-a"), ("stop", "project-b")]
    assert [load_preview(j, data_root)["state"] for j in (JOB_A, JOB_B)] == ["stopped", "stopped"]
    assert worker.live_jobs == frozenset()


def test_a_live_record_from_an_earlier_server_is_adopted(jobs, data_root):
    runner, clock = Runner(serve=SERVED, probe=PROBED), Clock()
    request_preview(JOB_A, "start", now=T0, data_root=data_root)
    first = _worker(jobs, data_root, runner, clock)
    first.submit(JOB_A)
    first.step()
    path = preview_path(JOB_B, data_root)
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"schema": "remedy.preview.v1", "state": "failed"}))
    second = _worker(jobs, data_root, Runner(probe=PROBED), clock)
    second.adopt_live()
    assert second.live_jobs == frozenset({JOB_A})


def test_adopting_with_no_jobs_directory_finds_nothing(jobs, data_root):
    worker = _worker(jobs, data_root, Runner(), Clock())
    worker.adopt_live()
    assert worker.live_jobs == frozenset()


def test_the_thread_acts_on_a_submission_without_waiting_for_the_tick(jobs, data_root):
    runner = Runner(serve=SERVED, probe=PROBED, stop=STOPPED)
    worker = _worker(jobs, data_root, runner, Clock())
    worker.start(tick_seconds=60)
    try:
        request_preview(JOB_A, "start", now=T0, data_root=data_root)
        worker.submit(JOB_A)
        deadline = time.monotonic() + 5
        while load_preview(JOB_A, data_root)["state"] != "live" and time.monotonic() < deadline:
            time.sleep(0.02)
        assert load_preview(JOB_A, data_root)["state"] == "live"
    finally:
        worker.close()
    assert load_preview(JOB_A, data_root)["state"] == "stopped"


def test_with_no_runner_given_the_worker_uses_the_harness_runner(jobs, data_root, monkeypatch):
    runner = Runner(serve=SERVED, probe=PROBED)
    monkeypatch.setattr(preview_runner, "run_runtime_verb", runner)
    worker = PreviewWorker(ttl_seconds=900, load_job=jobs.get, clock=Clock(),
                           data_root=data_root)
    request_preview(JOB_A, "start", now=T0, data_root=data_root)
    worker.submit(JOB_A)
    worker.step()
    assert runner.calls == [("serve", "project-a"), ("probe", "project-a")]
