# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 670-684: Backend Basis Hardening Final.
UI/design work is PAUSED.

## Canonical Review File
`.agent/live_review.md` — NOT `.data/live_review.md`

## Backend Component Status — Post Steps 670-684
| Component | Status | Evidence |
|-----------|--------|----------|
| Proposed task lifecycle | **100%** | 95+ tests, subprocess CLI |
| Materialization into Job.tasks | **100%** | do_materialize proven E2E |
| Fixture task execution | **100%** | BudgetGate, events, persistence |
| Worker one-task execution | **100%** | Budget enforced, started+completed events |
| Execution events | **100%** | started + completed/blocked, proposed_task_id linked |
| Queue/finalize gates | **100%** | blocks unresolved, not-materialized, corrupt, blocked |
| Modular architecture (Baukasten) | **100%** | 10+ guard tests |
| Worker CLI subprocess | **100%** | 6 runtime tests incl budget args |
| Propose CLI subprocess | **100%** | 11 runtime tests, shared helper |
| Backend readiness v3 | **100%** | execution_health, list_jobs_safe, structured |
| Lock timeout/busy | **100%** | test_lock_timeout_on_busy, test_lock_released_on_exception |
| Single-load read-modify-write | **100%** | approve/reject/defer single load in lock |
| Budget CLI args | **100%** | --max-steps, --max-tokens, --max-runtime-seconds |
| Smoke script | **100%** | scripts/remedy_backend_basis_smoke.sh |
| Ollama via task_execution | **0%** | legacy autorun path |
| Real test execution | **0%** | no test discovery |
| Rollback/snapshot | **0%** | |
| Overnight execution | **0%** | gate always returns not ready |
| UI/dashboard | paused | |
| Dashboard reconcile | **not started** | R-610-002, UI paused |

## Do Not Reopen Without Evidence
Components marked 100% above are considered closed. To reopen:
- Must have a failing test or reproducible bug
- Must not be "I think it could be better" without regression evidence
- Runtime CLI file hang in different environment → fix in that environment's tests

## Definition of Regression
A component regresses if: existing test fails, or new test reveals persisted-state corruption, or subprocess CLI returns non-zero where it was zero.

## Resource Safety
All pytest runs use scripts/remedy_pytest.sh (flock + timeout).
