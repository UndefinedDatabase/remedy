# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Round 1 committed C0a, C0b, C1 and C2 correctly and
stopped at a red gate whose two causes were both defects in the reviewer's own
block; those commits are kept and round 2 repairs the record and finishes the
work round 1 could not reach.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store `<data_root>/task_jobs/<16hex>/job.json` become one record with
one id shape minted by one function; a Run becomes the evidence case a Job
points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

Round 2 restores the one byte round 1's block cost the review record, books
round 1's verdict and the reviewer's two authoring slips, claims F260 in the
STATUS ledger, and writes `.agent/f260_inventory.md` — the measured reading of
every job, run and evidence area on disk, both job record shapes, every id shape
minted, and the re-grepped consumer list. It rules nothing.

## Next Steps

- Rule DECISION F260 D1 (where the classic job fields live) and D2 (the one id
  shape) from the inventory, and settle where a Run's evidence lives now that
  `<data_root>/runs/` is measured as already occupied by the run log.
- Write the one minting and resolving function and move every job-taking command
  onto it while both stores still exist (T001, part 2).
- T002: the extended Mission record, the unified Job record, the run directory.

## Risks

- The feature file orders `task_jobs/` "renamed to `runs/`" onto a path the run
  log already writes. The collision is recorded before anything moves; ruling it
  is round 3's first job.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
