"""F041 T002 — the preview record and its state machine (DECISION F041 D3).

The runtime verbs are a scripted stand-in here: each test names the envelope every verb answers
and reads back both the calls made and the record written. The link is the property under
test above all: it appears only after a probe passed, and never in any other state.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from packages.orchestration.preview_control import (
    PREVIEW_STATES,
    VerbResult,
    idle_stop_due,
    load_preview,
    mark_viewed,
    preview_path,
    preview_view,
    request_preview,
    revalidate_live,
    run_pending,
    stop_if_idle,
)

JOB_ID = "0123456789abcdef0123456789abcdef"
T0 = datetime(2026, 9, 29, 12, 0, 0, tzinfo=timezone.utc)
T1 = datetime(2026, 9, 29, 12, 0, 5, tzinfo=timezone.utc)

SERVED = VerbResult(True, {"ok": True, "url": "http://127.0.0.1:5173/", "port": 5173})
PROBED = VerbResult(True, {"ok": True, "url": "http://127.0.0.1:5173/", "port": 5173,
                           "status_code": 200})
STOPPED = VerbResult(True, {"ok": True, "stopped": True})
NO_RUNTIME = VerbResult(False, {"ok": False, "error": "runtime_config_error",
                                "message": "no runtime detected"})
DEAD_START = VerbResult(False, {"ok": False, "error": "runtime_start_failed",
                                "message": "the application exited with code 1"})
BAD_PROBE = VerbResult(False, {"ok": False, "error": "runtime_not_ready",
                               "message": "health status 500"})
STOP_FAILED = VerbResult(False, {"ok": False, "error": "runtime_stop_failed",
                                 "message": "processes survived"})


class Runner:
    def __init__(self, **answers: VerbResult) -> None:
        self.answers = answers
        self.calls: list[tuple[str, str]] = []

    def __call__(self, verb: str, root: Path) -> VerbResult:
        self.calls.append((verb, str(root)))
        return self.answers[verb]


@pytest.fixture
def data_root(tmp_path: Path) -> Path:
    return tmp_path / "data"


@pytest.fixture
def job(tmp_path: Path) -> SimpleNamespace:
    project = tmp_path / "project"
    project.mkdir()
    return SimpleNamespace(job_id=JOB_ID, repo_path=str(project))


def test_a_job_with_no_record_reads_as_stopped_with_no_link(data_root):
    assert load_preview(JOB_ID, data_root) == {
        "schema": "remedy.preview.v1", "job_id": JOB_ID, "state": "stopped", "requested": "",
        "url": "", "port": 0, "reason": "", "updated_at": "", "viewed_at": "",
    }
    assert preview_view(JOB_ID, data_root) == {
        "state": "stopped", "url": "", "port": 0, "reason": "", "updated_at": ""}


def test_the_states_are_exactly_these():
    assert PREVIEW_STATES == ("stopped", "starting", "probing", "live", "failed",
                              "not_applicable")


def test_a_start_request_is_recorded_as_starting_and_runs_nothing(data_root):
    record = request_preview(JOB_ID, "start", now=T0, data_root=data_root)
    assert record["state"] == "starting"
    assert record["requested"] == "start"
    assert record["updated_at"] == T0.isoformat()
    assert json.loads(preview_path(JOB_ID, data_root).read_text()) == record
    assert preview_view(JOB_ID, data_root)["url"] == ""


def test_an_unknown_action_is_refused(data_root):
    with pytest.raises(ValueError):
        request_preview(JOB_ID, "restart", now=T0, data_root=data_root)
    assert not preview_path(JOB_ID, data_root).exists()


def test_a_start_that_serves_and_probes_is_live_with_its_link(data_root, job):
    runner = Runner(serve=SERVED, probe=PROBED)
    request_preview(JOB_ID, "start", now=T0, data_root=data_root)
    record = run_pending(job, runner, now=T1, data_root=data_root)
    assert runner.calls == [("serve", job.repo_path), ("probe", job.repo_path)]
    assert record == {
        "schema": "remedy.preview.v1", "job_id": JOB_ID, "state": "live", "requested": "",
        "url": "http://127.0.0.1:5173/", "port": 5173, "reason": "",
        "updated_at": T1.isoformat(), "viewed_at": T1.isoformat(),
    }
    assert preview_view(JOB_ID, data_root) == {
        "state": "live", "url": "http://127.0.0.1:5173/", "port": 5173, "reason": "",
        "updated_at": T1.isoformat()}


def test_the_link_is_the_probes_not_the_serves(data_root, job):
    moved = VerbResult(True, {"ok": True, "url": "http://127.0.0.1:5174/", "port": 5174})
    request_preview(JOB_ID, "start", now=T0, data_root=data_root)
    run_pending(job, Runner(serve=SERVED, probe=moved), now=T1, data_root=data_root)
    assert preview_view(JOB_ID, data_root)["url"] == "http://127.0.0.1:5174/"
    assert preview_view(JOB_ID, data_root)["port"] == 5174


def test_a_project_with_no_runtime_is_not_applicable(data_root, job):
    runner = Runner(serve=NO_RUNTIME)
    request_preview(JOB_ID, "start", now=T0, data_root=data_root)
    record = run_pending(job, runner, now=T1, data_root=data_root)
    assert runner.calls == [("serve", job.repo_path)]
    assert (record["state"], record["reason"], record["url"]) == (
        "not_applicable", "no runtime detected", "")


def test_a_start_that_dies_is_failed_with_the_harness_message(data_root, job):
    runner = Runner(serve=DEAD_START)
    request_preview(JOB_ID, "start", now=T0, data_root=data_root)
    record = run_pending(job, runner, now=T1, data_root=data_root)
    assert runner.calls == [("serve", job.repo_path)]
    assert (record["state"], record["reason"], record["url"], record["port"]) == (
        "failed", "the application exited with code 1", "", 0)


def test_a_failed_probe_shows_no_link_and_stops_the_runtime_again(data_root, job):
    runner = Runner(serve=SERVED, probe=BAD_PROBE, stop=STOPPED)
    request_preview(JOB_ID, "start", now=T0, data_root=data_root)
    record = run_pending(job, runner, now=T1, data_root=data_root)
    assert runner.calls == [("serve", job.repo_path), ("probe", job.repo_path),
                            ("stop", job.repo_path)]
    assert (record["state"], record["reason"], record["url"], record["port"]) == (
        "failed", "started but health check failed: health status 500", "", 0)
    assert preview_view(JOB_ID, data_root)["url"] == ""


def test_the_record_is_probing_while_the_probe_runs(data_root, job):
    seen = []

    def runner(verb, root):
        if verb == "probe":
            seen.append(load_preview(JOB_ID, data_root)["state"])
            return PROBED
        return SERVED

    request_preview(JOB_ID, "start", now=T0, data_root=data_root)
    run_pending(job, runner, now=T1, data_root=data_root)
    assert seen == ["probing"]


def test_a_start_while_live_changes_nothing(data_root, job):
    request_preview(JOB_ID, "start", now=T0, data_root=data_root)
    live = run_pending(job, Runner(serve=SERVED, probe=PROBED), now=T1, data_root=data_root)
    later = datetime(2026, 9, 29, 13, 0, 0, tzinfo=timezone.utc)
    assert request_preview(JOB_ID, "start", now=later, data_root=data_root) == live
    runner = Runner()
    assert run_pending(job, runner, now=later, data_root=data_root) == live
    assert runner.calls == []


def test_a_stop_stops_and_clears_the_link(data_root, job):
    request_preview(JOB_ID, "start", now=T0, data_root=data_root)
    run_pending(job, Runner(serve=SERVED, probe=PROBED), now=T1, data_root=data_root)
    request_preview(JOB_ID, "stop", now=T1, data_root=data_root)
    runner = Runner(stop=STOPPED)
    record = run_pending(job, runner, now=T1, data_root=data_root)
    assert runner.calls == [("stop", job.repo_path)]
    assert (record["state"], record["requested"], record["url"], record["port"],
            record["reason"]) == ("stopped", "", "", 0, "stopped on request")


def test_a_stop_that_fails_says_so(data_root, job):
    request_preview(JOB_ID, "stop", now=T0, data_root=data_root)
    record = run_pending(job, Runner(stop=STOP_FAILED), now=T1, data_root=data_root)
    assert (record["state"], record["reason"]) == ("failed", "could not stop: processes survived")


@pytest.mark.parametrize("repo_path", ["", "missing-folder"])
def test_a_job_without_a_project_folder_runs_nothing(data_root, tmp_path, repo_path):
    job = SimpleNamespace(job_id=JOB_ID,
                          repo_path=str(tmp_path / repo_path) if repo_path else "")
    request_preview(JOB_ID, "start", now=T0, data_root=data_root)
    runner = Runner()
    record = run_pending(job, runner, now=T1, data_root=data_root)
    assert runner.calls == []
    assert (record["state"], record["reason"]) == ("failed", "the job has no project folder to run")


def test_an_unreadable_or_foreign_record_reads_as_stopped(data_root):
    path = preview_path(JOB_ID, data_root)
    path.parent.mkdir(parents=True)
    path.write_text("not json")
    assert load_preview(JOB_ID, data_root)["state"] == "stopped"
    path.write_text(json.dumps({"schema": "other", "state": "live", "url": "http://x/"}))
    assert preview_view(JOB_ID, data_root)["url"] == ""
    path.write_text(json.dumps({"schema": "remedy.preview.v1", "state": "exploded"}))
    assert load_preview(JOB_ID, data_root)["state"] == "stopped"


# -- round 4 (DECISION F041 D4): the view's gate, the viewed clock, the idle stop and the
# -- revalidation of a live preview.

def _live(job, data_root):
    request_preview(JOB_ID, "start", now=T0, data_root=data_root)
    return run_pending(job, Runner(serve=SERVED, probe=PROBED), now=T0, data_root=data_root)


def _after(seconds):
    return datetime.fromtimestamp(T0.timestamp() + seconds, tz=timezone.utc)


def test_the_view_shows_a_link_only_while_live_whatever_the_record_holds(data_root):
    path = preview_path(JOB_ID, data_root)
    path.parent.mkdir(parents=True)
    for state in ("stopped", "starting", "probing", "failed", "not_applicable"):
        path.write_text(json.dumps({
            "schema": "remedy.preview.v1", "job_id": JOB_ID, "state": state, "requested": "",
            "url": "http://127.0.0.1:9/", "port": 9, "reason": "r", "updated_at": "",
            "viewed_at": ""}))
        view = preview_view(JOB_ID, data_root)
        assert (view["state"], view["url"], view["port"]) == (state, "", 0)


def test_viewing_a_live_preview_moves_its_clock_and_nothing_else(data_root, job):
    live = _live(job, data_root)
    record = mark_viewed(JOB_ID, now=T1, data_root=data_root)
    assert record == {**live, "viewed_at": T1.isoformat()}
    assert load_preview(JOB_ID, data_root) == record


def test_viewing_a_preview_that_is_not_live_writes_nothing(data_root):
    assert mark_viewed(JOB_ID, now=T1, data_root=data_root)["state"] == "stopped"
    assert not preview_path(JOB_ID, data_root).exists()


@pytest.mark.parametrize(("seconds", "ttl", "due"), [
    (899, 900, False), (900, 900, True), (5000, 0, False), (5000, -1, False),
])
def test_the_idle_limit_counts_from_the_last_view(data_root, job, seconds, ttl, due):
    record = _live(job, data_root)
    assert idle_stop_due(record, now=_after(seconds), ttl_seconds=ttl) is due


def test_a_record_that_is_not_live_is_never_idle_due(data_root):
    assert idle_stop_due(load_preview(JOB_ID, data_root), now=T1, ttl_seconds=1) is False


def test_an_idle_preview_is_stopped_and_says_why(data_root, job):
    _live(job, data_root)
    runner = Runner(stop=STOPPED)
    record = stop_if_idle(job, runner, now=_after(900), ttl_seconds=900, data_root=data_root)
    assert runner.calls == [("stop", job.repo_path)]
    assert (record["state"], record["url"], record["port"], record["reason"]) == (
        "stopped", "", 0, "stopped after 900 seconds without a viewer")


def test_a_viewed_preview_is_not_stopped(data_root, job):
    _live(job, data_root)
    mark_viewed(JOB_ID, now=_after(800), data_root=data_root)
    runner = Runner()
    record = stop_if_idle(job, runner, now=_after(1000), ttl_seconds=900, data_root=data_root)
    assert runner.calls == []
    assert record["state"] == "live"


def test_a_live_preview_that_still_answers_keeps_its_link(data_root, job):
    live = _live(job, data_root)
    runner = Runner(probe=PROBED)
    assert revalidate_live(job, runner, now=T1, data_root=data_root) == live
    assert runner.calls == [("probe", job.repo_path)]


def test_a_live_preview_that_stops_answering_loses_its_link_and_is_stopped(data_root, job):
    _live(job, data_root)
    runner = Runner(probe=BAD_PROBE, stop=STOPPED)
    record = revalidate_live(job, runner, now=T1, data_root=data_root)
    assert runner.calls == [("probe", job.repo_path), ("stop", job.repo_path)]
    assert (record["state"], record["url"], record["reason"]) == (
        "failed", "", "the app stopped answering: health status 500")
    assert preview_view(JOB_ID, data_root)["url"] == ""


def test_revalidating_a_preview_that_is_not_live_runs_nothing(data_root, job):
    runner = Runner()
    assert revalidate_live(job, runner, now=T1, data_root=data_root)["state"] == "stopped"
    assert runner.calls == []
