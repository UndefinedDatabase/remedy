# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 11 are reviewed and 2 to 11 PASSED. T001 is
CLOSED. T002 is open: the job record has MOVED, R-0814 is resolved, both
resolvers return `str`, and the run store has one spelling.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store, now `<data_root>/jobs/<16hex>/job.json`, become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

THE TEST SIDE OF THE ONE SPELLING. Round 11 moved every `_pingpong_runs_dir`
reference onto `data_paths.pingpong_runs_dir` / `pingpong_run_dir` and left
fourteen hand-spelled `"pingpong_runs"` path components in seven test files,
which never named the deleted helper and so were invisible to that sweep. They
are the test-side twin of R-0814 — a path built by hand does not follow its
writer — and this round moves them onto the pair.

## Next Steps

- THE RUN MOVE, which needs its own session: `pingpong_runs_dir` and
  `pingpong_run_dir` collapse into `runs_dir` and `run_dir`, AND the run LOG at
  `<data_root>/runs/<job_id>/` must move to the run id in the SAME commit, or
  `timeline.load_run_events` reads one directory keyed two ways — DECISION F260
  D0 measured that collision. It needs a fresh reading of `run_log.py` and
  `timeline.py`, which no round so far has touched.
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
