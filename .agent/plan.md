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
R7 continues T002 with the test-failure producer, and it starts by repairing
what reading that branch exposed. The card names the failing command from the
event key `command`, which no producer writes — the emitter writes
`command_safe` — so every such card in production reads `Test '?' failed.`
That is `R-0712`, registered and fixed here, and the branch then gets its refs
and its one unkeyed outcome and joins the enforced set.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R6 verdict and R-0712 | ordered | findings persist before repair |
| C3 the R-0712 fix | ordered | S2, the command read |
| C4 the triple, the gate set, two retired comments | ordered | S3 to S5 |
| C5 its tests | ordered | S6, then the red-proofs |
| C6 the handback | ordered | |

## Next Steps
1. T002 continues with the repo-dirty and patch-approval producers, each
   joining `TRIPLE_REQUIRED_TYPES` in the commit that gives it a real triple.
2. Then memory-review and stop-reason, then the two branches that already
   carry an options list.
3. T003 card enrichment and the chip deep links, then the integration gate.

## Risks
- Two types are enforced from this round on, so a later change that regresses
  either triple raises instead of rendering. That is the intent.
- The inbox guard's own test-failure fixture writes the older `command` key,
  so the fix keeps reading it; the new tests cover the real producer's key.
