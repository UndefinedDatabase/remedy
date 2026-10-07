# Plan — F116 Cost anomaly alarm

## Goal
A runaway between checkpoints can no longer burn quietly: one burn detector compares a run's spend
rate with what is expected, a trip warns an attended job and pauses an unattended one with the
arithmetic in the decision, and the watchdog's burn tripwire uses the same detector
(docs/roadmap/features/T3_F116.md). DECISION F116 D1 fixes the slices and their order.

## Current Step
Session 3, round 8: book round 7; then the last part of T003's second half, DECISION F116 D8: a
new trip writes one `job_burn_tripped` run-log event, and `docs/system/cost-anomaly-alarm-v1.md`
documents the whole alarm. With it T001, T002 and T003 are built.

## Next Steps
1. The amend0930b-slow-cap hardening stage: an acceptance audit by a fresh worker given only the
   feature file and the repository, one mutation-proved test per Acceptance and Goal statement,
   at least one proof through the command line.
2. Repair of every gap the audit finds, at most three repair rounds, then the audit repeated for
   the statements that had gaps.
3. The closure sequence.

## Risks
- The trailing baseline needs eight measured calls in one run before it can trip, and samples do
  not survive a stop and relaunch, so a short run is never judged.
- After T003 the agreement tables of `tests/orchestration/test_burn_detector.py` compare the
  detector with the watchdog's translation of it; the watchdog's own literal tests are what hold
  its behaviour.
- F116 owns no open finding. R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157,
  R-1158, R-1162, R-1172 (Low) stay open, owned by F297.
