# Plan — F258 Self-use track v2

Branch: feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge
commit of pull request 225. SESSION 1, round 2.

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
| the F040 closure candidate | done | round 1 |
| the F258 claim and the seam inventory | done | round 1 |
| T001 part 1 — schema v2, the provenance field | done | this round |
| T001 part 2 — the generator module | open | next round |
| T002 consumed means executed | open | |
| T003 findings flow back | open | |

## Next Steps
1. This round bumps the self-use queue schema to v2 (DECISION F258 D1): a
   required `provenance` field joins the five existing keys, the shipped
   queue's four items are migrated in the same commit range, and both test
   files plus the two describing docs are kept in step.
2. The round after it builds `packages/orchestration/self_use_generator.py`,
   the source-priority search itself, using round 1's inventory finding that
   no code caller of `plan_next_self_use_item` exists today.
3. T002 depends on T001 producing a real item to run against; T003 wires
   existing finding-ledger machinery once T002 exists.

## Risks
- R-0570 (Low) stays OPEN, routed away, unrelated to this branch.
- The version check stays an EXACT match, not a range (DECISION F258 D1): a
  v1-shaped file is refused after this round, by design, symmetric with the
  existing "a file from the future is refused" rule.
