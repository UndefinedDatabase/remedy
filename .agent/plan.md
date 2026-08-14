# Plan — F077 Autonomy watchdog

Branch: feature/f077-autonomy-watchdog, cut from main after the F057 closure
PR #199 merged. F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free
finding id: R-0385. Open findings: eighteen — R-0361, R-0362, R-0363,
R-0364, R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377,
R-0378, R-0379, R-0380, R-0381, R-0382, R-0384 — the nineteen carried minus
R-0383, which the R6 verdict resolves. R-0384 only LANDS this round and
stays open. `.agent/live_review.md` is the source of truth for this ledger;
this file mirrors it and nothing else.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger, postmortems and actuals, and on
no-progress repetition, a burn-rate anomaly or goal drift it PAUSES the mission
and raises one decision per trip class carrying the evidence triple. It stops;
it never repairs. Thresholds live in config, not code.

## Current Step
R7 — record the R6 verdict, resolve R-0383, settle the eight T002 questions as
DECISIONS F077 D1-D8, and repair R-0384's three stale docstrings.

T002's code is NOT built this round. The eight questions the T002 inventory
left open each had a shape consequence, and building before settling them is
how a round discovers a schema decision halfway through. D1-D8 settle them.

## Next Steps
1. R8 — T002 the code D1-D8 unblock: the pause, the deduped decision, the
   `watchdog_tripped` ledger entry and the unit tests, as a callable action in
   `watchdog.py` NOT yet wired into `run_mission`.
2. R9 — wire the watchdog into the loop's iteration seam, pay the four
   whole-ledger guards in `tests/orchestration/test_mission_e2e.py` that a new
   entry kind breaks, and add the loop-integration test.
3. R10 — T003 the manual CLI including the missing `mission resume` verb (D4)
   and the report surface. R11 — integration gate, then closure.

## Risks
- The F077 feature file asserts "every loop-dispatched job carries its
  milestone link", which is false as a field on the job or on
  `MissionJobLink`. T001 therefore builds goal_drift off the ledger's
  `move.payload.milestone_id`, not off the job.
- Eighteen open findings is the largest carry any feature has held.
