# Plan — Steps 4845-4856: Job Runner CLI Control + Execution Metadata Closure v2

## Goal
Fix repair-round coercion bug, add execution metadata, strengthen guards and tests.

## Current Step
Complete. All implementation, tests, verification done. Pending handoff.

## Completed
- Step 4845: Fix `--repair-rounds 0` coercion — removed `or 2`, use resolve_repair_rounds
- Step 4846: Repair-round source in job execution metadata — JobPlan.repair_rounds_source
- Step 4847: Pass repair-round source into run_pingpong per task
- Step 4848: Real CLI handler tests for omitted/default repair rounds
- Step 4849: Real CLI handler tests for explicit zero
- Step 4850: Real CLI handler tests for explicit one
- Step 4851: Fix command catalog may_execute_commands=True for do.job-run
- Step 4852: Target repo mutation guard negative test via monkeypatch
- Step 4853: Partial-run status JOB_PAUSED for --max-tasks
- Step 4854: Job report repair metadata (rounds/source/per-task)
- Step 4855: Preserved all safety + token-bounded context
- Step 4856: Architecture guard clean, handoff pending
