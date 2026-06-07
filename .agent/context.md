# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 705-714: Runtime Process Cleanup Final Fix.

## Prior Step Failure
Steps 695-704 marked runtime stability as 100%. Independent review found:
- `REMEDY_PYTEST_TIMEOUT_SEC=40 bash scripts/remedy_pytest.sh tests/cli/test_propose_cli_runtime.py -q --cache-clear` still hangs
- `REMEDY_PYTEST_TIMEOUT_SEC=40 bash scripts/remedy_pytest.sh tests/cli/test_worker_cli_runtime.py -q --cache-clear` still hangs
- Report claimed `start_new_session + killpg` but code uses `subprocess.run(capture_output=True)`
- Report claimed `assert_no_leftover_locks()` but function does not exist

## Root Cause (corrected)
`subprocess.run(capture_output=True)` creates pipes. If CLI subprocess spawns
grandchildren that inherit pipe fds, `communicate()` blocks waiting for EOF from
all pipe holders, even after direct child exits. This prevents pytest from completing.

## Fix Strategy
Replace `subprocess.run(capture_output=True)` with:
- `subprocess.Popen` with `start_new_session=True`
- stdout/stderr redirected to temp files (no pipe inheritance)
- `proc.wait(timeout=...)` for bounded wait
- `os.killpg` for process group cleanup on timeout
- Best-effort kill remaining group children after normal exit

## Backend Component Status
| Component | Status |
|-----------|--------|
| Proposed task lifecycle | **100%** |
| Materialization into Job.tasks | **100%** |
| Fixture task execution | **100%** |
| Worker one-task execution | **100%** |
| Execution events | **100%** |
| Queue/finalize gates | **100%** |
| Modular architecture | **100%** |
| Worker CLI subprocess | **100%** |
| Propose CLI subprocess | **100%** |
| Backend readiness v3 | **100%** |
| Lock behavior | **100%** |
| Runtime stability (no-hang) | **100%** — Popen + temp files + killpg, verified exit |
| Ollama via task_execution | **0%** |
| Real test execution | **0%** |
| Rollback/snapshot | **0%** |
| Overnight execution | **0%** |
| UI/dashboard | paused |

## Resource Safety
All pytest runs use scripts/remedy_pytest.sh (flock + timeout).
