# Plan — F116 Cost anomaly alarm

## Goal
A runaway between checkpoints can no longer burn quietly: one burn detector compares a run's spend
rate with what is expected, a trip warns an attended job and pauses an unattended one with the
arithmetic in the decision, and the watchdog's burn tripwire uses the same detector
(docs/roadmap/features/T3_F116.md). DECISION F116 D1 fixes the slices and their order.

## Current Step
Session 3, round 13, the closure sequence's last content round: book round 12, whose one full
suite was green, and the once-per-feature consolidation pass of the pre-emission checklist in
`docs/agents/planner_reviewer_prompt.md`, which stays at 34 items. The session ends after this
round, so that the evidence round starts in a fresh one.

## Next Steps
1. The evidence round: the feature's evidence bundle, the staging-copy reclaim and the fresh
   review zip (docs/roadmap/STATUS_closure_protocol.md, algorithm steps 1 and 2).
2. The closing round: the ledger rotation, the STATUS line, the README sync, the self-use item's
   `consumed_by`, and the pull request, which the next feature's Open PR Gate merges.

## Risks
- The trailing baseline needs eight measured calls in one run before it can trip, and samples do
  not survive a stop and relaunch, so a short run is never judged.
- F116 owns no open finding. R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157,
  R-1158, R-1162, R-1172 (Low) stay open, owned by F297.
