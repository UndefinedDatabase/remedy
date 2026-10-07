# Plan — F116 Cost anomaly alarm

## Goal
A runaway between checkpoints can no longer burn quietly: one burn detector compares a run's spend
rate with what is expected, a trip warns an attended job and pauses an unattended one with the
arithmetic in the decision, and the watchdog's burn tripwire uses the same detector
(docs/roadmap/features/T3_F116.md). DECISION F116 D1 fixes the slices and their order.

## Current Step
Session 1, round 5: book round 4, resolve R-1167, register R-1168 and R-1169 and repair both; then
T002's unattended half, DECISION F116 D5: a job whose plan was approved unattended is paused at the
safe point that reads a new trip, with one `[burn_alarm]` decision carrying the arithmetic and the
options resume and abandon, while an attended job keeps running.

## Next Steps
1. T003: the watchdog's burn tripwire calls the detector and its own arithmetic is deleted; the
   job report names a recorded trip; the documentation of the whole alarm.
2. The amend0930b-slow-cap hardening stage, then the closure sequence.

## Risks
- The trailing baseline needs eight measured calls in one run before it can trip, and samples do
  not survive a stop and relaunch, so a short run is never judged.
- R-1168 and R-1169 (Low) are F116's own, repaired this round. R-1160 (Medium) and R-1138, R-1139,
  R-1143, R-1149, R-1156, R-1157, R-1158, R-1162 (Low) stay open, owned by F297.
