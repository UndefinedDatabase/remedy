# Plan — F077 Autonomy watchdog

Branch: feature/f077-autonomy-watchdog, cut from main after PR #199 merged.
F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding id: R-0392.
Open findings: TWENTY-TWO — R-0380, R-0381, R-0361, R-0362, R-0363, R-0364,
R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379,
R-0382, R-0385, R-0386, R-0387, R-0389, R-0391 — recomputed mechanically at R12
from `.agent/live_review.md`: 26 registered, 4 resolved (R-0383, R-0384, R-0388,
R-0390), no duplicate id. That file is the source of truth; this one mirrors it.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger, postmortems and actuals, and on
no-progress repetition, a burn-rate anomaly or goal drift it PAUSES the mission
and raises one decision per trip class carrying the evidence triple. It stops;
it never repairs. Thresholds live in config, not code.

## Current Step
R12 — the repair, and no production file was touched. Recorded first: the R11
PASS, R-0391 against the reviewer, R-0388 resolved as a MISDIAGNOSIS and R-0390
resolved (C1), then DECISION F077 D11 (C2). D11 withdraws D10 unimplemented:
`grep -c '_record(iteration'` returns eleven in `orchestrator_loop.py` — ten
calls plus the definition at line 1036 — and two of those calls, the executed
move at line 1210 and the R-0190 blocked-completion escalation at line 1253,
fire in ONE pass at ONE number. The "one entry per iteration, numbered once"
invariant R-0388 asserted therefore never existed; `iteration` is an
ATTRIBUTION, not a key. C3 repaired the test and not the loop:
`test_one_entry_per_iteration_numbered_from_one` becomes
`test_iterations_are_numbered_in_sequence_from_one` and asserts `[1, 2, 3, 3]`
with `watchdog_tripped` fourth. The file moves from `1 failed, 195 passed` at
base `28c50487` to `196 passed` at HEAD.

## Next Steps
1. R13 — T003: the manual CLI, the missing `mission resume` verb (D4) and the
   report surface. Its first commit also records R12's own verdict, which
   cannot be on disk at this HEAD — the last round of a session cannot gate
   itself.
2. R14 — integration gate, then closure.

## Risks
- A mission resumed AFTER its watchdog decision is answered still carries the
  tripping run in its ledger and trips again — T003's, per D4.
- goal_drift reads the ledger's `move.payload.milestone_id`, never the job.
- Twenty-two open findings is the largest carry any feature has held.
