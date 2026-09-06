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
from packages.orchestration.data_paths import job_dir
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
        (job_dir(job.job_id) / "result.diff").write_bytes(b"tampered\n")

        res = promote_job(job.job_id, str(repo), dry_run=True)
        assert res.status == "blocked"
        assert "job_result_diff_invalid" in res.blocked_reason
        assert "sha256" in res.blocked_reason

    def test_a_missing_job_result_diff_blocks(self, repo, monkeypatch):
        job, _ = _run_job(repo, monkeypatch, {"one.txt": "hello\n"})
        (job_dir(job.job_id) / "result.diff").unlink()

        res = promote_job(job.job_id, str(repo), dry_run=True)
        assert res.status == "blocked"
        assert "job_result_diff_invalid" in res.blocked_reason

    def test_a_mismatched_base_commit_blocks(self, repo, monkeypatch):
        job, _ = _run_job(repo, monkeypatch, {"one.txt": "hello\n"})
        path = job_dir(job.job_id) / "job.json"
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


# ---------------------------------------------------------------------------
# Finding 2 — the root JobPlan hand-off is exported and verified
# ---------------------------------------------------------------------------

class TestRootJobEvidence:
    def _export(self, job, tmp_path):
        out = tmp_path / "ev"
        export_job_evidence(job.job_id, str(out))
        return out

    def test_root_worktree_json_and_result_diff_are_exported(
        self, repo, monkeypatch, tmp_path,
    ):
        job, _ = _run_job(repo, monkeypatch, {"one.txt": "hello\n"})
        out = self._export(job, tmp_path)

        doc = json.loads((out / "worktree.json").read_text())
        assert doc["isolation_mode"] == "worktree"
        assert doc["branch"] == f"remedy/{job_worktree_id(job.job_id)}"
        assert doc["path"] == f".remedy-wt/{job_worktree_id(job.job_id)}"
        assert doc["base_commit"] and doc["head"]
        assert doc["cleanup_status"] == "clean"
        assert doc["auto_merged"] is False
        assert doc["result_diff"]["sha256"] == job.result_diff_sha256
        assert doc["result_diff"]["size_bytes"] == job.result_diff_size_bytes
        assert "one.txt" in (out / "result.diff").read_text()

    def test_workspace_diff_no_longer_claims_a_missing_workspace(
        self, repo, monkeypatch, tmp_path,
    ):
        job, _ = _run_job(repo, monkeypatch, {"one.txt": "hello\n"})
        out = self._export(job, tmp_path)
        ws = (out / "workspace.diff").read_text()
        assert "unavailable" not in ws
        assert "one.txt" in ws
        assert job.result_diff_sha256 in ws

    def test_the_root_handoff_passes_the_artifact_contract(
        self, repo, monkeypatch, tmp_path,
    ):
        job, _ = _run_job(repo, monkeypatch, {"one.txt": "hello\n"})
        out = self._export(job, tmp_path)
        check = check_worktree_artifacts(str(out))
        assert check["verdict"] == "PASS"
        assert check["job_level_handoff"] is True
        assert check["diffs_verified"] >= 2          # root + task

    def test_one_byte_root_tamper_blocks(self, repo, monkeypatch, tmp_path):
        job, _ = _run_job(repo, monkeypatch, {"one.txt": "hello\n"})
        out = self._export(job, tmp_path)
        data = bytearray((out / "result.diff").read_bytes())
        data[-1] ^= 0x01
        (out / "result.diff").write_bytes(bytes(data))

        check = check_worktree_artifacts(str(out))
        assert check["verdict"] == "BLOCKED"
        assert check["result_diff_hash_mismatches"]

    def test_missing_root_diff_blocks_even_when_task_diffs_are_valid(
        self, repo, monkeypatch, tmp_path,
    ):
        job, _ = _run_job(repo, monkeypatch, {"one.txt": "hello\n"})
        out = self._export(job, tmp_path)
        (out / "result.diff").unlink()

        check = check_worktree_artifacts(str(out))
        assert check["verdict"] == "BLOCKED"
        assert check["missing_result_diffs"] == ["result.diff"]

    def test_no_root_worktree_json_blocks_a_worktree_job(self, repo, monkeypatch, tmp_path):
        job, _ = _run_job(repo, monkeypatch, {"one.txt": "hello\n"})
        out = self._export(job, tmp_path)
        (out / "worktree.json").unlink()

        check = check_worktree_artifacts(str(out))
        assert check["verdict"] == "BLOCKED"
        assert check["missing_job_handoff"] == ["worktree.json"]

    def test_an_unsafe_or_symlinked_root_source_is_never_copied(
        self, repo, monkeypatch, tmp_path,
    ):
        job, _ = _run_job(repo, monkeypatch, {"one.txt": "hello\n"})
        job_root = job_dir(job.job_id)
        secret = tmp_path / "secret"
        secret.write_bytes(b"TOPSECRET\n")
        (job_root / "result.diff").unlink()
        (job_root / "result.diff").symlink_to(secret)

        out = self._export(load_job_plan(job.job_id), tmp_path)  # reloaded job
        assert not (out / "result.diff").exists()
        doc = json.loads((out / "worktree.json").read_text())
        assert doc["result_diff"] is None
        assert "symlink" in doc["result_diff_error"]
        assert b"TOPSECRET" not in (out / "workspace.diff").read_bytes()

    def test_copy_mode_job_needs_no_worktree_diff(self, tmp_path, monkeypatch):
        plain = tmp_path / "plain"
        plain.mkdir()
        (plain / "base.txt").write_text("base\n")
        job = parse_job_file(ONE_TASK, str(plain))

        class _P:
            def build(self, prompt, **kw):
                return BuilderOutput(summary="noop", files_changed=[], provider="fake")

            def review(self, prompt, **kw):
                return ReviewerOutput(verdict="pass", confidence="high",
                                      summary="ok", provider="fake")

        prov = _P()
        done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                       builder_name="fake", reviewer_name="fake", max_rounds=1)
        assert done.isolation_mode == "copy"
        out = tmp_path / "ev"
        export_job_evidence(done.job_id, str(out))
        assert not (out / "worktree.json").exists()
        check = check_worktree_artifacts(str(out))
        assert check["verdict"] == "NOT_APPLICABLE"


