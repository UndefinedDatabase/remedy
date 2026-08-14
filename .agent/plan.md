# Plan — F077 Autonomy watchdog

Branch: feature/f077-autonomy-watchdog, cut from main after the F057 closure
PR #199 merged. F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free
finding id: R-0383. Open findings: seventeen — the fourteen carried from F057
(R-0361, R-0362, R-0363, R-0364, R-0367, R-0368, R-0369, R-0371, R-0374,
R-0375, R-0376, R-0377, R-0378, R-0379) plus R-0380, R-0381 and R-0382.
`.agent/live_review.md` is the source of truth for this ledger; this file
mirrors it and nothing else.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger, postmortems and actuals, and on
no-progress repetition, a burn-rate anomaly or goal drift it PAUSES the mission
and raises one decision per trip class carrying the evidence triple. It stops;
it never repairs. Thresholds live in config, not code.

## Current Step
R2 is done: the R1 verdict and R-0382 are on the record, and the T001 inventory
is in `.agent/f077_inventory.md`. Headline — Q2: `run_mission` re-evaluates the
`mission.status != MISSION_STATUS_ACTIVE` guard on EVERY iteration from a
record re-read by `load_mission`, so T002's pause acceptance already holds and
needs no loop prerequisite (but that path writes no ledger entry and builds no
boundary handoff). Q3: no milestone field exists on the job or on
`MissionJobLink` — the attribution lives only in the loop's ledger, as
`move.payload.milestone_id` beside `outcome.job_id` on `dispatch_job` entries
(`dispatched_job_for`), which makes goal_drift buildable as specified.

## Next Steps
1. R3 — T001 the three evaluators as pure functions over fixture ledgers, with
   unit tests per tripwire (fires / just-under-threshold does not). Settle the
   nine open questions listed at the end of the inventory first.
2. R4 — T002 pause, decision, dedup, ledger entry, loop-integration test.
3. R5 — T003 the manual CLI and the report surface.
4. R6 — integration gate and closure.

## Risks
- The inventory contradicts the feature file on one point: T2_F077 asserts
  "every loop-dispatched job carries its milestone link", which is false as a
  field on the job. R3 must build goal_drift off the ledger, not off the job.
- Seventeen open findings is the largest carry any feature has started with.
