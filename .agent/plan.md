# Plan — F116 Cost anomaly alarm

## Goal
A runaway between checkpoints can no longer burn quietly: one burn detector compares a run's spend
rate with what is expected, a trip warns an attended job and pauses an unattended one with the
arithmetic in the decision, and the watchdog's burn tripwire uses the same detector
(docs/roadmap/features/T3_F116.md). DECISION F116 D1 fixes the slices and their order.

## Current Step
Session 3, round 11, the closure sequence's first round: book round 10; then the self-use item of
closure precondition 6, generated into `scripts/self_use_queue.json` and run to its approval gate
through `run_next_self_use_item`, never applied, its record saved under `.agent/selfuse_f116/`.

## Next Steps
1. Review the self-use run and register every defect `describe_self_use_run_defects` names.
2. The integration gate: the feature's one full suite, its transcript and its cost lines.
3. The checklist consolidation pass, the evidence bundle and the review zip, the ledger rotation,
   the STATUS line and the pull request.

## Risks
- The self-use run spends real money on the configured frontier provider, at most the budget its
  role and item declare.
- The trailing baseline needs eight measured calls in one run before it can trip, and samples do
  not survive a stop and relaunch, so a short run is never judged.
- F116 owns no open finding. R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157,
  R-1158, R-1162, R-1172 (Low) stay open, owned by F297.
