# Plan — F276 Data-root hygiene & disk budget

Branch: feature/f276-data-root-hygiene, cut from `main` at `43d14817`
(the merge commit of pull request 260, F273's closure).

## Goal

Every directory class under the data root has a named owner and a reclaim
rule, an operator reclaims scratch through one preview-first command, and a
job refuses to start below a disk floor
(`docs/roadmap/features/T2_F276.md`).

## Current Step

Round 5 books round 4's verdict, registers R-1003, R-1004 and R-1005, and
repairs R-1003 under DECISION F276 D6: the staging copy is freed by
`job apply` when its work is consumed, never by the completion hook, because
a copy job has no branch and its copy is the deliverable.

## Next Steps

1. T004 — `min_free_disk_bytes` on `JobBudgets` behind an injectable probe,
   the `free_disk` limit inside `evaluate_budget`, the STOPPED path with
   post-mortem status `disk_exhausted`, and a `doctor` disk section. The
   reviewer's dry run of it is built and red-proved.
2. The closure sequence part one: the Built State paragraph, the integrity
   check, the integration gate's one full suite run with its transcript
   committed, and the evidence job with a fresh review package.
3. The closure sequence part two: the STATUS flip with the README counters
   and the pull request into `main`, which the next session's Open PR Gate
   merges.
