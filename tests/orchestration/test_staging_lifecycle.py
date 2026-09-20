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
# The terminal hook, which releases NOTHING (DECISION F276 D6)
# ---------------------------------------------------------------------------

def test_a_completed_copy_job_keeps_its_staging_copy_through_the_hook(root):
    """THE REGRESSION GUARD of DECISION F276 D6, and the point of the round.

    T003 released here, at job completion. That destroyed the deliverable of every
    copy job nobody had applied yet, because a copy job has NO retained branch —
    its staging copy is the only place the work exists, and ``job_apply`` reads
    that very directory as its sole apply source. Measured: 19 red nodes in
    ``tests/orchestration/test_job_apply.py`` at ``f7d668d9``, all green at
    ``92d4c38b`` and under a neuter of the four added lines. Put the release back
    into the hook and this test goes red — which is the whole reason it exists.
    """
    job = _job(root, RunState.COMPLETED)
    staging = _staging(root, job.job_id)
    assert staging.is_dir()

    # handle=None IS the copy case: a copy job never has a worktree handle.
    _finalize_job_workspace(job, None)

    assert staging.is_dir()
    assert (staging / "copied.txt").exists()


def test_a_running_copy_job_is_refused_by_the_release_s_own_floor(root):
    """LAYER TWO, unchanged by D6: `remedy job resume` will want this scratch.

    The hook keeps it because the hook keeps everything now; the interesting claim
    is the one below it — the PUBLIC function refuses a non-terminal job on its own
    authority, in ``data_reclaim``'s vocabulary, so nothing can free what reclaim
    would refuse.
    """
    job = _job(root, RunState.RUNNING)
    staging = _staging(root, job.job_id)

    _finalize_job_workspace(job, None)
    assert staging.is_dir()

    outcome = release_staging_workspace(job.job_id, root)
    assert outcome.reason == "job_not_terminal"
    assert outcome.existed is True
    assert outcome.released is False
    assert staging.is_dir()


def test_release_frees_a_failed_job_on_its_own_authority(root):
    """LAYER TWO's positive case: FAILED clears reclaim's floor, so a direct call frees it.

    Its pair is the parametrised hook test above, where the same FAILED job is kept:
    the hook asks nobody, the function decides for itself.
    """
    job = _job(root, RunState.FAILED)
    staging = _staging(root, job.job_id)

    outcome = release_staging_workspace(job.job_id, root)

    assert outcome.released is True
    assert outcome.reason == ""
    assert not staging.exists()


@pytest.mark.parametrize("state", [
    RunState.COMPLETED, RunState.FAILED, RunState.BLOCKED,
    RunState.PAUSED, RunState.STOPPED, RunState.CANCELLED,
])
def test_the_terminal_hook_keeps_every_copy_job_whatever_its_state(root, state):
    """DECISION F276 D6: the hook's copy branch frees NOTHING, in any state.

    ``COMPLETED`` is in this list on purpose and is the state that regressed; the
    other five were already kept by T003 and are here so a repair that traded one
    state for another cannot pass. What frees a copy is an APPLY that applied, and
    failing that, ``remedy data reclaim`` when the operator asks.
    """
    job = _job(root, state)
    staging = _staging(root, job.job_id)

    _finalize_job_workspace(job, None)

    assert staging.is_dir()
    assert (staging / "copied.txt").exists()


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


# ---------------------------------------------------------------------------
# The apply is what CONSUMES a copy, and the only thing that frees it
# (DECISION F276 D6). These run the REAL ``run_job`` over a NON-GIT target —
# which is what puts a job in ``isolation_mode="copy"`` — with the fake builder
# and reviewer, so no provider is called, and then the REAL ``apply_job``.
# ---------------------------------------------------------------------------

_APPLY_JOB_TEXT = """\
# Job: Staging Release

## Task 1
Add a test file.

Acceptance:
- file exists
"""


