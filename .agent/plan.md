# Plan — F258 Self-use track v2

Branch: feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge
commit of pull request 225. SESSION 3, round 10.

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
| T001/T002/T003, integration gate | done | rounds 2-7 |
| preconditions 1, 3, 5, 6 | done | rounds 8-9 |
| precondition 4 — Built State section | open | this round |
| evidence job + review zip | open | next round |
| STATUS + README + final PR | open | final round |

## Next Steps
1. Book round 9's own verdict (`Gate: F258 R9`) into
   `.agent/live_review.md`, per amend0827 rule 1.
2. Add one dated line to `.agent/prose_slips.md` recording round 9's
   skipped negative controls (no R-id — process-only, no product
   effect, amend0827 rule 2).
3. Append a `## Built State (F258, 2026-08-30)` section to
   `docs/roadmap/features/T5_F258.md` (precondition 4), summarizing
   T001/T002/T003 as shipped and naming R-0757 as the one open,
   documented risk.
4. `tests/docs/` gates this round (docs/roadmap/** in the change set).
5. The evidence job, the review zip and the final STATUS/README/PR
   commit are the next rounds, not this one.

## Risks
- R-0570 (Low), R-0736 (Medium): OPEN, unrelated to F258's own code.
- R-0757 (Medium): OPEN, this branch's own defect, documented, not
  fixed here.
- No closure candidate is open; `.agent/candidates.md` stays empty.
