"""F264 T001 — `remedy chat <job_id> "<message>"` records a steering message for a job.

Temporary data roots only. No provider call is ever made.
"""
from __future__ import annotations

import json

import pytest

from apps.cli.grouped import main as grouped_main
from packages.core.models import RunState
from packages.orchestration import pingpong_job as PJ
from packages.orchestration import steering as ST

ONE_TASK = "# One\n\n## Task 1 — write\n\nWrite one.txt.\n"


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


def _job(tmp_path, state: RunState = RunState.RUNNING) -> PJ.JobPlan:
    job = PJ.parse_job_file(ONE_TASK, str(tmp_path))
    job.state = state
    PJ.save_job_plan(job)
    return job


def _run(argv: list[str]) -> int:
    try:
        grouped_main(argv)
    except SystemExit as exc:
        return int(exc.code or 0)
    return 0


class TestChatSend:
    def test_the_bare_group_form_records_the_message(self, tmp_path, capsys):
        job = _job(tmp_path)
        assert _run(["chat", job.job_id, "Keep the public API unchanged.", "--json"]) == 0
        out = json.loads(capsys.readouterr().out)
        assert out["ok"] is True
        assert out["job_id"] == job.job_id
        assert out["message_id"] == "sm-0001"
        [record] = ST.list_steering_messages(job.job_id)
        assert record["text"] == "Keep the public API unchanged."
        assert record["channel"] == "cli"
        assert record["record_sha256"] == out["record_sha256"]

    def test_a_unique_prefix_names_the_job(self, tmp_path, capsys):
        job = _job(tmp_path)
        assert _run(["chat", "send", job.job_id[:8], "Smaller commits."]) == 0
        text = capsys.readouterr().out
        assert f"Message sm-0001 recorded for job {job.job_id}." in text
        assert "next safe point" in text
        assert [r["text"] for r in ST.list_steering_messages(job.job_id)] == ["Smaller commits."]

    def test_an_unknown_job_exits_1_and_records_nothing(self, tmp_path, capsys):
        assert _run(["chat", "feedfacefeedface", "Hello.", "--json"]) == 1
        out = json.loads(capsys.readouterr().out)
        assert out["ok"] is False
        assert out["error"] == "invalid_job_id"

    def test_an_ended_job_exits_3_and_records_nothing(self, tmp_path, capsys):
        job = _job(tmp_path, RunState.COMPLETED)
        assert _run(["chat", job.job_id, "Too late.", "--json"]) == 3
        out = json.loads(capsys.readouterr().out)
        assert out["error"] == "job_not_steerable"
        assert ST.list_steering_messages(job.job_id) == []

    def test_an_empty_message_exits_2_and_records_nothing(self, tmp_path, capsys):
        job = _job(tmp_path)
        assert _run(["chat", job.job_id, "   ", "--json"]) == 2
        out = json.loads(capsys.readouterr().out)
        assert out["error"] == "invalid_message"
        assert ST.list_steering_messages(job.job_id) == []
