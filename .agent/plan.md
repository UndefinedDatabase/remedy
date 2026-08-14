# Plan — F077 Autonomy watchdog

Branch: feature/f077-autonomy-watchdog, cut from main after the F057 closure
PR #199 merged. F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free
finding id: R-0385. Open findings: nineteen — R-0361, R-0362, R-0363, R-0364,
R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378,
R-0379, R-0380, R-0381, R-0382, R-0383, R-0384 — the eighteen carried plus
R-0384. `.agent/live_review.md` is the source of truth for this ledger; this
file mirrors it and nothing else.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger, postmortems and actuals, and on
no-progress repetition, a burn-rate anomaly or goal drift it PAUSES the mission
and raises one decision per trip class carrying the evidence triple. It stops;
it never repairs. Thresholds live in config, not code.

## Current Step
R6 — record the R5 verdict, register R-0384, close the session.

R5 is DONE: the R4 verdict and R-0383 are on the record in
`.agent/live_review.md`, R-0383's repair has LANDED in
`packages/orchestration/watchdog.py` but is NOT yet resolved — only the next
reviewer verdict replaces its `Landed:` line with a `Done:` line — and the T002
inventory is in `.agent/f077_t002_inventory.md`.

R-0384 is registered this round and is PRE-EXISTING: the `set_mission_status`
docstring in `packages/orchestration/mission_state.py`, echoed on
`_cmd_mission_set_status`, claims the status is only ever written by an
explicit human command, while `mission_achieved` and `execute_move` in
`packages/orchestration/orchestrator_loop.py` already write it autonomously.
It is repaired INSIDE the R7 round that makes it worse, not before.

No production or documentation file changes this round.

## Next Steps
1. R7 — T002 the pause, one decision per trip class, the per-trip-class dedup,
   the `watchdog_tripped` ledger entry and the loop-integration test. That
   block must FIRST settle the eight open questions at the end of
   `.agent/f077_t002_inventory.md`; it also repairs R-0384.
2. R8 — T003 the manual CLI and the report surface.
3. R9 — integration gate, then closure.

## Risks
- The F077 feature file asserts "every loop-dispatched job carries its
  milestone link", which is false as a field on the job or on
  `MissionJobLink`. T001 therefore builds goal_drift off the ledger's
  `move.payload.milestone_id`, not off the job.
- Nineteen open findings is the largest carry any feature has held.
