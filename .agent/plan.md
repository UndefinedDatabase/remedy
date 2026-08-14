# Plan — F077 Autonomy watchdog

Branch: feature/f077-autonomy-watchdog, cut from main after the F057 closure
PR #199 merged. F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free
finding id: R-0383. Open findings: seventeen — R-0361, R-0362, R-0363, R-0364,
R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378,
R-0379, R-0380, R-0381, R-0382. `.agent/live_review.md` is the source of truth
for this ledger; this file mirrors it and nothing else.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger, postmortems and actuals, and on
no-progress repetition, a burn-rate anomaly or goal drift it PAUSES the mission
and raises one decision per trip class carrying the evidence triple. It stops;
it never repairs. Thresholds live in config, not code.

## Current Step
R4 — T001, the three tripwire evaluators as PURE functions over ledger entries.
New `packages/orchestration/watchdog.py` carries `evaluate_no_progress`,
`evaluate_burn_anomaly` and `evaluate_goal_drift` plus the `evaluate_ledger`
aggregator and the frozen `Trip` evidence record. Four threshold keys join
`packages/orchestration/config.py`: `watchdog.no_progress_repeats`,
`watchdog.burn_window`, `watchdog.burn_min_samples`,
`watchdog.burn_multiplier`. The new `tests/orchestration/test_watchdog.py`
pins each tripwire against its just-under-threshold twin.

R3 recorded the R2 verdict on `.agent/live_review.md` and closed the previous
session; it wrote no production file. Round numbering shifted by one at R3 —
what this mirror called R3 (T001) is now R4 — which is why plan.md and
context.md are re-synced here, in R4's first commit.

## Next Steps
1. R5 — T002 pause, decision, dedup, ledger entry, loop-integration test. The
   decision attachment and the loop invocation point are still open questions
   and are settled there, not here.
2. R6 — T003 the manual CLI and the report surface.
3. R7 — integration gate, then closure.

## Risks
- The F077 feature file asserts "every loop-dispatched job carries its
  milestone link", which is false as a field on the job or on
  `MissionJobLink`. T001 therefore builds goal_drift off the ledger's
  `move.payload.milestone_id`, not off the job.
- Seventeen open findings is the largest carry any feature has started with.
