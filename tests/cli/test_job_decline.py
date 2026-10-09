"""F304 T003 — one command declines a completed job's result, recorded as the operator's own act.

`remedy job decline <job> --reason <text> --json` records the decline on the job and applies
nothing; the job then reads `waits_for_apply` false and leaves `awaiting_apply`, and `remedy job
ownership` names the decline with the command line's door and the reason (DECISION F304 D5).

In-process through `apps.cli.grouped.main`, with the real `run_job` and fake providers, the way
`tests/orchestration/test_job_apply_commit.py` drives them, and the data root under `tmp_path`.
"""
from __future__ import annotations

import json

import pytest

from apps.cli.client_interface import OPERATION_ANSWER_KEYS, OPERATION_REFUSAL_TOKENS
from apps.cli.grouped import main
from packages.orchestration.job_apply import apply_job, job_result_decline
from packages.orchestration.pingpong_job import JobPlan, load_job_plan, save_job_plan
from tests.orchestration.test_job_apply_history import (  # noqa: F401  (autouse fixture)
    _completed,
    data_root,
)
from tests.orchestration.test_job_worktree_integration import (  # noqa: F401  (fixture)
    _git,
    repo,
)


def _answer(capsys, *argv: str) -> dict:
    main([*argv, "--json"])
    return json.loads(capsys.readouterr().out)


def _refused(capsys, *argv: str, code: int) -> dict:
    with pytest.raises(SystemExit) as exc:
        main([*argv, "--json"])
    assert exc.value.code == code
    data = json.loads(capsys.readouterr().out)
    assert data["ok"] is False and data["error"] in OPERATION_REFUSAL_TOKENS["job.decline"], data
    return data


def _digest_job(capsys, job_id: str) -> tuple[dict, list[str]]:
    client = _answer(capsys, "status")["client"]
    [entry] = [job for job in client["jobs"] if job["job_id"] == job_id]
    return entry, client["awaiting_apply"]


def test_a_declined_job_no_longer_waits_and_its_ownership_names_the_decline(
        repo, monkeypatch, capsys):
    job = _completed(repo, monkeypatch)
    monkeypatch.chdir(repo)
    entry, awaiting = _digest_job(capsys, job.job_id)
    assert entry["waits_for_apply"] is True and job.job_id in awaiting

    data = _answer(capsys, "job", "decline", job.job_id, "--reason", "the page is not wanted")

    keys = set(data) - {"ok", "schema_version"}
    assert sorted(keys) == ["already_declined", "declined_at", "job_id", "reason", "source"]
    assert keys <= set(OPERATION_ANSWER_KEYS["job.decline"])
    assert (data["ok"], data["job_id"], data["reason"], data["source"]) == (
        True, job.job_id, "the page is not wanted", "cli")
    assert data["already_declined"] is False and data["declined_at"]
    entry, awaiting = _digest_job(capsys, job.job_id)
    assert entry["waits_for_apply"] is False and job.job_id not in awaiting
    [declined] = [e for e in _answer(capsys, "job", "ownership", job.job_id)["entries"]
                  if e["action"] == "result_declined"]
    assert (declined["actor"]["door"], declined["text"]) == ("cli", "the page is not wanted")
    assert declined["ts"] == data["declined_at"]
    assert not (repo / "one.txt").exists()


def test_a_second_decline_answers_the_first_unchanged(repo, monkeypatch, capsys):
    job = _completed(repo, monkeypatch)
    first = _answer(capsys, "job", "decline", job.job_id, "--reason", "first reason")

    second = _answer(capsys, "job", "decline", job.job_id, "--reason", "second reason")

    assert second["already_declined"] is True
    assert (second["reason"], second["declined_at"]) == (first["reason"], first["declined_at"])
    assert job_result_decline(load_job_plan(job.job_id))["reason"] == "first reason"


def test_a_job_that_is_not_completed_is_refused_and_nothing_is_recorded(capsys):
    job = JobPlan(job_title="still planned")
    save_job_plan(job)

    data = _refused(capsys, "job", "decline", str(job.job_id), "--reason", "too early", code=3)

    assert data["error"] == "job_not_declinable"
    assert job_result_decline(load_job_plan(str(job.job_id))) is None


def test_a_job_whose_result_landed_is_refused_and_nothing_is_recorded(repo, monkeypatch, capsys):
    job = _completed(repo, monkeypatch)
    assert apply_job(job.job_id, str(repo), approve=True).status == "applied"

    data = _refused(capsys, "job", "decline", job.job_id, "--reason", "too late", code=3)

    assert data["error"] == "job_already_applied"
    assert job_result_decline(load_job_plan(job.job_id)) is None


def test_a_blank_reason_exits_2_and_nothing_is_recorded(repo, monkeypatch, capsys):
    job = _completed(repo, monkeypatch)

    data = _refused(capsys, "job", "decline", job.job_id, "--reason", "   ", code=2)

    assert data["error"] == "missing_argument"
    assert job_result_decline(load_job_plan(job.job_id)) is None


def test_the_text_answer_names_the_job_and_the_reason(repo, monkeypatch, capsys):
    job = _completed(repo, monkeypatch)

    main(["job", "decline", job.job_id, "--reason", "not wanted"])

    out = capsys.readouterr().out
    assert f"The result of job {job.job_id} is declined: not wanted" in out
    assert "Nothing was applied" in out


def test_a_decline_keeps_the_door_its_source_names(repo, monkeypatch, capsys):
    """DECISION F253 D11: the public HTTP API passes `--source api`, and the record keeps it."""
    job = _completed(repo, monkeypatch)

    data = _answer(capsys, "job", "decline", job.job_id, "--reason", "not wanted",
                   "--source", "api")

    assert data["source"] == "api"
    assert job_result_decline(load_job_plan(job.job_id))["source"] == "api"
    [declined] = [e for e in _answer(capsys, "job", "ownership", job.job_id)["entries"]
                  if e["action"] == "result_declined"]
    assert (declined["actor"]["door"], declined["actor"]["recorded_as"]) == ("", "api")
