# Plan — F307 Findings paydown v9

## Goal
Pay down the open findings F307 takes at its claim, each by the repair its own text names, with
the evidence that discharged it, and carry R-1246, R-1326, R-1351 and R-1353 by name to the next
paydown (docs/roadmap/features/T2_F307.md; DECISIONs F307 D1 to D28).

## Current Step
Round 30 (session 7): the closure's first repair round (amend0917-throughput rule 2) — book round
29 and R-1420, record the client answers again, and run the closure's one full suite again on the
repaired tree.

## Next Steps
1. The evidence bundle and the review package (a green suite), or the next repair round naming
   every bad node id (a red one; at most three repair rounds).
2. The closing round: the Built State, R-1246, R-1281, R-1326, R-1351, R-1353 and R-1418
   re-assigned to the next findings paydown, the ledger rotation, that paydown registered, the
   STATUS line, the README and the pull request.

## Risks
- A round's selection is every test file that names a touched module by import or by path, every
  test file that reads a changed page by its path (R-1416, R-1417), and every test that runs a
  recorder over a changed answer (R-1420).
- `packages/orchestration/mission_contract.py` stands at 991 lines, nine below the file limit.
- The guard now reads two levels; a job the installed service runs during a test run turns it red,
  and such a run exports its own `REMEDY_DATA_DIR` (DECISION F307 D25).
