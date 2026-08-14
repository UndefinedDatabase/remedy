# Plan — F077 Autonomy watchdog

Branch: feature/f077-autonomy-watchdog, cut from main after the F057 closure
PR #199 merged. F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free
finding id: R-0382. Open findings: sixteen — the fourteen carried from F057
(R-0361, R-0362, R-0363, R-0364, R-0367, R-0368, R-0369, R-0371, R-0374,
R-0375, R-0376, R-0377, R-0378, R-0379) plus R-0380 and R-0381 registered this
round from the closure candidates. `.agent/live_review.md` is the source of
truth for this ledger; this file mirrors it and nothing else.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger, postmortems and actuals, and on
no-progress repetition, a burn-rate anomaly or goal drift it PAUSES the mission
and raises one decision per trip class carrying the evidence triple. It stops;
it never repairs. Thresholds live in config, not code.

## Current Step
R1 is done: PR #199 merged, F077 claimed, this record reset carrying the F057
open set forward, R-0380 and R-0381 registered, candidates carrier emptied.

## Next Steps
1. R2 — the T001 inventory, read-only, no production edit: the loop's ledger
   entry format and its writer, the mission pause seam and whether the loop
   re-reads it per iteration, and the milestone link on dispatched jobs. Every
   answer carries a file-and-symbol citation, into `.agent/f077_inventory.md`.
2. R3 — T001 the three evaluators as pure functions plus unit tests.
3. R4 — T002 pause, decision, dedup, ledger entry, loop-integration test.
4. R5 — T003 the manual CLI and the report surface.

## Risks
- The feature file assumes the loop may lack a per-iteration pause check.
  `orchestrator_loop.py` already refuses a mission whose `mission.status !=
  MISSION_STATUS_ACTIVE`; R2 must establish whether that check is re-evaluated
  each iteration or only at entry, because T002's acceptance depends on it.
- Sixteen open findings is the largest carry any feature has started with.
