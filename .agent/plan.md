# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 14 are reviewed and 2 to 14 PASSED. T001 is
CLOSED. T002 is open: the job record has MOVED, R-0814 is resolved, both
resolvers return `str`, the ping-pong run store has one spelling on both sides,
and the run-log store has one spelling on the whole production side.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store, now `<data_root>/jobs/<16hex>/job.json`, become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

ONE RUN PER INVOCATION. `timeline.append_run_event` mints a new run id on every
call, so five events of one resume become five runs in five files — measured on
the shipped function. The module takes ONE run id for the life of the process
and passes it, which is what `RunLogWriter`'s docstring already promises. This
is registered as finding R-0816 and ruled by DECISION F260 D7.

## Next Steps

- `Job.run_refs`, the plural run list D1 names and nothing on disk carries yet.
  It is meaningful only once a run is an invocation rather than an event, which
  is what this round buys.
- THE RE-KEY ITSELF: `run_log_dir` and `pingpong_run_dir` collapse onto
  `run_dir`, keyed by RUN id — DECISION F260 D1. The reader side needs a job to
  name its runs, so `run_refs` above is its prerequisite.
- The rest of T002: the unified record's own administrative fields — eight of
  D1's eleven have no counterpart in `JobPlan` — and the Mission extension.
- Then T003 consumer by consumer; T004 the classic runner, the classic store and
  the resolver collapse together (DECISION F260 D5); T005 the reachability test
  and the cluster deletion.

## Risks

- The test side of the run-log spelling is DECLINED, not forgotten: DECISION
  F260 D6 records why, and the re-key inherits those sites.
- The soft limit is 25 rounds or 7 sessions. This is round 15 of session 6, so
  the SESSION limit is reached next session and split-and-close is the endgame.
  Every round leaves a self-consistent tree so that close is available at any
  point.
