# Plan — F205 Multi-repo missions

## Goal
One order can name several registered projects: the mission plans one job per repository, each
job is applied, committed and pushed in its own repository, every record stays in its own project,
and the digest and the public API name each job's repository
(docs/roadmap/features/T13_F205.md; DECISIONs F205 D1 to D4).

## Current Step
Round 4 on `feature/f205-multi-repo-missions`: book round 3, and the walk over several projects —
the order file names one project per `project` line; `remedy do` plans one job in each project's
repository under one mission, applies and commits each in its own repository and pushes each
repository once; client interface 1.8 (DECISION F205 D4).

## Next Steps
1. The loop switches project per job.
2. The digest and the public API name each job's repository; a mission answers references only.
3. The upkeep across repositories; the fixture mission over two repositories; the leak regression.
4. Closure, with the cockpit's chips registered as a follow-up feature.

## Risks
- `mission_state.py` stands at 991 lines with no row; the next round that grows it first takes
  step (2) of its boundary on the structure page.
- `orchestrator_loop.py`, `job_apply.py` and `public_api.py` are on the structure page; each round
  that touches one moves code out first.
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219,
  R-1220, R-1225, R-1230 and R-1235 (Low) are open and owned by F297; F205 owns none.
