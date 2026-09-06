"""F006 correction, Finding 3 — the REAL ``remedy job resume`` recovers a worktree.

Before this fix ``worktrees.recover()`` had no production caller: an interrupted
run's worktree was rediscoverable only from tests. These tests drive the actual
CLI command (``apps.cli.commands.job._cmd_resume``) against a temporary git
repository and a persisted, interrupted run record.

The resume continuation itself (``execute_resume_from_apply``) is stubbed, so no
test runner and — above all — no provider is ever invoked.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from uuid import uuid4

import pytest

from apps.cli.commands import job as job_cmd
from packages.core.models import Job, RunState
from packages.orchestration import event_replay
from packages.orchestration import worktrees as W
from packages.orchestration.data_paths import pingpong_run_dir
from packages.orchestration.storage import save_job


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


def _write_events(job_id: str) -> None:
    from packages.orchestration.data_paths import resolve_data_root
    runs = resolve_data_root() / "runs" / job_id
    runs.mkdir(parents=True, exist_ok=True)
    events = [
        {"event": "autorun_started", "metadata": {}, "timestamp": "2026-07-11T00:00:00Z"},
        {"event": "patch_intent_applied", "metadata": {}, "timestamp": "2026-07-11T00:00:01Z"},
    ]
    with (runs / "run.jsonl").open("w") as fh:
        for e in events:
            fh.write(json.dumps(e) + "\n")


def _persist_interrupted_run(run_id: str, job_id: str, repo: Path, handle) -> Path:
    """The record a killed run leaves behind: a worktree still marked active."""
    run_dir = pingpong_run_dir(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "result.json").write_text(json.dumps({
        "run_id": run_id,
        "job_id": job_id,
        "repo_path": str(repo),
        "final_status": "",
        "isolation_mode": "worktree",
        "worktree": {
            "isolation_mode": "worktree",
            "branch": handle.branch,
            "path": handle.relative_path,
            "base_commit": handle.base_commit,
            "head": handle.head_commit,
            "lock_id": f"{run_id}.lock",
            "cleanup_status": "active",
            "cleanup_error": "",
            "result_diff": None,
            "result_diff_error": "",
        },
    }, indent=2) + "\n")
    return run_dir


@pytest.fixture
def interrupted(repo, monkeypatch):
    """A job whose run was killed while it owned a worktree with real work in it."""
    jid = uuid4()
    run_id = "runkilled01"

    handle = W.create(run_id, repo)
    (Path(handle.path) / "a.txt").write_text("interrupted work\n")
    expected_diff = W.diff(handle)
    W.release_lock(handle)                      # the process dies; no remove()

    run_dir = _persist_interrupted_run(run_id, str(jid), repo, handle)
    save_job(Job(id=jid, name="killed", state=RunState.RUNNING))
    _write_events(str(jid))

    # The continuation past the checkpoint is not what is under test — and it must
    # never call a provider or a test runner.
    called: dict = {}

    def _stub(job, checkpoint_id, data_dir, workspace_root=None):
        called["checkpoint_id"] = checkpoint_id
        called["workspace_root"] = str(workspace_root or "")
        # What the continuation can SEE: it must be looking at the recovered
        # worktree, not at an empty job workspace.
        called["seen"] = (Path(workspace_root) / "a.txt").read_text() if workspace_root else ""
        called["worktree_present"] = bool(workspace_root) and Path(workspace_root).is_dir()
        return event_replay.ResumeResult(
            checkpoint_id=checkpoint_id, checkpoint_kind="source_apply_proven",
            resume_mode="from_apply", resumed=True, tests_passed=True,
        )

    monkeypatch.setattr(event_replay, "execute_resume_from_apply", _stub)

    return {
        "job_id": str(jid), "run_id": run_id, "repo": repo, "handle": handle,
        "run_dir": run_dir, "expected_diff": expected_diff, "called": called,
        "checkpoint": f"{jid}-applied",
    }


def _resume(interrupted, capsys) -> dict:
    job_cmd._cmd_resume(interrupted["job_id"],
                        checkpoint_id=interrupted["checkpoint"], json_output=True)
    return json.loads(capsys.readouterr().out)


class TestResumeRecoversTheWorktree:
    def test_interrupted_worktree_is_recovered_through_the_real_resume_command(
        self, interrupted, capsys,
    ):
        out = _resume(interrupted, capsys)
        wts = out["worktrees"]
        assert len(wts) == 1
        assert wts[0]["recovered"] is True
        assert wts[0]["run_id"] == interrupted["run_id"]
        # It really did continue through the existing safe checkpoint.
        assert interrupted["called"]["checkpoint_id"] == interrupted["checkpoint"]
        assert out["resumed"] is True

    def test_exact_branch_and_path_are_reused(self, interrupted, capsys):
        out = _resume(interrupted, capsys)
        wt = out["worktrees"][0]
        rid = interrupted["run_id"]
        assert wt["branch"] == f"remedy/{rid}" == interrupted["handle"].branch
        assert wt["worktree_path"] == f".remedy-wt/{rid}"
        # No replacement branch was invented.
        branches = _git(interrupted["repo"], "branch", "--format=%(refname:short)").split()
        assert [b for b in branches if b.startswith("remedy/")] == [f"remedy/{rid}"]

    def test_the_diff_survives_the_interruption(self, interrupted, capsys):
        out = _resume(interrupted, capsys)
        diff_file = interrupted["run_dir"] / "result.diff"
        text = diff_file.read_text()
        assert text == interrupted["expected_diff"]
        assert "interrupted work" in text
        assert out["worktrees"][0]["result_diff_size_bytes"] == len(text.encode())

    def test_successful_resume_cleans_the_worktree_but_keeps_the_branch(
        self, interrupted, capsys,
    ):
        repo = interrupted["repo"]
        main_before = _git(repo, "rev-parse", "HEAD").strip()

        out = _resume(interrupted, capsys)

        assert out["worktrees"][0]["cleanup_status"] == "clean"
        assert out["worktrees"][0]["branch_kept"] is True
        assert not Path(interrupted["handle"].path).exists()
        assert len(W.list_worktrees(repo)) == 1
        assert W._branch_exists(repo, f"remedy/{interrupted['run_id']}")
        # No automatic merge: main is untouched and still clean.
        assert _git(repo, "rev-parse", "HEAD").strip() == main_before
        assert _git(repo, "status", "--porcelain") == ""
        assert (repo / "a.txt").read_text() == "v1\n"

    def test_persisted_record_is_updated_to_clean(self, interrupted, capsys):
        _resume(interrupted, capsys)
        data = json.loads((interrupted["run_dir"] / "result.json").read_text())
        wt = data["worktree"]
        assert wt["cleanup_status"] == "clean"
        assert wt["recovered_by_resume"] is True
        assert wt["result_diff"]["size_bytes"] > 0

    def test_second_resume_finds_no_stale_active_state(self, interrupted, capsys):
        _resume(interrupted, capsys)
        out = _resume(interrupted, capsys)
        assert out["worktrees"] == []          # nothing left to recover
        assert out["resumed"] is True


class TestResumeBlocksHonestly:
    def test_branch_mismatch_blocks_and_creates_no_replacement_branch(
        self, interrupted, capsys, repo,
    ):
        # The record claims a branch that is not this run's own.
        path = interrupted["run_dir"] / "result.json"
        data = json.loads(path.read_text())
        data["worktree"]["branch"] = "remedy/someone-else"
        path.write_text(json.dumps(data, indent=2))

        with pytest.raises(SystemExit) as exc:
            job_cmd._cmd_resume(interrupted["job_id"],
                                checkpoint_id=interrupted["checkpoint"],
                                json_output=True)
        assert exc.value.code == 1
        out = json.loads(capsys.readouterr().out)
        assert out["resumed"] is False
        assert out["blocked_reason"] == "worktree_recovery_blocked"
        assert "does not match recorded" in out["worktrees"][0]["blocked_reason"]

        assert not W._branch_exists(repo, "remedy/someone-else")
        assert Path(interrupted["handle"].path).is_dir()   # nothing destroyed
        assert interrupted["called"] == {}                 # no continuation ran

    def test_base_commit_mismatch_blocks(self, interrupted, capsys):
        path = interrupted["run_dir"] / "result.json"
        data = json.loads(path.read_text())
        data["worktree"]["base_commit"] = "0" * 40
        path.write_text(json.dumps(data, indent=2))

        with pytest.raises(SystemExit):
            job_cmd._cmd_resume(interrupted["job_id"],
                                checkpoint_id=interrupted["checkpoint"],
                                json_output=True)
        out = json.loads(capsys.readouterr().out)
        assert "not in the repository" in out["worktrees"][0]["blocked_reason"]

    def test_missing_worktree_with_retained_branch_is_handled_honestly(
        self, interrupted, capsys, repo,
    ):
        # The physical worktree is gone, the result branch survived.
        W.remove(W.recover(interrupted["run_id"], repo), keep_branch=True)

        with pytest.raises(SystemExit):
            job_cmd._cmd_resume(interrupted["job_id"],
                                checkpoint_id=interrupted["checkpoint"],
                                json_output=True)
        out = json.loads(capsys.readouterr().out)
        wt = out["worktrees"][0]
        assert wt["recovered"] is False
        assert "physical worktree is gone" in wt["blocked_reason"]
        assert wt["branch_kept"] is True
        # Blocked honestly: no replacement branch, no copied workspace.
        assert W._branch_exists(repo, f"remedy/{interrupted['run_id']}")
        assert interrupted["called"] == {}

    def test_a_live_run_holding_the_lock_blocks_resume(self, interrupted, capsys, repo):
        holder = W.recover(interrupted["run_id"], repo)   # simulate the run still alive
        try:
            with pytest.raises(SystemExit):
                job_cmd._cmd_resume(interrupted["job_id"],
                                    checkpoint_id=interrupted["checkpoint"],
                                    json_output=True)
            out = json.loads(capsys.readouterr().out)
            assert "lock is held" in out["worktrees"][0]["blocked_reason"]
            assert interrupted["called"] == {}
        finally:
            W.remove(holder)


class TestNoProviderCalls:
    def test_resume_never_constructs_a_provider(self, interrupted, capsys, monkeypatch):
        import packages.orchestration.pingpong_loop as PL

        def forbidden(*a, **kw):
            raise AssertionError("a provider was constructed during resume")

        monkeypatch.setattr(PL, "_create_provider_with_cwd", forbidden)
        monkeypatch.setattr(PL, "run_pingpong", forbidden)
        out = _resume(interrupted, capsys)
        assert out["worktrees"][0]["recovered"] is True


class TestTwoPhaseResume:
    """The continuation must run INSIDE the recovered worktree, and cleanup must
    happen only afterwards — never before."""

    def test_continuation_sees_the_recovered_modified_file(self, interrupted, capsys):
        out = _resume(interrupted, capsys)
        called = interrupted["called"]
        assert called["worktree_present"] is True
        assert called["workspace_root"] == interrupted["handle"].path
        assert called["seen"] == "interrupted work\n"      # the run's own change
        assert out["worktrees"][0]["recovered"] is True

    def test_cleanup_happens_only_after_a_successful_continuation(
        self, interrupted, capsys, repo,
    ):
        out = _resume(interrupted, capsys)
        # During the continuation the worktree still existed (asserted above);
        # after it, it is gone and the branch is kept.
        assert not Path(interrupted["handle"].path).exists()
        assert out["worktrees"][0]["cleanup_status"] == "clean"
        assert W._branch_exists(repo, f"remedy/{interrupted['run_id']}")
        assert len(W.list_worktrees(repo)) == 1

    def test_failed_tests_keep_the_worktree_recoverable(
        self, interrupted, capsys, repo, monkeypatch,
    ):
        def _failing(job, checkpoint_id, data_dir, workspace_root=None):
            return event_replay.ResumeResult(
                checkpoint_id=checkpoint_id, resume_mode="from_apply",
                resumed=True, tests_passed=False, stop_reason="test_failed_after_apply",
            )

        monkeypatch.setattr(event_replay, "execute_resume_from_apply", _failing)
        out = _resume(interrupted, capsys)

        wt = out["worktrees"][0]
        assert wt["recovered"] is False
        assert wt["cleanup_status"] == "retained"          # never "clean"
        assert Path(interrupted["handle"].path).is_dir()
        assert (Path(interrupted["handle"].path) / "a.txt").read_text() == "interrupted work\n"
        assert json.loads((interrupted["run_dir"] / "result.json").read_text())[
            "worktree"]["cleanup_status"] == "retained"

    def test_raising_continuation_keeps_the_worktree_recoverable(
        self, interrupted, repo, monkeypatch,
    ):
        def _raising(job, checkpoint_id, data_dir, workspace_root=None):
            raise RuntimeError("continuation exploded")

        monkeypatch.setattr(event_replay, "execute_resume_from_apply", _raising)
        with pytest.raises(RuntimeError, match="continuation exploded"):
            job_cmd._cmd_resume(interrupted["job_id"],
                                checkpoint_id=interrupted["checkpoint"],
                                json_output=True)

        assert Path(interrupted["handle"].path).is_dir()
        wt = json.loads((interrupted["run_dir"] / "result.json").read_text())["worktree"]
        assert wt["cleanup_status"] == "retained"
        # The lock was released, so a later resume can claim the SAME worktree.
        rec = W.recover(interrupted["run_id"], repo)
        assert rec is not None and rec.branch == f"remedy/{interrupted['run_id']}"
        W.release_lock(rec)

    def test_second_resume_after_failure_reuses_the_same_branch_and_path(
        self, interrupted, capsys, repo, monkeypatch,
    ):
        main_before = _git(repo, "rev-parse", "HEAD").strip()

        def _failing(job, checkpoint_id, data_dir, workspace_root=None):
            return event_replay.ResumeResult(
                checkpoint_id=checkpoint_id, resume_mode="from_apply",
                resumed=True, tests_passed=False,
            )

        monkeypatch.setattr(event_replay, "execute_resume_from_apply", _failing)
        first = _resume(interrupted, capsys)
        assert first["worktrees"][0]["cleanup_status"] == "retained"

        # Second resume: tests pass this time.
        seen: dict = {}

        def _passing(job, checkpoint_id, data_dir, workspace_root=None):
            seen["root"] = str(workspace_root)
            seen["content"] = (Path(workspace_root) / "a.txt").read_text()
            return event_replay.ResumeResult(
                checkpoint_id=checkpoint_id, resume_mode="from_apply",
                resumed=True, tests_passed=True,
            )

        monkeypatch.setattr(event_replay, "execute_resume_from_apply", _passing)
        second = _resume(interrupted, capsys)

        rid = interrupted["run_id"]
        wt = second["worktrees"][0]
        assert seen["root"] == interrupted["handle"].path          # the exact path
        assert seen["content"] == "interrupted work\n"             # the work survived
        assert wt["branch"] == f"remedy/{rid}"
        assert wt["worktree_path"] == f".remedy-wt/{rid}"
        assert wt["recovered"] is True and wt["cleanup_status"] == "clean"

        # Only one remedy branch ever existed: no replacement, no copy fallback.
        branches = _git(repo, "branch", "--format=%(refname:short)").split()
        assert [b for b in branches if b.startswith("remedy/")] == [f"remedy/{rid}"]
        assert not Path(interrupted["handle"].path).exists()
        assert (interrupted["run_dir"] / "result.diff").read_text() == interrupted["expected_diff"]

        # Main checkout untouched throughout, and nothing was ever merged.
        assert _git(repo, "rev-parse", "HEAD").strip() == main_before
        assert _git(repo, "status", "--porcelain") == ""
        assert (repo / "a.txt").read_text() == "v1\n"
