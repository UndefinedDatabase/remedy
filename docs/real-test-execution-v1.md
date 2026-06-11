# Real Test Execution v1

## Overview

Test execution in Remedy v1 is contract-gated, resource-safe, and evidence-linked. Every test run passes through the central Test Execution Service (`packages/orchestration/test_execution_service.py`) which enforces all gates before any process starts.

## Dual Gate Requirement

A real test command may only run when **both** conditions are true:

1. **Permission granted**: `remedy job permit <job_id> repo_test_run allow`
2. **Contract budget set**: `remedy contract set <job_id> max_test_runs <n>`

Either gate alone is insufficient. The default contract has `max_test_runs=0`.

## Gate Order

`execute_test_run(request)` enforces gates in this order:

1. Load job safely
2. Validate target repository exists
3. Verify `repo_test_run` permission
4. Load persisted RunContract + validate
5. Load RunUsage
6. Evaluate `run_test` action (contract + budget)
7. Acquire test execution lease (prevents concurrent runs)
8. Discover safe test command via `command_discovery.py`
9. Execute with process isolation
10. Persist usage and test record
11. Emit lifecycle events
12. Create TestFailureArtifact if failed/timeout
13. Release lease (always via try/finally)

Gates 1-8 are blocked-before-start — they consume zero test run slots.

## Process Isolation

The subprocess runs with:

- `subprocess.Popen` (not `subprocess.run`)
- `start_new_session=True` — child gets its own process group
- `stdin=subprocess.DEVNULL`
- `close_fds=True`
- stdout and stderr written directly to a bounded workspace file (not pipes)

On timeout:

1. `os.killpg(pgid, SIGTERM)` — graceful termination
2. Wait up to 3 seconds
3. `os.killpg(pgid, SIGKILL)` — force kill
4. `proc.wait()` — reap

Descendant processes cannot keep execution hanging.

## Environment Sanitization

Before the subprocess starts, the environment is filtered by `_build_safe_env()`:

- **Stripped**: any key whose name contains `token`, `secret`, `password`, `passwd`, `credential`, `api_key`, `apikey`, `private_key`, `access_key`, etc.
- **Preserved**: `PATH`, `HOME`, `USER`, `SHELL`, `TERM`, `LANG`, `TMPDIR`, `VIRTUAL_ENV`, `GOPATH`, `CARGO_HOME`, locale variables, etc.

**No `.env` files are read or loaded.**

**OS-level network isolation is NOT implemented in v1.** `no_cloud=True` in the contract is a policy statement, not a network sandbox.

## Raw Output

Raw stdout and stderr are written to:

```
<data_dir>/workspaces/<job_id>/test_runs/<test_run_id>.txt
```

Maximum size: 1 MiB. Larger output is truncated with a `[remedy output truncated]` marker.

**Raw output is never included in**:
- `TestExecutionResult` fields
- Job metadata test run records
- Timeline events
- TestFailureArtifact
- Review Bundle

The output file path (`output_ref`) is the only reference stored.

## Automatic Failure Artifact

For `status in (failed, timeout, environment_failure)`, a `TestFailureArtifact` is created automatically with:

- `test_run_id` linkage
- Safe failure kind and summary
- Output reference (not content)
- Optional intent/task/apply linkage

Next safe action points to:

```
remedy repair start <job_id> <failure_artifact_id> --json
```

## Linkage

The CLI supports optional linkage:

```
remedy test run <job_id> \
  --task-id <id> \
  --intent-id <id> \
  --apply-id <id> \
  --timeout-seconds <n> \
  --json
```

Invalid IDs are validated before the test runs.

Linked tests propagate to Proof Chain:
- Passed linked test → proof confirmed for that change
- Failed/timeout linked test → proof failed for that change
- Unlinked test → does not verify unrelated changes

## Concurrency

Only one test run per job is allowed at a time. A second simultaneous request returns `test_run_already_active`. The lease is always released (pass, fail, timeout, or exception).

## Timeout

The actual process timeout is the minimum of:
- System maximum (600 seconds)
- Requested timeout (if provided)
- Remaining `max_runtime_seconds` from the contract

If no runtime remains, the run is blocked before starting.

## Usage Accounting

- `test_runs_used` incremented **only on actual process start** (not on blocked runs)
- `runtime_seconds_used` incremented by actual measured duration
- Both values are persisted atomically after each run
- Second run blocks when `test_runs_used >= max_test_runs`

## Guidance

When blocked, the CLI provides the appropriate next safe action:

| Reason | Guidance |
|--------|----------|
| Permission missing | `remedy job permit <job_id> repo_test_run allow` |
| Budget zero/exhausted | `remedy contract set <job_id> max_test_runs <n>` |
| Action denied | `remedy contract inspect <job_id> --json` |
| Another run active | `remedy test status <job_id>` (safe retry, not immediate) |

Every guidance command exists in the command catalog.

## CLI

```
remedy test run <job_id> [--task-id T] [--intent-id I] [--apply-id A]
                         [--timeout-seconds N] [--json]
remedy test discover <job_id> [--json]
```

Text output (non-JSON) is written to stderr for blocked/failed runs, stdout for passed.

## Limitations in v1

- No OS-level network sandbox (no_cloud is a contract policy, not a kernel firewall)
- No automatic repair triggered by test failures (requires `remedy repair start ...`)
- No snapshot/rollback implementation
- No overnight/unattended mode
