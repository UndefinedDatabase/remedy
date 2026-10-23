# Plan — F133 Provider trust score

## Goal
Make "which model earns which work" a rolling, queryable fact: per model and role, the pass quota,
the repair need, the format-error rate and the cost per pass, each with its window and sample size,
in one trust home; `remedy stats trust` shows it, and routing reads it only as a recommendation.

## Current Step
Round 1: claim F133, re-head the review record, DECISION F133 D1, and T001's inventory
`.agent/f133_inventory.md`, reviewed before any code.

## Next Steps
1. T002: the aggregation, its windows and floors, goldens on a constructed history; DECISION F133 D2
   names the module and its sources from the inventory.
2. T003: `remedy stats trust`, the recommendation line, the routing-context note, docs, end-to-end.
3. The closure sequence.

## Risks
- The four metrics may not all have a recorded source today; the inventory says which, and T002
  shows a missing one as missing rather than inventing it.
