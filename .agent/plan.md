# Plan — F298 Machine client contract v1.1: what a client can rely on

## Goal
One document generated from the code names every operation, field, word, token and exit code a
program meets when it drives Remedy, and the machine client page is its rendering
(docs/roadmap/features/T12_F298.md, T001). F298 closes at T001's scope; T002 to T007 moved to F304
(DECISION F298 D21).

## Current Step
Session 5, round 22: the hardening stage's audit is saved (sixteen claims, fifteen proved at once,
one gap), and R-1179 and R-1180 are registered and repaired by tests (DECISION F298 D22); round
21's verdict is booked.

## Next Steps
1. Repeat the audit for the claims that had gaps, by a fresh worker; record the stage in F298's
   Built State (operator amendment amend0930b-slow-cap rule 4).
2. The closure sequence (docs/roadmap/STATUS_closure_protocol.md): the one full suite, the
   evidence bundle and review zip, the ledger rotation, the STATUS line, the pull request.

## Risks
- The closure suite is the feature's one full run; a red node there starts the repair rule.
- R-1179 and R-1180 (Low) are F298's own and land this round; R-1160 (Medium) and R-1138, R-1139,
  R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176 (Low) stay open, owned by F297.
