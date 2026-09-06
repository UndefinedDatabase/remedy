# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 3 are reviewed; rounds 2 and 3 PASSED. T001
is closed: the inventory is on disk and DECISION F260 D1 and D2 are ruled.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store `<data_root>/task_jobs/<16hex>/job.json` become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

Round 4 is the first production-code round. It ships the three id-minting
functions DECISION F260 D2 rules — `mint_job_id`, `mint_run_id` and
`mint_episode_id`, each a separate `def` returning `uuid4().hex[:16]` — into
`packages/orchestration/data_paths.py`, with a test class that pins the shape,
the freshness, the three-distinct-objects property an alias would break, and the
`UUID()` rejection that is the whole reason the id shapes must converge. A
mutation red-proof in a disposable worktree proves the tests catch a widened
slice.

## Next Steps

- The ONE resolver D2 rules, replacing `resolve_job_id` and `resolve_any_job_id`,
  written while both stores still exist and deleted from its predecessors only in
  T004.
- T002: the extended Mission record, the unified Job record under
  `jobs/<16hex>/` with its evidence beside it, and `runs/<run_id>/` keyed by run
  id. Finding R-0814 is fixed here, because that layout removes the split root.
- T003 consumer by consumer, T004 the classic runner, T005 the reachability test
  and the cluster deletion, in that order.

## Risks

- D1 changes what `<data_root>/runs/` is keyed by, from job id to run id. Every
  reader of the old shape must move in the same commit as its writer, or a run
  log becomes unreadable between two commits.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
