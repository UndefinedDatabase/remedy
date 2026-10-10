# Plan — F301 Mission upkeep: every fifth job cleans up

## Goal
A mission keeps its project clean by itself: after every fifth completed job, the next job is an
upkeep job Remedy plans from its own records — the findings earlier jobs left open, the project's
structure measure, and what was replaced and not deleted — by rules a person can read, with a skip
only as a recorded decision (docs/roadmap/features/T7_F301.md; DECISIONs F301 D1 to D5).

## Current Step
Round 8 on `feature/f301-mission-upkeep`: book round 7, then the acceptance fixture of six jobs
through the command line, `tests/regression/test_f301_acceptance.py`, and the feature file's Built
State with the mission upkeep page marked built. Session 1 ends after this round; the closure
starts fresh.

## Next Steps
1. The closure's first round, in a new session: the consolidation of the §3 checklist, the
   self-use item run to its approval gate, and the one full suite on the tree that ships.
2. The evidence round: the evidence job and the review package.
3. The closing round: the Built State's readings, the ledger rotation, the STATUS line, the README
   sync and the pull request.

## Risks
- The structure ratchet holds every round: no line may be added to a listed function or file.
- The closure suite runs once, in the primary checkout; a red node is this feature's to repair.
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219,
  R-1220, R-1225 and R-1230 (Low) are open and owned by F297.
