# Live Review — Steps 1110-1134

Reviewer: parallel reviewer
Scope: Test Evidence Durability + Snapshot / Rollback Proof v1
Timestamp: 2026-06-12

## Verdict
IN PROGRESS — Step 1110 (reconcile) complete. Steps 1111-1134 pending.

## Prior Block Status
- Steps 940-974: PASS
- Steps 975-994: PASS
- Steps 995-1009: PASS
- Steps 1010-1029: PASS WITH RISKS
- Steps 1030-1044: PASS WITH RISKS
- Steps 1045-1064: PASS
- Steps 1065-1084: PASS WITH RISKS (R-0027 carry-forward, resolved in 1086)
- Steps 1085-1109: PASS WITH RISKS (R-0038/R-0041/R-0042/R-0043 carry-forward)

## Finding Ledger

### R-0027: high_risk_command_execution not in canonical action vocabulary

- **Status**: Resolved
- **Severity**: Low
- **Area**: canonical-actions
- **Details**: `_DEFAULT_REQUIRES_APPROVAL` had `"high_risk_command_execution"` not in `ALL_KNOWN_ACTIONS`.
- **Resolution**: Step 1086 replaced with `ContractAction.ARBITRARY_SHELL`. `validate_run_contract()` now checks `requires_approval_for` for unknown actions. Default contract validates with zero errors. 4 new tests confirm canonical invariant.

### R-0029: test_runner.py uses capture_output=True (pipe-based)

- **Status**: Resolved
- **Severity**: Blocker
- **Area**: process-isolation
- **Details**: `test_runner.py:202-206` uses `subprocess.run(argv, capture_output=True, timeout=...)`. Buffers all stdout/stderr in memory via pipes. For large test suites: OOM risk, pipe deadlock risk. Block spec requires file-backed output.
- **Evidence**: `test_runner.py:202` — `proc = subprocess.run(argv, cwd=str(repo_root), capture_output=True, timeout=timeout_sec)`.
- **Resolution**: New `test_execution_service.py:_run_isolated_process()` uses `subprocess.Popen` with file-backed output (`output_file`). No `capture_output=True`. Test `test_uses_popen_not_subprocess_run` verifies at source level. Uncommitted.

### R-0030: No process-group cleanup on timeout

- **Status**: Resolved
- **Severity**: Blocker
- **Area**: process-isolation
- **Details**: No `start_new_session=True`. No `os.killpg()`. `subprocess.run` timeout kills direct child only — descendants survive. No SIGTERM-then-SIGKILL sequence. No `stdin=DEVNULL`. No `close_fds=True`.
- **Resolution**: `test_execution_service.py:_run_isolated_process()` uses `start_new_session=True`, `stdin=DEVNULL`, `close_fds=True`. `_kill_process_group()` does `os.killpg(pgid, SIGTERM)` → 3s wait → `os.killpg(pgid, SIGKILL)` → `proc.wait()`. Tests verify all 4 flags at source level. Uncommitted.

### R-0031: No contract enforcement in test_runner.py

- **Status**: Resolved
- **Severity**: Blocker
- **Area**: run-contract
- **Details**: `run_tests_local()` does not check RunContract. No `evaluate_run_action(contract, "run_test")`. No `max_test_runs` check. No `test_runs_used` increment. CLI is the only enforcement point — bypass is trivial.
- **Resolution**: New `test_execution_service.py:execute_test_run()` enforces 13-gate order: load job → validate repo → permission check → load+validate contract → load usage → evaluate_run_action(RUN_TEST) → acquire lease → discover command → execute isolated → persist usage → persist record → emit events → create failure artifact. 7 gate tests verify all block reasons. Uncommitted.

### R-0032: No secret/environment stripping before subprocess

- **Status**: Resolved
- **Severity**: High
- **Area**: environment
- **Details**: `subprocess.run` at line 202 inherits full `os.environ`. Secret-like env vars (API_KEY, SECRET, TOKEN, PASSWORD, AWS_*, OPENAI_*, etc.) visible to child test process.
- **Resolution**: `_build_safe_env()` strips keys matching 14 secret patterns (token, secret, password, credential, api_key, etc.). Only `_ALWAYS_KEEP` names and `_SAFE_ENV_PREFIXES` preserved. Unknown keys silently dropped (strict-safe). 11 env policy tests verify stripping. Uncommitted.

### R-0033: No concurrency guard for same job/repo

- **Status**: Resolved
- **Severity**: High
- **Area**: concurrency
- **Details**: No lease or lock prevents two simultaneous test runs for same job or repo. Could cause filesystem contention, test interference, usage double-counting.
- **Resolution**: `TestExecutionLease` uses `fcntl.flock(LOCK_EX|LOCK_NB)` per job_id. Acquired at Gate 7, released in `finally` block. 3 lease tests verify acquire/release, concurrent fail, idempotent release. Uncommitted.

### R-0034: No TestFailureArtifact created on failed/timeout runs

- **Status**: Resolved
- **Severity**: High
- **Area**: failure-artifact
- **Details**: `run_tests_local()` returns `TestRunRecord` with status "failed"/"timeout" but does not create `TestFailureArtifact`. Repair loop requires these to create fix tasks.
- **Resolution**: Gate 13 in `execute_test_run()` calls `_create_failure_artifact()` on failed/timeout/environment_failure. Uses existing `build_test_failure_artifact` + `persist_failure_artifact`. Result.failure_artifact_id set. Event emitted. Uncommitted.

### R-0035: test_runs_used not incremented by test_runner

