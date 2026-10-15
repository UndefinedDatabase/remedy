"""A dirty working tree is the job's captured baseline (operator amendment amend1014b, D5 and D6).

Real git repositories and the real `run_job` with a fake builder that appends to README.md; no
provider is called. The builder records the bytes it saw, which is the proof the workspace was
seeded from the target's visible state and not from HEAD.
"""
from __future__ import annotations

import os
import stat
from pathlib import Path

import pytest

from packages.orchestration import dirty_baseline as DB
from packages.orchestration.job_apply import (
    TARGET_CHANGED_DURING_RUN,
    apply_job,
    apply_refusal,
    export_job_apply_json,
    summarize_job_apply,
)
from packages.orchestration.job_evidence import job_result_diff_source
from packages.orchestration.pingpong_job import JOB_COMPLETED, parse_job_file, run_job
from packages.orchestration.pingpong_provider import BuilderOutput, ReviewerOutput
from tests.orchestration.test_job_apply_history import _state, data_root  # noqa: F401 (autouse)
from tests.orchestration.test_job_worktree_integration import _git, repo  # noqa: F401 (fixture)

_JOB = "# Edit the readme\n\n## Task 1 — extend README.md\n\nAppend a line to `README.md`.\n"
_DIRTY = "# Base\n\nThe person's own uncommitted sentence.\n"


class _AppendBuilder:
    def __init__(self, holder: dict, seen: dict):
        self.holder, self.seen = holder, seen

    def build(self, prompt, **kw):
        ws = Path(self.holder["path"])
        self.seen["saw"] = (ws / "README.md").read_text()
        with open(ws / "README.md", "a") as fh:
            fh.write("The job's reviewed paragraph.\n")
        return BuilderOutput(summary="appended", files_changed=["README.md"], provider="fake")

    def review(self, prompt, **kw):
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok", provider="fake")


def _run(repo: Path, monkeypatch, seen: dict):
    from packages.orchestration import worktrees as W

    job = parse_job_file(_JOB, str(repo))
    holder: dict = {}
    real = W.create

    def spy(job_id, r):
        h = real(job_id, r)
        holder["path"] = h.path
        return h

    monkeypatch.setattr(W, "create", spy)
    prov = _AppendBuilder(holder, seen)
    return run_job(job.job_id, builder_provider=prov, reviewer_provider=prov,
                   builder_name="fake", reviewer_name="fake", max_rounds=1)


