"""F263 T001 — the human change record: detected, certified, and written before any re-base.

Temporary git repositories only. No provider call is ever made.
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
    (r / "keep.txt").write_text("keep\n")
    (r / "edit.txt").write_text("before\n")
    (r / "gone.txt").write_text("gone\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "init")
    return r


def _hand_edit(repo: Path) -> None:
    (repo / "edit.txt").write_text("after, by hand\n")
    (repo / "new.txt").write_text("new\n")
    (repo / "gone.txt").unlink()


class TestTheLastKnownState:
    def test_a_clean_checkout_captures_its_committed_tree_and_head(self, repo):
        state = HC.capture_target_state(repo)
        assert state.tree == _git(repo, "rev-parse", "HEAD^{tree}").strip()
        assert state.head == _git(repo, "rev-parse", "HEAD").strip()

    def test_capture_includes_untracked_files_and_leaves_the_users_index_alone(self, repo):
        (repo / "staged.txt").write_text("staged\n")
        _git(repo, "add", "staged.txt")
        (repo / "untracked.txt").write_text("untracked\n")
        index_before = (repo / ".git" / "index").read_bytes()
        state = HC.capture_target_state(repo)
        assert (repo / ".git" / "index").read_bytes() == index_before
        listed = _git(repo, "ls-tree", "-r", "--name-only", state.tree).split()
        assert "untracked.txt" in listed and "staged.txt" in listed

    def test_the_state_round_trips_through_its_dict(self, repo):
        state = HC.capture_target_state(repo)
        assert HC.TargetState.from_dict(state.to_dict()) == state
        assert HC.TargetState.from_dict(None) is None
        assert HC.TargetState.from_dict({"head": "x"}) is None


class TestDetection:
    def test_an_unmoved_target_is_no_human_change(self, repo):
        state = HC.capture_target_state(repo)
        assert HC.detect_human_change(repo, state) is None

    def test_a_hand_edit_is_listed_file_by_file_with_gits_letter(self, repo):
        state = HC.capture_target_state(repo)
        _hand_edit(repo)
        change = HC.detect_human_change(repo, state)
        assert change is not None
        assert [(f.path, f.status) for f in change.files] == [
            ("edit.txt", "M"), ("gone.txt", "D"), ("new.txt", "A")]
        assert change.before == state and change.after.tree != state.tree

    def test_tool_noise_and_remedy_artifacts_alone_are_no_human_change(self, repo):
        state = HC.capture_target_state(repo)
        (repo / "__pycache__").mkdir()
        (repo / "__pycache__" / "mod.cpython-312.pyc").write_bytes(b"\0")
        (repo / "remedy-review-20260101-000000.zip").write_bytes(b"PK")
        assert HC.detect_human_change(repo, state) is None

    def test_noise_beside_a_real_edit_is_reported_apart_from_it(self, repo):
        state = HC.capture_target_state(repo)
        (repo / "edit.txt").write_text("after\n")
        (repo / "remedy-review-20260101-000000.zip").write_bytes(b"PK")
        change = HC.detect_human_change(repo, state)
        assert [f.path for f in change.files] == ["edit.txt"]
        assert change.ignored_operational == ("remedy-review-20260101-000000.zip",)


class TestTheRecord:
    def _record(self, repo) -> Path:
        state = HC.capture_target_state(repo)
        _hand_edit(repo)
        change = HC.detect_human_change(repo, state)
        return HC.write_human_change_record("job-1", repo, change, detected_by="test")

    def test_the_record_lives_in_the_jobs_evidence_and_verifies(self, repo):
        path = self._record(repo)
        assert path.parent == job_evidence_dir("job-1") / HC.RECORD_DIRNAME
        body = json.loads(path.read_text())
        assert body["schema"] == HC.SCHEMA and body["detected_by"] == "test"
        assert [f["path"] for f in body["files"]] == ["edit.txt", "gone.txt", "new.txt"]
        assert HC.verify_human_change_record(path) == []

    def test_the_diff_carries_the_hand_edit_itself(self, repo):
        path = self._record(repo)
        diff = (path.parent / json.loads(path.read_text())["diff"]["path"]).read_text()
        assert "+after, by hand" in diff and "-before" in diff and "+new" in diff

    def test_a_changed_diff_byte_fails_verification(self, repo):
        path = self._record(repo)
        diff = path.parent / json.loads(path.read_text())["diff"]["path"]
        diff.write_bytes(diff.read_bytes().replace(b"by hand", b"by hanD"))
        assert HC.verify_human_change_record(path) == ["diff sha256 does not match the record"]

    def test_a_changed_record_field_fails_verification(self, repo):
        path = self._record(repo)
        body = json.loads(path.read_text())
        body["files"] = body["files"][:1]
        path.write_text(json.dumps(body))
        assert HC.verify_human_change_record(path) == ["record_sha256 does not match the record"]

    def test_the_same_transition_is_certified_once(self, repo):
        state = HC.capture_target_state(repo)
        _hand_edit(repo)
        first = HC.write_human_change_record(
            "job-1", repo, HC.detect_human_change(repo, state), detected_by="test")
        before = first.read_bytes()
        again = HC.write_human_change_record(
            "job-1", repo, HC.detect_human_change(repo, state), detected_by="test")
        assert again == first and first.read_bytes() == before


class TestAbsorb:
    def test_the_record_is_on_disk_before_the_rebase_runs(self, repo):
        state = HC.capture_target_state(repo)
        _hand_edit(repo)
        seen: list[bool] = []

        def rebase(change):
            folder = job_evidence_dir("job-1") / HC.RECORD_DIRNAME
            seen.append(HC.verify_human_change_record(
                folder / f"{HC.record_id_for(change)}.json") == [])

        outcome = HC.absorb("job-1", repo, state, detected_by="test", rebase=rebase)
        assert outcome.status == "absorbed" and seen == [True]

    def test_a_failed_rebase_leaves_the_record_and_the_hand_edit(self, repo):
        state = HC.capture_target_state(repo)
        _hand_edit(repo)

        def rebase(change):
            raise RuntimeError("rebase failed")

        with pytest.raises(RuntimeError, match="rebase failed"):
            HC.absorb("job-1", repo, state, detected_by="test", rebase=rebase)
        records = sorted((job_evidence_dir("job-1") / HC.RECORD_DIRNAME).glob("*.json"))
        assert len(records) == 1 and HC.verify_human_change_record(records[0]) == []
        assert (repo / "edit.txt").read_text() == "after, by hand\n"
        assert not (repo / "gone.txt").exists()

    def test_an_unmoved_target_calls_no_rebase_and_writes_nothing(self, repo):
        state = HC.capture_target_state(repo)
        outcome = HC.absorb("job-1", repo, state, detected_by="test",
                            rebase=lambda change: pytest.fail("rebase called"))
        assert outcome.status == "unchanged"
        assert not (job_evidence_dir("job-1") / HC.RECORD_DIRNAME).exists()


class TestTheJobRecordsItsLastKnownState:
    def test_a_git_job_workspace_records_the_target_state_behind_a_ref(self, repo):
        job = PJ.parse_job_file("# One\n\n## Task 1 — write\n\nWrite one.txt.\n", str(repo))
        _, handle = PJ._create_job_workspace(job)
        try:
            last = job.target_last_known
            assert last["tree"] == HC.capture_target_state(repo).tree
            assert last["ref"].endswith("/" + HC.LAST_KNOWN_REF_NAME)
            assert W.resolve_checkpoint_ref(repo, last["ref"]) == last["tree"]
            again = PJ._import_job(json.loads(json.dumps(PJ._export_job(job))))
            assert again.target_last_known == last
        finally:
            W.release_lock(handle)

    def test_the_final_hand_off_keeps_the_last_known_ref(self, repo):
        job = PJ.parse_job_file("# One\n\n## Task 1 — write\n\nWrite one.txt.\n", str(repo))
        _, handle = PJ._create_job_workspace(job)
        try:
            assert PJ._drop_checkpoint_refs(job) == ""
            ref = job.target_last_known["ref"]
            assert W.resolve_checkpoint_ref(repo, ref) == job.target_last_known["tree"]
        finally:
            W.release_lock(handle)
