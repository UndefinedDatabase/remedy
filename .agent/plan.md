# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 7 are reviewed; 2 through 7 PASSED. T001 is
CLOSED. T002 is open: `data_paths` holds the one spelling of DECISION F260 D1's
target layout, every evidence path is built from it, and DECISION F260 D4 records
why the resolver waits for the store.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store `<data_root>/task_jobs/<16hex>/job.json` become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

Give the PING-PONG store one spelling too. `data_paths` gains `task_job_dir` and
`task_job_record_path`, mirroring the D1 pair; `pingpong_job._jobs_dir` is
DELETED and its six users, `job_evidence`'s cross-module import of it, and
seventeen test call sites across seven files all move onto the accessors. The
store does not move: only its spelling changes, so the record move that follows
is a change to two function bodies rather than a sweep of every caller.

## Next Steps

- The record move itself: `task_job_dir` and `task_job_record_path` collapse into
  `job_dir` and `job_record_path`, so `<data_root>/task_jobs/<16hex>/job.json`
  becomes `<data_root>/jobs/<16hex>/job.json`. `data_paths._task_job_id_matches`
  moves with it, in the same commit, or every ping-pong job becomes unresolvable.
  Finding R-0814 is resolved there, against the fix clause it carries.
- The ONE resolver, in the same round group as that move, because 40 of the 42
  job-taking call sites take a `UUID` today (DECISION F260 D4).
- Then `runs/<run_id>/` keyed by run id, T003 consumer by consumer, T004 the
  classic runner, T005 the reachability test and the cluster deletion.

## Risks

- D1 changes what `<data_root>/runs/` is keyed by, from job id to run id. Every
  reader of the old shape must move in the same commit as its writer.
- `pingpong_job` imports `data_paths` only inside function bodies, so each call
  site carries its own import; one such site sits inside a compound boolean and
  is easy to miss.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
