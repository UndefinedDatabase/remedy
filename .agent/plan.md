# Plan — F077 Autonomy watchdog

Branch: feature/f077-autonomy-watchdog, cut from main after PR #199 merged.
F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding id: R-0393.
Open findings: TWENTY-THREE — R-0380, R-0381, R-0361, R-0362, R-0363, R-0364,
R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379,
R-0382, R-0385, R-0386, R-0387, R-0389, R-0391, R-0392 — recomputed mechanically
at R13 from `.agent/live_review.md`: 27 registered, 4 resolved (R-0383, R-0384,
R-0388, R-0390), no duplicate id. That file is the source of truth; this one
mirrors it.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger, postmortems and actuals, and on
no-progress repetition, a burn-rate anomaly or goal drift it PAUSES the mission
and raises one decision per trip class carrying the evidence triple. It stops;
it never repairs. Thresholds live in config, not code.

## Current Step
R13 — the inventory round, and NO file under `packages/`, `apps/`, `tests/` or
`docs/` was touched. C1 recorded the R12 PASS and registered R-0392 (the
reviewer's own "eleven `_record` call sites" is ten). C2 wrote
`.agent/f077_t003_inventory.md`, answering eight questions about T003's surface
from the code. Three of the block's own premises were checked and corrected
there: `evaluate_ledger` is the only side-effect-free entry point but takes
entries, not a mission id, so no read-only mission-shaped call exists yet;
`_status_for_verb` is one of THREE places the verb list is encoded; and
`mission report` is a facade over the dogfood run keyed on a RUN id, so the
paused-mission report has no insertion point there today. The safe point that
refuses a non-active mission writes NO ledger entry.

## Next Steps
1. R14 — build T003 against the inventory: the manual `mission watchdog` CLI,
   the `mission resume` verb (D4), the report surface and their tests. The
   handlers go in `mission_cmd.py`; `worker_facade_cmd.py` carries an exact-set
   guard that a second registration there turns red.
2. R15 — integration gate, then closure.

## Risks
- A mission resumed AFTER its watchdog decision is answered still carries the
  tripping run in its ledger and trips again — the code CONFIRMS it for all
  three tripwires, so D4's verb buys exactly one iteration (inventory Q8).
- goal_drift reads the ledger's `move.payload.milestone_id`, never the job.
- Twenty-three open findings is the largest carry any feature has held.
