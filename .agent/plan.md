# Plan — F018 Budgets & Stop Conditions (Final Acceptance Closure)

## Goal
Close 9 exact reproductions from the reviewed package. Fix authoritative
stopped-job override, closed Actuals sources, Verification V1.1 with full
fields, reproducible Runtime Gate, always-rebuild refresh, manifest HEAD
cross-check, privacy-safe report, full F018 base, truthful docs. One
canonical ZIP from accepted F017 merge base.

## Status: IMPLEMENTING — tests pass, docs updated, pending commit + Evidence + ZIP

## Scope 1 — Authoritative stopped-job and Actuals contracts
- [x] run_job: reject budget replacement on stopped jobs (not just CLI)
- [x] Actuals: preserve original measurement sources across resume
- [x] Actuals: remove "persisted_resume" from emitted sources
- [x] Actuals: validate source vocabulary in persisted actuals decoder
- [x] Tests: direct run_job override blocked, persisted budget unchanged,
      invalid source rejected, sources survive two resumes

## Scope 2 — Verification V1.1 and reproducible runtime gate
- [x] VT schema 1.1.0: retain all fields (head_sha, output_hash, selected,
      deselected, skipped, node_ids, duration_seconds)
- [x] Do not strip fields in manual_attestation.py
- [x] Timestamp from real generated time, not hardcoded
- [x] Runtime Gate reproducible from packaged VT + source
- [x] Add critical node bindings for key behaviors
- [x] Tests: VT v1.1 roundtrip, gate rebuild from packaged inputs

## Scope 3 — Staged refresh, privacy and final-HEAD enforcement
- [x] Refresh: always rebuild gate and compare, never trust existing PASS
- [x] Refresh: redact absolute paths from report
- [x] Manifest: validate bound_run.head_sha == Review Subject HEAD
- [x] Manifest: validate output_hash sha256 syntax
- [x] Tests: stale v1.1 wrong HEAD, privacy scan, HEAD mismatch

## Scope 4 — Full-feature review scope and real E2E tests
- [x] Run complete test matrix per scope 10
- [x] New tests for each reproduction (22 new authority tests)
- [ ] Evidence base: 190b3528a2dada6a27fdd9c2fdb75a6a00e7ea43

## Scope 5 — Truthful docs, final Evidence and one newest authoritative ZIP
- [x] Fix "8067 full suite passing" claim (report failures truthfully)
- [x] Update STATUS.md, T0_F018.md, plan.md
- [ ] Commit all tracked files
- [ ] Fresh Evidence from F017 merge base
- [ ] One make_review_zip.sh invocation
- [ ] No post-ZIP commit

## Constraints
No Fable/subagents/providers/network/Docker.
Do not amend/squash. Do not push/PR/merge.
F018 [~]. F146 [ ].
