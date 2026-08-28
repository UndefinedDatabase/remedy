# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 D1 through D8.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the design amendments that reconcile it with the source.

## Current Step
R15 closes T003 and rules its deep link. The evidence panel the feature file
sends the chips to is `docs/roadmap/features/T5_F023.md` T003, and F023 is
unclaimed in `docs/roadmap/STATUS.md`, so F032 ships the ENTRY POINT rather
than a link to nothing: the card takes an optional `onOpenEvidence` handler, a
receipt renders as a control only when one is supplied and as the span R14
shipped when none is, and no ref's `target` reaches the markup either way.
DECISION F032 D8 and amendment A7 record the ruling and how to reverse it.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R14 verdict | ordered | the record is touched first |
| C3 the D8 ruling and the A7 amendment | ordered | |
| C4 the component and its styles | ordered | S2 to S6, one commit |
| C5 the contract guards | ordered | S7 |
| C6 the handback | ordered | |

## Next Steps
1. The integration gate — the full suite, per docs/agents/integration_gate.md.
2. The closure sequence: evidence job, a fresh review zip, the STATUS line and
   the pull request, per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- The card's guards read the `.tsx` as TEXT, and the whole-file counts they
  carry bind every line this round adds as tightly as the markup they were
  written for.
- The handler's arm is unreached today, because nothing supplies the prop. It
  is typechecked and text-pinned, never behaviour-tested, and F023 is the
  feature that first runs it.
