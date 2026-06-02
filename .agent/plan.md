# Plan — Steps 359-366

## Goal
Resume truth closure: no no-op resume claims, honest blocking.

## Current Step
All steps complete. Ready for commit + push.

## Steps
- [x] Step 359: R-12001 preflight + regression tests (2 tests)
- [x] Step 360: Checkpoint semantics — context_ready inspectable, from_approval blocked (missing_patch_payload)
- [x] Step 361: from_approval blocked honestly (no fake run_autorun)
- [x] Step 362: from_apply real test-runner resume implemented
- [x] Step 363: from_test_failure blocked (resume_mode_not_implemented)
- [x] Step 364: Dry-run accuracy — matches new semantics
- [x] Step 365: CLI/UI resume truth — unimplemented modes say blocked not resumed
- [x] Step 366: Baseline 3922 passed, 7 skipped. Vitest 35. TypeScript clean. Build OK.
