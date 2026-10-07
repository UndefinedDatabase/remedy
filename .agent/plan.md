# Plan — F116 Cost anomaly alarm

## Goal
A runaway between checkpoints can no longer burn quietly: one burn detector compares a run's spend
rate with what is expected, a trip warns an attended job and pauses an unattended one with the
arithmetic in the decision, and the watchdog's burn tripwire uses the same detector
(docs/roadmap/features/T3_F116.md). DECISION F116 D1 fixes the slices and their order.

## Current Step
Session 3, round 12, the closure sequence's integration gate: book round 11; build `apps/ui` once,
because this branch changed `apps/ui/src`; then the feature's one full suite,
`python3 -m pytest -n auto -q`, and `scripts/closure_suite_cost.py`, committed as
`.agent/authored/f116-closure-suite.txt`.

## Next Steps
1. Review the transcript: a green suite goes on to the checklist consolidation pass; a red one
   gets a repair round naming every bad node id (amend0917-throughput rule 2).
2. The evidence bundle and the review zip, the ledger rotation, the STATUS line and the pull
   request.

## Risks
- The trailing baseline needs eight measured calls in one run before it can trip, and samples do
  not survive a stop and relaunch, so a short run is never judged.
- F116 owns no open finding. R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157,
  R-1158, R-1162, R-1172 (Low) stay open, owned by F297.
