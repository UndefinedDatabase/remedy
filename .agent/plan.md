# Plan — F116 Cost anomaly alarm

## Goal
A runaway between checkpoints can no longer burn quietly: one burn detector compares a run's spend
rate with what is expected, a trip warns an attended job and pauses an unattended one with the
arithmetic in the decision, and the watchdog's burn tripwire uses the same detector
(docs/roadmap/features/T3_F116.md). DECISION F116 D1 fixes the slices and their order.

## Current Step
Session 3, round 9, the hardening stage's first repair round: book round 8 and the acceptance
audit, register R-1173, R-1174 and R-1175 and repair all three, DECISION F116 D9: the burn
decision names `remedy job run` as what continues a burn-paused job, `remedy job budget` shows a
recorded burn alarm on a job with no budgets, and the first trip's whole decision is pinned.

## Next Steps
1. Repeat the acceptance audit for the claims that had gaps, 9b and 23, and for the decision's
   impact; repair what it still finds, at most two more repair rounds.
2. The feature file's Built State paragraph on the audit (amend0930b-slow-cap rule 4).
3. The closure sequence.

## Risks
- The trailing baseline needs eight measured calls in one run before it can trip, and samples do
  not survive a stop and relaunch, so a short run is never judged.
- Answering the burn decision only records the choice; continuing or ending the job stays with
  `remedy job run` and the existing stop, by DECISION F116 D9.
- R-1173, R-1174 and R-1175 (Low) are F116's own, repaired this round. R-1160 (Medium) and
  R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172 (Low) stay open, owned
  by F297.
