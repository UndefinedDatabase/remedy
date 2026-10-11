# Plan — F205 Multi-repo missions

## Goal
One order can name several registered projects: the mission plans one job per repository, each
job is applied, committed and pushed in its own repository, every record stays in its own project,
and the digest and the public API name each job's repository
(docs/roadmap/features/T13_F205.md; DECISIONs F205 D1 to D7).

## Current Step
Side task on `feature/ci-manual-dispatch` (operator amend1011-manual-hosted-ci, 2026-10-11): the
hosted CI workflow becomes `workflow_dispatch` only; the local gates stay mandatory. Touches
`ci.yml`, one guard test, AGENTS.md's Open PR Gate and `docs/system/ci-self-check-v1.md`.

## Next Steps
1. The Open PR Gate merges pull request #323 once its hosted checks are read green.
2. The next feature's first commit books `Gate: F205 R10` and `Gate: F205 S4` and the prose slips
   the handoff carries.
3. Rule A5: the next unchecked line in `docs/roadmap/STATUS.md`, F297, Findings paydown v7.

## Risks
- `mission_state.py` stands at 994 lines with no row; the next round that grows it first takes
  step (2) of its boundary on the structure page.
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219,
  R-1220, R-1225, R-1230, R-1235 and, from main, R-1236 to R-1243 are open and owned by F297;
  F205 owns none.
