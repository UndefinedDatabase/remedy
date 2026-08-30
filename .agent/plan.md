# Plan — F258 Self-use track v2

Branch: feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge
commit of pull request 225. SESSION 3, round 9.

## Goal
"Remedy is used on Remedy" keeps running with zero operator input: a generator
replenishes the self-use queue with exactly one dated, provenanced item
whenever it is empty at close, the consumed item is actually RUN through the
real job path under a small budget and stopped at the normal approval gate
rather than only planned, and any defect the run surfaces flows back into the
standard finding ledger.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001/T002/T003 | done | rounds 2-6 |
| integration-gate round | done | round 7 |
| precondition 6 — plan + run for real | done | round 8 |
| preconditions 1, 3, 5 | open | this round |
| precondition 4 — Built State section | open | next round |
| evidence job + review zip | open | next round |
| STATUS + README + final PR | open | final round |

## Next Steps
1. Register R-0757 (Medium — self-use runner silently resolves a fake
   provider by default) in `.agent/live_review.md`, own commit, before
   any verdict text — the finding round 8's real run surfaced.
2. Book round 8's own verdict (`Gate: F258 R8`) into the same file, per
   amend0827 rule 1.
3. Re-confirm preconditions 3 and 5 after this round's own edits
   (integrity check, tree/push state); precondition 1's closure-scoped
   reading: every F258-scoped open finding is Medium/Low (R-0570,
   R-0736, R-0757) — none Blocker/High.
4. Precondition 4, the evidence job, the review zip and the final
   STATUS/README/PR commit are the next rounds, not this one.

## Risks
- R-0570 (Low), R-0736 (Medium): OPEN, unrelated to F258's own code.
- R-0757 (Medium): OPEN, this branch's own defect, documented under
  this closure's PASS WITH RISKS reading, not fixed here.
- No closure candidate is open; `.agent/candidates.md` stays empty.
