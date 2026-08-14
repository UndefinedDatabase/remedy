# Plan — F077 Autonomy watchdog

Branch: feature/f077-autonomy-watchdog, cut from main after PR #199 merged.
F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding id: R-0393.
Open findings: TWENTY-THREE — R-0380, R-0381, R-0361, R-0362, R-0363, R-0364,
R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379,
R-0382, R-0385, R-0386, R-0387, R-0389, R-0391, R-0392 — recomputed mechanically
at R14 from `.agent/live_review.md`: 27 registered, 4 resolved (R-0383, R-0384,
R-0388, R-0390), no duplicate id. That file is the source of truth; this one
mirrors it.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger, postmortems and actuals, and on
no-progress repetition, a burn-rate anomaly or goal drift it PAUSES the mission
and raises one decision per trip class carrying the evidence triple. It stops;
it never repairs. Thresholds live in config, not code.

## Current Step
R14 — the first half of T003, built against `.agent/f077_t003_inventory.md`.
C1 recorded the R13 PASS. DECISION F077 D12 is on the record: the
paused-by-watchdog trip leads `remedy mission show`, not `mission report`,
because that command is a dogfood-run facade keyed on a RUN id that never loads
a Mission. C2 extracted `watchdog.evaluate_mission` — the read-only twin of
`watchdog_pass`, same reads and no write — and routed `watchdog_pass` through
it. C3 added the read-only `remedy mission watchdog <id>`; C4 added `mission
resume`, D4-scoped to the status alone, across all three encodings of the verb
list. The report surface is NOT built here.

## Next Steps
1. R15 — the report surface under DECISION F077 D12: the trip lead block in
   `_cmd_mission_show` and its tests. Its FIRST commit owes R14's own
   `Gate: R14 — ` paragraph, which cannot exist before this round is reviewed.
2. R16 — integration gate, then closure.

## Risks
- A mission resumed AFTER its watchdog decision is answered still carries the
  tripping run in its ledger and trips again — the code CONFIRMS it for all
  three tripwires, so D4's verb buys exactly one iteration (inventory Q8).
- R14 shipped `mission resume` at exactly that scope, and DECISION F077 D12
  does not address the re-trip; no round yet owns it.
- goal_drift reads the ledger's `move.payload.milestone_id`, never the job.
- Twenty-three open findings is the largest carry any feature has held.
