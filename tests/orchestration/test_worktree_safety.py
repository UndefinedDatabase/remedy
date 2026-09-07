"""F006 safety corrections — never lose the work, never keep the lock, never copy
bytes from outside the run directory.

Covers:
* Finding 1 — a failed ``result.diff`` write must RETAIN the worktree (the run's
  changes are uncommitted, so the worktree is the only copy of them);
* Finding 3 — ``worktrees.remove()`` releases its lock on every exit, however it
  fails, and never claims a clean cleanup it did not achieve;
* Finding 4 — the evidence exporter contains the diff source before copying a
  single byte (no traversal, no absolute path, no symlink, hash and size checked).

Temporary git repositories and fake providers only. No provider call is made.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from packages.orchestration import job_evidence as JE
from packages.orchestration import worktrees as W
from packages.orchestration.artifact_contract_gate import check_worktree_artifacts
from packages.orchestration.data_paths import run_dir
from packages.orchestration.job_evidence import _resolve_result_diff_source
from packages.orchestration.pingpong_loop import (
    load_run,
    run_pingpong,
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
    (r / "a.txt").write_text("v1\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "init")
    return r


class _WritingProvider:
    def __init__(self, holder: dict, content: str = "changed\n"):
        self._holder = holder
        self._content = content

    def build(self, prompt, **kw):
        target = self._holder.get("path") or ""
        assert target, "fake builder has no worktree to write into"
        (Path(target) / "a.txt").write_text(self._content)
        return BuilderOutput(summary="edited", files_changed=["a.txt"], provider="fake")

    def review(self, prompt, **kw):
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok",
                              provider="fake")


def _run_with_broken_diff(repo, monkeypatch, content="precious work\n"):
    holder: dict = {}
    real_create = W.create

    def spy(job, r):
        h = real_create(job, r)
        holder["path"] = h.path
        return h

    monkeypatch.setattr(W, "create", spy)

    def boom(handle, out_path):
        raise OSError("disk full")

    monkeypatch.setattr(W, "write_result_diff", boom)
    prov = _WritingProvider(holder, content)
    res = run_pingpong("goal", str(repo), builder_provider=prov, reviewer_provider=prov,
                       builder_name="fake", reviewer_name="fake", max_rounds=1)
    return res, Path(holder["path"])


# ---------------------------------------------------------------------------
# Finding 1 — a failed diff write must never destroy the only copy of the work
# ---------------------------------------------------------------------------

class TestDiffWriteFailureRetainsWork:
    def test_worktree_and_changes_survive(self, repo, monkeypatch):
        res, path = _run_with_broken_diff(repo, monkeypatch)
        assert path.is_dir()
        assert (path / "a.txt").read_text() == "precious work\n"

    def test_worktree_stays_registered_and_branch_remains(self, repo, monkeypatch):
        res, path = _run_with_broken_diff(repo, monkeypatch)
        assert W._worktree_registered(repo, path)
        assert len(W.list_worktrees(repo)) == 2          # main + retained worktree
        assert W._branch_exists(repo, res.worktree_branch)

    def test_persisted_status_is_recoverable_not_clean(self, repo, monkeypatch):
        res, _ = _run_with_broken_diff(repo, monkeypatch)
        wt = load_run(res.run_id)["worktree"]
        assert wt["cleanup_status"] == "failed_recoverable"
        assert wt["cleanup_status"] != "clean"
        assert "disk full" in wt["result_diff_error"]
        assert wt["result_diff"] is None
        # branch, path, base and head are all preserved for the recovery.
        assert wt["branch"] == res.worktree_branch
        assert wt["path"] == f".remedy-wt/{res.run_id}"
        assert wt["base_commit"] and wt["head"]

    def test_lock_is_claimable_by_recovery(self, repo, monkeypatch):
        res, _ = _run_with_broken_diff(repo, monkeypatch)
        rec = W.recover(res.run_id, repo)                # would raise if locked
        assert rec is not None and rec.branch == res.worktree_branch
        W.release_lock(rec)

    def test_find_recoverable_runs_sees_it(self, repo, monkeypatch):
        from packages.orchestration.worktree_resume import find_recoverable_runs
        res, _ = _run_with_broken_diff(repo, monkeypatch)
        # The run record carries no job id here, so match on the run itself.
        data = load_run(res.run_id)
        assert data["worktree"]["cleanup_status"] in (
            __import__("packages.orchestration.worktree_resume", fromlist=["x"])
            .RECOVERABLE_STATES
        )
        data["job_id"] = "job-x"
        (run_dir(res.run_id) / "result.json").write_text(
            json.dumps(data, indent=2)
        )
        found = [d["run_id"] for d in find_recoverable_runs("job-x")]
        assert found == [res.run_id]

    def test_resume_regenerates_the_missing_diff_then_cleans(self, repo, monkeypatch):
        from packages.orchestration.worktree_resume import resume_worktree_run
        real_write = W.write_result_diff
        res, path = _run_with_broken_diff(repo, monkeypatch)
        monkeypatch.setattr(W, "write_result_diff", real_write)   # disk healthy again

        out = resume_worktree_run(res.run_id)
        assert out.recovered is True
        diff = (run_dir(res.run_id) / "result.diff").read_text()
        assert "precious work" in diff
        # Only NOW is the physical worktree removed — and the branch is kept.
        assert not path.exists()
        assert len(W.list_worktrees(repo)) == 1
        assert W._branch_exists(repo, res.worktree_branch)
        assert load_run(res.run_id)["worktree"]["cleanup_status"] == "clean"
        assert _git(repo, "status", "--porcelain") == ""


# ---------------------------------------------------------------------------
# Finding 3 — remove() always releases its lock, never lies about cleanup
# ---------------------------------------------------------------------------

class TestRemoveAlwaysReleasesItsLock:
    @pytest.mark.parametrize("stage", [
        "inventory", "worktree_remove", "prune", "final_check", "rmtree",
    ])
    def test_injected_failure_still_releases_the_lock(self, repo, monkeypatch, stage):
        other = W.create("otherjob", repo)               # a bystander run
        (Path(other.path) / "a.txt").write_text("other job work\n")

        h = W.create("job1", repo)
        (Path(h.path) / "a.txt").write_text("job1 work\n")

        calls = {"n": 0}
        real_git = W._git
        real_registered = W._worktree_registered

        if stage == "inventory":
            def bad_registered(root, path):
                raise W.WorktreeError("inventory broken")
            monkeypatch.setattr(W, "_worktree_registered", bad_registered)
        elif stage == "final_check":
            def flaky_registered(root, path):
                calls["n"] += 1
                if calls["n"] > 1:               # the post-removal verification
                    raise W.WorktreeError("inventory broken")
                return real_registered(root, path)
            monkeypatch.setattr(W, "_worktree_registered", flaky_registered)
        elif stage in ("worktree_remove", "prune"):
            want = "remove" if stage == "worktree_remove" else "prune"

            def bad_git(repo_, *args, check=True):
                if args[:1] == ("worktree",) and len(args) > 1 and args[1] == want:
                    raise W.WorktreeError(f"git worktree {want} exploded")
                return real_git(repo_, *args, check=check)
            monkeypatch.setattr(W, "_git", bad_git)
        else:                                    # rmtree
            import shutil

            def skip_remove(repo_, *args, check=True):
                # git leaves the directory in place; the physical delete then fails.
                if args[:2] == ("worktree", "remove"):
                    return ""
                return real_git(repo_, *args, check=check)

            def bad_rmtree(p):
                raise OSError("permission denied")

            monkeypatch.setattr(W, "_git", skip_remove)
            monkeypatch.setattr(shutil, "rmtree", bad_rmtree)

        res = W.remove(h)

        assert res["cleanup_status"] == "failed"        # never a false "clean"
        assert res["cleanup_error"]
        monkeypatch.undo()

        # The lock is claimable again, so recovery can still reach the worktree.
        again = W.recover("job1", repo)
        assert again is not None
        # The bystander's worktree and content are untouched.
        assert (Path(other.path) / "a.txt").read_text() == "other job work\n"
        W.remove(again)
        W.remove(other)

    def test_a_successful_remove_still_reports_clean(self, repo):
        h = W.create("job1", repo)
        res = W.remove(h)
        assert res["cleanup_status"] == "clean" and res["cleanup_error"] == ""
        assert W.create("job1", repo).branch == "remedy/job1"   # lock free

    def test_retain_for_recovery_keeps_the_worktree_but_frees_the_lock(self, repo):
        h = W.create("job1", repo)
        (Path(h.path) / "a.txt").write_text("kept\n")
        res = W.retain_for_recovery(h, "diff not persisted")
        assert res["cleanup_status"] == "failed_recoverable"
        assert res["worktree_retained"] is True
        assert Path(h.path).is_dir()
        assert W._worktree_registered(repo, Path(h.path))
        rec = W.recover("job1", repo)                 # lock is free
        assert rec is not None
        assert (Path(rec.path) / "a.txt").read_text() == "kept\n"
        W.remove(rec)


# ---------------------------------------------------------------------------
# Finding 4 — contain the diff source before copying any bytes
# ---------------------------------------------------------------------------

def _recorded(data: bytes, path: str = "result.diff") -> dict:
    return {"path": path, "sha256": hashlib.sha256(data).hexdigest(),
            "size_bytes": len(data)}


class _Task:
    task_id = "T001"
    run_id = "run1"
    status = "done"


def _run_dir_with(tmp_path, monkeypatch, data: bytes = b"diff --git a/a b/a\n") -> Path:
    runs = run_dir("run1")
    runs.mkdir(parents=True, exist_ok=True)
    (runs / "result.diff").write_bytes(data)
    return runs


class TestDiffSourceContainment:
    def test_traversal_path_is_rejected(self, tmp_path, monkeypatch):
        run_dir = _run_dir_with(tmp_path, monkeypatch)
        secret = run_dir.parent.parent / "secret.txt"
        secret.write_bytes(b"TOPSECRET\n")
        src, err = _resolve_result_diff_source(
            run_dir, _recorded(b"TOPSECRET\n", "../../secret.txt"))
        assert src is None
        assert "escapes the run directory" in err

    def test_absolute_path_is_rejected(self, tmp_path, monkeypatch):
        run_dir = _run_dir_with(tmp_path, monkeypatch)
        secret = tmp_path / "secret"
        secret.write_bytes(b"TOPSECRET\n")
        src, err = _resolve_result_diff_source(
            run_dir, _recorded(b"TOPSECRET\n", str(secret)))
        assert src is None
        assert "not a relative path" in err

    def test_symlink_named_result_diff_is_rejected(self, tmp_path, monkeypatch):
        run_dir = _run_dir_with(tmp_path, monkeypatch)
        secret = tmp_path / "secret"
        secret.write_bytes(b"TOPSECRET\n")
        (run_dir / "result.diff").unlink()
        (run_dir / "result.diff").symlink_to(secret)
        src, err = _resolve_result_diff_source(run_dir, _recorded(b"TOPSECRET\n"))
        assert src is None
        assert "symlink" in err

    def test_nested_path_is_rejected_as_non_canonical(self, tmp_path, monkeypatch):
        run_dir = _run_dir_with(tmp_path, monkeypatch)
        (run_dir / "sub").mkdir()
        (run_dir / "sub" / "result.diff").write_bytes(b"x\n")
        src, err = _resolve_result_diff_source(
            run_dir, _recorded(b"x\n", "sub/result.diff"))
        assert src is None
        assert "canonical" in err

    def test_hash_mismatch_is_rejected(self, tmp_path, monkeypatch):
        run_dir = _run_dir_with(tmp_path, monkeypatch, b"real\n")
        rec = _recorded(b"real\n")
        rec["sha256"] = "0" * 64
        src, err = _resolve_result_diff_source(run_dir, rec)
        assert src is None and "sha256" in err

    def test_size_mismatch_is_rejected(self, tmp_path, monkeypatch):
        run_dir = _run_dir_with(tmp_path, monkeypatch, b"real\n")
        rec = _recorded(b"real\n")
        rec["size_bytes"] = 999
        src, err = _resolve_result_diff_source(run_dir, rec)
        assert src is None and "size" in err

    def test_canonical_source_is_accepted(self, tmp_path, monkeypatch):
        run_dir = _run_dir_with(tmp_path, monkeypatch, b"real diff\n")
        src, err = _resolve_result_diff_source(run_dir, _recorded(b"real diff\n"))
        assert err == ""
        assert src == run_dir / "result.diff"


class TestExporterCopiesNoExternalBytes:
    def _export(self, tmp_path, run_data) -> tuple[Path, dict]:
        out = tmp_path / "export"
        task_out = out / "task_runs" / "T001"
        task_out.mkdir(parents=True)
        written: dict[str, str] = {}
        JE._write_task_worktree_evidence(
            _Task(), run_data, task_out, "task_runs/T001", written)
        return task_out, written

    def _run_data(self, rd) -> dict:
        return {"worktree": {
            "isolation_mode": "worktree", "branch": "remedy/run1",
            "path": ".remedy-wt/run1", "base_commit": "abc", "head": "abc",
            "cleanup_status": "clean", "cleanup_error": "",
            "result_diff": rd, "result_diff_error": "",
        }}

    def test_traversal_source_copies_nothing(self, tmp_path, monkeypatch):
        run_dir = _run_dir_with(tmp_path, monkeypatch)
        secret = run_dir.parent.parent / "secret.txt"
        secret.write_bytes(b"TOPSECRET\n")

        task_out, written = self._export(
            tmp_path, self._run_data(_recorded(b"TOPSECRET\n", "../../secret.txt")))

        assert not (task_out / "result.diff").exists()
        assert "task_runs/T001/result.diff" not in written
        doc = json.loads((task_out / "worktree.json").read_text())
        assert doc["result_diff"] is None
        assert "escapes the run directory" in doc["result_diff_error"]
        # No external bytes anywhere in the exported evidence.
        for p in task_out.rglob("*"):
            if p.is_file():
                assert b"TOPSECRET" not in p.read_bytes()

    def test_symlink_source_copies_nothing(self, tmp_path, monkeypatch):
        run_dir = _run_dir_with(tmp_path, monkeypatch)
        secret = tmp_path / "secret"
        secret.write_bytes(b"TOPSECRET\n")
        (run_dir / "result.diff").unlink()
        (run_dir / "result.diff").symlink_to(secret)

        task_out, written = self._export(
            tmp_path, self._run_data(_recorded(b"TOPSECRET\n")))
        assert not (task_out / "result.diff").exists()
        doc = json.loads((task_out / "worktree.json").read_text())
        assert doc["result_diff"] is None and "symlink" in doc["result_diff_error"]

    def test_tampered_source_copies_nothing(self, tmp_path, monkeypatch):
        run_dir = _run_dir_with(tmp_path, monkeypatch, b"real\n")
        rec = _recorded(b"real\n")
        (run_dir / "result.diff").write_bytes(b"tampered\n")   # bytes changed

        task_out, _ = self._export(tmp_path, self._run_data(rec))
        assert not (task_out / "result.diff").exists()
        doc = json.loads((task_out / "worktree.json").read_text())
        assert "sha256" in doc["result_diff_error"]

    def test_valid_source_is_exported_and_passes_the_contract(self, tmp_path, monkeypatch):
        data = b"diff --git a/a.txt b/a.txt\n+ok\n"
        _run_dir_with(tmp_path, monkeypatch, data)

        task_out, written = self._export(tmp_path, self._run_data(_recorded(data)))
        assert (task_out / "result.diff").read_bytes() == data
        assert "task_runs/T001/result.diff" in written

        # A worktree job must ALSO export its root hand-off; the contract requires
        # both layers, so add it before asserting the bundle passes.
        ev = task_out.parent.parent
        (ev / "result.diff").write_bytes(data)
        (ev / "worktree.json").write_text(json.dumps({
            "isolation_mode": "worktree", "branch": "remedy/job-1",
            "path": ".remedy-wt/job-1", "base_commit": "abc", "head": "abc",
            "cleanup_status": "clean", "auto_merged": False,
            "result_diff": {"path": "result.diff",
                            "sha256": hashlib.sha256(data).hexdigest(),
                            "size_bytes": len(data)},
            "handoff_coverage": {
                "verdict": "PASS",
                "root_changed_files": ["a.txt"],
                "reviewed_task_files": ["a.txt"],
                "unexpected_root_files": [], "missing_root_files": [],
            },
        }, indent=2))

        check = check_worktree_artifacts(str(ev))
        assert check["verdict"] == "PASS" and check["diffs_verified"] == 2
