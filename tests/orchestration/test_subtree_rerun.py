"""F029 T001 — subtree reset: the subtree, the walk, the refusals and the reset
with its hash proof.

Real, temporary git repositories only, each checked out on ``remedy/job-<id>``
as ``run_job`` leaves a worktree-mode job. No provider is ever invoked.
"""
from __future__ import annotations

import os
import subprocess
from collections.abc import Sequence
from pathlib import Path

import pytest

from packages.orchestration import checkpoints
from packages.orchestration import pingpong_job as PJ
from packages.orchestration import subtree_rerun as SR
from packages.orchestration import worktrees as W

JOB_ID = "subtreetestjob"
BRANCH = f"remedy/job-{JOB_ID}"


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
    _git(r, "checkout", "-q", "-b", BRANCH)
    (r / "base.txt").write_text("base\n")
    _git(r, "add", "-A")
    subprocess.run(
        ["git", "-c", "user.name=T", "-c", "user.email=t@e.com", "-c", "commit.gpgsign=false",
         "commit", "-qm", "init"],
        cwd=str(r), check=True, capture_output=True, text=True,
    )
    return r


def _snapshot(repo: Path) -> tuple[str, str, str]:
    return (
        _git(repo, "rev-parse", "HEAD").strip(),
        _git(repo, "rev-parse", "HEAD^{tree}").strip(),
        _git(repo, "status", "--porcelain"),
    )


def _land(repo: Path, job_id: str, task_id: str, *, write: dict[str, str] | None = None,
          delete: Sequence[str] = (), chmod_x: Sequence[str] = ()) -> str:
    """Land one task commit on ``repo``'s current (``remedy/``-prefixed) branch."""
    for name, content in (write or {}).items():
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    for name in delete:
        (repo / name).unlink()
    for name in chmod_x:
        path = repo / name
        path.chmod(path.stat().st_mode | 0o111)
    message = f"land {task_id}\n\n{W.REMEDY_JOB_TRAILER}: {job_id}\n{W.REMEDY_TASK_TRAILER}: {task_id}\n"
    return W.commit_job_worktree(str(repo), message)


def _land_bare(repo: Path, job_id: str, *, write: dict[str, str] | None = None) -> str:
    """Land a commit carrying only the ``Remedy-Job`` trailer — no task claims it."""
    for name, content in (write or {}).items():
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    message = f"manual edit\n\n{W.REMEDY_JOB_TRAILER}: {job_id}\n"
    return W.commit_job_worktree(str(repo), message)


def _task(task_id: str, *, planned_id: str | None = None, depends_on: Sequence[str] = (),
          status: str = PJ.TASK_PENDING, worktree_commit: str = "",
          task_start_tree: str = "") -> PJ.TaskEntry:
    inputs: dict = {}
    if planned_id is not None:
        inputs["plan"] = {"planned_id": planned_id, "depends_on": list(depends_on)}
    return PJ.TaskEntry(task_id=task_id, title=task_id, status=status, inputs=inputs,
                         worktree_commit=worktree_commit, task_start_tree=task_start_tree)


def _job(job_id: str, repo_path, tasks: Sequence[PJ.TaskEntry], worktree_head: str,
         isolation_mode: str = "worktree") -> PJ.JobPlan:
    return PJ.JobPlan(job_id=job_id, repo_path=str(repo_path), isolation_mode=isolation_mode,
                       worktree_head=worktree_head, tasks=list(tasks))


# ---------------------------------------------------------------------------
# S2 — the subtree
# ---------------------------------------------------------------------------

