# Plan — F116 Cost anomaly alarm

## Goal
A runaway between checkpoints can no longer burn quietly: one burn detector compares a run's spend
rate with what is expected, a trip warns an attended job and pauses an unattended one with the
arithmetic in the decision, and the watchdog's burn tripwire uses the same detector
(docs/roadmap/features/T3_F116.md). DECISION F116 D1 fixes the slices and their order.

## Current Step
Session 1, round 4: book round 3, resolve R-1165 and R-1166, register R-1167 and repair it; then
T002's wiring, DECISION F116 D4: `run_job` records every counted provider call in the monitor,
reads it at each safe point where no stop fired, keeps the newest trip on the job as
`burn_reading`, and `remedy job budget` shows it, with its documentation.

## Next Steps
1. T002, unattended: a trip pauses an unattended job with one decision carrying the arithmetic,
   and a re-trip updates that decision's evidence; the job report names the trip.
2. T003: the watchdog's burn tripwire calls the detector and its own arithmetic is deleted; docs.
3. The amend0930b-slow-cap hardening stage, then the closure sequence.

## Risks
- The trailing baseline needs eight measured calls in one run before it can trip, and samples do
  not survive a stop and relaunch, so a short run is never judged.
- R-1167 (Low) is F116's own, repaired this round. R-1160 (Medium) and R-1138, R-1139, R-1143,
  R-1149, R-1156, R-1157, R-1158, R-1162 (Low) stay open, owned by F297.
