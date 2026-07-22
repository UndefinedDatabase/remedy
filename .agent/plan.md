# Plan — F018 Budgets & Stop Conditions (Evidence Integrity Closure)

## Goal
Close 10 exact blocking reproductions from the reviewed BLOCKED_EVIDENCE
package. Fix truthful Verification V1.1 producer, generic Manual Completion
compatibility, strict persisted Actuals and first_running_at, honest budget
display, exact Runtime Gate critical bindings, single-Evidence packaging,
truthful terminal handoff. One canonical ZIP from F017 merge base
190b3528a2dada6a27fdd9c2fdb75a6a00e7ea43.

## Status: COMMITTING

## Scope 1 — Unified truthful Verification V1.1
- [x] _run_verifications: schema_version "1.1.0" (was "1.0.0" with V1.1 fields)
- [x] _run_verifications: add duration_seconds (monotonic) and deselected to runs
- [x] _default_verification_runner: capture duration, emit deselected
- [x] Normalize injected runner output: derive missing V1.1 fields safely
- [x] Generic Manual Completion: fix 4 failing tests through production compat
- [x] VT cross-consistency: selected derived from node_ids or p+f+s

## Scope 2 — Strict persisted Actuals and first-running authority
- [x] Persisted actuals: require schema_version == "1.0.0" (missing/unknown blocks)
- [x] Persisted actuals: require actual_sources when actual_call_count > 0
- [x] first_running_at: invalid text blocks (not silently becomes now())
- [x] first_running_at: timezone-naive blocks
- [x] Corrupt state reaches no workspace, provider or mutation
- [x] Tests for each strict guard (3 new classes, 9 tests)

## Scope 3 — Honest budget display and exact Runtime bindings
- [x] _cmd_job_budget: pass real persisted actual_sources (not "persisted_job_actuals")
- [x] _cmd_job_budget: corrupt record → status "corrupt" with diagnostic
- [x] Runtime Gate: bind strongest test_run_job_rejects_budget_on_stopped
- [x] Runtime Gate: add critical bindings for strict behaviors (3 new nodes)

## Scope 4 — Clean single-Evidence package contents
- [x] make_review_zip.sh: exclude .agent/Evidence/ from find walk

## Scope 5 — Tests, truthful docs, final canonical ZIP
- [x] Run complete test matrix: 513 passed in 8 suites
- [x] Update STATUS.md, T0_F018.md, context.md, live_review.md
- [ ] Commit all tracked files
- [ ] Fresh Evidence from base 190b3528
- [ ] One make_review_zip.sh invocation
- [ ] No post-ZIP commit

## Constraints
No Fable/subagents/providers/network/Docker.
Do not amend/squash. Do not push/PR/merge.
F018 [~]. F146 [ ].
