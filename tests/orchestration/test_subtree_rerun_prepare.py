"""F029 T002 (round 2) — the rerun preparation: admission, the fold and the
per-task model (DECISION F029 D2).

``TestS2Fields`` and ``TestFoldSubtreeRerun`` exercise the pure pieces directly.
``TestPrepareSubtreeRerun`` drives ``prepare_subtree_rerun`` end to end through
``run_job`` with fake providers, exactly as ``test_job_worktree_integration.py``
drives ``run_job`` itself, and its refusals. No provider is ever invoked.
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest

from packages.orchestration import pingpong_job as PJ
from packages.orchestration import subtree_rerun as SR
from packages.orchestration import worktrees as W
from packages.orchestration.data_paths import job_evidence_dir, job_record_path
from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_COMPLETED,
    JOB_PAUSED,
    JOB_PLANNED,
    JOB_RUNNING,
    job_worktree_id,
    load_job_plan,
    parse_job_file,
    run_job,
    save_job_plan,
)
from packages.orchestration.pingpong_loop import load_run
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


JOB_TEXT_3 = """# Three-task job

## Task 1 — create task1.txt

Create `task1.txt`.

## Task 2 — create task2.txt

Create `task2.txt`.

## Task 3 — create task3.txt

Create `task3.txt`.
"""


class _NamedFileBuilder:
    """Fake Builder: writes the ``taskN.txt`` file the composed prompt names.

    Prompt-driven, not call-count-driven, so it writes the SAME file whichever
    task runs it and however many times — the original run and a later rerun
    of the same task both land on the file that task's own title names.
    """

    def __init__(self, cwd_holder: dict):
        self._cwd = cwd_holder
        self.calls = 0

    def build(self, prompt, **kw):
        self.calls += 1
        ws = Path(self._cwd["path"])
        name = re.search(r"task\d+\.txt", prompt).group(0)
        (ws / name).write_text(f"{name} attempt {self.calls}\n")
        return BuilderOutput(summary=f"wrote {name}", files_changed=[name], provider="fake")

    def review(self, prompt, **kw):
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok", provider="fake")


def _run_three_task_job(repo: Path, monkeypatch, prov: _NamedFileBuilder | None = None, **kw):
    job = parse_job_file(JOB_TEXT_3, str(repo))
    holder: dict = {}
    real_create = W.create

    def spy(job_id, r):
        h = real_create(job_id, r)
        holder["path"] = h.path
        return h

    monkeypatch.setattr(W, "create", spy)
    prov = prov or _NamedFileBuilder(holder)
    prov._cwd = holder   # the spy's holder, whichever builder instance we were given
    done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                   builder_name="fake", reviewer_name="fake", max_rounds=1, **kw)
    return done


# ---------------------------------------------------------------------------
# S2 — the new fields survive a save/load roundtrip
# ---------------------------------------------------------------------------

class TestS2Fields:
    def test_every_new_field_set_survives_save_and_load(self, tmp_path):
        task = PJ.TaskEntry(task_id="T1", attempt=3,
                            attempts=[{"attempt": 1, "status": "pending"}],
                            model_override="claude-x")
        job = PJ.JobPlan(job_id="f029fieldstest", repo_path=str(tmp_path), tasks=[task],
                         reruns=[{"rerun_id": "rerun-1"}])

        save_job_plan(job)
        loaded = load_job_plan(job.job_id)

        assert loaded.reruns == [{"rerun_id": "rerun-1"}]
        assert loaded.tasks[0].attempt == 3
        assert loaded.tasks[0].attempts == [{"attempt": 1, "status": "pending"}]
        assert loaded.tasks[0].model_override == "claude-x"

    def test_a_record_without_the_four_keys_loads_defaults(self, tmp_path):
        job = PJ.JobPlan(job_id="f029legacytest", repo_path=str(tmp_path),
                         tasks=[PJ.TaskEntry(task_id="T1")])
        path = save_job_plan(job)
        data = json.loads(path.read_text())
        del data["reruns"]
        for t in data["tasks"]:
            del t["attempt"]
            del t["attempts"]
            del t["model_override"]
        path.write_text(json.dumps(data))

        loaded = load_job_plan(job.job_id)

        assert loaded.reruns == []
        assert loaded.tasks[0].attempt == 1
        assert loaded.tasks[0].attempts == []
        assert loaded.tasks[0].model_override == ""


# ---------------------------------------------------------------------------
# S4 — the fold, over synthetic entries
# ---------------------------------------------------------------------------

def _reset(subtree, *, root_task_id="T2", base_commit="base123", reset_commit="reset456",
          paths=("a.py",), exact=True, pre_task_tree_equal=None):
    return {
        "root_task_id": root_task_id,
        "subtree": list(subtree),
        "base_commit": base_commit,
        "reset_commit": reset_commit,
        "paths": list(paths),
        "exact": exact,
        "proof": {"paths_checked": len(paths), "paths_equal": True, "tree_equals_base": exact},
        "pre_task_tree_equal": pre_task_tree_equal,
    }


NOW = datetime(2026, 9, 27, 12, 0, 0, tzinfo=timezone.utc)


class TestFoldSubtreeRerun:
    def test_attempt_record_and_every_cleared_field(self):
        t2 = PJ.TaskEntry(task_id="T2", status=PJ.TASK_APPLIED, run_id="run-1",
                          worktree_commit="c1", final_status="passed",
                          final_status_detail="", reviewer_verdict="pass", test_passed=True,
                          output_artifact_ids=["a1"], model_override="old-model",
                          repair_rounds_used=2, tripped_limit="", error="",
                          task_start_tree="tree1", task_start_tree_ref="ref1",
                          task_start_recorded_at="2026-09-01T00:00:00+00:00",
                          task_attempt_state="complete", attempt=1)
        job = PJ.JobPlan(job_id="J1", tasks=[t2])
        reset = _reset(["T2"])

        record = SR.fold_subtree_rerun(
            job, reset, rerun_id="rerun-1", model_override="new-model", actor="operator",
            now=NOW, moved_streams={"T2": "rerun_attempts/T2/attempt-1"},
        )

        assert t2.attempts == [{
            "attempt": 1,
            "status": PJ.TASK_APPLIED,
            "final_status": "passed",
            "reviewer_verdict": "pass",
            "test_passed": True,
            "run_id": "run-1",
            "worktree_commit": "c1",
            "model_override": "old-model",
            "output_artifact_ids": ["a1"],
            "stream_evidence": "rerun_attempts/T2/attempt-1",
            "rerun_id": "rerun-1",
            "ended_at": NOW.isoformat(),
        }]
        assert t2.attempt == 2
        assert t2.status == PJ.TASK_PENDING
        assert t2.model_override == "new-model"
        assert t2.run_id == ""
        assert t2.final_status == ""
        assert t2.final_status_detail == ""
        assert t2.reviewer_verdict == ""
        assert t2.error == ""
        assert t2.task_start_tree == ""
        assert t2.task_start_tree_ref == ""
        assert t2.task_start_recorded_at == ""
        assert t2.task_attempt_state == ""
        assert t2.worktree_commit == ""
        assert t2.tripped_limit == ""
        assert t2.safe_diff_files == []
        assert t2.output_artifact_ids == []
        assert t2.test_passed is None
        assert t2.apply_manifest is None
        assert t2.proof_summary is None
        assert t2.repair_rounds_used == 0
        assert record["rerun_id"] == "rerun-1"

    def test_never_run_pending_task_keeps_attempt_one_and_no_record(self):
        t2 = PJ.TaskEntry(task_id="T2", status=PJ.TASK_PENDING)
        job = PJ.JobPlan(job_id="J1", tasks=[t2])
        reset = _reset(["T2"])

        SR.fold_subtree_rerun(job, reset, rerun_id="rerun-1", model_override="", actor="a",
                              now=NOW, moved_streams={})

        assert t2.attempts == []
        assert t2.attempt == 1
        assert t2.status == PJ.TASK_PENDING

    def test_skipped_outside_task_restored_applied_one_is_not(self):
        t2 = PJ.TaskEntry(task_id="T2", status=PJ.TASK_PENDING)
        t3 = PJ.TaskEntry(task_id="T3", status=PJ.TASK_SKIPPED)
        t4 = PJ.TaskEntry(task_id="T4", status=PJ.TASK_APPLIED)
        job = PJ.JobPlan(job_id="J1", tasks=[t2, t3, t4])
        reset = _reset(["T2"])

        record = SR.fold_subtree_rerun(job, reset, rerun_id="rerun-1", model_override="",
                                       actor="a", now=NOW, moved_streams={})

        assert t3.status == PJ.TASK_PENDING
        assert t4.status == PJ.TASK_APPLIED
        assert record["restored_pending"] == ["T3"]

    def test_completed_job_becomes_paused(self):
        t2 = PJ.TaskEntry(task_id="T2", status=PJ.TASK_PENDING)
        job = PJ.JobPlan(job_id="J1", tasks=[t2], state=JOB_COMPLETED, finished_at="2026-09-01")
        reset = _reset(["T2"])

        SR.fold_subtree_rerun(job, reset, rerun_id="rerun-1", model_override="", actor="a",
                              now=NOW, moved_streams={})

        assert job.state == JOB_PAUSED
        assert job.finished_at == ""
        assert job.worktree_cleanup_status == "retained"
        assert job.worktree_cleanup_error == ""

    def test_blocked_job_stays_blocked(self):
        t2 = PJ.TaskEntry(task_id="T2", status=PJ.TASK_PENDING)
        job = PJ.JobPlan(job_id="J1", tasks=[t2], state=JOB_BLOCKED)
        reset = _reset(["T2"])

        SR.fold_subtree_rerun(job, reset, rerun_id="rerun-1", model_override="", actor="a",
                              now=NOW, moved_streams={})

        assert job.state == JOB_BLOCKED

    def test_model_block_with_and_without_an_override(self):
        t2 = PJ.TaskEntry(task_id="T2", status=PJ.TASK_PENDING)
        ec = PJ.ExecutionConfig(builder_model="configured-model")
        job = PJ.JobPlan(job_id="J1", tasks=[t2], execution_config=ec)
        reset = _reset(["T2"])

        without = SR.fold_subtree_rerun(job, reset, rerun_id="rerun-1", model_override="",
                                        actor="a", now=NOW, moved_streams={})
        assert without["model"] == {"override": "", "configured": "configured-model", "reason": ""}

        t2.status = PJ.TASK_PENDING
        with_override = SR.fold_subtree_rerun(
            job, reset, rerun_id="rerun-2", model_override="picked-model", actor="a", now=NOW,
            moved_streams={},
        )
        assert with_override["model"] == {
            "override": "picked-model", "configured": "configured-model",
            "reason": SR.HUMAN_OVERRIDE_REASON,
        }


# ---------------------------------------------------------------------------
# S5 — the preparation, end to end through `run_job`
# ---------------------------------------------------------------------------

class TestPrepareSubtreeRerunEndToEnd:
    def test_prepare_then_rerun_with_model_override(self, repo, monkeypatch):
        job = _run_three_task_job(repo, monkeypatch)
        assert job.state == JOB_COMPLETED
        job_id = job.job_id
        wt_path = W.worktree_path_for(repo, job_worktree_id(job_id))
        assert not wt_path.exists()                       # cleaned after completion
        assert W._branch_exists(str(repo), job.worktree_branch)
        # `_finalize_job_workspace` drops the checkpoint ref on a clean completion.
        assert W.resolve_checkpoint_ref(job.repo_path, job.job_initial_tree_ref) == ""

        t1_run_id, t1_commit = job.tasks[0].run_id, job.tasks[0].worktree_commit
        old_t2_run_id, old_t2_commit = job.tasks[1].run_id, job.tasks[1].worktree_commit
        old_t3_run_id, old_t3_commit = job.tasks[2].run_id, job.tasks[2].worktree_commit

        stream_dir = PJ._task_stream_dir(job_id, "T002")
        stream_dir.mkdir(parents=True)
        (stream_dir / "marker.txt").write_text("stream marker")

        result = SR.prepare_subtree_rerun(job_id, "T002", model_override="rerun-model")

        assert result["subtree"] == ["T002", "T003"]
        assert result["exact"] is True
        assert result["worktree_rematerialized"] is True

        reloaded = load_job_plan(job_id)
        assert reloaded.state == JOB_PAUSED
        r1, r2, r3 = reloaded.tasks
        assert r1.run_id == t1_run_id
        assert r1.worktree_commit == t1_commit
        assert r1.attempt == 1
        for r, old_run_id, old_commit in ((r2, old_t2_run_id, old_t2_commit),
                                          (r3, old_t3_run_id, old_t3_commit)):
            assert r.status == PJ.TASK_PENDING
            assert r.attempt == 2
            assert len(r.attempts) == 1
            assert r.attempts[0]["run_id"] == old_run_id
            assert r.attempts[0]["worktree_commit"] == old_commit
            assert r.model_override == "rerun-model"

        assert len(reloaded.reruns) == 1
        assert reloaded.reruns[0]["model"] == {
            "override": "rerun-model", "configured": "", "reason": "human_override"}
        assert reloaded.worktree_cleanup_status == "retained"
        # DECISION F029 D2: the ref completion dropped is set again, protecting the tree.
        assert (W.resolve_checkpoint_ref(job.repo_path, job.job_initial_tree_ref)
                == job.job_initial_tree)

        assert (wt_path / "task1.txt").exists()
        assert not (wt_path / "task2.txt").exists()
        assert not (wt_path / "task3.txt").exists()

        assert W.lock_is_held(str(repo), job_worktree_id(job_id)) is False

        moved = job_evidence_dir(job_id) / "rerun_attempts" / "T002" / "attempt-1" / "marker.txt"
        assert moved.read_text() == "stream marker"
        assert not stream_dir.exists()

        # Run again: T002 and T003 re-execute with the override; T001 is untouched.
        holder = {"path": str(wt_path)}
        prov2 = _NamedFileBuilder(holder)
        done2 = run_job(job_id, builder_provider=prov2, reviewer_provider=prov2,
                        builder_name="fake", reviewer_name="fake", max_rounds=1)

        assert done2.state == JOB_COMPLETED
        f1, f2, f3 = done2.tasks
        assert f1.run_id == t1_run_id
        assert f2.run_id != old_t2_run_id and f2.run_id
        assert f3.run_id != old_t3_run_id and f3.run_id

        # Old run directories are untouched.
        assert load_run(old_t2_run_id) is not None
        assert load_run(old_t3_run_id) is not None

        for new_run_id in (f2.run_id, f3.run_id):
            run = load_run(new_run_id)
            assert run["provider_evidence"]["builder_configured_model"] == "rerun-model"

        branch_commit_count = int(
            _git(repo, "rev-list", "--count", job.worktree_branch).strip())
        # init + T1 + T2(v1) + T3(v1) + reset + T2(v2) + T3(v2)
        assert branch_commit_count == 7


class TestPrepareSubtreeRerunRefusals:
    def _completed_job(self, repo, monkeypatch):
        job = _run_three_task_job(repo, monkeypatch)
        assert job.state == JOB_COMPLETED
        return job

    def _bytes(self, job_id):
        return job_record_path(job_id).read_bytes()

    def test_job_not_found(self):
        with pytest.raises(SR.SubtreeRerunRefused) as excinfo:
            SR.prepare_subtree_rerun("no-such-job", "T001")
        assert excinfo.value.code == "job_not_found"

    def test_model_invalid_leaves_job_json_untouched(self, repo, monkeypatch):
        job = self._completed_job(repo, monkeypatch)
        before = self._bytes(job.job_id)

        with pytest.raises(SR.SubtreeRerunRefused) as excinfo:
            SR.prepare_subtree_rerun(job.job_id, "T002", model_override="bad model!")

        assert excinfo.value.code == "model_invalid"
        assert self._bytes(job.job_id) == before
        assert not W.worktree_path_for(repo, job_worktree_id(job.job_id)).exists()

    def test_job_running_state_leaves_job_json_untouched(self, repo, monkeypatch):
        job = self._completed_job(repo, monkeypatch)
        job.state = JOB_RUNNING
        save_job_plan(job)
        before = self._bytes(job.job_id)

        with pytest.raises(SR.SubtreeRerunRefused) as excinfo:
            SR.prepare_subtree_rerun(job.job_id, "T002")

        assert excinfo.value.code == "job_running"
        assert self._bytes(job.job_id) == before
        assert not W.worktree_path_for(repo, job_worktree_id(job.job_id)).exists()

    def test_job_running_for_a_lock_the_test_itself_holds(self, repo, monkeypatch):
        job = self._completed_job(repo, monkeypatch)
        before = self._bytes(job.job_id)
        handle = W.create(job_worktree_id(job.job_id), job.repo_path)
        try:
            with pytest.raises(SR.SubtreeRerunRefused) as excinfo:
                SR.prepare_subtree_rerun(job.job_id, "T002")
            assert excinfo.value.code == "job_running"
            assert self._bytes(job.job_id) == before
        finally:
            W.remove(handle, keep_branch=True)

    def test_job_not_rerunnable_for_planned(self, repo, monkeypatch):
        job = self._completed_job(repo, monkeypatch)
        job.state = JOB_PLANNED
        save_job_plan(job)
        before = self._bytes(job.job_id)

        with pytest.raises(SR.SubtreeRerunRefused) as excinfo:
            SR.prepare_subtree_rerun(job.job_id, "T002")

        assert excinfo.value.code == "job_not_rerunnable"
        assert self._bytes(job.job_id) == before
        assert not W.worktree_path_for(repo, job_worktree_id(job.job_id)).exists()

    def test_task_not_committed(self, repo, monkeypatch):
        job = self._completed_job(repo, monkeypatch)
        job.tasks[1].worktree_commit = ""
        save_job_plan(job)
        before = self._bytes(job.job_id)

        with pytest.raises(SR.SubtreeRerunRefused) as excinfo:
            SR.prepare_subtree_rerun(job.job_id, "T002")

        assert excinfo.value.code == "task_not_committed"
        assert self._bytes(job.job_id) == before
        assert not W.worktree_path_for(repo, job_worktree_id(job.job_id)).exists()

    def test_worktree_drift_after_re_add_removes_the_worktree_again(self, repo, monkeypatch):
        job = self._completed_job(repo, monkeypatch)
        job.worktree_head = "f" * 40
        save_job_plan(job)
        before = self._bytes(job.job_id)
        wt_path = W.worktree_path_for(repo, job_worktree_id(job.job_id))

        with pytest.raises(SR.SubtreeRerunRefused) as excinfo:
            SR.prepare_subtree_rerun(job.job_id, "T002")

        assert excinfo.value.code == "worktree_drift"
        assert self._bytes(job.job_id) == before
        assert not wt_path.exists()


# ---------------------------------------------------------------------------
# R-1081 — the worktree lock is never left held past a failed preparation
# ---------------------------------------------------------------------------

class TestR1081Repair:
    def test_occupied_archive_destination_refuses_before_worktree_touched(self, repo, monkeypatch):
        job = _run_three_task_job(repo, monkeypatch)
        assert job.state == JOB_COMPLETED
        job_id = job.job_id
        wt_path = W.worktree_path_for(repo, job_worktree_id(job_id))

        stream_dir = PJ._task_stream_dir(job_id, "T002")
        stream_dir.mkdir(parents=True)
        (stream_dir / "marker.txt").write_text("stream marker")

        occupied = job_evidence_dir(job_id) / "rerun_attempts" / "T002" / "attempt-1"
        occupied.mkdir(parents=True)
        (occupied / "earlier.txt").write_text("an earlier attempt's evidence")

        before = job_record_path(job_id).read_bytes()

        with pytest.raises(SR.SubtreeRerunRefused) as excinfo:
            SR.prepare_subtree_rerun(job_id, "T002")

        assert excinfo.value.code == "stream_archive_occupied"
        assert not wt_path.exists()
        assert job_record_path(job_id).read_bytes() == before
        assert stream_dir.exists()   # nothing was moved

    def test_a_failing_save_leaves_the_lock_free_and_the_error_propagating(self, repo, monkeypatch):
        job = _run_three_task_job(repo, monkeypatch)
        assert job.state == JOB_COMPLETED
        job_id = job.job_id

        def _boom(_job):
            raise OSError("disk gone")

        monkeypatch.setattr(SR, "save_job_plan", _boom)

        with pytest.raises(OSError):
            SR.prepare_subtree_rerun(job_id, "T002")

        assert W.lock_is_held(str(repo), job_worktree_id(job_id)) is False
