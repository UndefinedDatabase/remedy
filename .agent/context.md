# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 685-694: Runtime Hang Kill, Backend Basis Actually Final.
UI/design work is PAUSED.

## Canonical Review File
`.agent/live_review.md` — NOT `.data/live_review.md`

## Hang Root Cause (Found Step 686)
Lock files left on disk by `_file_lock` context manager. The `.lock` files were created by
`os.open(..., O_CREAT | O_RDWR)` but never deleted after lock release. In some environments,
stale lock files on shared/tmp filesystems caused `flock()` contention in subsequent subprocesses.
Additionally, there was a double `os.close(fd)` bug in the finally block.

**Fix**: `_file_lock` now deletes lock file after releasing lock and closing fd. Double-close removed.
Anti-hang guard: `assert_no_leftover_locks()` in test fixture teardown.
Subprocess isolation: `start_new_session=True` + `os.killpg` on timeout.

## Basis Closed Criteria (All Proven)
1. Propose runtime file exits cleanly — 11 passed, 0 errors
2. Worker runtime file exits cleanly — 6 passed, 0 errors
3. Smoke script exits cleanly — 177 passed
4. Worker executes persisted task — test_worker_execution.py
5. Events exist — started + completed/blocked
6. Readiness/finalize correct — test_proposed_tasks.py
7. No leftover lock files — assert_no_leftover_locks guard

## Backend Component Status — Post Steps 685-694
| Component | Status |
|-----------|--------|
| Proposed task lifecycle | **100%** |
| Materialization into Job.tasks | **100%** |
| Fixture task execution | **100%** |
| Worker one-task execution | **100%** |
| Execution events | **100%** |
| Queue/finalize gates | **100%** |
| Modular architecture (Baukasten) | **100%** |
| Worker CLI subprocess | **100%** |
| Propose CLI subprocess | **100%** |
| Backend readiness v3 | **100%** |
| Lock behavior (timeout + cleanup) | **100%** |
| Runtime stability (no-hang) | **100%** |
| Ollama via task_execution | **0%** |
| Real test execution | **0%** |
| Rollback/snapshot | **0%** |
| Overnight execution | **0%** |
| UI/dashboard | paused |

## Do Not Reopen Without Evidence
Components at 100% require a failing test or reproducible bug to reopen.

## Resource Safety
All pytest runs use scripts/remedy_pytest.sh (flock + timeout).
