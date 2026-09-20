"""The copy-mode lifecycle: the release, and the two filters (F276 T003).

Every fixture writes a REAL job record through ``save_job_plan`` and, where git is
involved, a REAL ``git init``ed repository, so the terminal check and the ignore
rules these tests exercise are the ones production reads rather than stubs of them.
No test touches the operator's data root: each builds its own tree under ``tmp_path``
and points ``REMEDY_DATA_DIR`` at it through ``monkeypatch``.
"""
from __future__ import annotations

import os
import subprocess

import pytest

from packages.core.models import RunState
from packages.orchestration.pingpong_job import (
    JobPlan,
    _finalize_job_workspace,
    save_job_plan,
)
from packages.orchestration.staging_workspace import (
    GITIGNORE_FILTER_APPLIED,
    GITIGNORE_FILTER_NO_GIT,
    MAX_COPY_FILE_BYTES,
    STAGING_DATA_CLASS,
    create_staging_workspace,
    release_staging_workspace,
    staging_dir_name,
)


@pytest.fixture()
def root(tmp_path, monkeypatch):
    """An isolated data root, set IN-PROCESS — never a shell assignment."""
    r = tmp_path / "data"
    r.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(r))
    return r


def _job(root, state: RunState, isolation_mode: str = "copy") -> JobPlan:
    """One persisted job record under ``root``; returns the in-memory plan too."""
    from packages.orchestration.data_paths import mint_job_id

    job = JobPlan(job_id=mint_job_id(), repo_path=str(root), state=state)
    job.isolation_mode = isolation_mode
    save_job_plan(job, root)
    return job


def _staging(root, job_id: str, payload: bytes = b"x" * 128):
    """That job's staging copy, as ``_create_job_workspace_copy`` would leave it."""
    d = root / STAGING_DATA_CLASS / staging_dir_name(job_id)
    d.mkdir(parents=True)
    (d / "copied.txt").write_bytes(payload)
    return d


