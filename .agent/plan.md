# Plan — release-candidate verification of PR 360-364 (operator order exec-1018c, 2026-10-18)

## Goal
Verify the stacked release (#360 → #361 → #362 → #363 → #364) as one production change, fix only
real remaining defects in a dependent PR, and hand over one release-candidate report. Branch
`feature/release-candidate-verify` from PR 364's head `eb439f9fb`; worktree `.remedy-wt/rc-verify`.
No merge, no deploy; `.agent/STOP`, supervisor, live checkout and `.data` untouched.

## Current Step
1. Lifecycle: every state's offered `end`/`next` taken through the real public API dispatch
   (R-1361 repaired: abandon of a job a dead walk left running).

## Next Steps
2. Lifecycle matrix integration test over HTTP + real CommandRunner (12 states, two clients).
3. Repair (#363): scope, budget, cancel, identical failures, infra vs test failure.
4. Review-report capture and ZIP export end to end; Universe contract.
5. API 1.17 → 1.21 compatibility matrix (machine-checkable).
6. P1 measurements from recorded evidence only (no live data root).
7. One full local gate on the final commit; release handoff; PR.

## Risks
- Workstation shared with Universe: one pytest tree at a time, `-n 4` for focused runs.
