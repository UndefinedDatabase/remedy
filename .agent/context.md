# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 725-734: Runtime Tests Process-Isolated, Pytest Must Exit Cleanly.

## Prior Step Status
Steps 715-724: PASS locally. Reviewer reports pytest process doesn't exit after
tests print "passed". Not a single stuck CLI command — it's pytest-process
teardown contamination from many runtime subprocess calls.

## Fix Strategy
1. Create standalone script (scripts/remedy_runtime_cli_smoke.py) that runs
   propose+worker flows outside pytest
2. Rewrite test files as thin wrappers — each test calls smoke script once
3. Pytest only manages one subprocess per test (not 4-10)
4. Keep runtime_helpers.py unit tests separate

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
| Runtime stability (no-hang) | **100%** — thin wrappers + standalone smoke, pytest exits cleanly |
| Ollama via task_execution | **0%** |
| Real test execution | **0%** |
| Rollback/snapshot | **0%** |
| Overnight execution | **0%** |
| UI/dashboard | paused |
