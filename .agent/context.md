# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 735-744: Combined Pytest Exit Fix, Backend Smoke Must Exit.

## Prior Step Status
Steps 725-734: PASS individually (propose 0.71s, worker 0.87s, smoke 2.86s).
Reviewer reports: combined pytest of runtime files + helper still hangs after "8 passed".
Backend smoke hangs because it bundles runtime files in one pytest command.

## Fix Strategy
1. Remove capture_output=True from thin wrappers → Popen + temp files
2. Split smoke into separate pytest invocations (runtime files isolated)
3. Document: "Do not combine runtime wrapper + helper tests in one pytest process"

## Runtime Test Isolation Rule
Do NOT combine runtime wrapper tests and runtime helper tests in one pytest
process. Each must run in its own pytest invocation. The backend smoke script
enforces this by running separate `scripts/remedy_pytest.sh` calls per file.

Supported verification path:
- `scripts/remedy_runtime_cli_smoke.py --mode all` (standalone)
- `scripts/remedy_pytest.sh tests/cli/test_propose_cli_runtime.py -q`
- `scripts/remedy_pytest.sh tests/cli/test_worker_cli_runtime.py -q`
- `scripts/remedy_pytest.sh tests/cli/test_runtime_helpers.py -q`
- `scripts/remedy_backend_basis_smoke.sh`

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
| Runtime stability (no-hang) | **100%** — isolated invocations + no pipes + standalone smoke |
| Ollama via task_execution | **0%** |
| Real test execution | **0%** |
| Rollback/snapshot | **0%** |
| Overnight execution | **0%** |
| UI/dashboard | paused |