# ---------------------------------------------------------------------------
# Findings 3 + 4 — real JobPlan resume and the durable task-start tree
# ---------------------------------------------------------------------------

class TestJobPlanResumeAfterCrash:
    def _crashed_job(self, repo, monkeypatch, partial="partial work\n"):
        """A job whose task 1 wrote partial.txt and then 'died' before review."""
        job = parse_job_file(ONE_TASK, str(repo))
        wt_id = job_worktree_id(job.job_id)

        handle = W.create(wt_id, repo)                 # the runner's worktree
        job.job_workspace_path = handle.path
        job.isolation_mode = "worktree"
        job.worktree_branch = handle.branch
        job.worktree_path = handle.relative_path
        job.worktree_base_commit = handle.base_commit
        job.worktree_head = handle.head_commit
        job.worktree_cleanup_status = "active"
        job.job_initial_tree = W.write_tree(handle)
        job.job_initial_tree_ref = W.checkpoint_ref(wt_id, "job-initial")
        W.set_checkpoint_ref(repo, job.job_initial_tree_ref, job.job_initial_tree)
        job.status = PJ.JOB_RUNNING

        task = job.tasks[0]
        task.status = PJ.TASK_RUNNING
        task.task_start_tree = W.write_tree(handle)    # BEFORE any provider call
        task.task_start_tree_ref = W.checkpoint_ref(wt_id, "start", task.task_id)
        W.set_checkpoint_ref(repo, task.task_start_tree_ref, task.task_start_tree)
        task.task_attempt_state = "active"
        PJ._persist_job(job)

        (Path(handle.path) / "partial.txt").write_text(partial)   # partial work
        W.release_lock(handle)                                    # the process dies
        return job, handle

    def test_resume_uses_the_16_char_jobplan_id_and_the_same_worktree(
        self, repo, monkeypatch,
    ):
        job, handle = self._crashed_job(repo, monkeypatch)
        assert len(job.job_id) == 16                  # a JobPlan id, not a UUID

        holder = {"path": handle.path}
        prov = _Builder(holder, {"finished.txt": "done\n"})
        done = resume_job_plan(job.job_id, builder_provider=prov,
                               reviewer_provider=prov, builder_name="fake",
                               reviewer_name="fake", max_rounds=1)

        assert done.status == JOB_COMPLETED
        assert done.worktree_branch == job.worktree_branch     # same branch
        assert done.worktree_path == job.worktree_path         # same path
        branches = _git(repo, "branch", "--format=%(refname:short)").split()
        assert [b for b in branches if b.startswith("remedy/")] == [job.worktree_branch]

    def test_the_pre_crash_file_stays_inside_the_task_diff_and_review(
        self, repo, monkeypatch,
    ):
        from packages.orchestration.data_paths import run_dir

        job, handle = self._crashed_job(repo, monkeypatch)
        holder = {"path": handle.path}
        seen: dict = {}
        prov = _Builder(holder, {"finished.txt": "done\n"}, seen)

        done = resume_job_plan(job.job_id, builder_provider=prov,
                               reviewer_provider=prov, builder_name="fake",
                               reviewer_name="fake", max_rounds=1)
        task = done.tasks[0]

        # The Reviewer saw BOTH files — the pre-crash one is not invisible.
        assert "partial.txt" in seen["reviewer_prompt"]
        assert "finished.txt" in seen["reviewer_prompt"]
        # Task-local diff, safe-diff file list and apply manifest all carry both.
        task_diff = (run_dir(task.run_id) / "result.diff").read_text()
        assert "partial.txt" in task_diff and "finished.txt" in task_diff
        assert sorted(task.safe_diff_files) == ["finished.txt", "partial.txt"]
        assert sorted(task.apply_manifest.applied_files) == ["finished.txt", "partial.txt"]
        # And so does the final job hand-off: nothing entered it unreviewed.
        job_diff = (job_dir(done.job_id) / "result.diff").read_text()
        assert "partial.txt" in job_diff and "finished.txt" in job_diff

    def test_the_original_task_start_tree_is_reused_not_replaced(
        self, repo, monkeypatch,
    ):
        job, handle = self._crashed_job(repo, monkeypatch)
        original_tree = load_job_plan(job.job_id).tasks[0].task_start_tree

        holder = {"path": handle.path}
        prov = _Builder(holder, {"finished.txt": "done\n"})
        done = resume_job_plan(job.job_id, builder_provider=prov,
                               reviewer_provider=prov, builder_name="fake",
                               reviewer_name="fake", max_rounds=1)

        task = done.tasks[0]
        assert task.task_start_tree == original_tree   # never re-snapshotted
        assert task.task_attempt_state == "complete"

    def test_a_crash_before_any_change_still_resumes_cleanly(self, repo, monkeypatch):
        job, handle = self._crashed_job(repo, monkeypatch, partial="")
        (Path(handle.path) / "partial.txt").unlink()   # nothing was written

        holder = {"path": handle.path}
        prov = _Builder(holder, {"finished.txt": "done\n"})
        done = resume_job_plan(job.job_id, builder_provider=prov,
                               reviewer_provider=prov, builder_name="fake",
                               reviewer_name="fake", max_rounds=1)
        assert done.status == JOB_COMPLETED
        assert done.tasks[0].safe_diff_files == ["finished.txt"]

    def test_a_second_crash_during_the_resumed_attempt_is_still_recoverable(
        self, repo, monkeypatch,
    ):
        job, handle = self._crashed_job(repo, monkeypatch)

        # The resumed attempt dies too: another partial file, no cleanup.
        rec = W.recover(job_worktree_id(job.job_id), repo)
        (Path(rec.path) / "partial2.txt").write_text("second partial\n")
        W.release_lock(rec)

        holder = {"path": handle.path}
        prov = _Builder(holder, {"finished.txt": "done\n"})
        done = resume_job_plan(job.job_id, builder_provider=prov,
                               reviewer_provider=prov, builder_name="fake",
                               reviewer_name="fake", max_rounds=1)

        task = done.tasks[0]
        assert done.status == JOB_COMPLETED
        assert sorted(task.safe_diff_files) == [
            "finished.txt", "partial.txt", "partial2.txt",
        ]                                       # every crash artifact was reviewed

    def test_a_completed_clean_job_is_not_rematerialized_by_resume(
        self, repo, monkeypatch,
    ):
        job, holder = _run_job(repo, monkeypatch, {"one.txt": "hello\n"})
        again = resume_job_plan(job.job_id)
        assert again.status == JOB_COMPLETED
        assert again.worktree_cleanup_status == "clean"
        assert not Path(holder["path"]).exists()     # no worktree recreated
        assert len(W.list_worktrees(repo)) == 1


