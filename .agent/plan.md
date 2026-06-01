# Plan — Steps 297-304

## Goal
Post-rearchitecture polish, source apply cleanup, project memory into planning/execution.

## Current Step
All steps complete. Ready for commit + push.

## Steps
- [x] Step 297: Rename 97 step-numbered test classes to descriptive invariant names
- [x] Step 298: Consolidate _rollback/revert_apply, surface rollback errors (R-6007/R-6008)
- [x] Step 299: Define MemoryContextSummary contract — approved-only, bounded, redacted
- [x] Step 300: Feed approved memory into planner prompt with safe metadata
- [x] Step 301: Feed approved memory into TaskExecutionContext with safe metadata
- [x] Step 302: Emit project_memory_recalled events, add memory_used_count to dashboard
- [x] Step 303: 14 memory safety/regression tests — no leaks, no fake nodes
- [x] Step 304: Full baseline 3727 passed, 1 skipped. Vitest 21 passed. TypeScript clean. Build OK.
