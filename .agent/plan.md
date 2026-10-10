# Plan — F205 Multi-repo missions

## Goal
One order can name several registered projects: the mission plans one job per repository, each
job is applied, committed and pushed in its own repository, every record stays in its own project,
and the digest and the public API name each job's repository
(docs/roadmap/features/T13_F205.md; DECISIONs F205 D1 to D6).

## Current Step
Round 6 on `feature/f205-multi-repo-missions`: book round 5, register and repair R-1236, and the
digest names each job's repository and each mission's projects, client interface 1.9, after the
write routes' builders leave `public_api.py` and one job's digest entry leaves
`build_client_digest` (DECISION F205 D6).

## Next Steps
1. The upkeep across repositories, and the leak regression over mission data.
2. Closure, with the cockpit's chips registered as a follow-up feature.

## Risks
- `mission_state.py` stands at 994 lines with no row; the next round that grows it first takes
  step (2) of its boundary on the structure page.
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219,
  R-1220, R-1225, R-1230 and R-1235 (Low) are open and owned by F297; R-1236 (High) is owned by
  F205 and repaired in round 6.
