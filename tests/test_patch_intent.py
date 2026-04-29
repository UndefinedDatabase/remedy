"""
Tests for packages/orchestration/patch_intent.py.

Covers:
  - PatchIntent model: field defaults, validation
  - PatchIntentSet model: field defaults, serialization round-trip
  - derive_patch_intents: known eligible task types, unknown types, ineligible types
  - verify_patch_intent_set: valid set, absolute path, traversal, non-md, empty intent, empty set
  - materialize_patch_intents: correct file path, JSON content, empty set returns None
  - artifact metadata: patch_intent_file and patch_intent_count set correctly
  - Step 10.5 additions:
      - null-byte path rejected by verifier
      - missing artifact.id / task_id raises RuntimeError
      - keyword sync: _INTENT_RULES and _REPO_PATH_RULES keyword sets stay in sync
      - verification errors recorded in artifact metadata; no file written
  - Step 11 additions (dry-run preview and explanation layer):
      - _extract_proposed_lines: known sections parsed correctly
      - generate_dry_run_preview: no repo → preview-only; existing file → modify;
        missing file → create; empty intents → empty list
      - format_dry_run_explanations: correct labeled block format

All tests are deterministic — no live Ollama, no builder, no repo writes.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from packages.core.models import Artifact
from packages.orchestration.patch_intent import (
    PatchDryRunResult,
    PatchIntent,
    PatchIntentSet,
    _extract_proposed_lines,
    derive_patch_intents,
    format_dry_run_explanations,
    generate_dry_run_preview,
    materialize_patch_intents,
    verify_patch_intent_set,
)
from packages.orchestration.workspace import LocalWorkspaceRuntime


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_artifact(
    task_id: UUID | None = None,
    task_type: str = "test_task",
    summary: str = "A test summary",
) -> Artifact:
    return Artifact(
        name=f"task_output_{task_type}",
        content="Builder Execution Output\n\nProposed Changes:\n  - change A",
        mime_type="text/plain",
        task_id=task_id or uuid4(),
        metadata={"task_type": task_type, "summary": summary},
    )


def _make_runtime(tmp_path: Path) -> LocalWorkspaceRuntime:
    os.environ["REMEDY_DATA_DIR"] = str(tmp_path)
    return LocalWorkspaceRuntime(job_id=uuid4())


# ---------------------------------------------------------------------------
# PatchIntent model
# ---------------------------------------------------------------------------


class TestPatchIntentModel:
    def test_required_fields(self):
        pi = PatchIntent(target_path="README.md", intent="Update readme")
        assert pi.target_path == "README.md"
        assert pi.intent == "Update readme"

    def test_optional_fields_default_to_none_or_empty(self):
        pi = PatchIntent(target_path="README.md", intent="Update")
        assert pi.rationale is None
        assert pi.expected_effect is None
        assert pi.safety_notes == []

    def test_safety_notes_populated(self):
        pi = PatchIntent(
            target_path="docs/guide.md",
            intent="Add guide",
            safety_notes=["note1", "note2"],
        )
        assert len(pi.safety_notes) == 2


# ---------------------------------------------------------------------------
# PatchIntentSet model
# ---------------------------------------------------------------------------


class TestPatchIntentSetModel:
    def test_empty_intents_is_valid(self):
        task_id = uuid4()
        artifact_id = uuid4()
        pis = PatchIntentSet(task_id=task_id, artifact_id=artifact_id)
        assert pis.intents == []

    def test_serialization_round_trip(self):
        task_id = uuid4()
        artifact_id = uuid4()
        pis = PatchIntentSet(
            task_id=task_id,
            artifact_id=artifact_id,
            intents=[PatchIntent(target_path="README.md", intent="Update")],
        )
        raw = pis.model_dump_json()
        pis2 = PatchIntentSet.model_validate_json(raw)
        assert pis2.task_id == task_id
        assert len(pis2.intents) == 1
        assert pis2.intents[0].target_path == "README.md"


# ---------------------------------------------------------------------------
# derive_patch_intents
# ---------------------------------------------------------------------------


class TestDerivePatchIntents:
    def test_readme_task_type_produces_readme_intent(self):
        artifact = _make_artifact(task_type="write_readme")
        pis = derive_patch_intents(artifact, "write_readme")
        assert len(pis.intents) == 1
        assert pis.intents[0].target_path == "README.md"

    def test_plan_task_type_produces_docs_remedy_path(self):
        artifact = _make_artifact(task_type="create_plan")
        pis = derive_patch_intents(artifact, "create_plan")
        assert len(pis.intents) == 1
        assert pis.intents[0].target_path.startswith("docs/remedy/")
        assert pis.intents[0].target_path.endswith(".md")

    def test_doc_task_type_produces_docs_path(self):
        artifact = _make_artifact(task_type="write_doc")
        pis = derive_patch_intents(artifact, "write_doc")
        assert len(pis.intents) == 1
        assert pis.intents[0].target_path.startswith("docs/")

    def test_architecture_task_type_produces_docs_path(self):
        artifact = _make_artifact(task_type="update_architecture")
        pis = derive_patch_intents(artifact, "update_architecture")
        assert len(pis.intents) == 1
        assert "architecture" in pis.intents[0].target_path

    def test_ineligible_task_type_produces_no_intents(self):
        artifact = _make_artifact(task_type="write_tests")
        pis = derive_patch_intents(artifact, "write_tests")
        assert pis.intents == []

    def test_implement_task_type_produces_no_intents(self):
        artifact = _make_artifact(task_type="implement_feature")
        pis = derive_patch_intents(artifact, "implement_feature")
        assert pis.intents == []

    def test_intent_uses_summary_when_available(self):
        artifact = _make_artifact(task_type="write_readme", summary="Improve the readme")
        pis = derive_patch_intents(artifact, "write_readme")
        assert pis.intents[0].intent == "Improve the readme"

    def test_intent_uses_fallback_when_no_summary(self):
        artifact = _make_artifact(task_type="write_readme", summary="")
        artifact.metadata["summary"] = ""
        pis = derive_patch_intents(artifact, "write_readme")
        assert "write_readme" in pis.intents[0].intent

    def test_safety_notes_are_populated(self):
        artifact = _make_artifact(task_type="write_readme")
        pis = derive_patch_intents(artifact, "write_readme")
        assert any("not applied" in note for note in pis.intents[0].safety_notes)

    def test_raises_on_planning_artifact(self):
        artifact = _make_artifact(task_type="write_readme")
        artifact.task_id = None  # planning artifacts have task_id=None
        with pytest.raises(RuntimeError, match="task_id is None"):
            derive_patch_intents(artifact, "write_readme")

    def test_spec_document_routes_to_docs_remedy(self):
        # Regression: "spec_document" must match "spec" before "doc"
        artifact = _make_artifact(task_type="spec_document")
        pis = derive_patch_intents(artifact, "spec_document")
        assert pis.intents[0].target_path.startswith("docs/remedy/")

    def test_artifact_ids_preserved(self):
        artifact = _make_artifact(task_type="write_readme")
        pis = derive_patch_intents(artifact, "write_readme")
        assert pis.task_id == artifact.task_id
        assert pis.artifact_id == artifact.id


# ---------------------------------------------------------------------------
# verify_patch_intent_set
# ---------------------------------------------------------------------------


class TestVerifyPatchIntentSet:
    def test_empty_set_is_valid(self):
        pis = PatchIntentSet(task_id=uuid4(), artifact_id=uuid4())
        assert verify_patch_intent_set(pis) == []

    def test_valid_relative_md_path_is_valid(self):
        pis = PatchIntentSet(
            task_id=uuid4(),
            artifact_id=uuid4(),
            intents=[PatchIntent(target_path="README.md", intent="Update")],
        )
        assert verify_patch_intent_set(pis) == []

    def test_absolute_path_is_rejected(self):
        pis = PatchIntentSet(
            task_id=uuid4(),
            artifact_id=uuid4(),
            intents=[PatchIntent(target_path="/etc/passwd", intent="bad")],
        )
        errors = verify_patch_intent_set(pis)
        assert any("absolute" in e for e in errors)

    def test_traversal_is_rejected(self):
        pis = PatchIntentSet(
            task_id=uuid4(),
            artifact_id=uuid4(),
            intents=[PatchIntent(target_path="../outside/repo.md", intent="bad")],
        )
        errors = verify_patch_intent_set(pis)
        assert any("traversal" in e for e in errors)

    def test_non_md_extension_is_rejected(self):
        pis = PatchIntentSet(
            task_id=uuid4(),
            artifact_id=uuid4(),
            intents=[PatchIntent(target_path="src/main.py", intent="Edit source")],
        )
        errors = verify_patch_intent_set(pis)
        assert any(".md" in e for e in errors)

    def test_empty_intent_string_is_rejected(self):
        pis = PatchIntentSet(
            task_id=uuid4(),
            artifact_id=uuid4(),
            intents=[PatchIntent(target_path="README.md", intent="")],
        )
        errors = verify_patch_intent_set(pis)
        assert any("intent" in e for e in errors)

    def test_derived_intents_pass_verification(self):
        # Intents produced by derive_patch_intents must always pass verification.
        for task_type in ("write_readme", "create_plan", "write_architecture"):
            artifact = _make_artifact(task_type=task_type, summary="Some summary")
            pis = derive_patch_intents(artifact, task_type)
            errors = verify_patch_intent_set(pis)
            assert errors == [], f"Errors for {task_type}: {errors}"


# ---------------------------------------------------------------------------
# materialize_patch_intents
# ---------------------------------------------------------------------------


class TestMaterializePatchIntents:
    def test_empty_set_returns_none(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        runtime = LocalWorkspaceRuntime(job_id=uuid4())
        pis = PatchIntentSet(task_id=uuid4(), artifact_id=uuid4())
        result = materialize_patch_intents(pis, runtime, 0, "test")
        assert result is None

    def test_non_empty_set_writes_file(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        runtime = LocalWorkspaceRuntime(job_id=uuid4())
        task_id = uuid4()
        pis = PatchIntentSet(
            task_id=task_id,
            artifact_id=uuid4(),
            intents=[PatchIntent(target_path="README.md", intent="Update readme")],
        )
        mf = materialize_patch_intents(pis, runtime, 2, "write_readme")
        assert mf is not None
        assert mf.path.exists()

    def test_file_path_follows_naming_convention(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        runtime = LocalWorkspaceRuntime(job_id=uuid4())
        task_id = uuid4()
        pis = PatchIntentSet(
            task_id=task_id,
            artifact_id=uuid4(),
            intents=[PatchIntent(target_path="README.md", intent="Update")],
        )
        mf = materialize_patch_intents(pis, runtime, 1, "write_readme")
        assert mf is not None
        name = mf.path.name
        assert name.startswith("001_")
        assert name.endswith(".json")
        assert task_id.hex[:8] in name

    def test_file_is_valid_json(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        runtime = LocalWorkspaceRuntime(job_id=uuid4())
        pis = PatchIntentSet(
            task_id=uuid4(),
            artifact_id=uuid4(),
            intents=[PatchIntent(target_path="README.md", intent="Update")],
        )
        mf = materialize_patch_intents(pis, runtime, 0, "readme")
        assert mf is not None
        data = json.loads(mf.path.read_text())
        assert "intents" in data
        assert data["intents"][0]["target_path"] == "README.md"

    def test_file_lives_in_patch_intents_subdir(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        runtime = LocalWorkspaceRuntime(job_id=uuid4())
        pis = PatchIntentSet(
            task_id=uuid4(),
            artifact_id=uuid4(),
            intents=[PatchIntent(target_path="README.md", intent="Update")],
        )
        mf = materialize_patch_intents(pis, runtime, 0, "readme")
        assert mf is not None
        assert mf.path.parent.name == "patch_intents"


# ---------------------------------------------------------------------------
# artifact metadata integration
# ---------------------------------------------------------------------------


class TestPatchIntentArtifactMetadata:
    def test_metadata_keys_set_when_intents_exist(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        runtime = LocalWorkspaceRuntime(job_id=uuid4())
        artifact = _make_artifact(task_type="write_readme", summary="Update readme content")
        pis = derive_patch_intents(artifact, "write_readme")
        pi_mf = materialize_patch_intents(pis, runtime, 0, "write_readme")
        assert pi_mf is not None
        # Simulate CLI metadata assignment
        artifact.metadata["patch_intent_file"] = str(pi_mf.path)
        artifact.metadata["patch_intent_count"] = len(pis.intents)
        assert "patch_intent_file" in artifact.metadata
        assert artifact.metadata["patch_intent_count"] == 1

    def test_no_metadata_set_when_no_intents(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        runtime = LocalWorkspaceRuntime(job_id=uuid4())
        artifact = _make_artifact(task_type="implement_feature")
        pis = derive_patch_intents(artifact, "implement_feature")
        pi_mf = materialize_patch_intents(pis, runtime, 0, "implement_feature")
        assert pi_mf is None
        assert "patch_intent_file" not in artifact.metadata
        assert "patch_intent_count" not in artifact.metadata


# ---------------------------------------------------------------------------
# Step 10.5: invariant guards (RuntimeError)
# ---------------------------------------------------------------------------


class TestDerivePatchIntentsInvariantGuards:
    def test_raises_runtime_error_on_none_task_id(self):
        artifact = _make_artifact(task_type="write_readme")
        artifact.task_id = None
        with pytest.raises(RuntimeError, match="task_id is None"):
            derive_patch_intents(artifact, "write_readme")

    def test_raises_runtime_error_on_none_artifact_id(self):
        artifact = _make_artifact(task_type="write_readme")
        artifact.id = None  # type: ignore[assignment]
        with pytest.raises(RuntimeError, match="artifact.id is None"):
            derive_patch_intents(artifact, "write_readme")


# ---------------------------------------------------------------------------
# Step 10.5: null-byte path rejection
# ---------------------------------------------------------------------------


class TestVerifyNullBytePath:
    def test_null_byte_in_path_is_rejected(self):
        pis = PatchIntentSet(
            task_id=uuid4(),
            artifact_id=uuid4(),
            intents=[PatchIntent(target_path="README\x00.md", intent="bad")],
        )
        errors = verify_patch_intent_set(pis)
        assert any("null byte" in e for e in errors)

    def test_clean_path_not_flagged_for_null_byte(self):
        pis = PatchIntentSet(
            task_id=uuid4(),
            artifact_id=uuid4(),
            intents=[PatchIntent(target_path="README.md", intent="Update")],
        )
        errors = verify_patch_intent_set(pis)
        assert not any("null byte" in e for e in errors)


# ---------------------------------------------------------------------------
# Step 10: rule sync contract between _INTENT_RULES and _REPO_PATH_RULES
# ---------------------------------------------------------------------------


class TestKeywordSync:
    """Three-layer contract between _INTENT_RULES and _REPO_PATH_RULES.

    Both tables must be kept byte-for-byte identical because they implement the
    same routing policy in two different subsystems (repo application and patch
    intent derivation).  The three tests enforce this at increasing precision:

    1. set equality   — a keyword added to one table but not the other is caught.
    2. order equality — both tables are first-match-wins; a keyword promoted or
                        demoted in one table changes routing semantics silently.
    3. mapping equality — template strings must match; changing a target path in
                          one table without updating the other silently diverges
                          the paths both systems would write.
    """

    def test_intent_rules_and_repo_rules_keyword_sets_match(self):
        """Ensures future additions/removals cannot silently diverge."""
        # These are private module attributes; tests rely on them intentionally
        # to enforce the sync contract between the two rule tables.
        from packages.orchestration.patch_intent import _INTENT_RULES
        from packages.orchestration.repo_applicator import _REPO_PATH_RULES

        intent_keywords = {k for k, _ in _INTENT_RULES}
        repo_keywords = {k for k, _ in _REPO_PATH_RULES}
        assert intent_keywords == repo_keywords, (
            f"keyword sets diverged — "
            f"only in _INTENT_RULES: {intent_keywords - repo_keywords}, "
            f"only in _REPO_PATH_RULES: {repo_keywords - intent_keywords}"
        )

    def test_intent_rules_and_repo_rules_keyword_order_matches(self):
        """Ensures keyword evaluation order is identical between tables.

        Both tables are first-match-wins, so order is part of the contract.
        A keyword promoted or demoted in one table but not the other changes
        routing semantics silently — this test catches that.
        """
        # These are private module attributes; tests rely on them intentionally
        # to enforce the sync contract between the two rule tables.
        from packages.orchestration.patch_intent import _INTENT_RULES
        from packages.orchestration.repo_applicator import _REPO_PATH_RULES

        intent_order = [k for k, _ in _INTENT_RULES]
        repo_order = [k for k, _ in _REPO_PATH_RULES]
        assert intent_order == repo_order, (
            f"keyword order diverged — "
            f"_INTENT_RULES order: {intent_order}, "
            f"_REPO_PATH_RULES order: {repo_order}"
        )

    def test_intent_rules_and_repo_rules_full_mapping_matches(self):
        """Ensures keyword→template mappings are byte-for-byte identical.

        Matching keywords and matching order alone is insufficient: a template
        could be changed in one table (e.g. 'docs/{safe_type}.md' →
        'docs/remedy/{safe_type}.md') without touching the other, causing the
        two systems to silently route the same task type to different paths.
        This test catches such template drift.
        """
        # These are private module attributes; tests rely on them intentionally
        # to enforce the sync contract between the two rule tables.
        from packages.orchestration.patch_intent import _INTENT_RULES
        from packages.orchestration.repo_applicator import _REPO_PATH_RULES

        intent_map = {k: t for k, t in _INTENT_RULES}
        repo_map = {k: t for k, t in _REPO_PATH_RULES}
        assert intent_map == repo_map, (
            f"keyword→template mappings diverged — "
            f"_INTENT_RULES: {intent_map}, "
            f"_REPO_PATH_RULES: {repo_map}"
        )


# ---------------------------------------------------------------------------
# Step 10.5: verification errors surfaced in metadata; no file written
# ---------------------------------------------------------------------------


class TestPatchIntentErrorSurfacing:
    def test_verification_errors_recorded_in_artifact_metadata(self, tmp_path, monkeypatch):
        """When verify returns errors, they are recorded in artifact metadata."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        artifact = _make_artifact(task_type="write_readme", summary="Update readme")
        pis = PatchIntentSet(
            task_id=artifact.task_id,
            artifact_id=artifact.id,
            intents=[PatchIntent(target_path="/etc/passwd", intent="bad")],
        )
        pi_errors = verify_patch_intent_set(pis)
        # Simulate CLI behavior: record errors in metadata when non-empty
        assert pi_errors, "Expected errors from invalid path"
        artifact.metadata["patch_intent_errors"] = pi_errors
        assert "patch_intent_errors" in artifact.metadata
        assert len(artifact.metadata["patch_intent_errors"]) > 0

    def test_invalid_intent_does_not_write_file(self, tmp_path, monkeypatch):
        """When verify returns errors, no patch intent file is written."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        runtime = LocalWorkspaceRuntime(job_id=uuid4())
        pis = PatchIntentSet(
            task_id=uuid4(),
            artifact_id=uuid4(),
            intents=[PatchIntent(target_path="/etc/passwd", intent="bad")],
        )
        pi_errors = verify_patch_intent_set(pis)
        assert pi_errors, "Expected errors from invalid path"
        # Simulate the CLI conditional: errors → skip materialize.
        # If we follow the CLI logic (only materialize when not pi_errors), result is None.
        mf = materialize_patch_intents(pis, runtime, 0, "bad") if not pi_errors else None
        assert mf is None  # no file written because errors are present

    def test_valid_intent_does_not_set_errors_key(self, tmp_path, monkeypatch):
        """When verify passes, patch_intent_errors must not be set in metadata."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        runtime = LocalWorkspaceRuntime(job_id=uuid4())
        artifact = _make_artifact(task_type="write_readme", summary="Update readme")
        pis = derive_patch_intents(artifact, "write_readme")
        pi_errors = verify_patch_intent_set(pis)
        assert pi_errors == []
        # Simulate CLI: only record errors if pi_errors is non-empty
        if pi_errors:
            artifact.metadata["patch_intent_errors"] = pi_errors
        else:
            pi_mf = materialize_patch_intents(pis, runtime, 0, "write_readme")
            if pi_mf is not None:
                artifact.metadata["patch_intent_file"] = str(pi_mf.path)
                artifact.metadata["patch_intent_count"] = len(pis.intents)
        assert "patch_intent_errors" not in artifact.metadata
        assert "patch_intent_file" in artifact.metadata


