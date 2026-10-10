# Plan — F205 Multi-repo missions

## Goal
One order can name several registered projects: the mission plans one job per repository, each
job is applied, committed and pushed in its own repository, every record stays in its own project,
and the digest and the public API name each job's repository
(docs/roadmap/features/T13_F205.md; DECISIONs F205 D1 to D3).

## Current Step
Round 3 on `feature/f205-multi-repo-missions`: book round 2, and the structural steps the walk
over several projects needs first — the walk's context, targets, cockpit, apply and push and
summaries leave `do_sequence.py`, and what `remedy do` reads before any step leaves `do_cmd.py`
(DECISION F205 D3); no behaviour changes.

## Next Steps
1. The order file names several projects; `remedy do` plans one job per repository, and each job
   is applied, committed and pushed in its own repository; an unreachable one ends the walk
   honestly.
2. The loop switches project per job.
3. The digest and the public API name each job's repository; a mission answers references only.
4. The upkeep across repositories; the fixture mission over two repositories; the leak regression.
5. Closure, with the cockpit's chips registered as a follow-up feature.

## Risks
- `mission_state.py` stands at 991 lines with no row; the next round that grows it first takes
  step (2) of its boundary on the structure page.
- `orchestrator_loop.py`, `job_apply.py` and `public_api.py` are on the structure page; each round
  that touches one moves code out first.
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219,
  R-1220, R-1225, R-1230 and R-1235 (Low) are open and owned by F297; F205 owns none.
