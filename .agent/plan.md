# Plan — F116 Cost anomaly alarm

## Goal
A runaway between checkpoints can no longer burn quietly: one burn detector compares a run's spend
rate with what is expected, a trip warns an attended job and pauses an unattended one with the
arithmetic in the decision, and the watchdog's burn tripwire uses the same detector
(docs/roadmap/features/T3_F116.md). DECISION F116 D1 fixes the slices and their order.

## Current Step
Session 3, round 6: book round 5 (FAIL on its lint gate), resolve R-1168 and R-1169, register
R-1170 and R-1171 and repair both; then T003's first half, DECISION F116 D6: the watchdog's
`evaluate_burn_anomaly` becomes a translation onto the burn detector's trailing basis, its own
arithmetic is deleted, its trip names its basis, and the watchdog page says so.

## Next Steps
1. T003's second half: the job's report names a recorded trip, and the documentation of the whole
   alarm.
2. The amend0930b-slow-cap hardening stage: an acceptance audit by a fresh worker, then repair of
   every gap it finds.
3. The closure sequence.

## Risks
- The trailing baseline needs eight measured calls in one run before it can trip, and samples do
  not survive a stop and relaunch, so a short run is never judged.
- After T003 the agreement tables of `tests/orchestration/test_burn_detector.py` compare the
  detector with the watchdog's translation of it; the watchdog's own literal tests are what hold
  its behaviour.
- R-1170 and R-1171 (Low) are F116's own, repaired this round. R-1160 (Medium) and R-1138, R-1139,
  R-1143, R-1149, R-1156, R-1157, R-1158, R-1162 (Low) stay open, owned by F297.
