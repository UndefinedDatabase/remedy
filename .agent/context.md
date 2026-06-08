# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 785-794: Final Smoke Decoupling.

## Prior Step Status
Steps 775-784: PASS — Python supervisors replace Bash chaining. But backend
smoke still mixes standalone runtime smoke with runtime helper self-tests in
same supervisor chain. Helper tests are toxic when chained with runtime smoke.

## Fix
Remove helper tests from backend smoke. Three separate smoke surfaces:
1. Backend basis: standalone runtime + orchestration/storage
2. Runtime wrapper: propose + worker wrappers
3. Process isolation: helper tests + smoke contract tests + runner tests

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
| Runtime stability (no-hang) | **100%** — three separate smoke surfaces, all exit clean |
| Ollama via task_execution | **0%** |
| Real test execution | **0%** |
| Rollback/snapshot | **0%** |
| Overnight execution | **0%** |
| UI/dashboard | paused |
