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
R14 renders what R13's model carries: the receipts as chips on the card, the
honest note when a card has none, and each answer's expected outcome and
downside under the answer they belong to. It is the first F032 round the
canonical design reference binds, and §17 of its `ux_spec.md` decides the
markup — a ref's scrubbed label is shown, its raw target never is. The
component's existing contract guards read it as text, so this round adds its
own guards rather than leaving new markup unpinned.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R13 verdict | ordered | the record is touched first |
| C3 the component and its styles | ordered | S2 to S5, one commit |
| C4 the contract guards | ordered | S6 |
| C5 the handback | ordered | |

## Next Steps
1. T003c: the chips become deep links into the evidence panel, the slice that
   finally uses the `target` R14 deliberately does not render.
2. The integration gate — the full suite, per docs/agents/integration_gate.md.
3. The closure sequence: evidence job, a fresh review zip, the STATUS line and
   the pull request, per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- The card's guards read the `.tsx` as TEXT, so a class name or an attribute
  carrying the substring `hidden`, or an `aria-live` added after the outcome
  paragraph, turns a guard red for a reason unrelated to what it protects.
- The empty cases are collapsed out of flow rather than removed, because the
  node has to stay in the accessibility tree; that is finding R-0686's lesson
  and the neighbouring rules already carry it.