class TestSubtreeIds:
    def test_diamond_subtree_of_middle_and_of_root(self):
        t1 = _task("T1", planned_id="P1")
        t2 = _task("T2", planned_id="P2", depends_on=("P1",), status=PJ.TASK_APPLIED)
        t3 = _task("T3", planned_id="P3", depends_on=("P1",), status=PJ.TASK_APPLIED)
        t4 = _task("T4", planned_id="P4", depends_on=("P2", "P3"))
        t5 = _task("T5", planned_id="P5")   # independent
        tasks = [t1, t2, t3, t4, t5]

        assert SR.rerun_subtree_ids(tasks, "T2") == ["T2", "T4"]
        assert SR.rerun_subtree_ids(tasks, "T1") == ["T1", "T2", "T3", "T4"]

    def test_legacy_task_without_plan_input_chains_to_predecessor(self):
        t1 = _task("T1", planned_id="P1")
        t2 = _task("T2")   # no inputs["plan"]: depends on its predecessor, T1
        tasks = [t1, t2]

        assert SR.rerun_subtree_ids(tasks, "T1") == ["T1", "T2"]

    def test_unknown_task_lists_first_ten_ids_and_the_rest(self):
        tasks = [_task(f"T{i}") for i in range(1, 12)]   # eleven tasks

        with pytest.raises(SR.SubtreeRerunRefused) as excinfo:
            SR.rerun_subtree_ids(tasks, "ZZZ")

        err = excinfo.value
        assert err.code == "unknown_task"
        expected_listing = ", ".join(f"T{i}" for i in range(1, 11)) + " and 1 more"
        assert err.detail == f"there is no task 'ZZZ' in this job; its tasks are: {expected_listing}"


# ---------------------------------------------------------------------------
# S3/S4/S6 — the walk, the plan and the exact reset with its hash proof
# ---------------------------------------------------------------------------

