"""amend1015 Phase 1.1 — the run story, `build_client_story`, read from real fake-provider runs.

Every story here comes from a job the real runner ran with fake providers in a temporary data
root, or from such a job's record moved to one state the runner writes; each is checked against
the closed words of `client_story_words` by `story_problems`.
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from packages.core.models import RunState
from packages.orchestration.client_story import build_client_story
from packages.orchestration.client_story_words import STORY_STEP_IDS, story_problems

_JOB = "# Job: story\n\n## Task 1\nDo a thing.\n\nAcceptance:\n- done\n"
_NOW = datetime(2026, 10, 15, 12, 0, tzinfo=timezone.utc)


@pytest.fixture
def data_root(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def repo(tmp_path) -> Path:
    path = tmp_path / "repo"
    path.mkdir()
    subprocess.run("git init -q && git config user.email t@t && git config user.name t "
                   "&& echo '# demo' > README.md && git add -A && git commit -qm init",
                   shell=True, cwd=path, check=True)
    return path


def _fake(**kw):
    from packages.orchestration.pingpong_provider import FakeProvider

    return FakeProvider(**kw)


def _run(repo: Path, *, builder_error: str = "") -> str:
    from packages.orchestration.pingpong_job import parse_job_file, run_job

    job = parse_job_file(_JOB, str(repo))
    builder = _fake(builder_error=builder_error) if builder_error else _fake()
    run_job(job.job_id, builder_provider=builder, reviewer_provider=_fake(), repair_rounds=2)
    return job.job_id


def _story(job_id: str, data_root: Path) -> dict:
    from packages.orchestration.pingpong_job import load_job_plan_safe
    from packages.orchestration.timeline import load_run_events

    plan, _degraded = load_job_plan_safe(job_id)
    story = build_client_story(plan, events=load_run_events(data_root, job_id), now=_NOW)
    assert story_problems(story) == []
    assert [step["id"] for step in story["steps"]] == list(STORY_STEP_IDS)
    assert story["note_open"] is False
    assert "$" not in json.dumps(story)
    return story


def _step(story: dict, step_id: str) -> dict:
    return next(step for step in story["steps"] if step["id"] == step_id)


def _save(job_id: str, **fields) -> None:
    from packages.orchestration.pingpong_job import _persist_job, load_job_plan_safe

    plan, _degraded = load_job_plan_safe(job_id)
    for name, value in fields.items():
        setattr(plan, name, value)
    _persist_job(plan)


def test_a_finished_run_reads_done_and_offers_its_apply(data_root, repo):
    job_id = _run(repo)
    story = _story(job_id, data_root)

    assert story["order"] == "story"
    assert story["state"] == "done"
    assert story["state_detail"] == {"changed_files": 1}
    assert story["next"] == {"action": "apply",
                             "route": {"method": "POST", "path": f"/api/v1/jobs/{job_id}/apply"}}
    building = _step(story, "building")
    assert building["status"] == "done"
    assert [task["status"] for task in building["tasks"]] == ["done"]
    assert building["tasks"][0]["rounds"] >= 1
    assert building["phrase"]["key"] == "changed_file_in_rounds"
    assert _step(story, "reading")["phrase"] == {"key": "found_files",
                                                 "args": {"n": 1, "first": "README.md"}}
    # exec-1017 D2: no test was asked for and none ran, which is not "the project names no test command".
    assert _step(story, "checking")["phrase"]["key"] == "tests_not_requested"
    assert story["verification"] == {"status": "not_required", "required": False}
    assert _step(story, "finished")["phrase"] == {"key": "waiting_for_apply", "args": {"n": 1}}
    assert [change["path"] for change in story["changes"]] == building["tasks"][0]["files"]
    numbers = story["numbers"]
    assert numbers["rounds"] >= 1
    assert numbers["calls"] is None  # a job of no registered project has no call ledger to read
    assert numbers["tokens_in"] is None and numbers["tokens_out"] is None  # amend1015f D4
    assert building["tokens"] is None
    assert story["started_at"] and story["ended_at"] and story["updated_at"]


def test_an_applied_result_reads_done_applied_with_nothing_next(data_root, repo):
    from packages.orchestration.job_apply import apply_job

    job_id = _run(repo)
    assert apply_job(job_id, str(repo), approve=True).status == "applied"
    story = _story(job_id, data_root)

    assert story["state"] == "done_applied"
    assert story["next"] == {"action": "none", "route": None}
    assert _step(story, "finished")["phrase"]["key"] == "applied"


def test_a_declined_result_reads_stopped_declined(data_root, repo):
    from packages.orchestration.job_apply import decline_job_result
    from packages.orchestration.pingpong_job import _persist_job, load_job_plan_safe

    job_id = _run(repo)
    plan, _degraded = load_job_plan_safe(job_id)
    decline_job_result(plan, reason="not wanted", source="test", now=_NOW)
    _persist_job(plan)
    story = _story(job_id, data_root)

    assert story["state"] == "stopped"
    assert story["state_detail"] == {"reason": {"key": "declined", "args": {}}}
    assert story["next"]["action"] == "none"
    assert _step(story, "finished") == {"id": "finished", "status": "skipped",
                                        "phrase": {"key": "declined", "args": {}}, "tokens": None}
    assert "not wanted" not in json.dumps(story)


def test_instructions_too_large_for_one_call_read_as_their_own_reason(data_root, repo):
    """exec-1018 (R-1347): a builder call refused because the repository's instructions cannot be
    carried whole is a context error, never a missing provider, and its story says why."""
    job_id = _run(repo, builder_error="provider_error: project_rules_too_large: AGENTS.md (40,000 "
                                      "characters) is more than one call carries whole; not started")
    story = _story(job_id, data_root)

    assert story["state"] == "failed"
    assert story["state_detail"] == {"reason": {"key": "project_rules_too_large", "args": {}}}
    assert "40,000" not in json.dumps(story)            # a closed word, never Remedy's sentence

def test_a_provider_failure_reads_failed_and_offers_no_retry(data_root, repo):
    """amend1015c D3 (R-1331): a run of a job whose task ended blocked re-attempts nothing, so the
    story offers no step that cannot succeed."""
    job_id = _run(repo, builder_error="provider_unavailable: down")
    story = _story(job_id, data_root)

    assert story["state"] == "failed"
    assert story["state_detail"] == {"reason": {"key": "provider_unavailable",
                                                "args": {"provider": "fake"}}}
    assert story["next"] == {"action": "none", "route": None}
    building = _step(story, "building")
    assert building["status"] == "failed"
    assert [task["status"] for task in building["tasks"]] == ["failed"]
    assert _step(story, "finished")["status"] == "failed"
    assert story["changes"] == []
    assert story["ended_at"] is not None
    assert "down" not in json.dumps(story)


def test_a_budget_stop_asks_whether_to_extend(data_root, repo):
    job_id = _run(repo)
    _save(job_id, state=RunState.STOPPED, stop_source="budget")
    story = _story(job_id, data_root)

    assert story["state"] == "waiting"
    assert story["state_detail"]["question"] == "token_budget"
    assert story["next"]["action"] == "answer"
    assert story["next"]["route"]["path"].startswith(f"/api/v1/jobs/{job_id}/decisions/")


@pytest.mark.parametrize(("state", "stop_source", "reason", "action"), [
    (RunState.STOPPED, "budget", "budget_exhausted", "none"),
    # exec-1017c (R-1340): a stop on request is resumable, so it is no cancel and it offers its resume.
    (RunState.STOPPED, "operator", "stopped", "resume"),
    (RunState.CANCELLED, "", "cancelled", "none"),
    (RunState.PAUSED, "", "paused", "none"),
])
def test_a_stopped_job_names_why(data_root, repo, monkeypatch, state, stop_source, reason, action):
    import packages.orchestration.decision_queue as decision_queue

    monkeypatch.setattr(decision_queue, "list_decisions", lambda plan, events: [])  # answered
    job_id = _run(repo)
    _save(job_id, state=state, stop_source=stop_source)
    story = _story(job_id, data_root)

    assert story["state"] == "stopped"
    assert story["state_detail"] == {"reason": {"key": reason, "args": {}}}
    route = {"method": "POST", "path": f"/api/v1/jobs/{job_id}/run"} if action == "resume" else None
    assert story["next"] == {"action": action, "route": route}


def test_a_planned_job_reads_queued_and_offers_its_run(data_root, repo):
    """exec-1017c (R-1340): it read `planning`, its planning step `running`, with no next step."""
    from packages.orchestration.pingpong_job import parse_job_file

    job = parse_job_file(_JOB, str(repo))
    story = _story(job.job_id, data_root)

    assert (story["state"], story["state_detail"]) == ("queued", {})
    assert story["next"] == {"action": "run", "route": {"method": "POST", "path": f"/api/v1/jobs/{job.job_id}/run"}}
    assert _step(story, "planning")["status"] == "done"
    assert _step(story, "building")["status"] == "waiting"
    assert story["started_at"] is None and story["ended_at"] is None
    assert story["numbers"] == {"duration_s": None, "tokens_in": None, "tokens_out": None,
                                "calls": None, "model_turns": None, "rounds": None}
    assert story["verification"] == {"status": "pending", "required": False}


def test_a_running_job_reads_reading_then_working_then_checking(data_root, repo):
    from packages.orchestration.pingpong_job import TASK_PENDING, TASK_RUNNING, load_job_plan_safe, parse_job_file

    job = parse_job_file(_JOB, str(repo))
    plan, _degraded = load_job_plan_safe(job.job_id)
    plan.state = RunState.RUNNING
    plan.first_running_at = "2026-10-15T11:59:00+00:00"
    plan.tasks[0].status = TASK_PENDING
    task_id = plan.tasks[0].task_id

    reading = build_client_story(plan, events=[], now=_NOW)
    assert reading["state"] == "reading"
    assert reading["numbers"]["duration_s"] == 60
    assert reading["ended_at"] is None

    plan.tasks[0].status = TASK_RUNNING
    started = [{"event": "task_run_started", "task_id": task_id,
                "timestamp": "2026-10-15T11:59:10+00:00"}]
    working = build_client_story(plan, events=started, now=_NOW)
    assert working["state"] == "working"
    assert working["state_detail"]["round"] == 1
    assert _step(working, "building")["phrase"]["key"] == "working_on_file"
    assert story_problems(working) == []

    one_round = started + [{"event": "task_round_completed", "task_id": task_id,
                            "timestamp": "2026-10-15T11:59:20+00:00",
                            "metadata": {"round_number": 1, "outcome": "needs_repair"}}]
    assert build_client_story(plan, events=one_round, now=_NOW)["state_detail"]["round"] == 2

    checking = build_client_story(plan, events=one_round + [
        {"event": "test_run_started", "task_id": task_id, "timestamp": "2026-10-15T11:59:30+00:00"}],
        now=_NOW)
    assert checking["state"] == "checking"
    assert _step(checking, "checking")["status"] == "running"
    assert story_problems(checking) == []


def test_an_open_decision_reads_waiting_and_names_its_answer_route(data_root, repo, monkeypatch):
    import packages.orchestration.decision_queue as decision_queue

    job_id = _run(repo)
    monkeypatch.setattr(decision_queue, "list_decisions", lambda plan, events: [
        SimpleNamespace(id="dec 1", type="token_budget", status="open"),
        SimpleNamespace(id="dec 0", type="done_before", status="answered")])
    story = _story(job_id, data_root)

    assert story["state"] == "waiting"
    assert story["state_detail"] == {"question": "token_budget", "decision_id": "dec 1"}
    assert story["next"] == {"action": "answer", "route": {
        "method": "POST", "path": f"/api/v1/jobs/{job_id}/decisions/dec%201"}}



def test_a_job_queued_after_another_names_it_until_its_result_lands(data_root, repo, monkeypatch):
    """The lab's job 537d7c3612864597 read `planning`, step `running`, next `none` (R-1340)."""
    import packages.orchestration.job_apply as job_apply
    from packages.orchestration.order_jobs import ORDER_JOB_WAITS_KEY
    from packages.orchestration.pingpong_job import parse_job_file

    job = parse_job_file(_JOB, str(repo))
    _save(job.job_id, metadata={ORDER_JOB_WAITS_KEY: "aaaa000000000001"})

    story = _story(job.job_id, data_root)
    assert (story["state"], story["state_detail"]) == ("queued", {"after_job": "aaaa000000000001"})
    assert story["next"] == {"action": "none", "route": None}      # the next step is that job's apply

    monkeypatch.setattr(job_apply, "job_apply_landed", lambda job_id: True)
    assert _story(job.job_id, data_root)["next"]["action"] == "run"


