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
R9 closes session 2. It upgrades the stop-reason producer, which copied a
structured record into a card and cited none of its identifiers, and it
registers and fixes `R-0713`: the patch-approval summary's `'?'` default can
never fire, because `list_patch_intents` always sets `target_path` and leaves
it EMPTY rather than absent, so an intent naming no file rendered a card with
no subject at all. Four of the eight producing types are enforced after this
round.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R8 verdict and R-0713 | ordered | findings persist before repair |
| C3 the R-0713 fix | ordered | S2, one line |
| C4 the stop-reason triple and the gate set | ordered | S3 to S5 |
| C5 its tests | ordered | S6, then the red-proofs |
| C6 the session-closing handback | ordered | |

## Next Steps
1. Next session: re-read `.agent/STOP` from disk, then the Open PR Gate, then
   author `Done: R-0713` against the fix this round landed.
2. T002 finishes with memory-review, repo-dirty and the two branches that
   already carry an options list. Repo-dirty's event carries the thinnest
   evidence of the eight; the flight plan has two arms and only one offers
   options, so enforcing that type needs a ruling on what a RESOLVED decision
   owes.
3. T003 card enrichment and the chip deep links, then the integration gate.

## Risks
- `R-0713` is fixed in code but stays OPEN in the record until a reviewer
  authors its `Done:` text.
- Four types are enforced from this round on, so a later change that regresses
  any of their triples raises instead of rendering. That is the intent.
