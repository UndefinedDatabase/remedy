# Plan — F056 Missions: persistent goal, jobs as execution units

## Goal
Give goals that outlive one job a first-class home: a MISSION holds
the persistent goal and links an ordered chain of jobs. Follow-up
jobs are structurally forced to verify the previous state FIRST
(injected verify task, not prompt hope). Missions never auto-create
— explicit human opt-in only (`remedy mission start`, or a
plan-approval payload item defaulting to NO).

## Current Step
R1 (LARGE, SPLIT round) COMPLETE, handed back: T001 record + store
+ link/list/show, T002 intake hint + approval opt-in (default NO),
T003 `mission continue` + injected verify-first + the two-job
fixture end-to-end. Every slice gate, the canary, the docs gate and
the full suite green; tree clean; nothing pushed.

## Next Steps
- Reviewer gates R1 (78f5f608..HEAD); repair rounds as found.
- Closure (STATUS `[x]`, evidence zip) is its own later round.

## Risks
- `mission` CLI group already exists (internal run-loop facade):
  new subcommands join it rather than shadow it.
- Verify-first must be enforced by structure (task injection +
  validator), never by prompt text.
