"""F270 T002/T003 — `remedy job apply --approve --commit-with-history` (DECISION F270 D2).

The job branch `remedy/job-<job id>` carries one Remedy commit per applied task
(DECISION F270 D1). With the flag, `apply_job` merges it with `--no-ff` onto the
operator's current branch, as the operator, after every existing gate; each
refusal leaves HEAD, the branch, the index, the status and every file as they
were. Drives the real `run_job` with fake providers; no provider is called.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

import pytest

from packages.orchestration import worktrees as W
from packages.orchestration.job_apply import (
    HISTORY_REFUSED,
    apply_job,
    export_job_apply_json,
    load_job_apply_record,
    summarize_job_apply,
)
from packages.orchestration.pingpong_job import JOB_COMPLETED, parse_job_file, run_job
from packages.orchestration.pingpong_provider import BuilderOutput, ReviewerOutput
from tests.orchestration.test_job_worktree_integration import (  # noqa: F401  (fixture)
    _git,
    _run_two_task_job,
    repo,
)

HISTORY_KEYS = ("commit_with_history", "merged_branch", "target_branch",
                "history_commits", "merge_commit", "merge_conflicts")


@pytest.fixture(autouse=True)
def data_root(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    for key in ("GIT_AUTHOR_NAME", "GIT_AUTHOR_EMAIL",
                "GIT_COMMITTER_NAME", "GIT_COMMITTER_EMAIL"):
        monkeypatch.delenv(key, raising=False)
    return root


def _state(repo: Path) -> dict:
    """HEAD, the symbolic ref, the index, the status, MERGE_HEAD and every file's sha256."""
    files = {}
    for dirpath, dirnames, filenames in os.walk(repo):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for name in filenames:
            path = Path(dirpath) / name
            files[str(path.relative_to(repo))] = hashlib.sha256(path.read_bytes()).hexdigest()
    ref = subprocess.run(["git", "symbolic-ref", "-q", "HEAD"], cwd=str(repo),
                         capture_output=True, text=True, timeout=60)
    return {
        "head": _git(repo, "rev-parse", "HEAD").strip(),
        "ref": (ref.returncode, ref.stdout.strip()),
        "index": _git(repo, "ls-files", "-s"),
        "status": _git(repo, "status", "--porcelain", "--untracked-files=all"),
        "merge_head": (repo / ".git" / "MERGE_HEAD").exists(),
        "files": files,
    }


def _completed(repo: Path, monkeypatch):
    job = _run_two_task_job(repo, monkeypatch, {})
    assert job.state == JOB_COMPLETED and job.isolation_mode == "worktree"
    return job


def _operator_commit(repo: Path, rel: str, text: str, message: str) -> str:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", message)
    return _git(repo, "rev-parse", "HEAD").strip()


def _hook(repo: Path, name: str, script: str) -> None:
    hook = repo / ".git" / "hooks" / name
    hook.parent.mkdir(parents=True, exist_ok=True)
    hook.write_text(script)
    hook.chmod(0o755)


def _apply_with_history(repo: Path, job, **kw):
    return apply_job(job.job_id, str(repo), approve=True, commit_with_history=True, **kw)


def _refused(result, before: dict, repo: Path) -> str:
    """The refusal's one sentence, after proving nothing on disk changed."""
    assert result.status == "blocked", (result.status, result.blocked_reason)
    assert result.blocked_reason.startswith(f"{HISTORY_REFUSED}: "), result.blocked_reason
    sentence = result.blocked_reason[len(HISTORY_REFUSED) + 2:]
    assert sentence.endswith(".") and ". " not in sentence, sentence
    assert result.merge_commit == "" and result.files_applied == []
    assert _state(repo) == before
    return sentence