def _git_repo(path):
    """A REAL git repository at ``path``; skips when the sandbox refuses ``git init``."""
    path.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(["git", "init", "-q", str(path)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        pytest.skip(f"git init refused: rc={proc.returncode} {proc.stderr.strip()!r}")
    return path


# ---------------------------------------------------------------------------
# The release, on the hook the worktree cleanup already uses
# ---------------------------------------------------------------------------

def test_terminal_copy_job_is_released_by_the_hook(root):
    """THE RED PROOF the feature file names: remove the call and this reddens."""
    job = _job(root, RunState.COMPLETED)
    staging = _staging(root, job.job_id)
    assert staging.is_dir()

    # handle=None IS the copy case: a copy job never has a worktree handle.
    _finalize_job_workspace(job, None)

    assert not staging.exists()


def test_non_terminal_copy_job_keeps_its_staging_copy(root):
    """`remedy job resume` will want it, so a running job's scratch is not freed."""
    job = _job(root, RunState.RUNNING)
    staging = _staging(root, job.job_id)

    _finalize_job_workspace(job, None)

    assert staging.is_dir()
    assert (staging / "copied.txt").exists()

    outcome = release_staging_workspace(job.job_id, root)
    assert outcome.reason == "job_not_terminal"
    assert outcome.existed is True
    assert outcome.released is False


def test_failed_copy_job_keeps_its_staging_copy_through_the_hook(root):
    """LAYER ONE. The hook is as strict as the worktree path: only COMPLETED frees.

    A FAILED job IS terminal to ``data_reclaim``, so this is not the release refusing
    — it is the hook never asking, exactly as a FAILED worktree job keeps its
    worktree. Widen the hook's condition to ``job_is_terminal`` and this reddens.
    """
    job = _job(root, RunState.FAILED)
    staging = _staging(root, job.job_id)

    _finalize_job_workspace(job, None)

    assert staging.is_dir()
    assert (staging / "copied.txt").exists()


def test_release_frees_that_same_failed_job_on_its_own_authority(root):
    """LAYER TWO. The public function's own floor is reclaim's, and FAILED clears it.

    The pair with the test above: the same job, the same state, released when called
    directly and kept when reached through the hook. Two layers, each pinned.
    """
    job = _job(root, RunState.FAILED)
    staging = _staging(root, job.job_id)

    outcome = release_staging_workspace(job.job_id, root)

    assert outcome.released is True
    assert outcome.reason == ""
    assert not staging.exists()


@pytest.mark.parametrize("state", [
    RunState.BLOCKED, RunState.PAUSED, RunState.STOPPED, RunState.CANCELLED,
])
def test_the_hook_keeps_every_copy_job_that_did_not_complete(root, state):
    """Each keeps its pending work or its evidence; `data reclaim` offers them later."""
    job = _job(root, state)
    staging = _staging(root, job.job_id)

    _finalize_job_workspace(job, None)

    assert staging.is_dir()


def test_second_release_is_a_no_op_not_an_error(root):
    job = _job(root, RunState.COMPLETED)
    staging = _staging(root, job.job_id)

    first = release_staging_workspace(job.job_id, root)
    assert first.released is True
    assert first.existed is True
    assert first.freed_bytes > 0
    assert not staging.exists()

    second = release_staging_workspace(job.job_id, root)
    assert second.released is False
    assert second.existed is False
    assert second.reason == ""          # a no-op, NOT a refusal
    assert second.freed_bytes == 0


def test_symlinked_staging_path_is_refused(root, tmp_path):
    """A link is never followed and never deleted — the target survives."""
    job = _job(root, RunState.COMPLETED)
    outside = tmp_path / "not_scratch"
    outside.mkdir()
    (outside / "precious.txt").write_text("keep me")

    class_dir = root / STAGING_DATA_CLASS
    class_dir.mkdir(parents=True)
    link = class_dir / staging_dir_name(job.job_id)
    link.symlink_to(outside, target_is_directory=True)

    outcome = release_staging_workspace(job.job_id, root)

    assert outcome.reason == "symlink"
    assert outcome.released is False
    assert link.is_symlink()
    assert (outside / "precious.txt").read_text() == "keep me"


def test_release_reason_vocabulary_is_the_reclaim_command_s(root):
    """No second spelling: every reason release returns is one reclaim already names."""
    from packages.orchestration.data_reclaim import REFUSAL_REASONS

    job = _job(root, RunState.RUNNING)
    _staging(root, job.job_id)
    assert release_staging_workspace(job.job_id, root).reason in REFUSAL_REASONS


# ---------------------------------------------------------------------------
# The copy filters
# ---------------------------------------------------------------------------

def test_gitignored_large_artifact_is_not_copied_and_is_recorded(tmp_path):
    repo = _git_repo(tmp_path / "target")
    (repo / ".gitignore").write_text("*.zip\n")
    (repo / "README.md").write_text("# real source")
    artifact = repo / "remedy-review-20260920.zip"
    artifact.write_bytes(b"Z" * 300_000)

    ws = create_staging_workspace(repo, tmp_path / "staging", "0123456789abcdef")

    assert not (ws.staging_dir / "remedy-review-20260920.zip").exists()
    assert (ws.staging_dir / "README.md").exists()
    assert ws.excluded_ignored == ["remedy-review-20260920.zip"]
    assert ws.excluded_oversize == []
    assert ws.excluded_bytes == artifact.stat().st_size == 300_000
    assert ws.gitignore_filter == GITIGNORE_FILTER_APPLIED


#: A LITERAL, deliberately not derived from ``MAX_COPY_FILE_BYTES``: a fixture sized
#: from the constant would follow it wherever it went, and a test whose input moves
#: with the thing it measures cannot red-prove a raised ceiling.
_OVER_CEILING_BYTES = 17 * 1024 * 1024


def test_the_ceiling_has_the_value_its_measurement_chose():
    assert MAX_COPY_FILE_BYTES == 16 * 1024 * 1024
    assert _OVER_CEILING_BYTES > MAX_COPY_FILE_BYTES


def test_file_over_the_ceiling_is_skipped_even_when_git_does_not_ignore_it(tmp_path):
    """The ceiling is the BACKSTOP: no ignore rule covers this path and it still goes."""
    repo = _git_repo(tmp_path / "target")
    (repo / ".gitignore").write_text("*.zip\n")
    (repo / "small.txt").write_text("source")
    huge = repo / "enormous.bin"
    with open(huge, "wb") as fh:          # sparse: st_size is real, the disk cost is not
        fh.truncate(_OVER_CEILING_BYTES)
    assert huge.stat().st_size == _OVER_CEILING_BYTES

    ws = create_staging_workspace(repo, tmp_path / "staging", "0123456789abcdef")

    assert not (ws.staging_dir / "enormous.bin").exists()
    assert (ws.staging_dir / "small.txt").exists()
    assert ws.excluded_oversize == ["enormous.bin"]
    assert ws.excluded_ignored == []
    assert ws.excluded_bytes == _OVER_CEILING_BYTES


def test_non_git_target_still_copies_and_says_the_filter_was_absent(tmp_path):
    repo = tmp_path / "target"
    repo.mkdir()
    (repo / "notes.txt").write_text("a target with no git at all")
    (repo / "build.log").write_text("x" * 100)

    ws = create_staging_workspace(repo, tmp_path / "staging", "0123456789abcdef")

    assert (ws.staging_dir / "notes.txt").exists()
    assert (ws.staging_dir / "build.log").exists()
    assert ws.files_copied == 2
    assert ws.excluded_ignored == []
    assert ws.excluded_bytes == 0
    assert ws.gitignore_filter == GITIGNORE_FILTER_NO_GIT
    assert ".git" in ws.gitignore_detail


def test_the_ignore_pass_is_one_subprocess_for_the_whole_tree(tmp_path, monkeypatch):
    """One process, not one per file — the candidate list goes in on stdin."""
    import packages.orchestration.staging_workspace as sw

    repo = _git_repo(tmp_path / "target")
    (repo / ".gitignore").write_text("*.log\n")
    for i in range(12):
        (repo / f"src{i}.py").write_text(f"x = {i}")
        (repo / f"out{i}.log").write_text("noise")

    calls: list[list[str]] = []
    real = sw.subprocess.run

    def spy(cmd, *args, **kwargs):
        calls.append(list(cmd))
        return real(cmd, *args, **kwargs)

    monkeypatch.setattr(sw.subprocess, "run", spy)
    ws = create_staging_workspace(repo, tmp_path / "staging", "0123456789abcdef")

    assert calls == [["git", "check-ignore", "--stdin", "-z"]]
    assert len(ws.excluded_ignored) == 12
    # 12 sources plus `.gitignore` itself: only dot-DIRECTORIES are excluded, and
    # nothing in this slice changed that.
    assert ws.files_copied == 13


def test_a_tracked_file_over_no_ignore_rule_is_copied(tmp_path):
    """`check-ignore` consults the index, so tracked source is never filtered out."""
    repo = _git_repo(tmp_path / "target")
    (repo / ".gitignore").write_text("*.zip\n")
    keeper = repo / "keeper.zip"
    keeper.write_bytes(b"tracked despite the pattern")
    add = subprocess.run(["git", "-C", str(repo), "add", "-f", "keeper.zip"],
                         capture_output=True, text=True)
    if add.returncode != 0:
        pytest.skip(f"git add refused: {add.stderr.strip()!r}")

    ws = create_staging_workspace(repo, tmp_path / "staging", "0123456789abcdef")

    assert (ws.staging_dir / "keeper.zip").exists()
    assert ws.excluded_ignored == []


# ---------------------------------------------------------------------------
# The end-to-end shape: a copy, then its release
# ---------------------------------------------------------------------------

def test_a_copy_made_under_the_data_root_is_the_one_the_release_finds(root, tmp_path):
    """The release derives its path from the class registry, not from the record."""
    repo = tmp_path / "target"
    repo.mkdir()
    (repo / "main.py").write_text("print('hi')")

    job = _job(root, RunState.COMPLETED)
    parent = root / STAGING_DATA_CLASS
    parent.mkdir(parents=True)
    ws = create_staging_workspace(repo, parent, job.job_id)
    assert ws.staging_dir.is_dir()

    job.job_workspace_path = "/somewhere/else/entirely"   # input, not authority
    outcome = release_staging_workspace(job.job_id, root)

    assert outcome.released is True
    assert outcome.path == os.fspath(ws.staging_dir)
    assert not ws.staging_dir.exists()
