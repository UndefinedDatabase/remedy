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
Resolved). R3 (SPLIT): persist the ledger, then run the integration
gate per docs/agents/integration_gate.md — full suite at HEAD, full
suite at the merge base in a throwaway worktree on a throwaway
branch with UI build-artifact parity, comm comparison, attribution
of every id. This round FIXES nothing: a red gate is a result to
report, and any repair is its own later round.

## Next Steps
- Reviewer issues the R3 gate verdict (1725cc60..HEAD).
- Closure round (STATUS `[x]`, evidence job + fresh review zip, PR)
  — its own round.

## Risks
- `mission` CLI group already exists (internal run-loop facade):
  new subcommands join it rather than shadow it.
- Verify-first must be enforced by structure (task injection +
  validator), never by prompt text.
