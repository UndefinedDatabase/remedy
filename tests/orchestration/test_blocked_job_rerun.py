"""amend1015 Phase 1.2 — a run of a job whose task ended blocked ends blocked, never `running`.

A plain `remedy job run` re-attempts no such task, a retry with `--retry` does (R-1331). Before this
repair, a run of a job whose task had ended blocked skipped that task, ran nothing, and left the
job's record reading `running` with no run alive, so the story said "working" for ever. A job that
runs nothing and still has a blocked task ends blocked again, keeping the reason it had.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from packages.core.models import RunState

_JOB = "# Job: rerun\n\n## Task 1\nDo a thing.\n\nAcceptance:\n- done\n"


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


def test_a_run_of_a_job_whose_task_ended_blocked_ends_blocked(data_root, repo):
    from packages.orchestration.pingpong_job import load_job_plan_safe, parse_job_file, run_job
    from packages.orchestration.pingpong_provider_fake import FakeProvider

    job = parse_job_file(_JOB, str(repo))
    first = run_job(job.job_id, builder_provider=FakeProvider(builder_error="provider_unavailable: down"),
                    reviewer_provider=_passing(), repair_rounds=0)
    assert first.state == RunState.BLOCKED
    reason = first.error
    assert reason

    again = run_job(job.job_id, builder_provider=_passing(), reviewer_provider=_passing(),
                    repair_rounds=0)

    stored, _degraded = load_job_plan_safe(job.job_id)
    assert again.state == RunState.BLOCKED
    assert stored.state == RunState.BLOCKED
    assert stored.error == reason
    assert [task.status for task in stored.tasks] == ["blocked"]
