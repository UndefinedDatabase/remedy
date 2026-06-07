# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 755-764: Backend Smoke Final Isolation.

## Prior Step Status
Steps 745-754: PASS locally. Reviewer reports backend smoke still hangs when
running runtime pytest wrappers sequentially. The wrappers reintroduce
pytest-process runtime contamination even in separate invocations.

## Fix
1. Backend smoke: standalone runtime smoke + helpers + orchestration (no wrappers)
2. New script: remedy_runtime_wrapper_smoke.sh for separate wrapper testing
3. Harden remedy_pytest.sh with --kill-after so stuck pytest can't hang forever

## Runtime Test Architecture
- `scripts/remedy_runtime_cli_smoke.py` — standalone, no pytest, full isolation
- `scripts/remedy_backend_basis_smoke.sh` — uses standalone smoke, not wrappers
- `scripts/remedy_runtime_wrapper_smoke.sh` — separate wrapper verification
- `tests/cli/test_propose_cli_runtime.py` — thin wrapper, run individually only
- `tests/cli/test_worker_cli_runtime.py` — thin wrapper, run individually only

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
| Runtime stability (no-hang) | **100%** — smoke uses standalone runtime, no wrappers |
| Ollama via task_execution | **0%** |
| Real test execution | **0%** |
| Rollback/snapshot | **0%** |
| Overnight execution | **0%** |
| UI/dashboard | paused |
