# Plan

## Goal
Step 14: Artifact Kinds v1

## Status
COMPLETE — 503 tests pass

## Steps
1. [x] Add ArtifactKind enum (7 values) to packages/core/models.py
2. [x] Add kind: ArtifactKind = ArtifactKind.UNKNOWN field to Artifact
3. [x] Set kind=PLANNING at planning artifact creation sites (job_runner, llm_planner)
4. [x] Set kind=BUILDER_PROPOSAL at builder artifact creation site (task_runner)
5. [x] Create packages/orchestration/artifact_index.py (4 helpers)
6. [x] Add tests/test_artifact_kinds.py (47 tests)
7. [x] Update docs/architecture.md (ArtifactKind section)
8. [ ] Update .agent files and commit

## Branch
feature/step14-artifact-kinds
