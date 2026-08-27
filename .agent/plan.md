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
T002 is COMPLETE: all eight producing types carry real triples and the emit
gate is fully live. R13 opens T003 on the browser side, where nothing has read
`evidence_refs`, `outcomes` or `evidence_status` since T001b put them on the
wire. It projects all three in `apps/ui/src/api/decisionCard.ts` — the layer
DECISION F031 D5 puts all branching in — and attaches each option's outcome to
ITS OWN answer. No `.tsx` and no CSS this round.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R12 verdict | ordered | the record is touched first |
| C3 the model and its types | ordered | S2 to S7 |
| C4 its tests | ordered | S8 |
| C5 the handback | ordered | |

## Next Steps
1. T003b: the card component projects what the model now carries — chips for
   the refs, each option's outcome and downside under its own answer. It is
   the round that touches `.tsx` and CSS, so it is bound by the canonical
   design reference, and it must first read the source-counting guards in
   `tests/ui_contracts/test_decision_answer_wiring.py`.
2. T003c: the chips deep-link into the evidence panel.
3. The integration gate, then the closure sequence.

## Risks
- §17 of `docs/ui/design_reference/ux_spec.md` forbids the UI to show raw ids
  or present/missing signals, and a ref's `target` is often exactly a raw id.
  The model therefore decides the display text and routes it through
  `scrubUiText`; a renderer that reached for `target` instead would reintroduce
  the leak the model exists to prevent.
- The model is the only layer the shipped vitest config can cover, so keeping
  the component out of this round is what makes every line of it testable.
