# Plan — F276 Data-root hygiene & disk budget

Branch: feature/f276-data-root-hygiene, cut from `main` at `43d14817`
(the merge commit of pull request 260, F273's closure).

## Goal

Every directory class under the data root has a named owner and a reclaim
rule, an operator reclaims scratch through one preview-first command, and a
job refuses to start below a disk floor
(`docs/roadmap/features/T2_F276.md`).

## Current Step

Round 6 books round 5's verdict, resolves R-1003, and builds T004 under
DECISION F276 D7: `min_free_disk_bytes` on `JobBudgets` behind an injected
probe, the floor read inside `evaluate_budget` so all four safe points
reach it, the STOPPED path with post-mortem status `disk_exhausted`, and a
`doctor` disk section. T001 to T004 are then built.

## Next Steps

1. The closure sequence part one: the Built State paragraph naming what each
   slice built and what is carried, the integrity check, and the integration
   gate's one full suite run with its transcript committed as
   `.agent/authored/f276-closure-suite.txt`.
2. The closure sequence part two: the evidence job and a fresh review
   package, then the STATUS flip with the README counters and the pull
   request into `main`, which the next session's Open PR Gate merges.
3. R-1004 and R-1005 stay open and owned by F282; R-0984's hosted-CI reading
   is answered by the first CI run of this feature's own pull request.
