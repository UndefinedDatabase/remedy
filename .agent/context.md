# Context

## Active Branch
`feature/step10-patch-intent`

## PR
None yet.

## Scope
Step 10: Patch Intent v1. Structured existing-file change proposals, never applied.
Clearly unrelated to Step 9 permission model — new branch is correct.

## Constraints
- NO patch application, NO repo writes beyond existing doc generation
- NO shell, NO Git, NO Docker, NO source editing
- repo_overwrite stays reserved
- Patch intents are workspace-only artifacts (JSON files in .data/workspaces/)
- target_path must be relative, no traversal, .md only (doc-like paths)
- Derivation is conservative: task_type keyword match only
- PatchIntentSet can be empty (no intents = valid, no file written)

## Assumptions
- patch_intent.py lives in packages/orchestration/ (same layer as repo_applicator)
- Derivation uses same keyword table as repo_applicator (doc targets only)
- Patch intent materialization reuses existing LocalWorkspaceRuntime
- Verification is a pure function returning a list of error strings
- Patch intents derived only when vr.passed (completed tasks only)
