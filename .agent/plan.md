# Plan — F116 Cost anomaly alarm

## Goal
A runaway between checkpoints can no longer burn quietly: one burn detector compares a run's spend
rate with what is expected, a trip warns an attended job and pauses an unattended one with the
arithmetic in the decision, and the watchdog's burn tripwire uses the same detector
(docs/roadmap/features/T3_F116.md). DECISION F116 D1 fixes the slices and their order.

## Current Step
Session 3, round 10, the end of the hardening stage: book round 9 and the repeat audit, resolve
R-1173, R-1174 and R-1175, and write the feature file's Built State with the stage's record
(amend0930b-slow-cap rule 4, closure preconditions 4, 7 and 8).

## Next Steps
1. The closure sequence (docs/roadmap/STATUS_closure_protocol.md): the self-use run of
   precondition 6, then the integration gate's one full suite, then the checklist consolidation
   pass, then the evidence bundle and the review zip, then the closing round with the ledger
   rotation, the STATUS line and the pull request.

## Risks
- The trailing baseline needs eight measured calls in one run before it can trip, and samples do
  not survive a stop and relaunch, so a short run is never judged.
- Answering the burn decision only records the choice; continuing or ending the job stays with
  `remedy job run` and the existing stop, by DECISION F116 D9.
- F116 owns no open finding. R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157,
  R-1158, R-1162, R-1172 (Low) stay open, owned by F297.