class TestTheMerge:
    def test_h1_the_merge_lands_both_task_commits_as_the_operator(self, repo, monkeypatch):
        job = _completed(repo, monkeypatch)
        # The operator moved on after the job forked: a real, non-fast-forward merge.
        own = _operator_commit(repo, "hand.txt", "mine\n", "Add my own note")
        hook_log = repo / ".git" / "commit-msg-ran"
        _hook(repo, "commit-msg", f"#!/bin/sh\necho ran >> {hook_log}\n")

        result = _apply_with_history(repo, job)

        assert result.status == "applied", result.blocked_reason
        head = _git(repo, "rev-parse", "HEAD").strip()
        assert result.merge_commit == head
        assert _git(repo, "log", "-1", "--format=%P", head).split() == [own, job.worktree_head]
        second_side = _git(repo, "rev-list", "--reverse", f"{head}^1..{head}^2").split()
        assert second_side == [t.worktree_commit for t in job.tasks]
        assert len(second_side) == 2 and result.history_commits == second_side
        # The files are the job's result; the operator's own file is kept; the tree is clean.
        assert (repo / "one.txt").read_text() == "from task one\n"
        assert (repo / "two.txt").read_text() == "task two saw: from task one\n"
        assert (repo / "hand.txt").read_text() == "mine\n"
        assert _git(repo, "status", "--porcelain", "--untracked-files=all") == ""
        # The operator's identity and hook; the message; the trailers.
        who = _git(repo, "log", "-1", "--format=%an <%ae>|%cn <%ce>", head).strip()
        assert who == "T <t@e.com>|T <t@e.com>"
        assert hook_log.read_text() == "ran\n"
        message = _git(repo, "log", "-1", "--format=%B", head).strip()
        paragraphs = message.split("\n\n")
        assert paragraphs[0] == f"Merge the 2 task commits of Remedy job {job.job_id[:8]}"
        assert len(paragraphs[0]) <= 72
        assert job.worktree_branch in paragraphs[1] and result.target_branch in paragraphs[1]
        assert paragraphs[-2] == "contract: none"
        trailers = _git(repo, "log", "-1", "--format=%(trailers:only,unfold)", head).split("\n")
        assert f"Remedy-Job: {job.job_id}" in trailers
        assert "Co-authored-by: Remedy <remedy@local>" in trailers
        # The record, the summary, and the job branch kept.
        record = load_job_apply_record(job.job_id, result.job_apply_id)
        assert record["status"] == "applied" and record["merge_commit"] == head
        assert record["commit_with_history"] is True and record["merge_conflicts"] == []
        assert record["merged_branch"] == job.worktree_branch
        assert record["target_branch"] == _git(repo, "symbolic-ref", "--short", "HEAD").strip()
        assert record["history_commits"] == second_side
        assert sorted(record["files_applied"]) == ["one.txt", "two.txt"]
        summary = summarize_job_apply(result)
        assert f"Merged 2 task commit(s) of {job.worktree_branch}" in summary
        assert head in summary and "Nothing was pushed." in summary
        assert "No commits or pushes were made" not in summary
        assert W._branch_exists(repo, job.worktree_branch)

    def test_h2_no_ff_even_where_a_fast_forward_was_possible(self, repo, monkeypatch):
        job = _completed(repo, monkeypatch)
        base = _git(repo, "rev-parse", "HEAD").strip()
        assert base == job.worktree_base_commit          # HEAD is an ancestor of the tip
        result = _apply_with_history(repo, job)
        assert result.status == "applied", result.blocked_reason
        assert _git(repo, "log", "-1", "--format=%P", "HEAD").split() == [base, job.worktree_head]

    def test_h3_without_approve_the_flag_previews_and_names_the_refusals(
        self, repo, monkeypatch,
    ):
        job = _completed(repo, monkeypatch)
        before = _state(repo)
        result = apply_job(job.job_id, str(repo), approve=False, commit_with_history=True)
        assert result.status == "dry_run" and result.merge_commit == ""
        assert _state(repo) == before
        summary = summarize_job_apply(result)
        assert "--approve --commit-with-history" in summary
        assert "would be refused" not in summary
        # A dirty tree: the preview names the refusal the real run would meet.
        (repo / "scratch.txt").write_text("wip\n")
        before = _state(repo)
        preview = apply_job(job.job_id, str(repo), approve=False, commit_with_history=True)
        assert preview.status == "dry_run"
        assert _state(repo) == before
        assert any("uncommitted changes in scratch.txt" in r for r in preview.blocked_reasons)
        assert "would be refused" in summarize_job_apply(preview)


