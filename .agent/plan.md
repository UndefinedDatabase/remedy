# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 D1 through D7.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the design amendments that reconcile it with the source.

## Current Step
R11 upgrades the flight-plan approval, the first producing type with TWO arms:
a pending card carrying the two options the write door accepts, and a resolved
card carrying none. The emit gate selects on type alone and never reads
`status`, so both arms are enforced together — DECISION F032 D7 records why
that is the right reading and what a resolved card's outcome then means. The
round also books the R10 verdict and repoints the two unenforced-type guards to
a type with no producer, so they stop moving every round.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R10 verdict and one prose-slip line | ordered | the record first |
| C3 DECISION F032 D7 | ordered | the ruling S5 rests on |
| C4 both arms and the gate entry | ordered | S2 to S6, one commit |
| C5 the tests and the repointed guards | ordered | S7 and S8 |
| C6 the handback | ordered | |

## Next Steps
1. The task decision, the last producing type. Its options come from the
   escalation record and are arbitrary strings, so its outcomes are built per
   option rather than written out, and it has a resolved arm that DECISION
   F032 D7 already rules on. With it the gate set is complete and T002 ends.
2. T003 card enrichment and the chip deep links, which is the first F032 work
   to touch `apps/` and therefore the design reference.
3. The integration gate, then the closure sequence.

## Risks
- Rule (g) compares outcome keys against the options list in both directions,
  so the pending arm is the first producer where a mis-keyed outcome raises
  rather than merely reading oddly.
- Seven types are enforced from this round on, so a later change that regresses
  any of their triples raises instead of rendering. That is the intent.
