# Plan — F116 Cost anomaly alarm

## Goal
A runaway between checkpoints can no longer burn quietly: one burn detector compares a run's spend
rate with what is expected, a trip warns an attended job and pauses an unattended one with the
arithmetic in the decision, and the watchdog's burn tripwire uses the same detector
(docs/roadmap/features/T3_F116.md). DECISION F116 D1 fixes the slices and their order.

## Current Step
Session 3, round 7: book round 6 and resolve R-1170 and R-1171; then the first part of T003's
second half, DECISION F116 D7: `remedy job show` and the report section show a recorded burn
alarm as its plain sentence through one tolerant reader, and no throttle is built because a job
has no parallel width.

## Next Steps
1. The rest of T003's second half: one run-log event when a new trip is recorded, and the page
   that documents the whole alarm.
2. The amend0930b-slow-cap hardening stage: an acceptance audit by a fresh worker, then repair of
   every gap it finds.
3. The closure sequence.

## Risks
- The trailing baseline needs eight measured calls in one run before it can trip, and samples do
  not survive a stop and relaunch, so a short run is never judged.
- After T003 the agreement tables of `tests/orchestration/test_burn_detector.py` compare the
  detector with the watchdog's translation of it; the watchdog's own literal tests are what hold
  its behaviour.
- F116 owns no open finding. R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157,
  R-1158, R-1162, R-1172 (Low) stay open, owned by F297.