class TestPlainApproveIsUnchanged:
    def test_h8_plain_approve_copies_and_leaves_head_alone(self, repo, monkeypatch):
        job = _completed(repo, monkeypatch)
        head = _git(repo, "rev-parse", "HEAD").strip()
        result = apply_job(job.job_id, str(repo), approve=True)
        assert result.status == "applied" and result.merge_commit == ""
        assert result.commit_with_history is False
        assert _git(repo, "rev-parse", "HEAD").strip() == head
        assert sorted(_git(repo, "status", "--porcelain").splitlines()) == [
            "?? one.txt", "?? two.txt"]
        assert "No commits or pushes were made" in summarize_job_apply(result)


class TestRefusals:
    def test_h4_a_dirty_tree_is_refused_naming_the_path(self, repo, monkeypatch):
        job = _completed(repo, monkeypatch)
        (repo / "scratch.txt").write_text("wip\n")
        before = _state(repo)
        sentence = _refused(_apply_with_history(repo, job), before, repo)
        assert "uncommitted changes in scratch.txt" in sentence

    def test_h5_a_committed_hand_edit_is_refused_by_the_baseline_gate_and_kept(
        self, repo, monkeypatch,
    ):
        job = _completed(repo, monkeypatch)
        _operator_commit(repo, "one.txt", "my hand edit\n", "Edit one by hand")
        before = _state(repo)
        result = _apply_with_history(repo, job)
        assert result.status == "blocked"
        assert result.blocked_reason.startswith("baseline_check_failed:")
        assert "target_created_since_job: one.txt" in result.blocked_reason
        assert result.merge_commit == "" and result.files_applied == []
        assert _state(repo) == before
        assert (repo / "one.txt").read_text() == "my hand edit\n"

    def test_h6_a_git_conflict_is_aborted_naming_the_unmerged_paths(
        self, repo, monkeypatch,
    ):
        """A file/directory clash passes every file gate; only git itself sees it."""
        job = _one_task_job(repo, monkeypatch, "pkg/mod.txt")
        _operator_commit(repo, "pkg", "a file where the job makes a directory\n",
                         "Add pkg as a file")
        before = _state(repo)
        result = _apply_with_history(repo, job)
        sentence = _refused(result, before, repo)
        assert result.merge_conflicts, result.blocked_reason
        assert "conflicts in" in sentence and "aborted" in sentence
        for path in result.merge_conflicts:
            assert path in sentence
        assert (repo / "pkg").read_text() == "a file where the job makes a directory\n"

    @pytest.mark.parametrize("git_target", [False, True])
    def test_h7_a_staging_job_is_refused_and_a_plain_approve_still_copies(
        self, tmp_path, git_target,
    ):
        from tests.orchestration.test_job_apply import _make_baselined_job

        job, _ws, target, rel = _make_baselined_job(tmp_path)
        if git_target:
            for args in (("init", "-q"), ("config", "user.email", "t@e.com"),
                         ("config", "user.name", "T"), ("add", "-A"),
                         ("commit", "-qm", "init")):
                _git(target, *args)
        before = (target / rel).read_bytes()
        result = apply_job(job.job_id, str(target), approve=True, commit_with_history=True)
        assert result.status == "blocked"
        assert result.blocked_reason.startswith(f"{HISTORY_REFUSED}: ")
        assert "ran in a staging copy" in result.blocked_reason
        assert "a plain --approve copies" in result.blocked_reason
        assert result.files_applied == [] and (target / rel).read_bytes() == before
        plain = apply_job(job.job_id, str(target), approve=True)
        assert plain.status == "applied"
        assert (target / rel).read_text() == "modified\n"

    def test_h9_a_detached_head_is_refused(self, repo, monkeypatch):
        job = _completed(repo, monkeypatch)
        _git(repo, "checkout", "-q", "--detach")
        before = _state(repo)
        assert "detached HEAD" in _refused(_apply_with_history(repo, job), before, repo)

    def test_h10_a_moved_branch_tip_is_refused(self, repo, monkeypatch):
        job = _completed(repo, monkeypatch)
        tree = _git(repo, "rev-parse", f"{job.worktree_head}^{{tree}}").strip()
        extra = _git(repo, "commit-tree", tree, "-p", job.worktree_head,
                     "-m", "someone else").strip()
        _git(repo, "update-ref", f"refs/heads/{job.worktree_branch}", extra)
        before = _state(repo)
        sentence = _refused(_apply_with_history(repo, job), before, repo)
        assert "not the reviewed work" in sentence
        assert _git(repo, "rev-parse", job.worktree_branch).strip() == extra

    def test_h11_a_deleted_branch_is_refused(self, repo, monkeypatch):
        job = _completed(repo, monkeypatch)
        _git(repo, "branch", "-D", job.worktree_branch)
        before = _state(repo)
        assert "does not exist" in _refused(_apply_with_history(repo, job), before, repo)

    def test_h12_skip_blocked_does_not_combine_with_the_flag(self, repo, monkeypatch):
        job = _completed(repo, monkeypatch)
        before = _state(repo)
        sentence = _refused(_apply_with_history(repo, job, skip_blocked=True), before, repo)
        assert "--skip-blocked" in sentence

    def test_h13_a_refusing_pre_merge_commit_hook_is_aborted_and_quoted(
        self, repo, monkeypatch,
    ):
        job = _completed(repo, monkeypatch)
        _hook(repo, "pre-merge-commit", "#!/bin/sh\necho no merges on fridays >&2\nexit 1\n")
        before = _state(repo)
        sentence = _refused(_apply_with_history(repo, job), before, repo)
        assert '"no merges on fridays"' in sentence and "aborted" in sentence
        assert _git(repo, "log", "--format=%s").splitlines() == ["init"]


