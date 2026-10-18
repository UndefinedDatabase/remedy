# Plan — release-candidate verification of PR 360-364 (operator order exec-1018c, 2026-10-18)

## Goal
Verify the stacked release (#360 → #361 → #362 → #363 → #364) as one production change, fix only
real remaining defects in a dependent PR, and hand over one release-candidate report. Branch
`feature/release-candidate-verify` from PR 364's head `eb439f9fb`; worktree `.remedy-wt/rc-verify`.
No merge, no deploy; `.agent/STOP`, supervisor, live checkout and `.data` untouched.

## Current Step
7. P1 sections 8 (providers, security) and 9 (lessons); then the full gate, handoff and PR.
   Done: R-1361..R-1364, lifecycle matrix (15 rows over HTTP), API matrix 1.17-1.21 (D5),
   builder targeting from the task's words (D6, replayed on real prompts, turns unmeasured).

## Next Steps
- One full local gate on the final commit; release handoff (13 sections); dependent PR.

## Risks
- Workstation shared with Universe: one pytest tree at a time, `-n 4` for focused runs.
