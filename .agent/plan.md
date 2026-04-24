# Plan

## Goal
Step 8: Controlled Repo Attachment and Safe Generated File Application.

## Status
COMPLETE

## What Was Done
1. [x] Branch: feature/step8-repo-attachment (from feature/step6-workspace-runtime — PR chain)
2. [x] Carry-in: finalize_task raises RuntimeError on missing artifact_id or not-found artifact
3. [x] Create packages/orchestration/repo_applicator.py
4. [x] Update CLI: attach-repo command + run-next-task-local repo application
5. [x] Tests: test_repo_applicator.py + 2 carry-in tests; 239 total passing
6. [x] Docs: README.md + docs/architecture.md
7. [x] Update context.md + decisions.md
8. [x] Run tests, commit, push

## Key Decisions
- Branch from feature/step6-workspace-runtime (not main) — Step 8 needs workspace/verifier
  changes that are not yet merged to main. Documents as PR chain.
- repo_applicator.py: new module; keyword mapping only; no overwriting; boundary-safe writes
- apply_task_output_to_repo: ineligible → []; file exists → []; boundary violation → RuntimeError
- Repo application runs only on vr.passed and job.metadata["target_repo"] set
- Failed-artifact diagnostics carry-in: both empty-list and not-found cases now raise

## Branch
feature/step8-repo-attachment — new branch (clearly unrelated to workspace runtime)