# ---------------------------------------------------------------------------
# Step 11: dry-run preview and explanation layer
# ---------------------------------------------------------------------------

_SAMPLE_CONTENT = (
    "Summary:\n"
    "  Updates the README with installation steps.\n"
    "\n"
    "Proposed Changes:\n"
    "  - Add installation section\n"
    "  - Add usage examples\n"
    "  - Link to changelog\n"
    "\n"
    "Notes:\n"
    "  - Backward compatible\n"
)


class TestExtractProposedLines:
    """_extract_proposed_lines correctly isolates the Proposed Changes section."""

    def test_extracts_known_lines(self):
        lines = _extract_proposed_lines(_SAMPLE_CONTENT)
        assert lines == [
            "Add installation section",
            "Add usage examples",
            "Link to changelog",
        ]

    def test_excludes_notes_section(self):
        lines = _extract_proposed_lines(_SAMPLE_CONTENT)
        assert not any("Backward compatible" in ln for ln in lines)

    def test_excludes_summary_section(self):
        lines = _extract_proposed_lines(_SAMPLE_CONTENT)
        assert not any("Updates the README" in ln for ln in lines)

    def test_empty_content_returns_empty(self):
        assert _extract_proposed_lines("") == []

    def test_no_proposed_changes_section_returns_empty(self):
        content = "Summary:\n  something\nNotes:\n  nothing\n"
        assert _extract_proposed_lines(content) == []


