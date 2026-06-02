# Plan — Steps 351-358

## Goal
Event-ledger replay, safe checkpoints, checkpoint resume v1.

## Current Step
All steps complete. Ready for commit + push.

## Steps
- [x] Step 351: Preflight + layout regression guard (5 tests)
- [x] Step 352: Event replay model — reconstruct job progress from events (6 tests)
- [x] Step 353: Safe checkpoint detection — resume-safe boundaries (4 tests)
- [x] Step 354: CLI: event replay, job checkpoints, job resume commands
- [x] Step 355: Resume dry-run (3 tests)
- [x] Step 356: Safe resume v1 — conservative from_approval mode
- [x] Step 357: Dashboard/UI read-only resume visibility (ResumeCard)
- [x] Step 358: Baseline 3916 passed, 7 skipped. Vitest 35. TypeScript clean. Build OK.
