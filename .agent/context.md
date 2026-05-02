# Context

## Active Branch
`feature/step14-artifact-kinds`

## PR
(none yet)

## Scope
Step 14 + 14.1–14.3 + Step 15: Artifact Kinds v1 + Polish + Verifier Profiles v1.
- New: ArtifactKind str Enum in packages/core/models.py (7 values: UNKNOWN, PLANNING, BUILDER_PROPOSAL, WORKSPACE_MATERIALIZATION, VERIFICATION, PATCH_INTENT, REPO_APPLICATION)
- Updated: Artifact model gains kind: ArtifactKind = ArtifactKind.UNKNOWN (backward-compat default)
- Updated: job_runner.py → sets kind=PLANNING on planning artifact
- Updated: llm_planner.py → sets kind=PLANNING on planning artifact; annotate_planning_result uses planning_artifact()
- Updated: task_runner.py → sets kind=BUILDER_PROPOSAL on task artifact; _build_execution_context uses planning_artifact() (public name, no alias)
- New: packages/orchestration/artifact_index.py (artifacts_by_kind, first_artifact_by_kind, task_artifacts_by_kind, planning_artifact)
- New: tests/test_artifact_kinds.py (53 tests)
- New: 2 additional tests in test_task_runner.py for explicit-kind and legacy context lookup
- Updated: docs/architecture.md (Artifact Kinds v1 section + active vs reserved note)
568 tests pass.

## Step 15 additions
- New: packages/orchestration/verifier_profiles.py (VerifierProfile dataclass, 4 profiles: generic/repo_doc/analysis_doc/implementation_plan)
- Updated: task_registry.py → _ROUTE_RULES is now a 4-tuple (keyword, description, route, profile)
- Updated: verifier.py → profile-driven checks after workspace checks: required_section, min_proposed_changes, forbidden_phrase
- New: tests/test_verifier_profiles.py (unit tests)
- Updated: test_task_registry.py (profile mapping tests)
- Updated: test_verifier.py (profile integration tests)
- Updated: docs/architecture.md (Verifier Profiles v1 section)

## Key decisions
- kind defaults to UNKNOWN for backward-compat with pre-Step-14 JSON
- planning_artifact() prefers explicit kind=PLANNING, falls back to legacy (name="planning_output", task_id=None, kind=UNKNOWN only)
- Legacy fallback requires kind==UNKNOWN — wrongly-kinded artifacts named "planning_output" are not matched
- All three planning artifact lookup sites use planning_artifact(): annotate_planning_result, _build_execution_context
- v1 active kinds: PLANNING, BUILDER_PROPOSAL; reserved for future: WORKSPACE_MATERIALIZATION, VERIFICATION, PATCH_INTENT, REPO_APPLICATION
- is_known_task_type v1 invariant: is_known_task_type ≡ repo_route is not None (still holds)
- Verifier profile fallback: unknown name or None → generic (permissive, no forbidden phrases, min 1 change)
