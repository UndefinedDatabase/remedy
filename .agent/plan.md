# Plan — Steps 147-154

## Goal
Blocker/advisory split, repair context, repair loop, reviewer recommendations,
memory candidates, live UI v2, UX polish.

## Current Step
All steps complete. Final commit.

## Steps
- [x] Step 147: Dev status blocker/advisory split — crash=blocker, not-ready=advisory
- [x] Step 148: Commit-readiness can return ready=true for fixture job
- [x] Step 149: Repair context v1 — safe failure summary, no raw stdout/stderr
- [x] Step 150: Deterministic repair loop E2E — 2-cycle fixture via --fixture-builder repair-loop
- [x] Step 151: Reviewer recommendation v1 — fixture reviewer, accept/reject, no auto-append
- [x] Step 152: Memory candidate v1 — human approval required, deduplication
- [x] Step 153: Live run UI v2 — repair_loop_used, reviewer_pending_count, memory_candidate_count
- [x] Step 154: UX polish gate — task ribbon, reduced-motion, next-action, no metadata wall

## Tests
- 32 new tests in test_steps_147_154.py
- 3313 total tests passing
- Frontend builds clean (Vite)
