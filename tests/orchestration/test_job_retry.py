"""R-1331 — a retry of a job whose task ended blocked runs that task again (DECISION F307 D22).

Every job here is run by the real runner with fake providers in a temporary data root. A plain run
of a job whose task ended blocked re-attempts nothing (`test_blocked_job_rerun.py`); a retry puts
that task back to pending first, through `retry_blocked_job_tasks` and through
`remedy job run <job> --retry`.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from packages.core.models import RunState
from packages.orchestration.job_retry import retry_blocked_job_tasks

REPO = Path(__file__).resolve().parents[2]
_ONE = "# Job: retry\n\n## Task 1\nDo a thing.\n\nAcceptance:\n- done\n"
_TWO = _ONE + "\n## Task 2\nDo another thing.\n\nAcceptance:\n- done\n"


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
    from packages.orchestration.pingpong_provider_fake import FakeProvider

    return FakeProvider(pass_on_round=1, fail_on_round=99, **kw)


def _blocked(repo: Path, text: str = _ONE) -> str:
    """The id of a job whose first task ended blocked because its builder was unavailable."""
    from packages.orchestration.pingpong_job import parse_job_file, run_job

    job = parse_job_file(text, str(repo))
    first = run_job(job.job_id, builder_provider=_fake(builder_error="provider_unavailable: down"),
                    reviewer_provider=_fake(), repair_rounds=0)
    assert first.state == RunState.BLOCKED
    return job.job_id


def _stored(job_id: str):
    from packages.orchestration.pingpong_job import load_job_plan

    return load_job_plan(job_id)


def test_a_retry_puts_the_blocked_task_back_and_the_run_completes_it(data_root, repo):
    from packages.orchestration.pingpong_job import run_job

    job_id = _blocked(repo)
    job = _stored(job_id)
    assert job.error and job.finished_at

    assert retry_blocked_job_tasks(job) == (job.tasks[0].task_id,)
    stored = _stored(job_id)
    assert [(t.status, t.error) for t in stored.tasks] == [("pending", "")]
    assert (stored.error, stored.finished_at) == ("", "")

    again = run_job(job_id, builder_provider=_fake(), reviewer_provider=_fake(), repair_rounds=0)
    assert again.state == RunState.COMPLETED
    assert [t.status for t in _stored(job_id).tasks] == ["applied_to_job_workspace"]


def test_a_retry_restores_the_tasks_the_block_skipped(data_root, repo):
    job_id = _blocked(repo, _TWO)
    job = _stored(job_id)
    assert [t.status for t in job.tasks] == ["blocked", "skipped"]

    assert retry_blocked_job_tasks(job) == tuple(t.task_id for t in job.tasks)
    assert [t.status for t in _stored(job_id).tasks] == ["pending", "pending"]


def test_a_task_a_veto_makes_unreachable_stays_skipped(monkeypatch):
    from packages.orchestration import pingpong_job, task_veto

    saved: list = []
    monkeypatch.setattr(pingpong_job, "save_job_plan", saved.append)
    monkeypatch.setattr(task_veto, "veto_unreachable", lambda tasks, vetoed: ("t3",))
    tasks = [SimpleNamespace(task_id=tid, status=status, error="e" if status == "blocked" else "")
             for tid, status in (("t1", "vetoed"), ("t2", "blocked"), ("t3", "skipped"), ("t4", "skipped"))]
    job = SimpleNamespace(state=RunState.BLOCKED, tasks=tasks, error="e", finished_at="then")

    assert retry_blocked_job_tasks(job) == ("t2", "t4")
    assert [t.status for t in tasks] == ["vetoed", "pending", "skipped", "pending"]
    assert saved == [job]


def test_a_job_that_is_not_blocked_is_left_as_it_is(data_root, repo):
    from packages.orchestration.data_paths import job_record_path
    from packages.orchestration.pingpong_job import parse_job_file, run_job

    job = parse_job_file(_ONE, str(repo))
    done = run_job(job.job_id, builder_provider=_fake(), reviewer_provider=_fake(), repair_rounds=0)
    assert done.state == RunState.COMPLETED
    before = job_record_path(job.job_id).read_bytes()

    assert retry_blocked_job_tasks(_stored(job.job_id)) == ()
    assert job_record_path(job.job_id).read_bytes() == before


def _job_run(job_id: str, repo: Path, *options: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "job", "run", job_id, *options,
         "--builder-provider", "fake", "--reviewer-provider", "fake", "--repair-rounds", "2", "--json"],
        cwd=str(repo), capture_output=True, text=True, timeout=120,
        env={**os.environ, "PYTHONPATH": str(REPO)})


def test_remedy_job_run_retry_runs_the_task_a_plain_run_leaves_blocked(data_root, repo):
    job_id = _blocked(repo)

    plain = _job_run(job_id, repo)
    assert plain.returncode == 1, plain.stdout + plain.stderr
    assert json.loads(plain.stdout)["error"] == "job_blocked"

    retried = _job_run(job_id, repo, "--retry")
    assert retried.returncode == 0, retried.stdout + retried.stderr
    answer = json.loads(retried.stdout)
    assert (answer["ok"], answer["status"]) == (True, "completed")
    assert _stored(job_id).state == RunState.COMPLETED
