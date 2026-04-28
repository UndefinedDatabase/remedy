# Plan

## Goal
Step 10.5: Patch Intent Reliability Hotfix — observability, rule consistency, invariant guards.

## Status
COMPLETE — ready to push and update PR #10

## Steps
1. [x] Reconstruct context from repo (session resume)
2. [x] Strengthen patch_intent.py:
       - derive_patch_intents: RuntimeError (not ValueError) for missing task_id/artifact.id
       - verify_patch_intent_set: reject null bytes in target_path
3. [x] Surface verification errors in CLI (main.py):
       - print warning to stderr when pi_errors non-empty
       - record patch_intent_errors in artifact metadata
       - don't write file when errors exist
4. [x] Add new tests (8 new tests, 39 total in test_patch_intent.py):
       - null-byte path rejected
       - missing artifact.id raises RuntimeError
       - missing task_id raises RuntimeError (updated from ValueError)
       - keyword sync (_INTENT_RULES vs _REPO_PATH_RULES)
       - verification errors recorded in metadata
       - invalid intent does not write file
       - valid intent does not set errors key
5. [x] Update docs/architecture.md (verify checks, metadata table, invariant guards)
6. [x] Update .agent/decisions.md and context.md
7. [x] All 59 tests pass — commit, push, update PR

## Branch
feature/step10-patch-intent

## PR
#10 (open) — update after push
