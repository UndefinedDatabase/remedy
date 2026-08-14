# Plan — F077 Autonomy watchdog

Branch: feature/f077-autonomy-watchdog, cut from main after the F057 closure
PR #199 merged. F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free
finding id: R-0386. Open findings: EIGHTEEN — R-0361, R-0362, R-0363,
R-0364, R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377,
R-0378, R-0379, R-0380, R-0381, R-0382, R-0385 — the eighteen carried into
R8, minus R-0384 which the R7 verdict resolves, plus R-0385 which it
registers. The R8 block predicted seventeen; the set recomputed mechanically
from the record is EIGHTEEN and is reported unadjusted.
`.agent/live_review.md` is the source of truth for this ledger; this file
mirrors it and nothing else.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger, postmortems and actuals, and on
no-progress repetition, a burn-rate anomaly or goal drift it PAUSES the mission
and raises one decision per trip class carrying the evidence triple. It stops;
it never repairs. Thresholds live in config, not code.

## Current Step
R8 — T002's action. `act_on_trips` in `packages/orchestration/watchdog.py`
is the pause, the deduped decision and the `watchdog_tripped` ledger entry,
built exactly as DECISIONS F077 D1-D8 settle them, with twelve new unit
tests beside the thirteen T001 ones.

The action ships UNWIRED (D8): `orchestrator_loop.py` neither imports it nor
calls it. This round's green gate therefore proves the action correct in
isolation and proves NOTHING about the loop.

## Next Steps
1. R9 — wire the action into the loop's iteration seam, pay the four
   whole-ledger guards in `tests/orchestration/test_mission_e2e.py` that a new
   entry kind breaks, and add the loop-integration test.
2. R10 — T003 the manual CLI including the missing `mission resume` verb (D4)
   and the report surface.
3. R11 — integration gate, then closure.

## Risks
- The F077 feature file asserts "every loop-dispatched job carries its
  milestone link", which is false as a field on the job or on
  `MissionJobLink`. T001 therefore builds goal_drift off the ledger's
  `move.payload.milestone_id`, not off the job.
- DECISION F077 D7 says R8 adds the watchdog clause to the three repaired
  docstrings; the R8 block's Change line forbids touching those files. The
  block was followed and the clause is deferred — R9 owns it, in the round
  that gives the watchdog a caller.
- Eighteen open findings is the largest carry any feature has held.
