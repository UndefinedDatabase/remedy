"""F006 integrity — checkpoints survive GC, the hand-off is exactly the reviewed
work, promotion preserves file modes, and temporary cleanup never lies.

* Finding 1 — active tree checkpoints are protected by private Remedy refs.
* Finding 2 — the root diff must equal the union of the applied task manifests.
* Finding 3 — promotion reproduces the reviewed git file mode, not just the bytes.
* Finding 4 — temporary promotion cleanup is checked and reported honestly.

Temporary git repositories, fake providers and monkeypatching only. No provider
call is ever made.
"""
from __future__ import annotations

import json
import os
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
    JOB_BLOCKED,
    JOB_COMPLETED,
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


ONE_TASK = "# One\n\n## Task 1 — write\n\nWrite one.txt.\n"
TWO_TASKS = (
    "# Two\n\n## Task 1 — prior\n\nWrite prior.txt.\n\n"
    "## Task 2 — finish\n\nWrite finished.txt.\n"
)


class _Builder:
    """Fake Builder: writes the files for the current task; records review input."""

    def __init__(self, holder: dict, per_call: list[dict], seen: dict | None = None):
        self._holder = holder
        self._per_call = per_call
        self.calls = 0
        self.seen = seen if seen is not None else {}

    def build(self, prompt, **kw):
        ws = Path(self._holder["path"])
        files = self._per_call[min(self.calls, len(self._per_call) - 1)]
        self.calls += 1
        for name, content in files.items():
            (ws / name).write_text(content)
        return BuilderOutput(summary="wrote", files_changed=list(files), provider="fake")

    def review(self, prompt, **kw):
        self.seen["reviewer_prompt"] = prompt
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok",
                              provider="fake")


def _spy(monkeypatch, holder):
    real = W.create

    def create(job_id, r):
        h = real(job_id, r)
        holder["path"] = h.path
        return h

    monkeypatch.setattr(W, "create", create)


def _run(repo, monkeypatch, per_call, text=ONE_TASK, seen=None, **kw):
    job = parse_job_file(text, str(repo))
    holder: dict = {}
    _spy(monkeypatch, holder)
    prov = _Builder(holder, per_call, seen)
    done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                   builder_name="fake", reviewer_name="fake", max_rounds=1, **kw)
    return done, holder


# ---------------------------------------------------------------------------
# Finding 1 — checkpoint refs keep active trees alive through gc/prune
# ---------------------------------------------------------------------------

