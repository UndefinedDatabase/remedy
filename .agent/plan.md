# Plan — F077 Autonomy watchdog

Branch: feature/f077-autonomy-watchdog, cut from main after PR #199 merged.
F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding id: R-0396.
Open findings: TWENTY-SIX — R-0380, R-0381, R-0361, R-0362, R-0363, R-0364,
R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379,
R-0382, R-0385, R-0386, R-0387, R-0389, R-0391, R-0392, R-0393, R-0394, R-0395 —
recomputed at the session close from `.agent/live_review.md`: 30 registered,
4 resolved (R-0383, R-0384, R-0388, R-0390), no duplicate id. It is the source of
truth; this one mirrors it.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger, postmortems and actuals, and on
no-progress repetition, a burn-rate anomaly or goal drift it PAUSES the mission
and raises one decision per trip class carrying the evidence triple. It stops;
it never repairs. Thresholds live in config, not code.

## Current Step
R16 — the integration gate per docs/agents/integration_gate.md: the full suite
on the branch AND at the merge base 6227c3a2, compared with `comm`, every
branch-only and base-only id attributed, and the evidence committed under
`.agent/gate_f077_r16/`. F077 has run no base comparison in any round, so this
one owes the whole procedure rather than the branch-only re-run F254 took under
its own DECISION D14. The round's FIRST commit is not the gate work: it is the
verdict on R15's four session-close rounds, recorded as `Gate: R15-close`, so
that no round on this branch is unreviewed while the suite runs.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: the evidence job, a
   FRESH review zip (a zip failure is a closure blocker), the authored STATUS
   line committed last on the branch, then the PR — which is not merged now.
2. Closure still owes an ist-doc for the watchdog under `docs/`, registered in
   `docs/README.md`. No round has written it yet.
3. A branch-only failure the gate reproduces is a BLOCKER whose repair is its
   own reviewer-gated round, never folded into the closure round.

## Risks
- A mission resumed AFTER its watchdog decision is answered still carries the
  tripping run in its ledger and trips again — the code CONFIRMS it for all
  three tripwires, so D4's verb buys exactly one iteration (inventory Q8).
- R14 shipped `mission resume` at exactly that scope, and DECISION F077 D12
  does not address the re-trip; no round yet owns it.
- goal_drift reads the ledger's `move.payload.milestone_id`, never the job.
- Twenty-six open findings is the largest carry any feature has held.