class TestExactResetAndProof:
    def test_reset_of_middle_task_restores_predecessor_tree(self, repo):
        t1_sha = _land(repo, JOB_ID, "T1", write={"a.py": "v1\n"})
        t1_tree = _git(repo, "rev-parse", "HEAD^{tree}").strip()
        t2_sha = _land(repo, JOB_ID, "T2", write={"a.py": "v2\n", "b.py": "b\n"}, chmod_x=["a.py"])
        t3_sha = _land(repo, JOB_ID, "T3", write={"b.py": "b2\n", "c.py": "c\n"}, delete=["base.txt"])
        head = t3_sha

        tasks = [
            _task("T1", planned_id="P1", worktree_commit=t1_sha, status=PJ.TASK_APPLIED,
                  task_start_tree=""),
            _task("T2", planned_id="P2", depends_on=("P1",), worktree_commit=t2_sha,
                  status=PJ.TASK_APPLIED, task_start_tree=t1_tree),
            _task("T3", planned_id="P3", depends_on=("P2",), worktree_commit=t3_sha,
                  status=PJ.TASK_APPLIED),
        ]
        job = _job(JOB_ID, repo, tasks, worktree_head=head)

        result = SR.apply_subtree_reset(job, "T2", repo)

        assert result["subtree"] == ["T2", "T3"]
        assert result["exact"] is True
        assert result["pre_task_tree_equal"] is True
        assert result["reset_tree"] == t1_tree
        assert not (repo / "c.py").exists()
        assert (repo / "base.txt").exists()
        assert (repo / "a.py").read_text() == "v1\n"
        assert not (os.stat(repo / "a.py").st_mode & 0o111)
        assert not (repo / "b.py").exists()

        trailers_text = _git(repo, "log", "-1", "--format=%(trailers:only,unfold)")
        assert f"{W.REMEDY_JOB_TRAILER}: {JOB_ID}" in trailers_text
        assert f"{SR.RERUN_TRAILER}: T2" in trailers_text

        assert W.is_ancestor(repo, t2_sha, "HEAD")
        assert W.is_ancestor(repo, t3_sha, "HEAD")

    def test_pre_task_tree_equal_is_none_without_a_recorded_start_tree(self, repo):
        t1_sha = _land(repo, JOB_ID, "T1", write={"a.py": "v1\n"})
        t2_sha = _land(repo, JOB_ID, "T2", write={"a.py": "v2\n"})
        tasks = [
            _task("T1", planned_id="P1", worktree_commit=t1_sha),
            _task("T2", planned_id="P2", depends_on=("P1",), worktree_commit=t2_sha,
                  task_start_tree=""),
        ]
        job = _job(JOB_ID, repo, tasks, worktree_head=t2_sha)

        result = SR.apply_subtree_reset(job, "T2", repo)

        assert result["exact"] is True
        assert result["pre_task_tree_equal"] is None

    def test_completed_elsewhere_task_outside_subtree_keeps_its_own_file(self, repo):
        t1_sha = _land(repo, JOB_ID, "T1", write={"a.py": "v1\n"})
        t2_sha = _land(repo, JOB_ID, "T2", write={"a.py": "v2\n", "b.py": "b\n"})
        t3_sha = _land(repo, JOB_ID, "T3", write={"b.py": "b2\n", "c.py": "c\n"}, delete=["base.txt"])
        t4_sha = _land(repo, JOB_ID, "T4", write={"d.py": "d\n"})   # independent, applied after T3

        tasks = [
            _task("T1", planned_id="P1", worktree_commit=t1_sha),
            _task("T2", planned_id="P2", depends_on=("P1",), worktree_commit=t2_sha),
            _task("T3", planned_id="P3", depends_on=("P2",), worktree_commit=t3_sha),
            _task("T4", planned_id="P4", worktree_commit=t4_sha),
        ]
        job = _job(JOB_ID, repo, tasks, worktree_head=t4_sha)

        result = SR.apply_subtree_reset(job, "T2", repo)

        assert result["exact"] is False
        assert result["pre_task_tree_equal"] is None
        assert (repo / "d.py").read_text() == "d\n"
        assert not (repo / "c.py").exists()
        assert (repo / "base.txt").exists()
        assert (repo / "a.py").read_text() == "v1\n"

    def test_interleaving_refused_when_outside_task_touches_a_subtree_path(self, repo):
        t1_sha = _land(repo, JOB_ID, "T1", write={"a.py": "v1\n"})
        t2_sha = _land(repo, JOB_ID, "T2", write={"a.py": "v2\n", "b.py": "b\n"})
        t3_sha = _land(repo, JOB_ID, "T3", write={"b.py": "b2\n"})
        t4_sha = _land(repo, JOB_ID, "T4", write={"a.py": "v3\n"})   # touches a subtree path

        tasks = [
            _task("T1", planned_id="P1", worktree_commit=t1_sha),
            _task("T2", planned_id="P2", depends_on=("P1",), worktree_commit=t2_sha),
            _task("T3", planned_id="P3", depends_on=("P2",), worktree_commit=t3_sha),
            _task("T4", planned_id="P4", worktree_commit=t4_sha),
        ]
        job = _job(JOB_ID, repo, tasks, worktree_head=t4_sha)
        before = _snapshot(repo)

        with pytest.raises(SR.SubtreeRerunRefused) as excinfo:
            SR.apply_subtree_reset(job, "T2", repo)

        err = excinfo.value
        assert err.code == "interleaved"
        assert err.facts == {"interleaving": [{"by": "T4", "paths": ["a.py"]}]}
        assert _snapshot(repo) == before

    def test_interleaving_names_a_trailerless_commit_by_its_sha(self, repo):
        t1_sha = _land(repo, JOB_ID, "T1", write={"a.py": "v1\n"})
        t2_sha = _land(repo, JOB_ID, "T2", write={"a.py": "v2\n"})
        bare_sha = _land_bare(repo, JOB_ID, write={"a.py": "v3\n"})

        tasks = [
            _task("T1", planned_id="P1", worktree_commit=t1_sha),
            _task("T2", planned_id="P2", depends_on=("P1",), worktree_commit=t2_sha),
        ]
        job = _job(JOB_ID, repo, tasks, worktree_head=bare_sha)

        with pytest.raises(SR.SubtreeRerunRefused) as excinfo:
            SR.plan_subtree_reset(job, "T2", repo)

        err = excinfo.value
        assert err.code == "interleaved"
        assert err.facts == {"interleaving": [{"by": f"commit {bare_sha[:12]}", "paths": ["a.py"]}]}

    def test_second_rerun_of_the_same_task_again_restores_predecessor_tree(self, repo):
        t1_sha = _land(repo, JOB_ID, "T1", write={"a.py": "v1\n"})
        t1_tree = _git(repo, "rev-parse", "HEAD^{tree}").strip()
        t2_sha = _land(repo, JOB_ID, "T2", write={"a.py": "v2\n", "b.py": "b\n"})
        t3_sha = _land(repo, JOB_ID, "T3", write={"b.py": "b2\n"})

        tasks = [
            _task("T1", planned_id="P1", worktree_commit=t1_sha),
            _task("T2", planned_id="P2", depends_on=("P1",), worktree_commit=t2_sha),
            _task("T3", planned_id="P3", depends_on=("P2",), worktree_commit=t3_sha),
        ]
        job = _job(JOB_ID, repo, tasks, worktree_head=t3_sha)
        result1 = SR.apply_subtree_reset(job, "T2", repo)
        assert result1["exact"] is True
        assert result1["reset_tree"] == t1_tree

        # A fresh T2 attempt lands on top of the first reset; T002 has cleared T3's
        # worktree_commit back to "" because T3 returned to pending.
        t2b_sha = _land(repo, JOB_ID, "T2", write={"a.py": "v3\n"})
        tasks2 = [
            _task("T1", planned_id="P1", worktree_commit=t1_sha),
            _task("T2", planned_id="P2", depends_on=("P1",), worktree_commit=t2b_sha),
            _task("T3", planned_id="P3", depends_on=("P2",), worktree_commit=""),
        ]
        job2 = _job(JOB_ID, repo, tasks2, worktree_head=t2b_sha)

        result2 = SR.apply_subtree_reset(job2, "T2", repo)

        assert result2["exact"] is True
        assert result2["reset_tree"] == t1_tree


