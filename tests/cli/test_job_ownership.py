"""`remedy job ownership` — F035 T003, DECISION F035 D4.

Modelled on `test_job_steer.py`: the CLI handler is proved through the real argv dispatcher,
over a real `JobPlan` saved to a temp data root. The view itself — `ownership_view` — is
proved in `tests/orchestration/test_ownership_phrases.py`; this file proves the CLI's
wrapping: the job-id resolution every job command shares, the exit code each refusal maps
to, the JSON envelope, and the text form's per-entry sentence layout.
"""
from __future__ import annotations

import json
from uuid import uuid4

import pytest

from packages.orchestration import pingpong_job as pj
from packages.orchestration.pingpong_job import JobPlan, TaskEntry

_VETO_METADATA = {
    "request_id": "r1",
    "requested_at": "2026-08-29T00:00:00+00:00",
    "actor": "alice",
    "reason": "bad approach",
    "status_at_veto": "completed",
    "unreachable_task_ids": [],
}


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


@pytest.fixture
def job() -> pj.JobPlan:
    job = JobPlan(job_title="CLI ownership test", tasks=[TaskEntry(title="write a readme")])
    pj.save_job_plan(job)
    return job


def _run(argv: list[str], capsys) -> tuple[int, str]:
    from apps.cli.grouped import main

    try:
        code = main(argv)
    except SystemExit as exc:
        code = exc.code
    return (code or 0), capsys.readouterr().out


def _give_job_one_action(job: pj.JobPlan) -> None:
    job.metadata["task_vetoes"] = {job.tasks[0].task_id: dict(_VETO_METADATA)}
    pj.save_job_plan(job)


class TestOwnershipTextAndJSON:
    def test_the_text_form_reports_no_action_for_an_empty_ledger(self, job, capsys):
        code, out = _run(["job", "ownership", str(job.job_id)], capsys)
        assert code == 0
        assert out == f"No action is recorded for job {job.job_id} yet.\n"

    def test_the_text_form_lists_one_sentence_per_entry(self, job, capsys):
        _give_job_one_action(job)
        code, out = _run(["job", "ownership", str(job.job_id)], capsys)
        assert code == 0
        lines = out.splitlines()
        assert lines[0] == f"Who did what in job {job.job_id}:"
        assert len(lines) == 2
        assert lines[1].startswith("  - ")
        assert "vetoed" in lines[1]

    def test_the_json_form_emits_the_views_own_keys_for_an_empty_ledger(self, job, capsys):
        code, out = _run(["job", "ownership", str(job.job_id), "--json"], capsys)
        assert code == 0
        body = json.loads(out)
        assert body["ok"] is True
        assert body["job_id"] == str(job.job_id)
        assert body["schema"] == "remedy.ownership.v1"
        assert body["entries"] == []

    def test_the_json_form_carries_a_sentence_on_every_entry(self, job, capsys):
        _give_job_one_action(job)
        code, out = _run(["job", "ownership", str(job.job_id), "--json"], capsys)
        assert code == 0
        body = json.loads(out)
        assert body["entries"]
        assert all(e["sentence"] for e in body["entries"])


class TestOwnershipExitCodes:
    def test_a_malformed_job_id_exits_1(self, capsys):
        """MEASURED against `resolve_job_id_or_fail` (`apps/cli/job_id_arg.py`): every
        `JobIdError` it catches that is not `JobIdAmbiguous` — a malformed shape among
        them — answers `invalid_job_id` at `fail()`'s own default exit code, 1, never 2;
        2 is reachable only through a genuinely ambiguous prefix match, which this string
        is not."""
        code, out = _run(["job", "ownership", "../etc", "--json"], capsys)
        assert code == 1
        assert json.loads(out)["error"] == "invalid_job_id"

    def test_an_unknown_job_exits_3(self, capsys):
        code, out = _run(["job", "ownership", str(uuid4()), "--json"], capsys)
        assert code == 3
        assert json.loads(out)["error"] == "job_not_found"

    def test_a_ledger_that_raises_exits_1(self, job, capsys, monkeypatch):
        from packages.orchestration import ownership as own

        def _raise(_job):
            raise own.OwnershipError("boom")

        monkeypatch.setattr("packages.orchestration.ownership.build_ownership_ledger", _raise)
        code, out = _run(["job", "ownership", str(job.job_id), "--json"], capsys)
        assert code == 1
        body = json.loads(out)
        assert body["error"] == "ownership_unreadable"
        assert "boom" in body["message"]
