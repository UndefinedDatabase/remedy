"""R-1332, DECISION F307 D21: a job a run leaves blocked keeps the time it ended."""
from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest

from packages.core.models import RunState

_JOB = "# Job: finish\n\n## Task 1\nDo a thing.\n\nAcceptance:\n- done\n"


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


def _passing():
    from packages.orchestration.pingpong_provider_fake import FakeProvider

    return FakeProvider(pass_on_round=1, fail_on_round=99)


def _blocked_once(repo: Path):
    from packages.orchestration.pingpong_job import parse_job_file, run_job
    from packages.orchestration.pingpong_provider_fake import FakeProvider

    job = parse_job_file(_JOB, str(repo))
    run_job(job.job_id, builder_provider=FakeProvider(builder_error="provider_unavailable: down"),
            reviewer_provider=_passing(), repair_rounds=0)
    return job.job_id


def test_a_job_a_run_leaves_blocked_keeps_the_time_it_ended(data_root, repo):
    from packages.orchestration.pingpong_job import load_job_plan

    started = datetime.now(timezone.utc)
    job_id = _blocked_once(repo)

    stored = load_job_plan(job_id)
    assert stored.state == RunState.BLOCKED
    ended = datetime.fromisoformat(stored.finished_at)
    assert ended.tzinfo is not None and started <= ended <= datetime.now(timezone.utc)


def test_a_run_that_finds_its_task_already_blocked_keeps_a_finish_time_too(data_root, repo):
    """The second run ends blocked through `blocked_rerun_reason`, not through `_block_job`."""
    from packages.orchestration.pingpong_job import load_job_plan, run_job, save_job_plan

    job_id = _blocked_once(repo)
    stored = load_job_plan(job_id)
    stored.finished_at = ""
    save_job_plan(stored)

    again = run_job(job_id, builder_provider=_passing(), reviewer_provider=_passing(), repair_rounds=0)

    stored = load_job_plan(job_id)
    assert again.state == stored.state == RunState.BLOCKED
    assert stored.finished_at and again.finished_at == stored.finished_at


def test_a_run_of_a_job_with_no_record_writes_no_record(data_root):
    from packages.orchestration.pingpong_job import load_job_plan, run_job

    answer = run_job("0123456789abcdef")

    assert answer.state == RunState.BLOCKED and answer.finished_at == ""
    assert load_job_plan("0123456789abcdef") is None


def test_the_wrapper_leaves_a_finish_time_and_a_job_that_is_not_blocked_alone(data_root, repo):
    from packages.orchestration.job_run_finish import stamp_blocked_job_finish
    from packages.orchestration.pingpong_job import load_job_plan, parse_job_file, save_job_plan

    job = parse_job_file(_JOB, str(repo))
    stamped = stamp_blocked_job_finish(lambda: load_job_plan(job.job_id))
    assert stamped().finished_at == ""                      # a planned job is not blocked

    job = load_job_plan(job.job_id)
    job.state, job.finished_at = RunState.BLOCKED, "2026-01-01T00:00:00+00:00"
    save_job_plan(job)
    assert stamped().finished_at == "2026-01-01T00:00:00+00:00"
    assert load_job_plan(job.job_id).finished_at == "2026-01-01T00:00:00+00:00"
