# Plan

## Goal
Step 10: Patch Intent v1 — structured existing-file change proposals, no apply yet.

## Status
READY TO COMMIT

## Steps
1. [x] Open PR Gate: PR #9 merged, on main, new branch feature/step10-patch-intent
2. [x] Update .agent/plan.md, context.md, decisions.md
3. [x] Create packages/orchestration/patch_intent.py:
       PatchIntent + PatchIntentSet models, derive_patch_intents,
       verify_patch_intent_set, materialize_patch_intents
4. [x] Update apps/cli/main.py:
       - fix no-pending-tasks (early PENDING check before workspace_write guard)
       - remove dead mf-is-None branch
       - integrate patch intent derivation, verification, materialization, output
5. [x] Create tests/test_patch_intent.py (35 tests) + no-pending-tasks tests in test_cli_main.py (3)
6. [x] Update README.md and docs/architecture.md
7. [ ] Self-review, commit, push, create PR

## Branch
feature/step10-patch-intent

## PR
None yet — create when ready
