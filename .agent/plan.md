# Plan — F056 Missions: persistent goal, jobs as execution units

## Goal
Give goals that outlive one job a first-class home: a MISSION holds
the persistent goal and links an ordered chain of jobs. Follow-up
jobs are structurally forced to verify the previous state FIRST
(injected verify task, not prompt hope). Missions never auto-create
— explicit human opt-in only (`remedy mission start`, or a
plan-approval payload item defaulting to NO).

## Current Step
R1 PASS (78f5f608..e8c3c147), R2 PASS (e8c3c147..1725cc60, R-0163
Resolved). R3 COMPLETE, handed back: integration gate run per
docs/agents/integration_gate.md. Branch 14744 passed exit 0 with
zero FAILED; base at 78f5f608 in a throwaway worktree with UI
artifact parity; comm -13 EMPTY, every comm -23 id attributed to
the environment class and shown non-reproducible. No repair was
indicated and none was done. Evidence in .agent/gate_f056_r3/.

## Next Steps
- Reviewer issues the R3 gate verdict (1725cc60..HEAD).
- Closure round (STATUS `[x]`, evidence job + fresh review zip, PR)
  — its own round.

## Risks
- `mission` CLI group already exists (internal run-loop facade):
  new subcommands join it rather than shadow it.
- Verify-first must be enforced by structure (task injection +
  validator), never by prompt text.