class TestCheckpointRefsSurviveGc:
    def _crashed_two_task_job(self, repo, monkeypatch):
        """Task 1 accepted prior.txt; task 2 started, wrote partial.txt, died."""
        job, holder = _run(repo, monkeypatch, [{"prior.txt": "prior\n"}],
                           text=TWO_TASKS, max_tasks=1)
        assert job.status == "paused"
        assert job.tasks[0].status == PJ.TASK_APPLIED

        handle = W.recover(job_worktree_id(job.job_id), repo)
        job = load_job_plan(job.job_id)
        task2 = job.tasks[1]
        task2.status = PJ.TASK_RUNNING
        task2.task_start_tree = W.write_tree(handle)          # uncommitted job state
        task2.task_start_tree_ref = W.checkpoint_ref(
            job_worktree_id(job.job_id), "start", task2.task_id)
        W.set_checkpoint_ref(repo, task2.task_start_tree_ref, task2.task_start_tree)
        task2.task_attempt_state = "active"
        job.status = PJ.JOB_RUNNING
        PJ._persist_job(job)

        (Path(handle.path) / "partial.txt").write_text("partial\n")
        W.release_lock(handle)                                # the process dies
        return job, handle

    def test_the_task_start_tree_survives_git_gc_prune(self, repo, monkeypatch):
        job, handle = self._crashed_two_task_job(repo, monkeypatch)
        tree = load_job_plan(job.job_id).tasks[1].task_start_tree

        _git(repo, "gc", "--prune=now", "--quiet")            # aggressive collection

        assert W.object_exists(repo, tree)                    # the ref kept it alive
        assert W.resolve_checkpoint_ref(
            repo, job.tasks[1].task_start_tree_ref) == tree

    def test_resume_after_gc_reviews_pre_crash_and_post_resume_files(
        self, repo, monkeypatch,
    ):
        from packages.orchestration.pingpong_loop import _pingpong_runs_dir

        job, handle = self._crashed_two_task_job(repo, monkeypatch)
        _git(repo, "gc", "--prune=now", "--quiet")

        holder = {"path": handle.path}
        seen: dict = {}
        prov = _Builder(holder, [{"finished.txt": "done\n"}], seen)
        done = resume_job_plan(job.job_id, builder_provider=prov,
                               reviewer_provider=prov, builder_name="fake",
                               reviewer_name="fake", max_rounds=1)

        assert done.status == JOB_COMPLETED
        t2 = done.tasks[1]
        assert "partial.txt" in seen["reviewer_prompt"]
        assert "finished.txt" in seen["reviewer_prompt"]
        diff = (_pingpong_runs_dir() / t2.run_id / "result.diff").read_text()
        assert "partial.txt" in diff and "finished.txt" in diff
        assert "prior.txt" not in diff              # task 1's work is not re-reported
        assert sorted(t2.safe_diff_files) == ["finished.txt", "partial.txt"]

    def test_a_deleted_checkpoint_ref_blocks_instead_of_re_snapshotting(
        self, repo, monkeypatch,
    ):
        job, handle = self._crashed_two_task_job(repo, monkeypatch)
        W.delete_checkpoint_ref(repo, job.tasks[1].task_start_tree_ref)

        holder = {"path": handle.path}
        prov = _Builder(holder, [{"finished.txt": "done\n"}])
        done = resume_job_plan(job.job_id, builder_provider=prov,
                               reviewer_provider=prov, builder_name="fake",
                               reviewer_name="fake", max_rounds=1)

        assert done.status == JOB_BLOCKED
        assert "checkpoint_ref_missing" in done.error
        # The work is kept, the lock is free, no hidden fresh baseline was taken.
        assert (Path(handle.path) / "partial.txt").read_text() == "partial\n"
        assert done.worktree_cleanup_status == "retained"
        rec = W.recover(job_worktree_id(job.job_id), repo)
        assert rec is not None
        W.release_lock(rec)

    def test_a_ref_pointing_at_the_wrong_tree_blocks(self, repo, monkeypatch):
        job, handle = self._crashed_two_task_job(repo, monkeypatch)
        rec = W.recover(job_worktree_id(job.job_id), repo)
        other_tree = W.write_tree(rec)                    # a DIFFERENT tree
        W.release_lock(rec)
        W.set_checkpoint_ref(repo, job.tasks[1].task_start_tree_ref, other_tree)

        holder = {"path": handle.path}
        prov = _Builder(holder, [{"finished.txt": "done\n"}])
        done = resume_job_plan(job.job_id, builder_provider=prov,
                               reviewer_provider=prov, builder_name="fake",
                               reviewer_name="fake", max_rounds=1)
        assert done.status == JOB_BLOCKED
        assert "checkpoint_ref_mismatch" in done.error

    def test_a_completed_job_drops_its_checkpoint_refs(self, repo, monkeypatch):
        job, _ = _run(repo, monkeypatch, [{"one.txt": "hello\n"}])
        assert job.status == JOB_COMPLETED and job.worktree_cleanup_status == "clean"

        assert W.resolve_checkpoint_ref(repo, job.job_initial_tree_ref) == ""
        for t in job.tasks:
            assert W.resolve_checkpoint_ref(repo, t.task_start_tree_ref) == ""
        # The result branch is NOT a checkpoint ref and is untouched.
        assert W._branch_exists(repo, job.worktree_branch)

    def test_a_retained_job_keeps_its_checkpoint_refs(self, repo, monkeypatch):
        job, handle = self._crashed_two_task_job(repo, monkeypatch)
        reloaded = load_job_plan(job.job_id)
        assert W.resolve_checkpoint_ref(
            repo, reloaded.job_initial_tree_ref) == reloaded.job_initial_tree
        assert W.resolve_checkpoint_ref(
            repo, reloaded.tasks[1].task_start_tree_ref
        ) == reloaded.tasks[1].task_start_tree

    def test_checkpoint_refs_live_in_the_private_namespace_only(self, repo, monkeypatch):
        job, handle = self._crashed_two_task_job(repo, monkeypatch)
        refs = _git(repo, "for-each-ref", "--format=%(refname)").split()
        checkpoints = [r for r in refs if "checkpoints" in r]
        assert checkpoints
        assert all(r.startswith("refs/remedy/checkpoints/") for r in checkpoints)
        with pytest.raises(W.WorktreeError):
            W.set_checkpoint_ref(repo, "refs/heads/main", job.job_initial_tree)


# ---------------------------------------------------------------------------
# Finding 2 — the root hand-off must be exactly the reviewed task work
# ---------------------------------------------------------------------------

def _rogue_hook(monkeypatch, holder: dict, name: str = "rogue.txt"):
    """A finalization hook that sneaks an unreviewed file into the worktree."""
    real = PJ._check_handoff_coverage

    def hooked(job, handle):
        (Path(holder["path"]) / name).write_text("never reviewed\n")
        return real(job, handle)

    monkeypatch.setattr(PJ, "_check_handoff_coverage", hooked)


