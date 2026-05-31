# Plan — Steps 247-252

## Goal
Data-Honest Mission Control Contract: remove fake UI state, create truth contract.

## Current Step
All steps complete. Ready to commit.

## Steps
- [x] Step 247: Repo + handoff truth hygiene (context.md, plan.md, PR gate)
- [x] Step 248: Dashboard truth contract v1 (source_kind, synthetic_count, demo_mode)
- [x] Step 249: No-fake UI state pass (remove DISPLAY_ROWS, honest empty states)
- [x] Step 250: Real graph source contract (source_kind on nodes)
- [x] Step 251: Event ledger → live activity (derive from run-log)
- [x] Step 252: Operator summary + smoke alignment (CLI + tests)

## Test Results
- 148 tests passed (test_steps_172_201 + test_steps_208_226 + test_steps_247_252), 0 failed
- TypeScript: clean (no errors)
- Build: 1.80s, 515 kB JS, 15 kB CSS
