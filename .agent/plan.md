# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 D1 through D5.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the design amendments that reconcile it with the source.

## Current Step
R5 closes session 1. It books the reviewer's verdicts on R2, R3 and R4, all
PASS, and registers and fixes `R-0711`: `R-0710`'s repair finally let memory
cards flagged `needs_review` reach the inbox, and they arrived under a summary
reporting their VALIDITY, so a card surfaced for review announced itself as
active. T001 is complete after this round — the schema, the emit gate, the
legacy placeholder and the canary are all on disk and pinned.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 three verdicts and R-0711 | ordered | findings persist before repair |
| C3 the summary fix | ordered | S1 through S3 |
| C4 its tests | ordered | S4, then the red-proof |
| C5 the Landed line | ordered | worker's only record text |
| C6 the handback | ordered | session-closing |

## Next Steps
1. Next session: re-read `.agent/STOP` from disk, then the Open PR Gate, then
   author `Done: R-0711` against the fix this round landed.
2. T002: upgrade the producers one at a time, adding each type to
   `TRIPLE_REQUIRED_TYPES` only once its triple is real, with the content
   goldens and the anti-boilerplate assertions.
3. T003 card enrichment and the chip deep links, then the integration gate.

## Risks
- `R-0711` is fixed in code but stays OPEN in the record until a reviewer
  authors its `Done:` text; the `Landed:` line is what says so on disk.
- `TRIPLE_REQUIRED_TYPES` is still empty, so the gate protects nothing in
  production yet. That is by design and T002 is what closes it.
