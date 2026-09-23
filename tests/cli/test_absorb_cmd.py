"""F263 T002 — `remedy absorb`: certify a hand edit and re-base this repository's jobs onto it.

Temporary git repositories only. No provider call is ever made.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from apps.cli.commands.absorb_cmd import _cmd_absorb
from apps.cli.grouped import main as grouped_main
from packages.core.models import RunState
from packages.orchestration import human_change as HC
from packages.orchestration import pingpong_job as PJ
from packages.orchestration import worktrees as W
from packages.orchestration.data_paths import job_evidence_dir

ONE_TASK = "# One\n\n## Task 1 — write\n\nWrite one.txt.\n"


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True).stdout


def _repo(path: Path) -> Path:
    path.mkdir()
    _git(path, "init", "-q")
    _git(path, "config", "user.email", "t@e.com")
    _git(path, "config", "user.name", "T")
    _git(path, "config", "commit.gpgsign", "false")
    (path / "edit.txt").write_text("before\n")
    _git(path, "add", "-A")
    _git(path, "commit", "-qm", "init")
    return path


@pytest.fixture
def repo(tmp_path) -> Path:
    return _repo(tmp_path / "repo")


def _job(repo: Path) -> PJ.JobPlan:
    """A git job with its workspace made and its lock released, persisted like a paused job."""
    job = PJ.parse_job_file(ONE_TASK, str(repo))
    _, handle = PJ._create_job_workspace(job)
    W.release_lock(handle)
    PJ.save_job_plan(job)
    return job


def _json(capsys) -> dict:
    return json.loads(capsys.readouterr().out)


class TestAbsorb:
    def test_a_hand_edit_is_certified_and_the_job_rebased_onto_it(self, repo, capsys):
        job = _job(repo)
        before = job.target_last_known["tree"]
        (repo / "edit.txt").write_text("after, by hand\n")
        _cmd_absorb(repo=str(repo), json_output=True)
        out = _json(capsys)
        assert out["ok"] is True
        [row] = out["jobs"]
        assert row["job_id"] == job.job_id and row["status"] == "absorbed"
        assert row["files"] == [{"path": "edit.txt", "status": "M"}]
        record = job_evidence_dir(job.job_id) / HC.RECORD_DIRNAME / row["record"]
        assert HC.verify_human_change_record(record) == []
        reloaded = PJ.load_job_plan(job.job_id)
        now = HC.capture_target_state(repo).tree
        assert reloaded.target_last_known["tree"] == now != before
        assert W.resolve_checkpoint_ref(repo, reloaded.target_last_known["ref"]) == now
        assert (repo / "edit.txt").read_text() == "after, by hand\n"

    def test_a_second_absorb_finds_nothing_new(self, repo, capsys):
        job = _job(repo)
        (repo / "edit.txt").write_text("after, by hand\n")
        _cmd_absorb(repo=str(repo), json_output=True)
        capsys.readouterr()
        _cmd_absorb(repo=str(repo), json_output=True)
        assert _json(capsys)["jobs"] == [
            {"job_id": job.job_id, "status": "unchanged", "record": None, "files": []}]

    def test_a_running_job_is_not_touched(self, repo, capsys):
        job = PJ.parse_job_file(ONE_TASK, str(repo))
        _, handle = PJ._create_job_workspace(job)
        PJ.save_job_plan(job)
        try:
            (repo / "edit.txt").write_text("after, by hand\n")
            _cmd_absorb(repo=str(repo), json_output=True)
            assert [r["status"] for r in _json(capsys)["jobs"]] == ["skipped_running"]
            assert not (job_evidence_dir(job.job_id) / HC.RECORD_DIRNAME).exists()
        finally:
            W.release_lock(handle)

    def test_a_job_of_another_repository_is_not_touched(self, repo, tmp_path, capsys):
        other = _job(_repo(tmp_path / "other"))
        _job(repo)
        (repo / "edit.txt").write_text("after, by hand\n")
        _cmd_absorb(repo=str(repo), json_output=True)
        assert other.job_id not in [r["job_id"] for r in _json(capsys)["jobs"]]

    def test_a_job_without_a_last_known_state_is_skipped(self, repo, capsys):
        job = _job(repo)
        job.target_last_known = None
        PJ.save_job_plan(job)
        _cmd_absorb(repo=str(repo), json_output=True)
        assert [r["status"] for r in _json(capsys)["jobs"]] == ["skipped_no_state"]

    def test_a_failed_or_cancelled_job_is_not_touched(self, repo, capsys):
        for state in (RunState.FAILED, RunState.CANCELLED):
            job = _job(repo)
            job.state = state
            PJ.save_job_plan(job)
        (repo / "edit.txt").write_text("after, by hand\n")
        _cmd_absorb(repo=str(repo), json_output=True)
        assert _json(capsys)["jobs"] == []

    def test_job_names_one_job_and_an_unknown_one_fails(self, repo, capsys):
        first, second = _job(repo), _job(repo)
        (repo / "edit.txt").write_text("after, by hand\n")
        _cmd_absorb(repo=str(repo), job_filter=first.job_id, json_output=True)
        assert [r["job_id"] for r in _json(capsys)["jobs"]] == [first.job_id]
        assert PJ.load_job_plan(second.job_id).target_last_known == second.target_last_known
        with pytest.raises(SystemExit) as exc:
            _cmd_absorb(repo=str(repo), job_filter="no-such-job", json_output=True)
        assert exc.value.code == 1

    def test_outside_a_git_repository_it_fails(self, tmp_path, capsys):
        with pytest.raises(SystemExit) as exc:
            _cmd_absorb(repo=str(tmp_path), json_output=True)
        assert exc.value.code == 1
        assert _json(capsys)["error"] == "not_a_git_repository"

    def test_the_plain_text_names_each_job(self, repo, capsys):
        job = _job(repo)
        (repo / "edit.txt").write_text("after, by hand\n")
        _cmd_absorb(repo=str(repo))
        assert f"job {job.job_id}: absorbed — 1 file(s)" in capsys.readouterr().out


class TestTheLockProbe:
    def test_a_held_lock_reads_held_and_a_released_one_does_not(self, repo):
        job = PJ.parse_job_file(ONE_TASK, str(repo))
        _, handle = PJ._create_job_workspace(job)
        wt_id = PJ.job_worktree_id(job.job_id)
        assert W.lock_is_held(repo, wt_id) is True
        W.release_lock(handle)
        assert W.lock_is_held(repo, wt_id) is False
        assert W.lock_is_held(repo, "job-never-claimed") is False


class TestTheCommandLine:
    def test_bare_absorb_runs_the_command(self, repo, monkeypatch, capsys):
        _job(repo)
        (repo / "edit.txt").write_text("after, by hand\n")
        monkeypatch.chdir(repo)
        assert grouped_main(["absorb", "--json"]) in (0, None)
        assert [r["status"] for r in _json(capsys)["jobs"]] == ["absorbed"]
