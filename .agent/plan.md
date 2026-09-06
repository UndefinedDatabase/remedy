# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 13 are reviewed and 2 to 13 PASSED. T001 is
CLOSED. T002 is open: the job record has MOVED, R-0814 is resolved, both
resolvers return `str`, the ping-pong run store has one spelling on both sides,
and the run-log store has one spelling on the production READ side.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store, now `<data_root>/jobs/<16hex>/job.json`, become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

ONE SPELLING FOR THE RUN-LOG JOIN. `RunLogWriter.__init__` still joins
`root / self._job_id` onto a runs BASE it is handed — the last production
hand-spelling of the job-keyed layout. It takes a DATA root instead and builds
its directory with `data_paths.run_log_dir`. Eight production call sites and
three test files move with it.

## Next Steps

- THE RE-KEY ITSELF: `run_log_dir` and `pingpong_run_dir` collapse onto
  `run_dir`, keyed by RUN id — DECISION F260 D1. `RunLogWriter` already mints a
  run id, so the writer side is short; the READER side needs a job to name its
  runs, which makes the step below its prerequisite.
- `Job.run_refs`, the plural run list D1 names and nothing on disk carries yet:
  no reader can find a job's runs once `<data_root>/runs/` is keyed by run id.
- The rest of T002: the unified record's own administrative fields — measured at
  `4f265f91`, eight of D1's eleven have no counterpart in `JobPlan` — and the
  Mission extension.
- Then T003 consumer by consumer; T004 the classic runner, the classic store and
  the resolver collapse together (DECISION F260 D5); T005 the reachability test
  and the cluster deletion.

## Risks

- The test side of the run-log spelling is DECLINED, not forgotten: DECISION
  F260 D6 records why, and the re-key inherits those sites.
- The soft limit is 25 rounds or 7 sessions. This is round 14 of session 5 and
  the remaining scope is larger than the rounds left, so split-and-close is the
  likely endgame and each round leaves a self-consistent tree.
