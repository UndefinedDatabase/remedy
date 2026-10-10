# Plan — F205 Multi-repo missions

## Goal
One order can name several registered projects: the mission plans one job per repository, each
job is applied, committed and pushed in its own repository, every record stays in its own project,
and the digest and the public API name each job's repository
(docs/roadmap/features/T13_F205.md; DECISIONs F205 D1 to D7).

## Current Step
Round 7 on `feature/f205-multi-repo-missions`: book round 6, and the upkeep of a mission over
several projects works where its next job works, measuring that repository and carrying that
project's findings alone; a regression holds the leak property over a mission's data
(DECISION F205 D7). This is the last building round.

## Next Steps
1. Closure: the checklist's consolidation pass, the closure's self-use item, the one full suite,
   the cockpit's chips registered as a follow-up feature, the evidence and the package, then the
   STATUS line, the ledger rotation and the pull request.

## Risks
- `mission_state.py` stands at 994 lines with no row; the next round that grows it first takes
  step (2) of its boundary on the structure page.
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219,
  R-1220, R-1225, R-1230 and R-1235 (Low) are open and owned by F297; R-1237 (Low) is owned by
  F205 and repaired in round 7.
