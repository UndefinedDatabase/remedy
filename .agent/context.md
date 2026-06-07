# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 745-754: Remove Runtime Smoke Duplication, Backend Smoke Must Exit.

## Prior Step Status
Steps 735-744: PASS individually. Reviewer reports backend smoke hangs because
standalone smoke (--mode all) runs first, then wrapper tests call it again.
Double execution leaves state that prevents second pytest wrapper from exiting.

## Fix
Remove `python3 scripts/remedy_runtime_cli_smoke.py --mode all` from backend
basis smoke. Wrappers already call it internally — no coverage loss.

## Runtime Test Isolation Rule
- Do NOT chain standalone runtime smoke before wrapper pytest files in same script
- Do NOT combine runtime wrapper + helper tests in one pytest process
- Each runtime file runs in its own pytest invocation

Supported verification path:
- `scripts/remedy_pytest.sh tests/cli/test_propose_cli_runtime.py -q`
- `scripts/remedy_pytest.sh tests/cli/test_worker_cli_runtime.py -q`
- `scripts/remedy_pytest.sh tests/cli/test_runtime_helpers.py -q`
- `scripts/remedy_backend_basis_smoke.sh`
- `python3 scripts/remedy_runtime_cli_smoke.py --mode all` (standalone only)

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
| Runtime stability (no-hang) | **100%** — no duplication, isolated invocations, no pipes |
| Ollama via task_execution | **0%** |
| Real test execution | **0%** |
| Rollback/snapshot | **0%** |
| Overnight execution | **0%** |
| UI/dashboard | paused |
