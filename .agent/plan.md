# Plan — F077 Autonomy watchdog

Branch: feature/f077-autonomy-watchdog, cut from main after PR #199 merged.
F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding id: R-0391.
Open findings: TWENTY-THREE — R-0380, R-0381, R-0361, R-0362, R-0363, R-0364,
R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379,
R-0382, R-0385, R-0386, R-0387, R-0388, R-0389, R-0390 — recomputed mechanically
at R11 from `.agent/live_review.md`: 25 registered, 2 resolved (R-0383, R-0384),
no duplicate id. That file is the source of truth; this one mirrors it.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger, postmortems and actuals, and on
no-progress repetition, a burn-rate anomaly or goal drift it PAUSES the mission
and raises one decision per trip class carrying the evidence triple. It stops;
it never repairs. Thresholds live in config, not code.

## Current Step
R11 — HALTED at C3 by the block's own stop clause; NO code changed. Recorded
first: the R10 FAIL verdict, findings R-0387 to R-0390 and DECISION F077 D10
(C0a, C0b, C1, C2). C3 orders `run_mission` to stop passing its iteration
number so a trip takes `next_iteration_index`, and makes that conditional on
the loop never recording after a trip — "if you find a path where the loop DOES
record after a trip, stop and report it". There is one: the safe point runs
BEFORE the top-of-loop status check, so a stop requested in the window after a
trip records an entry at exactly the number the watchdog took. Probed with the
ordered change applied in a disposable worktree: `[1, 2, 3, 4, 4]`. At base,
unchanged: `[1, 2, 3, 3, 4]`. Both numberings duplicate on that path.

## Next Steps
1. R12 — the reviewer re-decides D10 against the safe-point path, then the
   repair lands and `test_one_entry_per_iteration_numbered_from_one` goes
   green.
2. R13 — T003: the manual CLI, the missing `mission resume` verb (D4) and the
   report surface.
3. R14 — integration gate, then closure.

## Risks
- `test_orchestrator_loop.py::test_one_entry_per_iteration_numbered_from_one`
  is RED (1 failed, 195 passed) at base AND at HEAD; this round moved it
  neither way.
- A mission resumed AFTER its watchdog decision is answered still carries the
  tripping run in its ledger and trips again — T003's, per D4.
- goal_drift reads the ledger's `move.payload.milestone_id`, never the job.
- Twenty-three open findings is the largest carry any feature has held.
