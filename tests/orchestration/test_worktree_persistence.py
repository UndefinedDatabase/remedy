"""F006 correction, Finding 1 — the worktree hand-off must be DURABLE.

A run's worktree metadata and its deterministic ``result.diff`` have to survive
``_persist_run()``/``load_run()``, reach the job evidence export, and be
re-verifiable byte-for-byte by the artifact contract. Temporary git repositories
and fake providers only: no provider call is ever made.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from packages.orchestration import worktrees as W
from packages.orchestration.artifact_contract_gate import (
    build_artifact_contract_gate,
    check_worktree_artifacts,
)
from packages.orchestration.data_paths import run_dir
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
    """Fake Builder/Reviewer. Writes into the worktree the loop created."""

    def __init__(self, holder: dict, content: str = "changed\n"):
        self._holder = holder
        self._content = content

    def build(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume: str | None = None):
        target = self._holder.get("path") or ""
        assert target, "fake builder has no worktree to write into"
        (Path(target) / "a.txt").write_text(self._content)
        return BuilderOutput(summary="edited a.txt", files_changed=["a.txt"],
                             provider="fake")

    def review(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume: str | None = None):
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok",
                              provider="fake")


def _run(monkeypatch, repo: Path, *, job_id: str = "", content: str = "changed\n"):
    holder: dict = {}
    real_create = W.create

    def spy(job, r):
        h = real_create(job, r)
        holder["path"] = h.path
        return h

    monkeypatch.setattr(W, "create", spy)
    prov = _WritingProvider(holder, content)
    return run_pingpong(
        "goal", str(repo), builder_provider=prov, reviewer_provider=prov,
        builder_name="fake", reviewer_name="fake", max_rounds=1, job_id=job_id,
    )


# ---------------------------------------------------------------------------
# 1-2. The persisted run record carries the complete hand-off
# ---------------------------------------------------------------------------

class TestPersistedRunRecord:
    def test_load_run_contains_every_worktree_field(self, repo, monkeypatch):
        res = _run(monkeypatch, repo)
        data = load_run(res.run_id)
        assert data is not None

        wt = data["worktree"]
        assert data["isolation_mode"] == "worktree"
        assert wt["isolation_mode"] == "worktree"
        assert wt["branch"] == res.worktree_branch == f"remedy/{res.run_id}"
        assert wt["path"] == res.worktree_path == f".remedy-wt/{res.run_id}"
        assert wt["base_commit"] == res.worktree_base_commit
        assert wt["head"] == res.worktree_head
        assert wt["lock_id"] == f"{res.run_id}.lock"
        assert wt["cleanup_status"] == "clean"
        assert wt["cleanup_error"] == ""
        assert wt["result_diff"]["path"] == "result.diff"
        assert wt["result_diff"]["sha256"] == res.result_diff_sha256
        assert wt["result_diff"]["size_bytes"] == res.result_diff_size_bytes

    def test_no_private_absolute_path_is_persisted(self, repo, monkeypatch):
        res = _run(monkeypatch, repo)
        wt = load_run(res.run_id)["worktree"]
        for value in wt.values():
            assert not str(value).startswith("/")

    def test_result_diff_reference_resolves_and_hash_and_size_match(self, repo, monkeypatch):
        res = _run(monkeypatch, repo)
        wt = load_run(res.run_id)["worktree"]

        diff_file = run_dir(res.run_id) / wt["result_diff"]["path"]
        data = diff_file.read_bytes()
        assert hashlib.sha256(data).hexdigest() == wt["result_diff"]["sha256"]
        assert len(data) == wt["result_diff"]["size_bytes"]
        assert b"+changed" in data

    def test_cleanup_status_is_never_clean_before_cleanup(self, repo, monkeypatch):
        # A retained run still owns its worktree: it must NOT claim a clean cleanup.
        holder: dict = {}
        real_create = W.create

        def spy(job, r):
            h = real_create(job, r)
            holder["path"] = h.path
            return h

        monkeypatch.setattr(W, "create", spy)
        prov = _WritingProvider(holder)
        res = run_pingpong("goal", str(repo), builder_provider=prov,
                           reviewer_provider=prov, builder_name="fake",
                           reviewer_name="fake", max_rounds=1, keep_staging=True)
        assert load_run(res.run_id)["worktree"]["cleanup_status"] == "retained"
        assert Path(res.staging_path).is_dir()

    def test_diff_persistence_error_retains_the_worktree_and_the_work(
        self, repo, monkeypatch,
    ):
        # Replaces the earlier assertion that a diff-write failure still ended in a
        # "clean" cleanup: the run's changes are UNCOMMITTED, so removing the
        # worktree with no persisted diff would destroy the only copy of the work.
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
        prov = _WritingProvider(holder, "work worth keeping\n")
        res = run_pingpong("goal", str(repo), builder_provider=prov,
                           reviewer_provider=prov, builder_name="fake",
                           reviewer_name="fake", max_rounds=1)

        wt = load_run(res.run_id)["worktree"]
        assert "disk full" in wt["result_diff_error"]
        assert wt["result_diff"] is None                  # no diff is claimed
        assert wt["cleanup_status"] == "failed_recoverable"   # never "clean"
        # The physical worktree — and the work inside it — survived.
        path = Path(holder["path"])
        assert path.is_dir()
        assert (path / "a.txt").read_text() == "work worth keeping\n"
        assert W._worktree_registered(repo, path)
        assert W._branch_exists(repo, wt["branch"])
        # The lock was released, so recovery can claim it.
        rec = W.recover(res.run_id, repo)
        assert rec is not None and rec.branch == wt["branch"]
        W.remove(rec)


# ---------------------------------------------------------------------------
# 7. Copy fallback must not be asked for a worktree diff
# ---------------------------------------------------------------------------

class TestCopyFallback:
    def test_copy_mode_reports_copy_and_owes_no_diff(self, tmp_path, monkeypatch):
        plain = tmp_path / "plain"          # NOT a git repository
        plain.mkdir()
        (plain / "a.txt").write_text("v1\n")

        class _Noop:
            def build(self, prompt, **kw):
                return BuilderOutput(summary="noop", files_changed=[], provider="fake")

            def review(self, prompt, **kw):
                return ReviewerOutput(verdict="pass", confidence="high",
                                      summary="ok", provider="fake")

        prov = _Noop()
        res = run_pingpong("goal", str(plain), builder_provider=prov,
                           reviewer_provider=prov, builder_name="fake",
                           reviewer_name="fake", max_rounds=1)
        wt = load_run(res.run_id)["worktree"]
        assert res.isolation_mode == "copy"
        assert wt["isolation_mode"] == "copy"
        assert wt["result_diff"] is None
        assert wt["branch"] == "" and wt["path"] == ""

    def test_copy_mode_evidence_does_not_require_a_diff(self, tmp_path):
        ev = tmp_path / "ev"
        (ev / "task_runs" / "T001").mkdir(parents=True)
        (ev / "task_runs" / "T001" / "worktree.json").write_text(json.dumps({
            "isolation_mode": "copy", "result_diff": None,
        }))
        check = check_worktree_artifacts(str(ev))
        assert check["verdict"] == "NOT_APPLICABLE"
        assert check["applicable"] is False


# ---------------------------------------------------------------------------
# 3-6. Evidence export, review ZIP, tamper and missing-diff blocking
# ---------------------------------------------------------------------------

def _root_handoff(ev: Path, data: bytes) -> None:
    """A worktree JobPlan must also export its root hand-off, or the contract blocks."""
    (ev / "result.diff").write_bytes(data)
    (ev / "worktree.json").write_text(json.dumps({
        "schema_version": "1.0.0",
        "isolation_mode": "worktree",
        "branch": "remedy/job-1", "path": ".remedy-wt/job-1",
        "base_commit": "abc", "head": "abc", "cleanup_status": "clean",
        "result_diff": {"path": "result.diff",
                        "sha256": hashlib.sha256(data).hexdigest(),
                        "size_bytes": len(data)},
        "auto_merged": False,
        "handoff_coverage": {
            "verdict": "PASS",
            "root_changed_files": ["a.txt"],
            "reviewed_task_files": ["a.txt"],
            "unexpected_root_files": [], "missing_root_files": [],
        },
    }, indent=2))


def _evidence_dir_with_diff(tmp_path, diff_text: str = "diff --git a/a.txt b/a.txt\n"):
    ev = tmp_path / "ev"
    task = ev / "task_runs" / "T001"
    task.mkdir(parents=True)
    data = diff_text.encode()
    _root_handoff(ev, data)
    (task / "result.diff").write_bytes(data)
    (task / "worktree.json").write_text(json.dumps({
        "schema_version": "1.0.0",
        "task_id": "T001",
        "run_id": "run1",
        "isolation_mode": "worktree",
        "branch": "remedy/run1",
        "worktree_path": ".remedy-wt/run1",
        "base_commit": "abc",
        "worktree_head": "abc",
        "cleanup_status": "clean",
        "result_diff": {
            "path": "result.diff",
            "sha256": hashlib.sha256(data).hexdigest(),
            "size_bytes": len(data),
        },
    }, indent=2))
    return ev, task


class TestEvidenceExport:
    def test_job_evidence_export_contains_result_diff(self, repo, monkeypatch, tmp_path):
        from packages.orchestration.job_evidence import _write_task_run_evidence

        res = _run(monkeypatch, repo)

        class _Task:
            task_id = "T001"
            run_id = res.run_id
            status = "done"

        out = tmp_path / "export"
        written: dict[str, str] = {}
        _write_task_run_evidence(_Task(), str(out), written)

        assert "task_runs/T001/result.diff" in written
        assert "task_runs/T001/worktree.json" in written
        doc = json.loads((out / "task_runs" / "T001" / "worktree.json").read_text())
        assert doc["branch"] == res.worktree_branch
        assert doc["worktree_path"] == res.worktree_path
        assert doc["base_commit"] == res.worktree_base_commit
        assert doc["worktree_head"] == res.worktree_head
        assert doc["cleanup_status"] == "clean"
        assert doc["auto_merged"] is False
        assert doc["result_diff"]["sha256"] == res.result_diff_sha256
        assert doc["result_diff"]["size_bytes"] == res.result_diff_size_bytes

        exported = (out / "task_runs" / "T001" / "result.diff").read_bytes()
        assert hashlib.sha256(exported).hexdigest() == res.result_diff_sha256

    def test_exported_diff_passes_the_artifact_contract(self, tmp_path):
        ev, _ = _evidence_dir_with_diff(tmp_path)
        check = check_worktree_artifacts(str(ev))
        assert check["verdict"] == "PASS"
        assert check["diffs_verified"] == 2          # root hand-off + task diff
        assert check["job_level_handoff"] is True
        assert check["worktree_tasks"] == ["(job)", "T001"]

    def test_review_zip_carries_the_exported_diff(self, repo, monkeypatch, tmp_path):
        # The review ZIP packs the evidence export verbatim; prove the diff is in
        # the file list that gets packed (no ZIP tooling needed to prove inclusion).
        import zipfile

        from packages.orchestration.job_evidence import _write_task_run_evidence

        res = _run(monkeypatch, repo)

        class _Task:
            task_id = "T001"
            run_id = res.run_id
            status = "done"

        out = tmp_path / "export"
        _write_task_run_evidence(_Task(), str(out), {})

        zip_path = tmp_path / "bundle.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            for p in sorted(out.rglob("*")):
                if p.is_file():
                    zf.write(p, str(p.relative_to(out)))

        with zipfile.ZipFile(zip_path) as zf:
            names = zf.namelist()
            assert "task_runs/T001/result.diff" in names
            assert "task_runs/T001/worktree.json" in names
            packed = zf.read("task_runs/T001/result.diff")
        assert hashlib.sha256(packed).hexdigest() == res.result_diff_sha256


class TestTamperBlocking:
    def test_one_byte_tamper_blocks_the_contract(self, tmp_path):
        ev, task = _evidence_dir_with_diff(tmp_path)
        data = bytearray((task / "result.diff").read_bytes())
        data[-1] ^= 0x01                                    # exactly one byte
        (task / "result.diff").write_bytes(bytes(data))

        check = check_worktree_artifacts(str(ev))
        assert check["verdict"] == "BLOCKED"
        assert check["result_diff_hash_mismatches"]
        assert check["diffs_verified"] == 1          # only the untouched root diff

    def test_tamper_blocks_the_whole_gate(self, tmp_path):
        ev, task = _evidence_dir_with_diff(tmp_path)
        (task / "result.diff").write_bytes(b"totally different bytes\n")
        gate = build_artifact_contract_gate(str(ev))
        assert gate["verdict"] == "BLOCKED"
        assert any("sha256 mismatch" in i for i in gate["issues"])

    def test_missing_diff_blocks_the_contract(self, tmp_path):
        ev, task = _evidence_dir_with_diff(tmp_path)
        (task / "result.diff").unlink()
        check = check_worktree_artifacts(str(ev))
        assert check["verdict"] == "BLOCKED"
        assert check["missing_result_diffs"] == ["task_runs/T001/result.diff"]

    def test_unreferenced_replacement_diff_is_rejected(self, tmp_path):
        ev = tmp_path / "ev"
        task = ev / "task_runs" / "T001"
        task.mkdir(parents=True)
        (task / "result.diff").write_bytes(b"planted\n")     # no worktree.json
        check = check_worktree_artifacts(str(ev))
        assert check["verdict"] == "BLOCKED"
        assert check["unreferenced_result_diffs"] == ["task_runs/T001/result.diff"]

    def test_manual_only_job_stays_not_applicable(self, tmp_path):
        ev = tmp_path / "ev"
        (ev / "task_runs" / "T001").mkdir(parents=True)
        (ev / "task_runs" / "T001" / "manifest.json").write_text("{}")
        check = check_worktree_artifacts(str(ev))
        assert check["verdict"] == "NOT_APPLICABLE"
        assert check["applicable"] is False
