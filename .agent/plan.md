# Plan — F116 Cost anomaly alarm

## Goal
A runaway between checkpoints can no longer burn quietly: one burn detector compares a run's spend
rate with what is expected, a trip warns an attended job and pauses an unattended one with the
arithmetic in the decision, and the watchdog's burn tripwire uses the same detector
(docs/roadmap/features/T3_F116.md). DECISION F116 D1 fixes the slices and their order.

## Current Step
Session 1, round 1: the claim. Branch from `main` at `e80b95467`, mark F116 `[~]` in STATUS,
re-head the review record and book F287's round 17, record DECISION F116 D1 and the slice order,
and save the claim's measurement as `.agent/f116_inventory.md`. No production code.

## Next Steps
1. T001: `packages/orchestration/burn_detector.py`, the pure detector with its window math, floors,
   multiplier and basis labels, and its table tests in `tests/orchestration/test_burn_detector.py`.
2. T002: the job runner calls the detector at its safe point; attended warning, unattended pause
   decision with the arithmetic, one open trip decision per job.
3. T003: the watchdog's burn tripwire calls the detector and its own arithmetic is deleted; docs.
4. The amend0930b-slow-cap hardening stage, then the closure sequence.

## Risks
- The ledger gives every call of one task run the same timestamp, so a window spans whole task
  runs; a run with very few task runs gives the detector little to measure.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162 (Low) stay
  open, owned by F297.