@pytest.mark.parametrize(("state", "action"), [
    (RunState.COMPLETED, "decline"), (RunState.RUNNING, "abandon"), (RunState.PLANNED, "abandon"),
    (RunState.STOPPED, "abandon"), (RunState.PAUSED, "abandon"), (RunState.BLOCKED, "abandon"),
    (RunState.FAILED, None), (RunState.CANCELLED, None),
])
def test_every_open_job_names_its_way_out_and_an_ended_one_none(data_root, repo, monkeypatch, state, action):
    """exec-1018b (R-1360): `next` is the one step forward and was `none` for a stopped, blocked or
    waiting job, so a client could close none of them; `end` is always the way out while the job is open."""
    import packages.orchestration.decision_queue as decision_queue

    monkeypatch.setattr(decision_queue, "list_decisions", lambda plan, events: [])
    job_id = _run(repo)
    _save(job_id, state=state)
    story = _story(job_id, data_root)

    route = {"method": "POST", "path": f"/api/v1/jobs/{job_id}/{action}"} if action else None
    assert story["end"] == ({"action": action, "route": route} if action else None)


def test_an_applied_or_declined_result_has_no_way_out_left(data_root, repo):
    from packages.orchestration.job_apply import apply_job, decline_job_result
    from packages.orchestration.pingpong_job import _persist_job, load_job_plan_safe

    applied = _run(repo)
    assert apply_job(applied, str(repo), approve=True).status == "applied"
    declined = _run(repo)
    plan, _degraded = load_job_plan_safe(declined)
    decline_job_result(plan, reason="not wanted", source="test", now=_NOW)
    _persist_job(plan)

    assert _story(applied, data_root)["end"] is None and _story(declined, data_root)["end"] is None
