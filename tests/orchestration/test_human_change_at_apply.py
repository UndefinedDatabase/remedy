"""F263 T003 — `job apply` absorbs a hand edit before a single file is copied.

The second demo case of T2_F263.md (DECISION amend0921-operator-feedback D4): the user edits
the repository by hand between the run's end and `job apply`, and the apply absorbs the edit
and neither overwrites nor discards it. A hand edit to a file the job changed too stops the
apply and says why (DECISION D-E).

Temporary git repositories and fake providers only. No provider call is ever made.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from packages.orchestration import human_change as HC
from packages.orchestration import worktrees as W
from packages.orchestration.data_paths import job_evidence_dir
from packages.orchestration.job_apply import apply_job
from packages.orchestration.pingpong_job import JOB_COMPLETED, parse_job_file, run_job
from packages.orchestration.pingpong_provider import BuilderOutput, ReviewerOutput

ONE_TASK = "# One\n\n## Task 1 — write\n\nWrite one.txt.\n"


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True).stdout


@pytest.fixture
def repo(tmp_path) -> Path:
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q")
    _git(r, "config", "user.email", "t@e.com")
    _git(r, "config", "user.name", "T")
    _git(r, "config", "commit.gpgsign", "false")
    (r / "base.txt").write_text("base\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "init")
    return r


class _Builder:
    """Fake builder: writes one.txt into the job worktree; may also edit the main checkout."""

    def __init__(self, holder: dict, repo: Path, during_run: dict[str, str]):
        self._holder, self._repo, self._during_run = holder, repo, during_run

    def build(self, prompt, **kw):
        (Path(self._holder["path"]) / "one.txt").write_text("one.txt by the job\n")
        for rel, text in self._during_run.items():
            (self._repo / rel).write_text(text)
        return BuilderOutput(summary="wrote", files_changed=["one.txt"], provider="fake")

    def review(self, prompt, **kw):
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok", provider="fake")


def _completed_job(repo, monkeypatch, during_run=None):
    job = parse_job_file(ONE_TASK, str(repo))
    holder: dict = {}
    real = W.create

    def create(job_id, r):
        h = real(job_id, r)
        holder["path"] = h.path
        return h

    monkeypatch.setattr(W, "create", create)
    prov = _Builder(holder, repo, during_run or {})
    done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                   builder_name="fake", reviewer_name="fake", max_rounds=1)
    assert done.state == JOB_COMPLETED, done.error
    return done


def _records(job_id: str) -> list[dict]:
    folder = job_evidence_dir(job_id) / HC.RECORD_DIRNAME
    return [json.loads(p.read_text()) for p in sorted(folder.glob("hcr-*.json"))]


class TestTheSecondDemoCase:
    def test_a_hand_edit_after_the_run_is_absorbed_and_kept_by_the_apply(
            self, repo, monkeypatch):
        job = _completed_job(repo, monkeypatch)
        (repo / "base.txt").write_text("edited by hand after the run\n")
        result = apply_job(job.job_id, str(repo), approve=True)
        assert result.status == "applied", result.blocked_reason
        assert (repo / "base.txt").read_text() == "edited by hand after the run\n"
        assert (repo / "one.txt").read_text() == "one.txt by the job\n"
        [record] = _records(job.job_id)
        assert record["detected_by"] == "apply"
        assert [f["path"] for f in record["files"]] == ["base.txt"]

    def test_an_apply_with_no_hand_edit_writes_no_record(self, repo, monkeypatch):
        job = _completed_job(repo, monkeypatch)
        result = apply_job(job.job_id, str(repo), approve=True)
        assert result.status == "applied", result.blocked_reason
        assert _records(job.job_id) == []


class TestAHandEditTheJobMeetsStopsTheApply:
    def test_after_the_run_it_is_refused_and_named(self, repo, monkeypatch):
        job = _completed_job(repo, monkeypatch)
        (repo / "one.txt").write_text("the human's own one.txt\n")
        result = apply_job(job.job_id, str(repo), approve=True)
        assert result.status == "blocked"
        assert result.blocked_reason.startswith("baseline_check_failed: ")
        assert "; human_change_conflict: one.txt changed by hand " in result.blocked_reason
        assert (repo / "one.txt").read_text() == "the human's own one.txt\n"
        assert [f["path"] for f in _records(job.job_id)[0]["files"]] == ["one.txt"]

    def test_during_the_run_it_is_refused_and_named_too(self, repo, monkeypatch):
        job = _completed_job(repo, monkeypatch, {"one.txt": "the human's own one.txt\n"})
        result = apply_job(job.job_id, str(repo), approve=True)
        assert result.status == "blocked"
        assert result.blocked_reason.startswith("baseline_check_failed: ")
        assert "; human_change_conflict: one.txt changed by hand " in result.blocked_reason
        assert (repo / "one.txt").read_text() == "the human's own one.txt\n"


class TestAFailedAbsorptionStopsTheApply:
    def test_the_apply_is_refused_with_the_reason_and_copies_nothing(self, repo, monkeypatch):
        job = _completed_job(repo, monkeypatch)

        def unreadable(path):
            raise HC.HumanChangeError("the target cannot be read")

        monkeypatch.setattr(HC, "capture_target_state", unreadable)
        result = apply_job(job.job_id, str(repo), approve=True)
        assert result.status == "blocked"
        assert result.blocked_reason == "human_change_absorb_failed: the target cannot be read"
        assert not (repo / "one.txt").exists()


class TestTheRecordedPaths:
    def test_a_record_that_does_not_verify_names_nothing(self, repo, tmp_path):
        state = HC.capture_target_state(repo)
        (repo / "base.txt").write_text("edited\n")
        change = HC.detect_human_change(repo, state)
        record = HC.write_human_change_record("job-1", repo, change, detected_by="test")
        assert HC.recorded_human_changes("job-1") == frozenset({"base.txt"})
        body = json.loads(record.read_text())
        body["detected_by"] = "someone else"
        record.write_text(json.dumps(body))
        assert HC.recorded_human_changes("job-1") == frozenset()
        assert HC.recorded_human_changes("job-without-records") == frozenset()
