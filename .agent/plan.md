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
R8 upgrades the patch-approval producer, the richest evidence in the queue and
until now the least cited: the intent it is about and the file it would change
are both on the record the branch already reads. It takes the optionless shape,
because its `next_actions` are command lines rather than option words and
amendment A3 puts growing an options list out of scope. The round also books
the R7 verdict, resolves `R-0712`, and finishes the stale-count sweep that R6
and R7 each left one sentence short.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R7 verdict and Done: R-0712 | ordered | the record moves first |
| C3 the patch-approval triple and the gate set | ordered | S1 to S4 |
| C4 the stale-count sweep | ordered | S5, defined by property |
| C5 its tests | ordered | S6, then the red-proofs |
| C6 the handback | ordered | |

## Next Steps
1. T002 continues with the memory-review and stop-reason producers, each
   joining `TRIPLE_REQUIRED_TYPES` in the commit that gives it a real triple.
2. Then repo-dirty, whose event carries the thinnest evidence of the eight and
   needs its refs thought through, and the two branches that already carry an
   options list — the flight plan's resolved arm owes a ruling.
3. T003 card enrichment and the chip deep links, then the integration gate.

## Risks
- Three types are enforced from this round on, so a later change that regresses
  any of their triples raises instead of rendering. That is the intent.
- The flight-plan branch has two arms and only one carries options; enforcing
  that type will need a ruling on what a RESOLVED decision owes.
