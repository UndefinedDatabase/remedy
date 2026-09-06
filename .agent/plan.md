# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 9 are reviewed and 2 to 9 PASSED. T001 is
CLOSED. T002 is open: the record has MOVED and finding R-0814 is resolved; what
remains of T002 is the one resolver over it.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store, now `<data_root>/jobs/<16hex>/job.json`, become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

THE RESOLVER RETURNS A STRING. `data_paths.resolve_job_id` is annotated and
returns `str` instead of `UUID`, and `storage.load_job` / `load_job_safe` accept
either. DECISION F260 D4 named this the one thing standing between the two
resolvers and a collapse into one. Measured in a worktree before the round: the
change costs FIVE tests, every one asserting the return type, and ZERO
production call sites, because `load_job` formats its path from the id.

## Next Steps

- COLLAPSE the two resolvers into one, now that they share a return type: one
  `str`-returning function over both stores, the loser deleted in the same
  commit. Finding R-0809 — four wordings for "unknown id", and a real id of the
  other store rejected — belongs here.
- Then `runs/<run_id>/` keyed by run id, replacing `pingpong_runs/`.
- Then T003 consumer by consumer, T004 the classic runner and the classic
  store, T005 the reachability test and the cluster deletion.

## Risks

- Widening what `resolve_job_id` accepts changes an ERROR path: an id of the
  other store today exits 1 with "no job matches prefix" and would instead
  reach `load_job` and raise. That is R-0809's territory and needs its own test.
- D1 changes what `<data_root>/runs/` is keyed by, from job id to run id. Every
  reader of the old shape must move in the same commit as its writer.
- `<data_root>/jobs/` holds both `<uuid>.json` files and `<16hex>/` directories.
  Any new reader of that directory must make the same file/directory
  distinction the two matchers make.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
