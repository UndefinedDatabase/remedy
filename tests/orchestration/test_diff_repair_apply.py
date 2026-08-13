"""Tests for diff_repair_apply.py (F111 T002, apply half).

Seven proofs, one per behaviour the feature file names: a clean diff lands, a
conflicting hunk falls back with BOTH files byte-identical to their pre-attempt
state, a fence-denied path never reaches the applicator, a validation rejection
short-circuits, a creation diff falls back instead of creating (DECISION F111
D6), a blank context line stripped in transport still lands (R-0313), and the
job's own fences are used when the caller passes none.

The approved-job scaffolding is the one
tests/orchestration/test_source_apply_transaction.py already uses: a real Job
with repo_generated_write, one Artifact carrying patch_intent_explanations, and
an APPROVED intent. Nothing here fakes the applicator except where a test must
prove the applicator is NOT reached.
"""

from __future__ import annotations

from uuid import uuid4

from packages.core.models import JobFences
from packages.orchestration.diff_repair_apply import (
    DIFF_REPAIR_MODE_DIFF,
    DIFF_REPAIR_MODE_FULL_FALLBACK,
    apply_diff_repair,
)
from packages.orchestration.diff_repair_response import DiffRepairResponse


def _make_approved_job(tmp_path, monkeypatch):
    """A saved Job with repo_generated_write and one APPROVED patch intent."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    from packages.core.models import Artifact, Job
    from packages.orchestration.approval_queue import (
        APPROVAL_APPROVED,
        make_intent_id,
        set_approval_state,
    )
    from packages.orchestration.permissions import Capability, set_permission
    from packages.orchestration.storage import save_job

    job = Job(name="diff-repair-apply-test")
    set_permission(job, Capability.repo_generated_write, allow=True)

    artifact = Artifact(task_id=uuid4(), name="test-patch", content="")
    artifact.metadata = {"patch_intent_explanations": [
        {"file": "test", "action": "modify", "risk": "low",
         "reason": "test", "summary": "test patch"}
    ]}
    job.artifacts.append(artifact)
    save_job(job)

    intent_id = make_intent_id(artifact.id, 0)
    set_approval_state(job, intent_id, APPROVAL_APPROVED)
    return job, intent_id


def _applicator_must_not_run(*args, **kwargs):
    """Stand-in that fails the test if the applicator is reached at all."""
    raise AssertionError("apply_structured_patch must not be called")


def test_clean_diff_applies_and_reports_diff_mode(tmp_path, monkeypatch):
    """A well-formed, in-fence diff lands and the round reports mode `diff`."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "a.py").write_text("line1\nline2\n")

    job, intent_id = _make_approved_job(tmp_path, monkeypatch)
    response = DiffRepairResponse(
        diff=(
            "--- a/a.py\n"
            "+++ b/a.py\n"
            "@@ -1,2 +1,2 @@\n"
            "-line1\n"
            "+LINE1\n"
            " line2\n"
        ),
        files=("a.py",),
    )

    result = apply_diff_repair(response, repo, job=job, intent_id=intent_id)

    assert result.mode == DIFF_REPAIR_MODE_DIFF
    assert result.applied is True
    assert result.fallback_reason == ""
    assert (repo / "a.py").read_text() == "LINE1\nline2\n"


def test_conflicting_hunk_falls_back_and_leaves_both_files_untouched(
    tmp_path, monkeypatch
):
    """All-or-nothing: the clean section is rolled back with the failing one.

    The proof reads the REAL files after the call, not the result object: a
    result that merely claims nothing was applied cannot show a partial write.
    """
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "a.py").write_text("line1\nline2\n")
    (repo / "b.py").write_text("beta1\nbeta2\n")

    job, intent_id = _make_approved_job(tmp_path, monkeypatch)
    response = DiffRepairResponse(
        diff=(
            "--- a/a.py\n"
            "+++ b/a.py\n"
            "@@ -1,2 +1,2 @@\n"
            "-line1\n"
            "+LINE1\n"
            " line2\n"
            "--- a/b.py\n"
            "+++ b/b.py\n"
            "@@ -1,2 +1,2 @@\n"
            "-not-the-real-line\n"
            "+REPLACED\n"
            " beta2\n"
        ),
        files=("a.py", "b.py"),
    )

    a_before = (repo / "a.py").read_bytes()
    b_before = (repo / "b.py").read_bytes()

    result = apply_diff_repair(response, repo, job=job, intent_id=intent_id)

    assert result.mode == DIFF_REPAIR_MODE_FULL_FALLBACK
    assert result.applied is False
    assert result.fallback_reason.startswith("apply_failed:")
    assert (repo / "a.py").read_bytes() == a_before
    assert (repo / "b.py").read_bytes() == b_before