- **Status**: Resolved
- **Severity**: High
- **Area**: usage-ledger
- **Details**: `run_tests_local()` does not call `save_usage()` to increment `test_runs_used`. Usage tracking exists in `run_contract.py` but test_runner doesn't use it. Blocked-before-start must NOT consume budget.
- **Resolution**: Gate 10 in `execute_test_run()` reloads job, loads usage, increments `test_runs_used += 1` and `runtime_seconds_used += duration_ms/1000.0`, then `save_usage()`. Blocked-before-start confirmed zero cost via `test_blocked_does_not_consume_usage`. Uncommitted.

### R-0036: max_test_runs=0 makes tests permanently impossible without documented escape

- **Status**: Resolved
- **Severity**: Medium
- **Area**: run-contract
- **Details**: Default contract had `max_test_runs=0` and `run_test` not in `_DEFAULT_ALLOWED_ACTIONS`.
- **Resolution**: Step 1087 adds `run_test` to `_DEFAULT_ALLOWED_ACTIONS`. Zero-budget check in `evaluate_run_action` blocks `run_test` when `max_test_runs==0`. Dual gate: (1) permission `repo_test_run allow`, (2) `contract set max_test_runs N`. 7 new tests confirm dual-gate invariant.

### R-0037: Step 1084 handoff not committed — context.md lists resolved gaps as current

- **Status**: Resolved
- **Severity**: Medium
- **Area**: handoff
- **Details**: context.md "Truth Gaps" 1-7 all resolved but still listed as current. plan.md Step 1084 unchecked.
- **Resolution**: Step 1085 commit `016d715` closes Step 1084, updates context.md (truth gaps removed), marks plan.md complete. PR #52 merged to main.

### R-0038: Silent exception swallowing in persistence helpers

- **Status**: Open → Fix in Steps 1115-1116
- **Severity**: Medium (raised from Low — budget consumed silently on evidence loss)
- **Area**: error-handling
- **Details**: `_persist_test_record()` (line 775) and `_create_failure_artifact()` (line 829) both `except Exception: pass`. Budget consumed, no durable record.

### R-0041: Fake test.status next_safe_action

- **Status**: Open → Fix in Step 1111
- **Severity**: Medium
- **Area**: command-catalog
- **Details**: `execute_test_run()` emits `"remedy test status {job.id}"` when lease is held (line ~600). `test.status` does not exist in command catalog. Emitting nonexistent commands violates catalog truth invariant.

### R-0042: Test lease is job-scoped only — concurrent repo tests possible

- **Status**: Open → Fix in Step 1112
- **Severity**: Medium
- **Area**: concurrency
- **Details**: `TestExecutionLease` key = job_id only. Two different jobs targeting the same repository can run tests simultaneously, causing filesystem contention and test interference.

### R-0043: Partial evidence persistence — usage consumed without durable record

- **Status**: Open → Fix in Steps 1114-1116
- **Severity**: High
- **Area**: evidence-durability
- **Details**: Usage, test record, events, and failure artifact are finalized in separate saves. Crash after usage increment but before record persist = budget consumed + invisible run. No atomic finalization path. No evidence_status field on result to signal partial persistence.

### R-0039: Old test_runner.py:run_tests_local() still has capture_output=True

- **Status**: Resolved
- **Severity**: Medium
- **Area**: deprecation
- **Details**: Old `test_runner.py:run_tests_local()` retains `subprocess.run(capture_output=True)` without contract enforcement. Until CLI routes through new service (Step 1099) and old function is deprecated, callers can bypass all gates.
- **Resolution**: Commit `0abf570` (Step 1099) routes `test.run` CLI through `execute_test_run()`. `_cmd_run_tests_local()` replaced with `_cmd_run_tests()`. No references to `run_tests_local` remain in CLI. Old function still exists in `test_runner.py` but is no longer called from production paths.

### R-0040: 2 old CLI tests fail — gate order + message format mismatch

- **Status**: Resolved
- **Severity**: Medium
- **Area**: test-compatibility
- **Details**: 2 tests in `tests/test_test_runner.py::TestCliRunTestsLocal` failed after service routing:
  1. `test_permission_missing_exits_1`: permission gate now fires before target_repo gate (security-correct order).
  2. `test_no_target_repo_exits_1`: message text "No target repository" vs old literal "target_repo".
- **Resolution**: Step 1104-1106 commit: swapped gates 2/3 (permission before target_repo), updated old test assertion. 5163 passed, 1 pre-existing fail, 8 skipped.

## Baseline Checks (Pre-Worker)

| Check | Status | Notes |
|-------|--------|-------|
| Previous block closure | PASS | Step 1084 committed, PR #52 merged, context.md updated |
| Central test service | PASS (committed) | test_execution_service.py with 13-gate execute_test_run() |
| Permission/contract | PASS (committed) | Gates 3-6: permission + contract + budget + evaluate_run_action |
| Process isolation | PASS (committed) | Popen + start_new_session + file-backed output |
| Environment | PASS (committed) | _build_safe_env strips 14 secret patterns |
| Lease/concurrency | PASS (committed) | fcntl.flock per job_id, released in finally |
| Timeout cleanup | PASS (committed) | SIGTERM→3s→SIGKILL→wait on process group |
| Usage ledger | PASS (committed) | test_runs_used + runtime_seconds_used incremented post-exec |
| Failure artifact | PASS (committed) | _create_failure_artifact on failed/timeout/env_failure |
| Proof linkage | PASS (committed) | test_run_timed_out collected in proof chain |
| CLI runtime | PASS | 5163 passed, 23 new runtime tests, R-0040 resolved |
| Redaction | PASS (committed) | No raw output in Result, events, metadata, review bundle |
| Progress/feature/review | PASS (committed) | Test results → ProgressItem, test_execution_summary in bundle |
