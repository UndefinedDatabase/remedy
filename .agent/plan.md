# Plan

## Goal
Step 19: Approval Queue v1 — metadata-only approval decisions for patch intents.

## Prior step
Step 18 (+ 18.1) delivered Cockpit v1 and conservative auto-continue safety fix.

## Status
COMPLETE — 826 tests pass. Ready to commit and open PR.

## Steps
1. [x] Create packages/orchestration/approval_queue.py
2. [x] Add 4 CLI commands to apps/cli/main.py (list/show/approve/reject-patch-intent)
3. [x] Update cockpit.py — approval-aware attention + next action
4. [x] Create tests/test_patch_intent_approval.py (57 tests)
5. [x] Run full suite (826 pass)
6. [x] Update docs/architecture.md — Approval Queue v1 section
7. [x] Update .agent files
8. [ ] Commit all Step 19 changes
9. [ ] Push to feature/step19-approval-queue-v1
10. [ ] Create PR for Step 19

## Branch
feature/step19-approval-queue-v1
