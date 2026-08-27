# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 D1 through D5.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the design amendments that reconcile it with the source.

## Current Step
R4 is T001b: the emit gate, the legacy placeholder and the canary.
`HumanDecision` gains one optional field, `export_decision_json` gains three
keys, and `list_decisions` calls the enforcement DECISION F032 D1 puts at the
emit point. Enforcement is opt-in per type and the set starts EMPTY, so no
existing producer changes behaviour while the gate is live and pinned from the
first commit. `R-0710` is fixed here because this is the first round to edit
`packages/orchestration/decision_queue.py`.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 DECISION F032 D5 | ordered | per-card marker, opt-in enforcement |
| C3 the feature file amendment A5 | ordered | where a builder reads it |
| C4 the wiring and the R-0710 fix | ordered | S1 through S9 |
| C5 the tests and the canary | ordered | S10, then the red-proofs |
| C6 the handback | ordered | |

## Next Steps
1. T002: upgrade the producers one at a time, adding each type to
   `TRIPLE_REQUIRED_TYPES` only once its triple is real, with the content
   goldens and the anti-boilerplate assertions.
2. T003: card enrichment, the chips and the evidence-panel deep links.
3. The integration gate, then closure.

## Risks
- The opt-in set is what keeps this round safe. If a producer is added to it
  before its triple is real, every job carrying that decision type raises.
- The reviewer, not the worker, writes `R-0710`'s resolution; until then it
  stays open in the record even though the code is fixed.
