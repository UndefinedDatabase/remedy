# Plan — F116 Cost anomaly alarm

## Goal
A runaway between checkpoints can no longer burn quietly: one burn detector compares a run's spend
rate with what is expected, a trip warns an attended job and pauses an unattended one with the
arithmetic in the decision, and the watchdog's burn tripwire uses the same detector
(docs/roadmap/features/T3_F116.md). DECISION F116 D1 fixes the slices and their order.

## Current Step
Session 1, round 3: book round 2 and register R-1165 and R-1166; repair both in the detector's
tests and docstring; then T002's first part, DECISION F116 D3: `packages/orchestration/job_burn.py`
with `JobBurnMonitor`, its configuration resolver and record shape, the five `job_burn.*` keys, the
regenerated environment guide, and its tests. Nothing calls the monitor yet.

## Next Steps
1. T002, wiring: `run_job` records each counted provider call in the monitor, evaluates at its safe
   point, persists a tripped reading on the job and shows it in `remedy job budget`.
2. T002, unattended: a trip pauses an unattended job with one decision carrying the arithmetic.
3. T003: the watchdog's burn tripwire calls the detector and its own arithmetic is deleted; docs.
4. The amend0930b-slow-cap hardening stage, then the closure sequence.

## Risks
- The trailing baseline needs eight measured calls in one run before it can trip, and samples do
  not survive a stop and relaunch, so a short run is never judged.
- R-1165 and R-1166 (Low) are F116's own, repaired this round. R-1160 (Medium) and R-1138, R-1139,
  R-1143, R-1149, R-1156, R-1157, R-1158, R-1162 (Low) stay open, owned by F297.
