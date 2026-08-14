# Plan — F077 Autonomy watchdog

Branch: feature/f077-autonomy-watchdog, cut from main after PR #199 merged.
F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding id: R-0394.
Open findings: TWENTY-FOUR — R-0380, R-0381, R-0361, R-0362, R-0363, R-0364,
R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379,
R-0382, R-0385, R-0386, R-0387, R-0389, R-0391, R-0392, R-0393 — recomputed
mechanically at R15 from `.agent/live_review.md`: 28 registered, 4 resolved
(R-0383, R-0384, R-0388, R-0390), no duplicate id. That file is the source of
truth; this one mirrors it.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger, postmortems and actuals, and on
no-progress repetition, a burn-rate anomaly or goal drift it PAUSES the mission
and raises one decision per trip class carrying the evidence triple. It stops;
it never repairs. Thresholds live in config, not code.

## Current Step
R15 — the second half of T003, which completes it. C1 recorded the R14 PASS and
registered R-0393 (a red-proof is a PAIR: one `-k` selection for the green run
and every mutated run). C2 added `watchdog.latest_trips_from_ledger`, a pure
reader that reconstructs the trips a ledger already RECORDS — newest per kind,
in the fixed kind order, torn entries skipped. C3 put the lead into
`_cmd_mission_show` under DECISION F077 D12: a PAUSED mission's text output
leads with the trip and its pointer to `remedy mission watchdog`, its `--json`
gains a top-level `watchdog_trips`, and an unpaused one is unchanged. `show`
stays read-only — it re-evaluates nothing.

## Next Steps
1. R16 — the integration gate per docs/agents/integration_gate.md. It owes no
   gate paragraph: R15 was reviewed and its verdict is on the record, so R16's
   first commit is the integration gate's own work.
2. Closure per docs/roadmap/STATUS_closure_protocol.md — which still owes an
   ist-doc for the watchdog under `docs/`, registered in `docs/README.md`. No
   round has written it yet.

## Risks
- A mission resumed AFTER its watchdog decision is answered still carries the
  tripping run in its ledger and trips again — the code CONFIRMS it for all
  three tripwires, so D4's verb buys exactly one iteration (inventory Q8).
- R14 shipped `mission resume` at exactly that scope, and DECISION F077 D12
  does not address the re-trip; no round yet owns it.
- goal_drift reads the ledger's `move.payload.milestone_id`, never the job.
- Twenty-four open findings is the largest carry any feature has held.
