# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 D1 through D6.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the design amendments that reconcile it with the source.

## Current Step
R6 opens session 2 and starts T002. It books the R5 verdict and resolves
`R-0711`, then upgrades the FIRST producer: the budget stop carries refs into
the budget evidence it already computes, and one expected outcome and one
downside per choice, and `token_budget` becomes the first member of
`TRIPLE_REQUIRED_TYPES` in that same commit. DECISION F032 D6 rules where that
card's options list comes from, because the emit gate reads a decision's
options from `payload["options"]` and this branch carried none.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R5 verdict and the R-0711 resolution | ordered | the record moves first |
| C3 DECISION F032 D6 and its amendment | ordered | the ruling before the code |
| C4 the budget triple and the gate set | ordered | S1 through S5 |
| C5 its tests | ordered | S6, then the red-proofs |
| C6 the handback | ordered | |

## Next Steps
1. T002 continues with the patch-approval and repo-dirty producers, each
   joining `TRIPLE_REQUIRED_TYPES` in the commit that gives it a real triple.
2. Then test-failure, memory-review and stop-reason, then the two branches
   that already carry an options list.
3. T003 card enrichment and the chip deep links, then the integration gate.

## Risks
- The gate is live for one type from this round on, so a later change that
  regresses the budget triple raises instead of rendering. That is the intent.
- Seven producing types still carry the honest legacy placeholder, so the
  gate protects only `token_budget` until each is upgraded in turn.
