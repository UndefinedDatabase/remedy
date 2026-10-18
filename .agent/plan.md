# Plan — release-candidate verification of PR 360-364 (operator order exec-1018c, 2026-10-18)

## Goal
Verify the stacked release (#360 → #361 → #362 → #363 → #364) as one production change, fix only
real remaining defects in a dependent PR, and hand over one release-candidate report. Branch
`feature/release-candidate-verify` from PR 364's head `eb439f9fb`; worktree `.remedy-wt/rc-verify`.
No merge, no deploy; `.agent/STOP`, supervisor, live checkout and `.data` untouched. Outside the
roadmap queue: F078 stays next.

## Current Step
8. Full local gate on the final commit, then the PR (result in its body). Handoff written.
   Done: R-1361..R-1364, lifecycle matrix (15 rows over HTTP), API matrix 1.17-1.21 (D5),
   builder targeting from the task's words (D6, replayed on real prompts, turns unmeasured).

## Next Steps
- Operator: review with 360-364, merge 360 → 361 → 362 → 363 → 364 → this; deploy per handoff 12.

## Risks
- Workstation shared with Universe: one pytest tree at a time, `-n 4` for focused runs.