# ---------------------------------------------------------------------------
# S4 — the refusals; every one leaves the branch exactly as it was
# ---------------------------------------------------------------------------

class TestRefusalsAreSideEffectFree:
    def test_not_worktree_mode(self, repo):
        t1_sha = _land(repo, JOB_ID, "T1", write={"a.py": "v1\n"})
        tasks = [_task("T1", worktree_commit=t1_sha)]
        job = _job(JOB_ID, repo, tasks, worktree_head=t1_sha, isolation_mode="copy")
        before = _snapshot(repo)

        with pytest.raises(SR.SubtreeRerunRefused) as excinfo:
            SR.plan_subtree_reset(job, "T1", repo)

        assert excinfo.value.code == "not_worktree_mode"
        assert _snapshot(repo) == before

    def test_task_not_committed(self, repo):
        head = _git(repo, "rev-parse", "HEAD").strip()
        tasks = [_task("T1", worktree_commit="")]
        job = _job(JOB_ID, repo, tasks, worktree_head=head)
        before = _snapshot(repo)

        with pytest.raises(SR.SubtreeRerunRefused) as excinfo:
            SR.plan_subtree_reset(job, "T1", repo)

        assert excinfo.value.code == "task_not_committed"
        assert _snapshot(repo) == before

    def test_worktree_drift_message_matches_checkpoints_wording_exactly(self, repo):
        t1_sha = _land(repo, JOB_ID, "T1", write={"a.py": "v1\n"})
        tasks = [_task("T1", worktree_commit=t1_sha)]
        job = _job(JOB_ID, repo, tasks, worktree_head="f" * 40)
        before = _snapshot(repo)

        with pytest.raises(SR.SubtreeRerunRefused) as excinfo:
            SR.plan_subtree_reset(job, "T1", repo)

        err = excinfo.value
        assert err.code == "worktree_drift"
        assert err.detail == checkpoints.worktree_drift_message(job.worktree_head, t1_sha)
        assert _snapshot(repo) == before

    def test_worktree_drift_for_a_missing_worktree_path_names_unknown(self, repo, tmp_path):
        t1_sha = _land(repo, JOB_ID, "T1", write={"a.py": "v1\n"})
        tasks = [_task("T1", worktree_commit=t1_sha)]
        job = _job(JOB_ID, repo, tasks, worktree_head=t1_sha)
        missing = tmp_path / "does-not-exist"

        with pytest.raises(SR.SubtreeRerunRefused) as excinfo:
            SR.plan_subtree_reset(job, "T1", missing)

        err = excinfo.value
        assert err.code == "worktree_drift"
        assert err.detail == checkpoints.worktree_drift_message(t1_sha, "unknown")

    def test_worktree_dirty_names_an_untracked_file(self, repo):
        t1_sha = _land(repo, JOB_ID, "T1", write={"a.py": "v1\n"})
        tasks = [_task("T1", worktree_commit=t1_sha)]
        job = _job(JOB_ID, repo, tasks, worktree_head=t1_sha)
        (repo / "stray.txt").write_text("oops\n")
        before = _snapshot(repo)

        with pytest.raises(SR.SubtreeRerunRefused) as excinfo:
            SR.plan_subtree_reset(job, "T1", repo)

        err = excinfo.value
        assert err.code == "worktree_dirty"
        assert "stray.txt" in err.detail
        assert _snapshot(repo) == before

    def test_commit_not_on_branch_for_a_commit_on_another_branch(self, repo):
        t1_sha = _land(repo, JOB_ID, "T1", write={"a.py": "v1\n"})
        _git(repo, "checkout", "-q", "-b", "other-branch")
        (repo / "other.py").write_text("x\n")
        _git(repo, "add", "-A")
        subprocess.run(
            ["git", "-c", "user.name=T", "-c", "user.email=t@e.com", "-c", "commit.gpgsign=false",
             "commit", "-qm", "other"],
            cwd=str(repo), check=True, capture_output=True, text=True,
        )
        other_sha = _git(repo, "rev-parse", "HEAD").strip()
        _git(repo, "checkout", "-q", BRANCH)

        tasks = [_task("T1", worktree_commit=other_sha)]
        job = _job(JOB_ID, repo, tasks, worktree_head=t1_sha)
        before = _snapshot(repo)

        with pytest.raises(SR.SubtreeRerunRefused) as excinfo:
            SR.plan_subtree_reset(job, "T1", repo)

        err = excinfo.value
        assert err.code == "commit_not_on_branch"
        assert other_sha[:12] in err.detail
        assert _snapshot(repo) == before

    def test_subtree_order_for_a_dependent_commit_preceding_the_root(self, repo):
        t1_sha = _land(repo, JOB_ID, "T1", write={"a.py": "v1\n"})
        t2_sha = _land(repo, JOB_ID, "T2", write={"a.py": "v2\n"})
        tasks = [
            _task("T1", planned_id="P1", worktree_commit=t1_sha),
            _task("T2", planned_id="P2", depends_on=("P1",), worktree_commit=t2_sha),
            # T3 depends on T2 but its recorded commit (T1's) precedes T2's on the branch.
            _task("T3", planned_id="P3", depends_on=("P2",), worktree_commit=t1_sha),
        ]
        job = _job(JOB_ID, repo, tasks, worktree_head=t2_sha)
        before = _snapshot(repo)

        with pytest.raises(SR.SubtreeRerunRefused) as excinfo:
            SR.plan_subtree_reset(job, "T2", repo)

        err = excinfo.value
        assert err.code == "subtree_order"
        assert "T3" in err.detail
        assert _snapshot(repo) == before


