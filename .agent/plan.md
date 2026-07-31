# Plan — F056 Missions: persistent goal, jobs as execution units

## Goal
Give goals that outlive one job a first-class home: a MISSION holds
the persistent goal and links an ordered chain of jobs. Follow-up
jobs are structurally forced to verify the previous state FIRST
(injected verify task, not prompt hope). Missions never auto-create
— explicit human opt-in only (`remedy mission start`, or a
plan-approval payload item defaulting to NO).

## Current Step
R1 PASS (78f5f608..e8c3c147). R2 (SPLIT): persist the ledger, then
fix R-0163 — amend the feature file's CLI line (authored bytes) and
add the status-transition surface `remedy mission
achieve/abandon/pause` as thin wrappers over set_mission_status.
No new transition rules; mission_state.py itself needs no change.

## Next Steps
- Reviewer gates R2 (e8c3c147..HEAD).
- Integration-gate round, then closure (STATUS `[x]`, evidence
  zip) — each its own later round.

## Risks
- `mission` CLI group already exists (internal run-loop facade):
  new subcommands join it rather than shadow it.
- Verify-first must be enforced by structure (task injection +
  validator), never by prompt text.
