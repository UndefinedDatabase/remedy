# Plan — F157 Capability matrix & honest degradation

## Goal
A declarative register maps every capability-consuming feature to the capabilities it requires
and to one registered degradation; one central `require_or_degrade` call sits at each usage site;
a per-run `degraded` evidence field, a report section and a UI badge show when a degradation ran;
a guard fails a capability read outside the matrix (`docs/roadmap/features/T8_F157.md`).

## Current Step
Round 1: claim F157, re-head the review record and book F314's round 9, DECISION F157 D1, and
T001 — the inventory of every capability check in the tree, its fallback and its tests, with a
draft register — committed as `.agent/f157_inventory.md` for review.

## Next Steps
1. T002: the matrix module, the evidence field, the guard rules and their unit tests, with the
   register frozen from the reviewed inventory by DECISION F157 D2.
2. T003: one consolidation order per consumer with its existing tests unmodified, the report
   section, the UI badge and the reduced-capability end-to-end.
3. The closure sequence: the integration gate, the evidence package, the STATUS acceptance.

## Risks
- The feature file's suggested design predates F151's contract in `packages/contracts/`; where the
  two disagree, the inventory names it and DECISION F157 D2 decides.
