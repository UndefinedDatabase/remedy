# Plan

## Goal
Step 7: Task Contract v1 and Verifier Gate.

## Status
IN PROGRESS — continuing on feature/step6-workspace-runtime (PR #7)

## Steps
1. [ ] verifier.py: TaskContract, VerificationCheckResult, VerificationResult, verify_task_output
2. [ ] task_runner.py: remove COMPLETED marking from run_next_task; add finalize_task()
3. [ ] CLI: integrate verify_task_output + finalize_task into run-next-task-local flow
4. [ ] Tests: update test_task_runner.py; add test_verifier.py
5. [ ] Docs: README + architecture.md
6. [ ] .agent state + commits + push

## Key Decisions
- task stays RUNNING after run_next_task; COMPLETED only after verify_task_output passes
- verify_task_output is pure (no mutation); finalize_task() applies state change
- verification failure rolls task back to PENDING and records failures in artifact.metadata
- TaskContract: minimal Pydantic model capturing the three require_* flags (all True by default)
- No FAILED state introduced; task returns to PENDING on failure (retryable)
- test_context_includes_prior_task_summaries: rewritten to set up COMPLETED state directly

## Branch
feature/step6-workspace-runtime — Step 7 is in-scope (workspace runtime progression)
PR to update: #7
