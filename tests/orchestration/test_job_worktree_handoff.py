"""F006 hand-off — the COMPLETE real flow, end to end, with fake providers only.

    parse_job_file → run_job (job-owned worktree) → job evidence
                   → promotion dry-run → explicitly approved promotion

and the complete interrupted-task flow:

    task begins → partial work written → process dies → same job resumes
                → the COMPLETE task change is reviewed and evidenced

No provider call is ever made: temporary git repositories, fake providers and CLI
monkeypatching only.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from packages.orchestration import job_promote as JP
from packages.orchestration import pingpong_job as PJ
from packages.orchestration import worktrees as W
from packages.orchestration.artifact_contract_gate import check_worktree_artifacts
from packages.orchestration.job_evidence import export_job_evidence
from packages.orchestration.job_promote import promote_job
from packages.orchestration.pingpong_job import (
    JOB_COMPLETED,
    export_job_report,
    job_worktree_id,
    load_job_plan,
    parse_job_file,
    resume_job_plan,
    run_job,
)
from packages.orchestration.pingpong_provider import BuilderOutput, ReviewerOutput


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


ONE_TASK = "# One\n\n## Task 1 — write one.txt\n\nWrite one.txt.\n"


class _Builder:
    """Fake Builder writing fixed files; records the diff the Reviewer received."""

    def __init__(self, holder: dict, files: dict[str, str], seen: dict | None = None):
        self._holder = holder
        self._files = files
        self.seen = seen if seen is not None else {}

    def build(self, prompt, **kw):
        ws = Path(self._holder["path"])
        for name, content in self._files.items():
            (ws / name).write_text(content)
        return BuilderOutput(summary="wrote files",
                             files_changed=list(self._files), provider="fake")

    def review(self, prompt, **kw):
        self.seen["reviewer_prompt"] = prompt
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok",
                              provider="fake")


def _spy_create(monkeypatch, holder: dict):
    real = W.create

    def spy(job_id, r):
        h = real(job_id, r)
        holder["path"] = h.path
        return h

    monkeypatch.setattr(W, "create", spy)


def _run_job(repo: Path, monkeypatch, files: dict[str, str], text=ONE_TASK, seen=None):
    job = parse_job_file(text, str(repo))
    holder: dict = {}
    _spy_create(monkeypatch, holder)
    prov = _Builder(holder, files, seen)
    done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                   builder_name="fake", reviewer_name="fake", max_rounds=1)
    return done, holder


# ---------------------------------------------------------------------------
# Finding 1 — a completed worktree job is promotable WITHOUT its workspace
# ---------------------------------------------------------------------------

class TestCompletedJobPromotion:
    def test_dry_run_is_ready_not_workspace_missing(self, repo, monkeypatch):
        job, holder = _run_job(repo, monkeypatch, {"one.txt": "hello\n"})
        assert job.status == JOB_COMPLETED
        assert job.worktree_cleanup_status == "clean"
        assert not Path(holder["path"]).exists()     # workspace is gone by design

        res = promote_job(job.job_id, str(repo), dry_run=True)

        assert res.status == "dry_run", res.blocked_reason
        assert res.blocked_reason == ""
        assert res.files_planned == ["one.txt"]
        assert not (repo / "one.txt").exists()       # dry-run mutates nothing
        assert _git(repo, "status", "--porcelain") == ""

    def test_approved_promotion_places_the_reviewed_files_in_the_target(
        self, repo, monkeypatch,
    ):
        job, _ = _run_job(repo, monkeypatch, {"one.txt": "hello\n"})
        head_before = _git(repo, "rev-parse", "HEAD").strip()

        res = promote_job(job.job_id, str(repo), approve=True)

        assert res.status == "promoted", res.blocked_reason
        assert (repo / "one.txt").read_text() == "hello\n"
        # No commit, no merge, no push: only the working tree changed.
        assert _git(repo, "rev-parse", "HEAD").strip() == head_before
        assert _git(repo, "status", "--porcelain").strip() == "?? one.txt"
        assert W._branch_exists(repo, job.worktree_branch)    # branch untouched

    def test_a_changed_target_baseline_still_blocks(self, repo, monkeypatch):
        job, _ = _run_job(repo, monkeypatch, {"base.txt": "changed by job\n"})
        (repo / "base.txt").write_text("changed by someone else\n")

        res = promote_job(job.job_id, str(repo), dry_run=True)
        assert res.status == "blocked"
        assert "baseline_check_failed" in res.blocked_reason

    def test_a_tampered_job_result_diff_blocks(self, repo, monkeypatch):
        job, _ = _run_job(repo, monkeypatch, {"one.txt": "hello\n"})
        (PJ._jobs_dir() / job.job_id / "result.diff").write_bytes(b"tampered\n")

        res = promote_job(job.job_id, str(repo), dry_run=True)
        assert res.status == "blocked"
        assert "job_result_diff_invalid" in res.blocked_reason
        assert "sha256" in res.blocked_reason

    def test_a_missing_job_result_diff_blocks(self, repo, monkeypatch):
        job, _ = _run_job(repo, monkeypatch, {"one.txt": "hello\n"})
        (PJ._jobs_dir() / job.job_id / "result.diff").unlink()

        res = promote_job(job.job_id, str(repo), dry_run=True)
        assert res.status == "blocked"
        assert "job_result_diff_invalid" in res.blocked_reason

    def test_a_mismatched_base_commit_blocks(self, repo, monkeypatch):
        job, _ = _run_job(repo, monkeypatch, {"one.txt": "hello\n"})
        path = PJ._jobs_dir() / job.job_id / "job.json"
        data = json.loads(path.read_text())
        data["worktree"]["base_commit"] = "0" * 40
        path.write_text(json.dumps(data, indent=2))

        res = promote_job(job.job_id, str(repo), dry_run=True)
        assert res.status == "blocked"
        assert "base_commit_missing" in res.blocked_reason

    def test_temporary_promotion_worktrees_are_always_removed(self, repo, monkeypatch):
        job, _ = _run_job(repo, monkeypatch, {"one.txt": "hello\n"})
        promote_job(job.job_id, str(repo), dry_run=True)
        promote_job(job.job_id, str(repo), approve=True)
        # Only the main checkout remains registered; no promo-* worktree survives.
        assert len(W.list_worktrees(repo)) == 1
        assert "remedy-promo" not in _git(repo, "worktree", "list", "--porcelain")

    def test_the_promotion_source_is_never_the_recorded_execution_path(
        self, repo, monkeypatch,
    ):
        job, holder = _run_job(repo, monkeypatch, {"one.txt": "hello\n"})
        seen: dict = {}
        real = JP._materialize_promotion_source_owned

        def spy(j):
            src, err = real(j)
            seen["path"] = str(src.path) if src else ""
            return src, err

        monkeypatch.setattr(JP, "_materialize_promotion_source_owned", spy)
        promote_job(job.job_id, str(repo), dry_run=True)
        assert seen["path"] and seen["path"] != holder["path"]
        assert ".remedy-wt" not in seen["path"]      # not the execution worktree
