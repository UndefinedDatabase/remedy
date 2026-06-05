# Plan — Steps 670-684: Backend Basis Hardening Final

## Goal
Runtime no-hang, budget CLI, execution_health, lock tests, clean handoff.

## Current Step
684 — Final baseline

## Steps
- [x] 670: Handoff — risks, plan
- [x] 671: Shared subprocess helper (tests/cli/runtime_helpers.py)
- [x] 672: Propose runtime refactored to use helper
- [x] 673: Worker runtime refactored to use helper + budget test
- [x] 674: Performance bounds via timeout in helper
- [x] 675: Worker CLI budget args (--max-steps, --max-tokens, --max-runtime-seconds)
- [x] 676: execution_health section in backend_readiness
- [x] 677: list_jobs_safe consumed by backend_readiness
- [x] 678: Lock timeout/busy test (test_lock_timeout_on_busy)
- [x] 679: Double-load-in-lock cleanup — approve/reject/defer single load
- [x] 680: Worker lease cleanup on budget block (release_lease before return)
- [x] 681: Worker loop uses max_steps through once path
- [x] 682: Backend basis smoke script
- [x] 683: Completion table with freeze rules
- [x] 684: Full baseline: 4432 passed, 0 failed, 8 skipped

## Review Findings Resolved
- R-640-003 (list_jobs_safe unused) → backend_readiness calls list_jobs_safe
- R-640-004 (no execution_health) → added section
- R-595-003 (no lock timeout test) → test_lock_timeout_on_busy
- R-595-005 (double-load in lock) → single-load approve/reject/defer
- R-655-001, R-655-002 → same as above
- Lock fd double-close bug fixed in _file_lock timeout path
