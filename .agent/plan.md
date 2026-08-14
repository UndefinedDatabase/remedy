# Plan — F077 Autonomy watchdog

Branch: feature/f077-autonomy-watchdog, cut from main after PR #199 merged.
F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding id: R-0398.
Open findings: TWENTY-EIGHT — R-0380, R-0381, R-0361, R-0362, R-0363, R-0364,
R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379,
R-0382, R-0385, R-0386, R-0387, R-0389, R-0391, R-0392, R-0393, R-0394, R-0395,
R-0396, R-0397 — recomputed from `.agent/live_review.md` at R17: 32 registered,
4 resolved (R-0383, R-0384, R-0388, R-0390), no duplicate id. It is the source
of truth; this one mirrors it.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger, postmortems and actuals, and on
no-progress repetition, a burn-rate anomaly or goal drift it PAUSES the mission
and raises one decision per trip class carrying the evidence triple. It stops;
it never repairs. Thresholds live in config, not code.

## Current Step
R17 — record the R16 integration gate as `Gate: R16 — PASS`, register R-0396
(the gate's attribution named an exclusive cause the code refutes) and R-0397
(the block ordered a verbatim transcript AND `git diff --check` silence, which
a pytest traceback cannot satisfy together), and write the deliverable closure
has owed since T003 finished: `docs/system/autonomy-watchdog-v1.md`, built
state only, registered in `docs/README.md`. The two registrations and every
count they invalidate land in ONE commit, which is what R-0395 exists to force.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: the evidence job, a
   FRESH review zip (a zip failure is a closure blocker), the authored STATUS
   line committed last on the branch, then the PR — which is not merged now.
2. The integration gate is DONE and green — 16898 passed on the branch, zero
   branch-only failures — so closure re-confirms the suite, never re-opens it.

## Risks
- A mission resumed AFTER its watchdog decision is answered still carries the
  tripping run in its ledger and trips again — the code CONFIRMS it for all
  three tripwires, so D4's verb buys exactly one iteration (inventory Q8).
- R14 shipped `mission resume` at exactly that scope, and DECISION F077 D12
  does not address the re-trip; no round yet owns it.
- goal_drift reads the ledger's `move.payload.milestone_id`, never the job.
- Twenty-eight open findings is the largest carry any feature has held.
- R-0396's amendment target, docs/agents/integration_gate.md, is outside this
  feature's change set, so every future gate reproduces the eight phantom
  ui_server base failures until some feature owns that doc.
