# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the orchestrator brief.

## Current Step
R1 claims F032 in the roadmap ledger, cuts the branch, resets this record set
for the new feature and puts the F032 source inventory on disk. The inventory
is the round's substance: the feature file's design names one enqueue seam
"every producer already funnels through", while the eight producing branches of
`decision_queue.list_decisions` derive from eight different subsystems, so
where the gate can live at all is a measurement this feature takes before it
plans T001.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 plan and context for F032 | ordered | first substantive commit |
| C2 STATUS claim, open to active | ordered | |
| C3 live-review header reset | ordered | findings carried forward |
| C4 the F032 source inventory | ordered | Q1-Q8, each measured |
| C5 the handback | ordered | |

## Next Steps
1. Book R1's verdict into `.agent/live_review.md` and plan T001 against the
   inventory — the schema, and the enforcement point the inventory names.
2. T001: schema v2, the enforcement gate, legacy rendering, the CI canary and
   its unit tests.
3. T002 the per-producer upgrades, then T003 card enrichment and chip
   deep links.

## Risks
- The feature file's Design names one enqueue seam. If the inventory measures
  none, the spec is wrong and the reviewer rules a DECISION under §4 item 7
  rather than widening scope silently.
- `.agent/live_review.md` is append-only below `## Findings`. R1 rewrites the
  header region and nothing else, and that region is proved byte-identical.