class TestHandoffCoverage:
    def test_a_clean_job_reports_pass_and_exact_equality(self, repo, monkeypatch):
        job, _ = _run(repo, monkeypatch, [{"one.txt": "hello\n"}])
        assert job.handoff_coverage_verdict == "PASS"
        assert job.root_changed_files == job.reviewed_task_files == ["one.txt"]
        assert job.unexpected_root_files == [] and job.missing_root_files == []

    def test_an_unexpected_final_file_blocks_completion(self, repo, monkeypatch):
        job = parse_job_file(ONE_TASK, str(repo))
        holder: dict = {}
        _spy(monkeypatch, holder)
        _rogue_hook(monkeypatch, holder)
        prov = _Builder(holder, [{"one.txt": "hello\n"}])

        done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                       builder_name="fake", reviewer_name="fake", max_rounds=1)

        assert done.status == JOB_BLOCKED
        assert "job_handoff_coverage_failed" in done.error
        assert done.handoff_coverage_verdict == "FAIL"
        assert done.unexpected_root_files == ["rogue.txt"]
        # No authoritative root hand-off is exported, and the work is retained.
        assert done.result_diff_path == ""
        assert not (job_dir(done.job_id) / "result.diff").exists()
        assert done.worktree_cleanup_status == "retained"
        assert Path(holder["path"]).is_dir()

    def test_a_blocked_coverage_job_cannot_be_promoted(self, repo, monkeypatch):
        job = parse_job_file(ONE_TASK, str(repo))
        holder: dict = {}
        _spy(monkeypatch, holder)
        _rogue_hook(monkeypatch, holder)
        prov = _Builder(holder, [{"one.txt": "hello\n"}])
        done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                       builder_name="fake", reviewer_name="fake", max_rounds=1)

        res = promote_job(done.job_id, str(repo), dry_run=True)
        assert res.status == "blocked"
        assert "job_not_completed" in res.blocked_reason
        assert not (repo / "one.txt").exists()

    def test_evidence_exports_the_coverage_and_the_contract_requires_pass(
        self, repo, monkeypatch, tmp_path,
    ):
        job, _ = _run(repo, monkeypatch, [{"one.txt": "hello\n"}])
        out = tmp_path / "ev"
        export_job_evidence(job.job_id, str(out))

        doc = json.loads((out / "worktree.json").read_text())
        cov = doc["handoff_coverage"]
        assert cov["verdict"] == "PASS"
        assert cov["root_changed_files"] == cov["reviewed_task_files"] == ["one.txt"]

        check = check_worktree_artifacts(str(out))
        assert check["verdict"] == "PASS"
        assert check["handoff_coverage_verdict"] == "PASS"

    def test_the_contract_blocks_an_extra_file_in_the_root_diff(
        self, repo, monkeypatch, tmp_path,
    ):
        job, _ = _run(repo, monkeypatch, [{"one.txt": "hello\n"}])
        out = tmp_path / "ev"
        export_job_evidence(job.job_id, str(out))

        # The diff itself carries an unreviewed file — the bytes and the recorded
        # hash are re-synced, so ONLY a semantic check can catch this.
        import hashlib
        diff = (out / "result.diff").read_text()
        diff += (
            "diff --git a/rogue.txt b/rogue.txt\n"
            "new file mode 100644\n--- /dev/null\n+++ b/rogue.txt\n@@ -0,0 +1 @@\n"
            "+never reviewed\n"
        )
        data = diff.encode()
        (out / "result.diff").write_bytes(data)
        doc = json.loads((out / "worktree.json").read_text())
        doc["result_diff"]["sha256"] = hashlib.sha256(data).hexdigest()
        doc["result_diff"]["size_bytes"] = len(data)
        (out / "worktree.json").write_text(json.dumps(doc, indent=2))

        check = check_worktree_artifacts(str(out))
        assert check["verdict"] == "BLOCKED"
        assert any("unreviewed files" in i for i in check["handoff_coverage_issues"])

    def test_the_contract_blocks_a_missing_reviewed_file(
        self, repo, monkeypatch, tmp_path,
    ):
        job, _ = _run(repo, monkeypatch, [{"one.txt": "hello\n"}])
        out = tmp_path / "ev"
        export_job_evidence(job.job_id, str(out))
        doc = json.loads((out / "worktree.json").read_text())
        doc["handoff_coverage"]["reviewed_task_files"] = ["one.txt", "two.txt"]
        (out / "worktree.json").write_text(json.dumps(doc, indent=2))

        check = check_worktree_artifacts(str(out))
        assert check["verdict"] == "BLOCKED"
        assert any("omits reviewed files" in i or "!=" in i
                   for i in check["handoff_coverage_issues"])

    def test_promotion_blocks_when_the_source_carries_an_extra_file(
        self, repo, monkeypatch,
    ):
        job, _ = _run(repo, monkeypatch, [{"one.txt": "hello\n"}])

        # A rogue file reaches the materialized promotion source.
        real = JP._materialize_promotion_source_owned

        def hooked(j):
            src, err = real(j)
            if src is not None:
                (src.path / "rogue.txt").write_text("never reviewed\n")
            return src, err

        monkeypatch.setattr(JP, "_materialize_promotion_source_owned", hooked)

        res = promote_job(job.job_id, str(repo), dry_run=True)
        assert res.status == "blocked"
        assert "promotion_coverage_failed" in res.blocked_reason
        assert res.unexpected_source_files == ["rogue.txt"]
        assert not (repo / "one.txt").exists()


