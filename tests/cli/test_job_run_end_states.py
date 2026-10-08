"""R-1184 — `remedy job run` answers a run that ended stuck, failed or at its budget as a refusal.

A run that ends `blocked`, `failed` or stopped by its budget answers `"ok": false` with
`job_blocked`, `job_failed` or `job_stopped_by_budget`, every key of the job's report beside the
token, and exit 1; a run that completes, pauses at the operator's request or at `--tasks`, or
stops at the operator's request answers as before (DECISION F304 D8). `remedy job resume`, which
hands a job the engine has run to the same handler, answers the same way.

The first test drives a real run that blocks, through the command line alone, as the second gate
test's two-job path would if the client forgot its builder and reviewer. The table drives every
end state through the handler, with `run_job` standing in for the engine.
"""
from __future__ import annotations

import json

import pytest

from apps.cli.client_interface import OPERATION_REFUSAL_TOKENS
from apps.cli.grouped import main
from packages.core.models import RunState
from packages.orchestration.pingpong_job import JobPlan, save_job_plan
from tests.cli.test_machine_client_paths import UNATTENDED, _client, _remedy

ROLES = ("--builder-provider", "fake", "--reviewer-provider", "fake")


def test_a_run_that_blocks_answers_job_blocked_with_its_report(tmp_path):
    repo, order_file, env = _client(tmp_path)
    code, done = _remedy(["do", str(order_file), *UNATTENDED, "--force-mission"], repo, env)
    assert code == 0, done
    first, second = done["job_ids"]
    code, applied = _remedy(["job", "apply", first, "--approve", "--commit-auto"], repo, env)
    assert code == 0, applied

    # The second job never started, so it has no builder or reviewer of its own to run with.
    code, ran = _remedy(["job", "run", second], repo, env)

    assert (code, ran["ok"], ran["error"], ran["status"]) == (1, False, "job_blocked", "blocked")
    assert ran["error"] in OPERATION_REFUSAL_TOKENS["job.run"]
    assert ran["job_id"] == second and ran["tasks"]


@pytest.fixture
def planned_job(tmp_path, monkeypatch) -> JobPlan:
    """A planned job on a scratch data root; `run_job` ends it in the state a test sets."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    job = JobPlan(job_title="end states")
    save_job_plan(job)
    return job


def _end_in(monkeypatch, job: JobPlan, state: RunState, stop_source: str = "") -> None:
    def ended(job_id, **_kwargs):
        job.state, job.stop_source = state, stop_source
        return job

    monkeypatch.setattr("packages.orchestration.pingpong_job.run_job", ended)


@pytest.mark.parametrize(("state", "stop_source"), [
    (RunState.COMPLETED, ""), (RunState.PAUSED, ""), (RunState.STOPPED, "cli"),
], ids=["completed", "paused", "stopped-by-the-operator"])
def test_an_end_the_client_asked_for_answers_ok(planned_job, monkeypatch, capsys, state, stop_source):
    _end_in(monkeypatch, planned_job, state, stop_source)

    main(["job", "run", str(planned_job.job_id), *ROLES, "--json"])

    body = json.loads(capsys.readouterr().out)
    assert (body["ok"], body["status"]) == (True, state.value)


@pytest.mark.parametrize(("state", "stop_source", "token"), [
    (RunState.STOPPED, "budget", "job_stopped_by_budget"),
    (RunState.BLOCKED, "", "job_blocked"),
    (RunState.FAILED, "", "job_failed"),
], ids=["stopped-by-its-budget", "blocked", "failed"])
def test_a_stuck_failed_or_budget_stopped_end_is_refused_with_its_report(
        planned_job, monkeypatch, capsys, state, stop_source, token):
    _end_in(monkeypatch, planned_job, state, stop_source)

    with pytest.raises(SystemExit) as exc:
        main(["job", "run", str(planned_job.job_id), *ROLES, "--json"])

    assert exc.value.code == 1
    body = json.loads(capsys.readouterr().out)
    assert (body["ok"], body["error"], body["status"]) == (False, token, state.value)
    assert body["job_id"] == str(planned_job.job_id) and "tasks" in body


def test_the_text_answer_prints_the_report_and_exits_1(planned_job, monkeypatch, capsys):
    _end_in(monkeypatch, planned_job, RunState.BLOCKED)

    with pytest.raises(SystemExit) as exc:
        main(["job", "run", str(planned_job.job_id), *ROLES])

    assert exc.value.code == 1
    out, err = capsys.readouterr()
    assert str(planned_job.job_id) in out
    assert err.startswith(f"Error: Job {planned_job.job_id} ended blocked")
