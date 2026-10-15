"""amend1015c D5 — one job's change from git, `job_client_diff`, read from real fake-provider runs.

Operator order amend1015-final-closure, E3: every answer here comes from a job the real runner
ran with fake providers in a temporary repository, and every patch is compared with what git
itself prints for the same commits.
"""
from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest

from packages.orchestration import client_diff
from packages.orchestration.client_diff import ClientDiffRefusal, job_client_diff

_JOB = "# Job: diff\n\n## Task 1\nDo a thing.\n\nAcceptance:\n- done\n"
_NOW = datetime(2026, 10, 15, 12, 0, tzinfo=timezone.utc)


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


def _run(repo: Path, *, builder_error: str = "") -> str:
    from packages.orchestration.pingpong_job import parse_job_file, run_job
    from packages.orchestration.pingpong_provider import FakeProvider

    job = parse_job_file(_JOB, str(repo))
    builder = FakeProvider(builder_error=builder_error) if builder_error else FakeProvider()
    run_job(job.job_id, builder_provider=builder, reviewer_provider=FakeProvider(), repair_rounds=2)
    return job.job_id


def _plan(job_id: str):
    from packages.orchestration.pingpong_job import load_job_plan_safe

    plan, _degraded = load_job_plan_safe(job_id)
    return plan


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          check=True).stdout


def _check_shape(answer: dict) -> None:
    assert set(answer) == {"job", "state", "files", "truncated"}
    assert answer["state"] in client_diff.DIFF_STATES
    for row in answer["files"]:
        assert set(row) == {"path", "change", "added", "removed", "patch", "truncated"}
        assert row["change"] in client_diff.DIFF_CHANGES
        assert isinstance(row["added"], int) and isinstance(row["removed"], int)


def test_a_prepared_result_is_the_job_branch_against_its_base(data_root, repo):
    job_id = _run(repo)
    plan = _plan(job_id)
    answer = job_client_diff(job_id, plan)
    _check_shape(answer)

    assert answer["state"] == "prepared" and answer["truncated"] is False
    assert len(answer["files"]) == 1
    row = answer["files"][0]
    expected = _git(repo, "diff", "--src-prefix=a/", "--dst-prefix=b/", plan.worktree_base_commit,
                    plan.worktree_head, "--", row["path"])
    assert row["patch"] == expected and row["truncated"] is False
    assert row["change"] == "added" and row["removed"] == 0
    assert row["added"] == sum(1 for line in expected.splitlines()
                               if line.startswith("+") and not line.startswith("+++"))
    # The target is untouched: the change lives on the job's branch only.
    assert _git(repo, "status", "--porcelain") == ""


def test_an_applied_result_is_the_commit_its_apply_landed(data_root, repo):
    from packages.orchestration.job_apply import apply_job

    job_id = _run(repo)
    prepared = job_client_diff(job_id, _plan(job_id))
    assert apply_job(job_id, str(repo), approve=True, commit_message="landed").status == "applied"
    answer = job_client_diff(job_id, _plan(job_id))
    _check_shape(answer)

    assert answer["state"] == "applied"
    head = _git(repo, "rev-parse", "HEAD").strip()
    assert _git(repo, "log", "-1", "--format=%s") == "landed\n"
    expected = _git(repo, "diff", "--src-prefix=a/", "--dst-prefix=b/", f"{head}^1", head)
    assert "".join(row["patch"] for row in answer["files"]) == expected
    assert [row["path"] for row in answer["files"]] == [row["path"] for row in prepared["files"]]


def test_a_plain_apply_reads_applied_with_the_job_branchs_change(data_root, repo):
    from packages.orchestration.job_apply import apply_job

    job_id = _run(repo)
    prepared = job_client_diff(job_id, _plan(job_id))
    assert apply_job(job_id, str(repo), approve=True).status == "applied"
    assert _git(repo, "log", "--format=%s") == "init\n"  # a plain apply commits nothing
    answer = job_client_diff(job_id, _plan(job_id))
    assert answer == {**prepared, "state": "applied"}


def test_a_declined_result_still_shows_its_change(data_root, repo):
    from packages.orchestration.job_apply import decline_job_result
    from packages.orchestration.pingpong_job import _persist_job

    job_id = _run(repo)
    plan = _plan(job_id)
    decline_job_result(plan, reason="no", source="test", now=_NOW)
    _persist_job(plan)
    answer = job_client_diff(job_id, _plan(job_id))
    _check_shape(answer)
    assert answer["state"] == "declined" and len(answer["files"]) == 1


def test_a_result_whose_apply_met_a_hand_change_reads_conflict(data_root, repo):
    from packages.orchestration.job_apply import apply_job

    job_id = _run(repo)
    [row] = job_client_diff(job_id, _plan(job_id))["files"]
    target = repo / row["path"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("written by hand\n")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "by hand"], check=True)
    assert apply_job(job_id, str(repo), approve=True).status != "applied"
    answer = job_client_diff(job_id, _plan(job_id))
    _check_shape(answer)
    assert answer["state"] == "conflict" and len(answer["files"]) == 1


def test_a_failed_job_reads_failed_with_no_change(data_root, repo):
    job_id = _run(repo, builder_error="provider_unavailable: down")
    answer = job_client_diff(job_id, _plan(job_id))
    _check_shape(answer)
    assert answer == {"job": job_id, "state": "failed", "files": [], "truncated": False}


def test_a_job_that_has_not_ended_is_refused(data_root, repo):
    from packages.orchestration.pingpong_job import parse_job_file

    job = parse_job_file(_JOB, str(repo))
    with pytest.raises(ClientDiffRefusal) as caught:
        job_client_diff(job.job_id, _plan(job.job_id))
    assert caught.value.token == "diff_not_ready"


def test_a_job_whose_commits_are_gone_is_refused_unavailable(data_root, repo):
    job_id = _run(repo)
    plan = _plan(job_id)
    plan.worktree_head = "0" * 40
    with pytest.raises(ClientDiffRefusal) as caught:
        job_client_diff(job_id, plan)
    assert caught.value.token == "diff_unavailable"


def test_patches_are_capped_per_file_and_in_total(data_root, repo, monkeypatch):
    job_id = _run(repo)
    monkeypatch.setattr(client_diff, "FILE_PATCH_LIMIT", 120)
    answer = job_client_diff(job_id, _plan(job_id))
    [row] = answer["files"]
    assert row["truncated"] is True and answer["truncated"] is True
    assert 0 < len(row["patch"].encode()) <= 120 and row["patch"].endswith("\n")
    monkeypatch.setattr(client_diff, "FILE_PATCH_LIMIT", 64 * 1024)
    monkeypatch.setattr(client_diff, "TOTAL_PATCH_LIMIT", 0)
    [row] = job_client_diff(job_id, _plan(job_id))["files"]
    assert row["patch"] == "" and row["truncated"] is True and row["added"] > 0


def test_a_sensitive_path_keeps_its_counts_but_never_its_patch(data_root, repo):
    base = _git(repo, "rev-parse", "HEAD").strip()
    (repo / ".env").write_text("TOKEN=secret-value\n")
    subprocess.run(["git", "-C", str(repo), "add", "-f", ".env"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "env"], check=True)
    head = _git(repo, "rev-parse", "HEAD").strip()
    row = client_diff._file_row(str(repo), base, head, ("added", ".env", ""), 10_000)
    assert row == {"path": ".env", "change": "added", "added": 1, "removed": 0, "patch": "",
                   "truncated": True}