@pytest.fixture
def dirty_repo(repo) -> Path:
    (repo / "README.md").write_text("# Base\n")
    (repo / "notes.txt").write_text("notes\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "readme and notes")
    (repo / "README.md").write_text(_DIRTY)
    (repo / "notes.txt").write_text("notes, edited by hand\n")
    return repo


# --- 10. the workspace starts from the dirty bytes ------------------------------------------

def test_the_workspace_is_seeded_from_the_visible_bytes_and_the_diff_is_the_delta(dirty_repo, monkeypatch):
    seen: dict = {}
    head_before = _git(dirty_repo, "rev-parse", "HEAD")
    job = _run(dirty_repo, monkeypatch, seen)

    assert job.state == JOB_COMPLETED
    assert seen["saw"] == _DIRTY                                   # not the HEAD blob "# Base\n"
    assert {e["path"] for e in job.start_baseline["entries"]} == {"README.md", "notes.txt"}
    assert job.start_baseline["commit"] and job.start_baseline["head"] == head_before.strip()
    diff = job_result_diff_source(job)[0].read_text()
    added = [ln for ln in diff.splitlines() if ln.startswith("+") and not ln.startswith("+++")]
    assert added == ["+The job's reviewed paragraph."]            # the person's sentence is context
    assert "notes.txt" not in diff
    assert (dirty_repo / "README.md").read_text() == _DIRTY        # the target was only read
    assert _git(dirty_repo, "stash", "list") == ""


def test_a_clean_target_records_no_baseline(repo, monkeypatch):
    (repo / "README.md").write_text("# Base\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "readme")
    job = _run(repo, monkeypatch, {})
    assert job.state == JOB_COMPLETED and job.start_baseline is None


# --- 11. apply over an unchanged dirty baseline ---------------------------------------------

def test_apply_changes_only_the_reviewed_delta_and_leaves_other_dirt_alone(dirty_repo, monkeypatch):
    job = _run(dirty_repo, monkeypatch, {})
    before = _git(dirty_repo, "rev-parse", "HEAD")

    result = apply_job(job.job_id, str(dirty_repo), approve=True)

    assert result.status == "applied", result.blocked_reason
    assert (dirty_repo / "README.md").read_text() == _DIRTY + "The job's reviewed paragraph.\n"
    assert (dirty_repo / "notes.txt").read_text() == "notes, edited by hand\n"
    assert _git(dirty_repo, "rev-parse", "HEAD") == before          # no commit
    assert result.baseline_files_applied == ["README.md"]
    assert result.preserved_dirty_paths == ["notes.txt"]
    assert export_job_apply_json(result)["preserved_dirty_paths"] == ["notes.txt"]


# --- 12. a concurrent change blocks ---------------------------------------------------------

def test_a_change_after_capture_blocks_the_apply_and_survives_byte_for_byte(dirty_repo, monkeypatch):
    job = _run(dirty_repo, monkeypatch, {})
    (dirty_repo / "README.md").write_text("changed by someone else while the job ran\n")
    snapshot = _state(dirty_repo)

    result = apply_job(job.job_id, str(dirty_repo), approve=True, commit_auto=True)

    assert result.status == "blocked" and not result.commit_sha
    token, sentence = apply_refusal(result)
    assert token == TARGET_CHANGED_DURING_RUN == "target_changed_during_run"
    assert "README.md" in sentence and "nothing was applied" in sentence
    assert _state(dirty_repo) == snapshot


def test_head_moving_during_the_run_blocks_a_dirty_start_apply(dirty_repo, monkeypatch):
    job = _run(dirty_repo, monkeypatch, {})
    _git(dirty_repo, "commit", "-q", "--allow-empty", "-m", "someone committed meanwhile")

    result = apply_job(job.job_id, str(dirty_repo), approve=True)

    assert result.status == "blocked" and apply_refusal(result)[0] == TARGET_CHANGED_DURING_RUN
    assert "HEAD moved" in result.blocked_reason
    assert (dirty_repo / "README.md").read_text() == _DIRTY


# --- 13. selective auto-commit --------------------------------------------------------------

def test_commit_auto_commits_only_the_job_file_and_says_it_held_earlier_edits(dirty_repo, monkeypatch):
    job = _run(dirty_repo, monkeypatch, {})

    result = apply_job(job.job_id, str(dirty_repo), approve=True, commit_auto=True)

    assert result.status == "applied" and result.commit_sha, result.blocked_reason
    assert _git(dirty_repo, "show", "--name-only", "--format=", "HEAD").split() == ["README.md"]
    assert _git(dirty_repo, "status", "--porcelain").split() == ["M", "notes.txt"]
    assert (dirty_repo / "notes.txt").read_text() == "notes, edited by hand\n"
    assert _git(dirty_repo, "stash", "list") == ""
    assert _DIRTY.splitlines()[2] in _git(dirty_repo, "show", "HEAD:README.md")
    text = summarize_job_apply(result)
    assert "README.md already held uncommitted edits when the job started" in text
    assert "(and any commit of it)" in text and "notes.txt" in text


# --- 14. unsupported and exactly represented states ----------------------------------------

def _conflict(repo: Path) -> None:
    (repo / "c.txt").write_text("base\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "c")
    _git(repo, "checkout", "-q", "-b", "other")
    (repo / "c.txt").write_text("other\n")
    _git(repo, "commit", "-qam", "other side")
    _git(repo, "checkout", "-q", "-")
    (repo / "c.txt").write_text("mine\n")
    _git(repo, "commit", "-qam", "my side")
    import subprocess
    subprocess.run(["git", "merge", "other"], cwd=repo, capture_output=True, check=False)


def test_unresolved_conflicts_and_a_nested_repository_are_refused_with_the_cause(repo):
    _conflict(repo)
    with pytest.raises(DB.DirtyBaselineUnsupported, match="unresolved merge conflicts in c.txt"):
        DB.capture_dirty_baseline(repo)
    _git(repo, "merge", "--abort")
    _git(repo, "init", "-q", str(repo / "sub"))
    with pytest.raises(DB.DirtyBaselineUnsupported, match="nested repository or submodule"):
        DB.capture_dirty_baseline(repo)


def test_a_conflict_stops_do_before_any_step_and_does_not_ask_for_a_clean_tree(repo, capsys):
    from apps.cli.commands.do_cmd import _resolve_do_commit_flags

    _conflict(repo)
    with pytest.raises(SystemExit) as exc:
        _resolve_do_commit_flags(str(repo), commit=None, commit_auto=False,
                                 commit_with_history=False, push=False, plan_only=False)
    err = capsys.readouterr().err
    assert exc.value.code == 2 and "unresolved merge conflicts" in err and "Nothing was run." in err
    assert "commit or stash" not in err


def test_modes_symlinks_deletions_and_untracked_files_are_represented_exactly(repo, tmp_path):
    (repo / "run.sh").write_text("#!/bin/sh\n")
    (repo / "gone.txt").write_text("gone\n")
    (repo / "link").symlink_to("base.txt")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "files")
    (repo / "run.sh").chmod(0o755)
    (repo / "gone.txt").unlink()
    (repo / "link").unlink()
    (repo / "link").write_text("now a regular file\n")
    (repo / "fresh.txt").write_text("untracked\n")
    (repo / "newlink").symlink_to("fresh.txt")

    baseline = DB.capture_dirty_baseline(repo)
    kinds = {e.path: (e.kind, e.executable) for e in baseline.entries}
    assert kinds == {"run.sh": ("file", True), "gone.txt": ("absent", False),
                     "link": ("file", False), "fresh.txt": ("file", False),
                     "newlink": ("symlink", False)}

    workspace = tmp_path / "ws"
    _git(repo, "worktree", "add", "-q", "--detach", str(workspace), "HEAD")
    assert DB.seed_workspace_from_baseline(baseline, workspace) is True
    assert not (workspace / "gone.txt").exists()
    assert os.access(workspace / "run.sh", os.X_OK) and not (workspace / "link").is_symlink()
    assert os.readlink(workspace / "newlink") == "fresh.txt"
    assert (workspace / "fresh.txt").read_text() == "untracked\n"
    assert _git(workspace, "status", "--porcelain") == ""          # the baseline is committed
    assert DB.baseline_drift(repo, baseline.to_dict()) == []
    (repo / "run.sh").chmod(0o644)
    assert DB.baseline_drift(repo, baseline.to_dict()) == ["run.sh"]
    assert stat.S_IMODE(os.stat(repo / "fresh.txt").st_mode)        # the target is still readable


def test_size_and_count_limits_refuse_instead_of_copying(repo, monkeypatch):
    monkeypatch.setattr(DB, "MAX_BASELINE_PATHS", 2)
    for i in range(3):
        (repo / f"f{i}.txt").write_text("x\n")
    with pytest.raises(DB.DirtyBaselineUnsupported, match="uncommitted paths, over the 2"):
        DB.capture_dirty_baseline(repo)
