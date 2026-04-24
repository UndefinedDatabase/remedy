# Plan

## Goal
Step 7.5: Verification Retry Semantics Hotfix.

## Status
COMPLETE. All changes on feature/step6-workspace-runtime (PR #7).

## What Was Done
1. finalize_task: task.output_artifact_ids.clear() on failure — stale artifact ref removed
2. materialize_task_output: lookup artifact via task.output_artifact_ids[0] not task_id scan
   — prevents stale artifact being materialized on retry
3. CLI: sys.exit(1) after verification failure output (save_job called first)
4. Tests: 5 new in test_task_runner.py, 3 new in test_verifier.py; all 195 passing
5. decisions.md: documented all three decisions

## Key Decisions
- clear output_artifact_ids on failure: verifier checks [0] which is then always new
- materialize via output_artifact_ids[0]: precise lookup, no stale-artifact ambiguity
- failed artifact kept in job.artifacts: diagnostic value retained
- exit(1) after save_job: rolled-back state persisted before process terminates

## Branch
feature/step6-workspace-runtime (PR #7) — in-scope per PR Continuity Rule
