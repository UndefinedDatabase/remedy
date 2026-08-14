# Plan — F077 Autonomy watchdog

Branch: feature/f077-autonomy-watchdog, cut from main after the F057 closure
PR #199 merged. F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free
finding id: R-0387. Open findings: NINETEEN — R-0361, R-0362, R-0363,
R-0364, R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377,
R-0378, R-0379, R-0380, R-0381, R-0382, R-0385, R-0386 — the eighteen carried
into R9 plus R-0386, which the R8 verdict registers against the reviewer.
Recomputed mechanically from the record: 21 registered, 2 resolved (R-0383,
R-0384), 19 open. `.agent/live_review.md` is the source of truth for this
ledger; this file mirrors it and nothing else.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger, postmortems and actuals, and on
no-progress repetition, a burn-rate anomaly or goal drift it PAUSES the mission
and raises one decision per trip class carrying the evidence triple. It stops;
it never repairs. Thresholds live in config, not code.

## Current Step
R9 — state only. Record the R8 verdict (PASS), register R-0386 against the
reviewer, and close the session with a handoff a cold session can start from.
No code this round; T002's wiring is R10's work and is NOT started here.

T002's action `act_on_trips` landed in R8 and is still UNWIRED (D8):
`orchestrator_loop.py` neither imports nor calls it, so nothing in a running
mission reaches it and the R8 PASS says nothing about the loop.

## Next Steps
1. R10 — wire `act_on_trips` into `run_mission`'s iteration seam, pay the four
   whole-ledger guards in `tests/orchestration/test_mission_e2e.py`, and write
   DECISION F077 D7's watchdog clause into the `set_mission_status` and
   `_cmd_mission_set_status` docstrings in the same commit as the call site.
2. R11 — T003 the manual CLI including the missing `mission resume` verb (D4)
   and the report surface.
3. R12 — integration gate, then closure.

## Risks
- The F077 feature file asserts "every loop-dispatched job carries its
  milestone link", which is false as a field on the job or on
  `MissionJobLink`. T001 therefore builds goal_drift off the ledger's
  `move.payload.milestone_id`, not off the job.
- DECISION F077 D7's watchdog clause is still unwritten: the R8 block's Change
  line forbade the files it names. R10 owns it, in the round that gives the
  watchdog a caller, because only then is the claim true.
- Nineteen open findings is the largest carry any feature has held.
