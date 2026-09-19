# Plan — F276 Data-root hygiene & disk budget

Branch: feature/f276-data-root-hygiene, cut from `main` at `43d14817`
(the merge commit of pull request 260, F273's closure).

## Goal

Every directory class under the data root has a named owner and a reclaim
rule, an operator reclaims scratch through one preview-first command, and a
job refuses to start below a disk floor
(`docs/roadmap/features/T2_F276.md`).

## Current Step

Round 1 claims F276, re-heads the review record, books F273 round 25's
verdict with the colour of its pull request's hosted CI, registers and
repairs R-1001 — the study dispatch test that reddens that CI — and builds
T001: the data-root class registry, `footprint()` and `remedy data usage`.

## Next Steps

1. T002 — `remedy data reclaim`, dry run by default, `--apply` deleting only
   the paths its own preview named, refusing a non-terminal workspace and
   any path that is not a direct child of a class directory.
2. T003 — the copy-mode lifecycle: `release_staging_workspace(job_id)` on the
   terminal-state hook, a `.gitignore`-aware copy filter and a per-file size
   ceiling, with the release call's removal as the red proof.
3. T004 — `min_free_disk_bytes` on `JobBudgets` behind an injectable probe,
   checked at job start and every safe point, exhaustion taking the STOPPED
   path with post-mortem reason `disk_exhausted`, and a `doctor` disk section.
