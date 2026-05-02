"""
Tests for ArtifactKind (packages/core/models.py) and
artifact_index helpers (packages/orchestration/artifact_index.py).

Covers:
  - ArtifactKind: enum values, str identity, all expected members present
  - Artifact.kind: field exists, default is UNKNOWN, persists through JSON roundtrip
  - Backward-compat: old JSON without 'kind' deserializes to UNKNOWN
  - Creation sites: planning artifacts get PLANNING, builder artifacts get BUILDER_PROPOSAL
  - artifacts_by_kind: returns matching artifacts in order, empty for absent kind
  - first_artifact_by_kind: returns first match, None for absent kind
  - task_artifacts_by_kind: filters by both task_id and kind
  - planning_artifact: prefers explicit PLANNING kind, falls back to legacy convention,
    returns None when no planning artifact present

All tests are deterministic — no I/O, no live services.
"""

from __future__ import annotations

import json
from uuid import UUID, uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job
from packages.orchestration.artifact_index import (
    artifacts_by_kind,
    first_artifact_by_kind,
    planning_artifact,
    task_artifacts_by_kind,
)
from packages.orchestration.job_runner import plan_job
from packages.orchestration.llm_planner import annotate_planning_result, plan_job_with_llm
from packages.orchestration.planner_models import PlannerOutput, ProposedTask


# ---------------------------------------------------------------------------
# ArtifactKind: enum structure
# ---------------------------------------------------------------------------


class TestArtifactKindEnum:
    def test_is_str_enum(self):
        assert isinstance(ArtifactKind.UNKNOWN, str)

    def test_all_expected_members_present(self):
        expected = {
            "UNKNOWN",
            "PLANNING",
            "BUILDER_PROPOSAL",
            "WORKSPACE_MATERIALIZATION",
            "VERIFICATION",
            "PATCH_INTENT",
            "REPO_APPLICATION",
        }
        assert {m.name for m in ArtifactKind} == expected

    def test_values_are_snake_case_strings(self):
        for member in ArtifactKind:
            assert member.value == member.value.lower()
            assert " " not in member.value

    def test_unknown_value(self):
        assert ArtifactKind.UNKNOWN.value == "unknown"

    def test_planning_value(self):
        assert ArtifactKind.PLANNING.value == "planning"

    def test_builder_proposal_value(self):
        assert ArtifactKind.BUILDER_PROPOSAL.value == "builder_proposal"

    def test_workspace_materialization_value(self):
        assert ArtifactKind.WORKSPACE_MATERIALIZATION.value == "workspace_materialization"

    def test_verification_value(self):
        assert ArtifactKind.VERIFICATION.value == "verification"

    def test_patch_intent_value(self):
        assert ArtifactKind.PATCH_INTENT.value == "patch_intent"

    def test_repo_application_value(self):
        assert ArtifactKind.REPO_APPLICATION.value == "repo_application"

    def test_str_identity(self):
        """ArtifactKind.PLANNING == 'planning' because it's a str enum."""
        assert ArtifactKind.PLANNING == "planning"

    def test_roundtrip_from_value(self):
        for member in ArtifactKind:
            assert ArtifactKind(member.value) is member


# ---------------------------------------------------------------------------
# Artifact.kind field
# ---------------------------------------------------------------------------


class TestArtifactKindField:
    def test_default_is_unknown(self):
        artifact = Artifact(name="x", content="y")
        assert artifact.kind == ArtifactKind.UNKNOWN

    def test_explicit_planning_kind(self):
        artifact = Artifact(name="x", content="y", kind=ArtifactKind.PLANNING)
        assert artifact.kind == ArtifactKind.PLANNING

    def test_explicit_builder_proposal_kind(self):
        artifact = Artifact(name="x", content="y", kind=ArtifactKind.BUILDER_PROPOSAL)
        assert artifact.kind == ArtifactKind.BUILDER_PROPOSAL

    def test_kind_field_present_in_model_fields(self):
        assert "kind" in Artifact.model_fields

    def test_json_roundtrip_preserves_kind(self):
        artifact = Artifact(name="x", content="y", kind=ArtifactKind.PLANNING)
        dumped = artifact.model_dump_json()
        loaded = Artifact.model_validate_json(dumped)
        assert loaded.kind == ArtifactKind.PLANNING

    def test_json_roundtrip_unknown(self):
        artifact = Artifact(name="x", content="y")
        dumped = artifact.model_dump_json()
        loaded = Artifact.model_validate_json(dumped)
        assert loaded.kind == ArtifactKind.UNKNOWN

    def test_backward_compat_old_json_no_kind_field(self):
        """Old JSON without 'kind' deserializes to UNKNOWN (Pydantic default)."""
        old_json = json.dumps({
            "id": str(uuid4()),
            "name": "planning_output",
            "content": "old content",
            "mime_type": "text/plain",
            "task_id": None,
            "metadata": {},
        })
        artifact = Artifact.model_validate_json(old_json)
        assert artifact.kind == ArtifactKind.UNKNOWN

    def test_json_with_kind_string_value_parses(self):
        """JSON with a string 'kind' value (e.g. 'planning') is accepted."""
        data = json.dumps({
            "id": str(uuid4()),
            "name": "x",
            "content": "y",
            "mime_type": "text/plain",
            "task_id": None,
            "kind": "planning",
            "metadata": {},
        })
        artifact = Artifact.model_validate_json(data)
        assert artifact.kind == ArtifactKind.PLANNING


