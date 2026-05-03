# Context

## Active Branch
`feature/step16-run-logs`

## PR
(none yet)

## Scope
Step 16: Run Logs v1 — append-only JSONL event trail.

New files:
- packages/orchestration/run_log.py: RunEvent dataclass, RunLogWriter, new_run_id, read_run_events
- tests/test_run_log.py: 40 unit tests for run_log primitives
- tests/test_run_log_cli.py: 24 CLI integration tests for run log events

Modified:
- apps/cli/main.py: wired RunLogWriter into _cmd_create_job, _cmd_plan_job_local, _cmd_run_next_task_local
- docs/architecture.md: Run Logs v1 section added

## Key facts
- Log path: <REMEDY_DATA_DIR>/runs/<job_id>/<run_id>.jsonl
- run_id is a UUID4 hex string; one per CLI invocation
- Each event is a JSON object on one line (append-only)
- Redaction: no full content/prompts logged
- log= output added to plan-job-local and run-next-task-local
- create-job logs job_created (no log= printed for that command)
- 635 tests pass
