# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 10 are reviewed and 2 to 10 PASSED. T001 is
CLOSED. T002 is open: the job record has MOVED, R-0814 is resolved, and both
resolvers now return `str`.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store, now `<data_root>/jobs/<16hex>/job.json`, become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

ONE SPELLING FOR THE RUN STORE. `data_paths` gains `pingpong_runs_dir` and
`pingpong_run_dir`, and `pingpong_loop._pingpong_runs_dir` is DELETED with its
thirty-nine production references and its test references moved onto the pair.
The store does NOT move: only its spelling changes, so D1's collapse into
`<data_root>/runs/<run_id>/` becomes two function bodies. DECISION F260 D5 is
recorded in the same round, moving the resolver collapse to T004.

## Next Steps

- The run move itself: `pingpong_runs_dir` and `pingpong_run_dir` collapse into
  `runs_dir` and `run_dir`. The run LOG at `<data_root>/runs/<job_id>/` must
  move to the run id in the same commit, or `timeline.load_run_events` reads a
  directory keyed two ways — DECISION F260 D0 measured that collision.
- The unified record's own fields, and the Mission extension (order, contract,
  mission plan, job refs), which is the rest of T002.
- Then T003 consumer by consumer; T004 the classic runner, the classic store and
  the resolver collapse together (DECISION F260 D5); T005 the reachability test
  and the cluster deletion.

## Risks

- `<data_root>/runs/` is keyed by JOB id today and D1 keys it by RUN id. Every
  reader of the old shape moves in the same commit as its writer.
- `<data_root>/jobs/` holds both `<uuid>.json` files and `<16hex>/` directories.
  Any new reader of that directory must make the same file/directory
  distinction the two matchers make.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
