# Plan — F116 Cost anomaly alarm

## Goal
A runaway between checkpoints can no longer burn quietly: one burn detector compares a run's spend
rate with what is expected, a trip warns an attended job and pauses an unattended one with the
arithmetic in the decision, and the watchdog's burn tripwire uses the same detector
(docs/roadmap/features/T3_F116.md). DECISION F116 D1 fixes the slices and their order.

## Current Step
Session 1, round 2: T001. Book round 1, then build `packages/orchestration/burn_detector.py` as
DECISION F116 D2 specifies, a pure function with a per-sample trailing basis and a per-hour class
basis, with its table tests in `tests/orchestration/test_burn_detector.py` and its entry in the
orphan-module guard's `ALLOWED_UNWIRED`.

## Next Steps
1. T002: the job runner calls the detector at its safe point; attended warning, unattended pause
   decision with the arithmetic, one open trip decision per job; the configuration keys; the
   `ALLOWED_UNWIRED` entry removed.
2. T003: the watchdog's burn tripwire calls the detector and its own arithmetic is deleted; docs.
3. The amend0930b-slow-cap hardening stage, then the closure sequence.

## Risks
- The ledger gives every call of one task run the same timestamp, so a window spans whole task
  runs; a run with very few task runs gives the detector little to measure.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162 (Low) stay
  open, owned by F297.
