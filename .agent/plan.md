# Plan — F077 Autonomy watchdog

Branch: feature/f077-autonomy-watchdog, cut from main after PR #199 merged.
F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding id: R-0387.
Open findings: NINETEEN — R-0361, R-0362, R-0363, R-0364, R-0367, R-0368,
R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379, R-0380,
R-0381, R-0382, R-0385, R-0386 — recomputed mechanically at R10 from
`.agent/live_review.md`: 21 registered, 2 resolved (R-0383, R-0384), no
duplicate id. That file is the source of truth; this one mirrors it.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger, postmortems and actuals, and on
no-progress repetition, a burn-rate anomaly or goal drift it PAUSES the mission
and raises one decision per trip class carrying the evidence triple. It stops;
it never repairs. Thresholds live in config, not code.

## Current Step
R10 — the wiring. `watchdog.watchdog_pass` is the loop's single entry point
into the watchdog, and `run_mission` calls it once per CONTINUING iteration
(never a terminal one), so a tripwire finally reaches a running mission. D7's
watchdog clause landed in the `set_mission_status` and `_cmd_mission_set_status`
docstrings in the same commit as the call site. Three new tests drive the
production path under the real default thresholds: a scripted three-dispatch run
trips `no_progress`, the pause it writes stops a SECOND `run_mission` from
dispatching anything, and a two-dispatch run writes nothing at all.

BLOCKER, declared and NOT repaired. `test_orchestrator_loop.py::
TestTheLedgerCoversEveryIteration::test_one_entry_per_iteration_numbered_from_one`
is RED at this commit (196 passed at base `24600478`, 1 failed / 195 at HEAD).
It scripts three identical dispatches under `max_iterations=3`, which now trips
`no_progress`, so its ledger reads `[1, 2, 3, 3]` against `== [1, 2, 3]`. It is
a stale whole-ledger guard of exactly the class D8 predicted — D8 and D9 both
looked only at `test_mission_e2e.py`, which measured GREEN. The R10 block names
twelve files and makes gate 8 the sole authority for a thirteenth, so no gate
authorises repairing this one.

## Next Steps
1. R11 — repair that one stale guard, the only red on the branch; then T003:
   the manual CLI including the missing `mission resume` verb (D4) and the
   report surface.
2. R12 — integration gate, then closure.

## Risks
- A mission resumed AFTER its watchdog decision is answered still carries the
  tripping run in its ledger and trips again on the next pass — real `mission
  resume` semantics, assigned to T003 by D4 and deliberately unsolved in R10.
- goal_drift reads the ledger's `move.payload.milestone_id`, never the job: the
  feature file's "every dispatched job carries its milestone link" is false.
- Nineteen open findings is the largest carry any feature has held.
