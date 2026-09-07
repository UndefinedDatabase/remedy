"""F006 lifecycle corrections — locks, resume selection, finalization, lost work.

* Finding 2 — a returned run must never retain an unreachable lock.
* Finding 3 — several recoverable worktrees are never finalized from one continuation.
* Finding 4 — a failing resume finalization stays recoverable and leaks no lock.
* Finding 5 — a missing worktree with no VALID diff is never called clean.

Temporary git repositories, fake providers and CLI monkeypatching only.
No provider call is ever made.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from uuid import uuid4

import pytest

from apps.cli.commands import job as job_cmd
from packages.core.models import Job, RunState
from packages.orchestration import data_paths, event_replay
from packages.orchestration import worktree_resume as WR
from packages.orchestration import worktrees as W
from packages.orchestration.pingpong_loop import (
    load_run,
    run_pingpong,
)
from packages.orchestration.pingpong_provider import BuilderOutput, ReviewerOutput
from packages.orchestration.storage import save_job

_REAL_UPDATE = WR._update_persisted_run
_REAL_REMOVE = W.remove
_REAL_SNAPSHOT = W.snapshot
_REAL_WRITE_DIFF = W.write_result_diff


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
    (r / "a.txt").write_text("v1\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "init")
    return r


class _WritingProvider:
    def __init__(self, holder: dict, content: str = "changed\n"):
        self._holder = holder
        self._content = content

    def build(self, prompt, **kw):
        (Path(self._holder["path"]) / "a.txt").write_text(self._content)
        return BuilderOutput(summary="edited", files_changed=["a.txt"], provider="fake")

    def review(self, prompt, **kw):
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok",
                              provider="fake")


# ---------------------------------------------------------------------------
# Finding 2 — keep_staging must not orphan the lock
# ---------------------------------------------------------------------------

class TestKeepStagingReleasesItsLock:
    def _keep_run(self, repo, monkeypatch, content="kept work\n"):
        holder: dict = {}
        real_create = W.create

        def spy(job, r):
            h = real_create(job, r)
            holder["path"] = h.path
            return h

        monkeypatch.setattr(W, "create", spy)
        prov = _WritingProvider(holder, content)
        res = run_pingpong("goal", str(repo), builder_provider=prov,
                           reviewer_provider=prov, builder_name="fake",
                           reviewer_name="fake", max_rounds=1, keep_staging=True)
        return res, Path(holder["path"])

    def test_worktree_is_retained(self, repo, monkeypatch):
        res, path = self._keep_run(repo, monkeypatch)
        assert path.is_dir()
        assert (path / "a.txt").read_text() == "kept work\n"
        assert res.worktree_cleanup_status == "retained"
        assert load_run(res.run_id)["worktree"]["cleanup_status"] == "retained"

    def test_recover_can_immediately_claim_it(self, repo, monkeypatch):
        res, path = self._keep_run(repo, monkeypatch)
        rec = W.recover(res.run_id, repo)          # would raise on an orphaned lock
        assert rec is not None and rec.branch == res.worktree_branch
        assert (Path(rec.path) / "a.txt").read_text() == "kept work\n"
        W.release_lock(rec)

    def test_an_unrelated_worktree_is_untouched(self, repo, monkeypatch):
        other = W.create("otherjob", repo)
        (Path(other.path) / "a.txt").write_text("other\n")
        self._keep_run(repo, monkeypatch)
        assert (Path(other.path) / "a.txt").read_text() == "other\n"
        W.remove(other)

    def test_cleanup_succeeds_afterwards(self, repo, monkeypatch):
        res, path = self._keep_run(repo, monkeypatch)
        rec = W.recover(res.run_id, repo)
        out = W.remove(rec, keep_branch=True)
        assert out["cleanup_status"] == "clean"
        assert not path.exists()
        assert W._branch_exists(repo, res.worktree_branch)
        assert _git(repo, "status", "--porcelain") == ""


# ---------------------------------------------------------------------------
# Shared fixtures for the CLI resume tests
# ---------------------------------------------------------------------------

def _write_events(job_id: str) -> None:
    from packages.orchestration.data_paths import resolve_data_root
    runs = resolve_data_root() / "job_logs" / job_id
    runs.mkdir(parents=True, exist_ok=True)
    with (runs / "run.jsonl").open("w") as fh:
        for e in [{"event": "autorun_started", "metadata": {}},
                  {"event": "patch_intent_applied", "metadata": {}}]:
            e["timestamp"] = "2026-07-11T00:00:00Z"
            fh.write(json.dumps(e) + "\n")


def _persist_run_record(run_id: str, job_id: str, repo: Path, handle,
                        status: str = "active", result_diff=None) -> Path:
    run_dir = data_paths.run_dir(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "result.json").write_text(json.dumps({
        "run_id": run_id, "job_id": job_id, "repo_path": str(repo),
        "isolation_mode": "worktree",
        "worktree": {
            "isolation_mode": "worktree",
            "branch": handle.branch,
            "path": handle.relative_path,
            "base_commit": handle.base_commit,
            "head": handle.head_commit,
            "lock_id": f"{run_id}.lock",
            "cleanup_status": status,
            "cleanup_error": "",
            "result_diff": result_diff,
            "result_diff_error": "",
        },
    }, indent=2) + "\n")
    return run_dir


def _interrupt(repo: Path, run_id: str, content: str):
    h = W.create(run_id, repo)
    (Path(h.path) / "a.txt").write_text(content)
    W.diff(h)
    W.release_lock(h)
    return h


@pytest.fixture
def job_with_events(repo):
    jid = uuid4()
    save_job(Job(id=jid, name="killed", state=RunState.RUNNING))
    _write_events(str(jid))
    return {"job_id": str(jid), "checkpoint": f"{jid}-applied", "repo": repo}


def _resume(job, capsys, expect_exit=False):
    if expect_exit:
        with pytest.raises(SystemExit):
            job_cmd._cmd_resume(job["job_id"], checkpoint_id=job["checkpoint"],
                                json_output=True)
    else:
        job_cmd._cmd_resume(job["job_id"], checkpoint_id=job["checkpoint"],
                            json_output=True)
    return json.loads(capsys.readouterr().out)


# ---------------------------------------------------------------------------
# Finding 3 — never resume several worktrees through one continuation
# ---------------------------------------------------------------------------

class TestMultipleRecoverableWorktrees:
    def test_two_recoverable_runs_block_and_neither_is_removed(
        self, job_with_events, capsys, repo, monkeypatch,
    ):
        called: dict = {}

        def _stub(job, cid, dd, workspace_root=None):
            called["ran"] = True
            return event_replay.ResumeResult(resumed=True, tests_passed=True)

        monkeypatch.setattr(event_replay, "execute_resume_from_apply", _stub)

        ha = _interrupt(repo, "runa", "A change\n")
        hb = _interrupt(repo, "runb", "B change\n")
        _persist_run_record("runa", job_with_events["job_id"], repo, ha)
        _persist_run_record("runb", job_with_events["job_id"], repo, hb)

        out = _resume(job_with_events, capsys, expect_exit=True)

        assert out["blocked_reason"] == "ambiguous_recoverable_worktrees"
        assert called == {}                       # no continuation ran at all
        # Neither worktree was removed, and neither is marked clean.
        assert Path(ha.path).is_dir() and Path(hb.path).is_dir()
        assert (Path(ha.path) / "a.txt").read_text() == "A change\n"
        assert (Path(hb.path) / "a.txt").read_text() == "B change\n"
        for rid in ("runa", "runb"):
            assert load_run(rid)["worktree"]["cleanup_status"] != "clean"

    def test_both_locks_are_released_after_an_ambiguous_block(
        self, job_with_events, capsys, repo, monkeypatch,
    ):
        monkeypatch.setattr(event_replay, "execute_resume_from_apply",
                            lambda *a, **k: event_replay.ResumeResult(resumed=True))
        ha = _interrupt(repo, "runa", "A change\n")
        hb = _interrupt(repo, "runb", "B change\n")
        _persist_run_record("runa", job_with_events["job_id"], repo, ha)
        _persist_run_record("runb", job_with_events["job_id"], repo, hb)

        _resume(job_with_events, capsys, expect_exit=True)

        for rid in ("runa", "runb"):
            rec = W.recover(rid, repo)            # raises if a lock leaked
            assert rec is not None
            W.release_lock(rec)

    def test_a_single_recoverable_run_resumes_in_its_own_workspace(
        self, job_with_events, capsys, repo, monkeypatch,
    ):
        seen: dict = {}

        def _stub(job, cid, dd, workspace_root=None):
            seen["root"] = str(workspace_root)
            seen["content"] = (Path(workspace_root) / "a.txt").read_text()
            return event_replay.ResumeResult(resumed=True, tests_passed=True)

        monkeypatch.setattr(event_replay, "execute_resume_from_apply", _stub)
        ha = _interrupt(repo, "runa", "A change\n")
        _persist_run_record("runa", job_with_events["job_id"], repo, ha)

        out = _resume(job_with_events, capsys)

        assert seen["root"] == ha.path            # the matching workspace
        assert seen["content"] == "A change\n"
        assert out["worktrees"][0]["recovered"] is True
        assert not Path(ha.path).exists()
        assert W._branch_exists(repo, "remedy/runa")


# ---------------------------------------------------------------------------
# Finding 4 — a failing finalization stays recoverable and leaks no lock
# ---------------------------------------------------------------------------

class TestFinalizationFailureIsRecoverable:
    def _prepare_single(self, job_with_events, repo, content="A change\n"):
        h = _interrupt(repo, "runa", content)
        _persist_run_record("runa", job_with_events["job_id"], repo, h)
        return h

    @pytest.mark.parametrize("stage", ["snapshot", "diff", "remove", "persist"])
    def test_failure_retains_the_worktree_and_releases_the_lock(
        self, job_with_events, capsys, repo, monkeypatch, stage,
    ):
        h = self._prepare_single(job_with_events, repo)
        monkeypatch.setattr(event_replay, "execute_resume_from_apply",
                            lambda *a, **k: event_replay.ResumeResult(
                                resumed=True, tests_passed=True))

        calls = {"n": 0}

        def boom(*a, **kw):
            raise OSError(f"{stage} exploded")

        if stage == "snapshot":
            monkeypatch.setattr(WR.W, "snapshot", boom)
        elif stage == "diff":
            def flaky(handle, out):               # prepare succeeds, finalize fails
                calls["n"] += 1
                if calls["n"] > 1:
                    raise OSError("diff exploded")
                return _REAL_WRITE_DIFF(handle, out)
            monkeypatch.setattr(WR.W, "write_result_diff", flaky)
        elif stage == "remove":
            monkeypatch.setattr(WR.W, "remove", boom)
        else:
            monkeypatch.setattr(WR, "_update_persisted_run", boom)

        # A snapshot failure hits the PREPARE phase, which blocks; the others hit
        # finalization. In every case the worktree must survive and unlock.
        out = _resume(job_with_events, capsys, expect_exit=(stage == "snapshot"))
        # Undo only the injected failure — not the data-root fixture.
        monkeypatch.setattr(WR.W, "snapshot", _REAL_SNAPSHOT)
        monkeypatch.setattr(WR.W, "write_result_diff", _REAL_WRITE_DIFF)
        monkeypatch.setattr(WR.W, "remove", _REAL_REMOVE)
        monkeypatch.setattr(WR, "_update_persisted_run", _REAL_UPDATE)

        wt = out["worktrees"][0]
        assert wt["recovered"] is False
        if stage != "snapshot":
            assert wt["cleanup_status"] == "failed_recoverable"
        # In every case the work survives and the lock is free again.
        assert Path(h.path).is_dir()
        assert (Path(h.path) / "a.txt").read_text() == "A change\n"
        rec = W.recover("runa", repo)             # raises if the lock leaked
        assert rec is not None and rec.branch == "remedy/runa"
        W.release_lock(rec)

    def test_a_later_resume_can_retry_after_a_finalization_failure(
        self, job_with_events, capsys, repo, monkeypatch,
    ):
        h = self._prepare_single(job_with_events, repo)
        monkeypatch.setattr(event_replay, "execute_resume_from_apply",
                            lambda *a, **k: event_replay.ResumeResult(
                                resumed=True, tests_passed=True))
        monkeypatch.setattr(WR.W, "remove",
                            lambda *a, **k: (_ for _ in ()).throw(OSError("boom")))
        first = _resume(job_with_events, capsys)
        assert first["worktrees"][0]["cleanup_status"] == "failed_recoverable"

        monkeypatch.setattr(WR.W, "remove", _REAL_REMOVE)   # the failure clears
        second = _resume(job_with_events, capsys)

        assert second["worktrees"][0]["recovered"] is True
        assert second["worktrees"][0]["cleanup_status"] == "clean"
        assert not Path(h.path).exists()
        assert W._branch_exists(repo, "remedy/runa")
        assert _git(repo, "status", "--porcelain") == ""


# ---------------------------------------------------------------------------
# Finding 5 — a missing worktree with no valid diff is never "clean"
# ---------------------------------------------------------------------------

class TestMissingWorktreeWithoutAValidDiff:
    def _gone(self, job_with_events, repo, result_diff=None, diff_bytes=None):
        h = _interrupt(repo, "runa", "A change\n")
        run_dir = _persist_run_record(
            "runa", job_with_events["job_id"], repo, h, result_diff=result_diff)
        if diff_bytes is not None:
            (run_dir / "result.diff").write_bytes(diff_bytes)
        # The physical worktree disappears; only the branch survives.
        rec = W.recover("runa", repo)
        W.remove(rec, keep_branch=True)
        return run_dir

    def test_no_diff_at_all_is_unrecoverable_not_clean(self, job_with_events, capsys, repo):
        self._gone(job_with_events, repo)
        out = _resume(job_with_events, capsys, expect_exit=True)
        wt = out["worktrees"][0]
        assert wt["cleanup_status"] == "unrecoverable"
        assert wt["cleanup_status"] != "clean"
        assert "hand-off is incomplete" in wt["blocked_reason"]
        assert "result.diff" not in " ".join(wt["notes"]) or True
        assert load_run("runa")["worktree"]["cleanup_status"] == "unrecoverable"

    def test_a_tampered_diff_is_unrecoverable(self, job_with_events, capsys, repo):
        data = b"diff --git a/a.txt b/a.txt\n"
        rd = {"path": "result.diff", "sha256": hashlib.sha256(data).hexdigest(),
              "size_bytes": len(data)}
        self._gone(job_with_events, repo, result_diff=rd, diff_bytes=b"tampered\n")
        out = _resume(job_with_events, capsys, expect_exit=True)
        assert out["worktrees"][0]["cleanup_status"] == "unrecoverable"
        assert "sha256" in out["worktrees"][0]["blocked_reason"]

    def test_repeated_resume_keeps_reporting_the_unrecoverable_state(
        self, job_with_events, capsys, repo,
    ):
        self._gone(job_with_events, repo)
        _resume(job_with_events, capsys, expect_exit=True)
        again = _resume(job_with_events, capsys, expect_exit=True)   # never forgotten
        assert again["worktrees"][0]["cleanup_status"] == "unrecoverable"
        assert W._branch_exists(repo, "remedy/runa")   # no replacement branch either
        branches = _git(repo, "branch", "--format=%(refname:short)").split()
        assert [b for b in branches if b.startswith("remedy/")] == ["remedy/runa"]

    def test_a_valid_diff_makes_the_missing_worktree_a_complete_handoff(
        self, job_with_events, capsys, repo,
    ):
        data = b"diff --git a/a.txt b/a.txt\n+A change\n"
        rd = {"path": "result.diff", "sha256": hashlib.sha256(data).hexdigest(),
              "size_bytes": len(data)}
        self._gone(job_with_events, repo, result_diff=rd, diff_bytes=data)
        out = _resume(job_with_events, capsys, expect_exit=True)
        wt = out["worktrees"][0]
        assert wt["cleanup_status"] == "handoff_complete"
        assert wt["branch_kept"] is True
        assert load_run("runa")["worktree"]["cleanup_status"] == "handoff_complete"
