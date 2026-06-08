# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 765-774: Pytest Wrapper Process Isolation.

## Prior Step Status
Steps 755-764: PASS locally. Reviewer reports backend smoke still hangs during
orchestration/storage pytest stage. Root cause: `remedy_pytest.sh` runs
`timeout python3 -m pytest` with inherited stdout/stderr. Child/grandchild
processes keep pipes open, caller waits for EOF indefinitely.

## Fix
Create `scripts/remedy_pytest_runner.py` — Python runner using Popen with
start_new_session=True, temp files for stdout/stderr, killpg cleanup.
Wire `remedy_pytest.sh` to call runner instead of direct `timeout pytest`.

## Runtime Test Architecture
- `scripts/remedy_pytest_runner.py` — pipe-safe pytest execution
- `scripts/remedy_pytest.sh` — flock + calls runner
- `scripts/remedy_runtime_cli_smoke.py` — standalone, no pytest
- `scripts/remedy_backend_basis_smoke.sh` — standalone smoke + helpers + orchestration
- `scripts/remedy_runtime_wrapper_smoke.sh` — separate wrapper verification

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
| Runtime stability (no-hang) | **100%** — pipe-safe runner, all smoke exits clean |
| Ollama via task_execution | **0%** |
| Real test execution | **0%** |
| Rollback/snapshot | **0%** |
| Overnight execution | **0%** |
| UI/dashboard | paused |