# ---------------------------------------------------------------------------
# Finding 3 — promotion preserves the reviewed file mode
# ---------------------------------------------------------------------------

def _is_exec(p: Path) -> bool:
    return os.access(p, os.X_OK)


class TestFileModePromotion:
    def _job_with_script(self, repo, monkeypatch, mode: int, content="#!/bin/sh\n"):
        (repo / "script.sh").write_text("#!/bin/sh\necho old\n")
        (repo / "script.sh").chmod(mode)
        _git(repo, "add", "-A")
        _git(repo, "commit", "-qm", "script")

        class _ModeBuilder(_Builder):
            def build(self, prompt, **kw):
                ws = Path(self._holder["path"])
                f = ws / "script.sh"
                f.write_text(content)
                f.chmod(self.target_mode)
                return BuilderOutput(summary="chmod", files_changed=["script.sh"],
                                     provider="fake")

        job = parse_job_file("# S\n\n## Task 1 — chmod\n\nchmod script.\n", str(repo))
        holder: dict = {}
        _spy(monkeypatch, holder)
        prov = _ModeBuilder(holder, [{}])
        return job, holder, prov

    def test_0644_to_0755_survives_promotion(self, repo, monkeypatch):
        job, holder, prov = self._job_with_script(repo, monkeypatch, 0o644)
        prov.target_mode = 0o755
        done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                       builder_name="fake", reviewer_name="fake", max_rounds=1)
        assert done.status == JOB_COMPLETED
        proof = done.tasks[0].apply_manifest.applied_file_proofs[0]
        assert proof.baseline_mode == "100644" and proof.final_mode == "100755"

        res = promote_job(done.job_id, str(repo), approve=True)
        assert res.status == "promoted", res.blocked_reason
        assert _is_exec(repo / "script.sh")                     # the chmod survived
        assert res.modes_applied["script.sh"] == "100755"

    def test_0755_to_0644_survives_promotion(self, repo, monkeypatch):
        job, holder, prov = self._job_with_script(repo, monkeypatch, 0o755)
        prov.target_mode = 0o644
        done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                       builder_name="fake", reviewer_name="fake", max_rounds=1)
        proof = done.tasks[0].apply_manifest.applied_file_proofs[0]
        assert proof.baseline_mode == "100755" and proof.final_mode == "100644"

        res = promote_job(done.job_id, str(repo), approve=True)
        assert res.status == "promoted", res.blocked_reason
        assert not _is_exec(repo / "script.sh")

    def test_a_newly_created_executable_keeps_its_mode(self, repo, monkeypatch):
        class _NewExec(_Builder):
            def build(self, prompt, **kw):
                f = Path(self._holder["path"]) / "tool.sh"
                f.write_text("#!/bin/sh\necho hi\n")
                f.chmod(0o755)
                return BuilderOutput(summary="new exec", files_changed=["tool.sh"],
                                     provider="fake")

        job = parse_job_file("# T\n\n## Task 1 — tool\n\nAdd tool.\n", str(repo))
        holder: dict = {}
        _spy(monkeypatch, holder)
        prov = _NewExec(holder, [{}])
        done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                       builder_name="fake", reviewer_name="fake", max_rounds=1)
        proof = done.tasks[0].apply_manifest.applied_file_proofs[0]
        assert proof.existed_before_job is False and proof.final_mode == "100755"

        res = promote_job(done.job_id, str(repo), approve=True)
        assert res.status == "promoted", res.blocked_reason
        assert (repo / "tool.sh").read_text().startswith("#!/bin/sh")
        assert _is_exec(repo / "tool.sh")
        # Bytes AND mode match, with no commit, merge or push.
        assert _git(repo, "rev-parse", "HEAD").strip() == _git(
            repo, "rev-parse", done.worktree_base_commit).strip()

    def test_a_mode_changed_after_review_blocks_promotion(self, repo, monkeypatch):
        job, holder, prov = self._job_with_script(repo, monkeypatch, 0o644)
        prov.target_mode = 0o755
        done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                       builder_name="fake", reviewer_name="fake", max_rounds=1)

        real = JP._materialize_promotion_source_owned

        def hooked(j):
            src, err = real(j)
            if src is not None:
                (src.path / "script.sh").chmod(0o644)     # the reviewed mode is lost
            return src, err

        monkeypatch.setattr(JP, "_materialize_promotion_source_owned", hooked)
        res = promote_job(done.job_id, str(repo), approve=True)

        assert res.status == "blocked"
        assert "mode_check_failed" in res.blocked_reason
        assert not _is_exec(repo / "script.sh")           # the target is untouched