# ---------------------------------------------------------------------------
# Creation sites: planning artifacts
# ---------------------------------------------------------------------------


class TestPlanningArtifactKind:
    def test_deterministic_planner_sets_planning_kind(self):
        job = Job(name="test", user_prompt="do stuff")
        result = plan_job(job)
        assert result.changed is True
        planning = next(
            (a for a in result.job.artifacts if a.name == "planning_output"),
            None,
        )
        assert planning is not None
        assert planning.kind == ArtifactKind.PLANNING

    def test_llm_planner_sets_planning_kind(self):
        job = Job(name="test", user_prompt="do stuff")

        def fake_planner(prompt: str) -> PlannerOutput:
            return PlannerOutput(
                summary="test plan",
                proposed_tasks=[
                    ProposedTask(task_type="write_readme", description="Write README"),
                ],
            )

        result = plan_job_with_llm(job, fake_planner)
        assert result.changed is True
        planning = next(
            (a for a in result.job.artifacts if a.name == "planning_output"),
            None,
        )
        assert planning is not None
        assert planning.kind == ArtifactKind.PLANNING


# ---------------------------------------------------------------------------
# Creation sites: builder artifacts
# ---------------------------------------------------------------------------


class TestBuilderArtifactKind:
    def test_run_next_task_sets_builder_proposal_kind(self):
        from packages.orchestration.builder_models import BuilderOutput
        from packages.orchestration.task_runner import run_next_task

        job = Job(name="test", user_prompt="do stuff")
        plan_job(job)

        def fake_builder(ctx):
            return BuilderOutput(
                summary="done",
                proposed_changes=["change one"],
            )

        result = run_next_task(job, fake_builder)
        assert result.changed is True
        task_artifact = next(
            (a for a in result.job.artifacts if a.task_id == result.task_id),
            None,
        )
        assert task_artifact is not None
        assert task_artifact.kind == ArtifactKind.BUILDER_PROPOSAL


# ---------------------------------------------------------------------------
# artifacts_by_kind
# ---------------------------------------------------------------------------


def _make_artifact(
    kind: ArtifactKind,
    task_id: UUID | None = None,
    name: str = "x",
) -> Artifact:
    return Artifact(name=name, content="c", kind=kind, task_id=task_id)


class TestArtifactsByKind:
    def test_returns_matching_artifacts(self):
        arts = [
            _make_artifact(ArtifactKind.PLANNING),
            _make_artifact(ArtifactKind.BUILDER_PROPOSAL),
            _make_artifact(ArtifactKind.PLANNING),
        ]
        result = artifacts_by_kind(arts, ArtifactKind.PLANNING)
        assert len(result) == 2
        assert all(a.kind == ArtifactKind.PLANNING for a in result)

    def test_returns_empty_for_absent_kind(self):
        arts = [_make_artifact(ArtifactKind.PLANNING)]
        assert artifacts_by_kind(arts, ArtifactKind.VERIFICATION) == []

    def test_returns_empty_for_empty_sequence(self):
        assert artifacts_by_kind([], ArtifactKind.PLANNING) == []

    def test_preserves_original_order(self):
        arts = [_make_artifact(ArtifactKind.BUILDER_PROPOSAL) for _ in range(3)]
        result = artifacts_by_kind(arts, ArtifactKind.BUILDER_PROPOSAL)
        assert result == arts

    def test_returns_list(self):
        arts = [_make_artifact(ArtifactKind.PLANNING)]
        result = artifacts_by_kind(arts, ArtifactKind.PLANNING)
        assert isinstance(result, list)

    def test_does_not_mutate_input(self):
        arts = [_make_artifact(ArtifactKind.PLANNING)]
        original_len = len(arts)
        artifacts_by_kind(arts, ArtifactKind.PLANNING)
        assert len(arts) == original_len


# ---------------------------------------------------------------------------
# first_artifact_by_kind
# ---------------------------------------------------------------------------


