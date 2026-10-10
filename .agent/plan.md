# Plan — F205 Multi-repo missions

## Goal
One order can name several registered projects: the mission plans one job per repository, each
job is applied, committed and pushed in its own repository, every record stays in its own project,
and the digest and the public API name each job's repository
(docs/roadmap/features/T13_F205.md; DECISIONs F205 D1 to D7).

## Current Step
Round 10 on `feature/f205-multi-repo-missions`, the closing round: book round 9, the Built State's
closure readings, the ledger rotation, F205 accepted in STATUS with the README sync and `SU-055`'s
`consumed_by`, and the pull request, left unmerged.

## Next Steps
1. The next session: Phase 1 rule 1, then the Open PR Gate merges F205's pull request after its
   hosted checks are read, and round 10's verdict is booked in the next feature's first commit.
2. Rule A5: the next unchecked line in `docs/roadmap/STATUS.md`.

## Risks
- `mission_state.py` stands at 994 lines with no row; the next round that grows it first takes
  step (2) of its boundary on the structure page.
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219,
  R-1220, R-1225, R-1230 and R-1235 (Low) are open and owned by F297; F205 owns none.
