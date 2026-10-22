# Plan — F074 Estimate calibration

## Goal
Estimates stop being folklore: per task class and role, damped distributions of what tasks really
cost, measured from the cost ledger, replace the configured class defaults in all three consumers of
the shared estimator once a class has enough samples, labelled `calibrated(n)`, while thin classes
stay on their defaults (docs/roadmap/features/T3_F074.md; DECISION F074 D1).

## Current Step
Round 1 (session 1): claim F074, book F113's round 6, and land T001 and T002 — the calibration
module, the resolver's table, the estimator's class argument in its three consumers, their tests
and the page.

## Next Steps
1. T003: `remedy stats calibration` and the plan's band annotation, with the page completed.
2. The closure sequence: the integration gate with its one full suite and a self-use run, the
   evidence round, the closing round.

## Risks
- None of F074's own; the open findings, R-1246 to R-1421, are owned by F314.
