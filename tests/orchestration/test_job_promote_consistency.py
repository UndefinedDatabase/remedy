"""F006 promotion consistency — baseline modes, persisted cleanup, honest failures.

* Finding 1 — target file-MODE drift blocks promotion, not just content drift.
* Finding 2 — the persisted promotion record matches the returned result, cleanup
  fields included, for every outcome.
* Finding 3 — a materialization failure never swallows a cleanup failure.
* Finding 4 — a partial success plus a failed cleanup is unmistakable in the CLI
  summary.

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
from packages.orchestration import worktrees as W
from packages.orchestration.job_promote import (
    export_job_promotion_json,
    promote_job,
    summarize_job_promotion,
)
from packages.orchestration.pingpong_job import (
    JOB_COMPLETED,
    parse_job_file,
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


class _Builder:
    def __init__(self, holder: dict, write):
        self._holder = holder
        self._write = write

    def build(self, prompt, **kw):
        files = self._write(Path(self._holder["path"]))
        return BuilderOutput(summary="wrote", files_changed=files, provider="fake")

    def review(self, prompt, **kw):
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok",
                              provider="fake")


def _run_job(repo, monkeypatch, write, text="# J\n\n## Task 1 — go\n\nDo it.\n"):
    job = parse_job_file(text, str(repo))
    holder: dict = {}
    real = W.create

    def spy(job_id, r):
        h = real(job_id, r)
        holder["path"] = h.path
        return h

    monkeypatch.setattr(W, "create", spy)
    prov = _Builder(holder, write)
    done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                   builder_name="fake", reviewer_name="fake", max_rounds=1)
    assert done.status == JOB_COMPLETED, done.error
    return done


def _committed_script(repo: Path, mode: int, content: str = "old\n") -> None:
    f = repo / "script.sh"
    f.write_text(content)
    f.chmod(mode)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "script")


def _edit_script(new_content: str, mode: int | None = None):
    def write(ws: Path) -> list[str]:
        f = ws / "script.sh"
        f.write_text(new_content)
        if mode is not None:
            f.chmod(mode)
        return ["script.sh"]
    return write


def _persisted(job_id: str, promotion_id: str) -> dict:
    path = JP._promotions_dir() / job_id / f"{promotion_id}.json"
    return json.loads(path.read_text())


# ---------------------------------------------------------------------------
# Finding 1 — the target's MODE is part of the baseline
# ---------------------------------------------------------------------------

class TestBaselineModeDrift:
    def test_content_unchanged_but_target_chmod_to_0755_blocks(self, repo, monkeypatch):
        _committed_script(repo, 0o644)
        job = _run_job(repo, monkeypatch, _edit_script("new\n", 0o644))

        (repo / "script.sh").chmod(0o755)          # an external chmod, post-job

        res = promote_job(job.job_id, str(repo), dry_run=True)
        assert res.status == "blocked"
        assert "target_mode_changed_since_job: script.sh" in res.blocked_reason
        statuses = {r.path: r.baseline_status for r in res.file_readiness}
        assert statuses["script.sh"] == "target_mode_changed_since_job"
        assert (repo / "script.sh").read_text() == "old\n"    # nothing promoted
        assert os.access(repo / "script.sh", os.X_OK)         # chmod not reverted

    def test_content_unchanged_but_target_chmod_to_0644_blocks(self, repo, monkeypatch):
        _committed_script(repo, 0o755)
        job = _run_job(repo, monkeypatch, _edit_script("new\n", 0o755))

        (repo / "script.sh").chmod(0o644)

        res = promote_job(job.job_id, str(repo), dry_run=True)
        assert res.status == "blocked"
        assert "target_mode_changed_since_job" in res.blocked_reason

    def test_content_and_mode_both_changed_blocks(self, repo, monkeypatch):
        _committed_script(repo, 0o644)
        job = _run_job(repo, monkeypatch, _edit_script("new\n", 0o755))

        (repo / "script.sh").write_text("someone else\n")
        (repo / "script.sh").chmod(0o755)

        res = promote_job(job.job_id, str(repo), dry_run=True)
        assert res.status == "blocked"
        assert "target_changed_since_job" in res.blocked_reason

    def test_unchanged_content_and_mode_stays_ready(self, repo, monkeypatch):
        _committed_script(repo, 0o644)
        job = _run_job(repo, monkeypatch, _edit_script("new\n", 0o755))

        res = promote_job(job.job_id, str(repo), dry_run=True)
        assert res.status == "dry_run", res.blocked_reason
        assert res.files_planned == ["script.sh"]
        statuses = {r.path: r.baseline_status for r in res.file_readiness}
        assert statuses["script.sh"] == "target_matches_baseline"

    def test_the_mode_drift_check_also_runs_immediately_before_apply(
        self, repo, monkeypatch,
    ):
        _committed_script(repo, 0o644)
        job = _run_job(repo, monkeypatch, _edit_script("new\n", 0o755))

        # The chmod lands AFTER the first readiness pass, before the apply pass.
        real_check = JP._check_baseline_readiness
        calls = {"n": 0}

        def flaky(target, workspace, planned, proofs):
            calls["n"] += 1
            if calls["n"] == 2:                       # the pre-apply recheck
                (repo / "script.sh").chmod(0o755)
            return real_check(target, workspace, planned, proofs)

        monkeypatch.setattr(JP, "_check_baseline_readiness", flaky)
        res = promote_job(job.job_id, str(repo), approve=True)

        assert res.status == "blocked"
        assert "baseline_check_before_apply_failed" in res.blocked_reason
        assert "target_mode_changed_since_job" in res.blocked_reason
        assert (repo / "script.sh").read_text() == "old\n"     # never applied

    def test_a_newly_created_file_has_no_baseline_mode(self, repo, monkeypatch):
        def write(ws: Path) -> list[str]:
            f = ws / "tool.sh"
            f.write_text("#!/bin/sh\n")
            f.chmod(0o755)
            return ["tool.sh"]

        job = _run_job(repo, monkeypatch, write)
        proof = job.tasks[0].apply_manifest.applied_file_proofs[0]
        assert proof.existed_before_job is False
        assert proof.baseline_mode == "" and proof.final_mode == "100755"

        res = promote_job(job.job_id, str(repo), dry_run=True)
        assert res.status == "dry_run"

        # The existing creation-collision rule still applies.
        (repo / "tool.sh").write_text("someone got there first\n")
        res2 = promote_job(job.job_id, str(repo), dry_run=True)
        assert res2.status == "blocked"
        assert "target_created_since_job" in res2.blocked_reason

    def test_source_mode_fidelity_is_still_enforced(self, repo, monkeypatch):
        _committed_script(repo, 0o644)
        job = _run_job(repo, monkeypatch, _edit_script("new\n", 0o755))

        real = JP._materialize_promotion_source_owned

        def hooked(j):
            src, err = real(j)
            if src is not None and not err:
                (src.path / "script.sh").chmod(0o644)    # reviewed mode lost
            return src, err

        monkeypatch.setattr(JP, "_materialize_promotion_source_owned", hooked)
        res = promote_job(job.job_id, str(repo), approve=True)
        assert res.status == "blocked"
        assert "mode_check_failed" in res.blocked_reason
        assert not os.access(repo / "script.sh", os.X_OK)


# ---------------------------------------------------------------------------
# Finding 2 — the persisted record equals the returned result
# ---------------------------------------------------------------------------

_CLEANUP_FIELDS = (
    "temporary_worktree_removed",
    "temporary_registration_removed",
    "cleanup_status",
    "cleanup_error",
)


def _assert_record_matches(res) -> dict:
    record = _persisted(res.job_id, res.promotion_id)
    assert record["status"] == res.status
    cleanup = record["temporary_worktree_cleanup"]
    for field in _CLEANUP_FIELDS:
        assert cleanup[field] == getattr(res, field), field
    assert record["files_applied"] == res.files_applied
    # And the whole exported view agrees with the returned object.
    assert record == export_job_promotion_json(res)
    return record


class TestPersistedRecordMatchesResult:
    def _job(self, repo, monkeypatch):
        return _run_job(repo, monkeypatch,
                        lambda ws: [(ws / "one.txt").write_text("hello\n"), "one.txt"][1:]
                        and ["one.txt"])

    def test_clean_dry_run_persists_a_clean_cleanup(self, repo, monkeypatch):
        job = self._job(repo, monkeypatch)
        res = promote_job(job.job_id, str(repo), dry_run=True)

        assert res.status == "dry_run"
        assert res.cleanup_status == "clean"
        record = _assert_record_matches(res)
        cleanup = record["temporary_worktree_cleanup"]
        assert cleanup["cleanup_status"] == "clean"
        assert cleanup["temporary_worktree_removed"] is True
        assert cleanup["temporary_registration_removed"] is True

    def test_clean_approved_promotion_persists_a_clean_cleanup(self, repo, monkeypatch):
        job = self._job(repo, monkeypatch)
        res = promote_job(job.job_id, str(repo), approve=True)

        assert res.status == "promoted"
        record = _assert_record_matches(res)
        assert record["temporary_worktree_cleanup"]["cleanup_status"] == "clean"
        assert record["files_applied"] == ["one.txt"]

    def test_a_failed_post_test_still_persists_the_cleanup(self, repo, monkeypatch):
        job = self._job(repo, monkeypatch)
        res = promote_job(job.job_id, str(repo), approve=True, test_command="false")

        assert res.status == "promoted_test_failed"
        record = _assert_record_matches(res)
        assert record["temporary_worktree_cleanup"]["cleanup_status"] == "clean"
        assert (repo / "one.txt").exists()          # the files really were applied

    def test_a_blocked_mode_check_still_persists_the_cleanup(self, repo, monkeypatch):
        _committed_script(repo, 0o644)
        job = _run_job(repo, monkeypatch, _edit_script("new\n", 0o755))
        real = JP._materialize_promotion_source_owned

        def hooked(j):
            src, err = real(j)
            if src is not None and not err:
                (src.path / "script.sh").chmod(0o644)
            return src, err

        monkeypatch.setattr(JP, "_materialize_promotion_source_owned", hooked)
        res = promote_job(job.job_id, str(repo), approve=True)

        assert res.status == "blocked"
        record = _assert_record_matches(res)
        assert record["temporary_worktree_cleanup"]["cleanup_status"] == "clean"

    def test_cleanup_failure_after_a_dry_run_is_persisted(self, repo, monkeypatch):
        job = self._job(repo, monkeypatch)
        _fail_worktree_remove(monkeypatch)
        res = promote_job(job.job_id, str(repo), dry_run=True)

        assert res.status == "dry_run_cleanup_failed"
        record = _assert_record_matches(res)
        assert record["temporary_worktree_cleanup"]["cleanup_status"] == "failed"
        assert not (repo / "one.txt").exists()

    def test_cleanup_failure_after_files_were_applied_is_persisted(
        self, repo, monkeypatch,
    ):
        job = self._job(repo, monkeypatch)
        _fail_worktree_remove(monkeypatch)
        res = promote_job(job.job_id, str(repo), approve=True)

        assert res.status == "promoted_cleanup_failed"
        assert res.files_applied == ["one.txt"]
        record = _assert_record_matches(res)
        assert record["files_applied"] == ["one.txt"]
        assert record["temporary_worktree_cleanup"]["cleanup_status"] == "failed"


def _fail_worktree_remove(monkeypatch):
    real_run = subprocess.run

    def fake_run(argv, *a, **kw):
        if isinstance(argv, list) and argv[:3] == ["git", "worktree", "remove"]:
            return subprocess.CompletedProcess(argv, 1, "", "remove exploded")
        return real_run(argv, *a, **kw)

    monkeypatch.setattr(JP.subprocess, "run", fake_run)


# ---------------------------------------------------------------------------
# Finding 3 — a materialization failure never hides a cleanup failure
# ---------------------------------------------------------------------------

def _break_diff(job) -> None:
    """Make result.diff verified-but-unapplicable (hash and size stay correct)."""
    import hashlib

    from packages.orchestration.data_paths import task_job_dir
    from packages.orchestration.pingpong_job import _persist_job, load_job_plan

    path = task_job_dir(job.job_id) / "result.diff"
    data = (
        b"diff --git a/absent.txt b/absent.txt\n"
        b"--- a/absent.txt\n+++ b/absent.txt\n"
        b"@@ -1 +1 @@\n-was never here\n+nonsense\n"
    )
    path.write_bytes(data)
    reloaded = load_job_plan(job.job_id)
    reloaded.result_diff_sha256 = hashlib.sha256(data).hexdigest()
    reloaded.result_diff_size_bytes = len(data)
    _persist_job(reloaded)


class TestMaterializationFailuresReportCleanup:
    def _job(self, repo, monkeypatch):
        return _run_job(repo, monkeypatch,
                        lambda ws: [(ws / "one.txt").write_text("hello\n")] and ["one.txt"])

    def test_apply_check_failure_with_a_clean_cleanup(self, repo, monkeypatch):
        job = self._job(repo, monkeypatch)
        _break_diff(job)

        res = promote_job(job.job_id, str(repo), dry_run=True)

        assert res.status == "blocked"
        assert "job_diff_not_applicable" in res.blocked_reason
        assert res.cleanup_status == "clean"
        assert res.temporary_worktree_removed and res.temporary_registration_removed
        assert len(W.list_worktrees(repo)) == 1          # nothing left behind
        _assert_record_matches(res)

    def test_apply_check_failure_with_a_cleanup_failure_reports_both(
        self, repo, monkeypatch,
    ):
        job = self._job(repo, monkeypatch)
        _break_diff(job)
        _fail_worktree_remove(monkeypatch)

        res = promote_job(job.job_id, str(repo), dry_run=True)

        assert res.status == "materialization_failed_cleanup_failed"
        assert "job_diff_not_applicable" in res.blocked_reason   # original reason kept
        assert res.cleanup_status == "failed"
        assert any("cleanup_failed" in r for r in res.blocked_reasons)
        assert res.temporary_registration_removed is False       # honestly reported
        _assert_record_matches(res)

    def test_worktree_add_failure_with_a_cleanup_failure(self, repo, monkeypatch):
        job = self._job(repo, monkeypatch)
        real_run = subprocess.run

        def fake_run(argv, *a, **kw):
            if isinstance(argv, list) and argv[:3] == ["git", "worktree", "add"]:
                return subprocess.CompletedProcess(argv, 1, "", "add exploded")
            if isinstance(argv, list) and argv[:3] == ["git", "worktree", "remove"]:
                return subprocess.CompletedProcess(argv, 1, "", "remove exploded")
            return real_run(argv, *a, **kw)

        monkeypatch.setattr(JP.subprocess, "run", fake_run)
        res = promote_job(job.job_id, str(repo), dry_run=True)

        assert "promotion_worktree_failed" in res.blocked_reason
        assert res.cleanup_status in ("clean", "failed")
        # Whatever happened, it is REPORTED — never silently dropped.
        assert res.cleanup_status == "clean" or res.cleanup_error
        _assert_record_matches(res)

    def test_git_apply_failure_with_a_cleanup_failure(self, repo, monkeypatch):
        job = self._job(repo, monkeypatch)
        real_run = subprocess.run
        seen = {"check": 0}

        def fake_run(argv, *a, **kw):
            if isinstance(argv, list) and argv[:2] == ["git", "apply"]:
                if "--check" in argv:
                    seen["check"] += 1
                    return real_run(argv, *a, **kw)
                return subprocess.CompletedProcess(argv, 1, "", "apply exploded")
            if isinstance(argv, list) and argv[:3] == ["git", "worktree", "remove"]:
                return subprocess.CompletedProcess(argv, 1, "", "remove exploded")
            return real_run(argv, *a, **kw)

        monkeypatch.setattr(JP.subprocess, "run", fake_run)
        res = promote_job(job.job_id, str(repo), dry_run=True)

        assert "job_diff_apply_failed" in res.blocked_reason
        assert res.status == "materialization_failed_cleanup_failed"
        assert res.cleanup_status == "failed" and res.cleanup_error
        _assert_record_matches(res)

    def test_an_unexpected_exception_after_creation_is_still_cleaned_up(
        self, repo, monkeypatch,
    ):
        job = self._job(repo, monkeypatch)
        real_run = subprocess.run

        def fake_run(argv, *a, **kw):
            if isinstance(argv, list) and argv[:2] == ["git", "apply"]:
                raise OSError("git vanished")
            return real_run(argv, *a, **kw)

        monkeypatch.setattr(JP.subprocess, "run", fake_run)
        res = promote_job(job.job_id, str(repo), dry_run=True)

        assert "promotion_materialization_error" in res.blocked_reason
        assert res.cleanup_status == "clean"
        assert len(W.list_worktrees(repo)) == 1
        assert "remedy-promo" not in _git(repo, "worktree", "list", "--porcelain")


# ---------------------------------------------------------------------------
# Finding 4 — the human summary spells out a partial success
# ---------------------------------------------------------------------------

class TestCleanupFailureSummaries:
    def _job(self, repo, monkeypatch):
        return _run_job(repo, monkeypatch,
                        lambda ws: [(ws / "one.txt").write_text("hello\n")] and ["one.txt"])

    def test_a_promoted_cleanup_failure_says_the_target_changed(self, repo, monkeypatch):
        job = self._job(repo, monkeypatch)
        _fail_worktree_remove(monkeypatch)
        res = promote_job(job.job_id, str(repo), approve=True)

        text = summarize_job_promotion(res)
        assert "The target was changed." in text
        assert "Files applied: ['one.txt']" in text
        assert "Temporary promotion cleanup failed." in text
        assert "Manual cleanup is required." in text
        assert "git worktree list" in text          # the stale registration is named

    def test_a_dry_run_cleanup_failure_says_the_target_was_not_changed(
        self, repo, monkeypatch,
    ):
        job = self._job(repo, monkeypatch)
        _fail_worktree_remove(monkeypatch)
        res = promote_job(job.job_id, str(repo), dry_run=True)

        text = summarize_job_promotion(res)
        assert "The target was NOT changed (dry-run only)." in text
        assert "Temporary promotion cleanup failed." in text
        assert "Manual cleanup is required." in text
        assert not (repo / "one.txt").exists()

    def test_a_clean_run_summary_makes_no_cleanup_noise(self, repo, monkeypatch):
        job = self._job(repo, monkeypatch)
        res = promote_job(job.job_id, str(repo), dry_run=True)
        text = summarize_job_promotion(res)
        assert "Temp worktree cleanup: clean" in text
        assert "Manual cleanup is required." not in text


# ---------------------------------------------------------------------------
# Cleanup exception safety — a throwing cleanup must never escape promote_job()
# ---------------------------------------------------------------------------

_REAL_RUN = subprocess.run


def _raise_on_git(monkeypatch, subcommand: str, exc: Exception):
    """Make one cleanup git command RAISE (not just fail).

    Patching ``JP.subprocess.run`` patches the module attribute globally, so the
    injected failure is undone with ``_restore_git`` before the test does its own
    housekeeping git calls.
    """
    previous = subprocess.run

    def fake_run(argv, *a, **kw):
        if isinstance(argv, list) and argv[:3] == ["git", "worktree", subcommand]:
            raise exc
        return previous(argv, *a, **kw)

    monkeypatch.setattr(JP.subprocess, "run", fake_run)


def _restore_git(monkeypatch):
    monkeypatch.setattr(JP.subprocess, "run", _REAL_RUN)


class TestCleanupExceptionSafety:
    def _job(self, repo, monkeypatch):
        return _run_job(repo, monkeypatch,
                        lambda ws: [(ws / "one.txt").write_text("hello\n")] and ["one.txt"])

    def test_remove_timeout_becomes_a_structured_failed_cleanup(self, repo, monkeypatch):
        # The exact independently observed scenario.
        job = self._job(repo, monkeypatch)
        _raise_on_git(monkeypatch, "remove", subprocess.TimeoutExpired(
            ["git", "worktree", "remove", "--force", "..."], 120))

        res = promote_job(job.job_id, str(repo), dry_run=True)   # must NOT raise

        assert res.status == "dry_run_cleanup_failed"
        assert res.cleanup_status == "failed"
        assert "timed out" in res.cleanup_error
        _assert_record_matches(res)
        assert not (repo / "one.txt").exists()      # dry-run changed nothing

    @pytest.mark.parametrize("exc", [
        FileNotFoundError("git not found"),
        OSError("disk on fire"),
        RuntimeError("something odd"),
    ])
    def test_remove_raising_any_exception_is_contained(self, repo, monkeypatch, exc):
        job = self._job(repo, monkeypatch)
        _raise_on_git(monkeypatch, "remove", exc)

        res = promote_job(job.job_id, str(repo), dry_run=True)

        assert res.status == "dry_run_cleanup_failed"
        assert res.cleanup_status == "failed" and res.cleanup_error
        assert type(exc).__name__ in res.cleanup_error or "timed out" in res.cleanup_error
        _assert_record_matches(res)

    @pytest.mark.parametrize("exc", [
        subprocess.TimeoutExpired(["git", "worktree", "prune"], 60),
        OSError("prune exploded"),
    ])
    def test_prune_raising_is_contained_and_remove_still_ran(
        self, repo, monkeypatch, exc,
    ):
        job = self._job(repo, monkeypatch)
        _raise_on_git(monkeypatch, "prune", exc)

        res = promote_job(job.job_id, str(repo), dry_run=True)

        assert res.status == "dry_run_cleanup_failed"
        assert res.cleanup_status == "failed"
        assert "prune" in res.cleanup_error
        # The remove step still ran, so the physical worktree really is gone.
        assert res.temporary_worktree_removed is True
        assert res.temporary_registration_removed is True
        _assert_record_matches(res)

    def test_remove_throws_but_the_secondary_filesystem_cleanup_succeeds(
        self, repo, monkeypatch,
    ):
        job = self._job(repo, monkeypatch)
        _raise_on_git(monkeypatch, "remove", subprocess.TimeoutExpired(
            ["git", "worktree", "remove"], 120))

        res = promote_job(job.job_id, str(repo), dry_run=True)

        # rmtree still removed the directory; the STALE REGISTRATION is reported.
        assert res.temporary_worktree_removed is True
        assert res.temporary_registration_removed is False
        assert "still registered" in res.cleanup_error
        assert res.cleanup_status == "failed"

    def test_a_remaining_registration_is_reported(self, repo, monkeypatch):
        job = self._job(repo, monkeypatch)
        _raise_on_git(monkeypatch, "remove", subprocess.TimeoutExpired(
            ["git", "worktree", "remove"], 120))
        _raise_on_git(monkeypatch, "prune", subprocess.TimeoutExpired(
            ["git", "worktree", "prune"], 60))

        res = promote_job(job.job_id, str(repo), dry_run=True)
        assert res.temporary_registration_removed is False
        text = summarize_job_promotion(res)
        assert "A temporary git worktree registration may remain" in text
        assert "Manual cleanup is required." in text

        # Clean the leftover registration so the fixture repo ends tidy.
        _restore_git(monkeypatch)
        _git(repo, "worktree", "prune")

    def test_inventory_throwing_after_the_git_commands_is_contained(
        self, repo, monkeypatch,
    ):
        job = self._job(repo, monkeypatch)
        monkeypatch.setattr(W, "_worktree_registered",
                            lambda *a, **k: (_ for _ in ()).throw(
                                RuntimeError("inventory broken")))

        res = promote_job(job.job_id, str(repo), dry_run=True)

        assert res.status == "dry_run_cleanup_failed"
        assert "worktree inventory failed" in res.cleanup_error
        assert res.temporary_registration_removed is False
        _assert_record_matches(res)

    def test_an_approved_promotion_survives_a_cleanup_timeout(self, repo, monkeypatch):
        job = self._job(repo, monkeypatch)
        _raise_on_git(monkeypatch, "remove", subprocess.TimeoutExpired(
            ["git", "worktree", "remove", "--force", "..."], 120))

        res = promote_job(job.job_id, str(repo), approve=True)   # must NOT raise

        assert res.status == "promoted_cleanup_failed"
        assert res.files_applied == ["one.txt"]
        assert (repo / "one.txt").read_text() == "hello\n"      # the target DID change
        assert res.cleanup_status == "failed"
        record = _assert_record_matches(res)
        assert record["files_applied"] == ["one.txt"]

        text = summarize_job_promotion(res)
        assert "The target was changed." in text
        assert "Files applied: ['one.txt']" in text
        assert "Manual cleanup is required." in text
        _restore_git(monkeypatch)
        _git(repo, "worktree", "prune")

    def test_a_materialization_failure_plus_a_cleanup_timeout_reports_both(
        self, repo, monkeypatch,
    ):
        job = self._job(repo, monkeypatch)
        _break_diff(job)
        _raise_on_git(monkeypatch, "remove", subprocess.TimeoutExpired(
            ["git", "worktree", "remove"], 120))

        res = promote_job(job.job_id, str(repo), dry_run=True)

        assert res.status == "materialization_failed_cleanup_failed"
        assert "job_diff_not_applicable" in res.blocked_reason   # original reason kept
        assert res.cleanup_status == "failed" and "timed out" in res.cleanup_error
        _assert_record_matches(res)
        _restore_git(monkeypatch)
        _git(repo, "worktree", "prune")

    def test_the_cleanup_helper_itself_never_raises(self, repo, monkeypatch):
        job = self._job(repo, monkeypatch)
        _raise_on_git(monkeypatch, "remove", subprocess.TimeoutExpired(
            ["git", "worktree", "remove"], 120))
        source, err = JP._materialize_promotion_source_owned(
            __import__("packages.orchestration.pingpong_job", fromlist=["x"])
            .load_job_plan(job.job_id))
        assert source is not None and not err

        out = JP._cleanup_promotion_source(source)      # total: returns, never raises

        assert out["cleanup_status"] == "failed"
        assert "timed out" in out["cleanup_error"]
        assert isinstance(out["temporary_worktree_removed"], bool)
        _restore_git(monkeypatch)
        _git(repo, "worktree", "prune")

    def test_an_unexpectedly_raising_cleanup_helper_is_still_contained(
        self, repo, monkeypatch,
    ):
        job = self._job(repo, monkeypatch)
        monkeypatch.setattr(JP, "_cleanup_promotion_source",
                            lambda src: (_ for _ in ()).throw(
                                RuntimeError("cleanup helper exploded")))

        res = promote_job(job.job_id, str(repo), approve=True)   # must NOT raise

        assert res.status == "promoted_cleanup_failed"
        assert res.files_applied == ["one.txt"]
        assert "cleanup raised unexpectedly" in res.cleanup_error
        _assert_record_matches(res)
        _git(repo, "worktree", "prune")   # the helper was patched, not subprocess
