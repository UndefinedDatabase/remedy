# Live Review — Steps 4845-4856: Job Runner CLI Control + Execution Metadata Closure v2

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-25

## Verdict (reviewer-owned)
(pending)

## Builder handoff

### Step 4845 — Preserve explicit --repair-rounds 0
- `do_cmd.py` L823: removed `int(getattr(args, "repair_rounds", None) or 2)` — 0 was falsy, coerced to 2
- Changed handler lambda to pass raw `getattr(args, "repair_rounds", None)` (None when omitted, 0 when explicit)
- `_cmd_do_job_run` now accepts `repair_rounds: int | None = None` and calls `resolve_repair_rounds()` internally
- Same resolver semantics as single-task `do run` — negative raises, above cap raises

### Step 4846 — Repair-round source in job execution metadata
- Added `repair_rounds_allowed: int` and `repair_rounds_source: str` to `JobPlan` dataclass
- Persisted in `_export_job` / `_import_job` round-trip
- Values: `{"repair_rounds_allowed": 0, "repair_rounds_source": "cli"}` or `{"repair_rounds_allowed": 2, "repair_rounds_source": "default"}`

### Step 4847 — Pass repair-round source into run_pingpong per task
- `run_job()` now accepts `repair_rounds_source: str = "default"`
- Passes to `run_pingpong()` call at L733: `repair_rounds_source=repair_rounds_source`
- Each task's `run_pingpong` result preserves the source

### Step 4848 — Real CLI handler tests for omitted/default
- `TestCliHandlerRepairRounds::test_omitted_gives_default`: exercises `COMMAND_HANDLERS["do.job-run"]` with args.repair_rounds=None
- Asserts `data["repair_rounds_allowed"] == 2` and `data["repair_rounds_source"] == "default"` from JSON output

### Step 4849 — Real CLI handler tests for explicit zero
- `TestCliHandlerRepairRounds::test_explicit_zero`: exercises handler with args.repair_rounds=0
- Asserts `repair_rounds_allowed == 0` and `repair_rounds_source == "cli"`
- Would have FAILED on the old code (0 or 2 → 2)
- `test_explicit_zero_no_repair_attempt`: confirms `repair_rounds_used == 0` per task

### Step 4850 — Real CLI handler tests for explicit one
- `TestCliHandlerRepairRounds::test_explicit_one`: exercises handler with args.repair_rounds=1
- Asserts `repair_rounds_allowed == 1` and `repair_rounds_source == "cli"`

### Step 4851 — Fix command catalog for do.job-run
- Changed `may_execute_commands=False` → `may_execute_commands=True` in catalog
- Updated help text: `"Max repair attempts per task (default: 2, 0=disabled)"`
- Tests: `TestCatalogMetadata` (4 tests) — job-run True, job-plan False, job-report False, no mutate_repo

### Step 4852 — Target repo mutation guard negative test
- `TestTargetMutationNegative::test_target_mutation_blocks_job`: monkeypatches `run_pingpong` to write `INJECTED.txt` to real repo after first task
- Asserts: `JOB_BLOCKED`, `target_mutated=True`, `INJECTED.txt` in changed files, second task skipped
- `test_mutation_reports_changed_files`: overwrites existing file, confirms guard reports it

### Step 4853 — Partial-run status JOB_PAUSED
- Added `JOB_PAUSED = "paused"` constant
- `run_job()` sets `JOB_PAUSED` when max_tasks stops execution with pending tasks remaining
- `_suggest_next_command` handles `JOB_PAUSED` → `remedy do job-run {job_id}`
- `format_job_report_text` shows `"Paused: N tasks pending"`
- `export_job_report` includes `"pending_tasks": count`
- Tests: `TestPartialRunStatus` (6 tests) — paused status, not running, copyable command, pending count, continuation, full run completed

### Step 4854 — Job report repair metadata
- `export_job_report` includes: `repair_rounds_allowed`, `repair_rounds_source`, `pending_tasks`
- `format_job_report_text` shows: `"Repair: N rounds (source: cli/default)"` + `"(disabled)"` when 0
- Per-task: `repair_rounds_used`, `repair_rounds_allowed` already present
- Tests: `TestReportRepairMetadata` (5 tests) — allowed, source, per-task, text report, context strategy

