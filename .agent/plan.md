# Plan — F056 Missions: persistent goal, jobs as execution units

## Goal
Give goals that outlive one job a first-class home: a MISSION holds
the persistent goal and links an ordered chain of jobs. Follow-up
jobs are structurally forced to verify the previous state FIRST
(injected verify task, not prompt hope). Missions never auto-create
— explicit human opt-in only (`remedy mission start`, or a
plan-approval payload item defaulting to NO).

## Current Step
R1 (LARGE, SPLIT round): T001 mission record + store + link /
list / show + unit tests → T002 intake mission-candidate hint +
approval opt-in (default NO) → T003 `mission continue` + injected
verify-first task + two-job fixture end-to-end. Per-slice gates,
stop-on-red.

## Next Steps
- Reviewer gates R1; repair rounds as found.
- Closure (STATUS `[x]`, evidence zip) is its own later round.

## Risks
- `mission` CLI group already exists (internal run-loop facade):
  new subcommands join it rather than shadow it.
- Verify-first must be enforced by structure (task injection +
  validator), never by prompt text.
