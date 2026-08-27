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
R10 opens session 3 with the two producers that cite nothing at all: the
dirty-repo card, whose whole evidence is one run-log event, and the
memory-review card, which names a key and states a reason it never cites. Both
branches are optionless, so each owes exactly one unkeyed outcome. The round
also books the R9 verdict and writes the `Done:` text for `R-0713`, fixed in
code at R9 and open in the record since. Six of the eight producing types are
enforced when it ends.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R9 verdict and `Done: R-0713` | ordered | the record is touched first |
| C3 the repo-dirty triple and its gate entry | ordered | S2 and S3 |
| C4 the memory-review triple and its gate entry | ordered | S4 and S5 |
| C5 the tests, and the two guards C4 falsifies | ordered | S6 and S7 |
| C6 the handback | ordered | |

## Next Steps
1. The flight-plan approval, whose PENDING arm carries `payload["options"]`
   while its RESOLVED arm carries none. The emit gate does not branch on
   status, so enforcing that type needs a ruling on what a resolved card owes.
2. The task decision, whose options come from the escalation record and are
   arbitrary, so its outcomes are built per option rather than written out.
   With it the gate set is complete and T002 ends.
3. T003 card enrichment and the chip deep links, then the integration gate.

## Risks
- Two tests in `tests/orchestration/test_decision_evidence.py` use
  `memory_review` as their example of an UNENFORCED type. C4 makes that false
  and C5 repoints both, so the pair has to land in one round.
- Six types are enforced from this round on, so a later change that regresses
  any of their triples raises instead of rendering. That is the intent.