class TestJobPlanResumeCli:
    def test_the_cli_resumes_a_16_char_jobplan_id(self, repo, monkeypatch, capsys):
        from apps.cli.commands import do_cmd

        job = parse_job_file(ONE_TASK, str(repo))
        # A fake-provider run through the REAL CLI command: `fake` is Remedy's
        # built-in fake provider, so no provider call leaves the process.
        # max-tasks is an F012 material control and travels in RunInvocation,
        # not as a bare kwarg (do_cmd._cmd_do_job_run docstring).
        from apps.cli.commands.run_invocation import RunInvocation
        do_cmd._cmd_do_job_run(job.job_id, builder="fake", reviewer="fake",
                               max_rounds=1, json_output=True,
                               invocation=RunInvocation(max_tasks=1))
        capsys.readouterr()

        do_cmd._cmd_do_job_resume(job.job_id, builder="fake", reviewer="fake",
                                  max_rounds=1, json_output=True)
        out = json.loads(capsys.readouterr().out)
        assert out["job_id"] == job.job_id
        assert out["isolation_mode"] == "worktree"
        assert out["worktree"]["branch"] == f"remedy/{job_worktree_id(job.job_id)}"

    def test_the_cli_refuses_an_unknown_jobplan_id(self, capsys):
        from apps.cli.commands import do_cmd
        with pytest.raises(SystemExit):
            do_cmd._cmd_do_job_resume("deadbeefdeadbeef", json_output=True)
        assert "job_not_found" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# Finding 5/6 — the whole flow, and the report of a disposable workspace
