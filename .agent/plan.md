# Plan — F307 Findings paydown v9

## Goal
Pay down the open findings F307 takes at its claim, each by the repair its own text names, with
the evidence that discharged it, and carry the rest by name to the next paydown
(docs/roadmap/features/T2_F307.md; DECISIONs F307 D1 to D28).

## Current Step
Round 32 (session 7): the closing round — book round 31, re-assign R-1246, R-1281, R-1326,
R-1351, R-1353 and R-1418 to F314, the Built State, the rotation, F314 registered, F307 accepted
in STATUS with the README sync and SU-073's consumed_by, and the pull request, left unmerged.

## Next Steps
1. The next session: Phase 1 rule 1, then the Open PR Gate merges F307's pull request, then the
   next feature's first commit books round 32's verdict, then Rule A5.

## Risks
- A round's selection is every test file that names a touched module by import or by path, every
  test file that reads a changed page by its path (R-1416, R-1417), and every test that runs a
  recorder over a changed answer (R-1420).
- `packages/orchestration/mission_contract.py` stands at 991 lines, nine below the file limit.
