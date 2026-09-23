"""F263 T003 — a git job absorbs a hand edit at its safe points and keeps running.

The demo case of T2_F263.md: the user edits a file by hand while a job is running. The job
does not block on drift; the edit is certified as a human change record in the job's evidence,
the job's last known state moves onto it, and the file keeps the human's bytes.

Temporary git repositories and fake providers only. No provider call is ever made.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from packages.orchestration import human_change as HC
from packages.orchestration import pingpong_job as PJ
from packages.orchestration import worktrees as W
from packages.orchestration.data_paths import job_evidence_dir
from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_COMPLETED,
    load_job_plan,
    parse_job_file,
    run_job,
)
from packages.orchestration.pingpong_provider import BuilderOutput, ReviewerOutput

ONE_TASK = "# One\n\n## Task 1 — write\n\nWrite one.txt.\n"
TWO_TASKS = (
    "# Two\n\n## Task 1 — first\n\nWrite one.txt.\n\n"
    "## Task 2 — second\n\nWrite two.txt.\n"
)


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
    """Fake builder: writes the task's file into the job worktree; on its first call a human
    also edits the MAIN checkout, which is the demo case."""

    def __init__(self, holder: dict, repo: Path, hand_edit: dict[str, str]):
        self._holder = holder
        self._repo = repo
        self._hand_edit = hand_edit
        self.calls = 0

    def build(self, prompt, **kw):
        name = "one.txt" if self.calls == 0 else "two.txt"
        (Path(self._holder["path"]) / name).write_text(f"{name} by the job\n")
        if self.calls == 0:
            for rel, text in self._hand_edit.items():
                (self._repo / rel).write_text(text)
        self.calls += 1
        return BuilderOutput(summary="wrote", files_changed=[name], provider="fake")

    def review(self, prompt, **kw):
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok", provider="fake")


def _run(repo, monkeypatch, text, hand_edit):
    job = parse_job_file(text, str(repo))
    holder: dict = {}
    real = W.create

    def create(job_id, r):
        h = real(job_id, r)
        holder["path"] = h.path
        return h

    monkeypatch.setattr(W, "create", create)
    prov = _Builder(holder, repo, hand_edit)
    return run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                   builder_name="fake", reviewer_name="fake", max_rounds=1)


def _records(job_id: str) -> list[dict]:
    folder = job_evidence_dir(job_id) / HC.RECORD_DIRNAME
    return [json.loads(p.read_text()) for p in sorted(folder.glob("hcr-*.json"))]


class TestTheDemoCase:
    def test_a_hand_edit_during_a_job_is_absorbed_and_the_job_completes(self, repo, monkeypatch):
        done = _run(repo, monkeypatch, TWO_TASKS, {"base.txt": "edited by hand\n"})
        assert done.state == JOB_COMPLETED, done.error
        assert (repo / "base.txt").read_text() == "edited by hand\n"
        [record] = _records(done.job_id)
        assert [f["path"] for f in record["files"]] == ["base.txt"]
        assert record["detected_by"].startswith("run:")
        folder = job_evidence_dir(done.job_id) / HC.RECORD_DIRNAME
        assert HC.verify_human_change_record(folder / f"{record['record_id']}.json") == []
        reloaded = load_job_plan(done.job_id)
        assert reloaded.target_last_known["tree"] == HC.capture_target_state(repo).tree

    def test_a_hand_edit_to_the_file_the_job_writes_is_kept_and_certified(
            self, repo, monkeypatch):
        done = _run(repo, monkeypatch, ONE_TASK, {"one.txt": "the human's own one.txt\n"})
        assert done.state == JOB_COMPLETED, done.error
        assert (repo / "one.txt").read_text() == "the human's own one.txt\n"
        [record] = _records(done.job_id)
        assert record["files"] == [{"path": "one.txt", "status": "A"}]

    def test_a_job_without_a_hand_edit_writes_no_record(self, repo, monkeypatch):
        done = _run(repo, monkeypatch, ONE_TASK, {})
        assert done.state == JOB_COMPLETED, done.error
        assert _records(done.job_id) == []


class TestEverySafePointChecks:
    def test_the_checks_are_counted_and_timed(self, repo, monkeypatch):
        done = _run(repo, monkeypatch, TWO_TASKS, {})
        checks = load_job_plan(done.job_id).metadata["human_change_checks"]
        # Two tasks: the episode start, and per task the point before it, the run's own safe
        # points, the point before its apply and the point after it.
        assert checks["count"] >= 1 + 2 * 3
        assert checks["total_seconds"] >= checks["max_seconds"] > 0


class TestAFailedAbsorptionStopsAndSaysWhy:
    def test_the_job_blocks_with_the_reason_and_the_edit_stays(self, repo, monkeypatch):
        real = HC.capture_target_state
        calls = {"n": 0}

        def failing(path):
            # The job's own last known state, the episode start and the point before the task
            # read the target; every read after them — inside the task's run — fails.
            calls["n"] += 1
            if calls["n"] > 3:
                raise HC.HumanChangeError("the target cannot be read")
            return real(path)

        monkeypatch.setattr(HC, "capture_target_state", failing)
        done = _run(repo, monkeypatch, ONE_TASK, {"base.txt": "edited by hand\n"})
        assert done.state == JOB_BLOCKED
        assert done.error.startswith("human_change_absorb_failed at run_safe_point: ")
        assert done.tasks[0].status == PJ.TASK_BLOCKED
        assert (repo / "base.txt").read_text() == "edited by hand\n"


class TestAJobFromBeforeF263:
    def test_a_resumed_job_without_a_last_known_state_gets_one(self, repo, monkeypatch):
        job = parse_job_file(ONE_TASK, str(repo))
        path, handle = PJ._acquire_job_workspace(job)
        W.release_lock(handle)
        job.target_last_known = None
        PJ.save_job_plan(job)
        holder = {"path": path}
        prov = _Builder(holder, repo, {})
        done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                       builder_name="fake", reviewer_name="fake", max_rounds=1)
        assert done.state == JOB_COMPLETED, done.error
        assert load_job_plan(done.job_id).target_last_known["tree"]