class TestFirstArtifactByKind:
    def test_returns_first_match(self):
        first = _make_artifact(ArtifactKind.PLANNING, name="first")
        second = _make_artifact(ArtifactKind.PLANNING, name="second")
        arts = [first, second]
        assert first_artifact_by_kind(arts, ArtifactKind.PLANNING) is first

    def test_returns_none_for_absent_kind(self):
        arts = [_make_artifact(ArtifactKind.PLANNING)]
        assert first_artifact_by_kind(arts, ArtifactKind.VERIFICATION) is None

    def test_returns_none_for_empty_sequence(self):
        assert first_artifact_by_kind([], ArtifactKind.PLANNING) is None

    def test_returns_single_match(self):
        a = _make_artifact(ArtifactKind.BUILDER_PROPOSAL)
        assert first_artifact_by_kind([a], ArtifactKind.BUILDER_PROPOSAL) is a


# ---------------------------------------------------------------------------
# task_artifacts_by_kind
# ---------------------------------------------------------------------------


class TestTaskArtifactsByKind:
    def test_returns_matching_task_and_kind(self):
        tid = uuid4()
        a = _make_artifact(ArtifactKind.BUILDER_PROPOSAL, task_id=tid)
        b = _make_artifact(ArtifactKind.BUILDER_PROPOSAL, task_id=uuid4())
        result = task_artifacts_by_kind([a, b], tid, ArtifactKind.BUILDER_PROPOSAL)
        assert result == [a]

    def test_returns_empty_when_task_id_absent(self):
        tid = uuid4()
        a = _make_artifact(ArtifactKind.BUILDER_PROPOSAL, task_id=uuid4())
        assert task_artifacts_by_kind([a], tid, ArtifactKind.BUILDER_PROPOSAL) == []

    def test_returns_empty_when_kind_absent(self):
        tid = uuid4()
        a = _make_artifact(ArtifactKind.PLANNING, task_id=tid)
        assert task_artifacts_by_kind([a], tid, ArtifactKind.BUILDER_PROPOSAL) == []

    def test_returns_multiple_matching(self):
        tid = uuid4()
        a = _make_artifact(ArtifactKind.BUILDER_PROPOSAL, task_id=tid)
        b = _make_artifact(ArtifactKind.BUILDER_PROPOSAL, task_id=tid)
        result = task_artifacts_by_kind([a, b], tid, ArtifactKind.BUILDER_PROPOSAL)
        assert result == [a, b]

    def test_returns_empty_for_empty_sequence(self):
        assert task_artifacts_by_kind([], uuid4(), ArtifactKind.PLANNING) == []


# ---------------------------------------------------------------------------
# planning_artifact
# ---------------------------------------------------------------------------


class TestPlanningArtifact:
    def test_finds_explicit_planning_kind(self):
        a = _make_artifact(ArtifactKind.PLANNING)
        result = planning_artifact([a])
        assert result is a

    def test_prefers_explicit_planning_over_legacy(self):
        """Explicit kind=PLANNING must be preferred over legacy name convention."""
        legacy = Artifact(
            name="planning_output",
            content="old",
            task_id=None,
            kind=ArtifactKind.UNKNOWN,
        )
        explicit = _make_artifact(ArtifactKind.PLANNING, name="planning_output")
        # explicit comes second in the list — but kind match wins
        result = planning_artifact([legacy, explicit])
        assert result is explicit

    def test_falls_back_to_legacy_convention(self):
        """Legacy artifact: name='planning_output', task_id=None, kind=UNKNOWN."""
        legacy = Artifact(
            name="planning_output",
            content="old",
            task_id=None,
            kind=ArtifactKind.UNKNOWN,
        )
        result = planning_artifact([legacy])
        assert result is legacy

    def test_legacy_fallback_requires_task_id_none(self):
        """Legacy fallback must not match artifacts with a non-None task_id."""
        tid = uuid4()
        a = Artifact(
            name="planning_output",
            content="x",
            task_id=tid,
            kind=ArtifactKind.UNKNOWN,
        )
        assert planning_artifact([a]) is None

    def test_returns_none_when_no_planning_artifact(self):
        arts = [
            _make_artifact(ArtifactKind.BUILDER_PROPOSAL),
            _make_artifact(ArtifactKind.UNKNOWN),
        ]
        assert planning_artifact(arts) is None

    def test_legacy_fallback_rejects_wrong_kind(self):
        """Legacy fallback must not match name='planning_output', task_id=None with a
        non-UNKNOWN, non-PLANNING kind.  Only UNKNOWN triggers the fallback path."""
        for bad_kind in (
            ArtifactKind.BUILDER_PROPOSAL,
            ArtifactKind.VERIFICATION,
            ArtifactKind.PATCH_INTENT,
            ArtifactKind.REPO_APPLICATION,
            ArtifactKind.WORKSPACE_MATERIALIZATION,
        ):
            a = Artifact(
                name="planning_output",
                content="x",
                task_id=None,
                kind=bad_kind,
            )
            assert planning_artifact([a]) is None, (
                f"planning_artifact should return None for kind={bad_kind!r} "
                "but legacy fallback incorrectly matched it"
            )

    def test_returns_none_for_empty_sequence(self):
        assert planning_artifact([]) is None

    def test_returns_first_planning_artifact(self):
        first = _make_artifact(ArtifactKind.PLANNING, name="first")
        second = _make_artifact(ArtifactKind.PLANNING, name="second")
        result = planning_artifact([first, second])
        assert result is first

    def test_deterministic_planner_artifact_found(self):
        """End-to-end: deterministic planner output is found by planning_artifact."""
        job = Job(name="test", user_prompt="prompt")
        result = plan_job(job)
        found = planning_artifact(result.job.artifacts)
        assert found is not None
        assert found.kind == ArtifactKind.PLANNING

    def test_llm_planner_artifact_found(self):
        """End-to-end: LLM planner output is found by planning_artifact."""
        job = Job(name="test", user_prompt="prompt")

        def fake_planner(prompt: str) -> PlannerOutput:
            return PlannerOutput(
                summary="s",
                proposed_tasks=[ProposedTask(task_type="t", description="d")],
            )

        result = plan_job_with_llm(job, fake_planner)
        found = planning_artifact(result.job.artifacts)
        assert found is not None
        assert found.kind == ArtifactKind.PLANNING