# ---------------------------------------------------------------------------

class TestEndToEndJobFlow:
    def test_plan_run_report_evidence_promote_dry_run(self, repo, monkeypatch, tmp_path):
        status_before = _git(repo, "status", "--porcelain")
        head_before = _git(repo, "rev-parse", "HEAD").strip()

        job, _ = _run_job(repo, monkeypatch, {"one.txt": "hello\n"})
        assert job.status == JOB_COMPLETED
        assert job.isolation_mode == "worktree"       # a copy here is a FAILURE

        report = export_job_report(job)
        assert report["isolation_mode"] == "worktree"
        assert report["handoff_available"] is True
        assert report["has_workspace_changes"] is True
        assert report["worktree"]["workspace_expected_present"] is False
        assert report["result_diff"]["sha256"] == job.result_diff_sha256
        assert "job-promote" in report["next_command"]

        out = tmp_path / "ev"
        export_job_evidence(job.job_id, str(out))
        assert "unavailable" not in (out / "workspace.diff").read_text()
        assert check_worktree_artifacts(str(out))["verdict"] == "PASS"

        dry = promote_job(job.job_id, str(repo), dry_run=True)
        assert dry.status == "dry_run" and dry.files_planned == ["one.txt"]

        # Nothing was promoted automatically; the checkout is byte-identical.
        assert _git(repo, "status", "--porcelain") == status_before == ""
        assert _git(repo, "rev-parse", "HEAD").strip() == head_before
        assert not (repo / "one.txt").exists()

    def test_the_explicit_approval_step_is_separate(self, repo, monkeypatch):
        job, _ = _run_job(repo, monkeypatch, {"one.txt": "hello\n"})
        promote_job(job.job_id, str(repo), dry_run=True)
        assert not (repo / "one.txt").exists()        # still nothing

        res = promote_job(job.job_id, str(repo), approve=True)
        assert res.status == "promoted"
        assert (repo / "one.txt").read_text() == "hello\n"
        assert _git(repo, "rev-parse", "HEAD").strip() == _git(
            repo, "rev-parse", job.worktree_base_commit).strip()   # no commit