def test_fence_denied_path_never_reaches_the_applicator(tmp_path, monkeypatch):
    """The acceptance criterion: rejection happens BEFORE any applicator call."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "remedy.toml").write_text("x = 1\ny = 3\n")

    job, intent_id = _make_approved_job(tmp_path, monkeypatch)
    monkeypatch.setattr(
        "packages.orchestration.diff_repair_apply.apply_structured_patch",
        _applicator_must_not_run,
    )
    response = DiffRepairResponse(
        diff=(
            "--- a/remedy.toml\n"
            "+++ b/remedy.toml\n"
            "@@ -1,2 +1,2 @@\n"
            "-x = 1\n"
            "+x = 2\n"
            " y = 3\n"
        ),
        files=("remedy.toml",),
    )

    result = apply_diff_repair(response, repo, job=job, intent_id=intent_id)

    assert result.mode == DIFF_REPAIR_MODE_FULL_FALLBACK
    assert result.fallback_reason.startswith("fence_denied:")
    assert "remedy.toml" in result.fallback_reason
    assert result.apply_id == ""


def test_validation_rejection_short_circuits_before_the_applicator(
    tmp_path, monkeypatch
):
    """A declared path the diff never touches stops the round with no disk work."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "a.py").write_text("line1\nline2\n")
    (repo / "b.py").write_text("beta1\nbeta2\n")

    job, intent_id = _make_approved_job(tmp_path, monkeypatch)
    monkeypatch.setattr(
        "packages.orchestration.diff_repair_apply.apply_structured_patch",
        _applicator_must_not_run,
    )
    response = DiffRepairResponse(
        diff=(
            "--- a/b.py\n"
            "+++ b/b.py\n"
            "@@ -1,2 +1,2 @@\n"
            "-beta1\n"
            "+BETA1\n"
            " beta2\n"
        ),
        files=("a.py",),
    )

    result = apply_diff_repair(response, repo, job=job, intent_id=intent_id)

    assert result.mode == DIFF_REPAIR_MODE_FULL_FALLBACK
    assert result.fallback_reason.startswith("validation:")
    assert result.apply_id == ""


def test_new_file_creation_diff_falls_back_instead_of_creating(
    tmp_path, monkeypatch
):
    """DECISION F111 D6: a creation diff is NOT applied as a diff in v1.

    `source_apply._apply_unified_diff` requires the target to exist, so the
    `@@ -0,0 +1,N @@` answer fails the apply and the round falls back to the
    full-file path, which creates files through `_apply_file_op`'s `create`
    action. See docs/roadmap/features/T2_F111.md, Built State section D6.
    """
    repo = tmp_path / "repo"
    repo.mkdir()

    job, intent_id = _make_approved_job(tmp_path, monkeypatch)
    response = DiffRepairResponse(
        diff=(
            "--- /dev/null\n"
            "+++ b/new.py\n"
            "@@ -0,0 +1,2 @@\n"
            "+alpha\n"
            "+beta\n"
        ),
        files=("new.py",),
    )

    result = apply_diff_repair(response, repo, job=job, intent_id=intent_id)

    assert result.mode == DIFF_REPAIR_MODE_FULL_FALLBACK
    assert result.applied is False
    assert result.fallback_reason.startswith("apply_failed:")
    assert (repo / "new.py").exists() is False


def test_stripped_blank_context_line_lands_instead_of_falling_back(
    tmp_path, monkeypatch
):
    """R-0313: a blank context line that lost its space no longer costs the round.

    This EXACT input returned mode `full_fallback` before
    `diff_repair_response.normalize_diff_blank_context` existed: the applicator
    read the bare "" as neither context, removal nor addition, so `-b` was
    compared against the wrong original line and every hunk was rejected. The
    applicator is unchanged; the response half now hands it a repaired diff.
    """
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "c.py").write_text("a\n\nb\n")

    job, intent_id = _make_approved_job(tmp_path, monkeypatch)
    response = DiffRepairResponse(
        diff=(
            "--- a/c.py\n"
            "+++ b/c.py\n"
            "@@ -1,3 +1,3 @@\n"
            " a\n"
            "\n"
            "-b\n"
            "+B\n"
        ),
        files=("c.py",),
    )

    result = apply_diff_repair(response, repo, job=job, intent_id=intent_id)

    assert result.mode == DIFF_REPAIR_MODE_DIFF
    assert result.applied is True
    assert (repo / "c.py").read_text() == "a\n\nB\n"


def test_job_fences_are_derived_when_the_caller_passes_none(tmp_path, monkeypatch):
    """No `job_fences` argument means the JOB's fences, not the default spec.

    `docs/guide.md` passes the default spec, so this test only goes green if the
    job's own allow list reached `precheck_diff_repair_fences`.
    """
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "docs").mkdir()
    (repo / "docs" / "guide.md").write_text("intro\nbody\n")

    job, intent_id = _make_approved_job(tmp_path, monkeypatch)
    job.fences = JobFences(allow=["src/**"], deny=[])

    response = DiffRepairResponse(
        diff=(
            "--- a/docs/guide.md\n"
            "+++ b/docs/guide.md\n"
            "@@ -1,2 +1,2 @@\n"
            "-intro\n"
            "+INTRO\n"
            " body\n"
        ),
        files=("docs/guide.md",),
    )

    result = apply_diff_repair(response, repo, job=job, intent_id=intent_id)

    assert result.mode == DIFF_REPAIR_MODE_FULL_FALLBACK
    assert result.fallback_reason.startswith("fence_denied:")
    assert "docs/guide.md" in result.fallback_reason
    assert any("docs/guide.md" in entry for entry in result.errors)
    assert (repo / "docs" / "guide.md").read_text() == "intro\nbody\n"
