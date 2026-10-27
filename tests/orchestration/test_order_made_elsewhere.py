"""Operator amendment amend1027b-v1, A3: the order of a job no `POST /api/v1/orders` started.

A job made by `remedy do` in a terminal named only its batch's 32-character id, which no order
route takes, so an app could neither poll nor cancel its order (the remedy edition's F036). Since
1.32 every job names its order by 16 characters, and the order routes resolve the first 16
characters of a batch's id back to it. Each test walks a real `remedy do run` with the fake
builder and reviewer from a terminal folder, not from an order folder of the supervisor.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
from types import SimpleNamespace

import pytest

from packages.core.models import RunState
from tests.orchestration.scale_harness import commit_repository

README = {"README.md": "# Project\n\nA projcet with a typo.\n"}


@pytest.fixture
def walked(tmp_path, monkeypatch):
    """One finished terminal walk: (job, batch id, project id)."""
    from apps.cli.grouped import main
    from packages.orchestration.mission_state import list_missions, project_ids_with_missions
    from packages.orchestration.pingpong_job import load_job_plan

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    repo = commit_repository(tmp_path / "work", README)
    monkeypatch.chdir(tmp_path)
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.suppress(SystemExit):
        main(["do", "run", "--repo", str(repo), "--builder-provider", "fake", "--reviewer-provider", "fake",
              "--json", "--no-ui", "--run-unattended", "--", "Fix the typo in README.md."])
    [job_id] = json.loads(out.getvalue())["job_ids"]
    [project_id] = project_ids_with_missions()
    [mission] = list_missions(project_id)
    [batch_id] = {link.order_id for link in mission.job_links if link.job_id == job_id}
    return load_job_plan(job_id), batch_id, project_id


def _client(command: list[str]) -> dict:
    from apps.cli.grouped import main

    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.suppress(SystemExit):
        main(command)
    return json.loads(out.getvalue())


def test_the_job_names_its_order_by_sixteen_characters_everywhere(walked):
    from packages.orchestration.client_digest import build_client_digest
    from packages.orchestration.client_story import job_client_story

    job, batch_id, _project = walked
    assert len(batch_id) == 32
    assert job_client_story(str(job.job_id), job)["order_id"] == batch_id[:16]
    [entry] = [e for e in build_client_digest()["jobs"] if e["job_id"] == str(job.job_id)]
    assert (entry["order_id"], entry["order_batch_id"]) == (batch_id[:16], batch_id)


def test_the_order_routes_read_and_cancel_the_order_of_a_job_made_elsewhere(walked):
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import order_record_for_job, read_order_record

    job, batch_id, _project = walked
    order_id = batch_id[:16]
    polled = _client(["client", "order", order_id, "--json"])
    assert polled["ok"] is True and polled["order_id"] == order_id
    assert (polled["state"], polled["phase"], polled["answer"]) == ("ended", "awaiting_apply", None)
    assert [entry["job_id"] for entry in polled["jobs"]] == [str(job.job_id)]
    assert _client(["client", "order-story", order_id, "--json"])["missions"][0]["milestones"][0]["jobs"][0][
        "job_id"] == str(job.job_id)

    cancelled = _client(["client", "cancel-order", order_id, "--decline-results", "--reason", "nicht mehr nötig",
                         "--json"])
    assert cancelled["ok"] is True
    assert [(e["job_id"], e["outcome"]) for e in cancelled["jobs"]] == [(str(job.job_id), "declined")]
    assert _client(["client", "cancel-order", order_id, "--json"])["already_cancelled"] is True
    # The request has a folder of its own, beside no order.json, so it is no order of the supervisor.
    paths = serve_paths()
    assert (paths.orders_dir / order_id / "cancel.json").is_file()
    assert read_order_record(paths, order_id) is None
    assert order_record_for_job(paths, str(job.job_id)) is None


def test_a_job_a_terminal_may_still_run_gets_a_stop_request_not_an_end(walked):
    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan

    job, batch_id, _project = walked
    job.state = RunState.RUNNING
    save_job_plan(job)

    cancelled = _client(["client", "cancel-order", batch_id[:16], "--json"])

    assert [e["outcome"] for e in cancelled["jobs"]] == ["cancel_pending"]
    assert load_job_plan(str(job.job_id)).state == RunState.RUNNING


def test_an_id_no_batch_begins_with_is_still_not_found(walked):
    answer = _client(["client", "order", "ffffffffffffffff", "--json"])
    assert answer["ok"] is False and answer["error"] == "order_not_found"


def test_a_client_reads_such_an_order_only_for_its_own_projects(walked):
    from packages.orchestration.client_scope import client_order_read_refusal

    _job, batch_id, project_id = walked
    assert client_order_read_refusal(SimpleNamespace(name="orb", projects=(project_id,)), batch_id[:16]) is None
    refusal = client_order_read_refusal(SimpleNamespace(name="orb", projects=("other",)), batch_id[:16])
    assert refusal is not None and "may not read order" in refusal
