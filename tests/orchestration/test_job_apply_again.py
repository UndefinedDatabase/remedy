"""amend1015 Phase 1.3 — a second apply of a job whose result landed answers `job_already_applied`.

A client that sends its apply again after a lost answer must read that its apply already landed,
not that someone changed the target (`target_changed_during_run`), which is what a second apply
answered before (DECISION amend1015f D16). A result the person reverted by hand still lands again.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

_JOB = "# Job: again\n\n## Task 1\nDo a thing.\n\nAcceptance:\n- done\n"


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


def _completed_job(repo: Path) -> str:
    from packages.orchestration.pingpong_job import parse_job_file, run_job
    from packages.orchestration.pingpong_provider import FakeProvider

    job = parse_job_file(_JOB, str(repo))
    run_job(job.job_id, builder_provider=FakeProvider(), reviewer_provider=FakeProvider(),
            repair_rounds=2)
    return job.job_id


def test_a_second_apply_of_a_landed_result_is_refused_as_already_applied(data_root, repo):
    from packages.orchestration.job_apply import APPLY_NOT_READY_TOKENS, apply_job, apply_refusal

    job_id = _completed_job(repo)
    first = apply_job(job_id, str(repo), approve=True)
    assert first.status == "applied" and apply_refusal(first) is None

    second = apply_job(job_id, str(repo), approve=True)
    token, sentence = apply_refusal(second)
    assert token == "job_already_applied"
    assert "already applied" in sentence and job_id in sentence
    assert token in APPLY_NOT_READY_TOKENS


def test_a_result_reverted_by_hand_lands_again(data_root, repo):
    from packages.orchestration.job_apply import apply_job, apply_refusal

    job_id = _completed_job(repo)
    first = apply_job(job_id, str(repo), approve=True)
    for path in first.files_applied:
        (repo / path).unlink()

    again = apply_job(job_id, str(repo), approve=True)
    assert again.status == "applied", again.blocked_reason
    assert apply_refusal(again) is None
