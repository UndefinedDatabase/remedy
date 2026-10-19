# Plan — release readiness of PR 360-365 (operator order rel-1019, 2026-10-19)

## Goal
Make the stacked release (#360 → #361 → #362 → #363 → #364 → #365) a reviewed, deployable,
dependable release: recover the newest handback, re-verify the stack independently, fix only
reproduced defects in one dependent PR, and hand over one German release handoff. Branch
`feature/release-readiness` from PR 365's head `7181a2311`; worktree `.remedy-wt/release-readiness`.
No merge, no deploy; `.agent/STOP`, supervisor, live checkout and `.data` untouched. Outside the
roadmap queue: F078 stays next.

## Current Step
6. Handoff, then the full local gate once on the final commit, then the PR (not merged).
   Done: 1. handback recovered, ZIP diagnosed (D1); 2. R-1365 (D2); 3. R-1366 (D3); 4. R-1367 (D4);
   5. measurements: one real run, live jobs read-only, scale matrix, ZIP with a real report (D5).

## Next Steps
- Operator: review PRs 360-365 and this one; merge in order; deploy per handoff section 12.

## Risks
- Workstation shared with Universe: one pytest tree at a time, `-n 6` at most.
