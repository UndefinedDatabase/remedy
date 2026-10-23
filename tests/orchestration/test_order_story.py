"""The story of an order, not only of a job (operator amendment amend1023-universe-trust, DECISION
amend1023 D11): `order_story.order_client_story`, its route and the order jobs' new keys, seeded with
the recording script's own seeds so the kit's recorded answer and these tests read one order."""
from __future__ import annotations

from datetime import datetime, timezone

import pytest

from packages.orchestration.order_story import ORDER_STORY_JOB_STATES, order_story_answer
from scripts.record_client_answers import (
    KIT_MISSION_ID,
    KIT_ORDER_ID,
    WAITING_JOB_ID,
    WORKING_JOB_ID,
    _seed_order,
    _seed_running_jobs,
)


@pytest.fixture()
def seeded(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setattr("packages.orchestration.job_insight.model_server_state",
                        lambda: {"provider": "ollama", "host": "stub", "state": "reachable", "loaded": [], "queue": None})
    now = datetime.now(timezone.utc)
    _seed_running_jobs(now)
    _seed_order(now)
    return now


def test_the_order_jobs_carry_their_mission_and_no_criterion_while_nothing_blocks(seeded):
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import order_record_payload, read_order_record

    paths = serve_paths()
    jobs = order_record_payload(paths, read_order_record(paths, KIT_ORDER_ID))["jobs"]
    assert {job["mission_id"] for job in jobs} == {KIT_MISSION_ID}
    assert all(job["blocking_criterion"] is None for job in jobs)
    assert [job["tasks"] for job in jobs][0] == {"total": 1, "done": 0, "current": "style.css"}


def test_a_blocked_job_names_the_criterion_it_did_not_meet_in_both_answers(seeded):
    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import TASK_BLOCKED, load_job_plan, save_job_plan

    job = load_job_plan(WORKING_JOB_ID)
    job.state = RunState.BLOCKED
    job.tasks[0].status = TASK_BLOCKED
    job.tasks[0].acceptance = "docs/chat_gedaechtnis_map.md exists"
    save_job_plan(job)
    answer = order_story_answer(order=KIT_ORDER_ID)
    first = answer["missions"][0]["milestones"][0]["jobs"][0]
    assert (first["state"], first["state_detail"]) == ("blocked", {"criterion": "docs/chat_gedaechtnis_map.md exists"})
    assert first["round"] is None and first["tool"] is None


def test_every_state_word_is_closed_and_an_unknown_order_is_refused(seeded):
    answer = order_story_answer(order=KIT_ORDER_ID)
    states = {job["state"] for mission in answer["missions"] for milestone in mission["milestones"]
              for job in milestone["jobs"]}
    assert states <= set(ORDER_STORY_JOB_STATES)
    assert [job["job_id"] for milestone in answer["missions"][0]["milestones"] for job in milestone["jobs"]][-1] == (
        WAITING_JOB_ID)
    refused = order_story_answer(order="0000000000000000")
    assert (refused["ok"], refused["error"]) == (False, "order_not_found")


def test_the_route_answers_the_command_and_a_client_reads_only_its_own_projects(seeded):
    from packages.orchestration.api_clients import ApiClient
    from packages.orchestration.public_api import answer_public_api_get

    path = f"/api/v1/orders/{KIT_ORDER_ID}/story"
    status, body, _headers = answer_public_api_get(path)
    assert status == 200 and body["client"] == "orb-universe"
    assert answer_public_api_get("/api/v1/orders/0000000000000000/story")[0] == 404
    stranger = ApiClient(name="stranger", token="s" * 40, projects=("elsewhere",), max_total_tokens=None,
                         max_provider_calls=None, may_apply=False)
    status, body, _headers = answer_public_api_get(path, "", stranger)
    assert (status, body["error"]) == (403, "api_client_policy_refused")


def test_the_launcher_keeps_the_client_that_sent_the_order(tmp_path, monkeypatch):
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import OrderLauncher, read_order_record

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    paths = serve_paths()
    launcher = OrderLauncher(paths, argv_prefix=["python3", "-c", "pass"])
    record = launcher.start("Fix it", [], client="orb-remedy")
    launcher.wait(record.order_id, timeout=30)
    assert read_order_record(paths, record.order_id).client == "orb-remedy"
    unnamed = launcher.start("Fix it", [])
    launcher.wait(unnamed.order_id, timeout=30)
    assert read_order_record(paths, unnamed.order_id).client == ""
