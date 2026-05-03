# Plan

## Goal
Step 16: Run Logs v1 — append-only JSONL event trail for every Remedy operation.

## Status
COMPLETE — 635 tests pass

## Steps
1. [x] Create packages/orchestration/run_log.py (RunEvent, RunLogWriter, new_run_id, read_run_events)
2. [x] Wire into _cmd_create_job: job_created event
3. [x] Wire into _cmd_plan_job_local: planning_started, planning_completed/failed + log= output
4. [x] Wire into _cmd_run_next_task_local: full event sequence + log= output
5. [x] Create tests/test_run_log.py (unit tests for RunLogWriter, RunEvent, helpers)
6. [x] Create tests/test_run_log_cli.py (CLI integration tests for all event types)
7. [x] Update docs/architecture.md (Run Logs v1 section)
8. [x] Update .agent files and commit

## Branch
feature/step16-run-logs
