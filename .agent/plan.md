# Plan — F056 Missions: persistent goal, jobs as execution units

## Goal
Give goals that outlive one job a first-class home: a MISSION holds
the persistent goal and links an ordered chain of jobs. Follow-up
jobs are structurally forced to verify the previous state FIRST
(injected verify task, not prompt hope). Missions never auto-create
— explicit human opt-in only (`remedy mission start`, or a
plan-approval payload item defaulting to NO).

## Current Step
R1/R2/R3 all PASS; R3 carries the INTEGRATION GATE PASS and the
full-suite claim (LAST_REVIEWED_SHA b41a4b53). R4 (SPLIT closure)
per docs/roadmap/STATUS_closure_protocol.md v4: ledger → Built
State → preconditions (integrity check, clean tree, push) →
evidence job (feature-scoped f056) → fresh review zip → closure
commit (STATUS [x] + README sync + final .agent state) → PR.
No merge: the PR merges at the next feature's Open PR Gate.

## Next Steps
- Reviewer verifies closure (b41a4b53..HEAD) and ends the session
  with the feature-done banner.
- The closure PR merges at the next feature's Open PR Gate.

## Risks
- `mission` CLI group already exists (internal run-loop facade):
  new subcommands join it rather than shadow it.
- Verify-first must be enforced by structure (task injection +
  validator), never by prompt text.