# ---------------------------------------------------------------------------
# S5 — the commit message
# ---------------------------------------------------------------------------

class TestBuildRerunCommitMessage:
    def test_one_dependent_and_one_path(self):
        job = PJ.JobPlan(job_id="J1", repo_path="/tmp/x")
        plan = {"root_task_id": "T2", "subtree": ["T2", "T4"],
                "base_commit": "0123456789abcdef", "paths": ["a.py"]}

        msg = SR.build_rerun_commit_message(job, plan)

        assert msg.startswith("rerun: reset task T2 and 1 dependent task\n\n")
        assert "changing a.py" in msg
        assert msg.endswith(f"{W.REMEDY_JOB_TRAILER}: J1\n{SR.RERUN_TRAILER}: T2\n")

    def test_three_dependents_and_no_changed_file(self):
        job = PJ.JobPlan(job_id="J1", repo_path="/tmp/x")
        plan = {"root_task_id": "T1", "subtree": ["T1", "T2", "T3", "T4"],
                "base_commit": "abcdefabcdef", "paths": []}

        msg = SR.build_rerun_commit_message(job, plan)

        assert "reset task T1 and 3 dependent tasks" in msg
        assert "changing no file" in msg

    def test_more_than_five_paths_are_truncated(self):
        job = PJ.JobPlan(job_id="J1", repo_path="/tmp/x")
        paths = [f"f{i}.py" for i in range(7)]
        plan = {"root_task_id": "T1", "subtree": ["T1"], "base_commit": "0" * 12, "paths": paths}

        msg = SR.build_rerun_commit_message(job, plan)

        named = ", ".join(paths[:5])
        assert f"changing {named}, ..." in msg
