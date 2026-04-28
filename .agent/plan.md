# Plan

## Goal
Step 10.6: Patch Intent Rule Ordering and CLI Coverage Hotfix.

## Status
COMPLETE — committed, pushing

## Steps
1. [x] Reconstruct context from repo (session resume)
2. [x] Fix derive_patch_intents docstring: ValueError → RuntimeError
3. [x] Add rule-ordering test to TestKeywordSync (ordered-list comparison)
4. [x] Add CLI-level patch intent error test (TestPatchIntentErrorsCLI, mocked internals)
5. [x] Update .agent/decisions.md
6. [x] 61 tests pass — commit, push

## Branch
feature/step10-patch-intent

## PR
#10 (open) — update after push