class _OneFileBuilder:
    def __init__(self, holder: dict, rel: str):
        self._holder, self._rel = holder, rel

    def build(self, prompt, **kw):
        path = Path(self._holder["path"]) / self._rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("from the job\n")
        return BuilderOutput(summary="wrote", files_changed=[self._rel], provider="fake")

    def review(self, prompt, **kw):
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok",
                              provider="fake")


def _one_task_job(repo: Path, monkeypatch, rel: str):
    job = parse_job_file(f"# One-file job\n\n## Task 1 — write {rel}\n\nWrite `{rel}`.\n",
                         str(repo))
    holder: dict = {}
    real_create = W.create

    def spy(job_id, r):
        handle = real_create(job_id, r)
        holder["path"] = handle.path
        return handle

    monkeypatch.setattr(W, "create", spy)
    builder = _OneFileBuilder(holder, rel)
    done = run_job(job.job_id, builder_provider=builder, reviewer_provider=builder,
                   builder_name="fake", reviewer_name="fake", max_rounds=1)
    assert done.state == JOB_COMPLETED, done.error
    return done


class TestThroughTheCli:
    def test_a_refused_and_a_merging_run_exit_zero_with_their_record_keys(
        self, repo, monkeypatch, data_root,
    ):
        from tests.cli.runtime_helpers import run_grouped_cli

        job = _completed(repo, monkeypatch)
        argv = ["job", "apply", job.job_id, "--repo", str(repo), "--approve",
                "--commit-with-history", "--json"]
        (repo / "scratch.txt").write_text("wip\n")
        refused = run_grouped_cli(argv, data_root, timeout=120)
        assert refused.returncode == 0, refused.stderr      # a blocked apply exits 0
        data = json.loads(refused.stdout)
        assert data["status"] == "blocked"
        assert data["blocked_reason"].startswith(f"{HISTORY_REFUSED}: ")
        assert all(key in data for key in HISTORY_KEYS)
        assert data["commit_with_history"] is True and data["merge_commit"] == ""
        (repo / "scratch.txt").unlink()

        merged = run_grouped_cli(argv, data_root, timeout=120)
        assert merged.returncode == 0, merged.stderr
        data = json.loads(merged.stdout)
        assert data["status"] == "applied", data["blocked_reason"]
        assert all(key in data for key in HISTORY_KEYS)
        assert data["merge_commit"] == _git(repo, "rev-parse", "HEAD").strip()
        assert data["merged_branch"] == job.worktree_branch
        assert len(data["history_commits"]) == 2
        # And export carries the same keys for a result that never merged.
        assert all(key in export_job_apply_json(apply_job(job.job_id, str(repo)))
                   for key in HISTORY_KEYS)