### Step 4855 — Preserved safety and token-bounded context
All existing tests pass unchanged:
- Deterministic task IDs (5 tests)
- Strict workspace apply (8 tests)
- Missing/env/traversal/duplicate artifact blocking (5 tests)
- Target repo guard clean path (2 tests)
- Task completion gate (3 tests)
- Proof summaries (3 tests)
- Token context policy (1 test)
- Token-bounded prompts (5 tests)
- Existing flow preservation (9 tests)
- Persistence round-trip (3 tests)
- Job plan parsing (8 tests)

### Step 4856 — Architecture guard
All clean:
- No `or 2` coercion on repair_rounds in production code
- No stale `remedy do job run/plan/report` (space-separated)
- No `do.job-run` with `may_execute_commands=False`
- No `shell=True` in product code
- No `subprocess` in pingpong_job
- No `git commit/push/reset/checkout`
- No `os.environ`/`getenv`
- No `live_review.md` product dependency
- No auto-promotion
- No task IDs from heading number
- No silent workspace apply skips
- Path safety: traversal, .env, .git, keys, unsafe dirs blocked
- Token-bounded: last 5 summaries, 2000-char body limit
- Full repo not in prompt
- No env/API key leakage
- Task body not in public report (only internal persistence, already bounded)

## Edited file and line-range map
- `apps/cli/commands/do_cmd.py` L697-731 (handler), L828 (lambda) — repair-rounds fix
- `apps/cli/command_catalog.py` L2384, L2391 — catalog metadata fix
- `packages/orchestration/pingpong_job.py` L46 (JOB_PAUSED), L137-138 (JobPlan fields), L265-266 (export), L303-304 (import), L635 (run_job param), L664-667 (metadata set), L736 (repair_rounds_source pass), L808-820 (paused status), L926-942 (report metadata), L997-1008 (text report repair info), L1028-1029 (suggest paused)
- `tests/orchestration/test_job_task_runner.py` L694-1033 — 30 new tests across 6 classes

## Test counts
- Job task runner: 95/95 pass (was 65, +30 new)
- Job fulfillment: 109/109 pass (twice, deterministic)
- Fast lane: 571/571 pass
- Runtime lane: 57/57 pass (4/4 suites)
- Lint: ruff clean, mypy clean (200 source files)
- Full suite: 7837 passed, 8 skipped, 1 deselected, 0 failed (236s)

## Test classes added (Steps 4845-4856)
- TestRepairRoundsCoercion (7 tests): resolver None/0/1/negative/cap, job-run explicit zero, job-run default
- TestCliHandlerRepairRounds (6 tests): omitted, explicit zero, explicit one, no repair attempt, report disabled, report json source
- TestCatalogMetadata (4 tests): job-run execute, job-run no mutate, job-plan no execute, job-report no execute
- TestTargetMutationNegative (2 tests): mutation blocks, mutation reports files
- TestPartialRunStatus (6 tests): paused, not running, copyable command, pending count, continuation, full completed
- TestReportRepairMetadata (5 tests): allowed, source, per-task, text report, context strategy

## What this proves
- `--repair-rounds 0` truly disables repair (0 is not coerced to 2)
- Omitted `--repair-rounds` defaults to 2 via resolve_repair_rounds
- `--repair-rounds 1` uses exactly one repair round
- Repair-round source visible in job reports (CLI and JSON)
- do.job-run admits command execution in catalog
- Target repo mutation during job execution blocks the job
- Partial max-tasks run produces "paused" not "running"
- Continuation after pause completes remaining tasks
- All previous safety invariants preserved

## What this does not prove
- Real provider (Claude/Ollama) repair behavior — only fake providers tested
- Multi-task repair interaction — repair_rounds=1 with fail-then-pass not tested at job level (would need FakeProvider sequence control per task)
- Real CLI subprocess invocation — tests exercise handler lambdas, not full `remedy do job-run` subprocess
- Production job file parsing edge cases beyond current test fixtures
- Target repo promotion — explicitly not built yet

## Final 5-minute quiet-window check
Builder will wait 5 minutes after commit before writing final handoff confirmation.
