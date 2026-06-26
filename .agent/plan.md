# Plan — Steps 4975-4990: Job Promote Baseline-Aware Safety Closure v2

## Goal
Replace naive target-cleanliness check with baseline-aware promotion that records
pre-job file hashes and uses them for safety checks, enabling legitimate reviewed
modifications to existing files while still blocking external changes.

## Current Step
All implementation and tests complete. Ready for commit.

## Completed
- Step 4975: `AppliedFileProof` dataclass with path, hashes, task_id, run_id
- Step 4976: Baseline capture in `_strict_apply_to_workspace` + `job_baselines` tracking in `run_job`
- Step 4977: `_check_baseline_readiness` replaces `_check_target_cleanliness`, `FileReadiness` model
- Step 4978: Legacy jobs without baseline proof: new files allowed, existing-file modifications blocked
- Step 4979: Promotion record persistence test fixed (file-based blocker)
- Step 4980: Preflight persistence check verified correct
- Step 4981: Regression test — legitimate existing-file modification promotes
- Step 4982: Regression test — target changed after job blocks
- Step 4983: Regression test — target file created after job blocks
- Step 4984: Regression test — workspace changed after review blocks
- Step 4985: Existing symlink/containment tests pass (9 tests)
- Step 4986: Grouped CLI subprocess tests (4 tests: dry-run JSON, approve, blocked, nonexistent)
- Step 4987: Dry-run output shows per-file baseline status
- Step 4988: Redaction and promotion records preserved
- Step 4989: Full suite 8037 passed (1 pre-existing failure in test_project_brain)
- Step 4990: Architecture guard clean, final handoff

## Test Counts
- job_promote: 61 (was 46, +15 new)
- Full suite: 8037 passed (1 pre-existing failure in test_project_brain)