@pytest.fixture()
def copy_job(root, tmp_path):
    """A COMPLETED copy-mode job over a non-git target, and its staging copy."""
    from pathlib import Path

    from packages.orchestration.pingpong_job import parse_job_file, run_job
    from packages.orchestration.pingpong_provider import FakeProvider

    target = tmp_path / "target"
    target.mkdir()
    (target / "README.md").write_text("# Demo\n")

    plan = parse_job_file(_APPLY_JOB_TEXT, str(target))
    done = run_job(
        plan.job_id,
        builder_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
        reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
        repair_rounds=0,
    )
    assert done.state == RunState.COMPLETED, done.error
    assert done.isolation_mode == "copy"
    staging = Path(done.job_workspace_path)
    assert staging.is_dir(), "the job's own copy must survive its completion"
    return done, target, staging


def test_a_completed_copy_job_that_was_never_applied_keeps_its_copy(copy_job):
    """END TO END, and the regression the 19 ``test_job_apply`` nodes needed.

    Nothing between ``run_job`` returning and an operator deciding what to do may
    delete this directory: it holds work nobody has taken.
    """
    _done, _target, staging = copy_job

    assert staging.is_dir()
    assert any(staging.rglob("*"))


def test_an_applied_copy_jobs_staging_copy_is_gone_after_the_apply(copy_job):
    from packages.orchestration.job_apply import apply_job

    done, target, staging = copy_job

    result = apply_job(done.job_id, str(target), approve=True)

    assert result.status == "applied"
    assert not staging.exists()
    assert result.staging_release.startswith("released ")


def test_a_dry_run_apply_leaves_the_staging_copy_in_place(copy_job):
    """A preview consumes nothing, so it frees nothing."""
    from packages.orchestration.job_apply import apply_job

    done, target, staging = copy_job

    result = apply_job(done.job_id, str(target), dry_run=True)

    assert result.status == "dry_run"
    assert staging.is_dir()
    assert result.staging_release == "kept (apply status dry_run)"


def test_an_unapproved_apply_leaves_the_staging_copy_in_place(copy_job):
    """No ``--approve`` is a preview too, by a different route to the same status."""
    from packages.orchestration.job_apply import apply_job

    done, target, staging = copy_job

    result = apply_job(done.job_id, str(target))

    assert result.status == "dry_run"
    assert staging.is_dir()


def test_a_blocked_apply_leaves_the_staging_copy_in_place(copy_job):
    """The apply refused, so the work is still untaken and its copy still holds it."""
    from packages.orchestration.job_apply import apply_job

    done, target, staging = copy_job
    missing_target = target / "not_a_directory"

    result = apply_job(done.job_id, str(missing_target), approve=True)

    assert result.status == "blocked"
    assert not missing_target.exists()
    assert staging.is_dir()
    assert result.staging_release == "kept (apply status blocked)"


def test_a_second_apply_of_the_same_job_finds_its_source_gone(copy_job):
    """What the release MEANS, stated from the other side."""
    from packages.orchestration.job_apply import apply_job

    done, target, staging = copy_job

    assert apply_job(done.job_id, str(target), approve=True).status == "applied"
    assert not staging.exists()

    second = apply_job(done.job_id, str(target), approve=True)
    assert second.status == "blocked"
    assert "workspace_missing" in second.blocked_reason


def test_the_no_op_release_is_reported_as_already_gone_not_as_a_refusal(root):
    """``existed=False`` is a no-op, and must never be rendered as a refusal."""
    from packages.orchestration.job_apply import (
        JobApplyResult,
        _release_consumed_staging_copy,
    )

    job = _job(root, RunState.COMPLETED)          # no staging copy on disk at all
    result = JobApplyResult(job_id=job.job_id, status="applied")

    _release_consumed_staging_copy(job, result)

    assert result.staging_release == "already gone"


def test_a_worktree_job_gets_no_staging_release_line_at_all(root):
    """The field stays EMPTY for a mode that has no staging copy — not "kept"."""
    from packages.orchestration.job_apply import (
        JobApplyResult,
        _release_consumed_staging_copy,
    )

    job = _job(root, RunState.COMPLETED, isolation_mode="worktree")
    result = JobApplyResult(job_id=job.job_id, status="applied")

    _release_consumed_staging_copy(job, result)

    assert result.staging_release == ""
