"""exec-1017c (R-1339) — a cancelled job ends for good, through the real `run_job` loop.

The cancel is requested the way `remedy job abandon` requests it, sometimes from inside a provider
call, so each test asks what the runner did with work in flight: it finished the call, started
nothing new and ended the job `cancelled`, never `stopped` (which `remedy job run` would resume).
Fake providers only; every data root lives in pytest's temporary directory.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration.decision_queue import budget_decision_id, list_decisions
from packages.orchestration.job_cancel import (
    JOB_CANCEL_METADATA_KEY,
    JobCancelRefused,
    cancel_job,
    job_cancel_request,
    request_job_cancel_marker,
)
from packages.orchestration.job_stop_now import request_job_stop
from packages.orchestration.pingpong_job import (
    JOB_COMPLETED,
    JOB_STOPPED,
    TASK_PENDING,
    load_job_plan,
    parse_job_file,
    run_job,
    save_job_plan,
)
from packages.orchestration.pingpong_provider import FakeProvider
from packages.orchestration.safe_points import request_stop, stop_requested, stop_status

_TWO_TASK_JOB = """\
# Job: Cancel Test

## Task 1
Add a helper module.

Acceptance:
- module exists

## Task 2
Add a second module.

Acceptance:
- module exists
"""


@pytest.fixture
def data_root(tmp_path: Path, monkeypatch) -> Path:
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    path = tmp_path / "repo"
    path.mkdir()
    (path / "README.md").write_text("# demo\n")
    return path


class CancellingProvider(FakeProvider):
    """A passing fake that cancels its job from inside its first build call, as a person would."""

    def __init__(self, job_id: str = "", *, cancel_on_build: int = 0) -> None:
        super().__init__(pass_on_round=1, fail_on_round=99)
        self.job_id, self.cancel_on_build, self.build_calls, self.answers = job_id, cancel_on_build, 0, []

    def build(self, prompt, **kwargs):
        self.build_calls += 1
        if self.cancel_on_build and self.build_calls == self.cancel_on_build:
            self.answers.append(cancel_job(load_job_plan(self.job_id), reason="not wanted", source="test"))
        return super().build(prompt, **kwargs)


def test_a_running_job_ends_cancelled_at_its_next_safe_point_and_never_runs_again(data_root, repo):
    job = parse_job_file(_TWO_TASK_JOB, str(repo))
    builder = CancellingProvider(job.job_id, cancel_on_build=1)

    ended = run_job(job.job_id, builder_provider=builder, reviewer_provider=CancellingProvider(),
                    repair_rounds=0)

    # The request found the job running, so it was pending; the call in flight finished.
    assert builder.answers[0]["cancel_pending"] is True and builder.answers[0]["job_status"] == "running"
    assert builder.build_calls == 1
    assert ended.state == RunState.CANCELLED
    assert ended.tasks[1].status == TASK_PENDING            # the second task never started
    reloaded = load_job_plan(job.job_id)
    assert reloaded.state == RunState.CANCELLED
    assert reloaded.metadata[JOB_CANCEL_METADATA_KEY]["reason"] == "not wanted"
    assert reloaded.finished_at
    # The stop that carried it was consumed as one episode, never left pending.
    assert stop_requested(job.job_id) is None and stop_status(job.job_id).consumed_count == 1

    again = CancellingProvider()
    rerun = run_job(job.job_id, builder_provider=again, reviewer_provider=again, repair_rounds=0)
    assert again.build_calls == 0
    assert rerun.error.startswith("job_cancelled:")
    assert load_job_plan(job.job_id).state == RunState.CANCELLED


def test_a_job_that_never_started_is_cancelled_at_once_and_twice_is_the_same_cancel(data_root, repo):
    job = parse_job_file(_TWO_TASK_JOB, str(repo))

    first = cancel_job(load_job_plan(job.job_id), reason="abandoned", source="cli")
    second = cancel_job(load_job_plan(job.job_id), reason="again", source="api")

    assert (first["job_status"], first["cancel_pending"], first["already_cancelled"]) == (
        "cancelled", False, False)
    assert second["already_cancelled"] is True
    assert second["cancel"]["reason"] == "abandoned"            # the first request stands
    assert load_job_plan(job.job_id).state == RunState.CANCELLED
    provider = CancellingProvider()
    run_job(job.job_id, builder_provider=provider, reviewer_provider=provider, repair_rounds=0)
    assert provider.build_calls == 0


def test_a_stopped_job_that_ran_is_cancelled_and_its_resume_runs_nothing(data_root, repo):
    job = parse_job_file(_TWO_TASK_JOB, str(repo))
    request_stop(job.job_id, "pause", "cli")
    stopped = run_job(job.job_id, builder_provider=CancellingProvider(),
                      reviewer_provider=CancellingProvider(), repair_rounds=0)
    assert stopped.state == JOB_STOPPED

    answer = cancel_job(load_job_plan(job.job_id), reason="not wanted", source="cli", runner_alive=True)

    assert (answer["job_status"], answer["cancel_pending"]) == ("cancelled", False)
    provider = CancellingProvider()
    run_job(job.job_id, builder_provider=provider, reviewer_provider=provider, repair_rounds=0)
    assert provider.build_calls == 0


def test_a_request_no_runner_reached_settles_the_job_when_a_run_begins(data_root, repo):
    """A crash, or a supervisor restart, between the request and its settling resurrects nothing."""
    job = parse_job_file(_TWO_TASK_JOB, str(repo))
    record = load_job_plan(job.job_id)
    record.state = RunState.RUNNING          # as a runner that died mid-run left it
    save_job_plan(record)
    request_job_cancel_marker(job.job_id, reason="abandoned", source="api")
    request_stop(job.job_id, "abandoned", "api")

    provider = CancellingProvider()
    resumed = run_job(job.job_id, builder_provider=provider, reviewer_provider=provider, repair_rounds=0)

    assert provider.build_calls == 0
    assert resumed.state == RunState.CANCELLED and load_job_plan(job.job_id).state == RunState.CANCELLED
    assert stop_requested(job.job_id) is None          # the stale stop request went with it


def test_a_running_job_whose_runner_is_gone_is_cancelled_at_once(data_root, repo):
    job = parse_job_file(_TWO_TASK_JOB, str(repo))
    record = load_job_plan(job.job_id)
    record.state = RunState.RUNNING
    save_job_plan(record)

    answer = cancel_job(record, reason="orphan", source="cli", runner_alive=False)

    assert (answer["job_status"], answer["cancel_pending"]) == ("cancelled", False)
    assert stop_requested(job.job_id) is None


@pytest.mark.parametrize("state", [JOB_COMPLETED, RunState.FAILED])
def test_a_finished_job_is_refused_and_keeps_its_state(data_root, repo, state):
    job = parse_job_file(_TWO_TASK_JOB, str(repo))
    record = load_job_plan(job.job_id)
    record.state = state
    save_job_plan(record)

    with pytest.raises(JobCancelRefused) as refused:
        cancel_job(record, reason="x", source="cli")

    assert refused.value.token == "job_not_cancellable"
    assert load_job_plan(job.job_id).state == state
    assert job_cancel_request(job.job_id) is None          # nothing was written


def test_a_stop_of_a_job_that_never_started_under_a_cancel_request_ends_it_cancelled(data_root, repo):
    job = parse_job_file(_TWO_TASK_JOB, str(repo))
    request_job_cancel_marker(job.job_id, reason="abandoned", source="api")

    _signal, ended = request_job_stop(job.job_id, reason="abandoned", source="api")

    assert ended is True and load_job_plan(job.job_id).state == RunState.CANCELLED


def test_a_cancelled_job_asks_no_decision():
    """A budget stop asks its token_budget decision; once the job is cancelled nothing is asked."""
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry

    now = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    job = JobPlan(job_title="budget-stopped", tasks=[TaskEntry(title="d")])
    job.stop_source, job.stop_reason, job.stop_request_id = "budget", "budget_exhausted:deadline", "req1"
    job.stopped_at, job.budgets = now.isoformat(), {"deadline": "2025-12-01T00:00:00+00:00"}
    event = {"event": "job_stopped", "timestamp": now.isoformat(),
             "metadata": {"source": "budget", "request_id": "req1", "reason": job.stop_reason,
                          "exhausted_limit": "deadline"}}
    assert budget_decision_id("req1") in [d.id for d in list_decisions(job, [event])]

    job.state = RunState.CANCELLED

    assert list_decisions(job, [event]) == []


def test_a_cancel_during_the_jobs_final_gate_ends_it_cancelled_and_nothing_is_applied(tmp_path, monkeypatch):
    """exec-1018b (R-1357): the job's DoD gate runs after its last safe point and may run the project's
    tests for minutes. A cancel that arrives then was answered `cancel_pending`, yet the job ended
    `completed` and the walk's `--apply` applied it. It ends `cancelled` now, and nothing lands."""
    import contextlib
    import io
    import json
    import os

    from apps.cli.grouped import main
    from packages.orchestration import dod_gate
    from tests.orchestration.scale_harness import FakePlannerService, commit_repository

    readme = "# P\n\nA projcet.\n"
    work = commit_repository(tmp_path / "work", {"README.md": readme,
                                                 "package.json": '{"scripts": {"test": "node --test"}}\n'})
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.chdir(work)
    FakePlannerService(target="README.md").install(monkeypatch)
    answers: list[dict] = []
    gate = dod_gate.run_job_gate

    def cancelled_while_gating(job_id, root, **kwargs):
        answers.append(cancel_job(load_job_plan(job_id), reason="no longer wanted", source="test"))
        return gate(job_id, root, **kwargs)
    monkeypatch.setattr(dod_gate, "run_job_gate", cancelled_while_gating)
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.suppress(SystemExit):
        main(["do", "Fix the typo in README.md. Run the tests.", "--repo", ".", "--builder-provider", "fake",
              "--reviewer-provider", "fake", "--json", "--no-ui", "--run-unattended", "--apply"])
    [job_id] = json.loads(out.getvalue())["job_ids"]

    assert [a["cancel_pending"] for a in answers] == [True]
    assert load_job_plan(job_id).state == RunState.CANCELLED
    assert (work / "README.md").read_text() == readme
