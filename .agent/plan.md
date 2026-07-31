# Plan — F056 Missions: persistent goal, jobs as execution units

## Goal
Give goals that outlive one job a first-class home: a MISSION holds
the persistent goal and links an ordered chain of jobs. Follow-up
jobs are structurally forced to verify the previous state FIRST
(injected verify task, not prompt hope). Missions never auto-create
— explicit human opt-in only (`remedy mission start`, or a
plan-approval payload item defaulting to NO).

## Current Step
R1/R2/R3 all PASS. R4 CLOSURE COMPLETE, handed back: Built State
recorded, preconditions green (integrity passed=true, clean tree,
branch pushed), evidence job 057a2de1dde14778, package
remedy-review-20260731-210415-READY_FOR_REVIEW.zip (READY, first
attempt BLOCKED and recorded), STATUS [x] + README sync landed as
the last content commit, PR open and NOT merged.

## Next Steps
- Reviewer verifies closure (b41a4b53..HEAD) and ends the session
  with the feature-done banner.
- The closure PR merges at the next feature's Open PR Gate.

## Risks
- `mission` CLI group already exists (internal run-loop facade):
  new subcommands join it rather than shadow it.
- Verify-first must be enforced by structure (task injection +
  validator), never by prompt text.
