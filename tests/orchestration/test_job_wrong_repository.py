"""F330 (operator order beweis): an unattended job whose work is not in its repository ends at once."""
from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from packages.orchestration import job_run_finish, pingpong_job, pingpong_loop
from packages.orchestration.job_stop_text import job_stop
from packages.orchestration.job_wrong_repository import NOT_IN_THIS_REPOSITORY, end_job_not_in_this_repository
from packages.orchestration.order_jobs import JOB_UNATTENDED_KEY
from packages.orchestration.pingpong_provider import _parse_reviewer_json, _parse_reviewer_structured
from packages.orchestration.review_scope_rules import REVIEWER_SCOPE_RULES

WRONG_REPO = {"id": "tzbwja-wrong-repo", "severity": "high", "file": "", "kind": NOT_IN_THIS_REPOSITORY,
              "summary": "This repository has no diff view; the work belongs in universe-chat."}


def _job(*, unattended=True, changed=(), kind=NOT_IN_THIS_REPOSITORY):
    # WHY a namespace: the ending reads only these fields, as a JobPlan carries them.
    task = SimpleNamespace(id="t1", title="Diff-Schrift zu groß auf Mobile", status="blocked", run_id="run-1",
                           safe_diff_files=list(changed))
    job = SimpleNamespace(job_id="44f5ec598488464c", state="blocked", tasks=[task], stop_reason="",
                          repo_path="/home/user/Repos/remedy-backend", finished_at="", pause=None, error="",
                          metadata={JOB_UNATTENDED_KEY: unattended})
    return job, {"rounds": [{"round": 1, "reviewer": {"verdict": "blocked", "findings": [{**WRONG_REPO, "kind": kind}]}}]}


@pytest.fixture
def run_record(monkeypatch):
    records: dict[str, dict] = {}
    monkeypatch.setattr(pingpong_loop, "load_run", lambda run_id: records[run_id])
    return records


def test_an_unattended_job_with_no_change_ends_failed_with_the_reason_and_the_repository(run_record):
    job, run_record["run-1"] = _job()
    assert end_job_not_in_this_repository(job)
    assert (str(job.state), job.stop_reason) == ("failed", "not_in_this_repository") and job.finished_at
    stop = job_stop(job)
    assert stop["reason"] == NOT_IN_THIS_REPOSITORY
    assert stop["text"] == (
        "Remedy ended the job without a change, because the review says the work of task \"Diff-Schrift zu groß "
        "auf Mobile\" does not belong in the repository remedy-backend (/home/user/Repos/remedy-backend): "
        "This repository has no diff view; the work belongs in universe-chat.")


@pytest.mark.parametrize("variant", [{"changed": ["src/view.py"]}, {"unattended": False}, {"kind": ""}])
def test_a_changed_file_an_attended_job_or_another_finding_stays_on_the_review_path(run_record, variant):
    job, run_record["run-1"] = _job(**variant)
    assert not end_job_not_in_this_repository(job)
    assert (job.state, job.stop_reason) == ("blocked", "")


def test_the_run_wrapper_ends_and_saves_the_job(run_record, monkeypatch):
    job, run_record["run-1"] = _job()
    saved = []
    monkeypatch.setattr(pingpong_job, "load_job_plan_safe", lambda job_id: (job, False))
    monkeypatch.setattr(pingpong_job, "save_job_plan", saved.append)
    monkeypatch.setattr(job_run_finish, "settle_jobs_waiting_for", lambda job_id: None)
    returned = SimpleNamespace(job_id=job.job_id, state="blocked", stop_reason="", finished_at="", metadata={})
    result = job_run_finish.stamp_blocked_job_finish(lambda job_id: returned)(job.job_id)
    assert saved == [job] and str(result.state) == "failed" and result.stop_reason == NOT_IN_THIS_REPOSITORY


def test_the_reviewer_is_asked_for_the_kind_and_both_parsers_keep_it():
    assert f"finding whose kind is {NOT_IN_THIS_REPOSITORY}" in REVIEWER_SCOPE_RULES
    verdict = {"verdict": "blocked", "findings": [{**WRONG_REPO, "required_fix": ""}], "confidence": "high",
               "summary": "Not in this repository."}
    [free] = _parse_reviewer_json(json.dumps(verdict), 1, 1).findings
    [strict] = _parse_reviewer_structured(json.dumps({"schema_v": "rv1", **verdict}), 1, 1).findings
    assert free.kind == strict.kind == NOT_IN_THIS_REPOSITORY
