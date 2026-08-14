# Plan — F077 Autonomy watchdog

Branch: feature/f077-autonomy-watchdog, cut from main after PR #199 merged.
F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding id: R-0403.
Open findings: THIRTY-TWO — R-0361, R-0362, R-0363, R-0364, R-0367, R-0368,
R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379, R-0380, R-0381,
R-0382, R-0385, R-0386, R-0387, R-0389, R-0391, R-0392, R-0393, R-0394, R-0395,
R-0396, R-0397, R-0399, R-0400, R-0401, R-0402 — recomputed from
`.agent/live_review.md` at R20: 37 registered, 5 resolved (R-0383, R-0384,
R-0388, R-0390, R-0398), no duplicate id. All are Medium or Low; there are no
High or blocker findings, which is what closure precondition 1 requires.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger, postmortems and actuals, and on
no-progress repetition, a burn-rate anomaly or goal drift it PAUSES the mission
and raises one decision per trip class carrying the evidence triple. It stops;
it never repairs. Thresholds live in config, not code.

## Current Step
R20 — closure. All five preconditions hold: every round has a PASS verdict and
every finding is an open Medium or Low; the reviewer re-ran the full suite
itself and measured 16898 passed, 19 skipped at exit 0; `integrity check` is
passed=true with `high_blockers_open` clear and zero relevant untracked files;
the feature file's Built State landed at 4fa56b23; and the tree is clean with
the branch pushed. What remains is the evidence job, the FRESH review zip, the
closure commit and the PR.

## Next Steps
1. Evidence job `f077-closure`, then the review zip — a failing zip build is a
   closure BLOCKER, never a thing to work around.
2. The closure commit LAST on the branch: STATUS `[x]` and the README count and
   tier sync in the SAME commit (R-0154; tests/docs pins the count to the
   ledger), plus the final `.agent/` state. Then the PR, which is NOT merged
   this session — it merges at F082's start via the Open PR Gate.

## Risks
- A mission resumed AFTER its watchdog decision is answered still carries the
  tripping run in its ledger and trips again — the code CONFIRMS it for all
  three tripwires, so D4's verb buys exactly one iteration (inventory Q8), and
  DECISION F077 D12 does not address the re-trip.
- Thirty-two open findings is the largest carry any feature has held.
- R-0396's amendment target, docs/agents/integration_gate.md, is outside this
  feature's change set, so every future integration gate reproduces the eight
  phantom ui_server base failures until some feature owns that doc.
