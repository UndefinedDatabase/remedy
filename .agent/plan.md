# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 8 are reviewed and 2 to 8 PASSED. T001 is
CLOSED. T002 is open, and this round is its centre: the ping-pong record moves
to the root DECISION F260 D1 rules.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store `<data_root>/task_jobs/<16hex>/job.json` become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

THE RECORD MOVE. `data_paths.task_job_dir` and `task_job_record_path` are
deleted and `pingpong_job._persist_job` writes through `job_record_path`, so
`<data_root>/task_jobs/<16hex>/job.json` becomes
`<data_root>/jobs/<16hex>/job.json` and a job's record and its evidence share
one root. `data_paths._task_job_id_matches` moves onto `jobs_dir()` in the SAME
commit, or every ping-pong job becomes unresolvable. Finding R-0814's remaining
fix conditions — one root, and a test asserting it — are discharged here.

## Next Steps

- The ONE resolver over the one store: `resolve_job_id` and `resolve_any_job_id`
  collapse into one `str`-returning function, which needs `storage.load_job`'s
  signature and its forty call sites across nine `apps/cli/commands/` modules
  (DECISION F260 D4). Finding R-0809 belongs to that step.
- Then `runs/<run_id>/` keyed by run id, replacing `pingpong_runs/`.
- Then T003 consumer by consumer, T004 the classic runner, T005 the
  reachability test and the cluster deletion.

## Risks

- D1 changes what `<data_root>/runs/` is keyed by, from job id to run id. Every
  reader of the old shape must move in the same commit as its writer.
- `pingpong_job` imports `data_paths` only inside function bodies, so each call
  site carries its own import; one such site sits inside a compound boolean.
- `<data_root>/jobs/` now holds both `<uuid>.json` files and `<16hex>/`
  directories. The two matchers were measured not to see each other's entries,
  but any new reader of that directory must make the same distinction.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
