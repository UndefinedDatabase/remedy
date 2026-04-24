# Plan

## Goal
Step 7: Task Contract v1 and Verifier Gate.

## Status
COMPLETE. All changes on feature/step6-workspace-runtime (PR #7).

## What Was Done
1. verifier.py (new): TaskContract, VerificationCheckResult, VerificationResult, verify_task_output (7 deterministic checks)
2. task_runner.py: run_next_task no longer marks COMPLETED; new finalize_task() applies VerificationResult
3. CLI: run-next-task-local flow: build → annotate → materialize → verify → finalize → save_job
4. test_task_runner.py: 4 state-transition tests updated; 8 finalize_task tests added (36 total)
5. test_verifier.py (new): 13 focused tests — happy path, each failing check, full-flow integration
6. README.md + docs/architecture.md: Task Contract v1, verifier gate, state table, ordering

## Key Decisions
- task stays RUNNING after run_next_task; COMPLETED only after verify_task_output passes
- verify_task_output is pure (no mutation); finalize_task() applies state change
- verification failure rolls task to PENDING, records failures in artifact.metadata — no exception
- TaskContract: minimal Pydantic model capturing 3 require_* flags (all True by default)
- No FAILED state: task returns to PENDING on failure — simpler and retryable
- test_context_includes_prior_task_summaries: rewritten to set COMPLETED state manually

## Branch
feature/step6-workspace-runtime (PR #7) — Step 7 in-scope as workspace/runtime progression
