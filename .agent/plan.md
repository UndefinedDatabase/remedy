# Plan — F307 Findings paydown v9

## Goal
Pay down the open findings F307 takes at its claim, each by the repair its own text names, with
the evidence that discharged it, and carry R-1246, R-1351 and R-1353 by name to the next paydown
(docs/roadmap/features/T2_F307.md; DECISIONs F307 D1 to D27).

## Current Step
Round 27 (session 6): book round 26 with R-1330; step (1) of `doctor_core_report`, then R-1291,
one check shape, one table and one scrubber for both doctor commands (DECISION F307 D27).

## Next Steps
1. Book round 27 with R-1291 (T007 closed); then R-1326, the `[roles]` table, or its carry to the
   next paydown with the reason.
2. T021, the closing structural step.
3. The closure sequence, which carries R-1281's rest, R-1246, R-1351, R-1353 and R-1418.

## Risks
- Several slices edit functions or files the structure ledger lists; each draws that row's
  boundary first, in a commit of its own, and every edit of a listed file is line-neutral or
  shrinks it.
- A round's selection is every test file that names a touched module by import or by path, and
  every test file that reads a changed page by its path (R-1416, R-1417).
- `packages/orchestration/mission_contract.py` stands at 991 lines, nine below the file limit.
- The guard now reads two levels; a job the installed service runs during a test run turns it red,
  and such a run exports its own `REMEDY_DATA_DIR` (DECISION F307 D25).
