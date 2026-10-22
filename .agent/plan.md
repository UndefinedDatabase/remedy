# Plan — F074 Estimate calibration

## Goal
Estimates stop being folklore: per task class and role, damped distributions of what tasks really
cost, measured from the cost ledger, replace the configured class defaults in all three consumers of
the shared estimator once a class has enough samples, labelled `calibrated(n)`, while thin classes
stay on their defaults (docs/roadmap/features/T3_F074.md; DECISIONs F074 D1 and D2).

## Current Step
Round 2 (session 1): book round 1, and land T003 — `remedy stats calibration`, the calibrated
midpoint beside a band in `remedy job plan-show`, their tests and the page completed.

## Next Steps
1. The closure sequence: the integration gate with its one full suite and a self-use run, the
   evidence round, the closing round.

## Risks
- None of F074's own; the open findings, R-1246 to R-1421, are owned by F314.
