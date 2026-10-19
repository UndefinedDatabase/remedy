# Plan — release readiness of PR 360-365 (operator order rel-1019, 2026-10-19)

## Goal
Make the stacked release (#360 → #361 → #362 → #363 → #364 → #365) a reviewed, deployable,
dependable release: recover the newest handback, re-verify the stack independently, fix only
reproduced defects in one dependent PR, and hand over one German release handoff. Branch
`feature/release-readiness` from PR 365's head `7181a2311`; worktree `.remedy-wt/release-readiness`.
No merge, no deploy; `.agent/STOP`, supervisor, live checkout and `.data` untouched. Outside the
roadmap queue: F078 stays next.

## Current Step
3. R-1366 repaired (D3): a rejected plan offers no `run`; plan approval rows in the lifecycle matrix.
   Done: 1. handback recovered, ZIP diagnosed (D1); 2. R-1365 pending cancel of a dead runner (D2).

## Next Steps
- 3b. Repair owners re-run independently (real `node --test` scenarios).
- 4. Scale matrix and real-model evidence: read, not re-run, unless the load allows.
- 5. Review-report ZIP: a captured disposable HTTP order through the ordinary no-argument export.
- 6. Full local gate once on the final commit; handoff; PR (not merged).

## Risks
- Workstation shared with Universe: one pytest tree at a time, `-n 6` at most.