class TestGenerateDryRunPreview:
    """generate_dry_run_preview covers all three action paths and the empty-set path."""

    def _make_pis(self, task_type: str = "write_readme") -> PatchIntentSet:
        artifact = _make_artifact(task_type=task_type, summary="Some change")
        return derive_patch_intents(artifact, task_type)

    def test_empty_intents_returns_empty_list(self):
        pis = PatchIntentSet(task_id=uuid4(), artifact_id=uuid4(), intents=[])
        results = generate_dry_run_preview(pis, _SAMPLE_CONTENT, "unknown")
        assert results == []

    def test_no_repo_root_gives_preview_only(self):
        pis = self._make_pis("write_readme")
        results = generate_dry_run_preview(pis, _SAMPLE_CONTENT, "write_readme", repo_root=None)
        assert len(results) == 1
        r = results[0]
        assert r.action == "preview-only"
        assert r.target_path == "README.md"
        assert "no repository attached" in r.diff_preview
        assert "README.md" in r.diff_preview

    def test_existing_file_gives_modify(self, tmp_path):
        readme = tmp_path / "README.md"
        readme.write_text("# Project\nExisting content.\n")
        pis = self._make_pis("write_readme")
        results = generate_dry_run_preview(pis, _SAMPLE_CONTENT, "write_readme", tmp_path)
        assert len(results) == 1
        r = results[0]
        assert r.action == "modify"
        assert "README.md" in r.diff_preview
        assert "existing file" in r.diff_preview
        assert "proposed additions" in r.diff_preview

    def test_missing_file_gives_create(self, tmp_path):
        pis = self._make_pis("write_readme")
        results = generate_dry_run_preview(pis, _SAMPLE_CONTENT, "write_readme", tmp_path)
        assert len(results) == 1
        r = results[0]
        assert r.action == "create"
        assert "new file" in r.diff_preview

    def test_proposed_lines_appear_in_preview(self, tmp_path):
        pis = self._make_pis("write_readme")
        results = generate_dry_run_preview(pis, _SAMPLE_CONTENT, "write_readme", tmp_path)
        assert "Add installation section" in results[0].diff_preview

    def test_reason_includes_task_type(self):
        pis = self._make_pis("write_readme")
        results = generate_dry_run_preview(pis, _SAMPLE_CONTENT, "write_readme")
        assert "write_readme" in results[0].reason

    def test_summary_is_truncated_to_120_chars(self):
        long_summary = "x" * 200
        artifact = _make_artifact(task_type="write_readme", summary=long_summary)
        artifact.metadata["summary"] = long_summary
        pis = derive_patch_intents(artifact, "write_readme")
        results = generate_dry_run_preview(pis, _SAMPLE_CONTENT, "write_readme")
        assert len(results[0].summary) <= 120

    def test_returns_patch_dry_run_result_instances(self):
        pis = self._make_pis("write_readme")
        results = generate_dry_run_preview(pis, _SAMPLE_CONTENT, "write_readme")
        assert all(isinstance(r, PatchDryRunResult) for r in results)

    def test_existing_file_context_lines_appear(self, tmp_path):
        readme = tmp_path / "README.md"
        readme.write_text("# Header\nLine two\nLine three\nLine four\nLine five\n")
        pis = self._make_pis("write_readme")
        results = generate_dry_run_preview(pis, _SAMPLE_CONTENT, "write_readme", tmp_path)
        preview = results[0].diff_preview
        assert "# Header" in preview  # first context line appears


class TestFormatDryRunExplanations:
    """format_dry_run_explanations produces a correctly structured text block."""

    def _make_result(self, **kwargs) -> PatchDryRunResult:
        defaults = dict(
            target_path="README.md",
            action="modify",
            reason="task type 'write_readme'",
            summary="adds installation and usage sections",
            diff_preview="",
        )
        defaults.update(kwargs)
        return PatchDryRunResult(**defaults)

    def test_empty_results_returns_empty_string(self):
        assert format_dry_run_explanations([]) == ""

    def test_single_result_contains_all_fields(self):
        r = self._make_result()
        text = format_dry_run_explanations([r])
        assert "Planned change:" in text
        assert "README.md" in text
        assert "modify" in text
        assert "write_readme" in text
        assert "adds installation" in text

    def test_multiple_results_all_appear(self):
        r1 = self._make_result(target_path="README.md")
        r2 = self._make_result(target_path="docs/guide.md", action="create")
        text = format_dry_run_explanations([r1, r2])
        assert "README.md" in text
        assert "docs/guide.md" in text
        assert "create" in text
