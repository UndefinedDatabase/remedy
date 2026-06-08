# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 775-784: Backend Smoke Python Supervisor.

## Prior Step Status
Steps 765-774: PASS — pipe-safe pytest runner created. But backend smoke
still hangs in reviewer env because Bash script chains process-heavy phases
in one shell process. Inherited fds/process state from one phase leak into next.

## Fix
Replace Bash chaining with Python supervisor. Each phase runs via isolated
Popen (start_new_session + temp files + killpg). Shell script becomes thin
wrapper that calls Python supervisor.

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
| Runtime stability (no-hang) | **100%** — Python supervisor, all smoke exits clean |
| Ollama via task_execution | **0%** |
| Real test execution | **0%** |
| Rollback/snapshot | **0%** |
| Overnight execution | **0%** |
| UI/dashboard | paused |
