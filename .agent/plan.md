# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 4 are reviewed; 2, 3 and 4 PASSED. T001's
inventory is on disk, DECISION F260 D1 and D2 are ruled, and the three minting
functions ship in `packages/orchestration/data_paths.py`.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store `<data_root>/task_jobs/<16hex>/job.json` become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

Finish T001's minting half at the CALL SITES. The four inline `uuid4().hex[:16]`
mints that name a job, a run or an episode move onto the shipped functions:
`JobPlan.job_id` and both `active_episode_id` assignments in `pingpong_job.py`,
and `PingPongResult.run_id` in `pingpong_loop.py`. Both modules stop naming
`uuid4` at all. A new guard test pins the two dataclass defaults by OBJECT
IDENTITY, which a look-alike lambda cannot satisfy, and parses the module for
the two episode sites, which have no object to compare.

## Next Steps

- The ONE resolver D2 rules, replacing `resolve_job_id` and `resolve_any_job_id`,
  written while both stores still exist and deleted from its predecessors only in
  T004.
- T002: the extended Mission record, the unified Job record under
  `jobs/<16hex>/` with its evidence beside it, and `runs/<run_id>/` keyed by run
  id. Finding R-0814 is fixed there, because that layout removes the split root.
- T003 consumer by consumer, T004 the classic runner, T005 the reachability test
  and the cluster deletion, in that order.

## Risks

- D1 changes what `<data_root>/runs/` is keyed by, from job id to run id. Every
  reader of the old shape must move in the same commit as its writer, or a run
  log becomes unreadable between two commits.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
