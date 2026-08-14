# Plan — F077 Autonomy watchdog

Branch: feature/f077-autonomy-watchdog, cut from main after the F057 closure
PR #199 merged. F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free
finding id: R-0384. Open findings: eighteen — R-0361, R-0362, R-0363, R-0364,
R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378,
R-0379, R-0380, R-0381, R-0382, R-0383. `.agent/live_review.md` is the source
of truth for this ledger; this file mirrors it and nothing else.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger, postmortems and actuals, and on
no-progress repetition, a burn-rate anomaly or goal drift it PAUSES the mission
and raises one decision per trip class carrying the evidence triple. It stops;
it never repairs. Thresholds live in config, not code.

## Current Step
R5 — record the R4 verdict, repair R-0383, then inventory T002.

R-0383 is the reviewer's own defect carried into code: the R4 block asserted
that `packages/orchestration/watchdog.py` reads no file while the same section
ordered `watchdog_thresholds_from_config` to call `get_config()`, and the
module docstring inherited the false clause. The repair narrows that docstring
to the three evaluators and their helpers and names the threshold resolver as
the one function that reaches outside. No behaviour and no signature changes.

`.agent/f077_t002_inventory.md` then answers the seven questions T002 cannot be
planned without — decision attachment with no linked job, the `HumanDecision`
record and its dedup carrier, what "until resolved" is on disk, appending a
ledger entry from outside `run_mission`, the `set_mission_status` docstring if
the watchdog becomes a second pause writer, the loop-integration seam, and the
whole-file count assertions a new decision type would break. It is READ-ONLY
investigation: no file under packages/, apps/, tests/ or docs/ changes, and no
part of T002 is built this round.

## Next Steps
1. R6 — T002 the pause, the decision, the per-trip-class dedup and the
   `watchdog_tripped` ledger entry, plus the loop-integration test. The
   inventory's open questions are settled there, not here.
2. R7 — T003 the manual CLI and the report surface.
3. R8 — integration gate, then closure.

## Risks
- The F077 feature file asserts "every loop-dispatched job carries its
  milestone link", which is false as a field on the job or on
  `MissionJobLink`. T001 therefore builds goal_drift off the ledger's
  `move.payload.milestone_id`, not off the job.
- Eighteen open findings is the largest carry any feature has held.
