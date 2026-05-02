# Context

## Active Branch
`feature/step14-artifact-kinds`

## PR
(none yet)

## Scope
Step 14 + 14.1: Artifact Kinds v1 + Polish.
- New: ArtifactKind str Enum in packages/core/models.py (7 values: UNKNOWN, PLANNING, BUILDER_PROPOSAL, WORKSPACE_MATERIALIZATION, VERIFICATION, PATCH_INTENT, REPO_APPLICATION)
- Updated: Artifact model gains kind: ArtifactKind = ArtifactKind.UNKNOWN (backward-compat default)
- Updated: job_runner.py → sets kind=PLANNING on planning artifact
- Updated: llm_planner.py → sets kind=PLANNING on planning artifact; annotate_planning_result now uses planning_artifact() helper
- Updated: task_runner.py → sets kind=BUILDER_PROPOSAL on task artifact
- New: packages/orchestration/artifact_index.py (artifacts_by_kind, first_artifact_by_kind, task_artifacts_by_kind, planning_artifact)
- New: tests/test_artifact_kinds.py (51 tests, incl. 4 annotate_planning_result tests)
- Updated: docs/architecture.md (Artifact Kinds v1 section + active vs reserved note)
507 tests pass.

## Key decisions
- kind defaults to UNKNOWN for backward-compat with pre-Step-14 JSON
- planning_artifact() prefers explicit kind=PLANNING, falls back to legacy name+task_id convention
- annotate_planning_result uses planning_artifact() — no inline lookup
- v1 active kinds: PLANNING, BUILDER_PROPOSAL; reserved for future: WORKSPACE_MATERIALIZATION, VERIFICATION, PATCH_INTENT, REPO_APPLICATION
- is_known_task_type v1 invariant: is_known_task_type ≡ repo_route is not None (still holds)
