# Plan — F307 Findings paydown v9

## Goal
Pay down the open findings F307 takes at its claim, each by the repair its own text names, with
the evidence that discharged it, and carry R-1246, R-1326, R-1351 and R-1353 by name to the next
paydown (docs/roadmap/features/T2_F307.md; DECISIONs F307 D1 to D28).

## Current Step
Round 28 (session 6): book round 27 with R-1291; T021, step (3) of `run_job` begun with the final
job review (DECISION F307 D28).

## Next Steps
1. Book round 28 (T021 closed); then the closure sequence, per
   `docs/roadmap/STATUS_closure_protocol.md`, in a session of its own: the one full suite, the
   evidence package, the Built State, the next paydown registered with R-1246, R-1326, R-1351,
   R-1353, R-1418 and R-1281's rest, the ledger rotation and the STATUS flip.

## Risks
- A round's selection is every test file that names a touched module by import or by path, and
  every test file that reads a changed page by its path (R-1416, R-1417).
- `packages/orchestration/mission_contract.py` stands at 991 lines, nine below the file limit.
- The guard now reads two levels; a job the installed service runs during a test run turns it red,
  and such a run exports its own `REMEDY_DATA_DIR` (DECISION F307 D25).