# ---------------------------------------------------------------------------
# annotate_planning_result
# ---------------------------------------------------------------------------


def _fake_planner(prompt: str) -> PlannerOutput:
    return PlannerOutput(
        summary="s",
        proposed_tasks=[ProposedTask(task_type="write_readme", description="d")],
    )


_ANNOTATE_KWARGS = dict(
    provider="test-provider",
    role="planner",
    model="test-model",
    elapsed_ms=123.4,
)


class TestAnnotatePlanningResult:
    def test_annotates_explicit_planning_kind(self):
        """annotate_planning_result enriches the PLANNING artifact via planning_artifact()."""
        job = Job(name="j", user_prompt="p")
        result = plan_job_with_llm(job, _fake_planner)
        annotate_planning_result(result, **_ANNOTATE_KWARGS)
        artifact = planning_artifact(result.job.artifacts)
        assert artifact is not None
        assert artifact.metadata["provider"] == "test-provider"
        assert artifact.metadata["model"] == "test-model"
        assert artifact.metadata["role"] == "planner"
        assert artifact.metadata["task_count"] == 1
        assert artifact.metadata["elapsed_ms"] == 123

    def test_annotates_legacy_artifact(self):
        """annotate_planning_result falls back to legacy name+task_id convention."""
        job = Job(name="j", user_prompt="p")
        result = plan_job_with_llm(job, _fake_planner)
        # Locate the planning artifact by kind (not by position) and downgrade it
        # to simulate a pre-Step-14 (legacy) artifact.
        pa = first_artifact_by_kind(result.job.artifacts, ArtifactKind.PLANNING)
        assert pa is not None, "test setup: planner must produce a PLANNING artifact"
        pa.kind = ArtifactKind.UNKNOWN
        annotate_planning_result(result, **_ANNOTATE_KWARGS)
        # The legacy fallback (name="planning_output", task_id=None, kind=UNKNOWN)
        # must still be found by planning_artifact().
        found = planning_artifact(result.job.artifacts)
        assert found is not None
        assert found.metadata["provider"] == "test-provider"

    def test_noop_when_changed_false(self):
        """No metadata is written when result.changed is False."""
        job = Job(name="j", user_prompt="p")
        plan_job_with_llm(job, _fake_planner)
        # Planning already done; second call returns changed=False.
        result2 = plan_job_with_llm(job, _fake_planner)
        assert result2.changed is False
        annotate_planning_result(result2, **_ANNOTATE_KWARGS)
        # Artifacts belong to the already-planned job — none should get the annotation.
        for a in result2.job.artifacts:
            assert "provider" not in a.metadata

    def test_noop_when_no_planning_artifact(self):
        """annotate_planning_result is safe when no planning artifact exists."""
        job = Job(name="j", user_prompt="p")
        result = plan_job_with_llm(job, _fake_planner)
        result.job.artifacts.clear()
        # Must not raise.
        annotate_planning_result(result, **_ANNOTATE_KWARGS)