# ---------------------------------------------------------------------------
# Finding 4 — temporary promotion cleanup is observable and honest
# ---------------------------------------------------------------------------

class TestPromotionCleanupHonesty:
    def _completed(self, repo, monkeypatch):
        job, _ = _run(repo, monkeypatch, [{"one.txt": "hello\n"}])
        return job

    def test_a_normal_run_leaves_no_temporary_worktree(self, repo, monkeypatch):
        job = self._completed(repo, monkeypatch)
        res = promote_job(job.job_id, str(repo), dry_run=True)
        assert res.cleanup_status == "clean" and res.cleanup_error == ""
        assert res.temporary_worktree_removed and res.temporary_registration_removed
        assert "remedy-promo" not in _git(repo, "worktree", "list", "--porcelain")
        assert len(W.list_worktrees(repo)) == 1

    @pytest.mark.parametrize("stage", ["remove", "prune", "inventory", "rmtree"])
    def test_injected_cleanup_failures_are_reported(
        self, repo, monkeypatch, stage,
    ):
        job = self._completed(repo, monkeypatch)
        real_run = subprocess.run

        def fake_run(argv, *a, **kw):
            if isinstance(argv, list) and argv[:2] == ["git", "worktree"]:
                if stage == "remove" and argv[2] == "remove":
                    return subprocess.CompletedProcess(argv, 1, "", "remove exploded")
                if stage == "prune" and argv[2] == "prune":
                    return subprocess.CompletedProcess(argv, 1, "", "prune exploded")
            return real_run(argv, *a, **kw)

        if stage == "inventory":
            monkeypatch.setattr(W, "_worktree_registered",
                                lambda *a, **k: (_ for _ in ()).throw(
                                    W.WorktreeError("inventory broken")))
        elif stage == "rmtree":
            import shutil
            monkeypatch.setattr(shutil, "rmtree",
                                lambda *a, **k: (_ for _ in ()).throw(
                                    OSError("permission denied")))
        else:
            monkeypatch.setattr(JP.subprocess, "run", fake_run)

        res = promote_job(job.job_id, str(repo), dry_run=True)

        assert res.cleanup_status == "failed"
        assert res.cleanup_error
        assert res.status == "dry_run_cleanup_failed"     # never a silent clean run
        assert not (repo / "one.txt").exists()            # dry-run mutated nothing

    def test_an_approved_promotion_with_a_failing_cleanup_says_so(
        self, repo, monkeypatch,
    ):
        job = self._completed(repo, monkeypatch)
        real_run = subprocess.run

        def fake_run(argv, *a, **kw):
            if isinstance(argv, list) and argv[:3] == ["git", "worktree", "remove"]:
                return subprocess.CompletedProcess(argv, 1, "", "remove exploded")
            return real_run(argv, *a, **kw)

        monkeypatch.setattr(JP.subprocess, "run", fake_run)
        res = promote_job(job.job_id, str(repo), approve=True)
        monkeypatch.setattr(JP.subprocess, "run", real_run)   # only undo the failure

        # The promotion really happened; the cleanup really failed. Both are told.
        assert res.status == "promoted_cleanup_failed"
        assert res.files_applied == ["one.txt"]
        assert (repo / "one.txt").read_text() == "hello\n"
        assert res.cleanup_status == "failed"
        assert any("cleanup_failed" in r for r in res.blocked_reasons)

        record = json.loads(
            (JP._promotions_dir() / job.job_id / f"{res.promotion_id}.json").read_text()
        )
        assert record["temporary_worktree_cleanup"]["cleanup_status"] == "failed"
