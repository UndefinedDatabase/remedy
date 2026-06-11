# Live Review — Steps 1085-1109

Reviewer: parallel reviewer
Scope: Real Test Execution — contract-gated, resource-safe, evidence-linked
Timestamp: 2026-06-11

## Verdict
PENDING — baseline scan complete, 3 blockers + 4 high identified, worker has not started this block yet

## Prior Block Status
- Steps 940-974: PASS
- Steps 975-994: PASS
- Steps 995-1009: PASS
- Steps 1010-1029: PASS WITH RISKS
- Steps 1030-1044: PASS WITH RISKS
- Steps 1045-1064: PASS
- Steps 1065-1084: PASS WITH RISKS (R-0027 low carry-forward)

## Finding Ledger

### R-0027: high_risk_command_execution not in canonical action vocabulary

- **Status**: Open (carry forward)
- **Severity**: Low
- **Area**: canonical-actions
- **Details**: `_DEFAULT_REQUIRES_APPROVAL` at `run_contract.py:178` has `"high_risk_command_execution"` not in `ALL_KNOWN_ACTIONS`.
- **Expected fix**: Add to ContractAction or replace with canonical name.

### R-0029: test_runner.py uses capture_output=True (pipe-based)

- **Status**: Open
- **Severity**: Blocker
- **Area**: process-isolation
- **Details**: `test_runner.py:202-206` uses `subprocess.run(argv, capture_output=True, timeout=...)`. Buffers all stdout/stderr in memory via pipes. For large test suites: OOM risk, pipe deadlock risk. Block spec requires file-backed output.
- **Evidence**: `test_runner.py:202` — `proc = subprocess.run(argv, cwd=str(repo_root), capture_output=True, timeout=timeout_sec)`.
- **Expected fix**: Use `Popen` with file descriptors writing to temp files. Read file after process exits.

### R-0030: No process-group cleanup on timeout

- **Status**: Open
- **Severity**: Blocker
- **Area**: process-isolation
- **Details**: No `start_new_session=True`. No `os.killpg()`. `subprocess.run` timeout kills direct child only — descendants survive. No SIGTERM-then-SIGKILL sequence. No `stdin=DEVNULL`. No `close_fds=True`.
- **Evidence**: `test_runner.py:202` — plain subprocess.run, no session or group handling. `TimeoutExpired` at line 212 does not kill process group.
- **Expected fix**: `Popen` with `start_new_session=True`, `stdin=DEVNULL`, `close_fds=True`. On timeout: `os.killpg(proc.pid, SIGTERM)`, brief wait, `os.killpg(proc.pid, SIGKILL)`, `proc.wait()`.

### R-0031: No contract enforcement in test_runner.py

- **Status**: Open
- **Severity**: Blocker
- **Area**: run-contract
- **Details**: `run_tests_local()` does not check RunContract. No `evaluate_run_action(contract, "run_test")`. No `max_test_runs` check. No `test_runs_used` increment. CLI is the only enforcement point — bypass is trivial.
- **Evidence**: `test_runner.py:136-138` docstring: "Does NOT check the repo_test_run permission — the caller (CLI) is responsible for that gate."
- **Expected fix**: Create central Test Execution Service that enforces contract + usage + permission, or add gates to `run_tests_local` directly.

### R-0032: No secret/environment stripping before subprocess

- **Status**: Open
- **Severity**: High
- **Area**: environment
- **Details**: `subprocess.run` at line 202 inherits full `os.environ`. Secret-like env vars (API_KEY, SECRET, TOKEN, PASSWORD, AWS_*, OPENAI_*, etc.) visible to child test process.
- **Evidence**: Docstring line 26: "inherits os.environ (no extra vars, no .env reading)" — confirms no stripping.
- **Expected fix**: Build filtered env dict stripping keys matching secret patterns before passing to Popen.

### R-0033: No concurrency guard for same job/repo

- **Status**: Open
- **Severity**: High
- **Area**: concurrency
- **Details**: No lease or lock prevents two simultaneous test runs for same job or repo. Could cause filesystem contention, test interference, usage double-counting.
- **Expected fix**: File-based lease per job_id in workspace, released on completion/error/timeout.

### R-0034: No TestFailureArtifact created on failed/timeout runs

- **Status**: Open
- **Severity**: High
- **Area**: failure-artifact
- **Details**: `run_tests_local()` returns `TestRunRecord` with status "failed"/"timeout" but does not create `TestFailureArtifact`. Repair loop requires these to create fix tasks.
- **Expected fix**: On failed/timeout, create `TestFailureArtifact` with safe fields linking to test run.

### R-0035: test_runs_used not incremented by test_runner

- **Status**: Open
- **Severity**: High
- **Area**: usage-ledger
- **Details**: `run_tests_local()` does not call `save_usage()` to increment `test_runs_used`. Usage tracking exists in `run_contract.py` but test_runner doesn't use it. Blocked-before-start must NOT consume budget.
- **Expected fix**: Increment `test_runs_used` on actual process start only. Record measured runtime in `runtime_seconds_used`.

### R-0036: max_test_runs=0 makes tests permanently impossible without documented escape

- **Status**: Open
- **Severity**: Medium
- **Area**: run-contract
- **Details**: Default contract: `max_test_runs=0`, `run_test` not in `_DEFAULT_ALLOWED_ACTIONS`. User cannot enable tests through `contract set` alone since `allowed_actions` is not a settable field.
- **Evidence**: `run_contract.py:205` — `max_test_runs=0`. `run_contract.py:137-145` — no `run_test`.
- **Expected fix**: Document explicit steps to enable: `contract set max_test_runs N`, plus add a safe enable path for `run_test` in allowed_actions.

### R-0037: Step 1084 handoff not committed — context.md lists resolved gaps as current

- **Status**: Resolved
- **Severity**: Medium
- **Area**: handoff
- **Details**: context.md "Truth Gaps" 1-7 all resolved but still listed as current. plan.md Step 1084 unchecked.
- **Resolution**: Step 1085 commit `016d715` closes Step 1084, updates context.md (truth gaps removed), marks plan.md complete. PR #52 merged to main.

## Baseline Checks (Pre-Worker)

| Check | Status | Notes |
|-------|--------|-------|
| Previous block closure | PASS | Step 1084 committed, PR #52 merged, context.md updated |
| Central test service | ABSENT | test_runner.py exists but no service with gates |
| Permission/contract | FAIL | No contract check in test_runner |
| Process isolation | FAIL | capture_output=True, no session, no group cleanup |
| Environment | FAIL | No secret stripping |
| Lease/concurrency | ABSENT | No guard |
| Timeout cleanup | FAIL | Kills child only, descendants survive |
| Usage ledger | FAIL | test_runs_used not incremented |
| Failure artifact | ABSENT | No TestFailureArtifact on failure |
| Proof linkage | ABSENT | No proof integration yet |
| CLI runtime | PASS (prior) | Existing tests adequate |
| Redaction | PASS (partial) | TestRunRecord safe; raw output in workspace file |
| Progress/feature/review | PASS (prior) | Need test events wired |
