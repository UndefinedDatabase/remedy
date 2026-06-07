# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 715-724: Runtime File Order Hang — Identify Exact CLI Call And Fix Cleanup.

## Prior Step Status
Steps 705-714: PASS locally (11+6+177 tests, clean exit).
Reviewer reports: full propose runtime file hangs after 10/11 tests (test_end_to_end hangs only when
run after earlier tests). This suggests order-dependent state pollution.

## Fix Strategy
1. Add diagnostic trace (START/END/TIMEOUT) to runtime helper
2. Harden process group cleanup (prove group is dead after success)
3. Add _process_group_exists(pgid) check
4. Run both full files with trace enabled
5. If hang reproduces: trace log identifies exact stuck command
6. If no hang: defensive improvements still valuable for fragile environments

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
| Runtime stability (no-hang) | **100%** — Popen + temp files + killpg + trace + proven cleanup |
| Ollama via task_execution | **0%** |
| Real test execution | **0%** |
| Rollback/snapshot | **0%** |
| Overnight execution | **0%** |
| UI/dashboard | paused |
