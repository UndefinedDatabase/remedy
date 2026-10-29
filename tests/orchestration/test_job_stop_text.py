"""F325 — every stop says why: the story's `stop`, each order job's `stop_text`, `job show`'s `stop.text`."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from packages.orchestration.job_stop_text import (
    STOP_REASON_REVIEW_BLOCKED,
    STOP_REASON_TESTS_FAILED,
    job_stop,
    job_stop_text,
)

_NOW = datetime(2026, 10, 29, 12, 0, tzinfo=timezone.utc)


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch):
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


def _review_blocked_job(tmp_path: Path, findings: list[dict], run_id: str = "6afc431f57f5aaaa"):
    """Job 92af245f83d246d3 of 2026-10-28: its first task blocked by the review, `stop.reason` empty."""
    from packages.core.models import RunState
    from packages.orchestration import data_paths
    from packages.orchestration.pingpong_job import TASK_BLOCKED, parse_job_file, save_job_plan

    repo = tmp_path / "repo"
    repo.mkdir(exist_ok=True)
    job = parse_job_file("# Job: Pictures\n\n## Task 1: Add the tests\nAdd the tests.\n\nAcceptance:\n- tested\n\n"
                         "## Task 2\nDocument it.\n\nAcceptance:\n- documented\n", str(repo))
    task = job.tasks[0]
    task.status, task.final_status, task.reviewer_verdict = TASK_BLOCKED, "staged_blocked", "blocked"
    task.error = "completion_gate_failed: final_status=staged_blocked; reviewer_verdict=blocked"
    task.run_id = run_id
    run_dir = data_paths.run_dir(task.run_id)
    run_dir.mkdir(parents=True)
    (run_dir / "result.json").write_text(json.dumps(
        {"rounds": [{"round": 2, "reviewer": {"verdict": "blocked", "findings": findings}}]}), encoding="utf-8")
    job.state = RunState.BLOCKED
    save_job_plan(job)
    return job


_MEDIUM = {"id": "R2", "severity": "medium", "file": "tests/test_images.py",
           "summary": "Still no test run against the staged worktree."}


def test_a_job_its_review_blocked_names_the_verdict_and_the_findings_severity(tmp_path: Path) -> None:
    job = _review_blocked_job(tmp_path, [_MEDIUM])
    assert job.stop_reason == ""
    stop = job_stop(job)
    assert stop["reason"] == STOP_REASON_REVIEW_BLOCKED
    assert stop["text"] == ('The review ended task "Add the tests" with the verdict blocked on one medium '
                            'finding; the first (medium): Still no test run against the staged worktree.')
    several = _review_blocked_job(tmp_path, [dict(_MEDIUM, severity="low"), _MEDIUM, dict(_MEDIUM, severity="high")],
                                  run_id="6afc431f57f5bbbb")
    assert "on one high, one medium and one low findings;" in job_stop_text(several)


def test_the_story_the_order_view_and_job_show_say_the_same_sentence(tmp_path: Path, capsys) -> None:
    from apps.cli.commands.job import _cmd_show_job
    from packages.orchestration.client_story import build_client_story
    from packages.orchestration.order_jobs import _job_entry

    job = _review_blocked_job(tmp_path, [_MEDIUM])
    sentence = job_stop_text(job)
    assert build_client_story(job, events=[], now=_NOW)["stop"] == {"reason": STOP_REASON_REVIEW_BLOCKED,
                                                                   "text": sentence}
    assert _job_entry(job)["stop_text"] == sentence
    _cmd_show_job(str(job.job_id), json_output=True)
    shown = json.loads(capsys.readouterr().out)
    assert shown["stop"]["text"] == sentence and shown["stop"]["reason"] == STOP_REASON_REVIEW_BLOCKED


def test_every_stopped_state_carries_a_sentence(tmp_path: Path) -> None:
    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import TASK_FAILED, parse_job_file

    repo = tmp_path / "repo"
    repo.mkdir()
    job = parse_job_file("# Job: Demo\n\n## Task 1: Fix README\nFix README.\n\nAcceptance:\n- fixed\n", str(repo))
    assert job_stop(job) == {"reason": "", "text": ""}           # a job that did not stop says nothing
    for state in (RunState.STOPPED, RunState.CANCELLED, RunState.FAILED, RunState.BLOCKED):
        job.state = state
        assert job_stop_text(job), state
    job.state, job.stop_reason = RunState.STOPPED, "operator_stop"
    assert job_stop_text(job) == "The job stopped: operator stop."
    job.stop_text = "Stopped by the order's cancel."
    assert job_stop_text(job) == "Stopped by the order's cancel."
    failed = parse_job_file("# Job: Demo\n\n## Task 1: Fix README\nFix README.\n\nAcceptance:\n- fixed\n", str(repo))
    failed.state, failed.tasks[0].status, failed.tasks[0].test_passed = RunState.FAILED, TASK_FAILED, False
    assert job_stop(failed)["reason"] == STOP_REASON_TESTS_FAILED
    assert job_stop_text(failed).startswith('The tests of task "Fix README')
