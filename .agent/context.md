# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 695-704: Runtime Exit Final Fix.

## Hang Root Cause
Runtime test files imported `packages.orchestration.proposed_tasks` which uses `fcntl.flock`.
When `add_proposed_task` was called in-process, the flock fd (even after release and unlink)
left kernel-level lock state that prevented pytest from exiting on some platforms.

**Fix**: Runtime test files no longer import any module that uses fcntl.flock.
All test data setup uses direct JSON file writes via `runtime_helpers.py`.
Subprocess helper uses `subprocess.run` with `stdin=DEVNULL, close_fds=True`.

## Note
A test file that prints "passed" but does not exit is a failure.

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
| Runtime stability (no-hang) | **100%** — no flock in test process |
| Ollama via task_execution | **0%** |
| Real test execution | **0%** |
| Rollback/snapshot | **0%** |
| Overnight execution | **0%** |
| UI/dashboard | paused |

## Resource Safety
All pytest runs use scripts/remedy_pytest.sh (flock + timeout).
