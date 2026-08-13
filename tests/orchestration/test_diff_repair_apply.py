"""Tests for diff_repair_apply.py (F111 T002, apply half).

Nine proofs, one per behaviour the feature file names: a clean diff lands, a
conflicting hunk falls back with BOTH files byte-identical to their pre-attempt
state, a rollback the applicator could not finish is reported instead of being
summarised as a clean tree (R-0316), a fence-denied path never reaches the
applicator, a validation rejection short-circuits, a creation diff falls back
instead of creating (DECISION F111 D6), a blank context line stripped in
transport still lands (R-0313), a two-file answer whose first file continues
past its hunk lands (R-0317), and the job's own fences are used when the caller
passes none.

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
from packages.orchestration.source_apply import ApplyResult


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
    # The other half of R-0316: a rollback that DID finish reports a clean tree,
    # so the honest-count path below cannot be satisfied by always reporting one.
    assert result.rollback_incomplete is False
    assert result.files_modified == 0


def test_incomplete_rollback_reports_the_real_count_not_a_clean_tree(
    tmp_path, monkeypatch
):
    """R-0316: a rollback that did not finish is never summarised as 0 files.

    `source_apply._rollback_from_snapshot` catches OSError per entry and appends
    `rollback_incomplete (N file(s)): …` to the errors, leaving those files
    half-restored. That OSError cannot be provoked from outside the applicator,
    so the applicator is stubbed with the exact result shape it produces: what
    is under test is THIS seam's reading of that error string, not the rollback.
    """
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "a.py").write_text("line1\nline2\n")

    job, intent_id = _make_approved_job(tmp_path, monkeypatch)

    def _apply_with_failed_rollback(*args, **kwargs):
        return ApplyResult(
            apply_id="x",
            success=False,
            files_modified=1,
            files_created=0,
            errors=[
                "a.py: diff hunks did not apply cleanly",
                "rollback_incomplete (1 file(s)): a.py",
            ],
            snapshot_id="s",
            snapshot_verified=True,
        )

    monkeypatch.setattr(
        "packages.orchestration.diff_repair_apply.apply_structured_patch",
        _apply_with_failed_rollback,
    )
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

    assert result.mode == DIFF_REPAIR_MODE_FULL_FALLBACK
    assert result.applied is False
    assert result.rollback_incomplete is True
    assert result.files_modified == 1


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


def test_two_file_answer_whose_first_file_continues_past_its_hunk_lands(
    tmp_path, monkeypatch
):
    """R-0317: a blank line between two file sections is no longer eaten.

    Before the R-0317 fix this EXACT input returned mode `full_fallback`: the
    first hunk declares `@@ -1,3 +1,3 @@` over a body that spends only two old
    and two new lines, so the separator blank still fell inside the declared
    budget, was rewritten to " " and rode into `split_diff_by_path` as a
    trailing context line of app.py — which the applicator then compared against
    `more = 3` and rejected. The applicator is unchanged; the normaliser now
    classifies that blank by what FOLLOWS it.
    """
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "app.py").write_text("import os\nvalue = 1\nmore = 3\n")
    (repo / "util.py").write_text("helper = 1\n")

    job, intent_id = _make_approved_job(tmp_path, monkeypatch)
    response = DiffRepairResponse(
        diff=(
            "--- a/app.py\n+++ b/app.py\n@@ -1,3 +1,3 @@\n import os\n-value = 1\n"
            "+value = 2\n\n--- a/util.py\n+++ b/util.py\n@@ -1,1 +1,1 @@\n"
            "-helper = 1\n+helper = 2\n"
        ),
        files=("app.py", "util.py"),
    )

    result = apply_diff_repair(response, repo, job=job, intent_id=intent_id)

    assert result.mode == DIFF_REPAIR_MODE_DIFF
    assert result.applied is True
    assert (repo / "app.py").read_text() == "import os\nvalue = 2\nmore = 3\n"
    assert (repo / "util.py").read_text() == "helper = 2\n"


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
