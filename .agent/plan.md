# Plan — F307 Findings paydown v9

## Goal
Pay down the open findings F307 takes at its claim, each by the repair its own text names, with
the evidence that discharged it, and carry R-1246, R-1351 and R-1353 by name to the next paydown
(docs/roadmap/features/T2_F307.md; DECISIONs F307 D1 to D21).

## Current Step
Round 21 (session 5): book round 20 with R-1417 and R-1323 (T015 closed); T016's first half,
R-1332: a job a run leaves blocked keeps the time it ended (DECISION F307 D21).

## Next Steps
1. Book round 21 with R-1332; then R-1331, the retry of a blocked task, after its three structural
   steps (DECISION F307 D21 (3)): step (1) of `_cmd_job_run`'s boundary, the next group of
   `command_catalog.py` and the next step of `public_api.py`, each in a commit of its own.
2. T017 to T020, each with its structural step first where a listed function or file is touched
   (DECISION F307 D5); R-1291 with `doctor_core_report`'s boundary.
3. T021, the closing structural step; then the closure sequence, which carries R-1281's rest.

## Risks
- Several slices edit functions or files the structure ledger lists; each draws that row's
  boundary first, in a commit of its own, and every edit of a listed file is line-neutral or
  shrinks it.
- A round's selection is every test file that names a touched module by import or by path, and
  every test file that reads a changed page by its path (R-1416, R-1417).
- `packages/orchestration/mission_contract.py` stands at 991 lines, nine below the file limit.
- The operator's live service writes the data root the test guard watches (R-1411, T019).
