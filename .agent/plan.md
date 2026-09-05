# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). F259 is accepted and its page
`docs/system/vocabulary.md` is binding for every name this feature introduces.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store `<data_root>/task_jobs/<16hex>/job.json` become one record with
one id shape minted by one function; a Run becomes the evidence case a Job
points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 the records and writers, T003 the consumers, T004 the classic
runner, T005 the reachability test and the cluster deletion.

## Current Step

Round 1 claims F260, books the F259 R10 verdict into the review record, and
writes `.agent/f260_inventory.md` — the measured reading of every job, run and
evidence area on disk, both job record shapes, every id shape minted, and the
re-grepped consumer list. It rules nothing: DECISION F260 D1 and D2 are ruled in
round 2 from this measurement.

## Next Steps

- Rule DECISION F260 D1 (where the classic job fields live) and D2 (the one id
  shape) from the inventory, and settle where a Run's evidence lives now that
  `<data_root>/runs/` is measured as already occupied by the run log.
- Write the one minting and resolving function, and move every job-taking
  command onto it while both stores still exist (T001, part 2).
- T002: the extended Mission record, the unified Job record, the run directory.

## Risks

- The feature file orders `task_jobs/` "renamed to `runs/`" onto a path the run
  log already writes. Round 1 records the collision; round 2 must rule it before
  any directory moves, or the rename silently merges two keyspaces — one keyed
  by job id, one by run id.
- The prototype cluster deletion (T005) is large and irreversible in one
  direction only. It runs last, behind a reachability test that is green BEFORE
  the first `git rm`.
