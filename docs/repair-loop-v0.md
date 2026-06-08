# Repair Loop v0

When a test fails after apply/test, Remedy creates structured failure evidence and a fix task.
First "Remedy keeps working" moment — no raw output in UI, CLI, or events.

## Flow

```
Test failure → TestFailureArtifact → Fix Task → [optional Fixture Patch Intent] → Stop
```

## Commands

### Start repair loop
```bash
remedy repair start <job_id> <failure_artifact_id> [--fixture-patch-intent] [--json]
```

### Show failure artifact
```bash
remedy repair failure-show <job_id> <failure_artifact_id> [--json]
```

## What gets created

1. **TestFailureArtifact** — structured evidence with:
   - `failure_kind`: test_failed, command_failed, timeout, collection_failed, environment_failed, unknown
   - `safe_summary`: bounded, redacted summary (no raw stdout/stderr)
   - `command_safe`: normalized command (secrets stripped)
   - `output_ref`: basename only (no absolute paths)
   - Links to related intent, apply, task, and test run

2. **Fix Task** — a new Task on the job with:
   - `failure_artifact_id` in inputs
   - `failure_kind` and `safe_summary` for context
   - Idempotent: won't duplicate if already exists

3. **Events** — `test_failure_artifact_created` and `repair_task_created`

## Stop reasons

- `fix_task_created` — fix task created, no patch intent requested
- `approval_required` — fixture patch intent awaiting approval
- `job_not_found` / `failure_artifact_not_found` — error cases

## Safety

- No raw stdout/stderr in artifacts, events, or CLI output
- No absolute paths — output_ref is basename only
- Commands normalized: secrets stripped, bounded to 200 chars
- Summaries bounded to 200-500 chars
- Repair loop stops before any risky action (no apply, no test execution)
- Next safe action commands validated against catalog
