# Running tests + snapshot/rollback proof — user guide (v1)

This guide explains, in plain language, what Remedy can test now, and what its snapshot/rollback
proof does and does **not** mean.

## What Remedy can test now

Remedy can run your project's **allowed** test command through a safe, bounded runner and record the
result as durable evidence. It captures pass/fail, exit code, and duration; raw output is kept private
and never shown in summaries.

```
remedy test run <job_id> ...        # runs the allowed test (contract-gated)
remedy test list <job_id> --json    # safe history
remedy test result <test_run_id> --json
```

## Why commands are allowlisted

Remedy never runs an arbitrary command you type. It only runs a **discovered** test command (from your
Makefile, justfile, Taskfile, package.json, pyproject, or project constitution). Shell metacharacters
and destructive tools (rm, dd, sudo, git, curl, pip, npm, …) are rejected. There is no shell — the
command is run as a fixed argument list. By default the run budget is 0, so a test only runs after you
raise the contract's `max_test_runs`.

## What a snapshot proof means

```
remedy snapshot create <job_id> --json
```

A snapshot proof (v1) records a **metadata snapshot point** — a hash of your repo's file inventory and
a dirty-file count. It proves "here is the state we noted", but it does **not** store file contents.

## Difference between a recorded snapshot and a real rollback restore

This is important: a recorded snapshot is **not** a rollback. v1 cannot restore your repo from a
metadata snapshot. So:

- `snapshot create` → records a snapshot point (`restore_available: false`).
- `rollback proof` → reports honestly whether a real restore path exists. In v1 it is almost always
  `restore_available: false` and `restore_tested: false`, with the limitations listed. It only reports
  `true` when a verified apply-scoped recovery already exists.

```
remedy rollback proof <job_id> --snapshot-id <id> --json
```

## How test failures become repair tasks

When an allowed test fails, Remedy creates a safe Test Failure Artifact (no raw output) and points you
at repair. Remedy does **not** auto-repair — you choose.

## What is not automated yet

- No real rollback restore (metadata proof only).
- No model/provider/Ollama/worker execution.
- No auto-apply, auto-approve, autonomous repair, or auto-PR.
- No full overnight autonomy.
