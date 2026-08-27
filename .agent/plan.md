# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 from D1.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and, from this round, the design amendments that reconcile it
with the source.

## Current Step
R2 books R1's verdict and the one defect with product effect that R1's
inventory found, and rules the three conflicts between the feature file's
suggested Design and the measured source: there is no enqueue seam, there is no
typed provenance vocabulary, and six of the eight producing branches carry no
options list. Each is settled as a DECISION and written into the feature file
so T001 is specified against what the source has.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 gate F032 R1 and register R-0710 | ordered | one finding, none resolved |
| C3 DECISION F032 D1, D2 and D3 | ordered | the three spec conflicts |
| C4 feature-file design amendments | ordered | the same three, where a
  builder reads them |
| C5 the handback | ordered | |

## Next Steps
1. T001a: the evidence-triple schema and the emit gate at the derivation
   point D1 names, with the guards R1's inventory Q8 lists red-proved.
2. T001b: legacy rendering for records without a triple, and the CI canary
   that a tripleless producer must fail.
3. T002 the per-producer upgrades, then T003 card enrichment and chip links.

## Risks
- D2 builds a minimal ref type inside F032 rather than waiting for F066, which
  is unclaimed. If F066 later lands a different vocabulary, the reversal is
  named in D2 and is a rename, not a redesign.
- The open set stands at 250 after this round. None of it blocks F032.
