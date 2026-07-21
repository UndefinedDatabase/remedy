# Plan — F018 Budgets & Stop Conditions (Final Closure)

## Goal
Close 10 blocking reproductions from external review of
remedy-review-20260721-235837-READY_FOR_REVIEW.zip.
Steps 1-10 scope-based closure. One canonical READY_FOR_REVIEW ZIP.

## Status: COMMITTING

## Scope 1 — Clean branch history
- [x] Backup mixed branch, cherry-pick 14 legitimate commits
- [x] Exclude Evidence blobs from git tracking (.gitignore)

## Scope 2 — Strict persisted budget decode
- [x] model_validate failure blocks as corrupt_budget_state (never None)

## Scope 3 — Strict resumed actuals
- [x] Reject bool/float/string/negative for persisted counter fields
- [x] Validate actual_call_count <= provider_call_count

## Scope 4 — BudgetCounters invariants
- [x] Closed source vocabulary (_VALID_SOURCES)
- [x] Measured tokens require measured calls
- [x] Measured calls require sources
- [x] Timezone-aware started_at

## Scope 5 — JobPlan Decision Queue compatibility
- [x] getattr fallback for .metadata and .artifacts on JobPlan
- [x] AttributeError catch in list_patch_intents and derive_stop_reasons

## Scope 6 — Stopped job budget override block
- [x] CLI refuses budget flags on stopped jobs (exit 2, Decision workflow)

## Scope 7 — Real runtime gate
- [x] Replace test-name-existence checks with test_execution_binding checks
- [x] Gate accepts verification_data, binds to executed test records
- [x] Zero-checks guard (empty checks → BLOCKED)
- [x] Gate schema version bumped to 1.1.0
- [x] Evidence pipeline writes gate AFTER verification_tests

## Scope 8 — Verification authority
- [x] All F018 suites pass: 258 tests
- [x] Related suites pass: 389 tests
- [x] Gate + flow suites pass: 260 tests

## Scope 9 — Docs & state updates
- [x] plan.md updated
- [ ] context.md updated
- [ ] live_review.md updated
- [ ] T0_F018.md updated
- [ ] STATUS.md updated

## Scope 10 — Final sequencing
- [ ] Commit all tracked files
- [ ] Confirm clean tree
- [ ] Generate Evidence + ZIP
- [ ] Verify HEAD/hashes/size/members

## Constraints
No Fable/subagents/providers/network/Docker.
Do not amend/squash. Do not push/PR/merge.
F018 [~]. F146 [ ].
