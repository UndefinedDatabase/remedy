# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 D1 through D4.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the design amendments that reconcile it with the source.

## Current Step
R3 is T001a: the schema and its validator, wired to nothing. One new module
`packages/orchestration/decision_evidence.py` and one new test file. The emit
gate DECISION F032 D1 rules is deliberately held back to T001b so that the
wiring round can spend its whole gate budget on the guards it moves, which
inventory Q8 lists. DECISION F032 D4 settles the names against the two
collisions the reviewer measured in the source.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 DECISION F032 D4 and one prose slip | ordered | names, and a wrapped row |
| C3 the feature file amendment A4 | ordered | where a builder reads it |
| C4 the new module | ordered | S1 through S8 |
| C5 the new tests | ordered | S9, then the red-proofs |
| C6 the handback | ordered | |

## Next Steps
1. T001b: the emit gate at `list_decisions`, legacy rendering for records with
   no triple, and the CI canary a tripleless producer must fail. That round
   first edits `packages/orchestration/decision_queue.py`, so `R-0710`'s fix
   clause binds it.
2. T002 the per-producer upgrades, with the content goldens.
3. T003 card enrichment and the chip deep links.

## Risks
- The schema lands at C4 with no test until C5. That is ordered rather than
  accidental, and the round does not end between them.
- `R-0710` stays open through this round by design; it is not a `while I am
  here` edit and its fix has a named owner.
